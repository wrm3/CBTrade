#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import numpy as np
import pandas as pd
import pandas_ta as pta
from scipy.ndimage import gaussian_filter1d
import traceback
import warnings
from datetime import datetime as dt, timedelta
import time

from libs.bot_coinbase import cb, cb_candles_get
#from libs.bot_db_read import db_ohlcv_freq_get, db_ohlcv_prod_id_freqs
#from libs.bot_db_write import db_tbl_ohlcv_prod_id_insupd_many


from libs.bot_db_ohlcv import (
    db_ohlcv_freq_get, 
    db_ohlcv_prod_id_freqs,
    db_tbl_ohlcv_prod_id_insupd_many
)

from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_common import dir_val, dttm_get, func_begin, func_end, print_adv
from libs.lib_dicts import AttrDict
from libs.lib_common import beep
from libs.lib_colors import G

warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_ta'
log_name      = 'bot_ta'
lib_secs_max  = 0

# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

def ta_main_new(pair, st):
	func_name = 'ta_main_new'
	func_str = f'{lib_name}.{func_name}(pair, st)'
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# t00 = time.perf_counter()

	try:

		prod_id     = pair.prod_id
		ta          = AttrDict()
		prc_mkt     = pair.prc_mkt
		rfreq       = ''
		df          = None
		dfs         = {}
		dfs_ins_many = {}


		# print('')
		# Getting the Candlestick Data
		# t0 = time.perf_counter()
		dfs = ta_ohlcv(pair, st)
		# t1 = time.perf_counter()
		# secs = round(t1 - t0, 2)
		# print(f'{func_name} - ta_ohlcv completed in {secs}')

		# Assigning the Real Time Close Price
		close_price = dfs['1min']['close'].iloc[-1]


		# print('')
		# database insert
		# t0 = time.perf_counter()
		rfreqs = ['1min','5min', '15min', '30min', '1h', '4h', '1d']
		for rfreq in rfreqs:
			dfs_ins_many[rfreq] = dfs[rfreq]
		db_tbl_ohlcv_prod_id_insupd_many(prod_id, dfs_ins_many)
		# t1 = time.perf_counter()
		# secs = round(t1 - t0, 2)
		# print(f'{func_name} - db_tbl_ohlcv_prod_id_insupd_many completed in {secs}')


		# print('')
		# reduced list, previous was used for forming current candles
		# t0 = time.perf_counter()
		rfreqs = ['5min', '15min', '30min', '1h', '4h', '1d']
		# Adding the Technical Analysis Indicators
		for rfreq in rfreqs:
			# t0 = time.perf_counter()
			ta[rfreq]            = AttrDict()
			ta[rfreq].df         = None
			ta[rfreq].curr       = AttrDict()
			ta[rfreq].last       = AttrDict()
			ta[rfreq].prev       = AttrDict()
			df = dfs[rfreq]
			df = ta_add_indicators(df, st, prc_mkt, rfreq)
			ta[rfreq].df = df
			for x in range(0,-6,-1):
				desc = f'ago{abs(x)}'
				y = x - 1
				for k in df:
					if not rfreq in ta: ta[rfreq] = AttrDict()
					if not k in ta[rfreq]: ta[rfreq][k] = AttrDict()
					ta[rfreq][k][desc] =  df[k].iloc[y]
			# t1 = time.perf_counter()
			# secs = round(t1 - t0, 2)
			# print(f'{func_name} - ta_add_indicators {rfreq} completed in {secs}')


		# Check that all forming candles have the same final close price since they are real time
		for rfreq in rfreqs:
			if ta[rfreq].df['close'].iloc[-1] != close_price:
				print(f"line 302 => rfreq : {rfreq}, end : {ta[rfreq].df.index.max()}, close_price : {close_price:>.8f}, close : {ta[rfreq].df['close'].iloc[-1]:>.8f}")
				print(f"Debug Info Final => {ta[rfreq].df.tail(5)}")  # Add this line for more debug info
				ta = 'Error!'
				break

	except Exception as e:
		print(f'{func_name} ==> errored... {e}')
		print(dttm_get())
		traceback.print_exc()
		print(type(e))
		print(e)
		print(f'rfreq {type(rfreq)} : {rfreq}')
		print(f'df {type(df)} :  {df}')
		ta = None

	# t01 = time.perf_counter()
	# secs = round(t01 - t00, 2)
	# print('')
	# print(f'{func_name} completed in {secs}')
	# print('')

	func_end(fnc)
	return ta

#<=====>#

def ta_ohlcv(pair, st):
	func_name = 'ta_ohlcv'
	func_str = f'{lib_name}.{func_name}(pair, st)'
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=2)
#	G(func_str)

#	t0 = time.perf_counter()
	try:

		prod_id     = pair.prod_id
		rfreq       = ''
		df          = None
		dfs         = {}

#		rfreqs = ['1min', '3min', '5min', '15min', '30min', '1h', '4h', '1d']
		rfreqs = ['1min', '5min', '15min', '30min', '1h', '4h', '1d']

		ohlcv_meths = {}

		ohlcv_last_dttms = db_ohlcv_prod_id_freqs(prod_id)

		utc_now = dt.utcnow()
		for freq in rfreqs:
			ohlcv_meth = {}
			ohlcv_meth['prod_id']       = prod_id
			ohlcv_meth['freq']          = freq
			ohlcv_meth['last_start_dttm'] = None

			for ohlcv_last_dttm in ohlcv_last_dttms:
				this_freq = ohlcv_last_dttm['freq']
				if this_freq == freq:
					ohlcv_meth['last_start_dttm'] = ohlcv_last_dttm['last_start_dttm']

			if freq == '1min':
				ohlcv_meth['elapsed_max']   = 60
#			elif freq == '3min':
#				ohlcv_meth['elapsed_max']   = 180
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
#			else:
#				print(f'elapsed since last api call : {ohlcv_meth['elapsed']}')

			ohlcv_meths[freq] = ohlcv_meth

#			print(ohlcv_meth)

		for freq in ohlcv_meths:
			if ohlcv_meths[freq]['method'] == 'api':
				msg = 'getting {} {} hist from api'.format(prod_id, freq)
				dfs[freq] = ta_df_api_get(prod_id, freq)
			else:
				msg = 'getting {} {} hist from db'.format(prod_id, freq)
				dfs[freq] = ta_df_hist_db(prod_id, freq)

		pair.dfs = dfs
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

			if rfreq == '1min':
				csv_fname = f'data/{pair.prod_id}_{rfreq}.csv'
				dir_val(csv_fname)
				dfs[rfreq].to_csv(csv_fname, index=True)

		# ensure we have a minimal number of rows
		for rfreq in rfreqs:
			if len(dfs[rfreq]) < 350:
				# print_adv()
				# print(f'df - {rfreq} has {len(dfs[rfreq])} rows before...')
				# print(dfs[rfreq].head(3))
				# print(dfs[rfreq].tail(3))
				# print_adv()
#				dfs[rfreq] = ta_df_fill_rows(df=dfs[rfreq], min_rows=500, time_index_col='timestamp')
				dfs[rfreq] = ta_df_fill_rows(df=dfs[rfreq], min_rows=200)
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

	except Exception as e:
		print(f'{func_name} ==> errored... {e}')
		print(dttm_get())
		traceback.print_exc()
		print(type(e))
		print(e)
		print(f'rfreq {type(rfreq)} : {rfreq}')
		print(f'df {type(df)} :  {df}')
		ta = None

		# Print most recent signal times
		signal_cols = [
			'nwe_rev_buy_signal', 
			'nwe_rev_sell_signal',
			'nwe_env_buy_signal', 
			'nwe_env_sell_signal',
			'nwe_combined_buy_signal',
			'nwe_combined_sell_signal'
		]
		
		for col in signal_cols:
			if df[col].any():  # Check if there are any signals
				last_signal = df[df[col] == 1].index[-1]
				print(f"Last {col}: {last_signal} {'↑' if 'buy' in col else '↓'}")

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return dfs

