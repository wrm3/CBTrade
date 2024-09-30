#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.bot_common import freqs_get
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_common import dttm_get, func_begin, func_end, print_adv, beep, speak
from libs.lib_colors import BoW
from libs.lib_colors import GoW
import traceback


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

def buy_strats_avail_get(pair):
	func_name = 'buy_strats_avail_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = pair.prod_id
	pst     = pair.pst

	# New Strat Add Section
	pair.strat_sha_yn = 'N'
	if not pst.buy.strats.sha.prod_ids:
		pair.strat_sha_yn = 'Y'
	elif prod_id in pst.buy.strats.sha.prod_ids:
		pair.strat_sha_yn = 'Y'
	if pst.buy.strats.sha.prod_ids_skip:
		if prod_id in pst.buy.strats.sha.prod_ids_skip:
			pair.strat_sha_yn = 'N'

	pair.strat_imp_macd_yn = 'N'
	if not pst.buy.strats.imp_macd.prod_ids:
		pair.strat_imp_macd_yn = 'Y'
	elif prod_id in pst.buy.strats.imp_macd.prod_ids:
		pair.strat_imp_macd_yn = 'Y'
	if pst.buy.strats.imp_macd.prod_ids_skip:
		if prod_id in pst.buy.strats.imp_macd.prod_ids_skip:
			pair.strat_imp_macd_yn = 'N'

	pair.strat_emax_yn = 'N'
	if not pst.buy.strats.emax.prod_ids:
		pair.strat_emax_yn = 'Y'
	elif prod_id in pst.buy.strats.emax.prod_ids:
		pair.strat_emax_yn = 'Y'
	if pst.buy.strats.emax.prod_ids_skip:
		if prod_id in pst.buy.strats.emax.prod_ids_skip:
			pair.strat_emax_yn = 'N'

	pair.strat_drop_yn = 'N'
	if not pst.buy.strats.drop.prod_ids:
		pair.strat_drop_yn = 'Y'
	elif prod_id in pst.buy.strats.drop.prod_ids:
		pair.strat_drop_yn = 'Y'
	if pst.buy.strats.drop.prod_ids_skip:
		if prod_id in pst.buy.strats.drop.prod_ids_skip:
			pair.strat_drop_yn = 'N'

	pair.strat_bb_bo_yn = 'N'
	if not pst.buy.strats.bb_bo.prod_ids:
		pair.strat_bb_bo_yn = 'Y'
	elif prod_id in pst.buy.strats.bb_bo.prod_ids:
		pair.strat_bb_bo_yn = 'Y'
	if pst.buy.strats.bb_bo.prod_ids_skip:
		if prod_id in pst.buy.strats.bb_bo.prod_ids_skip:
			pair.strat_bb_bo_yn = 'N'

	pair.strat_bb_yn = 'N'
	if not pst.buy.strats.bb.prod_ids:
		pair.strat_bb_yn = 'Y'
	elif prod_id in pst.buy.strats.bb.prod_ids:
		pair.strat_bb_yn = 'Y'
	if pst.buy.strats.bb.prod_ids_skip:
		if prod_id in pst.buy.strats.bb.prod_ids_skip:
			pair.strat_bb_yn = 'N'

	func_end(fnc)
	return pair

#<=====>#

