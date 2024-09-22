#<=====>#
# Import All Scope
#<=====>#

import_all_func_list =  []
import_all_func_list.append("buy_logic")
import_all_func_list.append("buy_logic_mkt_boosts")
import_all_func_list.append("buy_logic_strat_boosts")
import_all_func_list.append("buy_logic_deny")
import_all_func_list.append("buy_logic_mkt_deny")
import_all_func_list.append("buy_logic_strat_deny")
import_all_func_list.append("buy_ords_check")
import_all_func_list.append("buy_header")
import_all_func_list.append("disp_buy")
import_all_func_list.append("buy_log")
import_all_func_list.append("buy_sign_rec")
import_all_func_list.append("ord_mkt_buy")
import_all_func_list.append("ord_mkt_buy_orig")
import_all_func_list.append("ord_lmt_buy_open")
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
lib_name      = 'bot_cls_buy'
log_name      = 'bot_cls_buy'
lib_secs_max  = 2

#<=====>#
# Assignments Pre
#<=====>#

#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

def buy_logic(self, buy_mkts, mkt, trade_perf, trade_strat_perfs, ta):
	func_name = 'buy_logic'
	func_str = f'{lib_name}.{func_name}(buy_mkts, mkt, trade_perf, trade_strat_perfs, ta)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=6)
	# G(func_str)

	st                        = settings.settings_load()
	prod_id                   = mkt.prod_id
	buy_yn                    = 'N'
	wait_yn                   = 'Y'
	mkt.buy_strat_type        = ''
	mkt.buy_strat_name        = ''
	mkt.buy_strat_freq        = ''
	debug_yn                  = 'N'
	buy_signals               = []

	self.buy_header(prod_id)
	self.show_buy_header_tf        = False

	# skip buy logic if the prod_id not in the buy_mkts (ie it has positions to sell)
	if prod_id not in buy_mkts:
		RoW(f'{prod_id} not in buy_mkts, bypassing buy logic...')
		func_end(fnc)
		return mkt
	else:
		if debug_yn == 'Y':
			BoW(f'{prod_id} in buy_mkts, allowing buy logic...')

	# skip buy logic if ta is not present
	if not ta:
		RoW(f'{prod_id} was not successful collecting ta, bypassing buy logic...')
		func_end(fnc)
		return mkt
	else:
		if debug_yn == 'Y':
			BoW(f'{prod_id} was successful collecting ta, allowing buy logic...')

	# loop throug all buy tests
	for trade_strat_perf in trade_strat_perfs:

		# set default values
		buy_yn                                         = 'N'
		buy_deny_yn                                    = 'N'
		wait_yn                                        = 'Y'

		# format trade_strat_perf
		trade_strat_perf                               = dec_2_float(trade_strat_perf)
		trade_strat_perf                               = AttrDictConv(in_dict=trade_strat_perf)

		# default trade size & open position max
		trade_strat_perf.trade_size                    = settings.get_ovrd(in_dict=self.st.spot.buy.trade_size, in_key=prod_id)
		trade_strat_perf.restricts_strat_open_cnt_max  = settings.get_ovrd(in_dict=self.st.spot.buy.strat_open_cnt_max, in_key=prod_id) 

		# get strat performance boots
		# adjusts trade size & open position max
		mkt, trade_strat_perf                          = self.buy_logic_strat_boosts(mkt, trade_strat_perf)

		# perform buy strategy checks
		mkt, trade_perf, trade_strat_perf, buy_yn, wait_yn, buy_signals, self.reserve_locked_tf = buy_strats_check(self.st, mkt, trade_perf, trade_strat_perf, ta, buy_signals, self.reserve_locked_tf)

		# display
		self.disp_buy(mkt, trade_strat_perf)

		# these will have been checked before hand unless we forced the tests anyways
		if buy_yn == 'Y':

			# bot deny
			if buy_deny_yn == 'N':
				buy_deny_yn = self.buy_logic_deny(mkt, trade_perf)

			# mkt deny
			if buy_deny_yn == 'N':
				buy_deny_yn, trade_perf = self.buy_logic_mkt_deny(mkt, trade_perf)

			# strat deny
			if buy_deny_yn == 'N':
				buy_deny_yn, trade_strat_perf = self.buy_logic_strat_deny(mkt, trade_strat_perf)

			if buy_deny_yn == 'N':
				buy_deny_yn = buy_strats_deny(mkt, trade_strat_perf, buy_yn, wait_yn)

		mkt.buy_yn       = buy_yn
		mkt.buy_deny_yn  = buy_deny_yn
		mkt.wait_yn      = wait_yn

		dttm = dttm_get()
		if buy_yn == 'Y':

			WoM(f'bot.buy_logic !!! * buy_yn : {buy_yn} * buy_deny_yn : {buy_deny_yn}')

			self.show_buy_header_tf = True
			if buy_deny_yn == 'N':
				self.buy_live(mkt, trade_strat_perf)
				txt = '!!! BUY !!!'
				m = '{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f} * STRAT: {}'
				msg = m.format(dttm, txt, mkt.prc_buy, trade_strat_perf.trade_size, mkt.bal_avail, mkt.buy_strat_name)
				WoG(msg)
				WoG(msg)
				WoG(msg)
				symb = prod_id.split(',')[0]
				msg = f'buying {symb} for {trade_strat_perf.trade_size} USDC with strategy {mkt.buy_strat_name} on the {mkt.buy_strat_freq} timeframe'
				WoG(msg)

				if self.st.speak_yn == 'Y': speak_async(msg)

				trade_perf.bo_elapsed        = 0
				trade_perf.pos_elapsed       = 0
				trade_perf.last_elapsed      = 0
				trade_perf.open_poss_cnt     += 1

				mkt.bal_avail                -= trade_strat_perf.trade_size
				mkt.spendable_amt            -= trade_strat_perf.trade_size

				msg = f'{mkt.quote_curr_symb} * Balance : ${mkt.bal_avail:>.2f} * Reserve : ${mkt.reserve_amt:>.2f} * Spendable : ${mkt.spendable_amt:>.2f} * '
				WoG(msg)

			elif buy_deny_yn == 'Y':
				if prod_id in self.buy_mkts:
					if self.st.spot.buy.allow_tests_yn == 'Y':
						if trade_strat_perf.open_cnt == 0:
							txt = '!!! BUY * TEST * !!!'
							m = '{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f} * STRAT: {}'
							msg = m.format(dttm, txt, mkt.prc_buy, trade_strat_perf.trade_size, mkt.bal_avail, mkt.buy_strat_name)
							WoG(msg)
							WoG(msg)
							WoG(msg)

							self.buy_test(mkt, trade_strat_perf)

		elif buy_yn == 'N' :
			txt = '!!! WAIT !!!'
			m = '{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f}'
			msg = m.format(dttm, txt, mkt.prc_buy, trade_strat_perf.trade_size, mkt.bal_avail)