#<=====>#

def ta_ohlcv_range(prod_id, freq='1h', sd='2024-01-01', td='2024-12-31'):
	func_name = 'ta_ohlcv_range'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, freq={freq}, sd={sd}, td={td})'
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=2)
#	G(func_str)

#	t0 = time.perf_counter()
	df          = None
	sd          = int(pd.Timestamp(sd).timestamp())
	td          = int(pd.Timestamp(td).timestamp())
	df          = cb_candles_get(prod_id, start = sd, end = td, freq = freq)
	df          = ta_df_dropna(df)

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

# get basic know we need indicators
def ta_df_api_get(prod_id, rfreq) -> dict:
	func_name = 'ta_df_api_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, rfreq={rfreq})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# t0 = time.perf_counter()
	# print_adv(2)
	df_db  = ta_df_hist_db(prod_id, rfreq)
	df_api = cb_candles_get(product_id=prod_id, rfreq=rfreq, min_rows=299)
	df_db  = ta_df_dropna(df_db)
	df_api = ta_df_dropna(df_api)
	# print(f'df_db  : {df_db.head(3)}')
	# print(f'df_db  : {df_db.tail(3)}')
	# print(f'df_db  : {len(df_db)}')
	# print(f'df_db  : {len(df_db)}')
	# print(f'df_api : {df_api.head(3)}')
	# print(f'df_api : {df_api.tail(3)}')
	# print(f'df_api : {len(df_api)}')
	# print(f'df_api  : {len(df_api)}')
	if len(df_db) > 0:
		df = ta_df_merge_db_and_api(prod_id, rfreq, df_db, df_api)
	else:
		df = df_api
	# print(f'df      : {df.head(3)}')
	# print(f'df      : {df.tail(3)}')
	# print(f'df      : {len(df)}')
	df = ta_df_dropna(df)
	# print(f'df  : {len(df_api)}')

	# t1 = time.perf_counter()
	# secs = round(t1 - t0, 2)
	# print(f'{func_name} {rfreq} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

def ta_df_hist_db(prod_id, freq):
	func_name = "ta_df_hist_db"
	func_str = f"{lib_name}.{func_name}(prod_id={prod_id}, freq={freq})"
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# t0 = time.perf_counter()
	df = None
	try:
		hist = db_ohlcv_freq_get(prod_id, freq, lmt=500)

		hdata = []

		for h in hist:
			hdict = {}
			hdict['timestamp']  = h['timestamp']
			hdict['open']       = float(h['open'])
			hdict['high']       = float(h['high'])
			hdict['low']        = float(h['low'])
			hdict['close']      = float(h['close'])
			hdict['volume']     = float(h['volume'])
			hdata.append(hdict)

		df = pd.DataFrame(hdata, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
		df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
		df.set_index('timestamp', inplace=True)

		d = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}

		roffset = None
		if roffset:
			df = df.resample(freq, offset=roffset).agg(d)
		else:
			df = df.resample(freq).agg(d)

		# print(f'before dropna {len(df)}')
		# print(df.head(3))
		# print(df.tail(3))
		df = ta_df_dropna(df)
		# print(f'after dropna {len(df)}')
		# print(df.head(3))
		# print(df.tail(3))

	except Exception:
		print(func_name + 'errored.')
		beep()
		raise
		exit()

	# t1 = time.perf_counter()
	# secs = round(t1 - t0, 2)
	# print(f'{func_name} {freq} completed in {secs}')

	fnc = func_end(fnc)
	return df

#<=====>#

# get basic know we need indicators
def ta_df_fill_rows(df, min_rows=300, time_index_col=None) -> dict:
	func_name = 'ta_df_fill_rows'
	func_str = f'{lib_name}.{func_name}(min_rows={min_rows}, time_index_col={time_index_col})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	
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

	# Calculate the frequency
	if len(datetime_series) > 1:
		freq = datetime_series[1] - datetime_series[0]
	else:
		# If only one row, default to a daily frequency
		freq = pd.Timedelta('1D')

	# Get the oldest timestamp
	oldest_timestamp = datetime_series[0]

	# Generate new timestamps stepping backward
	new_timestamps = [oldest_timestamp - freq * i for i in range(delta, 0, -1)]

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

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#


def ta_df_dropna(df, cols=['open', 'high', 'low', 'close', 'volume']):
	func_name = 'ta_df_dropna'
	func_str = f'{lib_name}.{func_name}(df)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	df = df.dropna(subset=cols)
	df = df[(df[cols] != 0).any(axis=1)]

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#


def ta_df_merge_db_and_api(prod_id, freq, df_db, df_api):
	func_name = 'ta_df_merge_db_and_api'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, freq={freq})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# t0 = time.perf_counter()
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

	try:
		# Fetch data from the database
#		df_db = ta_df_hist_db(prod_id, freq)
		# Fetch data from the API
#		df_api = ta_df_api_get(prod_id, freq)

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
		df_merged = pd.concat([df_db, df_api]).sort_index()

#		# Update the database with the merged data
#		db_tbl_ohlcv_prod_id_insupd_many(prod_id, {freq: df_merged})

	except Exception as e:
		print(f'{func_name} ==> errored... {e}')
		traceback.print_exc()
		df_merged = None

	# t1 = time.perf_counter()
	# secs = round(t1 - t0, 2)
	# print(f'{func_name} {freq} completed in {secs}')

	func_end(fnc)
	return df_merged

#<=====>#

