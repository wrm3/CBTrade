#<=====>#
# Import All Scope
#<=====>#

import_all_func_list =  []
import_all_func_list.append("sell_logic")
import_all_func_list.append("sell_pos_logic")
import_all_func_list.append("sell_pos_blocks")
import_all_func_list.append("sell_logic_forced")
import_all_func_list.append("sell_logic_hard_profit")
import_all_func_list.append("sell_logic_hard_stop")
import_all_func_list.append("sell_logic_trailing_profit")
import_all_func_list.append("sell_logic_trailing_stop")
import_all_func_list.append("sell_logic_atr_stop")
import_all_func_list.append("sell_logic_trailing_atr_stop")
import_all_func_list.append("sell_logic_deny_all_green")
import_all_func_list.append("sell_header")
import_all_func_list.append("disp_sell")
import_all_func_list.append("disp_sell_tests")
import_all_func_list.append("sell_log")
import_all_func_list.append("sell_sign_rec")
import_all_func_list.append("ord_mkt_sell")
import_all_func_list.append("ord_mkt_sell_orig")
import_all_func_list.append("ord_lmt_sell_open")
import_all_func_list.append("sell_ords_check")
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
from datetime import datetime as dt
from datetime import timedelta
from pprint import pprint
import os
import pandas as pd 
import sys
import time
import traceback
import warnings
import uuid
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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from main import MyClass

from lib_charts                   import *
from lib_common                   import *
from lib_colors                   import *
from lib_strings                  import *

from bot_common                   import *
from bot_coinbase                 import *
from bot_db_read                  import *
from bot_db_write                 import *
from bot_logs                     import *
from bot_secrets                  import secrets
from bot_settings                 import settings
from bot_strats                   import *
from bot_ta                       import *
from bot_theme                    import *

# from report                            import report_buys_recent
# from report                            import report_open
# from report                            import report_open_by_age
# from report                            import report_open_by_prod_id
# from report                            import report_sells_recent

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_cls_sell'
log_name      = 'bot_cls_sell'
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




def sell_logic(self, mkt, ta, open_poss):
	func_name = 'sell_logic'
	func_str = f'{lib_name}.{func_name}(mkt, ta, open_poss)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=6)
	# G(func_str)

	prod_id = mkt.prod_id
	st = settings.settings_load()

	self.sell_header(prod_id)
	show_sell_header_tf = False

	if not open_poss:
		print(f'{prod_id} has no open positions...')
		func_end(fnc)
		return mkt

	db_poss_check_mkt_dttm_upd(prod_id)
	mkt.check_mkt_dttm = db_poss_check_mkt_dttm_get(prod_id)

	for pos in open_poss:
		pos = dec_2_float(pos)
		pos = AttrDictConv(in_dict=pos)
		pos.age_mins = pos.new_age_mins
		del pos['new_age_mins']
		pos_id = pos.pos_id

		try:
			pos = self.sell_pos_logic(mkt, ta, pos)
			if pos.sell_yn == 'Y' and pos.sell_block_yn == 'N':
				self.show_sell_header_tf = True

		except Exception as e:
			print(f'{dttm_get()} {func_name} {prod_id} {pos_id}==> errored : ({type(e)}) {e}')
			traceback.print_exc()
			pass

	chart_mid(len_cnt=240, bold=True)

	func_end(fnc)
	return mkt

#<=====>#