#			BoW(msg)

		# Save Files
		if buy_yn == 'Y':
			if self.st.spot.buy.save_files_yn == 'Y':
				fname = f"saves/{prod_id}_BUY_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt"
				writeit(fname, '=== MKT ===')
				for k in mkt:
					writeit(fname, f'{k} : {mkt[k]}')

	chart_mid(len_cnt=240, bold=True)

	func_end(fnc)
	return mkt

#<=====>#

def buy_logic_mkt_boosts(self, mkt, trade_perf):
	func_name = 'buy_logic_mkt_boosts'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id                   = mkt.prod_id
	debug_yn                  = 'N'
	show_boosts_yn            = self.st.spot.buy.show_boosts_yn

	# get default open position max for strat
	# add double override logic strat + prod
	# fixme
	trade_perf.restricts_open_poss_cnt_max = settings.get_ovrd(in_dict=self.st.spot.buy.open_poss_cnt_max, in_key=prod_id) 

	# Open Position Count Checks Performance Based
	# Boost allowed max positions based upon past performance
	if trade_perf.tot_cnt >= 5 and trade_perf.gain_loss_pct_day > 0.1:
		trade_perf.restricts_open_poss_cnt_max *= 2
		if show_boosts_yn == 'Y':
			msg = ''
			msg += f'    * BOOST BUY STRAT : '
			msg += f'{mkt.prod_id} '
			msg += f'has {trade_perf.tot_cnt} trades '
			msg += f'with performance {trade_perf.gain_loss_pct_day:>.8f} % < 0 % '
			msg += f'boosting allowed open pos ... '
			msg = cs(msg, font_color='blue', bg_color='white')
			chart_row(msg, len_cnt= 240)
	else:
		if debug_yn == 'Y':
			print(f'{func_name}, tot_cnt : {trade_perf.tot_cnt}, gain_loss_pct_day : {trade_perf.gain_loss_pct_day}, strat_open_cnt_max : {trade_perf.restricts_open_poss_cnt_max}')

	func_end(fnc)
	return mkt, trade_perf

#<=====>#

