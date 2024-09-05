#<=====>#
# Import All Scope
#<=====>#
import_all_func_list = []
import_all_func_list.append("calc_chg_pct")
import_all_func_list.append("cb_buy_base_size_calc")
import_all_func_list.append("cb_sell_base_size_calc")
import_all_func_list.append("trade_perf_get")
import_all_func_list.append("trade_strat_perf_get")
import_all_func_list.append("freqs_get")
import_all_func_list.append("prt_cols")
import_all_func_list.append("writeit")
import_all_func_list.append("json_load")
import_all_func_list.append("json_write")
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
import json
import os
import pandas as pd 
import sys
import time
import warnings
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

#from cls_AttrDict                      import *
#from cls_db_mysql                      import db_mysql
#from cls_settings                      import Settings

from lib_common                        import *
from lib_colors                        import cs, cp

#from lib_common                        import EmptyObject

from bot_db_read                       import *
from bot_settings                      import settings
#from bot_theme                         import *

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_common'
log_name      = 'bot_common'
lib_verbosity = 0
lib_debug_lvl = 0
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

#<=====>#

def calc_chg_pct(old_val, new_val, dec_prec=2):
	func_name = 'calc_chg_pct'
	func_str = f'{lib_name}.{func_name}(old_val={old_val}, new_val={new_val}, dec_prec={dec_prec})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	chg_pct = round((((new_val - old_val) / old_val) * 100), dec_prec)

	func_end(fnc)
	return chg_pct

#<=====>#

# buy limit orders
def cb_buy_base_size_calc(buy_prc, spend_amt, base_size_incr, base_size_min, base_size_max):
	func_name = 'cb_buy_base_size_calc'
	func_str = f'{lib_name}.{func_name}(buy_prc={buy_prc:>.8f}, spend_amt={spend_amt:>.8f}, base_size_incr={base_size_incr:>.8f}, base_size_min={base_size_min:>.8f}, base_size_max={base_size_max:>.8f}'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	trade_size     = dec(spend_amt) / dec(buy_prc)
	print(f'trade_size : {trade_size:>.8f} passed in...')

	if trade_size < dec(base_size_min):
		print(f'...selling less {trade_size:>.8f} than coinbase allows {base_size_min}...exiting...')
		beep()
		beep()
		beep()
		func_end(fnc)
		return str(0)
	print(f'trade_size : {trade_size:>.8f} after base_size_min {base_size_min:>.8f} check...')

	sell_blocks = int(dec(trade_size) / dec(base_size_incr))
	trade_size = sell_blocks * dec(base_size_incr)
	print(f'trade_size : {trade_size:>.8f} after sell_block {sell_blocks} increments of {base_size_incr:>.8f}...')

	if trade_size > dec(base_size_max):
		trade_size = dec(base_size_max)
	print(f'trade_size : {trade_size:>.8f} after base_size_max {base_size_max:>.8f} check...')

	func_end(fnc)
	return str(trade_size)

#<=====>#

def cb_sell_base_size_calc(sell_cnt, prc_chg_pct, base_size_incr, base_size_min, base_size_max, bal_cnt=0, hold_cnt=0, pocket_pct=0, clip_pct=0):
	func_name = 'cb_sell_base_size_calc'
	func_str = ''
	func_str += f'{lib_name}.{func_name}('
	func_str += f'sell_cnt={sell_cnt:>.8f}, '
	func_str += f'prc_chg_pct={prc_chg_pct:>.8f}, '
	func_str += f'base_size_incr={base_size_incr:>.8f}, '
	func_str += f'base_size_min={base_size_min:>.8f}, '
	func_str += f'base_size_max={base_size_max:>.8f}, '
	func_str += f'bal_cnt={bal_cnt:>.8f}, '
	func_str += f'hold_cnt={hold_cnt:>.8f}, '
	func_str += f'pocket_pct={pocket_pct:>.4f}, '
	func_str += f'clip_pct={clip_pct:>.4f}'
	func_str += ')'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	sell_cnt_max     = dec(sell_cnt)
#	print(f'sell_cnt_max : {sell_cnt_max:>.8f} passed in...')

	if sell_cnt_max > dec(hold_cnt):
		print(f'...selling more {sell_cnt_max:>.8f} than we are position is holding {hold_cnt:>.8f} onto...exiting...')
		beep()
		beep()
		beep()
		func_end(fnc)
		return 0
