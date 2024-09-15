#<=====>#
# Description
#<=====>#


#<=====>#
# Import All
#<=====>#
import_all_func_list = []

import_all_func_list.append("db_check_ohlcv_prod_id_piano")
import_all_func_list.append("db_check_ohlcv_prod_id_table")
import_all_func_list.append("db_tbl_ohlcv_prod_id_insupd")
import_all_func_list.append("db_tbl_ohlcv_prod_id_insupd_many")

import_all_func_list.append("db_safe_string")
import_all_func_list.append("db_curr_prc_mkt_upd")
import_all_func_list.append("db_curr_prc_stable_upd")
import_all_func_list.append("db_curr_prc_upd")
import_all_func_list.append("db_buy_ords_stat_upd")
import_all_func_list.append("db_poss_err_upd")
import_all_func_list.append("db_poss_stat_upd")
import_all_func_list.append("db_sell_ords_stat_upd")

import_all_func_list.append("db_poss_check_mkt_dttm_upd")
import_all_func_list.append("db_poss_check_last_dttm_upd")

import_all_func_list.append("db_tbl_del")
import_all_func_list.append("db_tbl_insupd")
import_all_func_list.append("db_tbl_bals_insupd")
import_all_func_list.append("db_tbl_buy_ords_insupd")
import_all_func_list.append("db_tbl_buy_signs_insupd")
import_all_func_list.append("db_tbl_buy_signals_insupd")
import_all_func_list.append("db_tbl_currs_insupd")
import_all_func_list.append("db_tbl_mkts_insupd")
import_all_func_list.append("db_tbl_ords_insupd")
import_all_func_list.append("db_tbl_poss_insupd")
import_all_func_list.append("db_tbl_sell_signs_insupd")
import_all_func_list.append("db_tbl_sell_signals_insupd")
import_all_func_list.append("db_tbl_sell_ords_insupd")
import_all_func_list.append("db_table_csvs_dump")
__all__ = import_all_func_list

#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Common Modules
#<=====>#
import pandas as pd
import sys
import os
import re
import time
from datetime import timedelta
from datetime import datetime as dt
import sqlparse


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

from cls_db_mysql                  import db_mysql
from lib_common                    import *
from lib_colors                    import *
from lib_strings                   import *

#from bot_common                    import *
from bot_db_read                   import *
from bot_secrets                   import secrets

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_db_write'
log_name      = 'bot_db_write'
lib_verbosity = 1
lib_debug_lvl = 1
verbosity     = 1
debug_lvl     = 1
lib_secs_max  = 0.5
lib_secs_max  = 0.5

#<=====>#
# Assignments Pre
#<=====>#

sc = secrets.settings_load()
db = db_mysql(sc.mysql.host, sc.mysql.port, sc.mysql.db, sc.mysql.user, sc.mysql.pw)

#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def db_safe_string(in_str):
	# Regular expression pattern to match allowed characters
	allowed_chars_pattern = r"[^a-zA-Z0-9\s\.,;:'\"?!@#\$%\^&\*\(\)_\+\-=\[\]\{\}<>\/\\]"
	# Replace characters not in the allowed set with an empty string
	out_str = re.sub(allowed_chars_pattern, '', in_str)
	return out_str

#<=====>#

def db_poss_check_mkt_dttm_upd(prod_id):
	func_name = 'db_poss_check_mkt_dttm_upd'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "update cbtrade.poss p "
	sql += "  set p.check_mkt_dttm = NOW() "
	sql += "  where p.pos_stat in ('OPEN')"
	sql += f"  and p.prod_id = '{prod_id}'"
	db.execute(sql)

	func_end(fnc)

#<=====>#

def db_poss_check_last_dttm_upd(pos_id):
	func_name = 'db_poss_check_last_dttm_upd'
	func_str = f'{lib_name}.{func_name}(pos_id={pos_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "update cbtrade.poss p "
	sql += "  set p.check_last_dttm = NOW() "
	sql += f"  where p.pos_id = {pos_id}"
	db.execute(sql)

	func_end(fnc)