def sell_pos_logic(self, mkt, ta, pos):
	func_name = 'sell_pos_logic'
	func_str = f'{lib_name}.{func_name}(mkt, ta, pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1)
	# G(func_str)

	pos                       = self.pos_upd(pos=pos, mkt=mkt)
	pos.sell_strat_type       = ''
	pos.sell_strat_name       = ''
	prod_id                   = mkt.prod_id
	pos_id                    = pos.pos_id
	sell_yn                   = 'N'
	sell_block_yn             = 'N'
	hodl_yn                   = 'Y'
	sell_signals              = []

	self.disp_sell(pos)
	db_poss_check_last_dttm_upd(pos_id)
	pos.check_last_dttm = db_poss_check_last_dttm_get(pos_id)

	# Logic that will block the sell from happening
	sell_block_yn = self.sell_pos_blocks(mkt, pos)

	# Sell By Strat Logic
	if sell_yn == 'N' and ta:
		mkt, pos, sell_yn, hodl_yn, sell_signals, self.show_sell_header_tf = sell_strats_check(self.st, mkt, ta, pos, sell_yn, hodl_yn, sell_signals, self.show_sell_header_tf, sell_block_yn)

	# Forced Sell Logic
	if sell_yn == 'N':
		mkt, pos, sell_yn, hodl_yn, sell_block_yn = self.sell_logic_forced(mkt, pos, sell_yn, hodl_yn, sell_block_yn)
		sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
		sell_signals.append(sell_signal)

	# Take Profits
	if pos.prc_chg_pct > 0:
		if sell_yn == 'N':
			if self.st.spot.sell.take_profit.hard_take_profit_yn == 'Y':
				mkt, pos, sell_yn, hodl_yn = self.sell_logic_hard_profit(mkt, pos, sell_block_yn)
				sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
				sell_signals.append(sell_signal)

		if sell_yn == 'N':
			if self.st.spot.sell.take_profit.trailing_profit_yn == 'Y':
				mkt, pos, sell_yn, hodl_yn = self.sell_logic_trailing_profit(mkt, pos, sell_block_yn)
				sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
				sell_signals.append(sell_signal)

	# Stop Loss
	if pos.prc_chg_pct < 0:
		if sell_yn == 'N':
			if self.st.spot.sell.stop_loss.hard_stop_loss_yn == 'Y':
				mkt, pos, sell_yn, hodl_yn = self.sell_logic_hard_stop(mkt, pos, sell_block_yn)
				sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
				sell_signals.append(sell_signal)

		if sell_yn == 'N':
			if self.st.spot.sell.stop_loss.trailing_stop_loss_yn == 'Y':
				mkt, pos, sell_yn, hodl_yn = self.sell_logic_trailing_stop(mkt, pos, sell_block_yn)
				sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
				sell_signals.append(sell_signal)

		if sell_yn == 'N':
			if self.st.spot.sell.stop_loss.atr_stop_loss_yn == 'Y':
				mkt, pos, sell_yn, hodl_yn = self.sell_logic_atr_stop(mkt, ta, pos, sell_block_yn)
				sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
				sell_signals.append(sell_signal)

		if sell_yn == 'N':
			if self.st.spot.sell.stop_loss.trailing_atr_stop_loss_yn == 'Y':
				mkt, pos, sell_yn, hodl_yn = self.sell_logic_trailing_atr_stop(mkt, ta, pos, sell_block_yn)
				sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
				sell_signals.append(sell_signal)

	if sell_yn == 'Y' and sell_block_yn == 'N' and ta:
		sell_block_yn = self.sell_logic_deny_all_green(mkt, ta, pos)

	# Forced Sell Logic
	# Second calling so a forced sell still overwrites a forced don't sell
	if sell_yn == 'N' or (sell_yn == 'Y' and sell_block_yn == 'Y'):
		mkt, pos, sell_yn, hodl_yn, sell_block_yn = self.sell_logic_forced(mkt, pos, sell_yn, hodl_yn, sell_block_yn)

		sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
		sell_signals.append(sell_signal)

	if sell_yn == 'Y' and sell_block_yn == 'Y':
		hodl_yn = 'Y'
	elif sell_yn == 'Y' and sell_block_yn == 'N':
		hodl_yn = 'N'

	db_tbl_poss_insupd(pos)

	if sell_yn == 'Y' and sell_block_yn == 'N':
		if pos.test_tf == 0:
			pos = self.sell_live(mkt, pos)
			if pos.gain_loss_amt > 0:
				symb = prod_id.split(',')[0]
				msg = f'WIN, selling {symb} for ${round(pos.gain_loss_amt_est,2)} '
				if self.st.speak_yn == 'Y': speak_async(msg)
				if pos.gain_loss_amt >= 1:
					play_cash()
			elif pos.gain_loss_amt < 0:
				symb = prod_id.split(',')[0]
				msg = f'LOSS, selling {symb} for ${round(pos.gain_loss_amt_est,2)} '
				if self.st.speak_yn == 'Y': speak_async(msg)
				if pos.gain_loss_amt <= -1:
					play_thunder()
		elif pos.test_tf == 1:
			pos = self.sell_test(mkt, pos)

	if sell_yn == 'Y':
		if self.st.spot.sell.save_files_yn == 'Y':
			fname = f"saves/{prod_id}_SELL_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt"
			writeit(fname, '=== MKT ===')
			for k in mkt:
				writeit(fname, f'{k} : {mkt[k]}'.format(k, mkt[k]))
			writeit(fname, '')
			writeit(fname, '')
			writeit(fname, '=== POS ===')
			for k in pos:
				writeit(fname, f'{k} : {pos[k]}')

	pos.sell_yn = sell_yn
	pos.sell_block_yn = sell_block_yn
	pos.hodl_yn = hodl_yn

	func_end(fnc)
	return pos

#<=====>#

def sell_pos_blocks(self, mkt, pos):
	func_name = 'sell_pos_blocks'
	func_str = f'{lib_name}.{func_name}(mkt, pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1)
	# G(func_str)

	prod_id     = pos.prod_id
	pos_id      = pos.pos_id

	sell_block_yn = 'N'

	if self.st.spot.sell.selling_on_yn == 'N':
		sell_block_yn = 'Y'
		msg = f'    * SELL BLOCK * selling_on_yn : {sell_block_yn} - self.st.spot.sell.selling_on_yn == N'
		if self.st.spot.sell.show_tests_yn in ('Y','F'):
			BoW(msg)

	if self.st.spot.sell.never_sell_all_yn == 'Y':
		sell_block_yn = 'Y'
		msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - self.st.spot.sell.never_sell_all_yn == Y'
		if self.st.spot.sell.show_tests_yn in ('Y','F'):
			BoW(msg)

	if self.st.spot.sell.never_sell_loss_all_yn == 'Y' and pos.prc_chg_pct < 0:
		sell_block_yn = 'Y'
		msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - self.st.spot.sell.never_sell_loss_all_yn == Y and pos.prc_chg_pct < 0'
		if self.st.spot.sell.show_tests_yn in ('Y','F'):
			BoW(msg)

	if prod_id in self.st.spot.sell.never_sell.prod_ids:
		sell_block_yn = 'Y'
		msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} - in self.st.spot.sell.never_sell.prod_ids'
		if self.st.spot.sell.show_tests_yn in ('Y','F'):
			BoW(msg)

	if prod_id in self.st.spot.sell.never_sell_loss.prod_ids and pos.prc_chg_pct < 0:
		sell_block_yn = 'Y'
		msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} - in self.st.spot.sell.never_sell_loss.prod_ids and pos.prc_chg_pct < 0'
		if self.st.spot.sell.show_tests_yn in ('Y','F'):
			BoW(msg)

	if pos_id in self.st.spot.sell.never_sell.pos_ids:
		sell_block_yn = 'Y'
		msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} {pos.pos_id} - pos_id in self.st.spot.sell.never_sell.pos_ids'
		if self.st.spot.sell.show_tests_yn in ('Y','F'):
			BoW(msg)

	if pos_id in self.st.spot.sell.never_sell_loss.pos_ids and pos.prc_chg_pct < 0:
		sell_block_yn = 'Y'
		msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} {pos.pos_id} - pos_id in self.st.spot.sell.never_sell_loss.pos_ids and pos.prc_chg_pct < 0'
		if self.st.spot.sell.show_tests_yn in ('Y','F'):
			BoW(msg)

	# Market Price Range Looks Very Suspect
	if mkt.prc_range_pct >= 5:
		sell_block_yn = 'Y'
		msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} - has a price range variance of {mkt.prc_range_pct}, this price range looks sus... skipping sell'
		BoW(msg)
		beep(3)

	func_end(fnc)
	return sell_block_yn

