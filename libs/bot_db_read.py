#<=====>#
# Description
#<=====>#



#<=====>#
# Import All
#<=====>#

import_all_func_list = []
import_all_func_list.append("db_safe_string")
import_all_func_list.append("db_mkts_loop_get")
import_all_func_list.append("db_mkts_loop_top_perfs_prod_ids_get")
import_all_func_list.append("db_mkts_loop_top_gains_prod_ids_get")
import_all_func_list.append("db_mkts_loop_top_prc_chg_prod_ids_get")
import_all_func_list.append("db_mkts_loop_top_vol_chg_prod_ids_get")
import_all_func_list.append("db_mkts_loop_top_vol_chg_pct_prod_ids_get")
import_all_func_list.append("db_mkts_loop_poss_open_prod_ids_get")
import_all_func_list.append("db_mkts_loop_watched_prod_ids_get")
import_all_func_list.append("db_mkt_elapsed_get")
import_all_func_list.append("db_mkt_strat_elapsed_get")
import_all_func_list.append("db_open_trade_amts_get")
import_all_func_list.append("db_bals_get")
import_all_func_list.append("db_bal_get_by_symbol")
import_all_func_list.append("db_buy_ords_open_get")
import_all_func_list.append("db_buy_ords_get_by_uuid")
import_all_func_list.append("db_trade_perf_get")
import_all_func_list.append("db_mkts_open_cnt_get")
import_all_func_list.append("db_mkt_prc_get_by_prod_id")
import_all_func_list.append("db_mkt_sizing_data_get_by_uuid")
import_all_func_list.append("db_trade_strat_perf_get")
import_all_func_list.append("db_mkt_strats_stats_open_get")
import_all_func_list.append("db_mkt_strats_used_get")
import_all_func_list.append("db_perf_summaries_get")
import_all_func_list.append("db_pos_get_by_pos_id")
import_all_func_list.append("db_pos_open_get_by_prod_id")
import_all_func_list.append("db_poss_close_recent_get")
import_all_func_list.append("db_poss_open_cnt_get_by_prod_id")
import_all_func_list.append("db_poss_open_get")
import_all_func_list.append("db_poss_open_max_trade_size_get")
import_all_func_list.append("db_poss_open_get")
import_all_func_list.append("db_poss_open_recent_get")
import_all_func_list.append("db_sell_ords_open_get")
import_all_func_list.append("db_sell_ords_get_by_uuid")
import_all_func_list.append("db_strats_perf_get_all")
import_all_func_list.append("db_strats_w_stats_get_all")
import_all_func_list.append("db_view_trade_perf_get_by_prod_id")
__all__ = import_all_func_list


#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports - Common Modules
#<=====>#
# import pandas as pd
import sys
import os
import re
import time


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

#from bot_common                    import *
from bot_secrets                   import secrets


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_db_read'
log_name      = 'bot_db_read'
lib_verbosity = 1
lib_debug_lvl = 1
verbosity     = 1
debug_lvl     = 1
lib_secs_max  = 0.33
lib_secs_max  = 10


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

'''

drop view if exists cbtrade.view_mkt_perf;
create view cbtrade.view_mkt_perf as 
  from cbtrade.poss p
  where ignore_tf = 0
  group by p.prod_id
  order by gain_loss_pct_day desc
  ;

'''

#<=====>#

def db_safe_string(in_str):
	# Regular expression pattern to match allowed characters
	allowed_chars_pattern = r"[^a-zA-Z0-9\s\.,;:'\"?!@#\$%\^&\*\(\)_\+\-=\[\]\{\}<>\/\\]"
	# Replace characters not in the allowed set with an empty string
	out_str = re.sub(allowed_chars_pattern, '', in_str)
	return out_str

#<=====>#

def db_mkts_loop_get(loop_mkts=None, stable_mkts=None, err_mkts=None):
	func_name = 'db_mkts_loop_get'
	func_str = '{}.{}(mkts, stable_mkts, err_mkts)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	# products in settings
	sql = ""
	sql += " select m.mkt_id "
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

#	sql += "   , vmp.prod_id "
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