#<=====>#

# def db_check_ohlcv_prod_id_freqs_table(prod_id, freq):
# 	func_name = 'db_check_ohlcv_prod_id_freqs_table'
# 	G(func_name)


# 	sql = ''
# 	sql += 'create table if not exists ohlcv_prod_id_freqs ('
# 	sql += '    prod_id           varchar(64) '
# 	sql += '  , freq              varchar(64) '
# 	sql += '  , last_start_dttm   timestamp default current_timestamp '
# 	sql += '  , dlm               timestamp default current_timestamp on update current_timestamp '
# 	sql += ');'

# 	db.execute(sql)

#<=====>#

def db_check_ohlcv_prod_id_piano(prod_id, in_data):
	func_name = 'db_check_ohlcv_prod_id_piano'
#	G(func_name)

#	freqs = ['1min','3min','5min','15min','30min','1h','4h','1d']
	freqs = ['1min','5min','15min','30min','1h','4h','1d']

	sql = ''
	sql += 'create table if not exists '
	sql += f'ohlcv_{prod_id}_piano('
	sql += '    prod_id     varchar(64) '
	for freq in freqs:
		sql += '  , timestamp   timestamp '
		sql += '  , freq_{freq}        varchar(64) '
		sql += '  , open_{freq}        decimal(36, 12) '
		sql += '  , high_{freq}        decimal(36, 12) '
		sql += '  , low_{freq}         decimal(36, 12) '
		sql += '  , close_{freq}       decimal(36, 12) '
		sql += '  , volume_{freq}      decimal(36, 12) '
		sql += '  , start_dttm_{freq}  timestamp, '
		sql += '  , end_dttm_{freq}    timestamp '
	sql += '  , upd_dttm    timestamp '
	sql += '  , dlm         timestamp default current_timestamp on update current_timestamp '                              
	sql += ');'

	db.execute(sql)

#<=====>#

def db_check_ohlcv_prod_id_table(prod_id):
	func_name = 'db_check_ohlcv_prod_id_table'
#	G(func_name)

	prod_id = prod_id.replace('-','_')

	sql = ""
	sql += "create table if not exists "
	sql += f"ohlcv_{prod_id} ("
	sql += "  timestamp     timestamp "
	sql += "  , freq        varchar(64) "
	sql += "  , open        decimal(36, 12) "
	sql += "  , high        decimal(36, 12) "
	sql += "  , low         decimal(36, 12) "
	sql += "  , close       decimal(36, 12) "
	sql += "  , volume      decimal(36, 12) "
	sql += "  , start_dttm  timestamp "
	sql += "  , end_dttm    timestamp "
	sql += "  , upd_dttm    timestamp default current_timestamp on update current_timestamp "
	sql += "  , dlm         timestamp default current_timestamp on update current_timestamp "
	sql += "  , unique(timestamp, freq) "
	sql += "  )"
#	print(sql)
	db.execute(sql)
	time.sleep(0.05)


#<=====>#

def db_tbl_ohlcv_prod_id_insupd(prod_id, freq, in_df):
	func_name = 'db_tbl_ohlcv_prod_id_insupd'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, freq={freq}, in_df)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()

	prod_id = prod_id.replace('-','_')

	in_df['freq'] = freq

	in_df['start_dttm'] = in_df.index
	if freq == '1min':
		in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=59) 
