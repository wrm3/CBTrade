#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.bot_cls_buy import BUY
from libs.bot_cls_sell import POS
from libs.bot_coinbase import cb_bid_ask_by_amt_get, cb_mkt_prc_dec_calc
from libs.bot_common import calc_chg_pct
from libs.bot_db_read import (
    db_mkt_elapsed_get, db_mkt_strat_elapsed_get, db_pos_open_get_by_prod_id, 
    db_poss_check_mkt_dttm_get, db_poss_open_max_trade_size_get, db_trade_strat_perf_get, db_view_trade_perf_get_by_prod_id
)
from libs.bot_db_write import (
    db_poss_check_mkt_dttm_upd, db_tbl_mkts_insupd, db_tbl_poss_insupd
)
from libs.bot_settings import bot_settings_get, debug_settings_get, get_lib_func_secs_max, mkt_settings_get, pair_settings_get
from libs.bot_strats_buy import buy_strats_avail_get, buy_strats_get
from libs.bot_ta import ta_main_new
from libs.bot_theme import cs_pct_color_50
from libs.cls_settings import AttrDict
from libs.lib_charts import chart_bottom, chart_headers, chart_mid, chart_row, chart_top
from libs.lib_colors import WoG, WoR, YoK, cp, cs
from libs.lib_common import AttrDictConv, beep, dec_2_float, dttm_get, func_begin, func_end, print_adv
import time
import traceback


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


#<=====>#
# Classes
#<=====>#

class PAIR(AttrDict):

	def __init__(pair, mkt, pair_dict, mode='full'):
		pair.class_name                = 'PAIR'
		pair.mkt                            = mkt
		for k, v in pair_dict.items():
			pair[k] = v
		pair.mode                           = mode
		pair.symb                           = pair.mkt.symb
		pair.dst, pair.debug_settings       = debug_settings_get()
		pair.bst, pair.bot_settings         = bot_settings_get()
		pair.mst, pair.mkt_settings         = mkt_settings_get(symb=pair.symb)
		pair.pst                            = pair_settings_get(symb=pair.symb, prod_id = pair.prod_id)                
		pair.pst                            = AttrDictConv(in_dict=pair.pst)
		pair.buy_strats                     = buy_strats_get()
		pair.show_buy_header_tf             = True


	#<=====>#

	def main_loop(pair):
		func_name = 'main_loop'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id = pair.prod_id

		if pair.mode == 'sell':
			check_mkt_dttm = db_poss_check_mkt_dttm_get(prod_id)

			if check_mkt_dttm > pair.check_mkt_dttm:
				print_adv()
				YoK(f'another bot with mode sell has updated {prod_id} market since starting..., old : {pair.check_mkt_dttm}, new : {check_mkt_dttm} skipping...')
				return pair.mkt

			db_poss_check_mkt_dttm_upd(prod_id)
			check_mkt_dttm = db_poss_check_mkt_dttm_get(prod_id)
			pair.check_mkt_dttm = check_mkt_dttm

		# formatting the mkt
		prod_id = pair.prod_id

		# This is only for disp_pair
		pair.mkts_tot = len(pair.mkt.loop_pairs)
		# lets Avoid Trading Stable Coins Against One Another
		if pair.base_curr_symb in pair.pst.stable_coins:
			func_end(fnc)
			return

		# build Out Everything We Will Need in the Market
		print_adv(2)

		title_msg = f'* Pair Summary * {prod_id} * {dttm_get()} * {pair.mkt.dttm_start_loop} * {pair.mkt.loop_age} * {pair.mkt.cnt}/{len(pair.mkt.loop_pairs)} *'
		chart_top(len_cnt=240, bold=True)
		chart_mid(in_str=title_msg, len_cnt=240, bold=True)

		# build the market
		pair.pair_build()

		# process the market
		pair.pair_logic()

