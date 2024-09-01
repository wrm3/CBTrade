#<=====>#
# Description
#<=====>#



#<=====>#
# Import All
#<=====>#
import_all_func_list = []
import_all_func_list.append("db_buy_ords_get_by_uuid")
import_all_func_list.append("db_buy_ords_stat_upd")
import_all_func_list.append("db_sell_ords_get_by_uuid")
import_all_func_list.append("db_sell_ords_stat_upd")
import_all_func_list.append("db_pos_get_by_pos_id")
import_all_func_list.append("db_poss_open_recent_get")
import_all_func_list.append("db_poss_close_recent_get")
import_all_func_list.append("db_poss_mkts_get_all")
import_all_func_list.append("db_poss_stat_upd")
import_all_func_list.append("db_loop_forced_mkts_get")
import_all_func_list.append("db_force_buy_done_upd")
import_all_func_list.append("db_mkts_perf_get_all")
import_all_func_list.append("db_mkt_perf_get")
import_all_func_list.append("db_strats_w_stats_get_all")
import_all_func_list.append("db_strats_perf_get_all")
import_all_func_list.append("db_loop_mkts_get_all")
import_all_func_list.append("db_loop_mkts_w_poss_open_get_all")
import_all_func_list.append("db_loop_mkts_watched_get_all")
import_all_func_list.append("db_loop_mkts_top_perfs_get_all")
import_all_func_list.append("db_loop_mkts_top_prc_chg_get_all")
import_all_func_list.append("db_loop_mkts_top_vol_chg_get_all")
import_all_func_list.append("db_loop_mkts_top_vol_chg_pct_get_all")
import_all_func_list.append("db_poss_err_upd")
import_all_func_list.append("db_poss_open_get")
import_all_func_list.append("db_poss_close_recent_get")
import_all_func_list.append("db_poss_open_max_trade_size_get")
import_all_func_list.append("db_pos_open_data_get")
import_all_func_list.append("db_mkt_strats_stats_open_get")
import_all_func_list.append("db_mkt_strat_perf_get")
import_all_func_list.append("db_buy_ords_open_get")
import_all_func_list.append("db_sell_ords_open_get")
import_all_func_list.append("db_curr_prc_upd")
import_all_func_list.append("db_curr_prc_stable_upd")
import_all_func_list.append("db_curr_prc_mkt_upd")
import_all_func_list.append("db_bal_get_by_symbol")
import_all_func_list.append("db_mkt_prc_get_by_prod_id")
#import_all_func_list.append("db_last_buy_elapsed_get")
#import_all_func_list.append("db_last_buy_strat_elapsed_get")
import_all_func_list.append("db_safe_string")
import_all_func_list.append("db_rug_upd")
import_all_func_list.append("db_tbl_del")
import_all_func_list.append("db_tbl_insupd")
import_all_func_list.append("db_tbl_currs_insupd")
import_all_func_list.append("db_tbl_bals_insupd")
import_all_func_list.append("db_tbl_mkts_insupd")
import_all_func_list.append("db_tbl_ords_insupd")
import_all_func_list.append("db_tbl_buy_ords_insupd")
import_all_func_list.append("db_tbl_sell_ords_insupd")
import_all_func_list.append("db_tbl_poss_insupd")
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

from bot_secrets                   import secrets


#<=====>#
# Variables
#<=====>#
lib_name      = 'lib_db'
log_name      = 'lib_db'
lib_verbosity = 1
lib_debug_lvl = 1
verbosity     = 1
debug_lvl     = 1


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

def db_mkts_loop_get(loop_mkts=None, stable_mkts=None, err_mkts=None):
    func_name = 'db_mkts_loop_get'
    func_str = '{}.{}(mkts, stable_mkts, err_mkts)'.format(lib_name, func_name)
#    G(func_str)
    fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
    if verbosity >= 2: print_func_name(func_str, adv=2)

    # products in settings
    sql = ""
    sql += " select m.mkt_id "
    sql += "   , m.mkt_name "
    sql += "   , m.prod_id "
    sql += "   , m.prc "
    sql += "   , m.ask_prc "
    sql += "   , m.buy_prc "
    sql += "   , m.bid_prc "
    sql += "   , m.sell_prc "
    sql += "   , m.prc_mid_mkt "
    sql += "   , m.prc_pct_chg_24h "
    sql += "   , m.vol_24h "
    sql += "   , m.vol_base_24h "
    sql += "   , m.vol_quote_24h "
    sql += "   , m.vol_pct_chg_24h "

