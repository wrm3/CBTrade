#!/usr/bin/env python3
"""
Bulk load CSV data into database - MUCH faster than incremental inserts!
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.bot_db_ohlcv import db_ohlcv, db_tbl_insupd
from libs.common import dttm_get
import pandas as pd
from datetime import timedelta

CSV_FILE = 'backtest/csv_cache/btc_usdc_1min.csv'
BATCH_SIZE = 10000  # Load 10,000 rows at a time
PROD_ID = 'BTC-USDC'

def get_table_name(prod_id):
    """Convert product ID to table name format"""
    return f"ohlcv_{prod_id.replace('-', '_')}"

def load_csv_to_database():
    """
    Load CSV file into database in large batches
    """
    print(f"[START] Loading CSV to database at {dttm_get()}")
    print(f"CSV File: {CSV_FILE}")
    
    if not os.path.exists(CSV_FILE):
        print(f"[ERROR] CSV file not found: {CSV_FILE}")
        return False
    
    # Check file size
    file_size = os.path.getsize(CSV_FILE) / (1024 * 1024)  # MB
    print(f"CSV Size: {file_size:.1f} MB")
    
    # Count lines
    print("[INFO] Counting rows in CSV...")
    with open(CSV_FILE, 'r') as f:
        total_rows = sum(1 for line in f) - 1  # Subtract header
    print(f"Total rows: {total_rows:,}")
    
    # Load and process in chunks
    print(f"[INFO] Loading in batches of {BATCH_SIZE:,} rows...")
    
    table_name = get_table_name(PROD_ID)
    total_inserted = 0
    total_skipped = 0
    start_time = time.time()
    
    for chunk_num, chunk in enumerate(pd.read_csv(CSV_FILE, chunksize=BATCH_SIZE), 1):
        chunk_start = time.time()
        
        # Prepare data for database
        # Parse datetime strings as UTC to avoid DST issues
        chunk['start_dttm'] = pd.to_datetime(chunk['timestamp'], utc=True).dt.tz_localize(None)
        chunk['end_dttm'] = chunk['start_dttm'] + timedelta(seconds=59)
        
        # Timestamp field stays as UTC datetime
        chunk['timestamp'] = chunk['start_dttm']
        
        # Remove duplicates within chunk
        chunk = chunk.drop_duplicates(subset=['timestamp', 'freq'])
        
        # Convert to records
        records = chunk.to_dict(orient='records')
        
        # Check which timestamps already exist in database
        timestamps = [str(row['start_dttm']) for row in records]
        
        if timestamps:
            ts_list = "','".join(timestamps)
            check_sql = f"""
                SELECT start_dttm 
                FROM {table_name} 
                WHERE freq = '1min' 
                AND start_dttm IN ('{ts_list}')
            """
            
            existing = db_ohlcv.seld(check_sql)
            
            if existing:
                existing_set = set([str(row['start_dttm']) for row in existing])
                # Filter to only NEW records
                new_records = [r for r in records if str(r['start_dttm']) not in existing_set]
                skipped = len(records) - len(new_records)
                total_skipped += skipped
                records = new_records
                
                if skipped > 0:
                    print(f"  Chunk {chunk_num}: Skipped {skipped} existing, inserting {len(records)} new")
        
        # Insert new records
        if records:
            # Prepare for database format
            db_records = []
            for r in records:
                db_records.append({
                    'timestamp': r['start_dttm'],
                    'freq': r['freq'],
                    'open': float(r['open']),
                    'high': float(r['high']),
                    'low': float(r['low']),
                    'close': float(r['close']),
                    'volume': float(r['volume']),
                    'start_dttm': r['start_dttm'],
                    'end_dttm': r['end_dttm']
                })
            
            try:
                db_tbl_insupd(table_name, db_records, exit_on_error=False)
                total_inserted += len(records)
                
                elapsed = time.time() - chunk_start
                progress = (chunk_num * BATCH_SIZE) / total_rows * 100
                
                print(f"  Chunk {chunk_num}: Inserted {len(records):,} rows in {elapsed:.2f}s "
                      f"(Progress: {progress:.1f}%, Total: {total_inserted:,})")
                
            except Exception as e:
                error_str = str(e)
                # If it's a datetime error, give more detail
                if 'datetime' in error_str.lower() or '1292' in error_str:
                    print(f"  [ERROR] Chunk {chunk_num}: Invalid datetime detected, skipping chunk")
                    print(f"    Error: {error_str[:200]}")
                else:
                    print(f"  [ERROR] Failed to insert chunk {chunk_num}: {e}")
                    import traceback
                    traceback.print_exc()
                continue
    
    total_elapsed = time.time() - start_time
    
    print(f"\n[SUCCESS] Load completed!")
    print(f"Total inserted: {total_inserted:,} candles")
    print(f"Total skipped (duplicates): {total_skipped:,} candles")
    print(f"Total time: {total_elapsed/60:.1f} minutes")
    print(f"Rate: {total_inserted/total_elapsed:.0f} rows/second")
    
    return True

if __name__ == '__main__':
    success = load_csv_to_database()
    
    if success:
        print("\n[DONE] You can now delete the CSV file if desired")
        print(f"  rm {CSV_FILE}")
    else:
        print("\n[FAILED] Check errors above")