#		db_tbl_mkts_insupd(pair)
		print_adv(2)

		func_end(fnc)
		return pair.mkt

	#<=====>#

	def pair_build(pair):
		func_name = 'pair_build'
		func_str = f'{lib_name}.{func_name}(m)'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		prod_id = pair.prod_id

		# Estimate the true buy/sell prices by looking at the order book
		pricing_cnt                    = pair.pst.buy.trade_size
		max_poss_open_trade_size       = float(db_poss_open_max_trade_size_get(prod_id))
		if max_poss_open_trade_size:
			if max_poss_open_trade_size > pricing_cnt:
				pricing_cnt = max_poss_open_trade_size

		pair.prc_mkt              = pair.prc
		bid_prc, ask_prc          = cb_bid_ask_by_amt_get(mkt=pair, buy_sell_size=pricing_cnt)
		pair.prc_bid              = bid_prc
		pair.prc_ask              = ask_prc
		pair.prc_dec              = cb_mkt_prc_dec_calc(pair.prc_bid, pair.prc_ask)
		pair.prc_buy              = round(pair.prc_ask, pair.prc_dec)
		pair.prc_sell             = round(pair.prc_bid, pair.prc_dec)
		pair.prc_range_pct        = ((pair.prc_buy - pair.prc_sell) / pair.prc) * 100
		pair.prc_buy_diff_pct     = ((pair.prc - pair.prc_buy) / pair.prc) * 100
		pair.prc_sell_diff_pct    = ((pair.prc - pair.prc_sell) / pair.prc) * 100

		# Market Performance
		pair.pair_trade_perf_get()

		# get default settings
		pair.trade_perf.restricts_buy_delay_minutes   = pair.pst.buy.buy_delay_minutes
		pair.trade_perf.restricts_open_poss_cnt_max   = pair.pst.buy.open_poss_cnt_max

		# get market performance boosts

