#<=====>#
# Import All Scope
#<=====>#

import_all_func_list =  []
import_all_func_list.append("POS")
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
from lib_dicts                    import * 

from bot_common                   import *
from bot_coinbase                 import *
from bot_db_read                  import *
from bot_db_write                 import *
from bot_logs                     import *
from bot_secrets                  import secrets
from bot_settings                 import settings
from bot_strats_sell              import *
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
lib_secs_max  = 2

#<=====>#
# Assignments Pre
#<=====>#

#<=====>#
# Classes
#<=====>#

class POS(AttrDict):

	def __init__(self, mkt, pos, ta):
		self.mkt                       = mkt
#		pprint(pos)
		for k, v in pos.items():
			self[k] = v
#		pprint(self)
		self.age_mins = self.new_age_mins
#		del pos['new_age_mins']
#		sys.exit()
#		print(f'age_mins : {self.age_mins}')
		self.st                   = settings.settings_load()
		self.sell_yn              = 'N'
		self.sell_block_yn        = 'N'
		self.hodl_yn              = 'N'
		self.ta                   = ta
		self.symb                 = self.prod_id.split(',')[0]
		self.sell_prc             = mkt.prc_sell

		self.sell_yn              = 'N'
		self.hodl_yn              = 'Y'
		self.sell_block_yn        = 'N'
		self.sell_force_yn        = 'N'

		self.sell_blocks          = []
		self.sell_forces          = []
		self.sell_tests           = []
		self.sell_test_sells      = []
		self.sell_test_hodls      = []

		self.sell_signals         = []

		self.sell_strat_type      = ''
		self.sell_strat_name      = ''

	#<=====>#

	def sell_settings(self):
		func_name = 'sell_settings'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1)
		# G(func_str)

		# "selling_on_yn": "Y",
		# "force_all_tests_yn": "Y",
		# "show_tests_yn": "N",
		# "show_tests_min": 101,
		# "save_files_yn": "N",
		# "sell_limit_yn": "N",
		self.st.selling_on_yn                    = self.st.spot.sell.selling_on_yn
		self.st.force_all_tests_yn               = self.st.spot.sell.force_all_tests_yn

		self.st.show_blocks_yn                   = self.st.spot.sell.show_blocks_yn
		self.st.show_forces_yn                   = self.st.spot.sell.show_forces_yn

		self.st.show_tests_yn                    = self.st.spot.sell.show_tests_yn
		self.st.show_tests_min                   = self.st.spot.sell.show_tests_min
		self.st.save_files_yn                    = self.st.spot.sell.save_files_yn
		self.st.sell_limit_yn                    = self.st.spot.sell.sell_limit_yn

		# "take_profit": {
		# 	"hard_take_profit_yn": "Y",
		# 	"hard_take_profit_pct": 100,
		# 	"trailing_profit_yn": "Y",
		# 	"trailing_profit_trigger_pct": 3
		# },
		self.st.hard_take_profit_yn              = self.st.spot.sell.take_profit.hard_take_profit_yn
		self.st.hard_take_profit_pct             = self.st.spot.sell.take_profit.hard_take_profit_pct
		self.st.trailing_profit_yn               = self.st.spot.sell.take_profit.trailing_profit_yn
		self.st.trailing_profit_trigger_pct      = self.st.spot.sell.take_profit.trailing_profit_trigger_pct

		# "stop_loss": {
		# 	"hard_stop_loss_yn": "Y",
		# 	"hard_stop_loss_pct": 10,
		# 	"trailing_stop_loss_yn": "Y",
		# 	"trailing_stop_loss_pct": 10,
		# 	"atr_stop_loss_yn": "N",
		# 	"atr_stop_loss_rfreq": "1d",
		# 	"trailing_atr_stop_loss_yn": "N",
		# 	"trailing_atr_stop_loss_pct": 70,
		# 	"trailing_atr_stop_loss_rfreq": "1d"
		# },
		self.st.hard_stop_loss_yn                = self.st.spot.sell.stop_loss.hard_stop_loss_yn
		self.st.hard_stop_loss_pct               = self.st.spot.sell.stop_loss.hard_stop_loss_pct

		self.st.trailing_stop_loss_yn            = self.st.spot.sell.stop_loss.trailing_stop_loss_yn
		self.st.trailing_stop_loss_pct           = self.st.spot.sell.stop_loss.trailing_stop_loss_pct

		self.st.atr_stop_loss_yn                 = self.st.spot.sell.stop_loss.atr_stop_loss_yn
		self.st.atr_stop_loss_rfeq               = self.st.spot.sell.stop_loss.atr_stop_loss_rfreq

		self.st.trailing_atr_stop_loss_yn        = self.st.spot.sell.stop_loss.trailing_atr_stop_loss_yn
		self.st.trailing_atr_stop_loss_pct       = self.st.spot.sell.stop_loss.trailing_atr_stop_loss_pct
		self.st.trailing_atr_stop_loss_rfreq     = self.st.spot.sell.stop_loss.trailing_atr_stop_loss_rfreq

		# "force_sell_all_yn": "N",
		# "force_sell": {
		# 	"prod_ids": [
		# 		"CBETH-USDC",
		# 		"LSETH-USDC",
		# 		"MSOL-USDC",
		# 		"WAMPL-USDC",
		# 		"WAXL-USDC",
		# 		"WBTC-USDC",
		# 		"WCFG-USDC",
		# 		"MATIC-USDC"
		# 	],
		# 	"pos_ids": []
		# },
		self.st.force_sell_all_yn                = self.st.spot.sell.force_sell_all_yn
		self.st.force_sell_prod_ids              = self.st.spot.sell.force_sell.prod_ids
		self.st.force_sell_pos_ids               = self.st.spot.sell.force_sell.pos_ids

		# "never_sell_all_yn": "N",
		# "never_sell": {
		# 	"prod_ids": [],
		# 	"pos_ids": []
		# },
		self.st.never_sell_all_yn                = self.st.spot.sell.never_sell_all_yn
		self.st.never_sell_prod_ids              = self.st.spot.sell.never_sell.prod_ids
		self.st.never_sell_pos_ids               = self.st.spot.sell.never_sell.pos_ids

		# "never_sell_loss_all_yn": "N",
		# "never_sell_loss": {
		# 	"prod_ids": [],
		# 	"pos_ids": []
		# },
		self.st.never_sell_loss_all_yn           = self.st.spot.sell.never_sell_loss_all_yn
		self.st.never_sell_loss_prod_ids         = self.st.spot.sell.never_sell_loss.prod_ids
		self.st.never_sell_loss_pos_ids          = self.st.spot.sell.never_sell_loss.pos_ids

		func_end(fnc)


	#<=====>#

	def sell_pos_logic(self):
		func_name = 'sell_pos_logic'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1)
		# G(func_str)

		# Settings
		self.sell_settings()

		self.bal_cnt = cb_bal_get(self.mkt.base_curr_symb)
		if self.bal_cnt == 0:
			self.bal_cnt = cb_bal_get(self.symb)
		if self.bal_cnt == 0:
			print(f'{lib_name}.{func_name} => {self.prod_id} balance is {self.bal_cnt}...')
			beep(3)
			sys.exit()

		self.disp_sell()
		db_poss_check_last_dttm_upd(self.pos_id)
		self.check_last_dttm = db_poss_check_last_dttm_get(self.pos_id)

		# Halt And Catch Fire
		sos = db_sell_ords_get_by_pos_id(self.pos_id)
		if sos:
			print(f'{lib_name}.{func_name} => Halt & Catch Fire...')
			del self['ta']
			del self['mkt']
			del self['st']
			print(self)
			print('')
			for so in sos:
				print(so)
				print('')
			beep(10)
			sys.exit()

		# Forced Sell Logic
		if self.sell_yn == 'N':
			self.sell_pos_forces()

		# Logic that will block the sell from happening
		if self.sell_force_yn == 'N':
			self.sell_pos_blocks()

		# Sells Tests that don't require TA
		if self.sell_yn == 'N':
			self.sell_tests_before_ta()

		if self.sell_yn == 'N':
			if not self.ta:
				t0 = time.perf_counter()
				try:
					print(f'{func_name} - getting ta for {self.prod_id} for the first time this loop...')
					self.ta = mkt_ta_main_new(self.mkt, self.st)
					if not self.ta:
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
#						beep(3)
					elif self.ta == 'Error!':
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {self.prod_id} - close prices do not match')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {self.prod_id} - close prices do not match')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {self.prod_id} - close prices do not match')
						self.ta = None
