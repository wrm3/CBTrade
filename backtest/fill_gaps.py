#!/usr/bin/env python3
"""Fill gaps in existing OHLCV data - targets partial days"""

import os
import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.bot_db_ohlcv import db_ohlcv, db_tbl_insupd
from libs.common import dttm_get
from coinbase.rest import RESTClient
import pandas as pd
import threading

# Load environment
load_dotenv()
cb = RESTClient(
    api_key=os.getenv('COINBASE_API_KEY'),
    api_secret=os.getenv('COINBASE_API_SECRET')
)

PROD_ID = 'BTC-USDC'
FREQ = '1min'
GRANULARITY = 'ONE_MINUTE'
API_TIMEOUT = 30
SLEEP_BETWEEN_REQUESTS = 0.75

def get_table_name(prod_id):
    """Convert product ID to table name format"""
    return f"ohlcv_{prod_id.replace('-', '_')}"

def find_partial_days(prod_id, freq='1min', min_threshold=1300):
    """
    Find days with partial data (less than 1440 candles)
    
    Args:
        prod_id: Product ID
        freq: Frequency
        min_threshold: Only flag days with less than this many candles
        
    Returns:
        List of dates that need filling
    """
    table_name = get_table_name(prod_id)
    
    sql = f"""
        SELECT 
            DATE(start_dttm) as trade_date,
            COUNT(*) as candle_count,
            MIN(start_dttm) as first_candle,
            MAX(start_dttm) as last_candle
        FROM {table_name}
        WHERE freq = '{freq}'
        GROUP BY DATE(start_dttm)
        HAVING COUNT(*) < {min_threshold}
        ORDER BY trade_date DESC
    """
    
    result = db_ohlcv.seld(sql)
    return result if isinstance(result, list) else ([result] if result else [])

def fetch_day_candles(prod_id, date, granularity='ONE_MINUTE'):
    """
    Fetch all candles for a specific day (in chunks to avoid 350 limit)
    
    Args:
        prod_id: Product ID
        date: Date object or string (YYYY-MM-DD)
        granularity: Candle granularity
        
    Returns:
        List of candle dicts or None on failure
    """
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=0)
    
    # Break into 6-hour chunks (360 minutes each = under 350 limit)
    all_candles = []
    chunk_hours = 6
    current_start = start_of_day
    
    print(f"  Fetching day {date.strftime('%Y-%m-%d')} in {24//chunk_hours} chunks...")
    
    while current_start < end_of_day:
        current_end = current_start + timedelta(hours=chunk_hours) - timedelta(seconds=1)
        if current_end > end_of_day:
            current_end = end_of_day
        
        start_ts = int(current_start.timestamp())
        end_ts = int(current_end.timestamp())
        
        # Fetch candles with timeout
        result = [None]
        exception = [None]
        
        def api_call():
            try:
                result[0] = cb.get_candles(
                    product_id=prod_id,
                    start=start_ts,
                    end=end_ts,
                    granularity=granularity
                )
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=api_call)
        thread.daemon = True
        thread.start()
        thread.join(timeout=API_TIMEOUT)
        
        if thread.is_alive():
            print(f"    [WARN] API timeout for chunk {current_start.strftime('%H:%M')}-{current_end.strftime('%H:%M')}")
            return None
        
        if exception[0]:
            print(f"    [ERROR] {exception[0]}")
            return None
        
        response = result[0]
        
        if response and hasattr(response, 'candles'):
            for candle in response.candles:
                c = candle.to_dict()
                all_candles.append({
                    'timestamp': int(c['start']),
                    'open': float(c['open']),
                    'high': float(c['high']),
                    'low': float(c['low']),
                    'close': float(c['close']),
                    'volume': float(c['volume'])
                })
        
        # Move to next chunk
        current_start = current_end + timedelta(seconds=1)
        
        # Small sleep between chunks
        if current_start < end_of_day:
            time.sleep(0.5)
    
    return all_candles

