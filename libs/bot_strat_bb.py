<<<<<<< Updated upstream
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
from libs.bot_strat_common import disp_sell_tests, exit_if_logic

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strat_bb'
log_name      = 'bot_strat_bb'


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

#<=====>#


def buy_strat_settings_bb(st):
	func_name = 'buy_strat_settings_bb'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# bb
	buy_strat_st = {
					"use_yn": "Y",
					"freqs": ["1d", "4h", "1h", "30min", "15min"],
					"inner_per": 34,
					"inner_sd": 2.3,
					"outer_per": 34,
					"outer_sd": 2.7,
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

def sell_strat_settings_bb(st):
	func_name = 'sell_strat_settings_bb'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# bb
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

# Bollinger Band Bounce
def buy_strat_bb(buy, ta, pst):
	func_name = 'buy_strat_bb'
	func_str = f'{lib_name}.{func_name}(buy, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		all_passes           = []
		all_fails            = []
		prod_id              = buy.prod_id
		buy.buy_yn           = 'Y'
		buy.wait_yn          = 'N'
		buy.show_tests_yn    = buy.pst.buy.strats.bb.show_tests_yn

		buy.rfreq            = buy.trade_strat_perf.buy_strat_freq
		freqs, faster_freqs  = freqs_get(buy.rfreq)

		curr_close           = buy.ta[buy.rfreq]['close']['ago0']
		curr_bb_lower_inner  = buy.ta[buy.rfreq]['bb_lower_inner']['ago0']
		last_low             = buy.ta[buy.rfreq]['low']['ago1']
		last_bb_lower_outer  = buy.ta[buy.rfreq]['bb_lower_outer']['ago1']
		prev_low             = buy.ta[buy.rfreq]['low']['ago2']
		prev_bb_lower_outer  = buy.ta[buy.rfreq]['bb_lower_outer']['ago2']

		# Last Close Below Outer BB Lower
		msg = f'{buy.rfreq} last low : {last_low:>.8f} < bb lower outer : {last_bb_lower_outer:>.8f} or prev low : {prev_low:>.8f} < bb lower outer : {prev_bb_lower_outer:>.8f}'
		if last_low < last_bb_lower_outer or prev_low < prev_bb_lower_outer:
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# Current Close Above Inner BB Lower
		msg = f'{buy.rfreq} current close : {curr_close:>.8f} above inner bb lower : {curr_bb_lower_inner:>.8f}'
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
				msg = f'{freq} {ago} candles == green : {color}'
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
				msg = f'{freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Nadaraya-Watson Estimator - Estimated Is Green
		ago_list = ['ago0','ago1']
		for ago in ago_list:
			m = '{} Nadaraya-Watson Estimator color {} == green : {}'
			msg = m.format(freq, ago, buy.ta[buy.rfreq]['nwe_color'][ago])
			if buy.ta[freq]['ha_color'][ago] == 'green':
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.buy_strat_type  = 'dn'
			buy.buy_strat_name  = 'bb'
			buy.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		buy.trade_strat_perf.pass_cnt     = len(all_passes)
		buy.trade_strat_perf.fail_cnt     = len(all_fails)
		buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
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

#	print(f'{lib_name}.{func_name} => prod_id : {buy.prod_id}, buy_yn : {buy.buy_yn}, wait_yn : {buy.wait_yn}')

	func_end(fnc)
	return buy, ta

#<=====>#

def sell_strat_bb(mkt, pos, ta, pst):
	func_name = 'sell_strat_bb'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		sell_prc    = mkt.prc_sell
		all_sells   = []
		all_hodls   = []

		rfreq = pos.buy_strat_freq
		freq = pos.buy_strat_freq

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
			msg = f'SELL COND: {rfreq} current price : {sell_prc:>.8f} below bb lower outer : {curr_bb_lower_outer:>.8f} and gain_pct < 0 : {pos.gain_loss_pct_est}'
			all_sells.append(msg)
		else:
			bb_downward_spiral_tf = False
			msg = f'HODL COND: {rfreq} current price : {sell_prc:>.8f} above bb lower outer : {curr_bb_lower_outer:>.8f} and gain_pct < 0 : {pos.gain_loss_pct_est}'
			all_hodls.append(msg)

		if bb_downward_spiral_tf:
			pos.sell_yn  = 'Y'
		else:
			pos.sell_yn  = 'N'

		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
		msg = '    SELL TESTS - Bollinger Band'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, pst=pst, all_sells=all_sells, all_hodls=all_hodls)


		pos = exit_if_logic(pos=pos, pst=pst)


		if pos.sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'bb'
			pos.sell_strat_freq = freq
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

=======
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
from libs.bot_strat_common import disp_sell_tests, exit_if_logic

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strat_bb'
log_name      = 'bot_strat_bb'


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

#<=====>#


