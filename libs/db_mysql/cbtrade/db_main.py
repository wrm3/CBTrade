#<=====>#
# Description
#<=====>#
"""
CBTrade Database Main Module - MySQL Implementation
"""
 
#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Public
#<=====>#
import importlib
import os
import sys
import time
import traceback
from datetime import datetime
from dotenv import load_dotenv
from fstrent_colors import G
from pprint import pprint
from typing import Dict, List, Tuple


#<=====>#
# Imports - Project
#<=====>#
from libs.db_mysql.mysql_handler import MySQLDB
from libs.common import (
    AttrDict
    , AttrDictConv
    , AttrDictEnh
    , dttm_get
    , dttm_unix
    , beep, DictValCheck, narc
)


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.db_main'
log_name      = 'cbtrade.db_main'


# <=====>#
# Assignments Pre
# <=====>#
debug_tf = False

# Initialize database connection using unified library
load_dotenv()
DB_PATH = os.getenv('DB_PATH', 'db/cbtrade.db')



#<=====>#
# Classes
#<=====>#

class CBTRADE_DB(MySQLDB):

    # db_common
    from libs.db_mysql.cbtrade.db_common import to_scalar_dict
    to_scalar_dict                     = to_scalar_dict


    # db_read
    from libs.db_mysql.cbtrade.db_read import (
        db_sell_ords_problems_get
        , db_sell_double_check
    )
    db_sell_ords_problems_get          = db_sell_ords_problems_get
    db_sell_double_check               = db_sell_double_check


    # db_reports
    from libs.db_mysql.cbtrade.db_reports import (
        db_closed_overview_recent_test
        , db_closed_overview_recent_live
        , db_strats_w_stats_get_all
        , db_strats_perf_get_all
        , db_poss_open_recent_get
        , db_poss_closed_recent_get
        , db_poss_open_get
    )
    db_closed_overview_recent_test     = db_closed_overview_recent_test
    db_closed_overview_recent_live     = db_closed_overview_recent_live
    db_strats_w_stats_get_all          = db_strats_w_stats_get_all
    db_strats_perf_get_all             = db_strats_perf_get_all
    db_poss_open_recent_get            = db_poss_open_recent_get
    db_poss_closed_recent_get          = db_poss_closed_recent_get
    db_poss_open_get                   = db_poss_open_get


    # tbl_bals
    from libs.db_mysql.cbtrade.tbl_bals import  (
        db_bals_exists
        , db_bals_trigs
        , db_bals_get
        , db_bals_insupd
        , db_bals_prc_mkt_upd
    )
    db_bals_exists                     = db_bals_exists
    db_bals_trigs                      = db_bals_trigs
    db_bals_get                        = db_bals_get
    db_bals_insupd                     = db_bals_insupd
    db_bals_prc_mkt_upd                = db_bals_prc_mkt_upd


    # tbl_buy_decisions
    from libs.db_mysql.cbtrade.tbl_buy_decisions import  (
        db_buy_decisions_exists
        , db_buy_decisions_ins
        , db_buy_decisions_cleanup_old
    )
    db_buy_decisions_exists            = db_buy_decisions_exists
    db_buy_decisions_ins               = db_buy_decisions_ins
    db_buy_decisions_cleanup_old       = db_buy_decisions_cleanup_old

    # tbl_buy_signals
    from libs.db_mysql.cbtrade.tbl_buy_signals import (
        db_buy_signals_exists
        , db_buy_signals_ins
        , db_buy_signals_cleanup_old
    )
    db_buy_signals_exists              = db_buy_signals_exists
    db_buy_signals_ins                 = db_buy_signals_ins
    db_buy_signals_cleanup_old         = db_buy_signals_cleanup_old

    # tbl_buy_ords
    from libs.db_mysql.cbtrade.tbl_buy_ords import  (
        db_buy_ords_exists
        , db_buy_ords_trigs
        , db_buy_ords_get
        , db_buy_ords_open_get
        , db_buy_ords_insupd
        , db_buy_ords_stat_upd
        , db_buy_check_get
        , db_mkt_sizing_data_get_by_uuid
    )
    db_buy_ords_exists                 = db_buy_ords_exists
    db_buy_ords_trigs                  = db_buy_ords_trigs
    db_buy_ords_get                    = db_buy_ords_get
    db_buy_ords_open_get               = db_buy_ords_open_get
    db_buy_ords_insupd                 = db_buy_ords_insupd
    db_buy_ords_stat_upd               = db_buy_ords_stat_upd
    db_buy_check_get                   = db_buy_check_get
    db_mkt_sizing_data_get_by_uuid     = db_mkt_sizing_data_get_by_uuid

    # tbl_buy_strats
    from libs.db_mysql.cbtrade.tbl_buy_strats import  (
        db_buy_strats_exists
        , db_buy_strats_get
        , db_buy_strats_insupd
    )
    db_buy_strats_exists               = db_buy_strats_exists
    db_buy_strats_get                   = db_buy_strats_get
    db_buy_strats_insupd                = db_buy_strats_insupd


    # tbl_currs
    from libs.db_mysql.cbtrade.tbl_currs import  (
        db_currs_exists
        , db_currs_trigs
        , db_currs_get
        , db_currs_insupd
        , db_currs_prc_upd
        , db_currs_prc_stable_upd
        , db_currs_prc_mkt_upd
    )
    # tbl_currs
    db_currs_exists                  = db_currs_exists
    db_currs_trigs                   = db_currs_trigs
    db_currs_get                   = db_currs_get
    db_currs_insupd                = db_currs_insupd
    db_currs_prc_upd               = db_currs_prc_upd
    db_currs_prc_stable_upd        = db_currs_prc_stable_upd
    db_currs_prc_mkt_upd           = db_currs_prc_mkt_upd



    from libs.db_mysql.cbtrade.tbl_mkt_checks import  (
        db_mkt_checks_exists
        , db_mkt_checks_trigs
        , db_mkt_checks_get
        , db_mkt_checks_insupd
        , db_mkt_checks_buy_upd
        , db_mkt_checks_sell_upd
    )
    # tbl_mkt_checks
    db_mkt_checks_exists               = db_mkt_checks_exists
    db_mkt_checks_trigs                = db_mkt_checks_trigs
    db_mkt_checks_get                  = db_mkt_checks_get
    db_mkt_checks_insupd               = db_mkt_checks_insupd
    db_mkt_checks_buy_upd              = db_mkt_checks_buy_upd
    db_mkt_checks_sell_upd             = db_mkt_checks_sell_upd

    # tbl_mkts
    from libs.db_mysql.cbtrade.tbl_mkts import  (
        db_mkts_exists
        , db_mkts_trigs
        , db_mkts_get
        , db_mkt_prc_get
        , db_mkts_open_cnt_get
        , db_pairs_loop_get
        , db_pairs_loop_top_prc_chg_prod_ids_get
        , db_pairs_loop_top_vol_chg_prod_ids_get
        , db_pairs_loop_top_vol_chg_pct_prod_ids_get
        , db_pairs_loop_watched_prod_ids_get
        , db_mkts_insupd

    )

    # tbl_mkts
    db_mkts_exists                   = db_mkts_exists
    db_mkts_trigs                   = db_mkts_trigs
    db_mkts_get                   = db_mkts_get
    db_mkt_prc_get                = db_mkt_prc_get
    db_mkts_open_cnt_get          = db_mkts_open_cnt_get
    db_pairs_loop_get             = db_pairs_loop_get
    db_pairs_loop_top_prc_chg_prod_ids_get     = db_pairs_loop_top_prc_chg_prod_ids_get
    db_pairs_loop_top_vol_chg_prod_ids_get     = db_pairs_loop_top_vol_chg_prod_ids_get
    db_pairs_loop_top_vol_chg_pct_prod_ids_get = db_pairs_loop_top_vol_chg_pct_prod_ids_get
    db_pairs_loop_watched_prod_ids_get         = db_pairs_loop_watched_prod_ids_get
    db_mkts_insupd                = db_mkts_insupd

    # tbl_ords
    from libs.db_mysql.cbtrade.tbl_ords import  (
        db_ords_exists
        , db_ords_trigs
        , db_ords_get
        , db_ords_insupd
    )
    db_ords_exists                   = db_ords_exists
    db_ords_trigs                   = db_ords_trigs
    db_ords_get                   = db_ords_get
    db_ords_insupd                = db_ords_insupd

    # tbl_poss
    from libs.db_mysql.cbtrade.tbl_poss import  (
        db_poss_exists
        , db_poss_trigs
        , db_poss_get
        , db_mkt_strat_elapsed_get
        , db_prod_ids_traded
        , db_prod_ids_strats_traded
        , db_poss_open_recent_get
        , db_poss_close_recent_get
        , db_open_overview
        , db_closed_overview
        , db_pair_strat_freq_spent
        , db_pair_strat_spent
        , db_bot_spent
        , db_pair_spent
        , db_poss_open_get_by_prod_id
        , db_poss_open_max_trade_size_get
        , db_open_trade_amts_get
        , db_poss_check_last_dttm_get
        , db_poss_check_last_dttm_upd
        , db_sell_double_check_optimized
        , db_pairs_loop_poss_open_prod_ids_get
        , db_poss_insupd
        , db_poss_err_upd
        , db_poss_upd
        , db_poss_upd_sell
        , db_poss_upd_close
    )
    db_poss_exists                   = db_poss_exists
    db_poss_trigs                   = db_poss_trigs
    db_poss_get                   = db_poss_get
    db_mkt_strat_elapsed_get      = db_mkt_strat_elapsed_get
    db_prod_ids_traded            = db_prod_ids_traded
    db_prod_ids_strats_traded     = db_prod_ids_strats_traded
    db_poss_open_recent_get       = db_poss_open_recent_get
    db_poss_close_recent_get      = db_poss_close_recent_get
    db_open_overview              = db_open_overview
    db_closed_overview            = db_closed_overview
    db_pair_strat_freq_spent      = db_pair_strat_freq_spent
    db_pair_strat_spent           = db_pair_strat_spent
    db_bot_spent                  = db_bot_spent
    db_pair_spent                 = db_pair_spent
    db_poss_open_get_by_prod_id   = db_poss_open_get_by_prod_id
    db_poss_open_max_trade_size_get = db_poss_open_max_trade_size_get
    db_open_trade_amts_get        = db_open_trade_amts_get
    db_poss_check_last_dttm_get   = db_poss_check_last_dttm_get
    db_poss_check_last_dttm_upd   = db_poss_check_last_dttm_upd
    db_sell_double_check_optimized = db_sell_double_check_optimized
    db_pairs_loop_poss_open_prod_ids_get       = db_pairs_loop_poss_open_prod_ids_get
    db_poss_insupd                = db_poss_insupd
    db_poss_err_upd               = db_poss_err_upd
    db_poss_upd                   = db_poss_upd
    db_poss_upd_sell              = db_poss_upd_sell
    db_poss_upd_close             = db_poss_upd_close

    # tbl_sell_ords
    from libs.db_mysql.cbtrade.tbl_sell_ords import  (
        db_sell_ords_exists
        , db_sell_ords_trigs
        , db_sell_ords_get
        , db_sell_check_get
        , db_sell_ords_insupd
    )
    db_sell_ords_exists                = db_sell_ords_exists
    db_sell_ords_trigs                 = db_sell_ords_trigs
    db_sell_ords_get                   = db_sell_ords_get
    db_sell_check_get                  = db_sell_check_get
    db_sell_ords_insupd                = db_sell_ords_insupd

    # tbl_trade_perfs
    # from libs.db.db_cb.tbl_trade_perfs import trade_perf_new
    from libs.db_mysql.cbtrade.tbl_trade_perfs import  (
        db_trade_perfs_exists
        , db_trade_perfs_trigs
        , db_trade_perfs_get
        , db_trade_perfs_recalc_single
        , db_trade_perfs_recalc
        , db_pairs_loop_top_perfs_prod_ids_get
        , db_pairs_loop_top_gains_prod_ids_get
        , db_trade_perfs_insupd
    )
    db_trade_perfs_get                         = db_trade_perfs_get
    db_trade_perfs_recalc_single               = db_trade_perfs_recalc_single
    db_trade_perfs_recalc                      = db_trade_perfs_recalc
    db_pairs_loop_top_perfs_prod_ids_get       = db_pairs_loop_top_perfs_prod_ids_get
    db_pairs_loop_top_gains_prod_ids_get       = db_pairs_loop_top_gains_prod_ids_get
    db_trade_perfs_insupd                      = db_trade_perfs_insupd
    db_trade_perfs_exists                      = db_trade_perfs_exists
    db_trade_perfs_trigs                      = db_trade_perfs_trigs
    db_trade_perfs_get                         = db_trade_perfs_get

    # tbl_trade_strat_perfs
    from libs.db_mysql.cbtrade.tbl_trade_strat_perfs import  (
        db_trade_strat_perfs_exists
        , db_trade_strat_perfs_trigs
        , db_trade_strat_perfs_get
        , db_trade_strat_perfs_recalc_single
        , db_trade_strat_perfs_recalc
        , db_trade_strat_perfs_insupd
        , trade_strat_perfs_flag_upd
    )
    db_trade_strat_perfs_get                   = db_trade_strat_perfs_get
    db_trade_strat_perfs_recalc_single         = db_trade_strat_perfs_recalc_single
    db_trade_strat_perfs_recalc                = db_trade_strat_perfs_recalc
    db_trade_strat_perfs_insupd                = db_trade_strat_perfs_insupd
    db_trade_strat_perfs_exists                = db_trade_strat_perfs_exists
    db_trade_strat_perfs_trigs                = db_trade_strat_perfs_trigs
    trade_strat_perfs_flag_upd                 = trade_strat_perfs_flag_upd

    @narc(1)
    def db_poss_sell_order_problems_get(self):
        """Check for position/sell order integrity issues - based on original cbtrade_2025_05_26 logic"""
        if self.debug_tf: G(f'==> CBTRADE_DB.db_poss_sell_order_problems_get()')
        
        sql = """
        WITH SellOrderStats AS (
            SELECT 
                pos_id, 
                COUNT(*) AS sell_order_count 
            FROM sell_ords
            WHERE ord_stat = 'OPEN'
            GROUP BY pos_id
        )
        SELECT 
            'pos.pos_stat = OPEN but there is a sell order(s) on sell_ords' AS reason,
            p.pos_id, 
            p.prod_id, 
            p.pos_stat, 
            p.test_txn_yn, 
            so.so_id
        FROM poss p
        LEFT JOIN sell_ords so ON so.pos_id = p.pos_id AND so.ord_stat = 'OPEN'
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
        LEFT JOIN sell_ords so ON so.pos_id = p.pos_id AND so.ord_stat = 'OPEN'
        LEFT JOIN SellOrderStats sos ON p.pos_id = sos.pos_id
        WHERE p.ignore_tf = 0 
        AND sos.sell_order_count > 1
        """
        
        try:
            return self.seld(sql, always_list_yn='Y') or []
        except Exception as e:
            print(f"db_poss_sell_order_problems_get failed: {e}")
            return []

    @narc(1)
    def table_cols(self, table):
        """Cached table columns to avoid repeated database calls"""
        if table not in self._table_columns_cache:
            # Call parent method once and cache result
            self._table_columns_cache[table] = super().table_cols(table)
        return self._table_columns_cache[table]

    #<=====>#

    def __init__(self, auto_init=True):
        self.debug_tf = debug_tf
        # Cache table columns to avoid repeated database calls
        self._table_columns_cache = {}
        super().__init__(
            db_host=os.getenv('DB_HOST', 'localhost'),
            db_port=int(os.getenv('DB_PORT', '3306')),
            db_name=os.getenv('DB_NAME', 'cbtrade'),
            db_user=os.getenv('DB_USER', 'cbtrade'),
            db_pw=os.getenv('DB_PW', 'cbtrade'),
            auto_schema=auto_init
        )
        # Ensure triggers are present after schema init
        try:
            self.install_core_triggers()
        except Exception as e:
            if self.debug_tf:
                print(f"Trigger install warning: {e}")

    @narc(1)
    def get_required_tables(self) -> Dict[str, str]:
        return {
            'bals': self.db_bals_exists(),
            'buy_decisions': self.db_buy_decisions_exists(),
            'buy_signals': self.db_buy_signals_exists(),
            'buy_ords': self.db_buy_ords_exists(),
            'currs': self.db_currs_exists(),
            'mkt_checks': self.db_mkt_checks_exists(),
            'mkts': self.db_mkts_exists(),
            'ords': self.db_ords_exists(),
            'poss': self.db_poss_exists(),
            'sell_ords': self.db_sell_ords_exists(),
            'trade_perfs': self.db_trade_perfs_exists(),
            'trade_strat_perfs': self.db_trade_strat_perfs_exists(),
        }

    @narc(1)
    def get_required_indexes(self) -> List[str]:
        # Indexes are typically part of the CREATE TABLE statement in MySQL
        # but can be added here if needed.
        return []

    #<=====>#
    # Trigger installation (non-OHLCV)
    #<=====>#

    @narc(1)
    def install_core_triggers(self):
        if self.debug_tf: G('==> CBTRADE_DB.install_core_triggers()')
        trig_sql = []
        trig_sql += self.db_bals_trigs()
        trig_sql += self.db_currs_trigs()
        trig_sql += self.db_buy_ords_trigs()
        trig_sql += self.db_sell_ords_trigs()
        trig_sql += self.db_poss_trigs()
        trig_sql += self.db_mkt_checks_trigs()
        trig_sql += self.db_mkts_trigs()
        trig_sql += self.db_ords_trigs()


        # Execute
        for s in trig_sql:
            self.execute(s)