def save_candles_to_db(prod_id, candles, freq='1min'):
    """Save candles to database"""
    if not candles:
        return True
    
    df = pd.DataFrame(candles)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)
    df = df.sort_index()
    
    df['freq'] = freq
    df['start_dttm'] = df.index
    df['end_dttm'] = df['start_dttm'] + timedelta(seconds=59)
    
    data = df.reset_index().to_dict(orient='records')
    table_name = get_table_name(prod_id)
    
    try:
        db_tbl_insupd(table_name, data, exit_on_error=False)
        return True
    except Exception as e:
        print(f"  [ERROR] Database: {e}")
        return False

def fill_gaps(prod_id, freq='1min', skip_recent_days=2):
    """
    Fill gaps in existing data
    
    Args:
        prod_id: Product ID
        freq: Frequency
        skip_recent_days: Skip this many recent days (they're being filled by live bots)
    """
    print("=" * 80)
    print("GAP FILLING FOR BTC-USDC")
    print("=" * 80)
    print(f"Product: {prod_id}")
    print(f"Frequency: {freq}")
    print(f"Skipping last {skip_recent_days} days (live bot data)")
    print("=" * 80)
    print()
    
    # Find partial days
    print("[INFO] Scanning for partial days...")
    partial_days = find_partial_days(prod_id, freq)
    
    if not partial_days:
        print("[OK] No partial days found - all data is complete!")
        return True
    
    # Filter out recent days (being filled by live bots)
    cutoff_date = (datetime.now() - timedelta(days=skip_recent_days)).date()
    days_to_fill = [
        day for day in partial_days 
        if datetime.strptime(str(day['trade_date']), '%Y-%m-%d').date() < cutoff_date
    ]
    
    if not days_to_fill:
        print(f"[OK] Found {len(partial_days)} partial days, but they're all within the last {skip_recent_days} days")
        print("     These will be filled naturally by your running bots.")
        return True
    
    print(f"[INFO] Found {len(days_to_fill)} partial days to fill (excluding recent {skip_recent_days} days)")
    print()
    
    # Show what we'll fill
    print("Days to fill:")
    for day in days_to_fill:
        print(f"  {day['trade_date']}: {day['candle_count']:,}/1,440 candles ({(day['candle_count']/1440)*100:.1f}%)")
    print()
    
    # Fill each day
    filled = 0
    failed = 0
    
    for i, day in enumerate(days_to_fill, 1):
        date_str = str(day['trade_date'])
        existing = day['candle_count']
        
        print(f"[{i}/{len(days_to_fill)}] Filling {date_str} (currently {existing:,}/1,440 candles)...")
        
        # Fetch full day
        candles = fetch_day_candles(prod_id, date_str, GRANULARITY)
        
        if candles is None:
            print(f"  [FAILED] Could not fetch data")
            failed += 1
            continue
        
        if len(candles) == 0:
            print(f"  [WARN] No candles returned (may be before BTC listing)")
            continue
        
        print(f"  Retrieved {len(candles):,} candles")
        
        # Save to database
        if save_candles_to_db(prod_id, candles, freq):
            filled += 1
            print(f"  [OK] Saved to database")
        else:
            failed += 1
            print(f"  [FAILED] Could not save to database")
        
        # Rate limit
        if i < len(days_to_fill):
            time.sleep(SLEEP_BETWEEN_REQUESTS)
        
        print()
    
    # Summary
    print("=" * 80)
    print("GAP FILLING SUMMARY")
    print("=" * 80)
    print(f"Days processed: {len(days_to_fill)}")
    print(f"Successfully filled: {filled}")
    print(f"Failed: {failed}")
    print("=" * 80)
    
    return failed == 0

if __name__ == '__main__':
    print(f"\n[START] Gap filling started at {dttm_get()}\n")
    
    success = fill_gaps(
        prod_id=PROD_ID,
        freq=FREQ,
        skip_recent_days=2  # Skip last 2 days (live bot data)
    )
    
    if success:
        print(f"\n[SUCCESS] Gap filling completed at {dttm_get()}")
        sys.exit(0)
    else:
        print(f"\n[FAILED] Gap filling completed with errors at {dttm_get()}")
        sys.exit(1)
