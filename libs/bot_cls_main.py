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
from libs.lib_strings                  import *

from libs.bot_cls_buy                  import *
from libs.bot_cls_sell                 import *
from libs.bot_common                   import *
from libs.bot_coinbase                 import *
from libs.bot_db_read                  import *
from libs.bot_db_write                 import *
from libs.bot_logs                     import *
from libs.bot_secrets                  import secrets
from libs.bot_settings                 import settings
from libs.bot_strats_buy               import *
from libs.bot_strats_sell              import *
from libs.bot_ta                       import *
from libs.bot_theme                    import *

from libs.bot_reports                  import report_buys_recent
from libs.bot_reports                  import report_open
from libs.bot_reports                  import report_open_by_age
from libs.bot_reports                  import report_open_by_prod_id
from libs.bot_reports                  import report_sells_recent


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_cls_main'
log_name      = 'bot_cls_main'
lib_secs_max  = 2

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
#		print('calling cb_mkts_refresh')
		cb_mkts_refresh()
		self.refresh_wallet_tf         = True
		self.wallet_refresh(force_tf=True)
		self.show_buy_header_tf        = True
#		self.show_sell_header_tf       = True
		# don't change this value, need more codiging for USDT or USD, someday integrae USDT/USD/BTC/ETH
		self.quote_curr_symb           = 'USDC'
		self.mode                      = 'full' # full, auto, buy, sell
		self.mode_sub                  = None

	buy_logic                      = buy_logic
	buy_logic_mkt_boosts           = buy_logic_mkt_boosts
	buy_logic_strat_boosts         = buy_logic_strat_boosts
	buy_logic_deny                 = buy_logic_deny
	buy_logic_mkt_deny             = buy_logic_mkt_deny
	buy_logic_strat_deny           = buy_logic_strat_deny
	buy_ords_check                 = buy_ords_check
	buy_header                     = buy_header
	disp_buy                       = disp_buy
	buy_log                        = buy_log
	buy_sign_rec                   = buy_sign_rec
	ord_mkt_buy                    = ord_mkt_buy
	ord_mkt_buy_orig               = ord_mkt_buy_orig
	ord_lmt_buy_open               = ord_lmt_buy_open
	# sell_logic                     = sell_logic
	# sell_pos_logic                 = sell_pos_logic
	# sell_pos_blocks                = sell_pos_blocks
	# sell_logic_forced              = sell_logic_forced
	# sell_logic_hard_profit         = sell_logic_hard_profit
	# sell_logic_hard_stop           = sell_logic_hard_stop
	# sell_logic_trailing_profit     = sell_logic_trailing_profit
	# sell_logic_trailing_stop       = sell_logic_trailing_stop
	# sell_logic_atr_stop            = sell_logic_atr_stop
	# sell_logic_trailing_atr_stop   = sell_logic_trailing_atr_stop
	# sell_logic_deny_all_green      = sell_logic_deny_all_green
	# sell_header                    = sell_header
	# disp_sell                      = disp_sell
	# disp_sell_tests                = disp_sell_tests
	# sell_log                       = sell_log
	# sell_sign_rec                  = sell_sign_rec
	# ord_mkt_sell                   = ord_mkt_sell
	# ord_mkt_sell_orig              = ord_mkt_sell_orig
	# ord_lmt_sell_open              = ord_lmt_sell_open
	# sell_ords_check                = sell_ords_check


	#<=====>#

	def before_start(self):
		func_name = 'before_start'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=30)
#		G(func_str)

		# this is here just to proof that sounds alerts will be heard
		if self.st.speak_yn == 'Y': speak_async('Coinbase Trade Bot Online')

		self.wallet_refresh(force_tf=True)
		db_table_csvs_dump()

		func_end(fnc)

	#<=====>#

	def bot_loop(self):
		func_name = 'bot_loop'
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
				print_adv(4)

				self.st = settings.reload()

#				print('calling cb_mkts_refresh')
				cb_mkts_refresh()

				if self.mode in ('buy'):
					# intentionaly here, keep single threaded
#					self.sell_ords_check()
					self.buy_ords_check()
					report_buys_recent(cnt=20)
				elif self.mode in ('sell'):
					self.sell_ords_check()
					report_sells_recent(cnt=20)
				else:
					self.buy_ords_check()
					self.sell_ords_check()
					report_buys_recent(cnt=20)
					report_sells_recent(cnt=20)

				self.wallet_refresh(force_tf=True)
				self.mkts_loop()

				if self.mode in ('buy'):
					# intentionaly here, keep single threaded
#					self.sell_ords_check()
					self.buy_ords_check()
					report_buys_recent(cnt=20)
				elif self.mode in ('sell'):
					self.sell_ords_check()
					report_open_by_age()
					report_sells_recent(cnt=20)
				else:
					self.buy_ords_check()
					self.sell_ords_check()
					report_open_by_age()
					report_buys_recent(cnt=20)
					report_sells_recent(cnt=20)

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

					hmsg = f"$ {'usdc bal':^9} | $ {'reserve':^9} | $ {'available':^9} | {'reserves state':^14} | "
					WoM(hmsg)

					for trade_curr in self.trade_currs:
						msg = f"$ {self.bal_avails[trade_curr]:>9.2f} | $ {self.reserve_amts[trade_curr]:>9.2f} | $ {self.spendable_amts[trade_curr]:>9.2f} | "
						if self.reserve_locked_tf:
							msg += f"{'LOCKED':^14} | "
						else:
							msg += f"{'UNLOCKED':^14} | "
						WoG(msg)

				print_adv(4)
				WoB(f"{'<----- // ===== | == END == | ===== \\ ----->':^200}")
				print_adv(4)

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

	def auto_loop(self):
		func_name = 'auto_loop'
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
				print_adv(4)

				self.st = settings.reload()

				self.sell_ords_check()
				self.buy_ords_check()
