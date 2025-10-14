# BTC-USDC OHLCV Backfill Script

## Overview

This script backfills historical 1-minute candle data for **BTC-USDC** from **June 1, 2022** to **October 4, 2024** into your OHLCV database.

**Key Features:**
- ✅ Slow API rate (0.75s between requests) to avoid interfering with active trading bots
- ✅ Automatic resume capability if interrupted
- ✅ Progress tracking and checkpoints
- ✅ Error handling and retry logic
- ✅ Database validation

---

## Time Period Covered

```
Start: June 1, 2022 00:00:00
End:   October 4, 2024 23:59:59

Coverage:
✅ 2022 Bear Market Tail (Jun-Dec 2022)
✅ 2023 Full Recovery (All of 2023)
✅ 2024 Bull Market (Jan-Oct 2024)

Total: ~858 days (~1.2 million candles)
```

---

## What This Script Does

### 1. **Checks Existing Data**
```bash
# The script first checks what's already in the database
# If you've partially backfilled before, it will resume where it left off
```

### 2. **Fetches Historical Data**
```bash
# Works backwards from October 4, 2024 to June 1, 2022
# Fetches 300 candles per request (Coinbase max)
# ~0.75 seconds between requests (conservative rate)
```

### 3. **Saves to Database**
```bash
# Saves to: ohlcv_BTC_USDC table
# Fields: timestamp, open, high, low, close, volume, freq, start_dttm, end_dttm
```

### 4. **Progress Tracking**
```bash
# Shows progress every 10 requests
# Checkpoint every 60 seconds
# Can be interrupted (Ctrl+C) and resumed later
```

---

## Estimated Runtime

### With Conservative Settings (0.75s per request):
```
Total requests: ~4,118 API calls
Total time: ~51 minutes
Rate: ~1.33 requests/second
```

### Disk Space:
```
~1.2 million candles × ~100 bytes = ~120 MB
```

---

## How to Run

### Step 1: Ensure Active Bots are Running
```bash
# Make sure your 3 active trading bots are running
# This script is designed to NOT interfere with them
```

### Step 2: Run the Backfill Script
```bash
uv run python backfill_ohlcv_btc.py
```

### Step 3: Go Eat!
```bash
# Script will run for ~51 minutes
# You'll see progress updates every ~10 requests
# Safe to let it run in background
```

---

## What You'll See

### Initial Output:
```
================================================================================
BTC-USDC OHLCV BACKFILL
================================================================================
Product: BTC-USDC
Frequency: 1min / ONE_MINUTE
Target Period: 2022-06-01 to 2024-10-04
API Rate Limit: 0.75s between requests (~1.3 req/sec)
================================================================================

📊 Checking existing data in database...
   No existing data found (fresh backfill)

📈 Backfill Plan:
   Total minutes to fetch: 1,235,520
   Estimated API requests: 4,119
   Estimated time: 51.5m

🐌 Running SLOWLY to avoid interfering with active trading bots...
   You can go eat - this will take a while!
```

### During Execution:
```
📡 Request 10/4,119 (0.2%) | Elapsed: 7.5s | Fetching: 2024-10-04 18:00 - 2024-10-04 23:00
📡 Request 20/4,119 (0.5%) | Elapsed: 15.0s | Fetching: 2024-10-04 13:00 - 2024-10-04 18:00
📡 Request 30/4,119 (0.7%) | Elapsed: 22.5s | Fetching: 2024-10-04 08:00 - 2024-10-04 13:00
...
✅ Checkpoint: 3,000 candles saved so far
...
📡 Request 1000/4,119 (24.3%) | Elapsed: 12.5m | Fetching: 2024-09-15 10:00 - 2024-09-15 15:00
```

### Completion:
```
================================================================================
✅ BACKFILL COMPLETE!
================================================================================
Total API requests: 4,118
Total candles saved: 1,235,520
Total time: 51.5m
Average: 399.7 candles/second

📊 Final Database Status:
   Total candles in DB: 1,235,520
   Earliest: 2022-06-01 00:00:00
   Latest: 2024-10-04 23:59:00

================================================================================

🎉 Backfill completed successfully at 2024-10-04 18:45:30
✅ You can now run backtests on BTC-USDC from 2022-06-01 to 2024-10-04
```

