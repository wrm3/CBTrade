#<=====>#
# Description
#<=====>#


#<=====>#
# Import All
#<=====>#

import_all_func_list = []
import_all_func_list.append("ddb_check_tables")
import_all_func_list.append("ddb_check_ohlcv_table")
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
from pprint import pprint

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
from cls_db_duckdb                 import db_duckdb

from lib_common                    import *
from lib_colors                    import *

#from bot_common                    import *
from bot_secrets                   import secrets

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_ddb'
log_name      = 'bot_ddb'
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
ddb = db_duckdb('db/cbtrade.ddb')

#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

'''
import duckdb

# Connect to the first DuckDB database
conn = duckdb.connect('database1.duckdb')

# Attach the second DuckDB database
conn.execute("ATTACH 'database2.duckdb' AS db2;")

# Now, you can query across both databases
result = conn.execute("""
    SELECT users.name, orders.order_id
    FROM users
    JOIN db2.orders ON users.user_id = orders.user_id;
""").fetchall()

print(result)
'''


#<=====>#

def ddb_check_tables():
	func_name = 'ddb_check_tables'
	G(func_name)

	ddb_table_currs()
	ddb_table_bals()
	ddb_table_mkts()
	ddb_table_force_buy()
	ddb_table_buy_strats()
	ddb_table_buy_ords()
	ddb_table_sell_ords()
	ddb_table_poss()
	ddb_table_buy_signs()
	ddb_table_sell_signs()
	ddb_table_ords()
#	ddb_check_ohlcv_table()


#<=====>#

def ddb_check_ohlcv_table(prod_id, freq):
	func_name = 'ddb_check_ohlcv_table'
	G(func_name)

	prod_id = prod_id.replace('-','_')

	sql = ''
	sql += 'create table if not exists '
	sql += f'ohlcv_{prod_id}_{freq} ('
	sql += 'timestamp timestamp, '
	sql += 'freq VARCHAR(64), '
	sql += 'open   DECIMAL(36, 12),'
	sql += 'high   DECIMAL(36, 12), '
	sql += 'low    DECIMAL(36, 12), '
	sql += 'close  DECIMAL(36, 12), '
	sql += 'volume DECIMAL(36, 12)'
	sql += ');'

	ddb.execute(sql)

#<=====>#

