# MySQL OHLCV Database Implementation

This module provides MySQL-based OHLCV (Open-High-Low-Close-Volume) database operations for the CBTrade system.

## Core Features

- MySQL database backend with proper timestamp handling
- Single table per trading pair with frequency column for all timeframes
- Automatic table creation and trigger setup
- Full error handling and timestamp synchronization
- Comprehensive candle age visualization
- Maintains interface compatibility with existing codebase

## Usage

```python
# Import directly
from libs.db_mysql.ohlcv.db_main import create_ohlcv_db, show_ohlcv_age, show_all_ohlcv_age

# Create database instance for a trading pair
db = create_ohlcv_db('BTC-USDC')

# Save OHLCV data
df = pd.DataFrame(...) # DataFrame with OHLCV data and datetime index
db.save_ohlcv_data('1min', df)

# Load OHLCV data
df = db.load_ohlcv_data('1min', limit=300)

# Show candle age status
show_ohlcv_age('BTC-USDC')
show_all_ohlcv_age() # Show all pairs
```

## Database Structure

Each trading pair gets its own table with the pattern `ohlcv_{pair_id}` where pair_id has dashes replaced with underscores (e.g., BTC-USDC becomes ohlcv_btc_usdc).

The tables include:
- Timestamp and frequency columns
- OHLCV price and volume data
- Start/end times in both datetime and unix timestamp formats
- Update tracking fields
- MySQL triggers to keep timestamps synchronized

## Function Map (Old → New)

The implementation maintains compatibility with the older `cls_bot_db_ohlcv.py` file by providing the same function names and signatures:

- `db_tbl_insupd()` - Insert/update records with proper upsert handling
- `db_ohlcv_prod_id_freqs()` - Get frequency summary for a pair
- `db_ohlcv_freq_get()` - Get OHLCV data for a specific pair/frequency
- `db_check_ohlcv_prod_id_table()` - Ensure table exists for a pair
- `db_tbl_ohlcv_prod_id_insupd()` - Insert/update OHLCV data for a pair
- `db_tbl_ohlcv_prod_id_insupd_many()` - Insert/update multiple frequencies
- `db_ohlcv_table_names_get()` - Get all OHLCV table names
- `db_ohlcv_dump()` - Export OHLCV data to CSV

## Improvements

- Better error handling with full stack traces
- Automatic trigger creation for timestamp synchronization
- Support for multiple timeframes in a single table
- Comprehensive age display for candle data
- Consistent interface with original codebase