#	sql += "   , m.mkt_venue "
#	sql += "   , m.ignore_tf "

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

	sql += "   , m.note1 "
	sql += "   , m.note2 "
	sql += "   , m.note3 "
	sql += "   , m.add_dttm "
	sql += "   , m.upd_dttm "
	sql += "   , m.dlm "

	sql += "   , vmp.test_tf "
	sql += "  from cbtrade.mkts m "
	sql += "  left outer join cbtrade.view_mkt_perf vmp on vmp.prod_id = m.prod_id "
	sql += "  where 1=1 "
	sql += "  and m.mkt_limit_only_tf = 0 "
	if loop_mkts:
		loop_mkts_str = "'" + "', '".join(loop_mkts) + "'"
		sql += "   and m.prod_id in ({}) ".format(loop_mkts_str)
	if stable_mkts:
		stable_mkts_str = "'" + "', '".join(stable_mkts) + "'"
		sql += "   and m.prod_id not in ({}) ".format(stable_mkts_str)
	if err_mkts:
		err_mkts_str = "'" + "', '".join(err_mkts) + "'"
		sql += "   and m.prod_id not in ({}) ".format(err_mkts_str)

	sql += "   order by vmp.gain_loss_pct_hr desc "

	mkts = db.seld(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_mkts_loop_top_perfs_prod_ids_get(lmt=None, pct_min=0):
	func_name = 'db_mkts_loop_top_perfs_prod_ids_get'
	func_str = f'{lib_name}.{func_name}(lmt={lmt}, pct_min={pct_min})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = " "
	sql += "select x.prod_id "
	sql += "  from cbtrade.view_mkt_perf x "
	sql += "  where 1=1 "
	if pct_min > 0:
		sql += f"  and x.gain_loss_pct_day > {pct_min} "
	else:
		sql += "  and x.gain_loss_pct_day > 0 "
	sql += "  order by x.gain_loss_pct_day desc "
	if lmt:
		sql += "  limit {} ".format(lmt)
	mkts = db.sel(sql)

#	print(f'top mkts by perf : {mkts}')

	func_end(fnc)
	return mkts

#<=====>#

def db_mkts_loop_top_gains_prod_ids_get(lmt=None):
	func_name = 'db_mkts_loop_top_gains_prod_ids_get'
	func_str = '{lib_name}.{func_name}(lmt={lmt})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = " "
	sql += "select x.prod_id "
	sql += "  from cbtrade.view_mkt_perf x "
	sql += "  where 1=1 "
	sql += "  and x.gain_loss_amt > 0 "
	sql += "  order by x.gain_loss_amt desc "
	if lmt:
		sql += "  limit {} ".format(lmt)
	mkts = db.sel(sql)

#	print(f'top mkts by perf : {mkts}')

	func_end(fnc)
	return mkts

#<=====>#

def db_mkts_loop_top_prc_chg_prod_ids_get(lmt=None, pct_min=0):
	func_name = 'db_mkts_loop_top_prc_chg_prod_ids_get'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select prod_id "
	sql += "   from mkts m  "
	sql += "   where quote_curr_symb = 'USDC'  "
#	sql += "   and base_curr_symb not in ('USDT','GUSD','PYUSD','PAX')  "
#	sql += "   and m.prod_id not in ({})".format(stable_mkts_str)
#	sql += "   and m.prod_id not in ({})".format(err_mkts_str)
	sql += "   and m.prc_pct_chg_24h > 0 "
	sql += f"   and m.prc_pct_chg_24h > {pct_min} "
#	sql += "   and prc_pct_chg_24h > 0 "
#	sql += "   and TIMESTAMPDIFF(HOUR, add_dttm, NOW()) > 24 "
	sql += "   and mkt_status_tf             = 'online' " # varchar(64)
	sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
#	sql += "   and mkt_watched_tf            = 0 " # tinyint default 0
	sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
#	sql += "   and mkt_new_tf                = 0 " # tinyint default 0
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

def db_mkts_loop_top_vol_chg_prod_ids_get(lmt=None):
	func_name = 'db_mkts_loop_top_vol_chg_prod_ids_get'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select prod_id  "
	sql += "   from mkts m "
	sql += "   where quote_curr_symb = 'USDC'  "
#	sql += "   and m.prod_id not in ({})".format(stable_mkts_str)
#	sql += "   and m.prod_id not in ({})".format(err_mkts_str)
#	sql += "   and base_curr_symb not in ('USDT','GUSD','PYUSD','PAX')  "
#	sql += "   and prc_pct_chg_24h > 0 " # intentional
#	sql += "   and TIMESTAMPDIFF(HOUR, add_dttm, NOW()) > 24 "
	sql += "   and mkt_status_tf             = 'online' " # varchar(64)
	sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
#	sql += "   and mkt_watched_tf            = 0 " # tinyint default 0
	sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
#	sql += "   and mkt_new_tf                = 0 " # tinyint default 0
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

def db_mkts_loop_top_vol_chg_pct_prod_ids_get(lmt=None):
	func_name = 'db_mkts_loop_top_vol_chg_pct_prod_ids_get'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select prod_id  "
	sql += "   from mkts m "
	sql += "   where quote_curr_symb = 'USDC'  "
#	sql += "   and base_curr_symb not in ('USDT','GUSD','PYUSD','PAX')  "
#	sql += "   and m.prod_id not in ({})".format(stable_mkts_str)
#	sql += "   and m.prod_id not in ({})".format(err_mkts_str)
#	sql += "   and prc_pct_chg_24h > 0 " # intentional
#	sql += "   and vol_pct_chg_24h > 0 "
#	sql += "   and TIMESTAMPDIFF(HOUR, add_dttm, NOW()) > 24 "
	sql += "   and mkt_status_tf             = 'online' " # varchar(64)
	sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
#	sql += "   and mkt_watched_tf            = 0 " # tinyint default 0
	sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
#	sql += "   and mkt_new_tf                = 0 " # tinyint default 0
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

def db_mkts_loop_watched_prod_ids_get():
	func_name = 'db_mkts_loop_watched_prod_ids_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select m.prod_id "
	sql += "   from cbtrade.mkts m "
	sql += "   where m.ignore_tf = 0 "
	sql += "   and m.mkt_watched_tf = 1 "
	sql += "   order by m.prod_id "
	mkts = db.sel(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_mkts_loop_poss_open_prod_ids_get():
	func_name = 'db_mkts_loop_poss_open_prod_ids_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select prod_id "
	sql += "   from cbtrade.poss "
	sql += "   where ignore_tf = 0 "
	sql += "   and test_tf = 0 "
	sql += "   and pos_stat in ('OPEN','SELL') "
	mkts = db.sel(sql)

	func_end(fnc)
	return mkts

#<=====>#

def db_open_trade_amts_get():
	func_name = 'db_open_trade_amts_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select p.base_curr_symb, sum(p.buy_cnt) as open_trade_amt"
	sql += "  from cbtrade.poss p"
	sql += "  where 1=1"
#	sql += f"  and p.base_curr_symb = '{symb}}'"
	sql += "  and p.ignore_tf = 0"
	sql += "  and p.test_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select symb as curr, bal_avail from cbtrade.bals"
	bals = db.seld(sql)
	if not bals:
		bals = {}
#	print(f'{symb} bal : {bal:>.8f}')

	func_end(fnc)
	return bals

#<=====>#

def db_bal_get_by_symbol(symb):
	func_name = 'db_bal_get_by_symbol'
	func_str = '{}.{}(symb={})'.format(lib_name, func_name, symb)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select bal_avail from cbtrade.bals where symb = '{}'".format(symb)
	bal = db.sel(sql)
	if not bal:
		bal = 0
	bal = float(bal)
#	print(f'{symb} bal : {bal:>.8f}')

	func_end(fnc)
	return bal

#<=====>#

def db_buy_ords_open_get():
	func_name = 'db_buy_ords_open_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select * "
	sql += "  from buy_ords  "
	sql += "  where 1=1 "
	sql += "  and ord_stat = 'OPEN'  "
	sql += "  and ignore_tf = 0"
	bos = db.seld(sql)

	func_end(fnc)
	return bos

#<=====>#

def db_buy_ords_get_by_uuid(buy_order_uuid):
	func_name = 'db_buy_ords_get_by_uuid'
	func_str = '{}.{}(buy_order_uuid={})'.format(lib_name, func_name, buy_order_uuid)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	bo_elapsed_def = 9999
	pos_elapsed_def = 9999

	sql = ""
	sql += "select TIMESTAMPDIFF(MINUTE, max(bo.buy_begin_dttm), NOW()) + 1 as bo_elapsed "
	sql += "  from cbtrade.buy_ords bo "
	sql += "  where bo.ignore_tf = 0 "
	sql += "  and bo.test_tf = 0 "
	sql += f" and bo.prod_id = '{prod_id}' "
	sql += "  and bo.ord_stat in ('OPEN','FILL') "
	bo_elapsed = db.sel(sql)
	if not bo_elapsed:
		bo_elapsed = bo_elapsed_def

	sql = ""
	sql += "select coalesce(TIMESTAMPDIFF(MINUTE, max(p.pos_begin_dttm), NOW()) + 1, 9999) as pos_elapsed "
	sql += "  from cbtrade.poss p "
	sql += "  where p.ignore_tf = 0 "
	sql += "  and p.test_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	strat_bo_elapsed_def = 9999
	strat_pos_elapsed_def = 9999

	sql = ""
	sql += "select TIMESTAMPDIFF(MINUTE, max(bo.buy_begin_dttm), NOW()) + 1 as bo_elapsed "
	sql += "  from cbtrade.buy_ords bo "
	sql += "  where bo.ignore_tf = 0 "
	sql += "  and bo.test_tf = 0 "
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
	sql += "  and p.test_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
	sql += "  and p.test_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
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
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from (select bs.buy_strat_type, bs.buy_strat_name, bs.buy_strat_desc, f.freq as buy_strat_freq "
	sql += "                  from cbtrade.buy_strats bs "
	sql += "                  join cbtrade.freqs f) x"
	sql += "          left outer join cbtrade.poss p on p.buy_strat_type = x.buy_strat_type and p.buy_strat_name = x.buy_strat_name and p.buy_strat_freq = x.buy_strat_freq "
	sql += "          where p.ignore_tf = 0 "
	sql += "          and p.test_tf = 0 "
	sql += "          and p.prod_id = '{}' ".format(prod_id)
	sql += "          and p.buy_strat_type = '{}' ".format(buy_strat_type)
	sql += "          and p.buy_strat_name = '{}' ".format(buy_strat_name)
	sql += "          and p.buy_strat_freq = '{}' ".format(buy_strat_freq)
	sql += "          group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
	sql += "          ) x "
	sql += "  where 1=1 "
	sql += "  order by x.gain_loss_pct_hr desc "
#	print(sql)
	mkt_strat_perf = db.seld(sql)
	if mkt_strat_perf:
		mkt_strat_perf = mkt_strat_perf[0]

	func_end(fnc)
	return mkt_strat_perf

#<=====>#

def db_mkt_prc_get_by_prod_id(prod_id):
	func_name = 'db_mkt_prc_get_by_prod_id'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select prc from mkts where prod_id = '{}'".format(prod_id)
	mkt_prc = db.sel(sql)

	func_end(fnc)
	return mkt_prc

#<=====>#

def db_mkt_sizing_data_get_by_uuid(buy_order_uuid):
	func_name = 'db_mkt_sizing_data_get_by_uuid'
	func_str = '{}.{}(buy_order_uuid={})'.format(lib_name, func_name, buy_order_uuid)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select distinct buy_strat_type, buy_strat_name "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and test_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '15min'), 0) as cnt_15min "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and test_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '30min'), 0) as cnt_30min "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and test_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '1h'), 0) as cnt_1h "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and test_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '4h'), 0) as cnt_4h "
	sql += "   , coalesce((select count(*) "
	sql += "        from cbtrade.poss  "
	sql += "        where ignore_tf = 0 "
	sql += "        and test_tf = 0 "
	sql += "        and prod_id = p.prod_id  "
	sql += "        and buy_strat_type = p.buy_strat_type  "
	sql += "        and buy_strat_name = p.buy_strat_name  "
	sql += "        and pos_stat in ('OPEN','SELL') "
	sql += "        and buy_strat_freq = '1d'), 0) as cnt_1d "
	sql += "   from cbtrade.poss p "
	sql += "   where p.ignore_tf = 0 "
	sql += "   and p.test_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
	sql += "  and test_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	if pos_stat == 'OPEN':
		stat_sql = "  and p.pos_stat in ('OPEN','SELL') "
	elif pos_stat == 'CLOSE':
		stat_sql = "  and p.pos_stat in ('CLOSE') "
	else:
		stat_sql = ""

	sql = "select p.test_tf "
	if prod_id:
		sql += "  , p.prod_id "
	if pos_id:
		sql += "  , p.pos_id "
	sql += "  , p.prod_id as mkt "
	sql += "  , p.pos_stat "
	sql += "  , count(p.pos_id)                                                                     as tot_cnt  "