#				print('calling cb_mkts_refresh')
				cb_mkts_refresh()
				self.wallet_refresh(force_tf=True)

				self.mkts_lists_get()
				self.mkts_loop()

				self.sell_ords_check()
				self.buy_ords_check()

				report_buys_recent(cnt=20)
				report_sells_recent(cnt=20)
				report_open_by_age()

		#		# End of Market Loop Balance Display
				self.wallet_refresh()


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

				print_adv(4)
				WoB(f"{'<----- // ===== | == END == | ===== \\ ----->':^200}")
				print_adv(4)

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

	def mkt_build(self, m):
		func_name = 'mkt_build'
		func_str = f'{lib_name}.{func_name}(m)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=3)
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
		bid_prc, ask_prc                         = cb_bid_ask_by_amt_get(mkt=m, buy_sell_size=pricing_cnt)
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
		mkt, trade_perf                          = self.buy_logic_mkt_boosts(mkt, trade_perf)

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

	def disp_mkt(self, mkt, trade_perf, trade_strat_perfs):
		func_name = 'disp_mkt'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=3)
#		G(func_str)

		self.disp_mkt_summary(mkt, trade_perf, trade_strat_perfs)
		self.disp_mkt_stats(mkt, trade_perf, trade_strat_perfs)
		self.disp_mkt_performance(mkt, trade_perf, trade_strat_perfs)

		func_end(fnc)
		return mkt, trade_perf, trade_strat_perfs

	#<=====>#

	def disp_mkt_summary(self, mkt, trade_perf, trade_strat_perfs):
		func_name = 'disp_mkt_summary'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=3)
#		G(func_str)

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
		if mkt.prc_pct_chg_24h < 0:
			msg += cs(f"$ {mkt.prc_mkt:>14.8f}", 'white', 'red') + " | "
			msg += cs(f"{mkt.prc_pct_chg_24h:>10.4f} %", 'white', 'red') + " | "
		elif mkt.prc_pct_chg_24h > 0:
			msg += cs(f"$ {mkt.prc_mkt:>14.8f}", 'white', 'green') + " | "
			msg += cs(f"{mkt.prc_pct_chg_24h:>10.4f} %", 'white', 'green') + " | "
		else:
			msg += f"$ {mkt.prc_mkt:>14.8f} | "
			msg += f"{mkt.prc_pct_chg_24h:>10.4f} % | "

		msg += f"$ {mkt.prc_buy:>14.8f} | "
		msg += f"$ {mkt.prc_sell:>14.8f} | "
		msg += f"{mkt.prc_buy_diff_pct:>10.4f} % | "
		msg += f"{mkt.prc_sell_diff_pct:>10.4f} % | "

		if mkt.prc_range_pct < 0:
			msg += cs(f"{mkt.prc_range_pct:>10.4f} %", 'white', 'red') + " | "
		elif mkt.prc_range_pct > 0:
			msg += cs(f"{mkt.prc_range_pct:>10.4f} %", 'white', 'green') + " | "
		else:
			msg += f"{mkt.prc_range_pct:>10.4f} %" + " | "

		msg += cs(f"$ {mkt.bal_avail:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {mkt.reserve_amt:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {mkt.spendable_amt:>9.2f}", "white", "green") + " | "
		if self.reserve_locked_tf:
			msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
		else:
			msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
		chart_headers(in_str=hmsg, len_cnt=240, bold=True)
		chart_row(in_str=msg, len_cnt=240)
		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)
		return mkt, trade_perf, trade_strat_perfs

	#<=====>#

	def disp_mkt_stats(self, mkt, trade_perf, trade_strat_perfs):
		func_name = 'disp_mkt_stats'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=3)
#		G(func_str)

		# Market Basics
		prod_id = mkt.prod_id


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
		msg += f'{trade_perf.tot_cnt:>9}' + ' | '
		msg += cs(f'{trade_perf.win_cnt:>9}', font_color='white', bg_color='green') + ' | '
		msg += cs(f'{trade_perf.lose_cnt:>9}', font_color='white', bg_color='red') + ' | '
		msg += cs(f'{trade_perf.win_pct:>9.2f} %', font_color='white', bg_color='green') + ' | '
		msg += cs(f'{trade_perf.lose_pct:>9.2f} %', font_color='white', bg_color='red') + ' | '
		msg += cs(f'$ {trade_perf.win_amt:>9.4f}', font_color='white', bg_color='green') + ' | '
		msg += cs(f'$ {trade_perf.lose_amt:>9.4f}', font_color='white', bg_color='red') + ' | '
		msg += f'$ {trade_perf.tot_out_cnt:>9.4f}' + ' | '
		msg += f'$ {trade_perf.tot_in_cnt:>9.4f}' + ' | '
		msg += f'$ {trade_perf.val_curr:>9.4f}' + ' | '
		msg += f'$ {trade_perf.val_tot:>9.4f}' + ' | '
		if trade_perf.gain_loss_amt > 0:
			msg += cs(f'$ {trade_perf.gain_loss_amt:>9.4f}', font_color='white', bg_color='green') + ' | '
			msg += cs(f'{trade_perf.gain_loss_pct:>9.4f} %', font_color='white', bg_color='green') + ' | '
			msg += cs(f'{trade_perf.gain_loss_pct_hr:>9.4f} %', font_color='white', bg_color='green') + ' | '
			msg += cs(f'{trade_perf.gain_loss_pct_day:>9.4f} %', font_color='white', bg_color='green') + ' | '
		else:
			msg += cs(f'$ {trade_perf.gain_loss_amt:>9.4f}', font_color='white', bg_color='red') + ' | '
			msg += cs(f'{trade_perf.gain_loss_pct:>9.4f} %', font_color='white', bg_color='red') + ' | '
			msg += cs(f'{trade_perf.gain_loss_pct_hr:>9.4f} %', font_color='white', bg_color='red') + ' | '
			msg += cs(f'{trade_perf.gain_loss_pct_day:>9.4f} %', font_color='white', bg_color='red') + ' | '
		msg += f'{trade_perf.last_elapsed:>9}' + ' | '

		title_msg = f'* Market Stats * {prod_id} *'
		chart_mid(in_str=title_msg, len_cnt=240, bold=True)
		chart_headers(in_str=hmsg, len_cnt=240, bold=True)
		chart_row(msg, len_cnt=240)

		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)
		return mkt, trade_perf, trade_strat_perfs

	#<=====>#

	def disp_mkt_performance(self, mkt, trade_perf, trade_strat_perfs):
		func_name = 'disp_mkt_performance'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=3)
