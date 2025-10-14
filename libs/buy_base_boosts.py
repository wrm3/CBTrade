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
lib_name = 'buy_base_boosts'
log_name = 'buy_base_boosts'


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

@narc(1)
def buy_logic_mkt_boosts(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_mkt_boosts()')
    """
    Market-based boost logic for position limits and budget multipliers.
    Extracted from cls_bot_buy.py - preserves exact boost calculation logic.
    
    Applies market-level performance boosts:
    - Position limit doubling for good performers (>5 trades, >0.05% daily)
    - Budget multiplier doubling for excellent performers (>0.1% daily)
    
    EMERGENCY DISABLED - Position boost disabled to prevent excessive positions
    """

    # get default open position max for strat
    # add double override logic strat + prod
    # fixme
    self.buy.trade_perfs.restricts_open_poss_cnt_max = self.st_pair.buy.open_poss_cnt_max 

    # Keep budget multiplier boost as it doesn't affect position count
    if self.buy.trade_perfs['A'].gain_loss_close_pct_day > 0.1:
        self.buy.pair_budget_multiplier *= 2

#<=====>#

@narc(1)
def buy_logic_strat_boosts(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_boosts()')
    """
    Strategy-specific boost orchestration function.
    Extracted from cls_bot_buy.py - preserves exact orchestration logic.
    
    Coordinates strategy-level boosts:
    - Trade size boosts based on performance
    - Position limit boosts based on performance
    - Trade size cap enforcement
    """

    prod_id                       = self.buy.prod_id
    self.buy.buy_strat_type       = self.buy.trade_strat_perf['A'].buy_strat_type
    self.buy.buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    self.buy.buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    self.buy_logic_strat_boosts_trade_size()
    self.buy_logic_strat_boosts_position_max()

    if self.buy.trade_size > self.st_pair.buy.trade_size_max:
        msg = f'{self.buy.prod_id} {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} setting trade_size ${self.buy.trade_size} to cap max ${self.st_pair.buy.trade_size_max}... '
        self.buy.trade_size = self.st_pair.buy.trade_size_max
        self.buy.all_boosts.append(msg)

#<=====>#

@narc(1)
def buy_logic_strat_boosts_position_max(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_boosts_position_max()')
    """
    Strategy position limit boost calculations based on performance.
    Extracted from cls_bot_buy.py - preserves exact boost logic.
    
    Boosts position limits for strategies with:
    - Test mode: 25+ trades with >1% daily performance
    - Live mode: 25+ trades with >1% daily performance
    
    EMERGENCY DISABLED - This was causing excessive position opening
    """
    
    # DISABLED: This was causing position limits to grow exponentially 
    # if self.buy.trade_strat_perf['T'].tot_cnt >= 25 and self.buy.trade_strat_perf['T'].gain_loss_pct_day > 1:
    #     self.buy.trade_strat_perf['T'].restricts_max_open_poss_cnt *= 2
    #     if self.st_pair.buy.show_boosts_yn == 'Y':
    #         tsp_t = self.buy.trade_strat_perf['T']
    #         msg = f'{self.buy.prod_id} {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} has {tsp_t.tot_cnt} test closed trades with performance {tsp_t.gain_loss_pct_day:>.8f} % > 1 % boosting allowed open pos to {tsp_t.restricts_max_open_poss_cnt} ... '
    #         self.buy.all_boosts.append(msg)

    # DISABLED: This was causing position limits to grow exponentially 
    # if self.buy.trade_strat_perf['A'].tot_cnt >= 25 and max(self.buy.trade_strat_perf['A'].gain_loss_pct_day, self.buy.trade_strat_perf['L'].gain_loss_pct_day) > 1:
    #     self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt *= 2
    #     if self.st_pair.buy.show_boosts_yn == 'Y':
    #         tsp_a = self.buy.trade_strat_perf['A']
    #         tsp_l = self.buy.trade_strat_perf['L']
    #         msg = f'{self.buy.prod_id} {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} has {tsp_a.tot_cnt} closed trades with performance {max(tsp_a.gain_loss_pct_day, tsp_l.gain_loss_pct_day):>.8f} % > 1 % boosting allowed open pos to {tsp_l.restricts_max_open_poss_cnt} ... '
    #         self.buy.all_boosts.append(msg)
    
    # Add logging to show we're using base limits
    if self.st_pair.buy.show_boosts_yn == 'Y':
        msg = f'EMERGENCY MODE: {self.buy.prod_id} {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} using base position limits (boost disabled)'
        self.buy.all_boosts.append(msg)

#<=====>#

@narc(1)
def buy_logic_strat_boosts_trade_size(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_boosts_trade_size()')
    """
    Strategy trade size boost calculations based on performance.
    Extracted from cls_bot_buy.py - preserves exact boost calculation logic.
    
    Complex boost system with:
    - Minimum trade size initialization
    - Base trade size for positive performers
    - Fibonacci-like progressive boosts for exceptional performers
    - Performance thresholds: Configurable via settings (default: 0.10%, 0.25%, 0.5%, 1%, 3%, 5%, 8%, 13%, 21%, 34%, 55%, 89%)
    """
 
    prod_id = self.buy.prod_id
    strat_name = self.buy.buy_strat_name
    strat_freq = self.buy.buy_strat_freq

    tests_min                  = self.st_pair.strats[self.buy.buy_strat_name].buy.tests_min
    # tests_max                  = self.st_pair.strats[self.buy.buy_strat_name].buy.tests_max
    boost_tests_min            = self.st_pair.strats[self.buy.buy_strat_name].buy.boost_tests_min[self.buy.buy_strat_freq] 

    self.buy.trade_size       = self.buy.quote_size_min * self.st_pair.buy.trade_size_min_mult
    msg = f'{prod_id} ==> {strat_name} - {strat_freq} - quote_size_min {self.buy.quote_size_min} * trade_size_min_mult {self.st_pair.buy.trade_size_min_mult} = trade size : {self.buy.trade_size}... '
    self.buy.all_boosts.append(msg)

    #<=====>#

    # Live
    # give default value to strat with some history and positive impact
    if self.buy.trade_strat_perf['A'].tot_cnt >= tests_min and self.buy.trade_strat_perf['A'].gain_loss_pct_day  > 0:
        trade_size_b4 = self.buy.trade_size
        self.buy.trade_size = max(self.st_pair.buy.trade_size, self.buy.trade_size)
        msg = f'{prod_id} ==> {strat_name} - {strat_freq} - max ( st_pair.buy.trade_size {self.st_pair.buy.trade_size} , trade_size {trade_size_b4} ) = trade size : {self.buy.trade_size}... '
        self.buy.all_boosts.append(msg)

    #<=====>#

    tot_cnt = self.buy.trade_strat_perf['A'].tot_cnt
    live_gain_loss_pct_day = max(self.buy.trade_strat_perf['A'].gain_loss_pct_day, self.buy.trade_strat_perf['L'].gain_loss_pct_day)

    # Boost Trade Size for those with proven track records
    self.buy.pair_strat_budget_multiplier = 1.0
    # Get boost thresholds from settings (default to Fibonacci-like progression)
    daily_pct_rates = self.st_pair.buy.trade_size_boost_thresholds_pct_day
    for daily_pct_rate in daily_pct_rates:
        if self.buy.trade_strat_perf['A'].tot_cnt >= boost_tests_min:
            # Live
            if live_gain_loss_pct_day > daily_pct_rate:
                size_b4 = self.buy.trade_size
#                self.buy.trade_size *= 2
                self.buy.trade_size += self.buy.trade_size
                msg = f'{prod_id} ==> {strat_name} - {strat_freq} has {tot_cnt} closed trades with performance {live_gain_loss_pct_day:>.8f} % > {daily_pct_rate} % boosting trade size from {size_b4} => {self.buy.trade_size} ... '
                self.buy.all_boosts.append(msg)

    msg = f'{prod_id} ==> {strat_name} - {strat_freq} - buy_logic_strat_boosts_trade_size final trade size : {self.buy.trade_size}... '
    self.buy.all_boosts.append(msg)

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====> 