#						beep(3)
				except Exception as e:
					print(f'{dttm_get()} {func_name} - Get TA ==> {self.prod_id} = Error : ({type(e)}){e}')
					traceback.print_exc()
					beep(3)
					pass
				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				if secs >= 5:
					msg = cs(f'mkt_ta_main_new for {self.prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
					chart_row(msg, len_cnt=240)
					chart_mid(len_cnt=240)
			if self.ta:
				self.mkt.ta = self.ta




		# Sell By Strat Logic - These do require TA
		if self.sell_yn == 'N' and self.ta:
			self.mkt, self = sell_strats_check(self.mkt, self, self.ta)


		# This is a blocker that will only be checked for TA sells
		if self.sell_yn == 'Y':
			if self.sell_force_yn == 'N':
				if self.sell_block_yn == 'N':
					if self.ta:
						self.sell_deny_all_green()


		# # Forced Sell Logic
		# # Second calling so a forced sell still overwrites a forced don't sell
		# if self.sell_yn == 'N' or (self.sell_yn == 'Y' and self.sell_block_yn == 'Y'):
		# 	self.sell_forces()


		# Finalize YesNos
		if self.sell_force_yn == 'Y':
			self.sell_yn = 'Y'
			self.hodl_yn = 'N'
		elif self.sell_block_yn == 'Y':
			self.sell_yn = 'N'
			self.hodl_yn = 'Y'
		elif self.sell_yn == 'Y':
			self.hodl_yn = 'N'
		else:
			self.sell_yn = 'N'
			self.hodl_yn = 'Y'


		db_tbl_poss_insupd(self)


		if self.sell_yn == 'Y' and self.sell_block_yn == 'N':
			if self.test_tf == 0:
				self.sell_live()
				if self.error_tf:
					play_thunder()
					self.sell_yn = 'N'
					if self.st.speak_yn == 'Y': speak_async(self.reason)
				else:
					if self.gain_loss_amt > 0:
						msg = f'WIN, selling {self.symb} for ${round(self.gain_loss_amt_est,2)} '
						if self.st.speak_yn == 'Y': speak_async(msg)
						if self.gain_loss_amt >= 1:
							play_cash()
					elif self.gain_loss_amt < 0:
						msg = f'LOSS, selling {self.symb} for ${round(self.gain_loss_amt_est,2)} '
						if self.st.speak_yn == 'Y': speak_async(msg)
						if self.gain_loss_amt <= -1:
							play_thunder()
			elif self.test_tf == 1:
				pos = self.sell_test(self.mkt, self.pos)

		if self.sell_yn == 'Y':
			if self.st.save_files_yn == 'Y':
				fname = f"saves/{self.prod_id}_SELL_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt"
				writeit(fname, '=== MKT ===')
				for k in self.mkt:
					writeit(fname, f'{k} : {self.mkt[k]}'.format(k, self.mkt[k]))
				writeit(fname, '')
				writeit(fname, '')
				writeit(fname, '=== POS ===')
				for k in self:
					if isinstance(self[k], [str, list, dict, float, int, decimal.Decimal, datetime, time]):
						writeit(fname, f'{k} : {pos[k]}')
					else:
						print(f'{k} : {type(self[k])}')


		db_tbl_poss_insupd(self)


		if self.gain_loss_pct < -5:
			msg = f'sell_yn : {self.sell_yn}, sell_block_yn : {self.sell_block_yn}, hodl_yn : {self.hodl_yn}'
			chart_row(msg, len_cnt=240)
	#		for sell_signal in sell_signals:
	#			print(sell_signal)

		func_end(fnc)
		return self.mkt, self, self.ta

	#<=====>#

	def sell_pos_blocks(self):
		func_name = 'sell_pos_blocks'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1)
		# G(func_str)

		self.sell_block_selling_off()

		self.sell_block_never_sell_all()
		self.sell_block_never_sell_prod_id()
		self.sell_block_never_sell_pos_id()

		self.sell_block_never_sell_loss_all()
		self.sell_block_never_sell_loss_prod_id()
		self.sell_block_never_sell_loss_pos_id()

		self.sell_block_price_range_extreme()

		self.disp_sell_blocks()

		func_end(fnc)

	#<=====>#

	def sell_pos_forces(self):
		func_name = 'sell_pos_forces'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		self.sell_force_force_sell_db()

		self.sell_force_force_sell_all()
		self.sell_force_force_sell_prod_id()
		self.sell_force_force_sell_id()

		self.disp_sell_forces()

		func_end(fnc)

	#<=====>#

	def sell_tests_before_ta(self):
		func_name = 'sell_tests_before_ta'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		# Take Profits
		if self.prc_chg_pct > 0:
			if self.sell_yn == 'N':
				if self.st.hard_take_profit_yn == 'Y':
					self.sell_test_hard_profit()

			if self.sell_yn == 'N':
				if self.st.trailing_profit_yn == 'Y':
					self.sell_test_trailing_profit()

		# Stop Loss
		if self.prc_chg_pct < 0:
			if self.sell_yn == 'N':
				if self.st.hard_stop_loss_yn == 'Y':
					self.sell_test_hard_stop()

			if self.sell_yn == 'N':
				if self.st.trailing_stop_loss_yn == 'Y':
					self.sell_test_trailing_stop()

			if self.sell_yn == 'N':
				if self.st.atr_stop_loss_yn == 'Y':
					self.sell_test_atr_stop()

			if self.sell_yn == 'N':
				if self.st.trailing_atr_stop_loss_yn == 'Y':
					self.sell_test_trailing_atr_stop()

		func_end(fnc)

	#<=====>#

	def sell_block_selling_off(self):
		func_name = 'sell_block_selling_off'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.st.selling_on_yn == 'N':
			self.sell_block_yn = 'Y'
			msg = f'settings => selling_on_yn : {self.st.selling_on_yn}'
