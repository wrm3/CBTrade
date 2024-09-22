#<=====>#
# Description
#<=====>#


#<=====>#
# Import All
#<=====>#

import_all_func_list = []
import_all_func_list.append("report_open")
import_all_func_list.append("report_open_by_age")
import_all_func_list.append("report_open_by_gain")
import_all_func_list.append("report_open_by_prod_id")
import_all_func_list.append("report_buys_recent")
import_all_func_list.append("report_sells_recent")
import_all_func_list.append("report_strats_best")
import_all_func_list.append("report_pos_open")
import_all_func_list.append("report_pos_close")
import_all_func_list.append("report_strat")
import_all_func_list.append("report_strats")
import_all_func_list.append("disp_recent")
__all__ = import_all_func_list


#<=====>#
# Imports - Common Modules
#<=====>#

import sys
import os
import pytz
import sys
import time
import traceback
from datetime            import datetime
from pprint              import pprint

#<=====>#
# Imports - Download Modules
#<=====>#


#<=====>#
# Imports - Shared Library
#<=====>#
#shared_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SHARED_LIBS'))
#if shared_libs_path not in sys.path:
#	sys.path.append(shared_libs_path)


#<=====>#
# Imports - Local Library
#<=====>#
local_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'libs'))
if local_libs_path not in sys.path:
	sys.path.append(local_libs_path)

from lib_charts                   import *
from lib_common                   import *
from lib_colors                   import *
from lib_strings                  import *

from bot_common                    import *
from bot_db_read                   import *
from bot_settings                  import settings
from bot_theme                     import *
#from bot                               import bot

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_reports'
log_name      = 'bot_reports'
lib_verbosity = 1
lib_debug_lvl = 1
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

def report_open():
	func_name = 'report_open'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	poss = db_poss_open_get(include_test_yn='Y')

	if poss:
		print_adv(2)
		title = f'Open Positions - By Age'
		show_pos_open_header_yn = 'Y'
		poss_sorted = sorted(poss, key=lambda x: x["age_mins"], reverse=True)
		poss = poss_sorted
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
			pos.report_age = format_disp_age(pos.age_mins)
			report_pos_open(title, pos, show_pos_open_header_yn)
			show_pos_open_header_yn = 'N'

		chart_bottom(in_str='bottom1', len_cnt=260)

	if poss:
		print_adv(2)
		title = f'Open Positions - By Prod_id'
		show_pos_open_header_yn = 'Y'
		poss_sorted = sorted(poss, key=lambda x: x["prod_id"])
		poss = poss_sorted
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
			pos.report_age = format_disp_age(pos.age_mins)
			report_pos_open(title, pos, show_pos_open_header_yn)
			show_pos_open_header_yn = 'N'

		chart_bottom(in_str='bottom2', len_cnt=260)

	func_end(fnc)

	#<=====>#

#<=====>#

def report_open_by_age():
	func_name = 'report_open_by_age'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	poss = db_poss_open_get(include_test_yn='Y')

	if poss:
		print_adv(2)
		title = f'Open Positions - By Age'
		show_pos_open_header_yn = 'Y'
		poss_sorted = sorted(poss, key=lambda x: x["age_mins"], reverse=True)
		poss = poss_sorted
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
			pos.report_age = format_disp_age(pos.age_mins)
			report_pos_open(title, pos, show_pos_open_header_yn)
			show_pos_open_header_yn = 'N'

		chart_bottom(in_str='bottom3', len_cnt=226)

	func_end(fnc)

	#<=====>#

#<=====>#

def report_open_by_gain():
	func_name = 'report_open_by_gain'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	poss = db_poss_open_get(include_test_yn='Y')

	if poss:
		print_adv(2)
		title = f'Open Positions - By Prod_id'
		show_pos_open_header_yn = 'Y'
		poss_sorted = sorted(poss, key=lambda x: x["gain_loss_pct"], reverse=True)
		poss = poss_sorted
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
			pos.report_age = format_disp_age(pos.age_mins)
			report_pos_open(title, pos, show_pos_open_header_yn)
			show_pos_open_header_yn = 'N'

		chart_bottom(in_str='bottom4', len_cnt=226)
	func_end(fnc)

	#<=====>#

#<=====>#

def report_open_by_prod_id():
	func_name = 'report_open_by_prod_id'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	poss = db_poss_open_get(include_test_yn='Y')

	if poss:
		print_adv(2)
		title = f'Open Positions - By Prod_id'
		show_pos_open_header_yn = 'Y'
		poss_sorted = sorted(poss, key=lambda x: x["prod_id"])
		poss = poss_sorted
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
			pos.report_age = format_disp_age(pos.age_mins)
			report_pos_open(title, pos, show_pos_open_header_yn)
			show_pos_open_header_yn = 'N'

		chart_bottom(in_str='bottom4', len_cnt=226)
	func_end(fnc)

	#<=====>#

