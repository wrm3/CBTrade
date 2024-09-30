#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from datetime import datetime
from datetime import datetime as dt
from libs.bot_coinbase import cb, cb_client_order_id, cb_ord_get
from libs.bot_common import writeit
from libs.bot_db_read import db_mkts_open_cnt_get, db_pair_spent
from libs.bot_db_write import db_tbl_buy_ords_insupd
from libs.bot_settings import bot_settings_get, debug_settings_get, get_lib_func_secs_max, mkt_settings_get, pair_settings_get
from libs.bot_strats_buy import buy_strats_check, buy_strats_deny, buy_strats_get
from libs.cls_settings import AttrDict, Settings
from libs.lib_charts import chart_bottom, chart_headers, chart_mid, chart_row, chart_top
from libs.lib_colors import BoW, G, GoW, R, RoW, WoB, WoG, WoM, WoR, YoK, cp, cs
from libs.lib_common import AttrDictConv, beep, dec_2_float, dttm_get, func_begin, func_end, speak_async
from libs.bot_theme import cs_pct_color_50, cs_pct_color_100
import decimal
import os
import pandas as pd 
import sys
import time
import traceback
import uuid


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_cls_pair'
log_name      = 'bot_cls_pair'
lib_secs_max  = 2

# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)
# print(f'{lib_name}, lib_secs_max : {lib_secs_max}')


#<=====>#
# Classes
#<=====>#

class BUY(AttrDict):

	def __init__(buy, mkt, pair):
		buy.class_name                 = 'BUY'
		buy.mkt                        = mkt
		buy.pair                       = pair
		for k, v in pair.items():
			buy[k] = v
		buy.trade_perf                 = pair.trade_perf
		buy.trade_strat_perfs          = pair.trade_strat_perfs
		buy.ta                         = pair.ta
		buy.budget                     = buy.mkt.budget
		buy.symb                       = buy.mkt.symb
		buy.dst, buy.debug_settings    = debug_settings_get()
		buy.bst, buy.bot_settings      = bot_settings_get()
		buy.mst, buy.mkt_settings      = mkt_settings_get(symb=buy.symb)
		buy.pst                        = pair_settings_get(symb=buy.symb, prod_id = buy.prod_id)
		buy.pst                        = AttrDictConv(in_dict=buy.pst)
		buy.buy_strats                 = buy_strats_get()
		buy.reserve_locked_tf          = True
		buy.show_buy_header_tf         = True

	#<=====>#

	def main_loop(buy):
		func_name = 'main_loop'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id                   = buy.prod_id
		buy.buy_signals               = []
		buy.buy_header()
		buy.show_buy_header_tf        = False

		# buy.trade_strat_perf.buy_yn                = 'N'
		# buy.trade_strat_perf.buy_deny_yn           = 'N'

		# Returns
		# skip buy logic if the prod_id not in the buy_pairs (ie it has positions to sell)
		if prod_id not in buy.mkt.buy_pairs:
			RoW(f'{prod_id} not in buy_pairs, bypassing buy logic...')
			func_end(fnc)
			return buy

		# skip buy logic if ta is not present
		if not buy.ta:
			RoW(f'{prod_id} was not successful collecting ta, bypassing buy logic...')
			func_end(fnc)
			return buy

		buy.buy_logic_mkt_boosts()

		# loop throug all buy tests
		for trade_strat_perf in buy.trade_strat_perfs:
#			print(trade_strat_perf)


			buy.trade_strat_perf                          = trade_strat_perf

			# format trade_strat_perf
			buy.trade_strat_perf                          = dec_2_float(buy.trade_strat_perf)
			buy.trade_strat_perf                          = AttrDictConv(in_dict=buy.trade_strat_perf)

			# set default values
			buy.trade_strat_perf.buy_yn                   = 'N'
			buy.trade_strat_perf.buy_deny_yn              = 'N'
			buy.trade_strat_perf.wait_yn                  = 'Y'

			# default trade size & open position max
			buy.trade_strat_perf.trade_size                    = buy.pst.buy.trade_size
			buy.trade_strat_perf.restricts_strat_open_cnt_max  = buy.pst.buy.strat_open_cnt_max 

			# get strat performance boots
			# adjusts trade size & open position max
			buy.buy_logic_strat_boosts()

			# perform buy strategy checks
			buy = buy_strats_check(buy)

			# display
			buy.disp_buy()

			# these will have been checked before hand unless we forced the tests anyways
			if buy.trade_strat_perf.buy_yn == 'Y':

				buy.buy_size_budget_calc()
				buy.disp_budget()

				# bot deny
				if buy.trade_strat_perf.buy_deny_yn == 'N':
					buy.buy_logic_deny()

				# mkt deny
				if buy.trade_strat_perf.buy_deny_yn == 'N':
					buy.buy_logic_mkt_deny()

				# strat deny
				if buy.trade_strat_perf.buy_deny_yn == 'N':
					buy.buy_logic_strat_deny()

				if buy.trade_strat_perf.buy_deny_yn == 'N':
					buy = buy_strats_deny(buy)

				if buy.trade_strat_perf.buy_deny_yn == 'N':
					buy.buy_size_budget_calc()

			dttm = dttm_get()
			if buy.trade_strat_perf.buy_yn == 'Y':

				WoM(f'bot.buy_logic !!! * buy_yn : {buy.trade_strat_perf.buy_yn} * buy_deny_yn : {buy.trade_strat_perf.buy_deny_yn}')

				buy.show_buy_header_tf = True
				if buy.trade_strat_perf.buy_deny_yn == 'N':
					buy.buy_live()
					txt = '!!! BUY !!!'
					m = '{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f} * STRAT: {}'
					msg = m.format(dttm, txt, buy.prc_buy, buy.trade_strat_perf.trade_size, buy.mkt.budget.bal_avail, buy.buy_strat_name)
					WoG(msg)
					WoG(msg)
					WoG(msg)
					symb = prod_id.split(',')[0]
					msg = f'buying {symb} for {buy.trade_strat_perf.trade_size} USDC with strategy {buy.buy_strat_name} on the {buy.buy_strat_freq} timeframe'
					WoG(msg)

					if buy.pst.speak_yn == 'Y': speak_async(msg)

					buy.trade_perf.bo_elapsed        = 0
					buy.trade_perf.pos_elapsed       = 0
					buy.trade_perf.last_elapsed      = 0
					buy.trade_perf.open_poss_cnt     += 1

					buy.mkt.budget.bal_avail                -= buy.trade_strat_perf.trade_size
					buy.mkt.budget.spendable_amt            -= buy.trade_strat_perf.trade_size

					msg = f'{buy.quote_curr_symb} * Balance : ${buy.mkt.budget.bal_avail:>.2f} * Reserve : ${buy.mkt.budget.reserve_amt:>.2f} * Spendable : ${buy.mkt.budget.spendable_amt:>.2f} * '
					WoG(msg)

				elif buy.trade_strat_perf.buy_deny_yn == 'Y':
					if prod_id in buy.mkt.buy_pairs:
						if buy.pst.buy.allow_tests_yn == 'Y':
							if buy.trade_strat_perf.open_cnt == 0:
								txt = '!!! BUY * TEST * !!!'
								m = '{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f} * STRAT: {}'
								msg = m.format(dttm, txt, buy.prc_buy, buy.trade_strat_perf.trade_size, buy.mkt.budget.bal_avail, buy.buy_strat_name)
								WoG(msg)
								WoG(msg)
								WoG(msg)

								buy.buy_test()

			elif buy.trade_strat_perf.buy_yn == 'N' :
				txt = '!!! WAIT !!!'
				m = '{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f}'
				msg = m.format(dttm, txt, buy.prc_buy, buy.trade_strat_perf.trade_size, buy.mkt.budget.bal_avail)
	#			BoW(msg)

			buy.buy_save()

		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)

		# fix me
		# this should return buy.mkt & buy.pair, if anything in buy.pair is even changed... 
		return buy.mkt, buy

	#<=====>#

	def buy_logic_mkt_boosts(buy):
		func_name = 'buy_logic_mkt_boosts'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		# get default open position max for strat
		# add double override logic strat + prod
		# fixme
		buy.trade_perf.restricts_open_poss_cnt_max = buy.pst.buy.open_poss_cnt_max 

		# Open Position Count Checks Performance Based
		# Boost allowed max positions based upon past performance
		if buy.trade_perf.tot_cnt >= 5 and buy.trade_perf.gain_loss_pct_day > 0.1:
			buy.trade_perf.restricts_open_poss_cnt_max *= 2
			if buy.pst.buy.show_boosts_yn == 'Y':
				msg = ''
				msg += f'    * BOOST BUY STRAT : '
				msg += f'{buy.prod_id} '
				msg += f'has {buy.trade_perf.tot_cnt} trades '
				msg += f'with performance {buy.trade_perf.gain_loss_pct_day:>.8f} % < 0 % '
				msg += f'boosting allowed open pos ... '
				msg = cs(msg, font_color='blue', bg_color='white')
				chart_row(msg, len_cnt= 240)

		func_end(fnc)

	#<=====>#

	def buy_logic_strat_boosts(buy):
		func_name = 'buy_logic_strat_boosts'
		func_str = f'{lib_name}.{func_name}(mkt, trade_strat_perf)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id                   = buy.prod_id
		buy.buy_strat_type       = buy.trade_strat_perf.buy_strat_type
		buy.buy_strat_name       = buy.trade_strat_perf.buy_strat_name
		buy.buy_strat_freq       = buy.trade_strat_perf.buy_strat_freq

		# get default open position max for strat
		# add double override logic strat + prod
		# fixme
		buy.trade_strat_perf.restricts_strat_open_cnt_max = buy.pst.buy.strat_open_cnt_max 

		# Open Position Count Checks Performance Based
		# Boost allowed max positions based upon past performance
		if buy.trade_strat_perf.tot_cnt >= 25 and buy.trade_strat_perf.gain_loss_pct_day > 1:
			buy.trade_strat_perf.restricts_strat_open_cnt_max *= 2
			if buy.pst.buy.show_boosts_yn == 'Y':
				msg = ''
				msg += f'    * BOOST BUY STRAT : '
				msg += f'{buy.prod_id} '
				msg += f'{buy.buy_strat_name} - {buy.buy_strat_freq} '
				msg += f'has {buy.trade_strat_perf.tot_cnt} trades '
				msg += f'with performance {buy.trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % '
				msg += f'boosting allowed open pos ... '
				msg = cs(msg, font_color='blue', bg_color='white')
				chart_row(msg, len_cnt= 240)

		# get default open position max for strat
		# Assign Min Value For New Market + Strat with little history or poor performance
		trade_size_min_mult        = buy.pst.buy.trade_size_min_mult
		trade_size                 = buy.quote_size_min * trade_size_min_mult
		tests_min                  = buy.pst.buy.strats[buy.buy_strat_name].tests_min[buy.buy_strat_freq] 
		boost_tests_min            = buy.pst.buy.strats[buy.buy_strat_name].boost_tests_min[buy.buy_strat_freq] 

		# give default value to strat with some history and positive impact
		if buy.trade_strat_perf.tot_cnt >= tests_min and buy.trade_strat_perf.gain_loss_pct_day > 0:
			trade_size             = buy.pst.buy.trade_size 
		# give default value to strat with some history and positive impact
		elif buy.trade_strat_perf.tot_cnt >= 5 and buy.trade_strat_perf.win_pct >= 75:
			trade_size             = buy.pst.buy.trade_size 

		# Kid has potential, lets give it a little more earlier
		if buy.trade_strat_perf.tot_cnt >= 3 and buy.trade_strat_perf.gain_loss_pct_day > 0.05:
			trade_size             *= 2
		# Boost those with proven track records
		if buy.trade_strat_perf.tot_cnt >= tests_min and buy.trade_strat_perf.gain_loss_pct_day > 0.1:
			trade_size             *= 2
		# Boost those with proven track records
		if buy.trade_strat_perf.tot_cnt >= boost_tests_min and buy.trade_strat_perf.gain_loss_pct_day > 0.25:
			trade_size             *= 2
		# Boost those with proven track records
		if buy.trade_strat_perf.tot_cnt >= boost_tests_min and buy.trade_strat_perf.gain_loss_pct_day > 0.5:
			trade_size             *= 2
		# Boost those with proven track records
		if buy.trade_strat_perf.tot_cnt >= boost_tests_min and buy.trade_strat_perf.gain_loss_pct_day > 1:
			trade_size             *= 2
		# Boost those with proven track records
		if buy.trade_strat_perf.tot_cnt >= boost_tests_min and buy.trade_strat_perf.gain_loss_pct_day > 2:
			trade_size             *= 2
		# Boost those with proven track records
		if buy.trade_strat_perf.tot_cnt >= boost_tests_min and buy.trade_strat_perf.gain_loss_pct_day > 4:
			trade_size             *= 2

		if buy.pst.buy.show_boosts_yn == 'Y':
			msg = ''
			msg += f'    * BOOST BUY STRAT : {buy.prod_id} {buy.buy_strat_name} - {buy.buy_strat_freq} has {buy.trade_strat_perf.tot_cnt} trades '
			msg += f'with performance {buy.trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % boosting trade_size ${trade_size} ... '
			msg = cs(msg, font_color='blue', bg_color='white')
			chart_row(msg, len_cnt= 240)

		# assign final trade_size
		buy.trade_strat_perf.trade_size = trade_size

		func_end(fnc)

	#<=====>#

	def buy_logic_deny(buy):
		func_name = 'buy_logic_deny'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		buy.trade_strat_perf.buy_deny_yn               = 'N'

		if buy.pst.buy.buying_on_yn == 'N' :
			RoW(f'    * CANCEL BUY : buying has been turned off in settings...')
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		mkts_open_max = buy.pst.buy.mkts_open_max
		mkts_open_cnt = db_mkts_open_cnt_get()
		if buy.trade_perf.open_poss_cnt == 0 and mkts_open_cnt >= mkts_open_max:
			RoW(f'    * CANCEL BUY MKT : {buy.prod_id} maxed out {mkts_open_cnt} different markets, max : {mkts_open_max}...')
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		func_end(fnc)

	#<=====>#

	def buy_logic_mkt_deny(buy):
		func_name = 'buy_logic_mkt_deny'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id                   = buy.prod_id

		# # fixme
		# if buy.budget[trade_curr].spent_amt >= buy.budget[trade_curr].spend_max_amt:
		# 	msg = cs(f'We have spent our entire {trade_curr} budget... spent : {buy.budget[trade_curr].spent_amt} / {buy.budget[trade_curr].spend_max_amt} max...', 'white', 'red')
		# else:
		# 	msg = cs(f'We have more {trade_curr} budget to spend... spent : {buy.budget[trade_curr].spent_amt} / {buy.budget[trade_curr].spend_max_amt} max...', 'white', 'red')
		# buy.budget_display(trade_curr, title=t, footer=msg)
		# if buy.budget[trade_curr].spent_amt >= buy.budget[trade_curr].spend_max_amt:
		# 	if len(buy.pst.trade_currs) == 1:
		# 		time.sleep(30)
		# 	return

		# Open Position Count Checks Lower Good Performance
		special_prod_ids = buy.pst.buy.special_prod_ids
		if prod_id not in special_prod_ids:
			# Limit Max Position Count - By Market
			if buy.trade_perf.tot_cnt >= 10 and buy.trade_perf.gain_loss_pct_day < 0:
				RoW(f'    * LOWER OPEN POSS CNT : {buy.prod_id} has had {buy.trade_perf.tot_cnt} trades and has a gain loss pct per day of : {buy.trade_perf.gain_loss_pct_day}%, reducing open position max to 1...')
				buy.trade_perf.restricts_open_poss_cnt_max = 1

		# Open Position Count Checks
		if buy.trade_perf.open_poss_cnt >= buy.trade_perf.restricts_open_poss_cnt_max:
			RoW(f'    * CANCEL BUY MKT : {buy.prod_id} maxed out {buy.trade_perf.open_poss_cnt} allowed positions, max : {buy.trade_perf.restricts_open_poss_cnt_max}, bypassing buy logic...')
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		# Elapsed Since Last Market Buy
		if buy.trade_perf.restricts_buy_delay_minutes != 0 and buy.trade_perf.last_elapsed <= buy.trade_perf.restricts_buy_delay_minutes:
			msg = ''
			msg += f'    * CANCEL BUY MKT : '
			msg += f'{buy.prod_id} last market buy was '
			msg += f'{buy.trade_perf.last_elapsed} minutes ago, waiting until '
			msg += f'{buy.trade_perf.restricts_buy_delay_minutes} minutes...'
			BoW(msg)
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		# Market Is Set To Sell Immediately
		if prod_id in buy.pst.sell.force_sell.prod_ids:
			RoW(f'    * CANCEL BUY MKT : {buy.prod_id} is in the forced_sell.prod_ids settings, and would instantly sell...')
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		# Market Is Set To Limit Only on Coinbase
		if buy.mkt_limit_only_tf == 1:
			RoW(f'    * CANCEL BUY MKT : {buy.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		# Very Large Bid Ask Spread
		if buy.prc_range_pct >= 2:
			RoW(f'    * CANCEL BUY MKT : {buy.prod_id} has a price range variance of {buy.prc_range_pct}, this price range looks like trouble... skipping buy')
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		func_end(fnc)

	#<=====>#

	def buy_logic_strat_deny(buy):
		func_name = 'buy_logic_strat_deny'
		func_str = f'{lib_name}.{func_name}(mkt, trade_strat_perf)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id         = buy.prod_id
		buy_strat_type  = buy.trade_strat_perf.buy_strat_type
		buy_strat_name  = buy.trade_strat_perf.buy_strat_name
		buy_strat_freq  = buy.trade_strat_perf.buy_strat_freq

		special_prod_ids = buy.pst.buy.special_prod_ids
		if prod_id not in special_prod_ids:
			if buy.trade_strat_perf.tot_cnt >= 10 and buy.trade_strat_perf.gain_loss_pct_day < 0:
				msg = ''
				msg += f'    * CANCEL BUY STRAT : '
				msg += f'{buy.prod_id} '
				msg += f'{buy_strat_name} - {buy_strat_freq} '
				msg += f'has {buy.trade_strat_perf.tot_cnt} trades '
				msg += f'with performance {buy.trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % '
				msg += f'reducing allowed open pos ... '
				BoW(msg)
				buy.trade_strat_perf.restricts_strat_open_cnt_max = 1
				buy.trade_strat_perf.buy_deny_yn = 'Y'

			# Max Position Count - By Market & Strat
			if buy.trade_strat_perf.tot_cnt >= 25 and buy.trade_strat_perf.gain_loss_pct_day < 0:
				msg = ''
				msg += f'    * CANCEL BUY STRAT : '
				msg += f'{buy.prod_id} '
				msg += f'{buy_strat_name} - {buy_strat_freq} '
				msg += f'has {buy.trade_strat_perf.tot_cnt} trades '
				msg += f'with a gain loss pct per day of  {buy.trade_strat_perf.gain_loss_pct_day} % < 0 % '
				BoW(msg)
				buy.trade_strat_perf.buy_deny_yn = 'Y'

		# Max Positions by Strat
		if buy.trade_strat_perf.open_cnt >= buy.trade_strat_perf.restricts_strat_open_cnt_max:
			msg = ''
			msg += f'    * CANCEL BUY STRAT : '
			msg += f'{buy.prod_id} '
			msg += f'{buy_strat_name} - {buy_strat_freq} '
			msg += f'has {buy.trade_strat_perf.open_cnt} open '
			msg += f'with max {buy.trade_strat_perf.restricts_strat_open_cnt_max} in this strat... '
			BoW(msg)
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		# time delay between same prod_id & strat buy in minutes..
		if buy.trade_strat_perf.restricts_buy_strat_delay_minutes != 0 and buy.trade_strat_perf.strat_last_elapsed < buy.trade_strat_perf.restricts_buy_strat_delay_minutes:
			msg = ''
			msg += f'    * CANCEL BUY STRAT : '
			msg += f'{buy.prod_id} last strat '
			msg += f'{buy_strat_name} - {buy.trade_strat_perf.buy_strat_freq} buy was '
			msg += f'{buy.trade_strat_perf.strat_last_elapsed} minutes ago, waiting until '
			msg += f'{buy.trade_strat_perf.restricts_buy_strat_delay_minutes} minutes...'
			BoW(msg)
			buy.trade_strat_perf.buy_deny_yn = 'Y'

		func_end(fnc)

	#<=====>#

	def buy_header(buy):
		func_name = 'buy_header'
		func_str = f'{lib_name}.{func_name}()'
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

		title_msg = f'* BUY LOGIC * {buy.prod_id} *'
		chart_mid(in_str=title_msg, len_cnt=240, bold=True)
		chart_headers(in_str=hmsg, len_cnt=240, bold=True)
		buy.show_buy_header_tf = False

		func_end(fnc)

	#<=====>#

	def disp_buy(buy):
		func_name = 'disp_buy'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id          = buy.prod_id

		if buy.show_buy_header_tf:
			buy.buy_header()
			buy.show_buy_header_tf = False

		msg1 = ''
		msg1 += f'{buy.trade_strat_perf.prod_id:<15}' + ' | '
		msg1 += f'{buy.trade_strat_perf.buy_strat_name:<15}' + ' | '
		msg1 += f'{buy.trade_strat_perf.buy_strat_freq:<15}' + ' | '
		msg1 += f'{int(buy.trade_strat_perf.tot_cnt):>5}' + ' | '
		msg1 += f'{int(buy.trade_strat_perf.open_cnt):^2}/{int(buy.trade_strat_perf.restricts_strat_open_cnt_max):^2}' + ' | '
		msg1 += f'{int(buy.trade_strat_perf.close_cnt):>5}' + ' | '
		msg1 += f'{int(buy.trade_strat_perf.win_cnt):>5}' + ' | '
		msg1 += f'{int(buy.trade_strat_perf.lose_cnt):>5}' + ' | '
		msg1 += f'{buy.trade_strat_perf.win_pct:>6.2f} %' + ' | '
		msg1 += f'{buy.trade_strat_perf.lose_pct:>6.2f} %' + ' | '
		msg1 += f'{buy.trade_strat_perf.gain_loss_amt:>10.2f}' + ' | '
		msg1 += f'{buy.trade_strat_perf.gain_loss_pct:>10.2f} %' + ' | '
		msg1 += f'{buy.trade_strat_perf.gain_loss_pct_hr:>10.2f} %' + ' | '
		msg1 += f'{buy.trade_strat_perf.gain_loss_pct_day:>10.2f} %' + ' | '
		msg1 += f'{buy.trade_strat_perf.strat_last_elapsed:>7}' + ' | '
		msg1 += f'{buy.trade_strat_perf.trade_size:>16.8f}' + ' | '

		msg2 = ''
		msg2 += f' | {int(buy.trade_strat_perf.pass_cnt):>4}' + ' | '
		msg2 += f'{int(buy.trade_strat_perf.fail_cnt):>4}' + ' | '
		msg2 += f'{buy.trade_strat_perf.pass_pct:>6.2f} %' + ' | '

		if buy.trade_strat_perf.tot_cnt > 0:
			msg1 = cs_pct_color_50(pct=buy.trade_strat_perf.win_pct, msg=msg1)
		msg2 = cs_pct_color_100(pct=buy.trade_strat_perf.pass_pct, msg=msg2)

		if buy.trade_strat_perf.pass_pct > 0:
			msg = f'{msg1}{msg2}'
			chart_row(msg, len_cnt=240)

		if buy.trade_strat_perf.buy_yn == 'Y' or buy.pst.buy.show_tests_yn in ('Y') or buy.trade_strat_perf.pass_pct >= buy.pst.buy.show_tests_min:
			for msg in buy.trade_strat_perf.all_passes:
				msg = cs(msg, font_color='green')
				chart_row(msg, len_cnt=240)
				buy.show_buy_header_tf = True

		if buy.trade_strat_perf.buy_yn == 'Y' or buy.pst.buy.show_tests_yn in ('Y') or buy.trade_strat_perf.pass_pct >= buy.pst.buy.show_tests_min:
			for msg in buy.trade_strat_perf.all_fails:
				msg = cs(msg, font_color='red')
				chart_row(msg, len_cnt=240)
				buy.show_buy_header_tf = True

		func_end(fnc)

	#<=====>#

	def buy_size_budget_calc(buy):
		func_name = 'buy_size_budget_calc'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		buy.mkt.budget.pair_spent_amt            = 0
		buy.mkt.budget.pair_spent_up_amt         = 0
		buy.mkt.budget.pair_spent_dn_amt         = 0
		buy.mkt.budget.pair_spent_pct            = 0
		buy.mkt.budget.pair_spent_up_pct         = 0
		buy.mkt.budget.pair_spent_dn_pct         = 0

		buy.mkt.budget.pair_spend_max_amt        = buy.mkt.budget.spend_max_amt * (buy.pst.budget.mkt_shares / 100)
		buy.mkt.budget.pair_spend_up_max_amt     = buy.mkt.budget.pair_spend_max_amt * (buy.pst.budget.spend_up_max_pct / 100)
		buy.mkt.budget.pair_spend_dn_max_amt     = buy.mkt.budget.pair_spend_max_amt * (buy.pst.budget.spend_dn_max_pct / 100)

		# Get Pair Data
		pair_spent_data                = db_pair_spent(buy.prod_id)
		pair_spent_data                = dec_2_float(pair_spent_data)
		pair_spent_data                = AttrDictConv(in_dict=pair_spent_data)

		if pair_spent_data:
			buy.mkt.budget.pair_open_cnt             = pair_spent_data.open_cnt
			buy.mkt.budget.pair_open_up_cnt          = pair_spent_data.open_up_cnt
			buy.mkt.budget.pair_open_dn_cnt          = pair_spent_data.open_dn_cnt
			buy.mkt.budget.pair_open_dn_pct          = pair_spent_data.open_up_pct
			buy.mkt.budget.pair_open_dn_pct          = pair_spent_data.open_dn_pct

			buy.mkt.budget.pair_spent_amt            = pair_spent_data.spent_amt
			buy.mkt.budget.pair_spent_pct            = round((buy.mkt.budget.pair_spent_amt / buy.mkt.budget.pair_spend_max_amt) * 100, 2)
			buy.mkt.budget.pair_spent_up_amt         = pair_spent_data.spent_up_amt
			buy.mkt.budget.pair_spent_up_pct         = round((buy.mkt.budget.pair_spent_up_amt / buy.mkt.budget.pair_spend_up_max_amt) * 100, 2)
			buy.mkt.budget.pair_spent_dn_amt         = pair_spent_data.spent_dn_amt
			buy.mkt.budget.pair_spent_dn_pct         = round((buy.mkt.budget.pair_spent_dn_amt / buy.mkt.budget.pair_spend_dn_max_amt) * 100, 2)

		color_changed_tf = False
		disp_font_color = 'white'
		disp_bg_color   = 'red'
		# adjust the strat trade size based upon spendable amt
		buy.trade_strat_perf.target_trade_size = buy.trade_strat_perf.trade_size
		buy.trade_strat_perf.trade_size = buy.quote_size_min
		while buy.trade_strat_perf.trade_size <= buy.trade_strat_perf.target_trade_size - 1:
			if not color_changed_tf:
				if buy.trade_strat_perf.trade_size > buy.quote_size_min:
					disp_bg_color   = 'blue'
					color_changed_tf = True

			# General Spending
			if buy.mkt.budget.spent_amt + buy.trade_strat_perf.trade_size + buy.quote_size_min > buy.mkt.budget.spend_max_amt:
				msg = ''
				msg += '    * '
				msg += f'mkt.budget.spent_amt : {buy.mkt.budget.spent_amt:>12.6f} '
				msg += ' + '
				msg += f'trade_size  : {buy.trade_strat_perf.trade_size:>12.6f} + '
				msg += ' + '
				msg += f'quote_size_min  : {buy.quote_size_min:>12.6f} + '
				msg += f' > '
				msg += f'buy.mkt.budget.spend_max_amt : {buy.mkt.budget.spend_max_amt:>12.6f}'
				msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
				chart_row(in_str=msg, len_cnt=240)
				break

			# Pair Spending
			if buy.mkt.budget.pair_spent_amt + buy.trade_strat_perf.trade_size + buy.quote_size_min > buy.mkt.budget.pair_spend_max_amt:
				msg = ''
				msg += '    * '
				msg += f'mkt.budget.pair_spent_amt : {buy.mkt.budget.pair_spent_amt:>12.6f} '
				msg += ' + '
				msg += f'trade_size : {buy.trade_strat_perf.trade_size:>12.6f} + '
				msg += ' + '
				msg += f'quote_size_min : {buy.quote_size_min:>12.6f} + '
				msg += f' > '
				msg += f'buy.mkt.budget.pair_spend_max_amt : {buy.mkt.budget.pair_spend_max_amt:>12.6f}'
				msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
				chart_row(in_str=msg, len_cnt=240)
				break

			# Up Strategies
			if buy.trade_strat_perf.buy_strat_type == 'up':

				# General Up Strategy Spending
				if buy.mkt.budget.spent_up_amt + buy.trade_strat_perf.trade_size + buy.quote_size_min > buy.mkt.budget.spend_up_max_amt:
					msg = ''
					msg += '    * '
					msg += f'mkt.budget.spent_up_amt : {buy.mkt.budget.spent_up_amt:>12.6f} '
					msg += ' + '
					msg += f'trade_size : {buy.trade_strat_perf.trade_size:>12.6f} + '
					msg += ' + '
					msg += f'quote_size_min : {buy.quote_size_min:>12.6f} + '
					msg += f' > '
					msg += f'buy.mkt.budget.spend_up_max_amt : {buy.mkt.budget.spend_up_max_amt:>12.6f}'
					msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
					chart_row(in_str=msg, len_cnt=240)
					break

				# Pair Up Strategy Spending
				if buy.mkt.budget.pair_spent_up_amt + buy.trade_strat_perf.trade_size + buy.quote_size_min > buy.mkt.budget.pair_spend_up_max_amt:
					msg = ''
					msg += '    * '
					msg += f'mkt.budget.pair_spent_up_amt : {buy.mkt.budget.pair_spent_up_amt:>12.6f} '
					msg += ' + '
					msg += f'trade_size : {buy.trade_strat_perf.trade_size:>12.6f} + '
					msg += ' + '
					msg += f'quote_size_min : {buy.quote_size_min:>12.6f} + '
					msg += f' > '
					msg += f'buy.mkt.budget.pair_spend_up_max_amt : {buy.mkt.budget.pair_spend_up_max_amt:>12.6f}'
					msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
					chart_row(in_str=msg, len_cnt=240)
					break

			# Down Strategies
			if buy.trade_strat_perf.buy_strat_type == 'dn':

				# General Dn Strategy Spending
				if buy.mkt.budget.spent_dn_amt + buy.trade_strat_perf.trade_size + buy.quote_size_min > buy.mkt.budget.spend_dn_max_amt:
					msg = ''
					msg += '    * '
					msg += f'mkt.budget.spent_dn_amt : {buy.mkt.budget.spent_dn_amt:>12.6f} '
					msg += ' + '
					msg += f'trade_size : {buy.trade_strat_perf.trade_size:>12.6f} + '
					msg += ' + '
					msg += f'quote_size_min : {buy.quote_size_min:>12.6f} + '
					msg += f' > '
					msg += f'buy.mkt.budget.spend_dn_max_amt : {buy.mkt.budget.spend_dn_max_amt:>12.6f}'
					msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
					chart_row(in_str=msg, len_cnt=240)
					break

				# Pair Dn Strategy Spending
				if buy.mkt.budget.pair_spent_dn_amt + buy.trade_strat_perf.trade_size + buy.quote_size_min > buy.mkt.budget.pair_spend_dn_max_amt:
					msg = ''
					msg += '    * '
					msg += f'mkt.budget.pair_spent_dn_amt : {buy.mkt.budget.pair_spent_dn_amt:>12.6f} '
					msg += ' + '
					msg += f'trade_size : {buy.trade_strat_perf.trade_size:>12.6f} + '
					msg += ' + '
					msg += f'quote_size_min : {buy.quote_size_min:>12.6f} + '
					msg += f' > '
					msg += f'buy.mkt.budget.pair_spend_dn_max_amt : {buy.mkt.budget.pair_spend_dn_max_amt:>12.6f}'
					msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
					chart_row(in_str=msg, len_cnt=240)
					break

			# Available Funds
			if buy.trade_strat_perf.trade_size + buy.quote_size_min > buy.mkt.budget.spendable_amt:
				msg = ''
				msg += '    * '
				msg += f'trade_size : {buy.trade_strat_perf.trade_size:>12.6f} + '
				msg += ' + '
				msg += f'quote_size_min : {buy.quote_size_min:>12.6f} + '
				msg += f' > '
				msg += f'buy.mkt.budget.pair_spend_dn_max_amt : {buy.mkt.budget.spendable_amt:>12.6f}'
				msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
				chart_row(in_str=msg, len_cnt=240)
				break

			buy.trade_strat_perf.trade_size += buy.quote_size_min

		BoW(f'trade_size : {buy.trade_strat_perf.trade_size}, target_trade_size : {buy.trade_strat_perf.target_trade_size}')

		# deny if trade size exceeds spendable amt
		if buy.trade_strat_perf.trade_size == buy.quote_size_min:
			buy.trade_strat_perf.buy_deny_yn = 'Y'
			msg = cs(f'    * CANCEL LIVE BUY!!! {buy.quote_curr_symb} => budget funding => balance : {buy.mkt.budget.bal_avail:>.2f}, reserve amount : {buy.mkt.budget.reserve_amt:>.2f}, spendable amount : {buy.mkt.budget.spendable_amt:>.2f}, trade_size of {buy.trade_strat_perf.trade_size:>.2f}...', font_color='white', bg_color='red')
			chart_row(in_str=msg, len_cnt=240)

		func_end(fnc)

	#<=====>#

	def disp_budget(buy):
		func_name = 'disp_budget'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		hmsg = ""
		hmsg += f"{'lvl':<5} | "
		hmsg += f"$ {'balance':^9} | "
		hmsg += f"$ {'reserve':^9} | "
		hmsg += f"$ {'available':^9} | "
		hmsg += f"{'reserves state':^14} | "
		hmsg += f"$ {'spent':^12} | "
		hmsg += f"$ {'spent_max':^12} | "
		hmsg += f"{'spent_pct':^12} % | "
		hmsg += f"$ {'spent_up_amt':^12} | "
		hmsg += f"$ {'spent_up_max':^12} | "
		hmsg += f"{'up_pct':^12} % | "
		hmsg += f"$ {'spent_dn_amt':^12} | "
		hmsg += f"$ {'spent_dn_max':^12} | "
		hmsg += f"{'dn_pct':^12} % |"
		chart_headers(in_str=hmsg, len_cnt=240)

		disp_font_color = 'white'
		disp_bg_color   = 'green'
		if buy.mkt.budget.spent_pct >= 100 or buy.mkt.budget.spent_up_pct >= 100 or buy.mkt.budget.pair_spent_pct >= 100:
			disp_bg_color = 'red'

		msg = ""
		msg += f"{'mkt':<5} | "
		msg += cs(f"$ {buy.mkt.budget.bal_avail:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.reserve_amt:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.spendable_amt:>9.2f}", "white", "green") + " | "
		if buy.mkt.budget.reserve_locked_tf:
			msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
		else:
			msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
		msg += cs(f"$ {buy.mkt.budget.spent_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.spend_max_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"{buy.mkt.budget.spent_pct:>12.2f} %", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.spent_up_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.spend_up_max_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"{buy.mkt.budget.spent_up_pct:>12.2f} %", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.spent_dn_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.spend_dn_max_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"{buy.mkt.budget.spent_dn_pct:>12.2f} %", "white", "green") + " | "
		chart_row(in_str=msg, len_cnt=240, font_color=disp_font_color, bg_color=disp_bg_color)

		disp_font_color = 'white'
		disp_bg_color   = 'green'
		if buy.mkt.budget.pair_spent_pct >= 100 or buy.mkt.budget.pair_spent_up_pct >= 100 or buy.mkt.budget.pair_spent_dn_pct >= 100:
			disp_bg_color = 'red'

		msg = ""
		msg += f"{'pair':<5} | "
		msg += cs(f"$ {buy.mkt.budget.bal_avail:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.reserve_amt:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.spendable_amt:>9.2f}", "white", "green") + " | "
		if buy.reserve_locked_tf:
			msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
		else:
			msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
		msg += cs(f"$ {buy.mkt.budget.pair_spent_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.pair_spend_max_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"{buy.mkt.budget.pair_spent_pct:>12.2f} %", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.pair_spent_up_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.pair_spend_up_max_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"{buy.mkt.budget.pair_spent_up_pct:>12.2f} %", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.pair_spent_dn_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"$ {buy.mkt.budget.pair_spend_dn_max_amt:>12.6f}", "white", "green") + " | "
		msg += cs(f"{buy.mkt.budget.pair_spent_dn_pct:>12.2f} %", "white", "green") + " | "
		chart_row(in_str=msg, len_cnt=240, font_color=disp_font_color, bg_color=disp_bg_color)

		# Market Basics
		prod_id = buy.prod_id

		# Prices & Balances
		hmsg = ""

		msg = ""
		chart_headers(in_str=hmsg, len_cnt=240, bold=True)
		chart_row(in_str=msg, len_cnt=240)
		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)

	#<=====>#

	def buy_save(buy):
		func_name = 'buy_save'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		# Save Files
		if buy.trade_strat_perf.buy_yn == 'Y':
			if buy.pst.buy.save_files_yn == 'Y':
				fname = f"saves/{buy.prod_id}_BUY_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt"
				writeit(fname, '=== MKT ===')
				for k in buy:
					if isinstance(buy[k], [str, list, dict, float, int, decimal.Decimal, datetime, time]):
						writeit(fname, f'{k} : {buy[k]}')
					else:
						print(f'{k} : {type(buy[k])}')

		func_end(fnc)

	#<=====>#

	def buy_live(buy):
		func_name = 'buy_live'
		func_str = f'{lib_name}.{func_name}(mkt)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if buy.pst.buy.buy_limit_yn == 'Y':
			try:
				buy.ord_lmt_buy_open()
			except Exception as e:
				print(f'{func_name} ==> buy limit order failed, attempting market... {e}')
				beep(3)
				# buy.ord_mkt_buy(mkt, trade_strat_perf)
				buy.ord_mkt_buy_orig()
		else:
			# buy.ord_mkt_buy(mkt, trade_strat_perf)
			buy.ord_mkt_buy_orig()

		func_end(fnc)

	#<=====>#

	def buy_test(buy):
		func_name = 'buy_test'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		bo = AttrDict()
		bo.test_tf               = 1
		bo.symb                  = buy.symb
		bo.prod_id               = buy.prod_id
		bo.buy_order_uuid        = buy.gen_guid()
		bo.pos_type              = 'SPOT'
		bo.ord_stat              = 'OPEN'
		bo.buy_strat_type        = buy.trade_strat_perf.buy_strat_type
		bo.buy_strat_name        = buy.trade_strat_perf.buy_strat_name
		bo.buy_strat_freq        = buy.trade_strat_perf.buy_strat_freq
		bo.buy_begin_dttm        = dt.now()
		bo.buy_end_dttm          = dt.now()
		bo.buy_curr_symb         = buy.base_curr_symb
		bo.spend_curr_symb       = buy.quote_curr_symb
		bo.fees_curr_symb        = buy.quote_curr_symb
		bo.buy_cnt_est           = (buy.trade_strat_perf.target_trade_size * 0.996) / buy.prc_buy
		bo.buy_cnt_act           = (buy.trade_strat_perf.target_trade_size * 0.996) / buy.prc_buy
		bo.fees_cnt_act          = (buy.trade_strat_perf.target_trade_size * 0.004) / buy.prc_buy
		bo.tot_out_cnt           = buy.trade_strat_perf.target_trade_size
		bo.prc_buy_est           = buy.prc_buy
		bo.prc_buy_est           = buy.prc_buy
		bo.tot_prc_buy           = buy.prc_buy
		bo.prc_buy_slip_pct      = 0

		db_tbl_buy_ords_insupd(bo)
		time.sleep(.33)

		func_end(fnc)

	#<=====>#

	def gen_guid(buy):
		func_name = 'gen_guid'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		guid = str(uuid.uuid4())

		func_end(fnc)
		return guid

	#<=====>#

	def ord_mkt_buy(buy):
		func_name = 'ord_mkt_buy'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id               = buy.prod_id
		spend_amt             = str(buy.trade_strat_perf.trade_size)
		buy.refresh_wallet_tf    = True

		print(f'{func_name} => order = cb.fiat_market_buy(prod_id={prod_id}, spend_amt={spend_amt})')
		order = cb.fiat_market_buy(prod_id, spend_amt)
		buy.refresh_wallet_tf       = True
		time.sleep(0.33)

		ord_id = order.id

		o = cb_ord_get(order_id=ord_id)
		time.sleep(0.33)

		bo = None
		if o:
			bo = AttrDict()
			bo.prod_id               = buy.prod_id
			bo.symb                  = buy.symb
			bo.pos_type              = 'SPOT'
			bo.ord_stat              = 'OPEN'
			bo.buy_strat_type        = buy.buy_strat_type
			bo.buy_strat_name        = buy.buy_strat_name
			bo.buy_strat_freq        = buy.buy_strat_freq
			bo.buy_order_uuid        = ord_id
			bo.buy_begin_dttm        = dt.now()
			bo.buy_curr_symb         = buy.base_curr_symb
			bo.spend_curr_symb       = buy.quote_curr_symb
			bo.fees_curr_symb        = buy.quote_curr_symb
			bo.buy_cnt_est           = (buy.trade_size * 0.996) / buy.prc_buy
			bo.prc_buy_est           = buy.prc_buy
			db_tbl_buy_ords_insupd(bo)
			time.sleep(.33)
		else:
			print(f'{func_name} exit 1 : {o}')
			print(f'{func_name} exit 1 : {bo}')
			sys.exit()

		func_end(fnc)

	#<=====>#

	def ord_mkt_buy_orig(buy):
		func_name = 'ord_mkt_buy_orig'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		client_order_id       = cb_client_order_id()
		prod_id               = buy.prod_id
		spend_amt             = buy.trade_strat_perf.trade_size
		buy.refresh_wallet_tf    = True

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
		buy.refresh_wallet_tf       = True
		time.sleep(0.25)

		bo = None
		if o:
			if 'success' in o:
				if o['success']:
					bo = AttrDict()
					bo.prod_id               = buy.prod_id
					bo.symb                  = buy.symb
					bo.pos_type              = 'SPOT'
					bo.ord_stat              = 'OPEN'
					bo.buy_strat_type        = buy.buy_strat_type
					bo.buy_strat_name        = buy.buy_strat_name
					bo.buy_strat_freq        = buy.buy_strat_freq
					bo.buy_order_uuid        = o['success_response']['order_id']
					bo.buy_client_order_id   = o['success_response']['client_order_id']
					bo.buy_begin_dttm        = dt.now()
					bo.buy_curr_symb         = buy.base_curr_symb
					bo.spend_curr_symb       = buy.quote_curr_symb
					bo.fees_curr_symb        = buy.quote_curr_symb
					bo.buy_cnt_est           = (spend_amt * 0.996) / buy.prc_buy
					bo.prc_buy_est           = buy.prc_buy
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

	def ord_lmt_buy_open(buy):
		func_name = 'ord_lmt_buy_open'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id                   = buy.prod_id
		spend_amt                 = str(buy.trade_strat_perf.trade_size)
		order                     = cb.fiat_limit_buy(prod_id, spend_amt, price_multiplier=".995")
		buy.refresh_wallet_tf    = True
		time.sleep(0.25)

		ord_id = order.id
		o = cb_ord_get(order_id=ord_id)
		time.sleep(0.25)

		bo = None
		if o:
			bo = AttrDict()
			bo.prod_id               = buy.prod_id
			bo.symb                  = buy.symb
			bo.pos_type              = 'SPOT'
			bo.ord_stat              = 'OPEN'
			bo.buy_strat_type        = buy.buy_strat_type
			bo.buy_strat_name        = buy.buy_strat_name
			bo.buy_strat_freq        = buy.buy_strat_freq
			bo.buy_order_uuid        = ord_id # o['success_response']['order_id']
			bo.buy_begin_dttm        = dt.now()
			bo.buy_curr_symb         = buy.base_curr_symb
			bo.spend_curr_symb       = buy.quote_curr_symb
			bo.fees_curr_symb        = buy.quote_curr_symb
			bo.buy_cnt_est           = (buy.trade_size * 0.996) / buy.prc_buy
			bo.prc_buy_est           = buy.prc_buy
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
