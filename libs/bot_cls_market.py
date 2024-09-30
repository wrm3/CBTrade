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
from libs.bot_coinbase import cb_mkts_refresh, cb_wallet_refresh
from libs.bot_db_read import (
    db_bals_get, db_bot_spent, db_open_trade_amts_get, db_pairs_loop_get, db_pairs_loop_poss_open_prod_ids_get, db_pairs_loop_top_gains_prod_ids_get, db_pairs_loop_top_perfs_prod_ids_get, db_pairs_loop_top_prc_chg_prod_ids_get, db_pairs_loop_top_vol_chg_pct_prod_ids_get, db_pairs_loop_top_vol_chg_prod_ids_get, db_pairs_loop_watched_prod_ids_get,
    db_table_names_get
)
from libs.bot_db_write import db_check_ohlcv_prod_id_table
from libs.bot_cls_pair import PAIR
from libs.bot_reports import report_buys_recent, report_open_by_age, report_sells_recent
from libs.bot_settings import bot_settings_get, debug_settings_get, get_lib_func_secs_max, mkt_settings_get
from libs.bot_strats_buy import buy_strats_get
from libs.cls_settings import AttrDict, Settings
from libs.lib_charts import chart_bottom, chart_headers, chart_mid, chart_row, chart_top
from libs.lib_colors import cp, cs
from libs.lib_common import AttrDictConv, dec_2_float, dttm_get, func_begin, func_end, print_adv
import time

from libs.lib_strings import format_disp_age2


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_cls_market'
log_name      = 'bot_cls_market'
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

