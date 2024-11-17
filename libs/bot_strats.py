#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import json

from libs.bot_common import freqs_get
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_common import dttm_get, func_begin, func_end, print_adv, beep, speak
from libs.lib_colors import BoW
from libs.lib_colors import GoW
import traceback
from libs.lib_charts import chart_row
from libs.lib_colors import cs, cp, G

from libs.bot_strat_sha import buy_strat_sha, sell_strat_sha, buy_strat_settings_sha, sell_strat_settings_sha
from libs.bot_strat_imp_macd import buy_strat_imp_macd, sell_strat_imp_macd, buy_strat_settings_imp_macd, sell_strat_settings_imp_macd
from libs.bot_strat_bb import buy_strat_bb, sell_strat_bb, buy_strat_settings_bb, sell_strat_settings_bb
from libs.bot_strat_bb_bo import buy_strat_bb_bo, sell_strat_bb_bo, buy_strat_settings_bb_bo, sell_strat_settings_bb_bo
from libs.bot_strat_drop import buy_strat_drop, sell_strat_drop, buy_strat_settings_drop, sell_strat_settings_drop


#from libs.bot_strat_nwe import buy_strat_nwe, sell_strat_nwe, buy_strat_settings_nwe, sell_strat_settings_nwe
from libs.bot_strat_nwe_3row import buy_strat_nwe_3row, sell_strat_nwe_3row, buy_strat_settings_nwe_3row, sell_strat_settings_nwe_3row
from libs.bot_strat_nwe_env import buy_strat_nwe_env, sell_strat_nwe_env, buy_strat_settings_nwe_env, sell_strat_settings_nwe_env
from libs.bot_strat_nwe_rev import buy_strat_nwe_rev, sell_strat_nwe_rev, buy_strat_settings_nwe_rev, sell_strat_settings_nwe_rev


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strats'
log_name      = 'bot_strats'


# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)


