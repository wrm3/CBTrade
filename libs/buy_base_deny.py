#<=====>#
# Description - Buy Core Logic
# 
# Core buy logic orchestration functions extracted from cls_bot_buy.py
# Contains buy object initialization and main buy logic workflow.
#<=====>#

#<=====>#
# Imports
#<=====>#
import os
import sys
import time
import traceback
from datetime import datetime as dt
from datetime import timezone
import tzlocal
from datetime import datetime as dt
from datetime import timezone
from typing import Optional
from fstrent_colors import cs
from libs.common import (
    print_adv 
    , AttrDict
    , AttrDictConv
    , AttrDictEnh
    , beep
    , dec
    , narc
    , dttm_unix
    , dttm_get
    , format_disp_age
    , format_disp_age2
    , format_disp_age3
    , speak
    )

from fstrent_colors import cs
from fstrent_colors import cs
from fstrent_colors import cs
from pprint import pprint

from libs.common import (
   AttrDict, AttrDictConv, beep, dec, dttm_get, print_adv, speak
)

# from libs.strat_base import buy_strats_check, buy_strats_deny, buy_strats_get
from libs.theme import *


#<=====>#
# Variables
#<=====>#
lib_name = 'buy_base_test'
log_name = 'buy_base_test'


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

@narc(1)
def buy_logic_deny(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_deny()')
    """
    General buy denial logic placeholder.
    Extracted from cls_bot_buy.py - preserved for future expansion.
    """
    pass

#<=====>#

@narc(1)
def buy_logic_mkt_deny(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_mkt_deny()')
    """
    Market-level buy denial logic placeholder.
    Extracted from cls_bot_buy.py - preserved for future expansion.
    """
    pass

#<=====>#

@narc(1)
def buy_logic_strat_deny(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny()')
    """
    Strategy-level buy denial orchestration function.
    Extracted from cls_bot_buy.py - preserves exact risk management flow.
    
    Handles:
    - Global buying on/off switch
    - Force sell product protection
    - Live vs test trading denial routing
    """

    self.buy_logic_strat_deny_buying_on()
    self.buy_logic_strat_deny_force_sell()

    # Deny Live Trades
    if self.buy.test_txn_yn == 'N':
        self.buy_logic_strat_deny_live()

    # Deny Test Trades
    if self.buy.test_txn_yn == 'Y':
        self.buy_logic_strat_deny_test()    

#<=====>#

@narc(1)
def buy_logic_strat_deny_buying_on(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_buying_on()')
    """
    Strategy-level buy denial orchestration function.
    Extracted from cls_bot_buy.py - preserves exact risk management flow.
    
    Handles:
    - Global buying on/off switch
    - Force sell product protection
    - Live vs test trading denial routing
    """

    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq
    mkts_open_cnt        = self.cbtrade_db.db_mkts_open_cnt_get(mkt=self.mkt.symb)

    cfg = self.st_pair.buy.buy_strat_delay_minutes
    # Support both mapping (per-frequency) and scalar configuration
    if isinstance(cfg, dict):
        restricts_buy_strat_delay_minutes = cfg.get(buy_strat_freq, cfg.get('***', 0))
    else:
        try:
            restricts_buy_strat_delay_minutes = int(cfg)
        except Exception:
            restricts_buy_strat_delay_minutes = 0

    self.buy.trade_strat_perf['T'].restricts_buy_strat_delay_minutes = restricts_buy_strat_delay_minutes
    self.buy.trade_strat_perf['L'].restricts_buy_strat_delay_minutes = restricts_buy_strat_delay_minutes
    self.buy.trade_strat_perf['A'].restricts_buy_strat_delay_minutes  = restricts_buy_strat_delay_minutes

    if self.st_pair.buy.buying_on_yn == 'N' :
        msg = f'buying has been turned off in settings...'
        # msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
        # self.buy.all_live_or_test.append(msg)

        self.buy.setting_name = 'self.st_pair.buy.buying_on_yn'
        self.buy.setting_value = self.st_pair.buy.buying_on_yn
        self.buy.buy_stat_name = None
        self.buy.buy_stat_value = None
        self.buy.test_fnc_name = sys._getframe().f_code.co_name
        self.buy.test_msg = msg
        self.set_test_mode()
        self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_force_sell(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_force_sell()')
    """
    Strategy-level buy denial orchestration function.
    Extracted from cls_bot_buy.py - preserves exact risk management flow.
    
    Handles:
    - Global buying on/off switch
    - Force sell product protection
    - Live vs test trading denial routing
    """

    prod_id              = self.buy.prod_id

    # Market Is Set To Sell Immediately
    if prod_id in self.st_pair.sell.force_sell.prod_ids:
        msg = f'{self.buy.prod_id} is in the forced_sell.prod_ids settings, and would instantly sell...'
        # msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
        # self.buy.all_live_or_test.append(msg)

        self.buy.setting_name = 'self.st_pair.sell.force_sell.prod_ids'
        # 🔴 GILFOYLE FIX: Convert list to comma-separated string for database insert
        self.buy.setting_value = ','.join(self.st_pair.sell.force_sell.prod_ids) if isinstance(self.st_pair.sell.force_sell.prod_ids, list) else str(self.st_pair.sell.force_sell.prod_ids)
        self.buy.buy_stat_name = 'prod_id'
        self.buy.buy_stat_value = prod_id
        self.buy.test_fnc_name = sys._getframe().f_code.co_name
        self.buy.test_msg = msg
        self.set_test_mode()
        self.set_deny_mode()

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====> 