def buy_logic_strat_boosts(self, mkt, trade_strat_perf):
	func_name = 'buy_logic_strat_boosts'
	func_str = f'{lib_name}.{func_name}(mkt, trade_strat_perf)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id                   = mkt.prod_id
	buy_strat_type            = trade_strat_perf.buy_strat_type
	buy_strat_name            = trade_strat_perf.buy_strat_name
	buy_strat_freq            = trade_strat_perf.buy_strat_freq
	debug_yn                  = 'N'
	show_boosts_yn            = self.st.spot.buy.show_boosts_yn

	# get default open position max for strat
	# add double override logic strat + prod
	# fixme
	trade_strat_perf.restricts_strat_open_cnt_max = settings.get_ovrd(in_dict=self.st.spot.buy.strat_open_cnt_max, in_key=prod_id) 

	# Open Position Count Checks Performance Based
	# Boost allowed max positions based upon past performance
	if trade_strat_perf.tot_cnt >= 25 and trade_strat_perf.gain_loss_pct_day > 1:
		trade_strat_perf.restricts_strat_open_cnt_max *= 2
		if show_boosts_yn == 'Y':
			msg = ''
			msg += f'    * BOOST BUY STRAT : '
			msg += f'{mkt.prod_id} '
			msg += f'{buy_strat_name} - {buy_strat_freq} '
			msg += f'has {trade_strat_perf.tot_cnt} trades '
			msg += f'with performance {trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % '
			msg += f'boosting allowed open pos ... '
			msg = cs(msg, font_color='blue', bg_color='white')
			chart_row(msg, len_cnt= 240)
	else:
		if debug_yn == 'Y':
			print(f'{func_name}, tot_cnt : {trade_strat_perf.tot_cnt}, gain_loss_pct_day : {trade_strat_perf.gain_loss_pct_day}, strat_open_cnt_max : {trade_strat_perf.restricts_strat_open_cnt_max}')

	# get default open position max for strat
	# Assign Min Value For New Market + Strat with little history or poor performance
	trade_size_min_mult        = settings.get_ovrd(in_dict=self.st.spot.buy.trade_size_min_mult, in_key=prod_id)
	trade_size                 = mkt.quote_size_min * trade_size_min_mult
	tests_min                  = settings.get_ovrd(in_dict=self.st.spot.buy.strats[buy_strat_name].tests_min, in_key=buy_strat_freq) 
	boost_tests_min            = settings.get_ovrd(in_dict=self.st.spot.buy.strats[buy_strat_name].boost_tests_min, in_key=buy_strat_freq) 

	# give default value to strat with some history and positive impact
	if trade_strat_perf.tot_cnt >= tests_min and trade_strat_perf.gain_loss_pct_day > 0:
		trade_size            = settings.get_ovrd(in_dict=self.st.spot.buy.trade_size, in_key=prod_id) 
	# give default value to strat with some history and positive impact
	elif trade_strat_perf.tot_cnt >= 5 and trade_strat_perf.win_pct >= 90:
		trade_size             = settings.get_ovrd(in_dict=self.st.spot.buy.trade_size, in_key=prod_id) 
	else:
		if debug_yn == 'Y':
			print(f'{func_name}, tot_cnt : {trade_strat_perf.tot_cnt}, gain_loss_pct_day : {trade_strat_perf.gain_loss_pct_day}, trade_size : {trade_size}')

	# Kid has potential, lets give it a little more earlier
	if trade_strat_perf.tot_cnt >= 3 and trade_strat_perf.gain_loss_pct_day > 0.05:
		trade_size             *= 2
	# Boost those with proven track records
	if trade_strat_perf.tot_cnt >= tests_min and trade_strat_perf.gain_loss_pct_day > 0.1:
		trade_size             *= 2
	# Boost those with proven track records
	if trade_strat_perf.tot_cnt >= boost_tests_min and trade_strat_perf.gain_loss_pct_day > 0.25:
		trade_size             *= 2
	# Boost those with proven track records
	if trade_strat_perf.tot_cnt >= boost_tests_min and trade_strat_perf.gain_loss_pct_day > 0.5:
		trade_size             *= 2
	# Boost those with proven track records
	if trade_strat_perf.tot_cnt >= boost_tests_min and trade_strat_perf.gain_loss_pct_day > 1:
		trade_size             *= 2
	# Boost those with proven track records
	if trade_strat_perf.tot_cnt >= boost_tests_min and trade_strat_perf.gain_loss_pct_day > 2:
		trade_size             *= 2
	# Boost those with proven track records
	if trade_strat_perf.tot_cnt >= boost_tests_min and trade_strat_perf.gain_loss_pct_day > 4:
		trade_size             *= 2
	# Boost those with proven track records
	if trade_strat_perf.tot_cnt >= boost_tests_min and trade_strat_perf.gain_loss_pct_day > 8:
		trade_size             *= 2

	if show_boosts_yn == 'Y':
		msg = ''
		msg += f'    * BOOST BUY STRAT : {mkt.prod_id} {buy_strat_name} - {buy_strat_freq} has {trade_strat_perf.tot_cnt} trades '
		msg += f'with performance {trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % boosting trade_size ${trade_size} ... '
		msg = cs(msg, font_color='blue', bg_color='white')
		chart_row(msg, len_cnt= 240)

	if debug_yn == 'Y':
		print(f'{func_name}, tot_cnt : {trade_strat_perf.tot_cnt}, gain_loss_pct_day : {trade_strat_perf.gain_loss_pct_day}, trade_size : {trade_size}')

	# assign final trade_size
	trade_strat_perf.trade_size = trade_size

	func_end(fnc)
	return mkt, trade_strat_perf

#<=====>#

def buy_logic_deny(self, mkt, trade_perf):
	func_name = 'buy_logic_deny'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	buy_deny_yn               = 'N'
	debug_yn                  = 'N'

	if self.st.spot.buy.buying_on_yn == 'N' :
		RoW(f'    * CANCEL BUY : buying has been turned off in settings...')
		buy_deny_yn = 'Y'
	else:
		if debug_yn == 'Y':
			BoW(f'    * ALLOWED BUY : buying has been turned off in settings...')

	mkts_open_max = self.st.spot.buy.mkts_open_max
	mkts_open_cnt = db_mkts_open_cnt_get()
	if trade_perf.open_poss_cnt == 0 and mkts_open_cnt >= mkts_open_max:
		RoW(f'    * CANCEL BUY MKT : {mkt.prod_id} maxed out {mkts_open_cnt} different markets, max : {mkts_open_max}...')
		buy_deny_yn = 'Y'
	else:
		if debug_yn == 'Y':
			BoW(f'    * ALLOWED BUY MKT : {mkt.prod_id} maxed out {mkts_open_cnt} different markets, max : {mkts_open_max}...')

	func_end(fnc)
	return buy_deny_yn