def buy_strats_check(buy):
	func_name = 'buy_strats_check'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	buy.buy_yn               = 'N'
	buy.wait_yn              = 'Y'
	freq                 = buy.trade_strat_perf.buy_strat_freq

	# Buy Strategy - Double Smoothed Heikin Ashi 
	if buy.trade_strat_perf.buy_strat_name == 'sha':
		if buy.pst.buy.strats.sha.use_yn == 'Y' and buy.strat_sha_yn == 'Y':
			if freq in buy.pst.buy.strats.sha.freqs:
				buy = buy_strat_sha(buy)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Impulse MACD
	elif buy.trade_strat_perf.buy_strat_name == 'imp_macd':
		if buy.pst.buy.strats.imp_macd.use_yn == 'Y' and buy.strat_imp_macd_yn == 'Y':
			if freq in buy.pst.buy.strats.imp_macd.freqs:
				buy = buy_strat_imp_macd(buy)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Bollinger Band Breakout
	elif buy.trade_strat_perf.buy_strat_name == 'bb_bo':
		if buy.pst.buy.strats.bb_bo.use_yn == 'Y' and buy.strat_bb_bo_yn == 'Y':
			if freq in buy.pst.buy.strats.bb_bo.freqs:
				buy = buy_strat_bb_bo(buy)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Drop
	elif buy.trade_strat_perf.buy_strat_name == 'drop':
		if buy.pst.buy.strats.drop.use_yn == 'Y' and buy.strat_drop_yn == 'Y':
			if freq in buy.pst.buy.strats.drop.freqs:
				buy = buy_strat_drop(buy)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
				buy.buy_signals.append(buy_signal)

	# Buy Strategy - Bollinger Band
	elif buy.trade_strat_perf.buy_strat_name == 'bb':
		if buy.pst.buy.strats.bb.use_yn == 'Y' and buy.strat_bb_yn == 'Y':
			if freq in buy.pst.buy.strats.bb.freqs:
				buy = buy_strat_bb(buy)
				buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf.buy_strat_type, "buy_strat_name": buy.trade_strat_perf.buy_strat_name, "buy_strat_freq": buy.trade_strat_perf.buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
				buy.buy_signals.append(buy_signal)

	else:
		buy.buy_yn = 'N'
		buy.wait_yn = 'Y'

	func_end(fnc)
	return buy

#<=====>#

def buy_strats_deny(buy):
	func_name = 'buy_strats_deny'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	if buy.trade_strat_perf.buy_strat_name == 'sha' and buy.pair.strat_sha_yn == 'N':
		buy.trade_strat_perf.buy_deny_yn = 'Y'
	elif buy.trade_strat_perf.buy_strat_name == 'imp_macd' and buy.pair.strat_imp_macd_yn == 'N':
		buy.trade_strat_perf.buy_deny_yn = 'Y'
	elif buy.trade_strat_perf.buy_strat_name == 'emax' and buy.pair.strat_emax_yn == 'N':
		buy.trade_strat_perf.buy_deny_yn = 'Y'
	elif buy.trade_strat_perf.buy_strat_name == 'bb_bo' and buy.pair.strat_bb_bo_yn == 'N':
		buy.trade_strat_perf.buy_deny_yn = 'Y'
	elif buy.trade_strat_perf.buy_strat_name == 'bb' and buy.pair.strat_bb_yn == 'N':
		buy.trade_strat_perf.buy_deny_yn = 'Y'
	elif buy.trade_strat_perf.buy_strat_name == 'drop' and buy.pair.strat_drop_yn == 'N':
		buy.trade_strat_perf.buy_deny_yn = 'Y'

	func_end(fnc)
	return buy

#<=====>#