#		G(func_str)

		# Market Basics
		prod_id = mkt.prod_id

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

		title_msg = '* Strategy Past Performance *'
		chart_mid(in_str=title_msg, len_cnt=240, bold=True)
		chart_headers(hmsg, len_cnt=240, bold=True)

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
				msg += f'{x.strat_last_elapsed:>7}' + ' | '
				msg  = cs_pct_color_50(pct=x.win_pct, msg=msg)
				chart_row(in_str=msg, len_cnt=240)
		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)
		return mkt, trade_perf, trade_strat_perfs

	#<=====>#

	def mkts_lists_get(self):
		func_name = 'mkts_lists_get'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

#		chart_top(in_str='Market Collection', len_cnt=177)

		self.loop_mkts       = []
		self.buy_mkts        = []
		self.sell_mkts       = []

		if self.mode in ('buy', 'full'):
			self.buy_mkts = self.mkts_lists_buy_get()
			hmsg = f'buy mkts ({len(self.buy_mkts)}) :'
			chart_mid(in_str=hmsg, len_cnt=177)
			self.prt_cols(self.buy_mkts, cols=10)
			chart_bottom(len_cnt=177)
			print_adv()

		if self.mode in ('sell', 'full'):
			self.sell_mkts = self.mkts_lists_sell_get()
			hmsg = f'sell mkts ({len(self.sell_mkts)}) :'
			chart_mid(in_str=hmsg, len_cnt=177)
			self.prt_cols(self.sell_mkts, cols=10)
			chart_bottom(len_cnt=177)
			print_adv()

		self.loop_mkts.extend(self.buy_mkts)
		self.loop_mkts.extend(self.sell_mkts)

		stable_mkts           = self.st.spot.mkts.stable_mkts
		err_mkts              = self.st.spot.mkts.err_mkts
		mkts                  = db_mkts_loop_get(mode=self.mode, loop_mkts=self.loop_mkts, stable_mkts=stable_mkts, err_mkts=err_mkts)
		# Iterates through the mkts returned from MySQL and converts all decimals to floats
		# This is faster than making everything be done in decimals (which I would prefer)
		mkts                  = dec_2_float(mkts)
		self.loop_mkts        = mkts

