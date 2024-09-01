#<=====>#
# Import All Scope
#<=====>#
import_all_func_list = []
import_all_func_list.append("mkt_ta_main")
#import_all_func_list.append("ta_ohlcv_df_merge")
#import_all_func_list.append("ta_resample")
#import_all_func_list.append("ta_add_color")
#import_all_func_list.append("ta_add_ha")
#import_all_func_list.append("ta_add_sha")
#import_all_func_list.append("ta_add_sma")
#import_all_func_list.append("ta_add_ema")
#import_all_func_list.append("ta_add_atr")
#import_all_func_list.append("ta_add_rsi")
#import_all_func_list.append("ta_add_bbs")
#import_all_func_list.append("ta_add_impulse_macd")
#import_all_func_list.append("ta_add_high_low")
#
__all__ = import_all_func_list


#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports - Common Modules
#<=====>#

# from datetime import date
# from datetime import datetime
# from datetime import datetime as dt
# from datetime import timedelta
# from datetime import timezone
# from datetime import tzinfo
# from dateutil import parser as dt_prsr
# from pprint import pprint

# import decimal
# import json
import numpy as np
import sys
import os
import pandas as pd 
import pandas_ta as pta 
# import re
# import requests
# import schedule
# import sys
# import time
# import traceback
import warnings

warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


#<=====>#
# Imports - Download Modules
#<=====>#



#<=====>#
# Imports - Shared Library
#<=====>#
# shared_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SHARED_LIBS'))
# if shared_libs_path not in sys.path:
# 	sys.path.append(shared_libs_path)



#<=====>#
# Imports - Local Library
#<=====>#
local_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'libs'))
if local_libs_path not in sys.path:
	sys.path.append(local_libs_path)

from lib_common                    import *

from bot_common                    import *
from bot_coinbase                  import *


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_ta'
log_name      = 'bot_ta'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 0.33
lib_secs_max  = 10


#<=====>#
# Assignments Pre
#<=====>#



#<=====>#
# Classes
#<=====>#




#<=====>#
# Functions
#<=====>#

def mkt_ta_main(mkt, st):
	func_name = 'mkt_ta_main'
	func_str = f'{lib_name}.{func_name}(mkt, st)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	prod_id     = mkt.prod_id
	ta          = AttrDict()
	prc_mkt    = mkt.prc_mkt


	dfs = {}
	rfreqs = ['1min', '3min', '5min', '15min', '30min', '1h', '4h', '1d']
	for rfreq in rfreqs:
		dfs[rfreq] = ta_df_get(prod_id=prod_id, rfreq=rfreq)
	mkt.dfs = dfs


	rfreqs = ['1min', '3min', '5min', '15min', '30min', '1h', '4h', '1d']

	close_price = dfs['1min']['close'].iloc[-1]

#	# backfills the oldest rows to ensure we have min 250
#	for rfreq in rfreqs:
#		if len(dfs[rfreq]) < 300:
#			# Calculate the number of rows to replicate
#			rows_to_add = 300 - len(dfs[rfreq])
#			# Replicate the first row
#			first_row_replicated = pd.concat([dfs[rfreq].iloc[0:1]] * rows_to_add, ignore_index=True)
#			# Append the replicated rows to the start of the DataFrame
#			dfs[rfreq] = pd.concat([first_row_replicated, dfs[rfreq]], ignore_index=True)
#			# Ensure the index is a DatetimeIndex
#			if 'timestamp' in dfs[rfreq].columns:
#				dfs[rfreq]['timestamp'] = pd.to_datetime(dfs[rfreq]['timestamp'])
#				dfs[rfreq].set_index('timestamp', inplace=True)
#			else:
#				print(f"Warning: 'timestamp' column missing in {rfreq} data")