---

## If Something Goes Wrong

### Script Interrupted (Ctrl+C):
```bash
# Just run it again:
uv run python backfill_ohlcv_btc.py

# It will check existing data and resume where it left off
```

### API Errors:
```bash
# Script has automatic retry logic (5 attempts)
# If it fails completely, it will stop and tell you
# Just re-run and it will resume
```

### Database Errors:
```bash
# Check database connectivity
# Make sure ohlcv database is accessible
# Check .env file has correct DB_OHLCV_* credentials
```

---

## After Backfill Completes

### Verify Data:
```python
# Quick verification script
from libs.bot_db_ohlcv import db_ohlcv

sql = """
    SELECT 
        MIN(start_dttm) as earliest,
        MAX(start_dttm) as latest,
        COUNT(*) as total_candles
    FROM ohlcv_BTC_USDC
    WHERE freq = '1min'
"""

result = db_ohlcv.query(sql)
print(result)

# Expected:
# earliest: 2022-06-01 00:00:00
# latest: 2024-10-04 23:59:00
# total_candles: ~1,235,520
```

### Run Backtest:
```bash
# Now you can run the backtesting system!
uv run python backtest_example.py

# Or customize the date range:
# Edit backtest_example.py to use:
# start_date = '2022-06-01'
# end_date = '2024-10-04'
```

---

## Configuration Options

### If You Want to Speed Up (Not Recommended with Active Bots):
```python
# Edit backfill_ohlcv_btc.py line 44:
SLEEP_BETWEEN_REQUESTS = 0.5  # Faster (2 req/sec) - 34 minutes total

# Or even faster (use at your own risk):
SLEEP_BETWEEN_REQUESTS = 0.1  # Very fast (10 req/sec) - 7 minutes total
```

### If You Want to Slow Down Even More:
```python
# Edit backfill_ohlcv_btc.py line 44:
SLEEP_BETWEEN_REQUESTS = 1.5  # Super slow (0.67 req/sec) - 103 minutes total
```

### Change Date Range:
```python
# Edit backfill_ohlcv_btc.py lines 37-38:
START_DATE = datetime(2023, 1, 1, 0, 0, 0)  # Start from Jan 1, 2023
END_DATE = datetime(2024, 10, 4, 23, 59, 59)  # Keep end date same
```

---

## Safety Features

1. **Automatic Retry**: 5 retry attempts for each failed API call
2. **Resume Capability**: Can be interrupted and resumed anytime
3. **Progress Checkpoints**: Saves progress regularly
4. **Conservative Rate Limiting**: 0.75s between requests (won't trigger rate limits)
5. **Error Logging**: Full traceback for debugging
6. **Database Validation**: Checks existing data before starting

---

## Questions?

**Q: Can I run this while my trading bots are active?**  
A: Yes! The 0.75s sleep between requests is specifically designed to avoid interfering with your 3 active bots.

**Q: What if I want to backfill more pairs later?**  
A: Copy this script and change `PROD_ID = 'BTC-USDC'` to `'ETH-USDC'` or `'SOL-USDC'` etc.

**Q: Can I pause and resume?**  
A: Yes! Press Ctrl+C to stop, then re-run the script. It will detect existing data and resume.

**Q: How do I know if it's working?**  
A: You'll see progress updates every 10 requests (~7.5 seconds). If you don't see updates for 30+ seconds, there may be an issue.

**Q: What if I already have some data?**  
A: The script checks existing data first and only backfills missing gaps.

---

## Next Steps After Completion

1. ✅ Verify data completeness
2. ✅ Run test backtest (1 week period)
3. ✅ Run full backtest (June 2022 - Oct 2024)
4. ✅ Review strategy performance
5. ✅ Optimize strategy parameters

---

**Ready to start?**

```bash
uv run python backfill_ohlcv_btc.py
```

Then go enjoy your meal! 🍽️