#		# Display the markets that will be looped
#		disp_mkts = []
#		for m in self.loop_mkts:
#			disp_mkts.append(m['prod_id'])
#		hmsg = f'loop mkts ({len(self.loop_mkts)}) :'
#		chart_mid(in_str=hmsg, len_cnt=177)
#		self.prt_cols(disp_mkts, cols=10)

		# # Display the markets that will be looped
		# if self.mode in ('full', 'buy'):

		# # Display the markets that will be looped
		# if self.mode in ('full', 'sell'):

		func_end(fnc)

	#<=====>#

	def mkts_lists_buy_get(self):
		func_name = 'mkts_lists_buy_get'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		buy_mkts = []

		chart_top(in_str='Buy Market Collection', len_cnt=177)

		# get mkts from settings
		spot_mkts  = self.st.spot.mkts.trade_mkts
		if spot_mkts:
			mkts = list(set(spot_mkts))
			buy_mkts.extend(mkts)

		# Get The Markets with the best performance on the bot so far
		# By Gain Loss Percen Per Hour
		# Settings how many of these we will look at
		pct_min    = self.st.spot.mkts.extra_mkts_top_bot_perf_pct_min
		lmt_cnt    = self.st.spot.mkts.extra_mkts_top_bot_perf_cnt
		mkts       = db_mkts_loop_top_perfs_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min)
		if mkts:
			if self.st.spot.mkts.extra_mkts_top_bot_perf_yn == 'Y':
				hmsg = f'adding mkts top bot gain loss percent per day performers ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='WoG')
				buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_top_bot_perf_cnt > 0:
				hmsg = f'skipping mkts top bot gain loss percent per day performers ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the best performance on the bot so far
		# By Gain Loss Amount Total
		# Settings how many of these we will look at
		lmt_cnt    = self.st.spot.mkts.extra_mkts_top_bot_gains_cnt
		mkts       = db_mkts_loop_top_gains_prod_ids_get(lmt=lmt_cnt)
		if mkts:
			if self.st.spot.mkts.extra_mkts_top_bot_gains_yn == 'Y':
				hmsg = f'adding mkts top bot gain loss performers ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='WoG')
				buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_top_bot_gains_cnt > 0:
				hmsg = f'skipping mkts top bot gain loss performers ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h price increase
		# Settings how many of these we will look at
		pct_min    = self.st.spot.mkts.extra_mkts_prc_pct_chg_24h_pct_min
		lmt_cnt    = self.st.spot.mkts.extra_mkts_prc_pct_chg_24h_cnt
		mkts       = db_mkts_loop_top_prc_chg_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min)
		if mkts:
			if self.st.spot.mkts.extra_mkts_prc_pct_chg_24h_yn == 'Y':
				hmsg = f'adding mkts top price increases ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='WoG')
				buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_prc_pct_chg_24h_cnt > 0:
				hmsg = f'skipping mkts top price increases ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h volume increase
		# Settings how many of these we will look at
		lmt_cnt    = self.st.spot.mkts.extra_mkts_vol_quote_24h_cnt
		mkts       = db_mkts_loop_top_vol_chg_prod_ids_get(lmt=lmt_cnt)
		if mkts:
			if self.st.spot.mkts.extra_mkts_vol_quote_24h_yn == 'Y':
				hmsg = f'adding mkts highest volume ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='WoG')
				buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_vol_quote_24h_cnt > 0:
				hmsg = f'skipping mkts highest volume ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h volume percent increase
		# Settings how many of these we will look at
		lmt_cnt    = self.st.spot.mkts.extra_mkts_vol_pct_chg_24h_cnt
		mkts       = db_mkts_loop_top_vol_chg_pct_prod_ids_get(lmt=lmt_cnt)
		if mkts:
			if self.st.spot.mkts.extra_mkts_vol_pct_chg_24h_yn == 'Y':
				hmsg = f'adding mkts highest volume increase ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='WoG')
				buy_mkts.extend(mkts)
			elif self.st.spot.mkts.extra_mkts_vol_pct_chg_24h_cnt > 0:
				hmsg = f'skipping mkts highest volume increase ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets that are marked as favorites on Coinbase
		mkts       = db_mkts_loop_watched_prod_ids_get()
		if mkts:
			if self.st.spot.mkts.extra_mkts_watched_yn == 'Y':
				hmsg = f'adding watched markets ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='WoG')
				buy_mkts.extend(mkts)
			else:
				hmsg = f'skipping watched markets ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				self.prt_cols(mkts, cols=10, clr='GoW')

		func_end(fnc)
		return buy_mkts

	#<=====>#

	def mkts_lists_sell_get(self):
		func_name = 'mkts_lists_sell_get'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		chart_top(in_str='Sell Market Collection', len_cnt=177)

		sell_mkts = []

		# Get The Markets with Open Positions
		# They all need to be looped through buy/sell logic
		mkts       = db_mkts_loop_poss_open_prod_ids_get()
		if mkts:
			mkts = list(set(mkts))
			hmsg = f'adding markets with open positions ({len(mkts)}) :'
			chart_mid(in_str=hmsg, len_cnt=177)
			self.prt_cols(mkts, cols=10)

			sell_mkts.extend(mkts)

		func_end(fnc)
		return sell_mkts

	#<=====>#

	def mkts_loop(self):
		func_name = 'mkts_loop'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=12)
#		G(func_str)

		print_adv(3)
		WoM(f"{'Markets Loop':^200}")
		print_adv(1)

		self.mkts_lists_get()

		cnt = 0
		# loop through all mkts for buy/sell logic
		t0 = time.perf_counter()

		dttm_start_loop = dttm_get()	
		t_loop = time.perf_counter()

		self.ohlcv_tables_check()

		for m in self.loop_mkts:
			cnt += 1
			t00 = time.perf_counter()

			m = AttrDictConv(in_dict=m)

			prod_id = m.prod_id
			first_letter = left(prod_id,1).lower()

			if self.mode == 'sell':
#				print_adv()
#				print_adv()

#				print(f'm.check_mkt_dttm : {m.check_mkt_dttm} ({type(m.check_mkt_dttm)})')
				check_mkt_dttm = db_poss_check_mkt_dttm_get(prod_id)
#				print(f'check_mkt_dttm   : {check_mkt_dttm} ({type(check_mkt_dttm)})')

				if check_mkt_dttm > m.check_mkt_dttm:
#					YoM(f'another bot with mode sell has updated {prod_id} market since starting... skipping...')
					print_adv(2)
					YoK(f'another bot with mode sell has updated {prod_id} market since starting..., old : {m.check_mkt_dttm}, new : {check_mkt_dttm} skipping...')
