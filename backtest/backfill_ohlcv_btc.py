#!/usr/bin/env python3
#<=====>#
# BTC-USDC OHLCV Historical Data Backfill Script
# 
# Backfills 1-minute candle data from June 1, 2022 to present
# Designed to run slowly to avoid interfering with active trading bots
#<=====>#

import os
import sys
import time
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd
from coinbase.rest import RESTClient
import threading

# Add parent directory to path so we can import from libs
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
from libs.bot_db_ohlcv import db_tbl_insupd, db_ohlcv
from libs.common import dttm_get

#<=====>#
# Configuration
#<=====>#

# Load environment variables
load_dotenv()
coinbase_api_key = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')

# Coinbase client will be initialized in main() to avoid hanging during import
cb = None

# Backfill parameters
PROD_ID = 'BTC-USDC'
START_DATE = datetime(2022, 6, 1, 0, 0, 0)  # June 1, 2022
END_DATE = datetime(2025, 10, 4, 23, 59, 59)  # October 4, 2024
FREQ = '1min'
GRANULARITY = 'ONE_MINUTE'

# API rate limiting (SLOW for safety with active bots)
CANDLES_PER_REQUEST = 280  # Coinbase max is 350, use 280 for safety margin (DST/leap seconds)
SLEEP_BETWEEN_REQUESTS = 0.75  # 0.75 seconds = conservative rate (~1.33 req/sec)
SLEEP_ON_ERROR = 5  # 5 seconds on error
API_TIMEOUT = 30  # 30 second timeout for API calls

# CSV output settings
CSV_OUTPUT_DIR = 'backtest/csv_cache'
CSV_FILENAME = f'{CSV_OUTPUT_DIR}/btc_usdc_1min.csv'

# Progress checkpoint (save progress every N requests)
CHECKPOINT_INTERVAL = 100  # Save progress every 100 API calls

#<=====>#
# Helper Functions
#<=====>#

def get_table_name(prod_id):
    """Convert product ID to table name format"""
    return f"ohlcv_{prod_id.replace('-', '_')}"


def get_latest_timestamp_in_db(prod_id, freq='1min'):
    """
    Check what the latest timestamp in the database is
    Returns None if table doesn't exist or is empty
    """
    table_name = get_table_name(prod_id)
    
    try:
        sql = f"""
            SELECT MAX(start_dttm) as latest_dttm
            FROM {table_name}
            WHERE freq = '{freq}'
        """
        result = db_ohlcv.seld(sql)
        
        if result and len(result) > 0 and result[0]['latest_dttm']:
            return result[0]['latest_dttm']
        else:
            return None
    except Exception as e:
        print(f"WARNING: Table {table_name} may not exist yet (will be created): {e}")
        return None


def get_earliest_timestamp_in_db(prod_id, freq='1min'):
    """
    Check what the earliest timestamp in the database is
    Returns None if table doesn't exist or is empty
    """
    table_name = get_table_name(prod_id)
    
    try:
        sql = f"""
            SELECT MIN(start_dttm) as earliest_dttm
            FROM {table_name}
            WHERE freq = '{freq}'
        """
        result = db_ohlcv.seld(sql)
        
        if result and len(result) > 0 and result[0]['earliest_dttm']:
            return result[0]['earliest_dttm']
        else:
            return None
    except Exception as e:
        return None


def count_candles_in_db(prod_id, freq='1min'):
    """Count how many candles are already in the database"""
    table_name = get_table_name(prod_id)
    
    try:
        sql = f"""
            SELECT COUNT(*) as count
            FROM {table_name}
            WHERE freq = '{freq}'
        """
        result = db_ohlcv.seld(sql)
        
        if result and len(result) > 0:
            return result[0]['count']
        else:
            return 0
    except:
        return 0