#			BoW(msg)
#			beep(3)
			self.sell_blocks.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_block_never_sell_all(self):
		func_name = 'sell_block_never_sell_all'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.st.never_sell_all_yn == 'Y':
			self.sell_block_yn = 'Y'
			msg = f'settings => never_sell_all_yn : {self.st.never_sell_all_yn}'
#			BoW(msg)
#			beep(3)
			self.sell_blocks.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_block_never_sell_loss_all(self):
		func_name = 'sell_block_never_sell_loss_all'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.st.never_sell_loss_all_yn == 'Y' and self.prc_chg_pct < 0:
			self.sell_block_yn = 'Y'
			msg = f'settings => never_sell_loss_all_yn : {self.st.never_sell_loss_all_yn}'
#			BoW(msg)
#			beep(3)
			self.sell_blocks.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_block_never_sell_prod_id(self):
		func_name = 'sell_block_never_sell_prod_id'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.prod_id in self.st.never_sell_prod_ids:
			self.sell_block_yn = 'Y'
			msg = f'settings => never_sell.prod_ids : {self.prod_id}'
#			BoW(msg)
#			beep(3)
			self.sell_blocks.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_block_never_sell_loss_prod_id(self):
		func_name = 'sell_block_never_sell_loss_prod_id'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.prod_id in self.st.never_sell_loss_prod_ids and self.prc_chg_pct < 0:
			self.sell_block_yn = 'Y'
			msg = f'settings => never_sell_loss.prod_ids : {self.prod_id}'
#			BoW(msg)
#			beep(3)
			self.sell_blocks.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_block_never_sell_pos_id(self):
		func_name = 'sell_block_never_sell_pos_id'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.pos_id in self.st.never_sell_pos_ids:
			self.sell_block_yn = 'Y'
			msg = f'settings => never_sell.pos_ids : {self.pos_id}'
#			BoW(msg)
#			beep(3)
			self.sell_blocks.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_block_never_sell_loss_pos_id(self):
		func_name = 'sell_block_never_sell_loss_pos_id'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.pos_id in self.st.never_sell_loss_pos_ids and self.prc_chg_pct < 0:
			self.sell_block_yn = 'Y'
			msg = f'settings => never_sell_loss.pos_ids : {self.pos_id}'
#			BoW(msg)
#			beep(3)
			self.sell_blocks.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_block_price_range_extreme(self):
		func_name = 'sell_block_price_range_extreme'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		# Market Price Range Looks Very Suspect
		if self.mkt.prc_range_pct >= 5:
			self.sell_block_yn = 'Y'
			msg = f'price range variance of {self.mkt.prc_range_pct}, bid : {self.bid_prc}, ask : {self.ask_prc}, this price range looks sus... skipping sell'
