#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import json
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_colors import B, G, M, R, BoW, GoW, MoW, RoW, WoB, WoG, WoM, WoR, YoK, cp, cs
from libs.lib_common import AttrDictConv, beep, dec, func_begin, func_end, print_adv, dir_val
import os


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_common'
log_name      = 'bot_common'


# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def calc_chg_pct(old_val, new_val, dec_prec=2):
	func_name = 'calc_chg_pct'
	func_str = f'{lib_name}.{func_name}(old_val={old_val}, new_val={new_val}, dec_prec={dec_prec})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	chg_pct = round((((new_val - old_val) / old_val) * 100), dec_prec)

	func_end(fnc)
	return chg_pct

#<=====>#

# buy limit orders
def cb_buy_base_size_calc(buy_prc, spend_amt, base_size_incr, base_size_min, base_size_max):
	func_name = 'cb_buy_base_size_calc'
	func_str = f'{lib_name}.{func_name}(buy_prc={buy_prc:>.8f}, spend_amt={spend_amt:>.8f}, base_size_incr={base_size_incr:>.8f}, base_size_min={base_size_min:>.8f}, base_size_max={base_size_max:>.8f}'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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

def freqs_get(rfreq):
	func_name = 'freqs_get'
	func_str = f'{lib_name}.{func_name}(rfreq={rfreq})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	if rfreq == '1d':
		freqs = ['5min', '15min', '30min', '1h', '4h', '1d']
		faster_freqs = ['5min', '15min', '30min', '1h', '4h']
	elif rfreq == '4h':
		freqs = ['5min', '15min', '30min', '1h', '4h']
		faster_freqs = ['5min', '15min', '30min', '1h']
	elif rfreq == '1h':
		freqs = ['5min', '15min', '30min', '1h']
		faster_freqs = ['5min', '15min', '30min']
	elif rfreq == '30min':
		freqs = ['5min', '15min', '30min']
		faster_freqs = ['5min', '15min']
	elif rfreq == '15min':
		freqs = ['5min', '15min']
		faster_freqs = ['5min']

	func_end(fnc)
	return freqs, faster_freqs

#<=====>#

def prt_cols(l, cols=10, clr='WoG'):
	func_name = 'prt_cols'
	func_str = f'{lib_name}.{func_name}()'
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
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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