#					YoM(f'another bot with mode sell has updated {prod_id} market since starting... skipping...')
#					print_adv()
#					print_adv()
					continue

				db_poss_check_mkt_dttm_upd(prod_id)
				check_mkt_dttm = db_poss_check_mkt_dttm_get(prod_id)
				m.check_mkt_dttm = check_mkt_dttm

				# if self.mode_sub == 1:
				# 	if first_letter not in ('a','c','e','g','i','k','m','o','q','s','u','w','y','1','3','5','7','9'):
				# 		continue
				# 	# # check if cnt is divisible by 2
				# 	# if cnt % 2 == 0:
				# 	# 	continue
				# if self.mode_sub == 2:
				# 	if first_letter not in ('b','d','f','h','j','l','n','p','r','t','v','x','z','0','2','4','6','8'):
				# 		continue
				# 	# # check if cnt is divisible by 2
				# 	# if cnt % 2 != 0:
				# 	# 	continue

			# formatting the mkt
			prod_id = m['prod_id']
			m = dec_2_float(m)
			m = AttrDictConv(in_dict=m)

			# This is only for disp_mkt
			m.cnt = cnt
			m.mkts_tot = len(self.loop_mkts)

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

			title_msg = f'* Market Summary * {prod_id} * {dttm_get()} * {dttm_start_loop} * {loop_age} * {cnt}/{len(self.loop_mkts)} *'
			chart_top(len_cnt=240, bold=True)
			chart_mid(in_str=title_msg, len_cnt=240, bold=True)

			# build the market
			mkt, trade_perf, trade_strat_perfs = self.mkt_build(m)

			# process the market
			mkt = self.mkt_logic(mkt, trade_perf, trade_strat_perfs)

			# end of Performance Timer for ind mkt
			t11 = time.perf_counter()
			secs = round(t11 - t00, 3)
			if secs > lib_secs_max:
				msg = f'mkt_loop for {prod_id} - took {secs} seconds...'
				in_str_len = len(msg)
				msg = cs(msg, font_color='white', bg_color='orangered')
				print(msg)

			chart_bottom(len_cnt=240, bold=True)

		# end of Performance Timer for mkt loop
		t1 = time.perf_counter()
		secs = round(t1 - t0, 3)
		if secs > lib_secs_max:
			cp(f'mkt_loops - took {secs} seconds to complete...', font_color='white', bg_color='orangered')

		func_end(fnc)

# 	#<=====>#

# 	def mkts_loop_buy_only(self):
# 		func_name = 'mkts_loop_buy_only'
# 		func_str = f'{lib_name}.{func_name}()'
# 		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# #		G(func_str)

# 		t0 = time.perf_counter()

# 		print_adv(3)
# 		WoM(f"{'Markets Loop':^200}")
# 		print_adv(1)

# 		self.mkts_lists_get()
# 		self.ohlcv_tables_check()

# 		cnt = 0
# 		# loop through all mkts for buy/sell logic

# 		dttm_start_loop = dttm_get()	
# 		t_loop = time.perf_counter()


# 		for m in self.loop_mkts:
# 			prod_id = m['prod_id']
# 			db_check_ohlcv_prod_id_table(prod_id)


# 		for m in self.loop_mkts:
# 			cnt += 1
# 			t00 = time.perf_counter()

# 			prod_id = m['prod_id']
# 			first_letter = left(prod_id,1).lower()

# 			if self.mode == 'sell':
# 				if self.mode_sub == 1:
# 					if first_letter not in ('a','c','e','g','i','k','m','o','q','s','u','w','y','1','3','5','7','9'):
# 						continue
# 					# # check if cnt is divisible by 2
# 					# if cnt % 2 == 0:
# 					# 	continue
# 				if self.mode_sub == 2:
# 					if first_letter not in ('b','d','f','h','j','l','n','p','r','t','v','x','z','0','2','4','6','8'):
# 						continue
# 					# # check if cnt is divisible by 2
# 					# if cnt % 2 != 0:
# 					# 	continue


# 			# formatting the mkt
# 			prod_id = m['prod_id']
# 			m = dec_2_float(m)
# 			m = AttrDictConv(in_dict=m)
# 			# This is only for disp_mkt
# 			m.cnt = cnt
# 			m.mkts_tot = len(self.loop_mkts)

# 			# lets Avoid Trading Stable Coins Against One Another
# 			if m.base_curr_symb in self.st.stable_coins:
# 				continue

# 			# refresh settings each loop for hot changes
# 			self.st = settings.reload()
# 			self.wallet_refresh()

# 			t_now = time.perf_counter()
# 			t_elapse = t_now - t_loop
# 			loop_age = format_disp_age2(t_elapse)

# 			# build Out Everything We Will Need in the Market
# 			print_adv(3)

# 			title_msg = f'* Market Summary * {prod_id} * {dttm_get()} * {dttm_start_loop} * {loop_age} * {cnt}/{len(self.loop_mkts)} *'
# 			chart_top(len_cnt=240, bold=True)
# 			chart_mid(in_str=title_msg, len_cnt=240, bold=True)

# 			# build the market
# 			mkt, trade_perf, trade_strat_perfs = self.mkt_build(m)

# 			# process the mkt
# 			mkt = self.mkt_logic(mkt, trade_perf, trade_strat_perfs)

# 			# end of Performance Timer for ind mkt
# 			t11 = time.perf_counter()
# 			secs = round(t11 - t00, 3)
# 			if secs > lib_secs_max:
# 				msg = f'mkt_loop for {prod_id} - took {secs} seconds...'
# 				in_str_len = len(msg)
# 				msg = cs(msg, font_color='white', bg_color='orangered')
# 				print(msg)

# 			chart_bottom(len_cnt=240, bold=True)

# 		# end of Performance Timer for mkt loop
# 		t1 = time.perf_counter()
# 		secs = round(t1 - t0, 3)
# 		if secs > lib_secs_max:
# 			cp(f'mkt_loops - took {secs} seconds to complete...', font_color='white', bg_color='orangered')

# 		func_end(fnc)

	#<=====>#

# 	def mkts_loop_sell_only(self):
# 		func_name = 'mkts_loop_sell_only'
# 		func_str = f'{lib_name}.{func_name}()'
# 		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# #		G(func_str)

# 		t0 = time.perf_counter()

# 		print_adv(3)
# 		WoM(f"{'Markets Loop':^200}")
# 		print_adv(1)

