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
lib_name = 'buy_base_deny_live'
log_name = 'buy_base_deny_live'


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

@narc(1)
def buy_logic_strat_deny_live(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live()')
    """
    Live trading denial logic with comprehensive risk management.
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

    prod_id              = self.buy.prod_id
    buy_strat_type       = self.buy.trade_strat_perf['A'].buy_strat_type
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    # find Me to remove after edits on 2025-09-06
    # r = self.cbtrade_db.db_mkt_strat_elapsed_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, test_txn_yn='N', show_sql_yn='N')
    # if r and len(r) >= 3:
    #     self.buy.trade_strat_perf['L'].strat_bo_elapsed   = r[0]
    #     self.buy.trade_strat_perf['L'].strat_pos_elapsed  = r[1]
    #     self.buy.trade_strat_perf['L'].strat_last_elapsed = r[2]
    #     if self.buy.trade_strat_perf['L'].strat_bo_elapsed > 9999:
    #         self.buy.trade_strat_perf['L'].strat_bo_elapsed = 9999
    #     if self.buy.trade_strat_perf['L'].strat_pos_elapsed > 9999:
    #         self.buy.trade_strat_perf['L'].strat_pos_elapsed = 9999
    #     if self.buy.trade_strat_perf['L'].strat_last_elapsed > 9999:
    #         self.buy.trade_strat_perf['L'].strat_last_elapsed = 9999
    # else:
    #     self.buy.trade_strat_perf['L'].strat_bo_elapsed   = 9999
    #     self.buy.trade_strat_perf['L'].strat_pos_elapsed  = 9999
    #     self.buy.trade_strat_perf['L'].strat_last_elapsed = 9999

    self.buy_logic_strat_deny_live_paper_trades_mode()
    self.buy_logic_strat_deny_live_test_mode_switch()
    self.buy_logic_strat_deny_live_market_open_position_limit()
    self.buy_logic_strat_deny_live_strategy_open_position_limit()
    self.buy_logic_strat_deny_live_product_open_position_limit()
    self.buy_logic_strat_deny_live_product_timing_delay()
    self.buy_logic_strat_deny_live_strategy_timing_delay()
    self.buy_logic_strat_deny_live_budget_pair_spending_limit()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_paper_trades_mode(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_paper_trades_mode()')
    """
    Live paper trades mode denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Live paper trades mode protection
    """

    if self.st_mkt.paper_trades_only_yn == 'Y':
        msg = f"paper_trades_only_yn = {self.st_mkt.paper_trades_only_yn}"
        self.buy.test_reason = msg
        # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

        self.buy.setting_name = 'self.st_mkt.paper_trades_only_yn'
        self.buy.setting_value = self.st_mkt.paper_trades_only_yn
        self.buy.buy_stat_name = 'self.st_mkt.paper_trades_only_yn'
        self.buy.buy_stat_value = self.st_mkt.paper_trades_only_yn
        self.buy.test_fnc_name = sys._getframe().f_code.co_name
        self.buy.test_msg = msg
        self.set_test_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_test_mode_switch(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_test_mode_switch()')
    """
    Live test mode switch denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Live test mode switch protection
    """

    prod_id              = self.buy.prod_id
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    tot_close_cnt              = self.buy.trade_strat_perf['A'].tot_close_cnt
    gain_loss_close_pct_day    = self.buy.trade_strat_perf['A'].gain_loss_close_pct_day
    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn
    test_txns_min               = self.st_pair.buy_test_txns.test_txns_min
    test_txns_max               = self.st_pair.buy_test_txns.test_txns_max
    # Get profitability threshold - already resolved by settings system for this prod_id
    profit_threshold            = self.st_pair.buy_test_txns.profitability_threshold_pct_day
    
    if self.buy.test_txn_yn == 'N':
        if test_txns_on_yn == 'Y' and tot_close_cnt < test_txns_min:
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {tot_close_cnt} trades  setting test mode ... '
            self.buy.test_reason = msg
            # msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
            # self.buy.all_live_or_test.append(msg)

            self.buy.setting_name = 'self.st_pair.buy_test_txns.test_txns_min'
            self.buy.setting_value = self.st_pair.buy_test_txns.test_txns_min
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[A].tot_close_cnt'
            self.buy.buy_stat_value = self.buy.trade_strat_perf['A'].tot_close_cnt
            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_test_mode()

        elif test_txns_on_yn == 'Y' and tot_close_cnt <= test_txns_max and gain_loss_close_pct_day < profit_threshold:
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {tot_close_cnt} trades with performance {gain_loss_close_pct_day:>.8f} % < {profit_threshold} % setting test mode... '
            self.buy.all_test_reasons.append(msg)
            self.buy.test_reason = msg
            # 🔴 REMOVED direct flag set - set_test_mode() handles this + forensic logging
            # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'st_pair.buy_test_txns.test_txns_max'
            self.buy.setting_value = self.st_pair.buy_test_txns.test_txns_max
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[A].tot_close_cnt'
            self.buy.buy_stat_value = self.buy.trade_strat_perf['A'].tot_close_cnt

            self.buy.setting_name2 = 'st_pair.buy_test_txns.profitability_threshold_pct_day'
            self.buy.setting_value2 = profit_threshold
            self.buy.buy_stat_name2 = 'self.buy.trade_strat_perfs[A].gain_loss_close_pct_day'
            self.buy.buy_stat_value2 = self.buy.trade_strat_perf['A'].gain_loss_close_pct_day

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_test_mode()

        elif test_txns_on_yn == 'Y' and tot_close_cnt > test_txns_max and gain_loss_close_pct_day < profit_threshold:
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {tot_close_cnt} trades with performance {gain_loss_close_pct_day:>.8f} % < {profit_threshold} % reducing allowed open pos, max pos 1 ... '
            self.buy.all_limits.append(msg)
            self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt = 1
            self.buy.trade_strat_perf['T'].restricts_max_open_poss_cnt = 1
            self.buy.test_reason = msg
            # 🔴 REMOVED direct flag set - set_test_mode() handles this + forensic logging
            # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'st_pair.buy_test_txns.test_txns_max'
            self.buy.setting_value = self.st_pair.buy_test_txns.test_txns_max
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[A].tot_close_cnt'
            self.buy.buy_stat_value = self.buy.trade_strat_perf['A'].tot_close_cnt

            self.buy.setting_name2 = 'st_pair.buy_test_txns.profitability_threshold_pct_day'
            self.buy.setting_value2 = profit_threshold
            self.buy.buy_stat_name2 = 'self.buy.trade_strat_perfs[A].gain_loss_close_pct_day'
            self.buy.buy_stat_value2 = self.buy.trade_strat_perf['A'].gain_loss_close_pct_day

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_test_mode()

        elif gain_loss_close_pct_day < profit_threshold:
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {tot_close_cnt} closed trades with performance {gain_loss_close_pct_day:>.8f} % < {profit_threshold} % reducing allowed open pos, max pos 1 ... '
            self.buy.all_test_reasons.append(msg)
            self.buy.test_reason = msg
            self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt = 1
            self.buy.trade_strat_perf['T'].restricts_max_open_poss_cnt = 1
            # 🔴 REMOVED direct flag set - set_test_mode() handles this + forensic logging
            # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'st_pair.buy_test_txns.profitability_threshold_pct_day'
            self.buy.setting_value = profit_threshold
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[A].gain_loss_close_pct_day'
            self.buy.buy_stat_value = self.buy.trade_strat_perf['A'].gain_loss_close_pct_day

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_test_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_market_open_position_limit(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_market_open_position_limit()')
    """
    Live market open position limit denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Live market open position limit protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Exceeded Max Count of Different Products in this Market
    mkts_open_cnt        = self.cbtrade_db.db_mkts_open_cnt_get(mkt=self.mkt.symb)
    mkts_open_max        = self.st_pair.buy.mkts_open_max
    if self.buy.test_txn_yn == 'N':
        if mkts_open_cnt >= mkts_open_max:
            msg = f'{prod_id} maxed out {self.mkt.symb} market, {mkts_open_cnt} of max : {mkts_open_max}...'
            self.buy.all_denies.append(msg)
            if test_txns_on_yn == 'Y':
                test_reason = f'flipping to test since {msg}'
                self.buy.test_reason = test_reason
                # msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
                # self.buy.all_live_or_test.append(msg)

                self.buy.setting_name = 'self.st_pair.buy.mkts_open_max'
                self.buy.setting_value = self.st_pair.buy.mkts_open_max
                self.buy.buy_stat_name = 'db_mkts_open_cnt_get(mkt=self.mkt.symb)'
                self.buy.buy_stat_value = mkts_open_cnt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
                # self.buy.all_live_or_test.append(msg)

                self.buy.setting_name = 'self.st_pair.buy.mkts_open_max'
                self.buy.setting_value = self.st_pair.buy.mkts_open_max
                self.buy.buy_stat_name = 'db_mkts_open_cnt_get(mkt=self.mkt.symb)'
                self.buy.buy_stat_value = mkts_open_cnt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_strategy_open_position_limit(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_strategy_open_position_limit()')
    """
    Live strategy open position limit denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Live strategy open position limit protection
    """

    prod_id              = self.buy.prod_id
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq
    test_txns_on_yn      = self.st_pair.buy_test_txns.test_txns_on_yn

    # Exceeded Max Open Positions In This Strat
    strat_open_live_cnt  = int(self.buy.trade_strat_perf['L'].tot_open_cnt)
    if self.buy.test_txn_yn == 'N':
        if strat_open_live_cnt >= self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt:
            max_pos_cnt = self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {strat_open_live_cnt} / {max_pos_cnt} open live trades, switching to test position... '
            self.buy.all_denies.append(msg)
            if test_txns_on_yn == 'Y':
                # 🔴 REMOVED direct flag set - set_test_mode() handles this + forensic logging
                self.buy.test_reason = msg
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.trade_strat_perfs[L].restricts_max_open_poss_cnt'
                self.buy.setting_value = self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt
                self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[L].tot_open_cnt'
                self.buy.buy_stat_value = strat_open_live_cnt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
                # self.buy.all_live_or_test.append(msg)

                self.buy.setting_name = 'self.buy.trade_strat_perfs[L].restricts_max_open_poss_cnt'
                self.buy.setting_value = self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt
                self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[L].tot_open_cnt'
                self.buy.buy_stat_value = strat_open_live_cnt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_product_open_position_limit(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_product_open_position_limit()')
    """
    Live product open position limit denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Live product open position limit protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn      = self.st_pair.buy_test_txns.test_txns_on_yn

    # Exceeded Max Open Positions In This Product
    prod_open_poss_cnt   = self.buy.trade_perfs['L'].tot_open_cnt
    if self.buy.test_txn_yn == 'N':
        if prod_open_poss_cnt >= self.buy.trade_perfs.restricts_open_poss_cnt_max:
            msg = f'{prod_id} maxed out {prod_open_poss_cnt} allowed positions in this product, max : {self.buy.trade_perfs.restricts_open_poss_cnt_max}, bypassing buy logic...'
            self.buy.all_denies.append(msg)
            if test_txns_on_yn == 'Y':
                # 🔴 REMOVED direct flag set - set_test_mode() handles this + forensic logging
                self.buy.test_reason = f'flipping to test since {msg}'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.trade_perfs.restricts_open_poss_cnt_max'
                self.buy.setting_value = self.buy.trade_perfs.restricts_open_poss_cnt_max
                self.buy.buy_stat_name = 'self.buy.trade_perfs.live_open_poss_cnt'
                self.buy.buy_stat_value = prod_open_poss_cnt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # 🔴 REMOVED direct flag set - set_deny_mode() handles this + forensic logging
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.trade_perfs.restricts_open_poss_cnt_max'
                self.buy.setting_value = self.buy.trade_perfs.restricts_open_poss_cnt_max
                self.buy.buy_stat_name = 'self.buy.trade_perfs.live_open_poss_cnt'
                self.buy.buy_stat_value = prod_open_poss_cnt
                
                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_product_timing_delay(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_product_timing_delay()')
    """
    Live product timing delay denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Live product timing delay protection
    """
    prod_id              = self.buy.prod_id
    live_delay_minutes = self.st_pair.buy.buy_delay_minutes

    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Elapsed Since Last Product Buy
    live_prod_elapsed = self.buy.trade_perfs['L'].last_elapsed
    if self.buy.test_txn_yn == 'N':
        msg = f'{prod_id} last prod_id => {live_prod_elapsed} / {live_delay_minutes} ago minutes'
        # self.buy.all_live_or_test.append(msg)
        # strategy_info = f'{buy_strat_name} - {buy_strat_freq} - live : strat_last_elapsed ==> {strategy_info:<50} {self.buy.trade_perfs['L'].last_elapsed:>5} / {live_strat_delay_minutes:>4}'
        # self.buy.all_live_or_test.append(f'{strategy_info:<50} {self.buy.trade_perfs['L'].last_elapsed:>5} / {live_strat_delay_minutes:>4}')

        if live_delay_minutes != 0 and live_prod_elapsed <= live_delay_minutes:
            # msg = f'{prod_id} last product buy was {live_prod_elapsed} minutes ago, waiting until {live_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                # msg = f'{prod_id} last product buy was {live_prod_elapsed} minutes / {live_strat_delay_minutes} ago minutes...'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'live_delay_minutes'
                self.buy.setting_value = live_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_perfs.last_elapsed'
                self.buy.buy_stat_value = live_prod_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # msg = f'{prod_id} last product buy was {live_prod_elapsed} minutes / {live_strat_delay_minutes} ago minutes...'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'live_delay_minutes'
                self.buy.setting_value = live_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_perfs.last_elapsed'
                self.buy.buy_stat_value = live_prod_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

        # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn}')

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_strategy_timing_delay(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_strategy_timing_delay()')
    """
    Live strategy timing delay denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Live strategy timing delay protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn      = self.st_pair.buy_test_txns.test_txns_on_yn
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    # Use settings-based delays instead of hardcoded values
    live_strat_delay_minutes = self.st_pair.buy.buy_strat_delay_minutes

    # Elapsed Since Last Product & Strat & Freq Buy
    live_strat_elapsed = self.buy.trade_strat_perf['L'].strat_last_elapsed
    if self.buy.test_txn_yn == 'N':
        msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} live buy => {live_strat_elapsed} / {live_strat_delay_minutes} ago minutes...'
        # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)
        # self.buy.all_live_or_test.append(f'{buy_strat_name} - {buy_strat_freq} - live : strat_last_elapsed {live_strat_elapsed:>5} / {live_strat_delay_minutes:>5}')

        if live_strat_delay_minutes != 0 and live_strat_elapsed < live_strat_delay_minutes:
            # msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {live_strat_elapsed} minutes ago, waiting until {live_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                # msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {live_strat_elapsed} minutes ago, waiting until {live_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'live_strat_delay_minutes'
                self.buy.setting_value = live_strat_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[L].strat_last_elapsed'
                self.buy.buy_stat_value = live_strat_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {live_strat_elapsed} minutes ago, waiting until {live_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'live_strat_delay_minutes'
                self.buy.setting_value = live_strat_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[L].strat_last_elapsed'
                self.buy.buy_stat_value = live_strat_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_budget_pair_spending_limit(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_budget_pair_spending_limit()')
    """
    Budget pair spending limit denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Budget pair spending limit protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Exceeded Max Spend Per Product    
    if self.buy.test_txn_yn == 'N':
        pair_spent_amt = self.budget.pair_spent_amt 
        trade_size = self.buy.trade_size 
        pair_spend_max_amt = self.budget.pair_spend_max_amt

        msg = f'{prod_id} has spent {pair_spent_amt} of {pair_spend_max_amt} and trade size is {trade_size}...'
        # self.buy.all_live_or_test.append(msg)

        if self.budget.pair_spent_amt + self.buy.trade_size > self.budget.pair_spend_max_amt:
            # msg = f'{prod_id} has spent {pair_spent_amt} and a purchase of {trade_size} wil exceed > {pair_spend_max_amt} ...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                # msg = f'{prod_id} has spent {pair_spent_amt} and a purchase of {trade_size} wil exceed > {pair_spend_max_amt} ...'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.budget.pair_spent_amt + self.buy.trade_size'
                self.buy.setting_value = self.budget.pair_spent_amt + self.buy.trade_size
                self.buy.buy_stat_name = 'self.budget.pair_spent_amt'
                self.buy.buy_stat_value = self.budget.pair_spent_amt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # msg = f'{prod_id} has spent {pair_spent_amt} and a purchase of {trade_size} wil exceed > {pair_spend_max_amt} ...'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.budget.pair_spent_amt + self.buy.trade_size'
                self.buy.setting_value = self.budget.pair_spent_amt + self.buy.trade_size
                self.buy.buy_stat_name = 'self.budget.pair_spent_amt'
                self.buy.buy_stat_value = self.budget.pair_spent_amt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_market_limit_only(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_market_limit_only()')
    """
    Market limit-only denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Coinbase limit-only market protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Market Is Set To Limit Only on Coinbase
    if self.buy.test_txn_yn == 'N':
        if self.buy.mkt_limit_only_tf == 1:
            msg = f'{prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                # msg = f'{prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.mkt_limit_only_tf'
                self.buy.setting_value = self.buy.mkt_limit_only_tf
                self.buy.buy_stat_name = 'self.buy.mkt_limit_only_tf'
                self.buy.buy_stat_value = self.buy.mkt_limit_only_tf

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # msg = f'{prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.mkt_limit_only_tf'
                self.buy.setting_value = self.buy.mkt_limit_only_tf
                self.buy.buy_stat_name = 'self.buy.mkt_limit_only_tf'
                self.buy.buy_stat_value = self.buy.mkt_limit_only_tf

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

#<=====>#

@narc(1)
def buy_logic_strat_deny_live_large_bid_ask_spread(self):
    if self.debug_tf: G(f'==> buy_base.buy_logic_strat_deny_live_large_bid_ask_spread()')
    """
    Large bid-ask spread denial logic.
    Extracted from cls_bot_buy.py - preserves exact safety logic.
    
    Handles:
    - Large bid-ask spread protection
    """

    prod_id              = self.buy.prod_id
    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Very Large Bid Ask Spread
    if self.buy.test_txn_yn == 'N':
        if self.buy.prc_range_pct >= 2:
            msg = f'{prod_id} has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... skipping buy'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                # msg = f'{prod_id} has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... skipping buy'
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.prc_range_pct'
                self.buy.setting_value = self.buy.prc_range_pct
                self.buy.buy_stat_name = 'self.buy.prc_range_pct'
                self.buy.buy_stat_value = self.buy.prc_range_pct

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                # msg = f'{prod_id} has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... denying buy'
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