#<=====>#
# Functions
#<=====>#

# @narc(1)
# def convert_to_scalar_dict(obj, debug=False):
#     """
#     Convert any object (dict-like or regular) to a dictionary with only scalar values.
#     This prevents the "dict can not be used as parameter" error in PyMySQL.
    
#     Args:
#         obj: The object to convert (can be AttrDictEnh, dict, or any object)
#         debug: Whether to print debug information
        
#     Returns:
#         dict: A dictionary containing only scalar values suitable for database operations
#     """
#     result_dict = {}
    
#     # Check if object is a dictionary-like object
#     if hasattr(obj, 'items') and callable(obj.items):
#         # It's a dictionary-like object (AttrDictEnh, dict, etc.)
#         for key, value in obj.items():
#             # Skip internal attributes and nested dictionaries/objects
#             if not key.startswith('_') and not isinstance(value, (dict, list, set, tuple)):
#                 result_dict[key] = value
#     else:
#         # It's a regular object, use dir() and getattr()
#         for key in dir(obj):
#             # Skip private attributes and methods
#             if key.startswith('_') or callable(getattr(obj, key)):
#                 continue
                
#             value = getattr(obj, key)
#             # Only include scalar values (no nested dicts, lists, etc.)
#             if not isinstance(value, (dict, list, set, tuple)) or value is None:
#                 result_dict[key] = value
                