#	# Backfills the oldest rows to ensure we have min 250
#	for rfreq in rfreqs:
#		if len(dfs[rfreq]) < 300:
#			# Calculate the number of rows to replicate
#			rows_to_add = 300 - len(dfs[rfreq])
#			# Replicate the first row
#			first_row = dfs[rfreq].iloc[0].to_frame().T
#			first_row_replicated = pd.concat([first_row] * rows_to_add, ignore_index=True)
#			# Ensure the timestamp column is present
#			first_row_replicated.index = pd.date_range(start=dfs[rfreq].index[0] - pd.Timedelta(minutes=rows_to_add), periods=rows_to_add, freq=rfreq)
#			first_row_replicated.index.name = 'timestamp'
#			# Append the replicated rows to the start of the DataFrame
#			dfs[rfreq] = pd.concat([first_row_replicated, dfs[rfreq]]).sort_index()

#	for rfreq in rfreqs:
#			print(f"Debug Info Initial => {dfs[rfreq].df.tail(5)}")  # Add this line for more debug info


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
			csv_fname = f'data/{mkt.prod_id}_{rfreq}.csv'
			dfs[rfreq].to_csv(csv_fname, index=True)

	for rfreq in rfreqs:
		if dfs[rfreq]['close'].iloc[-1] != close_price:
			print(f"line 149 => rfreq : {rfreq}, end : {dfs[rfreq].index.max()}, close : {dfs[rfreq]['close'].iloc[-1]}, close should be {close_price}")
			print('before fix')
			print(dfs[rfreq].tail(3))
			dfs[rfreq].loc[dfs[rfreq].index[-1], 'close'] = close_price
			dfs[rfreq].loc[dfs[rfreq].index[-1], 'open']  = dfs[rfreq]['close'].iloc[-2]
			print('after fix')
			print(dfs[rfreq].tail(3))

	# reduced list, previous was used for forming current candles
	rfreqs = ['3min', '5min', '15min', '30min', '1h', '4h', '1d']

	for rfreq in rfreqs:
#		print(f'rfreq : {rfreq}')
		ta[rfreq]            = AttrDict()
		ta[rfreq].df         = None
		ta[rfreq].curr       = AttrDict()
		ta[rfreq].last       = AttrDict()
		ta[rfreq].prev       = AttrDict()

		df = dfs[rfreq]
		df = ta_add_indicators(df, st, prc_mkt, rfreq)
		ta[rfreq].df = df

		csv_fname = f'data/{mkt.prod_id}_{rfreq}.csv'
		df.to_csv(csv_fname, index=True)

		for x in range(0,-6,-1):
			desc = f'ago{abs(x)}'
			y = x - 1
			for k in df:
				if not rfreq in ta: ta[rfreq] = AttrDict()
				if not k in ta[rfreq]: ta[rfreq][k] = AttrDict()
				ta[rfreq][k][desc] =  df[k].iloc[y]

	for rfreq in rfreqs:
		if ta[rfreq].df['close'].iloc[-1] != close_price:
			print(f"line 302 => rfreq : {rfreq}, end : {ta[rfreq].df.index.max()}, close_price : {close_price:>.8f}, close : {ta[rfreq].df['close'].iloc[-1]:>.8f}")
			print(f"Debug Info Final => {ta[rfreq].df.tail(5)}")  # Add this line for more debug info
			ta = 'Error!'
#			beep(3)
#			sys.exit()
			break

	func_end(fnc)
	return ta

#<=====>#

# get basic know we need indicators
def ta_df_get(prod_id, rfreq) -> dict:
	func_name = 'ta_df_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, rfreq={rfreq})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	df = cb_candles_get(product_id=prod_id, rfreq=rfreq, min_rows=299)

	func_end(fnc)
	return df

#<=====>#

