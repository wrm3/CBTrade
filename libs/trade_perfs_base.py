#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports - Public
#<=====>#
from datetime import datetime as dt
from fstrent_bkitup import backup_project as bkp, backup_script as bks
from fstrent_charts import *
from fstrent_colors import G
from pprint import pprint
from typing import Optional

#<=====>#
# Imports - Project
#<=====>#
from libs.common import (
    AttrDict
    , AttrDictEnh
    , dttm_get
    , dttm_unix
    , spacer
    , AllHaveVal
    , narc
    )

from libs.db_mysql.cbtrade.db_main import CBTRADE_DB
cbtrade_db = CBTRADE_DB()  # Create instance for backward compatibility

#<=====>#
# BackItUp
#<=====>#
bks(__file__)

#<=====>#
# Variables
#<=====>#
lib_name = 'trade_perf_base'
log_name = 'trade_perf_base'

# <=====>#
# Assignments Pre
# <=====>#
debug_tf = False


#<=====>#
# Classes
#<=====>#

class TRADE_PERF(AttrDictEnh):
    """Trade performance data structure matching MySQL table schema"""

    #<=====>#

    def __init__(self, data=None, force_recalc=False, **kwargs):
        if debug_tf: G(f'==> TRADE_PERF.init()')

        super().__init__(data, **kwargs)
        self.init_schema()
        if data:
            self.upd_data(data)
        else:
            if AllHaveVal(self.prod_id, self.lta):
                self.db_load()
            else:
                msg = f"TRADE_PERF.init() => Missing required fields: {self.prod_id}, {self.lta}"
                print(msg)
                raise ValueError(msg)

        if force_recalc:
            self.recalc()
        elif dttm_unix() - int(self.last_upd_unix) > 86400:
            self.recalc()

    #<=====>#

    @narc(1)
    def init_schema(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_PERF.init_schema()')

        # ==========================================
        # Core Identifiers
        # ==========================================
        self.base_symb                 : str               = ""
        self.quote_symb                : str               = ""
        self.prod_id                   : str               = ""
        self.lta                       : str               = ""
        
        # ==========================================
        # Timestamp Tracking
        # ==========================================
        self.last_upd_dttm             : Optional[dt]      = None
        self.last_upd_unix             : int               = 0
        
        # ==========================================
        # Trade Counts
        # ==========================================
        self.tot_cnt                   : int               = 0
        self.tot_open_cnt              : int               = 0
        self.tot_close_cnt             : int               = 0
        
        # ==========================================
        # Win/Loss Counts
        # ==========================================
        self.win_cnt                   : int               = 0
        self.win_open_cnt              : int               = 0
        self.win_close_cnt             : int               = 0
        self.lose_cnt                  : int               = 0
        self.lose_open_cnt             : int               = 0
        self.lose_close_cnt            : int               = 0
        
        # ==========================================
        # Win/Loss Percentages
        # ==========================================
        self.win_pct                   : float             = 0.0
        self.win_open_pct              : float             = 0.0
        self.win_close_pct             : float             = 0.0
        self.lose_pct                  : float             = 0.0
        self.lose_open_pct             : float             = 0.0
        self.lose_close_pct            : float             = 0.0
        
        # ==========================================
        # Age Tracking
        # ==========================================
        self.age_mins                  : float             = 0.0
        self.age_hours                 : float             = 0.0
        
        # ==========================================
        # Transaction Counts
        # ==========================================
        self.tot_out_cnt               : float             = 0.0
        self.tot_out_open_cnt          : float             = 0.0
        self.tot_out_close_cnt         : float             = 0.0
        self.tot_in_cnt                : float             = 0.0
        self.tot_in_open_cnt           : float             = 0.0
        self.tot_in_close_cnt          : float             = 0.0
        
        # ==========================================
        # Fee Tracking
        # ==========================================
        self.buy_fees_cnt              : float             = 0.0
        self.buy_fees_open_cnt         : float             = 0.0
        self.buy_fees_close_cnt        : float             = 0.0
        self.sell_fees_cnt_tot         : float             = 0.0
        self.sell_fees_open_cnt_tot    : float             = 0.0
        self.sell_fees_close_cnt_tot   : float             = 0.0
        self.fees_cnt_tot              : float             = 0.0
        self.fees_open_cnt_tot         : float             = 0.0
        self.fees_close_cnt_tot        : float             = 0.0
        
        # ==========================================
        # Trade Operation Counts
        # ==========================================
        self.buy_cnt                   : float             = 0.0
        self.buy_open_cnt              : float             = 0.0
        self.buy_close_cnt             : float             = 0.0
        self.sell_cnt_tot              : float             = 0.0
        self.sell_open_cnt_tot         : float             = 0.0
        self.sell_close_cnt_tot        : float             = 0.0
        self.hold_cnt                  : float             = 0.0
        self.hold_open_cnt             : float             = 0.0
        self.hold_close_cnt            : float             = 0.0
        self.pocket_cnt                : float             = 0.0
        self.pocket_open_cnt           : float             = 0.0
        self.pocket_close_cnt          : float             = 0.0
        self.clip_cnt                  : float             = 0.0
        self.clip_open_cnt             : float             = 0.0
        self.clip_close_cnt            : float             = 0.0
        
        # ==========================================
        # Order Counts
        # ==========================================
        self.sell_order_cnt            : int               = 0
        self.sell_order_open_cnt       : int               = 0
        self.sell_order_close_cnt      : int               = 0
        self.sell_order_attempt_cnt    : int               = 0
        self.sell_order_attempt_open_cnt: int              = 0
        self.sell_order_attempt_close_cnt: int             = 0

        # ==========================================
        # Value Tracking
        # ==========================================
        self.val_curr                  : float             = 0.0
        self.val_open_curr             : float             = 0.0
        self.val_close_curr            : float             = 0.0
        self.val_tot                   : float             = 0.0
        self.val_open_tot              : float             = 0.0
        self.val_close_tot             : float             = 0.0
        
        # ==========================================
        # Win/Loss Amounts
        # ==========================================
        self.win_amt                   : float             = 0.0
        self.win_open_amt              : float             = 0.0
        self.win_close_amt             : float             = 0.0
        self.lose_amt                  : float             = 0.0
        self.lose_open_amt             : float             = 0.0
        self.lose_close_amt            : float             = 0.0
        
        # ==========================================
        # Gain/Loss Tracking
        # ==========================================
        self.gain_loss_amt             : float             = 0.0
        self.gain_loss_open_amt        : float             = 0.0
        self.gain_loss_close_amt       : float             = 0.0
        self.gain_loss_amt_net         : float             = 0.0
        self.gain_loss_open_amt_net    : float             = 0.0
        self.gain_loss_close_amt_net   : float             = 0.0
        
        # ==========================================
        # Gain/Loss Percentages
        # ==========================================
        self.gain_loss_pct             : float             = 0.0
        self.gain_loss_open_pct        : float             = 0.0
        self.gain_loss_close_pct       : float             = 0.0
        self.gain_loss_pct_hr          : float             = 0.0
        self.gain_loss_open_pct_hr     : float             = 0.0
        self.gain_loss_close_pct_hr    : float             = 0.0
        self.gain_loss_pct_day         : float             = 0.0
        self.gain_loss_open_pct_day    : float             = 0.0
        self.gain_loss_close_pct_day   : float             = 0.0
        
        # ==========================================
        # Strategy Elapsed Times (using original field names)
        # ==========================================
        self.bo_elapsed                : float             = 9999
        self.pos_elapsed               : float             = 9999
        self.last_elapsed              : float             = 9999
        
        # ==========================================
        # Event-Driven Performance System
        # ==========================================
        self.needs_recalc_yn           : str               = ""
        
        # ==========================================
        # Audit Trail Fields
        # ==========================================
        self.add_dttm                  : Optional[dt]      = dt.now()
        self.dlm                       : Optional[dt]      = dt.now()
        self.add_unix                  : int               = dttm_unix()
        self.dlm_unix                  : int               = dttm_unix()

    #<=====>#

    @narc(1)
    def upd_data(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_PERF.upd_data()')
        if data:
            if isinstance(data, dict):
                for k, v in data.items():
                    setattr(self, k, v)
            elif isinstance(data, TRADE_PERF):
                for k, v in data.items():
                    setattr(self, k, v)
            else:
                msg = f"TRADE_PERF.upd_data() => No data provided to update"
                print(msg)
                raise ValueError(msg)
        else:
            msg = f"TRADE_PERF.upd_data() => No data provided to update"
            print(msg)
            raise ValueError(msg)

    #<=====>#

    @narc(1)
    def db_load(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_PERF.db_load()')
        if AllHaveVal(self.prod_id, self.lta):
            trade_perf = cbtrade_db.db_trade_perfs_get(self.prod_id, self.lta)
            self.upd_data(trade_perf)
        else:
            msg = f"TRADE_PERF.db_load() => Missing required fields: {self.prod_id}, {self.lta}"
            print(msg)
            raise ValueError(msg)

    #<=====>#

    @narc(1)
    def db_save(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_PERF.db_save()')
        cbtrade_db.db_trade_perfs_insupd(self)

    #<=====>#

    @narc(1)
    def recalc(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_PERF.recalc() ==> {self.prod_id} {self.lta}')
        trade_perf = cbtrade_db.db_trade_perfs_recalc(self.prod_id, self.lta)
        if trade_perf:
            self.upd_data(trade_perf)

    #<=====>#


#<=====>#
# Functions
#<=====>#

@narc(1)
def pair_trade_perfs_get(self):
    if debug_tf: G(f'==> trade_perfs_base.pair_trade_perfs_get()')
    """
    Get all strategy performances for a pair using centralized trade_perfs table
    - Uses centralized trade_perfs table in db
    - Assigns trade performance data to self.pair object
    """
    if debug_tf: G(f'==> trade_perfs_base.pair_trade_perfs_get()')
    
    # Build normalized L/T/A structure with defaults (no legacy keys)
    self.pair.trade_perfs = trade_perfs_get(self, prod_id=self.pair.prod_id)

#<=====>#

@narc(1)
def trade_perfs_get(self, prod_id:str='', lta:str='', force_recalc:bool=False):
    if debug_tf: G(f'==> trade_perfs_base.trade_perfs_get(prod_id={prod_id}, lta={lta}, force_recalc={force_recalc})')

    # Get all trade performances for the pair
    trade_perfs = cbtrade_db.db_trade_perfs_get(prod_id=prod_id, lta=lta, force_recalc=force_recalc)
    results = AttrDict()
    # print(f'trade_perfs_base.trade_perfs_get() ==> {type(trade_perfs)} trade_perfs found')

    if trade_perfs:
        if isinstance(trade_perfs, list):
            for x in trade_perfs:
                if isinstance(x, dict):
                    trade_perf = TRADE_PERF(data=x)
                    results[trade_perf.lta] = trade_perf
        else:
            trade_perf = TRADE_PERF(data=trade_perfs)
            results[trade_perf.lta] = trade_perf
    else:
        for lta in ('L', 'T', 'A'):
            x = AttrDict()
            x.prod_id = prod_id
            x.lta = lta
            x.last_upd_dttm = dttm_get()
            x.last_upd_unix = dttm_unix()
            x.tot_cnt = 0
            x.tot_open_cnt = 0
            x.tot_close_cnt = 0
            results[lta] = TRADE_PERF(data=x)

    # Backward-compatible default for max open positions restriction
    # Old system populated this on trade_perf; new system supplies it here
    default_open_poss_max = 1
    try:
        if hasattr(self, 'st_pair') and getattr(self.st_pair, 'buy', None):
            default_open_poss_max = getattr(self.st_pair.buy, 'open_poss_cnt_max', 1) or 1
    except Exception:
        default_open_poss_max = 1

    if 'restricts_open_poss_cnt_max' not in results:
        results.restricts_open_poss_cnt_max = default_open_poss_max

    # print(f'trade_perfs_base.trade_perfs_get() ==> {results}')
    return results

#<=====>#

@narc(1)
def trade_perfs_get_by_prod_id(self, prod_id:str, force_recalc:bool=False):
    if debug_tf: G(in_str=f'==> trade_perfs_base.trade_perfs_get(prod_id={prod_id}, force_recalc={force_recalc})')

    trade_perfs = cbtrade_db.db_trade_perfs_get(prod_id=prod_id, force_recalc=force_recalc)
    # print(f'trade_perfs_base.trade_perfs_get() ==> {type(trade_perfs)} trade_perfs found')

    st_open_poss_max = self.st_pair.buy.open_poss_cnt_max

    results = AttrDict()
    # Initialize with TRADE_PERF objects that have required fields
    results['L'] = TRADE_PERF({'prod_id': prod_id, 'lta': 'L'})
    results['T'] = TRADE_PERF({'prod_id': prod_id, 'lta': 'T'}) 
    results['A'] = TRADE_PERF({'prod_id': prod_id, 'lta': 'A'})

    now_unix = dttm_unix()
    for x in trade_perfs:
        x.prod_id = prod_id
        x.last_upd_dttm = dttm_get()
        x.last_upd_unix = dttm_unix()
        x.open_poss_cnt_max = st_open_poss_max
        
        # Calculate elapsed fields from timestamp columns for all consumers
        if hasattr(x, 'last_buy_unix') and x.last_buy_unix:
            x.last_elapsed = (now_unix - x.last_buy_unix) / 60
            if x.last_elapsed > 9999:
                x.last_elapsed = 9999
        else:
            x.last_elapsed = 9999
            
        results[x.lta] = TRADE_PERF(data=x)

    results.restricts_open_poss_cnt_max = st_open_poss_max
    return results

#<=====>#

@narc(1)
def trade_perfs_recalc_all(self, quote_symb:str=''):
    if debug_tf: G(f'==> trade_perfs_base.trade_perfs_recalc_all(quote_symb={quote_symb})')

    process_list = cbtrade_db.db_prod_ids_traded(quote_symb=quote_symb)
    print(f'==> {len(process_list)} products to process for {quote_symb}')
    
    if not process_list:
        print(f'    No products found for quote_symb: {quote_symb}')
        return

    save_count = 0
    for x in process_list:
        x = AttrDict(x)
        if debug_tf: print(f'Processing: {x}')
        prod_id = x.prod_id
            
        for lta in ('L', 'T', 'A'):
            trade_perfs = self.trade_perfs_get(prod_id=prod_id, lta=lta, force_recalc=True)
            for trade_perf in trade_perfs:
                # Create TRADE_PERF object with force_recalc=True
                trade_perf = TRADE_PERF(data=trade_perf, force_recalc=True)
                # trade_perf.db_save()
                save_count += 1
            
                print(f"{spacer} ✅ SAVED: {trade_perf.prod_id:<20} {trade_perf.lta:^1}")
                
    if debug_tf: print(f'==> COMPLETED: {save_count} trade performance records saved to database')

#<=====>#

@narc(1)
def trade_perfs_recalc_sp(prod_id:str, lta:str):
    """Minimal wrapper to call the MySQL stored procedure directly."""
    sql = ""
    sql += f"CALL sp_trade_perfs_recalc('{prod_id}','{lta}');"
    cbtrade_db.upd(sql)

#<=====>#

@narc(1)
def trade_perfs_recalc_sp_read(prod_id:str, lta:str):
    """Call the stored procedure and return all result sets as list of dict lists."""
    from pymysql.cursors import DictCursor
    results = []
    conn = cbtrade_db.get_connection()
    with conn.cursor(DictCursor) as cur:
        cur.execute("CALL sp_trade_perfs_recalc(%s,%s)", (prod_id, lta))
        while True:
            if cur.description:
                rows = cur.fetchall() or []
                results.append(rows)
            else:
                _ = cur.fetchall()
            if not cur.nextset():
                break
    return results

#<=====>#

@narc(1)
def pair_trade_perf_buy_upd(self, prod_id, lta=None):
    if debug_tf: G(f'==> trade_perfs_base.pair_trade_perf_buy_upd(prod_id={prod_id}, lta={lta})')
    """
    After a buy order is completed, update the strategy performance cache
    """
    # trade_perf = self.cbtrade_db.db_trade_perfs_recalc(prod_id, lta)
    # trade_perf.last_elapsed = 0
    # # Use sync write to centralized table
    # self.cbtrade_db.db_trade_perfs_insupd(trade_perf)
    sql = ""
    sql += f"update trade_perfs "
    sql += f"set needs_recalc_yn = 'Y' "
    sql += f"where prod_id = '{prod_id}' "
    sql += f"and lta = '{lta}'"
    cbtrade_db.upd(sql)

#<=====>#

@narc(1)
def pair_trade_perf_sell_upd(self, prod_id, lta=None):
    if debug_tf: G(f'==> trade_perfs_base.pair_trade_perf_sell_upd(prod_id={prod_id}, lta={lta})')
    """
    After a sell order is completed, update the strategy performance cache
    """
    # trade_perf = self.cbtrade_db.db_trade_perfs_recalc(prod_id, lta)
    # # Use sync write to centralized trade_perfs table
    # self.cbtrade_db.db_trade_perfs_insupd(trade_perf)
    sql = ""
    sql += f"update trade_perfs "
    sql += f"set needs_recalc_yn = 'Y' "
    sql += f"where prod_id = '{prod_id}' "
    sql += f"and lta = '{lta}'"
    cbtrade_db.upd(sql)

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#


#<=====># 