#<=====>#

def report_buys_recent(cnt=15, test_yn='N'):
	func_name = 'report_buys_recent'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	print_adv(2)

	title = f'Last {cnt} Opened Positions'
	if test_yn == 'N':
		title = f'Last {cnt} Opened Positions - Live'
	elif test_yn == 'Y':
		title = f'Last {cnt} Opened Positions - Test'

	poss = db_poss_open_recent_get(lmt=cnt, test_yn=test_yn)
#	poss = db_poss_close_recent_get(lmt=cnt)
	show_pos_open_header_yn = 'Y'
	if poss:
#		poss_sorted = sorted(poss, key=lambda x: x["age_mins"], reverse=True)
#		poss = poss_sorted
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
			pos.report_age = format_disp_age(pos.age_mins)
			report_pos_open(title, pos, show_pos_open_header_yn)
			show_pos_open_header_yn = 'N'

		chart_bottom(in_str='bottom5', len_cnt=226)
	func_end(fnc)

#<=====>#

def report_sells_recent(cnt=15, test_yn='N'):
	func_name = 'report_sells_recent'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	print_adv(2)

	title = f'Last {cnt} Closed Positions'
	if test_yn == 'N':
		title = f'Last {cnt} Closed Positions - Live'
	elif test_yn == 'Y':
		title = f'Last {cnt} Closed Positions - Test'

	poss = db_poss_close_recent_get(lmt=cnt, test_yn=test_yn)
	show_pos_close_header_yn = 'Y'
	if poss:
#		poss_sorted = sorted(poss, key=lambda x: x["age_mins"], reverse=True)
#		poss = poss_sorted
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_end_dttm = pos.pos_end_dttm.strftime('%m-%d-%Y %H:%M')
			pos.report_age = format_disp_age(pos.age_mins)
			report_pos_close(title, pos, show_pos_close_header_yn)
			show_pos_close_header_yn = 'N'

		chart_bottom(in_str='bottom6', len_cnt=251)
	func_end(fnc)

#<=====>#

def report_strats_best(cnt=10, min_trades=1):
	func_name = 'report_strats_best'
	func_str = f'{lib_name}.{func_name}(cnt={cnt}, min_trades={min_trades})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	print_adv(2)

	title = f'Best {cnt} Buy Strats with minimum of {min_trades} Trades'
	poss_strats = db_mkt_strats_used_get(min_trades)
	mkt_strats_perf = []

#	pprint(poss_strats)
	for x in poss_strats:
		prod_id        = x['prod_id']
		buy_strat_type = x['buy_strat_type']
		buy_strat_name = x['buy_strat_name']
		buy_strat_freq = x['buy_strat_freq']

		buy_strat_desc = ''
#		for z in buy_strats:
#			print(buy_strats[z])
#			if buy_strat_name == buy_strats[z]['buy_strat_name']:
#				buy_strat_desc = z['buy_strat_desc']
		if buy_strat_name == 'sha': buy_strat_desc = 'Double Smoothed Heikin Ashi'
		elif buy_strat_name == 'imp_macd': buy_strat_desc = 'Impulse MACD'
		elif buy_strat_name == 'emax': buy_strat_desc = 'Triple EMA Crossover'
		elif buy_strat_name == 'bb_bo': buy_strat_desc = 'Bollinger Band Breakout'
		elif buy_strat_name == 'drop': buy_strat_desc = 'Big Dip Strat'
		elif buy_strat_name == 'bb': buy_strat_desc = 'Double Bollinger Band'

		mkt_strat_perf = db_trade_strat_perf_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
#		pprint(mkt_strat_perf)
		mkt_strat_perf = dec_2_float(mkt_strat_perf)
		mkt_strat_perf = AttrDictConv(in_dict=mkt_strat_perf)
		if mkt_strat_perf:
			mkt_strat_perf.buy_strat_desc = buy_strat_desc