# get basic know we need indicators
def ta_add_indicators(df: pd.DataFrame, st, prc_mkt, rfreq) -> pd.DataFrame:
	func_name = 'ta_add_indicators'
	func_str = f'{lib_name}.{func_name}(df, st, prc_mkt={prc_mkt}, rfreq={rfreq})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	df['hl2']   = (df['high'] + df['low']) / 2
	df['hlc3']  = (df['high'] + df['low'] + df['close']) / 3
	df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
	df['hlcc4'] = (df['high'] + df['low'] + df['close'] + df['close']) / 3

	df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])
	df = df[(df[['open', 'high', 'low', 'close', 'volume']] != 0).any(axis=1)]

	if len(df) < 10:
		print('error gettings candles...')
		# t1 = time.perf_counter()
		# secs = round(t1 - t0, 2)
		# print(f'{func_name} completed in {secs}')
		func_end(fnc)
		return 'N','Y'

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

	# # Simple Moving Averages - Fibonacci
	# for per in (5, 8, 13, 21, 34, 55, 89, 100, 150, 200, 300):
	# 	df = ta_add_sma(df, per, col='close', label=f'sma{per}')

	# # Exponential Moving Averages - Fibonacci
	# for per in (5, 8, 13, 21, 34, 55, 89, 100, 150, 200, 300):
	# 	df = ta_add_ema(df, per, col='close', label=f'ema{per}')

	try:
		# New Strat Add Section
		# STRAT SHA
		# Smoothed Heikin Ashi Candles
		fast_sha_len1 = st.buy.strats.sha.fast_sha_len1 # 8
		fast_sha_len2 = st.buy.strats.sha.fast_sha_len2 # 8
		slow_sha_len1 = st.buy.strats.sha.slow_sha_len1 # 21
		slow_sha_len2 = st.buy.strats.sha.slow_sha_len2 # 21
		df = ta_add_sha(df, prc_mkt, sha_len1=fast_sha_len1, sha_len2=fast_sha_len2, tag='_fast')
		df = ta_add_sha(df, prc_mkt, sha_len1=slow_sha_len1, sha_len2=slow_sha_len2, tag='_slow')
	except Exception as e:
		traceback.print_exc()
		traceback.print_stack()
		print('error getting SHA...')
		beep(4)

	# STRAT IMP MACD
	per_ma   = st.buy.strats.imp_macd.per_ma   # 34 
	per_sign = st.buy.strats.imp_macd.per_sign # 9 
	df = ta_add_imp_macd(df, per_ma=per_ma, per_sign=per_sign)

	# STRAT BB
	inner_per = st.buy.strats.bb.inner_per # 21 
	inner_sd  = st.buy.strats.bb.inner_sd  # 2.3 
	outer_per = st.buy.strats.bb.outer_per # 21 
	outer_sd  = st.buy.strats.bb.outer_sd  # 2.7 
	df = ta_add_bb(df, per=inner_per, sd=inner_sd, tag='_inner')
	df = ta_add_bb(df, per=outer_per, sd=outer_sd, tag='_outer')

	# STRAT BB BO
	per = st.buy.strats.bb_bo.per # 21 
	sd  = st.buy.strats.bb_bo.sd  # 2.5 
	df = ta_add_bb(df, per=per, sd=sd, tag='_bb_bo')

	nwe_bw = 8
	df = ta_add_nwe(df, src='close', bandwidth=nwe_bw, tag='', rfreq=rfreq)
	df = ta_add_nwe_env(df, src='close', mult=3.0)
	df = ta_add_nwe_rev(df)

	# Highest, Lowest
	for x in (7,24,30):
		df[f'max{x}'] = df['high'].rolling(window=x).max()
		df[f'min{x}'] = df['low'].rolling(window=x).min()

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

def ta_add_color(df: pd.DataFrame) -> pd.DataFrame:
	func_name = 'ta_add_color'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	df['color'] = np.where(df['open'] < df['close'], 'green', 'red')

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

# Heiki Ashi
def ta_add_ha(df: pd.DataFrame) -> pd.DataFrame:
	func_name = 'ta_add_ha'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
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

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

# Average True Range
def ta_add_atr(df: pd.DataFrame, per=14) -> pd.DataFrame:
	func_name = 'ta_add_atr'
	func_str = f'{lib_name}.{func_name}(per={per})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	per = min(per, len(df))

	df['atr'] = pta.atr(high=df['high'], low=df['low'], close=df['close'], length=per, mamode='SMA')

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

def ta_add_rsi(df: pd.DataFrame, per=14) -> pd.DataFrame:
	func_name = 'ta_add_rsi'
	func_str = f'{lib_name}.{func_name}(per={per})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	per = min(per, len(df))

	df['rsi'] = pta.rsi(df['close'], length=per)

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

# Rate of Change
def ta_add_roc(df: pd.DataFrame, col='close', label=None, per=3) -> pd.DataFrame:
	func_name = 'ta_add_roc'
	func_str = f'{lib_name}.{func_name}(col={col}, label={label}, per={per})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	per = min(per, len(df))

	if not label:
		label = col

	label2 = f'{label}_roc'
	df[label2]                  = pta.roc(df[label], length=3)

	label3 = f'{label}_roc_up'
	df[label3]                  = df[label2]  > df[label2].shift(1)

	label4 = f'{label}_roc_dn'
	df[label4]                  = df[label2]  < df[label2].shift(1)

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

# Simple Moving Average
def ta_add_sma(df: pd.DataFrame, per, col='close', label=None) -> pd.DataFrame:
	func_name = 'ta_add_sma'
	func_str = f'{lib_name}.{func_name}(per={per}, col={col}, label={label})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	per = min(per, len(df))

	if not label:
		label = f'{col}_sma{per}'

	df[label]                   = pta.sma(df['close'], length=per)

	df = ta_add_roc(df, col=label)

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

# Exponential Moving Average
def ta_add_ema(df: pd.DataFrame, per, col='close', label=None) -> pd.DataFrame:
	func_name = 'ta_add_emas'
	func_str = f'{lib_name}.{func_name}(per={per}, col={col}, label={label})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	per = min(per, len(df))

	if not label:
		label = f'{col}_ema{per}'

	df[label]                   = pta.ema(df[col], length=per)

	df = ta_add_roc(df, col=label)

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

# Smoothed Heiki Ashi
def ta_add_sha(df: pd.DataFrame, prc_mkt, sha_len1=5, sha_len2=8, tag=None) -> pd.DataFrame:
	func_name = 'ta_add_sha'
	func_str = f'{lib_name}.{func_name}(df, prc_mkt={prc_mkt}, sha_len1={sha_len1}, sha_len2={sha_len2}, tag={tag})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	sha_len1 = min(sha_len1, len(df))
	sha_len2 = min(sha_len2, len(df))

	# Calculate EMAs for the original OHLC values
	df['ema_open']                        = df['open'].ewm(span=sha_len1, adjust=False).mean()
	df['ema_close']                       = df['close'].ewm(span=sha_len1, adjust=False).mean()
	df['ema_high']                        = df['high'].ewm(span=sha_len1, adjust=False).mean()
	df['ema_low']                         = df['low'].ewm(span=sha_len1, adjust=False).mean()

	# Calculate Heiken Ashi Close
	df['ha_ema_close']                    = (df['ema_open'] + df['ema_high'] + df['ema_low'] + df['ema_close']) / 4

	# Initialize 'ha_ema_open' with NaNs and then set the first valid value after 'sha_len1' periods
	df['ha_ema_open']                     = np.nan
	df.at[df.index[sha_len1], 'ha_ema_open'] = (df.at[df.index[sha_len1], 'ema_open'] + df.at[df.index[sha_len1], 'ema_close']) / 2

	# Calculate HA_Open using a loop (due to dependency on previous rows), starting after 'sha_len1'
	for i in range(sha_len1 + 1, len(df)):
		df.at[df.index[i], 'ha_ema_open'] = (df.at[df.index[i-1], 'ha_ema_open'] + df.at[df.index[i-1], 'ha_ema_close']) / 2

	# Calculate HA_High and HA_Low
	df['ha_ema_high']                     = df[['ema_high', 'ha_ema_open', 'ha_ema_close']].max(axis=1)
	df['ha_ema_low']                      = df[['ema_low', 'ha_ema_open', 'ha_ema_close']].min(axis=1)

	# Calculate EMAs for the Heiken Ashi OHLC values
	df['sha_open']                = df['ha_ema_open'].ewm(span=sha_len2, adjust=False).mean()
	df['sha_close']               = df['ha_ema_close'].ewm(span=sha_len2, adjust=False).mean()
	df['sha_high']                = df['ha_ema_high'].ewm(span=sha_len2, adjust=False).mean()
	df['sha_low']                 = df['ha_ema_low'].ewm(span=sha_len2, adjust=False).mean()

	# Smoothed Heikin Ashi Candle Colors
	# You might adjust the color coding logic based on how you want to visualize or use these values
	df['sha_color']               = np.where(df['sha_open'] < df['sha_close'], 'green', 'red')

	# Assuming the intention is to calculate the body size of the smoothed HA candle
	df['sha_body']                = (df['sha_close'] - df['sha_open']).abs()
	# The upper wick is the distance between the high price and the maximum of the open and close of the smoothed HA candle
	df['sha_wick_upper']          = df['sha_high'] - df[['sha_open', 'sha_close']].max(axis=1)
	# The lower wick is the distance between the low price and the minimum of the open and close of the smoothed HA candle
	df['sha_wick_lower']          = df[['sha_open', 'sha_close']].min(axis=1) - df['sha_low']

	# The 'df' DataFrame now includes smoothed Heiken Ashi OHLC values and colors.
	# removing unneeded columns used for calculation
	for c in('ema_open', 'ema_close', 'ema_high', 'ema_low','ha_ema_open', 'ha_ema_close', 'ha_ema_high', 'ha_ema_low'):
		df.pop(c)

	df['prc_abv_sha']               = prc_mkt > df['sha_close']
	df['prc_bel_sha']               = prc_mkt < df['sha_close']

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

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