#	elif freq == '3min':
#		in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=179) 
	elif freq == '5min':
		in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=299) 
	elif freq == '15min':
		in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=899) 
	elif freq == '30min':
		in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=1799) 
	elif freq == '1h':
		in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=3599) 
	elif freq == '4h':
		in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=14399) 
	elif freq == '1d':
		in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=86399) 

	in_data = in_df.reset_index().rename(columns={'index': 'timestamp'}).to_dict(orient='records')

	table_name = f'ohlcv_{prod_id}'
	db_tbl_insupd(table_name, in_data)

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	msg = cs(f'{func_str} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
#	print(msg)

	func_end(fnc)

#<=====>#

def db_tbl_ohlcv_prod_id_insupd_many(prod_id, in_dfs):
	func_name = 'db_tbl_ohlcv_prod_id_insupd_many'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, in_df)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	t0 = time.perf_counter()

	prod_id = prod_id.replace('-','_')

	all_data = []

	for rfreq in in_dfs:
		in_df = in_dfs[rfreq] 

		in_df['freq'] = rfreq

		in_df['start_dttm'] = in_df.index
		if rfreq == '1min':
			in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=59) 
#		elif rfreq == '3min':
#			in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=179) 
		elif rfreq == '5min':
			in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=299) 
		elif rfreq == '15min':
			in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=899) 
		elif rfreq == '30min':
			in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=1799) 
		elif rfreq == '1h':
			in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=3599) 
		elif rfreq == '4h':
			in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=14399) 
		elif rfreq == '1d':
			in_df['end_dttm'] = in_df['start_dttm'] + timedelta(seconds=86399) 

		in_data = in_df.reset_index().rename(columns={'index': 'timestamp'}).to_dict(orient='records')
		all_data.extend(in_data)

	table_name = f'ohlcv_{prod_id}'
	db_tbl_insupd(table_name, all_data)

#	t1 = time.perf_counter()
#	secs = round(t1 - t0, 2)
#	msg = cs(f'{func_str} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
#	print(msg)

	func_end(fnc)

#<=====>#

def db_curr_prc_upd(prc_usd, symb):
	func_name = 'db_curr_prc_upd'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "update cbtrade.currs c"
	sql += "  set c.prc_usd = {} ".format(prc_usd)
	sql += "  where c.symb = '{}' ".format(symb)
	db.execute(sql)

	func_end(fnc)

#<=====>#

def db_curr_prc_stable_upd(stable_symbs=None):
	func_name = 'db_curr_prc_stable_upd'
	func_str = '{}.{}(stable_symbs={})'.format(lib_name, func_name, stable_symbs)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	if stable_symbs:
		if not isinstance(stable_symbs, list):
			stable_symbs = [stable_symbs]
	else:
		stable_symbs = []

	if isinstance(stable_symbs, list):
		stable_symbs.append('USD')
		stable_symbs.append('USDC')
		stable_symbs = list(set(stable_symbs))

	stable_symbs_str = "'" + "', '".join(stable_symbs) + "'"

	sql = ""
	sql += "update cbtrade.currs c "
	sql += "  set c.prc_usd = 1 "
	sql += "  where c.symb in ({}) ".format(stable_symbs_str)
	db.execute(sql)

	func_end(fnc)

#<=====>#

def db_curr_prc_mkt_upd():
	func_name = 'db_curr_prc_mkt_upd'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "update cbtrade.currs c "
	sql += "  set c.prc_usd = coalesce((select m.prc"
	sql += "                              from cbtrade.mkts m "
	sql += "                              where m.base_curr_symb = c.symb"
	sql += "                              and m.quote_curr_symb = 'USDC'),0)"
	db.execute(sql)

	func_end(fnc)

#<=====>#

def db_buy_ords_stat_upd(bo_id, ord_stat):
	func_name = 'db_buy_ords_stat_upd'
	func_str = '{}.{}(bo_id={}, ord_stat={})'.format(lib_name, func_name, bo_id, ord_stat)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = "update buy_ords set ord_stat = '{}' where bo_id = {}".format(ord_stat, bo_id)
	db.execute(sql)

	func_end(fnc)

#<=====>#