# get basic know we need indicators
def ta_add_indicators(df: pd.DataFrame, st, prc_mkt, rfreq) -> pd.DataFrame:
	func_name = 'ta_add_indicators'
	func_str = f'{lib_name}.{func_name}(df, st, prc_mkt={prc_mkt}, rfreq={rfreq})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

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
#	if mkt.strat_sha_yn == 'Y':
	# Smoothed Heikin Ashi Candles
	fast_sha_len1 = st.spot.buy.strats.sha.fast_sha_len1 # 8
	fast_sha_len2 = st.spot.buy.strats.sha.fast_sha_len2 # 8
	slow_sha_len1 = st.spot.buy.strats.sha.slow_sha_len1 # 21
	slow_sha_len2 = st.spot.buy.strats.sha.slow_sha_len2 # 21
	df = ta_add_sha(df, prc_mkt, sha_len1=fast_sha_len1, sha_len2=fast_sha_len2, tag='_fast')
	df = ta_add_sha(df, prc_mkt, sha_len1=slow_sha_len1, sha_len2=slow_sha_len2, tag='_slow')

	# STRAT IMP MACD
#	if mkt.strat_imp_macd_yn == 'Y':
	per_ma   = st.spot.buy.strats.imp_macd.per_ma   # 34 
	per_sign = st.spot.buy.strats.imp_macd.per_sign # 9 
	df = ta_add_imp_macd(df, per_ma=per_ma, per_sign=per_sign)

	# STRAT BB
#	if mkt.strat_bb_yn == 'Y':
	inner_per = st.spot.buy.strats.bb.inner_per # 21 
	inner_sd  = st.spot.buy.strats.bb.inner_sd  # 2.3 
	outer_per = st.spot.buy.strats.bb.outer_per # 21 
	outer_sd  = st.spot.buy.strats.bb.outer_sd  # 2.7 
	df = ta_add_bb(df, per=inner_per, sd=inner_sd, tag='_inner')
	df = ta_add_bb(df, per=outer_per, sd=outer_sd, tag='_outer')

	# STRAT BB BO
#	if mkt.strat_bb_bo_yn == 'Y':
	per = st.spot.buy.strats.bb_bo.per # 21 
	sd  = st.spot.buy.strats.bb_bo.sd  # 2.5 
	df = ta_add_bb(df, per=per, sd=sd, tag='_bb_bo')

	# Highest, Lowest
	for x in (7,24,30):
		df[f'max{x}'] = df['high'].rolling(window=x).max()
		df[f'min{x}'] = df['low'].rolling(window=x).min()

#	# Higher Highs, Lower Lows
#	df = ta_add_high_low(df)

	func_end(fnc)
	return df

#<=====>#

def ta_add_color(df: pd.DataFrame) -> pd.DataFrame:
	func_name = 'ta_add_color'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	df['color'] = np.where(df['open'] < df['close'], 'green', 'red')

	func_end(fnc)
	return df

#<=====>#

# Heiki Ashi
def ta_add_ha(df: pd.DataFrame) -> pd.DataFrame:
	func_name = 'ta_add_ha'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

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

#def atr(high, low, close, length=None, mamode=None, talib=None, drift=None, offset=None, **kwargs):
# Average True Range
def ta_add_atr(df: pd.DataFrame, per=14) -> pd.DataFrame:
	func_name = 'ta_add_atr'
	func_str = f'{lib_name}.{func_name}(per={per})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	per = min(per, len(df))

	df['atr'] = pta.atr(high=df['high'], low=df['low'], close=df['close'], length=per, mamode='SMA')

	func_end(fnc)
	return df

#<=====>#

def ta_add_rsi(df: pd.DataFrame, per=14) -> pd.DataFrame:
	func_name = 'ta_add_rsi'
	func_str = f'{lib_name}.{func_name}(per={per})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	per = min(per, len(df))

	df['rsi'] = pta.rsi(df['close'], length=per)

	func_end(fnc)
	return df

#<=====>#

# Rate of Change
def ta_add_roc(df: pd.DataFrame, col='close', label=None, per=3) -> pd.DataFrame:
	func_name = 'ta_add_roc'
	func_str = f'{lib_name}.{func_name}(col={col}, label={label}, per={per})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	per = min(per, len(df))

	if not label:
		label = col

#	df[label]                   = pta.sma(df[col], length=per)

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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

