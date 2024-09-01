#<=====>#
# Import All Scope
#<=====>#

import_all_func_list = []
import_all_func_list.append("buy_strats_get")
import_all_func_list.append("buy_strats_avail_get")
import_all_func_list.append("buy_strats_check")
import_all_func_list.append("buy_strats_deny")
#import_all_func_list.append("sell_strats_get")
import_all_func_list.append("sell_strats_avail_get")
import_all_func_list.append("sell_strats_check")
__all__ = import_all_func_list


#<=====>#
# Description
#<=====>#



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
# from datetime import timezone
# from datetime import tzinfo
# from datetime import timedelta
# from dateutil import parser as dt_prsr
# from pprint import pprint
#from coinbase.rest import RESTClient as cbclient

# https://github.com/rhettre/coinbase-advancedtrade-python/tree/main
# from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient as cbclient

#from rich import print as rprint
#from rich import print

#from rich.console import Console
#from rich.panel import Panel
#from rich.layout import Layout
#from rich.live import Live

# import ast
# import configparser
# import decimal
# import json
# import numpy as np
import sys
import os
import pandas as pd 
# import pandas_ta as pta 
# import pytz
# import re
# import requests
# import schedule
# import sys
# import time
import traceback
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

from bot_coinbase                  import *
from bot_common                    import *
from bot_db_read                   import *
from bot_db_write                  import *
from bot_logs                     import *
# from bot_secrets                   import secrets
from bot_settings                  import settings
from bot_ta                        import *
from bot_theme                     import *


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strats'
log_name      = 'bot_strats'
lib_verbosity = 0
lib_debug_lvl = 0
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

#<=====>#

def buy_strats_get():
	func_name = 'buy_strats_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	strats = {}
	strats['sha_15min']        = {'prod_id': '', 'buy_strat_nick': 'sha_15min'      , 'buy_strat_type': 'up', 'buy_strat_name': 'sha',      'buy_strat_desc': 'Double Smoothed Heikin Ashi', 'buy_strat_freq': '15min'}
	strats['sha_30min']        = {'prod_id': '', 'buy_strat_nick': 'sha_30min'      , 'buy_strat_type': 'up', 'buy_strat_name': 'sha',      'buy_strat_desc': 'Double Smoothed Heikin Ashi', 'buy_strat_freq': '30min'}
	strats['sha_1h']           = {'prod_id': '', 'buy_strat_nick': 'sha_1h'         , 'buy_strat_type': 'up', 'buy_strat_name': 'sha',      'buy_strat_desc': 'Double Smoothed Heikin Ashi', 'buy_strat_freq': '1h'}
	strats['sha_4h']           = {'prod_id': '', 'buy_strat_nick': 'sha_4h'         , 'buy_strat_type': 'up', 'buy_strat_name': 'sha',      'buy_strat_desc': 'Double Smoothed Heikin Ashi', 'buy_strat_freq': '4h'}
	strats['sha_1d']           = {'prod_id': '', 'buy_strat_nick': 'sha_1d'         , 'buy_strat_type': 'up', 'buy_strat_name': 'sha',      'buy_strat_desc': 'Double Smoothed Heikin Ashi', 'buy_strat_freq': '1d'}

	strats['imp_macd_15min']   = {'prod_id': '', 'buy_strat_nick': 'imp_macd_15min' , 'buy_strat_type': 'up', 'buy_strat_name': 'imp_macd', 'buy_strat_desc': 'Impulse MACD',                'buy_strat_freq': '15min'}
	strats['imp_macd_30min']   = {'prod_id': '', 'buy_strat_nick': 'imp_macd_30min' , 'buy_strat_type': 'up', 'buy_strat_name': 'imp_macd', 'buy_strat_desc': 'Impulse MACD',                'buy_strat_freq': '30min'}
	strats['imp_macd_1h']      = {'prod_id': '', 'buy_strat_nick': 'imp_macd_1h'    , 'buy_strat_type': 'up', 'buy_strat_name': 'imp_macd', 'buy_strat_desc': 'Impulse MACD',                'buy_strat_freq': '1h'}
	strats['imp_macd_4h']      = {'prod_id': '', 'buy_strat_nick': 'imp_macd_4h'    , 'buy_strat_type': 'up', 'buy_strat_name': 'imp_macd', 'buy_strat_desc': 'Impulse MACD',                'buy_strat_freq': '4h'}
	strats['imp_macd_1d']      = {'prod_id': '', 'buy_strat_nick': 'imp_macd_1d'    , 'buy_strat_type': 'up', 'buy_strat_name': 'imp_macd', 'buy_strat_desc': 'Impulse MACD',                'buy_strat_freq': '1d'}

	strats['emax_15min']       = {'prod_id': '', 'buy_strat_nick': 'emax_15min'     , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '15min'}
	strats['emax_30min']       = {'prod_id': '', 'buy_strat_nick': 'emax_30min'     , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '30min'}
	strats['emax_1h']          = {'prod_id': '', 'buy_strat_nick': 'emax_1h'        , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '1h'}
	strats['emax_4h']          = {'prod_id': '', 'buy_strat_nick': 'emax_4h'        , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '4h'}
	strats['emax_1d']          = {'prod_id': '', 'buy_strat_nick': 'emax_1d'        , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '1d'}

	strats['bb_bo_15min']      = {'prod_id': '', 'buy_strat_nick': 'bb_bo_15min'    , 'buy_strat_type': 'up', 'buy_strat_name': 'bb_bo',    'buy_strat_desc': 'Bollinger Band Breakout',     'buy_strat_freq': '15min'}
	strats['bb_bo_30min']      = {'prod_id': '', 'buy_strat_nick': 'bb_bo_30min'    , 'buy_strat_type': 'up', 'buy_strat_name': 'bb_bo',    'buy_strat_desc': 'Bollinger Band Breakout',     'buy_strat_freq': '30min'}
	strats['bb_bo_1h']         = {'prod_id': '', 'buy_strat_nick': 'bb_bo_1h'       , 'buy_strat_type': 'up', 'buy_strat_name': 'bb_bo',    'buy_strat_desc': 'Bollinger Band Breakout',     'buy_strat_freq': '1h'}
	strats['bb_bo_4h']         = {'prod_id': '', 'buy_strat_nick': 'bb_bo_4h'       , 'buy_strat_type': 'up', 'buy_strat_name': 'bb_bo',    'buy_strat_desc': 'Bollinger Band Breakout',     'buy_strat_freq': '4h'}
	strats['bb_bo_1d']         = {'prod_id': '', 'buy_strat_nick': 'bb_bo_1d'       , 'buy_strat_type': 'up', 'buy_strat_name': 'bb_bo',    'buy_strat_desc': 'Bollinger Band Breakout',     'buy_strat_freq': '1d'}

	strats['bb_15min']         = {'prod_id': '', 'buy_strat_nick': 'bb_15min'       , 'buy_strat_type': 'dn', 'buy_strat_name': 'bb',       'buy_strat_desc': 'Bollinger Band',              'buy_strat_freq': '15min'}
	strats['bb_30min']         = {'prod_id': '', 'buy_strat_nick': 'bb_30min'       , 'buy_strat_type': 'dn', 'buy_strat_name': 'bb',       'buy_strat_desc': 'Bollinger Band',              'buy_strat_freq': '30min'}
	strats['bb_1h']            = {'prod_id': '', 'buy_strat_nick': 'bb_1h'          , 'buy_strat_type': 'dn', 'buy_strat_name': 'bb',       'buy_strat_desc': 'Bollinger Band',              'buy_strat_freq': '1h'}
	strats['bb_4h']            = {'prod_id': '', 'buy_strat_nick': 'bb_4h'          , 'buy_strat_type': 'dn', 'buy_strat_name': 'bb',       'buy_strat_desc': 'Bollinger Band',              'buy_strat_freq': '4h'}
	strats['bb_1d']            = {'prod_id': '', 'buy_strat_nick': 'bb_1d'          , 'buy_strat_type': 'dn', 'buy_strat_name': 'bb',       'buy_strat_desc': 'Bollinger Band',              'buy_strat_freq': '1d'}

	strats['drop_15min']       = {'prod_id': '', 'buy_strat_nick': 'drop_15min'     , 'buy_strat_type': 'dn', 'buy_strat_name': 'drop',     'buy_strat_desc': 'Big Dip Strat',               'buy_strat_freq': '15min'}
	strats['drop_30min']       = {'prod_id': '', 'buy_strat_nick': 'drop_30min'     , 'buy_strat_type': 'dn', 'buy_strat_name': 'drop',     'buy_strat_desc': 'Big Dip Strat',               'buy_strat_freq': '30min'}
	strats['drop_1h']          = {'prod_id': '', 'buy_strat_nick': 'drop_1h'        , 'buy_strat_type': 'dn', 'buy_strat_name': 'drop',     'buy_strat_desc': 'Big Dip Strat',               'buy_strat_freq': '1h'}
	strats['drop_4h']          = {'prod_id': '', 'buy_strat_nick': 'drop_4h'        , 'buy_strat_type': 'dn', 'buy_strat_name': 'drop',     'buy_strat_desc': 'Big Dip Strat',               'buy_strat_freq': '4h'}
	strats['drop_1d']          = {'prod_id': '', 'buy_strat_nick': 'drop_1d'        , 'buy_strat_type': 'dn', 'buy_strat_name': 'drop',     'buy_strat_desc': 'Big Dip Strat',               'buy_strat_freq': '1d'}

	func_end(fnc)
	return strats

#<=====>#

def buy_strats_avail_get(mkt):
	func_name = 'buy_strats_avail_get'
	func_str = f'{lib_name}.{func_name}(mkt)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	st         = settings.settings_load()
	prod_id    = mkt.prod_id

	# New Strat Add Section
	mkt.strat_sha_yn = 'N'
	if not st.spot.buy.strats.sha.prod_ids:
		mkt.strat_sha_yn = 'Y'
	elif prod_id in st.spot.buy.strats.sha.prod_ids:
		mkt.strat_sha_yn = 'Y'
	if st.spot.buy.strats.sha.prod_ids_skip:
		if prod_id in st.spot.buy.strats.sha.prod_ids_skip:
			mkt.strat_sha_yn = 'N'

	mkt.strat_imp_macd_yn = 'N'
	if not st.spot.buy.strats.imp_macd.prod_ids:
		mkt.strat_imp_macd_yn = 'Y'
	elif prod_id in st.spot.buy.strats.imp_macd.prod_ids:
		mkt.strat_imp_macd_yn = 'Y'
	if st.spot.buy.strats.imp_macd.prod_ids_skip:
		if prod_id in st.spot.buy.strats.imp_macd.prod_ids_skip:
			mkt.strat_imp_macd_yn = 'N'

	mkt.strat_emax_yn = 'N'
	if not st.spot.buy.strats.emax.prod_ids:
		mkt.strat_emax_yn = 'Y'
	elif prod_id in st.spot.buy.strats.emax.prod_ids:
		mkt.strat_emax_yn = 'Y'
	if st.spot.buy.strats.emax.prod_ids_skip:
		if prod_id in st.spot.buy.strats.emax.prod_ids_skip:
			mkt.strat_emax_yn = 'N'

	mkt.strat_drop_yn = 'N'
	if not st.spot.buy.strats.drop.prod_ids:
		mkt.strat_drop_yn = 'Y'
	elif prod_id in st.spot.buy.strats.drop.prod_ids:
		mkt.strat_drop_yn = 'Y'
	if st.spot.buy.strats.drop.prod_ids_skip:
		if prod_id in st.spot.buy.strats.drop.prod_ids_skip:
			mkt.strat_drop_yn = 'N'

	mkt.strat_bb_bo_yn = 'N'
	if not st.spot.buy.strats.bb_bo.prod_ids:
		mkt.strat_bb_bo_yn = 'Y'
	elif prod_id in st.spot.buy.strats.bb_bo.prod_ids:
		mkt.strat_bb_bo_yn = 'Y'
	if st.spot.buy.strats.bb_bo.prod_ids_skip:
		if prod_id in st.spot.buy.strats.bb_bo.prod_ids_skip:
			mkt.strat_bb_bo_yn = 'N'

	mkt.strat_bb_yn = 'N'
	if not st.spot.buy.strats.bb.prod_ids:
		mkt.strat_bb_yn = 'Y'
	elif prod_id in st.spot.buy.strats.bb.prod_ids:
		mkt.strat_bb_yn = 'Y'
	if st.spot.buy.strats.bb.prod_ids_skip:
		if prod_id in st.spot.buy.strats.bb.prod_ids_skip:
			mkt.strat_bb_yn = 'N'

	func_end(fnc)
	return mkt