# fixme - readd
# 		pair.mkt, trade_perf                = pair.buy_logic_mkt_boosts(pair, trade_perf)

		# Market Strat Performances
		pair.trade_strat_perfs    = []
		# Market Strategy Performance
		for strat in pair.buy_strats:
			strat = pair.buy_strats[strat]
			strat = dec_2_float(strat)
			strat = AttrDictConv(in_dict=strat)
			trade_strat_perf = pair.trade_strat_perf_get(strat.buy_strat_type, strat.buy_strat_name, strat.buy_strat_freq)
			pair.trade_strat_perfs.append(trade_strat_perf)
		trade_strat_perfs_sorted = sorted(pair.trade_strat_perfs, key=lambda x: x["gain_loss_pct_day"], reverse=True)
		pair.trade_strat_perfs = trade_strat_perfs_sorted

		func_end(fnc)

	#<=====>#

	def pair_trade_perf_get(pair):
		func_name = 'pair_trade_perf_get'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		symb = pair.symb
		prod_id = pair.prod_id

		# Build to Defaults
		trade_perf = {}
		trade_perf['symb']                          = symb
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

		pair.trade_perf = trade_perf

		func_end(fnc)


	#<=====>#

	def trade_strat_perf_get(pair, buy_strat_type, buy_strat_name, buy_strat_freq):
		func_name = 'trade_strat_perf_get'
		func_str = f'{lib_name}.{func_name}(buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		symb = pair.symb
		prod_id = pair.prod_id

		trade_strat_perf = {}
		trade_strat_perf['symb']                = symb
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

		trade_strat_perf.restricts_buy_strat_delay_minutes = pair.mkt_settings.get_ovrd(pair.pst.buy.buy_strat_delay_minutes, in_key=buy_strat_freq)
		r = db_mkt_strat_elapsed_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
		trade_strat_perf.strat_bo_elapsed   = r[0]
		trade_strat_perf.strat_pos_elapsed  = r[1]
		trade_strat_perf.strat_last_elapsed = r[2]

		func_end(fnc)
		return trade_strat_perf

	#<=====>#

	def pair_logic(pair):
		func_name = 'pair_logic'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		mkt_logic_t0 = time.perf_counter()

		try:
			prod_id      = pair.prod_id

			if pair.mode in ('buy','full'):
				pair = buy_strats_avail_get(pair)
 
			pair.timings  = []

			# Market Summary
			t0 = time.perf_counter()
			try:
				pair.disp_pair()
			except Exception as e:
				print(f'{dttm_get()} {func_name} - Market Summary ==> {prod_id} = Error : ({type(e)}){e}')
				traceback.print_exc()
				traceback.print_stack()
				print_adv()
				print(f'{lib_name}.{func_name} - disp_pair')
				beep(3)
				pass
			t1 = time.perf_counter()
			secs = round(t1 - t0, 3)
			timing_data = {'Market Summary': secs}
			pair.timings.append(timing_data)


			# Market Technical Analysis
			pair.ta = None
			# adding this to attempt to speed up sell loop, by not calling for TA when we are not going to sell
			if pair.mode in ('buy','full'):
				t0 = time.perf_counter()
				try:
					pair.ta = ta_main_new(pair, pair.pst)
					if not pair.ta:
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> TA Errored and is None')
						func_end(fnc)
						return
					if pair.ta == 'Error!':
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
						WoR(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} - close prices do not match')
						func_end(fnc)
						return
				except Exception as e:
					print(f'{dttm_get()} {func_name} - Get TA ==> {prod_id} = Error : ({type(e)}){e}')
					traceback.print_exc()
					traceback.print_stack()
					print_adv()
					print(f'{lib_name}.{func_name}')
					beep(3)
					pass
				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				timing_data = {'Technical Analysis': secs}
				pair.timings.append(timing_data)


			if pair.mode in ('buy','full'):
				# Market Buy Logic
				t0 = time.perf_counter()
				if pair.pst.buy.buying_on_yn == 'Y' and prod_id in pair.mkt.buy_pairs:
					try:
						buy = BUY(mkt=pair.mkt, pair=pair)
						pair.mkt, pair = buy.main_loop() 
					except Exception as e:
						print(f'{dttm_get()} {func_name} - Buy Logic ==> {prod_id} = Error : ({type(e)}){e}')
						traceback.print_exc()
						traceback.print_stack()
						print_adv()
						print(f'{lib_name}.{func_name} - buy_logic')
						beep(3)
						pass
				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				timing_data = {'Buy Logic': secs}
				pair.timings.append(timing_data)
				if secs >= 5:
					msg = cs(f'buy_logic for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')


			if pair.mode in ('sell','full'):
				# Market Sell Logic
				t0 = time.perf_counter()
				if pair.pst.sell.selling_on_yn == 'Y':
					try:
						pair.open_poss = db_pos_open_get_by_prod_id(prod_id)
						if len(pair.open_poss) > 0:
							pair.sell_logic()
					except Exception as e:
						print(f'{dttm_get()} {func_name} - Sell Logic ==> {prod_id} = Error : ({type(e)}){e}')
						traceback.print_exc()
						traceback.print_stack()
						print_adv()
						print(f'{lib_name}.{func_name} -  sell_logic')
						beep(3)
						pass
				t1 = time.perf_counter()
				secs = round(t1 - t0, 2)
				timing_data = {'Sell Logic': secs}
				pair.timings.append(timing_data)


			t0 = time.perf_counter()

			db_tbl_mkts_insupd([pair])

			t1 = time.perf_counter()
			secs = round(t1 - t0, 2)


		except Exception as e:
			print(f'{func_name} ==> errored 2... {e}')

			print(dttm_get())
			traceback.print_exc()
			traceback.print_stack()
			print(type(e))
			print(e)
			print(f'prod_id : {pair.prod_id}')
			print_adv()
			print(f'{lib_name}.{func_name} -  end')
			beep(3)
			pass

		mkt_logic_t1 = time.perf_counter()
		secs = round(mkt_logic_t1 - mkt_logic_t0, 2)
		timing_data = {'Total Time': secs}
		pair.timings.append(timing_data)

		chart_mid(in_str='Timings', len_cnt=240)
		for x in pair.timings:
			for k,v in x.items():
				msg = f'actv : {k:>50}, elapsed : {v:>6.2f}'
				chart_row(in_str=msg, len_cnt=240)
		chart_bottom(len_cnt=240)

		func_end(fnc)

	#<=====>#

	def disp_pair(pair):
		func_name = 'disp_pair'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		pair.disp_pair_summary()
		pair.disp_pair_stats()
		pair.disp_pair_performance()

		func_end(fnc)

	#<=====>#

	def disp_pair_summary(pair):
		func_name = 'disp_pair_summary'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		# Market Basics
		prod_id = pair.prod_id

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
		if pair.prc_pct_chg_24h < 0:
			msg += cs(f"$ {pair.prc_mkt:>14.8f}", 'white', 'red') + " | "
			msg += cs(f"{pair.prc_pct_chg_24h:>10.4f} %", 'white', 'red') + " | "
		elif pair.prc_pct_chg_24h > 0:
			msg += cs(f"$ {pair.prc_mkt:>14.8f}", 'white', 'green') + " | "
			msg += cs(f"{pair.prc_pct_chg_24h:>10.4f} %", 'white', 'green') + " | "
		else:
			msg += f"$ {pair.prc_mkt:>14.8f} | "
			msg += f"{pair.prc_pct_chg_24h:>10.4f} % | "

		msg += f"$ {pair.prc_buy:>14.8f} | "
		msg += f"$ {pair.prc_sell:>14.8f} | "
		msg += f"{pair.prc_buy_diff_pct:>10.4f} % | "
		msg += f"{pair.prc_sell_diff_pct:>10.4f} % | "

		if pair.prc_range_pct < 0:
			msg += cs(f"{pair.prc_range_pct:>10.4f} %", 'white', 'red') + " | "
		elif pair.prc_range_pct > 0:
			msg += cs(f"{pair.prc_range_pct:>10.4f} %", 'white', 'green') + " | "
		else:
			msg += f"{pair.prc_range_pct:>10.4f} %" + " | "

		msg += cs(f"$ {pair.mkt.budget.bal_avail:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {pair.mkt.budget.reserve_amt:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {pair.mkt.budget.spendable_amt:>9.2f}", "white", "green") + " | "
		if pair.mkt.budget.reserve_locked_tf:
			msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
		else:
			msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
		chart_headers(in_str=hmsg, len_cnt=240, bold=True)
		chart_row(in_str=msg, len_cnt=240)
		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)

	#<=====>#

	def disp_pair_stats(pair):
		func_name = 'disp_pair_stats'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		# Market Basics
		prod_id = pair.prod_id

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
		msg += f'{pair.trade_perf.tot_cnt:>9}' + ' | '
		msg += cs(f'{pair.trade_perf.win_cnt:>9}', font_color='white', bg_color='green') + ' | '
		msg += cs(f'{pair.trade_perf.lose_cnt:>9}', font_color='white', bg_color='red') + ' | '
		msg += cs(f'{pair.trade_perf.win_pct:>9.2f} %', font_color='white', bg_color='green') + ' | '
		msg += cs(f'{pair.trade_perf.lose_pct:>9.2f} %', font_color='white', bg_color='red') + ' | '
		msg += cs(f'$ {pair.trade_perf.win_amt:>9.4f}', font_color='white', bg_color='green') + ' | '
		msg += cs(f'$ {pair.trade_perf.lose_amt:>9.4f}', font_color='white', bg_color='red') + ' | '
		msg += f'$ {pair.trade_perf.tot_out_cnt:>9.4f}' + ' | '
		msg += f'$ {pair.trade_perf.tot_in_cnt:>9.4f}' + ' | '
		msg += f'$ {pair.trade_perf.val_curr:>9.4f}' + ' | '
		msg += f'$ {pair.trade_perf.val_tot:>9.4f}' + ' | '
		if pair.trade_perf.gain_loss_amt > 0:
			msg += cs(f'$ {pair.trade_perf.gain_loss_amt:>9.4f}', font_color='white', bg_color='green') + ' | '
			msg += cs(f'{pair.trade_perf.gain_loss_pct:>9.4f} %', font_color='white', bg_color='green') + ' | '
			msg += cs(f'{pair.trade_perf.gain_loss_pct_hr:>9.4f} %', font_color='white', bg_color='green') + ' | '
			msg += cs(f'{pair.trade_perf.gain_loss_pct_day:>9.4f} %', font_color='white', bg_color='green') + ' | '
		else:
			msg += cs(f'$ {pair.trade_perf.gain_loss_amt:>9.4f}', font_color='white', bg_color='red') + ' | '
			msg += cs(f'{pair.trade_perf.gain_loss_pct:>9.4f} %', font_color='white', bg_color='red') + ' | '
			msg += cs(f'{pair.trade_perf.gain_loss_pct_hr:>9.4f} %', font_color='white', bg_color='red') + ' | '
			msg += cs(f'{pair.trade_perf.gain_loss_pct_day:>9.4f} %', font_color='white', bg_color='red') + ' | '
		msg += f'{pair.trade_perf.last_elapsed:>9}' + ' | '

		title_msg = f'* Market Stats * {prod_id} *'
		chart_mid(in_str=title_msg, len_cnt=240, bold=True)
		chart_headers(in_str=hmsg, len_cnt=240, bold=True)
		chart_row(msg, len_cnt=240)

		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)

	#<=====>#

	def disp_pair_performance(pair):
		func_name = 'disp_pair_performance'
		func_str = f'{lib_name}.{func_name}(mkt, trade_perf, trade_strat_perfs)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		# Market Basics
		prod_id = pair.prod_id

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

		for x in pair.trade_strat_perfs:
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

	#<=====>#

	def sell_logic(pair):
		func_name = 'sell_logic'
		func_str = f'{lib_name}.{func_name}(mkt, ta, open_poss)'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		# G(func_str)

		prod_id = pair.prod_id

		pair.show_sell_header_tf = True

		db_poss_check_mkt_dttm_upd(prod_id)
		pair.check_mkt_dttm = db_poss_check_mkt_dttm_get(prod_id)

		for pos_data in pair.open_poss:
			pos_data = dec_2_float(pos_data)
			pos_data = AttrDictConv(in_dict=pos_data)
			pos_id = pos_data.pos_id
			if pos_data.pos_stat == 'OPEN':
				try:
					pair.pos_upd(pos=pos_data)
					pos = POS(mkt=pair.mkt, pair=pair, pos_data=pos_data, ta=pair.ta)
					pair, pos, pair.ta = pos.sell_pos_logic()
					# Update to Database
					db_tbl_poss_insupd(pos)
				except Exception as e:
					print(f'{dttm_get()} {func_name} {prod_id} {pos_id}==> errored : ({type(e)}) {e}')
					traceback.print_exc()
					traceback.print_stack()
					pass

		chart_mid(len_cnt=240, bold=True)

		func_end(fnc)

	#<=====>#

	def pos_upd(pair, pos):
		func_name = 'pos_upd'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		symb = pair.symb
		pair.mst, pair.mkt_settings = mkt_settings_get(symb=pair.symb)

		pos.prc_curr         = pair.prc_sell

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
		pos.gain_loss_amt     = pos.val_tot - pos.tot_out_cnt
		pos.gain_loss_amt_est = pos.val_tot - pos.tot_out_cnt
		# Update Gain Loss % Highs & Lows
		if pos.gain_loss_amt_est > pos.gain_loss_amt_est_high: pos.gain_loss_amt_est_high = pos.gain_loss_amt_est
		if pos.gain_loss_amt_est < pos.gain_loss_amt_est_low:  pos.gain_loss_amt_est_low  = pos.gain_loss_amt_est

		# gain_loss_pct_est is to capture the pct at the time we decide to sell and should not be updated after
		pos.gain_loss_pct      = calc_chg_pct(old_val=pos.tot_out_cnt, new_val=pos.val_tot, dec_prec=4)
		pos.gain_loss_pct_est  = pos.gain_loss_pct
		# Update Gain Loss % Highs & Lows
		if pos.gain_loss_pct_est > pos.gain_loss_pct_est_high: pos.gain_loss_pct_est_high = pos.gain_loss_pct_est
		if pos.gain_loss_pct_est < pos.gain_loss_pct_est_low:  pos.gain_loss_pct_est_low  = pos.gain_loss_pct_est

		# Update to Database
		db_tbl_poss_insupd(pos)

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