#    sql += "   , vmp.prod_id "
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

#    sql += "   , m.mkt_venue "
#    sql += "   , m.ignore_tf "

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

    func_end(fnc, debug_lvl=lib_debug_lvl)
    return mkts

#<=====>#

def db_mkts_loop_top_perfs_prod_ids_get(lmt=None):
    func_name = 'db_mkts_loop_top_perfs_prod_ids_get'
    func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#    G(func_str)
    fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
    if verbosity >= 2: print_func_name(func_str, adv=2)

    sql = " "
    sql += "select x.prod_id "
    sql += "  from cbtrade.view_mkt_perf x "
    sql += "  where 1=1 "
    sql += "  and x.gain_loss_pct_hr > 0 "
    sql += "  order by x.gain_loss_pct_hr desc "
    if lmt:
        sql += "  limit {} ".format(lmt)
    mkts = db.sel(sql)

    print(f'top mkts by perf : {mkts}')

    func_end(fnc, debug_lvl=lib_debug_lvl)
    return mkts

#<=====>#

def db_mkts_loop_top_prc_chg_prod_ids_get(lmt=None):
    func_name = 'db_mkts_loop_top_prc_chg_prod_ids_get'
    func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#    G(func_str)
    fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
    if verbosity >= 2: print_func_name(func_str, adv=2)

    sql = ""
    sql += " select prod_id "
    sql += "   from mkts m  "
    sql += "   where quote_curr_symb = 'USDC'  "
#    sql += "   and base_curr_symb not in ('USDT','GUSD','PYUSD','PAX')  "
#    sql += "   and m.prod_id not in ({})".format(stable_mkts_str)
#    sql += "   and m.prod_id not in ({})".format(err_mkts_str)
    sql += "   and m.prc_pct_chg_24h > 0 "
#    sql += "   and prc_pct_chg_24h > 0 "
#    sql += "   and TIMESTAMPDIFF(HOUR, add_dttm, NOW()) > 24 "
    sql += "   and mkt_status_tf             = 'online' " # varchar(64)
    sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
#    sql += "   and mkt_watched_tf            = 0 " # tinyint default 0
    sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
#    sql += "   and mkt_new_tf                = 0 " # tinyint default 0
    sql += "   and mkt_cancel_only_tf        = 0 " # tinyint default 0
    sql += "   and mkt_limit_only_tf         = 0 " # tinyint default 0
    sql += "   and mkt_post_only_tf          = 0 " # tinyint default 0
    sql += "   and mkt_trading_disabled_tf   = 0 " # tinyint default 0
    sql += "   and mkt_auction_mode_tf       = 0 " # tinyint default 0
    sql += "   order by prc_pct_chg_24h desc "
    if lmt:
        sql += "  limit {} ".format(lmt)
    mkts = db.sel(sql)

    func_end(fnc, debug_lvl=lib_debug_lvl)
    return mkts

#<=====>#

def db_mkts_loop_top_vol_chg_prod_ids_get(lmt=None):
    func_name = 'db_mkts_loop_top_vol_chg_prod_ids_get'
    func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#    G(func_str)
    fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
    if verbosity >= 2: print_func_name(func_str, adv=2)

    sql = ""
    sql += " select prod_id  "
    sql += "   from mkts m "
    sql += "   where quote_curr_symb = 'USDC'  "
#    sql += "   and m.prod_id not in ({})".format(stable_mkts_str)
#    sql += "   and m.prod_id not in ({})".format(err_mkts_str)
#    sql += "   and base_curr_symb not in ('USDT','GUSD','PYUSD','PAX')  "
#    sql += "   and prc_pct_chg_24h > 0 " # intentional
#    sql += "   and TIMESTAMPDIFF(HOUR, add_dttm, NOW()) > 24 "
    sql += "   and mkt_status_tf             = 'online' " # varchar(64)
    sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
#    sql += "   and mkt_watched_tf            = 0 " # tinyint default 0
    sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
#    sql += "   and mkt_new_tf                = 0 " # tinyint default 0
    sql += "   and mkt_cancel_only_tf        = 0 " # tinyint default 0
    sql += "   and mkt_limit_only_tf         = 0 " # tinyint default 0
    sql += "   and mkt_post_only_tf          = 0 " # tinyint default 0
    sql += "   and mkt_trading_disabled_tf   = 0 " # tinyint default 0
    sql += "   and mkt_auction_mode_tf       = 0 " # tinyint default 0
    sql += "   order by vol_quote_24h desc "

    if lmt:
        sql += "  limit {} ".format(lmt)
    mkts = db.sel(sql)

    func_end(fnc, debug_lvl=lib_debug_lvl)
    return mkts

