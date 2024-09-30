#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from datetime import datetime as dt
from libs.bot_ta import ta_main_new
from libs.bot_theme import cs_pct_color
from libs.lib_common import dec, play_cash, play_thunder, speak_async
from datetime import datetime, timedelta
from libs.bot_coinbase import cb, cb_bal_get, cb_client_order_id, cb_ord_get
from libs.bot_common import calc_chg_pct, freqs_get, writeit
from libs.bot_db_read import db_poss_check_last_dttm_get, db_sell_double_check, db_sell_ords_get_by_pos_id
from libs.bot_db_write import db_poss_check_last_dttm_upd, db_poss_stat_upd, db_tbl_poss_insupd, db_tbl_sell_ords_insupd
from libs.bot_settings import bot_settings_get, debug_settings_get, get_lib_func_secs_max, mkt_settings_get
from libs.bot_strats_sell import sell_strats_check
from libs.cls_settings import AttrDict
from libs.lib_charts import chart_headers, chart_mid, chart_row
from libs.lib_colors import G, R, WoG, WoR, cs
from libs.lib_common import AttrDictConv, beep, dec_2_float, dttm_get, func_begin, func_end, print_adv
from libs.lib_strings import format_disp_age
from pprint import pprint
import decimal
import sys
import time
import traceback


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_cls_sell'
log_name      = 'bot_cls_sell'
lib_secs_max  = 2

# <=====>#
# Assignments Pre
# <=====>#

from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)


#<=====>#
# Classes
#<=====>#