#			BoW(msg)
#			beep(3)
			self.sell_blocks.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_force_force_sell_db(self):
		func_name = 'sell_force_force_sell_db'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.force_sell_tf == 1:
			self.sell_yn = 'Y'
			self.sell_force_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'force'
			self.sell_strat_name  = 'forced sell'
			msg = f'db => position marked as force sell... poss.force_sell_tf : {self.force_sell_tf}'
			self.sell_forces.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_force_force_sell_all(self):
		func_name = 'sell_force_force_sell_all'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.st.force_sell_all_yn == 'Y':
			self.sell_yn = 'Y'
			self.sell_force_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'force'
			self.sell_strat_name  = 'forced sell'
			msg = f'settings => force_sell_all_yn = {self.st.force_sell_all_yn}'
			self.sell_forces.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_force_force_sell_prod_id(self):
		func_name = 'sell_force_force_sell_prod_id'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.prod_id in self.st.force_sell_prod_ids:
			self.sell_yn = 'Y'
			self.sell_force_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'force'
			self.sell_strat_name  = 'forced sell'
			msg = f'settings => force_sell.prod_ids = {self.prod_id}'
			self.sell_forces.append(msg)

		func_end(fnc)

	#<=====>#

	def sell_force_force_sell_id(self):
		func_name = 'sell_force_force_sell_id'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.pos_id in self.st.force_sell_pos_ids:
			self.sell_yn = 'Y'
			self.sell_force_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'force'
			self.sell_strat_name  = 'forced sell'
			msg = f'settings => force_sell.pos_ids = {self.pos_id}'
			self.sell_forces.append(msg)

		func_end(fnc)

	#<=====>#

	# def sell_force_(self):
	# 	func_name = 'sell_force_'
	# 	func_str = f'{lib_name}.{func_name}()'
	# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# 	# G(func_str)


	# 	msg = f'    SELL TESTS - {self.prod_id} - {self.pos_id}- Forced Sell'
	# 	self.disp_sell_test_details(msg, all_sells, all_hodls)

	# 	func_end(fnc)

	#<=====>#

	def sell_test_hard_profit(self):
		func_name = 'sell_test_hard_profit'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Hard Take Profit Logic
		if self.prc_chg_pct >= self.st.hard_take_profit_pct:
			self.sell_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'profit'
			self.sell_strat_name = 'hard_profit'
			msg = f'    * SELL COND: ...hard profit pct => curr : {self.prc_chg_pct:>.2f}%, high : {self.prc_chg_pct_high:>.2f}%, drop : {self.prc_chg_pct_drop:>.2f}%, take_profit : {self.st.hard_take_profit_pct:>.2f}%, sell_yn : {self.sell_yn}'
			all_sells.append(msg)
		else:
			msg = f'    * HODL COND: ...hard profit => curr : {self.prc_chg_pct:>.2f}%, high : {self.prc_chg_pct_high:>.2f}%, drop : {self.prc_chg_pct_drop:>.2f}%, take_profit : {self.st.hard_take_profit_pct:>.2f}%, sell_yn : {self.sell_yn}'
			all_hodls.append(msg)

		msg = f'    SELL TESTS - {self.prod_id} - Hard Take Profit'
		self.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_hard_stop(self):
		func_name = 'sell_test_hard_stop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Hard Stop Loss Logic
		if self.prc_chg_pct <= abs(self.st.hard_stop_loss_pct) * -1:
			self.sell_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'stop_loss'
			self.sell_strat_name = 'hard_stop_loss'
			msg = f'    * SELL COND: ...hard stop loss => curr : {self.prc_chg_pct:>.2f}%, high : {self.prc_chg_pct_high:>.2f}%, drop : {self.prc_chg_pct_drop:>.2f}%, stop_loss : {self.st.hard_stop_loss_pct:>.2f}%, sell_yn : {self.sell_yn}'
			all_sells.append(msg)
		else:
			self.sell_yn = 'N'
			msg = f'    * HODL COND: ...hard stop loss => curr : {self.prc_chg_pct:>.2f}%, high : {self.prc_chg_pct_high:>.2f}%, drop : {self.prc_chg_pct_drop:>.2f}%, stop_loss : {self.st.hard_stop_loss_pct:>.2f}%, sell_yn : {self.sell_yn}'
			all_hodls.append(msg)

		self.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_trailing_profit(self):
		func_name = 'sell_test_trailing_profit'
		func_str  = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Trailing Profit Logic

		if self.prc_chg_pct > 0.5:
			max_drop_pct = -5
			if self.prc_chg_pct_high >= self.st.trailing_profit_trigger_pct:
				if self.prc_chg_pct_high >= 34:
					max_drop_pct = -1 * self.prc_chg_pct_high * .08
				elif self.prc_chg_pct_high >= 21:
					max_drop_pct = -1 * self.prc_chg_pct_high * .11
				elif self.prc_chg_pct_high >= 13:
					max_drop_pct = -1 * self.prc_chg_pct_high * .14
				elif self.prc_chg_pct_high >= 5:
					max_drop_pct = -1 * self.prc_chg_pct_high * .17
				elif self.prc_chg_pct_high >= 3:
					max_drop_pct = -1 * self.prc_chg_pct_high * .20
				elif self.prc_chg_pct_high >= 2:
					max_drop_pct = -1 * self.prc_chg_pct_high * .23
				elif self.prc_chg_pct_high >= 1:
					max_drop_pct = -1 * self.prc_chg_pct_high * .24

				max_drop_pct = round(max_drop_pct, 2)

				if self.prc_chg_pct_drop <= max_drop_pct:
					self.sell_yn = 'Y'
					self.hodl_yn = 'N'
					self.sell_strat_type = 'profit'
					self.sell_strat_name = 'trail_profit'
					msg = f'    * SELL COND: ...trailing profit => curr : {self.prc_chg_pct:>.2f}%, high : {self.prc_chg_pct_high:>.2f}%, drop : {self.prc_chg_pct_drop:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {self.sell_yn}'
					all_sells.append(msg)
				else:
					msg = f'    * HODL COND: ...trailing profit => curr : {self.prc_chg_pct:>.2f}%, high : {self.prc_chg_pct_high:>.2f}%, drop : {self.prc_chg_pct_drop:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {self.sell_yn}'
					all_hodls.append(msg)


		msg = f'    SELL TESTS - {self.prod_id} - Trailing Profit'
		self.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_trailing_stop(self):
		func_name = 'sell_test_trailing_stop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		stop_loss_pct = round(self.prc_chg_pct_high - abs(self.st.trailing_stop_loss_pct), 2)
		if self.prc_chg_pct < stop_loss_pct:
			self.sell_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'stop_loss'
			self.sell_strat_name = 'trail_stop'
			msg = f'    * SELL COND: ...trailing stop loss => curr : {self.prc_chg_pct:>.2f}%, high : {self.prc_chg_pct_high:>.2f}%, drop : {self.prc_chg_pct_drop:>.2f}%, trigger : {self.st.trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {self.sell_yn}'
			all_sells.append(msg)
		else:
			msg = f'    * HODL COND: ...trailing stop loss => curr : {self.prc_chg_pct:>.2f}%, high : {self.prc_chg_pct_high:>.2f}%, drop : {self.prc_chg_pct_drop:>.2f}%, trigger : {self.st.trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {self.sell_yn}'
			all_hodls.append(msg)

		msg = f'    SELL TESTS - {self.prod_id} - Trailing Stop Loss'
		self.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_atr_stop(self):
		func_name = 'sell_test_atr_stop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Trailing Stop Loss Logic
		atr_rfreq        = self.st.spot.sell.stop_loss.atr_stop_loss_rfreq
		atr              = self.ta[atr_rfreq]['atr']['ago0']
		atr_stop_loss    = self.prc_buy - atr

		if self.sell_prc < atr_stop_loss:
			self.sell_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'stop_loss'
			self.sell_strat_name = 'atr_stop'
			msg = f'    * SELL COND: ...ATR stop loss => curr : {self.sell_prc:>.8f}, atr : {atr:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {self.sell_yn}'
			all_sells.append(msg)
		else:
			msg = f'    * HODL COND: ...ATR stop loss => curr : {self.sell_prc:>.8f}, atr : {atr:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {self.sell_yn}'
			all_hodls.append(msg)


		msg = f'    SELL TESTS - {self.prod_id} - ATR Stop Loss'
		self.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_test_trailing_atr_stop(self):
		func_name = 'sell_test_trailing_atr_stop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells   = []
		all_hodls   = []

		# Trailing Stop Loss Logic
		atr_rfreq         = self.st.spot.sell.stop_loss.trailing_atr_stop_loss_rfreq
		atr_pct           = self.st.spot.sell.stop_loss.trailing_atr_stop_loss_pct
		atr               = self.ta[atr_rfreq]['atr']['ago0']
		atr_pct_mult      = atr_pct / 100
		atr_reduce        = atr * atr_pct_mult
		atr_stop_loss     = self.prc_high - atr_reduce

		if self.sell_prc < atr_stop_loss:
			self.sell_yn = 'Y'
			self.hodl_yn = 'N'
			self.sell_strat_type = 'stop_loss'
			self.sell_strat_name = 'trail_atr_stop'
			msg = f'    * SELL COND: ...ATR trailing stop loss => curr : {self.sell_prc:>.8f}, atr : {atr:>.8f}, atr_pct : {atr_pct:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {self.sell_yn}'
			all_hodls.append(msg)
		else:
			msg = f'    * HODL COND: ...ATR trailing stop loss => curr : {self.sell_prc:>.8f}, atr : {atr:>.8f}, atr_pct : {atr_pct:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {self.sell_yn}'
			all_sells.append(msg)

		msg = f'    SELL TESTS - {self.prod_id} - Trailing ATR Stop Loss'
		self.disp_sell_test_details(msg, all_sells, all_hodls)

		func_end(fnc)

	#<=====>#

	def sell_deny_all_green(self):
		func_name = 'sell_deny_all_green'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		all_sells                 = []
		all_hodls                 = []
		rfreq                     = self.buy_strat_freq
		freqs, faster_freqs       = freqs_get(rfreq)

		ha_color_5min  = self.ta['5min']['ha_color']['ago0']
		ha_color_15min = self.ta['15min']['ha_color']['ago0']
		ha_color_30min = self.ta['30min']['ha_color']['ago0']
		ha_color_1h    = self.ta['1h']['ha_color']['ago0']
		ha_color_4h    = self.ta['4h']['ha_color']['ago0']
		ha_color_1d    = self.ta['1d']['ha_color']['ago0']

		skip_checks = False
		if self.st.force_sell_all_yn == 'Y':
			skip_checks = True

		if self.prod_id in self.st.force_sell_prod_ids:
			skip_checks = True

		if self.pos_id in self.st.force_sell_pos_ids:
			skip_checks = True

		if not skip_checks:
			green_save = False

			if rfreq == '1d':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.sell_block_yn}'
				if ha_color_4h == 'green':
					if (ha_color_30min == 'green' or ha_color_15min == 'green') and ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.sell_block_yn}'
						green_save = True
			elif rfreq == '4h':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.sell_block_yn}'
				if ha_color_1h == 'green':
					if ha_color_15min == 'green' and ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.sell_block_yn}'
						green_save = True
			elif rfreq == '1h':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {self.sell_block_yn}'
				if ha_color_30min == 'green':
					if ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {self.sell_block_yn}'
						green_save = True
			elif rfreq == '30min':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {self.sell_block_yn}'
				if ha_color_15min == 'green':
					if ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {self.sell_block_yn}'
						green_save = True
			elif rfreq == '15min':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.sell_block_yn}'
				if ha_color_5min == 'green':
					if ha_color_5min == 'green':
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.sell_block_yn}'
						green_save = True


			if green_save:
				self.sell_block_yn = 'Y'
				all_hodls.append(pass_msg)
			else:
				msg = f'    * CANCEL SELL: ALL CANDLES NOT GREEN ==> Allowing Sell...   5min : {ha_color_5min}, 15min : {ha_color_15min}, 30min : {ha_color_30min}, sell_block_yn : {self.sell_block_yn}'
				all_sells.append(fail_msg)

		print(f'{func_name} - sell_block_yn : {self.sell_block_yn}, show_tests_yn : {self.st.show_tests_yn}')
		if self.sell_block_yn == 'Y' or self.st.show_tests_yn in ('Y','F'):
			msg = f'    SELL TESTS - {self.prod_id} - All Green Candes...'
			WoG(msg)
			if self.sell_block_yn == 'Y' or self.st.show_tests_yn in ('Y'):
				for e in all_sells:
					if self.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					self.mkt.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					self.mkt.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def sell_live(self):
		func_name = 'sell_live'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		if self.st.sell_limit_yn == 'N' and self.mkt.mkt_limit_only_tf == 1:
			print(f'{self.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')
			self.ord_mkt_sell_orig()
		elif self.st.sell_limit_yn == 'Y':
			try:
				self.ord_lmt_sell_open() 
			except Exception as e:
				print(f'{func_name} ==> sell limit order failed, attempting market... {e}')
				beep(3)
				self.ord_mkt_sell_orig()
		else:
			self.ord_mkt_sell_orig()

		# Update to Database
		db_tbl_poss_insupd(self)

		func_end(fnc)
