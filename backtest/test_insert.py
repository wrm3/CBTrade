#!/usr/bin/env python3
"""Test what's happening with the insert"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.bot_db_ohlcv import db_ohlcv
from datetime import datetime, timedelta
import pandas as pd

# Create a test candle
test_candle = {
    'timestamp': int(datetime(2025, 1, 1, 12, 0, 0).timestamp()),
    'open': 50000.0,
    'high': 50100.0,
    'low': 49900.0,
    'close': 50050.0,
    'volume': 123.45
}

# Convert to DataFrame (same as backfill script)
df = pd.DataFrame([test_candle])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
df.set_index('timestamp', inplace=True)

# Add freq and time columns
df['freq'] = '1min'
df['start_dttm'] = df.index
df['end_dttm'] = df['start_dttm'] + timedelta(seconds=59)

# Convert to dict (same as backfill script)
data = df.reset_index().to_dict(orient='records')

print("Data after reset_index():")
print(f"Number of records: {len(data)}")
print(f"Keys in first record: {list(data[0].keys())}")
print(f"\nFirst record:")
for k, v in data[0].items():
    print(f"  {k}: {v} (type: {type(v).__name__})")

# Try to build the INSERT like the backfill script does
cols = list(data[0].keys())
print(f"\nColumns before removing timestamp: {cols}")

if 'timestamp' in cols:
    cols.remove('timestamp')
    print(f"Columns after removing timestamp: {cols}")

# Check what the actual table columns are
print("\nActual table columns:")
table_cols = db_ohlcv.table_cols(table='ohlcv_BTC_USDC')
print(f"Table columns: {table_cols}")

# Check which columns match
print("\nColumn matching:")
for col in cols:
    if col in table_cols:
        print(f"  ✓ {col} - exists in table")
    else:
        print(f"  ✗ {col} - NOT in table!")