#<=====>#

def buy_logic_mkt_deny(self, mkt, trade_perf):
	func_name = 'buy_logic_mkt_deny'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id                   = mkt.prod_id
	buy_deny_yn               = 'N'
	debug_yn                  = 'N'

	# Open Position Count Checks Lower Good Performance
	special_prod_ids = self.st.spot.buy.special_prod_ids
	if prod_id not in special_prod_ids:
		# Limit Max Position Count - By Market
		if trade_perf.tot_cnt >= 10 and trade_perf.gain_loss_pct_day < 0:
			RoW(f'    * LOWER OPEN POSS CNT : {mkt.prod_id} has had {trade_perf.tot_cnt} trades and has a gain loss pct per day of : {trade_perf.gain_loss_pct_day}%, reducing open position max to 1...')
			trade_perf.restricts_open_poss_cnt_max = 1
		else:
			if debug_yn == 'Y':
				BoW(f'    * ALLOWED OPEN POSS CNT : {mkt.prod_id} has had {trade_perf.tot_cnt} trades and has a gain loss pct per day of : {trade_perf.gain_loss_pct_day}%, reducing open position max to 1...')

	# Open Position Count Checks
	if trade_perf.open_poss_cnt >= trade_perf.restricts_open_poss_cnt_max:
		RoW(f'    * CANCEL BUY MKT : {mkt.prod_id} maxed out {trade_perf.open_poss_cnt} allowed positions, max : {trade_perf.restricts_open_poss_cnt_max}, bypassing buy logic...')
		buy_deny_yn = 'Y'
	else:
		if debug_yn == 'Y':
			BoW(f'    * ALLOW BUY MKT : {mkt.prod_id} maxed out {trade_perf.open_poss_cnt} allowed positions, max : {trade_perf.restricts_open_poss_cnt_max}, bypassing buy logic...')

	# Elapsed Since Last Market Buy
	if trade_perf.restricts_buy_delay_minutes != 0 and trade_perf.last_elapsed <= trade_perf.restricts_buy_delay_minutes:
		msg = ''
		msg += f'    * CANCEL BUY MKT : '
		msg += f'{mkt.prod_id} last market buy was '
		msg += f'{trade_perf.last_elapsed} minutes ago, waiting until '
		msg += f'{trade_perf.restricts_buy_delay_minutes} minutes...'
		BoW(msg)
		buy_deny_yn = 'Y'
	else:
		if debug_yn == 'Y':
			msg = ''
			msg += f'    * ALLOW BUY MKT : '
			msg += f'{mkt.prod_id} last market buy was '
			msg += f'{trade_perf.last_elapsed} minutes ago, waiting until '
			msg += f'{trade_perf.restricts_buy_delay_minutes} minutes...'
			BoW(msg)

	# Market Is Set To Sell Immediately
	if prod_id in self.st.spot.sell.force_sell.prod_ids:
		RoW(f'    * CANCEL BUY MKT : {mkt.prod_id} is in the forced_sell.prod_ids settings, and would instantly sell...')
		buy_deny_yn = 'Y'
#		beep(3)
	else:
		if debug_yn == 'Y':
			BoW(f'    * ALLOW BUY MKT : {mkt.prod_id} is in the forced_sell.prod_ids settings, and would instantly sell...')

	# Market Is Set To Limit Only on Coinbase
	if mkt.mkt_limit_only_tf == 1:
		RoW(f'    * CANCEL BUY MKT : {mkt.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')
		buy_deny_yn = 'Y'
#		beep(3)
	else:
		if debug_yn == 'Y':
			BoW(f'    * ALLOW BUY MKT : {mkt.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')

	# Very Large Bid Ask Spread
	if mkt.prc_range_pct >= 2:
		RoW(f'    * CANCEL BUY MKT : {mkt.prod_id} has a price range variance of {mkt.prc_range_pct}, this price range looks like trouble... skipping buy')
		buy_deny_yn = 'Y'
#		beep(3)
	else:
		if debug_yn == 'Y':
			BoW(f'    * ALLOW BUY MKT : {mkt.prod_id} has a price range variance of {mkt.prc_range_pct}, this price range looks like trouble... skipping buy')

	func_end(fnc)
	return buy_deny_yn, trade_perf

#<=====>#

