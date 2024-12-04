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
from libs.lib_colors import cs, cp, G, WoR, WoG
from libs.lib_common import dttm_get, func_begin, func_end, print_adv, speak_async
from libs.lib_colors import BoW
from libs.bot_strat_common import disp_sell_tests
import pandas as pd
import numpy as np
import pandas_ta as pta


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strat_nwe_rev'
log_name      = 'bot_strat_nwe_rev'


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


def buy_strat_settings_nwe_rev(st):
	func_name = 'buy_strat_settings_nwe_rev'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# nwe
	buy_strat_st = {
					"use_yn": "Y",
					"freqs": ["1d", "4h", "1h", "30min", "15min"],
					"bandwidth": 8,
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

def sell_strat_settings_nwe_rev(st):
	func_name = 'sell_strat_settings_nwe_rev'
	func_str = f'{lib_name}.{func_name}(buy)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# nwe
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

def show_stuff(freq, ta, all_tf=False):
	func_name = 'buy_strat_nwe_env'
	func_str = f'{lib_name}.{func_name}(freq, ta)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	try:
		from pprint import pprint
		df = ta[freq].df
		# Print most recent signal times
		nwe_line       = df['nwe_line'].iloc[-1]
		nwe_mae        = df['nwe_mae'].iloc[-1]
		nwe_upper      = df['nwe_upper'].iloc[-1]
		nwe_lower      = df['nwe_lower'].iloc[-1]
		nwe_color      = df['nwe_color'].iloc[-1]
		nwe_color_last = df['nwe_color'].iloc[-2]
		nwe_color_prev = df['nwe_color'].iloc[-3]
		nwe_roc        = df['nwe_roc'].iloc[-1]
		nwe_roc_last   = df['nwe_roc'].iloc[-2]
		nwe_roc_prev   = df['nwe_roc'].iloc[-3]
		close          = df['close'].iloc[-1]

		print(f'{freq} => nwe_color : {nwe_color}, nwe_color_last : {nwe_color_last}, nwe_color_prev : {nwe_color_prev}')
		print(f'{freq} => close : {close:>18.12f}, nwe_mae : {nwe_mae:>18.12f}, nwe_line : {nwe_line:>18.12f}, nwe_upper : {nwe_upper:>18.12f}, nwe_lower : {nwe_lower:>18.12f}')
		print(f'{freq} => nwe_roc : {nwe_roc}, nwe_roc_last : {nwe_roc_last}, nwe_roc_prev : {nwe_roc_prev}')

		signal_cols = [
			'nwe_3row_buy_signal',
			'nwe_3row_sell_signal',
			'nwe_rev_buy_signal', 
			'nwe_rev_sell_signal',
			'nwe_env_buy_signal', 
			'nwe_env_sell_signal'
		]

		print(df[['nwe_line', 'nwe_roc', 'nwe_color', 'nwe_mae', 'nwe_upper', 'nwe_lower', 'nwe_3row_buy_signal', 'nwe_3row_sell_signal', 'nwe_rev_buy_signal', 'nwe_rev_sell_signal', 'nwe_env_buy_signal', 'nwe_env_sell_signal']].tail(5))

		if all_tf:
			for col in signal_cols:
				if df[col].any():  # Check if there are any signals
					signal_times = df[df[col] == 1].index.tolist()
					print(f"\nNWE - {freq} - All {col} {'↑' if 'buy' in col else '↓'}:")
					for signal_time in signal_times:
						print(f"  {signal_time}")
		else:
			for col in signal_cols:
				if df[col].any():  # Check if there are any signals
					last_signal = df[df[col] == 1].index[-1]
					print(f"NWE - {freq} - Last {col}: {last_signal} {'↑' if 'buy' in col else '↓'}")
	except Exception as e:
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		pass

	func_end(fnc)

#<=====>#

def buy_strat_nwe_rev(buy, ta, pst):
	func_name = 'buy_strat_nwe_rev'
	func_str = f'{lib_name}.{func_name}(buy, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	try:
		all_passes       = []
		all_fails        = []

		prod_id          = buy.prod_id
		buy.buy_yn       = 'Y'
		buy.wait_yn      = 'N'
		buy.show_tests_yn = buy.pst.buy.strats.nwe_rev.show_tests_yn


		buy.rfreq = buy.trade_strat_perf.buy_strat_freq
		freqs, faster_freqs = freqs_get(buy.rfreq)

		freq = buy.buy_strat_freq

		if pst.buy.strats.nwe_rev.show_tests_yn == 'Y':
			show_stuff(freq, ta, False)

		nwe_rev_buy_signal              = buy.ta[freq]['nwe_rev_buy_signal']['ago0']
		nwe_rev_sell_signal             = buy.ta[freq]['nwe_rev_sell_signal']['ago0']
		nwe_rev_buy_signal_last         = buy.ta[freq]['nwe_rev_buy_signal']['ago1']

		if buy.prod_id == 'BTC-USDC':
			if nwe_rev_buy_signal:
				speak_async(f"{buy.prod_id} has a Nadaraya Watson Reversal Buy Trigger on the {freq} timeframe")

		# -------------------------------
		# Integrate Buy Signals from Trend Reversal
		# -------------------------------
		if nwe_rev_buy_signal or (nwe_rev_buy_signal_last and not nwe_rev_sell_signal):
			msg = f'    * BUY SIGNAL: NWE_REV {freq} Trend Reversal detected (BULL)'
			buy.reason = msg.strip()
			all_passes.append(msg)
		else:
			buy.buy_yn = 'N'

		if buy.buy_yn == 'Y':
			buy.wait_yn = 'N'
			buy.buy_strat_type  = 'up'
			buy.buy_strat_name  = 'nwe_rev'
			buy.buy_strat_freq  = buy.rfreq
		else:
			buy.wait_yn = 'Y'

		# buy.trade_strat_perf.pass_cnt     = len(all_passes)
		# buy.trade_strat_perf.fail_cnt     = len(all_fails)
		# buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
		# buy.trade_strat_perf.pass_pct     = 0
		# if buy.trade_strat_perf.total_cnt > 0:
		# 	buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
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

def sell_strat_nwe_rev(mkt, pos, ta, pst):
	func_name = 'sell_strat_nwe_rev'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	try:
		# only_exit_if_profit_yn = 'Y'
		sell_prc    = mkt.prc_sell
		all_sells  = []
		all_hodls   = []

		freq = pos.buy_strat_freq

		if pst.sell.strats.nwe_rev.show_tests_yn == 'Y':
			show_stuff(freq, ta, False)

		nwe_color            = ta[freq]['nwe_color']['ago0']
		nwe_color_last       = ta[freq]['nwe_color']['ago1']

		nwe_buy              = ta[freq]['nwe_rev_buy_signal']['ago0']
		nwe_sell             = ta[freq]['nwe_rev_sell_signal']['ago0']
		nwe_sell_last        = ta[freq]['nwe_rev_sell_signal']['ago1']

		nwe_rev_buy_signal             = ta[freq]['nwe_rev_buy_signal']['ago0']
		nwe_rev_sell_signal            = ta[freq]['nwe_rev_sell_signal']['ago0']
		nwe_rev_sell_signal_last       = ta[freq]['nwe_rev_sell_signal']['ago1']

		if pos.prod_id == 'BTC-USDC':
			if nwe_rev_sell_signal:
				speak_async(f"{pos.prod_id} has a Nadaraya Watson Reversal Sell Trigger on the {freq} timeframe")

		if nwe_rev_sell_signal or (nwe_rev_sell_signal_last and not nwe_rev_buy_signal):
			pos.sell_yn = 'Y'
			pos.hodl_yn = 'N'
			msg = f'    * SELL SIGNAL: NWE_REV {freq} Trend Reversal (BEAR)'
			pos.reason = msg.strip()
			all_sells.append(msg)
		# elif nwe_color == 'red' and nwe_color_last == 'red':
		# 	pos.sell_yn = 'Y'
		# 	pos.hodl_yn = 'N'
		# 	msg = f'    * SELL SIGNAL: NWE_3ROW {freq} Red Shift'
		# 	pos.reason = msg.strip()
		# 	all_sells.append(msg)

		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
		msg = 'SELL TESTS - Nadaraya-Watson Estimator'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, pst=pst, all_sells=all_sells, all_hodls=all_hodls)

		exit_if_profit_yn      = pst.sell.strats.nwe_rev.exit_if_profit_yn
		exit_if_profit_pct_min = pst.sell.strats.nwe_rev.exit_if_profit_pct_min
		exit_if_loss_yn        = pst.sell.strats.nwe_rev.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(pst.sell.strats.nwe_rev.exit_if_loss_pct_max) * -1
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
			pos.sell_strat_name = 'nwe_rev'
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