#<=====>#

def sell_logic_forced(self, mkt, pos, sell_yn='N', hodl_yn='N', sell_block_yn='N'):
	func_name = 'sell_logic_forced'
	func_str = f'{lib_name}.{func_name}(mkt, pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id     = mkt.prod_id
	pos_id      = pos.pos_id
	all_sells   = []
	all_hodls   = []
	sell_yn     = 'N'
	hodl_yn     = 'Y'
	show_tests_yn         = self.st.spot.sell.show_tests_yn

	force_sell_all_yn     = self.st.spot.sell.force_sell_all_yn
	# from db table

	if pos.force_sell_tf == 1:
		sell_yn = 'Y'
		sell_block_yn = 'N'
		msg = f'    * SELL COND: position marked as force sell..., sell_yn : {sell_yn}'
		all_sells.append(msg)
	elif self.st.spot.sell.force_sell_all_yn == 'Y':
		sell_yn = 'Y'
		sell_block_yn = 'N'
		msg = f'    * SELL COND: force_sell_all_yn = {force_sell_all_yn} in settings..., sell_yn : {sell_yn}'
		all_sells.append(msg)
	elif prod_id in self.st.spot.sell.force_sell.prod_ids:
		sell_yn = 'Y'
		sell_block_yn = 'N'
		msg = f'    * SELL COND: {prod_id} is in force_sell_prods in settings..., sell_yn : {sell_yn}'
		all_sells.append(msg)
	elif pos_id in self.st.spot.sell.force_sell.pos_ids:
		sell_yn = 'Y'
		sell_block_yn = 'N'
		msg = f'    * SELL COND: position {pos_id} is in force_sell_poss in settings..., sell_yn : {sell_yn}'
		all_sells.append(msg)

	if sell_yn == 'Y':
		hodl_yn = 'N'
		pos.sell_strat_type = 'force'
		pos.sell_strat_name  = 'forced sell'
	else:
		hodl_yn = 'Y'

	msg = f'    SELL TESTS - {prod_id} - {pos_id}- Forced Sell'
	self.disp_sell_tests(msg, pos, all_sells, all_hodls, sell_yn, sell_block_yn, hodl_yn, show_tests_yn)

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn, sell_block_yn

#<=====>#