#<=====>#
# Notes
#<=====>#
#ADD_NEW_STARTS_HERE
# New Strat Add Section
# Need to also insert into cbtrade.buy_strats table
# Need to also add to settings buy & sell sections...
# SELECT * FROM cbtrade.buy_strats;
# insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc) values ('up', 'nwe', 'nadaraya-watson estimator');


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def buy_strats_get():
	func_name = 'buy_strats_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	strats = {}
	strats['nwe_3row_15min']      = {'prod_id': '', 'buy_strat_nick': 'nwe_3row_15min' , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_3row', 'buy_strat_desc': 'Nadaraya-Watson Estimator - 3 Row',    'buy_strat_freq': '15min'}
	strats['nwe_3row_30min']      = {'prod_id': '', 'buy_strat_nick': 'nwe_3row_30min' , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_3row', 'buy_strat_desc': 'Nadaraya-Watson Estimator - 3 Row',    'buy_strat_freq': '30min'}
	strats['nwe_3row_1h']         = {'prod_id': '', 'buy_strat_nick': 'nwe_3row_1h'    , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_3row', 'buy_strat_desc': 'Nadaraya-Watson Estimator - 3 Row',    'buy_strat_freq': '1h'}
	strats['nwe_3row_4h']         = {'prod_id': '', 'buy_strat_nick': 'nwe_3row_4h'    , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_3row', 'buy_strat_desc': 'Nadaraya-Watson Estimator - 3 Row',    'buy_strat_freq': '4h'}
	strats['nwe_3row_1d']         = {'prod_id': '', 'buy_strat_nick': 'nwe_3row_1d'    , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_3row', 'buy_strat_desc': 'Nadaraya-Watson Estimator - 3 Row',    'buy_strat_freq': '1d'}

	strats['nwe_env_15min']       = {'prod_id': '', 'buy_strat_nick': 'nwe_env_15min'  , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_env',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Envelope', 'buy_strat_freq': '15min'}
	strats['nwe_env_30min']       = {'prod_id': '', 'buy_strat_nick': 'nwe_env_30min'  , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_env',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Envelope', 'buy_strat_freq': '30min'}
	strats['nwe_env_1h']          = {'prod_id': '', 'buy_strat_nick': 'nwe_env_1h'     , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_env',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Envelope', 'buy_strat_freq': '1h'}
	strats['nwe_env_4h']          = {'prod_id': '', 'buy_strat_nick': 'nwe_env_4h'     , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_env',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Envelope', 'buy_strat_freq': '4h'}
	strats['nwe_env_1d']          = {'prod_id': '', 'buy_strat_nick': 'nwe_env_1d'     , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_env',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Envelope', 'buy_strat_freq': '1d'}

	strats['nwe_rev_15min']       = {'prod_id': '', 'buy_strat_nick': 'nwe_rev_15min'  , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_rev',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Reversal', 'buy_strat_freq': '15min'}
	strats['nwe_rev_30min']       = {'prod_id': '', 'buy_strat_nick': 'nwe_rev_30min'  , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_rev',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Reversal', 'buy_strat_freq': '30min'}
	strats['nwe_rev_1h']          = {'prod_id': '', 'buy_strat_nick': 'nwe_rev_1h'     , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_rev',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Reversal', 'buy_strat_freq': '1h'}
	strats['nwe_rev_4h']          = {'prod_id': '', 'buy_strat_nick': 'nwe_rev_4h'     , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_rev',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Reversal', 'buy_strat_freq': '4h'}
	strats['nwe_rev_1d']          = {'prod_id': '', 'buy_strat_nick': 'nwe_rev_1d'     , 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_rev',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Reversal', 'buy_strat_freq': '1d'}

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

	# strats['emax_15min']       = {'prod_id': '', 'buy_strat_nick': 'emax_15min'     , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '15min'}
	# strats['emax_30min']       = {'prod_id': '', 'buy_strat_nick': 'emax_30min'     , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '30min'}
	# strats['emax_1h']          = {'prod_id': '', 'buy_strat_nick': 'emax_1h'        , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '1h'}
	# strats['emax_4h']          = {'prod_id': '', 'buy_strat_nick': 'emax_4h'        , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '4h'}
	# strats['emax_1d']          = {'prod_id': '', 'buy_strat_nick': 'emax_1d'        , 'buy_strat_type': 'up', 'buy_strat_name': 'emax',     'buy_strat_desc': 'Triple EMA Crossover',        'buy_strat_freq': '1d'}

	func_end(fnc)
	return strats

#<=====>#

def buy_strat_settings_get(st):
	func_name = 'buy_strat_settings_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	from pprint import pprint
#	pprint(st)
#	print(type(st))f
#	st = json.loads(st)

	#ADD_NEW_STARTS_HERE
	st = buy_strat_settings_sha(st)
#	st = buy_strat_settings_nwe(st)
	st = buy_strat_settings_nwe_3row(st)
	st = buy_strat_settings_nwe_env(st)
	st = buy_strat_settings_nwe_rev(st)
	st = buy_strat_settings_imp_macd(st)
	st = buy_strat_settings_bb_bo(st)
	st = buy_strat_settings_bb(st)
	st = buy_strat_settings_drop(st)

#	st = json.dumps(st, indent=4)

	func_end(fnc)
	return st

#<=====>#

def sell_strat_settings_get(st):
	func_name = 'sell_strat_settings_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	st = json.loads(st)

	#ADD_NEW_STARTS_HERE
	st = sell_strat_settings_sha(st)
#	st = sell_strat_settings_nwe(st)
	st = sell_strat_settings_nwe_3row(st)
	st = sell_strat_settings_nwe_env(st)
	st = sell_strat_settings_nwe_rev(st)
	st = sell_strat_settings_imp_macd(st)
	st = sell_strat_settings_bb_bo(st)
	st = sell_strat_settings_bb(st)
	st = sell_strat_settings_drop(st)

#	st = json.dumps(st, indent=4)

	func_end(fnc)
	return st

#<=====>#

def buy_strats_avail_get(pair, pst):
	func_name = 'buy_strats_avail_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = pair.prod_id
	pst     = pst

	#ADD_NEW_STARTS_HERE
	# from pprint import pprint
	# pprint(pst.buy.strats.sha)

	# New Strat Add Section
	pair.strat_sha_yn = 'N'
	if not pst.buy.strats.sha.prod_ids:
		pair.strat_sha_yn = 'Y'
	elif prod_id in pst.buy.strats.sha.prod_ids:
		pair.strat_sha_yn = 'Y'
	if pst.buy.strats.sha.skip_prod_ids:
		if prod_id in pst.buy.strats.sha.skip_prod_ids:
			pair.strat_sha_yn = 'N'

	pair.strat_nwe_3row_yn = 'N'
	if not pst.buy.strats.nwe_3row.prod_ids:
		pair.strat_nwe_3row_yn = 'Y'
	elif prod_id in pst.buy.strats.nwe_3row.prod_ids:
		pair.strat_nwe_3row_yn = 'Y'
	if pst.buy.strats.nwe_3row.skip_prod_ids:
		if prod_id in pst.buy.strats.nwe_3row.skip_prod_ids:
			pair.strat_nwe_3row_yn = 'N'

	pair.strat_nwe_env_yn = 'N'
	if not pst.buy.strats.nwe_env.prod_ids:
		pair.strat_nwe_env_yn = 'Y'
	elif prod_id in pst.buy.strats.nwe_env.prod_ids:
		pair.strat_nwe_env_yn = 'Y'
	if pst.buy.strats.nwe_env.skip_prod_ids:
		if prod_id in pst.buy.strats.nwe_env.skip_prod_ids:
			pair.strat_nwe_env_yn = 'N'

	pair.strat_nwe_rev_yn = 'N'
	if not pst.buy.strats.nwe_rev.prod_ids:
		pair.strat_nwe_rev_yn = 'Y'
	elif prod_id in pst.buy.strats.nnwe_revwe.prod_ids:
		pair.strat_nwe_rev_yn = 'Y'
	if pst.buy.strats.nwe_rev.skip_prod_ids:
		if prod_id in pst.buy.strats.nwe_rev.skip_prod_ids:
			pair.strat_nwe_rev_yn = 'N'

	pair.strat_imp_macd_yn = 'N'
	if not pst.buy.strats.imp_macd.prod_ids:
		pair.strat_imp_macd_yn = 'Y'
	elif prod_id in pst.buy.strats.imp_macd.prod_ids:
		pair.strat_imp_macd_yn = 'Y'
	if pst.buy.strats.imp_macd.skip_prod_ids:
		if prod_id in pst.buy.strats.imp_macd.skip_prod_ids:
			pair.strat_imp_macd_yn = 'N'

	pair.strat_emax_yn = 'N'
	if not pst.buy.strats.emax.prod_ids:
		pair.strat_emax_yn = 'Y'
	elif prod_id in pst.buy.strats.emax.prod_ids:
		pair.strat_emax_yn = 'Y'
	if pst.buy.strats.emax.skip_prod_ids:
		if prod_id in pst.buy.strats.emax.skip_prod_ids:
			pair.strat_emax_yn = 'N'

	pair.strat_drop_yn = 'N'
	if not pst.buy.strats.drop.prod_ids:
		pair.strat_drop_yn = 'Y'
	elif prod_id in pst.buy.strats.drop.prod_ids:
		pair.strat_drop_yn = 'Y'
	if pst.buy.strats.drop.skip_prod_ids:
		if prod_id in pst.buy.strats.drop.skip_prod_ids:
			pair.strat_drop_yn = 'N'

	pair.strat_bb_bo_yn = 'N'
	if not pst.buy.strats.bb_bo.prod_ids:
		pair.strat_bb_bo_yn = 'Y'
	elif prod_id in pst.buy.strats.bb_bo.prod_ids:
		pair.strat_bb_bo_yn = 'Y'
	if pst.buy.strats.bb_bo.skip_prod_ids:
		if prod_id in pst.buy.strats.bb_bo.skip_prod_ids:
			pair.strat_bb_bo_yn = 'N'

	pair.strat_bb_yn = 'N'
	if not pst.buy.strats.bb.prod_ids:
		pair.strat_bb_yn = 'Y'
	elif prod_id in pst.buy.strats.bb.prod_ids:
		pair.strat_bb_yn = 'Y'
	if pst.buy.strats.bb.skip_prod_ids:
		if prod_id in pst.buy.strats.bb.skip_prod_ids:
			pair.strat_bb_yn = 'N'

	func_end(fnc)
	return pair

#<=====>#

def buy_strats_check(buy, ta, pst):
	func_name = 'buy_strats_check'
	func_str = f'{lib_name}.{func_name}(buy, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	buy.buy_yn          = 'N'
	buy.wait_yn         = 'Y'
	freq                = buy.trade_strat_perf.buy_strat_freq

	#ADD_NEW_STARTS_HERE

	# Buy Strategy - Double Smoothed Heikin Ashi 
	if buy.trade_strat_perf.buy_strat_name == 'sha':
		if buy.pst.buy.strats.sha.use_yn == 'Y' and buy.strat_sha_yn == 'Y':
			if freq in buy.pst.buy.strats.sha.freqs:
				buy, ta = buy_strat_sha(buy, ta, pst)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
#				print(buy_signal)
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Nadaraya-Waston 3Row
	elif buy.trade_strat_perf.buy_strat_name == 'nwe_3row':
		# print(f'{lib_name}.{func_name} => buy_yn : {buy.buy_yn}, buy.trade_strat_perf.buy_strat_name : {buy.trade_strat_perf.buy_strat_name}')
		if buy.pst.buy.strats.nwe_3row.use_yn == 'Y' and buy.strat_nwe_3row_yn == 'Y':
			if freq in buy.pst.buy.strats.nwe_3row.freqs:
				buy, ta = buy_strat_nwe_3row(buy, ta, pst)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
#				print(buy_signal)
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Nadaraya-Waston Envelope
	elif buy.trade_strat_perf.buy_strat_name == 'nwe_env':
		# print(f'{lib_name}.{func_name} => buy_yn : {buy.buy_yn}, buy.trade_strat_perf.buy_strat_name : {buy.trade_strat_perf.buy_strat_name}')
		if buy.pst.buy.strats.nwe_env.use_yn == 'Y' and buy.strat_nwe_env_yn == 'Y':
			if freq in buy.pst.buy.strats.nwe_env.freqs:
				buy, ta = buy_strat_nwe_env(buy, ta, pst)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
#				print(buy_signal)
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Nadaraya-Waston Reversal
	elif buy.trade_strat_perf.buy_strat_name == 'nwe_rev':
		# print(f'{lib_name}.{func_name} => buy_yn : {buy.buy_yn}, buy.trade_strat_perf.buy_strat_name : {buy.trade_strat_perf.buy_strat_name}')
		if buy.pst.buy.strats.nwe_rev.use_yn == 'Y' and buy.strat_nwe_rev_yn == 'Y':
			if freq in buy.pst.buy.strats.nwe_rev.freqs:
				buy, ta = buy_strat_nwe_rev(buy, ta, pst)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
#				print(buy_signal)
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Impulse MACD
	elif buy.trade_strat_perf.buy_strat_name == 'imp_macd':
		if buy.pst.buy.strats.imp_macd.use_yn == 'Y' and buy.strat_imp_macd_yn == 'Y':
			if freq in buy.pst.buy.strats.imp_macd.freqs:
				buy, ta = buy_strat_imp_macd(buy, ta, pst)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
#				print(buy_signal)
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Bollinger Band Breakout
	elif buy.trade_strat_perf.buy_strat_name == 'bb_bo':
		if buy.pst.buy.strats.bb_bo.use_yn == 'Y' and buy.strat_bb_bo_yn == 'Y':
			if freq in buy.pst.buy.strats.bb_bo.freqs:
				buy, ta = buy_strat_bb_bo(buy, ta, pst)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
#				print(buy_signal)
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Drop
	elif buy.trade_strat_perf.buy_strat_name == 'drop':
		if buy.pst.buy.strats.drop.use_yn == 'Y' and buy.strat_drop_yn == 'Y':
			if freq in buy.pst.buy.strats.drop.freqs:
				buy, ta = buy_strat_drop(buy, ta, pst)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
#				print(buy_signal)
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Bollinger Band
	elif buy.trade_strat_perf.buy_strat_name == 'bb':
		if buy.pst.buy.strats.bb.use_yn == 'Y' and buy.strat_bb_yn == 'Y':
			if freq in buy.pst.buy.strats.bb.freqs:
				buy, ta = buy_strat_bb(buy, ta, pst)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
#				print(buy_signal)
				buy.buy_signals.append(buy_signal)

	else:
		buy.buy_yn = 'N'
		buy.wait_yn = 'Y'

#	print(f'{lib_name}.{func_name} => prod_id : {buy.prod_id}, buy_yn : {buy.buy_yn}, wait_yn : {buy.wait_yn}')

	func_end(fnc)
	return buy, ta

#<=====>#

def buy_strats_deny(buy):
	func_name = 'buy_strats_deny'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	#ADD_NEW_STARTS_HERE

	if buy.trade_strat_perf.buy_strat_name == 'sha':
		if buy.strat_sha_yn == 'N':
			buy.buy_deny_yn = 'Y'

	elif buy.trade_strat_perf.buy_strat_name == 'nwe_3row':
		if buy.strat_nwe_3row_yn == 'N':
			buy.buy_deny_yn = 'Y'

	elif buy.trade_strat_perf.buy_strat_name == 'nwe_env':
		if buy.strat_nwe_env_yn == 'N':
			buy.buy_deny_yn = 'Y'

	elif buy.trade_strat_perf.buy_strat_name == 'nwe_rev':
		if buy.strat_nwe_rev_yn == 'N':
			buy.buy_deny_yn = 'Y'

	elif buy.trade_strat_perf.buy_strat_name == 'imp_macd':
		if buy.strat_imp_macd_yn == 'N':
			buy.buy_deny_yn = 'Y'

	elif buy.trade_strat_perf.buy_strat_name == 'emax':
		if buy.strat_emax_yn == 'N':
			buy.buy_deny_yn = 'Y'

	elif buy.trade_strat_perf.buy_strat_name == 'bb_bo':
		if buy.strat_bb_bo_yn == 'N':
			buy.buy_deny_yn = 'Y'

	elif buy.trade_strat_perf.buy_strat_name == 'bb':
		if buy.strat_bb_yn == 'N':
			buy.buy_deny_yn = 'Y'

	elif buy.trade_strat_perf.buy_strat_name == 'drop':
		if buy.strat_drop_yn == 'N':
			buy.buy_deny_yn = 'Y'

#	print(f'{lib_name}.{func_name} => prod_id : {buy.prod_id}, buy_yn : {buy.buy_yn}, wait_yn : {buy.wait_yn}')

	func_end(fnc)
	return buy

#<=====>#

def sell_strats_check(mkt, pos, ta, pst):
	func_name = 'sell_strats_check'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	#ADD_NEW_STARTS_HERE

	# Strategy Exit - Smoothed Heikin Ashi
	if pos.sell_yn == 'N':
		if pos.buy_strat_name == 'sha':
			mkt, pos, ta = sell_strat_sha(mkt, pos, ta, pst)

	if pos.sell_yn == 'N':
		if pos.buy_strat_name == 'nwe_3row':
			mkt, pos, ta = sell_strat_nwe_3row(mkt, pos, ta, pst)

	if pos.sell_yn == 'N':
		if pos.buy_strat_name == 'nwe_env':
			mkt, pos, ta = sell_strat_nwe_env(mkt, pos, ta, pst)

	if pos.sell_yn == 'N':
		if pos.buy_strat_name == 'nwe_rev':
			mkt, pos, ta = sell_strat_nwe_rev(mkt, pos, ta, pst)

	# Strategy Exit - Impulse MACD
		elif pos.buy_strat_name == 'imp_macd':
			mkt, pos, ta = sell_strat_imp_macd(mkt, pos, ta, pst)

	# Strategy Exit - Bollinger Band
		elif pos.buy_strat_name == 'bb':
			mkt, pos, ta = sell_strat_bb(mkt, pos, ta, pst)

	# Strategy Exit - Bollinger Band Breakout
		elif pos.buy_strat_name == 'bb_bo':
			mkt, pos, ta = sell_strat_bb_bo(mkt, pos, ta, pst)

	# Strategy Exit - Bollinger Band Breakout
		elif pos.buy_strat_name == 'drop':
			mkt, pos, ta = sell_strat_drop(mkt, pos, ta, pst)

	func_end(fnc)
	return mkt, pos, ta

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