# # Impulse MACD
# def ta_add_imp_macd(df: pd.DataFrame, per_ma=34, per_sign=9) -> pd.DataFrame:
# 	func_name = 'ta_add_imp_macd'
# 	func_str = f'{lib_name}.{func_name}(df, per_ma={per_ma}, per_sign={per_sign})'
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# #	G(func_str)

#	t0 = time.perf_counter()
# 	per_ma = min(per_ma, len(df))
# 	per_sign = min(per_sign, len(df))

# 	def calc_smma(src, length):
# 		smma = np.zeros_like(src)
# 		smma[0] = np.mean(src[:length])
# 		for i in range(1, len(src)):
# 			smma[i] = (smma[i-1] * (length - 1) + src.iloc[i]) / length
# 		return smma

# 	def calc_zlema(src, per):
# 		per = min(per, len(src))
# 		ema1 = pta.ema(src, length=per)
# 		ema2 = pta.ema(ema1, length=per)
# 		d = ema1 - ema2
# 		return ema1 + d

# 	df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3

# 	df['hi'] = calc_smma(df['high'], per_ma)
# 	df['lo'] = calc_smma(df['low'], per_ma)
# 	df['mi'] = calc_zlema(df['hlc3'], per_ma)

# 	df['md'] = np.where(df['mi'] > df['hi'], df['mi'] - df['hi'], np.where(df['mi'] < df['lo'], df['mi'] - df['lo'], 0))
# 	df['sb'] = pta.sma(df['md'], length=per_sign)
# 	df['sh'] = df['md'] - df['sb']

# 	df['mdc'] = np.where(df['hlc3'] > df['mi'], np.where(df['hlc3'] > df['hi'], 'lime', 'green'), np.where(df['hlc3'] < df['lo'], 'red', 'orange'))

# 	df['imp_mid']         = 0
# 	df['imp_macd']        = df['md']
# 	df['imp_macd_hist']   = df['sh']
# 	df['imp_macd_sign']   = df['sb']
# 	df['imp_macd_color']  = df['mdc']


# 	df['Long_Enter']   = 1 == 1
# 	df['Long_Exit']    = 1 == 1
# 	df['Short_Enter']  = 1 == 1
# 	df['Short_Exit']   = 1 == 1


# #	for c in('hlc3', 'hi', 'lo', 'mi','md', 'sb', 'sh', 'mdc'):
# 	for c in('hlc3', 'hi', 'lo','md', 'sb', 'sh', 'mdc'):
# 		df.pop(c)

# 	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
# 	return df


#<=====>#

# Impulse MACD with filter for strong momentum
def ta_add_imp_macd(df: pd.DataFrame, per_ma=34, per_sign=9, filter_strength=True, filter_period=25, threshold=0.5) -> pd.DataFrame:
	func_name = 'ta_add_imp_macd'
	func_str = f'{lib_name}.{func_name}(df, per_ma={per_ma}, per_sign={per_sign})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()

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
	df['hist_avg'] = df['sh'].rolling(window=filter_period).mean().abs()

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

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df


#<=====>#

# Bollinger Bands
def ta_add_bb(df: pd.DataFrame, per=20, sd=2, tag='') -> pd.DataFrame:
	func_name = 'ta_add_bbs'
	func_str = f'{lib_name}.{func_name}(df, per={per}, sd={sd}, tag={tag})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()
	per = min(per, len(df))

	# Calculate Bollinger Bands
	bbands                    = pta.bbands(df['close'], length=per, std=sd)

	# Extract upper and lower bands
	df[f'bb_upper{tag}']      = bbands[f'BBU_{per}_{sd}']
	df[f'bb_lower{tag}']      = bbands[f'BBL_{per}_{sd}']
	df[f'bb_mid{tag}']        = bbands[f'BBM_{per}_{sd}']
	df[f'bb_width{tag}']      = bbands[f'BBB_{per}_{sd}']
	df[f'bb_pct{tag}']        = bbands[f'BBP_{per}_{sd}']

	# Calculate Rate of Change (ROC)
	df[f'bb_upper_roc{tag}']  = pta.roc(df[f'bb_upper{tag}'], length=3)
	df[f'bb_lower_roc{tag}']  = pta.roc(df[f'bb_lower{tag}'], length=3)

	# Determine if bands are expanding or contracting
	df[f'bb{tag}_expanding']   = (df[f'bb_upper_roc{tag}'] > 0) & (df[f'bb_lower_roc{tag}'] < 0)
	df[f'bb{tag}_contracting'] = (df[f'bb_upper_roc{tag}'] < 0) & (df[f'bb_lower_roc{tag}'] > 0)

	# Determine if bands are heading up or down
	df[f'bb{tag}_upwards']   = (df[f'bb_upper_roc{tag}'] > 0) & (df[f'bb_lower_roc{tag}'] > 0)
	df[f'bb{tag}_downwards'] = (df[f'bb_upper_roc{tag}'] < 0) & (df[f'bb_lower_roc{tag}'] < 0)

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