#     if debug:
#         print(f"DEBUG: Converted object to dict with {len(result_dict)} keys: {list(result_dict.keys())[:5]}...")
        
#     return result_dict

@narc(1)
def ensure_database_ready(db_path: str, verbose: bool = False) -> bool:
    if debug_tf: G(f'==> db.cbtrade.db_main.ensure_database_ready(db_path={db_path}, verbose={verbose})')
    """
    Ensure required tables, indexes, and triggers exist for the cbtrade schema.
    Safe operations only: uses CREATE TABLE IF NOT EXISTS and DROP TRIGGER IF EXISTS
    before CREATE TRIGGER statements returned by the table modules.
    """
    try:
        db = CBTRADE_DB(auto_init=False)
        # Create/ensure all tables
        try:
            required = db.get_required_tables()
        except Exception:
            required = {}
        for tbl, create_sql in required.items():
            if verbose or db.debug_tf:
                G(f"Ensuring table exists: {tbl}")
            try:
                db.execute(create_sql)
            except Exception as e:
                if verbose or db.debug_tf:
                    print(f"Warning ensuring table {tbl}: {e}")
        # Indexes (if any are provided)
        try:
            for idx_sql in db.get_required_indexes() or []:
                if idx_sql:
                    db.execute(idx_sql)
        except Exception:
            pass
        # Triggers
        try:
            db.install_core_triggers()
        except Exception as e:
            if verbose or db.debug_tf:
                print(f"Trigger install warning: {e}")
        return True
    except Exception as e:
        if verbose:
            print(f"ensure_database_ready() error: {e}")
        return False

#<=====>#
# Post-Assigned Variables
#<=====>#

cbtrade_db = CBTRADE_DB()

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    cbtrade_db = CBTRADE_DB()
    cbtrade_db.test_connection()

#<=====>#