def ddb_table_currs():
	func_name = 'ddb_table_currs'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_curr_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS currs ("
	sql +="    curr_id                           INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_curr_id'),"
	sql +="    symb                              VARCHAR(64),"
	sql +="    name                              VARCHAR(64),"
	sql +="    curr_uuid                         VARCHAR(64),"
	sql +="    prc_usd                           DECIMAL(36, 12) DEFAULT 0,"
	sql +="    create_dttm                       TIMESTAMP,"
	sql +="    update_dttm                       TIMESTAMP,"
	sql +="    delete_dttm                       TIMESTAMP,"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(curr_uuid)"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_bals():
	func_name = 'ddb_table_bals'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_bal_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS bals ("
	sql +="    bal_id                            INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_bal_id'),"
	sql +="    curr_uuid                         VARCHAR(64),"
	sql +="    symb                              VARCHAR(64),"
	sql +="    name                              VARCHAR(64),"
	sql +="    bal_avail                         DECIMAL(36, 12) DEFAULT 0,"
	sql +="    bal_hold                          DECIMAL(36, 12) DEFAULT 0,"
	sql +="    bal_tot                           DECIMAL(36, 12) DEFAULT 0,"
	sql +="    rp_id                             VARCHAR(64),"
	sql +="    default_tf                        BOOLEAN DEFAULT 0,"
	sql +="    active_tf                         BOOLEAN DEFAULT 0,"
	sql +="    ready_tf                          BOOLEAN DEFAULT 0,"
	sql +="    create_dttm                       TIMESTAMP,"
	sql +="    update_dttm                       TIMESTAMP,"
	sql +="    delete_dttm                       TIMESTAMP,"
	sql +="    curr_prc_usd                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    curr_val_usd                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    del_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(curr_uuid)"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_mkts():
	func_name = 'ddb_table_mkts'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_mkt_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS mkts ("
	sql +="    mkt_id                            INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_mkt_id'),"
	sql +="    mkt_name                          VARCHAR(64),"
	sql +="    prod_id                           VARCHAR(64),"
	sql +="    mkt_venue                         VARCHAR(64),"
	sql +="    base_curr_symb                    VARCHAR(64),"
	sql +="    base_curr_name                    VARCHAR(64),"
	sql +="    base_size_incr                    DECIMAL(36, 12),"
	sql +="    base_size_min                     DECIMAL(36, 12),"
	sql +="    base_size_max                     DECIMAL(36, 12),"
	sql +="    quote_curr_symb                   VARCHAR(64),"
	sql +="    quote_curr_name                   VARCHAR(64),"
	sql +="    quote_size_incr                   DECIMAL(36, 12),"
	sql +="    quote_size_min                    DECIMAL(36, 12),"
	sql +="    quote_size_max                    DECIMAL(36, 12),"
	sql +="    mkt_status_tf                     VARCHAR(64),"
	sql +="    mkt_view_only_tf                  BOOLEAN DEFAULT 0,"
	sql +="    mkt_watched_tf                    BOOLEAN DEFAULT 0,"
	sql +="    mkt_is_disabled_tf                BOOLEAN DEFAULT 0,"
	sql +="    mkt_new_tf                        BOOLEAN DEFAULT 0,"
	sql +="    mkt_cancel_only_tf                BOOLEAN DEFAULT 0,"
	sql +="    mkt_limit_only_tf                 BOOLEAN DEFAULT 0,"
	sql +="    mkt_post_only_tf                  BOOLEAN DEFAULT 0,"
	sql +="    mkt_trading_disabled_tf           BOOLEAN DEFAULT 0,"
	sql +="    mkt_auction_mode_tf               BOOLEAN DEFAULT 0,"
	sql +="    prc                               DECIMAL(36, 12),"
	sql +="    prc_ask                           DECIMAL(36, 12),"
	sql +="    prc_buy                           DECIMAL(36, 12),"
	sql +="    prc_bid                           DECIMAL(36, 12),"
	sql +="    prc_sell                          DECIMAL(36, 12),"
	sql +="    prc_mid_mkt                       DECIMAL(36, 12),"
	sql +="    prc_pct_chg_24h                   DECIMAL(36, 12),"
	sql +="    vol_24h                           DECIMAL(36, 12),"
	sql +="    vol_base_24h                      DECIMAL(36, 12),"
	sql +="    vol_quote_24h                     DECIMAL(36, 12),"
	sql +="    vol_pct_chg_24h                   DECIMAL(36, 12),"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(prod_id)"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_force_buy():
	func_name = 'ddb_table_force_buy'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_fb_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS force_buy ("
	sql +="    fb_id                             INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_fb_id'),"
	sql +="    prod_id                           VARCHAR(64),"
	sql +="    base_symb                         VARCHAR(64),"
	sql +="    quote_symb                        VARCHAR(64),"
	sql +="    buy_amt                           DECIMAL(36, 12) DEFAULT 0,"
	sql +="    spend_amt                         DECIMAL(36, 12) DEFAULT 0,"
	sql +="    done_tf                           BOOLEAN DEFAULT 0,"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_buy_strats():
	func_name = 'ddb_table_buy_strats'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_bs_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS buy_strats ("
	sql +="    bs_id                             INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_bs_id'),"
	sql +="    buy_strat_type                    VARCHAR(64),"
	sql +="    buy_strat_name                    VARCHAR(64),"
	sql +="    buy_strat_desc                    VARCHAR(64),"
	sql +="    buy_strat_freq                    VARCHAR(64),"
	sql +="    freq_desc                         VARCHAR(64),"
	sql +="    freq_seconds                      INTEGER,"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
	sql +=");"
	ddb.execute(sql)

#	sql = "select * from buy_strats"
#	r = ddb.db.sql(sql).fetchall()
#	pprint(r)


	# -- Insert strategy values into buy_strats table"
	sql = ""
	sql += "insert into buy_strats ( buy_strat_type, buy_strat_name, buy_strat_desc, buy_strat_freq, freq_desc, freq_seconds ) "
	sql += "select strats.buy_strat_type, strats.buy_strat_name, strats.buy_strat_desc, freqs.buy_strat_freq, freqs.freq_desc, freqs.freq_seconds "
	sql += "from ( "
	sql += "select 'up' as buy_strat_type, 'sha'      as buy_strat_name, 'double smoothed heikin ashi' as buy_strat_desc "
	sql += "union "
	sql += "select 'up' as buy_strat_type, 'imp_macd' as buy_strat_name, 'impulse macd'                as buy_strat_desc "
	sql += "union "
	sql += "select 'up' as buy_strat_type, 'bb_bo'    as buy_strat_name, 'bollinger band breakout'     as buy_strat_desc "
	sql += "union "
	sql += "select 'up' as buy_strat_type, 'emax'     as buy_strat_name, 'triple ema crossover'        as buy_strat_desc "
	sql += "union "
	sql += "select 'dn' as buy_strat_type, 'bb'       as buy_strat_name, 'bollinger band'              as buy_strat_desc "
	sql += "union "
	sql += "select 'dn' as buy_strat_type, 'drop'     as buy_strat_name, 'buy the dip'                 as buy_strat_desc "
	sql += ") strats"
	sql += ", (select '15min' as buy_strat_freq, '15 minute' as freq_desc, 900 as freq_seconds "
	sql += "union "
	sql += "select '30min' as buy_strat_freq, '30 minute' as freq_desc, 1800 as freq_seconds "
	sql += "union "
	sql += "select '1h'    as buy_strat_freq, '1 hour'    as freq_desc, 3600 as freq_seconds "
	sql += "union "
	sql += "select '4h'    as buy_strat_freq, '4 hour'    as freq_desc, 14400 as freq_seconds "
	sql += "union "
	sql += "select '1d'    as buy_strat_freq, '1 day'     as freq_desc, 86400 as freq_seconds "
	sql += " ) freqs "
	sql += "  order by freqs.freq_seconds, strats.buy_strat_type desc, strats.buy_strat_name"
	r = ddb.db.sql(sql)
#	pprint(r)


#<=====>#

def ddb_table_buy_ords():
	func_name = 'ddb_table_buy_ords'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_bo_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS buy_ords ("
	sql +="    bo_id                             INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_bo_id'),"
	sql +="    test_tf                           BOOLEAN DEFAULT 0,"
	sql +="    prod_id                           VARCHAR(64),"
	sql +="    mkt_name                          VARCHAR(64),"
	sql +="    mkt_venue                         VARCHAR(64),"
	sql +="    buy_order_uuid                    VARCHAR(64),"
	sql +="    buy_client_order_id               VARCHAR(64),"
	sql +="    pos_type                          VARCHAR(64),"
	sql +="    ord_stat                          VARCHAR(64),"
	sql +="    buy_strat_type                    VARCHAR(64),"
	sql +="    buy_strat_name                    VARCHAR(64),"
	sql +="    buy_strat_freq                    VARCHAR(64),"
	sql +="    buy_asset_type                    VARCHAR(64),"
	sql +="    buy_begin_dttm                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    buy_end_dttm                      TIMESTAMP,"
	sql +="    buy_curr_symb                     VARCHAR(64),"
	sql +="    spend_curr_symb                   VARCHAR(64),"
	sql +="    fees_curr_symb                    VARCHAR(64),"
	sql +="    buy_cnt_est                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    buy_cnt_act                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    fees_cnt_act                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    tot_out_cnt                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_buy_est                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_buy_act                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    tot_prc_buy                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_buy_slip_pct                  DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(buy_order_uuid)"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_sell_ords():
	func_name = 'ddb_table_sell_ords'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_so_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS sell_ords ("
	sql +="    so_id                             INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_so_id'),"
	sql +="    test_tf                           BOOLEAN DEFAULT 0,"
	sql +="    prod_id                           VARCHAR(64),"
	sql +="    mkt_name                          VARCHAR(64),"
	sql +="    mkt_venue                         VARCHAR(64),"
	sql +="    pos_id                            INT,"
	sql +="    sell_seq_nbr                      INT,"
	sql +="    sell_order_uuid                   VARCHAR(64),"
	sql +="    sell_client_order_id              VARCHAR(64),"
	sql +="    pos_type                          VARCHAR(64),"
	sql +="    ord_stat                          VARCHAR(64),"
	sql +="    sell_strat_type                   VARCHAR(64),"
	sql +="    sell_strat_name                   VARCHAR(64),"
	sql +="    sell_strat_freq                   VARCHAR(64),"
	sql +="    sell_asset_type                   VARCHAR(64),"
	sql +="    sell_begin_dttm                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    sell_end_dttm                     TIMESTAMP,"
	sql +="    sell_curr_symb                    VARCHAR(64),"
	sql +="    recv_curr_symb                    VARCHAR(64),"
	sql +="    fees_curr_symb                    VARCHAR(64),"
	sql +="    sell_cnt_est                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    sell_cnt_act                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    fees_cnt_act                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    tot_in_cnt                        DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_sell_est                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_sell_act                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    tot_prc_buy                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_sell_slip_pct                 DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(sell_order_uuid)"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_poss():
	func_name = 'ddb_table_poss'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_pos_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS poss ("
	sql +="    pos_id                            INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_pos_id'),"
	sql +="    prod_id                           VARCHAR(64),"
	sql +="    pos_stat                          VARCHAR(64),"
	sql +="    pos_begin_dttm                    TIMESTAMP,"
	sql +="    pos_end_dttm                      TIMESTAMP,"
	sql +="    age_mins                          INT DEFAULT 0,"
	sql +="    tot_out_cnt                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    tot_in_cnt                        DECIMAL(36, 12) DEFAULT 0,"
	sql +="    buy_fees_cnt                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    sell_fees_cnt_tot                 DECIMAL(36, 12) DEFAULT 0,"
	sql +="    fees_cnt_tot                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    buy_cnt                           DECIMAL(36, 12) DEFAULT 0,"
	sql +="    sell_cnt_tot                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    hold_cnt                          DECIMAL(36, 12) DEFAULT 0,"
	sql +="    pocket_cnt                        DECIMAL(36, 12) DEFAULT 0,"
	sql +="    clip_cnt                          DECIMAL(36, 12) DEFAULT 0,"
	sql +="    pocket_pct                        DECIMAL(36, 12) DEFAULT 0,"
	sql +="    clip_pct                          DECIMAL(36, 12) DEFAULT 0,"
	sql +="    sell_order_cnt                    INT DEFAULT 0,"
	sql +="    sell_order_attempt_cnt            INT DEFAULT 0,"
	sql +="    prc_buy                           DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_curr                          DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_high                          DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_low                           DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_chg_pct                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_chg_pct_high                  DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_chg_pct_low                   DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_chg_pct_drop                  DECIMAL(36, 12) DEFAULT 0,"
	sql +="    prc_sell_avg                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    val_curr                          DECIMAL(36, 12) DEFAULT 0,"
	sql +="    val_tot                           DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_amt_est                 DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_amt_est_high            DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_amt_est_low             DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_amt                     DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_amt_net                 DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_pct_est                 DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_pct_est_high            DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_pct_est_low             DECIMAL(36, 12) DEFAULT 0,"
	sql +="    gain_loss_pct                     DECIMAL(36, 12) DEFAULT 0,"
	sql +="    buy_strat_type                    VARCHAR(64),"
	sql +="    buy_strat_name                    VARCHAR(64),"
	sql +="    buy_strat_freq                    VARCHAR(64),"
	sql +="    sell_strat_type                   VARCHAR(64),"
	sql +="    sell_strat_name                   VARCHAR(64),"
	sql +="    sell_strat_freq                   VARCHAR(64),"
	sql +="    bo_id                             INT,"
	sql +="    bo_uuid                           VARCHAR(64),"
	sql +="    buy_curr_symb                     VARCHAR(64),"
	sql +="    spend_curr_symb                   VARCHAR(64),"
	sql +="    sell_curr_symb                    VARCHAR(64),"
	sql +="    recv_curr_symb                    VARCHAR(64),"
	sql +="    fees_curr_symb                    VARCHAR(64),"
	sql +="    base_curr_symb                    VARCHAR(64),"
	sql +="    base_size_incr                    DECIMAL(36, 12),"
	sql +="    base_size_min                     DECIMAL(36, 12),"
	sql +="    base_size_max                     DECIMAL(36, 12),"
	sql +="    quote_curr_symb                   VARCHAR(64),"
	sql +="    quote_size_incr                   DECIMAL(36, 12),"
	sql +="    quote_size_min                    DECIMAL(36, 12),"
	sql +="    quote_size_max                    DECIMAL(36, 12),"
	sql +="    test_tf                           BOOLEAN DEFAULT 0,"
	sql +="    force_sell_tf                     BOOLEAN DEFAULT 0,"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    reason                            VARCHAR(1024),"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    mkt_name                          VARCHAR(64),"
	sql +="    mkt_venue                         VARCHAR(64),"
	sql +="    pos_type                          VARCHAR(64),"
	sql +="    buy_asset_type                    VARCHAR(64),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    del_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(bo_uuid)"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_buy_signs():
	func_name = 'ddb_table_buy_signs'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_bus_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS buy_signs ("
	sql +="    bus_id                            INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_bus_id'),"
	sql +="    test_tf                           BOOLEAN DEFAULT 0,"
	sql +="    prod_id                           VARCHAR(64),"
	sql +="    buy_strat_type                    VARCHAR(64),"
	sql +="    buy_strat_name                    VARCHAR(64),"
	sql +="    buy_strat_freq                    VARCHAR(64),"
	sql +="    buy_yn                            CHAR(1),"
	sql +="    wait_yn                           CHAR(1),"
	sql +="    bus_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    buy_curr_symb                     VARCHAR(64),"
	sql +="    spend_curr_symb                   VARCHAR(64),"
	sql +="    fees_curr_symb                    VARCHAR(64),"
	sql +="    buy_cnt_est                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    buy_prc_est                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    buy_sub_tot_est                   DECIMAL(36, 12) DEFAULT 0,"
	sql +="    buy_fees_est                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    buy_tot_est                       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    all_passes                        VARCHAR(2048),"
	sql +="    all_fails                         VARCHAR(2048),"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, bus_dttm)"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_sell_signs():
	func_name = 'ddb_table_sell_signs'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_sus_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS sell_signs ("
	sql +="    sus_id                            INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_sus_id'),"
	sql +="    test_tf                           BOOLEAN DEFAULT 0,"
	sql +="    prod_id                           VARCHAR(64),"
	sql +="    pos_id                            INT,"
	sql +="    sell_strat_type                   VARCHAR(64),"
	sql +="    sell_strat_name                   VARCHAR(64),"
	sql +="    sell_strat_freq                   VARCHAR(64),"
	sql +="    sell_asset_type                   VARCHAR(64),"
	sql +="    sell_yn                           CHAR(1),"
	sql +="    hodl_yn                           CHAR(1),"
	sql +="    sus_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    sell_curr_symb                    VARCHAR(64),"
	sql +="    recv_curr_symb                    VARCHAR(64),"
	sql +="    fees_curr_symb                    VARCHAR(64),"
	sql +="    sell_cnt_est                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    sell_prc_est                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    sell_sub_tot_est                  DECIMAL(36, 12) DEFAULT 0,"
	sql +="    sell_fees_est                     DECIMAL(36, 12) DEFAULT 0,"
	sql +="    sell_tot_est                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    all_sells                         VARCHAR(2048),"
	sql +="    all_hodls                         VARCHAR(2048),"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(prod_id, pos_id, sell_strat_type, sell_strat_name, sell_strat_freq, sus_dttm)"
	sql +=");"
	ddb.execute(sql)

#<=====>#

def ddb_table_ords():
	func_name = 'ddb_table_ords'
	G(func_name)

	sql ="CREATE SEQUENCE IF NOT EXISTS seq_ord_id START 1;"
	ddb.execute(sql)

	sql = ""
	sql +="CREATE TABLE IF NOT EXISTS ords ("
	sql +="    ord_id                            INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_ord_id'),"
	sql +="    ord_uuid                          VARCHAR(256),"
	sql +="    mkt_id                            INT,"
	sql +="    pos_id                            INT,"
	sql +="    buy_order_id                      INT,"
	sql +="    sell_order_id                     INT,"
	sql +="    prod_id                           VARCHAR(64),"
	sql +="    ord_bs                            VARCHAR(64),"
	sql +="    ord_cfg                           VARCHAR(1024),"
	sql +="    ord_base_size                     DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_end_time                      TIMESTAMP,"
	sql +="    ord_limit_prc                     DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_post_only                     BOOLEAN DEFAULT 0,"
	sql +="    ord_quote_size                    DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_stop_dir                      VARCHAR(64),"
	sql +="    ord_stop_prc                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_stop_trigger_prc              DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_type                          VARCHAR(64),"
	sql +="    order_id                          VARCHAR(64),"
	sql +="    ord_product_id                    VARCHAR(64),"
	sql +="    ord_user_id                       VARCHAR(64),"
	sql +="    ord_order_configuration           VARCHAR(1024),"
	sql +="    ord_side                          VARCHAR(64),"
	sql +="    ord_client_order_id               VARCHAR(64),"
	sql +="    ord_status                        VARCHAR(64),"
	sql +="    ord_time_in_force                 VARCHAR(64),"
	sql +="    ord_created_time                  TIMESTAMP,"
	sql +="    ord_completion_percentage         DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_filled_size                   DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_average_filled_price          DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_fee                           DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_number_of_fills               INT,"
	sql +="    ord_filled_value                  DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_pending_cancel                BOOLEAN DEFAULT 0,"
	sql +="    ord_size_in_quote                 BOOLEAN DEFAULT 0,"
	sql +="    ord_total_fees                    DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_size_inclusive_of_fees        BOOLEAN DEFAULT 0,"
	sql +="    ord_total_value_after_fees        DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_trigger_status                VARCHAR(64),"
	sql +="    ord_order_type                    VARCHAR(64),"
	sql +="    ord_reject_reason                 VARCHAR(64),"
	sql +="    ord_settled                       BOOLEAN DEFAULT 0,"
	sql +="    ord_product_type                  VARCHAR(64),"
	sql +="    ord_reject_message                VARCHAR(1024),"
	sql +="    ord_cancel_message                VARCHAR(1024),"
	sql +="    ord_order_placement_source        VARCHAR(64),"
	sql +="    ord_outstanding_hold_amount       DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_is_liquidation                BOOLEAN DEFAULT 0,"
	sql +="    ord_last_fill_time                TIMESTAMP,"
	sql +="    ord_edit_history                  VARCHAR(1024),"
	sql +="    ord_leverage                      DECIMAL(36, 12) DEFAULT 0,"
	sql +="    ord_margin_type                   VARCHAR(64),"
	sql +="    ord_retail_portfolio_id           VARCHAR(64),"
	sql +="    ignore_tf                         BOOLEAN DEFAULT 0,"
	sql +="    note1                             VARCHAR(1024),"
	sql +="    note2                             VARCHAR(1024),"
	sql +="    note3                             VARCHAR(1024),"
	sql +="    add_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    upd_dttm                          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    dlm                               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	sql +="    UNIQUE(ord_uuid)"
	sql +=");"
	ddb.execute(sql)

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#