#<=====>#

def db_mkts_loop_top_vol_chg_prod_ids_get(lmt=None):
    func_name = 'db_mkts_loop_top_vol_chg_prod_ids_get'
    func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#    G(func_str)
    fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
    if verbosity >= 2: print_func_name(func_str, adv=2)

    sql = ""
    sql += " select prod_id  "
    sql += "   from mkts m "
    sql += "   where quote_curr_symb = 'USDC'  "
#    sql += "   and base_curr_symb not in ('USDT','GUSD','PYUSD','PAX')  "
#    sql += "   and m.prod_id not in ({})".format(stable_mkts_str)
#    sql += "   and m.prod_id not in ({})".format(err_mkts_str)
#    sql += "   and prc_pct_chg_24h > 0 " # intentional
#    sql += "   and vol_pct_chg_24h > 0 "
#    sql += "   and TIMESTAMPDIFF(HOUR, add_dttm, NOW()) > 24 "
    sql += "   and mkt_status_tf             = 'online' " # varchar(64)
    sql += "   and mkt_view_only_tf          = 0 " # tinyint default 0
#    sql += "   and mkt_watched_tf            = 0 " # tinyint default 0
    sql += "   and mkt_is_disabled_tf        = 0 " # tinyint default 0
#    sql += "   and mkt_new_tf                = 0 " # tinyint default 0
    sql += "   and mkt_cancel_only_tf        = 0 " # tinyint default 0
    sql += "   and mkt_limit_only_tf         = 0 " # tinyint default 0
    sql += "   and mkt_post_only_tf          = 0 " # tinyint default 0
    sql += "   and mkt_trading_disabled_tf   = 0 " # tinyint default 0
    sql += "   and mkt_auction_mode_tf       = 0 " # tinyint default 0
    sql += "   order by vol_pct_chg_24h desc "
    if lmt:
        sql += "  limit {} ".format(lmt)
    mkts = db.sel(sql)

    func_end(fnc, debug_lvl=lib_debug_lvl)
    return mkts

#<=====>#

def db_mkts_loop_watched_prod_ids_get():
    func_name = 'db_mkts_loop_watched_prod_ids_get'
    func_str = f'{lib_name}.{func_name}()'
#    G(func_str)
    fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
    if verbosity >= 2: print_func_name(func_str, adv=2)

    sql = ""
    sql += " select m.prod_id "
    sql += "   from cbtrade.mkts m "
    sql += "   where m.ignore_tf = 0 "
    sql += "   and m.mkt_watched_tf = 1 "
    sql += "   order by m.prod_id "
    mkts = db.sel(sql)

    func_end(fnc, debug_lvl=lib_debug_lvl)
    return mkts

#<=====>#

def db_mkts_loop_poss_open_prod_ids_get():
    func_name = 'db_mkts_loop_poss_open_prod_ids_get'
    func_str = f'{lib_name}.{func_name}()'
#    G(func_str)
    fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
    if verbosity >= 2: print_func_name(func_str, adv=2)

    sql = ""
    sql += " select prod_id "
    sql += "   from poss "
    sql += "   where ignore_tf = 0 "
    sql += "   and pos_stat in ('OPEN','SELL') "
    mkts = db.sel(sql)

    func_end(fnc, debug_lvl=lib_debug_lvl)
    return mkts

#<=====>#