#			pprint(mkt_strat_perf)
			r = db_mkt_strat_elapsed_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
			mkt_strat_perf.strat_bo_elapsed   = r[0]
			mkt_strat_perf.strat_pos_elapsed  = r[1]
			mkt_strat_perf.strat_last_elapsed = r[2]
			mkt_strats_perf.append(mkt_strat_perf)
		else:
			pprint(x)
			pprint(mkt_strat_perf)

	mkt_strats_perf_sorted = sorted(mkt_strats_perf, key=lambda x: x["gain_loss_pct_day"], reverse=True)
	mkt_strats_perf = mkt_strats_perf_sorted

	show_strat_header_yn = 'Y'

	show_cnt = 0
	if mkt_strats_perf:
		for mkt_strat_perf in mkt_strats_perf:
			show_cnt += 1
			mkt_strat_perf = dec_2_float(mkt_strat_perf)
			mkt_strat_perf = AttrDictConv(in_dict=mkt_strat_perf)
			report_strat(title, mkt_strat_perf, show_strat_header_yn)
			show_strat_header_yn = 'N'
			if show_cnt >= cnt:
				break

		chart_bottom(in_str='bottom7', len_cnt=232)

	func_end(fnc)

#<=====>#

def report_pos_open(title, pos, show_pos_open_header_yn='Y'):
	func_name = 'report_pos_open'
	func_str = f'{lib_name}.{func_name}(pos)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

#	chart_title('Currently Open Positions - By Market', len(hmsg))

	hmsg = ''
	hmsg += f"{'mkt':^12} | "
	hmsg += f"{'T':^1} | "
	hmsg += f"{'pos_id':^6} | "
	hmsg += f"{'strat':^10} | "
	hmsg += f"{'freq':^10} | "
	hmsg += f"{'age':^10} | "
	hmsg += f"{'open @ est':^16} | "
#	hmsg += f"{'curr_val':^16} | "
	hmsg += f"{'buy_val':^16} | "
	hmsg += f"{'buy_prc':^14} | "
	hmsg += f"{'curr_prc':^14} | "
	hmsg += f"{'high_prc':^14} | "
	hmsg += f"{'gain_pct':^8} % | "
	hmsg += f"{'gain_top':^8} % | "
#	hmsg += f"{'gain_low':^8} % | "
	hmsg += f"{'drop_pct':^8} % | "
	hmsg += f"{'gain_loss':^14} | "
	hmsg += f"{'gain_loss_high':^14}"

	if show_pos_open_header_yn == 'Y':
		print(len(hmsg))
#		chart_top(len_cnt=len(hmsg))
		chart_top(in_str=title, len_cnt=len(hmsg), align='center')
		chart_headers(in_str=hmsg, len_cnt=len(hmsg), align='center')
		chart_mid(len_cnt=len(hmsg))
		show_pos_open_header_yn = 'N'

	if pos.test_tf == 1:
		test_tf = '*'
	else:
		test_tf = ''

	msg = ''
	msg += f'{pos.prod_id:<12} | '
	msg += f'{test_tf:^1} | '
	msg += f'{pos.pos_id:^6} | '
	msg += f'{pos.buy_strat_name:>10} | '
	msg += f'{pos.buy_strat_freq:>10} | '
	msg += f'{pos.report_age:>10} | '
	msg += f"{pos.pos_begin_dttm:>16} | "
#	msg += f'$ {pos.val_tot:>14.8f} | '
	msg += f'$ {pos.tot_out_cnt:>14.8f} | '
	msg += f'{pos.prc_buy:>14.8f} | '
	msg += f'{pos.prc_curr:>14.8f} | '
	msg += f'{pos.prc_high:>14.8f} | '
	msg += f'{pos.gain_loss_pct:>8.2f} % | '
	msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
#	msg += f'{pos.gain_loss_pct_est_low:>8.2f} % | '
	msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
	msg += f'{pos.gain_loss_amt:>14.8f} | '
	msg += f'{pos.gain_loss_amt_est_high:>14.8f}'

	msg = cs_pct_color(pos.prc_chg_pct, msg)
	chart_row(msg, len_cnt=len(hmsg))

	func_end(fnc)

	#<=====>#

def report_pos_close(title, pos, show_pos_close_header_yn='Y'):
	func_name = 'report_pos_close'
	func_str = f'{lib_name}.{func_name}(pos)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	hmsg = ""
	hmsg += f"{'mkt':^12} | "
	hmsg += f"{'T':^1} | "
	hmsg += f"{'pos_id':^6} | "
	hmsg += f"{'strat':^10} | "
	hmsg += f"{'freq':^5} | "
	hmsg += f"{'sell':^14} | "
	hmsg += f"{'age':^10} | "
	hmsg += f"{'sold @ est':^16} | "
#	hmsg += f"{'curr_val':^16} | "
	hmsg += f"{'buy_val':^16} | "
	hmsg += f"{'buy_prc':^14} | "
	hmsg += f"{'curr_prc':^14} | "