# 		self.mkts_lists_get()
# 		self.ohlcv_tables_check()

# 		cnt = 0
# 		# loop through all mkts for buy/sell logic

# 		dttm_start_loop = dttm_get()	
# 		t_loop = time.perf_counter()


# 		for m in self.loop_mkts:
# 			cnt += 1
# 			t00 = time.perf_counter()

# 			prod_id = m['prod_id']
# 			first_letter = left(prod_id,1).lower()

# 			if self.mode == 'sell':
# 				if self.mode_sub == 1:
# 					if first_letter not in ('a','c','e','g','i','k','m','o','q','s','u','w','y','1','3','5','7','9'):
# 						continue
# 					# # check if cnt is divisible by 2
# 					# if cnt % 2 == 0:
# 					# 	continue
# 				if self.mode_sub == 2:
# 					if first_letter not in ('b','d','f','h','j','l','n','p','r','t','v','x','z','0','2','4','6','8'):
# 						continue
# 					# # check if cnt is divisible by 2
# 					# if cnt % 2 != 0:
# 					# 	continue


# 			# formatting the mkt
# 			prod_id = m['prod_id']
# 			m = dec_2_float(m)
# 			m = AttrDictConv(in_dict=m)
# 			# This is only for disp_mkt
# 			m.cnt = cnt
# 			m.mkts_tot = len(self.loop_mkts)

# 			# lets Avoid Trading Stable Coins Against One Another
# 			if m.base_curr_symb in self.st.stable_coins:
# 				continue

# 			# refresh settings each loop for hot changes
# 			self.st = settings.reload()
# 			self.wallet_refresh()

# 			t_now = time.perf_counter()
# 			t_elapse = t_now - t_loop
# 			loop_age = format_disp_age2(t_elapse)

# 			# build Out Everything We Will Need in the Market
# 			print_adv(3)

# 			title_msg = f'* Market Summary * {prod_id} * {dttm_get()} * {dttm_start_loop} * {loop_age} * {cnt}/{len(self.loop_mkts)} *'
# 			chart_top(len_cnt=240, bold=True)
# 			chart_mid(in_str=title_msg, len_cnt=240, bold=True)

# 			# build the market
# 			mkt, trade_perf, trade_strat_perfs = self.mkt_build(m)

# 			# process the mkt
# 			mkt = self.mkt_logic(mkt, trade_perf, trade_strat_perfs)

# 			# end of Performance Timer for ind mkt
# 			t11 = time.perf_counter()
# 			secs = round(t11 - t00, 3)
# 			if secs > lib_secs_max:
# 				msg = f'mkt_loop for {prod_id} - took {secs} seconds...'
# 				in_str_len = len(msg)
# 				msg = cs(msg, font_color='white', bg_color='orangered')
# 				print(msg)

# 			chart_bottom(len_cnt=240, bold=True)

# 		# end of Performance Timer for mkt loop
# 		t1 = time.perf_counter()
# 		secs = round(t1 - t0, 3)
# 		if secs > lib_secs_max:
# 			cp(f'mkt_loops - took {secs} seconds to complete...', font_color='white', bg_color='orangered')

# 		func_end(fnc)

	#<=====>#

	def mkt_logic(self, mkt, trade_perf, trade_strat_perfs):
		func_name = 'mkt_logic'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=10)