def sell_logic_hard_profit(self, mkt, pos, sell_block_yn='N'):
	func_name = 'sell_logic_hard_profit'
	func_str = f'{lib_name}.{func_name}(mkt, pos, sell_block_yn={sell_block_yn})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id     = mkt.prod_id
	all_sells   = []
	all_hodls   = []
	sell_yn     = 'N'
	hodl_yn     = 'Y'
	show_tests_yn         = self.st.spot.sell.show_tests_yn

	# Hard Take Profit Logic
	prc_chg_pct           = pos.prc_chg_pct
	prc_chg_pct_high      = pos.prc_chg_pct_high
	prc_chg_pct_drop      = pos.prc_chg_pct_drop
	take_profit_pct       = self.st.spot.sell.take_profit.hard_take_profit_pct
	if prc_chg_pct >= take_profit_pct:
		sell_yn = 'Y'
		msg = f'    * SELL COND: ...hard profit pct => curr : {prc_chg_pct:>.2f}%, high : {prc_chg_pct_high:>.2f}%, drop : {prc_chg_pct_drop:>.2f}%, take_profit : {take_profit_pct:>.2f}%, sell_yn : {sell_yn}'
		all_sells.append(msg)
	else:
		sell_yn = 'N'
		msg = f'    * HODL COND: ...hard profit => curr : {prc_chg_pct:>.2f}%, high : {prc_chg_pct_high:>.2f}%, drop : {prc_chg_pct_drop:>.2f}%, take_profit : {take_profit_pct:>.2f}%, sell_yn : {sell_yn}'
		all_hodls.append(msg)

	if sell_yn == 'Y':
		hodl_yn = 'N'
		pos.sell_strat_type = 'profit'
		pos.sell_strat_name = 'hard_profit'
	else:
		hodl_yn = 'Y'

	msg = f'    SELL TESTS - {prod_id} - Hard Take Profit'
	self.disp_sell_tests(msg, pos, all_sells, all_hodls, sell_yn, sell_block_yn, hodl_yn, show_tests_yn)

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_logic_hard_stop(self, mkt, pos, sell_block_yn='N'):
	func_name = 'sell_logic_hard_stop'
	func_str = f'{lib_name}.{func_name}(mkt, pos, sell_block_yn={sell_block_yn})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id     = mkt.prod_id
	all_sells   = []
	all_hodls   = []
	sell_yn     = 'N'
	hodl_yn     = 'Y'
	show_tests_yn         = self.st.spot.sell.show_tests_yn

	# Hard Stop Loss Logic
	prc_chg_pct           = pos.prc_chg_pct
	prc_chg_pct_high      = pos.prc_chg_pct_high
	prc_chg_pct_drop      = pos.prc_chg_pct_drop
	hard_stop_loss_pct    = abs(self.st.spot.sell.stop_loss.hard_stop_loss_pct) * -1
	if pos.prc_chg_pct <= hard_stop_loss_pct:
		sell_yn = 'Y'
		msg = f'    * SELL COND: ...hard stop loss => curr : {prc_chg_pct:>.2f}%, high : {prc_chg_pct_high:>.2f}%, drop : {prc_chg_pct_drop:>.2f}%, stop_loss : {hard_stop_loss_pct:>.2f}%, sell_yn : {sell_yn}'
		all_sells.append(msg)
	else:
		sell_yn = 'N'
		msg = f'    * HODL COND: ...hard stop loss => curr : {prc_chg_pct:>.2f}%, high : {prc_chg_pct_high:>.2f}%, drop : {prc_chg_pct_drop:>.2f}%, stop_loss : {hard_stop_loss_pct:>.2f}%, sell_yn : {sell_yn}'
		all_hodls.append(msg)

	if sell_yn == 'Y':
		hodl_yn = 'N'
		pos.sell_strat_type = 'stop_loss'
		pos.sell_strat_name = 'hard_stop_loss'
	else:
		hodl_yn = 'Y'

	self.disp_sell_tests(msg, pos, all_sells, all_hodls, sell_yn, sell_block_yn, hodl_yn, show_tests_yn)

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_logic_trailing_profit(self, mkt, pos, sell_block_yn='N'):
	func_name = 'sell_logic_trailing_profit'
	func_str  = f'{lib_name}.{func_name}(mkt, pos, sell_block_yn={sell_block_yn})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id     = mkt.prod_id
	all_sells   = []
	all_hodls   = []
	sell_yn     = 'N'
	hodl_yn     = 'Y'
	show_tests_yn         = self.st.spot.sell.show_tests_yn

	# Trailing Profit Logic
	trailing_profit_trigger_pct = self.st.spot.sell.take_profit.trailing_profit_trigger_pct
	prc_chg_pct                 = pos.prc_chg_pct
	prc_chg_pct_high            = pos.prc_chg_pct_high
	prc_chg_pct_drop            = pos.prc_chg_pct_drop

	if prc_chg_pct > 0.5:
		max_drop_pct = -5
		if prc_chg_pct_high >= trailing_profit_trigger_pct:
			if prc_chg_pct_high >= 34:
				max_drop_pct = -1 * prc_chg_pct_high * .08
			elif prc_chg_pct_high >= 21:
				max_drop_pct = -1 * prc_chg_pct_high * .11
			elif prc_chg_pct_high >= 13:
				max_drop_pct = -1 * prc_chg_pct_high * .14
			elif prc_chg_pct_high >= 5:
				max_drop_pct = -1 * prc_chg_pct_high * .17
			elif prc_chg_pct_high >= 3:
				max_drop_pct = -1 * prc_chg_pct_high * .20
			elif prc_chg_pct_high >= 2:
				max_drop_pct = -1 * prc_chg_pct_high * .23
			elif prc_chg_pct_high >= 1:
				max_drop_pct = -1 * prc_chg_pct_high * .24

			max_drop_pct = round(max_drop_pct, 2)

			if prc_chg_pct_drop <= max_drop_pct:
				sell_yn = 'Y'
				msg = f'    * SELL COND: ...trailing profit => curr : {prc_chg_pct:>.2f}%, high : {prc_chg_pct_high:>.2f}%, drop : {prc_chg_pct_drop:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {sell_yn}'
				all_sells.append(msg)
			else:
				sell_yn = 'N'
				msg = f'    * HODL COND: ...trailing profit => curr : {prc_chg_pct:>.2f}%, high : {prc_chg_pct_high:>.2f}%, drop : {prc_chg_pct_drop:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {sell_yn}'
				all_hodls.append(msg)

	if sell_yn == 'Y':
		hodl_yn = 'N'
		pos.sell_strat_type = 'profit'
		pos.sell_strat_name = 'trail_profit'
	else:
		hodl_yn = 'Y'

	msg = f'    SELL TESTS - {prod_id} - Trailing Profit'
	self.disp_sell_tests(msg, pos, all_sells, all_hodls, sell_yn, sell_block_yn, hodl_yn, show_tests_yn)

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_logic_trailing_stop(self, mkt, pos, sell_block_yn='N'):
	func_name = 'sell_logic_trailing_stop'
	func_str = f'{lib_name}.{func_name}(mkt, pos, sell_block_yn={sell_block_yn})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id     = mkt.prod_id
	all_sells   = []
	all_hodls   = []
	sell_yn     = 'N'
	hodl_yn     = 'Y'
	show_tests_yn         = self.st.spot.sell.show_tests_yn

	# Trailing Stop Loss Logic
	trailing_stop_loss_pct     = abs(self.st.spot.sell.stop_loss.trailing_stop_loss_pct)
	prc_chg_pct                = pos.prc_chg_pct
	prc_chg_pct_high           = pos.prc_chg_pct_high
	prc_chg_pct_drop           = pos.prc_chg_pct_drop

	if sell_yn == 'N':
		stop_loss_pct = round(prc_chg_pct_high - trailing_stop_loss_pct, 2)
		if pos.prc_chg_pct < stop_loss_pct:
			sell_yn = 'Y'
			msg = f'    * SELL COND: ...trailing stop loss => curr : {prc_chg_pct:>.2f}%, high : {prc_chg_pct_high:>.2f}%, drop : {prc_chg_pct_drop:>.2f}%, trigger : {trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {sell_yn}'
			all_sells.append(msg)
		else:
			sell_yn     = 'N'
			msg = f'    * HODL COND: ...trailing stop loss => curr : {prc_chg_pct:>.2f}%, high : {prc_chg_pct_high:>.2f}%, drop : {prc_chg_pct_drop:>.2f}%, trigger : {trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {sell_yn}'
			all_hodls.append(msg)

	if sell_yn == 'Y':
		hodl_yn = 'N'
		pos.sell_strat_type = 'stop_loss'
		pos.sell_strat_name = 'trail_stop'
	else:
		hodl_yn = 'Y'

	msg = '    SELL TESTS - {prod_id} - Trailing Stop Loss'
	self.disp_sell_tests(msg, pos, all_sells, all_hodls, sell_yn, sell_block_yn, hodl_yn, show_tests_yn)

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_logic_atr_stop(self, mkt, ta, pos, sell_block_yn='N'):
	func_name = 'sell_logic_atr_stop'
	func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id     = mkt.prod_id
	sell_prc    = mkt.prc_sell
	all_sells   = []
	all_hodls   = []
	sell_yn     = 'N'
	hodl_yn     = 'Y'
	show_tests_yn         = self.st.spot.sell.show_tests_yn

	# Trailing Stop Loss Logic
	atr_rfreq        = self.st.spot.sell.stop_loss.atr_stop_loss_rfreq
	atr              = ta[atr_rfreq]['atr']['ago0']
	atr_stop_loss    = pos.prc_buy - atr

	if sell_prc < atr_stop_loss:
		sell_yn = 'Y'
		msg = f'    * SELL COND: ...ATR stop loss => curr : {sell_prc:>.8f}, atr : {atr:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {sell_yn}'
		all_sells.append(msg)
	else:
		sell_yn = 'N'
		msg = f'    * HODL COND: ...ATR stop loss => curr : {sell_prc:>.8f}, atr : {atr:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {sell_yn}'
		all_hodls.append(msg)

	if sell_yn == 'Y':
		hodl_yn = 'N'
		pos.sell_strat_type = 'stop_loss'
		pos.sell_strat_name = 'atr_stop'
	else:
		hodl_yn = 'Y'

	msg = f'    SELL TESTS - {prod_id} - ATR Stop Loss'
	self.disp_sell_tests(msg, pos, all_sells, all_hodls, sell_yn, sell_block_yn, hodl_yn, show_tests_yn)

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_logic_trailing_atr_stop(self, mkt, ta, pos, sell_block_yn='N'):
	func_name = 'sell_logic_trailing_atr_stop'
	func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id     = mkt.prod_id
	sell_prc    = mkt.prc_sell
	all_sells   = []
	all_hodls   = []
	sell_yn     = 'N'
	hodl_yn     = 'Y'
	show_tests_yn         = self.st.spot.sell.show_tests_yn

	# Trailing Stop Loss Logic
	if sell_yn == 'N':
		atr_rfreq         = self.st.spot.sell.stop_loss.trailing_atr_stop_loss_rfreq
		atr_pct           = self.st.spot.sell.stop_loss.trailing_atr_stop_loss_pct
		atr               = ta[atr_rfreq]['atr']['ago0']
		atr_pct_mult      = atr_pct / 100
		atr_reduce        = atr * atr_pct_mult
		atr_stop_loss     = pos.prc_high - atr_reduce

		if sell_prc < atr_stop_loss:
			sell_yn = 'Y'
			msg = f'    * SELL COND: ...ATR trailing stop loss => curr : {sell_prc:>.8f}, atr : {atr:>.8f}, atr_pct : {atr_pct:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {sell_yn}'
			all_hodls.append(msg)
		else:
			sell_yn = 'N'
			msg = f'    * HODL COND: ...ATR trailing stop loss => curr : {sell_prc:>.8f}, atr : {atr:>.8f}, atr_pct : {atr_pct:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {sell_yn}'
			all_sells.append(msg)

	if sell_yn == 'Y':
		hodl_yn = 'N'
		pos.sell_strat_type = 'stop_loss'
		pos.sell_strat_name = 'trail_atr_stop'
	else:
		hodl_yn = 'Y'

	msg = f'    SELL TESTS - {prod_id} - Trailing ATR Stop Loss'
	self.disp_sell_tests(msg, pos, all_sells, all_hodls, sell_yn, sell_block_yn, hodl_yn, show_tests_yn)

	func_end(fnc)
	return mkt, pos, sell_yn, hodl_yn

