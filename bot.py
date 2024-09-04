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

from libs.lib_charts                   import *
from libs.lib_common                   import *
from libs.lib_colors                   import *

from libs.bot_common                   import *
from libs.bot_coinbase                 import *
from libs.bot_db_read                  import *
from libs.bot_db_write                 import *
from libs.bot_logs                     import *
from libs.bot_secrets                  import secrets
from libs.bot_settings                 import settings
from libs.bot_strats                   import *
from libs.bot_ta                       import *
from libs.bot_theme                    import *

from report                            import report_buys_recent
from report                            import report_open
from report                            import report_open_by_age
from report                            import report_open_by_prod_id
from report                            import report_sells_recent

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot'
log_name      = 'bot'
lib_secs_max  = 0.33
lib_secs_max  = 10

#<=====>#
# Assignments Pre
#<=====>#

#<=====>#
# Classes
#<=====>#

class BOT():

	def __init__(self):
		self.fnc_secs_max              = 0.33
		self.sc                        = secrets.settings_load()
		self.st                        = settings.settings_load()
		self.trade_currs               = self.st.spot.trade_currs
		self.buy_strats                = buy_strats_get()
#		self.sell_strats               = sell_strats_get()
		self.bal_avails                = {}
		self.spendable_amts            = {}
		self.reserve_amts              = {}
		self.reserve_locked_tf         = True
		cb_mkts_refresh()
		self.refresh_wallet_tf         = True
		self.wallet_refresh(force_tf=True)
		self.show_buy_header_tf        = True
		self.show_sell_header_tf       = True
		# don't change this value, need more codiging for USDT or USD, someday integrae USDT/USD/BTC/ETH
		self.quote_curr_symb = 'USDC'

	#<=====>#

	def bot(self):
		func_name = 'bot'
		func_str = f'{lib_name}.{func_name}()'
#		G(func_str)

		self.before_start()

		cnt = 0
		while True:
			try:
				cnt += 1
				t0                = time.perf_counter()

				print_adv(4)
				WoB(f"{'<----- // ===== | == TOP == | ===== \\ ----->':^200}")

				self.st = settings.reload()

				self.before_loop()

				self.mkts_lists_get()
				self.mkts_loop()

				self.after_loop()

				# Dump CSVs of database tables for recovery
				if cnt == 1 or cnt % 10 == 0:
					db_table_csvs_dump()

				# End of Loop Display
				loop_secs = self.st.loop_secs
				print_adv(2)
				t1 = time.perf_counter()
				elapsed_seconds = round(t1 - t0, 2)
				if elapsed_seconds >= 5:
					WoB(f'loop {cnt} completed in {elapsed_seconds} seconds, sleeping {loop_secs} seconds and then restarting...')
					WoB(f'reserve_locked_tf : {self.reserve_locked_tf}')

					hmsg = ''
					hmsg += f"$ {'usdc bal':^9} | "
					hmsg += f"$ {'reserve':^9} | "
					hmsg += f"$ {'available':^9} | "
					hmsg += f"{'reserves state':^14} | "
					WoM(hmsg)

					for trade_curr in self.trade_currs:
						msg = ""
						msg += f"$ {self.bal_avails[trade_curr]:>9.2f} | "
						msg += f"$ {self.reserve_amts[trade_curr]:>9.2f} | "
						msg += f"$ {self.spendable_amts[trade_curr]:>9.2f} | "
						if self.reserve_locked_tf:
							msg += f"{'LOCKED':^14} | "
						else:
							msg += f"{'UNLOCKED':^14} | "
						WoG(msg)

				time.sleep(loop_secs)

			except KeyboardInterrupt as e:
				print(f'{func_name} ==> keyed exit... {e}')
				sys.exit()

			except Exception as e:
				loop_secs = self.st.loop_secs
				print(f'{func_name} ==> errored... {e}')
				print(dttm_get())
				traceback.print_exc()
				print(type(e))
				print(e)
				print(f'sleeping {loop_secs} seconds and then restarting')
				time.sleep(loop_secs)

	#<=====>#

	def before_start(self):
		func_name = 'before_loop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		# this is here just to proof that sounds alerts will be heard
		if self.st.speak_yn == 'Y': speak_async('Coinbase Trade Bot Online')

		self.wallet_refresh(force_tf=True)

		report_buys_recent(cnt=20)
		report_sells_recent(cnt=20)
		report_open_by_age()

		func_end(fnc)

	#<=====>#

	def before_loop(self):
		func_name = 'before_loop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		self.sell_ords_check()
		self.buy_ords_check()
		cb_mkts_refresh()
		self.wallet_refresh(force_tf=True)

		func_end(fnc)

	#<=====>#

	def after_loop(self):
		func_name = 'after_loop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		self.sell_ords_check()
		self.buy_ords_check()

		report_buys_recent(cnt=20)
		report_sells_recent(cnt=20)
		report_open_by_age()

