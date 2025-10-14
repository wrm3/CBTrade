#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#

 

#<=====>#
# Imports - Public
#<=====>#
import math
import os
from typing import Any
from pandas.core.series import Series
from pandas.core.series import Series
from pandas._libs.tslibs.timedeltas import Timedelta
import sys
import traceback
import warnings
from datetime import datetime as dt, timedelta
from datetime import timezone
import numpy as np
import pandas as pd
import pandas_ta as pta
from fstrent_colors import *

#<=====>#
# Imports - Project
#<=====>#
from libs.common import AttrDict
from libs.common import beep
from libs.common import dir_val
from libs.common import dttm_get
from libs.common import print_adv
from libs.common import narc
from libs.coinbase_handler import cb
from libs.db_mysql.ohlcv.db_main import OHLCV_DB

warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

#<=====>#
# Variables
#<=====>#
lib_name      = 'ta_base'
log_name      = 'ta_base'

# <=====>#
# Assignments Pre
# <=====>#
debug_tf = False
lib_secs_max  = 0

#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#


@narc(1)
def ta_main_new(pair, st_pair):
    if debug_tf: C(f'ta_base.ta_main_new() ==> {pair.prod_id}')
    
    prod_id     = pair.prod_id
    ta          = AttrDict()
    prc_mkt     = pair.prc_mkt
    rfreq       = ''
    df          = None
    dfs         = {}
    dfs_ins_many = {}

    dfs = ta_ohlcv(pair, st_pair)

    # Assigning the Real Time Close Price
    close_price = dfs['1min']['close'].iloc[-1]

    # database insert - save each timeframe using our new method
    rfreqs = ['1min','5min', '15min', '30min', '1h', '4h', '1d']
    ohlcv_db = OHLCV_DB(prod_id=prod_id)
    
    for rfreq in rfreqs:
        if rfreq in dfs and not dfs[rfreq].empty:
            # Save this timeframe's data using our new bulk insert method
            stats = ohlcv_db.save_ohlcv_data(freq=rfreq, df=dfs[rfreq])
            # print(f"📊 {prod_id} {rfreq}: {stats['inserted']} inserted, {stats['updated']} updated")

    # reduced list, previous was used for forming current candles
    rfreqs = ['5min', '15min', '30min', '1h', '4h', '1d']

    # Show current candle ages/prices after persistence so QA reflects saved state
    ohlcv_db.display_candle_status_with_age(prod_id, display_enabled=True)

    # Adding the Technical Analysis Indicators
    for rfreq in rfreqs:
        ta[rfreq]            = AttrDict()
        ta[rfreq].df         = None
        ta[rfreq].curr       = AttrDict()
        ta[rfreq].last       = AttrDict()
        ta[rfreq].prev       = AttrDict()
        df = dfs[rfreq]
        df = ta_add_indicators(df, st_pair, prc_mkt, rfreq)
        ta[rfreq].df = df
        # C(f'ta_base.ta_main_new() - before adding last 6 timer periods of indicatorsmade it here 107')
        for x in range(0,-6,-1):
            desc = f'ago{abs(x)}'
            y = x - 1
            for k in df:
                if not rfreq in ta: ta[rfreq] = AttrDict()
                if not k in ta[rfreq]: ta[rfreq][k] = AttrDict()
                ta[rfreq][k][desc] =  df[k].iloc[y]
        # C(f'ta_base.ta_main_new() - after adding last 6 timer periods of indicatorsmade it here 115')
    
    # ta.dfs = dfs

    # Check that all forming candles have the same final close price since they are real time
    C(f'ta_base.ta_main_new() - before checking that all forming candles have the same final close price - made it here 120')
    for rfreq in rfreqs:
        if ta[rfreq].df['close'].iloc[-1] != close_price:
            print(f"line 302 => rfreq : {rfreq}, end : {ta[rfreq].df.index.max()}, close_price : {close_price:>.8f}, close : {ta[rfreq].df['close'].iloc[-1]:>.8f}")
            print(f"Debug Info Final => {ta[rfreq].df.tail(5)}")  # Add this line for more debug info
    C(f'ta_base.ta_main_new() - after checking that all forming candles have the same final close price - made it here 125')

    return ta

#<=====>#


@narc(1)
def ta_ohlcv(pair, st_pair):
    if debug_tf: C(f'ta_base.ta_ohlcv() ==> {pair.prod_id}')

    prod_id     = pair.prod_id
    rfreq       = ''
    df          = None
    dfs         = {}

#        rfreqs = ['1min', '3min', '5min', '15min', '30min', '1h', '4h', '1d']
    rfreqs = ['1min', '5min', '15min', '30min', '1h', '4h', '1d']

    ohlcv_meths = {}

    ohlcv_db = OHLCV_DB(prod_id=prod_id)
    ohlcv_last_dttms = ohlcv_db.db_ohlcv_prod_id_freqs()

    utc_now = dt.now(timezone.utc)
    for freq in rfreqs:
        ohlcv_meth = {}
        ohlcv_meth['prod_id']       = prod_id
        ohlcv_meth['freq']          = freq
        ohlcv_meth['last_start_dttm'] = None

        for ohlcv_last_dttm in ohlcv_last_dttms:
            this_freq = ohlcv_last_dttm['freq']
            if this_freq == freq:
                # 🔧 CRITICAL FIX: Handle None datetime values to prevent AttributeError crashes
                # Some pairs may not have OHLCV data, causing last_start_dttm to be None
                if ohlcv_last_dttm['last_start_dttm'] is not None:
                    ohlcv_meth['last_start_dttm'] = ohlcv_last_dttm['last_start_dttm'].replace(tzinfo=timezone.utc)
                else:
                    # Keep as None if no data exists - this will trigger API fetch
                    ohlcv_meth['last_start_dttm'] = None
                    if debug_tf:
                        print(f"⚠️ No OHLCV data for {prod_id} {freq} - will fetch from API")

        if freq == '1min':
            ohlcv_meth['elapsed_max']   = 60
