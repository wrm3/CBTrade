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

from libs.bot_coinbase import cb, cb_candles_get
from libs.bot_db_read import db_ohlcv_freq_get, db_ohlcv_prod_id_freqs
from libs.bot_db_write import db_tbl_ohlcv_prod_id_insupd_many
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_common import dir_val, dttm_get, func_begin, func_end, print_adv
from libs.lib_dicts import AttrDict
from libs.lib_common import beep

warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_ta'
log_name      = 'bot_ta'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 2

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

	try:

		prod_id     = pair.prod_id
		ta          = AttrDict()
		prc_mkt     = pair.prc_mkt
		rfreq       = ''
		df          = None
		dfs         = {}
		dfs_ins_many = {}

		# Getting the Candlestick Data
		dfs = ta_ohlcv(pair, st)

		# Assigning the Real Time Close Price
		close_price = dfs['1min']['close'].iloc[-1]

		# reduced list, previous was used for forming current candles
#		rfreqs = ['3min', '5min', '15min', '30min', '1h', '4h', '1d']
		rfreqs = ['5min', '15min', '30min', '1h', '4h', '1d']

		# Adding the Technical Analysis Indicators
		for rfreq in rfreqs:
			ta[rfreq]            = AttrDict()
			ta[rfreq].df         = None
			ta[rfreq].curr       = AttrDict()
			ta[rfreq].last       = AttrDict()
			ta[rfreq].prev       = AttrDict()

			df = dfs[rfreq]

			dfs_ins_many[rfreq] = df

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

		db_tbl_ohlcv_prod_id_insupd_many(prod_id, dfs_ins_many)

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

	func_end(fnc)
	return ta

#<=====>#

def ta_ohlcv(pair, st):
	func_name = 'ta_ohlcv'
	func_str = f'{lib_name}.{func_name}(pair, st)'
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=2)
#	G(func_str)

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

			ohlcv_meths[freq] = ohlcv_meth

		for freq in ohlcv_meths:
			if ohlcv_meths[freq]['method'] == 'api':
				msg = 'getting {} {} hist from api'.format(prod_id, freq)
				dfs[freq] = ta_df_get(prod_id, freq)
			else:
				msg = 'getting {} {} hist from db'.format(prod_id, freq)
				dfs[freq] = ta_hist_db(prod_id, freq)

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

			# Ensure the index is a DatetimeIndex
			if not isinstance(dfs[rfreq].index, pd.DatetimeIndex):
				dfs[rfreq]['timestamp'] = pd.to_datetime(dfs[rfreq]['timestamp'])
				dfs[rfreq] = dfs[rfreq].set_index('timestamp')

			if rfreq == '1min':
				csv_fname = f'data/{pair.prod_id}_{rfreq}.csv'
				dir_val(csv_fname)
				dfs[rfreq].to_csv(csv_fname, index=True)

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

	func_end(fnc)
	return dfs

#<=====>#

def ta_hist_db(prod_id, freq):
	func_name = "ta_hist_db"
	func_str = f"{lib_name}.{func_name}(prod_id={prod_id})"
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	df = None
	try:
		hist = db_ohlcv_freq_get(prod_id, freq)

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
		df.dropna()

	except Exception:
		print(func_name + 'errored.')
		beep()
		raise
		exit()

	fnc = func_end(fnc)
	return df

#<=====>#

# get basic know we need indicators
def ta_df_get(prod_id, rfreq) -> dict:
	func_name = 'ta_df_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, rfreq={rfreq})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	df = cb_candles_get(product_id=prod_id, rfreq=rfreq, min_rows=299)

	func_end(fnc)
	return df

#<=====>#

# get basic know we need indicators
def ta_add_indicators(df: pd.DataFrame, st, prc_mkt, rfreq) -> pd.DataFrame:
	func_name = 'ta_add_indicators'
	func_str = f'{lib_name}.{func_name}(df, st, prc_mkt={prc_mkt}, rfreq={rfreq})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	df['hl2']   = (df['high'] + df['low']) / 2
	df['hlc3']  = (df['high'] + df['low'] + df['close']) / 3
	df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
	df['hlcc4'] = (df['high'] + df['low'] + df['close'] + df['close']) / 3

	df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])
	df = df[(df[['open', 'high', 'low', 'close', 'volume']] != 0).any(axis=1)]

	if len(df) < 10:
		print('error gettings candles...')
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

	# Simple Moving Averages - Fibonacci
	for per in (5, 8, 13, 21, 34, 55, 89, 100, 150, 200, 300):
		df = ta_add_sma(df, per, col='close', label=f'sma{per}')

	# Exponential Moving Averages - Fibonacci
	for per in (5, 8, 13, 21, 34, 55, 89, 100, 150, 200, 300):
		df = ta_add_ema(df, per, col='close', label=f'ema{per}')

	# New Strat Add Section
	# STRAT SHA
	# Smoothed Heikin Ashi Candles
	fast_sha_len1 = st.buy.strats.sha.fast_sha_len1 # 8
	fast_sha_len2 = st.buy.strats.sha.fast_sha_len2 # 8
	slow_sha_len1 = st.buy.strats.sha.slow_sha_len1 # 21
	slow_sha_len2 = st.buy.strats.sha.slow_sha_len2 # 21
	df = ta_add_sha(df, prc_mkt, sha_len1=fast_sha_len1, sha_len2=fast_sha_len2, tag='_fast')
	df = ta_add_sha(df, prc_mkt, sha_len1=slow_sha_len1, sha_len2=slow_sha_len2, tag='_slow')

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
	df = ta_add_nwe(df, src='close', bandwidth=nwe_bw, tag='_bb_bo')

	# Highest, Lowest
	for x in (7,24,30):
		df[f'max{x}'] = df['high'].rolling(window=x).max()
		df[f'min{x}'] = df['low'].rolling(window=x).min()

	func_end(fnc)
	return df