#	sql += "  , sum(case when p.gain_loss_amt > 0 then 1 else 0 end)                                as win_cnt "
#	sql += "  , sum(case when p.gain_loss_amt <= 0 then 1 else 0 end)                               as loss_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end)                          as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end)                          as lose_cnt  "

	sql += "  , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) "
	sql += "  ,   / count(p.pos_id) * 100, 2),0)                                                    as win_pct  "
	sql += "  , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) "
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

	sql += "  , round(sum(case when p.val_tot > p.tot_out_cnt  "
	sql += "                   then p.gain_loss_amt else 0 end), 2)                                 as win_amt  "
	sql += "  , round(sum(case when p.val_tot < p.tot_out_cnt  "
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
#	sql += "  join cbtrade.mkts m on m.prod_id = p.prod_id "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "

	# do not check test_tf here because we want to pull in all that simulated trading

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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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

def db_poss_close_recent_get(lmt=None):
	func_name = 'db_poss_close_recent_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and ignore_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select count(p.pos_id) as pos_cnt "
	sql += "   , coalesce(TIMESTAMPDIFF(MINUTE, p.pos_begin_dttm, NOW()) + 1, -1) as new_age_mins "
	sql += "   from cbtrade.poss p "
	sql += "   where 1=1 "
	sql += "   and p.ignore_tf = 0 "
	sql += "   and p.test_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select p.*"
	sql += "   , coalesce(TIMESTAMPDIFF(MINUTE, p.pos_begin_dttm, NOW()) + 1, -1) as new_age_mins "
	sql += "   from cbtrade.poss p "
	sql += "   where 1=1 "
	sql += "   and p.ignore_tf = 0 "