#	hmsg += f"{'high_prc':^14} | "
	hmsg += f"{'gain_pct':^8} % | "
	hmsg += f"{'gain_est':^8} % | "
	hmsg += f"{'gain_top':^8} % | "
#	hmsg += f"{'gain_low':^8} % | "
	hmsg += f"{'drop_pct':^8} % | "
	hmsg += f"{'gain_loss':^14} | "
	hmsg += f"{'gain_loss_est':^14} | "
	hmsg += f"{'gain_loss_high':^14}"

	if show_pos_close_header_yn == 'Y':
		print(len(hmsg))
		chart_top(in_str=title, len_cnt=len(hmsg), align='center')
		chart_headers(in_str=hmsg, len_cnt=len(hmsg), align='center')
		chart_mid(len_cnt=len(hmsg))
		show_pos_close_header_yn = 'N'

#	utc_timezone = pytz.utc
#	pos.pos_end_dttm = utc_timezone.localize(pos.pos_end_dttm)

	pos.pos_end_dttm = datetime.strptime(pos.pos_end_dttm, "%m-%d-%Y %H:%M")
	utc_timezone = pytz.utc
	pos.pos_end_dttm = utc_timezone.localize(pos.pos_end_dttm)
	local_timezone = pytz.timezone('America/New_York')
	pos.pos_end_dttm = pos.pos_end_dttm.astimezone(local_timezone)
	pos.pos_end_dttm = datetime.strftime(pos.pos_end_dttm, "%m-%d-%Y %H:%M")

	if pos.test_tf == 1:
		test_tf = '*'
	else:
		test_tf = ''

	msg = ''
	msg += f'{pos.prod_id:<12} | '
	msg += f'{test_tf:^1} | '
	msg += f'{pos.pos_id:<6} | '
	msg += f'{pos.buy_strat_name:>10} | '
	msg += f'{pos.buy_strat_freq:>5} | '
	msg += f'{pos.sell_strat_name:>14} | '
	msg += f'{pos.report_age:>10} | '
	msg += f"{pos.pos_end_dttm:>16} | "
#	msg += f'$ {pos.val_tot:>14.8f} | '
	msg += f'$ {pos.tot_out_cnt:>14.8f} | '
	msg += f'{pos.prc_buy:>14.8f} | '
	msg += f'{pos.prc_curr:>14.8f} | '
#	msg += f'{pos.prc_high:>14.8f} | '
	msg += f'{pos.gain_loss_pct:>8.2f} % | ' # Open Shows Estimates, Closed Shows Actual
	msg += f'{pos.gain_loss_pct_est:>8.2f} % | '  # Open Shows Estimates, Closed Shows Actual
	msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
#	msg += f'{pos.gain_loss_pct_est_low:>8.2f} % | '
	msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
	msg += f'{pos.gain_loss_amt:>14.8f} | '
	msg += f'{pos.gain_loss_amt_est:>14.8f} | '   # Open Shows Estimates, Closed Shows Actual
	msg += f'{pos.gain_loss_amt_est_high:>14.8f}'

	msg = cs_pct_color(pos.prc_chg_pct, msg)
	chart_row(msg, len_cnt=len(hmsg))

	func_end(fnc)

#<=====>#

def report_strat(title, mkt_strat_perf, show_strat_header_yn):
	func_name = 'report_strat'
	func_str = f'{lib_name}.{func_name}(title, mkt_strat_perf, show_strat_header_yn)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

#	pprint(mkt_strat_perf)

	hmsg = ""
#	hmsg += f"{x.prod_id} | "
#	hmsg += f"{x.buy_strat_type} | "
	hmsg += f"{'mkt':<15} | "
	hmsg += f"{'desc':<45} | "
	hmsg += f"{'strat':<15} | "
	hmsg += f"{'freq':<15} | "
	hmsg += f"{'total':^5} | "
	hmsg += f"{'open':^5} | "
	hmsg += f"{'close':^5} | "
	hmsg += f"{'wins':^5} | "
	hmsg += f"{'lose':^5} | "
	hmsg += f"{'win':^6} % | "
	hmsg += f"{'lose':^6} % | "
#	hmsg += f"{'hours':<6} | "
#	hmsg += f"{'tot_out_cnt':<10} | "
#	hmsg += f"{'tot_in_cnt':<10} | "
#	hmsg += f"{'fees_cnt_tot':<10} | "
#	hmsg += f"{'val_curr':<10} | "
#	hmsg += f"{'val_tot':<10} | "
	hmsg += f"{'gain_amt':^10} | "
	hmsg += f"{'gain_pct':^10} % | "
	hmsg += f"{'gain_hr':^10} % | "
	hmsg += f"{'gain_day':^10} % | "