#<=====>#

def buy_strats_check(st, mkt, trade_perf, trade_strat_perf, ta, buy_signals, reserve_release_tf):
	func_name = 'buy_strats_check'
	func_str = f'{lib_name}.{func_name}(st, mkt, trade_perf, trade_strat_perf, ta, reserve_release_tf={reserve_release_tf})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

#	show_buy_disp_yn     = 'Y'
	buy_yn               = 'N'
	wait_yn              = 'Y'
	freq                 = trade_strat_perf.buy_strat_freq

	# Buy Strategy - Double Smoothed Heikin Ashi 
	if trade_strat_perf.buy_strat_name == 'sha':
		if st.spot.buy.strats.sha.use_yn == 'Y' and mkt.strat_sha_yn == 'Y':
			if freq in st.spot.buy.strats.sha.freqs:
				mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn = buy_strat_sha(mkt, trade_perf, trade_strat_perf, ta)
				buy_signal = {"prod_id": mkt.prod_id, "buy_strat_type": trade_strat_perf.buy_strat_type, "buy_strat_name": trade_strat_perf.buy_strat_name, "buy_strat_freq": trade_strat_perf.buy_strat_freq, "buy_yn": buy_yn, "wait_yn": wait_yn}
				buy_signals.append(buy_signal)


	# Buy Strategy - Impulse MACD
	elif trade_strat_perf.buy_strat_name == 'imp_macd':
		if st.spot.buy.strats.imp_macd.use_yn == 'Y' and mkt.strat_imp_macd_yn == 'Y':
			if freq in st.spot.buy.strats.imp_macd.freqs:
				mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn = buy_strat_imp_macd(mkt, trade_perf, trade_strat_perf, ta)
				buy_signal = {"prod_id": mkt.prod_id, "buy_strat_type": trade_strat_perf.buy_strat_type, "buy_strat_name": trade_strat_perf.buy_strat_name, "buy_strat_freq": trade_strat_perf.buy_strat_freq, "buy_yn": buy_yn, "wait_yn": wait_yn}
				buy_signals.append(buy_signal)


	# Buy Strategy - Bollinger Band Breakout
	elif trade_strat_perf.buy_strat_name == 'bb_bo':
		if st.spot.buy.strats.bb_bo.use_yn == 'Y' and mkt.strat_bb_bo_yn == 'Y':
			if freq in st.spot.buy.strats.bb_bo.freqs:
				mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn = buy_strat_bb_bo(mkt, trade_perf, trade_strat_perf, ta)
				buy_signal = {"prod_id": mkt.prod_id, "buy_strat_type": trade_strat_perf.buy_strat_type, "buy_strat_name": trade_strat_perf.buy_strat_name, "buy_strat_freq": trade_strat_perf.buy_strat_freq, "buy_yn": buy_yn, "wait_yn": wait_yn}
				buy_signals.append(buy_signal)


	# Buy Strategy - Drop
	elif trade_strat_perf.buy_strat_name == 'drop':
		if st.spot.buy.strats.drop.use_yn == 'Y' and mkt.strat_drop_yn == 'Y':
			if freq in st.spot.buy.strats.drop.freqs:
				mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn, reserve_release_tf = buy_strat_drop(st, mkt, trade_perf, trade_strat_perf, ta, reserve_release_tf)
				buy_signal = {"prod_id": mkt.prod_id, "buy_strat_type": trade_strat_perf.buy_strat_type, "buy_strat_name": trade_strat_perf.buy_strat_name, "buy_strat_freq": trade_strat_perf.buy_strat_freq, "buy_yn": buy_yn, "wait_yn": wait_yn}
				buy_signals.append(buy_signal)


	# Buy Strategy - Bollinger Band
	elif trade_strat_perf.buy_strat_name == 'bb':
		if st.spot.buy.strats.bb.use_yn == 'Y' and mkt.strat_bb_yn == 'Y':
			if freq in st.spot.buy.strats.bb.freqs:
				mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn = buy_strat_bb(mkt, trade_perf, trade_strat_perf, ta)
				buy_signal = {"prod_id": mkt.prod_id, "buy_strat_type": trade_strat_perf.buy_strat_type, "buy_strat_name": trade_strat_perf.buy_strat_name, "buy_strat_freq": trade_strat_perf.buy_strat_freq, "buy_yn": buy_yn, "wait_yn": wait_yn}
				buy_signals.append(buy_signal)

	else:
		buy_yn = 'N'
		wait_yn = 'Y'
		# show_buy_disp_yn = 'N'

	func_end(fnc)
	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn, buy_signals, reserve_release_tf

#<=====>#

def buy_strats_deny(mkt, trade_strat_perf, buy_yn, wait_yn):
	func_name = 'buy_strats_deny'
	func_str = f'{lib_name}.{func_name}(mkt, trade_strat_perf, buy_yn={buy_yn}, wait_yn={wait_yn})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	# buy_strat_type = trade_strat_perf.buy_strat_type
	buy_deny_yn = 'N'
	buy_strat_name = trade_strat_perf.buy_strat_name
	# buy_strat_freq = trade_strat_perf.buy_strat_freq

	if buy_strat_name == 'sha' and mkt.strat_sha_yn == 'N':
#		BoW(f'this strat : {buy_strat_name} {buy_strat_freq} is not allowed by settings!!!')
		buy_deny_yn = 'Y'
	elif buy_strat_name == 'imp_macd' and mkt.strat_imp_macd_yn == 'N':
#		BoW(f'this strat : {buy_strat_name} {buy_strat_freq} is not allowed by settings!!!')
		buy_deny_yn = 'Y'
	elif buy_strat_name == 'emax' and mkt.strat_emax_yn == 'N':
#		BoW(f'this strat : {buy_strat_name} {buy_strat_freq} is not allowed by settings!!!')
		buy_deny_yn = 'Y'
	elif buy_strat_name == 'bb_bo' and mkt.strat_bb_bo_yn == 'N':
#		BoW(f'this strat : {buy_strat_name} {buy_strat_freq} is not allowed by settings!!!')
		buy_deny_yn = 'Y'
	elif buy_strat_name == 'bb' and mkt.strat_bb_yn == 'N':
#		BoW(f'this strat : {buy_strat_name} {buy_strat_freq} is not allowed by settings!!!')
		buy_deny_yn = 'Y'
	elif buy_strat_name == 'drop' and mkt.strat_drop_yn == 'N':
#		BoW(f'this strat : {buy_strat_name} {buy_strat_freq} is not allowed by settings!!!')
		buy_deny_yn = 'Y'

	func_end(fnc)
	return buy_yn, wait_yn

#<=====>#

# def sell_strats_get():
# 	func_name = 'sell_strats_get'
# 	func_str = f'{lib_name}.{func_name}()'
# #	G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 	if lib_verbosity >= 2: print_func_name(func_str, adv=2)


# 	func_end(fnc)
# 	return strats

#<=====>#

def buy_strat_sha(mkt, trade_perf, trade_strat_perf, ta):
	func_name = 'buy_strat_sha'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:

		all_passes       = []
		all_fails        = []
		prod_id          = mkt.prod_id
		curr_prc         = mkt.prc_buy
		buy_yn           = 'Y'
		wait_yn          = 'N'
#		show_tests_yn    = st.spot.buy.show_tests_yn
#		show_tests_min   = st.spot.buy.show_tests_min

		rfreq = trade_strat_perf.buy_strat_freq
		r     = freqs_get(rfreq)
		freqs =r[0]

#		if prod_id in ('DAR-USDC','IBEX-USDC'):
#			pprint(ta[rfreq]['sma100'])
#			pprint(ta[rfreq]['sma200'])

#		# General Trend
#		check_list = ['sma100']
#		sma = ta['1d']['sma300']['ago0']
#		msg = f'\t * BUY REQUIRE : {rfreq} Current Price : {curr_prc:>.8f} must be above current 1d sma300 : {sma}'
#		if not sma:
#			buy_yn  = 'N'
#			all_fails.append(msg)
#		elif curr_prc > sma:
#			all_passes.append(msg)
#		else:
#			buy_yn  = 'N'
#			all_fails.append(msg)