def buy_logic_strat_deny(self, mkt, trade_strat_perf):
	func_name = 'buy_logic_strat_deny'
	func_str = f'{lib_name}.{func_name}(mkt, trade_strat_perf)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	buy_deny_yn     = 'N'
	prod_id         = mkt.prod_id
	buy_strat_type  = trade_strat_perf.buy_strat_type
	buy_strat_name  = trade_strat_perf.buy_strat_name
	buy_strat_freq  = trade_strat_perf.buy_strat_freq
	debug_yn                  = 'Y'

	special_prod_ids = self.st.spot.buy.special_prod_ids
	if prod_id not in special_prod_ids:
		if trade_strat_perf.tot_cnt >= 10 and trade_strat_perf.gain_loss_pct_day < 0:
			msg = ''
			msg += f'    * CANCEL BUY STRAT : '
			msg += f'{mkt.prod_id} '
			msg += f'{buy_strat_name} - {buy_strat_freq} '
			msg += f'has {trade_strat_perf.tot_cnt} trades '
			msg += f'with performance {trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % '
			msg += f'reducing allowed open pos ... '
			BoW(msg)
			trade_strat_perf.restricts_strat_open_cnt_max = 1
			buy_deny_yn = 'Y'
		else:
			if debug_yn == 'Y':
				msg = ''
				msg += f'    * ALLOW BUY STRAT : '
				msg += f'{mkt.prod_id} '
				msg += f'{buy_strat_name} - {buy_strat_freq} '
				msg += f'has {trade_strat_perf.tot_cnt} trades '
				msg += f'with performance {trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % '
				msg += f'reducing allowed open pos ... '
				BoW(msg)

		# Max Position Count - By Market & Strat
		if trade_strat_perf.tot_cnt >= 25 and trade_strat_perf.gain_loss_pct_day < 0:
			msg = ''
			msg += f'    * CANCEL BUY STRAT : '
			msg += f'{mkt.prod_id} '
			msg += f'{buy_strat_name} - {buy_strat_freq} '
			msg += f'has {trade_strat_perf.tot_cnt} trades '
			msg += f'with a gain loss pct per day of  {trade_strat_perf.gain_loss_pct_day} % < 0 % '
			BoW(msg)
			buy_deny_yn = 'Y'
#			beep(3)
		else:
			if debug_yn == 'Y':
				msg = ''
				msg += f'    * ALLOW BUY STRAT : '
				msg += f'{mkt.prod_id} '
				msg += f'{buy_strat_name} - {buy_strat_freq} '
				msg += f'has {trade_strat_perf.tot_cnt} trades '
				msg += f'with a gain loss pct per day of  {trade_strat_perf.gain_loss_pct_day} % < 0 % '
				BoW(msg)

	# Max Positions by Strat
	if trade_strat_perf.open_cnt >= trade_strat_perf.restricts_strat_open_cnt_max:
		msg = ''
		msg += f'    * CANCEL BUY STRAT : '
		msg += f'{mkt.prod_id} '
		msg += f'{buy_strat_name} - {buy_strat_freq} '
		msg += f'has {trade_strat_perf.open_cnt} open '
		msg += f'with max {trade_strat_perf.restricts_strat_open_cnt_max} in this strat... '
		BoW(msg)
		buy_deny_yn = 'Y'
	else:
		if debug_yn == 'Y':
			msg = ''
			msg += f'    * ALLOW BUY STRAT : '
			msg += f'{mkt.prod_id} '
			msg += f'{buy_strat_name} - {buy_strat_freq} '
			msg += f'has {trade_strat_perf.open_cnt} open '
			msg += f'with max {trade_strat_perf.restricts_strat_open_cnt_max} in this strat... '
			BoW(msg)

	# time delay between same prod_id & strat buy in minutes..
	if trade_strat_perf.restricts_buy_strat_delay_minutes != 0 and trade_strat_perf.strat_last_elapsed < trade_strat_perf.restricts_buy_strat_delay_minutes:
		msg = ''
		msg += f'    * CANCEL BUY STRAT : '
		msg += f'{mkt.prod_id} last strat '
		msg += f'{buy_strat_name} - {trade_strat_perf.buy_strat_freq} buy was '
		msg += f'{trade_strat_perf.strat_last_elapsed} minutes ago, waiting until '
		msg += f'{trade_strat_perf.restricts_buy_strat_delay_minutes} minutes...'
		BoW(msg)
		buy_deny_yn = 'Y'
	else:
		if debug_yn == 'Y':
			msg = ''
			msg += f'    * ALLOW BUY STRAT : '
			msg += f'{mkt.prod_id} last strat '
			msg += f'{buy_strat_name} - {trade_strat_perf.buy_strat_freq} buy was '
			msg += f'{trade_strat_perf.strat_last_elapsed} minutes ago, waiting until '
			msg += f'{trade_strat_perf.restricts_buy_strat_delay_minutes} minutes...'
			BoW(msg)

	# adjust the strat trade size based upon spendable amt
	trade_strat_perf.target_trade_size = trade_strat_perf.trade_size
	trade_strat_perf.trade_size = mkt.quote_size_min
	while trade_strat_perf.trade_size <= trade_strat_perf.target_trade_size - 1:
		if trade_strat_perf.trade_size + 1 > mkt.spendable_amt:
			break
		trade_strat_perf.trade_size += 1
	BoW(f'trade_size : {trade_strat_perf.trade_size}, target_trade_size : {trade_strat_perf.target_trade_size}')

	# deny if trade size exceeds spendable amt
	if trade_strat_perf.trade_size > mkt.spendable_amt or trade_strat_perf.trade_size == mkt.quote_size_min:
		RoW(f'    * CANCEL LIVE BUY!!! {mkt.quote_curr_symb} balance : {mkt.bal_avail:>.2f}, reserve amount : {mkt.reserve_amt:>.2f}, spendable amount : {mkt.spendable_amt:>.2f} is below trade_size of {trade_strat_perf.trade_size:>.2f}...')
		buy_deny_yn = 'Y'
	else:
		if debug_yn == 'Y':
			BoW(f'    * ALLOW LIVE BUY!!! {mkt.quote_curr_symb} balance : {mkt.bal_avail:>.2f}, reserve amount : {mkt.reserve_amt:>.2f}, spendable amount : {mkt.spendable_amt:>.2f} is below trade_size of {trade_strat_perf.trade_size:>.2f}...')

	func_end(fnc)
	return buy_deny_yn, trade_strat_perf