def buy_strat_sha(buy):
	func_name = 'buy_strat_sha'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:

		all_passes       = []
		all_fails        = []
		prod_id          = buy.prod_id
		buy.buy_yn       = 'Y'
		buy.wait_yn      = 'N'

		buy.rfreq = buy.trade_strat_perf.buy_strat_freq
		r     = freqs_get(buy.rfreq)
		freqs =r[0]

		# Smoothed Heikin Ashi Trend - Fast - Multi Timeframe Above Current Price
		ago_list = ['ago0','ago1']
		for freq in freqs:
			for ago in ago_list:
				m = '    * BUY REQUIRE : {} current price : {:>.8f} >>> {} SHA - FAST close {:>.8f} - {}'
				msg = m.format(freq, buy.prc_buy, freq, buy.ta[freq]['sha_fast_close'][ago], ago)
				if buy.prc_buy > buy.ta[freq]['sha_fast_close'][ago]:
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Smoothed Heikin Ashi Trend - Fast - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in freqs:
			for ago in ago_list:
				m = '    * BUY REQUIRE : {} SHA_FAST candles {} == green : {}'
				msg = m.format(freq, ago, buy.ta[freq]['sha_fast_color'][ago])
				if buy.ta[freq]['sha_fast_color'][ago] == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Smoothed Heikin Ashi Trend - Slow - Multi Timeframe Above Current Price
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				m = '    * BUY REQUIRE : {} current price : {:>.8f} >>> {} SHA - SLOW close {:>.8f} - {}'
				msg = m.format(freq, buy.prc_buy, freq, buy.ta[freq]['sha_slow_close'][ago], ago)
				if buy.prc_buy > buy.ta[freq]['sha_slow_close'][ago]:
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Smoothed Heikin Ashi Trend - Slow - Multi Timeframe - Candles Are Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				m = '    * BUY REQUIRE : {} SHA_SLOW candles {} == green : {}'
				msg = m.format(freq, ago, buy.ta[freq]['sha_slow_color'][ago])
				if buy.ta[freq]['sha_slow_color'][ago] == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Check to make sure the body is growing body
		if buy.ta[buy.rfreq]['sha_fast_body']['ago0'] >= buy.ta[buy.rfreq]['sha_fast_body']['ago1'] >= buy.ta[buy.rfreq]['sha_fast_body']['ago2']:
			m = '    * BUY REQUIRE : {} growing body size TRUE - curr {:>.8f} >>> last {:>.8f} >>>  prev {:>.8f}'
			msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['sha_fast_body']['ago0'], buy.ta[buy.rfreq]['sha_fast_body']['ago1'],  buy.ta[buy.rfreq]['sha_fast_body']['ago2'])
			all_passes.append(msg)
		else:
			m = '    * BUY REQUIRE : {} growing body size FALSE - curr {:>.8f} >>> last {:>.8f} >>>  prev {:>.8f}'
			msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['sha_fast_body']['ago0'], buy.ta[buy.rfreq]['sha_fast_body']['ago1'],  buy.ta[buy.rfreq]['sha_fast_body']['ago2'])
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# Check Upper Wick Larger Than Lower Wick
		ago_list = ['ago0', 'ago1', 'ago2']
		for ago in ago_list:
			if buy.ta[buy.rfreq]['sha_fast_wick_upper'][ago] >= buy.ta[buy.rfreq]['sha_fast_wick_lower'][ago]:
				m = '    * BUY REQUIRE : {} larger upper wick - upper {:>.8f} >>> lower {:>.8f} - {}'
				msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['sha_fast_wick_upper'][ago], buy.ta[buy.rfreq]['sha_fast_wick_lower'][ago], ago)
				all_passes.append(msg)
			else:
				m = '    * BUY REQUIRE : {} growing body size - upper {:>.8f} <<< lower {:>.8f} - {}' 
				msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['sha_fast_wick_upper'][ago], buy.ta[buy.rfreq]['sha_fast_wick_lower'][ago], ago)
				buy.buy_yn  = 'N'
				all_fails.append(msg)

		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in freqs:
			for ago in ago_list:
				m = '    * BUY REQUIRE : {} HA candles {} == green : {}'
				msg = m.format(freq, ago, buy.ta[freq]['ha_color'][ago])
				if buy.ta[freq]['ha_color'][ago] == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Nadaraya-Watson Estimator - Estimated Is Green
		ago_list = ['ago0','ago1']
		for ago in ago_list:
			m = '    * BUY REQUIRE : {} Nadaraya-Watson Estimator color {} == green : {}'
			msg = m.format(freq, ago, buy.ta[buy.rfreq]['nwe_color'][ago])
			if buy.ta[freq]['ha_color'][ago] == 'green':
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.mkt.buy_strat_type  = 'up'
			buy.mkt.buy_strat_name  = 'sha'
			buy.mkt.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		buy.trade_strat_perf.pass_cnt     = len(all_passes)
		buy.trade_strat_perf.fail_cnt     = len(all_fails)
		buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
		buy.trade_strat_perf.all_passes   = all_passes
		buy.trade_strat_perf.all_fails    = all_fails
		buy.trade_strat_perf.buy_yn       = buy.buy_yn
		buy.trade_strat_perf.wait_yn      = buy.wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {buy.rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy.buy_yn  = 'N'
		buy.wait_yn = 'Y'

	buy.trade_strat_perf.buy_yn  = buy.buy_yn
	buy.trade_strat_perf.wait_yn = buy.wait_yn

	func_end(fnc)
	return buy

#<=====>#

def buy_strat_imp_macd(buy):
	func_name = 'buy_strat_imp_macd'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = buy.prod_id
		buy.buy_yn       = 'Y'
		buy.wait_yn      = 'N'

		buy.rfreq        = buy.trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(buy.rfreq)

		# Impulse MACD + ATR
		# MACD > Signal
		m = '    * BUY REQUIRE : {} impulse macd > signal ==> macd : {:>5}, signal : {:>5}'
		msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['imp_macd']['ago0'], buy.ta[buy.rfreq]['imp_macd_sign']['ago0'])
		if buy.ta[buy.rfreq]['imp_macd']['ago0'] > buy.ta[buy.rfreq]['imp_macd_sign']['ago0']:
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# MACD Line Should Be Green or Lime
		m = '    * BUY REQUIRE : {} impulse macd color must be lime or green ==> macd color : {:>5}'
		msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['imp_macd_color']['ago0'])
		if buy.ta[buy.rfreq]['imp_macd_color']['ago0'] in ('lime','green'):
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# MACD & Signal Should Be Sufficiently Appart and Not Hugging
		spread = buy.ta[buy.rfreq]['imp_macd']['ago0'] - buy.ta[buy.rfreq]['imp_macd_sign']['ago0']
		min_spread_pct = 5
		min_spread = buy.ta[buy.rfreq]['atr']['ago0'] * (min_spread_pct/100)
		m = '    * BUY REQUIRE : {} impulse macd_signal > atr_low * 0.0{} ==> macd : {:>5}, sign : {:>5}, spread : {:>5}, min_spread_pct : {:>5}, min_spread : {:>5}'
		msg = m.format(buy.rfreq, min_spread_pct, buy.ta[buy.rfreq]['imp_macd']['ago0'], buy.ta[buy.rfreq]['imp_macd_sign']['ago0'], spread, min_spread_pct, min_spread)
		if spread > min_spread:
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = buy.ta[freq]['color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = buy.ta[freq]['ha_color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Nadaraya-Watson Estimator - Estimated Is Green
		ago_list = ['ago0','ago1']
		for ago in ago_list:
			m = '    * BUY REQUIRE : {} Nadaraya-Watson Estimator color {} == green : {}'
			msg = m.format(freq, ago, buy.ta[buy.rfreq]['nwe_color'][ago])
			if buy.ta[freq]['ha_color'][ago] == 'green':
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.mkt.buy_strat_type  = 'up'
			buy.mkt.buy_strat_name  = 'imp_macd'
			buy.mkt.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		buy.trade_strat_perf.pass_cnt     = len(all_passes)
		buy.trade_strat_perf.fail_cnt     = len(all_fails)
		buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
		buy.trade_strat_perf.all_passes   = all_passes
		buy.trade_strat_perf.all_fails    = all_fails
		buy.trade_strat_perf.buy_yn       = buy.buy_yn
		buy.trade_strat_perf.wait_yn      = buy.wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {buy.rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy.buy_yn  = 'N'
		buy.wait_yn = 'Y'

	buy.trade_strat_perf.buy_yn  = buy.buy_yn
	buy.trade_strat_perf.wait_yn = buy.wait_yn

	func_end(fnc)
	return buy

#<=====>#

# Drop
def buy_strat_drop(buy):
	func_name = 'buy_strat_drop'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = buy.prod_id
		buy.buy_yn       = 'Y'
		buy.wait_yn      = 'N'

		buy.rfreq = buy.trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(buy.rfreq)

		# Price has recent x% drop below recent high
		max24 = buy.ta['1h']['max24']['ago0']
		drop_pct     = buy.pst.buy.strats.drop.drop_pct
		drop_pct_dec = (100-drop_pct) / 100
		target_prc   = max24 * drop_pct_dec

		if prod_id == 'BTC-USDC' and buy.rfreq == '1h':
			ago_list = ['ago0','ago1','ago2','ago3']
			for ago in ago_list:
				prc_drop_pct = round(((buy.prc_buy - max24) / max24) * 100, 2)
				if buy.prc_buy < target_prc:
					msg = f'    * RESERVES UNLOCKED * : recent ({ago}) current price {buy.prc_buy:>.8f} below {drop_pct:>.2f}% below max24 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
					BoW(msg)
					if buy.mkt.budget.reserve_locked_tf:
						buy.mkt.budget.reserve_locked_tf = False
						speak('UNLOCKING RESERVES')
				else:
					msg = f'    * RESERVES LOCKED * : recent ({ago}) current price {buy.prc_buy:>.8f} below {drop_pct:>.2f}% below max24 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
					GoW(msg)
					if not buy.mkt.budget.reserve_locked_tf:
						buy.mkt.budget.reserve_locked_tf = True

		ago_list = ['ago0','ago1','ago2','ago3']
		for ago in ago_list:
			prc_drop_pct = round(((buy.prc_buy - max24) / max24) * 100, 2)
			msg = f'    * BUY REQUIRE : recent ({ago}) current price {buy.prc_buy:>.8f} below {drop_pct:>.2f}% below max30 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
			if buy.prc_buy < target_prc:
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)

		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = buy.ta[freq]['color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = buy.ta[freq]['ha_color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.mkt.buy_strat_type  = 'dn'
			buy.mkt.buy_strat_name  = 'drop'
			buy.mkt.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		buy.trade_strat_perf.pass_cnt     = len(all_passes)
		buy.trade_strat_perf.fail_cnt     = len(all_fails)
		buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
		buy.trade_strat_perf.all_passes   = all_passes
		buy.trade_strat_perf.all_fails    = all_fails
		buy.trade_strat_perf.buy_yn       = buy.buy_yn
		buy.trade_strat_perf.wait_yn      = buy.wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {buy.rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy.buy_yn  = 'N'
		buy.wait_yn = 'Y'

	buy.trade_strat_perf.buy_yn  = buy.buy_yn
	buy.trade_strat_perf.wait_yn = buy.wait_yn

	func_end(fnc)
	return buy

#<=====>#

# Bollinger Band Breakout
def buy_strat_bb_bo(buy):
	func_name = 'buy_strat_bb_bo'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = buy.prod_id
		buy.buy_yn           = 'Y'
		buy.wait_yn          = 'N'

		buy.rfreq = buy.trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(buy.rfreq)

#		# General Trend
#		check_list = ['sma100']
#		for x in check_list:
#			sma = ta[rfreq][x]['ago0']
#			msg = f'    * BUY REQUIRE : {rfreq} Current Price : {buy.prc_buy:>.8f} must be above current {x} : {sma}'
#			if not sma:
#				buy.buy_yn  = 'N'
#				all_fails.append(msg)
#			elif buy.prc_buy > sma:
#				all_passes.append(msg)
#			else:
#				buy.buy_yn  = 'N'
#				all_fails.append(msg)

		# Current High Above Inner BB Lower
		m = '    * BUY REQUIRE : current {} high : {:>.8f} above bb upper : {:>.8f}'
		msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['high']['ago0'], buy.ta[buy.rfreq]['bb_upper_bb_bo']['ago0'])
		if buy.ta[buy.rfreq]['high']['ago0'] > buy.ta[buy.rfreq]['bb_upper_bb_bo']['ago0']:
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# Current Close Above Inner BB Lower
		m = '    * BUY REQUIRE : pervious {} close : {:>.8f} above bb upper : {:>.8f}'
		msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['close']['ago1'], buy.ta[buy.rfreq]['bb_upper_bb_bo']['ago1'])
		if buy.ta[buy.rfreq]['close']['ago1'] > buy.ta[buy.rfreq]['bb_upper_bb_bo']['ago1']:
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = buy.ta[freq]['color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = buy.ta[freq]['ha_color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.mkt.buy_strat_type  = 'up'
			buy.mkt.buy_strat_name  = 'bb_bo'
			buy.mkt.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		buy.trade_strat_perf.pass_cnt     = len(all_passes)
		buy.trade_strat_perf.fail_cnt     = len(all_fails)
		buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
		buy.trade_strat_perf.all_passes   = all_passes
		buy.trade_strat_perf.all_fails    = all_fails
		buy.trade_strat_perf.buy_yn       = buy.buy_yn
		buy.trade_strat_perf.wait_yn      = buy.wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {buy.rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy.buy_yn  = 'N'
		buy.wait_yn = 'Y'

	buy.trade_strat_perf.buy_yn  = buy.buy_yn
	buy.trade_strat_perf.wait_yn = buy.wait_yn

	func_end(fnc)
	return buy

#<=====>#

# Bollinger Band Bounce
def buy_strat_bb(buy):
	func_name = 'buy_strat_bb'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = buy.prod_id
		buy.buy_yn           = 'Y'
		buy.wait_yn          = 'N'

		buy.rfreq = buy.trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(buy.rfreq)

		curr_close             = buy.ta[buy.rfreq]['close']['ago0']
		curr_bb_lower_inner    = buy.ta[buy.rfreq]['bb_lower_inner']['ago0']
		last_low               = buy.ta[buy.rfreq]['low']['ago1']
		last_bb_lower_outer    = buy.ta[buy.rfreq]['bb_lower_outer']['ago1']
		prev_low               = buy.ta[buy.rfreq]['low']['ago2']
		prev_bb_lower_outer    = buy.ta[buy.rfreq]['bb_lower_outer']['ago2']

		# Last Close Below Outer BB Lower
		msg = f'    * BUY REQUIRE : {buy.rfreq} last low : {last_low:>.8f} < bb lower outer : {last_bb_lower_outer:>.8f} or prev low : {prev_low:>.8f} < bb lower outer : {prev_bb_lower_outer:>.8f}'
		if last_low < last_bb_lower_outer or prev_low < prev_bb_lower_outer:
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# Current Close Above Inner BB Lower
		msg = f'    * BUY REQUIRE : {buy.rfreq} current close : {curr_close:>.8f} above inner bb lower : {curr_bb_lower_inner:>.8f}'
		if curr_close > curr_bb_lower_inner:
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = buy.ta[freq]['color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = buy.ta[freq]['ha_color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Nadaraya-Watson Estimator - Estimated Is Green
		ago_list = ['ago0','ago1']
		for ago in ago_list:
			m = '    * BUY REQUIRE : {} Nadaraya-Watson Estimator color {} == green : {}'
			msg = m.format(freq, ago, buy.ta[buy.rfreq]['nwe_color'][ago])
			if buy.ta[freq]['ha_color'][ago] == 'green':
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.mkt.buy_strat_type  = 'dn'
			buy.mkt.buy_strat_name  = 'bb'
			buy.mkt.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		buy.trade_strat_perf.pass_cnt     = len(all_passes)
		buy.trade_strat_perf.fail_cnt     = len(all_fails)
		buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
		buy.trade_strat_perf.all_passes   = all_passes
		buy.trade_strat_perf.all_fails    = all_fails
		buy.trade_strat_perf.buy_yn       = buy.buy_yn
		buy.trade_strat_perf.wait_yn      = buy.wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {buy.rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy.buy_yn  = 'N'
		buy.wait_yn = 'Y'

	buy.trade_strat_perf.buy_yn  = buy.buy_yn
	buy.trade_strat_perf.wait_yn = buy.wait_yn

	func_end(fnc)
	return buy

#<=====>#

def buy_strat_emax(buy):
	func_name = 'buy_strat_emax'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		prod_id          = buy.prod_id
		buy.buy_yn           = 'Y'
		buy.wait_yn          = 'N'

		all_passes       = []
		all_fails        = []

		buy.rfreq = buy.trade_strat_perf.buy_strat_freq
		freqs, faster_freqs     = freqs_get(buy.rfreq)

		# Exponential Moving Average Crosses
		if 1==1:
			m = '    * BUY REQUIRE : current 15min ema5 :{:>.8f} >>> ema8:{:>.8f}'
			msg = m.format(buy.ta['15min']['ema5']['ago0'], buy.ta['15min']['ema8']['ago0'])
			if buy.ta['15min']['ema5']['ago0'] > buy.ta['15min']['ema8']['ago0']:
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)
		if 1==1:
			m = '    * BUY REQUIRE : current 15min ema8 :{:>.8f} >>> ema13:{:>.8f}'
			msg = m.format(buy.ta['15min']['ema8']['ago0'], buy.ta['15min']['ema13']['ago0'])
			if buy.ta['15min']['ema8']['ago0'] > buy.ta['15min']['ema13']['ago0']:
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)
		if 1==1:
			m = '    * BUY REQUIRE : current 15min ema13 :{:>.8f} >>> ema21:{:>.8f}'
			msg = m.format(buy.ta['15min']['ema13']['ago0'], buy.ta['15min']['ema21']['ago0'])
			if buy.ta['15min']['ema13']['ago0'] > buy.ta['15min']['ema21']['ago0']:
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)

		# Current Candle is Green
		ago_list = ['ago0']
		for freq in freqs:
			for ago in ago_list:
				color = buy.ta[freq]['color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} candles == green : {color}'
				if color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
		ago_list = ['ago0','ago1']
		for freq in faster_freqs:
			for ago in ago_list:
				ha_color = buy.ta[freq]['ha_color'][ago]
				msg = f'    * BUY REQUIRE : {freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.mkt.buy_strat_type  = 'up'
			buy.mkt.buy_strat_name  = 'ema_cross'
			buy.mkt.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		buy.trade_strat_perf.pass_cnt     = len(all_passes)
		buy.trade_strat_perf.fail_cnt     = len(all_fails)
		buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
		buy.trade_strat_perf.all_passes   = all_passes
		buy.trade_strat_perf.all_fails    = all_fails
		buy.trade_strat_perf.buy_yn       = buy.buy_yn
		buy.trade_strat_perf.wait_yn      = buy.wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {buy.rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy.buy_yn  = 'N'
		buy.wait_yn = 'Y'

	buy.trade_strat_perf.buy_yn  = buy.buy_yn
	buy.trade_strat_perf.wait_yn = buy.wait_yn

	func_end(fnc)
	return buy

#<=====>#

# def buy_strat_ema_stoch(st, mkt, trade_perf, trade_strat_perf, ta):
# 	func_name = 'buy_strat_ema_stoch'
# 	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf, ta)'
# 	G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 
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
# 	buy.prc_buy         = mkt.prc_buy
# 	buy.buy_yn           = 'Y'
# 	buy.wait_yn          = 'N'
# 	show_tests_yn    = pst.buy.show_tests_yn
# 	show_tests_min   = pst.buy.show_tests_min

# 	all_passes       = []
# 	all_fails        = []

# 	# General Trend
# 	if 1==1:
# 		m = '    * BUY REQUIRE : Current Price : {:>.8f} must be above current 15min SMA_100 : {:>.8f}'
# 		msg = m.format(buy.prc_buy, ta['15min']['sma100']['ago0'])
# 		if buy.prc_buy > ta['15min']['sma100']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '    * BUY REQUIRE : Current Price : {:>.8f} must be above current 15min SMA_200 : {:>.8f}'
# 		msg = m.format(buy.prc_buy, ta['15min']['sma200']['ago0'])
# 		if buy.prc_buy > ta['15min']['sma200']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)

# 	# Current Candle is Green
# 	if 1==1:
# 		m = '    * BUY REQUIRE : 5min candle green ==> current : {:>5}'
# 		msg = m.format(ta['5min']['color']['ago0'])
# 		if ta['5min']['color']['ago0'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '    * BUY REQUIRE : 15min candle green ==> current : {:>5}'
# 		msg = m.format(ta['15min']['color']['ago0'])
# 		if ta['15min']['color']['ago0'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '    * BUY REQUIRE : 30min candle green ==> current : {:>5}'
# 		msg = m.format(ta['30min']['color']['ago0'])
# 		if ta['30min']['color']['ago0'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)

# 	# Heikin Ashi Candles - Multi Timeframe - Candles Are Green
# 	if 1==1:
# 		m = '    * BUY REQUIRE : 5min HA candles green ==> current : {:>5}, last : {:>5}'
# 		msg = m.format(ta['5min']['ha_color']['ago0'], ta['5min']['ha_color']['ago1'])
# 		if ta['5min']['ha_color']['ago0'] == 'green' and ta['5min']['ha_color']['ago1'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '    * BUY REQUIRE : 15min HA candles green ==> current : {:>5}, last : {:>5}'
# 		msg = m.format(ta['15min']['ha_color']['ago0'], ta['15min']['ha_color']['ago1'])
# 		if ta['15min']['ha_color']['ago0'] == 'green' and ta['15min']['ha_color']['ago1'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '    * BUY REQUIRE : 30min HA candles green ==> current : {:>5}, last : {:>5}'
# 		msg = m.format(ta['30min']['ha_color']['ago0'], ta['30min']['ha_color']['ago1'])
# 		if ta['30min']['ha_color']['ago0'] == 'green' and ta['30min']['ha_color']['ago1'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '    * BUY REQUIRE : 15min HA candles green ==> current : {:>5}, last : {:>5}'
# 		msg = m.format(ta['15min']['ha_color']['ago0'], ta['15min']['ha_color']['ago1'])
# 		if ta['15min']['ha_color']['ago0'] == 'green' and ta['15min']['ha_color']['ago1'] == 'green':
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)

# 	# Exponential Moving Average Crosses
# 	if 1==1:
# 		m = '    * BUY REQUIRE : current 15min ema5 :{:>.8f} >>> ema8:{:>.8f}'
# 		msg = m.format(ta['15min']['ema5']['ago0'], ta['15min']['ema8']['ago0'])
# 		if ta['15min']['ema5']['ago0'] > ta['15min']['ema8']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '    * BUY REQUIRE : current 15min ema8 :{:>.8f} >>> ema13:{:>.8f}'
# 		msg = m.format(ta['15min']['ema8']['ago0'], ta['15min']['ema13']['ago0'])
# 		if ta['15min']['ema8']['ago0'] > ta['15min']['ema13']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)
# 	if 1==1:
# 		m = '    * BUY REQUIRE : current 15min ema13 :{:>.8f} >>> ema21:{:>.8f}'
# 		msg = m.format(ta['15min']['ema13']['ago0'], ta['15min']['ema21']['ago0'])
# 		if ta['15min']['ema13']['ago0'] > ta['15min']['ema21']['ago0']:
# 			all_passes.append(msg)
# 		else:
# 			buy.buy_yn  = 'N'
# 			all_fails.append(msg)

# 	if buy_yn == 'Y':
# 		buy.wait_yn = 'N'
# 		mkt.buy_strat_type  = 'up'
# 		mkt.buy_strat_name  = 'ema_cross'
# 		mkt.buy_strat_freq  = rfreq
# 	else:
# 		buy.wait_yn = 'Y'

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
# 
# 	show_tests_yn    = pst.buy.show_tests_yn
# 	show_tests_min   = pst.buy.show_tests_min

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
# 
# 	show_tests_yn    = pst.buy.show_tests_yn
# 	show_tests_min   = pst.buy.show_tests_min

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
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