#	print(f'sell_cnt_max : {sell_cnt_max:>.8f} after hold_cnt check...')

	if sell_cnt_max > dec(bal_cnt):
		print(f'...selling more {sell_cnt_max:>.8f} than we the wallet balance {bal_cnt:>.8f}...exiting...')
		beep()
		beep()
		beep()
		func_end(fnc)
		return 0
#	print(f'sell_cnt_max : {sell_cnt_max:>.8f} after bal_cnt check...')

	if prc_chg_pct > 0 and pocket_pct > 0:
		sell_cnt_max -= sell_cnt_max * (dec(pocket_pct) / 100) * (dec(prc_chg_pct)/100)
#	print(f'sell_cnt_max : {sell_cnt_max:>.8f} after pocket_pct {pocket_pct:>.2f}% calc...')

	if prc_chg_pct < 0 and clip_pct > 0:
		sell_cnt_max -= sell_cnt_max * (dec(clip_pct) / 100) * (abs(dec(prc_chg_pct))/100)
#	print(f'sell_cnt_max : {sell_cnt_max:>.8f} after clip_pct {clip_pct:>.2f}% calc...')

	sell_blocks = int(sell_cnt_max / dec(base_size_incr))
	sell_cnt_max = sell_blocks * dec(base_size_incr)
#	print(f'sell_cnt_max : {sell_cnt_max:>.8f} after sell_block {sell_blocks} increments of {base_size_incr:>.8f}...')

	if sell_cnt_max < dec(base_size_min):
		print(f'...selling less {sell_cnt_max:>.8f} than coinbase allows {base_size_min}...exiting...')
		beep()
		beep()
		beep()
		func_end(fnc)
		return 0
#	print(f'sell_cnt_max : {sell_cnt_max:>.8f} after base_size_min {base_size_min:>.8f} check...')

	if sell_cnt_max > dec(base_size_max):
		sell_cnt_max = dec(base_size_max)
#	print(f'sell_cnt_max : {sell_cnt_max:>.8f} after base_size_max {base_size_max:>.8f} check...')

	sell_cnt = sell_cnt_max

#	print(f'sell_cnt before : {sell_cnt}')
#	prc_dec = cb_mkt_prc_dec_calc(base_size_incr, base_size_incr)
#	sell_cnt = round(sell_cnt, prc_dec)
#	print(f'sell_cnt after  : {sell_cnt}')

	func_end(fnc)
	return sell_cnt

#<=====>#

def trade_perf_get(mkt):
	func_name = 'trade_perf_get'
	func_str = f'{lib_name}.{func_name}(mkt)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	prod_id = mkt.prod_id

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

	tp = db_view_trade_perf_get_by_prod_id(prod_id)
#	print(f'mp : {tp}')
	tp = dec_2_float(tp)
	tp = AttrDictConv(in_dict=tp)

	if tp:
		for k in tp:
			if tp[k]:
				trade_perf[k] = tp[k]

#	print(trade_perf)

	r = db_mkt_elapsed_get(prod_id)
	trade_perf.bo_elapsed   = r[0]
	trade_perf.pos_elapsed  = r[1]
	trade_perf.last_elapsed = r[2]

	open_poss = db_pos_open_get_by_prod_id(prod_id)
	trade_perf.open_poss_cnt = len(open_poss)

	msg = ''
	msg += f'trade_perf => '
	msg += f'bo_elapsed : {trade_perf.bo_elapsed}, '
	msg += f'pos_elapsed : {trade_perf.pos_elapsed}, '
	msg += f'last_elapsed : {trade_perf.last_elapsed}, '
	msg += f'buy_delay_minutes : {mkt.restricts_buy_delay_minutes}'
#	Y(msg)

	func_end(fnc)
	return trade_perf

#<=====>#

def trade_strat_perf_get(mkt, buy_strat_type, buy_strat_name, buy_strat_freq):
	func_name = 'trade_strat_perf_get'
	func_str = f'{lib_name}.{func_name}(mkt, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	st = settings.settings_load()

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
	trade_strat_perf = AttrDictConv(in_dict=trade_strat_perf)