#	hmsg += f"{'bo_elapsed':<10} | "
#	hmsg += f"{'pos_elapsed':<10} | "
	hmsg += f"{'elapsed':^7} | "

	if show_strat_header_yn == 'Y':
		print(len(hmsg))
		chart_top(in_str=title, len_cnt=len(hmsg), align='center')
		chart_headers(in_str=hmsg, len_cnt=len(hmsg), align='center')
		chart_mid(len_cnt=len(hmsg))
		show_strat_header_yn = 'N'

	msg = ''
	msg += f'{mkt_strat_perf.prod_id:<15} | '
#	msg += f'{mkt_strat_perf.buy_strat_type} | '
	msg += f'{mkt_strat_perf.buy_strat_desc:<45} | '
	msg += f'{mkt_strat_perf.buy_strat_name:<15} | '
	msg += f'{mkt_strat_perf.buy_strat_freq:<15} | '
	msg += f'{int(mkt_strat_perf.tot_cnt):>5} | '
	msg += f'{int(mkt_strat_perf.open_cnt):>5} | '
	msg += f'{int(mkt_strat_perf.close_cnt):>5} | '
	msg += f'{int(mkt_strat_perf.win_cnt):>5} | '
	msg += f'{int(mkt_strat_perf.lose_cnt):>5} | '
	msg += f'{mkt_strat_perf.win_pct:>6.2f} % | '
	msg += f'{mkt_strat_perf.lose_pct:>6.2f} % | '
#	msg += f'{mkt_strat_perf.age_hours:<6} | '
#	msg += f'{mkt_strat_perf.tot_out_cnt:<10} | '
#	msg += f'{mkt_strat_perf.tot_in_cnt:<10} | '
#	msg += f'{mkt_strat_perf.fees_cnt_tot:<10} | '
#	msg += f'{mkt_strat_perf.val_curr:<10} | '
#	msg += f'{mkt_strat_perf.val_tot:<10} | '
	msg += f'{mkt_strat_perf.gain_loss_amt:>10.2f} | '
	msg += f'{mkt_strat_perf.gain_loss_pct:>10.2f} % | '
	msg += f'{mkt_strat_perf.gain_loss_pct_hr:>10.2f} % | '
	msg += f'{mkt_strat_perf.gain_loss_pct_day:>10.2f} % | '
#	msg += f'{mkt_strat_perf.bo_elapsed:<10} | '
#	msg += f'{mkt_strat_perf.pos_elapsed:<10} | '
	msg += f'{mkt_strat_perf.strat_last_elapsed:>7} | '
	msg = cs_pct_color_50(pct=mkt_strat_perf.win_pct, msg=msg)

	chart_row(in_str=msg, len_cnt=len(hmsg))

	func_end(fnc)

#<=====>#

def report_strats():
	func_name = 'report_strats'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	hf = ''
	mf = ''
	hs = []

	hs.append('mkt')
	hf += '{:^12} | '
	mf += '{:<12} | '

	hs.append('stat')
	hf += '{:^8} | '
	mf += '{:^8} | '

	hs.append('win_cnt')
	hf += '{:^8} | '
	mf += '{:^8} | '

	hs.append('loss_cnt')
	hf += '{:^8} | '
	mf += '{:^8} | '

	hs.append('sell_cnt')
	mf += '{:^8} | '
	hf += '{:^8} | '

#	hs.append('sell_attempts')
#	hf += '{:^8} | '
#	mf += '{:^8} | '

	hs.append('spent_amt')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

	hs.append('recv_amt')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

	hs.append('win_amt')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

	hs.append('loss_amt')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

	hs.append('pocket_amt')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

	hs.append('clip_amt')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

	hs.append('hold_amt')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

	hs.append('val_curr')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

#	hs.append('fees_buy')
#	hf += '{:^21} | '
#	mf += '{:>21.8f} | '

