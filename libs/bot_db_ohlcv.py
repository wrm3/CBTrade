#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from datetime import datetime, timedelta
import time
import sqlparse
import os
import re
import traceback
from dotenv import load_dotenv

from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.cls_db_mysql import db_mysql
from libs.lib_common import func_begin, func_end, print_func_name
from libs.lib_colors import G, B
from libs.lib_common import dttm_get, beep

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_db_ohlcv'
log_name      = 'bot_db_ohlcv'


# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)

# Load environment variables from .env file
load_dotenv()
# Access environment variables
db_host = os.getenv('DB_OHLCV_HOST')
db_port = os.getenv('DB_OHLCV_PORT')
db_name = os.getenv('DB_OHLCV_NAME')
db_user = os.getenv('DB_OHLCV_USER')
db_pw   = os.getenv('DB_OHLCV_PW')

#print(db_host, '-', db_port, '-', db_name, '-', db_user, '-', db_pw)

db_ohlcv = db_mysql(db_host=db_host, db_port=int(db_port), db_name=db_name, db_user=db_user, db_pw=db_pw)


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

def db_tbl_del(table_name):
	sql = "delete from {} ".format(table_name)
	db_ohlcv.execute(sql)

#<=====>#

def db_tbl_insupd(table_name, in_data, rat_on_extra_cols_yn='N', exit_on_error=True):
	func_name = 'db_tbl_insupd'
	func_str = '{}.{}(table_name={}, in_data)'.format(lib_name, func_name, table_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	tbl_cols  = db_ohlcv.table_cols(table=table_name)
	data_cols = []
	ins_data  = []


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
						if k not in data_cols:
							if k in tbl_cols:
								data_cols.append(k)
							else:
								if table_name not in ('currs'):
									if rat_on_extra_cols_yn == 'Y':
										print('column : {} not defined in table {}...'.format(k, table_name))
				# looping through data to standardize for inserts
				for r in in_data:
					ins_dict = {}
					# prepopulate with None, which will become null 
					for k in data_cols: ins_dict[k] = None
					# assign actual values from data when present
					for k in r:
						if k in tbl_cols:
							ins_dict[k] = r[k]
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
		db_ohlcv.ins_one(sql=sql, vals=ins_data, exit_on_error=exit_on_error)
	else:
		db_ohlcv.ins_many(sql=sql, vals=ins_data, exit_on_error=exit_on_error)

	func_end(fnc)

#<=====>#

def db_ohlcv_prod_id_freqs(prod_id):
	func_name = 'db_ohlcv_prod_id_freqs'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = prod_id.replace('-','_')

	sql = ""
	sql += "select distinct x.freq "
	sql += "  , max(start_dttm) as last_start_dttm "
	sql += f"  from ohlcv_{prod_id} x "
	sql += "  where 1=1 "
	sql += "  group by x.freq "

	last_dttms = db_ohlcv.seld(sql)

	if not last_dttms:
		last_dttms = {}

	func_end(fnc)
	return last_dttms

#<=====>#

def db_ohlcv_freq_get(prod_id, freq, lmt=300):
	func_name = 'db_ohlcv_freq_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, freq={freq})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = prod_id.replace('-','_')

	sql = ""
	sql += "select * "
	sql += f"  from ohlcv_{prod_id} x "
	sql += f"  where freq = '{freq}' "
	sql += "   order by x.timestamp desc "
	sql += f"  limit {lmt} "

	ohlcv = db_ohlcv.seld(sql)

	if ohlcv:
		newest_timestamp = ohlcv[0]['timestamp']
		oldest_timestamp  = ohlcv[-1]['timestamp']
		newest = ohlcv[0]
		oldest = ohlcv[-1]
#		G(f'found {len(ohlcv)} rows for {prod_id}, freq : {freq}, newest : {newest_timestamp}, oldest : {oldest_timestamp}...')
#	print(newest)
#	print(oldest)
	elif not ohlcv:
		ohlcv = []

	func_end(fnc)
	return ohlcv

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

	db_ohlcv.execute(sql)

#<=====>#

def db_check_ohlcv_prod_id_table(prod_id):
	func_name = f'db_check_ohlcv_prod_id_table({prod_id})'
#	G(func_name)

	prod_id = prod_id.replace('-','_')

	sql = ""
	sql += "create table if not exists "
	sql += f" ohlcv.ohlcv_{prod_id} ("
	sql += "    timestamp   timestamp "
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
	sql += "  , INDEX idx_freq_timestamp (freq, timestamp DESC)"
	sql += "  )"
	db_ohlcv.execute(sql)

	time.sleep(0.05)


#<=====>#

def db_tbl_ohlcv_prod_id_insupd(prod_id, freq, in_df):
	func_name = 'db_tbl_ohlcv_prod_id_insupd'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, freq={freq}, in_df)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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

	try:
		db_tbl_insupd(table_name, in_data, exit_on_error=False)
	except Exception as e:
		print(f'{lib_name}.{func_str}')
		print(f'{func_name} ==> errored... {e}')
		print(dttm_get())
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		beep()

	func_end(fnc)

#<=====>#

def db_tbl_ohlcv_prod_id_insupd_many(prod_id, in_dfs):
	func_name = 'db_tbl_ohlcv_prod_id_insupd_many'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, in_df)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = prod_id.replace('-','_')

	all_data = []

	for rfreq in in_dfs:
		msg = f'inserting into ohlcv {prod_id} {rfreq}'
#		G(msg)

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

	try:
		table_name = f'ohlcv_{prod_id}'
		db_tbl_insupd(table_name, all_data, exit_on_error=False)
	except Exception as e:
		print(f'{lib_name}.{func_str}')
		print(f'{func_name} ==> errored... {e}')
		print(dttm_get())
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		beep()

	func_end(fnc)

#<=====>#

def db_ohlcv_dump(prod_id, freq='1min'):
	func_name = 'db_ohlcv_dump'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, freq={freq})'
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=6)
#	G(func_str)

	import pandas as pd
	from libs.lib_common import dir_val

	temp_prod_id = prod_id.replace('-','_')

	table_name = f"ohlcv.ohlcv_{temp_prod_id}"

	sql = ""
	sql += f"select timestamp, freq, open, high, low, close, volume, start_dttm, end_dttm, upd_dttm, dlm "
	sql += f"  from {table_name}"
	sql += f"  where freq = '{freq}'"
	print(sql)
	res = db_ohlcv.seld(sql)
	df = pd.DataFrame(res)
	csv_fname = f'ohlcv/{table_name}_table.csv'
	dir_val(csv_fname)
	df.to_csv(csv_fname, index=True)
	print(f'{csv_fname:<60} saved...')

	func_end(fnc)

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