#	sql += "   and p.test_tf = 0 "
	sql += "   and p.prod_id = '{}' ".format(prod_id)
	sql += "   and p.pos_stat in ('OPEN','SELL') "
#	sql += "   order by p.buy_strat_name, p.buy_strat_freq "
	sql += "   order by p.pos_id "
	poss = db.seld(sql)

	func_end(fnc)
	return poss

#<=====>#

def db_poss_open_max_trade_size_get(prod_id):
	func_name = 'db_poss_open_max_trade_size_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select max(p.buy_cnt) "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.prod_id = '{}' ".format(prod_id)
	sql += "  and p.ignore_tf = 0 "
	sql += "  and p.test_tf = 0 "
	sql += "  and pos_stat in ('OPEN','SELL') "
	sql += "  order by p.prod_id, p.pos_id "
	trade_size = db.sel(sql)

	func_end(fnc)
	return trade_size

#<=====>#

def db_mkts_open_cnt_get():
	func_name = 'db_mkts_open_cnt_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select count(distinct p.prod_id) "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "
	sql += "  and p.test_tf = 0 "
	mkt_open_cnt = db.sel(sql)

	func_end(fnc)
	return mkt_open_cnt

#<=====>#

def db_poss_open_get(prod_id=None):
	func_name = 'db_poss_open_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "
	sql += "  and p.test_tf = 0 "
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