#<=====>#

def ta_add_color(df: pd.DataFrame) -> pd.DataFrame:
	func_name = 'ta_add_color'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	df['color'] = np.where(df['open'] < df['close'], 'green', 'red')

	func_end(fnc)
	return df

#<=====>#

# Heiki Ashi
def ta_add_ha(df: pd.DataFrame) -> pd.DataFrame:
	func_name = 'ta_add_ha'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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

	func_end(fnc)
	return df

#<=====>#

# Average True Range
def ta_add_atr(df: pd.DataFrame, per=14) -> pd.DataFrame:
	func_name = 'ta_add_atr'
	func_str = f'{lib_name}.{func_name}(per={per})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	per = min(per, len(df))

	df['atr'] = pta.atr(high=df['high'], low=df['low'], close=df['close'], length=per, mamode='SMA')

	func_end(fnc)
	return df

#<=====>#

def ta_add_rsi(df: pd.DataFrame, per=14) -> pd.DataFrame:
	func_name = 'ta_add_rsi'
	func_str = f'{lib_name}.{func_name}(per={per})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	per = min(per, len(df))

	df['rsi'] = pta.rsi(df['close'], length=per)

	func_end(fnc)
	return df

#<=====>#

# Rate of Change
def ta_add_roc(df: pd.DataFrame, col='close', label=None, per=3) -> pd.DataFrame:
	func_name = 'ta_add_roc'
	func_str = f'{lib_name}.{func_name}(col={col}, label={label}, per={per})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	per = min(per, len(df))

	if not label:
		label = col

	label2 = f'{label}_roc'
	df[label2]                  = pta.roc(df[label], length=3)

	label3 = f'{label}_roc_up'
	df[label3]                  = df[label2]  > df[label2].shift(1)

	label4 = f'{label}_roc_dn'
	df[label4]                  = df[label2]  < df[label2].shift(1)

	func_end(fnc)
	return df

#<=====>#

# Simple Moving Average
def ta_add_sma(df: pd.DataFrame, per, col='close', label=None) -> pd.DataFrame:
	func_name = 'ta_add_sma'
	func_str = f'{lib_name}.{func_name}(per={per}, col={col}, label={label})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	per = min(per, len(df))

	if not label:
		label = f'{col}_sma{per}'

	df[label]                   = pta.sma(df['close'], length=per)

	df = ta_add_roc(df, col=label)

	func_end(fnc)
	return df

#<=====>#

# Exponential Moving Average
def ta_add_ema(df: pd.DataFrame, per, col='close', label=None) -> pd.DataFrame:
	func_name = 'ta_add_emas'
	func_str = f'{lib_name}.{func_name}(per={per}, col={col}, label={label})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	per = min(per, len(df))

	if not label:
		label = f'{col}_ema{per}'

	df[label]                   = pta.ema(df[col], length=per)

	df = ta_add_roc(df, col=label)

	func_end(fnc)
	return df

#<=====>#

# Smoothed Heiki Ashi
def ta_add_sha(df: pd.DataFrame, prc_mkt, sha_len1=5, sha_len2=8, tag=None) -> pd.DataFrame:
	func_name = 'ta_add_sha'
	func_str = f'{lib_name}.{func_name}(df, prc_mkt={prc_mkt}, sha_len1={sha_len1}, sha_len2={sha_len2}, tag={tag})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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

	func_end(fnc)
	return df

#<=====>#

# Impulse MACD
def ta_add_imp_macd(df: pd.DataFrame, per_ma=34, per_sign=9) -> pd.DataFrame:
	func_name = 'ta_add_imp_macd'
	func_str = f'{lib_name}.{func_name}(df, per_ma={per_ma}, per_sign={per_sign})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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

	for c in('hlc3', 'hi', 'lo', 'mi','md', 'sb', 'sh', 'mdc'):
		df.pop(c)

	func_end(fnc)
	return df

#<=====>#

# Bollinger Bands
def ta_add_bb(df: pd.DataFrame, per=20, sd=2, tag='') -> pd.DataFrame:
	func_name = 'ta_add_bbs'
	func_str = f'{lib_name}.{func_name}(df, per={per}, sd={sd}, tag={tag})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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

	func_end(fnc)
	return df

