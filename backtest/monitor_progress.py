#!/usr/bin/env python3
"""Monitor CSV loading progress"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libs.bot_db_ohlcv import db_ohlcv

CSV_TOTAL = 1_759_161  # Total rows in CSV
START_COUNT = 91_000   # Approximate starting count

print("Monitoring database load progress (Ctrl+C to stop)...\n")

try:
    while True:
        result = db_ohlcv.seld("SELECT COUNT(*) as cnt FROM ohlcv_BTC_USDC WHERE freq='1min'")
        current = result[0]['cnt']
        
        progress = (current / CSV_TOTAL) * 100
        loaded = current - START_COUNT
        remaining = CSV_TOTAL - current
        
        print(f"\r[{time.strftime('%H:%M:%S')}] "
              f"Current: {current:,} | "
              f"Loaded: {loaded:,} | "
              f"Remaining: {remaining:,} | "
              f"Progress: {progress:.1f}%", 
              end='', flush=True)
        
        if current >= CSV_TOTAL - 10000:  # Within 10k of completion
            print(f"\n\n✅ Load complete!")
            break
            
        time.sleep(30)  # Check every 30 seconds
        
except KeyboardInterrupt:
    print(f"\n\nMonitoring stopped. Current: {current:,} candles")