#            elif freq == '3min':
#                ohlcv_meth['elapsed_max']   = 180
        elif freq == '5min':
            ohlcv_meth['elapsed_max']   = 300
        elif freq == '15min':
            ohlcv_meth['elapsed_max']   = 900
        elif freq == '30min':
            ohlcv_meth['elapsed_max']   = 1800
        elif freq == '1h':
            ohlcv_meth['elapsed_max']   = 3600
        elif freq == '4h':
            ohlcv_meth['elapsed_max']   = 14400
        elif freq == '1d':
            ohlcv_meth['elapsed_max']   = 86400

        ohlcv_meth['utc_now']           = utc_now

        if ohlcv_meth['last_start_dttm']:
            ohlcv_meth['elapsed']       = (utc_now - ohlcv_meth['last_start_dttm'])/ timedelta(seconds=1)
        else:
            ohlcv_meth['elapsed']       = 9999999

        ohlcv_meth['method']            = 'api'
        if ohlcv_meth['elapsed'] < ohlcv_meth['elapsed_max']:
            ohlcv_meth['method']        = 'db'
#            else:
#                print(f'elapsed since last api call : {ohlcv_meth['elapsed']}')

        ohlcv_meths[freq] = ohlcv_meth

#            print(ohlcv_meth)

    for freq in ohlcv_meths:
        if ohlcv_meths[freq]['method'] == 'api':
            # print(f"[OHLCV] {prod_id} {freq}: method=api")
            dfs[freq] = ta_df_api_get(prod_id, freq)
        else:
            # print(f"[OHLCV] {prod_id} {freq}: method=db")
            dfs[freq] = ta_df_hist_db(prod_id, freq)
            # If DB lacks sufficient rows (e.g., daily has only 0-1 rows), fall back to API
            try:
                _rows = len(dfs.get(freq, []))
            except Exception:
                _rows = 0
            if _rows < 2:
                # print(f"[OHLCV] {prod_id} {freq}: db insufficient ({_rows} rows) → fallback to API")
                dfs[freq] = ta_df_api_get(prod_id, freq)
            else:
                # Staleness check: if most recent DB candle is older than its expected cadence, fallback to API
                try:
                    last_ts = dfs[freq].index.max() if hasattr(dfs[freq], 'index') and len(dfs[freq]) else None
                    if last_ts is not None:
                        now_utc = dt.now(timezone.utc)
                        age_secs = (now_utc - last_ts).total_seconds()
                        cadence = {
                            '1min': 60,
                            '5min': 300,
                            '15min': 900,
                            '30min': 1800,
                            '1h': 3600,
                            '4h': 14400,
                            '1d': 86400,
                        }.get(freq, 3600)
                        # small slack to avoid false positives
                        if age_secs > cadence + 5:
                            # print(f"[OHLCV] {prod_id} {freq}: db stale (age={int(age_secs)}s > {cadence}s) → fallback to API")
                            dfs[freq] = ta_df_api_get(prod_id, freq)
                except Exception:
                    pass

    pair.dfs = dfs

    # print(f"\n{'='*80}")
    # print(f"Available timeframes: {list(dfs.keys())}")
    # for freq, df in dfs.items():
    #     print(f"  {freq}: {len(df)} rows")
    # print(f"{'='*80}")
    
    close_price = dfs['1min']['close'].iloc[-1]
    rfreqs = ['1min', '5min', '15min', '30min', '1h', '4h', '1d']

    # populate the data for forming current candles
    for rfreq in rfreqs:
        if rfreq in ('1d','4h'):
            # remove last row
            dfs[rfreq] = dfs[rfreq].iloc[:-1]
            # get max index
            last_candle_dttm = dfs[rfreq].index.max()
            # get the 1h
            df_add = dfs['1h']
            # get the recent 1h
            df_add_filtered = df_add[df_add.index > last_candle_dttm]
            # assemble them
            dfs[rfreq] = pd.concat([dfs[rfreq], df_add_filtered]).sort_index()

        if rfreq not in ('1min'):
            # remove last row
            dfs[rfreq] = dfs[rfreq].iloc[:-1]
            # get max index
            last_candle_dttm = dfs[rfreq].index.max()
            # get the 1min
            df_add = dfs['1min']
            # get the recent 1min
            df_add_filtered = df_add[df_add.index > last_candle_dttm]
            # assemble them
            dfs[rfreq] = pd.concat([dfs[rfreq], df_add_filtered]).sort_index()

    for rfreq in rfreqs:
        if rfreq not in ('1min'):
            dfs[rfreq] = dfs[rfreq].resample(rfreq).agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
                }).dropna()

            dfs[rfreq] = dfs[rfreq].dropna(subset=['open', 'high', 'low', 'close', 'volume'])
            dfs[rfreq] = dfs[rfreq][(dfs[rfreq][['open', 'high', 'low', 'close', 'volume']] != 0).any(axis=1)]


        # Ensure the index is a DatetimeIndex
        if not isinstance(dfs[rfreq].index, pd.DatetimeIndex):
            dfs[rfreq]['timestamp'] = pd.to_datetime(dfs[rfreq]['timestamp'])
            dfs[rfreq] = dfs[rfreq].set_index('timestamp')

        # if rfreq == '1min':
        #     csv_fname = f'data/{pair.prod_id}_{rfreq}.csv'
        #     dir_val(csv_fname)
        #     dfs[rfreq].to_csv(csv_fname, index=True)

    # Save formed candles (post-resample) so ages/status align across frames
    for rfreq in rfreqs:
        if rfreq != '1min' and rfreq in dfs and not dfs[rfreq].empty:
            try:
                save_result = ohlcv_db.save_ohlcv_data(rfreq, dfs[rfreq])
                if debug_tf:
                    print(f"✅ Saved formed {rfreq}: {save_result['inserted']} inserted, {save_result['updated']} updated")
            except Exception as e:
                print(f"❌ Error saving formed {rfreq}: {e}")
                if debug_tf: traceback.print_exc()

    # Note: No additional DB save here. We keep saving only once (earlier),
    # and all subsequent shaping below remains in-memory for TA only.

    # Cap rows to mitigate memory pressure, then ensure minimum
    for rfreq in rfreqs:
        # hard cap first
        if len(dfs[rfreq]) > 500:
            dfs[rfreq] = dfs[rfreq].tail(500)
        if len(dfs[rfreq]) < 350:
            # print_adv()
            # print(f'df - {rfreq} has {len(dfs[rfreq])} rows before...')
            # print(dfs[rfreq].head(3))
            # print(dfs[rfreq].tail(3))
            dfs[rfreq] = ta_df_fill_rows(df=dfs[rfreq], min_rows=300, rfreq=rfreq)
            # print(dfs[rfreq].head(3))
            # print(dfs[rfreq].tail(3))
            # print(f'df - {rfreq} has {len(dfs[rfreq])} rows after...')
            # print_adv()
            # print_adv()

    # timer
    for rfreq in rfreqs:
        if dfs[rfreq]['close'].iloc[-1] != close_price:
            print(f"line 149 => rfreq : {rfreq}, end : {dfs[rfreq].index.max()}, close : {dfs[rfreq]['close'].iloc[-1]}, close should be {close_price}")
            print('before fix')
            print(dfs[rfreq].tail(3))
            dfs[rfreq].loc[dfs[rfreq].index[-1], 'close'] = close_price
            dfs[rfreq].loc[dfs[rfreq].index[-1], 'open']  = dfs[rfreq]['close'].iloc[-2]
            print('after fix')
            print(dfs[rfreq].tail(3))

    return dfs