#		return pos

	#<=====>#

	def sell_test(self, mkt, pos):
		func_name = 'sell_test'
		func_str = f'{lib_name}.{func_name}(pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

#		beep()

		so = AttrDict()
		so.test_tf                     = self.test_tf
		so.prod_id                     = self.prod_id
		so.mkt_name                    = self.mkt_name
		so.pos_id                      = self.pos_id
		so.sell_seq_nbr                = 1
		so.sell_order_uuid             = self.gen_guid()	
		so.pos_type                    = 'SPOT'
		so.ord_stat                    = 'OPEN'
		so.sell_strat_type             = self.sell_strat_type
		so.sell_strat_name             = self.sell_strat_name
		so.sell_strat_freq             = self.sell_strat_freq
		so.sell_begin_dttm             = dt.now()	
		so.sell_end_dttm               = dt.now()	
		so.sell_curr_symb              = self.sell_curr_symb
		so.recv_curr_symb              = self.recv_curr_symb	
		so.fees_curr_symb              = self.fees_curr_symb
		so.sell_cnt_est                = self.hold_cnt
		so.sell_cnt_act                = self.hold_cnt
		so.fees_cnt_act                = (self.hold_cnt * self.prc_sell) * 0.004
		so.tot_in_cnt                  = (self.hold_cnt * self.prc_sell) * 0.996
		so.prc_sell_est                = self.prc_sell
		so.prc_sell_act                = self.prc_sell
		so.tot_prc_buy                 = self.prc_sell
		so.prc_sell_slip_pct           = 0

		db_tbl_sell_ords_insupd(so)
		time.sleep(.33)

		func_end(fnc)