#	print(f'{prod_id:<20}  {buy_strat_name:<30}  {buy_strat_freq:<20}')
	msp = db_trade_strat_perf_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
#	print(type(msp))
#	print(f'msp : {msp}')
	if msp:
		for k in msp:
			if msp[k]:
				trade_strat_perf[k] = msp[k]

	mkt.restricts_buy_strat_delay_minutes = settings.get_ovrd(in_dict=st.spot.buy.buy_strat_delay_minutes, in_key=buy_strat_freq)
	r = db_mkt_strat_elapsed_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
	trade_strat_perf.strat_bo_elapsed   = r[0]
	trade_strat_perf.strat_pos_elapsed  = r[1]
	trade_strat_perf.strat_last_elapsed = r[2]

	msg = ''
	msg += f'trade_strat_perf 1483 => '
	msg += f'strat_bo_elapsed : {trade_strat_perf.strat_bo_elapsed}, '
	msg += f'strat_pos_elapsed : {trade_strat_perf.strat_pos_elapsed}, '
	msg += f'strat_last_elapsed : {trade_strat_perf.strat_last_elapsed}, '
	msg += f'buy_strat_delay_minutes : {mkt.restricts_buy_strat_delay_minutes}, '
	msg += f'buy_strat_name : {buy_strat_name}, '
	msg += f'buy_strat_freq : {buy_strat_freq}'
#	Y(msg)

	func_end(fnc)
	return trade_strat_perf

#<=====>#

def freqs_get(rfreq):
	func_name = 'freqs_get'
	func_str = f'{lib_name}.{func_name}(rfreq={rfreq})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	if rfreq == '1d':
		freqs = ['3min', '5min', '15min', '30min', '1h', '4h', '1d']
		faster_freqs = ['3min', '5min', '15min', '30min', '1h', '4h']
	elif rfreq == '4h':
		freqs = ['3min', '5min', '15min', '30min', '1h', '4h']
		faster_freqs = ['3min', '5min', '15min', '30min', '1h']
	elif rfreq == '1h':
		freqs = ['3min', '5min', '15min', '30min', '1h']
		faster_freqs = ['3min', '5min', '15min', '30min']
	elif rfreq == '30min':
		freqs = ['3min', '5min', '15min', '30min']
		faster_freqs = ['3min', '5min', '15min']
	elif rfreq == '15min':
		freqs = ['3min', '5min', '15min']
		faster_freqs = ['3min', '5min']

	func_end(fnc)
	return freqs, faster_freqs

#<=====>#

def prt_cols(l, cols=10, clr='WoG'):
	func_name = 'prt_cols'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	col_cnt = 0
	s = ''
	for x in l:
		col_cnt += 1
		if clr == 'WoG':
			s += cs(text=f'{x:<15}', font_color='white', bg_color='green')
		elif clr == 'GoW':
			s += cs(text=f'{x:<15}', font_color='green', bg_color='white')
#		print(f'col_cnt : {col_cnt}, col_cnt // 10 : {col_cnt // 10}')
		if col_cnt % cols == 0:
			print(s)
			s = ''
			col_cnt = 0
		elif col_cnt == len(l):
			s += ''
		else:
			s += ' | '
	if col_cnt > 0 and col_cnt < cols:
		print(s)
		print_adv()

	func_end(fnc)

#<=====>#

def writeit(fullfilename, msg):
	dir_val(fullfilename)
	with open(fullfilename, 'a') as fw:
		fw.writelines(msg)
		fw.writelines('\n')
		fw.close()
	return

#<=====>#

def json_load(fname, json_template=None):
	func_name = 'json_load'
	func_str = f'{lib_name}.{func_name}(fname={fname}, json_template)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	data = json_template

	if not json_template: json_template = {}
	if os.path.exists(fname):
		with open(fname, 'r') as f:
			data = json.load(f)
			data = AttrDictConv(in_dict=data)
	else:
		data = AttrDictConv(in_dict=json_template)
		json_write(data, fname)

	func_end(fnc)
	return data

#<=====>#

def json_write(data, fname):
	func_name = 'json_write'
	func_str = f'{lib_name}.{func_name}(data, fname={fname})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	with open(fname, 'w') as f:
		json.dump(data, f, indent=4)

	func_end(fnc)

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#
