#!/usr/bin/env python3
"""Check daily candle coverage to identify gaps"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.bot_db_ohlcv import db_ohlcv

# Query to get daily counts
sql = """
    SELECT 
        DATE(start_dttm) as trade_date,
        COUNT(*) as candle_count,
        MIN(start_dttm) as first_candle,
        MAX(start_dttm) as last_candle,
        CASE 
            WHEN COUNT(*) = 1440 THEN 'COMPLETE'
            WHEN COUNT(*) > 1300 THEN 'MOSTLY'
            WHEN COUNT(*) > 0 THEN 'PARTIAL'
            ELSE 'EMPTY'
        END as status
    FROM ohlcv_BTC_USDC 
    WHERE freq='1min'
    GROUP BY DATE(start_dttm)
    ORDER BY trade_date DESC
    LIMIT 100
"""

print("=" * 120)
print("DAILY BTC-USDC CANDLE COVERAGE (Most Recent 100 Days)")
print("=" * 120)
print(f"{'Date':<12} {'Candles':<10} {'Expected':<10} {'Status':<10} {'% Complete':<12} {'First Candle':<20} {'Last Candle':<20}")
print("-" * 120)

result = db_ohlcv.seld(sql)
if result:
    results = result if isinstance(result, list) else [result]
    
    complete_days = 0
    partial_days = 0
    
    for row in results:
        date = str(row['trade_date'])
        count = row['candle_count']
        first = str(row['first_candle'])
        last = str(row['last_candle'])
        status = row['status']
        
        # Calculate percentage
        pct = (count / 1440.0) * 100
        
        # Color code the status
        if status == 'COMPLETE':
            status_display = f"{status} OK"
            complete_days += 1
        elif status == 'MOSTLY':
            status_display = f"{status} OK"
            complete_days += 1
        else:
            status_display = f"{status}"
            partial_days += 1
        
        print(f"{date:<12} {count:<10,} {'1440':<10} {status_display:<10} {pct:>5.1f}%       {first:<20} {last:<20}")
    
    print("-" * 120)
    print(f"\nSummary: {complete_days} complete/mostly complete days, {partial_days} partial days")

# Now show the full date range
print("\n" + "=" * 120)
print("FULL DATE RANGE COVERAGE")
print("=" * 120)

sql_range = """
    SELECT 
        MIN(DATE(start_dttm)) as earliest_date,
        MAX(DATE(start_dttm)) as latest_date,
        COUNT(DISTINCT DATE(start_dttm)) as total_days,
        COUNT(*) as total_candles
    FROM ohlcv_BTC_USDC 
    WHERE freq='1min'
"""

result = db_ohlcv.seld(sql_range)
if result:
    r = result[0] if isinstance(result, list) else result
    print(f"Earliest Date: {r['earliest_date']}")
    print(f"Latest Date: {r['latest_date']}")
    print(f"Total Days with Data: {r['total_days']:,}")
    print(f"Total Candles: {r['total_candles']:,}")
    print(f"Expected Candles (for {r['total_days']:,} days): {r['total_days'] * 1440:,}")
    print(f"Average Candles/Day: {r['total_candles'] / r['total_days']:.0f}")

print("=" * 120)
print("\nNOTE: Each day should have 1,440 candles (24 hours × 60 minutes)")
print("      COMPLETE = 1,440 candles | MOSTLY = 1,300+ candles | PARTIAL = <1,300 candles")
print("=" * 120)