class POS(AttrDict):

	def __init__(pos, mkt, pair, pos_data, ta):
		pos.class_name                = 'POS'
		pos.mkt                            = mkt
		pos.pair                           = pair
		for k, v in pos_data.items():
			pos[k] = v
		pos.age_mins = pos.new_age_mins
		pos.symb                           = mkt.symb
		pos.dst, pos.debug_settings       = debug_settings_get()
		pos.bst, pos.bot_settings         = bot_settings_get()
		pos.mst, pos.mkt_settings         = mkt_settings_get(symb=pos.symb)
		pos.sell_yn                        = 'N'
		pos.sell_block_yn                  = 'N'
		pos.hodl_yn                        = 'N'
		pos.ta                             = ta
		pos.sell_prc                       = pair.prc_sell
		pos.sell_yn                        = 'N'
		pos.hodl_yn                        = 'Y'
		pos.sell_block_yn                  = 'N'
		pos.sell_force_yn                  = 'N'
		pos.sell_blocks                    = []
		pos.sell_forces                    = []
		pos.sell_tests                     = []
		pos.sell_test_sells                = []
		pos.sell_test_hodls                = []
		pos.sell_signals                   = []
		pos.sell_strat_type                = ''
		pos.sell_strat_name                = ''

	#<=====>#

	def sell_settings(pos):
		func_name = 'sell_settings'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		pos.mst.selling_on_yn                    = pos.mst.sell.selling_on_yn
		pos.mst.force_all_tests_yn               = pos.mst.sell.force_all_tests_yn

		pos.mst.show_blocks_yn                   = pos.mst.sell.show_blocks_yn
		pos.mst.show_forces_yn                   = pos.mst.sell.show_forces_yn

		pos.mst.show_tests_yn                    = pos.mst.sell.show_tests_yn
		pos.mst.show_tests_min                   = pos.mst.sell.show_tests_min
		pos.mst.save_files_yn                    = pos.mst.sell.save_files_yn
		pos.mst.sell_limit_yn                    = pos.mst.sell.sell_limit_yn

		pos.mst.hard_take_profit_yn              = pos.mst.sell.take_profit.hard_take_profit_yn
		pos.mst.hard_take_profit_pct             = pos.mst.sell.take_profit.hard_take_profit_pct
		pos.mst.trailing_profit_yn               = pos.mst.sell.take_profit.trailing_profit_yn
		pos.mst.trailing_profit_trigger_pct      = pos.mst.sell.take_profit.trailing_profit_trigger_pct

		pos.mst.hard_stop_loss_yn                = pos.mst.sell.stop_loss.hard_stop_loss_yn
		pos.mst.hard_stop_loss_pct               = pos.mst.sell.stop_loss.hard_stop_loss_pct

		pos.mst.trailing_stop_loss_yn            = pos.mst.sell.stop_loss.trailing_stop_loss_yn
		pos.mst.trailing_stop_loss_pct           = pos.mst.sell.stop_loss.trailing_stop_loss_pct

		pos.mst.atr_stop_loss_yn                 = pos.mst.sell.stop_loss.atr_stop_loss_yn
		pos.mst.atr_stop_loss_rfeq               = pos.mst.sell.stop_loss.atr_stop_loss_rfreq

		pos.mst.trailing_atr_stop_loss_yn        = pos.mst.sell.stop_loss.trailing_atr_stop_loss_yn
		pos.mst.trailing_atr_stop_loss_pct       = pos.mst.sell.stop_loss.trailing_atr_stop_loss_pct
		pos.mst.trailing_atr_stop_loss_rfreq     = pos.mst.sell.stop_loss.trailing_atr_stop_loss_rfreq

		pos.mst.force_sell_all_yn                = pos.mst.sell.force_sell_all_yn
		pos.mst.force_sell_prod_ids              = pos.mst.sell.force_sell.prod_ids
		pos.mst.force_sell_pos_ids               = pos.mst.sell.force_sell.pos_ids

		pos.mst.never_sell_all_yn                = pos.mst.sell.never_sell_all_yn
		pos.mst.never_sell_prod_ids              = pos.mst.sell.never_sell.prod_ids
		pos.mst.never_sell_pos_ids               = pos.mst.sell.never_sell.pos_ids

		pos.mst.never_sell_loss_all_yn           = pos.mst.sell.never_sell_loss_all_yn
		pos.mst.never_sell_loss_prod_ids         = pos.mst.sell.never_sell_loss.prod_ids
		pos.mst.never_sell_loss_pos_ids          = pos.mst.sell.never_sell_loss.pos_ids

		func_end(fnc)

	#<=====>#

	def sell_pos_logic(pos):
		func_name = 'sell_pos_logic'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		t0 = time.perf_counter()

		# Settings
		pos.sell_settings()

		pos.bal_cnt = cb_bal_get(pos.pair.base_curr_symb)
		if pos.bal_cnt == 0:
			pos.bal_cnt = cb_bal_get(pos.symb)
		if pos.bal_cnt == 0:
			print(f'{lib_name}.{func_name} => {pos.prod_id} balance is {pos.bal_cnt}...')
			beep(3)
			sys.exit()

		pos.disp_sell()
		db_poss_check_last_dttm_upd(pos.pos_id)
		pos.check_last_dttm = db_poss_check_last_dttm_get(pos.pos_id)

		# Halt And Catch Fire
		sos = db_sell_ords_get_by_pos_id(pos.pos_id)
		if sos:
			print(f'{lib_name}.{func_name} => Halt & Catch Fire...')
			del pos['ta']
			del pos['pair']
			del pos['st']
			print(pos)
			print('')
			for so in sos:
				print(so)
				print('')
			beep(10)
			sys.exit()

		# Forced Sell Logic
		if pos.sell_yn == 'N':
			pos.sell_pos_forces()

		# Logic that will block the sell from happening
		if pos.sell_force_yn == 'N':
			pos.sell_pos_blocks()

		# Sells Tests that don't require TA
		if pos.sell_yn == 'N':
			pos.sell_tests_before_ta()

		if pos.sell_yn == 'N':
			if not pos.ta:
				t0 = time.perf_counter()
				try:
					pos.ta = ta_main_new(pos.pair, pos.mst)
					if not pos.ta:
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')

					elif pos.ta == 'Error!':
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {pos.prod_id} - close prices do not match')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {pos.prod_id} - close prices do not match')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {pos.prod_id} - close prices do not match')
						pos.ta = None

				except Exception as e:
					print(f'{dttm_get()} {func_name} - Get TA ==> {pos.prod_id} = Error : ({type(e)}){e}')
					traceback.print_exc()
					beep(3)
					pass
				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				timing_data = {'Technical Analysis in Sell POS Logic': secs}
				pos.pair.timings.append(timing_data)
				if secs >= 5:
					msg = cs(f'mkt_ta_main_new for {pos.prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
					chart_row(msg, len_cnt=240)
					chart_mid(len_cnt=240)
			if pos.ta:
				pos.pair.ta = pos.ta

		# Sell By Strat Logic - These do require TA
		if pos.sell_yn == 'N' and pos.ta:
			pos.pair, pos = sell_strats_check(pos.pair, pos, pos.ta)

		# This is a blocker that will only be checked for TA sells
		if pos.sell_yn == 'Y':
			if pos.sell_force_yn == 'N':
				if pos.sell_block_yn == 'N':
					if pos.ta:
						pos.sell_deny_all_green()

		# Finalize YesNos
		if pos.sell_force_yn == 'Y':
			pos.sell_yn = 'Y'
			pos.hodl_yn = 'N'
		elif pos.sell_block_yn == 'Y':
			pos.sell_yn = 'N'
			pos.hodl_yn = 'Y'
		elif pos.sell_yn == 'Y':
			pos.hodl_yn = 'N'
		else:
			pos.sell_yn = 'N'
			pos.hodl_yn = 'Y'

#		db_tbl_poss_insupd(pos)

		if pos.sell_yn == 'Y' and pos.sell_block_yn == 'N':
			if pos.test_tf == 0:
				pos.sell_live()
				if pos.error_tf:
					play_thunder()
					pos.sell_yn = 'N'
					if pos.mst.speak_yn == 'Y': speak_async(pos.reason)
				else:
					if pos.gain_loss_amt > 0:
						msg = f'WIN, selling {pos.base_curr_symb} for ${round(pos.gain_loss_amt_est,2)} '
						if pos.mst.speak_yn == 'Y': speak_async(msg)
						if pos.gain_loss_amt >= 1:
							play_cash()
					elif pos.gain_loss_amt < 0:
						msg = f'LOSS, selling {pos.base_curr_symb} for ${round(pos.gain_loss_amt_est,2)} '
						if pos.mst.speak_yn == 'Y': speak_async(msg)
						if pos.gain_loss_amt <= -1:
							play_thunder()
			elif pos.test_tf == 1:
				pos = pos.sell_test()

		pos.sell_save()

#		db_tbl_poss_insupd(pos)

		t1 = time.perf_counter()
		secs = round(t1 - t0, 3)
		timing_data = {f'sell_logic, sell_pos_logic({pos.pos_id})': secs}
		pos.pair.timings.append(timing_data)

		func_end(fnc)
		return pos.pair, pos, pos.ta

	#<=====>#

	def sell_pos_blocks(pos):
		func_name = 'sell_pos_blocks'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		# sell_block_selling_off
		if pos.mst.selling_on_yn == 'N':
			pos.sell_block_yn = 'Y'
			msg = f'settings => selling_on_yn : {pos.mst.selling_on_yn}'
			pos.sell_blocks.append(msg)

		# sell_block_never_sell_all(pos):
		if pos.mst.never_sell_all_yn == 'Y':
			pos.sell_block_yn = 'Y'
			msg = f'settings => never_sell_all_yn : {pos.mst.never_sell_all_yn}'
			pos.sell_blocks.append(msg)

		# sell_block_never_sell_loss_all(pos):
		if pos.mst.never_sell_loss_all_yn == 'Y' and pos.prc_chg_pct < 0:
			pos.sell_block_yn = 'Y'
			msg = f'settings => never_sell_loss_all_yn : {pos.mst.never_sell_loss_all_yn}'
			pos.sell_blocks.append(msg)

		# sell_block_never_sell_prod_id(pos):
		if pos.prod_id in pos.mst.never_sell_prod_ids:
			pos.sell_block_yn = 'Y'
			msg = f'settings => never_sell.prod_ids : {pos.prod_id}'
			pos.sell_blocks.append(msg)

		# sell_block_never_sell_loss_prod_id(pos):
		if pos.prod_id in pos.mst.never_sell_loss_prod_ids and pos.prc_chg_pct < 0:
			pos.sell_block_yn = 'Y'
			msg = f'settings => never_sell_loss.prod_ids : {pos.prod_id}'
			pos.sell_blocks.append(msg)

		# sell_block_never_sell_pos_id(pos):
		if pos.pos_id in pos.mst.never_sell_pos_ids:
			pos.sell_block_yn = 'Y'
			msg = f'settings => never_sell.pos_ids : {pos.pos_id}'
			pos.sell_blocks.append(msg)

		#sell_block_never_sell_loss_pos_id(pos):
		if pos.pos_id in pos.mst.never_sell_loss_pos_ids and pos.prc_chg_pct < 0:
			pos.sell_block_yn = 'Y'
			msg = f'settings => never_sell_loss.pos_ids : {pos.pos_id}'
			pos.sell_blocks.append(msg)


		# sell_block_price_range_extreme(pos):
		# Market Price Range Looks Very Suspect
		if pos.pair.prc_range_pct >= 5:
			pos.sell_block_yn = 'Y'
			msg = f'price range variance of {pos.pair.prc_range_pct}, bid : {pos.bid_prc}, ask : {pos.ask_prc}, this price range looks sus... skipping sell'
			pos.sell_blocks.append(msg)

		pos.disp_sell_blocks()

		func_end(fnc)

	#<=====>#

	def sell_pos_forces(pos):
		func_name = 'sell_pos_forces'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		# sell_force_force_sell_db(pos):
		if pos.force_sell_tf == 1:
			pos.sell_yn = 'Y'
			pos.sell_force_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'force'
			pos.sell_strat_name  = 'forced sell'
			msg = f'db => position marked as force sell... poss.force_sell_tf : {pos.force_sell_tf}'
			pos.sell_forces.append(msg)

		# sell_force_force_sell_all(pos):
		if pos.mst.force_sell_all_yn == 'Y':
			pos.sell_yn = 'Y'
			pos.sell_force_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'force'
			pos.sell_strat_name  = 'forced sell'
			msg = f'settings => force_sell_all_yn = {pos.mst.force_sell_all_yn}'
			pos.sell_forces.append(msg)

		# sell_force_force_sell_prod_id(pos):
		if pos.prod_id in pos.mst.force_sell_prod_ids:
			pos.sell_yn = 'Y'
			pos.sell_force_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'force'
			pos.sell_strat_name  = 'forced sell'
			msg = f'settings => force_sell.prod_ids = {pos.prod_id}'
			pos.sell_forces.append(msg)

		# sell_force_force_sell_id(pos):
		if pos.pos_id in pos.mst.force_sell_pos_ids:
			pos.sell_yn = 'Y'
			pos.sell_force_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'force'
			pos.sell_strat_name  = 'forced sell'
			msg = f'settings => force_sell.pos_ids = {pos.pos_id}'
			pos.sell_forces.append(msg)

		pos.disp_sell_forces()

		func_end(fnc)

	#<=====>#

	def sell_tests_before_ta(pos):
		func_name = 'sell_tests_before_ta'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		# Take Profits
		if pos.prc_chg_pct > 0:
			if pos.sell_yn == 'N':
				if pos.mst.hard_take_profit_yn == 'Y':
					pos.sell_test_hard_profit()

			if pos.sell_yn == 'N':
				if pos.mst.trailing_profit_yn == 'Y':
					pos.sell_test_trailing_profit()

		# Stop Loss
		if pos.prc_chg_pct < 0:
			if pos.sell_yn == 'N':
				if pos.mst.hard_stop_loss_yn == 'Y':
					pos.sell_test_hard_stop()

			if pos.sell_yn == 'N':
				if pos.mst.trailing_stop_loss_yn == 'Y':
					pos.sell_test_trailing_stop()

			if pos.sell_yn == 'N':
				if pos.mst.atr_stop_loss_yn == 'Y':
					pos.sell_test_atr_stop()

			if pos.sell_yn == 'N':
				if pos.mst.trailing_atr_stop_loss_yn == 'Y':
					pos.sell_test_trailing_atr_stop()

		func_end(fnc)

	#<=====>#

	def sell_test_hard_profit(pos):
		func_name = 'sell_test_hard_profit'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Hard Take Profit Logic
		if pos.prc_chg_pct >= pos.mst.hard_take_profit_pct:
			pos.sell_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'profit'
			pos.sell_strat_name = 'hard_profit'
			msg = f'    * SELL COND: ...hard profit pct => curr : {pos.prc_chg_pct:>.2f}%, high : {pos.prc_chg_pct_high:>.2f}%, drop : {pos.prc_chg_pct_drop:>.2f}%, take_profit : {pos.mst.hard_take_profit_pct:>.2f}%, sell_yn : {pos.sell_yn}'
			all_sells.append(msg)
		else:
			msg = f'    * HODL COND: ...hard profit => curr : {pos.prc_chg_pct:>.2f}%, high : {pos.prc_chg_pct_high:>.2f}%, drop : {pos.prc_chg_pct_drop:>.2f}%, take_profit : {pos.mst.hard_take_profit_pct:>.2f}%, sell_yn : {pos.sell_yn}'
			all_hodls.append(msg)

		msg = f'    SELL TESTS - {pos.prod_id} - Hard Take Profit'
		pos.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_hard_stop(pos):
		func_name = 'sell_test_hard_stop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Hard Stop Loss Logic
		if pos.prc_chg_pct <= abs(pos.mst.hard_stop_loss_pct) * -1:
			pos.sell_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'stop_loss'
			pos.sell_strat_name = 'hard_stop_loss'
			msg = f'    * SELL COND: ...hard stop loss => curr : {pos.prc_chg_pct:>.2f}%, high : {pos.prc_chg_pct_high:>.2f}%, drop : {pos.prc_chg_pct_drop:>.2f}%, stop_loss : {pos.mst.hard_stop_loss_pct:>.2f}%, sell_yn : {pos.sell_yn}'
			all_sells.append(msg)
		else:
			pos.sell_yn = 'N'
			msg = f'    * HODL COND: ...hard stop loss => curr : {pos.prc_chg_pct:>.2f}%, high : {pos.prc_chg_pct_high:>.2f}%, drop : {pos.prc_chg_pct_drop:>.2f}%, stop_loss : {pos.mst.hard_stop_loss_pct:>.2f}%, sell_yn : {pos.sell_yn}'
			all_hodls.append(msg)

		pos.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_trailing_profit(pos):
		func_name = 'sell_test_trailing_profit'
		func_str  = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Trailing Profit Logic
		if pos.prc_chg_pct > 0.5:
			max_drop_pct = -5
			if pos.prc_chg_pct_high >= pos.mst.trailing_profit_trigger_pct:
				if pos.prc_chg_pct_high >= 34:
					max_drop_pct = -1 * pos.prc_chg_pct_high * .08
				elif pos.prc_chg_pct_high >= 21:
					max_drop_pct = -1 * pos.prc_chg_pct_high * .11
				elif pos.prc_chg_pct_high >= 13:
					max_drop_pct = -1 * pos.prc_chg_pct_high * .14
				elif pos.prc_chg_pct_high >= 5:
					max_drop_pct = -1 * pos.prc_chg_pct_high * .17
				elif pos.prc_chg_pct_high >= 3:
					max_drop_pct = -1 * pos.prc_chg_pct_high * .20
				elif pos.prc_chg_pct_high >= 2:
					max_drop_pct = -1 * pos.prc_chg_pct_high * .23
				elif pos.prc_chg_pct_high >= 1:
					max_drop_pct = -1 * pos.prc_chg_pct_high * .24

				max_drop_pct = round(max_drop_pct, 2)

				if pos.prc_chg_pct_drop <= max_drop_pct:
					pos.sell_yn = 'Y'
					pos.hodl_yn = 'N'
					pos.sell_strat_type = 'profit'
					pos.sell_strat_name = 'trail_profit'
					msg = f'    * SELL COND: ...trailing profit => curr : {pos.prc_chg_pct:>.2f}%, high : {pos.prc_chg_pct_high:>.2f}%, drop : {pos.prc_chg_pct_drop:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {pos.sell_yn}'
					all_sells.append(msg)
				else:
					msg = f'    * HODL COND: ...trailing profit => curr : {pos.prc_chg_pct:>.2f}%, high : {pos.prc_chg_pct_high:>.2f}%, drop : {pos.prc_chg_pct_drop:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {pos.sell_yn}'
					all_hodls.append(msg)

		msg = f'    SELL TESTS - {pos.prod_id} - Trailing Profit'
		pos.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_trailing_stop(pos):
		func_name = 'sell_test_trailing_stop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		stop_loss_pct = round(pos.prc_chg_pct_high - abs(pos.mst.trailing_stop_loss_pct), 2)
		if pos.prc_chg_pct < stop_loss_pct:
			pos.sell_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'stop_loss'
			pos.sell_strat_name = 'trail_stop'
			msg = f'    * SELL COND: ...trailing stop loss => curr : {pos.prc_chg_pct:>.2f}%, high : {pos.prc_chg_pct_high:>.2f}%, drop : {pos.prc_chg_pct_drop:>.2f}%, trigger : {pos.mst.trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {pos.sell_yn}'
			all_sells.append(msg)
		else:
			msg = f'    * HODL COND: ...trailing stop loss => curr : {pos.prc_chg_pct:>.2f}%, high : {pos.prc_chg_pct_high:>.2f}%, drop : {pos.prc_chg_pct_drop:>.2f}%, trigger : {pos.mst.trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {pos.sell_yn}'
			all_hodls.append(msg)

		msg = f'    SELL TESTS - {pos.prod_id} - Trailing Stop Loss'
		pos.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_atr_stop(pos):
		func_name = 'sell_test_atr_stop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Trailing Stop Loss Logic
		atr_rfreq        = pos.mst.sell.stop_loss.atr_stop_loss_rfreq
		atr              = pos.ta[atr_rfreq]['atr']['ago0']
		atr_stop_loss    = pos.prc_buy - atr

		if pos.sell_prc < atr_stop_loss:
			pos.sell_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'stop_loss'
			pos.sell_strat_name = 'atr_stop'
			msg = f'    * SELL COND: ...ATR stop loss => curr : {pos.sell_prc:>.8f}, atr : {atr:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {pos.sell_yn}'
			all_sells.append(msg)
		else:
			msg = f'    * HODL COND: ...ATR stop loss => curr : {pos.sell_prc:>.8f}, atr : {atr:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {pos.sell_yn}'
			all_hodls.append(msg)

		msg = f'    SELL TESTS - {pos.prod_id} - ATR Stop Loss'
		pos.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_trailing_atr_stop(pos):
		func_name = 'sell_test_trailing_atr_stop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Trailing Stop Loss Logic
		atr_rfreq         = pos.mst.sell.stop_loss.trailing_atr_stop_loss_rfreq
		atr_pct           = pos.mst.sell.stop_loss.trailing_atr_stop_loss_pct
		atr               = pos.ta[atr_rfreq]['atr']['ago0']
		atr_pct_mult      = atr_pct / 100
		atr_reduce        = atr * atr_pct_mult
		atr_stop_loss     = pos.prc_high - atr_reduce

		if pos.sell_prc < atr_stop_loss:
			pos.sell_yn = 'Y'
			pos.hodl_yn = 'N'
			pos.sell_strat_type = 'stop_loss'
			pos.sell_strat_name = 'trail_atr_stop'
			msg = f'    * SELL COND: ...ATR trailing stop loss => curr : {pos.sell_prc:>.8f}, atr : {atr:>.8f}, atr_pct : {atr_pct:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {pos.sell_yn}'
			all_hodls.append(msg)
		else:
			msg = f'    * HODL COND: ...ATR trailing stop loss => curr : {pos.sell_prc:>.8f}, atr : {atr:>.8f}, atr_pct : {atr_pct:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {pos.sell_yn}'
			all_sells.append(msg)

		msg = f'    SELL TESTS - {pos.prod_id} - Trailing ATR Stop Loss'
		pos.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_deny_all_green(pos):
		func_name = 'sell_deny_all_green'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells                 = []
		all_hodls                 = []
		rfreq                     = pos.buy_strat_freq
		freqs, faster_freqs       = freqs_get(rfreq)

		ha_color_5min  = pos.ta['5min']['ha_color']['ago0']
		ha_color_15min = pos.ta['15min']['ha_color']['ago0']
		ha_color_30min = pos.ta['30min']['ha_color']['ago0']
		ha_color_1h    = pos.ta['1h']['ha_color']['ago0']
		ha_color_4h    = pos.ta['4h']['ha_color']['ago0']
		ha_color_1d    = pos.ta['1d']['ha_color']['ago0']

		skip_checks = False
		if pos.mst.force_sell_all_yn == 'Y':
			skip_checks = True

		if pos.prod_id in pos.mst.force_sell_prod_ids:
			skip_checks = True

		if pos.pos_id in pos.mst.force_sell_pos_ids:
			skip_checks = True

		if not skip_checks:
			green_save = False

			if rfreq == '1d':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {pos.sell_block_yn}'
				if ha_color_4h == 'green':
					if (ha_color_30min == 'green' or ha_color_15min == 'green') and ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {pos.sell_block_yn}'
						green_save = True
			elif rfreq == '4h':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {pos.sell_block_yn}'
				if ha_color_1h == 'green':
					if ha_color_15min == 'green' and ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {pos.sell_block_yn}'
						green_save = True
			elif rfreq == '1h':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {pos.sell_block_yn}'
				if ha_color_30min == 'green':
					if ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {pos.sell_block_yn}'
						green_save = True
			elif rfreq == '30min':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {pos.sell_block_yn}'
				if ha_color_15min == 'green':
					if ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {pos.sell_block_yn}'
						green_save = True
			elif rfreq == '15min':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {pos.sell_block_yn}'
				if ha_color_5min == 'green':
					if ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {pos.sell_block_yn}'
						green_save = True

			if green_save:
				pos.sell_block_yn = 'Y'
				all_hodls.append(pass_msg)
			else:
				msg = f'    * CANCEL SELL: ALL CANDLES NOT GREEN ==> Allowing Sell...   5min : {ha_color_5min}, 15min : {ha_color_15min}, 30min : {ha_color_30min}, sell_block_yn : {pos.sell_block_yn}'
				all_sells.append(fail_msg)

		print(f'{func_name} - sell_block_yn : {pos.sell_block_yn}, show_tests_yn : {pos.mst.show_tests_yn}')
		if pos.sell_block_yn == 'Y' or pos.mst.show_tests_yn in ('Y','F'):
			msg = f'    SELL TESTS - {pos.prod_id} - All Green Candes...'
			WoG(msg)
			if pos.sell_block_yn == 'Y' or pos.mst.show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					pos.pair.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					pos.pair.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def sell_header(pos):
		func_name = 'sell_header'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		hmsg = ""
		hmsg += f"{'pair':^12} | "
		hmsg += f"{'T':^1} | "
		hmsg += f"{'pos_id':^6} | "
		hmsg += f"{'buy_strat':^12} | "
		hmsg += f"{'freq':^5} | "
		hmsg += f"{'age':^10} | "
		hmsg += f"{'buy_val':^16} | "
		hmsg += f"{'curr_val':^14} | "
		hmsg += f"{'buy_prc':^14} | "
		hmsg += f"{'curr_prc':^14} | "
		hmsg += f"{'high_prc':^14} | "
		hmsg += f"{'prc_pct':^8} % | "
		hmsg += f"{'prc_top':^8} % | "
		hmsg += f"{'prc_low':^8} % | "
		hmsg += f"{'prc_drop':^8} % | "
		hmsg += f"$ {'net_est':^14} | "
		hmsg += f"$ {'net_est_high':^14}"

		title_msg = f'* SELL LOGIC * {pos.prod_id} *'
		chart_mid(in_str=title_msg, len_cnt=240, bold=True)
		chart_headers(in_str=hmsg, len_cnt=240, bold=True)

		pos.pair.show_sell_header_tf = False

		func_end(fnc)

	#<=====>#

	def disp_sell(pos):
		func_name = 'disp_sell'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if pos.pair.show_sell_header_tf:
			pos.sell_header()
			pos.pair.show_sell_header_tf = False

		disp_age = format_disp_age(pos.age_mins)

		if pos.test_tf == 1:
			test_tf = 'T'
		else:
			test_tf = ''

		msg = ''
		msg += f'{pos.prod_id:<12}' + ' | '
		msg += f'{test_tf:^1}' + ' | '
		msg += f'{pos.pos_id:^6}' + ' | '
		msg += f'{pos.buy_strat_name:^12}' + ' | '
		msg += f'{pos.buy_strat_freq:^5}' + ' | '
		msg += f'{disp_age:^10}' + ' | '
		msg += f'{pos.tot_out_cnt:>16.8f}' + ' | '
		msg += f'{pos.val_curr:>14.8f}' + ' | '
		msg += f'{pos.prc_buy:>14.8f}' + ' | '
		msg += f'{pos.prc_curr:>14.8f}' + ' | '
		msg += f'{pos.prc_high:>14.8f}' + ' | '
		msg += f'{pos.prc_chg_pct:>8.2f} %' + ' | '
		msg += f'{pos.prc_chg_pct_high:>8.2f} %' + ' | '
		msg += f'{pos.prc_chg_pct_low:>8.2f} %' + ' | '
		msg += f'{pos.prc_chg_pct_drop:>8.2f} %' + ' | '
		msg += f'$ {pos.gain_loss_amt:>14.8f}' + ' | '
		msg += f'$ {pos.gain_loss_amt_est_high:>14.8f}'

		msg = cs_pct_color(pos.prc_chg_pct, msg)
		chart_row(msg, len_cnt=240)

		func_end(fnc)

	#<=====>#

	def disp_sell_blocks(pos):
		func_name = 'disp_sell_blocks'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		pos.mst.show_blocks_yn                   = pos.mst.sell.show_blocks_yn

		if pos.mst.show_blocks_yn == 'Y':
			for b in pos.sell_blocks:
				if pos.prc_chg_pct > 0:
					b = '    ' + cs('* SELL BLOCK *', font_color='white', bg_color='green') + ' ' + cs(b, font_color='green')
					chart_row(b, len_cnt=240)
				else:
					b = '    ' + cs('* SELL BLOCK *', font_color='white', bg_color='red')  + ' ' + cs(b, font_color='red')
					chart_row(b, len_cnt=240)
				pos.pair.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def disp_sell_forces(pos):
		func_name = 'disp_sell_forces'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if pos.mst.show_forces_yn == 'Y':
			for f in pos.sell_forces:
				if pos.prc_chg_pct > 0:
					f = '    ' + cs('* SELL FORCE *', font_color='white', bg_color='green')  + ' ' + cs(f, font_color='green')
					chart_row(f, len_cnt=240)
				else:
					f = '    ' + cs('* SELL FORCE *', font_color='white', bg_color='red')  + ' ' + cs(f, font_color='red')
					chart_row(f, len_cnt=240)
				pos.pair.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def disp_sell_tests(pos):
		func_name = 'disp_sell_tests'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if pos.mst.show_tests_yn == 'Y':
			for t in pos.sell_tests:
				if pos.prc_chg_pct > 0:
					t = '    ' + cs('* SELL TEST *', font_color='white', bg_color='green')  + ' ' + cs(t, font_color='green')
					chart_row(t, len_cnt=240)
				else:
					t = '    ' + cs('* SELL TEST *', font_color='white', bg_color='red')  + ' ' + cs(t, font_color='red')
					chart_row(t, len_cnt=240)
				pos.pair.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def disp_sell_test_details(pos, msg, all_sells, all_hodls):
		func_name = 'disp_sell_test_details'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pos.mst.show_tests_yn in ('Y','F'):
			msg = '    ' + cs('==> ' + msg + f' * sell => {pos.sell_yn} * sell_block => {pos.sell_block_yn} * hodl => {pos.hodl_yn}', font_color='white', bg_color='blue')
			chart_row(msg, len_cnt=240)
			if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pos.mst.show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						e = '    ' + cs('* ' + e, font_color='green')
						chart_row(e, len_cnt=240)
					else:
						e = '    ' + cs('* ' + e, font_color='red')
						chart_row(e, len_cnt=240)
					pos.pair.show_sell_header_tf = True
				for e in all_hodls:
					e = '    ' + cs('* ' + e, font_color='green', bg_color='white')
					chart_row(e, len_cnt=240)
					pos.pair.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def sell_save(pos):
		func_name = 'sell_save'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		if pos.sell_yn == 'Y':
			if pos.mst.save_files_yn == 'Y':
				fname = f"saves/{pos.prod_id}_SELL_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt"
				writeit(fname, '=== MKT ===')
				for k in pos.pair:
					writeit(fname, f'{k} : {pos.pair[k]}'.format(k, pos.pair[k]))
				writeit(fname, '')
				writeit(fname, '')
				writeit(fname, '=== POS ===')
				for k in pos:
					if isinstance(pos[k], [str, list, dict, float, int, decimal.Decimal, datetime, time]):
						writeit(fname, f'{k} : {pos[k]}')
					else:
						print(f'{k} : {type(pos[k])}')

		func_end(fnc)

	#<=====>#

	def sell_live(pos):
		func_name = 'sell_live'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		sell_data = db_sell_double_check(pos.pos_id)
		if sell_data and sell_data['pos_stat'] != 'OPEN':
			print('another bot must have changed the position status since we started!!! SKIPPING SELL!!!')
			beep(3)
		elif sell_data and sell_data['so_id'] is not None:
			print('another bot must have changed the position status since we started!!! SKIPPING SELL!!!')
			beep(3)
		else:
			db_tbl_poss_insupd(pos)
			if pos.mst.sell_limit_yn == 'N' and pos.pair.mkt_limit_only_tf == 1:
				print(f'{pos.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')
				pos.ord_mkt_sell_orig()
			elif pos.mst.sell_limit_yn == 'Y':
				try:
					pos.ord_lmt_sell_open() 
				except Exception as e:
					print(f'{func_name} ==> sell limit order failed, attempting market... {e}')
					beep(3)
					pos.ord_mkt_sell_orig()
			else:
				pos.ord_mkt_sell_orig()

			# Update to Database
			db_tbl_poss_insupd(pos)

		func_end(fnc)

	#<=====>#

	def sell_test(pos):
		func_name = 'sell_test'
		func_str = f'{lib_name}.{func_name}(pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		so = AttrDict()
		so.test_tf                     = pos.test_tf
		so.symb                        = pos.symb
		so.prod_id                     = pos.prod_id
		so.mkt_name                    = pos.mkt_name
		so.pos_id                      = pos.pos_id
		so.sell_seq_nbr                = 1
		so.sell_order_uuid             = pos.gen_guid()	
		so.pos_type                    = 'SPOT'
		so.ord_stat                    = 'OPEN'
		so.sell_strat_type             = pos.sell_strat_type
		so.sell_strat_name             = pos.sell_strat_name
		so.sell_strat_freq             = pos.sell_strat_freq
		so.sell_begin_dttm             = dt.now()	
		so.sell_end_dttm               = dt.now()	
		so.sell_curr_symb              = pos.sell_curr_symb
		so.recv_curr_symb              = pos.recv_curr_symb	
		so.fees_curr_symb              = pos.fees_curr_symb
		so.sell_cnt_est                = pos.hold_cnt
		so.sell_cnt_act                = pos.hold_cnt
		so.fees_cnt_act                = (pos.hold_cnt * pos.prc_sell) * 0.004
		so.tot_in_cnt                  = (pos.hold_cnt * pos.prc_sell) * 0.996
		so.prc_sell_est                = pos.prc_sell
		so.prc_sell_act                = pos.prc_sell
		so.tot_prc_buy                 = pos.prc_sell
		so.prc_sell_slip_pct           = 0

		db_tbl_sell_ords_insupd(so)
		time.sleep(.33)

		func_end(fnc)

#<=====>#

	def cb_sell_base_size_calc(pos, init_sell_cnt):
		func_name = 'cb_sell_base_size_calc'
		func_str = ''
		func_str += f'{lib_name}.{func_name}('
		func_str += f'sell_cnt={init_sell_cnt:>.8f}, '
		func_str += ')'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		sell_cnt_max     = dec(init_sell_cnt)

		pos.pocket_pct            = pos.mkt_settings.get_ovrd(in_dict=pos.mst.sell.rainy_day.pocket_pct, in_key=pos.prod_id)
		pos.clip_pct              = pos.mkt_settings.get_ovrd(in_dict=pos.mst.sell.rainy_day.clip_pct, in_key=pos.prod_id)
		pos.sell_prc              = pos.pair.prc_sell

		if sell_cnt_max > dec(pos.hold_cnt):
			print(f'...selling more {sell_cnt_max:>.8f} than we are position is holding {pos.hold_cnt:>.8f} onto...exiting...')
			beep(3)
			func_end(fnc)
			return 0

		if sell_cnt_max > dec(pos.bal_cnt):
			print(f'...selling more {sell_cnt_max:>.8f} than we the wallet balance {pos.bal_cnt:>.8f}...exiting...')
			beep(3)
			func_end(fnc)
			return 0

		if pos.prc_chg_pct > 0 and pos.pocket_pct > 0:
			sell_cnt_max -= sell_cnt_max * (dec(pos.pocket_pct) / 100) * (dec(pos.prc_chg_pct)/100)

		if pos.prc_chg_pct < 0 and pos.clip_pct > 0:
			sell_cnt_max -= sell_cnt_max * (dec(pos.clip_pct) / 100) * (abs(dec(pos.prc_chg_pct))/100)

		sell_blocks = int(sell_cnt_max / dec(pos.pair.base_size_incr))
		sell_cnt_max = sell_blocks * dec(pos.pair.base_size_incr)

		if sell_cnt_max < dec(pos.pair.base_size_min):
			print(f'...selling less {sell_cnt_max:>.8f} than coinbase allows {pos.pair.base_size_min}...exiting...')
			beep(3)
			func_end(fnc)
			return 0

		if sell_cnt_max > dec(pos.pair.base_size_max):
			sell_cnt_max = dec(pos.pair.base_size_max)

		pos.sell_cnt = sell_cnt_max

		func_end(fnc)

	#<=====>#

	def ord_mkt_sell(pos):
		func_name = 'ord_mkt_sell'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id               = pos.prod_id
		init_sell_cnt         = pos.hold_cnt

		end_time              = dt.now() + timedelta(minutes=5)
		end_time              = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

		pos.cb_sell_base_size_calc(init_sell_cnt)

		if pos.sell_cnt == 0:
			func_end(fnc)
			pos.symb = 'USDC'
			pos.pos_stat = 'ERR'
			pos.ignore_tf = 1
			pos.error_tf = 1
			pos.sell_yn = 'N'
			pos.reason = f'there are not enough {pos.buy_curr_symb} to complete this sale...'
			db_tbl_poss_insupd(pos)
		else:

			recv_amt = round(float(pos.sell_cnt) * float(pos.sell_prc),2)

			print(f'{func_name} => order = cb.fiat_market_sell(prod_id={prod_id}, recv_amt={recv_amt})')
			order = cb.fiat_market_sell(prod_id, recv_amt)
			pos.refresh_wallet_tf       = True
			time.sleep(0.33)

			ord_id = order.id
			o = cb_ord_get(order_id=ord_id)
			time.sleep(0.33)

			so = None
			if o:
				so = AttrDict()
				so.pos_id                = pos.pos_id
				so.symb                  = pos.symb
				so.prod_id               = pos.pair.prod_id
				so.pos_type              = 'SPOT'
				so.ord_stat              = 'OPEN'
				so.sell_order_uuid       = ord_id
				so.sell_begin_dttm       = dt.now()
				so.sell_strat_type       = pos.sell_strat_type
				so.sell_strat_name       = pos.sell_strat_name
				so.sell_curr_symb        = pos.pair.base_curr_symb
				so.recv_curr_symb        = pos.pair.quote_curr_symb
				so.fees_curr_symb        = pos.pair.quote_curr_symb
				so.sell_cnt_est          = pos.sell_cnt
				so.prc_sell_est          = pos.pair.prc_sell
				db_tbl_sell_ords_insupd(so)
				time.sleep(.33)
				db_poss_stat_upd(pos_id=pos.pos_id, pos_stat='SELL')
				pos.pos_stat = 'SELL'
			else:
				print(f'{func_name} exit 1 : {o}')
				print(f'{func_name} exit 1 : {so}')
				sys.exit()

		func_end(fnc)

	#<=====>#

	def ord_mkt_sell_orig(pos):
		func_name = 'ord_mkt_sell_orig'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		client_order_id       = cb_client_order_id()
		prod_id               = pos.prod_id
		init_sell_cnt         = pos.hold_cnt

		pos.cb_sell_base_size_calc(init_sell_cnt)

		if pos.sell_cnt == 0:
			func_end(fnc)
			pos.symb = 'USDC'
			pos.pos_stat = 'ERR'
			pos.ignore_tf = 1
			pos.error_tf = 1
			pos.sell_yn = 'N'
			pos.reason = f'there are not enough {pos.buy_curr_symb} to complete this sale...'
			db_tbl_poss_insupd(pos)
		else:
			oc = {}
			oc['market_market_ioc'] = {}
			oc['market_market_ioc']['base_size'] = f'{pos.sell_cnt:>.8f}'

			o = cb.create_order(
					client_order_id = client_order_id, 
					product_id = prod_id, 
					side = 'SELL', 
					order_configuration = oc
					)
			print(o)
			pos.refresh_wallet_tf       = True
			time.sleep(0.25)

			so = None
			if o:
				if 'success' in o:
					if o['success']:
						so = AttrDict()
						so.pos_id                = pos.pos_id
						so.symb                  = pos.symb
						so.prod_id               = pos.pair.prod_id
						so.pos_type              = 'SPOT'
						so.ord_stat              = 'OPEN'
						so.sell_order_uuid       = o['success_response']['order_id']
						so.sell_client_order_id  = o['success_response']['client_order_id']
						so.sell_begin_dttm       = dt.now()
						so.sell_strat_type       = pos.sell_strat_type
						so.sell_strat_name       = pos.sell_strat_name
						so.sell_curr_symb        = pos.pair.base_curr_symb
						so.recv_curr_symb        = pos.pair.quote_curr_symb
						so.fees_curr_symb        = pos.pair.quote_curr_symb
						so.sell_cnt_est          = pos.sell_cnt
						so.prc_sell_est          = pos.pair.prc_sell
						db_tbl_sell_ords_insupd(so)
						time.sleep(.25)
						db_poss_stat_upd(pos_id=pos.pos_id, pos_stat='SELL')
						pos.pos_stat = 'SELL'
					else:
						print(f'{func_name} exit 3 : {o}')
						pprint(o)
						print(f'{func_name} exit 3 : {so}')
						beep(3)
						print('exit on line 3451')
						sys.exit()
				else:
					print(f'{func_name} exit 2 : {o}')
					print(f'{func_name} exit 2 : {so}')
					beep(3)
					print('exit on line 3458')
					sys.exit()
			else:
				print(f'{func_name} exit 1 : {o}')
				print(f'{func_name} exit 1 : {so}')
				beep(3)
				print('exit on line 3465')
				sys.exit()

		func_end(fnc)

	#<=====>#

	def ord_lmt_sell_open(pos):
		func_name = 'ord_lmt_sell_open'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id               = pos.prod_id
		init_sell_cnt         = pos.hold_cnt

		end_time              = dt.now() + timedelta(minutes=5)
		end_time              = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

		pos.cb_sell_base_size_calc(init_sell_cnt)

		if pos.sell_cnt == 0:
			func_end(fnc)
			pos.symb = 'USDC'
			pos.pos_stat = 'ERR'
			pos.ignore_tf = 1
			pos.error_tf = 1
			pos.sell_yn = 'N'
			pos.reason = f'there are not enough {pos.buy_curr_symb} to complete this sale...'
			db_tbl_poss_insupd(pos)
		else:

			recv_amt = round(float(pos.sell_cnt) * float(pos.sell_prc),2)

			prc_mult = str(1)
			if pos.prc_chg_pct > 0:
				prc_mult = "1.005"
				order = cb.fiat_limit_sell(prod_id, recv_amt, price_multiplier=prc_mult)
			else:
				order = cb.fiat_limit_sell(prod_id, recv_amt)
			pos.refresh_wallet_tf       = True
			time.sleep(0.25)

			ord_id = order.id
			o = cb_ord_get(order_id=ord_id)
			time.sleep(0.25)

			so = None
			if o:
				so = AttrDict()
				so.pos_id                = pos.pos_id
				so.symb                  = pos.symb
				so.prod_id               = pos.pair.prod_id
				so.pos_type              = 'SPOT'
				so.ord_stat              = 'OPEN'
				so.sell_order_uuid       = ord_id # o['success_response']['order_id']
				so.sell_begin_dttm       = dt.now()
				so.sell_strat_type       = pos.sell_strat_type
				so.sell_strat_name       = pos.sell_strat_name
				so.sell_curr_symb        = pos.pair.base_curr_symb
				so.recv_curr_symb        = pos.pair.quote_curr_symb
				so.fees_curr_symb        = pos.pair.quote_curr_symb
				so.sell_cnt_est          = pos.sell_cnt
				so.prc_sell_est          = pos.pair.prc_sell
				db_tbl_sell_ords_insupd(so)
				time.sleep(.25)
				db_poss_stat_upd(pos_id=pos.pos_id, pos_stat='SELL')
				pos.pos_stat = 'SELL'
			else:
				print(f'{func_name} exit 1 : {o}')
				print(f'{func_name} exit 1 : {so}')
				sys.exit()

		func_end(fnc)

#<=====>#
# Functions
#<=====>#



#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