def ta_add_nwe(df: pd.DataFrame, src='close', bandwidth=8.0, mult=3.0, tag='', rfreq='') -> pd.DataFrame:
	func_name = 'ta_add_nwe'
	func_str = f'{lib_name}.{func_name}(df, src={src}, bandwidth={bandwidth}, tag={tag})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()

	from scipy.ndimage import gaussian_filter1d

	try:
		# Parameters - Method 1
		h = bandwidth
		mult = mult
		source = df[src].values
		n = len(source)
		
		nwe = gaussian_filter1d(source, sigma=h, mode='nearest')

		# Parameters - Method 2
		# h = bandwidth
		# source = df[src].values
		# n = len(source)
		# nwe = np.zeros(n)
		# half_window = 499  # Max bars back as in PineScript
		# # Precompute the Gaussian weights for efficiency
		# x = np.arange(-half_window, half_window + 1)
		# gauss_weights = np.exp(- (x ** 2) / (2 * h * h))
		# for i in range(n):
		# 	# Define the window boundaries
		# 	start_idx = max(0, i - half_window)
		# 	end_idx = min(n, i + half_window + 1)
		# 	window_size = end_idx - start_idx
		# 	# Adjust weights for the window
		# 	weights = gauss_weights[half_window - (i - start_idx):half_window + (end_idx - i)]
		# 	window_data = source[start_idx:end_idx]
		# 	# Compute NWE for the current point
		# 	sumw = np.sum(weights)
		# 	sumwx = np.sum(window_data * weights)
		# 	nwe[i] = sumwx / sumw if sumw != 0 else source[i]


		df['nwe_line'] = nwe
		df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)

		'''
		// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
		// © LuxAlgo

		//@version=5
		indicator("Nadaraya-Watson Envelope [LuxAlgo]", "LuxAlgo - Nadaraya-Watson Envelope", overlay = true, max_lines_count = 500, max_labels_count = 500, max_bars_back=500)
		//------------------------------------------------------------------------------
		//Settings
		//-----------------------------------------------------------------------------{
		h = input.float(8.,'Bandwidth', minval = 0)
		mult = input.float(3., minval = 0)
		src = input(close, 'Source')

		repaint = input(true, 'Repainting Smoothing', tooltip = 'Repainting is an effect where the indicators historical output is subject to change over time. Disabling repainting will cause the indicator to output the endpoints of the calculations')

		//Style
		upCss = input.color(color.teal, 'Colors', inline = 'inline1', group = 'Style')
		dnCss = input.color(color.red, '', inline = 'inline1', group = 'Style')

		//-----------------------------------------------------------------------------}
		//Functions
		//-----------------------------------------------------------------------------{
		//Gaussian window
		gauss(x, h) => math.exp(-(math.pow(x, 2)/(h * h * 2)))

		//-----------------------------------------------------------------------------}
		//Append lines
		//-----------------------------------------------------------------------------{
		n = bar_index

		var ln = array.new_line(0) 

		if barstate.isfirst and repaint
			for i = 0 to 499
				array.push(ln,line.new(na,na,na,na))

		//-----------------------------------------------------------------------------}
		//End point method
		//-----------------------------------------------------------------------------{
		var coefs = array.new_float(0)
		var den = 0.

		if barstate.isfirst and not repaint
			for i = 0 to 499
				w = gauss(i, h)
				coefs.push(w)

			den := coefs.sum()

		out = 0.
		if not repaint
			for i = 0 to 499
				out += src[i] * coefs.get(i)
		out /= den
		mae = ta.sma(math.abs(src - out), 499) * mult

		upper = out + mae
		lower = out - mae
		
		//-----------------------------------------------------------------------------}
		//Compute and display NWE
		//-----------------------------------------------------------------------------{
		float y2 = na
		float y1 = na

		nwe = array.new<float>(0)
		if barstate.islast and repaint
			sae = 0.
			//Compute and set NWE point 
			for i = 0 to math.min(499,n - 1)
				sum = 0.
				sumw = 0.
				//Compute weighted mean 
				for j = 0 to math.min(499,n - 1)
					w = gauss(i - j, h)
					sum += src[j] * w
					sumw += w

				y2 := sum / sumw
				sae += math.abs(src[i] - y2)
				nwe.push(y2)
			
			sae := sae / math.min(499,n - 1) * mult
			for i = 0 to math.min(499,n - 1)
				if i%2
					line.new(n-i+1, y1 + sae, n-i, nwe.get(i) + sae, color = upCss)
					line.new(n-i+1, y1 - sae, n-i, nwe.get(i) - sae, color = dnCss)
				
				if src[i] > nwe.get(i) + sae and src[i+1] < nwe.get(i) + sae
					label.new(n-i, src[i], '▼', color = color(na), style = label.style_label_down, textcolor = dnCss, textalign = text.align_center)
				if src[i] < nwe.get(i) - sae and src[i+1] > nwe.get(i) - sae
					label.new(n-i, src[i], '▲', color = color(na), style = label.style_label_up, textcolor = upCss, textalign = text.align_center)
				
				y1 := nwe.get(i)

		//-----------------------------------------------------------------------------}
		//Dashboard
		//-----------------------------------------------------------------------------{
		var tb = table.new(position.top_right, 1, 1
		, bgcolor = #1e222d
		, border_color = #373a46
		, border_width = 1
		, frame_color = #373a46
		, frame_width = 1)

		if repaint
			tb.cell(0, 0, 'Repainting Mode Enabled', text_color = color.white, text_size = size.small)

		//-----------------------------------------------------------------------------}
		//Plot
		//-----------------------------------------------------------------------------}
		plot(repaint ? na : out + mae, 'Upper', upCss)
		plot(repaint ? na : out - mae, 'Lower', dnCss)

		//Crossing Arrows
		plotshape(ta.crossunder(close, out - mae) ? low : na, "Crossunder", shape.labelup, location.absolute, color(na), 0 , text = '▲', textcolor = upCss, size = size.tiny)
		plotshape(ta.crossover(close, out + mae) ? high : na, "Crossover", shape.labeldown, location.absolute, color(na), 0 , text = '▼', textcolor = dnCss, size = size.tiny)

		//-----------------------------------------------------------------------------}
		'''

		# -------------------------------
		# Calculate Color & Signals
		# -------------------------------

		# Color based on trend
#		df['nwe_color'] = np.where(df['nwe_diff'] > 0, 'green', 'red')
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
			(df['nwe_roc'].shift(1) <= 0) &
			(df['nwe_roc'].shift(2) <= 0)
			).astype(int)

	except Exception as e:
		print(f"{dttm_get()} {func_name} ==> Error: {e}")
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