#<=====>#

def sell_logic_deny_all_green(self, mkt, ta, pos, sell_block_yn='N'):
	func_name = 'sell_logic_deny_all_green'
	func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id                   = mkt.prod_id
	all_sells                 = []
	all_hodls                 = []
	sell_block_yn             = 'N'
	show_tests_yn             = self.st.spot.sell.show_tests_yn
	rfreq                     = pos.buy_strat_freq
	freqs, faster_freqs       = freqs_get(rfreq)

	ha_color_5min  = ta['5min']['ha_color']['ago0']
	ha_color_15min = ta['15min']['ha_color']['ago0']
	ha_color_30min = ta['30min']['ha_color']['ago0']
	ha_color_1h    = ta['1h']['ha_color']['ago0']
	ha_color_4h    = ta['4h']['ha_color']['ago0']
	ha_color_1d    = ta['1d']['ha_color']['ago0']

	skip_checks = False
	if self.st.spot.sell.force_sell_all_yn == 'Y':
		skip_checks = True

	if pos.prod_id in self.st.spot.sell.force_sell.prod_ids:
		skip_checks = True

	if pos.pos_id in self.st.spot.sell.force_sell.pos_ids:
		skip_checks = True

	if not skip_checks:
		green_save = False

		if rfreq == '1d':
			fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {sell_block_yn}'
			if ha_color_4h == 'green':
				if (ha_color_30min == 'green' or ha_color_15min == 'green') and ha_color_5min == 'green':
					pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {sell_block_yn}'
					green_save = True
		elif rfreq == '4h':
			fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {sell_block_yn}'
			if ha_color_1h == 'green':
				if ha_color_15min == 'green' and ha_color_5min == 'green':
					pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {sell_block_yn}'
					green_save = True
		elif rfreq == '1h':
			fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {sell_block_yn}'
			if ha_color_30min == 'green':
				if ha_color_5min == 'green':
					pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {sell_block_yn}'
					green_save = True
		elif rfreq == '30min':
			fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {sell_block_yn}'
			if ha_color_15min == 'green':
				if ha_color_5min == 'green':
					pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {sell_block_yn}'
					green_save = True
		elif rfreq == '15min':
			fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {sell_block_yn}'
			if ha_color_5min == 'green':
				if ha_color_5min == 'green':
					pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {sell_block_yn}'
					green_save = True


		if green_save:
			sell_block_yn = 'N'
			all_hodls.append(pass_msg)
		else:
			msg = f'    * CANCEL SELL: ALL CANDLES NOT GREEN ==> Allowing Sell...   5min : {ha_color_5min}, 15min : {ha_color_15min}, 30min : {ha_color_30min}, sell_block_yn : {sell_block_yn}'
			all_sells.append(fail_msg)

	print(f'{func_name} - sell_block_yn : {sell_block_yn}, show_tests_yn : {show_tests_yn}')
	if sell_block_yn == 'Y' or show_tests_yn in ('Y','F'):
		msg = f'    SELL TESTS - {prod_id} - All Green Candes...'
		WoG(msg)
		if sell_block_yn == 'Y' or show_tests_yn in ('Y'):
			for e in all_sells:
				if pos.prc_chg_pct > 0:
					G(e)
				else:
					R(e)
				self.show_sell_header_tf = True
			for e in all_hodls:
				WoG(e)
				self.show_sell_header_tf = True

	func_end(fnc)
	return sell_block_yn

