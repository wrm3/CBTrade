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
lib_name      = 'bot_strat_bb_bo'
log_name      = 'bot_strat_bb_bo'


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


def buy_strat_settings_bb_bo(st):
	func_name = 'buy_strat_settings_bb_bo'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# bb_bo
	buy_strat_st = {
					"use_yn": "Y",
					"freqs": ["1d", "4h", "1h", "30min", "15min"],
					"per": 21,
					"sd": 2.1,
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

def sell_strat_settings_bb_bo(st):
	func_name = 'sell_strat_settings_bb_bo'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# bb_bo
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

# Bollinger Band Breakout
def buy_strat_bb_bo(buy, ta, pst):
	func_name = 'buy_strat_bb_bo'
	func_str = f'{lib_name}.{func_name}(buy, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		all_passes       = []
		all_fails        = []
		prod_id          = buy.prod_id
		buy.buy_yn           = 'Y'
		buy.wait_yn          = 'N'
		buy.show_tests_yn = buy.pst.buy.strats.bb_bo.show_tests_yn

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
			buy.buy_strat_type  = 'up'
			buy.buy_strat_name  = 'bb_bo'
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

	func_end(fnc)
	return buy, ta

#<=====>#

def sell_strat_bb_bo(mkt, pos, ta, pst):
	func_name = 'sell_strat_bb_bo'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		sell_prc    = mkt.prc_sell
		all_sells   = []
		all_hodls   = []

		rfreq = pos.buy_strat_freq
		freq = pos.buy_strat_freq

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

		if age_mins > min_mins and pos.gain_loss_pct_est < -3:
			msg = f'SELL COND: {rfreq} pos.gain_loss_pct_est < -3 : {pos.gain_loss_pct_est}'
			pos.sell_yn  = 'Y'
			all_sells.append(msg)
		else:
			pos.sell_yn  = 'N'

		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
		msg = '    SELL TESTS - Bollinger Bands Breakout'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, pst=pst, all_sells=all_sells, all_hodls=all_hodls)

		exit_if_profit_yn      = pst.sell.strats.drop.exit_if_profit_yn
		exit_if_profit_pct_min = pst.sell.strats.drop.exit_if_profit_pct_min
		exit_if_loss_yn        = pst.sell.strats.drop.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(pst.sell.strats.drop.exit_if_loss_pct_max) * -1
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
					msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} -  cancelling sell...'
					if pst.sell.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'

		if pos.sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = pos.buy_strat_name
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