#<=====>#

def buy_ords_check(self):
	func_name = 'buy_ords_check'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=3)
	# G(func_str)

	try:
		bos = db_buy_ords_open_get()
		if bos:
			print_adv(2)
			WoM(f"{'Buy Orders Check':^200}")

			bos_cnt = len(bos)
			cnt = 0
			for bo in bos:
				cnt += 1
				bo = dec_2_float(bo)
				bo = AttrDictConv(in_dict=bo)
				test_tf = bo.test_tf

				if test_tf == 0:
					ord_id = bo.buy_order_uuid
					o = cb_ord_get(order_id=ord_id)

					if o:
						o = dec_2_float(o)
						o = AttrDictConv(in_dict=o)

						if o.prod_id != bo.prod_id:
							print(func_str)
							print('error #1 !')
							beep(2)
							sys.exit()

						if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
							bo.buy_cnt_act                    = o.ord_filled_size
							bo.fees_cnt_act                   = o.ord_total_fees
							bo.tot_out_cnt                    = o.ord_total_value_after_fees
							bo.prc_buy_act                    = o.ord_average_filled_price # not sure this includes the fees
							bo.buy_end_dttm                   = o.ord_last_fill_time
							bo.tot_prc_buy                    = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
							if o.ord_settled:
								bo.ord_stat                   = 'FILL'
							bo.prc_buy_slip_pct               = round((bo.prc_buy_act - bo.prc_buy_est) / bo.prc_buy_est, 8)

							print(f'{cnt:>2} / {bos_cnt:>2}, prod_id : {bo.prod_id:<15}, bo_uuid : {bo.buy_order_uuid:<60}')

							db_tbl_buy_ords_insupd(bo)
							self.pos_open(bo.buy_order_uuid)

						elif o.ord_status == 'OPEN':
							print(o)
							print('WE NEED CODE HERE!!!')
							beep(2)

						else:
							print(func_str)
							print('error #2 !')
							beep(2)
							db_buy_ords_stat_upd(bo_id=bo.bo_id, ord_stat='ERR')

				elif test_tf == 1:
					bo.ord_stat = 'FILL'
					db_tbl_buy_ords_insupd(bo)
					self.pos_open(bo.buy_order_uuid)

			print_adv(2)

	except Exception as e:
		print(f'{func_name} ==> errored... {type(e)} {e}')
		traceback.print_exc()
		traceback.print_stack()
		print(f'so : {bo}')
		print(f'ord_id : {ord_id}')
		print(f'o : {o}')
		sys.exit()

	func_end(fnc)

#<=====>#

def buy_header(self, prod_id):
	func_name = 'buy_header'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	hmsg = ""
	hmsg += f"{'mkt':<15} | "
	hmsg += f"{'strat':<15} | "
	hmsg += f"{'freq':<15} | "
	hmsg += f"{'total':^5} | "
	hmsg += f"{'open':^5} | "
	hmsg += f"{'close':^5} | "
	hmsg += f"{'wins':^5} | "
	hmsg += f"{'lose':^5} | "
	hmsg += f"{'win':^6} % | "
	hmsg += f"{'lose':^6} % | "
	hmsg += f"{'gain_amt':^10} | "
	hmsg += f"{'gain_pct':^10} % | "
	hmsg += f"{'gain_hr':^10} % | "
	hmsg += f"{'gain_day':^10} % | "
	hmsg += f"{'elapsed':<7} | "
	hmsg += f"{'trade_size':^16} |  | "
	hmsg += f"{'pass':^4} | "
	hmsg += f"{'fail':^4} | "
	hmsg += f"{'test':^6} % | "

	title_msg = f'* BUY LOGIC * {prod_id} *'
	chart_mid(in_str=title_msg, len_cnt=240, bold=True)
	chart_headers(in_str=hmsg, len_cnt=240, bold=True)
	self.show_buy_header_tf = False

	func_end(fnc)

#<=====>#