#	hs.append('fees_sell')
#	hf += '{:^21} | '
#	mf += '{:>21.8f} | '

	hs.append('fees_tot')
	hf += '{:^10} | '
	mf += '{:>10.2f} | '

	hs.append('gain_loss_amt')
	hf += '{:^21} | '
	mf += '{:>21.8f} | '

	hs.append('gain_loss_amt_est_high')
	hf += '{:^21}'
	mf += '{:>21.8f}'

	header = hf.format(*hs)

	strats = db_strats_w_stats_get_all()

	for strat in strats:
		print_adv(2)

		buy_strat_type = strat['buy_strat_type']
		buy_strat_name = strat['buy_strat_name']
		buy_strat_freq = strat['buy_strat_freq']

		WoM('{:^200}'.format('Strategy ==> {} - {} - {}'.format(buy_strat_type.upper(), buy_strat_name.upper(), buy_strat_freq.upper())))

		x = db_strats_perf_get_all(buy_strat_type=buy_strat_type, buy_strat_name=buy_strat_name, buy_strat_freq=buy_strat_freq)
		if x:
			win_cnt_tot            = 0
			loss_cnt_tot           = 0
			sell_cnt_tot           = 0
			spent_amt_tot          = 0
			recv_amt_tot           = 0
			win_amt_tot            = 0
			loss_ant_tot           = 0
			hold_amt_tot           = 0
			pocket_amt_tot         = 0
			clip_amt_tot           = 0
			fees_buy_tot           = 0
			fees_sell_tot          = 0
			fees_tot_tot           = 0
			val_tot_tot            = 0
			gain_loss_amt_tot      = 0
			gain_loss_amt_est_high_tot = 0
	
			first_loop_yn = 'Y'
			for r in x:
				if first_loop_yn == 'Y':
					chart_headers(header, len(header))
					first_loop_yn = 'N'

				mkt                     = r['mkt']
				pos_stat                = r['pos_stat']
				win_cnt             = int(r['win_cnt'])
				loss_cnt            = int(r['loss_cnt'])
				sell_cnt            = int(r['sell_cnt'])
				spent_amt           = float(r['spent_amt'])
				recv_amt            = float(r['recv_amt'])
				win_amt             = float(r['win_amt'])
				loss_amt            = float(r['loss_amt'])
				hold_amt            = float(r['hold_amt'])
				pocket_amt          = float(r['pocket_amt'])
				clip_amt            = float(r['clip_amt'])
				val_tot             = float(r['val_tot'])
				fees_buy            = float(r['fees_buy'])
				fees_sell           = float(r['fees_sell'])
				fees_tot            = float(r['fees_tot'])
				gain_loss_amt       = float(r['gain_loss_amt'])
				gain_loss_amt_est_high  = float(r['gain_loss_amt_est_high'])

				win_cnt_tot            += win_cnt
				loss_cnt_tot           += loss_cnt
				sell_cnt_tot           += sell_cnt
				spent_amt_tot          += spent_amt
				recv_amt_tot           += recv_amt
				win_amt_tot            += win_amt
				loss_ant_tot           += loss_amt
				hold_amt_tot           += hold_amt
				pocket_amt_tot         += pocket_amt
				clip_amt_tot           += clip_amt
				fees_buy_tot           += fees_buy
				fees_sell_tot          += fees_sell
				fees_tot_tot           += fees_tot
				val_tot_tot            += val_tot
				gain_loss_amt_tot      += gain_loss_amt
				gain_loss_amt_est_high_tot += gain_loss_amt_est_high

				md = []
				md.append(mkt)
				md.append(pos_stat)
				md.append(win_cnt)
				md.append(loss_cnt)
				md.append(sell_cnt)
				md.append(spent_amt)
				md.append(recv_amt)
				md.append(win_amt)
				md.append(loss_amt)
				md.append(pocket_amt)
				md.append(clip_amt)
				md.append(hold_amt)
				md.append(val_tot)
				md.append(fees_tot)
				md.append(gain_loss_amt)
				md.append(gain_loss_amt_est_high)
				msg = mf.format(*md)
				if gain_loss_amt > 0:
					WoG(msg)
				elif gain_loss_amt < 0:
					WoR(msg)
				else:
					print(msg)

			header2 = header
			WoB(header2)

			ms2 = []
			ms2.append('')
			ms2.append('')
			ms2.append(win_cnt_tot)
			ms2.append(loss_cnt_tot)
			ms2.append(sell_cnt_tot)
			ms2.append(spent_amt_tot)
			ms2.append(recv_amt_tot )
			ms2.append(win_amt_tot)
			ms2.append(loss_ant_tot)
			ms2.append(pocket_amt_tot)
			ms2.append(clip_amt_tot)
			ms2.append(hold_amt_tot)
			ms2.append(val_tot_tot)
			ms2.append(fees_tot_tot)
			ms2.append(gain_loss_amt_tot)
			ms2.append(gain_loss_amt_est_high_tot)

			msg2 = mf.format(*ms2)
			if gain_loss_amt_tot > 0:
				WoG(msg2)
			elif gain_loss_amt_tot < 0:
				WoR(msg2)
			else:
				print(msg2)

	func_end(fnc)