#		return pos

#<=====>#

	def cb_sell_base_size_calc(self, init_sell_cnt):
		func_name = 'cb_sell_base_size_calc'
		func_str = ''
		func_str += f'{lib_name}.{func_name}('
		func_str += f'sell_cnt={init_sell_cnt:>.8f}, '
		func_str += ')'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		sell_cnt_max     = dec(init_sell_cnt)
#		print(f'sell_cnt_max : {sell_cnt_max:>.8f} passed in...')

		self.pocket_pct            = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.pocket_pct, in_key=self.prod_id)
		self.clip_pct              = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.clip_pct, in_key=self.prod_id)
		self.sell_prc              = self.mkt.prc_sell

		if sell_cnt_max > dec(self.hold_cnt):
			print(f'...selling more {sell_cnt_max:>.8f} than we are position is holding {self.hold_cnt:>.8f} onto...exiting...')
			beep(3)
			func_end(fnc)
			return 0

#		self.refresh_wallet_tf = True

		if sell_cnt_max > dec(self.bal_cnt):
			print(f'...selling more {sell_cnt_max:>.8f} than we the wallet balance {self.bal_cnt:>.8f}...exiting...')
			beep(3)
			func_end(fnc)
			return 0

		if self.prc_chg_pct > 0 and self.pocket_pct > 0:
			sell_cnt_max -= sell_cnt_max * (dec(self.pocket_pct) / 100) * (dec(self.prc_chg_pct)/100)

		if self.prc_chg_pct < 0 and self.clip_pct > 0:
			sell_cnt_max -= sell_cnt_max * (dec(self.clip_pct) / 100) * (abs(dec(self.prc_chg_pct))/100)

		sell_blocks = int(sell_cnt_max / dec(self.mkt.base_size_incr))
		sell_cnt_max = sell_blocks * dec(self.mkt.base_size_incr)

		if sell_cnt_max < dec(self.mkt.base_size_min):
			print(f'...selling less {sell_cnt_max:>.8f} than coinbase allows {self.mkt.base_size_min}...exiting...')
			beep(3)
			func_end(fnc)
			return 0

		if sell_cnt_max > dec(self.mkt.base_size_max):
			sell_cnt_max = dec(self.mkt.base_size_max)

		self.sell_cnt = sell_cnt_max

		func_end(fnc)
#		return sell_cnt

	#<=====>#

	def ord_mkt_sell(self):
		func_name = 'ord_mkt_sell'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id               = self.prod_id
		init_sell_cnt         = self.hold_cnt

		end_time              = dt.now() + timedelta(minutes=5)
		end_time              = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

		self.cb_sell_base_size_calc(init_sell_cnt)

		if self.sell_cnt == 0:
			func_end(fnc)
			self.pos_stat = 'ERR'
			self.ignore_tf = 1
			self.error_tf = 1
			self.sell_yn = 'N'
			self.reason = f'there are not enough {self.buy_curr_symb} to complete this sale...'
			db_tbl_poss_insupd(self)
		else:

			recv_amt = round(float(self.sell_cnt) * float(self.sell_prc),2)

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
				so.pos_id                = self.pos_id
				so.prod_id               = self.mkt.prod_id
				so.pos_type              = 'SPOT'
				so.ord_stat              = 'OPEN'
				so.sell_order_uuid       = ord_id
				so.sell_begin_dttm       = dt.now()
				so.sell_strat_type       = self.sell_strat_type
				so.sell_strat_name       = self.sell_strat_name
				so.sell_curr_symb        = self.mkt.base_curr_symb
				so.recv_curr_symb        = self.mkt.quote_curr_symb
				so.fees_curr_symb        = self.mkt.quote_curr_symb
				so.sell_cnt_est          = self.sell_cnt
				so.prc_sell_est          = self.mkt.prc_sell
				db_tbl_sell_ords_insupd(so)
				time.sleep(.33)
				db_poss_stat_upd(pos_id=self.pos_id, pos_stat='SELL')
				self.pos_stat = 'SELL'
			else:
				print(f'{func_name} exit 1 : {o}')
				print(f'{func_name} exit 1 : {so}')
				sys.exit()

		func_end(fnc)