def disp_buy(self, mkt, trade_strat_perf):
	func_name = 'disp_buy'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id          = mkt.prod_id
	show_tests_yn    = self.st.spot.buy.show_tests_yn
	show_tests_min   = self.st.spot.buy.show_tests_min

	if self.show_buy_header_tf:
		self.buy_header(prod_id)
		self.show_buy_header_tf = False

	msg1 = ''
	msg1 += f'{trade_strat_perf.prod_id:<15}' + ' | '
	msg1 += f'{trade_strat_perf.buy_strat_name:<15}' + ' | '
	msg1 += f'{trade_strat_perf.buy_strat_freq:<15}' + ' | '
	msg1 += f'{int(trade_strat_perf.tot_cnt):>5}' + ' | '
	msg1 += f'{int(trade_strat_perf.open_cnt):^2}/{int(trade_strat_perf.restricts_strat_open_cnt_max):^2}' + ' | '
	msg1 += f'{int(trade_strat_perf.close_cnt):>5}' + ' | '
	msg1 += f'{int(trade_strat_perf.win_cnt):>5}' + ' | '
	msg1 += f'{int(trade_strat_perf.lose_cnt):>5}' + ' | '
	msg1 += f'{trade_strat_perf.win_pct:>6.2f} %' + ' | '
	msg1 += f'{trade_strat_perf.lose_pct:>6.2f} %' + ' | '
	msg1 += f'{trade_strat_perf.gain_loss_amt:>10.2f}' + ' | '
	msg1 += f'{trade_strat_perf.gain_loss_pct:>10.2f} %' + ' | '
	msg1 += f'{trade_strat_perf.gain_loss_pct_hr:>10.2f} %' + ' | '
	msg1 += f'{trade_strat_perf.gain_loss_pct_day:>10.2f} %' + ' | '
	msg1 += f'{trade_strat_perf.strat_last_elapsed:>7}' + ' | '
	msg1 += f'{trade_strat_perf.trade_size:>16.8f}' + ' | '

	msg2 = ''
	msg2 += f' | {int(trade_strat_perf.pass_cnt):>4}' + ' | '
	msg2 += f'{int(trade_strat_perf.fail_cnt):>4}' + ' | '
	msg2 += f'{trade_strat_perf.pass_pct:>6.2f} %' + ' | '

	if trade_strat_perf.tot_cnt > 0:
		msg1 = cs_pct_color_50(pct=trade_strat_perf.win_pct, msg=msg1)
	msg2 = cs_pct_color_100(pct=trade_strat_perf.pass_pct, msg=msg2)

	if trade_strat_perf.pass_pct > 0:
		msg = f'{msg1}{msg2}'
		chart_row(msg, len_cnt=240)

	for msg in trade_strat_perf.all_passes:
		if trade_strat_perf.buy_yn == 'Y' or show_tests_yn in ('Y') or trade_strat_perf.pass_pct >= show_tests_min:
			msg = cs(msg, font_color='green')
			chart_row(msg, len_cnt=240)
			self.show_buy_header_tf = True

	for msg in trade_strat_perf.all_fails:
		if trade_strat_perf.buy_yn == 'Y' or show_tests_yn in ('Y') or trade_strat_perf.pass_pct >= show_tests_min:
			msg = cs(msg, font_color='red')
			chart_row(msg, len_cnt=240)
			self.show_buy_header_tf = True

	func_end(fnc)

#<=====>#

def buy_log(self, msg):
	func_name = 'buy_log'
	func_str = f'{lib_name}.{func_name}(msg)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	dt_str  = dt.now().strftime('%Y_%m_%d')
	logfile = f"logs_buy/{dt_str}_buy_log.txt"
	wmsg    = f'{dttm_get()} ==> {msg}'
	file_write(logfile, wmsg)

	func_end(fnc)

#<=====>#

def buy_sign_rec(self, mkt, trade_strat_perf):
	func_name = 'buy_sign_rec'
	func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	bs = {}
	bs["test_tf"]              = mkt.test_tf
	bs["prod_id"]              = mkt.prod_id
	bs["buy_strat_type"]       = mkt.buy_strat_type
	bs["buy_strat_name"]       = mkt.buy_strat_name
	bs["buy_strat_freq"]       = mkt.buy_strat_freq
	bs["buy_yn"]               = trade_strat_perf.buy_yn
	bs["wait_yn"]              = trade_strat_perf.wait_yn
	bs["buy_curr_symb"]        = mkt.base_curr_symb
	bs["spend_curr_symb"]      = mkt.quote_curr_symb
	bs["fees_curr_symb"]       = mkt.quote_curr_symb
	bs["buy_tot_est"]          = round(trade_strat_perf.trade_size, 8)
	bs["buy_fees_est"]         = round(trade_strat_perf.trade_size * 0.0025, 8)
	bs["buy_sub_tot_est"]      = bs["buy_tot_est"] - bs["buy_fees_est"]
	bs["buy_prc_est"]          = mkt.prc_buy
	bs["buy_cnt_est"]          = round(bs["buy_sub_tot_est"] / bs["buy_prc_est"],8)

	bs["all_passes"]           = ''
	bs["all_fails"]            = ''

	# Update to Database
	db_tbl_buy_signs_insupd(bs)

	func_end(fnc)

#<=====>#