#<=====>#

def disp_recent(show_pos_close_header_yn='Y'):
	func_name = 'disp_recent'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)

	print_adv(3)

	hmsg = ""
	hmsg += f"{'mkt':^16} | "
	hmsg += f"{'pos_id':^6} | "
	hmsg += f"{'strat':^10} | "
	hmsg += f"{'freq':^5} | "
	hmsg += f"{'sell':^14} | "
	hmsg += f"{'age':^10} | "
	hmsg += f"{'sold @ utc':^16} | "
#	hmsg += f"{'curr_val':^16} | "
	hmsg += f"{'buy_val':^16} | "
	hmsg += f"{'buy_prc':^14} | "
	hmsg += f"{'curr_prc':^14} | "
	hmsg += f"{'high_prc':^14} | "
	hmsg += f"{'gain_pct':^8} % | "
	hmsg += f"{'gain_est':^8} % | "
	hmsg += f"{'gain_top':^8} % | "
#	hmsg += f"{'gain_low':^8} % | "
	hmsg += f"{'drop_pct':^8} % | "
	hmsg += f"{'gain_loss':^14} | "
	hmsg += f"{'gain_loss_est':^14} | "
	hmsg += f"{'gain_loss_high':^14}"

	title = 'Recently Closed Positions'
	show_pos_close_header_yn = 'Y'
	if show_pos_close_header_yn == 'Y':
		print(len(hmsg))
		chart_top(in_str=title, len_cnt=len(hmsg), align='center')
		chart_headers(in_str=hmsg, len_cnt=len(hmsg), align='center')
		chart_mid(len_cnt=len(hmsg))
		show_pos_close_header_yn = 'N'

	poss = db_poss_close_recent_get(lmt=20)
	if poss:
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_end_dttm = pos.pos_end_dttm.strftime('%m-%d-%Y %H:%M')
			disp_age = format_disp_age(pos.age_mins)

			msg = ''
			msg += f'{pos.prod_id:<16} | '
			msg += f'{pos.pos_id:^6} | '
			msg += f'{pos.buy_strat_name:>10} | '
			msg += f'{pos.buy_strat_freq:>5} | '
			msg += f'{pos.sell_strat_name:>14} | '
			msg += f'{disp_age:>10} | '
			msg += f"{pos.pos_end_dttm:>16} | "
#			msg += f'$ {pos.val_tot:>14.8f} | '
			msg += f'$ {pos.tot_out_cnt:>14.8f} | '
			msg += f'{pos.prc_buy:>14.8f} | '
			msg += f'{pos.prc_curr:>14.8f} | '
			msg += f'{pos.prc_high:>14.8f} | '
			msg += f'{pos.gain_loss_pct:>8.2f} % | ' # Open Shows Estimates, Closed Shows Actual
			msg += f'{pos.gain_loss_pct_est:>8.2f} % | '  # Open Shows Estimates, Closed Shows Actual
			msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
#			msg += f'{pos.gain_loss_pct_est_low:>8.2f} % | '
			msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
			msg += f'{pos.gain_loss_amt:>14.8f} | '
			msg += f'{pos.gain_loss_amt_est:>14.8f} | '   # Open Shows Estimates, Closed Shows Actual
			msg += f'{pos.gain_loss_amt_est_high:>14.8f}'

			msg = cs_pct_color(pos.prc_chg_pct, msg)
			chart_row(in_str=msg, len_cnt=len(hmsg))

	print_adv(3)

	hmsg = ''
	hmsg += f"{'mkt':^16} | "
	hmsg += f"{'pos_id':^6} | "
	hmsg += f"{'strat':^10} | "
	hmsg += f"{'freq':^10} | "
	hmsg += f"{'age':^10} | "
	hmsg += f"{'open @ est':^16} | "
#	hmsg += f"{'curr_val':^16} | "
	hmsg += f"{'buy_val':^16} | "
	hmsg += f"{'buy_prc':^14} | "
	hmsg += f"{'curr_prc':^14} | "
	hmsg += f"{'high_prc':^14} | "
	hmsg += f"{'gain_pct':^8} % | "
	hmsg += f"{'gain_top':^8} % | "