def ta_add_nwe_env(df: pd.DataFrame, src='close', mult=3.0) -> pd.DataFrame:
	func_name = 'ta_add_nwe_env'
	func_str = f'{lib_name}.{func_name}(df, src={src})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()

	try:
		'''
		// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
		// © LuxAlgo

		//@version=5
		indicator("Nadaraya-Watson Smoothers [LuxAlgo]", "LuxAlgo - Nadaraya-Watson Smoothers", overlay = true, max_lines_count = 500, max_labels_count = 500, max_bars_back=500)
		//------------------------------------------------------------------------------
		//Settings
		//-----------------------------------------------------------------------------{
		h = input.float(8.,'Bandwidth', minval = 0)
		src = input(close,'Source')

		repaint = input(true, 'Repainting Smoothing', tooltip = 'Repainting is an effect where the indicators historical output is subject to change over time. Disabling repainting will cause the indicator to output the endpoint of the estimator')

		//Style
		upCss = input.color(color.teal, 'Colors', inline = 'inline1', group = 'Style')
		dnCss = input.color(color.red, '', inline = 'inline1', group = 'Style')

		//-----------------------------------------------------------------------------}
		//Functions
		//-----------------------------------------------------------------------------{
		//Gaussian window
		gauss(x, h) => math.exp(-(math.pow(x, 2)/(h * h * 2)))

		//-----------------------------------------------------------------------------}
		//Append lines
		//-----------------------------------------------------------------------------{
		n = bar_index

		var ln = array.new_line(0) 

		if barstate.isfirst and repaint
			for i = 0 to 499
				array.push(ln,line.new(na,na,na,na))

		//-----------------------------------------------------------------------------}
		//End point method
		//-----------------------------------------------------------------------------{
		var coefs = array.new_float(0)
		var den = 0.

		if barstate.isfirst and not repaint
			for i = 0 to 499
				w = gauss(i, h)
				coefs.push(w)

			den := coefs.sum()

		out = 0.
		if not repaint
			for i = 0 to 499
				out += src[i] * coefs.get(i)
		out /= den
		
		//-----------------------------------------------------------------------------}
		//Compute and display NWE
		//-----------------------------------------------------------------------------{
		float y2 = na
		float y1 = na
		float y1_d = na
		line l = na
		label lb = na

		if barstate.islast and repaint
			//Compute and set NWE point 
			for i = 0 to math.min(499,n - 1)
				sum = 0.
				sumw = 0.
				//Compute weighted mean 
				for j = 0 to math.min(499,n - 1)
					w = gauss(i - j, h)
					sum += src[j] * w
					sumw += w

				y2 := sum / sumw
				d = y2 - y1
				
				//Set coordinate line
				l := array.get(ln,i)
				line.set_xy1(l,n-i+1,y1)
				line.set_xy2(l,n-i,y2)
				line.set_color(l,y2 > y1 ? dnCss : upCss)
				line.set_width(l,2)
				
				if d * y1_d < 0
					label.new(n-i+1, src[i], y1_d < 0 ? '▲' : '▼'
					, color = color(na)
					, style = y1_d < 0 ? label.style_label_up : label.style_label_down
					, textcolor = y1_d < 0 ? upCss : dnCss
					, textalign = text.align_center)

				y1 := y2
				y1_d := d

		//-----------------------------------------------------------------------------}
		//Dashboard
		//-----------------------------------------------------------------------------{
		var tb = table.new(position.top_right, 1, 1, bgcolor = #1e222d, border_color = #373a46, border_width = 1, frame_color = #373a46, frame_width = 1)

		if repaint
			tb.cell(0, 0, 'Repainting Mode Enabled', text_color = color.white, text_size = size.small)

		//-----------------------------------------------------------------------------}
		//Plot
		//-----------------------------------------------------------------------------}
		plot(repaint ? na : out, 'NWE Endpoint Estimator', out > out[1] ? upCss : dnCss)

		//-----------------------------------------------------------------------------}
		'''

		# -------------------------------
		# Calculate Envelope & Signals
		# -------------------------------
		source = df[src].values
		nwe    = df['nwe_line']

		# Compute MAE as mean absolute error over the entire series
		mae = np.mean(np.abs(source - nwe)) * mult
		df['nwe_mae'] = mae
		
		# Compute upper and lower bands
		df['nwe_upper'] = df['nwe_line'] + mae
		df['nwe_lower'] = df['nwe_line'] - mae

		# Detect Buy Breach
		df['nwe_env_buy_breach'] = (
			(df['low'] < df['nwe_lower']) | 
			(df['low'].shift(1) < df['nwe_lower'].shift(1))
			)
		# Detect Buy Breach Depth
		df['nwe_env_buy_breach_depth'] = df.apply(
			lambda row: df[src][(df[src] < df['nwe_lower'])].min() if row['nwe_env_buy_breach'] else None,
			axis=1
		)
		# Generate Buy Signal from breach and recovery
		df['nwe_env_buy_signal'] = (
			(df['nwe_env_buy_breach']) &
			(df['color'] == 'green') &
			(df[src] > df['nwe_env_buy_breach_depth'].fillna(df[src]))
			)

		# Detect Sell Breach
		df['nwe_env_sell_breach'] = (
			(df[src] > df['nwe_upper']) | 
			(df[src].shift(1) > df['nwe_upper'].shift(1))
			)
		# Detect Sell Breach Height
		df['nwe_env_sell_breach_height'] = df.apply(
			lambda row: df[src][(df[src] > df['nwe_upper'])].max() if row['nwe_env_sell_breach'] else None,
			axis=1
		)
		# Generate Sell Signal from breach and recovery
		df['nwe_env_sell_signal'] = (
			(df['nwe_env_sell_breach']) &
			(df['color'] == 'red') &
			(df[src] < df['nwe_env_sell_breach_height'].fillna(df[src]))
			)

	except Exception as e:
		print(f"{dttm_get()} {func_name} ==> Error: {e}")
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

def ta_add_nwe_rev(df: pd.DataFrame) -> pd.DataFrame:
	func_name = 'ta_add_nwe_rev'
	func_str = f'{lib_name}.{func_name}(df)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()

	try:
		'''
		// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
		// © LuxAlgo

		//@version=5
		indicator("Nadaraya-Watson Envelope [LuxAlgo]", "LuxAlgo - Nadaraya-Watson Envelope", overlay = true, max_lines_count = 500, max_labels_count = 500, max_bars_back=500)
		//------------------------------------------------------------------------------
		//Settings
		//-----------------------------------------------------------------------------{
		h = input.float(8.,'Bandwidth', minval = 0)
		mult = input.float(3., minval = 0)
		src = input(close, 'Source')

		repaint = input(true, 'Repainting Smoothing', tooltip = 'Repainting is an effect where the indicators historical output is subject to change over time. Disabling repainting will cause the indicator to output the endpoints of the calculations')

		//Style
		upCss = input.color(color.teal, 'Colors', inline = 'inline1', group = 'Style')
		dnCss = input.color(color.red, '', inline = 'inline1', group = 'Style')

		//-----------------------------------------------------------------------------}
		//Functions
		//-----------------------------------------------------------------------------{
		//Gaussian window
		gauss(x, h) => math.exp(-(math.pow(x, 2)/(h * h * 2)))

		//-----------------------------------------------------------------------------}
		//Append lines
		//-----------------------------------------------------------------------------{
		n = bar_index

		var ln = array.new_line(0) 

		if barstate.isfirst and repaint
			for i = 0 to 499
				array.push(ln,line.new(na,na,na,na))

		//-----------------------------------------------------------------------------}
		//End point method
		//-----------------------------------------------------------------------------{
		var coefs = array.new_float(0)
		var den = 0.

		if barstate.isfirst and not repaint
			for i = 0 to 499
				w = gauss(i, h)
				coefs.push(w)

			den := coefs.sum()

		out = 0.
		if not repaint
			for i = 0 to 499
				out += src[i] * coefs.get(i)
		out /= den
		mae = ta.sma(math.abs(src - out), 499) * mult

		upper = out + mae
		lower = out - mae
		
		//-----------------------------------------------------------------------------}
		//Compute and display NWE
		//-----------------------------------------------------------------------------{
		float y2 = na
		float y1 = na

		nwe = array.new<float>(0)
		if barstate.islast and repaint
			sae = 0.
			//Compute and set NWE point 
			for i = 0 to math.min(499,n - 1)
				sum = 0.
				sumw = 0.
				//Compute weighted mean 
				for j = 0 to math.min(499,n - 1)
					w = gauss(i - j, h)
					sum += src[j] * w
					sumw += w

				y2 := sum / sumw
				sae += math.abs(src[i] - y2)
				nwe.push(y2)
			
			sae := sae / math.min(499,n - 1) * mult
			for i = 0 to math.min(499,n - 1)
				if i%2
					line.new(n-i+1, y1 + sae, n-i, nwe.get(i) + sae, color = upCss)
					line.new(n-i+1, y1 - sae, n-i, nwe.get(i) - sae, color = dnCss)
				
				if src[i] > nwe.get(i) + sae and src[i+1] < nwe.get(i) + sae
					label.new(n-i, src[i], '▼', color = color(na), style = label.style_label_down, textcolor = dnCss, textalign = text.align_center)
				if src[i] < nwe.get(i) - sae and src[i+1] > nwe.get(i) - sae
					label.new(n-i, src[i], '▲', color = color(na), style = label.style_label_up, textcolor = upCss, textalign = text.align_center)
				
				y1 := nwe.get(i)

		//-----------------------------------------------------------------------------}
		//Dashboard
		//-----------------------------------------------------------------------------{
		var tb = table.new(position.top_right, 1, 1, bgcolor = #1e222d, border_color = #373a46, border_width = 1, frame_color = #373a46, frame_width = 1)

		if repaint
			tb.cell(0, 0, 'Repainting Mode Enabled', text_color = color.white, text_size = size.small)

		//-----------------------------------------------------------------------------}
		//Plot
		//-----------------------------------------------------------------------------}
		plot(repaint ? na : out + mae, 'Upper', upCss)
		plot(repaint ? na : out - mae, 'Lower', dnCss)

		//Crossing Arrows
		plotshape(ta.crossunder(close, out - mae) ? low : na, "Crossunder", shape.labelup, location.absolute, color(na), 0 , text = '▲', textcolor = upCss, size = size.tiny)
		plotshape(ta.crossover(close, out + mae) ? high : na, "Crossover", shape.labeldown, location.absolute, color(na), 0 , text = '▼', textcolor = dnCss, size = size.tiny)

		//-----------------------------------------------------------------------------}
		'''

		# -------------------------------
		# Calculate Reversals & Signals
		# -------------------------------

		# Compute derivative of NWE line
		df['nwe_diff']            = df['nwe_line'].diff()
		df['nwe_diff_prev']       = df['nwe_diff'].shift(1)

		# Detect reversal points
		df['reversal']            = (df['nwe_diff'] * df['nwe_diff_prev'] < 0)
		df['reversal_up']         = df['reversal'] & (df['nwe_diff_prev'] < 0)
		df['reversal_down']       = df['reversal'] & (df['nwe_diff_prev'] > 0)


		# df['reversal_up']         = df['reversal'] & (df['nwe_diff_prev'] < 0)
		# df['reversal_down']       = df['reversal'] & (df['nwe_diff_prev'] > 0)


		# Generate Buy and Sell Signals based on reversals
		df['nwe_rev_buy_signal']  = df['reversal_up'].astype(int)
		df['nwe_rev_sell_signal'] = df['reversal_down'].astype(int)

	except Exception as e:
		print(f"{dttm_get()} {func_name} ==> Error: {e}")
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#