#		G(func_str)

		mkt_logic_t0 = time.perf_counter()

		try:
			prod_id      = mkt.prod_id
			self.st      = settings.reload()

			mkt          = buy_strats_avail_get(mkt)
			self.wallet_refresh()

			# Market Summary
			t0 = time.perf_counter()
			try:
				mkt, trade_perf, trade_strat_perfs = self.disp_mkt(mkt, trade_perf, trade_strat_perfs)
			except Exception as e:
				print(f'{dttm_get()} {func_name} - Market Summary ==> {prod_id} = Error : ({type(e)}){e}')
				traceback.print_exc()
				pprint(mkt)
				print_adv(3)
				beep(3)
				pass
			t1 = time.perf_counter()
			secs = round(t1 - t0, 3)
			if secs >= 5:
				msg = cs(f'disp_mkt for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
				chart_row(msg, len_cnt=240)
				chart_mid(len_cnt=240)


			# Market Technical Analysis
			ta = None
			# adding this to attempt to speed up sell loop, by not calling for TA when we are not going to sell
			if self.mode in ('buy','full'):
				t0 = time.perf_counter()
				try:
					ta = mkt_ta_main_new(mkt, self.st)
					if not ta:
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
	#					beep(3)
						func_end(fnc)
						return mkt
					if ta == 'Error!':
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
	#					beep(3)
						func_end(fnc)
						return mkt
				except Exception as e:
					print(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} = Error : ({type(e)}){e}')
					traceback.print_exc()
					pprint(mkt)
					print_adv(3)
					beep(3)
					pass
				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				if secs >= 5:
					msg = cs(f'mkt_ta_main_new for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
					chart_row(msg, len_cnt=240)
					chart_mid(len_cnt=240)


			if self.mode in ('buy','full'):
				# Market Buy Logic
				t0 = time.perf_counter()
				if self.st.spot.buy.buying_on_yn == 'Y' and prod_id in self.buy_mkts:
					try:
						mkt = self.buy_logic(self.buy_mkts, mkt, trade_perf, trade_strat_perfs, ta)
					except Exception as e:
						print(f'{dttm_get()} {func_name} - Buy Logic ==> {prod_id} = Error : ({type(e)}){e}')
						traceback.print_exc()
						pprint(mkt)
						print_adv(3)
						beep(3)
						pass
				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				if secs >= 5:
					msg = cs(f'buy_logic for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
					chart_row(msg, len_cnt=240)
					chart_mid(len_cnt=240)


			if self.mode in ('sell','full'):
				# Market Sell Logic
				t0 = time.perf_counter()
				if self.st.spot.sell.selling_on_yn == 'Y':
					try:
						open_poss = db_pos_open_get_by_prod_id(prod_id)
						if len(open_poss) > 0:
							mkt = self.sell_logic(mkt, ta, open_poss)
					except Exception as e:
						print(f'{dttm_get()} {func_name} - Sell Logic ==> {prod_id} = Error : ({type(e)}){e}')
						traceback.print_exc()
						pprint(mkt)
						print_adv(3)
						beep(3)
						pass
				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				if secs >= 5:
					msg = cs(f'sell_logic for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
					chart_row(msg, len_cnt=240)
					chart_mid(len_cnt=240)


			t0 = time.perf_counter()

			db_tbl_mkts_insupd([mkt])

			secs = round(t1 - t0, 2)
			if secs >= 2:
				msg = cs(f'db_tbl_mkts_insupd for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
				chart_row(msg, len_cnt=240)
				chart_mid(len_cnt=240)

		except Exception as e:
			print(f'{func_name} ==> errored 2... {e}')
			print(dttm_get())
			traceback.print_exc()
			print(type(e))
			print(e)
			print(f'prod_id : {mkt.prod_id}')
			pprint(mkt)
			print_adv(3)
			beep(3)
			pass

		mkt_logic_t1 = time.perf_counter()
		secs = round(mkt_logic_t1 - mkt_logic_t0, 2)
		if secs >= 5:
			msg = cs(f'mkt_logic for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
			chart_row(msg, len_cnt=240)
		else:
			msg = cs(f'mkt_logic for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='green')
			chart_row(msg, len_cnt=240)

		func_end(fnc)
		return mkt

	#<=====>#

	def buy_live(self, mkt, trade_strat_perf):
		func_name = 'buy_live'
		func_str = f'{lib_name}.{func_name}(mkt)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		if self.st.spot.buy.buy_limit_yn == 'Y':
			try:
				self.ord_lmt_buy_open(mkt, trade_strat_perf)
			except Exception as e:
				print(f'{func_name} ==> buy limit order failed, attempting market... {e}')
				beep(3)
				# self.ord_mkt_buy(mkt, trade_strat_perf)
				self.ord_mkt_buy_orig(mkt, trade_strat_perf)
		else:
			# self.ord_mkt_buy(mkt, trade_strat_perf)
			self.ord_mkt_buy_orig(mkt, trade_strat_perf)

		func_end(fnc)

	#<=====>#

	def buy_test(self, mkt, trade_strat_perf):
		func_name = 'buy_test'
		func_str = f'{lib_name}.{func_name}(mkt, trade_strat_perf)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

#		beep()

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

	def buy_ords_check(self):
		func_name = 'buy_ords_check'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=5)
#		G(func_str)

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
#								beep(3)
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
#								beep()

							else:
								print(func_str)
								print('error #2 !')
#								beep(3)
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
			pos.buy_curr_symb           = bo.buy_curr_symb
			pos.buy_cnt                 = bo.buy_cnt_act
			pos.spend_curr_symb         = bo.spend_curr_symb
			pos.fees_curr_symb          = bo.fees_curr_symb
			pos.buy_fees_cnt            = bo.fees_cnt_act
			pos.tot_out_cnt             = bo.tot_out_cnt
			pos.sell_curr_symb          = bo.buy_curr_symb
			pos.recv_curr_symb          = bo.spend_curr_symb
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

			db_tbl_poss_insupd(pos)

		func_end(fnc)

	#<=====>#

	def pos_upd(self, pos, mkt=None, so=None):
		func_name = 'pos_upd'
		func_str = f'{lib_name}.{func_name}(pos, mkt, so)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		G(func_str)

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


		if pos.pos_stat not in ('OPEN'):
			print(f'pos.pos_stat : {pos.pos_stat}')


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


		if pos.pos_stat == 'SELL' and not so:
			print('pos_stat = SELL and no SO was given, so we cannot close the position...')
			beep()


		if pos.pos_stat not in ('OPEN'):
			print(f'pos.pos_stat : {pos.pos_stat}')


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

		pos = self.pos_upd(mkt=None, pos=pos, so=so)

		func_end(fnc)

	#<=====>#

	def sell_logic(self, mkt, ta, open_poss):
		func_name = 'sell_logic'
		func_str = f'{lib_name}.{func_name}(mkt, ta, open_poss)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=6)
		# G(func_str)

		prod_id = mkt.prod_id
		st = settings.settings_load()

		mkt.show_sell_header_tf = True

		if not open_poss:
			print(f'{prod_id} has no open positions...')
			func_end(fnc)
			return mkt

		db_poss_check_mkt_dttm_upd(prod_id)
		mkt.check_mkt_dttm = db_poss_check_mkt_dttm_get(prod_id)

		for pos in open_poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos_id = pos.pos_id
			if pos.pos_stat == 'OPEN':
				try:
					pos = self.pos_upd(mkt=mkt, pos=pos)
					pos = POS(mkt, pos, ta)
					mkt, pos, ta = pos.sell_pos_logic()
				except Exception as e:
					print(f'{dttm_get()} {func_name} {prod_id} {pos_id}==> errored : ({type(e)}) {e}')
					traceback.print_exc()
					pass

		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)
		return mkt

	#<=====>#

	def sell_ords_check(self):
		func_name = 'sell_ords_check'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=5)
		G(func_str)

		try:
			cnt = 0

			iss = db_poss_sell_order_problems_get()
			if iss:
				for i in iss:
					print(i)
				beep(10)
				sys.exit()

#			x = db_poss_fix_stat_upd()
#			if x > 0:
#				print(f'marked OPEN the pos_stat of {x} positions in SELL stat but no OPEN sell_ords were found...')
#				beep(10)
#				sys.exit()

			sos = db_sell_ords_open_get()
			if sos:
				print_adv(2)
				WoM(f"{'Sell Orders Check':^200}")

				sos_cnt = len(sos)
				for so in sos:
					cnt += 1
					so = dec_2_float(so)
					so = AttrDictConv(in_dict=so)

					print(so)

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

						print(o)

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
								print('WE NEED CODE HERE #1 !!!')
								beep(10)
								sys.exit()

								if o.ord_filled_size > 0:
									so.sell_cnt_act                    = o.ord_filled_size
									so.fees_cnt_act                    = o.ord_total_fees
									so.tot_in_cnt                      = o.ord_total_value_after_fees
									so.prc_sell_act                    = o.ord_average_filled_price # not sure this includes the fees
									so.sell_end_dttm                   = o.ord_last_fill_time
									so.tot_prc_buy                     = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
									so.prc_sell_slip_pct               = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 8)
									print(f'{cnt:^4} / {sos_cnt:^4}, prod_id : {so.prod_id:<16}, pos_id : {so.pos_id:>7}, so_id : {so.so_id:>7}, so_uuid : {so.sell_order_uuid:<60}')
									beep(10)
									sys.exit()


									db_tbl_sell_ords_insupd(so)
		# this needs to be added when we add in support for limit orders
		#						else:
		#							r = cb_ord_cancel_orders(order_ids=[ord_id])
		#							db_sell_ords_stat_upd(so_id=so.so_id, ord_stat='CANC')
		#							db_poss_err_upd(pos_id=so.pos_id, pos_stat='OPEN')
							else:
								pprint(o)
								print('WE NEED CODE HERE #1 !!!')
								beep(10)
								sys.exit()
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

	def gen_guid(self):
		func_name = 'gen_guid'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		guid = str(uuid.uuid4())

		func_end(fnc)
		return guid

	#<=====>#

	# Function to fetch current positions
	def wallet_refresh(self, force_tf=False):
		func_name = 'wallet_refresh'
		func_str = f'{lib_name}.{func_name}(self.refresh_wallet_tf={self.refresh_wallet_tf}, force_tf={force_tf})'
		fnc = func_begin(func_name=func_name, func_str=func_str,  logname=log_name, secs_max=1.5)
#		G(func_str)

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
	#		reserve_amt                = max(tot_daily_reserve_amt, min_reserve_amt)
			reserve_amt                = tot_daily_reserve_amt + min_reserve_amt
		else:
			reserve_amt                = min_reserve_amt

		# print(f'min_reserve_amt       : {min_reserve_amt}')
		# print(f'day                   : {day}')
		# print(f'daily_reserve_amt     : {daily_reserve_amt}')
		# print(f'tot_daily_reserve_amt : {tot_daily_reserve_amt}')
		# print(f'reserve_amt           : {reserve_amt}')

		func_end(fnc)
		return reserve_amt

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

	def ohlcv_tables_check(self):
		func_name = 'ohlcv_tables_check'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	#	G(func_str)

		table_names = db_table_names_get()
		for m in self.loop_mkts:
			prod_id = m['prod_id']
			table_name = f'ohlcv_{prod_id}'.replace('-','_')
			if table_name not in table_names:
				db_check_ohlcv_prod_id_table(prod_id)

		func_end(fnc)

#<=====>#

	def prt_cols(self, l, cols=10, clr='WoG'):
		func_name = 'prt_cols'
		func_str = f'{lib_name}.{func_name}(l, cols={cols}, clr={clr})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	#	G(func_str)

		col_cnt = 0
		s = ''
		for x in l:
			col_cnt += 1
			if clr == 'WoG':
				s += cs(text=f'{x:<15}', font_color='white', bg_color='green')
			elif clr == 'GoW':
				s += cs(text=f'{x:<15}', font_color='green', bg_color='white')
			if col_cnt % cols == 0:
				chart_row(s, len_cnt=177)
				s = ''
				col_cnt = 0
			elif col_cnt == len(l):
				s += ''
			else:
				s += ' | '
		if col_cnt > 0 and col_cnt < cols:
			chart_row(s, len_cnt=177)

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

				"AAVE-USDC",
				"ADA-USDC",
				"ALGO-USDC",
				"ATOM-USDC",
				"AVAX-USDC",
				"BADGER-USDC",
				"BNB-USDC",
				"BONK-USDC",
				"BTC-USDC",
				"DOGE-USDC",
				"DOT-USDC",
				"ETH-USDC",
				"FTM-USDC",
				"HBAR-USDC",
				"HNT-USDC",
				"HONEY-USDC",
				"ICP-USDC",
				"JASMY-USDC",
				"LDO-USDC",
				"OMNI-USDC",
				"POL-USDC",
				"RNDR-USDC",
				"SHIB-USDC",
				"SOL-USDC",
				"SUI-USDC",
				"TON-USDC",
				"UNI-USDC",
				"WIF-USDC",
				"XRP-USDC"

				
'''