#		check_list = []
#		check_list.append(['ema5','ema8'])
#		check_list.append(['ema8','ema13'])
#		check_list.append(['ema13','ema21'])
#		for x, y in check_list:
#			m = '\t * BUY REQUIRE : current {} {} :{:>.8f} >>> {}:{:>.8f}'
#			msg = m.format(rfreq, x, ta[rfreq][x]['ago0'], y, ta[rfreq][y]['ago0'])
#			if ta[rfreq][x]['ago0'] > ta[rfreq][y]['ago0']:
#				all_passes.append(msg)
#			else:
#				all_fails.append(msg)


		# Smoothed Heikin Ashi Trend - Fast - Multi Timeframe Above Current Price
		ago_list = ['ago0','ago1']
		for freq in freqs:
			for ago in ago_list:
				m = '\t * BUY REQUIRE : {} current price : {:>.8f} >>> {} SHA - FAST close {:>.8f} - {}'
				msg = m.format(freq, curr_prc, freq, ta[freq]['sha_fast_close'][ago], ago)
				if curr_prc > ta[freq]['sha_fast_close'][ago]:
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Smoothed Heikin Ashi Trend - Fast - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in freqs:
			for ago in ago_list:
				m = '\t * BUY REQUIRE : {} SHA_FAST candles {} == green : {}'
				msg = m.format(freq, ago, ta[freq]['sha_fast_color'][ago])
				if ta[freq]['sha_fast_color'][ago] == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Smoothed Heikin Ashi Trend - Slow - Multi Timeframe Above Current Price
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				m = '\t * BUY REQUIRE : {} current price : {:>.8f} >>> {} SHA - SLOW close {:>.8f} - {}'
				msg = m.format(freq, curr_prc, freq, ta[freq]['sha_slow_close'][ago], ago)
				if curr_prc > ta[freq]['sha_slow_close'][ago]:
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Smoothed Heikin Ashi Trend - Slow - Multi Timeframe - Candles Are Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				m = '\t * BUY REQUIRE : {} SHA_SLOW candles {} == green : {}'
				msg = m.format(freq, ago, ta[freq]['sha_slow_color'][ago])
				if ta[freq]['sha_slow_color'][ago] == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Check to make sure the body is growing body
		if ta[rfreq]['sha_fast_body']['ago0'] >= ta[rfreq]['sha_fast_body']['ago1'] >= ta[rfreq]['sha_fast_body']['ago2']:
			m = '\t * BUY REQUIRE : {} growing body size TRUE - curr {:>.8f} >>> last {:>.8f} >>>  prev {:>.8f}'
			msg = m.format(rfreq, ta[rfreq]['sha_fast_body']['ago0'], ta[rfreq]['sha_fast_body']['ago1'],  ta[rfreq]['sha_fast_body']['ago2'])
			all_passes.append(msg)
		else:
			m = '\t * BUY REQUIRE : {} growing body size FALSE - curr {:>.8f} >>> last {:>.8f} >>>  prev {:>.8f}'
			msg = m.format(rfreq, ta[rfreq]['sha_fast_body']['ago0'], ta[rfreq]['sha_fast_body']['ago1'],  ta[rfreq]['sha_fast_body']['ago2'])
			buy_yn  = 'N'
			all_fails.append(msg)


		# Check Upper Wick Larger Than Lower Wick
		ago_list = ['ago0', 'ago1', 'ago2']
		for ago in ago_list:
			if ta[rfreq]['sha_fast_wick_upper'][ago] >= ta[rfreq]['sha_fast_wick_lower'][ago]:
				m = '\t * BUY REQUIRE : {} larger upper wick - upper {:>.8f} >>> lower {:>.8f} - {}'
				msg = m.format(rfreq, ta[rfreq]['sha_fast_wick_upper'][ago], ta[rfreq]['sha_fast_wick_lower'][ago], ago)
				all_passes.append(msg)
			else:
				m = '\t * BUY REQUIRE : {} growing body size - upper {:>.8f} <<< lower {:>.8f} - {}' 
				msg = m.format(rfreq, ta[rfreq]['sha_fast_wick_upper'][ago], ta[rfreq]['sha_fast_wick_lower'][ago], ago)
				buy_yn  = 'N'
				all_fails.append(msg)


		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in freqs:
			for ago in ago_list:
				m = '\t * BUY REQUIRE : {} HA candles {} == green : {}'
				msg = m.format(freq, ago, ta[freq]['ha_color'][ago])
				if ta[freq]['ha_color'][ago] == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		if buy_yn == 'Y':
			wait_yn = 'N'
			mkt.buy_strat_type  = 'up'
			mkt.buy_strat_name  = 'sha'
			mkt.buy_strat_freq  = rfreq
		else:
			wait_yn = 'Y'

		trade_strat_perf.pass_cnt     = len(all_passes)
		trade_strat_perf.fail_cnt     = len(all_fails)
		trade_strat_perf.total_cnt    = trade_strat_perf.pass_cnt + trade_strat_perf.fail_cnt
		trade_strat_perf.pass_pct     = round((trade_strat_perf.pass_cnt / trade_strat_perf.total_cnt) * 100, 2)
		trade_strat_perf.all_passes   = all_passes
		trade_strat_perf.all_fails    = all_fails
		trade_strat_perf.buy_yn       = buy_yn
		trade_strat_perf.wait_yn      = wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy_yn  = 'N'
		wait_yn = 'Y'

	# print(f'{func_name} * buy_yn : {buy_yn}  * wait_yn : {wait_yn}')
	# if buy_yn == 'Y':
	# 	speak(func_name)

	trade_strat_perf.buy_yn  = buy_yn
	trade_strat_perf.wait_yn = wait_yn

#	buy_sign_rec(mkt)

	func_end(fnc)
	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn

#<=====>#

def buy_strat_imp_macd(mkt, trade_perf, trade_strat_perf, ta):
	func_name = 'buy_strat_imp_macd'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = mkt.prod_id
		# curr_prc         = mkt.prc_buy
		buy_yn           = 'Y'
		wait_yn          = 'N'

		rfreq = trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(rfreq)
		# atr_rfreq        = "1d"


#		# General Trend
#		check_list = ['sma100']
#		for x in check_list:
#			sma = ta[rfreq][x]['ago0']
#			msg = f'\t * BUY REQUIRE : {rfreq} Current Price : {curr_prc:>.8f} must be above current {x} : {sma}'
#			if not sma:
#				buy_yn  = 'N'
#				all_fails.append(msg)
#			elif curr_prc > sma:
#				all_passes.append(msg)
#			else:
#				buy_yn  = 'N'
#				all_fails.append(msg)


		# Impulse MACD + ATR
		# MACD > Signal
		m = '\t * BUY REQUIRE : {} impulse macd > signal ==> macd : {:>5}, signal : {:>5}'
		msg = m.format(rfreq, ta[rfreq]['imp_macd']['ago0'], ta[rfreq]['imp_macd_sign']['ago0'])
		if ta[rfreq]['imp_macd']['ago0'] > ta[rfreq]['imp_macd_sign']['ago0']:
			all_passes.append(msg)
		else:
			buy_yn  = 'N'
			all_fails.append(msg)


		# MACD Line Should Be Green or Lime
		m = '\t * BUY REQUIRE : {} impulse macd color must be lime or green ==> macd color : {:>5}'
		msg = m.format(rfreq, ta[rfreq]['imp_macd_color']['ago0'])
		if ta[rfreq]['imp_macd_color']['ago0'] in ('lime','green'):
			all_passes.append(msg)
		else:
			buy_yn  = 'N'
			all_fails.append(msg)


		# MACD > Signal - Last
#		m = '\t * BUY REQUIRE : {} last impulse macd > last signal ==> macd : {:>5}, signal : {:>5}'
#		msg = m.format(rfreq, ta[rfreq]['imp_macd']['ago1'], ta[rfreq]['imp_macd_sign']['ago1'])
#		if ta[rfreq]['imp_macd']['ago1'] > ta[rfreq]['imp_macd_sign']['ago1']:
#			all_passes.append(msg)
#		else:
#			buy_yn  = 'N'
#			all_fails.append(msg)


		# MACD & Signal Should Be Sufficiently Appart and Not Hugging
		spread = ta[rfreq]['imp_macd']['ago0'] - ta[rfreq]['imp_macd_sign']['ago0']
		min_spread_pct = 5
		min_spread = ta[rfreq]['atr']['ago0'] * (min_spread_pct/100)
		m = '\t * BUY REQUIRE : {} impulse macd_signal > atr_low * 0.0{} ==> macd : {:>5}, sign : {:>5}, spread : {:>5}, min_spread_pct : {:>5}, min_spread : {:>5}'
		msg = m.format(rfreq, min_spread_pct, ta[rfreq]['imp_macd']['ago0'], ta[rfreq]['imp_macd_sign']['ago0'], spread, min_spread_pct, min_spread)
		if spread > min_spread:
			all_passes.append(msg)
		else:
			buy_yn  = 'N'
			all_fails.append(msg)


