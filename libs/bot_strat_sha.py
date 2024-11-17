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
import traceback
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_charts import chart_row
from libs.lib_colors import cs, cp, G
from libs.lib_common import dttm_get, func_begin, func_end, print_adv
from libs.lib_colors import BoW
from libs.bot_strat_common import disp_sell_tests


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strat_sha'
log_name      = 'bot_strat_sha'


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

def buy_strat_settings_sha(st):
	func_name = 'buy_strat_settings_sha'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# sha
	buy_strat_st = {
					"use_yn": "Y",
					"freqs": ["1d", "4h", "1h", "30min", "15min"],
					"fast_sha_len1": 8,
					"fast_sha_len2": 8,
					"slow_sha_len1": 13,
					"slow_sha_len2": 13,
					"prod_ids": [],
					"skip_prod_ids": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
					"boost_tests_min": {"15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11},
					"show_tests_yn": "Y"
					}

	st['buy']['strats']['sha'] = buy_strat_st

	func_end(fnc)
	return st

#<=====>#

def sell_strat_settings_sha(st):
	func_name = 'sell_strat_settings_sha'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# sha
	sell_strat_st = {
					"exit_if_profit_yn": "Y",
					"exit_if_profit_pct_min": 1,
					"exit_if_loss_yn": "N",
					"exit_if_loss_pct_max": 3,
					"skip_prod_ids": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
					"show_tests_yn": "Y"
					}

	st['sell']['strats']['sha'] = sell_strat_st

	func_end(fnc)
	return st

#<=====>#

def buy_strat_sha(buy, ta, pst):
	func_name = 'buy_strat_sha'
	func_str = f'{lib_name}.{func_name}(buy, ta, pst)'
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

		buy.show_tests_yn = buy.pst.buy.strats.sha.show_tests_yn

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
			buy.buy_strat_type  = 'up'
			buy.buy_strat_name  = 'sha'
			buy.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		# buy.trade_strat_perf.pass_cnt     = len(all_passes)
		# buy.trade_strat_perf.fail_cnt     = len(all_fails)
		# buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		# buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
		buy.all_passes   = all_passes
		buy.all_fails    = all_fails
		buy.buy_yn       = buy.buy_yn
		buy.wait_yn      = buy.wait_yn

	except Exception as e:
		print(f'{dttm_get()} {func_name} {buy.rfreq} {prod_id} ==> Error : ({type(e)}){e}')
		traceback.print_exc()
		print_adv(3)
		beep()
		buy.buy_yn  = 'N'
		buy.wait_yn = 'Y'

	buy.buy_yn  = buy.buy_yn
	buy.wait_yn = buy.wait_yn

	func_end(fnc)
	return buy, ta

#<=====>#

def sell_strat_sha(mkt, pos, ta, pst):
	func_name = 'sell_strat_sha'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		# only_exit_if_profit_yn = 'Y'
		sell_prc    = mkt.prc_sell
		all_sells  = []
		all_hodls   = []

		freq = pos.buy_strat_freq

		ha_color_5min = ta['5min']['ha_color']

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
			msg = f'SELL COND: {freq} sha fast body is shrinking - curr {sha_fast_body_curr:>.8f} <<< last {sha_fast_body_last:>.8f} <<<  prev {sha_fast_body_prev:>.8f}'
			all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} sha fast body not shrinking - curr {sha_fast_body_curr:>.8f} >>> last {sha_fast_body_last:>.8f} >>>  prev {sha_fast_body_prev:>.8f}'
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
			msg = f'SELL COND: {freq} sha slow body is shrinking - curr {sha_slow_body_curr:>.8f} <<< last {sha_slow_body_last:>.8f} <<<  prev {sha_slow_body_prev:>.8f}'
			all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} sha slow body not shrinking - curr {sha_slow_body_curr:>.8f} >>> last {sha_slow_body_last:>.8f} >>>  prev {sha_slow_body_prev:>.8f}'
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
				msg = f'SELL COND: {freq} {ago_desc} smaller upper wick - upper {sha_fast_wick_upper:>.8f} <<< lower {sha_fast_wick_lower:>.8f}'
				temp_all_sells.append(msg)
			else:
				sha_fast_upper_wick_weakening_tf = False
				msg = f'HODL COND: {freq} {ago_desc} larger upper wick - upper {sha_fast_wick_upper:>.8f} >>> lower {sha_fast_wick_lower:>.8f}' 
				temp_all_hodls.append(msg)
			# Need 4 in a row for test2 to be True

		if sha_fast_upper_wick_weakening_tf:
			msg = f'SELL COND: {freq} smaller upper wick for 4 consecutive candles'
			all_sells.append(msg)
			for msg in temp_all_sells:
				all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} larger upper wick in last 4 consecutive candles'
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
				msg = f'SELL COND: {freq} {ago_desc} smaller upper wick - upper {sha_slow_wick_upper:>.8f} <<< lower {sha_slow_wick_lower:>.8f}'
				temp_all_sells.append(msg)
			else:
				sha_slow_upper_wick_weakening_tf = False
				msg = f'HODL COND: {freq} {ago_desc} larger upper wick - upper {sha_slow_wick_upper:>.8f} >>> lower {sha_slow_wick_lower:>.8f}' 
				temp_all_hodls.append(msg)
			# Need 4 in a row for test2 to be True

		if sha_slow_upper_wick_weakening_tf:
			msg = f'SELL COND: {freq} smaller upper wick for 4 consecutive candles'
			all_sells.append(msg)
			for msg in temp_all_sells:
				all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} larger upper wick in last 4 consecutive candles'
			all_hodls.append(msg)
			for msg in temp_all_hodls:
				all_hodls.append(msg)

		# check if the price is intersecting the sha fast candles
		sha_fast_close = ta[freq]['sha_fast_close']['ago0']
		if sell_prc < sha_fast_close:
			sell_prc_intersect_sha_fast_tf = True
			msg = f'SELL COND: {freq} curr_price : {sell_prc:>.8f} is be below sha_fast_close {sha_fast_close:>.8f}'
			all_sells.append(msg)
		else:
			sell_prc_intersect_sha_fast_tf = False
			msg = f'HODL COND: {freq} curr_price : {sell_prc:>.8f} is be above sha_fast_close {sha_fast_close:>.8f}'
			all_hodls.append(msg)

		# check if sha fast candles are reddening
		sha_fast_color_curr = ta[freq]['sha_fast_color']['ago0']
		sha_fast_color_last = ta[freq]['sha_fast_color']['ago1']
		sha_fast_color_prev = ta[freq]['sha_fast_color']['ago2']
		if sha_fast_color_curr == 'red' and sha_fast_color_last == 'red' and sha_fast_color_prev == 'red':
			sha_fast_reddening_tf = True
			msg = f'SELL COND: {freq} sha fast colors ==> curr : {sha_fast_color_curr:>5}, last : {sha_fast_color_last:>5}, prev : {sha_fast_color_prev:>5}'
			all_sells.append(msg)
		else:
			sha_fast_reddening_tf = False
			msg = f'HODL COND: {freq} sha fast colors ==> curr : {sha_fast_color_curr:>5}, last : {sha_fast_color_last:>5}, prev : {sha_fast_color_prev:>5}'
			# YES!!! Allow the green candles to override the price touch above!
			all_hodls.append(msg)

		# check if sha slow candles are reddening
		sha_slow_color_curr = ta[freq]['sha_slow_color']['ago0']
		sha_slow_color_last = ta[freq]['sha_slow_color']['ago1']
		sha_slow_color_prev = ta[freq]['sha_slow_color']['ago2']
		if sha_slow_color_curr == 'red' and sha_slow_color_last == 'red' and sha_slow_color_prev == 'red':
			# sha_slow_reddening_tf = True
			msg = f'SELL COND: {freq} sha slow colors ==> curr : {sha_slow_color_curr:>5}, last : {sha_slow_color_last:>5}, prev : {sha_slow_color_prev:>5}'
			all_sells.append(msg)
		else:
			# sha_slow_reddening_tf = False
			msg = f'HODL COND: {freq} sha slow colors ==> curr : {sha_slow_color_curr:>5}, last : {sha_slow_color_last:>5}, prev : {sha_slow_color_prev:>5}'
			# YES!!! Allow the green candles to override the price touch above!
			all_hodls.append(msg)


		if sha_fast_body_shrinking_tf and sha_fast_upper_wick_weakening_tf and ha_color_5min == 'red':
			pos.sell_yn  = 'Y'
		elif sha_fast_body_shrinking_tf and sha_slow_body_shrinking_tf and ha_color_5min == 'red':
			pos.sell_yn  = 'Y'
		elif sell_prc_intersect_sha_fast_tf and (sha_fast_body_shrinking_tf or sha_slow_body_shrinking_tf or sha_fast_reddening_tf):
			pos.sell_yn  = 'Y'


		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
		msg = '    SELL TESTS - Smoothed Heikin Ashi'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, pst=pst, all_sells=all_sells, all_hodls=all_hodls)

		exit_if_profit_yn      = pst.sell.strats.sha.exit_if_profit_yn
		exit_if_profit_pct_min = pst.sell.strats.sha.exit_if_profit_pct_min
		exit_if_loss_yn        = pst.sell.strats.sha.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(pst.sell.strats.sha.exit_if_loss_pct_max) * -1
		if pos.sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pst.sell.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif pos.prc_chg_pct <= 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pst.sell.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'

		if pos.sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'sha'
			pos.sell_strat_freq = pos.buy_strat_freq
			pos.hodl_yn = 'N'
		else:
			pos.sell_yn = 'N'
			pos.hodl_yn = 'Y'

#		print(f'{lib_name}.{func_name} => prod_id : {pos.prod_id}, pos_id : {pos.pos_id}, sell_yn : {pos.sell_yn}, hodl_yn : {pos.hodl_yn}')

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {pos.prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos, ta

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