def db_poss_err_upd(pos_id, pos_stat):
	func_name = 'db_poss_err_upd'
	func_str = '{}.{}(pos_id={})'.format(lib_name, func_name, pos_id)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = "update poss set pos_stat = '{}' where pos_id = {}".format(pos_stat, pos_id)
	db.execute(sql)

	func_end(fnc)

#<=====>#

def db_poss_stat_upd(pos_id, pos_stat):
	func_name = 'db_poss_stat_upd'
	func_str = '{}.{}(pos_id={})'.format(lib_name, func_name, pos_id)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = "update poss set pos_stat = '{}' where pos_id = {}".format(pos_stat, pos_id)
	db.execute(sql)

	func_end(fnc)

#<=====>#

def db_sell_ords_stat_upd(so_id, ord_stat):
	func_name = 'db_sell_ords_stat_upd'
	func_str = '{}.{}(so_id={}, ord_stat={})'.format(lib_name, func_name, so_id, ord_stat)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = "update sell_ords set ord_stat = '{}' where so_id = {}".format(ord_stat, so_id)
	db.execute(sql)

	func_end(fnc)

#<=====>#

def db_tbl_del(table_name):
	sql = "delete from {} ".format(table_name)
	db.execute(sql)

#<=====>#

def db_tbl_insupd(table_name, in_data, rat_on_extra_cols_yn='N'):
	func_name = 'db_tbl_insupd'
	func_str = '{}.{}(table_name={}, in_data)'.format(lib_name, func_name, table_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

#	if table_name == 'mkts':
#		print('len(in_data)  : {}'.format(len(in_data)))
#		print('type(in_data) : {}'.format(type(in_data)))

	tbl_cols = db.table_cols(table=table_name)
	data_cols = []
	ins_data = []

	if isinstance(in_data, dict):
		if in_data:
			ins_type = 'one'
			if 'add_dttm' in in_data: del in_data['add_dttm']
			if 'dlm' in in_data: del in_data['dlm']
			for k in in_data:
				if k in tbl_cols:
					data_cols.append(k)
			for k in in_data:
				if k in tbl_cols:
					ins_data.append(in_data[k])
				else:
					if rat_on_extra_cols_yn == 'Y':
						print('column : {} not defined in table {}...'.format(k, table_name))

	# received a list of dictionaries
	elif isinstance(in_data, list):
#		for k in in_data[0]:
#			print('table: {}, data column : {}'.format(table_name, k))
		ins_data = []
		if in_data:
			if isinstance(in_data[0], dict):
				ins_type = 'many'
				# populating data_cols with all the distinct columns names 
				# from data and checking against table
				for r in in_data:
					if 'add_dttm' in in_data: del r['add_dttm']
					if 'dlm' in in_data: del r['dlm']
					for k in r:
#						print('table: {}, data column : {}'.format(table_name, k))
						if k not in data_cols:
							if k in tbl_cols:
								data_cols.append(k)
							else:
								if table_name not in ('currs'):
									if rat_on_extra_cols_yn == 'Y':
										print('column : {} not defined in table {}...'.format(k, table_name))
#				print('table : {}, tbl_cols  : {}'.format(table_name, tbl_cols))
#				print('table : {}, data_cols : {}'.format(table_name, data_cols))
				# looping through data to standardize for inserts
				for r in in_data:
					ins_dict = {}
					# prepopulate with None, which will become null 
					for k in data_cols: ins_dict[k] = None
					# assign actual values from data when present
					for k in r:
						if k in tbl_cols:
							ins_dict[k] = r[k]
#							if r[k]:
#								ins_dict[k] = r[k]
					# preparing list of the dict values for the insert
					ins_list = []
					for k in data_cols:
						ins_list.append(ins_dict[k])
					# adding the row list to the big list for inserts
					ins_data.append(ins_list)

	sql1 = " insert into {} ( ".format(table_name)

	sql2 = ", ".join(data_cols)

	sql3 = " ) values ( "

	sql4 = ', '.join(['%s'] * len(data_cols))

	sql5 = " ) on duplicate key update  "

	col1 = data_cols[0]
	sql6 = ' {} = values({})'.format(col1, col1)
	for col in data_cols:
		if col != col1:
			sql6 += ', {} = values({})'.format(col, col)

	sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6


	if table_name == 'mkts' and ins_type == 'one':
		print(f'sql  :')
		formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
		print(formatted_sql)
		print(f'vals : {ins_data}')

	if ins_type == 'one':
		db.ins_one(sql=sql, vals=ins_data)
	else:
		db.ins_many(sql=sql, vals=ins_data)

#	print(sql)

	func_end(fnc)

#<=====>#

def db_tbl_bals_insupd(in_data):
	func_name = 'db_tbl_bals_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'bals'
	db_tbl_del(table_name=table_name)
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_buy_ords_insupd(in_data):
	func_name = 'db_tbl_buy_ords_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'buy_ords'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_buy_signs_insupd(in_data):
	func_name = 'db_tbl_buy_signs_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'buy_signs'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_buy_signals_insupd(in_data):
	func_name = 'db_tbl_buy_signals_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'buy_signals'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_currs_insupd(in_data):
	func_name = 'db_tbl_currs_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'currs'
	db_tbl_del(table_name=table_name)
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_mkts_insupd(in_data):
	func_name = 'db_tbl_mkts_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

# 	rem_cols = []
# 	rem_cols.append('buy_yn')
# 	rem_cols.append('buy_deny_yn')
# 	rem_cols.append('wait_yn')
# 	rem_cols.append('age_hours')
# 	rem_cols.append('age_mins')
# 	rem_cols.append('buy_cnt')
# 	rem_cols.append('buy_delay_minutes')
# 	rem_cols.append('buy_diff_pct')
# 	rem_cols.append('buy_fees_cnt')
# 	rem_cols.append('trade_size')
# 	rem_cols.append('buy_strat_delay_minutes')
# 	rem_cols.append('buy_strat_freq')
# 	rem_cols.append('buy_strat_name')
# 	rem_cols.append('buy_strat_type')
# 	rem_cols.append('clip_cnt')
# 	rem_cols.append('dfs')
# 	rem_cols.append('bal_avail')
# 	rem_cols.append('reserve_amt')
# 	rem_cols.append('spendable_amt')
# 	rem_cols.append('buy_strat_freq')
# 	rem_cols.append('buy_strat_name')
# 	rem_cols.append('buy_strat_type')
# 	rem_cols.append('cnt')
# 	rem_cols.append('dfs')
# 	rem_cols.append('mkt_strat')
# 	rem_cols.append('mkts_tot')
# 	rem_cols.append('pricing')
# 	rem_cols.append('restricts')
# 	rem_cols.append('strats_available')
# 	rem_cols.append('test_tf')
# 	rem_cols.append('trade_perf')
# 	rem_cols.append('trade_strat_perf')
# 	rem_cols.append('trade_strat_perfs')
# 	rem_cols.append('trade_size')
# 	rem_cols.append('age_hours')
# 	rem_cols.append('age_mins')
# 	rem_cols.append('buy_cnt')
# 	rem_cols.append('buy_delay_minutes')
# 	rem_cols.append('buy_diff_pct')
# 	rem_cols.append('buy_fees_cnt')
# 	rem_cols.append('trade_size')
# 	rem_cols.append('buy_strat_delay_minutes')
# 	rem_cols.append('clip_cnt')
# 	rem_cols.append('dfs')
# 	rem_cols.append('fees_cnt_tot')
# 	rem_cols.append('gain_loss_amt')
# 	rem_cols.append('gain_loss_amt_net')
# 	rem_cols.append('gain_loss_pct')
# 	rem_cols.append('gain_loss_pct_hr')
# 	rem_cols.append('hold_cnt')
# 	rem_cols.append('lose_amt')
# 	rem_cols.append('lose_cnt')
# 	rem_cols.append('lose_pct')
# 	rem_cols.append('open_poss_cnt')
# 	rem_cols.append('open_poss_cnt_max')
# 	rem_cols.append('pocket_cnt')
# 	rem_cols.append('prc_dec')
# 	rem_cols.append('prc_range_pct')
# 	rem_cols.append('sell_cnt_tot')
# 	rem_cols.append('sell_diff_pct')
# 	rem_cols.append('sell_fees_cnt_tot')
# 	rem_cols.append('sell_order_attempt_cnt')
# 	rem_cols.append('sell_order_cnt')
# 	rem_cols.append('strat_open_cnt_max')
# 	rem_cols.append('strat_sha_yn')
# 	rem_cols.append('strat_imp_macd_yn')
# 	rem_cols.append('strat_emax_yn')
# 	rem_cols.append('strat_drop_yn')
# 	rem_cols.append('strat_bb_bo_yn')
# 	rem_cols.append('strat_bb_yn')
# 	rem_cols.append('test_tf')
# 	rem_cols.append('tot_cnt')
# 	rem_cols.append('tot_in_cnt')
# 	rem_cols.append('tot_out_cnt')
# 	rem_cols.append('val_curr')
# 	rem_cols.append('val_tot')
# 	rem_cols.append('win_amt')
# 	rem_cols.append('win_cnt')
# 	rem_cols.append('win_pct')
# 	rem_cols.append('cnt')
# 	rem_cols.append('mkts_tot')
# 	rem_cols.append('prc_mkt')
# 	rem_cols.append('prc_buy_diff_pct')
# 	rem_cols.append('prc_sell_diff_pct')
# 	rem_cols.append('restricts_open_poss_cnt_max')
# 	rem_cols.append('restricts_strat_open_cnt_max')
# 	rem_cols.append('restricts_buy_delay_minutes')
# 	rem_cols.append('restricts_buy_strat_delay_minutes')

# 	for k in rem_cols:
# 		if k in mkt:
# #			print('removing column : {}'.format(k))	
# 			del mkt[k]

	table_name = 'mkts'
	# I like deleting this just in case old products have been dropped
	# however I need to leave add_dttm as is, since coinbase does not 
	# have a listing data.  If the coin has not been listed long, we
	# cannot pull OHLCV data.  So I am filtering on add_dttm from this
	# table, meaning I can't delete before repopulating...
#	db_tbl_del(table_name=table_name)
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_ords_insupd(in_data):
	func_name = 'db_tbl_ords_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'ords'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_poss_insupd(in_data):
	func_name = 'db_tbl_poss_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	rem_cols = []	
	rem_cols.append('sell_yn')
	rem_cols.append('sell_block_yn')
	rem_cols.append('hodl_yn')
	for k in rem_cols:
		if k in in_data:
			del in_data[k]

	table_name = 'poss'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_sell_ords_insupd(in_data):
	func_name = 'db_tbl_sell_ords_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'sell_ords'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_sell_signs_insupd(in_data):
	func_name = 'db_tbl_sell_signs_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'sell_signs'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_tbl_sell_signals_insupd(in_data):
	func_name = 'db_tbl_sell_signals_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	table_name = 'sell_signals'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc)

#<=====>#

def db_table_csvs_dump():
	func_name = 'db_table_csvs_dump'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	tbls_list = db_table_names_get()
	tbls_exclude_list = []
	print('')
	for tbl in tbls_list:
		if tbl not in tbls_exclude_list and left(tbl,5) != 'ohlcv':
			sql = "select * from {}".format(tbl)
			res = db.seld(sql)
			df = pd.DataFrame(res)
			csv_fname = 'csvs/{}_table.csv'.format(tbl)
			dir_val(csv_fname)
			df.to_csv(csv_fname, index=True)
			print('{} saved...'.format(csv_fname))
	print('')

	func_end(fnc)

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#
