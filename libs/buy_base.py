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
lib_name = 'buy_core'
log_name = 'buy_core'


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

@narc(1)
def disp_buy_header(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_header()')
    """
    Display buy logic header with performance metrics columns.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    # if self.first_tf:
    if self.pair.show_buy_header_tf:
        hmsg = ""
        hmsg += f"{'strat':<15} | "
        hmsg += f"{'freq':<7} | "
        hmsg += f"{'total':^5} | "
        hmsg += f"{'open_test':^11} | "
        hmsg += f"{'open_live':^11} | "
        hmsg += f"{'close':^5} | "
        hmsg += f"{'wins':^5} | "
        hmsg += f"{'lose':^5} | "
        hmsg += f"{'win':^6} % | "
        hmsg += f"{'lose':^6} % | "
        hmsg += f"{'gain_amt':^12} | "
        hmsg += f"{'gain_amt_live':^14} | "
        hmsg += f"{'gain_pct':^10} % | "
        hmsg += f"{'gain_hr':^10} % | "
        hmsg += f"{'gain_day':^10} % | "
        hmsg += f"{'elapsed':^10} | "
        hmsg += f"{'trade_size':^16} | "
        hmsg += f"{'buy':^3} | "
        hmsg += f"{'test':^4} | "
        hmsg += f"{'deny':^4} | "
        hmsg += f"{'last_buy_sign':^20} "

        title_msg = f'* {self.buy.prod_id} * BUY LOGIC *'

        self.chrt.chart_top(in_str=title_msg, len_cnt=260, bold=True)
        guide = ""
        guide += f"{'':<15} | "
        guide += f"{'':<7} | "
        guide += f"{'A':^5} | "
        guide += f"{'T':^11} | "
        guide += f"{'L':^11} | "
        guide += f"{'A':^5} | "
        guide += f"{'A':^5} | "
        guide += f"{'A':^5} | "
        guide += f"{'A':^6}   | "
        guide += f"{'A':^6}   | "
        guide += f"{'A':^12} | "
        guide += f"{'L':^14} | "
        guide += f"{'A':^10}   | "
        guide += f"{'A':^10}   | "
        guide += f"{'A':^10}   | "
        guide += f"{'A':^10} | "
        guide += f"{'':^16} | "
        guide += f"{'':^3} | {'':^4} | {'':^4} | {'':^20}"
        self.chrt.chart_headers(in_str=guide, len_cnt=260, bold=True)
        self.chrt.chart_headers(in_str=hmsg, len_cnt=260, bold=True)
        self.pair.show_buy_header_tf = False

#<=====>#

@narc(1)
def disp_buy(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy()')
    """
    Display main buy logic information with strategy performance and timing data.
    Extracted from cls_bot_buy.py - preserves exact formatting and color logic.
    """

    prod_id          = self.buy.prod_id

    if self.buy.buy_yn == 'Y':
        self.pair.show_buy_header_tf = True

    if self.buy.buy_yn == 'Y':
        self.pair.show_buy_header_tf = True

    if self.pair.show_buy_header_tf:
        self.disp_buy_header()
        self.pair.show_buy_header_tf = False

    freq = self.buy.trade_strat_perf['A'].buy_strat_freq
    df = self.buy.ta[freq].df
    latest_timestamp = df.index.max()
    latest_timestamp_local = latest_timestamp.tz_localize('UTC')

    msg1 = ''
    tsp_a = self.buy.trade_strat_perf['A']  # Extract to avoid f-string quote conflicts
    tsp_t = self.buy.trade_strat_perf['T']
    tsp_l = self.buy.trade_strat_perf['L']
    
    msg1 += f'{tsp_a.buy_strat_name:<15}' + ' | '
    msg1 += f'{tsp_a.buy_strat_freq:<7}' + ' | '
    msg1 += f'{int(tsp_a.tot_cnt):>5}' + ' | '

    msg1 += f'{int(tsp_t.tot_open_cnt):^5}/{int(tsp_t.restricts_max_open_poss_cnt):^5}' + ' | '
    msg1 += f'{int(tsp_l.tot_open_cnt):^5}/{int(tsp_l.restricts_max_open_poss_cnt):^5}' + ' | '

    msg1 += f'{int(tsp_a.tot_close_cnt):>5}' + ' | '
    msg1 += f'{int(tsp_a.win_cnt):>5}' + ' | '
    msg1 += f'{int(tsp_a.lose_cnt):>5}' + ' | '
    msg1 += f'{tsp_a.win_pct:>6.2f} %' + ' | '
    msg1 += f'{tsp_a.lose_pct:>6.2f} %' + ' | '
    msg1 += f'{tsp_a.gain_loss_amt:>12.2f}' + ' | '
    msg1 += f'{tsp_l.gain_loss_amt:>14.2f}' + ' | '
    msg1 += f'{tsp_a.gain_loss_pct:>10.2f} %' + ' | '
    msg1 += f'{tsp_a.gain_loss_pct_hr:>10.2f} %' + ' | '
    msg1 += f'{tsp_a.gain_loss_pct_day:>10.2f} %' + ' | '
    elapsed_seconds = int(dttm_unix()) - int(tsp_a.last_buy_strat_unix or 0)
    msg1 += f'{format_disp_age3(elapsed_seconds):>10}' + ' | '
    msg1 += f'{self.buy.trade_size:>16.8f}'

    font_color = 'white'
    bg_color = 'black'
    if tsp_a.tot_cnt > 0:
        if tsp_a.tot_cnt > self.st_pair.buy_test_txns.test_txns_min:
            if tsp_a.gain_loss_pct_day > 0:
                font_color = 'white'
                bg_color = 'green'
            elif tsp_a.gain_loss_pct_day < 0:
                font_color = 'white'
                bg_color = 'red'
        else:
            if tsp_a.gain_loss_pct_day > 0:
                font_color = 'green'
                bg_color = 'black'
            elif tsp_a.gain_loss_pct_day < 0:
                font_color = 'red'
                bg_color = 'black'
    msg1 = cs(msg1, font_color=font_color, bg_color=bg_color) + ' | '

    msg2 = f'{self.buy.buy_yn:^3}' 
    msg3 = f'{self.buy.test_txn_yn:^4}'
    msg4 = f'{self.buy.buy_deny_yn:^4}'
    last_buy_sign = None
    last_buy_sign_str  = ''
    # Candidate 1: in-memory signal from current TA window
    mem_last = None
    if self.buy.buy_hist:
        try:
            mem_last = max(self.buy.buy_hist)
        except Exception:
            mem_last = None
    # Candidate 2: persisted history from trade_strat_perfs_get_all select (if provided)
    db_last = None
    try:
        db_last = getattr(tsp_a, 'last_buy_sign_hist_dttm', None)
    except Exception:
        db_last = None

    # Normalize and choose max across candidates
    candidates = []
    for cand in (mem_last, db_last):
        if cand is None:
            continue
        try:
            if getattr(cand, 'tzinfo', None) is None:
                cand = cand.replace(tzinfo=timezone.utc)
            candidates.append(cand)
        except Exception:
            pass
    if candidates:
        last_buy_sign = max(candidates)
        try:
            local_tz = tzlocal.get_localzone()
            last_buy_sign_local = last_buy_sign.astimezone(local_tz)
            last_buy_sign_str = last_buy_sign_local.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            last_buy_sign_str = str(last_buy_sign)

    if self.buy.buy_yn == 'Y' and self.buy.test_txn_yn == 'N':
        msg2 = cs(msg2, font_color='white', bg_color='green')
        msg3 = cs(msg3, font_color='white', bg_color='green')
        msg4 = cs(f'{msg4}', font_color='white', bg_color='green')

    elif self.buy.buy_yn == 'Y' and self.buy.test_txn_yn == 'Y':
        msg2 = cs(msg2, font_color='yellow', bg_color='green')
        msg3 = cs(msg3, font_color='yellow', bg_color='green')
        msg4 = cs(f'{msg4}', font_color='yellow', bg_color='green')

    if last_buy_sign == latest_timestamp_local:
        if self.buy.test_txn_yn == 'N':
            msg5 = cs(f'{last_buy_sign_str:>20}', font_color='white', bg_color='green')
        else:
            msg5 = cs(f'{last_buy_sign_str:>20}', font_color='yellow', bg_color='green')
    elif last_buy_sign and (dt.now(timezone.utc).date() - last_buy_sign.date()).days <= 1:
        msg5 = cs(f'{last_buy_sign_str:>20}', font_color='black', bg_color='green')

    elif last_buy_sign and (dt.now(timezone.utc).date() - last_buy_sign.date()).days <= 3:
        msg5 = cs(f'{last_buy_sign_str:>20}', font_color='green')

    elif last_buy_sign and (dt.now(timezone.utc).date() - last_buy_sign.date()).days <= 7:
        msg5 = cs(f'{last_buy_sign_str:>20}', font_color='yellow')

    else:
        msg5 = f'{last_buy_sign_str:>20}'

    msg2 += ' | '
    msg3 += ' | '
    msg4 += ' | '

    msg = msg1 + msg2 + msg3 + msg4 + msg5
    self.chrt.chart_row(msg, len_cnt=260)
    if self.buy.buy_yn == 'Y':
        self.pair.show_buy_header_tf = True

#<=====>#

@narc(1)
def disp_buy_passes(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_passes()')
    """
    Display buy strategy test passes with green formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    if self.buy.buy_yn == 'Y' or self.buy.show_tests_yn in ('Y') or self.st_pair.buy.show_tests_yn == 'Y':
        for x in self.buy.all_passes:
            txt = cs(f'==> BUY {self.buy.buy_strat_name} TEST PASSES : ', font_color='white', bg_color='green')
            txt2 = cs(x, font_color='green')
            msg = self.spacer + f'{txt:<50} {txt2}' 
            self.chrt.chart_row(msg, len_cnt=260)
        self.pair.buy_sell_header_tf = True

#<=====>#

@narc(1)
def disp_buy_fails(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_fails()')
    """
    Display buy strategy test failures with red formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    if self.buy.buy_yn == 'Y' or self.buy.show_tests_yn in ('Y') or self.st_pair.buy.show_tests_yn == 'Y':
        for x in self.buy.all_fails:
            txt = cs(f'==> BUY {self.buy.buy_strat_name} TEST FAILS : ', font_color='white', bg_color='red')
            txt2 = cs(x, font_color='red')
            msg = self.spacer + f'{txt:<50} {txt2}' 
            self.chrt.chart_row(msg, len_cnt=260)
        self.pair.buy_sell_header_tf = True

#<=====>#

@narc(1)
def disp_buy_boosts(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_boosts()')
    """
    Display buy boost information with green formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    if self.st_pair.buy.show_boosts_yn == 'Y':
        for x in self.buy.all_boosts:
            txt = cs('==> BUY BOOSTS : ', font_color='white', bg_color='green')
            txt2 = cs(x, font_color='green')
            msg = self.spacer + f'{txt:<30} {txt2}' 
            self.chrt.chart_row(msg, len_cnt=260)
            self.pair.show_buy_header_tf = True

#<=====>#

@narc(1)
def disp_buy_limits(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_limits()')
    """
    Display buy limit information with red formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    for x in self.buy.all_limits:
        txt = cs('==> BUY LIMITS : ', font_color='white', bg_color='red')
        txt2 = cs(x, font_color='red')
        msg = self.spacer + f'{txt:<30} {txt2}' 
        self.chrt.chart_row(msg, len_cnt=260)
        self.pair.show_buy_header_tf = True

#<=====>#

@narc(1)
def disp_buy_denies(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_denies()')
    """
    Display buy denial information with red formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    for x in self.buy.all_denies:
        txt = cs('==> BUY DENIES : ', font_color='white', bg_color='red')
        txt2 = cs(x, font_color='red')
        msg = self.spacer + f'{txt:<30} {txt2}' 
        self.chrt.chart_row(msg, len_cnt=260)
        self.pair.show_buy_header_tf = True

#<=====>#

@narc(1)
def disp_buy_cancels(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_cancels()')
    """
    Display buy cancellation information with red formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    for x in self.buy.all_cancels:
        txt = cs('==> BUY CANCELS : ', font_color='white', bg_color='red')
        txt2 = cs(x, font_color='red')
        msg = self.spacer + f'{txt:<30} {txt2}' 
        self.chrt.chart_row(msg, len_cnt=260)
        self.pair.show_buy_header_tf = True

#<=====>#

@narc(1)
def disp_buy_maxes(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_maxes()')
    """
    Display buy maximum information with orange formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    for x in self.buy.all_maxes:
        txt = cs('==> BUY MAXES : ', font_color='white', bg_color='orange')
        txt2 = cs(x, font_color='orange')
        msg = self.spacer + f'{txt:<30} {txt2}' 
        self.chrt.chart_row(msg, len_cnt=260)
        self.pair.show_buy_header_tf = True

#<=====>#

@narc(1)
def disp_buy_test_reasons(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_test_reasons()')
    """
    Display buy test mode reasons with orange/red formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    for x in self.buy.all_test_reasons:
        txt = cs('==> BUY TEST MODE REASONS : ', font_color='white', bg_color='orange')
        txt2 = cs(x, font_color='red')
        msg = self.spacer + f'{txt:<30} {txt2}' 
        self.chrt.chart_row(msg, len_cnt=260)
        self.pair.show_buy_header_tf = True

#<=====>#

@narc(1)
def disp_buy_live_or_test(self):
    if self.debug_tf: G(f'==> buy_base.disp_buy_live_or_test()')
    """
    Display live or test mode information with purple formatting.
    Extracted from cls_bot_buy.py - preserves exact formatting.
    """
    if len(self.buy.all_live_or_test) > 2:
        # beep()
        msg = self.spacer + cs(f'test_txn_yn : {self.buy.test_txn_yn}', 'white', 'purple')
        self.chrt.chart_row(in_str=msg, len_cnt=260, bold=True)
        for x in self.buy.all_live_or_test:
            msg = self.spacer + cs(x, 'white', 'purple')
            self.chrt.chart_row(in_str=msg, len_cnt=260, bold=True)
        self.pair.show_buy_header_tf = True

#<=====>#

@narc(1)
def buy_strats_build(self):
    if self.debug_tf: G(f'==> buy_base.buy_strats_build()')
    """Build buy_strats data"""

    buy_strats = self.buy_strats_get()
    buy_strats_list = []

    for k, buy_strat in buy_strats.items():
        buy_strat_list = [buy_strat['buy_strat_type'], buy_strat['buy_strat_name'], buy_strat['buy_strat_freq']]
        buy_strats_list.append(buy_strat_list)

    table_name = 'buy_strats'

    create_sql = self.cbtrade_db.db_buy_strats_exists()
    self.cbtrade_db.execute(create_sql)

    sql_clear = "delete from {} ".format(table_name)
    self.cbtrade_db.execute(sql_clear)

    sql = """
    insert into buy_strats (buy_strat_type, buy_strat_name, buy_strat_freq) VALUES (?, ?, ?)
    """
    self.cbtrade_db.ins_many(sql, buy_strats_list)

#<=====>#

@narc(1)
def buy_new(self):
    if self.debug_tf: G(f'==> buy_base.buy_new()')
    """
    Initialize buy object with default values and copy pair data.
    Extracted from cls_bot_buy.py - preserves exact initialization sequence.
    """

    self.buy                            = AttrDict()
    
    for k, v in self.pair.items():
        self.buy[k] = v
        
#    self.buy.class_name                 = 'BUY'
    self.buy.symb                       = self.mkt.symb
    self.buy.trade_perfs                = self.pair.trade_perfs
    self.buy.trade_strat_perfs          = self.pair.trade_strat_perfs
    self.buy.ta                         = self.pair.ta

    # Prefer previously computed availability flags if set during pair phase
    if hasattr(self, 'buy_strats') and self.buy_strats:
        self.buy.buy_strats = self.buy_strats
        # Also project individual strat_*_yn flags onto buy for strat checks
        try:
            for _k, _v in getattr(self.buy_strats, 'items', lambda: [])():
                if isinstance(_k, str) and _k.startswith('strat_') and _k.endswith('_yn'):
                    setattr(self.buy, _k, _v)
        except Exception:
            pass
    else:
        self.buy.buy_strats = self.buy_strats_get()

    self.buy.reserve_locked_tf          = True
    self.buy.buy_signals                = []
    self.buy.buy_yn                     = '*'
    self.buy.test_txn_yn                = 'N'
    self.buy.all_live_or_test           = []
    self.buy.buy_deny_yn                = 'N'
    self.buy.wait_yn                    = 'Y'
    self.buy.test_reason                = ''
    self.buy.reason                     = ''
    self.buy.note                       = ''
    self.buy.note2                      = ''
    self.buy.note3                      = ''

    self.buy.setting_name               = None
    self.buy.setting_value              = None
    self.buy.buy_stat_name              = None
    self.buy.buy_stat_value             = None
    self.buy.setting_name2              = None
    self.buy.setting_value2             = None
    self.buy.buy_stat_name2             = None
    self.buy.buy_stat_value2            = None
    self.buy.setting_name3              = None
    self.buy.setting_value3             = None
    self.buy.buy_stat_name3             = None
    self.buy.buy_stat_value3            = None
    self.buy.test_fnc_name              = None
    self.buy.test_msg                   = None

    # 🔴 GILFOYLE FIX: Initialize signal_id for forensic tracking
    # Will be auto-created on first buy_decision_add() call
    self.buy.signal_id                  = None

    self.buy.pair_budget_multiplier         = 1.0
    self.buy.pair_strat_budget_multiplier   = 1.0
    self.buy.buy_hist                   = []
    self.first_tf                       = True
    self.disp_buy_header()

#<=====>#

@narc(1)
def buy_signal_create(self) -> None:
    """
    🔴 GILFOYLE FIX: Create the buy signal ONCE at evaluation start.
    
    Creates the compact buy_signals row and stores signal_id for all subsequent decisions.
    This should be called ONCE per buy evaluation cycle, not multiple times.
    
    Returns signal_id for forensic linkage to multiple buy_decisions rows.
    
    Raises:
        Exception: If signal insert fails - NO silent failures for forensic integrity
    """
    # Ensure event timestamp exists
    if not getattr(self.buy, 'event_dttm', None):
        self.buy.event_dttm = dttm_get()
    
    # Insert compact signal row - RETURNS signal_id for forensic linkage
    # 🔴 NO TRY/CATCH - Let errors propagate for full script stop
    signal_id = self.cbtrade_db.db_buy_signals_ins(self.buy)
    
    # Store signal_id in buy object for ALL subsequent decision inserts
    # CRITICAL: Must be named 'signal_id' to match column name in db_buy_decisions_ins
    self.buy.signal_id = signal_id
    
    return signal_id

#<=====>#

@narc(1)
def buy_decision_add(self) -> None:
    """
    🔴 GILFOYLE FIX: Smart decision logging with auto-signal creation.
    
    If self.buy.signal_id is None (first decision for this strat/freq):
        1. Automatically calls buy_signal_create() to create signal
        2. Stores signal_id in self.buy.signal_id
    
    Then inserts decision row to buy_decisions table using self.buy.signal_id.
    Called multiple times during evaluation (test checks, deny checks, etc).
    
    This defensive design makes it impossible to log decisions without a signal.
        
    Raises:
        Exception: If signal creation or decision insert fails
    """
    # 🔴 DEFENSIVE: If signal_id doesn't exist, create signal first
    if not getattr(self.buy, 'signal_id', None):
        self.buy_signal_create()
    
    # Insert decision row ONLY - signal already exists (either created above or earlier)
    # 🔴 NO TRY/CATCH - Let errors propagate for full script stop
    self.cbtrade_db.db_buy_decisions_ins(self.buy)
    
    # Clear decision-specific fields for next decision
    self.buy.setting_name               = None
    self.buy.setting_value              = None
    self.buy.buy_stat_name              = None
    self.buy.buy_stat_value             = None

    self.buy.setting_name2              = None
    self.buy.setting_value2             = None
    self.buy.buy_stat_name2             = None
    self.buy.buy_stat_value2            = None

    self.buy.setting_name3              = None
    self.buy.setting_value3             = None
    self.buy.buy_stat_name3             = None
    self.buy.buy_stat_value3            = None

    self.buy.test_fnc_name              = None
    self.buy.test_msg                   = None

#<=====>#

@narc(1)
def buy_decision_log(self) -> None:
    """
    🔴 DEPRECATED: Legacy function that creates signal + decision together.
    
    ONLY used for final buy/no-buy outcome at end of evaluation.
    For all test/deny checks during evaluation, use buy_decision_add() instead.
    
    This creates both signal AND decision (old behavior for backward compatibility).
    
    Raises:
        Exception: If either insert fails - NO silent failures for forensic integrity
    """
    # Ensure event timestamp exists
    if not getattr(self.buy, 'event_dttm', None):
        self.buy.event_dttm = dttm_get()
    
    # If signal_id already exists, just add decision (don't create duplicate signal)
    if getattr(self.buy, 'signal_id', None):
        self.buy_decision_add()
    else:
        # Legacy path: Create signal + decision together
        signal_id = self.cbtrade_db.db_buy_signals_ins(self.buy)
        self.buy.signal_id = signal_id
        self.cbtrade_db.db_buy_decisions_ins(self.buy)
        
        self.buy.setting_name               = None
        self.buy.setting_value              = None
        self.buy.buy_stat_name              = None
        self.buy.buy_stat_value             = None

        self.buy.setting_name2              = None
        self.buy.setting_value2             = None
        self.buy.buy_stat_name2             = None
        self.buy.buy_stat_value2            = None

        self.buy.setting_name3              = None
        self.buy.setting_value3             = None
        self.buy.buy_stat_name3             = None
        self.buy.buy_stat_value3            = None

        self.buy.test_fnc_name              = None
        self.buy.test_msg                   = None

#<=====>#

# @safe_execute()  # 🔴 GILFOYLE: Important test mode setting function
@narc(1)
def set_test_mode(self):
    if self.debug_tf: G(f'==> buy_base.set_test_mode()')
    """
    Centralized function to set test_txn_yn = 'Y' and immediately update audit table.
    
    Args:
        self: The class instance with buy object
        reason: The reason why switching to test mode
        context: The context/location where the switch occurred
        
    Returns:
        bool: True if successful, False if failed (non-blocking)
    """

    # Set the test mode flag
    self.buy.test_txn_yn = 'Y'
    
    # 🔴 GILFOYLE FIX: Add decision ONLY - don't create new signal
    self.buy_decision_add()

#<=====>#

# @safe_execute()  # 🔴 GILFOYLE: Critical denial mode setting function
@narc(1)
def set_deny_mode(self):
    if self.debug_tf: G(f'==> buy_base.set_deny_mode()')
    """
    Centralized function to set buy_deny_yn = 'Y' and immediately update audit table.
    
    Args:
        self: The class instance with buy object
        reason: The reason why denying the buy
        context: The context/location where the denial occurred
        
    Returns:
        bool: True if successful, False if failed (non-blocking)
    """

    # Set the denial flag
    self.buy.buy_deny_yn = 'Y'
    
    # 🔴 GILFOYLE FIX: Add decision ONLY - don't create new signal
    self.buy_decision_add()

#<=====>#

# @safe_execute_critical(timing_threshold=30.0)  # 🔴 GILFOYLE: CRITICAL buy main logic - exit on failure
@narc(1)
def buy_main(self):
    if self.debug_tf: G(f'==> buy_base.buy_main()')
    """
    Main buy logic orchestration function.
    Extracted from cls_bot_buy.py - preserves exact workflow and integration patterns.
    
    This function:
    1. Handles voice announcements for major currencies
    2. Validates buy conditions (pair availability, technical analysis)
    3. Loops through all strategy performance combinations
    4. Integrates with boost logic, denial logic, and strategy execution
    5. Manages live vs test trading decisions
    6. Handles display and budget updates
    7. Calls buy execution functions
    """

    if self.buy.prod_id in ['BTC-USDC', 'ETH-USDC', 'SOL-USDC']:
        # Obey settings; avoid COM/OOM crashes
        try:
            enabled = getattr(self.st_pair, 'speak_yn', 'N') == 'Y'
        except Exception:
            enabled = False
        speak(f"{self.buy.base_curr_symb} - buy logic", speak_enabled=enabled)

    # Returns
    # skip buy logic if the prod_id not in the buy_pairs (ie it has positions to sell)
    if self.buy.prod_id not in self.mkt.buy_pairs:
        msg = f'{self.buy.prod_id} not in buy_pairs, bypassing buy logic...'
        self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='red', bg_color='white')
        return True  # 🔒 SUCCESS: Valid skip - not in buy pairs (not a lock issue)

    # skip buy logic if ta is not present
    if not self.buy.ta:
        msg = f'{self.buy.prod_id} was not successful collecting ta, bypassing buy logic...'
        self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='red', bg_color='white')
        return True  # 🔒 SUCCESS: Valid skip - no TA available (not a lock issue)

    restricts_open_poss_cnt_max_initial = self.buy.trade_perfs.restricts_open_poss_cnt_max

    self.buy.trade_strat_perfs_organized = AttrDict()
    for trade_strat_perf in self.buy.trade_strat_perfs:
        trade_strat_perf = AttrDict(trade_strat_perf)
        buy_strat_type = trade_strat_perf.buy_strat_type
        buy_strat_name = trade_strat_perf.buy_strat_name
        buy_strat_freq = trade_strat_perf.buy_strat_freq
        otsp_key = f'{buy_strat_type}_{buy_strat_name}_{buy_strat_freq}'
        if otsp_key not in self.buy.trade_strat_perfs_organized:
            self.buy.trade_strat_perfs_organized[otsp_key] = AttrDict()
        self.buy.trade_strat_perfs_organized[otsp_key][trade_strat_perf.lta] = trade_strat_perf

    # loop through all buy tests, ordered by combined daily performance desc
    try:
        strat_order = sorted(
            [AttrDict(x) for x in self.buy.trade_strat_perfs if getattr(x, 'lta', 'A') == 'A'],
            key=lambda r: (
                float(getattr(r, 'gain_loss_pct_day', 0.0) or 0.0),
                float(getattr(r, 'gain_loss_amt', 0.0) or 0.0)
            ),
            reverse=True
        )
        # Interleave A with its corresponding L/T looked up from organized dict during iteration below
    except Exception:
        strat_order = [AttrDict(x) for x in self.buy.trade_strat_perfs]

    for trade_strat_perf in strat_order:
        # format trade_strat_perf
        trade_strat_perf = AttrDict(trade_strat_perf)
        if trade_strat_perf.lta in ('L','T'):
            continue

        tsp_key = f'{trade_strat_perf.buy_strat_type}_{trade_strat_perf.buy_strat_name}_{trade_strat_perf.buy_strat_freq}'
        self.buy.trade_strat_perf            = AttrDict()
        self.buy.trade_strat_perf['A']       = trade_strat_perf
        self.buy.trade_strat_perf['L']       = self.buy.trade_strat_perfs_organized[tsp_key]["L"]
        self.buy.trade_strat_perf['T']       = self.buy.trade_strat_perfs_organized[tsp_key]["T"]

        # set default values
        self.buy.buy_yn                      = 'N'
        self.buy.test_txn_yn                 = 'N'
        self.buy.buy_deny_yn                 = 'N'
        self.buy.wait_yn                     = 'Y'
        self.buy.show_tests_yn               = 'N'

        self.buy.all_passes                  = []
        self.buy.all_fails                   = []
        self.buy.all_boosts                  = []
        self.buy.all_limits                  = []
        self.buy.all_denies                  = []
        self.buy.all_cancels                 = []
        self.buy.all_test_reasons            = []
        self.buy.all_maxes                   = []
        self.buy.all_live_or_test            = []
        self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> buy_yn, test_txn_yn, buy_deny_yn set to N')

        self.buy.buy_strat_type              = trade_strat_perf.buy_strat_type
        self.buy.buy_strat_name              = trade_strat_perf.buy_strat_name
        self.buy.buy_strat_freq              = trade_strat_perf.buy_strat_freq
        buy_strat_name                       = trade_strat_perf.buy_strat_name
        buy_strat_freq                       = trade_strat_perf.buy_strat_freq

        # 🔴 GILFOYLE FIX: Initialize signal_id to None for this strat/freq iteration
        # First call to buy_decision_add() will auto-create signal via defensive check
        self.buy.signal_id                   = None

        self.buy.trade_size                  = self.st_pair.buy.trade_size

        # Elapsed fields are now calculated centrally in trade_strat_perfs_get_all()
        self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt = self.st_pair.strats[buy_strat_name].buy.max_open_poss_cnt_live
        self.buy.trade_strat_perf['T'].restricts_max_open_poss_cnt = self.st_pair.strats[buy_strat_name].buy.max_open_poss_cnt_test

        self.buy.trade_perfs.restricts_open_poss_cnt_max = restricts_open_poss_cnt_max_initial
        self.buy_logic_mkt_boosts()

        # get strat performance boots
        # adjusts trade size & open position max
        self.buy_logic_strat_boosts()

        self.buy.st_pair = self.st_pair
        # perform buy strategy checks
        self.buy, self.pair.ta = self.buy_strats_check(self.buy, self.pair.ta, self.st_pair)

        # these will have been checked before hand unless we forced the tests anyways
        if self.buy.buy_yn == 'Y':
            # 🔴 GILFOYLE: Identify pair type (designated vs undesignated)
            designated_pairs = self.st_mkt.pairs.trade_pairs
            if self.buy.prod_id in designated_pairs:
                self.buy.pair_type = 'designated'
            else:
                self.buy.pair_type = 'undesignated'
            
            print(f"🔍 buy_main: {self.buy.prod_id} is {self.buy.pair_type} pair")
            
            # 🔴 GILFOYLE: Check undesignated budget limits BEFORE budget calculations
            if self.buy.pair_type == 'undesignated':
                # CHECK 1: Has the undesignated group exceeded their collective budget?
                if self.budget.undesignated_current_spend >= self.budget.undesignated_max_spend:
                    msg = f"Undesignated group budget exceeded: ${self.budget.undesignated_current_spend:.2f} >= ${self.budget.undesignated_max_spend:.2f}"
                    self.buy.test_fnc_name = 'undesignated_group_budget_check'
                    self.buy.test_msg = msg
                    self.buy.setting_name = 'undesignated_group_budget'
                    self.buy.setting_value = f"current=${self.budget.undesignated_current_spend:.2f}, max=${self.budget.undesignated_max_spend:.2f}"
                    self.set_deny_mode()
                    self.buy_decision_add()
                    print(f"🚫 DENIED: {msg}")
                    continue  # Skip to next strategy
                
                # CHECK 2: Would this pair exceed the individual undesignated limit?
                current_pair_value = self.pair.open_trade_amt if hasattr(self.pair, 'open_trade_amt') else 0
                
                if current_pair_value >= self.budget.undesignated_individual_max:
                    msg = f"{self.buy.prod_id} individual budget exceeded: ${current_pair_value:.2f} >= ${self.budget.undesignated_individual_max:.2f}"
                    self.buy.test_fnc_name = 'undesignated_individual_budget_check'
                    self.buy.test_msg = msg
                    self.buy.setting_name = 'undesignated_individual_budget'
                    self.buy.setting_value = f"pair_value=${current_pair_value:.2f}, max=${self.budget.undesignated_individual_max:.2f}"
                    self.set_deny_mode()
                    self.buy_decision_add()
                    print(f"🚫 DENIED: {msg}")
                    continue  # Skip to next strategy
                
                print(f"✅ PASS: {self.buy.prod_id} undesignated checks - group: ${self.budget.undesignated_current_spend:.2f}/${self.budget.undesignated_max_spend:.2f}, individual: ${current_pair_value:.2f}/${self.budget.undesignated_individual_max:.2f}")
            
            self.buy_size_budget_calc()

            # bot deny
            if self.buy.buy_deny_yn == 'N':
                self.buy_logic_deny()

            # mkt deny
            if self.buy.buy_deny_yn == 'N':
                self.buy_logic_mkt_deny()

            # strat deny
            if self.buy.buy_deny_yn == 'N':
                self.buy_logic_strat_deny()

            if self.buy.buy_deny_yn == 'N':
                self.buy = self.buy_strats_deny(self.buy)

            # special_prod_ids = self.st_pair.buy.special_prod_ids
            # if self.buy.prod_id in special_prod_ids:
            #     if self.buy.test_txn_yn == 'Y':
            #         print(cs(f'{self.buy.prod_id} in specials, flipping from test to live!!!', 'white', 'green'))
            #         self.buy.test_txn_yn = 'N'

            if self.buy.test_txn_yn == 'Y':
                msg = f'The buy signal on {self.buy.base_curr_symb} for {self.buy.trade_size} {self.buy.quote_curr_symb} with strategy {self.buy.buy_strat_name} on the {self.buy.buy_strat_freq} timeframe has been switched to test mode!'
                self.buy.all_test_reasons.append(msg)

            if self.buy.test_txn_yn == 'N':
                msg = f'The buy signal on {self.buy.base_curr_symb} for {self.buy.trade_size} {self.buy.quote_curr_symb} with strategy {self.buy.buy_strat_name} on the {self.buy.buy_strat_freq} timeframe has been switched to live mode!'
                self.buy.all_test_reasons.append(msg)
                # speak(msg)
                print(msg)
                print(msg)
                print(msg)

        dttm = dttm_get()

        # display
        self.disp_buy()

        if self.buy.buy_yn == 'Y':

            if self.buy.test_txn_yn == 'N':
                self.disp_budget()

            if self.buy.test_txn_yn == 'Y':
                if self.buy.buy_deny_yn == 'N':
                    if self.st_pair.buy_test_txns.test_txns_on_yn == 'Y':
                        self.pair.show_buy_header_tf = True
                        txt = '!!! BUY * TEST * !!!'
                        m = self.spacer + cs('{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f} * STRAT: {}', font_color='white', bg_color='green')
                        msg = m.format(dttm, txt, self.buy.prc_buy, self.buy.trade_size, self.budget.bal_avail, self.buy.buy_strat_name)
                        self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='white', bg_color='green')
                        self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='white', bg_color='green')
                        self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='white', bg_color='green')
                        # 🔒 CRITICAL: Check for lock verification failure
                        if self.buy_test() == False:
                            R(f"🚨 BUY MAIN EXITING: Test lock verification failed for {self.buy.prod_id}")
                            return False  # Bubble up failure to skip entire pair
                        msg = f'test buying {self.buy.base_curr_symb} for {self.buy.trade_size} {self.buy.quote_curr_symb} with strategy {self.buy.buy_strat_name} on the {self.buy.buy_strat_freq} timeframe'
                        self.buy.all_test_reasons.append(msg)

            else:
                if self.buy.buy_deny_yn == 'N':
                    # 🔒 CRITICAL: Check for lock verification failure
                    if self.buy_live() == False:
                        R(f"🚨 BUY MAIN EXITING: Live lock verification failed for {self.buy.prod_id}")
                        return False  # Bubble up failure to skip entire pair
                    self.pair.show_buy_header_tf = True
                    txt = '!!! BUY !!!'
                    m = self.spacer + cs('{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f} * STRAT: {}', font_color='white', bg_color='green')
                    msg = m.format(dttm, txt, self.buy.prc_buy, self.buy.trade_size, self.budget.bal_avail, self.buy.buy_strat_name)
                    self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='white', bg_color='green')
                    self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='white', bg_color='green')
                    self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='white', bg_color='green')
                    msg = f'buying {self.buy.base_curr_symb} for {self.buy.trade_size} {self.buy.quote_curr_symb} with strategy {self.buy.buy_strat_name} on the {self.buy.buy_strat_freq} timeframe'
                    self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='white', bg_color='green')

                    if self.st_pair.speak_yn == 'Y': speak(msg)

                    self.buy.trade_perfs['A'].tot_open_cnt   += 1
                    self.buy.trade_perfs['L'].tot_open_cnt  += 1

                    self.budget.bal_avail                -= self.buy.trade_size
                    self.budget.spendable_amt            -= self.buy.trade_size

                    msg = f'{self.buy.quote_curr_symb} * Balance : ${self.budget.bal_avail:>.2f} * Reserve : ${self.budget.reserve_amt:>.2f} * Spendable : ${self.budget.spendable_amt:>.2f} * '
                    self.chrt.chart_row(in_str=msg, len_cnt=260, font_color='white', bg_color='green')

        elif self.buy.buy_yn == 'N' :
            txt = '!!! WAIT !!!'
            m = self.spacer + cs('{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f}', font_color='white', bg_color='black')
            msg = m.format(dttm, txt, self.buy.prc_buy, self.buy.trade_size, self.budget.bal_avail)

        self.disp_buy_passes()
        self.disp_buy_fails()
        self.disp_buy_boosts()
        self.disp_buy_limits()
        self.disp_buy_denies()
        self.disp_buy_cancels()
        self.disp_buy_maxes()
        self.disp_buy_test_reasons()
        self.disp_buy_live_or_test()

        self.buy_save()

    self.chrt.chart_bottom(len_cnt=260, bold=True)
    print_adv()
    
    return True  # Success - buy main processing completed

#<=====>#

@narc(1)
def cb_buy_base_size_calc(self, buy_prc, spend_amt, base_size_incr, base_size_min, base_size_max):
    if self.debug_tf: G(f'==> buy_base.cb_buy_base_size_calc()')
    """
    Coinbase-specific buy base size calculation with API requirements.
    Extracted from cls_bot_buy.py - preserves exact Coinbase size handling.
    
    Handles:
    - Size increment compliance
    - Minimum size requirements  
    - Maximum size limits
    - Coinbase API size formatting
    """

    trade_size     = dec(spend_amt) / dec(buy_prc)
    print(f'trade_size : {trade_size:>.8f} passed in...')

    if trade_size < dec(base_size_min):
        # Trade size too small - check if we can afford 5x minimum for meaningful position
        minimum_viable_size = dec(base_size_min) * 5
        minimum_viable_cost = minimum_viable_size * dec(buy_prc)
        
        if dec(spend_amt) >= minimum_viable_cost:
            # Can afford meaningful position - round up to nearest viable size
            trade_size = minimum_viable_size
            print(f'...buying less than minimum, but can afford 5x minimum ({minimum_viable_size:>.8f}), setting to viable minimum...')
        else:
            # Can't afford meaningful position - return 0 to trigger test mode
            print(f'...buying less {trade_size:>.8f} than coinbase allows {base_size_min}...insufficient funds for 5x minimum (${minimum_viable_cost:.2f})...returning 0 for test mode...')
            return str(0)

    print(f'trade_size : {trade_size:>.8f} after base_size_min {base_size_min:>.8f} check...')

    sell_blocks = int(dec(trade_size) / dec(base_size_incr))
    trade_size = sell_blocks * dec(base_size_incr)
    print(f'trade_size : {trade_size:>.8f} after sell_block {sell_blocks} increments of {base_size_incr:>.8f}...')

    if trade_size > dec(base_size_max):
        trade_size = dec(base_size_max)
    print(f'trade_size : {trade_size:>.8f} after base_size_max {base_size_max:>.8f} check...')

    return str(trade_size)

#<=====>#

@narc(1)
def buy_size_budget_calc(self):
    if self.debug_tf: G(f'==> buy_base.buy_size_budget_calc()')
    """
    Comprehensive budget-based size calculation with spending controls.
    Extracted from cls_bot_buy.py - preserves exact budget allocation logic.
    
    Handles:
    - Market share allocation (shares vs percentages)
    - Budget multiplier application
    - Up/down strategy budget separation
    - Real-time spending tracking
    - Available funds validation
    - Trade size optimization loop
    - Test mode budget switching
    """

    self.budget.pair_spent_amt            = 0
    self.budget.pair_spent_up_amt         = 0
    self.budget.pair_spent_dn_amt         = 0
    self.budget.pair_spent_pct            = 0
    self.budget.pair_spent_up_pct         = 0
    self.budget.pair_spent_dn_pct         = 0

    self.budget.tot_shares = 0
    if self.st_mkt.budget.mkt_shares.shares_or_pcts == 'shares':
        for x in self.mkt.loop_pairs:
            prod_id = x['prod_id']
            if prod_id in self.st_mkt.budget.mkt_shares:
                self.budget.tot_shares += self.st_mkt.budget.mkt_shares[prod_id] 
            else:
                self.budget.tot_shares += self.st_mkt.budget.mkt_shares['***'] 

        self.budget.pair_spend_max_amt        = self.budget.spend_max_amt * (self.st_pair.budget.mkt_shares / self.budget.tot_shares)
        self.budget.pair_spend_up_max_amt     = self.budget.pair_spend_max_amt * (self.st_pair.budget.spend_up_max_pct / self.budget.tot_shares)
        self.budget.pair_spend_dn_max_amt     = self.budget.pair_spend_max_amt * (self.st_pair.budget.spend_dn_max_pct / self.budget.tot_shares)

    else:

        self.budget.pair_spend_max_amt        = self.budget.spend_max_amt * (self.st_pair.budget.mkt_shares / 100)
        self.budget.pair_spend_up_max_amt     = self.budget.pair_spend_max_amt * (self.st_pair.budget.spend_up_max_pct / 100)
        self.budget.pair_spend_dn_max_amt     = self.budget.pair_spend_max_amt * (self.st_pair.budget.spend_dn_max_pct / 100)

    # Apply Budget Multipliers
    self.budget.pair_spend_max_amt        = self.budget.pair_spend_max_amt * self.buy.pair_budget_multiplier * self.buy.pair_strat_budget_multiplier
    self.budget.pair_spend_up_max_amt     = self.budget.pair_spend_up_max_amt * self.buy.pair_budget_multiplier * self.buy.pair_strat_budget_multiplier   
    self.budget.pair_spend_dn_max_amt     = self.budget.pair_spend_dn_max_amt * self.buy.pair_budget_multiplier * self.buy.pair_strat_budget_multiplier

    # Get Pair Data
    pair_spent_data                = self.cbtrade_db.db_pair_spent(self.buy.prod_id)
    # normalize result to a single row
    if isinstance(pair_spent_data, list):
        pair_spent_data = pair_spent_data[0] if pair_spent_data else {}
    # pair_spent_data                = AttrDictConv(d=pair_spent_data)
    if isinstance(pair_spent_data, dict):
        pair_spent_data = AttrDict(pair_spent_data)

    if pair_spent_data:
        self.budget.pair_open_cnt             = pair_spent_data.open_cnt
        self.budget.pair_open_up_cnt          = pair_spent_data.open_up_cnt
        self.budget.pair_open_dn_cnt          = pair_spent_data.open_dn_cnt
        self.budget.pair_open_dn_pct          = pair_spent_data.open_up_pct
        self.budget.pair_open_dn_pct          = pair_spent_data.open_dn_pct

        self.budget.pair_spent_amt            = pair_spent_data.spent_amt
        self.budget.pair_spent_pct            = round((self.budget.pair_spent_amt / self.budget.pair_spend_max_amt) * 100, 2)
        self.budget.pair_spent_up_amt         = pair_spent_data.spent_up_amt
        self.budget.pair_spent_up_pct         = round((self.budget.pair_spent_up_amt / self.budget.pair_spend_up_max_amt) * 100, 2)
        self.budget.pair_spent_dn_amt         = pair_spent_data.spent_dn_amt
        self.budget.pair_spent_dn_pct         = round((self.budget.pair_spent_dn_amt / self.budget.pair_spend_dn_max_amt) * 100, 2)
    else:
        print('no pair_spent_data found...')
        self.budget.pair_open_cnt             = 0
        self.budget.pair_open_up_cnt          = 0
        self.budget.pair_open_dn_cnt          = 0
        self.budget.pair_open_dn_pct          = 0
        self.budget.pair_open_dn_pct          = 0

        self.budget.pair_spent_amt            = 0
        self.budget.pair_spent_pct            = 0
        self.budget.pair_spent_up_amt         = 0
        self.budget.pair_spent_up_pct         = 0
        self.budget.pair_spent_dn_amt         = 0
        self.budget.pair_spent_dn_pct         = 0

    color_changed_tf = False
    disp_font_color = 'white'
    disp_bg_color   = 'red'

    # adjust the strat trade size based upon spendable amt
    self.buy.target_trade_size = self.buy.trade_size

    self.buy.trade_size = self.buy.quote_size_min

    while self.buy.trade_size <= self.buy.target_trade_size - 1:
        if not color_changed_tf:
            if self.buy.trade_size > self.buy.quote_size_min:
                disp_bg_color   = 'blue'
                color_changed_tf = True

        # General Spending
        if self.budget.spent_amt + self.buy.trade_size + self.buy.quote_size_min > self.budget.spend_max_amt:
            msg = f'mkt.budget.spent_amt : {self.budget.spent_amt:>12.6f} + trade_size  : {self.buy.trade_size:>12.6f} + quote_size_min  : {self.buy.quote_size_min:>12.6f} + > self.budget.spend_max_amt : {self.budget.spend_max_amt:>12.6f}'
            self.buy.all_maxes.append(msg)
            self.buy.all_boosts.append(msg)
            break

        # Pair Spending
        if self.budget.pair_spent_amt + self.buy.trade_size + self.buy.quote_size_min > self.budget.pair_spend_max_amt:
            msg = f'mkt.budget.pair_spent_amt : {self.budget.pair_spent_amt:>12.6f} + trade_size : {self.buy.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget.pair_spend_max_amt : {self.budget.pair_spend_max_amt:>12.6f}'
            self.buy.all_maxes.append(msg)
            self.buy.all_boosts.append(msg)
            break

        # Up Strategies
        if self.buy.trade_strat_perf['L'].buy_strat_type == 'up':
            # General Up Strategy Spending
            if self.budget.spent_up_amt + self.buy.trade_size + self.buy.quote_size_min > self.budget.spend_up_max_amt:
                msg = f'mkt.budget.spent_up_amt : {self.budget.spent_up_amt:>12.6f} + trade_size : {self.buy.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget.spend_up_max_amt : {self.budget.spend_up_max_amt:>12.6f}'
                msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
                self.buy.all_maxes.append(msg)
                self.buy.all_boosts.append(msg)
                break

            # Pair Up Strategy Spending
            if self.budget.pair_spent_up_amt + self.buy.trade_size + self.buy.quote_size_min > self.budget.pair_spend_up_max_amt:
                msg = f'mkt.budget.pair_spent_up_amt : {self.budget.pair_spent_up_amt:>12.6f} + trade_size : {self.buy.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget.pair_spend_up_max_amt : {self.budget.pair_spend_up_max_amt:>12.6f}'
                self.buy.all_maxes.append(msg)
                self.buy.all_boosts.append(msg)
                break

        # Down Strategies
        if self.buy.trade_strat_perf['L'].buy_strat_type == 'dn':
            # General Dn Strategy Spending
            if self.budget.spent_dn_amt + self.buy.trade_size + self.buy.quote_size_min > self.budget.spend_dn_max_amt:
                msg = f'mkt.budget.spent_dn_amt : {self.budget.spent_dn_amt:>12.6f} + trade_size : {self.buy.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget.spend_dn_max_amt : {self.budget.spend_dn_max_amt:>12.6f}'
                self.buy.all_maxes.append(msg)
                self.buy.all_boosts.append(msg)
                break

            # Pair Dn Strategy Spending
            if self.budget.pair_spent_dn_amt + self.buy.trade_size + self.buy.quote_size_min > self.budget.pair_spend_dn_max_amt:
                msg = f'mkt.budget.pair_spent_dn_amt : {self.budget.pair_spent_dn_amt:>12.6f} + trade_size : {self.buy.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget.pair_spend_dn_max_amt : {self.budget.pair_spend_dn_max_amt:>12.6f}'
                self.buy.all_maxes.append(msg)
                break

        # Available Funds
        if self.buy.trade_size + self.buy.quote_size_min > self.budget.spendable_amt:
            msg = f'trade_size : {self.buy.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget.spendable_amt : {self.budget.spendable_amt:>12.6f}'
            self.buy.all_maxes.append(msg)
            self.buy.all_boosts.append(msg)
            break

        self.buy.trade_size += self.buy.quote_size_min

    # Fix Me?
    # deny if trade size exceeds spendable amt
    # Will this prevent the biggest trades on the best strats from being made?
    # Important to revisit this asap
    if self.budget.spendable_amt == 0:
        print(f"self.budget.spendable_amt : {self.budget.spendable_amt}")
        print(f"self.budget.bal_avail : {self.budget.bal_avail}")
        print(f"self.budget.reserve_amt : {self.budget.reserve_amt}")
        print(f"self.budget.spend_max_amt : {self.budget.spend_max_amt}")
        print(f"self.budget.pair_spend_max_amt : {self.budget.pair_spend_max_amt}")
        print(f"self.budget.spend_up_max_amt : {self.budget.spend_up_max_amt}")
        # beep()  # DISABLED - was beeping during budget calculations

    if self.buy.buy_yn == 'Y':
        if self.buy.trade_size == self.buy.quote_size_min:
            affordable_trade_size = min(self.budget.spendable_amt, self.buy.target_trade_size)
            minimum_viable_trade = self.buy.quote_size_min * 5  # Must be at least 2x minimum to be meaningful
            
            msg = f'{self.buy.prod_id} ==> {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} - trade_size : {self.buy.trade_size} == quote_size_min : {self.buy.quote_size_min} ...'
            
            if affordable_trade_size >= minimum_viable_trade:
                # We can afford a meaningful position - execute partial live trade
                self.buy.trade_size = affordable_trade_size
                position_reduction_pct = round((affordable_trade_size / self.buy.target_trade_size) * 100, 1)
                msg = f'{self.buy.quote_curr_symb} => PARTIAL POSITION SIZING => target: ${self.buy.target_trade_size:.2f}, affordable: ${affordable_trade_size:.2f} ({position_reduction_pct}%), executing live partial trade'
                self.buy.all_boosts.append(msg)
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)
                
                if hasattr(self.buy, 'all_denies'):
                    if not self.buy.all_denies:
                        self.buy.all_denies = []
                    self.buy.all_denies.append(f'Position sized down from ${self.buy.target_trade_size:.2f} to ${affordable_trade_size:.2f} due to budget constraints')
                
            elif self.st_pair.buy_test_txns.test_txns_on_yn == 'N':
                # Can't afford meaningful position and test mode disabled - deny the trade
                denial_msg = f'Insufficient funds for meaningful position: available ${affordable_trade_size:.2f} < minimum viable ${minimum_viable_trade:.2f}'
                self.buy.all_denies.append(denial_msg)
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + denial_msg)
                
                # 🔴 Set forensic fields before calling set_deny_mode()
                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.setting_name = 'affordable_trade_size'
                self.buy.setting_value = affordable_trade_size
                self.buy.buy_stat_name = 'minimum_viable_trade'
                self.buy.buy_stat_value = minimum_viable_trade
                self.buy.test_msg = denial_msg
                self.set_deny_mode()
                
            else:
                # Can't afford meaningful position - switch to test mode as last resort
                self.buy.trade_size = self.buy.target_trade_size
                msg = f'{self.buy.quote_curr_symb} => budget funding => balance : {self.budget.bal_avail:>.2f}, reserve amount : {self.budget.reserve_amt:.2f}, spendable amount : {self.budget.spendable_amt:.2f}, insufficient for meaningful position (need ${minimum_viable_trade:.2f}), switching to test...'
                self.buy.all_cancels.append(msg)
                self.buy.test_reason = msg
                # self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)
                
                # 🔴 Set forensic fields before calling set_test_mode()
                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.setting_name = 'minimum_viable_trade'
                self.buy.setting_value = minimum_viable_trade
                self.buy.buy_stat_name = 'affordable_trade_size'
                self.buy.buy_stat_value = affordable_trade_size
                self.buy.test_msg = msg
                self.set_test_mode()

#<=====>#

@narc(1)
def buy_save(self):
    if self.debug_tf: G(f'==> buy_base.buy_save()')
    """
    Save buy order data to files when buy order is confirmed.
    Extracted from cls_bot_buy.py - preserves exact file saving logic.
    """

    # Save Files
    if self.buy.buy_yn == 'Y':
        if self.st_pair.buy.save_files_yn == 'Y':
            fname = f"saves/{self.buy.prod_id}_BUY_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt"
            self.writeit(fname, '=== MKT ===')
            for k in self.buy:
                if isinstance(self.buy[k], ( str, list, dict, float, int, dt, time )):
                    self.writeit(fname, f'{k} : {self.buy[k]}')
                else:
                    print(f'{k} : {type(self.buy[k])}')

#<=====>#

@narc(1)
def buy_live(self):
    if self.debug_tf: G(f'==> buy_base.buy_live()')
    """
    Execute live buy orders with real money.
    Extracted from cls_bot_buy.py - preserves exact live trading logic.
    
    CRITICAL FUNCTION: Handles actual money transactions
    """

    # 🔒 CRITICAL RACE CONDITION PREVENTION: Verify bot owns buy lock
    if not self.verify_bot_lock(self.buy.prod_id, 'buy'):
        R(f"❌ BUY LOCK VERIFICATION FAILED - Another bot owns {self.buy.prod_id} buy lock, ABORTING TRADE!")
        beep(5)
        return False  # Signal failure to bubble up and skip to next pair

    order_uuid = None
    # Ensure Coinbase helper has current buy context
    try:
        self.cb.buy = self.buy
    except Exception:
        pass

    if self.st_pair.buy.buy_limit_yn == 'Y':
        self.cb.ord_lmt_buy_open()
    else:
        order_uuid = self.cb.ord_mkt_buy_orig()

    msg = f'    order_uuid : {order_uuid}'
    self.chrt.chart_row(msg, len_cnt=260)
    
    if order_uuid:  # Only reset if order was actually placed
        self.buy.trade_perfs['L'].last_elapsed = 0
    lta = 'L'

    # Update trade performance cache
    result1 = self.pair_trade_perf_buy_upd(self.buy.prod_id, 'A')
    result2 = self.pair_trade_perf_buy_upd(self.buy.prod_id, lta)

    # Update strategy performance cache  
    result3 = self.pair_trade_strat_perf_buy_upd(self.buy.prod_id, self.buy.buy_strat_type, self.buy.buy_strat_name, self.buy.buy_strat_freq, 'A')
    result4 = self.pair_trade_strat_perf_buy_upd(self.buy.prod_id, self.buy.buy_strat_type, self.buy.buy_strat_name, self.buy.buy_strat_freq, lta)

    self.buy_decision_log()

    return True  # Success - live buy operation completed

#<=====>#

@narc(1)
def buy_test(self):
    if self.debug_tf: G(f'==> buy_base.buy_test()')
    
    # 🔒 CRITICAL RACE CONDITION PREVENTION: Verify bot owns buy lock
    # Even test trades affect statistics and performance metrics
    if not self.verify_bot_lock(self.buy.prod_id, 'buy'):
        R(f"❌ BUY LOCK VERIFICATION FAILED - Another bot owns {self.buy.prod_id} buy lock, ABORTING TEST TRADE!")
        beep(3)
        return False  # Signal failure to bubble up and skip to next pair
    """
    Execute test/paper buy orders for simulation.
    Extracted from cls_bot_buy.py - preserves exact test trading logic.
    """

    tsp_t = self.buy.trade_strat_perf['T']
    msg = self.spacer + f'BUY TEST * {self.buy.prod_id} ==> {tsp_t.buy_strat_name} - {tsp_t.buy_strat_freq} - $ {self.buy.trade_size} '
    msg = cs(msg, font_color='white', bg_color='purple')
    self.chrt.chart_row(in_str=msg, len_cnt=260, bold=True)

    bo = AttrDict()
    bo.test_txn_yn           = 'Y'
    bo.symb                  = self.buy.symb
    bo.prod_id               = self.buy.prod_id
    bo.buy_order_uuid        = self.gen_guid()
    bo.pos_type              = 'SPOT'
    bo.ord_stat              = 'OPEN'
    bo.buy_strat_type        = self.buy.trade_strat_perf['T'].buy_strat_type
    bo.buy_strat_name        = self.buy.trade_strat_perf['T'].buy_strat_name
    bo.buy_strat_freq        = self.buy.trade_strat_perf['T'].buy_strat_freq
    bo.reason                = self.buy.reason
    bo.buy_begin_dttm        = dt.now(timezone.utc) # dt.now()
    bo.buy_end_dttm          = dt.now(timezone.utc) # dt.now()
    bo.buy_begin_unix        = int(dttm_unix())
    bo.buy_end_unix          = int(dttm_unix())

    bo.buy_curr_symb         = self.buy.base_curr_symb
    bo.spend_curr_symb       = self.buy.quote_curr_symb
    bo.fees_curr_symb        = self.buy.quote_curr_symb
    bo.buy_cnt_est           = (self.buy.target_trade_size * 0.996) / self.buy.prc_buy
    bo.buy_cnt_act           = (self.buy.target_trade_size * 0.996) / self.buy.prc_buy
    bo.fees_cnt_act          = (self.buy.target_trade_size * 0.004) / self.buy.prc_buy
    bo.tot_out_cnt           = self.buy.target_trade_size
    bo.prc_buy_est           = self.buy.prc_buy
    bo.prc_buy_act           = self.buy.prc_buy
    bo.tot_prc_buy           = self.buy.prc_buy
    bo.note                  = self.buy.note
    bo.note2                 = self.buy.note2
    bo.prc_buy_slip_pct      = 0

    self.cbtrade_db.db_buy_ords_insupd(bo)
    msg = f'    order_uuid : {bo.buy_order_uuid}'
    self.chrt.chart_row(msg, len_cnt=260)
    
    self.buy.trade_perfs['T'].last_elapsed      = 0
    lta = 'T'

    # Update trade performance cache
    result1 = self.pair_trade_perf_buy_upd(self.buy.prod_id, 'A')
    result2 = self.pair_trade_perf_buy_upd(self.buy.prod_id, lta)

    # Update strategy performance cache
    result3 = self.pair_trade_strat_perf_buy_upd(self.buy.prod_id, self.buy.buy_strat_type, self.buy.buy_strat_name, self.buy.buy_strat_freq, 'A')
    result4 = self.pair_trade_strat_perf_buy_upd(self.buy.prod_id, self.buy.buy_strat_type, self.buy.buy_strat_name, self.buy.buy_strat_freq, lta)
    
    # 🔴 FORENSIC LOGGING: Log test trade decisions
    self.buy_decision_log()
    
    return True  # Success - test buy operation completed

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====> 