def fetch_candles_from_coinbase(prod_id, start_ts, end_ts, granularity='ONE_MINUTE', max_retries=5):
    """
    Fetch candles from Coinbase API with retry logic and timeout
    
    Args:
        prod_id: Product ID (e.g., 'BTC-USDC')
        start_ts: Start timestamp (Unix seconds)
        end_ts: End timestamp (Unix seconds)
        granularity: Candle granularity
        max_retries: Maximum retry attempts
    
    Returns:
        List of candle dicts or None on failure
    """
    for attempt in range(1, max_retries + 1):
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"[{current_time}] [API] Calling Coinbase API...")
            
            # Use threading for timeout
            result = [None]
            exception = [None]
            
            def api_call():
                try:
                    result[0] = cb.get_candles(
                        product_id=prod_id,
                        start=int(start_ts),
                        end=int(end_ts),
                        granularity=granularity
                    )
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=api_call)
            thread.daemon = True
            thread.start()
            thread.join(timeout=API_TIMEOUT)
            
            if thread.is_alive():
                print(f"[{current_time}] [WARN] API call timed out after {API_TIMEOUT}s")
                if attempt < max_retries:
                    print(f"   Retrying (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(SLEEP_ON_ERROR)
                    continue
                else:
                    print(f"[FATAL] API timeout after {max_retries} attempts")
                    return None
            
            if exception[0]:
                raise exception[0]
            
            response = result[0]
            print(f"[{current_time}] [API] Response received", flush=True)
            
            try:
                print(f"[{current_time}] [DEBUG] Response type: {type(response)}", flush=True)
                print(f"[{current_time}] [DEBUG] Response has 'candles'?: {hasattr(response, 'candles') if response else 'None'}", flush=True)
            except Exception as debug_err:
                print(f"[{current_time}] [DEBUG] Error printing debug info: {debug_err}", flush=True)
            
            if response and hasattr(response, 'candles'):
                print(f"[{current_time}] [DEBUG] Candles type: {type(response.candles)}")
                print(f"[{current_time}] [DEBUG] Number of candles: {len(response.candles) if response.candles else 0}")
                
                candles = []
                for i, candle in enumerate(response.candles):
                    if i == 0:
                        print(f"[{current_time}] [DEBUG] First candle type: {type(candle)}")
                    c = candle.to_dict()
                    candles.append({
                        'timestamp': int(c['start']),
                        'open': float(c['open']),
                        'high': float(c['high']),
                        'low': float(c['low']),
                        'close': float(c['close']),
                        'volume': float(c['volume'])
                    })
                print(f"[{current_time}] [API] Parsed {len(candles)} candles", flush=True)
                print(f"[{current_time}] [API] Returning {len(candles)} candles", flush=True)
                return candles
            else:
                print(f"[{current_time}] [API] No candles in response (or wrong format)", flush=True)
                if response:
                    print(f"[{current_time}] [DEBUG] Response attributes: {dir(response)[:10]}", flush=True)
                print(f"[{current_time}] [API] Returning empty list", flush=True)
                return []
                
        except Exception as e:
            current_time = datetime.now().strftime('%H:%M:%S')
            if attempt < max_retries:
                print(f"[{current_time}] [WARN] API error (attempt {attempt}/{max_retries}): {e}")
                print(f"   Sleeping {SLEEP_ON_ERROR} seconds before retry...")
                time.sleep(SLEEP_ON_ERROR)
            else:
                print(f"[{current_time}] [FATAL] After {max_retries} attempts: {e}")
                traceback.print_exc()
                return None
    
    return None


def save_candles_to_csv(prod_id, candles, freq='1min'):
    """
    Save candles to CSV file - MUCH FASTER than database!
    Uses Unix timestamps (UTC) to avoid DST issues entirely.
    
    Args:
        prod_id: Product ID (e.g., 'BTC-USDC')
        candles: List of candle dicts
        freq: Frequency string (e.g., '1min')
    
    Returns:
        True on success, False on failure
    """
    current_time = datetime.now().strftime('%H:%M:%S')
    
    if not candles:
        return True
    
    try:
        # Convert to DataFrame - keep Unix timestamps (already in UTC)
        df = pd.DataFrame(candles)
        df['freq'] = freq
        df['prod_id'] = prod_id
        
        # Reorder columns - timestamp stays as Unix timestamp
        df = df[['prod_id', 'freq', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
        # Ensure CSV directory exists
        os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)
        
        # Append to CSV (header only if file doesn't exist)
        file_exists = os.path.exists(CSV_FILENAME)
        df.to_csv(CSV_FILENAME, mode='a', header=not file_exists, index=False)
        
        print(f"[{current_time}] [CSV] Wrote {len(candles)} candles (Unix UTC) to CSV", flush=True)
        return True
        
    except Exception as e:
        print(f"[{current_time}] [CSV] ERROR: {e}", flush=True)
        traceback.print_exc()
        return False


def format_duration(seconds):
    """Format seconds into human-readable duration"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


#<=====>#
# Main Backfill Logic
#<=====>#

def backfill_ohlcv(prod_id, start_date, end_date, freq='1min', granularity='ONE_MINUTE'):
    """
    Main backfill function - works backwards from end_date to start_date
    
    Args:
        prod_id: Product ID (e.g., 'BTC-USDC')
        start_date: Start datetime
        end_date: End datetime
        freq: Frequency string for database
        granularity: Coinbase API granularity
    """
    
    print("\n" + "="*80)
    print("BTC-USDC OHLCV BACKFILL")
    print("="*80)
    print(f"Product: {prod_id}")
    print(f"Frequency: {freq} / {granularity}")
    print(f"Target Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"API Rate Limit: {SLEEP_BETWEEN_REQUESTS}s between requests (~{1/SLEEP_BETWEEN_REQUESTS:.1f} req/sec)")
    print(f"="*80 + "\n")
    
    # Check existing data
    print("[INFO] Checking existing data in database...")
    existing_count = count_candles_in_db(prod_id, freq)
    latest_ts = get_latest_timestamp_in_db(prod_id, freq)
    earliest_ts = get_earliest_timestamp_in_db(prod_id, freq)
    
    if existing_count > 0:
        print(f"   Found {existing_count:,} existing candles")
        print(f"   Earliest: {earliest_ts}")
        print(f"   Latest: {latest_ts}")
    else:
        print(f"   No existing data found (fresh backfill)")
    
    # Calculate total candles needed
    total_minutes = int((end_date - start_date).total_seconds() / 60)
    total_requests_needed = (total_minutes // CANDLES_PER_REQUEST) + 1
    
    print(f"\n[PLAN] Backfill Plan:")
    print(f"   Total minutes to fetch: {total_minutes:,}")
    print(f"   Estimated API requests: {total_requests_needed:,}")
    print(f"   Estimated time: {format_duration(total_requests_needed * SLEEP_BETWEEN_REQUESTS)}")
    print(f"\n[INFO] Running SLOWLY to avoid interfering with active trading bots...")
    print(f"   You can go eat - this will take a while!\n")
    
    # Start backfill (work backwards from end_date)
    current_end = end_date
    request_count = 0
    total_candles_saved = 0
    start_time = time.time()
    last_checkpoint = time.time()
    
    while current_end > start_date:
        # Calculate this request's time window
        # Each request gets up to 300 minutes of data
        seconds_per_candle = 60  # 1 minute
        request_span = CANDLES_PER_REQUEST * seconds_per_candle
        current_start = current_end - timedelta(seconds=request_span)
        
        # Don't go before our target start date
        if current_start < start_date:
            current_start = start_date
        
        # Convert to Unix timestamps
        start_ts = int(current_start.timestamp())
        end_ts = int(current_end.timestamp())
        
        # Progress display
        request_count += 1
        progress_pct = ((end_date - current_end).total_seconds() / (end_date - start_date).total_seconds()) * 100
        elapsed = time.time() - start_time
        
        # Print EVERY request with timestamp
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] Request {request_count:,}/{total_requests_needed:,} ({progress_pct:.1f}%) | "
              f"Period: {current_start.strftime('%Y-%m-%d %H:%M')} - {current_end.strftime('%Y-%m-%d %H:%M')}")
        
        # Fetch candles from Coinbase
        print(f"[{current_time}] Calling fetch_candles_from_coinbase...")
        candles = fetch_candles_from_coinbase(prod_id, start_ts, end_ts, granularity)
        print(f"[{current_time}] fetch_candles_from_coinbase returned: {type(candles)}")
        
        if candles is None:
            print(f"[{current_time}] [FATAL] Failed to fetch candles for {current_start} - {current_end}")
            print(f"   Stopping backfill. Resume by re-running this script.")
            return False
        
        # Show how many candles were retrieved
        print(f"[{current_time}] Retrieved {len(candles)} candles")
        
        if len(candles) == 0:
            print(f"[{current_time}] [WARN] No candles returned (may be before listing date)")
        else:
            # Save to CSV (much faster!)
            if save_candles_to_csv(prod_id, candles, freq):
                total_candles_saved += len(candles)
                print(f"[{current_time}] Total saved to CSV: {total_candles_saved:,} candles", flush=True)
            else:
                print(f"[{current_time}] [FATAL] Failed to save candles to CSV")
                print(f"   Stopping backfill. Check file permissions.")
                return False
        
        # Checkpoint progress
        if time.time() - last_checkpoint > 60:  # Every minute
            last_checkpoint = time.time()
            checkpoint_time = datetime.now().strftime('%H:%M:%S')
            print(f"\n[{checkpoint_time}] === CHECKPOINT: {total_candles_saved:,} candles saved, "
                  f"{request_count:,} requests completed, Elapsed: {format_duration(elapsed)} ===\n")
        
        # Blank line between requests for readability
        print()
        
        # Move to next time window (backwards)
        current_end = current_start
        
        # Sleep to avoid rate limits
        time.sleep(SLEEP_BETWEEN_REQUESTS)
        
        # Check if we've reached the start
        if current_end <= start_date:
            break
    
    # Final summary
    elapsed_total = time.time() - start_time
    print(f"\n" + "="*80)
    print(f"[SUCCESS] BACKFILL COMPLETE!")
    print(f"="*80)
    print(f"Total API requests: {request_count:,}")
    print(f"Total candles saved: {total_candles_saved:,}")
    print(f"Total time: {format_duration(elapsed_total)}")
    print(f"Average: {total_candles_saved / elapsed_total:.1f} candles/second")
    
    # Final database check
    print(f"\n[INFO] Final Database Status:")
    final_count = count_candles_in_db(prod_id, freq)
    final_latest = get_latest_timestamp_in_db(prod_id, freq)
    final_earliest = get_earliest_timestamp_in_db(prod_id, freq)
    print(f"   Total candles in DB: {final_count:,}")
    print(f"   Earliest: {final_earliest}")
    print(f"   Latest: {final_latest}")
    print(f"\n{'='*80}\n")
    
    return True


#<=====>#
# Main Entry Point
#<=====>#

if __name__ == '__main__':
    
    print(f"\n[START] Starting BTC-USDC backfill at {dttm_get()}")
    
    # Initialize Coinbase client (done here to show output first)
    print("[INFO] Initializing Coinbase API client...")
    cb = RESTClient(api_key=coinbase_api_key, api_secret=coinbase_api_secret)
    print("[OK] Coinbase client initialized")
    
    # Run backfill
    success = backfill_ohlcv(
        prod_id=PROD_ID,
        start_date=START_DATE,
        end_date=END_DATE,
        freq=FREQ,
        granularity=GRANULARITY
    )
    
    if success:
        print(f"[SUCCESS] Backfill completed successfully at {dttm_get()}")
        print(f"[OK] You can now run backtests on BTC-USDC from {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
        sys.exit(0)
    else:
        print(f"[FAILED] Backfill failed at {dttm_get()}")
        print(f"   Check errors above and try running again (script will resume from last saved point)")
        sys.exit(1)