def db_poss_open_recent_get(lmt=None):
	func_name = 'db_poss_open_recent_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.ignore_tf = 0 "
	sql += "  and p.test_tf = 0 "
	sql += "  and pos_stat = 'OPEN' "
	sql += "  order by p.pos_begin_dttm desc "
	poss = db.seld(sql)
	if lmt:
		sql += "limit {}".format(lmt)
	poss = db.seld(sql)

	func_end(fnc)
	return poss

#<=====>#

def db_sell_ords_open_get():
	func_name = 'db_sell_ords_open_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select * "
	sql += "  from sell_ords  "
	sql += "  where 1=1 "
	sql += "  and ord_stat = 'OPEN' "
	sql += "  and ignore_tf = 0 "
	sql += "  order by so_id "
	sos = db.seld(sql)

	func_end(fnc)
	return sos

#<=====>#

def db_sell_ords_get_by_uuid(sell_order_uuid):
	func_name = 'db_sell_ords_get_by_uuid'
	func_str = '{}.{}(sell_order_uuid={})'.format(lib_name, func_name, sell_order_uuid)
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
#	sql += "  and p.test_tf = 0 "
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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = "select x.* "
	sql += "  from cbtrade.view_mkt_perf x "
	sql += "  where 1=1 "
#	sql += "  and x.ignore_tf = 0 "
	sql += "  and x.prod_id = '{}' ".format(prod_id)
	mkt_perf = db.seld(sql)
	if mkt_perf:
		mkt_perf = mkt_perf[0]

	func_end(fnc)
	return mkt_perf

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