#		return pos

	#<=====>#

	def ord_mkt_sell_orig(self):
		func_name = 'ord_mkt_sell_orig'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		client_order_id       = cb_client_order_id()
		prod_id               = self.prod_id
		init_sell_cnt         = self.hold_cnt

		self.cb_sell_base_size_calc(init_sell_cnt)

		if self.sell_cnt == 0:
			func_end(fnc)
			self.pos_stat = 'ERR'
			self.ignore_tf = 1
			self.error_tf = 1
			self.sell_yn = 'N'
			self.reason = f'there are not enough {self.buy_curr_symb} to complete this sale...'
			db_tbl_poss_insupd(self)
		else:
			oc = {}
			oc['market_market_ioc'] = {}
			oc['market_market_ioc']['base_size'] = f'{self.sell_cnt:>.8f}'

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
						so.pos_id                = self.pos_id
						so.prod_id               = self.mkt.prod_id
						so.pos_type              = 'SPOT'
						so.ord_stat              = 'OPEN'
						so.sell_order_uuid       = o['success_response']['order_id']
						so.sell_client_order_id  = o['success_response']['client_order_id']
						so.sell_begin_dttm       = dt.now()
						so.sell_strat_type       = self.sell_strat_type
						so.sell_strat_name       = self.sell_strat_name
						so.sell_curr_symb        = self.mkt.base_curr_symb
						so.recv_curr_symb        = self.mkt.quote_curr_symb
						so.fees_curr_symb        = self.mkt.quote_curr_symb
						so.sell_cnt_est          = self.sell_cnt
						so.prc_sell_est          = self.mkt.prc_sell
						db_tbl_sell_ords_insupd(so)
						time.sleep(.25)
#						print(f'setting pos : {self.pos_id} to SELL...')
						db_poss_stat_upd(pos_id=self.pos_id, pos_stat='SELL')
						self.pos_stat = 'SELL'
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
#		return pos

	#<=====>#

	def ord_lmt_sell_open(self):
		func_name = 'ord_lmt_sell_open'
		func_str = f'{lib_name}.{func_name}(mkt, pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id               = self.prod_id
		init_sell_cnt         = self.hold_cnt

		end_time              = dt.now() + timedelta(minutes=5)
		end_time              = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

		self.cb_sell_base_size_calc(init_sell_cnt)

		if self.sell_cnt == 0:
			func_end(fnc)
			self.pos_stat = 'ERR'
			self.ignore_tf = 1
			self.error_tf = 1
			self.sell_yn = 'N'
			self.reason = f'there are not enough {self.buy_curr_symb} to complete this sale...'
			db_tbl_poss_insupd(self)
		else:

			recv_amt = round(float(self.sell_cnt) * float(self.sell_prc),2)

			prc_mult = str(1)
			if self.prc_chg_pct > 0:
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
				so.pos_id                = self.pos_id
				so.prod_id               = self.mkt.prod_id
				so.pos_type              = 'SPOT'
				so.ord_stat              = 'OPEN'
				so.sell_order_uuid       = ord_id # o['success_response']['order_id']
				so.sell_begin_dttm       = dt.now()
				so.sell_strat_type       = self.sell_strat_type
				so.sell_strat_name       = self.sell_strat_name
				so.sell_curr_symb        = self.mkt.base_curr_symb
				so.recv_curr_symb        = self.mkt.quote_curr_symb
				so.fees_curr_symb        = self.mkt.quote_curr_symb
				so.sell_cnt_est          = self.sell_cnt
				so.prc_sell_est          = self.mkt.prc_sell
				db_tbl_sell_ords_insupd(so)
				time.sleep(.25)
				db_poss_stat_upd(pos_id=self.pos_id, pos_stat='SELL')
				self.pos_stat = 'SELL'
			else:
				print(f'{func_name} exit 1 : {o}')
				print(f'{func_name} exit 1 : {so}')
				sys.exit()

		func_end(fnc)