#<=====>#


@narc(1)
def ta_ohlcv_range(prod_id, freq='1h', sd='2024-01-01', td='2024-12-31'):
    if debug_tf: C(f'ta_base.ta_ohlcv_range() ==> {prod_id}')
    df        = None
    sd         = int(math.floor(pd.Timestamp(ts_input=sd).timestamp()))
    td         = int(math.floor(pd.Timestamp(ts_input=td).timestamp()))
    df         = cb.cb_candles_get(product_id=prod_id, start = sd, end = td, rfreq = freq)
    df         = ta_df_dropna(df)
    return df

#<=====>#


@narc(1)
def ta_df_api_get(prod_id, rfreq) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_df_api_get() ==> {prod_id}')
    df_db  = ta_df_hist_db(prod_id, rfreq)
    df_api = cb.cb_candles_get(product_id=prod_id, rfreq=rfreq, min_rows=299)
    # print(f"[OHLCV] {prod_id} {rfreq}: db_rows={len(df_db)}, api_rows={len(df_api)}")
    df_db  = ta_df_dropna(df_db)
    df_api = ta_df_dropna(df_api)
    if len(df_db) > 0:
        df = ta_df_merge_db_and_api(prod_id, rfreq, df_db, df_api)
    else:
        df = df_api
    df = ta_df_dropna(df)
    # print(f"[OHLCV] {prod_id} {rfreq}: merged_rows={len(df)}")
    return df

#<=====>#


@narc(1)
def ta_df_hist_db(prod_id, freq):
    if debug_tf: C(f'ta_base.ta_df_hist_db() ==> {prod_id}')

    df = None

    ohlcv_db = OHLCV_DB(prod_id=prod_id)
    
    # 🚀 NEW: Use the clean load_ohlcv_data method with pandas.read_sql()
    df = ohlcv_db.load_ohlcv_data(timeframe=freq, limit=300)
    # print(f"[OHLCV] {prod_id} {freq}: db_load_rows={len(df)} (pre-clean)")

    # 🔴 Handle empty DataFrame (no historical data exists)
    if df.empty:
        # Return empty DataFrame with proper structure when no historical data exists
        empty_df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        empty_df.set_index('timestamp', inplace=True)
        return empty_df

    # Clean, standard pandas - ensure timestamp_unix exists then convert to datetime index
    if 'timestamp_unix' not in df.columns:
        # Compatibility: some legacy tables/files may expose 'timestamp' or 'start_unix'
        if 'timestamp' in df.columns:
            # If already datetime, derive unix seconds; else coerce numeric seconds
            if pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp_unix'] = (df['timestamp'].astype('int64') // 10**9)
            else:
                df['timestamp_unix'] = pd.to_numeric(df['timestamp'], errors='coerce').astype('Int64')
        elif 'start_unix' in df.columns:
            df['timestamp_unix'] = pd.to_numeric(df['start_unix'], errors='coerce').astype('Int64')
        else:
            # As a last resort, return empty structured frame to avoid hard crash
            empty_df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            empty_df.set_index('timestamp', inplace=True)
            return empty_df

    df['timestamp'] = pd.to_datetime(df['timestamp_unix'], unit='s', errors='coerce')
    df.set_index('timestamp', inplace=True)
    
    # Keep only OHLCV columns 
    df = df[['open', 'high', 'low', 'close', 'volume']].copy()
    
    # Basic validation if needed
    df = df.dropna()  # Remove any NaN values

    # Ensure numeric types
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Resample data
    d = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}

    roffset = None
    if roffset:
        df = df.resample(freq, offset=roffset).agg(d)
    else:
        df = df.resample(freq).agg(d)

    df = ta_df_dropna(df)
    # print(f"[OHLCV] {prod_id} {freq}: db_final_rows={len(df)}")

    # Cap historical frame to reduce memory/CPU
    df = df.tail(500)
    return df

#<=====>#


@narc(1)
def ta_df_fill_rows(df, min_rows=300, time_index_col=None, rfreq: str = None) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_df_fill_rows()')

    """
    Ensures the DataFrame has at least `min_rows` rows by prepending duplicates of the oldest row,
    with proper timestamps matching the resampling frequency.

    Parameters:
    - df: pandas DataFrame containing your OHLCV data.
    - min_rows: The minimum number of rows the DataFrame should have.
    - time_index_col: Name of the datetime column if it's not the index. If None, assumes datetime index.

    Returns:
    - A DataFrame with at least `min_rows` rows.
    """
    current_rows = len(df)
    if current_rows >= min_rows:
        return df  # No need to add rows

    # If empty, we cannot infer timestamps – return as-is (caller should handle)
    if current_rows == 0:
        return df

    delta = min_rows - current_rows  # Number of rows to add

    # Determine the datetime index/column
    if time_index_col:
        # Ensure time_index_col is datetime type
        if not pd.api.types.is_datetime64_any_dtype(df[time_index_col]):
            df[time_index_col] = pd.to_datetime(df[time_index_col])

        # Ensure DataFrame is sorted by time_index_col in ascending order
        df = df.sort_values(by=time_index_col).reset_index(drop=True)

        datetime_series = df[time_index_col]
    else:
        # Assume datetime index
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        # Ensure DataFrame is sorted by index in ascending order
        df = df.sort_index()

    datetime_series = df.index

    # Determine frequency from provided rfreq if available; otherwise infer
    freq: pd.Timedelta | None = None
    if rfreq:
        # Map of time frequency strings to Timedelta objects
        freq_map = {
            '1min': pd.Timedelta(minutes=1),
            '5min': pd.Timedelta(minutes=5),
            '15min': pd.Timedelta(minutes=15),
            '30min': pd.Timedelta(minutes=30),
            '1h': pd.Timedelta(hours=1),
            '4h': pd.Timedelta(hours=4),
            '1d': pd.Timedelta(days=1),
        }
        freq_temp = freq_map.get(rfreq)
        if freq_temp is not None and isinstance(freq_temp, pd.Timedelta) and not pd.isna(freq_temp):
            freq = freq_temp
    if freq is None:
        if len(datetime_series) > 1:
            try:
                # Use median diff to avoid outliers causing extreme frequencies
                diffs: Series = pd.Series(data=datetime_series).diff().dropna()
                if len(diffs) > 0:
                    median_val = diffs.median()
                    if median_val is not None and not pd.isna(median_val):
                        freq_candidate = pd.to_timedelta(median_val)
                        # Only assign if result is not NaT
                        if isinstance(freq_candidate, pd.Timedelta) and not pd.isna(freq_candidate):
                            freq = freq_candidate
            except Exception:
                pass
        # If still unknown, skip filling instead of guessing wrong
        if freq is None:
            return df

    # Safety clamp: invalid or extreme frequencies can cause overflow
    if pd.isna(freq) or freq <= pd.Timedelta(value=0) or freq > pd.Timedelta(days=365*10):
        return df

    # If delta is absurdly large (e.g., > 10,000), abort fill to avoid massive backfill
    if delta > 10000:
        return df

    # Get the oldest timestamp
    oldest_timestamp: Any = datetime_series[0]

    # Generate new timestamps stepping backward (guard against overflow)
    try:
        new_timestamps = [oldest_timestamp - freq * i for i in range(delta, 0, -1)]
    except OverflowError:
        # If overflow occurs due to extreme freq, abort filling to avoid crash
        return df

    # Create new rows with data from oldest row
    oldest_row = df.iloc[0].copy()

    # Create a DataFrame with copies of the oldest row
    new_rows = pd.DataFrame([oldest_row] * delta)

    if time_index_col:
        # Assign new timestamps to time_index_col
        new_rows[time_index_col] = new_timestamps
    else:
        # Assign new timestamps to index
        new_rows.index = new_timestamps

    # Concatenate new rows with original DataFrame
    df = pd.concat([new_rows, df], ignore_index=bool(time_index_col))

    # If time_index_col is not used, ensure the index is a DatetimeIndex
    if not time_index_col:
        df.index = pd.DatetimeIndex(df.index)
    
    return df

