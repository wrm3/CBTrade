#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from dotenv import load_dotenv
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.cls_db_mysql import db_mysql
from libs.lib_common import func_begin, func_end, print_func_name
import sqlparse
import os
import re
from libs.lib_colors import G


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_db_read'
log_name      = 'bot_db_read'


# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)

# Load environment variables from .env file
load_dotenv()
# Access environment variables
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_pw   = os.getenv('DB_PW')

db = db_mysql(db_host=db_host, db_port=int(db_port), db_name=db_name, db_user=db_user, db_pw=db_pw)


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

def db_tbl_insupd(table_name, in_data, rat_on_extra_cols_yn='N', exit_on_error=True):
	func_name = 'db_tbl_insupd'
	func_str = '{}.{}(table_name={}, in_data)'.format(lib_name, func_name, table_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	tbl_cols  = db.table_cols(table=table_name)
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
		db.ins_one(sql=sql, vals=ins_data, exit_on_error=exit_on_error)
	else:
		db.ins_many(sql=sql, vals=ins_data, exit_on_error=exit_on_error)

	func_end(fnc)

#<=====>#

def db_mkt_checks_insupd(d):
	func_name = 'db_mkt_checks_insupd'
	func_str = f'{lib_name}.{func_name}(d)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	db_tbl_insupd(table_name='mkt_checks', in_data=d)

	func_end(fnc)

#<=====>#

def db_buy_check_get(prod_id):
	func_name = 'db_buy_check_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select mc.buy_check_dttm, mc.buy_check_guid, TIMESTAMPDIFF(MINUTE, mc.buy_check_dttm, NOW()) as elapsed "
	sql += f"  from cbtrade.mkt_checks mc "
	sql += f"  where mc.prod_id = '{prod_id}'"
	buy_check_dttm = db.sel(sql)

	if not buy_check_dttm:
		d = {}
		d['prod_id'] = prod_id
		db_mkt_checks_insupd(d)
		buy_check_dttm = db.sel(sql)
#		print(buy_check_dttm)

#	print(buy_check_dttm)
	func_end(fnc)
	return buy_check_dttm

#<=====>#

def db_sell_check_get(prod_id):
	func_name = 'db_sell_check_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select mc.sell_check_dttm, mc.sell_check_guid, TIMESTAMPDIFF(MINUTE, mc.sell_check_dttm, NOW()) as elapsed "
	sql += f"  from cbtrade.mkt_checks mc "
	sql += f"  where mc.prod_id = '{prod_id}'"
	sell_check_dttm = db.sel(sql)

	if not sell_check_dttm:
		d = {}
		d['prod_id'] = prod_id
		db_mkt_checks_insupd(d)
		sell_check_dttm = db.sel(sql)
#		print(sell_check_dttm)

#	print(sell_check_dttm)
	func_end(fnc)
	return sell_check_dttm

#<=====>#

def db_poss_check_mkt_dttm_get(prod_id):
	func_name = 'db_poss_check_mkt_dttm_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select max(p.check_mkt_dttm) "
	sql += f"  from cbtrade.poss p "
	sql += f"  where p.prod_id = '{prod_id}'"

	check_mkt_dttm = db.sel(sql)

	func_end(fnc)
	return check_mkt_dttm

#<=====>#

def db_poss_check_last_dttm_get(pos_id):
	func_name = 'db_poss_check_last_dttm_get'
	func_str = f'{lib_name}.{func_name}(pos_id={pos_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select p.check_last_dttm "
	sql += f"  from cbtrade.poss p "
	sql += f"  where p.pos_id = {pos_id}"

	check_last_dttm = db.sel(sql)

	func_end(fnc)
	return check_last_dttm

#<=====>#

def db_bot_spent(quote_curr_symb=None):
	func_name = 'db_bot_spent'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select x.symb "
	sql += "  , x.open_cnt "
	sql += "  , x.open_up_cnt "
	sql += "  , x.open_dn_cnt "
	sql += "  , round((x.open_up_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_up_pct "
	sql += "  , round((x.open_dn_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_dn_pct "
	sql += "  , x.spent_amt "
	sql += "  , x.spent_up_amt "
	sql += "  , x.spent_dn_amt "
	sql += "  , round((x.spent_up_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_up_pct "
	sql += "  , round((x.spent_dn_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_dn_pct "
	sql += "  from ( "
	sql += "select p.quote_curr_symb as symb  "
	sql += "  , p.prod_id "
	sql += "  , count(*) as open_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then 1 else 0 end) as open_up_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then 1 else 0 end) as open_dn_cnt "
	sql += "  , sum(p.tot_out_cnt) as spent_amt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then p.tot_out_cnt else 0 end) as spent_up_amt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then p.tot_out_cnt else 0 end) as spent_dn_amt "
	sql += "  from cbtrade.poss p "
	sql += "  where p.pos_stat in ('OPEN','SELL') "
	sql += "  and p.ignore_tf = 0 "
	sql += "  and p.test_txn_yn = 'N' "
	if quote_curr_symb:
		sql += f"  and p.quote_curr_symb = '{quote_curr_symb}' "
	sql += "  group by p.quote_curr_symb "
	sql += "  ) x "
	sql += "  order by x.symb "

	spent = db.seld(sql)

#	print(sql)
#	print(spent)

#	if not spent:
#		spent = {}

	func_end(fnc)
	return spent

#<=====>#

def db_pair_spent(prod_id=None):
	func_name = 'db_pair_spent'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select x.symb "
	sql += "  , x.prod_id "
	sql += "  , x.open_cnt "
	sql += "  , x.open_up_cnt "
	sql += "  , x.open_dn_cnt "
	sql += "  , round((x.open_up_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_up_pct "
	sql += "  , round((x.open_dn_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_dn_pct "
	sql += "  , x.spent_amt "
	sql += "  , x.spent_up_amt "
	sql += "  , x.spent_dn_amt "
	sql += "  , round((x.spent_up_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_up_pct "
	sql += "  , round((x.spent_dn_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_dn_pct "
	sql += "  from ( "
	sql += "select p.quote_curr_symb as symb  "
	sql += "  , p.prod_id "
	sql += "  , count(*) as open_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then 1 else 0 end) as open_up_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then 1 else 0 end) as open_dn_cnt "
	sql += "  , sum(p.tot_out_cnt) as spent_amt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then p.tot_out_cnt else 0 end) as spent_up_amt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then p.tot_out_cnt else 0 end) as spent_dn_amt "
	sql += "  from cbtrade.poss p "
	sql += "  where p.pos_stat in ('OPEN','SELL') "
	if prod_id:
		sql += f"  and p.prod_id = '{prod_id}' "
	sql += "  group by p.quote_curr_symb, p.prod_id "
	sql += "  ) x "
	sql += "  order by x.symb, x.prod_id "

	pair_spent = db.seld(sql)

	if not pair_spent:
		pair_spent = {}
	else:
		pair_spent = pair_spent[0]

	func_end(fnc)
	return pair_spent

#<=====>#

def db_pair_spent(prod_id=None):
	func_name = 'db_pair_spent'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select x.symb "
	sql += "  , x.prod_id "
	sql += "  , x.open_cnt "
	sql += "  , x.open_up_cnt "
	sql += "  , x.open_dn_cnt "
	sql += "  , round((x.open_up_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_up_pct "
	sql += "  , round((x.open_dn_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_dn_pct "
	sql += "  , x.spent_amt "
	sql += "  , x.spent_up_amt "
	sql += "  , x.spent_dn_amt "
	sql += "  , round((x.spent_up_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_up_pct "
	sql += "  , round((x.spent_dn_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_dn_pct "
	sql += "  from ( "
	sql += "select p.quote_curr_symb as symb  "
	sql += "  , p.prod_id "
	sql += "  , count(*) as open_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then 1 else 0 end) as open_up_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then 1 else 0 end) as open_dn_cnt "
	sql += "  , sum(p.tot_out_cnt) as spent_amt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then p.tot_out_cnt else 0 end) as spent_up_amt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then p.tot_out_cnt else 0 end) as spent_dn_amt "
	sql += "  from cbtrade.poss p "
	sql += "  where p.pos_stat in ('OPEN','SELL') "
	if prod_id:
		sql += f"  and p.prod_id = '{prod_id}' "
	sql += "  group by p.quote_curr_symb, p.prod_id "
	sql += "  ) x "
	sql += "  order by x.symb, x.prod_id "

	pair_spent = db.seld(sql)

	if not pair_spent:
		pair_spent = {}
	else:
		pair_spent = pair_spent[0]

	func_end(fnc)
	return pair_spent

#<=====>#

def db_pair_strat_spent(prod_id=None, buy_strat_type=None, buy_strat_name=None):
	func_name = 'db_pair_strat_spent'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select x.symb "
	sql += "  , x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.open_cnt "
	sql += "  , x.open_up_cnt "
	sql += "  , x.open_dn_cnt "
	sql += "  , round((x.open_up_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_up_pct "
	sql += "  , round((x.open_dn_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_dn_pct "
	sql += "  , x.spent_amt "
	sql += "  , x.spent_up_amt "
	sql += "  , x.spent_dn_amt "
	sql += "  , round((x.spent_up_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_up_pct "
	sql += "  , round((x.spent_dn_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_dn_pct "
	sql += "  from ( "
	sql += "select p.quote_curr_symb as symb  "
	sql += "  , p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name "
	sql += "  , count(*) as open_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then 1 else 0 end) as open_up_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then 1 else 0 end) as open_dn_cnt "
	sql += "  , sum(p.tot_out_cnt) as spent_amt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then p.tot_out_cnt else 0 end) as spent_up_amt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then p.tot_out_cnt else 0 end) as spent_dn_amt "
	sql += "  from cbtrade.poss p "
	sql += "  where p.pos_stat in ('OPEN','SELL') "
	if prod_id:
		sql += f"  and p.prod_id = '{prod_id}' "
	if buy_strat_type:
		sql += f"  and p.buy_strat_type = '{buy_strat_type}' "
	if buy_strat_name:
		sql += f"  and p.buy_strat_name = '{buy_strat_name}' "
	sql += "  group by p.quote_curr_symb, p.prod_id, p.buy_strat_type, p.buy_strat_name "
	sql += "  ) x "
	sql += "  order by x.symb, x.prod_id, x.buy_strat_type, x.buy_strat_name "

	pair_strat_spent = db.seld(sql)

	if not pair_strat_spent:
		pair_strat_spent = {}
	else:
		pair_strat_spent = pair_strat_spent[0]

	func_end(fnc)
	return pair_strat_spent

#<=====>#

def db_pair_strat_freq_spent(prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None):
	func_name = 'db_pair_strat_freq_spent'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select x.symb "
	sql += "  , x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.buy_strat_freq "
	sql += "  , x.open_cnt "
	sql += "  , x.open_up_cnt "
	sql += "  , x.open_dn_cnt "
	sql += "  , round((x.open_up_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_up_pct "
	sql += "  , round((x.open_dn_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_dn_pct "
	sql += "  , x.spent_amt "
	sql += "  , x.spent_up_amt "
	sql += "  , x.spent_dn_amt "
	sql += "  , round((x.spent_up_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_up_pct "
	sql += "  , round((x.spent_dn_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_dn_pct "
	sql += "  from ( "
	sql += "select p.quote_curr_symb as symb  "
	sql += "  , p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name "
	sql += "  , p.buy_strat_freq "
	sql += "  , count(*) as open_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then 1 else 0 end) as open_up_cnt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then 1 else 0 end) as open_dn_cnt "
	sql += "  , sum(p.tot_out_cnt) as spent_amt "
	sql += "  , sum(case when p.buy_strat_type = 'up' then p.tot_out_cnt else 0 end) as spent_up_amt "
	sql += "  , sum(case when p.buy_strat_type = 'dn' then p.tot_out_cnt else 0 end) as spent_dn_amt "
	sql += "  from cbtrade.poss p "
	sql += "  where p.pos_stat in ('OPEN','SELL') "
	if prod_id:
		sql += f"  and p.prod_id = '{prod_id}' "
	if buy_strat_type:
		sql += f"  and p.buy_strat_type = '{buy_strat_type}' "
	if buy_strat_name:
		sql += f"  and p.buy_strat_name = '{buy_strat_name}' "
	if buy_strat_freq:
		sql += f"  and p.buy_strat_freq = '{buy_strat_freq}' "
	sql += "  group by p.quote_curr_symb, p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
	sql += "  ) x "
	sql += "  order by x.symb, x.prod_id, x.buy_strat_type, x.buy_strat_name, x.buy_strat_freq "

	pair_strat_spent = db.seld(sql)

	if not pair_strat_spent:
		pair_strat_spent = {}
	else:
		pair_strat_spent = pair_strat_spent[0]

	func_end(fnc)
	return pair_strat_spent

#<=====>#

# def db_ohlcv_prod_id_freqs(prod_id):
# 	func_name = 'db_ohlcv_prod_id_freqs'
# 	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# #	G(func_str)

# 	prod_id = prod_id.replace('-','_')

# 	sql = ""
# 	sql += "select distinct x.freq "
# 	sql += "  , max(start_dttm) as last_start_dttm "
# 	sql += f"  from ohlcv_{prod_id} x "
# 	sql += "  where 1=1 "
# 	sql += "  group by x.freq "

# 	last_dttms = db.seld(sql)

# 	if not last_dttms:
# 		last_dttms = {}

# 	func_end(fnc)
# 	return last_dttms

#<=====>#

# def db_ohlcv_freq_get(prod_id, freq, lmt=500):
# 	func_name = 'db_ohlcv_freq_get'
# 	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, freq={freq})'
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# #	G(func_str)

# 	prod_id = prod_id.replace('-','_')

# 	sql = ""
# 	sql += "select * "
# 	sql += f"  from ohlcv_{prod_id} x "
# 	sql += f"  where freq = '{freq}' "
# 	sql += "   order by x.timestamp desc "
# 	sql += f"  limit {lmt} "

# 	ohlcv = db.seld(sql)

# 	if not ohlcv:
# 		ohlcv = []

# 	func_end(fnc)
# 	return ohlcv

#<=====>#

def db_sell_double_check(pos_id):
	func_name = 'db_sell_double_check'
	func_str = f'{lib_name}.{func_name}(pos_id={pos_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sell_data = None

	# products in settings
	sql = ""
	sql += " select p.pos_stat "
	sql += "   , so.so_id "
	sql += "  from cbtrade.poss p "
	sql += "  left outer join cbtrade.sell_ords so on so.pos_id = p.pos_id "
	sql += "  where 1=1 "
	sql += f" and p.pos_id = {pos_id} "

	sell_data = db.seld(sql)

	if sell_data:
		sell_data = sell_data[0]

	func_end(fnc)
	return sell_data

#<=====>#

def db_pairs_loop_get(mode='full', loop_pairs=None, stable_pairs=None, err_pairs=None, quote_curr_symb=None):
	func_name = 'db_pairs_loop_get'
	func_str = f'{lib_name}.{func_name}(mode={mode}, mkts, stable_pairs, err_pairs)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# products in settings
	sql = ""
	sql += " select distinct m.mkt_id "
	sql += "   , m.mkt_name "
	sql += "   , m.prod_id "
	sql += "   , m.prc "
	sql += "   , m.prc_ask "
	sql += "   , m.prc_buy "
	sql += "   , m.prc_bid "
	sql += "   , m.prc_sell "
	sql += "   , m.prc_mid_mkt "
	sql += "   , m.prc_pct_chg_24h "
	sql += "   , m.vol_24h "
	sql += "   , m.vol_base_24h "
	sql += "   , m.vol_quote_24h "
	sql += "   , m.vol_pct_chg_24h "

	sql += "   , vmp.tot_cnt "
	sql += "   , vmp.win_cnt "
	sql += "   , vmp.lose_cnt "
	sql += "   , vmp.win_pct "
	sql += "   , vmp.lose_pct "
	sql += "   , vmp.age_mins "
	sql += "   , vmp.age_hours "
	sql += "   , vmp.tot_out_cnt "
	sql += "   , vmp.tot_in_cnt "
	sql += "   , vmp.buy_fees_cnt "
	sql += "   , vmp.sell_fees_cnt_tot "
	sql += "   , vmp.fees_cnt_tot "
	sql += "   , vmp.buy_cnt "
	sql += "   , vmp.sell_cnt_tot "
	sql += "   , vmp.hold_cnt "
	sql += "   , vmp.pocket_cnt "
	sql += "   , vmp.clip_cnt "
	sql += "   , vmp.sell_order_cnt "
	sql += "   , vmp.sell_order_attempt_cnt "
	sql += "   , vmp.val_curr "
	sql += "   , vmp.val_tot "
	sql += "   , vmp.win_amt "
	sql += "   , vmp.lose_amt "
	sql += "   , vmp.gain_loss_amt "
	sql += "   , vmp.gain_loss_amt_net "
	sql += "   , vmp.gain_loss_pct "
	sql += "   , vmp.gain_loss_pct_hr "

	sql += "   , m.base_curr_symb "
	sql += "   , m.base_curr_name "
	sql += "   , m.base_size_incr "
	sql += "   , m.base_size_min "
	sql += "   , m.base_size_max "

	sql += "   , m.quote_curr_symb "
	sql += "   , m.quote_curr_name "
	sql += "   , m.quote_size_incr "
	sql += "   , m.quote_size_min "
	sql += "   , m.quote_size_max "
	sql += "   , m.mkt_status_tf "

	sql += "   , m.mkt_view_only_tf "
	sql += "   , m.mkt_watched_tf "
	sql += "   , m.mkt_is_disabled_tf "
	sql += "   , m.mkt_new_tf "
	sql += "   , m.mkt_cancel_only_tf "
	sql += "   , m.mkt_limit_only_tf "
	sql += "   , m.mkt_post_only_tf "
	sql += "   , m.mkt_trading_disabled_tf "
	sql += "   , m.mkt_auction_mode_tf "

	sql += "   , mc.buy_check_dttm "
	sql += "   , mc.sell_check_dttm "

	sql += "   , m.note1 "
	sql += "   , m.note2 "
	sql += "   , m.note3 "
	sql += "   , m.add_dttm "
	sql += "   , m.upd_dttm "
	sql += "   , m.dlm "

	sql += "   , (select max(p.check_mkt_dttm) from cbtrade.poss p where p.prod_id = m.prod_id) as check_mkt_dttm "

	sql += "  from cbtrade.mkts m "
	sql += "  left outer join cbtrade.view_mkt_perf vmp on vmp.prod_id = m.prod_id "
	sql += "  left outer join cbtrade.mkt_checks mc on mc.prod_id = m.prod_id "
	sql += "  where 1=1 "
	if quote_curr_symb:
		sql += f"  and .quote_curr_symb = '{quote_curr_symb}' "
	sql += "  and m.mkt_limit_only_tf = 0 "
	if loop_pairs:
		loop_pairs_str = "'" + "', '".join(loop_pairs) + "'"
		sql += "   and m.prod_id in ({}) ".format(loop_pairs_str)
	if stable_pairs:
		stable_pairs_str = "'" + "', '".join(stable_pairs) + "'"
		sql += "   and m.prod_id not in ({}) ".format(stable_pairs_str)
	if err_pairs:
		err_pairs_str = "'" + "', '".join(err_pairs) + "'"
		sql += "   and m.prod_id not in ({}) ".format(err_pairs_str)

	if mode == 'sell':
		sql += "   order by (select sum(p.tot_out_cnt) from cbtrade.poss p where p.prod_id = m.prod_id and p.pos_stat = 'OPEN') desc "
#		sql += "   order by vmp.gain_loss_pct_hr desc "
	else:
		sql += "   order by vmp.gain_loss_pct_hr desc "

	mkts = db.seld(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_pairs_loop_top_perfs_prod_ids_get(lmt=None, pct_min=0, quote_curr_symb=None):
	func_name = 'db_pairs_loop_top_perfs_prod_ids_get'
	func_str = f'{lib_name}.{func_name}(lmt={lmt}, pct_min={pct_min})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = " "
	sql += "select x.prod_id "
	sql += "  from cbtrade.view_mkt_perf x "
	sql += "   where 1=1  "
	if quote_curr_symb:
		sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
	if pct_min > 0:
		sql += f"  and x.gain_loss_pct_day > {pct_min} "
	else:
		sql += "  and x.gain_loss_pct_day > 0 "
	sql += "  order by x.gain_loss_pct_day desc "
	if lmt:
		sql += "  limit {} ".format(lmt)

	mkts = db.sel(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_pairs_loop_top_gains_prod_ids_get(lmt=None, quote_curr_symb=None):
	func_name = 'db_pairs_loop_top_gains_prod_ids_get'
	func_str = '{lib_name}.{func_name}(lmt={lmt})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = " "
	sql += "select x.prod_id "
	sql += "  from cbtrade.view_mkt_perf x "
	sql += "   where 1=1  "
	if quote_curr_symb:
		sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
	sql += "  and x.gain_loss_amt > 0 "
	sql += "  order by x.gain_loss_amt desc "
	if lmt:
		sql += "  limit {} ".format(lmt)

	mkts = db.sel(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_pairs_loop_top_prc_chg_prod_ids_get(lmt=None, pct_min=0, quote_curr_symb=None):
	func_name = 'db_pairs_loop_top_prc_chg_prod_ids_get'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += " select prod_id "
	sql += "   from mkts m  "
	sql += "   where 1=1  "
	if quote_curr_symb:
		sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
	sql += "   and m.prc_pct_chg_24h > 0 "
	sql += f"   and m.prc_pct_chg_24h > {pct_min} "
	sql += "   and mkt_status_tf             = 'online' " # varchar(64)
	sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
	sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
	sql += "   and mkt_cancel_only_tf        = 0 " # tinyint default 0
	sql += "   and mkt_limit_only_tf         = 0 " # tinyint default 0
	sql += "   and mkt_post_only_tf          = 0 " # tinyint default 0
	sql += "   and mkt_trading_disabled_tf   = 0 " # tinyint default 0
	sql += "   and mkt_auction_mode_tf       = 0 " # tinyint default 0
	sql += "   order by prc_pct_chg_24h desc "

	if lmt:
		sql += f"  limit {lmt} "

	mkts = db.sel(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_pairs_loop_top_vol_chg_prod_ids_get(lmt=None, quote_curr_symb=None):
	func_name = 'db_pairs_loop_top_vol_chg_prod_ids_get'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += " select prod_id  "
	sql += "   from mkts m "
	sql += "   where 1=1  "
	if quote_curr_symb:
		sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
	sql += "   and mkt_status_tf             = 'online' " # varchar(64)
	sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
	sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
	sql += "   and mkt_cancel_only_tf        = 0 " # tinyint default 0
	sql += "   and mkt_limit_only_tf         = 0 " # tinyint default 0
	sql += "   and mkt_post_only_tf          = 0 " # tinyint default 0
	sql += "   and mkt_trading_disabled_tf   = 0 " # tinyint default 0
	sql += "   and mkt_auction_mode_tf       = 0 " # tinyint default 0
	sql += "   order by vol_quote_24h desc "

	if lmt:
		sql += "  limit {} ".format(lmt)

	mkts = db.sel(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_pairs_loop_top_vol_chg_pct_prod_ids_get(lmt=None, quote_curr_symb=None):
	func_name = 'db_pairs_loop_top_vol_chg_pct_prod_ids_get'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += " select prod_id  "
	sql += "   from mkts m "
	sql += "   where 1=1  "
	if quote_curr_symb:
		sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
	sql += "   and mkt_status_tf             = 'online' " # varchar(64)
	sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
	sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
	sql += "   and mkt_cancel_only_tf        = 0 " # tinyint default 0
	sql += "   and mkt_limit_only_tf         = 0 " # tinyint default 0
	sql += "   and mkt_post_only_tf          = 0 " # tinyint default 0
	sql += "   and mkt_trading_disabled_tf   = 0 " # tinyint default 0
	sql += "   and mkt_auction_mode_tf       = 0 " # tinyint default 0
	sql += "   order by vol_pct_chg_24h desc "

	if lmt:
		sql += "  limit {} ".format(lmt)

	mkts = db.sel(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_pairs_loop_watched_prod_ids_get(quote_curr_symb=None):
	func_name = 'db_pairs_loop_watched_prod_ids_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += " select m.prod_id "
	sql += "   from cbtrade.mkts m "
	sql += "   where m.ignore_tf = 0 "
	if quote_curr_symb:
		sql += f"  and m.quote_curr_symb = '{quote_curr_symb}' "
	sql += "   and m.mkt_watched_tf = 1 "
	sql += "   order by m.prod_id "

	mkts = db.sel(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_pairs_loop_poss_open_prod_ids_get(quote_curr_symb=None):
	func_name = 'db_pairs_loop_poss_open_prod_ids_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += " select prod_id "
	sql += "   from cbtrade.poss "
	sql += "   where ignore_tf = 0 "
	if quote_curr_symb:
		sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
	sql += "   and pos_stat in ('OPEN','SELL') "

	mkts = db.sel(sql)
	if isinstance(mkts, str):
		mkts = [mkts]
	# print(mkts)
	# print(type(mkts))
	# print(len(mkts))

	func_end(fnc)
	return mkts

#<=====>#

def db_open_trade_amts_get():
	func_name = 'db_open_trade_amts_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select p.base_curr_symb, sum(p.buy_cnt) as open_trade_amt"
	sql += "  from cbtrade.poss p"
	sql += "  where 1=1"
	sql += "  and p.ignore_tf = 0"
	sql += "  and p.test_txn_yn = 'N' "
	sql += "  and p.pos_stat in ('OPEN','SELL')"
	sql += "  group by p.base_curr_symb"
	sql += "  order by p.base_curr_symb"
	open_trade_amts = db.seld(sql)

	func_end(fnc)
	return open_trade_amts

#<=====>#

def db_bals_get():
	func_name = 'db_bals_get'
	func_str = '{}.{}()'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select symb as curr, bal_avail from cbtrade.bals"
	bals = db.seld(sql)
	if not bals:
		bals = {}

	func_end(fnc)
	return bals

#<=====>#

def db_bal_get_by_symbol(symb):
	func_name = 'db_bal_get_by_symbol'
	func_str = '{}.{}(symb={})'.format(lib_name, func_name, symb)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select bal_avail from cbtrade.bals where symb = '{}'".format(symb)
	bal = db.sel(sql)
	if not bal:
		bal = 0
	bal = float(bal)

	func_end(fnc)
	return bal

#<=====>#

def db_buy_ords_open_get():
	func_name = 'db_buy_ords_open_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select bo.*, TIMESTAMPDIFF(MINUTE, bo.buy_begin_dttm, NOW()) as elapsed "
	sql += "  from buy_ords bo  "
	sql += "  where 1=1 "
	sql += "  and bo.ord_stat = 'OPEN'  "
	sql += "  and bo.ignore_tf = 0"

	bos = db.seld(sql)

	func_end(fnc)
	return bos

#<=====>#

def db_buy_ords_get_by_uuid(buy_order_uuid):
	func_name = 'db_buy_ords_get_by_uuid'
	func_str = '{}.{}(buy_order_uuid={})'.format(lib_name, func_name, buy_order_uuid)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select bo.* "
	sql += "  from buy_ords bo "
	sql += "  where 1=1 "
	sql += "  and bo.buy_order_uuid = '{}' ".format(buy_order_uuid)
	sql += "  and bo.ignore_tf = 0 "

	bo = db.seld(sql)

	if isinstance(bo, list) and len(bo) == 1:
		bo = bo[0]

	func_end(fnc)
	return bo

#<=====>#

# => 
def db_mkt_elapsed_get(prod_id):
	func_name = 'db_mkt_elapsed_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	bo_elapsed_def = 9999
	pos_elapsed_def = 9999

	sql = ""
	sql += "select TIMESTAMPDIFF(MINUTE, max(bo.buy_begin_dttm), NOW()) + 1 as bo_elapsed "
	sql += "  from cbtrade.buy_ords bo "
	sql += "  where bo.ignore_tf = 0 "
	sql += f" and bo.prod_id = '{prod_id}' "
	sql += "  and bo.ord_stat in ('OPEN','FILL') "

	bo_elapsed = db.sel(sql)

	if not bo_elapsed:
		bo_elapsed = bo_elapsed_def

	sql = ""
	sql += "select coalesce(TIMESTAMPDIFF(MINUTE, max(p.pos_begin_dttm), NOW()) + 1, 9999) as pos_elapsed "
	sql += "  from cbtrade.poss p "
	sql += "  where p.ignore_tf = 0 "
	sql += f" and p.prod_id = '{prod_id}' "
	sql += "  and p.pos_stat in ('OPEN','SELL') "

	pos_elapsed = db.sel(sql)

	if not pos_elapsed:
		pos_elapsed = pos_elapsed_def

	last_elapsed = min(bo_elapsed, pos_elapsed)

	func_end(fnc)
	return bo_elapsed, pos_elapsed, last_elapsed

#<=====>#

# => 
def db_mkt_strat_elapsed_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq):
	func_name = 'db_mkt_elapsed_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	strat_bo_elapsed_def = 9999
	strat_pos_elapsed_def = 9999

	sql = ""
	sql += "select TIMESTAMPDIFF(MINUTE, max(bo.buy_begin_dttm), NOW()) + 1 as bo_elapsed "
	sql += "  from cbtrade.buy_ords bo "
	sql += "  where bo.ignore_tf = 0 "
	sql += f" and bo.prod_id = '{prod_id}' "
	sql += f" and bo.buy_strat_type = '{buy_strat_type}' "
	sql += f" and bo.buy_strat_name = '{buy_strat_name}' "
	sql += f" and bo.buy_strat_freq = '{buy_strat_freq}' "
	sql += "  and bo.ord_stat in ('OPEN','FILL') "

	strat_bo_elapsed = db.sel(sql)

	if not strat_bo_elapsed:
		strat_bo_elapsed = strat_bo_elapsed_def

	sql = ""
	sql += "select coalesce(TIMESTAMPDIFF(MINUTE, max(p.pos_begin_dttm), NOW()) + 1, 9999) as strat_pos_elapsed "
	sql += "  from cbtrade.poss p "
	sql += "  where p.ignore_tf = 0 "
	sql += f" and p.prod_id = '{prod_id}' "
	sql += f" and p.buy_strat_type = '{buy_strat_type}' "
	sql += f" and p.buy_strat_name = '{buy_strat_name}' "
	sql += f" and p.buy_strat_freq = '{buy_strat_freq}' "
	sql += "  and p.pos_stat in ('OPEN','SELL') "

	strat_pos_elapsed = db.sel(sql)

	if not strat_pos_elapsed:
		strat_pos_elapsed = strat_pos_elapsed_def

	strat_last_elapsed = min(strat_bo_elapsed, strat_pos_elapsed)

	func_end(fnc)
	return strat_bo_elapsed, strat_pos_elapsed, strat_last_elapsed

#<=====>#

# => disp_perf
def db_trade_perf_get(pos_stat=None):
	func_name = 'db_trade_perf_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	if pos_stat == 'OPEN':
		stat_sql = "  and p.pos_stat in ('OPEN','SELL') "
	elif pos_stat == 'CLOSE':
		stat_sql = "  and p.pos_stat in ('CLOSE') "
	else:
		stat_sql = ""

	sql = "select p.prod_id as mkt "
	sql += "  , p.pos_stat "
	sql += "  , sum(case when p.gain_loss_amt > 0 then 1 else 0 end)                         as win_cnt "
	sql += "  , sum(case when p.gain_loss_amt <= 0 then 1 else 0 end)                        as loss_cnt "
	sql += "  , sum(p.sell_order_cnt)                                                        as sell_cnt "
	sql += "  , sum(p.sell_order_attempt_cnt)                                                as sell_attempts "
	sql += "  , round(sum(p.tot_out_cnt),2)                                                  as spent_amt "
	sql += "  , round(sum(p.tot_in_cnt),2)                                                   as recv_amt "
	sql += "  , round(sum(case when p.gain_loss_amt > 0  then p.gain_loss_amt else 0 end),2) as win_amt "
	sql += "  , round(sum(case when p.gain_loss_amt <= 0 then p.gain_loss_amt else 0 end),2) as loss_amt "
	sql += "  , sum(p.hold_cnt)                                                              as hold_cnt "
	sql += "  , round(sum(p.hold_cnt) * m.prc,2)                                             as hold_amt "
	sql += "  , sum(p.pocket_cnt)                                                            as pocket_cnt "
	sql += "  , round(sum(p.pocket_cnt) * m.prc,2)                                           as pocket_amt "
	sql += "  , sum(p.clip_cnt)                                                              as clip_cnt "
	sql += "  , round(sum(p.clip_cnt) * m.prc,2)                                             as clip_amt "
	sql += "  , round(sum(p.val_curr),2)                                                     as val_curr "
	sql += "  , round(sum(p.val_tot),2)                                                      as val_tot "
	sql += "  , round(sum(p.buy_fees_cnt),2)                                                 as fees_buy "
	sql += "  , round(sum(p.sell_fees_cnt_tot),2)                                            as fees_sell "
	sql += "  , round(sum(p.fees_cnt_tot),2)                                                 as fees_tot "
	sql += "  , round(sum(p.gain_loss_amt),2)                                                as gain_loss_amt "
	sql += "  , round(sum(p.gain_loss_amt_est_high),2)                                       as gain_loss_amt_est_high "
	sql += "  from cbtrade.poss p "
	sql += "  join cbtrade.mkts m on m.prod_id = p.prod_id "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "
	sql += stat_sql
	sql += "  group by p.prod_id, p.pos_stat  "
	sql += "  order by p.prod_id, p.pos_stat desc "

	mkts = db.seld(sql)

	func_end(fnc)
	return mkts

#<=====>#

# => disp_strats_best, mkt_summary
def db_trade_strat_perf_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq):
	func_name = 'db_trade_strat_perf_get'
	func_str = '{}.{}(prod_id={}, buy_strat_type={}, buy_strat_name={}, buy_strat_freq={})'.format(lib_name, func_name, prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.buy_strat_freq "
	sql += "  , coalesce(x.tot_cnt,0)                                    as tot_cnt "
	sql += "  , coalesce(x.open_cnt,0)                                   as open_cnt "
	sql += "  , coalesce(x.close_cnt,0)                                  as close_cnt "
	sql += "  , coalesce(x.win_cnt,0)                                    as win_cnt "
	sql += "  , coalesce(x.lose_cnt,0)                                   as lose_cnt "
	sql += "  , coalesce(x.win_pct,0)                                    as win_pct "
	sql += "  , coalesce(x.lose_pct,0)                                   as lose_pct "
	sql += "  , coalesce(x.age_hours,0)                                  as age_hours "
	sql += "  , coalesce(x.tot_out_cnt,0)                                as tot_out_cnt "
	sql += "  , coalesce(x.tot_in_cnt,0)                                 as tot_in_cnt "
	sql += "  , coalesce(x.fees_cnt_tot,0)                               as fees_cnt_tot "
	sql += "  , coalesce(x.val_curr,0)                                   as val_curr "
	sql += "  , coalesce(x.val_tot,0)                                    as val_tot "
	sql += "  , coalesce(x.gain_loss_amt,0)                              as gain_loss_amt "
	sql += "  , coalesce(x.gain_loss_pct,0)                              as gain_loss_pct "
	sql += "  , coalesce(x.gain_loss_pct_hr,0)                           as gain_loss_pct_hr "
	sql += "  , case when x.gain_loss_pct_hr is not null then x.gain_loss_pct_hr * 24 else 0 end as gain_loss_pct_day "
	sql += "  from (select p.prod_id "
	sql += "          , p.buy_strat_type "
	sql += "          , p.buy_strat_name "
	sql += "          , p.buy_strat_freq "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.pos_stat in ('OPEN','SELL') then 1 else 0 end) as open_cnt  "
	sql += "          , sum(case when p.pos_stat = 'CLOSE' then 1 else 0 end) as close_cnt  "
	sql += "          , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          from (select bs.buy_strat_type, bs.buy_strat_name, bs.buy_strat_desc, f.freq as buy_strat_freq "
	sql += "                  from cbtrade.buy_strats bs "
	sql += "                  join cbtrade.freqs f "
	sql += "                  where 1=1 "
	sql += "                  and bs.ignore_tf = 0 "
	sql += "                  and f.ignore_tf = 0) x"
	sql += "          left outer join cbtrade.poss p on p.buy_strat_type = x.buy_strat_type and p.buy_strat_name = x.buy_strat_name and p.buy_strat_freq = x.buy_strat_freq "
	sql += "          where p.ignore_tf = 0 "
	sql += "          and p.prod_id = '{}' ".format(prod_id)
	sql += "          and p.buy_strat_type = '{}' ".format(buy_strat_type)
	sql += "          and p.buy_strat_name = '{}' ".format(buy_strat_name)
	sql += "          and p.buy_strat_freq = '{}' ".format(buy_strat_freq)
	sql += "          group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
	sql += "          ) x "
	sql += "  where 1=1 "
	sql += "  order by x.gain_loss_pct_hr desc "

	mkt_strat_perf = db.seld(sql)

	if mkt_strat_perf:
		mkt_strat_perf = mkt_strat_perf[0]

	func_end(fnc)
	return mkt_strat_perf

#<=====>#

# => disp_strats_best, mkt_summary
def db_trade_strat_perf_all_get(min_trades=1):
	func_name = 'db_trade_strat_perf_all_get'
	func_str = '{}.{}()'.format(lib_name, func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)


	sql = ""
	sql += " WITH strategy_base AS ( "
	sql += "   SELECT bs.buy_strat_type "
	sql += "     , bs.buy_strat_name "
	sql += "     , bs.buy_strat_desc "
	sql += "     , f.freq as buy_strat_freq "
	sql += "     FROM cbtrade.buy_strats bs "
	sql += "     JOIN cbtrade.freqs f "
	sql += "     WHERE 1=1 "
	sql += "     AND bs.ignore_tf = 0 "
	sql += "     AND f.ignore_tf = 0 "
	sql += "     ), "
	sql += " position_stats AS ( "
	sql += "   SELECT p.prod_id "
	sql += "     , p.buy_strat_type "
	sql += "     , p.buy_strat_name "
	sql += "     , p.buy_strat_freq "
	sql += "     , COUNT(p.pos_id) as tot_cnt "
	sql += "     , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END) as open_cnt "
	sql += "     , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) as close_cnt "
	sql += "     , SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt THEN 1 ELSE 0 END) as win_cnt "
	sql += "     , SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt THEN 1 ELSE 0 END) as lose_cnt "
	sql += "     , SUM(p.age_mins) as age_mins "
	sql += "     , ROUND(SUM(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "     , ROUND(SUM(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "     , ROUND(SUM(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "     , ROUND(SUM(p.val_curr), 2) as val_curr "
	sql += "     , ROUND(SUM(p.val_tot), 2) as val_tot "
	sql += "     , ROUND(SUM(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "     FROM strategy_base x "
	sql += "     LEFT OUTER JOIN cbtrade.poss p ON p.buy_strat_type = x.buy_strat_type AND p.buy_strat_name = x.buy_strat_name AND p.buy_strat_freq = x.buy_strat_freq "
	sql += "     WHERE p.ignore_tf = 0 "
	sql += "     GROUP BY p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
	sql += "   ) "
	sql += " SELECT  "
	sql += "   prod_id, "
	sql += "   buy_strat_type, "
	sql += "   buy_strat_name, "
	sql += "   buy_strat_freq, "
	sql += "   COALESCE(tot_cnt, 0) as tot_cnt, "
	sql += "   COALESCE(open_cnt, 0) as open_cnt, "
	sql += "   COALESCE(close_cnt, 0) as close_cnt, "
	sql += "   COALESCE(win_cnt, 0) as win_cnt, "
	sql += "   COALESCE(lose_cnt, 0) as lose_cnt, "
	sql += "   COALESCE(ROUND(win_cnt * 100.0 / NULLIF(tot_cnt, 0), 2), 0) as win_pct, "
	sql += "   COALESCE(ROUND(lose_cnt * 100.0 / NULLIF(tot_cnt, 0), 2), 0) as lose_pct, "
	sql += "   COALESCE(age_mins / 60.0, 0) as age_hours, "
	sql += "   COALESCE(tot_out_cnt, 0) as tot_out_cnt, "
	sql += "   COALESCE(tot_in_cnt, 0) as tot_in_cnt, "
	sql += "   COALESCE(fees_cnt_tot, 0) as fees_cnt_tot, "
	sql += "   COALESCE(val_curr, 0) as val_curr, "
	sql += "   COALESCE(val_tot, 0) as val_tot, "
	sql += "   COALESCE(gain_loss_amt, 0) as gain_loss_amt, "
	sql += "   COALESCE(ROUND(gain_loss_amt * 100.0 / NULLIF(tot_out_cnt, 0), 2), 0) as gain_loss_pct, "
	sql += "   COALESCE(ROUND(gain_loss_amt * 100.0 / NULLIF(tot_out_cnt, 0) / NULLIF(age_mins / 60.0, 0), 8), 0) as gain_loss_pct_hr, "
	sql += "   COALESCE(ROUND(gain_loss_amt * 100.0 / NULLIF(tot_out_cnt, 0) / NULLIF(age_mins / 60.0, 0) * 24, 8), 0) as gain_loss_pct_day "
	sql += " FROM position_stats "
	sql += " WHERE 1=1 "
	if min_trades:
			sql += f"  and tot_cnt >= {min_trades} "
	sql += " ORDER BY gain_loss_pct_hr DESC "

	mkt_strat_perf = db.seld(sql)

#	if mkt_strat_perf:
#		mkt_strat_perf = mkt_strat_perf[0]

	func_end(fnc)
	return mkt_strat_perf

#<=====>#

def db_mkt_prc_get_by_prod_id(prod_id):
	func_name = 'db_mkt_prc_get_by_prod_id'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select prc from mkts where prod_id = '{}'".format(prod_id)

	mkt_prc = db.sel(sql)

	func_end(fnc)
	return mkt_prc

#<=====>#

def db_mkt_sizing_data_get_by_uuid(buy_order_uuid):
	func_name = 'db_mkt_sizing_data_get_by_uuid'
	func_str = '{}.{}(buy_order_uuid={})'.format(lib_name, func_name, buy_order_uuid)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select bo.* "
	sql += "  , m.base_curr_symb "
	sql += "  , m.base_size_incr "
	sql += "  , m.base_size_min "
	sql += "  , m.base_size_max "
	sql += "  , m.quote_curr_symb "
	sql += "  , m.quote_size_incr "
	sql += "  , m.quote_size_min "
	sql += "  , m.quote_size_max "
	sql += "  from buy_ords bo "
	sql += "  join mkts m on m.prod_id = bo.prod_id "
	sql += "  where 1=1 "
	sql += "  and bo.buy_order_uuid = '{}' ".format(buy_order_uuid)
	sql += "  and bo.ignore_tf = 0 "

	bos = db.seld(sql)

	func_end(fnc)
	return bos

#<=====>#

def db_mkt_strats_stats_open_get(prod_id):
	func_name = 'db_mkt_strats_stats_open_get'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += " select distinct buy_strat_type, buy_strat_name "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '15min'), 0) as cnt_15min "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '30min'), 0) as cnt_30min "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '1h'), 0) as cnt_1h "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '4h'), 0) as cnt_4h "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '1d'), 0) as cnt_1d "
	sql += "   from cbtrade.poss p "
	sql += "   where p.ignore_tf = 0 "
	sql += "   and p.prod_id = '{}' ".format(prod_id)
	sql += "   and p.pos_stat in ('OPEN','SELL') "
	sql += "   order by buy_strat_type, buy_strat_name "

	strats_stats = db.seld(sql)

	func_end(fnc)
	return strats_stats

#<=====>#

# for an on screen disp => disp_strats_best
def db_mkt_strats_used_get(min_trades):
	func_name = 'db_mkt_strats_used_get'
	func_str = f'{lib_name}.{func_name}(min_trades={min_trades})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	# products in settings
	sql = ""
	sql += " select distinct p.prod_id "
	sql += "   , p.buy_strat_type "
	sql += "   , p.buy_strat_name "
	sql += "   , p.buy_strat_freq "
	sql += "   , count(*) as cnt "
	sql += "  from cbtrade.poss p "
	sql += "  where 1=1 "
	sql += "  and ignore_tf = 0 "
	sql += "  group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
	sql += f"  having count(*) >= {min_trades} "
	sql += "  order by cnt desc "

	mkts = db.seld(sql)

	func_end(fnc)
	return mkts

#<=====>#

# => disp_perf
def db_perf_summaries_get(prod_id=None, pos_stat=None, pos_id=None):
	func_name = 'db_mkt_perf_summaries_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	if pos_stat == 'OPEN':
		stat_sql = "  and p.pos_stat in ('OPEN','SELL') "
	elif pos_stat == 'CLOSE':
		stat_sql = "  and p.pos_stat in ('CLOSE') "
	else:
		stat_sql = ""

	sql = "select p.pos_stat "
	if prod_id:
		sql += "  , p.prod_id "
	if pos_id:
		sql += "  , p.pos_id "
	sql += "  , p.prod_id as mkt "
	sql += "  , count(p.pos_id)                                                                     as tot_cnt  "
	sql += "  , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end)                          as win_cnt  "
	sql += "  , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end)                          as lose_cnt  "
	sql += "  , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) "
	sql += "  ,   / count(p.pos_id) * 100, 2),0)                                                    as win_pct  "
	sql += "  , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) "
	sql += "  ,   / count(p.pos_id) * 100, 2),0)                                                    as lose_pct  "
	sql += "  , sum(p.age_mins)                                                                     as age_mins "
	sql += "  , sum(p.age_mins) / 60                                                                as age_hours "
	sql += "  , sum(p.sell_order_cnt)                                                               as sell_cnt "
	sql += "  , sum(p.sell_order_cnt)                                                               as sell_order_cnt "
	sql += "  , sum(p.sell_order_attempt_cnt)                                                       as sell_attempts "
	sql += "  , sum(p.sell_order_attempt_cnt)                                                       as sell_order_attempt_cnt "
	sql += "  , sum(p.buy_cnt)                                                                      as buy_cnt "
	sql += "  , sum(p.sell_cnt_tot)                                                                 as sell_cnt_tot "
	sql += "  , round(sum(p.tot_out_cnt),2)                                                         as spent_amt "
	sql += "  , round(sum(p.tot_in_cnt),2)                                                          as recv_amt "
	sql += "  , round(sum(p.tot_out_cnt), 2)                                                        as tot_out_cnt "
	sql += "  , round(sum(p.tot_in_cnt), 2)                                                         as tot_in_cnt "
	sql += "  , round(sum(case when p.gain_loss_amt > 0  then p.gain_loss_amt else 0 end),2)        as win_amt "
	sql += "  , round(sum(case when p.gain_loss_amt <= 0 then p.gain_loss_amt else 0 end),2)        as loss_amt "
	sql += "  , sum(p.hold_cnt)                                                                     as hold_cnt "
	sql += "  , sum(p.pocket_cnt)                                                                   as pocket_cnt "
	sql += "  , sum(p.clip_cnt)                                                                     as clip_cnt "
	sql += "  , round(sum(p.hold_cnt) * m.prc,2)                                                    as hold_amt "
	sql += "  , round(sum(p.pocket_cnt) * m.prc,2)                                                  as pocket_amt "
	sql += "  , round(sum(p.clip_cnt) * m.prc,2)                                                    as clip_amt "
	sql += "  , round(sum(p.buy_fees_cnt),2)                                                        as fees_buy "
	sql += "  , round(sum(p.buy_fees_cnt), 2)                                                       as buy_fees_cnt "
	sql += "  , round(sum(p.sell_fees_cnt_tot),2)                                                   as fees_sell "
	sql += "  , round(sum(p.sell_fees_cnt_tot), 2)                                                  as sell_fees_cnt_tot "
	sql += "  , round(sum(p.fees_cnt_tot),2)                                                        as fees_tot "
	sql += "  , round(sum(p.fees_cnt_tot), 2)                                                       as fees_cnt_tot "
	sql += "  , round(sum(p.val_curr),2)                                                            as val_curr "
	sql += "  , round(sum(p.val_tot),2)                                                             as val_tot "
	sql += "  , round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt  "
	sql += "                   then p.gain_loss_amt else 0 end), 2)                                 as win_amt  "
	sql += "  , round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt  "
	sql += "                   then p.gain_loss_amt else 0 end), 2)                                 as lose_amt "
	sql += "  , round(sum(p.gain_loss_amt), 2)                                                      as gain_loss_amt "
	sql += "  , round(sum(p.gain_loss_amt_net), 2)                                                  as gain_loss_amt_net "
	sql += "  , round(sum(p.gain_loss_amt_est_high),2)                                              as gain_loss_amt_est_high "
	sql += "  , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt)  "
	sql += "          * 100, 2)                                                                     as gain_loss_pct "
	sql += "  , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt)  "
	sql += "          * 100 / (sum(p.age_mins) / 60), 8)                                            as gain_loss_pct_hr "
	sql += "  , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt)  "
	sql += "          * 100/ (sum(p.age_mins) / 60) * 24, 8)                                        as gain_loss_pct_day "
	sql += "  from cbtrade.poss p "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "

	# do not check test_txn_yn here because we want to pull in all that simulated trading

	sql += stat_sql

	if prod_id:
		sql += f"  and p.prod_id = '{prod_id}' "
	if pos_id:
		sql += f"  and p.pos_id = '{pos_id}' "

	sql += "  group by p.prod_id, p.pos_stat  "
	if pos_id:
		sql += f"  ,p.pos_id "
	sql += "  order by p.prod_id, p.pos_stat desc "
	if pos_id:
		sql += f"  ,p.pos_id "

	mkts = db.seld(sql)

	func_end(fnc)
	return mkts


#<=====>#

def db_pos_get_by_pos_id(pos_id):
	func_name = 'db_pos_get_by_pos_id'
	func_str = '{}.{}(pos_id={})'.format(lib_name, func_name, pos_id)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.pos_id = '{}' ".format(pos_id)
	sql += "  and p.ignore_tf = 0 "

	pos = db.seld(sql)

	if isinstance(pos, list) and len(pos) == 1:
		pos = pos[0]

	func_end(fnc)
	return pos

#<=====>#

def db_poss_open_recent_get(lmt=None, test_yn='N'):
	func_name = 'db_poss_open_recent_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "
	if test_yn == 'Y':
		sql += "  and test_txn_yn = 'Y' "
	elif test_yn == 'N':
		sql += "  and test_txn_yn = 'N' "
	sql += "  and pos_stat = 'OPEN' "
	sql += "  order by p.pos_begin_dttm desc "
	poss = db.seld(sql)
	if lmt:
		sql += "limit {}".format(lmt)

	poss = db.seld(sql)

	func_end(fnc)
	return poss

#<=====>#

def db_poss_close_recent_get(lmt=None, test_yn='N'):
	func_name = 'db_poss_close_recent_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and ignore_tf = 0 "
	if test_yn == 'Y':
		sql += "  and test_txn_yn = 'Y' "
	elif test_yn == 'N':
		sql += "  and test_txn_yn = 'N' "
	sql += "  and pos_stat = 'CLOSE' "
	sql += "  order by p.pos_end_dttm desc "
	poss = db.seld(sql)
	if lmt:
		sql += "limit {}".format(lmt)

	poss = db.seld(sql)

	func_end(fnc)
	return poss

#<=====>#

def db_poss_open_cnt_get_by_prod_id(prod_id):
	func_name = 'db_poss_open_cnt_get_by_prod_id'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += " select count(p.pos_id) as pos_cnt "
	sql += "   , coalesce(TIMESTAMPDIFF(MINUTE, p.pos_begin_dttm, NOW()) + 1, -1) as new_age_mins "
	sql += "   from cbtrade.poss p "
	sql += "   where 1=1 "
	sql += "   and p.ignore_tf = 0 "
	sql += "   and p.prod_id = '{}' ".format(prod_id)
	sql += "   and p.pos_stat in ('OPEN','SELL') "
#	sql += "   order by p.buy_strat_name, p.buy_strat_freq "
	sql += "   order by p.pos_id "

	pos_cnt = db.sel(sql)

	func_end(fnc)
	return pos_cnt

#<=====>#

def db_pos_open_get_by_prod_id(prod_id):
	func_name = 'db_pos_open_get_by_prod_id'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += " select p.*"
	sql += "   , coalesce(TIMESTAMPDIFF(MINUTE, p.pos_begin_dttm, NOW()) + 1, -1) as new_age_mins "
	sql += "   from cbtrade.poss p "
	sql += "   where 1=1 "
	sql += "   and p.ignore_tf = 0 "
	sql += "   and p.prod_id = '{}' ".format(prod_id)
	sql += "   and p.pos_stat in ('OPEN','SELL') "
#	sql += "   order by p.buy_strat_name, p.buy_strat_freq "
	sql += "   order by p.pos_id "

	poss = db.seld(sql)
#	print(f'poss => len : {len(poss)}, typ: {type(poss)}')


	func_end(fnc)
	return poss

#<=====>#

def db_poss_open_max_trade_size_get(prod_id):
	func_name = 'db_poss_open_max_trade_size_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select max(p.buy_cnt) "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.prod_id = '{}' ".format(prod_id)
	sql += "  and p.ignore_tf = 0 "
	sql += "  and pos_stat in ('OPEN','SELL') "
	sql += "  order by p.prod_id, p.pos_id "

	trade_size = db.sel(sql)

	func_end(fnc)
	if trade_size:
		return trade_size
	else:
		return 0

#<=====>#

def db_mkts_open_cnt_get():
	func_name = 'db_mkts_open_cnt_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select count(distinct p.prod_id) "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.pos_stat in ('OPEN','SELL') "
	sql += "  and p.ignore_tf = 0 "

	mkt_open_cnt = db.sel(sql)

	func_end(fnc)
	return mkt_open_cnt

#<=====>#

def db_poss_sell_order_problems_get():
	func_name = 'db_poss_sell_order_problems_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	poss = []

	sql = """
		WITH SellOrderStats AS (
			SELECT 
				pos_id, 
				COUNT(*) AS sell_order_count 
			FROM cbtrade.sell_ords
			GROUP BY pos_id
		)
		SELECT 
			'pos.pos_stat = SELL but no OPEN sell orders on sell_ords' AS reason,
			p.pos_id, 
			p.prod_id, 
			p.pos_stat, 
			p.test_txn_yn, 
			so.so_id
		FROM poss p
		LEFT JOIN cbtrade.sell_ords so ON so.pos_id = p.pos_id
		LEFT JOIN SellOrderStats sos ON p.pos_id = sos.pos_id
		WHERE p.ignore_tf = 0 
		AND p.pos_stat = 'SELL' 
		AND sos.sell_order_count IS NULL

		UNION ALL

		SELECT 
			'pos.pos_stat = OPEN but there is a sell order(s) on sell_ords' AS reason,
			p.pos_id, 
			p.prod_id, 
			p.pos_stat, 
			p.test_txn_yn, 
			so.so_id
		FROM poss p
		LEFT JOIN cbtrade.sell_ords so ON so.pos_id = p.pos_id
		LEFT JOIN SellOrderStats sos ON p.pos_id = sos.pos_id
		WHERE p.ignore_tf = 0 
		AND p.pos_stat = 'OPEN' 
		AND sos.sell_order_count > 0

		UNION ALL

		SELECT 
			'multiple sell orders' AS reason,
			p.pos_id, 
			p.prod_id, 
			p.pos_stat, 
			p.test_txn_yn, 
			so.so_id
		FROM poss p
		LEFT JOIN cbtrade.sell_ords so ON so.pos_id = p.pos_id
		LEFT JOIN SellOrderStats sos ON p.pos_id = sos.pos_id
		WHERE p.ignore_tf = 0 
		AND sos.sell_order_count > 1;
		"""

	poss = db.seld(sql)

	func_end(fnc)
	return poss

#<=====>#

def db_poss_open_get(prod_id=None, test_only_yn='N', live_only_yn='N'):
	func_name = 'db_poss_open_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "

	if test_only_yn == 'Y':
		sql += "  and p.test_txn_yn = 'Y' "
	elif live_only_yn == 'Y':
		sql += "  and p.test_txn_yn = 'N' "

	if prod_id:
		sql += f"  and prod_id = '{prod_id}' "
	sql += "  and pos_stat in ('OPEN','SELL') "
	if prod_id:
		sql += "  order by p.prod_id, p.pos_id "
	else:
		sql += "  order by p.pos_begin_dttm desc "

	poss = db.seld(sql)

	func_end(fnc)
	return poss

#<=====>#

def db_sell_ords_open_get():
	func_name = 'db_sell_ords_open_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select so.*, p.buy_strat_name, p.buy_strat_freq, TIMESTAMPDIFF(MINUTE, so.sell_begin_dttm, NOW()) as elapsed "
	sql += "  from sell_ords so "
	sql += "  join poss p on p.pos_id = so.pos_id "
	sql += "  where 1=1 "
	sql += "  and (so.ord_stat = 'OPEN' or p.pos_stat = 'SELL') "
	sql += "  and so.ignore_tf = 0 "
	sql += "  and p.ignore_tf = 0 "
	sql += "  order by so_id "

	sos = db.seld(sql)

	func_end(fnc)
	return sos

#<=====>#

def db_sell_ords_get_by_pos_id(pos_id):
	func_name = 'db_sell_ords_get_by_pos_id'
	func_str = f'{lib_name}.{func_name}(pos_id={pos_id})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select * "
	sql += "  from sell_ords  "
	sql += "  where 1=1 "
	sql += f"  and pos_id = {pos_id} "
	sql += "  and ignore_tf = 0 "
	sql += "  order by so_id "

	sos = db.seld(sql)

	func_end(fnc)
	return sos

#<=====>#

def db_sell_ords_get_by_uuid(sell_order_uuid):
	func_name = 'db_sell_ords_get_by_uuid'
	func_str = '{}.{}(sell_order_uuid={})'.format(lib_name, func_name, sell_order_uuid)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select so.* "
	sql += "  from sell_ords so "
	sql += "  where 1=1 "
	sql += "  and so.sell_order_uuid = '{}' ".format(sell_order_uuid)
	sql += "  and so.ignore_tf = 0 "

	so = db.seld(sql)

	if isinstance(so, list) and len(so) == 1:
		so = so[0]

	func_end(fnc)
	return so

#<=====>#

# for an on screen disp => disp_strats
def db_strats_perf_get_all(buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None):
	func_name = 'db_strats_perf_get_all'
	func_str = '{}.{}(buy_strat_type={}, buy_strat_name={}, buy_strat_freq={})'.format(lib_name, func_name, buy_strat_type, buy_strat_name, buy_strat_freq)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = "select p.prod_id as mkt "
	sql += "  , p.pos_stat "
	sql += "  , sum(case when p.gain_loss_amt > 0 then 1 else 0 end)                         as win_cnt "
	sql += "  , sum(case when p.gain_loss_amt <= 0 then 1 else 0 end)                        as loss_cnt "
	sql += "  , sum(p.sell_order_cnt)                                                        as sell_cnt "
	sql += "  , sum(p.sell_order_attempt_cnt)                                                as sell_attempts "
	sql += "  , round(sum(p.tot_out_cnt),2)                                                  as spent_amt "
	sql += "  , round(sum(p.tot_in_cnt),2)                                                   as recv_amt "
	sql += "  , round(sum(case when p.gain_loss_amt > 0  then p.gain_loss_amt else 0 end),2) as win_amt "
	sql += "  , round(sum(case when p.gain_loss_amt <= 0 then p.gain_loss_amt else 0 end),2) as loss_amt "
	sql += "  , sum(p.hold_cnt)                                                              as hold_cnt "
	sql += "  , round(sum(p.hold_cnt) * m.prc,2)                                             as hold_amt "
	sql += "  , sum(p.pocket_cnt)                                                            as pocket_cnt "
	sql += "  , round(sum(p.pocket_cnt) * m.prc,2)                                           as pocket_amt "
	sql += "  , sum(p.clip_cnt)                                                              as clip_cnt "
	sql += "  , round(sum(p.clip_cnt) * m.prc,2)                                             as clip_amt "
	sql += "  , round(sum(p.val_curr),2)                                                     as val_curr "
	sql += "  , round(sum(p.val_tot),2)                                                      as val_tot "
	sql += "  , round(sum(p.buy_fees_cnt),2)                                                 as fees_buy "
	sql += "  , round(sum(p.sell_fees_cnt_tot),2)                                            as fees_sell "
	sql += "  , round(sum(p.fees_cnt_tot),2)                                                 as fees_tot "
	sql += "  , round(sum(p.gain_loss_amt),2)                                                as gain_loss_amt "
	sql += "  , round(sum(p.gain_loss_amt_est_high),2)                                       as gain_loss_amt_est_high "
	sql += "  from cbtrade.poss p "
	sql += "  join cbtrade.mkts m on m.prod_id = p.prod_id "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "
	if buy_strat_type:
		sql = " and p.buy_strat_type = '{}'.format(buy_strat_type) "
	if buy_strat_name:
		sql = " and p.buy_strat_name = '{}'.format(buy_strat_name) "
	if buy_strat_freq:
		sql = " and p.buy_strat_freq = '{}'.format(buy_strat_freq) "
	sql += "  group by p.prod_id, p.pos_stat  "
	sql += "  order by p.prod_id, p.pos_stat desc "

	mkts = db.seld(sql)

	func_end(fnc)
	return mkts

#<=====>#

# for an on screen disp => disp_strats
def db_strats_w_stats_get_all():
	func_name = 'db_strats_w_stats_get_all'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "select distinct buy_strat_type, buy_strat_name, buy_strat_freq "
	sql += "  from cbtrade.poss "
	sql += "  where ignore_tf = 0"
	sql += "  order by buy_strat_type, buy_strat_name, buy_strat_freq "

	strats = db.seld(sql)

	func_end(fnc)
	return strats

#<=====>#

# => mkt_perf_get
def db_view_trade_perf_get_by_prod_id(prod_id):
	func_name = 'db_view_trade_perf_get_by_prod_id'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = "select x.* "
	sql += "  from cbtrade.view_mkt_perf x "
	sql += "  where 1=1 "
	sql += "  and x.prod_id = '{}' ".format(prod_id)

	mkt_perf = db.seld(sql)

	if mkt_perf:
		mkt_perf = mkt_perf[0]

	func_end(fnc)
	return mkt_perf

#<=====>#

# => mkt_perf_get
def db_table_names_get():
	func_name = 'db_table_names_get'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	sql = ""
	sql += "SELECT x.table_name as table_name "
	sql += "FROM information_schema.TABLES x "
	sql += "WHERE x.table_schema = 'cbtrade' "
	sql += "GROUP BY x.table_schema, x.table_name "

	table_names = db.sel(sql)

	func_end(fnc)
	return table_names

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