#	last_label = ''

	per = min(per, len(df))

	if not label:
		label = f'{col}_sma{per}'

	df[label]                   = pta.sma(df['close'], length=per)

	df = ta_add_roc(df, col=label)

#	label2 = f'{label}_roc'
#	df[label2]                  = pta.roc(df[label], length=3)
#	label3 = f'{label}_roc_up'
#	df[label3]                  = df[label2]  > df[label2].shift(1)
#	label4 = f'{label}_roc_dn'
#	df[label4]                  = df[label2]  < df[label2].shift(1)

	func_end(fnc)
	return df

#<=====>#

# Exponential Moving Average
def ta_add_ema(df: pd.DataFrame, per, col='close', label=None) -> pd.DataFrame:
	func_name = 'ta_add_emas'
	func_str = f'{lib_name}.{func_name}(per={per}, col={col}, label={label})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	per = min(per, len(df))

	if not label:
		label = f'{col}_ema{per}'

	df[label]                   = pta.ema(df[col], length=per)

	df = ta_add_roc(df, col=label)

#	label2 = f'{label}_roc'
#	df[label2]                  = pta.roc(df[label], length=3)
#	label3 = f'{label}_roc_up'
#	df[label3]                  = df[label2]  > df[label2].shift(1)
#	label4 = f'{label}_roc_dn'
#	df[label4]                  = df[label2]  < df[label2].shift(1)

	func_end(fnc)
	return df

#<=====>#

# Smoothed Heiki Ashi
def ta_add_sha(df: pd.DataFrame, prc_mkt, sha_len1=5, sha_len2=8, tag=None) -> pd.DataFrame:
	func_name = 'ta_add_sha'
	func_str = f'{lib_name}.{func_name}(df, prc_mkt={prc_mkt}, sha_len1={sha_len1}, sha_len2={sha_len2}, tag={tag})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

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

#def ta_ohlcv_df_merge(higher_df, lower_df, timeframe):
#	func_str = f'ta_ohlcv_df_merge(higher_df, lower_df, timeframe={timeframe})'
#
#	print('')
#	print('\n\n\n')
#	print(func_str)
#	print(f'local time est : {dttm_get()}')
#
#	print('')
#	print('higher_df:')
#	print(higher_df.tail(3))
#
#	print('')
#	print('lower_df:')
#	print(lower_df.tail(3))
#
#
#	# Ensure the index of higher_df and lower_df is a DatetimeIndex
#	if not isinstance(higher_df.index, pd.DatetimeIndex):
#		higher_df['timestamp'] = pd.to_datetime(higher_df['timestamp'])
#		higher_df = higher_df.set_index('timestamp')
#
#	if not isinstance(lower_df.index, pd.DatetimeIndex):
#		lower_df['timestamp'] = pd.to_datetime(lower_df['timestamp'])
#		lower_df = lower_df.set_index('timestamp')
#
#	# Remove any duplicate indices in higher_df
#	higher_df = higher_df[~higher_df.index.duplicated(keep='last')]
#
#	last_candle_end   = higher_df.index.max()
#	print('')
#	print(f'last_candle_end: {last_candle_end}')
#
#	# Filter and resample lower_df to get the current candle
#	filtered_lower_df = lower_df[lower_df.index > last_candle_end]
#	print('')
#	print('filtered_lower_df:')
#	print(filtered_lower_df.tail(3))
#
#	# Ensure timeframe string is correctly formatted for resampling
#	resample_timeframe = timeframe
#	print('')
#	print(f'resample_timeframe: {resample_timeframe}')
#
#	current_candle_df = filtered_lower_df.resample(resample_timeframe).agg({
#		'open': 'first',
#		'high': 'max',
#		'low': 'min',
#		'close': 'last',
#		'volume': 'sum'
#	}).dropna()
#
##	# Remove any duplicate indices in current_candle_df
##	current_candle_df = current_candle_df[~current_candle_df.index.duplicated(keep='last')]
#	print('')
#	print('current_candle_df:')
#	print(current_candle_df.tail(3))
#
#	# Concatenate higher_df and current_candle_df
#	df = pd.concat([higher_df, current_candle_df]).sort_index()
#
#	# Remove any duplicates in the final dataframe
#	df = df[~df.index.duplicated(keep='last')]
#
#	if not isinstance(df.index, pd.DatetimeIndex):
#		df['timestamp'] = pd.to_datetime(df['timestamp'])
#		df = df.set_index('timestamp')
#
#	df = df.reset_index()
#
#	print('')
#	print('out df:')
#	print(df.tail(3))
#
##	print('')
##	print('')
##	print('')
#
#	return df