def ta_add_nwe_orig(df: pd.DataFrame, src='close', bandwidth=8.0, mult=3.0, tag='', rfreq='') -> pd.DataFrame:
	func_name = 'ta_add_nwe_orig'
	func_str = f'{lib_name}.{func_name}(df, src={src}, bandwidth={bandwidth}, tag={tag})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()

	from scipy.ndimage import gaussian_filter1d

	try:
		# Parameters - Method 1
		h = bandwidth
		mult = mult
		source = df[src].values
		n = len(source)
		
		nwe = gaussian_filter1d(source, sigma=h, mode='nearest')

		# Parameters - Method 2
		# h = bandwidth
		# source = df[src].values
		# n = len(source)
		# nwe = np.zeros(n)
		# half_window = 499  # Max bars back as in PineScript
		# # Precompute the Gaussian weights for efficiency
		# x = np.arange(-half_window, half_window + 1)
		# gauss_weights = np.exp(- (x ** 2) / (2 * h * h))
		# for i in range(n):
		# 	# Define the window boundaries
		# 	start_idx = max(0, i - half_window)
		# 	end_idx = min(n, i + half_window + 1)
		# 	window_size = end_idx - start_idx
		# 	# Adjust weights for the window
		# 	weights = gauss_weights[half_window - (i - start_idx):half_window + (end_idx - i)]
		# 	window_data = source[start_idx:end_idx]
		# 	# Compute NWE for the current point
		# 	sumw = np.sum(weights)
		# 	sumwx = np.sum(window_data * weights)
		# 	nwe[i] = sumwx / sumw if sumw != 0 else source[i]


		df['nwe_line'] = nwe
		df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)




		'''
		// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
		// © LuxAlgo

		//@version=5
		indicator("Nadaraya-Watson Envelope [LuxAlgo]", "LuxAlgo - Nadaraya-Watson Envelope", overlay = true, max_lines_count = 500, max_labels_count = 500, max_bars_back=500)
		//------------------------------------------------------------------------------
		//Settings
		//-----------------------------------------------------------------------------{
		h = input.float(8.,'Bandwidth', minval = 0)
		mult = input.float(3., minval = 0)
		src = input(close, 'Source')

		repaint = input(true, 'Repainting Smoothing', tooltip = 'Repainting is an effect where the indicators historical output is subject to change over time. Disabling repainting will cause the indicator to output the endpoints of the calculations')

		//Style
		upCss = input.color(color.teal, 'Colors', inline = 'inline1', group = 'Style')
		dnCss = input.color(color.red, '', inline = 'inline1', group = 'Style')

		//-----------------------------------------------------------------------------}
		//Functions
		//-----------------------------------------------------------------------------{
		//Gaussian window
		gauss(x, h) => math.exp(-(math.pow(x, 2)/(h * h * 2)))

		//-----------------------------------------------------------------------------}
		//Append lines
		//-----------------------------------------------------------------------------{
		n = bar_index

		var ln = array.new_line(0) 

		if barstate.isfirst and repaint
			for i = 0 to 499
				array.push(ln,line.new(na,na,na,na))

		//-----------------------------------------------------------------------------}
		//End point method
		//-----------------------------------------------------------------------------{
		var coefs = array.new_float(0)
		var den = 0.

		if barstate.isfirst and not repaint
			for i = 0 to 499
				w = gauss(i, h)
				coefs.push(w)

			den := coefs.sum()

		out = 0.
		if not repaint
			for i = 0 to 499
				out += src[i] * coefs.get(i)
		out /= den
		mae = ta.sma(math.abs(src - out), 499) * mult

		upper = out + mae
		lower = out - mae
		
		//-----------------------------------------------------------------------------}
		//Compute and display NWE
		//-----------------------------------------------------------------------------{
		float y2 = na
		float y1 = na

		nwe = array.new<float>(0)
		if barstate.islast and repaint
			sae = 0.
			//Compute and set NWE point 
			for i = 0 to math.min(499,n - 1)
				sum = 0.
				sumw = 0.
				//Compute weighted mean 
				for j = 0 to math.min(499,n - 1)
					w = gauss(i - j, h)
					sum += src[j] * w
					sumw += w

				y2 := sum / sumw
				sae += math.abs(src[i] - y2)
				nwe.push(y2)
			
			sae := sae / math.min(499,n - 1) * mult
			for i = 0 to math.min(499,n - 1)
				if i%2
					line.new(n-i+1, y1 + sae, n-i, nwe.get(i) + sae, color = upCss)
					line.new(n-i+1, y1 - sae, n-i, nwe.get(i) - sae, color = dnCss)
				
				if src[i] > nwe.get(i) + sae and src[i+1] < nwe.get(i) + sae
					label.new(n-i, src[i], '▼', color = color(na), style = label.style_label_down, textcolor = dnCss, textalign = text.align_center)
				if src[i] < nwe.get(i) - sae and src[i+1] > nwe.get(i) - sae
					label.new(n-i, src[i], '▲', color = color(na), style = label.style_label_up, textcolor = upCss, textalign = text.align_center)
				
				y1 := nwe.get(i)

		//-----------------------------------------------------------------------------}
		//Dashboard
		//-----------------------------------------------------------------------------{
		var tb = table.new(position.top_right, 1, 1
		, bgcolor = #1e222d
		, border_color = #373a46
		, border_width = 1
		, frame_color = #373a46
		, frame_width = 1)

		if repaint
			tb.cell(0, 0, 'Repainting Mode Enabled', text_color = color.white, text_size = size.small)

		//-----------------------------------------------------------------------------}
		//Plot
		//-----------------------------------------------------------------------------}
		plot(repaint ? na : out + mae, 'Upper', upCss)
		plot(repaint ? na : out - mae, 'Lower', dnCss)

		//Crossing Arrows
		plotshape(ta.crossunder(close, out - mae) ? low : na, "Crossunder", shape.labelup, location.absolute, color(na), 0 , text = '▲', textcolor = upCss, size = size.tiny)
		plotshape(ta.crossover(close, out + mae) ? high : na, "Crossover", shape.labeldown, location.absolute, color(na), 0 , text = '▼', textcolor = dnCss, size = size.tiny)

		//-----------------------------------------------------------------------------}
		'''


		# -------------------------------
		# Calculate Envelope & Signals
		# -------------------------------

		# Compute MAE as mean absolute error over the entire series
		mae = np.mean(np.abs(source - nwe)) * mult
		df['nwe_mae'] = mae
		
		# Compute upper and lower bands
		df['nwe_upper'] = df['nwe_line'] + mae
		df['nwe_lower'] = df['nwe_line'] - mae

		# Generate Buy and Sell Signals based on Envelopes crossing
		df['nwe_env_buy_signal'] = (
			(df[src].shift(1) < df['nwe_lower'].shift(1)) &
			(df[src] >= df['nwe_lower'])
			).astype(int)
		df['nwe_env_sell_signal'] = (
			(df[src].shift(1) > df['nwe_upper'].shift(1)) &
			(df[src] <= df['nwe_upper'])
			).astype(int)



		'''
		// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
		// © LuxAlgo

		//@version=5
		indicator("Nadaraya-Watson Smoothers [LuxAlgo]", "LuxAlgo - Nadaraya-Watson Smoothers", overlay = true, max_lines_count = 500, max_labels_count = 500, max_bars_back=500)
		//------------------------------------------------------------------------------
		//Settings
		//-----------------------------------------------------------------------------{
		h = input.float(8.,'Bandwidth', minval = 0)
		src = input(close,'Source')

		repaint = input(true, 'Repainting Smoothing', tooltip = 'Repainting is an effect where the indicators historical output is subject to change over time. Disabling repainting will cause the indicator to output the endpoint of the estimator')

		//Style
		upCss = input.color(color.teal, 'Colors', inline = 'inline1', group = 'Style')
		dnCss = input.color(color.red, '', inline = 'inline1', group = 'Style')

		//-----------------------------------------------------------------------------}
		//Functions
		//-----------------------------------------------------------------------------{
		//Gaussian window
		gauss(x, h) => math.exp(-(math.pow(x, 2)/(h * h * 2)))

		//-----------------------------------------------------------------------------}
		//Append lines
		//-----------------------------------------------------------------------------{
		n = bar_index

		var ln = array.new_line(0) 

		if barstate.isfirst and repaint
			for i = 0 to 499
				array.push(ln,line.new(na,na,na,na))

		//-----------------------------------------------------------------------------}
		//End point method
		//-----------------------------------------------------------------------------{
		var coefs = array.new_float(0)
		var den = 0.

		if barstate.isfirst and not repaint
			for i = 0 to 499
				w = gauss(i, h)
				coefs.push(w)

			den := coefs.sum()

		out = 0.
		if not repaint
			for i = 0 to 499
				out += src[i] * coefs.get(i)
		out /= den
		
		//-----------------------------------------------------------------------------}
		//Compute and display NWE
		//-----------------------------------------------------------------------------{
		float y2 = na
		float y1 = na
		float y1_d = na
		line l = na
		label lb = na

		if barstate.islast and repaint
			//Compute and set NWE point 
			for i = 0 to math.min(499,n - 1)
				sum = 0.
				sumw = 0.
				//Compute weighted mean 
				for j = 0 to math.min(499,n - 1)
					w = gauss(i - j, h)
					sum += src[j] * w
					sumw += w

				y2 := sum / sumw
				d = y2 - y1
				
				//Set coordinate line
				l := array.get(ln,i)
				line.set_xy1(l,n-i+1,y1)
				line.set_xy2(l,n-i,y2)
				line.set_color(l,y2 > y1 ? dnCss : upCss)
				line.set_width(l,2)
				
				if d * y1_d < 0
					label.new(n-i+1, src[i], y1_d < 0 ? '▲' : '▼'
					, color = color(na)
					, style = y1_d < 0 ? label.style_label_up : label.style_label_down
					, textcolor = y1_d < 0 ? upCss : dnCss
					, textalign = text.align_center)

				y1 := y2
				y1_d := d

		//-----------------------------------------------------------------------------}
		//Dashboard
		//-----------------------------------------------------------------------------{
		var tb = table.new(position.top_right, 1, 1
		, bgcolor = #1e222d
		, border_color = #373a46
		, border_width = 1
		, frame_color = #373a46
		, frame_width = 1)

		if repaint
			tb.cell(0, 0, 'Repainting Mode Enabled', text_color = color.white, text_size = size.small)

		//-----------------------------------------------------------------------------}
		//Plot
		//-----------------------------------------------------------------------------}
		plot(repaint ? na : out, 'NWE Endpoint Estimator', out > out[1] ? upCss : dnCss)

		//-----------------------------------------------------------------------------}
		'''



		# Compute derivative of NWE line
		df['nwe_diff'] = df['nwe_line'].diff()
		df['nwe_diff_prev'] = df['nwe_diff'].shift(1)

		# Detect reversal points
		df['reversal'] = (df['nwe_diff'] * df['nwe_diff_prev'] < 0)
		df['reversal_up'] = df['reversal'] & (df['nwe_diff_prev'] < 0)
		df['reversal_down'] = df['reversal'] & (df['nwe_diff_prev'] > 0)

		# Generate Buy and Sell Signals based on reversals
		df['nwe_rev_buy_signal'] = df['reversal_up'].astype(int)
		df['nwe_rev_sell_signal'] = df['reversal_down'].astype(int)






		# -------------------------------
		# Calculate Color & Signals
		# -------------------------------

		# Color based on trend