def db_loop_mkts_get_all(loop_mkts=None, stable_mkts=None, err_mkts=None):
	func_name = 'db_loop_mkts_get_all'
	func_str = '{}.{}(mkts, stable_mkts, err_mkts)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	# products in settings
	sql = ""
	sql += " select m.mkt_id "
	sql += "   , m.mkt_name "
	sql += "   , m.prod_id "
	sql += "   , m.prc "
	sql += "   , m.ask_prc "
	sql += "   , m.buy_prc "
	sql += "   , m.bid_prc "
	sql += "   , m.sell_prc "
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_loop_mkts_watched_get_all():
	func_name = 'db_loop_mkts_watched_get_all'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select m.prod_id "
	sql += "   from cbtrade.mkts m "
	sql += "   where m.ignore_tf = 0 "
	sql += "   and m.mkt_watched_tf = 1 "
	sql += "   order by m.prod_id "
	mkts = db.sel(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_loop_mkts_w_poss_open_get_all():
	func_name = 'db_loop_mkts_w_poss_open_get_all'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select prod_id "
	sql += "   from poss "
	sql += "   where ignore_tf = 0 "
	sql += "   and pos_stat in ('OPEN','SELL') "
	mkts = db.sel(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_loop_mkts_top_perfs_get_all(lmt=None):
	func_name = 'db_loop_mkts_top_perfs_get_all'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = " "
	sql += "select x.prod_id "
	sql += "  from cbtrade.view_mkt_perf x "
	sql += "  where 1=1 "
	sql += "  and x.gain_loss_pct_hr > 0 "
	sql += "  order by x.gain_loss_pct_hr desc "
	if lmt:
		sql += "  limit {} ".format(lmt)
	mkts = db.sel(sql)

#	print(f'top mkts by perf : {mkts}')

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_loop_mkts_top_prc_chg_get_all(lmt=None):
	func_name = 'db_loop_mkts_top_prc_chg_get_all'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select prod_id "
	sql += "   from mkts m  "
	sql += "   where quote_curr_symb = 'USDC'  "
#	sql += "   and base_curr_symb not in ('USDT','GUSD','PYUSD','PAX')  "
#	sql += "   and m.prod_id not in ({})".format(stable_mkts_str)
#	sql += "   and m.prod_id not in ({})".format(err_mkts_str)
	sql += "   and m.prc_pct_chg_24h > 0 "
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
		sql += "  limit {} ".format(lmt)
	mkts = db.sel(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_loop_mkts_top_vol_chg_get_all(lmt=None):
	func_name = 'db_loop_mkts_top_vol_chg_get_all'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_loop_mkts_top_vol_chg_pct_get_all(lmt=None):
	func_name = 'db_loop_mkts_top_vol_chg_pct_get_all'
	func_str = '{}.{}(lmt={})'.format(lib_name, func_name, lmt)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_mkt_perf_get(prod_id):
	func_name = 'db_mkt_perf_get'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = "select x.* "
	sql += "  from cbtrade.view_mkt_perf x "
	sql += "  where 1=1 "
#	sql += "  and x.ignore_tf = 0 "
	sql += "  and x.prod_id = '{}' ".format(prod_id)
	mkt_perf = db.seld(sql)
	if mkt_perf:
		mkt_perf = mkt_perf[0]

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkt_perf

#<=====>#

#def db_last_buy_elapsed_get(prod_id):
#	func_name = 'db_last_buy_elapsed_get'
#	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
##	G(func_str)
#	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
#	if verbosity >= 2: print_func_name(func_str, adv=2)
#
#	st = settings_load()
#
#	bo_elapsed = st.spot.buy.buy_delay_minutes
#	sql = ""
#	sql += "select coalesce(TIMESTAMPDIFF(MINUTE, max(bo.buy_begin_dttm), NOW()), 9999) as bo_elapsed "
#	sql += "  from cbtrade.buy_ords bo "
#	sql += "  where 1=1"
#	sql += "  and bo.prod_id = '{}' ".format(prod_id)
##	sql += "  and bo.ord_stat not in ('TIME') "
#	sql += "  and bo.ord_stat in ('OPEN','FILL') "
#	data = db.seld(sql)
#	if data:
#		bo_elapsed = data[0]['bo_elapsed']
#
#	pos_elapsed = st.spot.buy.buy_delay_minutes
#	sql = ""
#	sql += "select coalesce(TIMESTAMPDIFF(MINUTE, max(p.pos_begin_dttm), NOW()), 9999) as pos_elapsed "
#	sql += "  from cbtrade.poss p "
#	sql += "  where 1=1 "
#	sql += "  and p.prod_id = '{}' ".format(prod_id)
#	sql += "  and p.pos_stat not in ('TIME') "
#	data = db.seld(sql)
#	if data:
#		pos_elapsed = data[0]['pos_elapsed']
#	last_elapsed = min(bo_elapsed, pos_elapsed)
#
#	func_end(fnc, debug_lvl=lib_debug_lvl)
#	return last_elapsed

#<=====>#

def db_mkt_strats_stats_open_get(prod_id):
	func_name = 'db_mkt_strats_stats_open_get'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return strats_stats

#<=====>#

def db_mkt_strat_perf_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq):
	func_name = 'db_mkt_strat_perf_get'
	func_str = '{}.{}(prod_id={}, buy_strat_type={}, buy_strat_name={}, buy_strat_freq={})'.format(lib_name, func_name, prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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
	sql += "  , (select coalesce(TIMESTAMPDIFF(MINUTE, max(bo.buy_begin_dttm), NOW()) + 1, 9999)  "
	sql += "       from cbtrade.buy_ords bo "
	sql += "       where bo.ignore_tf = 0 "
	sql += "       and bo.prod_id = x.prod_id "
	sql += "       and bo.buy_strat_type = x.buy_strat_type "
	sql += "       and bo.buy_strat_name = x.buy_strat_name "
	sql += "       and bo.buy_strat_freq = x.buy_strat_freq "
	sql += "       and bo.ord_stat in ('OPEN','FILL') "
	sql += "       ) as bo_elapsed "
	sql += "  , (select coalesce(TIMESTAMPDIFF(MINUTE, max(p.pos_begin_dttm), NOW()) + 1, 9999)  "
	sql += "       from cbtrade.poss p "
	sql += "       where p.ignore_tf = 0 "
	sql += "       and p.prod_id = x.prod_id "
	sql += "       and p.buy_strat_type = x.buy_strat_type "
	sql += "       and p.buy_strat_name = x.buy_strat_name "
	sql += "       and p.buy_strat_freq = x.buy_strat_freq "
	sql += "       and p.pos_stat in ('OPEN','SELL') "
	sql += "       ) as pos_elapsed "
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
	sql += "          where ignore_tf = 0 "
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkt_strat_perf

#<=====>#

#def db_last_buy_strat_elapsed_get(prod_id, strat_name, freq):
#	func_name = 'db_last_buy_strat_elapsed_get'
#	func_str = '{}.{}(prod_id={}, strat_name={}, freq={})'.format(lib_name, func_name, prod_id, strat_name, freq)
##	G(func_str)
#	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
#	if verbosity >= 2: print_func_name(func_str, adv=2)
#
#	st = settings_load()
#
#	bo_strat_elapsed = st.spot.buy.buy_delay_strat_minutes
#	sql = ""
#	sql += "select coalesce(TIMESTAMPDIFF(MINUTE, max(bo.buy_end_dttm), NOW()), 9999) as bo_elapsed "
#	sql += "  from cbtrade.buy_ords bo "
#	sql += "  where 1=1 "
##	sql += "  and bo.ord_stat not in ('TIME') "
#	sql += "  and bo.ord_stat in ('OPEN','FILL') "
#	sql += "  and bo.prod_id = '{}' ".format(prod_id)
#	sql += "  and bo.buy_strat_name = '{}' ".format(strat_name)
#	sql += "  and bo.buy_strat_freq = '{}' ".format(freq)
#	data = db.seld(sql)
#	if data:
#		bo_strat_elapsed = data[0]['bo_elapsed']
#
#	pos_strat_elapsed = st.spot.buy.buy_delay_strat_minutes
#	sql = ""
#	sql += "select coalesce(TIMESTAMPDIFF(MINUTE, max(p.pos_begin_dttm), NOW()), 9999) as pos_elapsed "
#	sql += "  from cbtrade.poss p "
#	sql += "  where 1=1 "
#	sql += "  and p.prod_id = '{}' ".format(prod_id)
#	sql += "  and p.buy_strat_name = '{}' ".format(strat_name)
#	sql += "  and p.buy_strat_freq = '{}' ".format(freq)
#	data = db.seld(sql)
#	if data:
#		pos_strat_elapsed = data[0]['pos_elapsed']
#	last_strat_elapsed = min(bo_strat_elapsed, pos_strat_elapsed)
#
#	func_end(fnc, debug_lvl=lib_debug_lvl)
#	return last_strat_elapsed

#<=====>#

def db_buy_ords_get_by_uuid(buy_order_uuid):
	func_name = 'db_buy_ords_get_by_uuid'
	func_str = '{}.{}(buy_order_uuid={})'.format(lib_name, func_name, buy_order_uuid)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return bo

#<=====>#

def db_sell_ords_get_by_uuid(sell_order_uuid):
	func_name = 'db_sell_ords_get_by_uuid'
	func_str = '{}.{}(sell_order_uuid={})'.format(lib_name, func_name, sell_order_uuid)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return so

#<=====>#

def db_pos_get_by_pos_id(pos_id):
	func_name = 'db_pos_get_by_pos_id'
	func_str = '{}.{}(pos_id={})'.format(lib_name, func_name, pos_id)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return pos

#<=====>#

def db_poss_mkts_get_all(min_trades):
	func_name = 'db_poss_mkts_get_all'
	func_str = f'{lib_name}.{func_name}(min_trades={min_trades})'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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
	sql += "  group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
	sql += f"  having count(*) >= {min_trades} "
	sql += "  order by cnt desc "
	mkts = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_loop_forced_mkts_get():
	func_name = 'db_loop_forced_mkts_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += " select fb.fb_id "
	sql += "   , m.prod_id "
	sql += "   , m.base_curr_symb "
	sql += "   , m.quote_curr_symb "
	sql += "   , m.base_size_incr "
	sql += "   , m.base_size_min "
	sql += "   , m.base_size_max "
	sql += "   , m.buy_prc "
	sql += "   , fb.buy_amt "
	sql += "   , fb.spend_amt "
	sql += "   , 'force' as buy_strat_type "
	sql += "   , 'force' as buy_strat_name "
	sql += "   from cbtrade.force_buy fb "
	sql += "   join cbtrade.mkts m on m.prod_id = fb.prod_id "
	sql += "   where fb.done_tf = 0 "
	mkts = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_mkts_perf_get_all(pos_stat=None):
	func_name = 'db_mkts_perf_get_all'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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
	sql += stat_sql
	sql += "  group by p.prod_id, p.pos_stat  "
	sql += "  order by p.prod_id, p.pos_stat desc "
	mkts = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_strats_w_stats_get_all():
	func_name = 'db_strats_w_stats_get_all'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select distinct buy_strat_type, buy_strat_name, buy_strat_freq "
	sql += "  from cbtrade.poss "
	sql += "  where ignore_tf = 0"
	sql += "  order by buy_strat_type, buy_strat_name, buy_strat_freq "
	strats = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return strats

#<=====>#

def db_strats_perf_get_all(buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None):
	func_name = 'db_strats_perf_get_all'
	func_str = '{}.{}(buy_strat_type={}, buy_strat_name={}, buy_strat_freq={})'.format(lib_name, func_name, buy_strat_type, buy_strat_name, buy_strat_freq)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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
	if buy_strat_type:
		sql = " and p.buy_strat_type = '{}'.format(buy_strat_type) "
	if buy_strat_name:
		sql = " and p.buy_strat_name = '{}'.format(buy_strat_name) "
	if buy_strat_freq:
		sql = " and p.buy_strat_freq = '{}'.format(buy_strat_freq) "
	sql += "  group by p.prod_id, p.pos_stat  "
	sql += "  order by p.prod_id, p.pos_stat desc "
	mkts = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkts

#<=====>#

def db_poss_open_get():
	func_name = 'db_poss_open_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and ignore_tf = 0 "
	sql += "  and pos_stat in ('OPEN','SELL') "
#	sql += "  order by p.prod_id, p.buy_strat_name, p.buy_strat_freq, p.pos_id "
	sql += "  order by p.prod_id, p.pos_id "
	poss = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return poss

#<=====>#

def db_poss_open_recent_get(lmt=None):
	func_name = 'db_poss_open_recent_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and ignore_tf = 0 "
	sql += "  and pos_stat = 'OPEN' "
	sql += "  order by p.pos_begin_dttm desc "
	poss = db.seld(sql)
	if lmt:
		sql += "limit {}".format(lmt)
	poss = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return poss

#<=====>#

def db_poss_close_recent_get(lmt=None):
	func_name = 'db_poss_close_recent_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select p.* "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and ignore_tf = 0 "
	sql += "  and pos_stat = 'CLOSE' "
	sql += "  order by p.pos_begin_dttm desc "
	poss = db.seld(sql)
	if lmt:
		sql += "limit {}".format(lmt)
	poss = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return poss

#<=====>#

def db_poss_close_recent_get(lmt=None):
	func_name = 'db_poss_close_recent_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return poss

#<=====>#

def db_poss_open_max_trade_size_get(prod_id):
	func_name = 'db_poss_open_max_trade_size_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select max(p.buy_cnt) "
	sql += "  from poss p "
	sql += "  where 1=1 "
	sql += "  and p.prod_id = '{}' ".format(prod_id)
	sql += "  and ignore_tf = 0 "
	sql += "  and pos_stat in ('OPEN','SELL') "
	sql += "  order by p.prod_id, p.pos_id "
	trade_size = db.sel(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return trade_size

#<=====>#

def db_pos_open_data_get(buy_order_uuid):
	func_name = 'db_pos_open_data_get'
	func_str = '{}.{}(buy_order_uuid={})'.format(lib_name, func_name, buy_order_uuid)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
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

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return bos

#<=====>#

def db_buy_ords_open_get():
	func_name = 'db_buy_ords_open_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select * "
	sql += "  from buy_ords  "
	sql += "  where 1=1 "
	sql += "  and ord_stat = 'OPEN'  "
	sql += "  and ignore_tf = 0"
	bos = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return bos

#<=====>#

def db_sell_ords_open_get():
	func_name = 'db_sell_ords_open_get'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select * "
	sql += "  from sell_ords  "
	sql += "  where 1=1 "
	sql += "  and ord_stat = 'OPEN' "
	sql += "  and ignore_tf = 0 "
	sql += "  order by so_id "
	sos = db.seld(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return sos

#<=====>#


def db_bal_get_by_symbol(symb):
	func_name = 'db_bal_get_by_symbol'
	func_str = '{}.{}(symb={})'.format(lib_name, func_name, symb)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select bal_avail from bals where symb = '{}'".format(symb)
	bal = db.sel(sql)
	if not bal:
		bal = 0
	bal = float(bal)
#	print(f'{symb} bal : {bal:>.8f}')

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return bal


#<=====>#

def db_mkt_prc_get_by_prod_id(prod_id):
	func_name = 'db_mkt_get'
	func_str = '{}.{}(prod_id={})'.format(lib_name, func_name, prod_id)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "select prc from mkts where prod_id = '{}'".format(prod_id)
	mkt_prc = db.sel(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)
	return mkt_prc

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
	db.execute(sql)

#<=====>#

def db_buy_ords_stat_upd(bo_id, ord_stat):
	func_name = 'db_buy_ords_stat_upd'
	func_str = '{}.{}(bo_id={}, ord_stat={})'.format(lib_name, func_name, bo_id, ord_stat)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = "update buy_ords set ord_stat = '{}' where bo_id = {}".format(ord_stat, bo_id)
	db.execute(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#

def db_sell_ords_stat_upd(so_id, ord_stat):
	func_name = 'db_sell_ords_stat_upd'
	func_str = '{}.{}(so_id={}, ord_stat={})'.format(lib_name, func_name, so_id, ord_stat)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = "update sell_ords set ord_stat = '{}' where so_id = {}".format(ord_stat, so_id)
	db.execute(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#

def db_poss_stat_upd(pos_id, pos_stat):
	func_name = 'db_poss_stat_upd'
	func_str = '{}.{}(pos_id={})'.format(lib_name, func_name, pos_id)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = "update poss set pos_stat = '{}' where pos_id = {}".format(pos_stat, pos_id)
	db.execute(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#

def db_force_buy_done_upd(fb_id):
	func_name = 'db_force_buy_done_upd'
	func_str = '{}.{}(fb_id={})'.format(lib_name, func_name, fb_id)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = "update cbtrade.force_buy set done_tf = 1 where fb_id = {}".format(fb_id)
	db.execute(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#

def db_poss_err_upd(pos_id, pos_stat):
	func_name = 'db_poss_err_upd'
	func_str = '{}.{}(pos_id={})'.format(lib_name, func_name, pos_id)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = "update poss set pos_stat = '{}' where pos_id = {}".format(pos_stat, pos_id)
	db.execute(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#

def db_curr_prc_upd(prc_usd, symb):
	func_name = 'db_curr_prc_upd'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "update cbtrade.currs c"
	sql += "  set c.prc_usd = {} ".format(prc_usd)
	sql += "  where c.symb = '{}' ".format(symb)
	db.execute(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#

def db_curr_prc_stable_upd(stable_symbs=None):
	func_name = 'db_curr_prc_stable_upd'
	func_str = '{}.{}(stable_symbs={})'.format(lib_name, func_name, stable_symbs)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#

def db_curr_prc_mkt_upd():
	func_name = 'db_curr_prc_mkt_upd'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	sql = ""
	sql += "update cbtrade.currs c "
	sql += "  set c.prc_usd = coalesce((select m.prc"
	sql += "                              from cbtrade.mkts m "
	sql += "                              where m.base_curr_symb = c.symb"
	sql += "                              and m.quote_curr_symb = 'USDC'),0)"
	db.execute(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)


#<=====>#

def db_tbl_insupd(table_name, in_data):
	func_name = 'db_tbl_insupd'
	func_str = '{}.{}(table_name={}, in_data)'.format(lib_name, func_name, table_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

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
	if ins_type == 'one':
		db.ins_one(sql=sql, vals=ins_data)
	else:
		db.ins_many(sql=sql, vals=ins_data)

#	print(sql)

	func_end(fnc, debug_lvl=lib_debug_lvl)


#<=====>#


def db_tbl_currs_insupd(in_data):
	func_name = 'db_tbl_currs_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	table_name = 'currs'
	db_tbl_del(table_name=table_name)
	db_tbl_insupd(table_name, in_data)

	func_end(fnc, debug_lvl=lib_debug_lvl)


#<=====>#


def db_tbl_bals_insupd(in_data):
	func_name = 'db_tbl_bals_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	table_name = 'bals'
	db_tbl_del(table_name=table_name)
	db_tbl_insupd(table_name, in_data)

	func_end(fnc, debug_lvl=lib_debug_lvl)


#<=====>#


def db_tbl_mkts_insupd(in_data):
	func_name = 'db_tbl_mkts_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

#	data = []
#	for mkt in in_data:
##		mkt['mkt_status_tf']           = tf2int(mkt['mkt_status_tf'])
#		mkt['mkt_view_only_tf']        = tf2int(mkt['mkt_view_only_tf'])
#		mkt['mkt_watched_tf']          = tf2int(mkt['mkt_watched_tf'])
#		mkt['mkt_is_disabled_tf']      = tf2int(mkt['mkt_is_disabled_tf'])
#		mkt['mkt_new_tf']              = tf2int(mkt['mkt_new_tf'])
#		mkt['mkt_cancel_only_tf']      = tf2int(mkt['mkt_cancel_only_tf'])
#		mkt['mkt_limit_only_tf']       = tf2int(mkt['mkt_limit_only_tf'])
#		mkt['mkt_post_only_tf']        = tf2int(mkt['mkt_post_only_tf'])
#		mkt['mkt_trading_disabled_tf'] = tf2int(mkt['mkt_trading_disabled_tf'])
#		mkt['mkt_auction_mode_tf']     = tf2int(mkt['mkt_auction_mode_tf'])
#		print(mkt)
#		data.append(mkt)
#	in_data=data

	table_name = 'mkts'
	# I like deleting this just in case old products have been dropped
	# however I need to leave add_dttm as is, since coinbase does not 
	# have a listing data.  If the coin has not been listed long, we
	# cannot pull OHLCV data.  So I am filtering on add_dttm from this
	# table, meaning I can't delete before repopulating...
#	db_tbl_del(table_name=table_name)
	db_tbl_insupd(table_name, in_data)

	func_end(fnc, debug_lvl=lib_debug_lvl)


#<=====>#


def db_tbl_ords_insupd(in_data):
	func_name = 'db_tbl_ords_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	table_name = 'ords'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc, debug_lvl=lib_debug_lvl)


#<=====>#


def db_tbl_buy_ords_insupd(in_data):
	func_name = 'db_tbl_buy_ords_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	table_name = 'buy_ords'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc, debug_lvl=lib_debug_lvl)


#<=====>#


def db_tbl_sell_ords_insupd(in_data):
	func_name = 'db_tbl_sell_ords_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	table_name = 'sell_ords'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc, debug_lvl=lib_debug_lvl)


#<=====>#


def db_tbl_poss_insupd(in_data):
	func_name = 'db_tbl_poss_insupd'
	func_str = '{}.{}(in_data)'.format(lib_name, func_name)
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	table_name = 'poss'
	db_tbl_insupd(table_name, in_data)

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#

def db_table_csvs_dump():
	func_name = 'db_table_csvs_dump'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name, logname=log_name, debug_lvl=lib_debug_lvl)
	if verbosity >= 2: print_func_name(func_str, adv=2)

	tbl_list = ['bals','buy_ords','currs','mkts','ords','sell_ords']
	print('')
	for tbl in tbl_list:
		sql = "select * from {}".format(tbl)
		res = db.seld(sql)
		df = pd.DataFrame(res)
		csv_fname = 'csvs/{}_table.csv'.format(tbl)
		df.to_csv(csv_fname, index=True)
		print('{} saved...'.format(csv_fname))
	print('')

	func_end(fnc, debug_lvl=lib_debug_lvl)

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