#<=====>#

#def ta_ohlcv_df_merge_orig(higher_df, lower_df, timeframe):
#	func_str = 'ta_ohlcv_df_merge_orig(higher_df, lower_df, timeframe={})'.format(timeframe)
#
#	# Ensure the index of higher_df and lower_df is a DatetimeIndex
#	if not isinstance(higher_df.index, pd.DatetimeIndex):
#		higher_df['timestamp'] = pd.to_datetime(higher_df['timestamp'])
#		higher_df = higher_df.set_index('timestamp')
#
#	if not isinstance(lower_df.index, pd.DatetimeIndex):
#		lower_df['timestamp'] = pd.to_datetime(lower_df['timestamp'])
#		lower_df = lower_df.set_index('timestamp')
#
#	# Remove any duplicate indices in higher_df
#	higher_df = higher_df[~higher_df.index.duplicated(keep='last')]
#
#	last_candle_end   = higher_df.index.max()
#
#	# Filter and resample lower_df to get the current candle
#	filtered_lower_df = lower_df[lower_df.index > last_candle_end]
#	current_candle_df = filtered_lower_df.resample(timeframe).agg({
#		'open': 'first',
#		'high': 'max',
#		'low': 'min',
#		'close': 'last',
#		'volume': 'sum'
#	})
#
#	# Remove any duplicate indices in current_candle_df
#	current_candle_df = current_candle_df[~current_candle_df.index.duplicated(keep='lasst')]
#
#	# Concatenate higher_df and current_candle_df
#	df = pd.concat([higher_df, current_candle_df]).sort_index()
#
#	# Remove any duplicates in the final dataframe
#	df = df[~df.index.duplicated(keep='first')]
#
#	df = df.reset_index()
#
#	return df

#<=====>#

#def ta_resample(df: pd.DataFrame, rfreq: str, roffset=None) -> pd.DataFrame:
#	func_name = 'ta_resample'
#	func_str = f'{lib_name}.{func_name}()'
##	G(func_str)
#	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	if lib_verbosity >= 2: print_func_name(func_str, adv=2)
#
#	"""
#	Resample DataFrame by <interval>.
#	"""
##	https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
##	Alias   Description
##	B       business day frequency
##	C       custom business day frequency (experimental)
##	D       calendar day frequency
##	W       weekly frequency
##	M       month end frequency
##	BM      business month end frequency
##	CBM     custom business month end frequency
##	MS      month start frequency
##	BMS     business month start frequency
##	CBMS    custom business month start frequency
##	Q       quarter end frequency
##	BQ      business quarter endfrequency
##	QS      quarter start frequency
##	BQS     business quarter start frequency
##	A       year end frequency
##	BA      business year end frequency
##	AS      year start frequency
##	BAS     business year start frequency
##	BH      business hour frequency
##	H       hourly frequency
##	T, min  minutely frequency
##	S       secondly frequency
##	L, ms   milliseonds
##	U, us   microseconds
##	N       nanoseconds
#
#	d = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
#
#	if roffset:
#		df = df.resample(rfreq, offset=roffset).agg(d)
#	else:
#		df = df.resample(rfreq).agg(d)
##	# added this for coinbase ONE_MINUTE resampling 5/6/24
#	df.dropna()
#
#	func_end(fnc)
#	return df

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
