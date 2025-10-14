#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports - Public
#<=====>#
import sys
import traceback
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
# bks(__file__)

#<=====>#
# Variables
#<=====>#
lib_name = 'trade_strat_perf_base'
log_name = 'trade_strat_perf_base'


# <=====>#
# Assignments Pre
# <=====>#
debug_tf = False


#<=====>#
# Classes
#<=====>#

class TRADE_STRAT_PERF(AttrDictEnh):
    """Strategy performance data structure matching SQLite table schema"""

    #<=====>#

    def __init__(self, data=None, force_recalc=False, **kwargs):
        if debug_tf: G(f'==> TRADE_STRAT_PERF.init()')

        super().__init__(data, **kwargs)
        self.init_schema()
        if data:
            self.upd_data(data)
        else:
            if AllHaveVal([self.prod_id, self.buy_strat_type, self.buy_strat_name, self.buy_strat_freq, self.lta]):
                self.db_load()
            else:
                msg = f"TRADE_STRAT_PERF.init() => Missing required fields: {self.prod_id}, {self.buy_strat_type}, {self.buy_strat_name}, {self.buy_strat_freq}, {self.lta}"
                print(msg)
                raise ValueError(msg)

        if force_recalc:
            self.recalc()
        elif dttm_unix() - int(self.last_upd_unix) > 86400:
            self.recalc()

    #<=====>#

    @narc(1)
    def init_schema(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_STRAT_PERF.init_schema()')

        # ==========================================
        # Core Identifiers
        # ==========================================
        self.base_symb                 : str               = ""
        self.quote_symb                : str               = ""
        self.prod_id                   : str               = ""
        self.lta                       : str               = ""
        self.buy_strat_type            : str               = ""
        self.buy_strat_name            : str               = ""
        self.buy_strat_freq            : str               = ""
        
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
        # Strategy Elapsed Times
        # ==========================================
        self.strat_bo_elapsed          : float             = 9999
        self.strat_pos_elapsed         : float             = 9999
        self.strat_last_elapsed        : float             = 9999
        
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
        if debug_tf: G(f'==> TRADE_STRAT_PERF.upd_data()')

        if data:
            if isinstance(data, dict):
                for k, v in data.items():
                    setattr(self, k, v)
            elif isinstance(data, TRADE_STRAT_PERF):
                for k, v in data.items():
                    setattr(self, k, v)
            else:
                msg = f"TRADE_STRAT_PERF.upd_data() => No data provided to update"
                print(msg)
                raise ValueError(msg)
        else:
            msg = f"TRADE_STRAT_PERF.upd_data() => No data provided to update"
            print(msg)
            raise ValueError(msg)

    #<=====>#

    @narc(1)
    def db_load(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_STRAT_PERF.db_load()')

        if AllHaveVal([self.prod_id, self.buy_strat_type, self.buy_strat_name, self.buy_strat_freq, self.lta]):
            trade_strat_perf = cbtrade_db.db_trade_strat_perfs_get(self.prod_id, self.buy_strat_type, self.buy_strat_name, self.buy_strat_freq, self.lta)
            self.upd_data(trade_strat_perf)
        else:
            msg = f"TRADE_STRAT_PERF.db_load() => Missing required fields: {self.prod_id}, {self.buy_strat_type}, {self.buy_strat_name}, {self.buy_strat_freq}, {self.lta}"
            print(msg)
            raise ValueError(msg)

    #<=====>#

    @narc(1)
    def db_save(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_STRAT_PERF.db_save()')
        cbtrade_db.db_trade_strat_perfs_insupd(self.to_dict())

    #<=====>#

    @narc(1)
    def recalc(self, data=None, **kwargs):
        if debug_tf: G(f'==> TRADE_STRAT_PERF.recalc()')
        trade_strat_perf = cbtrade_db.db_trade_strat_perfs_get(self.prod_id, self.buy_strat_type, self.buy_strat_name, self.buy_strat_freq, self.lta)
        if trade_strat_perf:
            self.upd_data(trade_strat_perf)

    #<=====>#


#<=====>#
# Functions
#<=====>#

# def trade_strat_perf_new(perf):
#     """Create a new trade performance object from database row"""
#     trade_strat_perf = TRADE_STRAT_PERF(perf)
#     # self.cbtrade_db.db_trade_strat_perfs_insupd(trade_strat_perf)
#     pprint(trade_strat_perf)
#     return trade_strat_perf

#<=====>#

@narc(1)
def pair_trade_strat_perfs_get(self):
    if debug_tf: G(f'==> trade_strat_perfs_base.pair_trade_strat_perfs_get()')
    """
    Get all strategy performances for a pair using centralized trade_strat_perfs table
    - Uses centralized trade_strat_perfs table in db
    - Assigns strategy performance data to self.pair object
    """
    if debug_tf: G(f'==> trade_strat_perfs_base.pair_trade_strat_perfs_get()')
    
    # Get all strategy performances for the pair
    strat_perfs = self.cbtrade_db.db_trade_strat_perfs_get_by_prod_id(self.pair.prod_id)
    
    # Initialize strategy performance container if it doesn't exist
    if not hasattr(self.pair, 'trade_strat_perfs'):
        self.pair.trade_strat_perfs = []
    
    # Store the strategy performances on the pair object
    self.pair.trade_strat_perfs = strat_perfs

#<=====>#

@narc(1)
def trade_strat_perfs_get(prod_id:str='', buy_strat_type:str='', buy_strat_name:str='', buy_strat_freq:str='', lta:str='', force_recalc:bool=False, buy_strats:dict={}):
    if debug_tf: G(f'==> trade_strat_perfs_base.trade_strat_perfs_get(prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta}, force_recalc={force_recalc})')

    # Get all strategy performances for the pair
    trade_strat_perfs = cbtrade_db.db_trade_strat_perfs_get(prod_id=prod_id, buy_strat_type=buy_strat_type, buy_strat_name=buy_strat_name, buy_strat_freq=buy_strat_freq, lta=lta, force_recalc=force_recalc)
    results = []
    # print(f'==> {len(trade_strat_perfs)} trade_strat_perfs found')
    if trade_strat_perfs:
        if isinstance(trade_strat_perfs, list):
            for x in trade_strat_perfs:
                trade_strat_perf = TRADE_STRAT_PERF(data=x)
                results.append(trade_strat_perf)
        else:
            x = trade_strat_perfs
            trade_strat_perf = TRADE_STRAT_PERF(data=x)
            results.append(trade_strat_perf)

    trade_strats_perfs_dict = AttrDict()
    for buy_strat in results:
        prod_id = buy_strat.prod_id
        buy_strat_type = buy_strat.buy_strat_type
        buy_strat_name = buy_strat.buy_strat_name
        buy_strat_freq = buy_strat.buy_strat_freq
        lta = buy_strat.lta

        if buy_strat_type not in trade_strats_perfs_dict:
            trade_strats_perfs_dict[buy_strat_type] = AttrDict()
        if buy_strat_name not in trade_strats_perfs_dict[buy_strat_type]:
            trade_strats_perfs_dict[buy_strat_type][buy_strat_name] = AttrDict()
        if buy_strat_freq not in trade_strats_perfs_dict[buy_strat_type][buy_strat_name]:
            trade_strats_perfs_dict[buy_strat_type][buy_strat_name][buy_strat_freq] = AttrDict()
        if lta not in trade_strats_perfs_dict[buy_strat_type][buy_strat_name][buy_strat_freq]:
            trade_strats_perfs_dict[buy_strat_type][buy_strat_name][buy_strat_freq][lta] = AttrDict()

        trade_strats_perfs_dict[buy_strat_type][buy_strat_name][buy_strat_freq][lta] = buy_strat

    return results

#<=====>#
 
@narc(1)
def trade_strat_perfs_get_all(self, prod_id:str='', buy_strat_type:str='', buy_strat_name:str='', buy_strat_freq:str='', lta:str='', force_recalc:bool=False, buy_strats:dict={}):
    if debug_tf: G(f'==> trade_strat_perfs_base.trade_strat_perfs_get(prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta}, force_recalc={force_recalc})')

    # traceback.print_stack()  # Direct call - no print() wrapper needed

    sql = f"""
        select coalesce(tsp.prod_id, p.base_symb) as base_symb
        , coalesce(tsp.prod_id, p.quote_symb) as quote_symb
        , coalesce(tsp.prod_id, p.prod_id) as prod_id
        , coalesce(tsp.lta, x.lta) as lta
        , coalesce(tsp.buy_strat_type, bs.buy_strat_type) as buy_strat_type
        , coalesce(tsp.buy_strat_name, bs.buy_strat_name) as buy_strat_name
        , coalesce(tsp.buy_strat_freq, bs.buy_strat_freq) as buy_strat_freq
        , coalesce(tsp.last_upd_dttm, '') as last_upd_dttm
        , coalesce(tsp.last_upd_unix, 0) as last_upd_unix
        , coalesce(tsp.tot_cnt, 0) as tot_cnt
        , coalesce(tsp.tot_open_cnt, 0) as tot_open_cnt
        , coalesce(tsp.tot_close_cnt, 0) as tot_close_cnt
        , coalesce(tsp.win_cnt, 0) as win_cnt
        , coalesce(tsp.win_open_cnt, 0) as win_open_cnt
        , coalesce(tsp.win_close_cnt, 0) as win_close_cnt
        , coalesce(tsp.lose_cnt, 0) as lose_cnt
        , coalesce(tsp.lose_open_cnt, 0) as lose_open_cnt
        , coalesce(tsp.lose_close_cnt, 0) as lose_close_cnt
        , coalesce(tsp.win_pct, 0) as win_pct
        , coalesce(tsp.win_open_pct, 0) as win_open_pct
        , coalesce(tsp.win_close_pct, 0) as win_close_pct
        , coalesce(tsp.lose_pct, 0) as lose_pct
        , coalesce(tsp.lose_open_pct, 0) as lose_open_pct
        , coalesce(tsp.lose_close_pct, 0) as lose_close_pct
        , coalesce(tsp.age_mins, 0) as age_mins
        , coalesce(tsp.age_hours, 0) as age_hours
        , coalesce(tsp.tot_out_cnt, 0) as tot_out_cnt
        , coalesce(tsp.tot_out_open_cnt, 0) as tot_out_open_cnt
        , coalesce(tsp.tot_out_close_cnt, 0) as tot_out_close_cnt
        , coalesce(tsp.tot_in_cnt, 0) as tot_in_cnt
        , coalesce(tsp.tot_in_open_cnt, 0) as tot_in_open_cnt
        , coalesce(tsp.tot_in_close_cnt, 0) as tot_in_close_cnt
        , coalesce(tsp.buy_fees_cnt, 0) as buy_fees_cnt
        , coalesce(tsp.buy_fees_open_cnt, 0) as buy_fees_open_cnt
        , coalesce(tsp.buy_fees_close_cnt, 0) as buy_fees_close_cnt
        , coalesce(tsp.sell_fees_cnt_tot, 0) as sell_fees_cnt_tot
        , coalesce(tsp.sell_fees_open_cnt_tot, 0) as sell_fees_open_cnt_tot
        , coalesce(tsp.sell_fees_close_cnt_tot, 0) as sell_fees_close_cnt_tot
        , coalesce(tsp.fees_cnt_tot, 0) as fees_cnt_tot
        , coalesce(tsp.fees_open_cnt_tot, 0) as fees_open_cnt_tot
        , coalesce(tsp.fees_close_cnt_tot, 0) as fees_close_cnt_tot
        , coalesce(tsp.buy_cnt, 0) as buy_cnt
        , coalesce(tsp.buy_open_cnt, 0) as buy_open_cnt
        , coalesce(tsp.buy_close_cnt, 0) as buy_close_cnt
        , coalesce(tsp.sell_cnt_tot, 0) as sell_cnt_tot
        , coalesce(tsp.sell_open_cnt_tot, 0) as sell_open_cnt_tot
        , coalesce(tsp.sell_close_cnt_tot, 0) as sell_close_cnt_tot
        , coalesce(tsp.hold_cnt, 0) as hold_cnt
        , coalesce(tsp.hold_open_cnt, 0) as hold_open_cnt
        , coalesce(tsp.hold_close_cnt, 0) as hold_close_cnt
        , coalesce(tsp.pocket_cnt, 0) as pocket_cnt
        , coalesce(tsp.pocket_open_cnt, 0) as pocket_open_cnt
        , coalesce(tsp.pocket_close_cnt, 0) as pocket_close_cnt
        , coalesce(tsp.clip_cnt, 0) as clip_cnt
        , coalesce(tsp.clip_open_cnt, 0) as clip_open_cnt
        , coalesce(tsp.clip_close_cnt, 0) as clip_close_cnt
        , coalesce(tsp.sell_order_cnt, 0) as sell_order_cnt
        , coalesce(tsp.sell_order_open_cnt, 0) as sell_order_open_cnt
        , coalesce(tsp.sell_order_close_cnt, 0) as sell_order_close_cnt
        , coalesce(tsp.sell_order_attempt_cnt, 0) as sell_order_attempt_cnt
        , coalesce(tsp.sell_order_attempt_open_cnt, 0) as sell_order_attempt_open_cnt
        , coalesce(tsp.sell_order_attempt_close_cnt, 0) as sell_order_attempt_close_cnt
        , coalesce(tsp.val_curr, 0) as val_curr
        , coalesce(tsp.val_open_curr, 0) as val_open_curr
        , coalesce(tsp.val_close_curr, 0) as val_close_curr
        , coalesce(tsp.val_tot, 0) as val_tot
        , coalesce(tsp.val_open_tot, 0) as val_open_tot
        , coalesce(tsp.val_close_tot, 0) as val_close_tot
        , coalesce(tsp.win_amt, 0) as win_amt
        , coalesce(tsp.win_open_amt, 0) as win_open_amt
        , coalesce(tsp.win_close_amt, 0) as win_close_amt
        , coalesce(tsp.lose_amt, 0) as lose_amt
        , coalesce(tsp.lose_open_amt, 0) as lose_open_amt
        , coalesce(tsp.lose_close_amt, 0) as lose_close_amt
        , coalesce(tsp.gain_loss_amt, 0) as gain_loss_amt
        , coalesce(tsp.gain_loss_open_amt, 0) as gain_loss_open_amt
        , coalesce(tsp.gain_loss_close_amt, 0) as gain_loss_close_amt
        , coalesce(tsp.gain_loss_amt_net, 0) as gain_loss_amt_net
        , coalesce(tsp.gain_loss_open_amt_net, 0) as gain_loss_open_amt_net
        , coalesce(tsp.gain_loss_close_amt_net, 0) as gain_loss_close_amt_net
        , coalesce(tsp.gain_loss_pct, 0) as gain_loss_pct
        , coalesce(tsp.gain_loss_open_pct, 0) as gain_loss_open_pct
        , coalesce(tsp.gain_loss_close_pct, 0) as gain_loss_close_pct
        , coalesce(tsp.gain_loss_pct_hr, 0) as gain_loss_pct_hr
        , coalesce(tsp.gain_loss_open_pct_hr, 0) as gain_loss_open_pct_hr
        , coalesce(tsp.gain_loss_close_pct_hr, 0) as gain_loss_close_pct_hr
        , coalesce(tsp.gain_loss_pct_day, 0) as gain_loss_pct_day
        , coalesce(tsp.gain_loss_open_pct_day, 0) as gain_loss_open_pct_day
        , coalesce(tsp.gain_loss_close_pct_day, 0) as gain_loss_close_pct_day
        , coalesce(floor((UNIX_TIMESTAMP() - coalesce(tsp.last_buy_strat_bo_unix,0))/60), 0) as strat_bo_elapsed
        , coalesce(floor((UNIX_TIMESTAMP() - coalesce(tsp.last_buy_strat_pos_unix,0))/60), 0) as strat_pos_elapsed
        , coalesce(floor((UNIX_TIMESTAMP() - coalesce(tsp.last_buy_strat_unix,0))/60), 0) as strat_last_elapsed
        , tsp.last_buy_strat_bo_unix
        , tsp.last_buy_strat_pos_unix
        , tsp.last_buy_strat_unix
        , tsp.last_buy_strat_bo_dttm
        , tsp.last_buy_strat_pos_dttm
        , tsp.last_buy_strat_dttm
        , coalesce(tsp.needs_recalc_yn, 'Y') as needs_recalc_yn
        , coalesce(tsp.add_dttm, '') as add_dttm
        , coalesce(tsp.dlm, '') as dlm
        , coalesce(tsp.add_unix, 1) as add_unix
        , coalesce(tsp.dlm_unix, 0) as dlm_unix
        , coalesce(bsg.event_dttm, '') as last_buy_sign_hist_dttm
        from buy_strats bs
        join (select 'L' as lta union select 'T' as lta union select 'A' as lta) x
        join (select '{prod_id}' as prod_id, SUBSTR('{prod_id}', 1, INSTR('{prod_id}', '-') - 1) as base_symb, SUBSTR('{prod_id}', INSTR('{prod_id}', '-') + 1) as quote_symb) p
        left outer join trade_strat_perfs tsp 
                        on tsp.prod_id = p.prod_id 
                        and tsp.buy_strat_type = bs.buy_strat_type 
                        and tsp.buy_strat_name = bs.buy_strat_name 
                        and tsp.buy_strat_freq = bs.buy_strat_freq 
                        and tsp.lta = x.lta
        left outer join (select prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, max(event_dttm) as event_dttm 
                           from buy_signals 
                           group by prod_id, buy_strat_type, buy_strat_name, buy_strat_freq) bsg 
                        on bsg.prod_id = p.prod_id 
                        and bsg.buy_strat_type = bs.buy_strat_type 
                        and bsg.buy_strat_name = bs.buy_strat_name 
                        and bsg.buy_strat_freq = bs.buy_strat_freq
        order by bs.buy_strat_type, bs.buy_strat_name, bs.buy_strat_freq, x.lta
        """
    r = cbtrade_db.seld(sql=sql, always_list_yn='Y')

    if debug_tf: print(f"trade_strat_perfs_base.trade_strat_perfs_get_all() ==> {len(r)} records found")

    now_unix = dttm_unix()

    results = []
    for x in r:
        trade_strat_perf = TRADE_STRAT_PERF(data=x)

        # Calculate age like the trade_perfs pattern
        trade_strat_perf.age_hours = (now_unix - trade_strat_perf.last_upd_unix) / 3600 if trade_strat_perf.last_upd_unix else 999
        
        # Apply the same pattern as trade_perfs: refresh if older than 24 hours OR if data is empty
        # if trade_strat_perf.age_hours > 24 or trade_strat_perf.tot_cnt == 0:
        # print(f"==> trade_strat_perf.age_hours: {trade_strat_perf.age_hours} {type(trade_strat_perf.age_hours)}")
        if trade_strat_perf.age_hours > 24 or trade_strat_perf.needs_recalc_yn == 'Y':
            # print(x)
            if debug_tf: print(f"🔄 trade_strat_perfs_base.trade_strat_perfs_get_all() ==> {prod_id}  Strategy performance for {trade_strat_perf.buy_strat_type} {trade_strat_perf.buy_strat_name} {trade_strat_perf.buy_strat_freq} {trade_strat_perf.lta} is stale ({trade_strat_perf.age_hours:.1f}h old), recalculating...")
            # Trigger recalculation for this specific strategy - use bulk call for all LTAs if multiple need refresh
            fresh_perf = cbtrade_db.db_trade_strat_perfs_recalc_single(prod_id, trade_strat_perf.buy_strat_type, trade_strat_perf.buy_strat_name, trade_strat_perf.buy_strat_freq, trade_strat_perf.lta)
            if fresh_perf:
                trade_strat_perf = fresh_perf
        
        # Calculate elapsed fields from timestamp columns for all consumers
        if hasattr(trade_strat_perf, 'last_buy_strat_bo_unix') and trade_strat_perf.last_buy_strat_bo_unix:
            trade_strat_perf.strat_bo_elapsed = (now_unix - trade_strat_perf.last_buy_strat_bo_unix) / 60
            if trade_strat_perf.strat_bo_elapsed > 9999:
                trade_strat_perf.strat_bo_elapsed = 9999
        else:
            trade_strat_perf.strat_bo_elapsed = 9999
            
        if hasattr(trade_strat_perf, 'last_buy_strat_pos_unix') and trade_strat_perf.last_buy_strat_pos_unix:
            trade_strat_perf.strat_pos_elapsed = (now_unix - trade_strat_perf.last_buy_strat_pos_unix) / 60
            if trade_strat_perf.strat_pos_elapsed > 9999:
                trade_strat_perf.strat_pos_elapsed = 9999
        else:
            trade_strat_perf.strat_pos_elapsed = 9999
            
        if hasattr(trade_strat_perf, 'last_buy_strat_unix') and trade_strat_perf.last_buy_strat_unix:
            trade_strat_perf.strat_last_elapsed = (now_unix - trade_strat_perf.last_buy_strat_unix) / 60
            if trade_strat_perf.strat_last_elapsed > 9999:
                trade_strat_perf.strat_last_elapsed = 9999
        else:
            trade_strat_perf.strat_last_elapsed = 9999
            
        results.append(trade_strat_perf)

    return results

#<=====>#

@narc(1)
def trade_strat_perfs_recalc_all(quote_symb:str=''):
    if debug_tf: G(f'==> trade_strat_perfs_base.trade_strat_perfs_recalc_all(quote_symb={quote_symb})')

    process_list = cbtrade_db.db_prod_ids_strats_traded(quote_symb=quote_symb)
    print(f'==> {len(process_list)} strategy variations to process for {quote_symb}')
    
    if not process_list:
        print(f'    No products found for quote_symb: {quote_symb}')
        return

    save_count = 0
    for x in process_list:
        x = AttrDict(x)
        # print(f'Processing: {x}')
        prod_id = x.prod_id
        buy_strat_type = x.buy_strat_type
        buy_strat_name = x.buy_strat_name
        buy_strat_freq = x.buy_strat_freq
            
        for lta in ('L', 'T', 'A'):
            trade_strat_perfs = trade_strat_perfs_get(prod_id=prod_id, buy_strat_type=buy_strat_type, buy_strat_name=buy_strat_name, buy_strat_freq=buy_strat_freq, lta=lta, force_recalc=True)
            for trade_strat_perf in trade_strat_perfs:
                # print(trade_strat_perf)
                # print(type(trade_strat_perf))
                # print(f"{spacer}{trade_strat_perf.prod_id:<20} {trade_strat_perf.buy_strat_type:<25} {trade_strat_perf.buy_strat_name:<25} {trade_strat_perf.buy_strat_freq:<25} {trade_strat_perf.lta:^1}")
                # Try different LTA values - start with common ones
                # Create TRADE_STRAT_PERF object with force_recalc=True
                trade_strat_perf = TRADE_STRAT_PERF(data=trade_strat_perf, force_recalc=True)
                # trade_strat_perf.db_save()
                save_count += 1
            
                print(f"{spacer} ✅ SAVED: {trade_strat_perf.prod_id:<20} {trade_strat_perf.buy_strat_type:<25} {trade_strat_perf.buy_strat_name:<25} {trade_strat_perf.buy_strat_freq:<25} {trade_strat_perf.lta:^1}")
                
    print(f'==> COMPLETED: {save_count} strategy performance records saved to database')

#<=====>#

@narc(1)
def trade_strat_perfs_recalc_sp(prod_id:str, buy_strat_type:str, buy_strat_name:str, buy_strat_freq:str, lta:str):
    """Minimal wrapper to call the MySQL stored procedure directly."""
    sql = ""
    sql += f"CALL sp_trade_strat_perfs_recalc('" \
           f"{prod_id}','{buy_strat_type}','{buy_strat_name}','{buy_strat_freq}','{lta}'" \
           f"');"
    cbtrade_db.upd(sql)

#<=====>#

@narc(1)
def trade_strat_perfs_recalc_sp_read(prod_id:str, buy_strat_type:str, buy_strat_name:str, buy_strat_freq:str, lta:str):
    """Call the stored procedure and return all result sets as list of dict lists."""
    from pymysql.cursors import DictCursor
    results = []
    conn = cbtrade_db.get_connection()
    with conn.cursor(DictCursor) as cur:
        cur.execute(
            "CALL sp_trade_strat_perfs_recalc(%s,%s,%s,%s,%s)",
            (prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta)
        )
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
def pair_trade_strat_perf_buy_upd(self, prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta=None):
    """
    Recalculate and persist strategy performance after a buy completes (per strategy, per L/T/A).
    """
    # if debug_tf:
    #     G(f"==> trade_strat_perfs_base.pair_trade_strat_perf_buy_upd()")
    #     G(f"    prod_id={prod_id}, buy_strat_type={buy_strat_type}")
    #     G(f"    buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta}")

    # perf = cbtrade_db.db_trade_strat_perfs_recalc_single(
    #     prod_id,
    #     buy_strat_type,
    #     buy_strat_name,
    #     buy_strat_freq,
    #     lta
    # )
    # if perf:
    #     try:
    #         # Nudge elapsed on successful buy update
    #         if isinstance(perf, dict) and 'strat_last_elapsed' in perf:
    #             perf['strat_last_elapsed'] = 0
    #         cbtrade_db.db_trade_strat_perfs_insupd(perf)
    #     except Exception as ex:
    #         print(f"WARNING: pair_trade_strat_perf_buy_upd persist failed: {ex}")
    #         sys.exit(1)
    # return perf
    sql = ""
    sql += f"update trade_strat_perfs "
    sql += f"set needs_recalc_yn = 'Y' "
    sql += f"where prod_id = '{prod_id}' "
    sql += f"and buy_strat_type = '{buy_strat_type}' "
    sql += f"and buy_strat_name = '{buy_strat_name}' "
    sql += f"and buy_strat_freq = '{buy_strat_freq}' "
    sql += f"and lta = '{lta}'"
    cbtrade_db.upd(sql)

#<=====>#

@narc(1)
def pair_trade_strat_perf_sell_upd(self, prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta=None):
    """
    Recalculate and persist strategy performance after a sell completes (per strategy, per L/T/A).
    """
    # if debug_tf:
    #     G(f"==> trade_strat_perfs_base.pair_trade_strat_perf_sell_upd()")
    #     G(f"    prod_id={prod_id}, buy_strat_type={buy_strat_type}")
    #     G(f"    buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta}")

    # perf = cbtrade_db.db_trade_strat_perfs_recalc_single(
    #     prod_id,
    #     buy_strat_type,
    #     buy_strat_name,
    #     buy_strat_freq,
    #     lta
    # )
    # if perf:
    #     try:
    #         # Nudge elapsed on successful buy update
    #         if isinstance(perf, dict) and 'strat_last_elapsed' in perf:
    #             perf['strat_last_elapsed'] = 0
    #         cbtrade_db.db_trade_strat_perfs_insupd(perf)
    #     except Exception as ex:
    #         print(f"WARNING: pair_trade_strat_perf_sell_upd persist failed: {ex}")
    #         sys.exit(1)
    # return perf
    sql = ""
    sql += f"update trade_strat_perfs "
    sql += f"set needs_recalc_yn = 'Y' "
    sql += f"where prod_id = '{prod_id}' "
    sql += f"and buy_strat_type = '{buy_strat_type}' "
    sql += f"and buy_strat_name = '{buy_strat_name}' "
    sql += f"and buy_strat_freq = '{buy_strat_freq}' "
    sql += f"and lta = '{lta}'"
    cbtrade_db.upd(sql)


#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    # debug = True
    for mkt in ('USD','USDC','BTC','ETH','SOL'):
        trade_strat_perfs_recalc_all(quote_symb=mkt)

#<=====>#