#		if 1==1:
#			atr_low = -1 * ta['1d']['atr']['ago0'] / 3
#			m = '\t * BUY REQUIRE : 1h impulse macd < atr_low (-1 * atr/3) ==> macd : {:>5}, atr_low : {:>5}'
#			msg = m.format(ta['1h']['imp_macd']['ago0'], atr_low)
#			if ta['1h']['imp_macd']['ago0'] < atr_low:
#				all_passes.append(msg)
#			else:
#				buy_yn  = 'N'
#				all_fails.append(msg)
#		if 1==1:
#			atr_low = -1 * ta['1d']['atr']['ago0'] / 3
#			m = '\t * BUY REQUIRE : 1h impulse macd_sign < atr_low (-1 * atr/3) ==> macd_sign : {:>5}, atr_low : {:>5}'
#			msg = msg.format(ta['1h']['imp_macd_sign']['ago0'], atr_low)
#			if ta['1h']['imp_macd_sign']['ago0'] < atr_low:
#				all_passes.append(msg)
#			else:
#				buy_yn  = 'N'
#				all_fails.append(msg)


		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = ta[freq]['color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
#				print(f'freq : {freq}, ago : {ago}')
				ha_color = ta[freq]['ha_color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		if buy_yn == 'Y':
			wait_yn = 'N'
			mkt.buy_strat_type  = 'up'
			mkt.buy_strat_name  = 'imp_macd'
			mkt.buy_strat_freq  = rfreq
		else:
			wait_yn = 'Y'

		trade_strat_perf.pass_cnt     = len(all_passes)
		trade_strat_perf.fail_cnt     = len(all_fails)
		trade_strat_perf.total_cnt    = trade_strat_perf.pass_cnt + trade_strat_perf.fail_cnt
		trade_strat_perf.pass_pct     = round((trade_strat_perf.pass_cnt / trade_strat_perf.total_cnt) * 100, 2)
		trade_strat_perf.all_passes   = all_passes
		trade_strat_perf.all_fails    = all_fails
		trade_strat_perf.buy_yn       = buy_yn
		trade_strat_perf.wait_yn      = wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy_yn  = 'N'
		wait_yn = 'Y'

	# print(f'{func_name} * buy_yn : {buy_yn}  * wait_yn : {wait_yn}')
	# if buy_yn == 'Y':
	# 	speak(func_name)

	trade_strat_perf.buy_yn  = buy_yn
	trade_strat_perf.wait_yn = wait_yn

#	buy_sign_rec(mkt)

	func_end(fnc)
	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn

#<=====>#

# Drop
def buy_strat_drop(st, mkt, trade_perf, trade_strat_perf, ta, reserve_release_tf):
	func_name = 'buy_strat_drop'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta, reserve_release_tf={reserve_release_tf})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = mkt.prod_id
		curr_prc         = mkt.prc_buy
		buy_yn           = 'Y'
		wait_yn          = 'N'
		reserve_release_tf = False

		rfreq = trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(rfreq)


#		# General Trend
#		check_list = ['sma100']
#		for x in check_list:
#			sma = ta[rfreq][x]['ago0']
#			msg = f'\t * BUY REQUIRE : {rfreq} Current Price : {curr_prc:>.8f} must be above current {x} : {sma}'
#			if not sma:
#				buy_yn  = 'N'
#				all_fails.append(msg)
#			elif curr_prc > sma:
#				all_passes.append(msg)
#			else:
#				buy_yn  = 'N'
#				all_fails.append(msg)


		# Price has recent x% drop below recent high
#		max30 = ta['1d']['max30']['ago0']
		max24 = ta['1h']['max24']['ago0']
		drop_pct     = settings.get_ovrd(in_dict=st.spot.buy.strats.drop.drop_pct, in_key=prod_id)
		drop_pct_dec = (100-drop_pct) / 100
#		target_prc   = max30 * drop_pct_dec
		target_prc   = max24 * drop_pct_dec

		if prod_id == 'BTC-USDC' and rfreq == '1h':
			ago_list = ['ago0','ago1','ago2','ago3']
			for ago in ago_list:
				prc_drop_pct = round(((curr_prc - max24) / max24) * 100, 2)
				if curr_prc < target_prc:
					msg = f'\t * RESERVES RELEASED * : recent ({ago}) current price {curr_prc:>.8f} below {drop_pct:>.2f}% below max24 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
					RoW(msg)
					if not reserve_release_tf:
						buy_log('')
						buy_log(msg)
						reserve_release_tf = True
#						self.wallet_refresh(force_tf=True)
				else:
					msg = f'\t * RESERVES ACTIVATED * : recent ({ago}) current price {curr_prc:>.8f} below {drop_pct:>.2f}% below max24 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
					GoW(msg)
					if reserve_release_tf:
						buy_log('')
						buy_log(msg)
						reserve_release_tf = False
#						self.wallet_refresh(force_tf=True)

#		print(f'max30        : {max30:>.8f}, drop_pct     : {drop_pct:>.2f}, drop_pct_dec : {drop_pct_dec:>.4f}, target_prc   : {target_prc:>.8f}')

		ago_list = ['ago0','ago1','ago2','ago3']
		for ago in ago_list:
#			cls = ta[rfreq]['close'][ago]
#			prc_drop_pct = round(((cls - max30) / max30) * 100, 2)
#			msg = f'\t * BUY REQUIRE : recent ({ago}) close {cls:>.8f} below {drop_pct:>.2f}% below max30 : {max30:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
			prc_drop_pct = round(((curr_prc - max24) / max24) * 100, 2)
			msg = f'\t * BUY REQUIRE : recent ({ago}) current price {curr_prc:>.8f} below {drop_pct:>.2f}% below max30 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
#			print(msg)
			if curr_prc < target_prc:
				all_passes.append(msg)
			else:
				buy_yn  = 'N'
				all_fails.append(msg)


		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = ta[freq]['color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = ta[freq]['ha_color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		if buy_yn == 'Y':
			wait_yn = 'N'
			mkt.buy_strat_type  = 'dn'
			mkt.buy_strat_name  = 'drop'
			mkt.buy_strat_freq  = rfreq
		else:
			wait_yn = 'Y'

		trade_strat_perf.pass_cnt     = len(all_passes)
		trade_strat_perf.fail_cnt     = len(all_fails)
		trade_strat_perf.total_cnt    = trade_strat_perf.pass_cnt + trade_strat_perf.fail_cnt
		trade_strat_perf.pass_pct     = round((trade_strat_perf.pass_cnt / trade_strat_perf.total_cnt) * 100, 2)
		trade_strat_perf.all_passes   = all_passes
		trade_strat_perf.all_fails    = all_fails
		trade_strat_perf.buy_yn       = buy_yn
		trade_strat_perf.wait_yn      = wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy_yn  = 'N'
		wait_yn = 'Y'

	# print(f'{func_name} * buy_yn : {buy_yn}  * wait_yn : {wait_yn}')
	# if buy_yn == 'Y':
	# 	speak(func_name)

	trade_strat_perf.buy_yn  = buy_yn
	trade_strat_perf.wait_yn = wait_yn

#	buy_sign_rec(mkt)

	func_end(fnc)
	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn, reserve_release_tf

#<=====>#

# Bollinger Band Breakout
def buy_strat_bb_bo(mkt, trade_perf, trade_strat_perf, ta):
	func_name = 'buy_strat_bb_bo'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = mkt.prod_id
		# curr_prc         = mkt.prc_buy
		buy_yn           = 'Y'
		wait_yn          = 'N'

		rfreq = trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(rfreq)


#		# General Trend
#		check_list = ['sma100']
#		for x in check_list:
#			sma = ta[rfreq][x]['ago0']
#			msg = f'\t * BUY REQUIRE : {rfreq} Current Price : {curr_prc:>.8f} must be above current {x} : {sma}'
#			if not sma:
#				buy_yn  = 'N'
#				all_fails.append(msg)
#			elif curr_prc > sma:
#				all_passes.append(msg)
#			else:
#				buy_yn  = 'N'
#				all_fails.append(msg)


		# Current High Above Inner BB Lower
		m = '\t * BUY REQUIRE : current {} high : {:>.8f} above bb upper : {:>.8f}'
		msg = m.format(rfreq, ta[rfreq]['high']['ago0'], ta[rfreq]['bb_upper_bb_bo']['ago0'])
		if ta[rfreq]['high']['ago0'] > ta[rfreq]['bb_upper_bb_bo']['ago0']:
			all_passes.append(msg)
		else:
			buy_yn  = 'N'
			all_fails.append(msg)


		# Current Close Above Inner BB Lower
		m = '\t * BUY REQUIRE : pervious {} close : {:>.8f} above bb upper : {:>.8f}'
		msg = m.format(rfreq, ta[rfreq]['close']['ago1'], ta[rfreq]['bb_upper_bb_bo']['ago1'])
		if ta[rfreq]['close']['ago1'] > ta[rfreq]['bb_upper_bb_bo']['ago1']:
			all_passes.append(msg)
		else:
			buy_yn  = 'N'
			all_fails.append(msg)


		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = ta[freq]['color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = ta[freq]['ha_color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		if buy_yn == 'Y':
			wait_yn = 'N'
			mkt.buy_strat_type  = 'up'
			mkt.buy_strat_name  = 'bb_bo'
			mkt.buy_strat_freq  = rfreq
		else:
			wait_yn = 'Y'

		trade_strat_perf.pass_cnt     = len(all_passes)
		trade_strat_perf.fail_cnt     = len(all_fails)
		trade_strat_perf.total_cnt    = trade_strat_perf.pass_cnt + trade_strat_perf.fail_cnt
		trade_strat_perf.pass_pct     = round((trade_strat_perf.pass_cnt / trade_strat_perf.total_cnt) * 100, 2)
		trade_strat_perf.all_passes   = all_passes
		trade_strat_perf.all_fails    = all_fails
		trade_strat_perf.buy_yn       = buy_yn
		trade_strat_perf.wait_yn      = wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy_yn  = 'N'
		wait_yn = 'Y'

	# print(f'{func_name} * buy_yn : {buy_yn}  * wait_yn : {wait_yn}')
	# if buy_yn == 'Y':
	# 	speak(func_name)

	trade_strat_perf.buy_yn  = buy_yn
	trade_strat_perf.wait_yn = wait_yn

#	buy_sign_rec(mkt)

	func_end(fnc)
	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn

#<=====>#

# Bollinger Band Bounce
def buy_strat_bb(mkt, trade_perf, trade_strat_perf, ta):
	func_name = 'buy_strat_bb'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = mkt.prod_id
		# curr_prc         = mkt.prc_buy
		buy_yn           = 'Y'
		wait_yn          = 'N'

		rfreq = trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(rfreq)

		# curr_color             = ta[rfreq]['color']['ago0']
		# curr_ha_color          = ta[rfreq]['ha_color']['ago0']
		# curr_low               = ta[rfreq]['low']['ago0']
		# curr_high              = ta[rfreq]['high']['ago0']
		curr_close             = ta[rfreq]['close']['ago0']
		# curr_bb_lower_outer    = ta[rfreq]['bb_lower_outer']['ago0']
		# curr_bb_upper_outer    = ta[rfreq]['bb_upper_outer']['ago0']
		curr_bb_lower_inner    = ta[rfreq]['bb_lower_inner']['ago0']
		# curr_bb_upper_inner    = ta[rfreq]['bb_upper_inner']['ago0']

		# last_color             = ta[rfreq]['color']['ago1']
		# last_ha_color          = ta[rfreq]['ha_color']['ago1']
		last_low               = ta[rfreq]['low']['ago1']
		# last_high              = ta[rfreq]['high']['ago1']
		# last_close             = ta[rfreq]['close']['ago1']
		last_bb_lower_outer    = ta[rfreq]['bb_lower_outer']['ago1']
		# last_bb_upper_outer    = ta[rfreq]['bb_upper_outer']['ago1']
		# last_bb_lower_inner    = ta[rfreq]['bb_lower_inner']['ago1']
		# last_bb_upper_inner    = ta[rfreq]['bb_upper_inner']['ago1']

		# prev_color             = ta[rfreq]['color']['ago2']
		# prev_ha_color          = ta[rfreq]['ha_color']['ago2']
		prev_low               = ta[rfreq]['low']['ago2']
		# prev_high              = ta[rfreq]['high']['ago2']
		# prev_close             = ta[rfreq]['close']['ago2']
		prev_bb_lower_outer    = ta[rfreq]['bb_lower_outer']['ago2']
		# prev_bb_upper_outer    = ta[rfreq]['bb_upper_outer']['ago2']
		# prev_bb_lower_inner    = ta[rfreq]['bb_lower_inner']['ago2']
		# prev_bb_upper_inner    = ta[rfreq]['bb_upper_inner']['ago2']

#		sma200                 = ta[rfreq]['sma200']['ago0']


#		# General Trend
#		check_list = ['sma100']
#		for x in check_list:
#			sma = ta[rfreq][x]['ago0']
#			msg = f'\t * BUY REQUIRE : {rfreq} Current Price : {curr_prc:>.8f} must be below current {x} : {sma}'
#			if not sma:
#				buy_yn  = 'N'
#				all_fails.append(msg)
#			elif curr_prc < sma:
#				all_passes.append(msg)
#			else:
#				buy_yn  = 'N'
#				all_fails.append(msg)


		# Last Close Below Outer BB Lower
		msg = f'\t * BUY REQUIRE : {rfreq} last low : {last_low:>.8f} < bb lower outer : {last_bb_lower_outer:>.8f} or prev low : {prev_low:>.8f} < bb lower outer : {prev_bb_lower_outer:>.8f}'
		if last_low < last_bb_lower_outer or prev_low < prev_bb_lower_outer:
			all_passes.append(msg)
		else:
			buy_yn  = 'N'
			all_fails.append(msg)


		# Current Close Above Inner BB Lower
		msg = f'\t * BUY REQUIRE : {rfreq} current close : {curr_close:>.8f} above inner bb lower : {curr_bb_lower_inner:>.8f}'
		if curr_close > curr_bb_lower_inner:
			all_passes.append(msg)
		else:
			buy_yn  = 'N'
			all_fails.append(msg)


		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = ta[freq]['color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = ta[freq]['ha_color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		if buy_yn == 'Y':
			wait_yn = 'N'
			mkt.buy_strat_type  = 'dn'
			mkt.buy_strat_name  = 'bb'
			mkt.buy_strat_freq  = rfreq
		else:
			wait_yn = 'Y'

		trade_strat_perf.pass_cnt     = len(all_passes)
		trade_strat_perf.fail_cnt     = len(all_fails)
		trade_strat_perf.total_cnt    = trade_strat_perf.pass_cnt + trade_strat_perf.fail_cnt
		trade_strat_perf.pass_pct     = round((trade_strat_perf.pass_cnt / trade_strat_perf.total_cnt) * 100, 2)
		trade_strat_perf.all_passes   = all_passes
		trade_strat_perf.all_fails    = all_fails
		trade_strat_perf.buy_yn       = buy_yn
		trade_strat_perf.wait_yn      = wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy_yn  = 'N'
		wait_yn = 'Y'

	# print(f'{func_name} * buy_yn : {buy_yn}  * wait_yn : {wait_yn}')
	# if buy_yn == 'Y':
	# 	speak(func_name)

	trade_strat_perf.buy_yn  = buy_yn
	trade_strat_perf.wait_yn = wait_yn

#	buy_sign_rec(mkt)

	func_end(fnc)
	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn

#<=====>#

def buy_strat_emax(mkt, trade_perf, trade_strat_perf, ta):
	func_name = 'buy_strat_emax'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
		prod_id          = mkt.prod_id
		# curr_prc         = mkt.prc_buy
		buy_yn           = 'Y'
		wait_yn          = 'N'

		all_passes       = []
		all_fails        = []

		rfreq = trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(rfreq)


#		# General Trend
#		check_list = ['sma100']
#		for x in check_list:
#			sma = ta[rfreq][x]['ago0']
#			msg = f'\t * BUY REQUIRE : {rfreq} Current Price : {curr_prc:>.8f} must be above current {x} : {sma}'
#			if not sma:
#				buy_yn  = 'N'
#				all_fails.append(msg)
#			elif curr_prc > sma:
#				all_passes.append(msg)
#			else:
#				buy_yn  = 'N'
#				all_fails.append(msg)


		# Exponential Moving Average Crosses
		if 1==1:
			m = '\t * BUY REQUIRE : current 15min ema5 :{:>.8f} >>> ema8:{:>.8f}'
			msg = m.format(ta['15min']['ema5']['ago0'], ta['15min']['ema8']['ago0'])
			if ta['15min']['ema5']['ago0'] > ta['15min']['ema8']['ago0']:
				all_passes.append(msg)
			else:
				buy_yn  = 'N'
				all_fails.append(msg)
		if 1==1:
			m = '\t * BUY REQUIRE : current 15min ema8 :{:>.8f} >>> ema13:{:>.8f}'
			msg = m.format(ta['15min']['ema8']['ago0'], ta['15min']['ema13']['ago0'])
			if ta['15min']['ema8']['ago0'] > ta['15min']['ema13']['ago0']:
				all_passes.append(msg)
			else:
				buy_yn  = 'N'
				all_fails.append(msg)
		if 1==1:
			m = '\t * BUY REQUIRE : current 15min ema13 :{:>.8f} >>> ema21:{:>.8f}'
			msg = m.format(ta['15min']['ema13']['ago0'], ta['15min']['ema21']['ago0'])
			if ta['15min']['ema13']['ago0'] > ta['15min']['ema21']['ago0']:
				all_passes.append(msg)
			else:
				buy_yn  = 'N'
				all_fails.append(msg)


		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = ta[freq]['color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = ta[freq]['ha_color'][ago]
				msg = f'\t * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy_yn  = 'N'
					all_fails.append(msg)


		if buy_yn == 'Y':
			wait_yn = 'N'
			mkt.buy_strat_type  = 'up'
			mkt.buy_strat_name  = 'ema_cross'
			mkt.buy_strat_freq  = rfreq
		else:
			wait_yn = 'Y'

		trade_strat_perf.pass_cnt     = len(all_passes)
		trade_strat_perf.fail_cnt     = len(all_fails)
		trade_strat_perf.total_cnt    = trade_strat_perf.pass_cnt + trade_strat_perf.fail_cnt
		trade_strat_perf.pass_pct     = round((trade_strat_perf.pass_cnt / trade_strat_perf.total_cnt) * 100, 2)
		trade_strat_perf.all_passes   = all_passes
		trade_strat_perf.all_fails    = all_fails
		trade_strat_perf.buy_yn       = buy_yn
		trade_strat_perf.wait_yn      = wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy_yn  = 'N'
		wait_yn = 'Y'

	# print(f'{func_name} * buy_yn : {buy_yn}  * wait_yn : {wait_yn}')
	# if buy_yn == 'Y':
	# 	speak(func_name)

	trade_strat_perf.buy_yn  = buy_yn
	trade_strat_perf.wait_yn = wait_yn

#	buy_sign_rec(mkt)

	func_end(fnc)
	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn

#<=====>#

# def buy_strat_ema_stoch(st, mkt, trade_perf, trade_strat_perf, ta):
# 	func_name = 'buy_strat_ema_stoch'
# 	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
# 	G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 	if lib_verbosity >= 2: print_func_name(func_str, adv=2)


# 	'''
# 	buy discount, sell premium
# 	https://www.youtube.com/watch?v=R8yLzmF_uPI

# 	possible higher high lower low etc price algo determination... last breach of an EMA such as 100?
# 	possible higher high lower low etc indicator algo determination... last breach of oversold/overbought

# 	long - buy at discounted price
# 		above 200per EMA 
# 		enter when the price has pulled back to at least the 50 EMA (100 EMA breach? for higher low)
# 		divergence - higher low on price, lower low stochastic while oversold

# 	short 
# 		below 200per EMA 
# 		enter when the price has reached to at least the 50 EMA (100 EMA breach? for lower high)
# 		divergence - lower high on price, higher high stochastic while overbought


# 	multi-timeframe confirmation
# 		lower timeframe 30m or 1hr
# 		ema lines show ranging with the 50 upwards, 100 less so, 200 flattish

# 	'''


# 	prod_id          = mkt.prod_id
# 	curr_prc         = mkt.prc_buy
# 	buy_yn           = 'Y'
# 	wait_yn          = 'N'
# 	show_tests_yn    = st.spot.buy.show_tests_yn
# 	show_tests_min   = st.spot.buy.show_tests_min

# 	all_passes       = []
# 	all_fails        = []

# 	# General Trend
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : Current Price : {:>.8f} must be above current 15min SMA_100 : {:>.8f}'
# 		msg = m.format(curr_prc, ta['15min']['sma100']['ago0'])
# 		if curr_prc > ta['15min']['sma100']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : Current Price : {:>.8f} must be above current 15min SMA_200 : {:>.8f}'
# 		msg = m.format(curr_prc, ta['15min']['sma200']['ago0'])
# 		if curr_prc > ta['15min']['sma200']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)


# 	# Current Candle is Green
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : 5min candle green ==> current : {:>5}'
# 		msg = m.format(ta['5min']['color']['ago0'])
# 		if ta['5min']['color']['ago0'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : 15min candle green ==> current : {:>5}'
# 		msg = m.format(ta['15min']['color']['ago0'])
# 		if ta['15min']['color']['ago0'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : 30min candle green ==> current : {:>5}'
# 		msg = m.format(ta['30min']['color']['ago0'])
# 		if ta['30min']['color']['ago0'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)


# 	# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : 5min HA candles green ==> current : {:>5}, last : {:>5}'
# 		msg = m.format(ta['5min']['ha_color']['ago0'], ta['5min']['ha_color']['ago1'])
# 		if ta['5min']['ha_color']['ago0'] == 'green' and ta['5min']['ha_color']['ago1'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : 15min HA candles green ==> current : {:>5}, last : {:>5}'
# 		msg = m.format(ta['15min']['ha_color']['ago0'], ta['15min']['ha_color']['ago1'])
# 		if ta['15min']['ha_color']['ago0'] == 'green' and ta['15min']['ha_color']['ago1'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : 30min HA candles green ==> current : {:>5}, last : {:>5}'
# 		msg = m.format(ta['30min']['ha_color']['ago0'], ta['30min']['ha_color']['ago1'])
# 		if ta['30min']['ha_color']['ago0'] == 'green' and ta['30min']['ha_color']['ago1'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : 15min HA candles green ==> current : {:>5}, last : {:>5}'
# 		msg = m.format(ta['15min']['ha_color']['ago0'], ta['15min']['ha_color']['ago1'])
# 		if ta['15min']['ha_color']['ago0'] == 'green' and ta['15min']['ha_color']['ago1'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)


# 	# Exponential Moving Average Crosses
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : current 15min ema5 :{:>.8f} >>> ema8:{:>.8f}'
# 		msg = m.format(ta['15min']['ema5']['ago0'], ta['15min']['ema8']['ago0'])
# 		if ta['15min']['ema5']['ago0'] > ta['15min']['ema8']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : current 15min ema8 :{:>.8f} >>> ema13:{:>.8f}'
# 		msg = m.format(ta['15min']['ema8']['ago0'], ta['15min']['ema13']['ago0'])
# 		if ta['15min']['ema8']['ago0'] > ta['15min']['ema13']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '\t * BUY REQUIRE : current 15min ema13 :{:>.8f} >>> ema21:{:>.8f}'
# 		msg = m.format(ta['15min']['ema13']['ago0'], ta['15min']['ema21']['ago0'])
# 		if ta['15min']['ema13']['ago0'] > ta['15min']['ema21']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy_yn  = 'N'
# 			all_fails.append(msg)


# 	if buy_yn == 'Y':
# 		wait_yn = 'N'
# 		mkt.buy_strat_type  = 'up'
# 		mkt.buy_strat_name  = 'ema_cross'
# 		mkt.buy_strat_freq  = rfreq
# 	else:
# 		wait_yn = 'Y'

# 	trade_strat_perf.pass_cnt = len(all_passes)
# 	trade_strat_perf.fail_cnt = len(all_fails)
# 	trade_strat_perf.total_cnt = trade_strat_perf.pass_cnt + trade_strat_perf.fail_cnt
# 	trade_strat_perf.pass_pct = round((trade_strat_perf.pass_cnt / trade_strat_perf.total_cnt) * 100, 2)

# 	buy_disp(trade_strat_perf)

# #	m = 'BUY TESTS => {:<12} => {:^6} => {:<30} => gain_pct_hr : {:>6.2f}%, pass_cnt : {:>5}, fail_cnt : {:>5}, pass_pct : {:>6.2f}%'
# #	msg = m.format(prod_id, rfreq, 'Strat EMA Crossover', trade_strat_perf.gain_loss_pct_hr, pass_cnt, fail_cnt, pass_pct)
# #
# ##	print_adv(1)
# #	cp_pct_color_100(trade_strat_perf.pass_pct, msg)
# 	if buy_yn == 'Y' or show_tests_yn in ('Y') or trade_strat_perf.pass_pct >= show_tests_min:
# 		for e in all_passes:
# 			G(e)
# 		for e in all_fails:
# 			R(e)

# #	cp_pct_color_100(pass_pct, msg)
# #	if buy_yn == 'Y' or show_tests_yn in ('Y','F') or pass_pct >= show_tests_min:
# #		if buy_yn == 'Y': WoG(msg)
# #		else: WoB(msg)
# #		if buy_yn == 'Y' or show_tests_yn in ('Y') or pass_pct >= show_tests_min:
# #			for e in all_passes:
# #				WoG(e)
# #		for e in all_fails:
# #			WoR(e)
# #	else:
# #		if pass_pct >= 80:
# #			GoW(msg)
# #		elif pass_pct >= 50:
# #			G(msg)
# #		else:
# #			print(msg)

# #		print('buy_yn : {}, wait_yn : {}'.format(buy_yn, wait_yn))

# 	trade_strat_perf.buy_yn  = buy_yn
# 	trade_strat_perf.wait_yn = wait_yn

# #	buy_sign_rec(mkt)

# 	func_end(fnc)
#	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn

#<=====>#

# def buy_strat_ema_stoch(st, mkt, trade_perf, trade_strat_perf, ta):
# 	func_name = 'buy_strat_ema_stoch'
# 	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
# #	G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

# 	show_tests_yn    = st.spot.buy.show_tests_yn
# 	show_tests_min   = st.spot.buy.show_tests_min

# 	'''
# 	https://www.youtube.com/watch?v=wzUk3gBabvQ
	
# 	https://drive.google.com/file/d/1tz0MLOW2dyH-8mKEviP4_3BZ64yxY9Jg/view
	
# 	//@version=5
# 	strategy("Supertrend with ADX Filter and Range Filter Strategy with NNFX ATR Stop Loss", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=15)
	
# 	// Inputs for ATR and Supertrend
# 	atrPeriod = input.int(8, title="ATR Length")
# 	factor = input.float(1.6, title="Factor", step=0.01)
# 	tradeDirection = input.string("Long Only", title="Trade Direction", options=["Long Only", "Short Only", "Both"])
	
# 	// ADX settings
# 	adxlen = input.int(14, title="ADX Smoothing")
# 	dilen = input.int(14, title="DI Length")
# 	adxLimit = input.int(18, title="ADX Limit Level")
	
# 	// Calculating ADX
# 	dirmov(len) =>
# 		up = ta.change(high)
# 		down = -ta.change(low)
# 		plusDM = na(up) ? na : (up > down and up > 0 ? up : 0)
# 		minusDM = na(down) ? na : (down > up and down > 0 ? down : 0)
# 		truerange = ta.rma(ta.tr, len)
# 		plus = fixnan(100 * ta.rma(plusDM, len) / truerange)
# 		minus = fixnan(100 * ta.rma(minusDM, len) / truerange)
# 		[plus, minus]
	
# 	adx(dilen, adxlen) =>
# 		[plus, minus] = dirmov(dilen)
# 		sum = plus + minus
# 		adx = 100 * ta.rma(math.abs(plus - minus) / (sum == 0 ? 1 : sum), adxlen)
# 		adx
	
# 	sig = adx(dilen, adxlen)
# 	adx_condition = sig > adxLimit
	
# 	// Calculating Supertrend
# 	[_, direction] = ta.supertrend(factor, atrPeriod)
	
# 	// Inputs for Range Filter
# 	per = input.int(175, minval=1, title="Sampling Period for Range Filter")
# 	mult = input.float(5.0, minval=0.1, title="Range Multiplier for Range Filter")
# 	src = close // defining the source for the range filter calculation
	
# 	// Smooth Average Range Calculation for Range Filter
# 	smoothrng(x, t, m) =>
# 		wper = t * 2 - 1
# 		avrng = ta.ema(math.abs(x - x[1]), t)
# 		smoothrng = ta.ema(avrng, wper) * m
# 		smoothrng
# 	smrng = smoothrng(src, per, mult)
	
# 	// Range Filter Calculation
# 	rngfilt(x, r) =>
# 		rngfilt = x
# 		rngfilt := x > nz(rngfilt[1]) ? x - r < nz(rngfilt[1]) ? nz(rngfilt[1]) : x - r : 
# 		   x + r > nz(rngfilt[1]) ? nz(rngfilt[1]) : x + r
# 		rngfilt
# 	filt = rngfilt(src, smrng)
	
# 	// Filter Direction
# 	var float upward = na
# 	var float downward = na
# 	upward := filt > filt[1] ? nz(upward[1]) + 1 : filt < filt[1] ? 0 : nz(upward[1])
# 	downward := filt < filt[1] ? nz(downward[1]) + 1 : filt > filt[1] ? 0 : nz(downward[1])
	
# 	// Target Bands
# 	hband = filt + smrng
# 	lband = filt - smrng
	
# 	// Colors
# 	upColor = color.white
# 	midColor = #90bff9
# 	downColor = color.blue
	
# 	filtcolor = upward > 0 ? upColor : downward > 0 ? downColor : midColor
# 	barcolor = src > filt and src > src[1] and upward > 0 ? upColor :
# 	   src > filt and src < src[1] and upward > 0 ? upColor : 
# 	   src < filt and src < src[1] and downward > 0 ? downColor : 
# 	   src < filt and src > src[1] and downward > 0 ? downColor : midColor
	
# 	filtplot = plot(filt, color=filtcolor, linewidth=2, title="Range Filter")
	
# 	// Target
# 	hbandplot = plot(hband, color=color.new(upColor, 70), title="High Target")
# 	lbandplot = plot(lband, color=color.new(downColor, 70), title="Low Target")
	
# 	// Fills
# 	fill(hbandplot, filtplot, color=color.new(upColor, 90), title="High Target Range")
# 	fill(lbandplot, filtplot, color=color.new(downColor, 90), title="Low Target Range")
	
# 	// Bar Color
# 	barcolor(barcolor)
	
# 	// Break Outs
# 	longCond = bool(na)
# 	shortCond = bool(na)
# 	longCond := src > filt and src > src[1] and upward > 0 or 
# 	   src > filt and src < src[1] and upward > 0
# 	shortCond := src < filt and src < src[1] and downward > 0 or 
# 	   src < filt and src > src[1] and downward > 0
	
# 	CondIni = 0
# 	CondIni := longCond ? 1 : shortCond ? -1 : CondIni[1]
# 	rangeLongCondition = longCond and CondIni[1] == -1
# 	rangeShortCondition = shortCond and CondIni[1] == 1
	
# 	// Define entry points with ADX and Supertrend filter
# 	longEntryCondition = ta.change(direction) < 0 and adx_condition and (tradeDirection == "Long Only" or tradeDirection == "Both")
# 	shortEntryCondition = ta.change(direction) > 0 and adx_condition and (tradeDirection == "Short Only" or tradeDirection == "Both")
	
# 	// ATR Settings for SL and TP
# 	atrLength = input.int(50, title="ATR Length for Stop Loss", minval=1)
# 	atrMultiplierSL = input.float(10, title="ATR Multiplier for SL", minval=0.1)
# 	riskRewardRatio = input.float(100.0, title="Risk/Reward Ratio", minval=0.1)
	
# 	atr = ta.atr(atrLength)
# 	risk = atr * atrMultiplierSL
	
# 	// Strategy entry with ATR-based stop loss and take profit
# 	if (longEntryCondition and (tradeDirection == "Long Only" or tradeDirection == "Both"))
# 		strategy.entry("Long", strategy.long)
# 		strategy.exit("Close Long", "Long", stop=close - risk, limit=close + risk * riskRewardRatio)
	
# 	if (shortEntryCondition and (tradeDirection == "Short Only" or tradeDirection == "Both"))
# 		strategy.entry("Short", strategy.short)
# 		strategy.exit("Close Short", "Short", stop=close + risk, limit=close - risk * riskRewardRatio)
	
# 	// Strategy exit conditions based on Range Filter
# 	exitLongCondition = rangeShortCondition and (tradeDirection == "Long Only" or tradeDirection == "Both")
# 	exitShortCondition = rangeLongCondition and (tradeDirection == "Short Only" or tradeDirection == "Both")
	
# 	if (exitLongCondition)
# 		strategy.close("Long")
# 	if (exitShortCondition)
# 		strategy.close("Short")
	
# 	// Optional Plotting for visualization
# 	plot(sig, title="ADX", color=color.red)
# 	plot(filt, "Range Filter", color=color.green)
# 	plot(filt[1], title="Previous Range Filter", color=color.blue)
# 	plotshape(rangeLongCondition, title="Buy Signal", text="Buy", textcolor=color.white, style=shape.labelup, size=size.small, location=location.belowbar, color=color.new(#aaaaaa, 20))
# 	plotshape(rangeShortCondition, title="Sell Signal", text="Sell", textcolor=color.white, style=shape.labeldown, size=size.small, location=location.abovebar, color=color.new(downColor, 20))
# 	'''

# 	trade_strat_perf.buy_yn  = buy_yn
# 	trade_strat_perf.wait_yn = wait_yn

# #	buy_sign_rec(mkt)

# 	func_end(fnc)
	#return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn

#<=====>#

# def buy_strat_trend_strength(st, mkt, trade_perf, trade_strat_perf, ta):
# 	func_name = 'buy_strat_trend_strength'
# 	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
# #	G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

# 	show_tests_yn    = st.spot.buy.show_tests_yn
# 	show_tests_min   = st.spot.buy.show_tests_min

# 	'''
# 	https://www.youtube.com/watch?v=cohyn6E0sXk
	
# 	// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
# 	// © AlgoAlpha
	
# 	//@version=5
# 	indicator("Trend Strength Signals [AlgoAlpha]", "AlgoAlpha - 𝑻𝒓𝒆𝒏𝒅 𝑺𝒕𝒓𝒆𝒏𝒈𝒕𝒉", true)
# 	c = input.bool(true, "Enable Cloud")
# 	lenn = input.int(20, "Period")
# 	mult = input.float(2.5, "Standard Deviation Multiplier for TP")
# 	tc = input.int(25, "Gauge Size", minval = 3)
# 	upColor = input.color(#00ffbb, "Up Color")
# 	downColor = input.color(#ff1100, "Down Color")
	
# 	// Guage Function
# 	t = table.new(position.middle_right, 3, tc+1),
# 	printTable(txt, col, row, color, txt1, col1, row1, color1) =>  
# 		table.cell(t, col, row, txt, bgcolor = color),
# 		table.cell(t, col1, row1, txt1, bgcolor = color1, text_color = color.white)
	
# 	len = lenn
# 	src = close
	
# 	basis = ta.sma(src, lenn)
# 	upper = basis + ta.stdev(src, len, true)
# 	lower = basis - ta.stdev(src, len, true)
	
# 	upper1 = basis + ta.stdev(src, len, true) * mult
# 	lower1 = basis - ta.stdev(src, len, true) * mult
	
# 	var trend = 0
	
# 	if src > basis and src > upper
# 		trend := 1
# 	if src < basis and src < lower
# 		trend := -1
	
# 	pu=plot(upper, "upper Line", color.new(chart.fg_color, 80), display = c ? display.all : display.none)
# 	pl=plot(lower, "lower Line", color.new(chart.fg_color, 80), display = c ? display.all : display.none)
	
# 	barcolor(src > upper ? upColor : src < lower ? downColor : chart.fg_color)
	
# 	grad = math.abs(basis-src)/(ta.highest(basis-src, 200))*100
# 	grad1 = math.min(grad,40)
# 	grad1 := 100-grad1
	
# 	xMax = 100
# 	xMin = 0
# 	range_ = xMax - xMin
# 	y = 1 - grad / range_
# 	y := y > 100 ? 100 : y < 0 ? 0 : y
	
# 	fill(pu, pl, color.new(chart.fg_color, ta.sma(grad1, 7)), "Trend Fill", display = c ? display.all : display.none)
	
# 	plotshape(ta.crossover(trend, 0), "Bullish Trend", shape.labelup, location.belowbar, upColor, text = "▲", textcolor = chart.fg_color)
# 	plotshape(ta.crossunder(trend, 0), "Bearish Trend", shape.labeldown, location.abovebar, downColor, text = "▼", textcolor = chart.fg_color)
	
# 	plotchar(ta.crossover(src, lower1), "Short TP", "X", location.belowbar, upColor, size = size.tiny)
# 	plotchar(ta.crossunder(src, upper1), "Long TP", "X", location.abovebar, downColor, size = size.tiny)
	
# 	// Draw Gauge
	
# 	for i = 1 to tc
# 		color_ = chart.fg_color
# 		color = color.from_gradient(i, 1, tc, src > basis ? upColor : downColor, color_)
# 		printTable("", 1, i, color, ">", 1, math.round(y*tc), #ffffff00)
	
# 	///////Alerts
# 	alertcondition(ta.crossover(trend, 0), "Bullish Trend")
# 	alertcondition(ta.crossunder(trend, 0), "Bearish Trend")
# 	alertcondition(ta.crossover(src, lower1), "Short TP")
# 	alertcondition(ta.crossunder(src, upper1), "Long TP")
# 	'''

# 	trade_strat_perf.buy_yn  = buy_yn
# 	trade_strat_perf.wait_yn = wait_yn

# #	buy_sign_rec(mkt)

# 	return mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn

#<=====>#

def sell_strats_avail_get(mkt):
	func_name = 'sell_strats_avail_get'
	func_str = f'{lib_name}.{func_name}(mkt)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)


	func_end(fnc)
	return mkt

#<=====>#

def sell_strats_check(st, mkt, ta, pos, sell_yn, hodl_yn, sell_signals, sell_block_yn='N'):
	func_name = 'sell_strats_check'
	func_str = f'{lib_name}.{func_name}(st, mkt, ta, pos, sell_block_yn={sell_block_yn})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	# Strategy Exit - Smoothed Heikin Ashi
	if sell_yn == 'N':
		if pos.buy_strat_name == 'sha':
#			print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_strat_sha()')
			mkt, pos, sell_yn, hodl_yn = sell_strat_sha(st, mkt, ta, pos, sell_block_yn=sell_block_yn)
			sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
			sell_signals.append(sell_signal)

	# Strategy Exit - Impulse MACD
	if sell_yn == 'N':
		if pos.buy_strat_name == 'imp_macd':
#			print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_strat_imp_macd()')
			mkt, pos, sell_yn, hodl_yn = sell_strat_imp_macd(st, mkt, ta, pos, sell_block_yn=sell_block_yn)
			sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
			sell_signals.append(sell_signal)

	# Strategy Exit - Bollinger Band
	if sell_yn == 'N':
		if pos.buy_strat_name == 'bb':
#			print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_strat_imp_macd()')
			mkt, pos, sell_yn, hodl_yn = sell_strat_bb(st, mkt, ta, pos, sell_block_yn=sell_block_yn)
			sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
			sell_signals.append(sell_signal)

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn, sell_signals

#<=====>#

def sell_strat_sha(st, mkt, ta, pos, sell_block_yn='N'):
	func_name = 'sell_strat_sha'
	func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
		# only_exit_if_profit_yn = 'Y'
		prod_id     = mkt.prod_id
		sell_prc    = mkt.prc_sell
		all_sells  = []
		all_hodls   = []
		sell_yn = 'N'
		hodl_yn = 'Y'
		show_tests_yn         = st.spot.sell.show_tests_yn

		freq = pos.buy_strat_freq
#		print('buy_strat_type : {}'.format(pos.buy_strat_type))
#		print('buy_strat_name : {}'.format(pos.buy_strat_name))
#		print('buy_strat_freq : {}'.format(pos.buy_strat_freq))

		# Check if sha fast body is growing or shrinking
		sha_fast_body_shrinking_tf = True
		sha_fast_body_curr = ta[freq]['sha_fast_body']['ago0']
		sha_fast_body_last = ta[freq]['sha_fast_body']['ago1']
		sha_fast_body_prev = ta[freq]['sha_fast_body']['ago2']

		if sha_fast_body_curr <= sha_fast_body_last <= sha_fast_body_prev:
			sha_fast_body_shrinking_tf = True
		else:
			sha_fast_body_shrinking_tf = False

		if sha_fast_body_shrinking_tf:
			msg = f'\t * SELL COND: {freq} sha fast body is shrinking - curr {sha_fast_body_curr:>.8f} <<< last {sha_fast_body_last:>.8f} <<<  prev {sha_fast_body_prev:>.8f}'
			all_sells.append(msg)
		else:
			msg = f'\t * HODL COND: {freq} sha fast body not shrinking - curr {sha_fast_body_curr:>.8f} >>> last {sha_fast_body_last:>.8f} >>>  prev {sha_fast_body_prev:>.8f}'
			all_hodls.append(msg)

		# Check if sha slow body is growing or shrinking
		sha_slow_body_shrinking_tf = True
		sha_slow_body_curr = ta[freq]['sha_slow_body']['ago0']
		sha_slow_body_last = ta[freq]['sha_slow_body']['ago1']
		sha_slow_body_prev = ta[freq]['sha_slow_body']['ago2']

		if sha_slow_body_curr <= sha_slow_body_last <= sha_slow_body_prev:
			sha_slow_body_shrinking_tf = True
		else:
			sha_slow_body_shrinking_tf = False

		if sha_slow_body_shrinking_tf:
			msg = f'\t * SELL COND: {freq} sha slow body is shrinking - curr {sha_slow_body_curr:>.8f} <<< last {sha_slow_body_last:>.8f} <<<  prev {sha_slow_body_prev:>.8f}'
			all_sells.append(msg)
		else:
			msg = f'\t * HODL COND: {freq} sha slow body not shrinking - curr {sha_slow_body_curr:>.8f} >>> last {sha_slow_body_last:>.8f} >>>  prev {sha_slow_body_prev:>.8f}'
			all_hodls.append(msg)



		# check if sha fast upper wick larger than lower wick
		sha_fast_upper_wick_weakening_tf = True
		ago_list = ['ago0', 'ago1', 'ago2', 'ago3']
		temp_all_sells = []
		temp_all_hodls = []
		for ago in ago_list:
			sha_fast_wick_upper = ta[freq]['sha_fast_wick_upper'][ago]
			sha_fast_wick_lower = ta[freq]['sha_fast_wick_lower'][ago]
			if ago == 'ago0': ago_desc = 'curr'
			elif ago == 'ago1': ago_desc = 'last'
			elif ago == 'ago2': ago_desc = 'prev'
			else: ago = 'curr'
			if sha_fast_wick_upper <= sha_fast_wick_lower:
				msg = f'\t * SELL COND: {freq} {ago_desc} smaller upper wick - upper {sha_fast_wick_upper:>.8f} <<< lower {sha_fast_wick_lower:>.8f}'
				temp_all_sells.append(msg)
			else:
				sha_fast_upper_wick_weakening_tf = False
				msg = f'\t * HODL COND: {freq} {ago_desc} larger upper wick - upper {sha_fast_wick_upper:>.8f} >>> lower {sha_fast_wick_lower:>.8f}' 
				temp_all_hodls.append(msg)
			# Need 4 in a row for test2 to be True

		if sha_fast_upper_wick_weakening_tf:
			msg = f'\t * SELL COND: {freq} smaller upper wick for 4 consecutive candles'
			all_sells.append(msg)
			for msg in temp_all_sells:
				all_sells.append(msg)
		else:
			msg = f'\t * HODL COND: {freq} larger upper wick in last 4 consecutive candles'
			all_hodls.append(msg)
			for msg in temp_all_hodls:
				all_hodls.append(msg)



		# check if sha slow upper wick larger than lower wick
		sha_slow_upper_wick_weakening_tf = True
		ago_list = ['ago0', 'ago1', 'ago2', 'ago3']
		temp_all_sells = []
		temp_all_hodls = []
		for ago in ago_list:
			sha_slow_wick_upper = ta[freq]['sha_slow_wick_upper'][ago]
			sha_slow_wick_lower = ta[freq]['sha_slow_wick_lower'][ago]
			if ago == 'ago0': ago_desc = 'curr'
			elif ago == 'ago1': ago_desc = 'last'
			elif ago == 'ago2': ago_desc = 'prev'
			else: ago = 'curr'
			if sha_slow_wick_upper <= sha_slow_wick_lower:
				msg = f'\t * SELL COND: {freq} {ago_desc} smaller upper wick - upper {sha_slow_wick_upper:>.8f} <<< lower {sha_slow_wick_lower:>.8f}'
				temp_all_sells.append(msg)
			else:
				sha_slow_upper_wick_weakening_tf = False
				msg = f'\t * HODL COND: {freq} {ago_desc} larger upper wick - upper {sha_slow_wick_upper:>.8f} >>> lower {sha_slow_wick_lower:>.8f}' 
				temp_all_hodls.append(msg)
			# Need 4 in a row for test2 to be True

		if sha_slow_upper_wick_weakening_tf:
			msg = f'\t * SELL COND: {freq} smaller upper wick for 4 consecutive candles'
			all_sells.append(msg)
			for msg in temp_all_sells:
				all_sells.append(msg)
		else:
			msg = f'\t * HODL COND: {freq} larger upper wick in last 4 consecutive candles'
			all_hodls.append(msg)
			for msg in temp_all_hodls:
				all_hodls.append(msg)



		# check if the price is intersecting the sha fast candles
		sha_fast_close = ta[freq]['sha_fast_close']['ago0']
		if sell_prc < sha_fast_close:
			sell_prc_intersect_sha_fast_tf = True
			msg = f'\t * SELL COND: {freq} curr_price : {sell_prc:>.8f} is be below sha_fast_close {sha_fast_close:>.8f}'
			all_sells.append(msg)
		else:
			sell_prc_intersect_sha_fast_tf = False
			msg = f'\t * HODL COND: {freq} curr_price : {sell_prc:>.8f} is be above sha_fast_close {sha_fast_close:>.8f}'
			all_hodls.append(msg)



		# check if sha fast candles are reddening
		sha_fast_color_curr = ta[freq]['sha_fast_color']['ago0']
		sha_fast_color_last = ta[freq]['sha_fast_color']['ago1']
		sha_fast_color_prev = ta[freq]['sha_fast_color']['ago2']
		if sha_fast_color_curr == 'red' and sha_fast_color_last == 'red' and sha_fast_color_prev == 'red':
			sha_fast_reddening_tf = True
			msg = f'\t * SELL COND: {freq} sha fast colors ==> curr : {sha_fast_color_curr:>5}, last : {sha_fast_color_last:>5}, prev : {sha_fast_color_prev:>5}'
			all_sells.append(msg)
		else:
			sha_fast_reddening_tf = False
			msg = f'\t * HODL COND: {freq} sha fast colors ==> curr : {sha_fast_color_curr:>5}, last : {sha_fast_color_last:>5}, prev : {sha_fast_color_prev:>5}'
			# YES!!! Allow the green candles to override the price touch above!
			all_hodls.append(msg)



		# check if sha slow candles are reddening
		sha_slow_color_curr = ta[freq]['sha_slow_color']['ago0']
		sha_slow_color_last = ta[freq]['sha_slow_color']['ago1']
		sha_slow_color_prev = ta[freq]['sha_slow_color']['ago2']
		if sha_slow_color_curr == 'red' and sha_slow_color_last == 'red' and sha_slow_color_prev == 'red':
			# sha_slow_reddening_tf = True
			msg = f'\t * SELL COND: {freq} sha slow colors ==> curr : {sha_slow_color_curr:>5}, last : {sha_slow_color_last:>5}, prev : {sha_slow_color_prev:>5}'
			all_sells.append(msg)
		else:
			# sha_slow_reddening_tf = False
			msg = f'\t * HODL COND: {freq} sha slow colors ==> curr : {sha_slow_color_curr:>5}, last : {sha_slow_color_last:>5}, prev : {sha_slow_color_prev:>5}'
			# YES!!! Allow the green candles to override the price touch above!
			all_hodls.append(msg)



#		sha_fast_body_shrinking_tf
#		sha_slow_body_shrinking_tf
#		sha_fast_upper_wick_weakening_tf
#		sha_slow_upper_wick_weakening_tf
#		sell_prc_intersect_sha_fast_tf
#		sha_fast_reddening_tf
#		sha_slow_reddening_tf

		if sha_fast_body_shrinking_tf and sha_fast_upper_wick_weakening_tf:
			sell_yn  = 'Y'
		elif sha_fast_body_shrinking_tf and sha_slow_body_shrinking_tf:
			sell_yn  = 'Y'
		elif sell_prc_intersect_sha_fast_tf and (sha_fast_body_shrinking_tf or sha_slow_body_shrinking_tf or sha_fast_reddening_tf):
			sell_yn  = 'Y'

#		if sell_prc_intersect_sha_fast_tf and sha_fast_body_shrinking_tf:
#			sell_yn  = 'Y'


		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			WoB('\tSELL TESTS - Smoothed Heikin Ashi')
			if (sell_yn == 'Y' and sell_block_yn == 'N')  or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
			for e in all_hodls:
				WoG(e)
#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')



		exit_if_profit_yn      = st.spot.sell.strats.sha.exit_if_profit_yn
		exit_if_profit_pct_min = st.spot.sell.strats.sha.exit_if_profit_pct_min
		exit_if_loss_yn        = st.spot.sell.strats.sha.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(st.spot.sell.strats.sha.exit_if_loss_pct_max) * -1
		if sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'\t * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						if show_tests_yn == 'Y':
							BoW(msg)
						sell_yn = 'N'
						hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'\t * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if show_tests_yn == 'Y':
						BoW(msg)
					sell_yn = 'N'
					hodl_yn = 'Y'
			elif pos.prc_chg_pct < 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'\t * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						if show_tests_yn == 'Y':
							BoW(msg)
						sell_yn = 'N'
						hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'\t * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if show_tests_yn == 'Y':
						BoW(msg)
					sell_yn = 'N'
					hodl_yn = 'Y'



		if sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'sha'
			pos.sell_strat_freq = pos.buy_strat_freq
			hodl_yn = 'N'
		else:
			sell_yn = 'N'
			hodl_yn = 'Y'

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_strat_imp_macd(st, mkt, ta, pos, sell_block_yn='N'):
	func_name = 'sell_strat_imp_macd'
	func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
		# only_exit_if_profit_yn = 'Y'
		prod_id     = mkt.prod_id
		# sell_prc    = mkt.prc_sell
		all_sells  = []
		all_hodls   = []
		sell_yn = 'N'
		hodl_yn = 'Y'
		show_tests_yn         = st.spot.sell.show_tests_yn

		freq = pos.buy_strat_freq
#		print('buy_strat_type : {}'.format(pos.buy_strat_type))
#		print('buy_strat_name : {}'.format(pos.buy_strat_name))
#		print('buy_strat_freq : {}'.format(pos.buy_strat_freq))

		# Impulse MACD + ATR
		# MACD > Signal
		imp_macd_curr      = ta[freq]['imp_macd']['ago0']
		imp_macd_sign_curr = ta[freq]['imp_macd_sign']['ago0']
		if imp_macd_curr < imp_macd_sign_curr:
			# macd_under_signal_tf = True
			msg = f'\t * SELL COND: {freq} impulse macd < signal ==> macd : {imp_macd_curr:>5}, signal : {imp_macd_sign_curr:>5}'
			all_sells.append(msg)
		else:
			msg = f'\t * HODL COND: {freq} impulse macd > signal ==> macd : {imp_macd_curr:>5}, signal : {imp_macd_sign_curr:>5}'
			# macd_under_signal_tf = False
			all_hodls.append(msg)

		# MACD Line Should Be Green or Lime
		imp_macd_color = ta[freq]['imp_macd_color']['ago0']
		if imp_macd_color in ('red','orange'):
			imp_macd_color_ok_tf = True
			#this is where it was erroring before
			msg = f'\t * SELL COND: {freq} impulse macd color must be lime or green ==> macd color : {imp_macd_color:>5}'
			all_sells.append(msg)
		else:
			imp_macd_color_ok_tf = False
			msg = f'\t * HODL COND: {freq} impulse macd color must be lime or green ==> macd color : {imp_macd_color:>5}'
			all_hodls.append(msg)

		if imp_macd_curr and imp_macd_color_ok_tf:
			sell_yn  = 'Y'

		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			WoB('\tSELL TESTS - Impluse MACD')
			if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
			for e in all_hodls:
				WoG(e)
#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

		exit_if_profit_yn      = st.spot.sell.strats.imp_macd.exit_if_profit_yn
		exit_if_profit_pct_min = st.spot.sell.strats.imp_macd.exit_if_profit_pct_min
		exit_if_loss_yn        = st.spot.sell.strats.imp_macd.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(st.spot.sell.strats.imp_macd.exit_if_loss_pct_max) * -1
		if sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'\t * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						if show_tests_yn == 'Y':
							BoW(msg)
						sell_yn = 'N'
						hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'\t * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if show_tests_yn == 'Y':
						BoW(msg)
					sell_yn = 'N'
					hodl_yn = 'Y'
			elif pos.prc_chg_pct < 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'\t * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						if show_tests_yn == 'Y':
							BoW(msg)
						sell_yn = 'N'
						hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'\t * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if show_tests_yn == 'Y':
						BoW(msg)
					sell_yn = 'N'
					hodl_yn = 'Y'

		if sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'imp_macd'
			pos.sell_strat_freq = freq
			hodl_yn = 'N'
		else:
			sell_yn = 'N'
			hodl_yn = 'Y'

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_strat_bb_bo(st, mkt, ta, pos, sell_block_yn='N'):
	func_name = 'sell_strat_bb_bo'
	func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
#		only_exit_if_profit_yn = 'Y'
		prod_id     = mkt.prod_id
		sell_prc    = mkt.prc_sell
		all_sells   = []
		all_hodls   = []
		sell_yn     = 'N'
		hodl_yn     = 'Y'
		show_tests_yn         = st.spot.sell.show_tests_yn

		rfreq = pos.buy_strat_freq
		freq = pos.buy_strat_freq

		curr_bb_upper_inner    = ta[freq]['bb_lower_inner']['ago0']


		# General Trend
		sell_prc_intersects_bb_upper_inner_tf
		if sell_prc < curr_bb_upper_inner:
			sell_prc_intersects_bb_upper_inner_tf = True
			msg = f'\t * SELL COND: {rfreq} current price : {sell_prc:>.8f} below bb upper inner : {curr_bb_upper_inner:>.8f}'
			all_sells.append(msg)
		else:
			sell_prc_intersects_bb_upper_inner_tf = False
			msg = f'\t * HODL COND: {rfreq} current price : {sell_prc:>.8f} below bb upper inner : {curr_bb_upper_inner:>.8f}'
			all_hodls.append(msg)


		if sell_prc_intersects_bb_upper_inner_tf:
			sell_yn = 'Y'
		else:
			sell_yn  = 'N'


		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			WoB('\tSELL TESTS - Bollinger Band Breakout')
			if (sell_yn == 'Y' and sell_block_yn == 'N')  or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
			for e in all_hodls:
				WoG(e)
#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')


		exit_if_profit_yn      = st.spot.sell.strats.bb_bo.exit_if_profit_yn
		exit_if_profit_pct_min = st.spot.sell.strats.bb_bo.exit_if_profit_pct_min
		exit_if_loss_yn        = st.spot.sell.strats.bb_bo.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(st.spot.sell.strats.bb_bo.exit_if_loss_pct_ma) * -1
		if sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'\t * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						if show_tests_yn == 'Y':
							BoW(msg)
						sell_yn = 'N'
						hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'\t * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if show_tests_yn == 'Y':
						BoW(msg)
					sell_yn = 'N'
					hodl_yn = 'Y'
			elif pos.prc_chg_pct < 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'\t * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						if show_tests_yn == 'Y':
							BoW(msg)
						sell_yn = 'N'
						hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'\t * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if show_tests_yn == 'Y':
						BoW(msg)
					sell_yn = 'N'
					hodl_yn = 'Y'


		if sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'bb_bo'
			pos.sell_strat_freq = freq
			hodl_yn = 'N'
		else:
			sell_yn = 'N'
			hodl_yn = 'Y'

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_strat_bb(st, mkt, ta, pos, sell_block_yn='N'):
	func_name = 'sell_strat_bb'
	func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	try:
		# only_exit_if_profit_yn = 'Y'
		prod_id     = mkt.prod_id
		sell_prc    = mkt.prc_sell
		all_sells   = []
		all_hodls   = []
		sell_yn     = 'N'
		hodl_yn     = 'Y'
		show_tests_yn         = st.spot.sell.show_tests_yn

		rfreq = pos.buy_strat_freq
		freq = pos.buy_strat_freq

#		, bb_upper_inner
#		, bb_lower_inner
#		, bb_mid_inner
#		, bb_width_inner
#		, bb_pct_inner
#		, bb_upper_roc_inner
#		, bb_lower_roc_inner
#		, bb_inner_expanding
#		, bb_inner_contracting
#	
#		, bb_upper_outer
#		, bb_lower_outer
#		, bb_mid_outer
#		, bb_width_outer
#		, bb_pct_outer
#		, bb_upper_roc_outer
#		, bb_lower_roc_outer
#		, bb_outer_expanding
#		, bb_outer_contracting

		# curr_bb_mid_inner     = ta[freq]['bb_mid_inner']['ago0']
		# curr_bb_upper_inner   = ta[freq]['bb_upper_inner']['ago0']
		curr_bb_lower_outer   = ta[freq]['bb_lower_outer']['ago0']
		age_mins          = pos.age_mins
		if freq == '15min':
			min_mins = 15
		elif freq == '30min':
			min_mins = 30
		elif freq == '1h':
			min_mins = 60
		elif freq == '4h':
			min_mins = 240
		elif freq == '1d':
			min_mins = 1440

		if age_mins > min_mins and sell_prc < curr_bb_lower_outer:
			bb_downward_spiral_tf = True
			msg = f'\t * SELL COND: {rfreq} current price : {sell_prc:>.8f} below bb lower outer : {curr_bb_lower_outer:>.8f} and gain_pct < 0 : {pos.gain_loss_pct_est}'
			all_sells.append(msg)
		else:
			bb_downward_spiral_tf = False
			msg = f'\t * HODL COND: {rfreq} current price : {sell_prc:>.8f} above bb lower outer : {curr_bb_lower_outer:>.8f} and gain_pct < 0 : {pos.gain_loss_pct_est}'
			all_hodls.append(msg)

		if bb_downward_spiral_tf:
			sell_yn  = 'Y'
		else:
			sell_yn  = 'N'


		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			WoB('\t SELL TESTS - Bollinger Band')
			if (sell_yn == 'Y' and sell_block_yn == 'N')  or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
			for e in all_hodls:
				WoG(e)
#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')


		exit_if_profit_yn      = st.spot.sell.strats.bb.exit_if_profit_yn
		exit_if_profit_pct_min = st.spot.sell.strats.bb.exit_if_profit_pct_min
		exit_if_loss_yn        = st.spot.sell.strats.bb.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(st.spot.sell.strats.bb.exit_if_loss_pct_max) * -1
		if sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'\t * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						if show_tests_yn == 'Y':
							BoW(msg)
						sell_yn = 'N'
						hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'\t * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if show_tests_yn == 'Y':
						BoW(msg)
					sell_yn = 'N'
					hodl_yn = 'Y'
			elif pos.prc_chg_pct < 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'\t * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						if show_tests_yn == 'Y':
							BoW(msg)
						sell_yn = 'N'
						hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'\t * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} -  cancelling sell...'
					if show_tests_yn == 'Y':
						BoW(msg)
					sell_yn = 'N'
					hodl_yn = 'Y'


		if sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'bb'
			pos.sell_strat_freq = freq
			hodl_yn = 'N'
		else:
			sell_yn = 'N'
			hodl_yn = 'Y'

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

# def sell_logic_ema_cross(st, mkt, pos):
# 	func_name = 'sell_logic_ema_cross'
# 	func_str = f'{lib_name}.{func_name}(mkt, ta, pos)'
# #	G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

# 	prod_id     = mkt.prod_id
# 	sell_prc    = mkt.prc_sell
# 	all_sells   = []
# 	all_hodls   = []
# 	sell_yn     = 'N'
# 	hodl_yn     = 'Y'
# 	show_tests_yn         = st.spot.sell.show_tests_yn

# #	# Exponential Moving Average Crosses
# #	if 1==1:
# #		if pos.prc_chg_pct > -5:
# #			msg = 'REQUIRE: current 1h ema5 :{:>.8f} >>> ema8:{:>.8f}'.format(mkt.ta_ema5_1h['ago0'], mkt.ta_ema8_1h['ago0'])
# #			if mkt.ta_ema5_abv_ema8_1h['ago0']:
# #				all_sells.append(msg)
# #			else:
# #				all_hodls.append(msg)
# #			msg = 'REQUIRE: current 1h ema8 :{:>.8f} >>> ema13:{:>.8f}'.format(mkt.ta_ema8_1h['ago0'], mkt.ta_ema13_1h['ago0'])
# #			if mkt.ta_ema8_abv_ema13_1h['ago0']:
# #				all_sells.append(msg)
# #			else:
# #				all_hodls.append(msg)
# #			msg = 'REQUIRE: current 1h ema13 :{:>.8f} >>> ema21:{:>.8f}'.format(mkt.ta_ema13_1h['ago0'], mkt.ta_ema21_1h['ago0'])
# #			if mkt.ta_ema13_abv_ema21_1h['ago0']:
# #				all_sells.append(msg)
# #			else:
# #				all_hodls.append(msg)
# #			if pos.buy_strat_name != 'bb' and not mkt.ta_ema5_abv_ema8_1h['ago0'] and not mkt.ta_ema8_abv_ema13_1h['ago0'] and not mkt.ta_ema13_abv_ema21_1h['ago0']:
# #				sell_yn  = 'Y'
# #				hodl_yn  = 'N'

# 	func_end(fnc)
# 	return mkt, pos, sell_yn, hodl_yn

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