#<=====>#

def sell_header(self, prod_id):
	func_name = 'sell_header'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	hmsg = ""
	hmsg += f"{'mkt':^12} | "
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

	title_msg = f'* SELL LOGIC * {prod_id} *'
	chart_mid(in_str=title_msg, len_cnt=240, bold=True)
	chart_headers(in_str=hmsg, len_cnt=240, bold=True)

	self.show_sell_header_tf = False

	func_end(fnc)

#<=====>#

def disp_sell(self, pos):
	func_name = 'disp_sell'
	func_str = f'{lib_name}.{func_name}(pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id = pos.prod_id

	if self.show_sell_header_tf:
		self.sell_header(prod_id)
		self.show_sell_header_tf = False

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

def disp_sell_tests(self, msg, pos, all_sells, all_hodls, sell_yn, sell_block_yn, hodl_yn, show_tests_yn):
	func_name = 'disp_sell_tests'
	func_str = f'{lib_name}.{func_name}(pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id = pos.prod_id

	if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
		msg = '    ' + cs('==> ' + msg + f' * sell => {sell_yn} * sell_block => {sell_block_yn} * hodl => {hodl_yn}', font_color='white', bg_color='blue')
		chart_row(msg, len_cnt=240)
		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y'):
			for e in all_sells:
				if pos.prc_chg_pct > 0:
					e = '    ' + cs('* ' + e, font_color='green')
					chart_row(e, len_cnt=240)
				else:
					e = '    ' + cs('* ' + e, font_color='red')
					chart_row(e, len_cnt=240)
				self.show_sell_header_tf = True
			for e in all_hodls:
				e = '    ' + cs('* ' + e, font_color='green', bg_color='white')
				chart_row(e, len_cnt=240)
				self.show_sell_header_tf = True
			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

	func_end(fnc)

#<=====>#

def sell_log(self, msg):
	func_name = 'sell_log'
	func_str = f'{lib_name}.{func_name}(msg)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	dt_str  = dt.now().strftime('%Y_%m_%d')
	logfile = f"logs_sell/{dt_str}_sell_log.txt"
	wmsg    = f'{dttm_get()} ==> {msg}'
	file_write(logfile, wmsg)

	func_end(fnc)

#<=====>#

def sell_sign_rec(self, pos):
	func_name = 'sell_sign_rec'
	func_str = f'{lib_name}.{func_name}(pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	ss = {}
	ss = {}
	ss["test_tf"]              = pos.test_tf
	ss["prod_id"]              = pos.prod_id
	ss["pos_id"]               = pos.pos_id
	ss["sell_strat_type"]      = pos.sell_strat_type
	ss["sell_strat_name"]      = pos.sell_strat_name
	ss["sell_strat_freq"]      = pos.sell_strat_freq
	ss["buy_yn"]               = pos.buy_yn
	ss["wait_yn"]              = pos.wait_yn
	ss["sell_curr_symb"]       = pos.sell_curr_symb
	ss["recv_curr_symb"]       = pos.recv_curr_symb
	ss["fees_curr_symb"]       = pos.fees_curr_symb
	ss["sell_cnt_est"]         = pos.sell_cnt_est
	ss["sell_prc_est"]         = pos.sell_prc_est
	ss["sell_sub_tot_est"]     = pos.sell_sub_tot_est
	ss["sell_fees_est"]        = pos.sell_fees_est
	ss["sell_tot_est"]         = pos.sell_tot_est

	# Update to Database
	db_tbl_sell_signs_insupd(ss)

	func_end(fnc)

#<=====>#

