# Fast CSV-Based Backfill Workflow

## Why CSV Instead of Direct Database?

**Problem:** Database inserts were taking 10-15 seconds per batch, making backfill extremely slow.

**Solution:** Write to CSV (instant) during collection, then bulk-load to database later (much faster).

## Workflow

### Step 1: Fast Collection (API → CSV)
```bash
cd C:\git\cbtrade
python backtest/backfill_ohlcv_btc.py
```

**What it does:**
- Fetches candles from Coinbase API
- Writes immediately to CSV file
- **Super fast** - no database bottleneck!
- Can be interrupted and resumed anytime

**Output file:** `backtest/csv_cache/btc_usdc_1min.csv`

**Speed:** ~1 second per request (0.75s API + 0.01s CSV write)
- **6,285 requests = ~2 hours** (vs. 26+ hours with database!)

### Step 2: Bulk Load (CSV → Database)
After collection completes, bulk-load the CSV:

```bash
cd C:\git\cbtrade
python backtest/load_csv_to_db.py
```

**What it does:**
- Loads CSV in 10,000-row batches
- Checks for existing timestamps
- Only inserts NEW candles
- Much faster than incremental inserts

**Speed:** ~1,000-5,000 rows/second
- **1.2 million candles = ~5-15 minutes**

## Commands

### Check Progress During Collection
```bash
# See how many lines in CSV
python -c "with open('backtest/csv_cache/btc_usdc_1min.csv') as f: print(f'{sum(1 for _ in f)-1:,} candles')"

# Check file size
python -c "import os; print(f'{os.path.getsize(\"backtest/csv_cache/btc_usdc_1min.csv\")/(1024*1024):.1f} MB')"
```

### Resume Collection After Interruption
Just run the backfill script again - it will:
1. Check what's already in CSV
2. Continue from where it left off

### Load to Database
```bash
python backtest/load_csv_to_db.py
```

### Delete CSV After Loading (Optional)
```bash
rm backtest/csv_cache/btc_usdc_1min.csv
```

## Benefits

✅ **26x faster collection** (~2 hours vs. 26+ hours)
✅ **Resumable** - interrupt and restart anytime
✅ **Portable** - CSV can be backed up, moved, shared
✅ **Inspectable** - open CSV in Excel to check data
✅ **Safer** - database load happens separately, controlled

## File Locations

- **CSV Cache:** `backtest/csv_cache/btc_usdc_1min.csv`
- **Collection Script:** `backtest/backfill_ohlcv_btc.py`
- **Loader Script:** `backtest/load_csv_to_db.py`
- **Coverage Checker:** `backtest/check_daily_coverage.py`

## Workflow Summary

```
1. Collect:  API → CSV (fast, ~2 hours)
2. Load:     CSV → Database (bulk, ~15 min)
3. Verify:   python backtest/check_daily_coverage.py
4. Done!     Delete CSV if desired
```