class MARKET(AttrDict):

	def __init__(mkt, symb, fpath, mode='full'):
		mkt.class_name                = 'MARKET'
		mkt.symb                      = symb
		mkt.fpath                     = fpath
		mkt.mode                      = mode # full, auto, buy, sell
		mkt.dst, mkt.debug_settings       = debug_settings_get()
		mkt.bst, mkt.bot_settings         = bot_settings_get()
		mkt.mst, mkt.mkt_settings         = mkt_settings_get(symb=mkt.symb)

		mkt.buy_strats                = buy_strats_get()

		mkt.budget                    = AttrDict()
		mkt.budget.bal_avail          = 0
		mkt.budget.spendable_amt      = 0
		mkt.budget.reserve_amt        = 0
		mkt.budget.reserve_locked_tf         = True

		mkt.refresh_wallet_tf         = True
		mkt.budget_refresh()
		mkt.wallet_refresh(force_tf=True)
		mkt.budget_refresh()
		mkt.reserve_amt_calc()

	#<=====>#

	def main_loop(mkt):
		func_name = 'main_loop'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		if mkt.mode in ('buy'):
			report_buys_recent(cnt=20)
			print_adv(3)
			mkt.wallet_refresh()
			mkt.pairs_loop()
			report_buys_recent(cnt=20)
			print_adv(3)

		elif mkt.mode in ('sell'):
			report_sells_recent(cnt=20)
			print_adv(3)
			mkt.wallet_refresh()
			mkt.pairs_loop()
			report_open_by_age()
			report_sells_recent(cnt=20)
			print_adv(3)

		else:
			mkt.buy_ords_check()
			mkt.sell_ords_check()
			cb_mkts_refresh()
			report_buys_recent(cnt=20)
			print_adv(3)
			report_sells_recent(cnt=20)
			print_adv(3)
			mkt.wallet_refresh()
			mkt.pairs_loop()
			mkt.buy_ords_check()
			mkt.sell_ords_check()
			report_open_by_age()
			print_adv(3)
			report_buys_recent(cnt=20)
			print_adv(3)
			report_sells_recent(cnt=20)
			print_adv(3)

		func_end(fnc)

	#<=====>#

	def pairs_loop(mkt):
		func_name = 'pairs_loop'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		mkt.budget_refresh()

		t = f'Markets Loop : {mkt.symb}'
		if mkt.mode == 'buy':
			if mkt.budget.spent_amt >= mkt.budget.spend_max_amt:
				msg = cs(f'We have spent our entire {mkt.symb} budget... spent : {mkt.budget.spent_amt} / {mkt.budget.spend_max_amt} max...', 'white', 'red')
			else:
				msg = cs(f'We have more {mkt.symb} budget to spend... spent : {mkt.budget.spent_amt} / {mkt.budget.spend_max_amt} max...', 'white', 'red')
			print(msg)
			mkt.budget_display(budget=mkt.budget, title=t, footer=msg)
			if mkt.budget.spent_amt >= mkt.budget.spend_max_amt:
				report_sells_recent(cnt=20)
				time.sleep(30)
				return



		cnt = 0
		# loop through all mkts for buy/sell logic
		t0 = time.perf_counter()

		mkt.pairs_list_get()

		mkt.dttm_start_loop = dttm_get()	
		mkt.t_loop = time.perf_counter()

		mkt.ohlcv_tables_check()

		for pair_dict in mkt.loop_pairs:
			cnt += 1
			pair_dict = dec_2_float(pair_dict)
			pair_dict = AttrDictConv(in_dict=pair_dict)

			mkt.t_now = time.perf_counter()
			mkt.t_elapse = mkt.t_now - mkt.t_loop
			mkt.cnt = cnt
			mkt.loop_age = format_disp_age2(mkt.t_elapse)

			pair = PAIR(mkt=mkt, pair_dict=pair_dict, mode=mkt.mode)
			mkt  = pair.main_loop()

			mkt.budget_display(budget=mkt.budget)

		t = f'Markets Loop : {mkt.symb}'

		if mkt.mode == 'buy':
			if mkt.budget.spent_amt >= mkt.budget.spend_max_amt:
				msg = cs(f'We have spent our entire {mkt.symb} budget... spent : {mkt.budget.spent_amt} / {mkt.budget.spend_max_amt} max...', 'white', 'red')
			else:
				msg = cs(f'We have more {mkt.symb} budget to spend... spent : {mkt.budget.spent_amt} / {mkt.budget.spend_max_amt} max...', 'white', 'red')
			print(msg)
			mkt.budget_display(budget=mkt.budget, title=t, footer=msg)
			if mkt.budget.spent_amt >= mkt.budget.spend_max_amt:
				report_sells_recent(cnt=20)
				time.sleep(30)
				return


		# end of Performance Timer for mkt loop
		t1 = time.perf_counter()
		secs = round(t1 - t0, 3)
		if secs > lib_secs_max:
			cp(f'{lib_name}.{func_name} - took {secs} seconds to complete...', font_color='white', bg_color='orangered')

		func_end(fnc)

	#<=====>#

	# Function to fetch current positions
	def wallet_refresh(mkt, force_tf=False):
		func_name = 'wallet_refresh'
		func_str = f'{lib_name}.{func_name}(mkt.refresh_wallet_tf={mkt.refresh_wallet_tf}, force_tf={force_tf})'
		fnc = func_begin(func_name=func_name, func_str=func_str,  logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		if mkt.refresh_wallet_tf or force_tf:
			cb_wallet_refresh()
			mkt.refresh_wallet_tf = False

			mkt.budget.reserve_amt      = 0
			mkt.budget.bal_avail        = 0
			mkt.budget.spendable_amt    = 0
			mkt.budget.open_trade_amt   = 0

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
				if curr == mkt.symb:
					mkt.budget.bal_avail = bal.bal_avail
					mkt.reserve_amt_calc()
					mkt.budget.spendable_amt = mkt.budget.bal_avail - mkt.budget.reserve_amt 
					if curr in open_trade_amts:
						mkt.budget.open_trade_amt = open_trade_amts[curr]
						mkt.budget.spendable_amt -= mkt.budget.open_trade_amt
					else:
						mkt.budget.open_trade_amt = 0

		func_end(fnc)

	#<=====>#

	def budget_refresh(mkt):
		func_name = 'budget_refresh'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		'''
		"budget": {
			"max_tot_loss": -250.0,
			"spend_max_amt": 2100.0,
			"spend_up_max_pct": 50.00,
			"spend_dn_max_pct": 50.00,
			"spend_max_pcts": {
				"***": {"spend_up_max_pct": 80, "spend_dn_max_pct": 20},
				"BTC-USDC": {"spend_up_max_pct": 60, "spend_dn_max_pct": 40},
				"ETH-USDC": {"spend_up_max_pct": 60, "spend_dn_max_pct": 40},
				"SOL-USDC": {"spend_up_max_pct": 60, "spend_dn_max_pct": 40}
			},
			"mkt_shares": {
				"***": 1,
				"BTC-USDC": 20,
				"ETH-USDC": 20,
				"SOL-USDC": 20,
				"SUI-USDC": 3
			},
			"reserve_amt": 1000.0,
			"reserve_addtl_daily_amt": 5
		},
		'''

		bot_spent_data  = db_bot_spent()[0]
		bot_spent_data  = dec_2_float(bot_spent_data)

		mkt.budget.symb               = mkt.symb
		mkt.budget.open_cnt           = 0
		mkt.budget.open_up_cnt        = 0
		mkt.budget.open_dn_cnt        = 0
		mkt.budget.open_up_pct        = 0
		mkt.budget.open_dn_pct        = 0

		mkt.budget.spend_max_amt      = mkt.mst.budget.spend_max_amt
		mkt.budget.spend_up_max_pct   = mkt.mst.budget.spend_up_max_pct
		mkt.budget.spend_dn_max_pct   = mkt.mst.budget.spend_up_max_pct
		mkt.budget.spend_up_max_amt   = mkt.budget.spend_up_max_pct / 100 * mkt.budget.spend_max_amt
		mkt.budget.spend_dn_max_amt   = mkt.budget.spend_dn_max_pct / 100 * mkt.budget.spend_max_amt
		mkt.budget.spent_amt          = 0
		mkt.budget.spent_pct          = 0
		mkt.budget.spent_up_pct       = 0
		mkt.budget.spent_dn_pct       = 0
		mkt.budget.spent_up_amt       = 0
		mkt.budget.spent_dn_amt       = 0

		mkt.budget.open_amt           = bot_spent_data['open_cnt']
		mkt.budget.open_up_amt        = bot_spent_data['open_up_cnt']
		mkt.budget.open_dn_amt        = bot_spent_data['open_dn_cnt']
		mkt.budget.open_up_pct        = bot_spent_data['open_up_pct']
		mkt.budget.open_dn_pct        = bot_spent_data['open_dn_pct']

		mkt.budget.spent_amt          = bot_spent_data['spent_amt']
		mkt.budget.spent_pct          = round((bot_spent_data['spent_amt'] / mkt.budget.spend_max_amt) * 100)

		mkt.budget.spent_up_amt       = bot_spent_data['spent_up_amt']
		mkt.budget.spent_dn_amt       = bot_spent_data['spent_dn_amt']
		mkt.budget.spent_up_pct       = round((bot_spent_data['spent_up_amt'] / mkt.budget.spent_amt) * 100)
		mkt.budget.spent_dn_pct       = round((bot_spent_data['spent_dn_amt'] / mkt.budget.spent_amt) * 100)

		mkt.budget.spendable_up_amt   = min(mkt.budget.spendable_amt, (mkt.budget.spend_up_max_amt - mkt.budget.spent_up_amt))
		mkt.budget.spendable_dn_amt   = min(mkt.budget.spendable_amt, (mkt.budget.spend_up_max_amt - mkt.budget.spent_dn_amt))

		func_end(fnc)

	#<=====>#

	def budget_display(mkt, budget=None, title=None, footer=None):
		func_name = 'budget_display'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		print_adv(2)
		if title:
			chart_top(in_str=title, len_cnt=218)
		else:
			chart_top(len_cnt=218)

		hmsg = ""
		hmsg += f"{'symb':^6}" + " | "
		hmsg += f"${'spent_amt':^12}" + " | "
		hmsg += f"${'max_amt':^12}" + " | "
		hmsg += f"{'spent_pct':^12} %" + " | "
		hmsg += f"${'spent_up_amt':^12}" + " | "
		hmsg += f"{'spent_up_pct':^12} %" + " | "
		hmsg += f"${'spent_dn_amt':^12}" + " | "
		hmsg += f"{'spent_dn_pct':^12} %" + ' | '
		hmsg += f"$ {'usdc bal':^9}" + " | "
		hmsg += f"$ {'reserve':^9}" + " | "
		hmsg += f"$ {'free':^12}" + " | "
		hmsg += f"$ {'free_up':^12}" + " | "
		hmsg += f"$ {'free_dn':^12}" + " | "
		hmsg += f"{'reserves state':^14}"
		chart_headers(in_str=hmsg, len_cnt=218)

		msg = ""
		msg += f"{budget['symb']:^6}" + " | "
		msg += f"${budget['spent_amt']:>12.4f}" + " | "
		msg += f"${budget['spend_max_amt']:>12.4f}" + " | "
		msg += f"{budget['spent_pct']:>12.2f} %" + " | "
		msg += f"${budget['spent_up_amt']:>12.4f}" + " | "
		msg += f"{budget['spent_up_pct']:>12.2f} %" + " | "
		msg += f"${budget['spent_dn_amt']:>12.4f}" + " | "
		msg += f"{budget['spent_dn_pct']:>12.2f} %" + " | "
		msg += cs(f"$ {mkt.budget.bal_avail:>9.2f}", "white", "green") + " | "
		msg += cs(f"$ {mkt.budget.reserve_amt:>9.2f}", "white", "green") + " | "
		if mkt.budget.spendable_amt > 0:
			msg += cs(f"$ {mkt.budget.spendable_amt:>12.5f}", "white", "green") + " | "
		else:
			msg += cs(f"$ {mkt.budget.spendable_amt:>12.5f}", "white", "red") + " | "
		if mkt.budget.spendable_up_amt > 0:
			msg += cs(f"$ {mkt.budget.spendable_up_amt:>12.5f}", "white", "green") + " | "
		else:
			msg += cs(f"$ {mkt.budget.spendable_up_amt:>12.5f}", "white", "red") + " | "
		if mkt.budget.spendable_dn_amt > 0:
			msg += cs(f"$ {mkt.budget.spendable_dn_amt:>12.5f}", "white", "green") + " | "
		else:
			msg += cs(f"$ {mkt.budget.spendable_dn_amt:>12.5f}", "white", "red") + " | "
		if mkt.budget.reserve_locked_tf:
			msg += cs(f"{'LOCKED':^14}", "yellow", "magenta")
		else:
			msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow")
		chart_row(in_str=msg, len_cnt=218)

		if footer:
			chart_mid(len_cnt=218)
			chart_row(in_str=footer, len_cnt=218)

		chart_bottom(len_cnt=218)
		print_adv(2)

		func_end(fnc)

	#<=====>#

	def reserve_amt_calc(mkt):
		func_name = 'reserve_amt_calc'
		func_str = f'{lib_name}.{func_name}(st, reserve_locked_tf={mkt.budget.reserve_locked_tf})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		day = dt.now().day
		min_reserve_amt                = mkt.mst.budget.reserve_amt
		daily_reserve_amt              = mkt.mst.budget.reserve_addtl_daily_amt
		tot_daily_reserve_amt          = day * daily_reserve_amt

		if mkt.budget.reserve_locked_tf:
			mkt.budget.reserve_amt    = tot_daily_reserve_amt + min_reserve_amt
		else:
			mkt.budget.reserve_amt    = min_reserve_amt

		func_end(fnc)

	#<=====>#

	def pairs_list_get(mkt):
		func_name = 'pairs_list_get'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		mkt.loop_pairs       = []
		mkt.buy_pairs        = []
		mkt.sell_pairs       = []

		if mkt.mode in ('buy', 'full'):
			mkt.buy_pairs = mkt.pairs_list_buy_get()
			hmsg = f'buy mkts ({len(mkt.buy_pairs)}) :'
			chart_mid(in_str=hmsg, len_cnt=177)
			mkt.prt_cols(mkt.buy_pairs, cols=10)
			chart_bottom(len_cnt=177)
			print_adv()

		if mkt.mode in ('sell', 'full'):
			mkt.sell_pairs = mkt.pairs_list_sell_get()
			hmsg = f'sell mkts ({len(mkt.sell_pairs)}) :'
			chart_mid(in_str=hmsg, len_cnt=177)
			mkt.prt_cols(mkt.sell_pairs, cols=10)
			chart_bottom(len_cnt=177)
			print_adv()

		mkt.loop_pairs.extend(mkt.buy_pairs)
		mkt.loop_pairs.extend(mkt.sell_pairs)

		stable_pairs           = mkt.mst.pairs.stable_pairs
		err_pairs              = mkt.mst.pairs.err_pairs
		mkts                  = db_pairs_loop_get(mode=mkt.mode, loop_pairs=mkt.loop_pairs, stable_pairs=stable_pairs, err_pairs=err_pairs)
		# Iterates through the mkts returned from MySQL and converts all decimals to floats
		# This is faster than making everything be done in decimals (which I would prefer)
		mkts                  = dec_2_float(mkts)
		mkt.loop_pairs        = mkts

		func_end(fnc)

	#<=====>#

	def pairs_list_buy_get(mkt):
		func_name = 'pairs_list_buy_get'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		buy_pairs = []

		print_adv(2)
		chart_top(in_str='Buy Market Collection', len_cnt=177)

		# get mkts from settings
		spot_pairs  = mkt.mst.pairs.trade_pairs
		if spot_pairs:
			mkts = list(set(spot_pairs))
			buy_pairs.extend(mkts)

		# Get The Markets with the best performance on the bot so far
		# By Gain Loss Percen Per Hour
		# Settings how many of these we will look at
		pct_min    = mkt.mst.pairs.extra_pairs_top_bot_perf_pct_min
		lmt_cnt    = mkt.mst.pairs.extra_pairs_top_bot_perf_cnt
		mkts       = db_pairs_loop_top_perfs_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min, quote_curr_symb=mkt.symb)
		if mkts:
			if mkt.mst.pairs.extra_pairs_top_bot_perf_yn == 'Y':
				hmsg = f'adding mkts top bot gain loss percent per day performers ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='WoG')
				buy_pairs.extend(mkts)
			elif mkt.mst.pairs.extra_pairs_top_bot_perf_cnt > 0:
				hmsg = f'skipping mkts top bot gain loss percent per day performers ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the best performance on the bot so far
		# By Gain Loss Amount Total
		# Settings how many of these we will look at
		lmt_cnt    = mkt.mst.pairs.extra_pairs_top_bot_gains_cnt
		mkts       = db_pairs_loop_top_gains_prod_ids_get(lmt=lmt_cnt, quote_curr_symb=mkt.symb)
		if mkts:
			if mkt.mst.pairs.extra_pairs_top_bot_gains_yn == 'Y':
				hmsg = f'adding mkts top bot gain loss performers ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='WoG')
				buy_pairs.extend(mkts)
			elif mkt.mst.pairs.extra_pairs_top_bot_gains_cnt > 0:
				hmsg = f'skipping mkts top bot gain loss performers ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h price increase
		# Settings how many of these we will look at
		pct_min    = mkt.mst.pairs.extra_pairs_prc_pct_chg_24h_pct_min
		lmt_cnt    = mkt.mst.pairs.extra_pairs_prc_pct_chg_24h_cnt
		mkts       = db_pairs_loop_top_prc_chg_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min, quote_curr_symb=mkt.symb)
		if mkts:
			if mkt.mst.pairs.extra_pairs_prc_pct_chg_24h_yn == 'Y':
				hmsg = f'adding mkts top price increases ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='WoG')
				buy_pairs.extend(mkts)
			elif mkt.mst.pairs.extra_pairs_prc_pct_chg_24h_cnt > 0:
				hmsg = f'skipping mkts top price increases ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h volume increase
		# Settings how many of these we will look at
		lmt_cnt    = mkt.mst.pairs.extra_pairs_vol_quote_24h_cnt
		mkts       = db_pairs_loop_top_vol_chg_prod_ids_get(lmt=lmt_cnt, quote_curr_symb=mkt.symb)
		if mkts:
			if mkt.mst.pairs.extra_pairs_vol_quote_24h_yn == 'Y':
				hmsg = f'adding mkts highest volume ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='WoG')
				buy_pairs.extend(mkts)
			elif mkt.mst.pairs.extra_pairs_vol_quote_24h_cnt > 0:
				hmsg = f'skipping mkts highest volume ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets with the top 24h volume percent increase
		# Settings how many of these we will look at
		lmt_cnt    = mkt.mst.pairs.extra_pairs_vol_pct_chg_24h_cnt
		mkts       = db_pairs_loop_top_vol_chg_pct_prod_ids_get(lmt=lmt_cnt, quote_curr_symb=mkt.symb)
		if mkts:
			if mkt.mst.pairs.extra_pairs_vol_pct_chg_24h_yn == 'Y':
				hmsg = f'adding mkts highest volume increase ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='WoG')
				buy_pairs.extend(mkts)
			elif mkt.mst.pairs.extra_pairs_vol_pct_chg_24h_cnt > 0:
				hmsg = f'skipping mkts highest volume increase ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='GoW')

		# Get The Markets that are marked as favorites on Coinbase
		mkts       = db_pairs_loop_watched_prod_ids_get(quote_curr_symb=mkt.symb)
		if mkts:
			if mkt.mst.pairs.extra_pairs_watched_yn == 'Y':
				hmsg = f'adding watched markets ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='WoG')
				buy_pairs.extend(mkts)
			else:
				hmsg = f'skipping watched markets ({len(mkts)}) :'
				chart_mid(in_str=hmsg, len_cnt=177)
				mkt.prt_cols(mkts, cols=10, clr='GoW')

		func_end(fnc)
		return buy_pairs

	#<=====>#

	def pairs_list_sell_get(mkt):
		func_name = 'pairs_list_sell_get'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		chart_top(in_str='Sell Market Collection', len_cnt=177)

		sell_pairs = []

		# Get The Markets with Open Positions
		# They all need to be looped through buy/sell logic
		pairs       = db_pairs_loop_poss_open_prod_ids_get(quote_curr_symb=mkt.symb)
		if pairs:
			pairs = list(set(pairs))
			hmsg = f'adding markets with open positions ({len(pairs)}) :'
			chart_mid(in_str=hmsg, len_cnt=177)
			mkt.prt_cols(pairs, cols=10)

			sell_pairs.extend(pairs)

		func_end(fnc)
		return sell_pairs

	#<=====>#

	def prt_cols(mkt, l, cols=10, clr='WoG'):
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

	def ohlcv_tables_check(mkt):
		func_name = 'ohlcv_tables_check'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	#	G(func_str)

		table_names = db_table_names_get()
		for m in mkt.loop_pairs:
			prod_id = m['prod_id']
			table_name = f'ohlcv_{prod_id}'.replace('-','_')
			if table_name not in table_names:
				db_check_ohlcv_prod_id_table(prod_id)

		func_end(fnc)

	#<=====>#

	def mkt_settings(mkt):
		func_name = 'mkt_settings'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		settings_template_json = {
			"edited_yn": "N",
			"speak_yn": "Y",
			"loop_secs": 15,
			"portfoilio_id": "",
			"stable_coins": ["DAI","GUSD","PAX","PYUSD","USD","USDC","USDT"],
			"trade_yn": "Y",
			"trade_live_yn": "Y",
			"budget": {
				"max_tot_loss": -250.0,
				"spend_max_amt": 2100.0,
				"spend_up_max_pct": 50.00,
				"spend_dn_max_pct": 50.00,
				"reserve_amt": 100.0,
				"reserve_addtl_daily_amt": 5,
				"spend_max_pcts": {
					"***": {"spend_up_max_pct": 80,"spend_dn_max_pct": 20},
					"BTC-USDC": {"spend_up_max_pct": 60,"spend_dn_max_pct": 40},
					"ETH-USDC": {"spend_up_max_pct": 60,"spend_dn_max_pct": 40},
					"SOL-USDC": {"spend_up_max_pct": 60,"spend_dn_max_pct": 40}
				},
				"mkt_shares": {
					"***": 1,
					"BTC-USDC": 20,
					"ETH-USDC": 20,
					"SOL-USDC": 20,
					"SUI-USDC": 3
				},
			},
			"pairs": {
				"trade_pairs": [
					"BTC-USDC",
					"ETH-USDC",
					"SOL-USDC",
					"SUI-USDC"
				],
				"stable_pairs": [
					"DAI-USDC",
					"GUSD-USDC",
					"PAX-USDC",
					"PYUSD-USDC",
					"USDT-USDC"
				],
				"err_pairs": [
					"DAI-USDC",
					"MATIC-USDC",
					"MKR-USDC"
				],
				"extra_pairs_watched_yn": "N",
				"extra_pairs_top_bot_perf_yn": "Y",
				"extra_pairs_top_bot_perf_cnt": 10,
				"extra_pairs_top_bot_perf_pct_min": 0.1,
				"extra_pairs_top_bot_gains_yn": "Y",
				"extra_pairs_top_bot_gains_cnt": 20,
				"extra_pairs_prc_pct_chg_24h_yn": "Y",
				"extra_pairs_prc_pct_chg_24h_cnt": 5,
				"extra_pairs_prc_pct_chg_24h_pct_min": 3,
				"extra_pairs_vol_quote_24h_yn": "N",
				"extra_pairs_vol_quote_24h_cnt": 3,
				"extra_pairs_vol_pct_chg_24h_yn": "N",
				"extra_pairs_vol_pct_chg_24h_cnt": 3
			},
			"buy": {
				"buying_on_yn": "Y",
				"force_all_tests_yn": "Y",
				"show_tests_yn": "N",
				"show_tests_min": 101,
				"save_files_yn": "N",
				"buy_limit_yn": "N",
				"show_boosts_yn": "N",
				"allow_tests_yn": "N",
				"mkts_open_max": 100,
				"special_prod_ids": [
					"BTC-USDC",
					"ETH-USDC",
					"SOL-USDC",
					"SUI-USDC"
				],
				"buy_delay_minutes": {
					"***": 5,
					"BTC-USDC": 1,
					"ETH-USDC": 1,
					"SOL-USDC": 1
				},
				"buy_strat_delay_minutes": {
					"***": 30,
					"BTC-USDC": 15,
					"ETH-USDC": 15,
					"SOL-USDC": 15,
					"15min": 8,
					"30min": 15,
					"1h": 30,
					"4h": 120,
					"1d": 720
				},
				"open_poss_cnt_max": {
					"***": 5,
					"BTC-USDC": 40,
					"ETH-USDC": 40,
					"SOL-USDC": 40
				},
				"strat_open_cnt_max": {
					"***": 1,
					"BTC-USDC": 5,
					"ETH-USDC": 5,
					"SOL-USDC": 5
				},
				"trade_size": {
					"***": 10,
					"BTC-USDC": 50,
					"ETH-USDC": 50,
					"SOL-USDC": 50
				},
				"trade_size_min_mult": {
					"***": 5,
					"BTC-USDC": 20,
					"ETH-USDC": 20,
					"SOL-USDC": 20
				},
				"strats": {
					"sha": {
						"use_yn": "Y",
						"freqs": ["1d","4h","1h","30min","15min"],
						"fast_sha_len1": 8,
						"fast_sha_len2": 8,
						"slow_sha_len1": 13,
						"slow_sha_len2": 13,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"***": 31,
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"imp_macd": {
						"use_yn": "Y",
						"freqs": ["1d","4h","1h","30min","15min"],
						"per_ma": 34,
						"per_sign": 9,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"***": 31,
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"emax": {
						"use_yn": "N",
						"freqs": ["1d","4h","1h","30min","15min"],
						"per_fast": 8,
						"per_mid": 13,
						"per_slow": 21,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"***": 31,
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"bb_bo": {
						"use_yn": "Y",
						"freqs": ["1d","4h","1h","30min","15min"],
						"per": 21,
						"sd": 2.1,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"***": 31,
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"bb": {
						"use_yn": "Y",
						"freqs": ["1d","4h","1h","30min","15min"],
						"inner_per": 34,
						"inner_sd": 2.3,
						"outer_per": 34,
						"outer_sd": 2.7,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"***": 31,
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"drop": {
						"use_yn": "Y",
						"freqs": ["1d","4h","1h","30min","15min"],
						"drop_pct": {
							"***": 4,
							"BTC-USDC": 4,
							"ETH-USDC": 4,
							"SOL-USDC": 4
						},
						"prod_ids": [
							"BTC-USDC",
							"ETH-USDC",
							"SOL-USDC"
						],
						"prod_ids_skip": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"***": 31,
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					}
				}
			},
			"sell": {
				"selling_on_yn": "Y",
				"force_all_tests_yn": "Y",
				"show_blocks_yn": "N",
				"show_forces_yn": "Y",
				"show_tests_yn": "N",
				"show_tests_min": 101,
				"save_files_yn": "N",
				"sell_limit_yn": "N",
				"take_profit": {
					"hard_take_profit_yn": "Y",
					"hard_take_profit_pct": 100,
					"trailing_profit_yn": "Y",
					"trailing_profit_trigger_pct": 3
				},
				"stop_loss": {
					"hard_stop_loss_yn": "Y",
					"hard_stop_loss_pct": 11,
					"trailing_stop_loss_yn": "N",
					"trailing_stop_loss_pct": 10,
					"atr_stop_loss_yn": "N",
					"atr_stop_loss_rfreq": "1d",
					"trailing_atr_stop_loss_yn": "N",
					"trailing_atr_stop_loss_pct": 70,
					"trailing_atr_stop_loss_rfreq": "1d"
				},
				"force_sell_all_yn": "N",
				"force_sell": {
					"prod_ids": [
						"CBETH-USDC",
						"LSETH-USDC",
						"MSOL-USDC",
						"WAMPL-USDC",
						"WAXL-USDC",
						"WBTC-USDC",
						"WCFG-USDC",
						"MATIC-USDC"
					],
					"pos_ids": [
						2741,
						3044
					]
				},
				"never_sell_all_yn": "N",
				"never_sell": {
					"prod_ids": [],
					"pos_ids": []
				},
				"never_sell_loss_all_yn": "N",
				"never_sell_loss": {
					"prod_ids": [
						"BTC-USDC",
						"ETH-USDC",
						"SOL-USDC"
					],
					"pos_ids": []
				},
				"strats": {
					"sha": {
						"exit_if_profit_yn": "Y",
						"exit_if_profit_pct_min": 1,
						"exit_if_loss_yn": "N",
						"exit_if_loss_pct_max": 3,
						"skip_prod_ids": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						}
					},
					"imp_macd": {
						"exit_if_profit_yn": "Y",
						"exit_if_profit_pct_min": 1,
						"exit_if_loss_yn": "N",
						"exit_if_loss_pct_max": 3,
						"skip_prod_ids": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						}
					},
					"bb_bo": {
						"exit_if_profit_yn": "Y",
						"exit_if_profit_pct_min": 1,
						"exit_if_loss_yn": "N",
						"exit_if_loss_pct_max": 3,
						"skip_prod_ids": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						}
					},
					"bb": {
						"exit_if_profit_yn": "Y",
						"exit_if_profit_pct_min": 1,
						"exit_if_loss_yn": "N",
						"exit_if_loss_pct_max": 3,
						"skip_prod_ids": [],
						"tests_min": {
							"***": 15,
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						}
					}
				},
				"rainy_day": {
					"pocket_pct": {
						"***": 10,
						"BTC-USDC": 50,
						"ETH-USDC": 50,
						"SOL-USDC": 50
					},
					"clip_pct": {
						"***": 0,
						"BTC-USDC": 5,
						"ETH-USDC": 5,
						"SOL-USDC": 5
					}
				}
			}
		}

		mkt.mkt_settings = Settings(f'settings/{mkt.fpath}', settings_template_json)
		mkt.mst = mkt.mkt_settings.settings_load()

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