def ord_mkt_buy(self, mkt, trade_strat_perf):
	func_name = 'ord_mkt_buy'
	func_str = f'{lib_name}.{func_name}(mkt)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id               = mkt.prod_id
	spend_amt             = str(trade_strat_perf.trade_size)

	print(f'{func_name} => order = cb.fiat_market_buy(prod_id={prod_id}, spend_amt={spend_amt})')
	order = cb.fiat_market_buy(prod_id, spend_amt)
	self.refresh_wallet_tf       = True
	time.sleep(0.33)

	ord_id = order.id

	o = cb_ord_get(order_id=ord_id)
	time.sleep(0.33)

	bo = None
	if o:
		bo = AttrDict()
		bo.prod_id               = mkt.prod_id
		bo.pos_type              = 'SPOT'
		bo.ord_stat              = 'OPEN'
		bo.buy_strat_type        = mkt.buy_strat_type
		bo.buy_strat_name        = mkt.buy_strat_name
		bo.buy_strat_freq        = mkt.buy_strat_freq
		bo.buy_order_uuid        = ord_id
		bo.buy_begin_dttm        = dt.now()
		bo.buy_curr_symb         = mkt.base_curr_symb
		bo.spend_curr_symb       = mkt.quote_curr_symb
		bo.fees_curr_symb        = mkt.quote_curr_symb
		bo.buy_cnt_est           = (mkt.trade_size * 0.996) / mkt.prc_buy
		bo.prc_buy_est           = mkt.prc_buy
		db_tbl_buy_ords_insupd(bo)
		time.sleep(.33)
	else:
		print(f'{func_name} exit 1 : {o}')
		print(f'{func_name} exit 1 : {bo}')
		sys.exit()

	func_end(fnc)

#<=====>#

def ord_mkt_buy_orig(self, mkt, trade_strat_perf):
	func_name = 'ord_mkt_buy_orig'
	func_str = f'{lib_name}.{func_name}(mkt)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	client_order_id = cb_client_order_id()
	prod_id               = mkt.prod_id
	spend_amt             = trade_strat_perf.trade_size

	oc = {}
	oc['market_market_ioc'] = {}
	oc['market_market_ioc']['quote_size'] = str(spend_amt)

	o = cb.create_order(
			client_order_id = client_order_id, 
			product_id = prod_id, 
			side = 'BUY', 
			order_configuration = oc
			)
	print(o)
	self.refresh_wallet_tf       = True
	time.sleep(0.25)

	bo = None
	if o:
		if 'success' in o:
			if o['success']:
				bo = AttrDict()
				bo.prod_id               = mkt.prod_id
				bo.pos_type              = 'SPOT'
				bo.ord_stat              = 'OPEN'
				bo.buy_strat_type        = mkt.buy_strat_type
				bo.buy_strat_name        = mkt.buy_strat_name
				bo.buy_strat_freq        = mkt.buy_strat_freq
				bo.buy_order_uuid        = o['success_response']['order_id']
				bo.buy_client_order_id   = o['success_response']['client_order_id']
				bo.buy_begin_dttm        = dt.now()
				bo.buy_curr_symb         = mkt.base_curr_symb
				bo.spend_curr_symb       = mkt.quote_curr_symb
				bo.fees_curr_symb        = mkt.quote_curr_symb
				bo.buy_cnt_est           = (spend_amt * 0.996) / mkt.prc_buy
				bo.prc_buy_est           = mkt.prc_buy
				db_tbl_buy_ords_insupd(bo)
				time.sleep(.25)
			else:
				print(f'{func_name} exit 3 : {o}')
				print(f'{func_name} exit 3 : {bo}')
				sys.exit()
		else:
			print(f'{func_name} exit 2 : {o}')
			print(f'{func_name} exit 2 : {bo}')
			sys.exit()
	else:
		print(f'{func_name} exit 1 : {o}')
		print(f'{func_name} exit 1 : {bo}')
		sys.exit()

	func_end(fnc)

#<=====>#

def ord_lmt_buy_open(self, mkt, trade_strat_perf):
	func_name = 'ord_lmt_buy_open'
	func_str = f'{lib_name}.{func_name}(mkt)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	prod_id                   = mkt.prod_id
	spend_amt                 = str(trade_strat_perf.trade_size)
	order                     = cb.fiat_limit_buy(prod_id, spend_amt, price_multiplier=".995")
	self.refresh_wallet_tf    = True
	time.sleep(0.25)

	ord_id = order.id
	o = cb_ord_get(order_id=ord_id)
	time.sleep(0.25)

	bo = None
	if o:
		bo = AttrDict()
		bo.prod_id               = mkt.prod_id
		bo.pos_type              = 'SPOT'
		bo.ord_stat              = 'OPEN'
		bo.buy_strat_type        = mkt.buy_strat_type
		bo.buy_strat_name        = mkt.buy_strat_name
		bo.buy_strat_freq        = mkt.buy_strat_freq
		bo.buy_order_uuid        = ord_id # o['success_response']['order_id']
		bo.buy_begin_dttm        = dt.now()
		bo.buy_curr_symb         = mkt.base_curr_symb
		bo.spend_curr_symb       = mkt.quote_curr_symb
		bo.fees_curr_symb        = mkt.quote_curr_symb
		bo.buy_cnt_est           = (mkt.trade_size * 0.996) / mkt.prc_buy
		bo.prc_buy_est           = mkt.prc_buy
		db_tbl_buy_ords_insupd(bo)
		time.sleep(.25)
	else:
		print(f'{func_name} exit 1 : {o}')
		print(f'{func_name} exit 1 : {bo}')
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
