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
lib_name = 'buy_base_deny_test'
log_name = 'buy_base_deny_test'


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

@narc(1)
def buy_logic_strat_deny_test(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_test()')
    """
    Test trading denial logic with comprehensive risk management.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Performance-based test mode switching
    - Market position limits
    - Strategy position limits  
    - Product position limits
    - Timing delays and elapsed time checks
    - Budget and spending limits
    - Coinbase limit-only market protection
    - Large bid-ask spread protection
    """

    # Elapsed fields are now calculated centrally in trade_strat_perfs_get_all() - no need to recalculate

    self.buy_logic_strat_deny_test_strategy_open_position_limit()
    self.buy_logic_strat_deny_test_product_timing_delay()
    self.buy_logic_strat_deny_test_strategy_timing_delay()
    self.buy_logic_strat_deny_test_large_bid_ask_spread()

#<=====>#

@narc(1)
def buy_logic_strat_deny_test_strategy_open_position_limit(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_test_strategy_open_position_limit()')
    """
    Test strategy open position limit denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Test strategy open position limit protection
    """


    prod_id              = self.buy.prod_id
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq
    test_txns_on_yn      = self.st_pair.buy_test_txns.test_txns_on_yn

    # Exceeded Max Open Positions In This Strat
    strat_open_test_cnt  = int(self.buy.trade_strat_perf['T'].tot_open_cnt)
    if self.buy.test_txn_yn == 'Y':

        if strat_open_test_cnt >= self.buy.trade_strat_perf['T'].restricts_max_open_poss_cnt:
            tsp_t = self.buy.trade_strat_perf['T']
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {strat_open_test_cnt} / {tsp_t.restricts_max_open_poss_cnt} open test trades, switching to test position... '
            self.buy.all_denies.append(msg)

            # 🔴 REMOVED direct flag set - set_deny_mode() handles this + forensic logging
            # msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
            # self.buy.all_live_or_test.append(msg)

            self.buy.setting_name = 'self.buy.trade_strat_perfs[T].restricts_max_open_poss_cnt'
            self.buy.setting_value = self.buy.trade_strat_perf['T'].restricts_max_open_poss_cnt
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[T].tot_open_cnt'
            self.buy.buy_stat_value = strat_open_test_cnt

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_test_product_timing_delay(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_test_product_timing_delay()')
    """
    Test product timing delay denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Test product timing delay protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn      = self.st_pair.buy_test_txns.test_txns_on_yn
    test_delay_minutes = self.st_pair.buy.buy_delay_minutes

    # Elapsed Since Last Product Buy
    test_prod_elapsed = self.buy.trade_perfs['T'].last_elapsed
    if self.buy.test_txn_yn == 'Y':
        msg = f'{prod_id} last product buy was {test_prod_elapsed} / {test_delay_minutes} ago minutes'
        # self.buy.all_live_or_test.append(msg)

        # tsp_t = self.buy.trade_strat_perf['T']
        # formatted_label = buy_strat_name + ' - ' + buy_strat_freq + ' - test : strat_last_elapsed ==> '
        # self.buy.all_live_or_test.append(f'{formatted_label:<50} {tsp_t.strat_last_elapsed:>5} / {test_strat_delay_minutes:>4}')

        if test_delay_minutes != 0 and test_prod_elapsed < test_delay_minutes:
            # msg = f'{prod_id} last product buy was {test_prod_elapsed} minutes ago, waiting until {test_strat_delay_minutes} minutes, denying test trade...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                # msg = f'{prod_id} last product buy was {test_prod_elapsed} minutes / {test_strat_delay_minutes} ago minutes...'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'test_delay_minutes'
                self.buy.setting_value = test_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_perfs.last_elapsed'
                self.buy.buy_stat_value = test_prod_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # msg = f'{prod_id} last product buy was {test_prod_elapsed} minutes / {test_strat_delay_minutes} ago minutes...'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'test_delay_minutes'
                self.buy.setting_value = test_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_perfs.last_elapsed'
                self.buy.buy_stat_value = test_prod_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

        # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn}')

#<=====>#

@narc(1)
def buy_logic_strat_deny_test_strategy_timing_delay(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_test_strategy_timing_delay()')
    """
    Test strategy timing delay denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Test strategy timing delay protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn
    buy_strat_type       = self.buy.trade_strat_perf['A'].buy_strat_type
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    # Use settings-based delays instead of hardcoded values
    test_strat_delay_minutes = self.st_pair.buy.buy_strat_delay_minutes

    # Elapsed Since Last Product & Strat & Freq Buy
    test_strat_elapsed = self.buy.trade_strat_perf['T'].strat_last_elapsed
    if self.buy.test_txn_yn == 'Y':
        msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {test_strat_elapsed} / {test_strat_delay_minutes} ago minutes...'
        # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)
        # self.buy.all_live_or_test.append(f'{buy_strat_name} - {buy_strat_freq} - test : strat_last_elapsed {test_strat_elapsed:>5} / {test_strat_delay_minutes:>5}')

        if test_strat_delay_minutes != 0 and test_strat_elapsed < test_strat_delay_minutes:
            # msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {test_strat_elapsed} minutes ago, waiting until {test_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            # msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {test_strat_elapsed} / {test_strat_delay_minutes} ago minutes...'
            # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'test_strat_delay_minutes'
            self.buy.setting_value = test_strat_delay_minutes
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[T].strat_last_elapsed'
            self.buy.buy_stat_value = test_strat_elapsed

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_test_large_bid_ask_spread(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_test_large_bid_ask_spread()')
    """
    Large bid-ask spread denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Large bid-ask spread protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Very Large Bid Ask Spread
    if self.buy.test_txn_yn == 'Y':
        if self.buy.prc_range_pct >= 2:
            msg = f'{prod_id} has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... skipping buy'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            # msg = f'{prod_id} has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... skipping buy'
            # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'self.buy.prc_range_pct'
            self.buy.setting_value = self.buy.prc_range_pct
            self.buy.buy_stat_name = 'self.buy.prc_range_pct'
            self.buy.buy_stat_value = self.buy.prc_range_pct

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_deny_mode()

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====> 