def buy_strat_settings_bb(st):
	func_name = 'buy_strat_settings_bb'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# bb
	buy_strat_st = {
					"use_yn": "Y",
					"freqs": ["1d", "4h", "1h", "30min", "15min"],
					"inner_per": 34,
					"inner_sd": 2.3,
					"outer_per": 34,
					"outer_sd": 2.7,
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

def sell_strat_settings_bb(st):
	func_name = 'sell_strat_settings_bb'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# bb
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

# Bollinger Band Bounce
def buy_strat_bb(buy, ta, pst):
	func_name = 'buy_strat_bb'
	func_str = f'{lib_name}.{func_name}(buy, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		all_passes           = []
		all_fails            = []
		prod_id              = buy.prod_id
		buy.buy_yn           = 'Y'
		buy.wait_yn          = 'N'
		buy.show_tests_yn    = buy.pst.buy.strats.bb.show_tests_yn

		buy.rfreq            = buy.trade_strat_perf.buy_strat_freq
		freqs, faster_freqs  = freqs_get(buy.rfreq)

		curr_close           = buy.ta[buy.rfreq]['close']['ago0']
		curr_bb_lower_inner  = buy.ta[buy.rfreq]['bb_lower_inner']['ago0']
		last_low             = buy.ta[buy.rfreq]['low']['ago1']
		last_bb_lower_outer  = buy.ta[buy.rfreq]['bb_lower_outer']['ago1']
		prev_low             = buy.ta[buy.rfreq]['low']['ago2']
		prev_bb_lower_outer  = buy.ta[buy.rfreq]['bb_lower_outer']['ago2']

		# Last Close Below Outer BB Lower
		msg = f'{buy.rfreq} last low : {last_low:>.8f} < bb lower outer : {last_bb_lower_outer:>.8f} or prev low : {prev_low:>.8f} < bb lower outer : {prev_bb_lower_outer:>.8f}'
		if last_low < last_bb_lower_outer or prev_low < prev_bb_lower_outer:
			all_passes.append(msg)
		else:
			buy.buy_yn  = 'N'
			all_fails.append(msg)

		# Current Close Above Inner BB Lower
		msg = f'{buy.rfreq} current close : {curr_close:>.8f} above inner bb lower : {curr_bb_lower_inner:>.8f}'
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
				msg = f'{freq} {ago} candles == green : {color}'
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
				msg = f'{freq} {ago} Heikin Ashi candles == green : {ha_color}'
				if ha_color == 'green':
					all_passes.append(msg)
				else:
					buy.buy_yn  = 'N'
					all_fails.append(msg)

		# Nadaraya-Watson Estimator - Estimated Is Green
		ago_list = ['ago0','ago1']
		for ago in ago_list:
			m = '{} Nadaraya-Watson Estimator color {} == green : {}'
			msg = m.format(freq, ago, buy.ta[buy.rfreq]['nwe_color'][ago])
			if buy.ta[freq]['ha_color'][ago] == 'green':
				all_passes.append(msg)
			else:
				buy.buy_yn  = 'N'
				all_fails.append(msg)

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.buy_strat_type  = 'dn'
			buy.buy_strat_name  = 'bb'
			buy.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		buy.trade_strat_perf.pass_cnt     = len(all_passes)
		buy.trade_strat_perf.fail_cnt     = len(all_fails)
		buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
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

#	print(f'{lib_name}.{func_name} => prod_id : {buy.prod_id}, buy_yn : {buy.buy_yn}, wait_yn : {buy.wait_yn}')

	func_end(fnc)
	return buy, ta

#<=====>#

def sell_strat_bb(mkt, pos, ta, pst):
	func_name = 'sell_strat_bb'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		sell_prc    = mkt.prc_sell
		all_sells   = []
		all_hodls   = []

		rfreq = pos.buy_strat_freq
		freq = pos.buy_strat_freq

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
			msg = f'SELL COND: {rfreq} current price : {sell_prc:>.8f} below bb lower outer : {curr_bb_lower_outer:>.8f} and gain_pct < 0 : {pos.gain_loss_pct_est}'
			all_sells.append(msg)
		else:
			bb_downward_spiral_tf = False
			msg = f'HODL COND: {rfreq} current price : {sell_prc:>.8f} above bb lower outer : {curr_bb_lower_outer:>.8f} and gain_pct < 0 : {pos.gain_loss_pct_est}'
			all_hodls.append(msg)

		if bb_downward_spiral_tf:
			pos.sell_yn  = 'Y'
		else:
			pos.sell_yn  = 'N'

		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
		msg = '    SELL TESTS - Bollinger Band'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, pst=pst, all_sells=all_sells, all_hodls=all_hodls)


		pos = exit_if_logic(pos=pos, pst=pst)


		if pos.sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'bb'
			pos.sell_strat_freq = freq
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

>>>>>>> Stashed changes