#	hmsg += f"{'gain_low':^8} % | "
	hmsg += f"{'drop_pct':^8} % | "
	hmsg += f"{'gain_loss':^14} | "
	hmsg += f"{'gain_loss_high':^14}"

	title = 'Currently Open Positions - By Market'
	show_pos_close_header_yn = 'Y'
	if show_pos_close_header_yn == 'Y':
		print(len(hmsg))
		chart_top(in_str=title, len_cnt=len(hmsg), align='center')
		chart_headers(in_str=hmsg, len_cnt=len(hmsg), align='center')
		chart_mid(len_cnt=len(hmsg))
		show_pos_close_header_yn = 'N'

	poss = db_poss_open_get()
	if poss:
		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
			disp_age = format_disp_age(pos.age_mins)

			msg = ''
			msg += f'{pos.prod_id:<16} | '
			msg += f'{pos.pos_id:^6} | '
			msg += f'{pos.buy_strat_name:>10} | '
			msg += f'{pos.buy_strat_freq:>10} | '
			msg += f'{disp_age:>10} | '
			msg += f"{pos.pos_begin_dttm:>16} | "
#			msg += f'$ {pos.val_tot:>14.8f} | '
			msg += f'$ {pos.tot_out_cnt:>14.8f} | '
			msg += f'{pos.prc_buy:>14.8f} | '
			msg += f'{pos.prc_curr:>14.8f} | '
			msg += f'{pos.prc_high:>14.8f} | '
			msg += f'{pos.gain_loss_pct:>8.2f} % | '
			msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
#			msg += f'{pos.gain_loss_pct_est_low:>8.2f} % | '
			msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
			msg += f'{pos.gain_loss_amt:>14.8f} | '
			msg += f'{pos.gain_loss_amt_est_high:>14.8f}'

			msg = cs_pct_color(pos.prc_chg_pct, msg)
			chart_row(in_str=msg, len_cnt=len(hmsg))

	print_adv(3)

	hmsg = ''
	hmsg += f"{'mkt':^16} | "
	hmsg += f"{'pos_id':^6} | "
	hmsg += f"{'strat':^10} | "
	hmsg += f"{'freq':^10} | "
	hmsg += f"{'age':^10} | "
	hmsg += f"{'open @ est':^16} | "
#	hmsg += f"{'curr_val':^16} | "
	hmsg += f"{'buy_val':^16} | "
	hmsg += f"{'buy_prc':^14} | "
	hmsg += f"{'curr_prc':^14} | "
	hmsg += f"{'high_prc':^14} | "
	hmsg += f"{'gain_pct':^8} % | "
	hmsg += f"{'gain_top':^8} % | "
#	hmsg += f"{'gain_low':^8} % | "
	hmsg += f"{'drop_pct':^8} % | "
	hmsg += f"{'gain_loss':^14} | "
	hmsg += f"{'gain_loss_high':^14}"

	title = 'Currently Open Positions - By Age Desc'
	show_pos_close_header_yn = 'Y'
	if show_pos_close_header_yn == 'Y':
		print(len(hmsg))
		chart_top(in_str=title, len_cnt=len(hmsg), align='center')
		chart_headers(in_str=hmsg, len_cnt=len(hmsg), align='center')
		chart_mid(len_cnt=len(hmsg))
		show_pos_close_header_yn = 'N'

#	poss = db_poss_open_get()
	if poss:
		poss_sorted = sorted(poss, key=lambda x: x["age_mins"], reverse=True)
		poss = poss_sorted

		for pos in poss:
			pos = dec_2_float(pos)
			pos = AttrDictConv(in_dict=pos)
			pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
			disp_age = format_disp_age(pos.age_mins)

			msg = ''
			msg += f'{pos.prod_id:<16} | '
			msg += f'{pos.pos_id:^6} | '
			msg += f'{pos.buy_strat_name:>10} | '
			msg += f'{pos.buy_strat_freq:>10} | '
			msg += f'{disp_age:>10} | '
			msg += f"{pos.pos_begin_dttm:>16} | "
#			msg += f'$ {pos.val_tot:>14.8f} | '
			msg += f'$ {pos.tot_out_cnt:>14.8f} | '
			msg += f'{pos.prc_buy:>14.8f} | '
			msg += f'{pos.prc_curr:>14.8f} | '
			msg += f'{pos.prc_high:>14.8f} | '
			msg += f'{pos.gain_loss_pct:>8.2f} % | '
			msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
#			msg += f'{pos.gain_loss_pct_est_low:>8.2f} % | '
			msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
			msg += f'{pos.gain_loss_amt:>14.8f} | '
			msg += f'{pos.gain_loss_amt_est_high:>14.8f}'

			msg = cs_pct_color(pos.prc_chg_pct, msg)
			chart_row(in_str=msg, len_cnt=len(hmsg))

	func_end(fnc)

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