#<=====>#

def ta_add_nwe_old(df: pd.DataFrame, src='close', bandwidth=8, tag='') -> pd.DataFrame:
	func_name = 'ta_add_nwe_old'
	func_str = f'{lib_name}.{func_name}(df, src={src}, bandwidth={bandwidth}, tag={tag})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# Nadaraya-Watson Estimator

	def gaussian_kernel(x, h):
		"""Gaussian function."""
		return np.exp(-(x ** 2) / (2 * h ** 2))

	def nadaraya_watson_smoother(src, bandwidth):
		"""Nadaraya-Watson Smoother."""
		smoothed_values = []
		for i in range(len(src)):
			weights = np.array([gaussian_kernel(i - j, bandwidth) for j in range(len(src))])
			weighted_sum = np.sum(src * weights)
			sum_of_weights = np.sum(weights)
			smoothed_value = weighted_sum / sum_of_weights if sum_of_weights != 0 else np.nan
			smoothed_values.append(smoothed_value)
		return np.array(smoothed_values)

	def compute_color(smoothed_values):
		"""Compute color based on whether the smoothed value is increasing or decreasing."""
		colors = []
		for i in range(1, len(smoothed_values)):
			if smoothed_values[i] > smoothed_values[i - 1]:
				colors.append('green')  # Up trend
			else:
				colors.append('red')  # Down trend
		colors.insert(0, 'green')  # Initial color (default to green)
		return colors

	# Parameters
	source = df[src]

	# Calculate the smoothed line and its color
	smoothed_line = nadaraya_watson_smoother(source.values, bandwidth)
	line_colors = compute_color(smoothed_line)

	# Add the smoothed line and its color to your DataFrame
	df['nwe_line'] = smoothed_line
	df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)
	df['nwe_color'] = line_colors

	func_end(fnc)
	return df

#<=====>#

import numpy as np
import pandas as pd

def ta_add_nwe(df: pd.DataFrame, src='close', bandwidth=8, tag='') -> pd.DataFrame:
    func_name = 'ta_add_nwe'
    func_str = f'{lib_name}.{func_name}(df, src={src}, bandwidth={bandwidth}, tag={tag})'
    fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)

    try:
        # Parameters
        source = df[src].values

        # Apply Gaussian filter
        smoothed_line = gaussian_filter1d(source, sigma=bandwidth, mode='reflect')

        # Compute Rate of Change (ROC)
        df['nwe_line'] = smoothed_line
        df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)
        
        # Compute Color based on trend
        diff = np.diff(smoothed_line, prepend=smoothed_line[0])
        df['nwe_color'] = np.where(diff > 0, 'green', 'red')

    except Exception as e:
        print(f"{dttm_get()} {func_name} ==> Error: {e}")
        traceback.print_exc()
        traceback.print_stack()
        print_adv(2)
        pass

    func_end(fnc)
    return df

#<=====>#

# def ta_add_high_low(df: pd.DataFrame) -> pd.DataFrame:
# 	# Higher Highs, Lower Lows
# 	# Initialize variables to track the previous high and low
# 	prev_high        = df['high'].iloc[0]
# 	prev_low         = df['low'].iloc[0]
# 	higher_highs     = True
# 	higher_lows      = True
# 	lower_highs      = True
# 	lower_lows       = True
# 	highest_close    = df['close'].iloc[0]
# 	lowest_close     = df['close'].iloc[0]
# 	# Loop through the DataFrame to check for higher highs and higher lows
# 	for i in range(1, len(df)):
# 		if df['close'].iloc[i] > highest_close: highest_close = df['close'].iloc[i]
# 		if df['close'].iloc[i] < lowest_close: lowest_close = df['close'].iloc[i]
# 		current_high = df['high'].iloc[i]
# 		current_low  = df['low'].iloc[i]
# 		if current_high <= prev_high: higher_highs = False
# 		if current_low <= prev_low: higher_lows = False
# 		if current_high >= prev_high: lower_highs = False
# 		if current_low >= prev_low: lower_lows = False
# 		# Update the previous values for the next iteration
# 		prev_high = current_high
# 		prev_low  = current_low
# 	ta_ad = AttrDict()
# 	ta_ad.curr.higher_highs =  higher_highs
# 	ta_ad.curr.higher_lows  =  higher_lows
# 	ta_ad.curr.lower_highs  =  lower_highs
# 	ta_ad.curr.lower_lows   =  lower_lows
# 	ta_ad.close_max         = float(highest_close)
# 	ta_ad.close_min         = float(lowest_close)
# 	ta_ad.prc_mkt_vs_highest_close_pct = round((prc_mkt - ta.close_max) / ta.close_max * 100, 2)
# 	ta_ad.prc_mkt_vs_lowest_close_pct  = round((prc_mkt - ta.close_min) / ta.close_min * 100, 2)
# 	return df, ta_ad

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
