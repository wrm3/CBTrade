# Backfill Script Debug Notes
*Created: 2025-10-05 01:47 AM*

## Issue Summary
The backfill script was hanging after the first API call. It would print "[API] Response received" but then nothing else.

## Fixes Applied

### 1. **Added Output Flushing**
   - Added `flush=True` to critical print statements
   - Python was likely buffering output when running in background
   - Now prints will appear immediately in real-time

### 2. **Comprehensive Debug Output**

#### API Call Flow:
```
[HH:MM:SS] [API] Calling Coinbase API...
[HH:MM:SS] [API] Response received
[HH:MM:SS] [DEBUG] Response type: <class '...'>
[HH:MM:SS] [DEBUG] Response has 'candles'?: True/False
[HH:MM:SS] [DEBUG] Candles type: <class '...'>
[HH:MM:SS] [DEBUG] Number of candles: 300
[HH:MM:SS] [DEBUG] First candle type: <class '...'>
[HH:MM:SS] [API] Parsed 300 candles
[HH:MM:SS] [API] Returning 300 candles
```

#### Database Save Flow:
```
[HH:MM:SS] [DB] save_candles_to_db called with 300 candles
[HH:MM:SS] [DB] Converting to DataFrame...
[HH:MM:SS] [DB] Prepared 300 records for insertion
[HH:MM:SS] [DB] Calling db_tbl_insupd for table ohlcv_BTC_USDC...
[HH:MM:SS] [DB] Insert completed successfully
```

#### Main Loop Flow:
```
[HH:MM:SS] Request 1/4,114 (0.0%) | Period: 2024-10-04 18:59 - 2024-10-04 23:59
[HH:MM:SS] Calling fetch_candles_from_coinbase...
[HH:MM:SS] fetch_candles_from_coinbase returned: <class 'list'>
[HH:MM:SS] Retrieved 300 candles
[HH:MM:SS] Saved to DB. Total saved: 300 candles
```

### 3. **What To Look For in Morning**

#### Success Pattern:
- You should see ALL the debug messages flowing through
- Each request should complete and show "Total saved: X candles"
- Candle count should increase steadily

#### If Still Hanging:
- Look for where the output stops
- The debug messages will show exactly which step is hanging:
  - If stops after "Response received" → Response parsing issue
  - If stops after "save_candles_to_db called" → Database issue
  - If stops after "Calling db_tbl_insupd" → Database hanging

#### Common Issues:
1. **"No candles in response"** - Requesting data before BTC was listed
2. **"API timeout"** - Coinbase API slow, will auto-retry
3. **"Database insertion error"** - Check MySQL is running and table exists

## Running the Script

```powershell
cd C:\git\cbtrade
python backtest/backfill_ohlcv_btc.py
```

Or if you want to see output in real-time:
```powershell
cd C:\git\cbtrade
python backtest/backfill_ohlcv_btc.py 2>&1 | Tee-Object -FilePath backfill.log
```

## What Changed in Code

1. **Lines 17:** Added `import threading` for timeout handling
2. **Lines 49:** Added `API_TIMEOUT = 30` config
3. **Lines 130-227:** Complete rewrite of `fetch_candles_from_coinbase()` with:
   - Threading-based timeout (30s max)
   - Extensive debug output at every step
   - Response type checking
   - Output flushing for real-time display

4. **Lines 226-276:** Added debug output to `save_candles_to_db()`:
   - Shows exactly what it's doing at each step
   - Shows when database calls start/complete

5. **Lines 369-371:** Added debug output in main loop:
   - Shows function calls and returns
   - Shows return types

## Next Steps if Issues Persist

If it's still hanging in the morning:
1. The debug output will show EXACTLY where
2. We can add even more granular debugging to that specific point
3. We may need to check if `db_tbl_insupd` is the culprit

## Expected Runtime

- **Total Requests:** 4,114
- **Rate:** ~1.3 requests/second with 0.75s sleep
- **Estimated Time:** ~51 minutes for full backfill
- **Database Size:** ~1.2 million 1-minute candles for June 2022 - Oct 2024

---

**IMPORTANT:** All debugging is non-destructive. The script will still save data correctly, it just has extra output now to help diagnose the hanging issue.
