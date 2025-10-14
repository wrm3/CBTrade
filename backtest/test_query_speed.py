#!/usr/bin/env python3
"""Test the speed of the existence check query"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.bot_db_ohlcv import db_ohlcv

# Test query with 3 timestamps
print("Testing query speed with 3 timestamps...")
start = time.time()
result = db_ohlcv.seld("""
    SELECT start_dttm 
    FROM ohlcv_BTC_USDC 
    WHERE freq='1min' 
    AND start_dttm IN ('2025-08-11 22:39:00', '2025-08-11 22:40:00', '2025-08-11 22:41:00')
""")
elapsed = time.time() - start
print(f"Query with 3 timestamps took {elapsed:.3f} seconds")
print(f"Returned {len(result) if result else 0} rows")

# Test query with 280 timestamps (full batch)
print("\nTesting query speed with 280 timestamps...")
timestamps = [f"'2025-08-11 {h:02d}:{m:02d}:00'" for h in range(12, 24) for m in range(0, 60)][:280]
ts_list = ",".join(timestamps)

start = time.time()
result = db_ohlcv.seld(f"""
    SELECT start_dttm 
    FROM ohlcv_BTC_USDC 
    WHERE freq='1min' 
    AND start_dttm IN ({ts_list})
""")
elapsed = time.time() - start
print(f"Query with 280 timestamps took {elapsed:.3f} seconds")
print(f"Returned {len(result) if result else 0} rows")

# Check if there's an index
print("\nChecking table indexes...")
indexes = db_ohlcv.seld("SHOW INDEX FROM ohlcv_BTC_USDC")
if indexes:
    for idx in indexes:
        print(f"Index: {idx['Key_name']} on {idx['Column_name']} (type: {idx['Index_type']})")
else:
    print("No indexes found!")