#		df['nwe_color'] = np.where(df['nwe_diff'] > 0, 'green', 'red')
		df['nwe_color'] = np.where(df['nwe_line'] > df['nwe_line'].shift(1), 'green', 'red')

		# Generate Buy and Sell Signals based on Color
		df['nwe_3row_buy_signal'] = (
			(df['nwe_color'] == 'green') &
			(df['nwe_color'].shift(1) == 'green') &
			(df['nwe_color'].shift(2) == 'green')
			).astype(int)
		# Generate Buy and Sell Signals based on Color
		df['nwe_3row_sell_signal'] = (
			(df['nwe_color'] == 'red') &
			(df['nwe_color'].shift(1) == 'red')
			).astype(int)

		'''
		# Assuming df is your DataFrame with OHLC data
		df = ta_add_nwe(df, src='close', bandwidth=8.0, mult=3.0)

		# Plotting (requires matplotlib)
		import matplotlib.pyplot as plt

		plt.figure(figsize=(12,6))
		plt.plot(df.index, df['close'], label='Close Price')
		plt.plot(df.index, df['nwe_line'], label='NWE Line')
		plt.plot(df.index, df['nwe_upper'], label='Upper Band', linestyle='--')
		plt.plot(df.index, df['nwe_lower'], label='Lower Band', linestyle='--')
		plt.legend()
		plt.show()
		'''


	except Exception as e:
		print(f"{dttm_get()} {func_name} ==> Error: {e}")
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	print(f'{func_name} completed in {secs}')

	func_end(fnc)
	return df

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