#<=====>#


@narc(1)
def ta_df_dropna(df, cols=['open', 'high', 'low', 'close', 'volume']):
    if debug_tf: C(f'ta_base.ta_df_dropna()')
    
    # 🔴 CRITICAL: Handle empty DataFrames to prevent KeyError crashes
    # This prevents bot crashes when API returns empty data during connectivity issues
    if df.empty:
        if debug_tf: C(f'ta_base.ta_df_dropna() => DataFrame is empty, returning as-is')
        return df
    
    # Check if required columns exist before trying to drop NA values
    missing_cols = [col for col in cols if col not in df.columns]
    if missing_cols:
        if debug_tf: C(f'ta_base.ta_df_dropna() => Missing columns {missing_cols}, returning empty DataFrame')
        return pd.DataFrame()  # Return empty DataFrame with proper structure
    
    df = df.dropna(subset=cols)
    df = df[(df[cols] != 0).any(axis=1)]
    return df

#<=====>#


@narc(1)
def ta_df_merge_db_and_api(prod_id, freq, df_db, df_api):
    if debug_tf: C(f'ta_base.ta_df_merge_db_and_api() ==> {prod_id}')
    """
    Fetches OHLCV data from the database and the API, merges them,
    replaces overlapping data with API data, updates the database,
    and returns the merged DataFrame.

    Parameters:
    - prod_id: The product ID (e.g., trading pair).
    - freq: The frequency of the data (e.g., '1min', '5min').

    Returns:
    - A merged pandas DataFrame containing OHLCV data.
    """

    # Ensure the indices are datetime and sorted
    if not isinstance(df_db.index, pd.DatetimeIndex):
        df_db.index = pd.to_datetime(df_db.index)
    if not isinstance(df_api.index, pd.DatetimeIndex):
        df_api.index = pd.to_datetime(df_api.index)

    df_db = df_db.sort_index()
    df_api = df_api.sort_index()

    # Identify overlapping timestamps
    overlapping_timestamps = df_db.index.intersection(df_api.index)

    # Remove overlapping timestamps from df_db
    if not overlapping_timestamps.empty:
        df_db = df_db.drop(overlapping_timestamps)

    # Merge the dataframes
    # df_merged = pd.concat([df_db, df_api]).sort_index()
    df_merged = pd.concat([d for d in (df_db, df_api) if d is not None and not d.empty]).sort_index()

    return df_merged

#<=====>#