def ord_mkt_sell(self, mkt, pos):
	func_name = 'ord_mkt_sell'
	func_str = f'{lib_name}.{func_name}(mkt, pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id               = pos.prod_id
	sell_cnt              = pos.hold_cnt
	base_size_incr        = mkt.base_size_incr
	base_size_min         = mkt.base_size_min
	base_size_max         = mkt.base_size_max
	bal_cnt               = cb_bal_get(mkt.base_curr_symb)
	hold_cnt              = pos.hold_cnt
	pocket_pct            = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.pocket_pct, in_key=prod_id)
	clip_pct              = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.clip_pct, in_key=prod_id)
	sell_prc              = mkt.prc_sell
	prc_chg_pct           = pos.prc_chg_pct

	end_time              = dt.now() + timedelta(minutes=5)
	end_time              = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

	sell_cnt              = cb_sell_base_size_calc(sell_cnt, prc_chg_pct, base_size_incr, base_size_min, base_size_max, bal_cnt, hold_cnt, pocket_pct, clip_pct)
	pos.sell_cnt          = sell_cnt

	if sell_cnt == 0:
		func_end(fnc)
		return pos

	recv_amt = round(float(sell_cnt) * float(sell_prc),2)

	print(f'{func_name} => order = cb.fiat_market_sell(prod_id={prod_id}, recv_amt={recv_amt})')
	order = cb.fiat_market_sell(prod_id, recv_amt)
	self.refresh_wallet_tf       = True
	time.sleep(0.33)

	ord_id = order.id
	o = cb_ord_get(order_id=ord_id)
	time.sleep(0.33)

	so = None
	if o:
		so = AttrDict()
		so.pos_id                = pos.pos_id
		so.prod_id               = mkt.prod_id
		so.pos_type              = 'SPOT'
		so.ord_stat              = 'OPEN'
		so.sell_order_uuid       = ord_id
		so.sell_begin_dttm       = dt.now()
		so.sell_strat_type       = pos.sell_strat_type
		so.sell_strat_name       = pos.sell_strat_name
		so.sell_curr_symb        = mkt.base_curr_symb
		so.recv_curr_symb        = mkt.quote_curr_symb
		so.fees_curr_symb        = mkt.quote_curr_symb
		so.sell_cnt_est          = sell_cnt
		so.prc_sell_est          = mkt.prc_sell
		db_tbl_sell_ords_insupd(so)
		time.sleep(.33)
		db_poss_stat_upd(pos_id=pos.pos_id, pos_stat='SELL')
	else:
		print(f'{func_name} exit 1 : {o}')
		print(f'{func_name} exit 1 : {so}')
		sys.exit()

	func_end(fnc)
	return pos

#<=====>#

def ord_mkt_sell_orig(self, mkt, pos):
	func_name = 'ord_mkt_sell_orig'
	func_str = f'{lib_name}.{func_name}(mkt, pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	client_order_id       = cb_client_order_id()
	prod_id               = pos.prod_id
	sell_cnt              = pos.hold_cnt
	base_size_incr        = mkt.base_size_incr
	base_size_min         = mkt.base_size_min
	base_size_max         = mkt.base_size_max
	bal_cnt               = cb_bal_get(mkt.base_curr_symb)
	hold_cnt              = pos.hold_cnt
	pocket_pct            = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.pocket_pct, in_key=prod_id)
	clip_pct              = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.clip_pct, in_key=prod_id)
	prc_chg_pct           = pos.prc_chg_pct

	sell_cnt = cb_sell_base_size_calc(sell_cnt, prc_chg_pct, base_size_incr, base_size_min, base_size_max, bal_cnt, hold_cnt, pocket_pct, clip_pct)

	if sell_cnt == 0:
		func_end(fnc)
		return pos

	oc = {}
	oc['market_market_ioc'] = {}
	oc['market_market_ioc']['base_size'] = f'{sell_cnt:>.8f}'

	o = cb.create_order(
			client_order_id = client_order_id, 
			product_id = prod_id, 
			side = 'SELL', 
			order_configuration = oc
			)
	print(o)
	self.refresh_wallet_tf       = True
	time.sleep(0.25)

	so = None
	if o:
		if 'success' in o:
			if o['success']:
				so = AttrDict()
				so.pos_id                = pos.pos_id
				so.prod_id               = mkt.prod_id
				so.pos_type              = 'SPOT'
				so.ord_stat              = 'OPEN'
				so.sell_order_uuid       = o['success_response']['order_id']
				so.sell_client_order_id  = o['success_response']['client_order_id']
				so.sell_begin_dttm       = dt.now()
				so.sell_strat_type       = pos.sell_strat_type
				so.sell_strat_name       = pos.sell_strat_name
				so.sell_curr_symb        = mkt.base_curr_symb
				so.recv_curr_symb        = mkt.quote_curr_symb
				so.fees_curr_symb        = mkt.quote_curr_symb
				so.sell_cnt_est          = sell_cnt
				so.prc_sell_est          = mkt.prc_sell
				db_tbl_sell_ords_insupd(so)
				time.sleep(.25)
				db_poss_stat_upd(pos_id=pos.pos_id, pos_stat='SELL')
			else:
				print(f'{func_name} exit 3 : {o}')
				pprint(o)
				print(f'{func_name} exit 3 : {so}')
				play_beep(reps=3)
				print('exit on line 3451')
				sys.exit()
		else:
			print(f'{func_name} exit 2 : {o}')
			print(f'{func_name} exit 2 : {so}')
			play_beep(reps=3)
			print('exit on line 3458')
			sys.exit()
	else:
		print(f'{func_name} exit 1 : {o}')
		print(f'{func_name} exit 1 : {so}')
		play_beep(reps=3)
		print('exit on line 3465')
		sys.exit()

	func_end(fnc)
	return pos

#<=====>#