#		return pos

	#<=====>#

	def sell_header(self):
		func_name = 'sell_header'
		func_str = f'{lib_name}.{func_name}()'
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

		title_msg = f'* SELL LOGIC * {self.prod_id} *'
		chart_mid(in_str=title_msg, len_cnt=240, bold=True)
		chart_headers(in_str=hmsg, len_cnt=240, bold=True)

		self.mkt.show_sell_header_tf = False

		func_end(fnc)

	#<=====>#

	def disp_sell(self):
		func_name = 'disp_sell'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.mkt.show_sell_header_tf:
			self.sell_header()
			self.mkt.show_sell_header_tf = False

		disp_age = format_disp_age(self.age_mins)

		if self.test_tf == 1:
			test_tf = 'T'
		else:
			test_tf = ''

		msg = ''
		msg += f'{self.prod_id:<12}' + ' | '
		msg += f'{test_tf:^1}' + ' | '
		msg += f'{self.pos_id:^6}' + ' | '
		msg += f'{self.buy_strat_name:^12}' + ' | '
		msg += f'{self.buy_strat_freq:^5}' + ' | '
		msg += f'{disp_age:^10}' + ' | '
		msg += f'{self.tot_out_cnt:>16.8f}' + ' | '
		msg += f'{self.val_curr:>14.8f}' + ' | '
		msg += f'{self.prc_buy:>14.8f}' + ' | '
		msg += f'{self.prc_curr:>14.8f}' + ' | '
		msg += f'{self.prc_high:>14.8f}' + ' | '
		msg += f'{self.prc_chg_pct:>8.2f} %' + ' | '
		msg += f'{self.prc_chg_pct_high:>8.2f} %' + ' | '
		msg += f'{self.prc_chg_pct_low:>8.2f} %' + ' | '
		msg += f'{self.prc_chg_pct_drop:>8.2f} %' + ' | '
		msg += f'$ {self.gain_loss_amt:>14.8f}' + ' | '
		msg += f'$ {self.gain_loss_amt_est_high:>14.8f}'

		msg = cs_pct_color(self.prc_chg_pct, msg)
		chart_row(msg, len_cnt=240)

		func_end(fnc)

	#<=====>#

	def disp_sell_blocks(self):
		func_name = 'disp_sell_blocks'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		self.st.show_blocks_yn                   = self.st.spot.sell.show_blocks_yn

		if self.st.show_blocks_yn == 'Y':
			for b in self.sell_blocks:
				if self.prc_chg_pct > 0:
					b = '    ' + cs('* SELL BLOCK *', font_color='white', bg_color='green') + ' ' + cs(b, font_color='green')
					chart_row(b, len_cnt=240)
				else:
					b = '    ' + cs('* SELL BLOCK *', font_color='white', bg_color='red')  + ' ' + cs(b, font_color='red')
					chart_row(b, len_cnt=240)
				self.mkt.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def disp_sell_forces(self):
		func_name = 'disp_sell_forces'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.st.show_forces_yn == 'Y':
			for f in self.sell_forces:
				if self.prc_chg_pct > 0:
					f = '    ' + cs('* SELL FORCE *', font_color='white', bg_color='green')  + ' ' + cs(f, font_color='green')
					chart_row(f, len_cnt=240)
				else:
					f = '    ' + cs('* SELL FORCE *', font_color='white', bg_color='red')  + ' ' + cs(f, font_color='red')
					chart_row(f, len_cnt=240)
				self.mkt.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def disp_sell_tests(self):
		func_name = 'disp_sell_tests'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.st.show_tests_yn == 'Y':
			for t in self.sell_tests:
				if self.prc_chg_pct > 0:
					t = '    ' + cs('* SELL TEST *', font_color='white', bg_color='green')  + ' ' + cs(t, font_color='green')
					chart_row(t, len_cnt=240)
				else:
					t = '    ' + cs('* SELL TEST *', font_color='white', bg_color='red')  + ' ' + cs(t, font_color='red')
					chart_row(t, len_cnt=240)
				self.mkt.show_sell_header_tf = True

		func_end(fnc)

	#<=====>#

	def disp_sell_test_details(self, msg, all_sells, all_hodls):
		func_name = 'disp_sell_test_details'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if (self.sell_yn == 'Y' and self.sell_block_yn == 'N') or self.st.show_tests_yn in ('Y','F'):
			msg = '    ' + cs('==> ' + msg + f' * sell => {self.sell_yn} * sell_block => {self.sell_block_yn} * hodl => {self.hodl_yn}', font_color='white', bg_color='blue')
			chart_row(msg, len_cnt=240)
			if (self.sell_yn == 'Y' and self.sell_block_yn == 'N') or self.st.show_tests_yn in ('Y'):
				for e in all_sells:
					if self.prc_chg_pct > 0:
						e = '    ' + cs('* ' + e, font_color='green')
						chart_row(e, len_cnt=240)
					else:
						e = '    ' + cs('* ' + e, font_color='red')
						chart_row(e, len_cnt=240)
					self.mkt.show_sell_header_tf = True
				for e in all_hodls:
					e = '    ' + cs('* ' + e, font_color='green', bg_color='white')
					chart_row(e, len_cnt=240)
					self.mkt.show_sell_header_tf = True
#				print(f'sell_yn : {self.sell_yn}, hodl_yn : {self.hodl_yn}')

		func_end(fnc)

	#<=====>#

	# def sell_log(self, msg):
	# 	func_name = 'sell_log'
	# 	func_str = f'{lib_name}.{func_name}(msg)'
	# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# 	# G(func_str)

	# 	dt_str  = dt.now().strftime('%Y_%m_%d')
	# 	logfile = f"logs_sell/{dt_str}_sell_log.txt"
	# 	wmsg    = f'{dttm_get()} ==> {msg}'
	# 	file_write(logfile, wmsg)

	# 	func_end(fnc)

	#<=====>#

	# def sell_sign_rec(self, pos):
	# 	func_name = 'sell_sign_rec'
	# 	func_str = f'{lib_name}.{func_name}(pos)'
	# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# 	# G(func_str)

	# 	ss = {}
	# 	ss = {}
	# 	ss["test_tf"]              = self.test_tf
	# 	ss["prod_id"]              = self.prod_id
	# 	ss["pos_id"]               = self.pos_id
	# 	ss["sell_strat_type"]      = self.sell_strat_type
	# 	ss["sell_strat_name"]      = self.sell_strat_name
	# 	ss["sell_strat_freq"]      = self.sell_strat_freq
	# 	ss["buy_yn"]               = self.buy_yn
	# 	ss["wait_yn"]              = self.wait_yn
	# 	ss["sell_curr_symb"]       = self.sell_curr_symb
	# 	ss["recv_curr_symb"]       = self.recv_curr_symb
	# 	ss["fees_curr_symb"]       = self.fees_curr_symb
	# 	ss["sell_cnt_est"]         = self.sell_cnt_est
	# 	ss["sell_prc_est"]         = self.sell_prc_est
	# 	ss["sell_sub_tot_est"]     = self.sell_sub_tot_est
	# 	ss["sell_fees_est"]        = self.sell_fees_est
	# 	ss["sell_tot_est"]         = self.sell_tot_est

	# 	# Update to Database
	# 	db_tbl_sell_signs_insupd(ss)

	# 	func_end(fnc)

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