@narc(1)
def ta_add_indicators(df: pd.DataFrame, st, prc_mkt, rfreq) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_indicators(len(df={len(df)}), st=st, prc_mkt={prc_mkt}, rfreq={rfreq})')
    # Clean, standard pandas - no magic functions
    try:
        # Basic validation if needed
        df = df.dropna()  # Remove any NaN values
        
        if df.empty:
            print(f'🚨 CRITICAL: No valid data after basic validation for {rfreq}')
            raise ValueError(f"No valid OHLCV data available for technical analysis on {rfreq} timeframe")
        
        df['hl2']   = (df['high'] + df['low']) / 2
        df['hlc3']  = (df['high'] + df['low'] + df['close']) / 3
        df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
        df['hlcc4'] = (df['high'] + df['low'] + df['close'] + df['close']) / 3

        df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])
        # Filter out rows where all OHLCV values are zero
        non_zero_mask = (df[['open', 'high', 'low', 'close', 'volume']] != 0).any(axis=1)
        df = df.loc[non_zero_mask]

        if len(df) < 10:
            print(f'🚨 CRITICAL: Insufficient data for {rfreq} - only {len(df)} rows, need at least 10')
            raise ValueError(f"Insufficient OHLCV data for {rfreq} timeframe: {len(df)} rows (minimum 10 required)")

        # Candle Color
        df = ta_add_color(df)

        # Heikin Ashi Candles
        df = ta_add_ha(df)

        # Close & HA_Close Rate Of Change
        df = ta_add_roc(df, col='close')
        df = ta_add_roc(df, col='ha_close')

        # RSI
        df = ta_add_rsi(df)
        df = ta_add_roc(df, col='rsi')

        # ATR
        df = ta_add_atr(df)

        # New Strat Add Section
        # STRAT SHA
        # Smoothed Heikin Ashi Candles
        fast_sha_len1 = st.strats.sha.fast_sha_len1 # 8
        fast_sha_len2 = st.strats.sha.fast_sha_len2 # 8
        slow_sha_len1 = st.strats.sha.slow_sha_len1 # 21
        slow_sha_len2 = st.strats.sha.slow_sha_len2 # 21
        if debug_tf: C(f'ta_base.ta_add_indicators() ==> calling (fast) ta_add_sha()')
        df = ta_add_sha(df, prc_mkt, sha_len1=fast_sha_len1, sha_len2=fast_sha_len2, tag='_fast')
        if debug_tf: C(f'ta_base.ta_add_indicators() ==> returning from (fast) ta_add_sha()')
        if debug_tf: C(f'ta_base.ta_add_indicators() ==> calling (slow) ta_add_sha()')
        df = ta_add_sha(df, prc_mkt, sha_len1=slow_sha_len1, sha_len2=slow_sha_len2, tag='_slow')
        if debug_tf: C(f'ta_base.ta_add_indicators() ==> returing from (slow)ta_add_sha()')

        # STRAT IMP MACD
        per_ma   = st.strats.imp_macd.per_ma   # 34 
        per_sign = st.strats.imp_macd.per_sign # 9 
        df = ta_add_imp_macd(df, per_ma=per_ma, per_sign=per_sign)

        # STRAT BB
        inner_per = st.strats.bb.inner_per # 21 
        inner_sd  = st.strats.bb.inner_sd  # 2.3 
        outer_per = st.strats.bb.outer_per # 21 
        outer_sd  = st.strats.bb.outer_sd  # 2.7 
        df = ta_add_bb(df, per=inner_per, sd=inner_sd, tag='_inner')
        df = ta_add_bb(df, per=outer_per, sd=outer_sd, tag='_outer')

        # STRAT BB BO
        per = st.strats.bb_bo.per # 21 
        sd  = st.strats.bb_bo.sd  # 2.5 
        df = ta_add_bb(df, per=per, sd=sd, tag='_bb_bo')

        nwe_bw = 8
        df = ta_add_nwe(df, src='close', bandwidth=nwe_bw, tag='', rfreq=rfreq)
        df = ta_add_nwe_env(df, src='close', mult=3.0)
        df = ta_add_nwe_rev(df)

        # Highest, Lowest
        # C(f'ta_base.ta_add_indicators() - before Adding Highs and Lows - made it here 653')
        for x in (7,24,30):
            df[f'max{x}'] = df['high'].rolling(window=x).max()
            df[f'min{x}'] = df['low'].rolling(window=x).min()

        # C(f'ta_base.ta_add_indicators() - after Adding Highs and Lows - made it here 658')

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_INDICATORS PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_INDICATORS PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_indicators() 672 leaving...')
    C(f'==> ta_base.ta_add_indicators() 673 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_color(df: pd.DataFrame) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_color(len(df={len(df)})')
    try:
        df['color'] = np.where(df['open'] < df['close'], 'green', 'red')

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_COLOR PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_COLOR PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_color() 975 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_ha(df: pd.DataFrame) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_ha(len(df={len(df)})')
    try:
        # Calculate Heikin Ashi Close
        df['ha_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

        # Initialize HA Open
        df['ha_open']                   = np.nan
        df.at[df.index[0], 'ha_open']                = (df.at[df.index[0], 'open'] + df.at[df.index[0], 'close']) / 2

        # Calculate HA Open for the rest of the rows
        for i in range(1, len(df)):
            df.at[df.index[i], 'ha_open'] = (df.at[df.index[i-1], 'ha_open'] + df.at[df.index[i-1], 'ha_close']) / 2

        # Calculate HA High and Low
        df['ha_high']                   = df[['ha_open','ha_close','high']].max(axis=1)
        df['ha_low']                    = df[['ha_open','ha_close','low']].min(axis=1)

        # HA Candle Height
        df['ha_span']                   = df['ha_high'] - df['ha_low']

        # HA Candle Body Height
        df['ha_body']                   = (df['ha_close'] - df['ha_open']).abs()

        # HA Candle Upper And Lower Wick Heights
        df['ha_wick_upper']             = df['ha_high'] - df[['ha_open','ha_close']].max(axis=1)
        df['ha_wick_lower']             = df[['ha_open','ha_close']].min(axis=1) - df['ha_low']

        # What percentage of each candle is body, uppper and lower wick
        df['ha_body_pct']               = round((df['ha_body'] / df['ha_span']) * 100, 2)
        df['ha_wick_upper_pct']         = round((df['ha_wick_upper'] / df['ha_span']) * 100, 2)
        df['ha_wick_lower_pct']         = round((df['ha_wick_lower'] / df['ha_span']) * 100, 2)

        # Existence of upper and lower wicks
        df['ha_wick_upper_none']        = df['ha_wick_upper_pct'] < 3
        df['ha_wick_lower_none']        = df['ha_wick_lower_pct'] < 3

        # HA Candle Color
        df['ha_color']                  = np.where(df['ha_open'] < df['ha_close'], 'green', 'red')

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_HA PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_HA PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_ha() 975 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_atr(df: pd.DataFrame, per=14) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_atr(len(df={len(df)}), per={per})')
    try:
        per = min(per, len(df))

        df['atr'] = pta.atr(high=df['high'], low=df['low'], close=df['close'], length=per, mamode='SMA')

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_ATR PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_ATR PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_atr() 975 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_rsi(df: pd.DataFrame, per=14) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_rsi(len(df={len(df)}), per={per})')
    try:
        per = min(per, len(df))

        df['rsi'] = pta.rsi(df['close'], length=per)

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_EMA PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_EMA PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_ema() 975 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_roc(df: pd.DataFrame, col='close', label=None, per=3) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_roc(len(df={len(df)}), col={col}, label={label}, per={per})')
    try:
        per = min(per, len(df))

        if not label:
            label = col

        label2 = f'{label}_roc'
        df[label2]                  = pta.roc(df[label], length=3)

        label3 = f'{label}_roc_up'
        df[label3]                  = df[label2]  > df[label2].shift(1)

        label4 = f'{label}_roc_dn'
        df[label4]                  = df[label2]  < df[label2].shift(1)
    

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_ROC PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_ROC PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_roc() 975 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_sma(df: pd.DataFrame, per, col='close', label=None) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_sma(len(df={len(df)}), per={per}, col={col}, label={label})')
    try:
        per = min(per, len(df))

        if not label:
            label = f'{col}_sma{per}'

        df[label]                   = pta.sma(df['close'], length=per)

        df = ta_add_roc(df, col=label)
    

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_SMA PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_SMA PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_sma() 975 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_ema(df: pd.DataFrame, per, col='close', label=None) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_ema(len(df={len(df)}), per={per}, col={col}, label={label})')
    try:
        per = min(per, len(df))

        if not label:
            label = f'{col}_ema{per}'

        df[label]                   = pta.ema(df[col], length=per)

        df = ta_add_roc(df, col=label)

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_EMA PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_EMA PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_ema() 975 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_sha(df: pd.DataFrame, prc_mkt, sha_len1=5, sha_len2=8, tag=None) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_sha(len(df={len(df)}), prc_mkt={prc_mkt}, sha_len1={sha_len1}, sha_len2={sha_len2}, tag={tag})')
    try:

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 809')
        # 🚨 CRITICAL FIX: Prevent index out of bounds - leave room for indexing
        # DataFrame indices are 0-based, so max valid index is len(df) - 1
        sha_len1 = min(sha_len1, len(df) - 1)
        sha_len2 = min(sha_len2, len(df) - 1)
        
        # 🚨 SAFETY CHECK: Ensure we have enough data for meaningful calculations
        if sha_len1 < 2 or sha_len2 < 2 or len(df) < 3:
            print(f"\n{'='*80}")
            print(f"🚨 INSUFFICIENT DATA FOR SHA CALCULATION")
            print(f"{'='*80}")
            print(f"DataFrame length: {len(df)}")
            print(f"sha_len1: {sha_len1}, sha_len2: {sha_len2}")
            print(f"Need at least 3 data points for SHA calculation")
            print(f"{'='*80}")
            raise ValueError(f"INSUFFICIENT DATA FOR SHA - df_len={len(df)}, sha_len1={sha_len1}, sha_len2={sha_len2}")

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 826')
        # Calculate EMAs for the original OHLC values
        df['ema_open']                        = df['open'].ewm(span=sha_len1, adjust=False).mean()
        df['ema_close']                       = df['close'].ewm(span=sha_len1, adjust=False).mean()
        df['ema_high']                        = df['high'].ewm(span=sha_len1, adjust=False).mean()
        df['ema_low']                         = df['low'].ewm(span=sha_len1, adjust=False).mean()

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 833')
        # Calculate Heiken Ashi Close
        df['ha_ema_close']                    = (df['ema_open'] + df['ema_high'] + df['ema_low'] + df['ema_close']) / 4

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 837')
        # Initialize 'ha_ema_open' with NaNs and then set the first valid value after 'sha_len1' periods
        df['ha_ema_open']                     = np.nan
        df.iloc[sha_len1, df.columns.get_loc('ha_ema_open')] = (df.iloc[sha_len1]['ema_open'] + df.iloc[sha_len1]['ema_close']) / 2

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 842')
        # 🚨 PERFORMANCE FIX: Replace slow loop with fully vectorized operations
        # Calculate ha_ema_open using expanding mean for better performance
        # Initialize with the first valid calculation
        initial_value = (df.iloc[sha_len1]['ema_open'] + df.iloc[sha_len1]['ema_close']) / 2
        
        # Create the series with proper initialization
        ha_open_series = pd.Series(index=df.index, dtype=float)
        ha_open_series.iloc[sha_len1] = initial_value
        
        # For subsequent values, use positional indexing to avoid DateTimeIndex label pitfalls
        # and numpy datetime dtype issues seen in pandas get_loc when using .loc with datetime labels.
        for i in range(sha_len1 + 1, len(df)):
            ha_open_series.iat[i] = (ha_open_series.iat[i-1] + df['ha_ema_close'].iat[i-1]) / 2
        
        df['ha_ema_open'] = ha_open_series

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 846')
        # Calculate HA_High and HA_Low
        df['ha_ema_high']                     = df[['ema_high', 'ha_ema_open', 'ha_ema_close']].max(axis=1)
        df['ha_ema_low']                      = df[['ema_low', 'ha_ema_open', 'ha_ema_close']].min(axis=1)

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 851')
        # Calculate EMAs for the Heiken Ashi OHLC values
        df['sha_open']                = df['ha_ema_open'].ewm(span=sha_len2, adjust=False).mean()
        df['sha_close']               = df['ha_ema_close'].ewm(span=sha_len2, adjust=False).mean()
        df['sha_high']                = df['ha_ema_high'].ewm(span=sha_len2, adjust=False).mean()
        df['sha_low']                 = df['ha_ema_low'].ewm(span=sha_len2, adjust=False).mean()

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 858')
        # Smoothed Heikin Ashi Candle Colors
        # You might adjust the color coding logic based on how you want to visualize or use these values
        df['sha_color']               = np.where(df['sha_open'] < df['sha_close'], 'green', 'red')

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 863')
        # Assuming the intention is to calculate the body size of the smoothed HA candle
        df['sha_body']                = (df['sha_close'] - df['sha_open']).abs()

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 867')
        # The upper wick is the distance between the high price and the maximum of the open and close of the smoothed HA candle
        df['sha_wick_upper']          = df['sha_high'] - df[['sha_open', 'sha_close']].max(axis=1)
        # The lower wick is the distance between the low price and the minimum of the open and close of the smoothed HA candle
        df['sha_wick_lower']          = df[['sha_open', 'sha_close']].min(axis=1) - df['sha_low']

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 873')
        # The 'df' DataFrame now includes smoothed Heiken Ashi OHLC values and colors.
        # removing unneeded columns used for calculation
        for c in('ema_open', 'ema_close', 'ema_high', 'ema_low','ha_ema_open', 'ha_ema_close', 'ha_ema_high', 'ha_ema_low'):
            df.pop(c)

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 894')  # Fixed line number
        df['prc_abv_sha']               = prc_mkt > df['sha_close']
        df['prc_bel_sha']               = prc_mkt < df['sha_close']

        if debug_tf: B(f'==> ta_base.ta_add_sha()  - Made It Here 883')
        if tag:
            df[f'sha{tag}_open']         = df['sha_open']
            df[f'sha{tag}_close']        = df['sha_close']
            df[f'sha{tag}_high']         = df['sha_high']
            df[f'sha{tag}_low']          = df['sha_low']
            df[f'sha{tag}_body']         = df['sha_body']
            df[f'sha{tag}_wick_upper']   = df['sha_wick_upper']
            df[f'sha{tag}_wick_lower']   = df['sha_wick_lower']
            df[f'sha{tag}_color']        = df['sha_color']
            df[f'prc_abv_sha{tag}']      = df['prc_abv_sha']
            df[f'prc_bel_sha{tag}']      = df['prc_bel_sha']
            for c in('sha_open', 'sha_close', 'sha_high', 'sha_low', 'sha_body', 'sha_wick_upper', 'sha_wick_lower', 'sha_color', 'prc_abv_sha', 'prc_bel_sha'):
                df.pop(c)

    except BaseException as e:  # ← Catch ALL exceptions including SystemExit
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_SHA PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"DataFrame length: {len(df)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        # 🚨 CRITICAL: Re-raise SystemExit to maintain exit behavior but with better logging
        if isinstance(e, SystemExit):
            print(f"🚨 SystemExit detected - function called sys.exit()")
            raise  # Re-raise SystemExit to maintain exit behavior
        else:
            # For other exceptions, exit with detailed error
            sys.exit(f"TA_ADD_SHA PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_sha() 910 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_imp_macd(df: pd.DataFrame, per_ma=34, per_sign=9, filter_strength=True, filter_period=25, threshold=0.5) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_imp_macd(len(df={len(df)}), per_ma={per_ma}, per_sign={per_sign}, filter_strength={filter_strength}, filter_period={filter_period}, threshold={threshold})')
    try:
        per_ma = min(per_ma, len(df))
        per_sign = min(per_sign, len(df))

        def calc_smma(src, length):
            smma = np.zeros_like(src)
            smma[0] = np.mean(src[:length])
            for i in range(1, len(src)):
                smma[i] = (smma[i-1] * (length - 1) + src.iloc[i]) / length
            return smma

        def calc_zlema(src, per):
            per = min(per, len(src))
            ema1 = pta.ema(src, length=per)
            ema2 = pta.ema(ema1, length=per)
            if ema1 is None or ema2 is None:
                return pd.Series(index=src.index, dtype=float)
            d = ema1 - ema2
            return ema1 + d

        df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3

        df['hi'] = calc_smma(df['high'], per_ma)
        df['lo'] = calc_smma(df['low'], per_ma)
        df['mi'] = calc_zlema(df['hlc3'], per_ma)

        df['md'] = np.where(df['mi'] > df['hi'], df['mi'] - df['hi'], np.where(df['mi'] < df['lo'], df['mi'] - df['lo'], 0))
        df['sb'] = pta.sma(df['md'], length=per_sign)
        df['sh'] = df['md'] - df['sb']

        df['mdc'] = np.where(df['hlc3'] > df['mi'], np.where(df['hlc3'] > df['hi'], 'lime', 'green'), np.where(df['hlc3'] < df['lo'], 'red', 'orange'))

        df['imp_mid']         = 0
        df['imp_macd']        = df['md']
        df['imp_macd_hist']   = df['sh']
        df['imp_macd_sign']   = df['sb']
        df['imp_macd_color']  = df['mdc']

        # Calculate the average intensity of the histogram over the last filter_period (e.g., 25 periods)
        df['hist_avg'] = df['sh'].rolling(window=filter_period).mean().abs() if hasattr(df['sh'].rolling(window=filter_period).mean(), 'abs') else np.abs(df['sh'].rolling(window=filter_period).mean())

        # Create conditions for Long and Short entries and exits with strength filter
        df['momentum_filter'] = (df['sh'].abs() > df['hist_avg'] * threshold) if filter_strength else True

        # MACD crosses above signal and momentum is strong
        df['Long_Enter'] = ((df['md'] > df['sb']) & (df['md'].shift(1) <= df['sb'].shift(1)) & df['momentum_filter']) & (df['mdc'] == 'line')

        # MACD crosses below signal
        df['Long_Exit'] = ((df['md'] < df['sb']) & (df['md'].shift(1) >= df['sb'].shift(1)))

        # MACD crosses below signal and momentum is strong
        df['Short_Enter'] = ((df['md'] < df['sb']) & (df['md'].shift(1) >= df['sb'].shift(1)) & df['momentum_filter']) & (df['mdc'] == 'red')

        # MACD crosses above signal
        df['Short_Exit'] = ((df['md'] > df['sb']) & (df['md'].shift(1) <= df['sb'].shift(1)))

        # Remove unnecessary columns
        for c in ('hlc3', 'hi', 'lo', 'md', 'sb', 'sh', 'hist_avg'):
            df.pop(c)
        

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_IMP_MACD PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_IMP_MACD PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_imp_macd() 975 leaving...')
    return df


#<=====>#


@narc(1)
def ta_add_bb(df: pd.DataFrame, per=20, sd=2, tag='') -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_bb(len(df={len(df)}), per={per}, sd={sd}, tag={tag})')
    try:

        per = min(per, len(df))

        # Calculate Bollinger Bands
        bbands = pta.bbands(df['close'], length=per, std=sd)

        # Extract upper and lower bands - check if bbands is not None
        if bbands is not None:
            df[f'bb_upper{tag}']      = bbands[f'BBU_{per}_{sd}']
            df[f'bb_lower{tag}']      = bbands[f'BBL_{per}_{sd}']
            df[f'bb_mid{tag}']        = bbands[f'BBM_{per}_{sd}']
            df[f'bb_width{tag}']      = bbands[f'BBB_{per}_{sd}']
            df[f'bb_pct{tag}']        = bbands[f'BBP_{per}_{sd}']
        else:
            # Handle case where bbands calculation fails
            df[f'bb_upper{tag}']      = None
            df[f'bb_lower{tag}']      = None
            df[f'bb_mid{tag}']        = None
            df[f'bb_width{tag}']      = None
            df[f'bb_pct{tag}']        = None

        # Calculate Rate of Change (ROC)
        df[f'bb_upper_roc{tag}']  = pta.roc(df[f'bb_upper{tag}'], length=3)
        df[f'bb_lower_roc{tag}']  = pta.roc(df[f'bb_lower{tag}'], length=3)

        # Determine if bands are expanding or contracting
        df[f'bb{tag}_expanding']   = (df[f'bb_upper_roc{tag}'] > 0) & (df[f'bb_lower_roc{tag}'] < 0)
        df[f'bb{tag}_contracting'] = (df[f'bb_upper_roc{tag}'] < 0) & (df[f'bb_lower_roc{tag}'] > 0)

        # Determine if bands are heading up or down
        df[f'bb{tag}_upwards']   = (df[f'bb_upper_roc{tag}'] > 0) & (df[f'bb_lower_roc{tag}'] > 0)
        df[f'bb{tag}_downwards'] = (df[f'bb_upper_roc{tag}'] < 0) & (df[f'bb_lower_roc{tag}'] < 0)
        

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_BB PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_BB PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_bb() 918 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_nwe(df: pd.DataFrame, src='close', bandwidth=8.0, mult=3.0, tag='', rfreq='') -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_nwe(len(df={len(df)}), src={src}, bandwidth={bandwidth}, mult={mult}, tag={tag}, rfreq={rfreq})')
    from scipy.ndimage import gaussian_filter1d

    try:
        # Parameters - Method 1
        h = bandwidth
        mult = mult
        source = df[src].values
        n = len(source)
        
        nwe = gaussian_filter1d(source, sigma=h, mode='nearest')

        df['nwe_line'] = nwe
        df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)

        # -------------------------------
        # Calculate Color & Signals
        # -------------------------------

        df['nwe_color'] = np.where(df['nwe_line'] > df['nwe_line'].shift(1), 'green', 'red')

        # Generate Buy and Sell Signals based on Color
        df['nwe_3row_buy_signal'] = (
            (df['nwe_color'] == 'green') &
            (df['nwe_color'].shift(1) == 'green') &
            (df['nwe_color'].shift(2) == 'green') &
            (df['nwe_roc'] >= 0) &
            (df['nwe_roc'].shift(1) >= 0)
            ).astype(int)
        # Generate Buy and Sell Signals based on Color
        df['nwe_3row_sell_signal'] = (
            (df['nwe_color'] == 'red') &
            (df['nwe_color'].shift(1) == 'red') &
            (df['nwe_color'].shift(2) == 'red') &
            (df['nwe_roc'] <= 0) &
            (df['nwe_roc'].shift(1) <= 0) 
            ).astype(int)

    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_NWE PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_NWE PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_nwe() 975 leaving...')
    return df

#<=====>#

@narc(1)
def ta_add_nwe_env(df: pd.DataFrame, src='close', mult=3.0) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_nwe_env(len(df={len(df)}), src={src}, mult={mult})')
    try:
        # -------------------------------
        # Calculate Envelope & Signals
        # -------------------------------
        source = df[src].values
        nwe    = df['nwe_line']
        # C(f'ta_base.ta_add_nwe_env() - made it here 1239')

        # Compute MAE as mean absolute error over the entire series
        mae = np.mean(np.abs(source - nwe)) * mult
        df['nwe_mae'] = mae
        # C(f'ta_base.ta_add_nwe_env() - made it here 1245')

        # Compute upper and lower bands
        df['nwe_upper'] = df['nwe_line'] + mae
        df['nwe_lower'] = df['nwe_line'] - mae
        # C(f'ta_base.ta_add_nwe_env() - made it here 1249')

        # Detect Buy Breach (mask + shifted mask)
        buy_breach_mask = (
            (df['low'] < df['nwe_lower']) |
            (df['low'].shift(1) < df['nwe_lower'].shift(1))
        )
        df['nwe_env_buy_breach'] = buy_breach_mask
        # C(f'ta_base.ta_add_nwe_env() - made it here 1256')

        # Compute global min depth once, then broadcast only to breach rows (vectorized)
        buy_depth_scalar = df[src].where(df[src] < df['nwe_lower']).min()
        df['nwe_env_buy_breach_depth'] = np.where(buy_breach_mask, buy_depth_scalar, np.nan)
        # C(f'ta_base.ta_add_nwe_env() - made it here 1263')

        # Generate Buy Signal from breach and recovery (vectorized)
        buy_depth_filled = df['nwe_env_buy_breach_depth'].fillna(df[src]).infer_objects(copy=False)
        df['nwe_env_buy_signal'] = (
            buy_breach_mask &
            (df['color'] == 'green') &
            (df[src] > buy_depth_filled)
        )
        # C(f'ta_base.ta_add_nwe_env() - made it here 1271')

        # Detect Sell Breach (mask + shifted mask)
        sell_breach_mask = (
            (df[src] > df['nwe_upper']) |
            (df[src].shift(1) > df['nwe_upper'].shift(1))
        )
        df['nwe_env_sell_breach'] = sell_breach_mask
        # C(f'ta_base.ta_add_nwe_env() - made it here 1277')

        # Compute global max height once, then broadcast only to breach rows (vectorized)
        sell_height_scalar = df[src].where(df[src] > df['nwe_upper']).max()
        df['nwe_env_sell_breach_height'] = np.where(sell_breach_mask, sell_height_scalar, np.nan)
        # C(f'ta_base.ta_add_nwe_env() - made it here 1285')

        # Generate Sell Signal from breach and recovery (vectorized)
        sell_height_filled = df['nwe_env_sell_breach_height'].fillna(df[src]).infer_objects(copy=False)
        df['nwe_env_sell_signal'] = (
            sell_breach_mask &
            (df['color'] == 'red') &
            (df[src] < sell_height_filled)
        )
        # C(f'ta_base.ta_add_nwe_env() - made it here 1293')

    # except Exception as e:
    except BaseException as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_NWE_ENV PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_NWE_ENV PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_nwe_env() 1134 leaving...')
    C(f'==> ta_base.ta_add_nwe_env() 1134 leaving...')
    return df

#<=====>#


@narc(1)
def ta_add_nwe_rev(df: pd.DataFrame) -> pd.DataFrame:
    if debug_tf: C(f'ta_base.ta_add_nwe_rev(len(df={len(df)})')
    try:
        # -------------------------------
        # Calculate Reversals & Signals
        # -------------------------------

        # Compute derivative of NWE line
        df['nwe_diff']            = df['nwe_line'].diff()
        df['nwe_diff_last']       = df['nwe_diff'].shift(1)
        # C(f'ta_base.ta_add_nwe_rev() - made it here 1327')

        # Detect reversal points
        df['reversal']            = (df['nwe_diff'] * df['nwe_diff_last'] < 0)
        df['reversal_up']         = df['reversal'] & (df['nwe_diff_last'] < 0)
        df['reversal_down']       = df['reversal'] & (df['nwe_diff_last'] > 0)
        # C(f'ta_base.ta_add_nwe_rev() - made it here 1333')

        # Generate Buy and Sell Signals based on reversals
        df['nwe_rev_buy_signal']  = df['reversal_up'].astype(int)
        df['nwe_rev_sell_signal'] = df['reversal_down'].astype(int)
        # C(f'ta_base.ta_add_nwe_rev() - made it here 1338')

    except BaseException as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL TA_ADD_NWE_REV PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"TA_ADD_NWE_REV PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if debug_tf: C(f'==> ta_base.ta_add_nwe_rev() 1277 leaving...')
    C(f'==> ta_base.ta_add_nwe_rev() 1353 leaving...')
    return df

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
