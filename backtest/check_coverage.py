#!/usr/bin/env python3
"""Quick script to check BTC-USDC data coverage"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.bot_db_ohlcv import db_ohlcv
from datetime import datetime, timedelta

# Check what we have
sql = """
    SELECT 
        COUNT(*) as count,
        MIN(start_dttm) as earliest,
        MAX(start_dttm) as latest
    FROM ohlcv_BTC_USDC 
    WHERE freq='1min'
"""

result = db_ohlcv.seld(sql)
if result:
    r = result[0] if isinstance(result, list) else result
    
    print("=" * 80)
    print("BTC-USDC DATA COVERAGE")
    print("=" * 80)
    print(f"Total Candles Saved: {r['count']:,}")
    print(f"Earliest Date: {r['earliest']}")
    print(f"Latest Date: {r['latest']}")
    print()
    
    # Calculate coverage
    target_start = datetime(2022, 6, 1, 0, 0, 0)
    target_end = datetime(2024, 10, 4, 23, 59, 59)
    
    earliest = datetime.fromisoformat(str(r['earliest']))
    latest = datetime.fromisoformat(str(r['latest']))
    
    total_minutes_needed = int((target_end - target_start).total_seconds() / 60)
    coverage_pct = (r['count'] / total_minutes_needed) * 100
    
    print(f"Target Period: {target_start.strftime('%Y-%m-%d')} to {target_end.strftime('%Y-%m-%d')}")
    print(f"Total Minutes Needed: {total_minutes_needed:,}")
    print(f"Coverage: {coverage_pct:.1f}%")
    print()
    
    # What's missing
    if earliest > target_start:
        missing_start = int((earliest - target_start).total_seconds() / 60)
        print(f"[MISSING] {missing_start:,} minutes at the START ({target_start} to {earliest})")
    
    if latest < target_end:
        missing_end = int((target_end - latest).total_seconds() / 60)
        print(f"[MISSING] {missing_end:,} minutes at the END ({latest} to {target_end})")
    
    print()
    print("=" * 80)
    print("RESUME STRATEGY")
    print("=" * 80)
    print("The backfill script will automatically:")
    print("1. Detect existing data range")
    print("2. Fill in missing data at the beginning (older history)")
    print("3. Skip duplicate time periods")
    print()
    print("Just run: python backtest/backfill_ohlcv_btc.py")
    print("=" * 80)

else:
    print("No data found in ohlcv_BTC_USDC table")