#		# End of Market Loop Balance Display
		self.wallet_refresh()

		func_end(fnc)

	#<=====>#

	def mkts_loop(self):
		func_name = 'mkts_loop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		print_adv()
		WoM(f"{'Markets Loop':^200}")

		cnt = 0
		# loop through all mkts for buy/sell logic
		t0 = time.perf_counter()

		dttm_start_loop = dttm_get()	
		t_loop = time.perf_counter()

		for m in self.mkts:
			cnt += 1
			t00 = time.perf_counter()

			# formatting the mkt
			prod_id = m['prod_id']
			m = dec_2_float(m)
			m = AttrDictConv(in_dict=m)
			# This is only for mkt_disp
			m.cnt = cnt
			m.mkts_tot = len(self.mkts)

			# lets Avoid Trading Stable Coins Against One Another
			if m.base_curr_symb in self.st.stable_coins:
				continue

			# refresh settings each loop for hot changes
			self.st = settings.reload()
			self.wallet_refresh()

			t_now = time.perf_counter()
			t_elapse = t_now - t_loop
			loop_age = format_disp_age2(t_elapse)

			# build Out Everything We Will Need in the Market
			print_adv(3)

			title_msg = f'* Market Summary * {prod_id} * {dttm_get()} * {dttm_start_loop} * {loop_age} * {cnt}/{len(self.mkts)}'
			chart_top(in_str=title_msg, len_cnt=240)

			# build the market
			mkt, trade_perf, trade_strat_perfs = self.mkt_build(m)

			# process the mkt
			mkt = self.mkt_logic(mkt, trade_perf, trade_strat_perfs)

			# end of Performance Timer for ind mkt
			t11 = time.perf_counter()
			secs = round(t11 - t00, 3)
			if secs > lib_secs_max:
				msg = f'mkt_loop for {prod_id} - took {secs} seconds...'
				in_str_len = len(msg)
				msg = cs(msg, font_color='white', bg_color='orangered')
				print(msg)

			chart_bottom(len_cnt=240)

		# end of Performance Timer for mkt loop
		t1 = time.perf_counter()
		secs = round(t1 - t0, 3)
		if secs > lib_secs_max:
			cp(f'mkt_loops - took {secs} seconds to complete...', font_color='white', bg_color='orangered')

		func_end(fnc)

	#<=====>#

	def mkts_lists_get(self):
		func_name = 'mkts_lists_get'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		loop_mkts = []
		self.buy_mkts = []
		self.trade_mkts = []	

		# get mkts from settings
		spot_mkts  = self.st.spot.mkts.trade_mkts
		self.trade_mkts = spot_mkts
		if spot_mkts:
			loop_mkts.extend(spot_mkts)
			loop_mkts = list(set(loop_mkts))
			self.buy_mkts.extend(loop_mkts)

		# Get The Markets with Open Positions
		# They all need to be looped through buy/sell logic
		mkts       = db_mkts_loop_poss_open_prod_ids_get()
		if mkts:
			mkts = list(set(mkts))
			WoB(f'adding markets with open positions ({len(mkts)}) :')
			prt_cols(mkts, cols=10)
			loop_mkts.extend(mkts)

		# Get The Markets with the best performance on the bot so far
		# By Gain Loss Percen Per Hour
		# Settings how many of these we will look at
		pct_min    = self.st.spot.mkts.extra_mkts_top_bot_perf_pct_min
		lmt_cnt    = self.st.spot.mkts.extra_mkts_top_bot_perf_cnt
		mkts       = db_mkts_loop_top_perfs_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min)
		if mkts:
			if self.st.spot.mkts.extra_mkts_top_bot_perf_yn == 'Y':
				WoB(f'adding mkts top bot gain loss percent per day performers ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='WoG')
				loop_mkts.extend(mkts)
				self.buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_top_bot_perf_cnt > 0:
				WoB(f'skipping mkts top bot gain loss percent per day  performers ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the best performance on the bot so far
		# By Gain Loss Amount Total
		# Settings how many of these we will look at
		lmt_cnt    = self.st.spot.mkts.extra_mkts_top_bot_gains_cnt
		mkts       = db_mkts_loop_top_gains_prod_ids_get(lmt=lmt_cnt)
		if mkts:
			if self.st.spot.mkts.extra_mkts_top_bot_gains_yn == 'Y':
				WoB(f'adding mkts top bot gain loss performers ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='WoG')
				loop_mkts.extend(mkts)
				self.buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_top_bot_gains_cnt > 0:
				WoB(f'skipping mkts top bot gain loss performers ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h price increase
		# Settings how many of these we will look at
		pct_min    = self.st.spot.mkts.extra_mkts_prc_pct_chg_24h_pct_min
		lmt_cnt    = self.st.spot.mkts.extra_mkts_prc_pct_chg_24h_cnt
		mkts       = db_mkts_loop_top_prc_chg_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min)
		if mkts:
			if self.st.spot.mkts.extra_mkts_prc_pct_chg_24h_yn == 'Y':
				WoB(f'adding mkts top price increases ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='WoG')
				loop_mkts.extend(mkts)
				self.buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_prc_pct_chg_24h_cnt > 0:
				WoB(f'skipping mkts top price increases ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h volume increase
		# Settings how many of these we will look at
		lmt_cnt    = self.st.spot.mkts.extra_mkts_vol_quote_24h_cnt
		mkts       = db_mkts_loop_top_vol_chg_prod_ids_get(lmt=lmt_cnt)
		if mkts:
			if self.st.spot.mkts.extra_mkts_vol_quote_24h_yn == 'Y':
				WoB(f'adding mkts highest volume ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='WoG')
				loop_mkts.extend(mkts)
				self.buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_vol_quote_24h_cnt > 0:
				WoB(f'skipping mkts highest volume ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h volume percent increase
		# Settings how many of these we will look at
		lmt_cnt    = self.st.spot.mkts.extra_mkts_vol_pct_chg_24h_cnt
		mkts       = db_mkts_loop_top_vol_chg_pct_prod_ids_get(lmt=lmt_cnt)
		if mkts:
			if self.st.spot.mkts.extra_mkts_vol_pct_chg_24h_yn == 'Y':
				WoB(f'adding mkts highest volume increase ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='WoG')
				loop_mkts.extend(mkts)
				self.buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_vol_pct_chg_24h_cnt > 0:
				WoB(f'skipping mkts highest volume increase ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets that are marked as favorites on Coinbase
		mkts       = db_mkts_loop_watched_prod_ids_get()
		if mkts:
			if self.st.spot.mkts.extra_mkts_watched_yn == 'Y':
				WoB(f'adding watched markets ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='WoG')
				loop_mkts.extend(mkts)
				self.buy_mkts.extend(mkts)
			else:
				WoB(f'skipping watched markets ({len(mkts)}) :')
				prt_cols(mkts, cols=10, clr='GoW')

		stable_mkts           = self.st.spot.mkts.stable_mkts
		err_mkts              = self.st.spot.mkts.err_mkts
		mkts                  = db_mkts_loop_get(loop_mkts=loop_mkts, stable_mkts=stable_mkts, err_mkts=err_mkts)
		# Iterates through the mkts returned from MySQL and converts all decimals to floats
		# This is faster than making everything be done in decimals (which I would prefer)
		mkts                  = dec_2_float(mkts)
		self.mkts             = mkts

		# Display the markets that will be looped
		disp_mkts = []
		for m in self.mkts:
			disp_mkts.append(m['prod_id'])
		WoB(f'loop mkts ({len(mkts)}) :')
		prt_cols(disp_mkts, cols=10)

		# Display the markets that will be looped
		WoB(f'buy mkts ({len(self.buy_mkts)}) :')
		prt_cols(self.buy_mkts, cols=10)

		func_end(fnc)

	#<=====>#

	def mkt_build(self, m):
		func_name = 'mkt_build'
		func_str = f'{lib_name}.{func_name}(m)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id = m.prod_id

		# build mkt obj
		mkt = AttrDict()
		for a in m:
			mkt[a] = m[a]

		# Estimate the true buy/sell prices by looking at the order book
		pricing_cnt                              = settings.get_ovrd(in_dict=self.st.spot.buy.trade_size, in_key=prod_id)
		max_poss_open_trade_size                 = db_poss_open_max_trade_size_get(prod_id)
		if max_poss_open_trade_size:
			if max_poss_open_trade_size > pricing_cnt:
				pricing_cnt = max_poss_open_trade_size
		mkt.prc_mkt                              = m.prc
		bid_prc, ask_prc                         = cb_bid_ask_by_amt_get(prod_id=prod_id, buy_sell_size=pricing_cnt)
		mkt.prc_bid                              = bid_prc
		mkt.prc_ask                              = ask_prc
		mkt.prc_dec                              = cb_mkt_prc_dec_calc(mkt.prc_bid, mkt.prc_ask)
		mkt.prc_buy                              = round(mkt.prc_ask, mkt.prc_dec)
		mkt.prc_sell                             = round(mkt.prc_bid, mkt.prc_dec)
		mkt.prc_range_pct                        = ((mkt.prc_buy - mkt.prc_sell) / mkt.prc) * 100
		mkt.prc_buy_diff_pct                     = ((mkt.prc - mkt.prc_buy) / mkt.prc) * 100
		mkt.prc_sell_diff_pct                    = ((mkt.prc - mkt.prc_sell) / mkt.prc) * 100

		# Market Performance
		trade_perf                               = self.mkt_trade_perf_get(mkt)

		# get default settings
		trade_perf.restricts_buy_delay_minutes   = settings.get_ovrd(in_dict=self.st.spot.buy.buy_delay_minutes, in_key=prod_id) 
		trade_perf.restricts_open_poss_cnt_max   = settings.get_ovrd(in_dict=self.st.spot.buy.open_poss_cnt_max, in_key=prod_id)

		# get market performance boosts
		mkt, trade_perf                          = self.mkt_boosts(mkt, trade_perf)

		# Market Strat Performances
		trade_strat_perfs    = []
		# Market Strategy Performance
		for strat in self.buy_strats:
			trade_strat_perf = self.buy_strats[strat]
			trade_strat_perf = dec_2_float(trade_strat_perf)
			trade_strat_perf = AttrDictConv(in_dict=trade_strat_perf)
			buy_strat_type   = trade_strat_perf.buy_strat_type
			buy_strat_name   = trade_strat_perf.buy_strat_name
			buy_strat_freq   = trade_strat_perf.buy_strat_freq
			trade_strat_perf = self.trade_strat_perf_get(mkt, buy_strat_type, buy_strat_name, buy_strat_freq)
			trade_strat_perfs.append(trade_strat_perf)
		trade_strat_perfs_sorted = sorted(trade_strat_perfs, key=lambda x: x["gain_loss_pct_day"], reverse=True)
		trade_strat_perfs = trade_strat_perfs_sorted

		# set the budget details for this quote currency
		for trade_curr in self.trade_currs:
			if trade_curr == mkt.quote_curr_symb:
				mkt.bal_avail      = self.bal_avails[trade_curr]
				mkt.reserve_amt    = self.reserve_amts[trade_curr]
				mkt.spendable_amt  = self.spendable_amts[trade_curr]

		func_end(fnc)
		return mkt, trade_perf, trade_strat_perfs

	#<=====>#

	def mkt_trade_perf_get(self, mkt):
		func_name = 'mkt_trade_perf_get'
		func_str = f'{lib_name}.{func_name}(mkt)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id = mkt.prod_id

		# Build to Defaults
		trade_perf = {}
		trade_perf['prod_id']                       = prod_id
		trade_perf['tot_cnt']                       = 0
		trade_perf['win_cnt']                       = 0
		trade_perf['lose_cnt']                      = 0
		trade_perf['win_pct']                       = 0
		trade_perf['lose_pct']                      = 0
		trade_perf['age_mins']                      = 0
		trade_perf['age_hours']                     = 0
		trade_perf['bo_elapsed']                    = 9999
		trade_perf['pos_elapsed']                   = 9999
		trade_perf['last_elapsed']                  = 0
		trade_perf['tot_out_cnt']                   = 0
		trade_perf['tot_in_cnt']                    = 0
		trade_perf['buy_fees_cnt']                  = 0
		trade_perf['sell_fees_cnt_tot']             = 0
		trade_perf['fees_cnt_tot']                  = 0
		trade_perf['buy_cnt']                       = 0
		trade_perf['sell_cnt_tot']                  = 0
		trade_perf['hold_cnt']                      = 0
		trade_perf['pocket_cnt']                    = 0
		trade_perf['clip_cnt']                      = 0
		trade_perf['sell_order_cnt']                = 0
		trade_perf['sell_order_attempt_cnt']        = 0
		trade_perf['val_curr']                      = 0
		trade_perf['val_tot']                       = 0
		trade_perf['win_amt']                       = 0
		trade_perf['lose_amt']                      = 0
		trade_perf['gain_loss_amt']                 = 0
		trade_perf['gain_loss_amt_net']             = 0
		trade_perf['gain_loss_pct']                 = 0
		trade_perf['gain_loss_pct_hr']              = 0
		trade_perf['gain_loss_pct_day']             = 0
		trade_perf = AttrDictConv(in_dict=trade_perf)

		# Get From Database
		tp = db_view_trade_perf_get_by_prod_id(prod_id)
		tp = dec_2_float(tp)
		tp = AttrDictConv(in_dict=tp)
		if tp:
			for k in tp:
				if tp[k]:
					trade_perf[k] = tp[k]

		# Get elapsed minues since last buy
		r = db_mkt_elapsed_get(prod_id)
		trade_perf.bo_elapsed   = r[0]
		trade_perf.pos_elapsed  = r[1]
		trade_perf.last_elapsed = r[2]

		# Get count of open positions
		open_poss = db_pos_open_get_by_prod_id(prod_id)
		trade_perf.open_poss_cnt = len(open_poss)

		func_end(fnc)
		return trade_perf

	#<=====>#

	def mkt_boosts(self, mkt, trade_perf):
		func_name = 'mkt_boosts'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		# Boost trade_perf.restricts_open_poss_cnt_max

		func_end(fnc)
		return mkt, trade_perf

	#<=====>#

	def mkt_disp(self, mkt, trade_perf, trade_strat_perfs):
		func_name = 'mkt_disp'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
#		G(func_str)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=3)

		# Market Basics
		prod_id = mkt.prod_id

		# Prices & Balances
		hmsg = ""
		hmsg += f"$ {'price':^14} | "
		hmsg += f"{'prc_chg':^10} % | "
		hmsg += f"$ {'buy_prc':^14} | "
		hmsg += f"$ {'sell_prc':^14} | "
		hmsg += f"{'buy_var':^10} % | "
		hmsg += f"{'sell_var':^10} % | "
		hmsg += f"{'spread_pct':^10} % | "
		hmsg += f"$ {'usdc bal':^9} | "
		hmsg += f"$ {'reserve':^9} | "
		hmsg += f"$ {'available':^9} | "
		hmsg += f"{'reserves state':^14} | "

		msg = ""
		msg += f"$ {mkt.prc_mkt:>14.8f} | "
		msg += f"{mkt.prc_pct_chg_24h:>10.4f} % | "
		msg += f"$ {mkt.prc_buy:>14.8f} | "
		msg += f"$ {mkt.prc_sell:>14.8f} | "
		msg += f"{mkt.prc_buy_diff_pct:>10.4f} % | "
		msg += f"{mkt.prc_sell_diff_pct:>10.4f} % | "
		msg += f"{mkt.prc_range_pct:>10.4f} % | "
		msg += cs(f"$ {mkt.bal_avail:>9.2f} | ", "white", "green")
		msg += cs(f"$ {mkt.reserve_amt:>9.2f} | ", "white", "green")
		msg += cs(f"$ {mkt.spendable_amt:>9.2f} | ", "white", "green")
		if self.reserve_locked_tf:
			msg += cs(f"{'LOCKED':^14} | ", "yellow", "magenta")
		else:
			msg += cs(f"{'UNLOCKED':^14} | ", "magenta", "yellow")
		chart_headers(in_str=hmsg, len_cnt=240)
		chart_row(in_str=msg, len_cnt=240)

		hmsg = ""
		hmsg += f"{'trades':^9} | "
		hmsg += f"{'wins':^9} | "
		hmsg += f"{'lose':^9} | "
		hmsg += f"{'win_pct':^9} % | "
		hmsg += f"{'lose_pct':^9} % | "
		hmsg += f"$ {'win_amt':^9} | "
		hmsg += f"$ {'lose_amt':^9} | "
		hmsg += f"$ {'spent':^9} | "
		hmsg += f"$ {'recv':^9} | "
		hmsg += f"$ {'hold':^9} | "
		hmsg += f"$ {'val':^9} | "
		hmsg += f"$ {'gain_amt':^9} | "
		hmsg += f"{'gain_pct':^9} % | "
		hmsg += f"{'gain_hr':^9} % | "
		hmsg += f"{'gain_day':^9} % | "
		hmsg += f"{'elapsed':^9} | "

		msg = ''
		msg += f'{trade_perf.tot_cnt:>9} | '
		msg += f'{trade_perf.win_cnt:>9} | '
		msg += f'{trade_perf.lose_cnt:>9} | '
		msg += f'{trade_perf.win_pct:>9.2f} % | '
		msg += f'{trade_perf.lose_pct:>9.2f} % | '
		msg += f'$ {trade_perf.win_amt:>9.4f} | '
		msg += f'$ {trade_perf.lose_amt:>9.4f} | '
		msg += f'$ {trade_perf.tot_out_cnt:>9.4f} | '
		msg += f'$ {trade_perf.tot_in_cnt:>9.4f} | '
		msg += f'$ {trade_perf.val_curr:>9.4f} | '
		msg += f'$ {trade_perf.val_tot:>9.4f} | '
		msg += f'$ {trade_perf.gain_loss_amt:>9.4f} | '
		msg += f'{trade_perf.gain_loss_pct:>9.4f} % | '
		msg += f'{trade_perf.gain_loss_pct_hr:>9.4f} % | '
		msg += f'{trade_perf.gain_loss_pct_day:>9.4f} % | '
		msg += f'{trade_perf.last_elapsed:>9} | '

		title_msg = f'* Market Stats * {prod_id} *'
		chart_mid(in_str=title_msg, len_cnt=240)
		chart_headers(in_str=hmsg, len_cnt=240)
		if trade_perf.gain_loss_pct > 0:
#			chart_row(in_str=msg, font_color='white', bg_color='green', len_cnt=240)
			WoG('|' + msg)
		else:
#			chart_row(in_str=msg, font_color='white', bg_color='red', len_cnt=240)
			WoR('|' + msg)

		hmsg = ""
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
		hmsg += f"{'elapsed':^7} | "

#		print_adv(2)
		title_msg = '* Buy Strategy Past Performance *'
		chart_mid(in_str=title_msg, len_cnt=240)
		chart_headers(hmsg, len_cnt=240)

		for x in trade_strat_perfs:
			x = dec_2_float(x)
			x = AttrDictConv(in_dict=x)

			if x.tot_cnt > 0:
				msg = ''
				msg += f'{x.buy_strat_name:<15} | '
				msg += f'{x.buy_strat_freq:<15} | '
				msg += f'{int(x.tot_cnt):>5} | '
				msg += f'{int(x.open_cnt):>5} | '
				msg += f'{int(x.close_cnt):>5} | '
				msg += f'{int(x.win_cnt):>5} | '
				msg += f'{int(x.lose_cnt):>5} | '
				msg += f'{x.win_pct:>6.2f} % | '
				msg += f'{x.lose_pct:>6.2f} % | '
				msg += f'{x.gain_loss_amt:>10.2f} | '
				msg += f'{x.gain_loss_pct:>10.2f} % | '
				msg += f'{x.gain_loss_pct_hr:>10.2f} % | '
				msg += f'{x.gain_loss_pct_day:>10.2f} % | '
				msg += f'{x.strat_last_elapsed:>7} | '
				msg  = '|' + cs_pct_color_50(pct=x.win_pct, msg=msg)
				print(msg)
#				chart_row(in_str=msg, len_cnt=240)

		func_end(fnc)
		return mkt, trade_perf, trade_strat_perfs

	#<=====>#

	def mkt_logic(self, mkt, trade_perf, trade_strat_perfs):
		func_name = 'mkt_logic'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		try:
			prod_id      = mkt.prod_id
			self.st      = settings.reload()

			mkt          = buy_strats_avail_get(mkt)
			self.wallet_refresh()

			# Market Summary
			try:
				t0 = time.perf_counter()

				mkt, trade_perf, trade_strat_perfs = self.mkt_disp(mkt, trade_perf, trade_strat_perfs)

				t1 = time.perf_counter()
				secs = round(t1 - t0, 3)
				if secs > lib_secs_max:
					cp(f'mkt_summary for {prod_id} - took {secs} seconds...', font_color='white', bg_color='orangered')
#					print_adv()

			except Exception as e:
				print(f'{dttm_get()} {func_name} - Market Summary ==> {prod_id} = Error : ({type(e)}){e}')
				traceback.print_exc()
				pprint(mkt)
				print_adv(3)
				beep()
				beep()
				beep()
				pass

			# Market Technical Analysis
			ta = None
			try:
				t0 = time.perf_counter()

#				if self.st.spot.buy.buying_on_yn == 'Y' or self.st.spot.sell.selling_on_yn == 'Y':
				ta = mkt_ta_main(mkt, self.st)
				if ta == 'Error!':
					WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
					WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
					WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
					beep()
					func_end(fnc)
					return mkt

				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				if secs > lib_secs_max:
					cp(f'mkt_ta_main for {prod_id}- took {secs} seconds...', font_color='white', bg_color='orangered')
#					print_adv()

			except Exception as e:
				print(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} = Error : ({type(e)}){e}')
				traceback.print_exc()
				pprint(mkt)
				print_adv(3)
				beep(3)
				pass

			# Market Buy Logic
			try:
				t0 = time.perf_counter()

#				if self.st.spot.buy.buying_on_yn == 'Y':
				mkt = self.buy_logic(self.buy_mkts, mkt, trade_perf, trade_strat_perfs, ta)

				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				if secs > lib_secs_max:
					cp(f'buy_logic for {prod_id} - took {secs} seconds...', font_color='white', bg_color='orangered')
#					print_adv()

			except Exception as e:
				print(f'{dttm_get()} {func_name} - Buy Logic ==> {prod_id} = Error : ({type(e)}){e}')
				traceback.print_exc()
				pprint(mkt)
				print_adv(3)
				beep(3)
				pass

			# Market Sell Logic
			try:
				t0 = time.perf_counter()

#				if self.st.spot.sell.selling_on_yn == 'Y':
				open_poss = db_pos_open_get_by_prod_id(prod_id)
				mkt = self.sell_logic(mkt, ta, open_poss)

				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				if secs > lib_secs_max:
					cp(f'sell_logic for {prod_id} - took {secs} seconds...', font_color='white', bg_color='orangered')
#					print_adv()

			except Exception as e:
				print(f'{dttm_get()} {func_name} - Sell Logic ==> {prod_id} = Error : ({type(e)}){e}')
				traceback.print_exc()
				pprint(mkt)
				print_adv(3)
				beep(3)
				pass

			db_tbl_mkts_insupd([mkt])

		except Exception as e:
			print(f'{func_name} ==> errored 2... {e}')
			print(dttm_get())
			traceback.print_exc()
			print(type(e))
			print(e)
			print(f'prod_id : {mkt.prod_id}')
			pprint(mkt)
			print_adv(3)
			beep()
			beep()
			beep()
			pass

		func_end(fnc)
		return mkt

	#<=====>#

	# Function to fetch current positions
	def wallet_refresh(self, force_tf=False):
		func_name = 'wallet_refresh'
		func_str = f'{lib_name}.{func_name}(self.refresh_wallet_tf={self.refresh_wallet_tf}, force_tf={force_tf})'
#		G(func_str)
		fnc = func_begin(func_name=func_name, func_str=func_str,  logname=log_name, secs_max=1.5)

		if self.refresh_wallet_tf or force_tf:
			cb_wallet_refresh()
			self.refresh_wallet_tf = False

			self.reserve_amts     = {}
			self.bal_avails       = {}
			self.spendable_amts   = {}
			self.open_trade_amts   = {}

			# when/if we start trading  against btc, eth, sol and not just usdc
			# we will need to add a deduction for the amount outstanding on trades 
			# that used other currencies

			open_trade_amts = {}
			open_trade_amts = AttrDictConv(in_dict=open_trade_amts)
			r = db_open_trade_amts_get()

			for x in r:
				x = AttrDictConv(in_dict=x)
				x = dec_2_float(x)
				if x['base_curr_symb'] in ('BTC', 'ETH', 'USDT', 'USDC'):
					open_trade_amts[x['base_curr_symb']] = x['open_trade_amt']

			bals = db_bals_get()
			for bal in bals:
				bal = dec_2_float(bal)
				bal = AttrDictConv(in_dict=bal)
				curr = bal.curr
				bal_avail = bal.bal_avail
				if curr in self.trade_currs:
					reserve_amt   = self.calc_reserve_amt(trade_curr=curr)
					self.reserve_amts[curr]   = reserve_amt
					self.bal_avails[curr]     = bal_avail
					spendable_amt = self.bal_avails[curr] - self.reserve_amts[curr] 
					if curr in open_trade_amts:
						open_trade_amt = open_trade_amts[curr]
						spendable_amt -= open_trade_amt
						self.open_trade_amts[curr] = open_trade_amts[curr]
					else:
						open_trade_amt = 0
						self.open_trade_amts[curr] = 0
					self.spendable_amts[curr] = spendable_amt
#					print(f'{func_name} - {curr} - bal_avail : {bal_avail}, reserve_amt : {reserve_amt}, open_trade_amt : {open_trade_amt}, spendable_amt : {spendable_amt}')

		func_end(fnc)

	#<=====>#

	def calc_reserve_amt(self, trade_curr):
		func_name = 'calc_reserve_amt'
		func_str = f'{lib_name}.{func_name}(st, reserve_locked_tf={self.reserve_locked_tf}, trade_curr={trade_curr})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		day = dt.now().day
		min_reserve_amt                = settings.get_ovrd(in_dict=self.st.spot.buy.reserve_amt, in_key=trade_curr)
		daily_reserve_amt              = settings.get_ovrd(in_dict=self.st.spot.buy.reserve_addtl_daily_amt, in_key=trade_curr)
		tot_daily_reserve_amt          = day * daily_reserve_amt

		if self.reserve_locked_tf:
	#		reserve_amt                    = max(tot_daily_reserve_amt, min_reserve_amt)
			reserve_amt           = tot_daily_reserve_amt + min_reserve_amt
		else:
			reserve_amt = 0

		func_end(fnc)
		return reserve_amt

	#<=====>#

	def buy_logic(self, buy_mkts, mkt, trade_perf, trade_strat_perfs, ta):
		func_name = 'buy_logic'
		func_str = f'{lib_name}.{func_name}(buy_mkts, mkt, trade_perf, trade_strat_perfs, ta)'
#		G(func_str)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=6)

		st                        = settings.settings_load()
		prod_id                   = mkt.prod_id
		buy_yn                    = 'N'
		wait_yn                   = 'Y'
		mkt.buy_strat_type        = ''
		mkt.buy_strat_name        = ''
		mkt.buy_strat_freq        = ''
	#	show_buy_disp_yn          = 'N'
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
			self.buy_disp(mkt, trade_strat_perf)

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
					if prod_id in self.trade_mkts:
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

		func_end(fnc)
		return mkt

	#<=====>#

	def trade_strat_perf_get(self, mkt, buy_strat_type, buy_strat_name, buy_strat_freq):
		func_name = 'trade_strat_perf_get'
		func_str = f'{lib_name}.{func_name}(mkt, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id = mkt.prod_id

		trade_strat_perf = {}
		trade_strat_perf['prod_id']             = prod_id
		trade_strat_perf['buy_strat_type']      = buy_strat_type
		trade_strat_perf['buy_strat_name']      = buy_strat_name
		trade_strat_perf['buy_strat_freq']      = buy_strat_freq
		trade_strat_perf['tot_cnt']             = 0
		trade_strat_perf['open_cnt']            = 0
		trade_strat_perf['close_cnt']           = 0
		trade_strat_perf['win_cnt']             = 0
		trade_strat_perf['lose_cnt']            = 0
		trade_strat_perf['win_pct']             = 0
		trade_strat_perf['lose_pct']            = 0
		trade_strat_perf['age_hours']           = 0
		trade_strat_perf['tot_out_cnt']         = 0
		trade_strat_perf['tot_in_cnt']          = 0
		trade_strat_perf['fees_cnt_tot']        = 0
		trade_strat_perf['val_curr']            = 0
		trade_strat_perf['val_tot']             = 0
		trade_strat_perf['gain_loss_amt']       = 0
		trade_strat_perf['gain_loss_pct']       = 0
		trade_strat_perf['gain_loss_pct_hr']    = 0
		trade_strat_perf['gain_loss_pct_day']   = 0
		trade_strat_perf['strat_bo_elapsed']    = 9999
		trade_strat_perf['strat_pos_elapsed']   = 9999
		trade_strat_perf['strat_last_elapsed']  = 9999

		trade_strat_perf['all_sells']           = []
		trade_strat_perf['all_hodls']           = []
		trade_strat_perf['all_passes']          = []
		trade_strat_perf['all_fails']           = []
		trade_strat_perf['pass_cnt']            = 0
		trade_strat_perf['fail_cnt']            = 0
		trade_strat_perf['pass_pct']            = 0

		trade_strat_perf = AttrDictConv(in_dict=trade_strat_perf)

		msp = db_trade_strat_perf_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
		if msp:
			for k in msp:
				if msp[k]:
					trade_strat_perf[k] = msp[k]

		trade_strat_perf.restricts_buy_strat_delay_minutes = settings.get_ovrd(in_dict=self.st.spot.buy.buy_strat_delay_minutes, in_key=buy_strat_freq)
		r = db_mkt_strat_elapsed_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
		trade_strat_perf.strat_bo_elapsed   = r[0]
		trade_strat_perf.strat_pos_elapsed  = r[1]
		trade_strat_perf.strat_last_elapsed = r[2]

		func_end(fnc)
		return trade_strat_perf

	#<=====>#

	def buy_logic_strat_boosts(self, mkt, trade_strat_perf):
		func_name = 'buy_logic_strat_boosts'
		func_str = f'{lib_name}.{func_name}(mkt, trade_strat_perf)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id                   = mkt.prod_id
		buy_strat_type            = trade_strat_perf.buy_strat_type
		buy_strat_name            = trade_strat_perf.buy_strat_name
		buy_strat_freq            = trade_strat_perf.buy_strat_freq
		debug_yn                  = 'N'

		# get default open position max for strat
		# add double override logic strat + prod
		# fixme
		trade_strat_perf.restricts_strat_open_cnt_max = settings.get_ovrd(in_dict=self.st.spot.buy.strat_open_cnt_max, in_key=prod_id) 

		# Open Position Count Checks Performance Based
		# Boost allowed max positions based upon past performance
		if trade_strat_perf.tot_cnt >= 25 and trade_strat_perf.gain_loss_pct_day > 1:
			msg = ''
			msg += f'    * BOOST BUY STRAT : '
			msg += f'{mkt.prod_id} '
			msg += f'{buy_strat_name} - {buy_strat_freq} '
			msg += f'has {trade_strat_perf.tot_cnt} trades '
			msg += f'with performance {trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % '
			msg += f'boosting allowed open pos ... '
			YoB(msg)
			trade_strat_perf.restricts_strat_open_cnt_max *= 2
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
		if trade_strat_perf.tot_cnt >= 3 and trade_strat_perf.gain_loss_pct_day > 0.25:
			trade_size             *= 2
		# Boost those with proven track records
		if trade_strat_perf.tot_cnt >= tests_min and trade_strat_perf.gain_loss_pct_day > 0.5:
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
#		G(func_str)

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
#		G(func_str)

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
			beep(3)
		else:
			if debug_yn == 'Y':
				BoW(f'    * ALLOW BUY MKT : {mkt.prod_id} is in the forced_sell.prod_ids settings, and would instantly sell...')

		# Market Is Set To Limit Only on Coinbase
		if mkt.mkt_limit_only_tf == 1:
			RoW(f'    * CANCEL BUY MKT : {mkt.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')
			buy_deny_yn = 'Y'
			beep(3)
		else:
			if debug_yn == 'Y':
				BoW(f'    * ALLOW BUY MKT : {mkt.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')

		# Very Large Bid Ask Spread
		if mkt.prc_range_pct >= 2:
			RoW(f'    * CANCEL BUY MKT : {mkt.prod_id} has a price range variance of {mkt.prc_range_pct}, this price range looks like trouble... skipping buy')
			buy_deny_yn = 'Y'
			beep(3)
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
#		G(func_str)

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
				beep(3)
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
#		G(func_str)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=3)

		try:
			bos = db_buy_ords_open_get()
			if bos:
				print_adv(2)
				WoM(f"{'Buy Orders Check':^200}")

				bos_cnt = len(bos)
				cnt = 0
				for bo in bos:
					cnt += 1
	#				print(bo)
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
								beep()
								beep()
								beep()
								sys.exit()
		#					print(f'(o.ord_completion_percentage : {o.ord_completion_percentage} {type(o.ord_completion_percentage)}')
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
								beep()
							else:
								print(func_str)
								print('error #2 !')
								beep(3)
								db_buy_ords_stat_upd(bo_id=bo.bo_id, ord_stat='ERR')
					elif test_tf == 1:
						bo.ord_stat = 'FILL'
#						bo.buy_end_dttm = bo.buy_begin_dttm
						db_tbl_buy_ords_insupd(bo)
						self.pos_open(bo.buy_order_uuid)

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

	def pos_open(self, buy_order_uuid):
		func_name = 'pos_open'
		func_str = f'{lib_name}.{func_name}(buy_order_uuid={buy_order_uuid})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		bos = db_mkt_sizing_data_get_by_uuid(buy_order_uuid)

		for bo in bos:
			bo = dec_2_float(bo)
			bo = AttrDictConv(in_dict=bo)
			pos = AttrDict()
			pos.test_tf                 = bo.test_tf
			pos.prod_id                 = bo.prod_id
			pos.mkt_name                = bo.mkt_name
			pos.mkt_venue               = bo.mkt_venue
			pos.base_curr_symb          = bo.buy_curr_symb
			pos.base_size_incr          = bo.base_size_incr
			pos.base_size_min           = bo.base_size_min
			pos.base_size_max           = bo.base_size_max
			pos.quote_curr_symb         = bo.quote_curr_symb
			pos.quote_size_incr         = bo.quote_size_incr
			pos.quote_size_min          = bo.quote_size_min
			pos.quote_size_max          = bo.quote_size_max
			pos.pos_type                = bo.pos_type
			pos.pos_stat                = 'OPEN'
			pos.pos_begin_dttm          = bo.buy_begin_dttm
			pos.bo_id                   = bo.bo_id
			pos.bo_uuid                 = bo.buy_order_uuid
			pos.buy_strat_type          = bo.buy_strat_type
			pos.buy_strat_name          = bo.buy_strat_name
			pos.buy_strat_freq          = bo.buy_strat_freq
#			pos.buy_asset_type          = bo.buy_asset_type
			pos.buy_curr_symb           = bo.buy_curr_symb
			pos.buy_cnt                 = bo.buy_cnt_act
			pos.spend_curr_symb         = bo.spend_curr_symb
			pos.fees_curr_symb          = bo.fees_curr_symb
			pos.buy_fees_cnt            = bo.fees_cnt_act
			pos.tot_out_cnt             = bo.tot_out_cnt
			pos.sell_curr_symb          = bo.buy_curr_symb
			pos.recv_curr_symb          = bo.spend_curr_symb
#			pos.sell_fees_curr_symb     = bo.fees_curr_symb
			pos.sell_order_cnt          = 0
			pos.sell_order_attempt_cnt  = 0
			pos.hold_cnt                = bo.buy_cnt_act
			pos.sell_cnt_tot            = 0
			pos.tot_in_cnt              = 0
			pos.sell_fees_cnt_tot       = 0
			pos.prc_buy                 = bo.tot_prc_buy
			pos.prc_curr                = bo.prc_buy_act
			pos.prc_high                = bo.prc_buy_act
			pos.prc_low                 = bo.prc_buy_act
			pos.prc_chg_pct             = 0
			pos.prc_chg_pct_high        = 0
			pos.prc_chg_pct_low         = 0
			pos.prc_chg_pct_drop        = 0

			pos.fees_cnt_tot            = bo.fees_cnt_act

			pos.gain_loss_amt_est       = 0
			pos.gain_loss_amt_est_low   = 0
			pos.gain_loss_amt_est_high  = 0
			pos.gain_loss_amt           = 0
			pos.gain_loss_amt_net       = 0

			pos.gain_loss_pct_est       = 0
			pos.gain_loss_pct_est_high  = 0
			pos.gain_loss_pct_est_low   = 0
			pos.gain_loss_pct           = 0

#			print(func_name)
#			pprint(pos)

			db_tbl_poss_insupd(pos)

		func_end(fnc)

	#<=====>#

	def sell_logic(self, mkt, ta, open_poss):
		func_name = 'sell_logic'
		func_str = f'{lib_name}.{func_name}(mkt, ta, open_poss)'
#		G(func_str)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=6)

		prod_id = mkt.prod_id
		st = settings.settings_load()

		self.sell_header(prod_id)
		show_sell_header_tf = False

		if not open_poss:
			print(f'{prod_id} has no open positions...')
			func_end(fnc)
			return mkt

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

		func_end(fnc)
		return mkt

	#<=====>#

	def sell_pos_logic(self, mkt, ta, pos):
		func_name = 'sell_pos_logic'
		func_str = f'{lib_name}.{func_name}(mkt, ta, pos)'
#		G(func_str)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1)

		pos                       = self.pos_upd(pos=pos, mkt=mkt)
		pos.sell_strat_type       = ''
		pos.sell_strat_name       = ''
		prod_id                   = mkt.prod_id
		pos_id                    = pos.pos_id
		sell_yn                   = 'N'
		sell_block_yn             = 'N'
		hodl_yn                   = 'Y'
		sell_signals              = []

		self.sell_disp(pos)

		# Logic that will block the sell from happening
#		if sell_yn == 'Y':
		sell_block_yn = self.sell_pos_blocks(mkt, pos)
#		print(f'sell_yn: {sell_yn}, sell_block_yn: {sell_block_yn}')

		# Sell By Strat Logic
		if sell_yn == 'N' and ta:
			mkt, pos, sell_yn, hodl_yn, sell_signals = sell_strats_check(self.st, mkt, ta, pos, sell_yn, hodl_yn, sell_signals, sell_block_yn)

		# Forced Sell Logic
		if sell_yn == 'N':
#			print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_strat_sha()')
			mkt, pos, sell_yn, hodl_yn = self.sell_logic_forced(mkt, pos, sell_block_yn)
			sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
			sell_signals.append(sell_signal)

		# Take Profits
		if pos.prc_chg_pct > 0:
			if sell_yn == 'N':
#				print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_logic_hard_profit()')
				if self.st.spot.sell.take_profit.hard_take_profit_yn == 'Y':
					mkt, pos, sell_yn, hodl_yn = self.sell_logic_hard_profit(mkt, pos, sell_block_yn)
					sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
					sell_signals.append(sell_signal)

			if sell_yn == 'N':
#				print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_logic_trailing_profit()')
				if self.st.spot.sell.take_profit.trailing_profit_yn == 'Y':
					mkt, pos, sell_yn, hodl_yn = self.sell_logic_trailing_profit(mkt, pos, sell_block_yn)
					sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
					sell_signals.append(sell_signal)

		# Stop Loss
		if pos.prc_chg_pct < 0:
			if sell_yn == 'N':
				if self.st.spot.sell.stop_loss.hard_stop_loss_yn == 'Y':
#					print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_logic_hard_stop()')
					mkt, pos, sell_yn, hodl_yn = self.sell_logic_hard_stop(mkt, pos, sell_block_yn)
					sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
					sell_signals.append(sell_signal)

			if sell_yn == 'N':
				if self.st.spot.sell.stop_loss.trailing_stop_loss_yn == 'Y':
#					print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_logic_trailing_stop()')
					mkt, pos, sell_yn, hodl_yn = self.sell_logic_trailing_stop(mkt, pos, sell_block_yn)
					sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
					sell_signals.append(sell_signal)

			if sell_yn == 'N':
				if self.st.spot.sell.stop_loss.atr_stop_loss_yn == 'Y':
#					print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_logic_atr_stop()')
					mkt, pos, sell_yn, hodl_yn = self.sell_logic_atr_stop(mkt, ta, pos, sell_block_yn)
					sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
					sell_signals.append(sell_signal)

			if sell_yn == 'N':
				if self.st.spot.sell.stop_loss.trailing_atr_stop_loss_yn == 'Y':
#					print(f'mkt, pos, sell_yn : {sell_yn}, hodl_yn: {hodl_yn} = sell_logic_trailing_atr_stop()')
					mkt, pos, sell_yn, hodl_yn = self.sell_logic_trailing_atr_stop(mkt, ta, pos, sell_block_yn)
					sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": sell_yn, "hodl_yn": hodl_yn}
					sell_signals.append(sell_signal)

		if sell_yn == 'Y' and sell_block_yn == 'N' and ta:
			sell_block_yn = self.sell_logic_deny_all_green(mkt, ta, pos)

		if sell_yn == 'Y' and sell_block_yn == 'Y':
			hodl_yn = 'Y'
		elif sell_yn == 'Y' and sell_block_yn == 'N':
			hodl_yn = 'N'

		db_tbl_poss_insupd(pos)

#		print(f'sell_yn: {sell_yn}, sell_block_yn: {sell_block_yn}, hodl_yn: {hodl_yn}')

		if sell_yn == 'Y' and sell_block_yn == 'N':
			if pos.test_tf == 0:
#				MoY('!!! WTF WTF WTF WTF !!!')
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

		# final_sell_signals = []
		# for sell_signal in sell_signals:
		# 	if sell_signal['sell_yn'] == 'Y':
		# 		final_sell_signals.append(sell_signal)
		# db_tbl_sell_signals_insupd(final_sell_signals)

		pos.sell_yn = sell_yn
		pos.sell_block_yn = sell_block_yn
		pos.hodl_yn = hodl_yn

		func_end(fnc)
		return pos

	#<=====>#

	def sell_pos_blocks(self, mkt, pos):
		func_name = 'sell_pos_blocks'
		func_str = f'{lib_name}.{func_name}(mkt, pos)'
#		G(func_str)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1)

		prod_id     = pos.prod_id
		pos_id      = pos.pos_id

		sell_block_yn = 'N'

		if self.st.spot.sell.selling_on_yn == 'N':
			sell_block_yn = 'Y'
			msg = f'    * SELL BLOCK * selling_on_yn : {sell_block_yn} - self.st.spot.sell.selling_on_yn == N'
			if self.st.spot.sell.show_tests_yn in ('Y','F'):
				BoW(msg)
#		print(f'sell_block_yn: {sell_block_yn} * selling_on_yn : {sell_block_yn} - self.st.spot.sell.selling_on_yn == N')

		if self.st.spot.sell.never_sell_all_yn == 'Y':
			sell_block_yn = 'Y'
			msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - self.st.spot.sell.never_sell_all_yn == Y'
			if self.st.spot.sell.show_tests_yn in ('Y','F'):
				BoW(msg)
#		print(f'sell_block_yn: {sell_block_yn} * sell_block_yn : {sell_block_yn} - self.st.spot.sell.never_sell_all_yn == Y')

		if self.st.spot.sell.never_sell_loss_all_yn == 'Y' and pos.prc_chg_pct < 0:
			sell_block_yn = 'Y'
			msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - self.st.spot.sell.never_sell_loss_all_yn == Y and pos.prc_chg_pct < 0'
			if self.st.spot.sell.show_tests_yn in ('Y','F'):
				BoW(msg)
#		print(f'sell_block_yn: {sell_block_yn} * sell_block_yn : {sell_block_yn} - self.st.spot.sell.never_sell_loss_all_yn == Y and pos.prc_chg_pct < 0')

		if prod_id in self.st.spot.sell.never_sell.prod_ids:
			sell_block_yn = 'Y'
			msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} - in self.st.spot.sell.never_sell.prod_ids'
			if self.st.spot.sell.show_tests_yn in ('Y','F'):
				BoW(msg)
#		print(f'sell_block_yn: {sell_block_yn} * sell_block_yn : {sell_block_yn} - {pos.prod_id} - in self.st.spot.sell.never_sell.prod_ids')

		if prod_id in self.st.spot.sell.never_sell_loss.prod_ids and pos.prc_chg_pct < 0:
			sell_block_yn = 'Y'
			msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} - in self.st.spot.sell.never_sell_loss.prod_ids and pos.prc_chg_pct < 0'
			if self.st.spot.sell.show_tests_yn in ('Y','F'):
				BoW(msg)
#		print(f'sell_block_yn: {sell_block_yn} * sell_block_yn : {sell_block_yn} - {pos.prod_id} - in self.st.spot.sell.never_sell_loss.prod_ids and pos.prc_chg_pct < 0')

		if pos_id in self.st.spot.sell.never_sell.pos_ids:
			sell_block_yn = 'Y'
			msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} {pos.pos_id} - pos_id in self.st.spot.sell.never_sell.pos_ids'
			if self.st.spot.sell.show_tests_yn in ('Y','F'):
				BoW(msg)
#		print(f'sell_block_yn: {sell_block_yn} * sell_block_yn : {sell_block_yn} - {pos.prod_id} {pos.pos_id} - pos_id in self.st.spot.sell.never_sell.pos_ids')

		if pos_id in self.st.spot.sell.never_sell_loss.pos_ids and pos.prc_chg_pct < 0:
			sell_block_yn = 'Y'
			msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} {pos.pos_id} - pos_id in self.st.spot.sell.never_sell_loss.pos_ids and pos.prc_chg_pct < 0'
			if self.st.spot.sell.show_tests_yn in ('Y','F'):
				BoW(msg)
#		print(f'sell_block_yn: {sell_block_yn}')

		# Market Price Range Looks Very Suspect
		if mkt.prc_range_pct >= 5:
			sell_block_yn = 'Y'
			msg = f'    * SELL BLOCK * sell_block_yn : {sell_block_yn} - {pos.prod_id} - has a price range variance of {mkt.prc_range_pct}, this price range looks sus... skipping sell'
			BoW(msg)
			beep(3)
#		print(f'sell_block_yn: {sell_block_yn} * sell_block_yn : {sell_block_yn} - {pos.prod_id} - has a price range variance of {mkt.prc_range_pct}, this price range looks sus... skipping sell')

		func_end(fnc)
		return sell_block_yn

	#<=====>#

	def sell_logic_forced(self, mkt, pos, sell_block_yn='N'):
		func_name = 'sell_logic_forced'
		func_str = f'{lib_name}.{func_name}(mkt, pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id     = mkt.prod_id
		pos_id      = pos.pos_id
		# sell_prc    = mkt.prc_sell
		all_sells   = []
		all_hodls   = []
		sell_yn     = 'N'
		hodl_yn     = 'Y'
		show_tests_yn         = self.st.spot.sell.show_tests_yn

		force_sell_all_yn     = self.st.spot.sell.force_sell_all_yn
		if pos.force_sell_tf == 1:
			sell_yn = 'Y'
			msg = f'    * SELL COND: position marked as force sell..., sell_yn : {sell_yn}'
			all_sells.append(msg)
		elif self.st.spot.sell.force_sell_all_yn == 'Y':
			sell_yn = 'Y'
			msg = f'    * SELL COND: force_sell_all_yn = {force_sell_all_yn} in settings..., sell_yn : {sell_yn}'
			all_sells.append(msg)
		elif prod_id in self.st.spot.sell.force_sell.prod_ids:
			sell_yn = 'Y'
			msg = f'    * SELL COND: {prod_id} is in force_sell_prods in settings..., sell_yn : {sell_yn}'
			all_sells.append(msg)
		elif pos_id in self.st.spot.sell.force_sell.pos_ids:
			sell_yn = 'Y'
			msg = f'    * SELL COND: position {pos_id} is in force_sell_poss in settings..., sell_yn : {sell_yn}'
			all_sells.append(msg)

		if sell_yn == 'Y':
			hodl_yn = 'N'
			pos.sell_strat_type = 'force'
			pos.sell_strat_name  = 'forced sell'
		else:
			hodl_yn = 'Y'

	#	if sell_yn == 'Y' or show_tests_yn in ('Y','F'):
		if sell_yn == 'Y':
			msg = f'    SELL TESTS - {prod_id} - {pos_id}- Forced Sell'
			WoG(msg)
			if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					self.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					self.show_sell_header_tf = True
				print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

		func_end(fnc)
		return mkt, pos, sell_yn, hodl_yn

	#<=====>#

	def sell_logic_hard_profit(self, mkt, pos, sell_block_yn='N'):
		func_name = 'sell_logic_hard_profit'
		func_str = f'{lib_name}.{func_name}(mkt, pos, sell_block_yn={sell_block_yn})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id     = mkt.prod_id
		# sell_prc    = mkt.prc_sell
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

	#	if sell_yn == 'Y' or show_tests_yn in ('Y','F'):
		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			msg = f'    SELL TESTS - {prod_id} - Hard Take Profit'
			WoG(msg)
			if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					self.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					selfshow_sell_header_tf = True
				print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

		func_end(fnc)
		return mkt, pos, sell_yn, hodl_yn

	#<=====>#

	def sell_logic_hard_stop(self, mkt, pos, sell_block_yn='N'):
		func_name = 'sell_logic_hard_stop'
		func_str = f'{lib_name}.{func_name}(mkt, pos, sell_block_yn={sell_block_yn})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id     = mkt.prod_id
		# sell_prc    = mkt.prc_sell
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

	#	if sell_yn == 'Y' or show_tests_yn in ('Y','F'):
		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			m = f'    SELL TESTS - {prod_id} - Hard Stop Loss'
			WoG(msg)
			if (sell_yn == 'Y' and sell_block_yn == 'N')  or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					self.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					self.show_sell_header_tf = True
	#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

		func_end(fnc)
		return mkt, pos, sell_yn, hodl_yn

	#<=====>#

	def sell_logic_trailing_profit(self, mkt, pos, sell_block_yn='N'):
		func_name = 'sell_logic_trailing_profit'
		func_str  = f'{lib_name}.{func_name}(mkt, pos, sell_block_yn={sell_block_yn})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id     = mkt.prod_id
		# sell_prc    = mkt.prc_sell
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

	#	if sell_yn == 'Y' or show_tests_yn in ('Y','F'):
		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			msg = f'    SELL TESTS - {prod_id} - Trailing Profit'
			WoG(msg)
			if (sell_yn == 'Y' and sell_block_yn == 'N')  or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					self.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					self.show_sell_header_tf = True
	#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

		func_end(fnc)
		return mkt, pos, sell_yn, hodl_yn

	#<=====>#

	def sell_logic_trailing_stop(self, mkt, pos, sell_block_yn='N'):
		func_name = 'sell_logic_trailing_stop'
		func_str = f'{lib_name}.{func_name}(mkt, pos, sell_block_yn={sell_block_yn})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id     = mkt.prod_id
		# sell_prc    = mkt.prc_sell
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

	#	if sell_yn == 'Y' or show_tests_yn in ('Y','F'):
		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			msg = '    SELL TESTS - {prod_id} - Trailing Stop Loss'
			WoR(msg)
			if (sell_yn == 'Y' and sell_block_yn == 'N')  or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					self.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					self.show_sell_header_tf = True
	#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

		func_end(fnc)
		return mkt, pos, sell_yn, hodl_yn

	#<=====>#

	def sell_logic_atr_stop(self, mkt, ta, pos, sell_block_yn='N'):
		func_name = 'sell_logic_atr_stop'
		func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

	#	if sell_yn == 'Y' or show_tests_yn in ('Y','F'):
		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			msg = f'    SELL TESTS - {prod_id} - ATR Stop Loss'
			WoR(msg)
			if (sell_yn == 'Y' and sell_block_yn == 'N')  or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					self.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					self.show_sell_header_tf = True
	#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

		func_end(fnc)
		return mkt, pos, sell_yn, hodl_yn

	#<=====>#

	def sell_logic_trailing_atr_stop(self, mkt, ta, pos, sell_block_yn='N'):
		func_name = 'sell_logic_trailing_atr_stop'
		func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

	#	if sell_yn == 'Y' or show_tests_yn in ('Y','F'):
		if (sell_yn == 'Y' and sell_block_yn == 'N') or show_tests_yn in ('Y','F'):
			msg = f'    SELL TESTS - {prod_id} - Trailing ATR Stop Loss'
			WoR(msg)
			if (sell_yn == 'Y' and sell_block_yn == 'N')  or show_tests_yn in ('Y'):
				for e in all_sells:
					if pos.prc_chg_pct > 0:
						G(e)
					else:
						R(e)
					self.show_sell_header_tf = True
				for e in all_hodls:
					WoG(e)
					self.show_sell_header_tf = True
	#			print(f'sell_yn : {sell_yn}, hodl_yn : {hodl_yn}')

		func_end(fnc)
		return mkt, pos, sell_yn, hodl_yn

	#<=====>#

	def sell_logic_deny_all_green(self, mkt, ta, pos, sell_block_yn='N'):
		func_name = 'sell_logic_deny_all_green'
		func_str = f'{lib_name}.{func_name}(mkt, ta, pos, sell_block_yn={sell_block_yn})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id                   = mkt.prod_id
		all_sells                 = []
		all_hodls                 = []
		sell_block_yn             = 'N'
		show_tests_yn             = self.st.spot.sell.show_tests_yn
		rfreq                     = pos.buy_strat_freq
		freqs, faster_freqs       = freqs_get(rfreq)

#		ha_color_1min  = ta['1min']['ha_color']['ago0']
		ha_color_3min  = ta['3min']['ha_color']['ago0']
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
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
				if ha_color_4h == 'green':
					if (ha_color_30min == 'green' or ha_color_15min == 'green') and (ha_color_5min == 'green' or ha_color_3min == 'green'):
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
						green_save = True
			elif rfreq == '4h':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
				if ha_color_1h == 'green':
					if ha_color_15min == 'green' and (ha_color_5min == 'green' or ha_color_3min == 'green'):
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
						green_save = True
			elif rfreq == '1h':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
				if ha_color_30min == 'green':
					if (ha_color_5min == 'green' or ha_color_3min == 'green'):
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
						green_save = True
			elif rfreq == '30min':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   30min : {ha_color_30min}, 15min : {ha_color_15min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
				if ha_color_15min == 'green':
					if (ha_color_5min == 'green' or ha_color_3min == 'green'):
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   30min : {ha_color_30min}, 15min : {ha_color_15min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
						green_save = True
			elif rfreq == '15min':
				fail_msg = f'    * SELL COND: ALL CANDLES NOT GREEN ==> Allowing Sell...   15min : {ha_color_15min}, 5min : {ha_color_5min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
				if ha_color_5min == 'green':
					if (ha_color_5min == 'green' or ha_color_3min == 'green'):
						pass_msg = f'    * HODL COND: ALL CANDLES GREEN ==> OVERIDING SELL!!!   15min : {ha_color_15min}, 5min : {ha_color_5min}, 3min : {ha_color_3min}, sell_block_yn : {sell_block_yn}'
						green_save = True
				
			if green_save:
				sell_block_yn = 'N'
				all_hodls.append(pass_msg)
#				WoG(msg)
			else:
				msg = f'    * CANCEL SELL: ALL CANDLES NOT GREEN ==> Allowing Sell...   5min : {ha_color_5min}, 15min : {ha_color_15min}, 30min : {ha_color_30min}, sell_block_yn : {sell_block_yn}'
				all_sells.append(fail_msg)
#				R(msg)

		print(f'sell_block_yn : {sell_block_yn}, show_tests_yn : {show_tests_yn}')
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

	def pos_upd(self, pos, mkt=None, so=None):
		func_name = 'pos_upd'
		func_str = f'{lib_name}.{func_name}(pos, mkt, so)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		st         = settings.settings_load()
		prod_id    = pos.prod_id

		# Update Sell Sizing Info from Market
		if mkt:
			pos.base_size_incr   = mkt.base_size_incr
			pos.quote_size_incr  = mkt.quote_size_incr
			pos.quote_size_min   = mkt.quote_size_min
			pos.quote_size_max   = mkt.quote_size_max
			pos.base_size_min    = mkt.base_size_min
			pos.base_size_max    = mkt.base_size_max

		# Update Sell Price
		if so:
			pos.prc_curr         = so.prc_sell_act
		elif mkt:
			pos.prc_curr         = mkt.prc_sell
		else:
			print(func_str)
			print('we have neither so or mkt!!!')
			sys.exit()

		# If we have a sell order we are closing the position
		if so:
			pos.pos_stat                              = 'CLOSE'
			pos.pos_end_dttm                          = so.sell_end_dttm
			pos.sell_order_cnt                        += 1
			pos.sell_order_attempt_cnt                += 1
			pos.hold_cnt                              -= so.sell_cnt_act
			pos.tot_in_cnt                            += so.tot_in_cnt
			pos.sell_cnt_tot                          += so.sell_cnt_act
			pos.fees_cnt_tot                          += so.fees_cnt_act
			pos.sell_fees_cnt_tot                     += so.fees_cnt_act
			pos.prc_sell_avg                          = round((pos.tot_in_cnt / pos.sell_cnt_tot), 8)

		# Update Sell Price Highs & Lows
		if pos.prc_curr > pos.prc_high: pos.prc_high = pos.prc_curr
		if pos.prc_curr < pos.prc_low: pos.prc_low = pos.prc_curr

		# Update Price Change %
		pos.prc_chg_pct = calc_chg_pct(old_val=pos.prc_buy, new_val=pos.prc_curr, dec_prec=4)
		# Update Price Change % Highs & Lows
		if pos.prc_chg_pct > pos.prc_chg_pct_high: pos.prc_chg_pct_high = pos.prc_chg_pct
		if pos.prc_chg_pct < pos.prc_chg_pct_low:  pos.prc_chg_pct_low  = pos.prc_chg_pct
		# Update Price Change Drop from Highest
		pos.prc_chg_pct_drop = round(pos.prc_chg_pct - pos.prc_chg_pct_high, 2)

		# Update Gain Loss Amt
		pos.val_curr          = pos.hold_cnt * pos.prc_curr
		pos.val_tot           = pos.val_curr + pos.tot_in_cnt

		# gain_loss_amt_est is to capture the pct at the time we decide to sell and should not be updated after
		if pos.pos_stat in ('OPEN'):
			pos.gain_loss_amt     = pos.val_tot - pos.tot_out_cnt
			pos.gain_loss_amt_est = pos.val_tot - pos.tot_out_cnt
			# Update Gain Loss % Highs & Lows
			if pos.gain_loss_amt_est > pos.gain_loss_amt_est_high: pos.gain_loss_amt_est_high = pos.gain_loss_amt_est
			if pos.gain_loss_amt_est < pos.gain_loss_amt_est_low:  pos.gain_loss_amt_est_low  = pos.gain_loss_amt_est
		elif pos.pos_stat in ('CLOSE'):
			pos.gain_loss_amt     = pos.val_tot - pos.tot_out_cnt
			pos.gain_loss_amt_net = pos.gain_loss_amt

		# gain_loss_pct_est is to capture the pct at the time we decide to sell and should not be updated after
		if pos.pos_stat in ('OPEN'):
			pos.gain_loss_pct      = calc_chg_pct(old_val=pos.tot_out_cnt, new_val=pos.val_tot, dec_prec=4)
			pos.gain_loss_pct_est  = pos.gain_loss_pct
			# Update Gain Loss % Highs & Lows
			if pos.gain_loss_pct_est > pos.gain_loss_pct_est_high: pos.gain_loss_pct_est_high = pos.gain_loss_pct_est
			if pos.gain_loss_pct_est < pos.gain_loss_pct_est_low:  pos.gain_loss_pct_est_low  = pos.gain_loss_pct_est
		elif pos.pos_stat in ('CLOSE'):
			# Need a Fix Here for CLOSE
			# Update Gain Loss %
			pos.gain_loss_pct = calc_chg_pct(old_val=pos.tot_out_cnt, new_val=pos.val_tot, dec_prec=4)

		# Finalize the Pocket & Clip Info
		if pos.pos_stat == 'CLOSE':
			if pos.prc_chg_pct > 0:
				pos.pocket_pct          = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.pocket_pct, in_key=prod_id) 
				pos.clip_pct            = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.clip_pct, in_key=prod_id) 
				pos.pocket_cnt          = pos.hold_cnt
				pos.clip_cnt            = 0
			else:
				pos.pocket_pct          = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.pocket_pct, in_key=prod_id) 
				pos.clip_pct            = settings.get_ovrd(in_dict=self.st.spot.sell.rainy_day.clip_pct, in_key=prod_id)
				pos.pocket_cnt          = 0
				pos.clip_cnt            = pos.hold_cnt

		# Update to Database
		db_tbl_poss_insupd(pos)

		func_end(fnc)
		return pos

	#<=====>#

	def sell_ords_check(self):
		func_name = 'sell_ords_check'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

	def pos_close(self, pos_id, sell_order_uuid):
		func_name = 'pos_close'
		func_str = f'{lib_name}.{func_name}(pos_id={pos_id}, sell_order_uuid={sell_order_uuid})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		pos = db_pos_get_by_pos_id(pos_id)
		pos = dec_2_float(pos)
		pos = AttrDictConv(in_dict=pos)

		so  = db_sell_ords_get_by_uuid(sell_order_uuid)
		so  = dec_2_float(so)
		so  = AttrDictConv(in_dict=so)

		pos = self.pos_upd(pos=pos, mkt=None, so=so)

		func_end(fnc)

	#<=====>#

	def buy_header(self, prod_id):
		func_name = 'buy_header'
		func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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
		chart_mid(in_str=title_msg, len_cnt=240)
		chart_headers(in_str=hmsg, len_cnt=240)
		self.show_buy_header_tf = False
		buy_log('')
		wmsg = f'{dttm_get()} ==> {hmsg}'
		buy_log(wmsg)

		func_end(fnc)

	#<=====>#

	def sell_header(self, prod_id):
		func_name = 'sell_header'
		func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

		sell_log('')
		wmsg = f'{dttm_get()} ==> {hmsg}'
		sell_log(wmsg)

		title_msg = f'* SELL LOGIC * {prod_id} *'
		chart_mid(in_str=title_msg, len_cnt=240)
		chart_headers(in_str=hmsg, len_cnt=240)

		self.show_sell_header_tf = False

		func_end(fnc)

	#<=====>#

	def buy_disp(self, mkt, trade_strat_perf):
		func_name = 'buy_disp'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id          = mkt.prod_id
		show_tests_yn    = self.st.spot.buy.show_tests_yn
		show_tests_min   = self.st.spot.buy.show_tests_min

		if self.show_buy_header_tf:
			self.buy_header(prod_id)
			self.show_buy_header_tf = False

		msg1 = ''
		msg1 += f'{trade_strat_perf.prod_id:<15} | '
		msg1 += f'{trade_strat_perf.buy_strat_name:<15} | '
		msg1 += f'{trade_strat_perf.buy_strat_freq:<15} | '
		msg1 += f'{int(trade_strat_perf.tot_cnt):>5} | '
		msg1 += f'{int(trade_strat_perf.open_cnt):>5} | '
		msg1 += f'{int(trade_strat_perf.close_cnt):>5} | '
		msg1 += f'{int(trade_strat_perf.win_cnt):>5} | '
		msg1 += f'{int(trade_strat_perf.lose_cnt):>5} | '
		msg1 += f'{trade_strat_perf.win_pct:>6.2f} % | '
		msg1 += f'{trade_strat_perf.lose_pct:>6.2f} % | '
		msg1 += f'{trade_strat_perf.gain_loss_amt:>10.2f} | '
		msg1 += f'{trade_strat_perf.gain_loss_pct:>10.2f} % | '
		msg1 += f'{trade_strat_perf.gain_loss_pct_hr:>10.2f} % | '
		msg1 += f'{trade_strat_perf.gain_loss_pct_day:>10.2f} % | '
		msg1 += f'{trade_strat_perf.strat_last_elapsed:>7} | '
		msg1 += f'{trade_strat_perf.trade_size:>16.8f} | '

		msg2 = ''
		msg2 += f' | {int(trade_strat_perf.pass_cnt):>4} | '
		msg2 += f'{int(trade_strat_perf.fail_cnt):>4} | '
		msg2 += f'{trade_strat_perf.pass_pct:>6.2f} % | '

		wmsg = f'{dttm_get()} ==> {msg1}{msg2}'
		buy_log(wmsg)

		in_str_len1 = len(msg1)
		in_str_len2 = len(msg2)
		in_str_len  = in_str_len1 + in_str_len2

		if trade_strat_perf.tot_cnt > 0:
			msg1 = cs_pct_color_50(pct=trade_strat_perf.win_pct, msg=msg1)
		msg2 = cs_pct_color_100(pct=trade_strat_perf.pass_pct, msg=msg2)

		if trade_strat_perf.pass_pct > 0:
			msg = f'{msg1}{msg2}'
			print(msg)
		else:
			msg = msg1

		for msg in trade_strat_perf.all_passes:
			buy_log(msg)
			if trade_strat_perf.buy_yn == 'Y' or show_tests_yn in ('Y') or trade_strat_perf.pass_pct >= show_tests_min:
				G('|' + msg)
				self.show_buy_header_tf = True

		for msg in trade_strat_perf.all_fails:
			buy_log(msg)
			if trade_strat_perf.buy_yn == 'Y' or show_tests_yn in ('Y') or trade_strat_perf.pass_pct >= show_tests_min:
				R( '|' + msg)
				self.show_buy_header_tf = True

		func_end(fnc)

	#<=====>#

	def sell_disp(self, pos):
		func_name = 'sell_disp'
		func_str = f'{lib_name}.{func_name}(pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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
		msg += f'{pos.prod_id:<12} | '
		msg += f'{test_tf:^1} | '
		msg += f'{pos.pos_id:^6} | '
		msg += f'{pos.buy_strat_name:^12} | '
		msg += f'{pos.buy_strat_freq:^5} | '
		msg += f'{disp_age:^10} | '
		msg += f'{pos.tot_out_cnt:>16.8f} | '
		msg += f'{pos.val_curr:>14.8f} | '
		msg += f'{pos.prc_buy:>14.8f} | '
		msg += f'{pos.prc_curr:>14.8f} | '
		msg += f'{pos.prc_high:>14.8f} | '
		msg += f'{pos.prc_chg_pct:>8.2f} % | '
		msg += f'{pos.prc_chg_pct_high:>8.2f} % | '
		msg += f'{pos.prc_chg_pct_low:>8.2f} % | '
		msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
		msg += f'$ {pos.gain_loss_amt:>14.8f} | '
		msg += f'$ {pos.gain_loss_amt_est_high:>14.8f}'

		wmsg = f'{dttm_get()} ==> {msg}'
		sell_log(wmsg)

		in_str_len = len(msg)
		msg = '|' + cs_pct_color(pos.prc_chg_pct, msg)
		print(msg)

		func_end(fnc)

	#<=====>#

	def buy_log(self, msg):
		func_name = 'buy_log'
		func_str = f'{lib_name}.{func_name}(msg)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		dt_str  = dt.now().strftime('%Y_%m_%d')
		logfile = f"logs_buy/{dt_str}_buy_log.txt"
		wmsg    = f'{dttm_get()} ==> {msg}'
		file_write(logfile, wmsg)

		func_end(fnc)

	#<=====>#

	def sell_log(self, msg):
		func_name = 'sell_log'
		func_str = f'{lib_name}.{func_name}(msg)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		dt_str  = dt.now().strftime('%Y_%m_%d')
		logfile = f"logs_sell/{dt_str}_sell_log.txt"
		wmsg    = f'{dttm_get()} ==> {msg}'
		file_write(logfile, wmsg)

		func_end(fnc)

	#<=====>#

	def buy_test(self, mkt, trade_strat_perf):
		func_name = 'buy_test'
		func_str = f'{lib_name}.{func_name}(mkt, trade_strat_perf)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		beep()

		bo = AttrDict()
		bo.test_tf               = 1
		bo.prod_id               = mkt.prod_id
		bo.buy_order_uuid        = self.gen_guid()
		bo.pos_type              = 'SPOT'
		bo.ord_stat              = 'OPEN'
		bo.buy_strat_type        = trade_strat_perf.buy_strat_type
		bo.buy_strat_name        = trade_strat_perf.buy_strat_name
		bo.buy_strat_freq        = trade_strat_perf.buy_strat_freq
		bo.buy_begin_dttm        = dt.now()
		bo.buy_end_dttm          = dt.now()
		bo.buy_curr_symb         = mkt.base_curr_symb
		bo.spend_curr_symb       = mkt.quote_curr_symb
		bo.fees_curr_symb        = mkt.quote_curr_symb
		bo.buy_cnt_est           = (trade_strat_perf.target_trade_size * 0.996) / mkt.prc_buy
		bo.buy_cnt_act           = (trade_strat_perf.target_trade_size * 0.996) / mkt.prc_buy
		bo.fees_cnt_act          = (trade_strat_perf.target_trade_size * 0.004) / mkt.prc_buy
		bo.tot_out_cnt           = trade_strat_perf.target_trade_size
		bo.prc_buy_est           = mkt.prc_buy
		bo.prc_buy_est           = mkt.prc_buy
		bo.tot_prc_buy           = mkt.prc_buy
		bo.prc_buy_slip_pct      = 0

		db_tbl_buy_ords_insupd(bo)
		time.sleep(.33)

		func_end(fnc)

	#<=====>#

	def sell_test(self, mkt, pos):
		func_name = 'sell_test'
		func_str = f'{lib_name}.{func_name}(pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		beep()

		so = AttrDict()
		so.test_tf                     = pos.test_tf
		so.prod_id                     = pos.prod_id
		so.mkt_name                    = pos.mkt_name
		so.pos_id                      = pos.pos_id
		so.sell_seq_nbr                = 1
		so.sell_order_uuid             = self.gen_guid()	
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
		so.fees_cnt_act                = (pos.hold_cnt * mkt.prc_sell) * 0.004
		so.tot_in_cnt                  = (pos.hold_cnt * mkt.prc_sell) * 0.996
		so.prc_sell_est                = mkt.prc_sell
		so.prc_sell_act                = mkt.prc_sell
		so.tot_prc_buy                 = mkt.prc_sell
		so.prc_sell_slip_pct           = 0

		db_tbl_sell_ords_insupd(so)
		time.sleep(.33)

		func_end(fnc)
		return pos

	#<=====>#

	def gen_guid(self):
		func_name = 'gen_guid'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		guid = str(uuid.uuid4())

		func_end(fnc)
		return guid

	#<=====>#

	def buy_live(self, mkt, trade_strat_perf):
		func_name = 'buy_live'
		func_str = f'{lib_name}.{func_name}(mkt)'
		G(func_str)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)

		if self.st.spot.buy.buy_limit_yn == 'Y':
			try:
				self.ord_lmt_buy_open(mkt, trade_strat_perf)
			except Exception as e:
				print(f'{func_name} ==> buy limit order failed, attempting market... {e}')
				play_beep(reps=3)
#				self.ord_mkt_buy(mkt, trade_strat_perf)
				self.ord_mkt_buy_orig(mkt, trade_strat_perf)
		else:
#			self.ord_mkt_buy(mkt, trade_strat_perf)
			self.ord_mkt_buy_orig(mkt, trade_strat_perf)

		func_end(fnc)

	#<=====>#

	def sell_live(self, mkt, pos):
		func_name = 'sell_live'
		func_str = f'{lib_name}.{func_name}(mkt, pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		if self.st.spot.sell.sell_limit_yn == 'N' and mkt.mkt_limit_only_tf == 1:
			print(f'{mkt.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')
			pos = self.ord_mkt_sell_orig(mkt, pos)
		elif self.st.spot.sell.sell_limit_yn == 'Y':
			try:
				pos = self.ord_lmt_sell_open(mkt, pos) 
			except Exception as e:
				print(f'{func_name} ==> sell limit order failed, attempting market... {e}')
				play_beep(reps=3)
				pos = self.ord_mkt_sell_orig(mkt, pos)
		else:
			pos = self.ord_mkt_sell_orig(mkt, pos)

		func_end(fnc)
		return pos

	#<=====>#

	def ord_mkt_buy(self, mkt, trade_strat_perf):
		func_name = 'ord_mkt_buy'
		func_str = f'{lib_name}.{func_name}(mkt)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

	def ord_mkt_sell(self, mkt, pos):
		func_name = 'ord_mkt_sell'
		func_str = f'{lib_name}.{func_name}(mkt, pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

	def ord_mkt_buy_orig(self, mkt, trade_strat_perf):
		func_name = 'ord_mkt_buy_orig'
		func_str = f'{lib_name}.{func_name}(mkt)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

	def ord_mkt_sell_orig(self, mkt, pos):
		func_name = 'ord_mkt_sell_orig'
		func_str = f'{lib_name}.{func_name}(mkt, pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

	def ord_lmt_buy_open(self, mkt, trade_strat_perf):
		func_name = 'ord_lmt_buy_open'
		func_str = f'{lib_name}.{func_name}(mkt)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id               = mkt.prod_id
		spend_amt             = str(trade_strat_perf.trade_size)
#		buy_prc               = mkt.prc_buy

#		order = cb.fiat_limit_buy(prod_id, spend_amt, buy_prc, price_multiplier=".995")
		order = cb.fiat_limit_buy(prod_id, spend_amt, price_multiplier=".995")
		self.refresh_wallet_tf       = True
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
#			bo.buy_client_order_id   = o['success_response']['client_order_id']
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

	def ord_lmt_sell_open(self, mkt, pos):
		func_name = 'ord_lmt_sell_open'
		func_str = f'{lib_name}.{func_name}(mkt, pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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
#			so.sell_client_order_id  =  # o['success_response']['client_order_id']
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

	def buy_sign_rec(self, mkt, trade_strat_perf):
		func_name = 'buy_sign_rec'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perf)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

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

	def sell_sign_rec(self, pos):
		func_name = 'sell_sign_rec'
		func_str = f'{lib_name}.{func_name}(pos)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		ss = {}
		ss = {}
		ss["test_tf"]              = pos.test_tf
		ss["prod_id"]              = pos.prod_id
		ss["pos_id"]               = pos.pos_id
		ss["sell_strat_type"]      = pos.sell_strat_type
		ss["sell_strat_name"]      = pos.sell_strat_name
		ss["sell_strat_freq"]      = pos.sell_strat_freq
#		ss["sell_asset_type"]      = pos.sell_asset_type
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
# Functions
#<=====>#

#<=====>#
# Post Variables
#<=====>#

bot = BOT()

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	bot.bot()

#<=====>#

'''
				"AAVE-USDC",
				"ADA-USDC",
				"AKT-USDC",
				"ALGO-USDC",
				"APT-USDC",
				"AR-USDC",
				"ARB-USDC",
				"ATOM-USDC",
				"AVAX-USDC",
				"BADGER-USDC",
				"BEAM-USDC",
				"BNB-USDC",
				"BNX-USDC",
				"BONK-USDC",
				"BTC-USDC",
				"BTT-USDC",
				"DOGE-USDC",
				"DOT-USDC",
				"DYP-USDC",
				"ETH-USDC",
				"FET-USDC",
				"FIL-USDC",
				"FLOW-USDC",
				"FTM-USDC",
				"FX-USDC",
				"GAL-USDC",
				"GFI-USDC",
				"GLM-USDC",
				"GRT-USDC",
				"HBAR-USDC",
				"HNT-USDC",
				"HONEY-USDC",
				"ICP-USDC",
				"IMX-USDC",
				"INJ-USDC",
				"JASMY-USDC",
				"JUP-USDC",
				"KLAY-USDC",
				"LDO-USDC",
				"LINK-USDC",
				"MATH-USDC",
				"MATIC-USDC",
				"MKR-USDC",
				"MNDE-USDC",
				"NEAR-USDC",
				"OMNI-USDC",
				"ONDO-USDC",
				"OP-USDC",
				"PEPE-USDC",
				"PYTH-USDC",
				"RENDER-USDC",
				"RNDR-USDC",
				"SEI-USDC",
				"SHIB-USDC",
				"SHPING-USDC",
				"SOL-USDC",
				"STRK-USDC",
				"STX-USDC",
				"SUI-USDC",
				"SUKU-USDC",
				"SWFTC-USDC",
				"TIA-USDC",
				"TNSR-USDC",
				"TON-USDC",
				"TRB-USDC",
				"TVK-USDC",
				"UMA-USDC",
				"UNI-USDC",
				"VET-USDC",
				"W-USDC",
				"WIF-USDC",
				"XRP-USDC"
'''

'''
				"ADA-USDC",
				"AVAX-USDC",
				"BONK-USDC",
				"BTC-USDC",
				"DOGE-USDC",
				"ETH-USDC",
				"LDO-USDC",
				"MATIC-USDC",
				"OMNI-USDC",
				"RNDR-USDC",
				"SHIB-USDC",
				"SOL-USDC",
				"UNI-USDC",
				"WIF-USDC"
'''

'''
				"ADA-USDC",
				"AVAX-USDC",
				"BADGER-USDC",
				"BNB-USDC",
				"BONK-USDC",
				"BTC-USDC",
				"DOGE-USDC",
				"DOT-USDC",
				"ETH-USDC",
				"HONEY-USDC",
				"ICP-USDC",
				"JASMY-USDC",
				"LDO-USDC",
				"MATIC-USDC",
				"OMNI-USDC",
				"RNDR-USDC",
				"SHIB-USDC",
				"SOL-USDC",
				"SUI-USDC",
				"TON-USDC",
				"UNI-USDC",
				"WIF-USDC",
				"XRP-USDC"
'''