def ord_lmt_sell_open(self, mkt, pos):
	func_name = 'ord_lmt_sell_open'
	func_str = f'{lib_name}.{func_name}(mkt, pos)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id               = pos.prod_id
	sell_cnt              = pos.hold_cnt
	base_size_incr        = mkt.base_size_incr
	base_size_min         = mkt.base_size_min
	base_size_max         = mkt.base_size_max
	bal_cnt               = cb_bal_get(mkt.base_curr_symb)
	hold_cnt              = pos.hold_cnt
	pocket_pct            = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.pocket_pct, in_key=prod_id)
	clip_pct              = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.clip_pct, in_key=prod_id)
	sell_prc              = mkt.prc_sell
	prc_chg_pct           = pos.prc_chg_pct

	end_time              = dt.now() + timedelta(minutes=5)
	end_time              = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

	sell_cnt              = cb_sell_base_size_calc(sell_cnt, prc_chg_pct, base_size_incr, base_size_min, base_size_max, bal_cnt, hold_cnt, pocket_pct, clip_pct)
	pos.sell_cnt          = sell_cnt

	if sell_cnt == 0:
		func_end(fnc)
		return pos

	recv_amt = round(float(sell_cnt) * float(sell_prc),2)

	prc_mult = str(1)
	if prc_chg_pct > 0:
		prc_mult = "1.005"
		order = cb.fiat_limit_sell(prod_id, recv_amt, price_multiplier=prc_mult)
	else:
		order = cb.fiat_limit_sell(prod_id, recv_amt)
	self.refresh_wallet_tf       = True
	time.sleep(0.25)

	ord_id = order.id
	o = cb_ord_get(order_id=ord_id)
	time.sleep(0.25)

	so = None
	if o:
		so = AttrDict()
		so.pos_id                = pos.pos_id
		so.prod_id               = mkt.prod_id
		so.pos_type              = 'SPOT'
		so.ord_stat              = 'OPEN'
		so.sell_order_uuid       = ord_id # o['success_response']['order_id']
		so.sell_begin_dttm       = dt.now()
		so.sell_strat_type       = pos.sell_strat_type
		so.sell_strat_name       = pos.sell_strat_name
		so.sell_curr_symb        = mkt.base_curr_symb
		so.recv_curr_symb        = mkt.quote_curr_symb
		so.fees_curr_symb        = mkt.quote_curr_symb
		so.sell_cnt_est          = sell_cnt
		so.prc_sell_est          = mkt.prc_sell
		db_tbl_sell_ords_insupd(so)
		time.sleep(.25)
		db_poss_stat_upd(pos_id=pos.pos_id, pos_stat='SELL')
	else:
		print(f'{func_name} exit 1 : {o}')
		print(f'{func_name} exit 1 : {so}')
		sys.exit()

	func_end(fnc)
	return pos

#<=====>#

def sell_ords_check(self):
	func_name = 'sell_ords_check'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	try:
		cnt = 0
		sos = db_sell_ords_open_get()
		if sos:
			print_adv(2)
			WoM(f"{'Sell Orders Check':^200}")

			sos_cnt = len(sos)
			for so in sos:
				cnt += 1
				so = dec_2_float(so)
				so = AttrDictConv(in_dict=so)

				test_tf = so.test_tf
				ord_id = so.sell_order_uuid

				if test_tf == 0:
					try:
						o = cb_ord_get(order_id=ord_id)
					except Exception as e:
						print(f'{func_name} ==> errored... {type(e)} {e}')
						traceback.print_exc()
						traceback.print_stack()
						print(f'so : {so}')
						beep()
						continue

					if o:
						o = dec_2_float(o)
						o = AttrDictConv(in_dict=o)
						if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
							so.sell_cnt_act                    = o.ord_filled_size
							so.fees_cnt_act                    = o.ord_total_fees
							so.tot_in_cnt                      = o.ord_total_value_after_fees
							so.prc_sell_act                    = o.ord_average_filled_price # not sure this includes the fees
							so.sell_end_dttm                   = o.ord_last_fill_time
							so.tot_prc_buy                     = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
							if o.ord_settled:
								so.ord_stat                    = 'FILL'
							so.prc_sell_slip_pct              = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 8)
							print(f'{cnt:^4} / {sos_cnt:^4}, prod_id : {so.prod_id:<16}, pos_id : {so.pos_id:>7}, so_id : {so.so_id:>7}, so_uuid : {so.sell_order_uuid:<60}')
							db_tbl_sell_ords_insupd(so)
							self.pos_close(so.pos_id, so.sell_order_uuid)
						elif o.ord_status == 'OPEN':
							print(o)
							print('WE NEED CODE HERE!!!')
							if o.ord_filled_size > 0:
								so.sell_cnt_act                    = o.ord_filled_size
								so.fees_cnt_act                    = o.ord_total_fees
								so.tot_in_cnt                      = o.ord_total_value_after_fees
								so.prc_sell_act                    = o.ord_average_filled_price # not sure this includes the fees
								so.sell_end_dttm                   = o.ord_last_fill_time
								so.tot_prc_buy                     = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
								so.prc_sell_slip_pct               = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 8)
								print(f'{cnt:^4} / {sos_cnt:^4}, prod_id : {so.prod_id:<16}, pos_id : {so.pos_id:>7}, so_id : {so.so_id:>7}, so_uuid : {so.sell_order_uuid:<60}')
								db_tbl_sell_ords_insupd(so)
	# this needs to be added when we add in support for limit orders
	#						else:
	#							r = cb_ord_cancel_orders(order_ids=[ord_id])
	#							db_sell_ords_stat_upd(so_id=so.so_id, ord_stat='CANC')
	#							db_poss_err_upd(pos_id=so.pos_id, pos_stat='OPEN')
						else:
							beep(3)
							pprint(o)
							db_sell_ords_stat_upd(so_id=so.so_id, ord_stat='ERR')
							db_poss_err_upd(pos_id=so.pos_id, pos_stat='OPEN')

				elif test_tf == 1:
					so.ord_stat = 'FILL'
					db_tbl_sell_ords_insupd(so)
					self.pos_close(so.pos_id, so.sell_order_uuid)

			print_adv(2)

	except Exception as e:
		print(f'{func_name} ==> errored... {type(e)} {e}')
		traceback.print_exc()
		traceback.print_stack()
		print(f'so : {so}')
		print(f'ord_id : {ord_id}')
		print(f'o : {o}')
		sys.exit()

	func_end(fnc)

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#



#<=====>#
