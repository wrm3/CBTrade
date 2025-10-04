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

    self.buy.pair_budget_multiplier         = 1.0
    self.buy.pair_strat_budget_multiplier   = 1.0
    self.buy.buy_hist                   = []
    self.first_tf                       = True
    self.disp_buy_header()

#<=====>#

@narc(1)
def buy_decision_log(self) -> None:
    """
    Centralized function to set test_txn_yn = 'Y' and immediately update audit table.
    
    Args:
        self: The class instance with buy object
        reason: The reason why switching to test mode
        context: The context/location where the switch occurred
        
    Returns:
        bool: True if successful, False if failed (non-blocking)
    
    """
    # Compact signal row for quick verification
    try:
        if not getattr(self.buy, 'event_dttm', None):
            self.buy.event_dttm = dttm_get()
    except Exception:
        pass
    try:
        self.cbtrade_db.db_buy_signals_ins(self.buy)
    except Exception:
        pass

    # Full decision audit row
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
    self.buy_decision_log()

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
    self.buy_decision_log()

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
    - Performance thresholds: 0.10%, 0.25%, 0.5%, 1%, 3%, 5%, 8%, 13%, 21%, 34%, 55%, 89%
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
    daily_pct_rates = [0.10, 0.25, 0.5, 1.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0]
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
        msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
        self.buy.all_live_or_test.append(msg)

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
        msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
        self.buy.all_live_or_test.append(msg)

        self.buy.setting_name = 'self.st_pair.sell.force_sell.prod_ids'
        self.buy.setting_value = self.st_pair.sell.force_sell.prod_ids
        self.buy.buy_stat_name = 'prod_id'
        self.buy.buy_stat_value = prod_id
        self.buy.test_fnc_name = sys._getframe().f_code.co_name
        self.buy.test_msg = msg
        self.set_test_mode()
        self.set_deny_mode()

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
        self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

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
    special_prod_ids     = self.st_pair.buy.special_prod_ids

    tot_close_cnt              = self.buy.trade_strat_perf['A'].tot_close_cnt
    gain_loss_close_pct_day    = self.buy.trade_strat_perf['A'].gain_loss_close_pct_day
    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn
    test_txns_min               = self.st_pair.buy_test_txns.test_txns_min
    test_txns_max               = self.st_pair.buy_test_txns.test_txns_max
    
    if self.buy.test_txn_yn == 'N':
        if test_txns_on_yn == 'Y' and tot_close_cnt < test_txns_min:
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {tot_close_cnt} trades  setting test mode ... '
            self.buy.test_reason = msg
            msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
            self.buy.all_live_or_test.append(msg)

            self.buy.setting_name = 'self.st_pair.buy_test_txns.test_txns_min'
            self.buy.setting_value = self.st_pair.buy_test_txns.test_txns_min
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[A].tot_close_cnt'
            self.buy.buy_stat_value = self.buy.trade_strat_perf['A'].tot_close_cnt
            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_test_mode()

        elif test_txns_on_yn == 'Y' and tot_close_cnt <= test_txns_max and gain_loss_close_pct_day < 0.025 and prod_id not in special_prod_ids:
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {tot_close_cnt} trades with performance {gain_loss_close_pct_day:>.8f} % < 0.025 % setting test mode... '
            self.buy.all_test_reasons.append(msg)
            self.buy.test_reason = msg
            self.buy.test_txn_yn = 'Y'
            self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'st_pair.buy_test_txns.test_txns_max'
            self.buy.setting_value = self.st_pair.buy_test_txns.test_txns_max
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[A].tot_close_cnt'
            self.buy.buy_stat_value = self.buy.trade_strat_perf['A'].tot_close_cnt

            self.buy.setting_name2 = 'hardcoded 0.025'
            self.buy.setting_value2 = 0.025
            self.buy.buy_stat_name2 = 'self.buy.trade_strat_perfs[A].gain_loss_close_pct_day'
            self.buy.buy_stat_value2 = self.buy.trade_strat_perf['A'].gain_loss_close_pct_day

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_test_mode()

        elif test_txns_on_yn == 'Y' and tot_close_cnt > test_txns_max and gain_loss_close_pct_day < 0.025 and prod_id not in special_prod_ids:
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {tot_close_cnt} trades with performance {gain_loss_close_pct_day:>.8f} % < 00.025 % reducing allowed open pos, max pos 1 ... '
            self.buy.all_limits.append(msg)
            self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt = 1
            self.buy.trade_strat_perf['T'].restricts_max_open_poss_cnt = 1
            self.buy.test_reason = msg
            self.buy.test_txn_yn = 'Y'
            self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'st_pair.buy_test_txns.test_txns_max'
            self.buy.setting_value = self.st_pair.buy_test_txns.test_txns_max
            self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[A].tot_close_cnt'
            self.buy.buy_stat_value = self.buy.trade_strat_perf['A'].tot_close_cnt

            self.buy.setting_name2 = 'hardcoded 0.025'
            self.buy.setting_value2 = 0.025
            self.buy.buy_stat_name2 = 'self.buy.trade_strat_perfs[A].gain_loss_close_pct_day'
            self.buy.buy_stat_value2 = self.buy.trade_strat_perf['A'].gain_loss_close_pct_day

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_test_mode()

        elif gain_loss_close_pct_day < 0.025 and prod_id not in special_prod_ids:
            msg = f'{prod_id} {buy_strat_name} - {buy_strat_freq} has {tot_close_cnt} closed trades with performance {gain_loss_close_pct_day:>.8f} % < 0.025 % reducing allowed open pos, max pos 1 ... '
            self.buy.all_test_reasons.append(msg)
            self.buy.test_reason = msg
            self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt = 1
            self.buy.trade_strat_perf['T'].restricts_max_open_poss_cnt = 1
            self.buy.test_txn_yn = 'Y'
            self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'hardcoded 0.025'
            self.buy.setting_value = 0.025
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
                msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
                self.buy.all_live_or_test.append(msg)

                self.buy.setting_name = 'self.st_pair.buy.mkts_open_max'
                self.buy.setting_value = self.st_pair.buy.mkts_open_max
                self.buy.buy_stat_name = 'db_mkts_open_cnt_get(mkt=self.mkt.symb)'
                self.buy.buy_stat_value = mkts_open_cnt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
                self.buy.all_live_or_test.append(msg)

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
                self.buy.test_txn_yn = 'Y'
                self.buy.test_reason = msg
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.trade_strat_perfs[L].restricts_max_open_poss_cnt'
                self.buy.setting_value = self.buy.trade_strat_perf['L'].restricts_max_open_poss_cnt
                self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[L].tot_open_cnt'
                self.buy.buy_stat_value = strat_open_live_cnt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                self.buy.buy_deny_yn = 'Y'
                msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
                self.buy.all_live_or_test.append(msg)

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
                self.buy.test_txn_yn = 'Y'
                self.buy.test_reason = f'flipping to test since {msg}'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.trade_perfs.restricts_open_poss_cnt_max'
                self.buy.setting_value = self.buy.trade_perfs.restricts_open_poss_cnt_max
                self.buy.buy_stat_name = 'self.buy.trade_perfs.live_open_poss_cnt'
                self.buy.buy_stat_value = prod_open_poss_cnt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                self.buy.buy_deny_yn = 'Y'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

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
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    if buy_strat_freq == '15min':
        live_strat_delay_minutes = 8
    elif buy_strat_freq == '30min':
        live_strat_delay_minutes = 16
    elif buy_strat_freq == '1h':
        live_strat_delay_minutes = 31
    elif buy_strat_freq == '4h':
        live_strat_delay_minutes = 121
    elif buy_strat_freq == '1d':
        live_strat_delay_minutes = 721
    else:
        live_strat_delay_minutes = 30

    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Elapsed Since Last Product Buy
    live_prod_elapsed = self.buy.trade_perfs['L'].last_elapsed
    if self.buy.test_txn_yn == 'N':
        msg = f'{prod_id} last product buy was {live_prod_elapsed} minutes / {live_strat_delay_minutes} ago minutes...'
        self.buy.all_live_or_test.append(msg)

        strategy_info = f'{buy_strat_name} - {buy_strat_freq} - live : strat_last_elapsed ==> '
        self.buy.all_live_or_test.append(f'{strategy_info:<50} {self.buy.trade_perfs['L'].last_elapsed:>5} / {live_strat_delay_minutes:>4}')

        if live_strat_delay_minutes != 0 and live_prod_elapsed <= live_strat_delay_minutes:
            msg = f'{prod_id} last product buy was {live_prod_elapsed} minutes ago, waiting until {live_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                msg = f'{prod_id} last product buy was {live_prod_elapsed} minutes / {live_strat_delay_minutes} ago minutes...'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'live_strat_delay_minutes'
                self.buy.setting_value = live_strat_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_perfs.last_elapsed'
                self.buy.buy_stat_value = live_prod_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                msg = f'{prod_id} last product buy was {live_prod_elapsed} minutes / {live_strat_delay_minutes} ago minutes...'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'live_strat_delay_minutes'
                self.buy.setting_value = live_strat_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_perfs.last_elapsed'
                self.buy.buy_stat_value = live_prod_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

        self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn}')

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
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    if buy_strat_freq == '15min':
        live_strat_delay_minutes = 8
    elif buy_strat_freq == '30min':
        live_strat_delay_minutes = 16
    elif buy_strat_freq == '1h':
        live_strat_delay_minutes = 31
    elif buy_strat_freq == '4h':
        live_strat_delay_minutes = 121
    elif buy_strat_freq == '1d':
        live_strat_delay_minutes = 721
    else:
        live_strat_delay_minutes = 30

    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Elapsed Since Last Product & Strat & Freq Buy
    live_strat_elapsed = self.buy.trade_strat_perf['L'].strat_last_elapsed
    if self.buy.test_txn_yn == 'N':
        msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {live_strat_elapsed} / {live_strat_delay_minutes} ago minutes...'
        self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)
        self.buy.all_live_or_test.append(f'{buy_strat_name} - {buy_strat_freq} - live : strat_last_elapsed {live_strat_elapsed:>5} / {live_strat_delay_minutes:>5}')

        if live_strat_delay_minutes != 0 and live_strat_elapsed < live_strat_delay_minutes:
            msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {live_strat_elapsed} minutes ago, waiting until {live_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {live_strat_elapsed} minutes ago, waiting until {live_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'live_strat_delay_minutes'
                self.buy.setting_value = live_strat_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_strat_perfs[L].strat_last_elapsed'
                self.buy.buy_stat_value = live_strat_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {live_strat_elapsed} minutes ago, waiting until {live_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

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
        self.buy.all_live_or_test.append(msg)

        if self.budget.pair_spent_amt + self.buy.trade_size > self.budget.pair_spend_max_amt:
            msg = f'{prod_id} has spent {pair_spent_amt} and a purchase of {trade_size} wil exceed > {pair_spend_max_amt} ...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                msg = f'{prod_id} has spent {pair_spent_amt} and a purchase of {trade_size} wil exceed > {pair_spend_max_amt} ...'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.budget.pair_spent_amt + self.buy.trade_size'
                self.buy.setting_value = self.budget.pair_spent_amt + self.buy.trade_size
                self.buy.buy_stat_name = 'self.budget.pair_spent_amt'
                self.buy.buy_stat_value = self.budget.pair_spent_amt

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                msg = f'{prod_id} has spent {pair_spent_amt} and a purchase of {trade_size} wil exceed > {pair_spend_max_amt} ...'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

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
                msg = f'{prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.mkt_limit_only_tf'
                self.buy.setting_value = self.buy.mkt_limit_only_tf
                self.buy.buy_stat_name = 'self.buy.mkt_limit_only_tf'
                self.buy.buy_stat_value = self.buy.mkt_limit_only_tf

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                msg = f'{prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

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
                msg = f'{prod_id} has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... skipping buy'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.prc_range_pct'
                self.buy.setting_value = self.buy.prc_range_pct
                self.buy.buy_stat_name = 'self.buy.prc_range_pct'
                self.buy.buy_stat_value = self.buy.prc_range_pct

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                msg = f'{prod_id} has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... denying buy'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'self.buy.prc_range_pct'
                self.buy.setting_value = self.buy.prc_range_pct
                self.buy.buy_stat_name = 'self.buy.prc_range_pct'
                self.buy.buy_stat_value = self.buy.prc_range_pct

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

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

            self.buy.buy_deny_yn = 'Y'
            msg = f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg
            self.buy.all_live_or_test.append(msg)

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
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    if buy_strat_freq == '15min':
        test_strat_delay_minutes = 8
    elif buy_strat_freq == '30min':
        test_strat_delay_minutes = 16
    elif buy_strat_freq == '1h':
        test_strat_delay_minutes = 31
    elif buy_strat_freq == '4h':
        test_strat_delay_minutes = 121
    elif buy_strat_freq == '1d':
        test_strat_delay_minutes = 721
    else:
        test_strat_delay_minutes = 30

    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Elapsed Since Last Product Buy
    test_prod_elapsed = self.buy.trade_perfs['T'].last_elapsed
    if self.buy.test_txn_yn == 'Y':
        msg = f'{prod_id} last product buy was {test_prod_elapsed} minutes / {test_strat_delay_minutes} ago minutes...'
        self.buy.all_live_or_test.append(msg)

        tsp_t = self.buy.trade_strat_perf['T']
        formatted_label = buy_strat_name + ' - ' + buy_strat_freq + ' - test : strat_last_elapsed ==> '
        self.buy.all_live_or_test.append(f'{formatted_label:<50} {tsp_t.strat_last_elapsed:>5} / {test_strat_delay_minutes:>4}')

        if test_strat_delay_minutes != 0 and test_prod_elapsed < test_strat_delay_minutes:
            msg = f'{prod_id} last product buy was {test_prod_elapsed} minutes ago, waiting until {test_strat_delay_minutes} minutes, denying test trade...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            if test_txns_on_yn == 'Y':
                msg = f'{prod_id} last product buy was {test_prod_elapsed} minutes / {test_strat_delay_minutes} ago minutes...'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'test_strat_delay_minutes'
                self.buy.setting_value = test_strat_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_perfs.last_elapsed'
                self.buy.buy_stat_value = test_prod_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_test_mode()

            else:
                msg = f'{prod_id} last product buy was {test_prod_elapsed} minutes / {test_strat_delay_minutes} ago minutes...'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

                self.buy.setting_name = 'test_strat_delay_minutes'
                self.buy.setting_value = test_strat_delay_minutes
                self.buy.buy_stat_name = 'self.buy.trade_perfs.last_elapsed'
                self.buy.buy_stat_value = test_prod_elapsed

                self.buy.test_fnc_name = sys._getframe().f_code.co_name
                self.buy.test_msg = msg
                self.set_deny_mode()

        self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn}')

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
    buy_strat_type       = self.buy.trade_strat_perf['A'].buy_strat_type
    buy_strat_name       = self.buy.trade_strat_perf['A'].buy_strat_name
    buy_strat_freq       = self.buy.trade_strat_perf['A'].buy_strat_freq

    if buy_strat_freq == '15min':
        test_strat_delay_minutes = 8
    elif buy_strat_freq == '30min':
        test_strat_delay_minutes = 16
    elif buy_strat_freq == '1h':
        test_strat_delay_minutes = 31
    elif buy_strat_freq == '4h':
        test_strat_delay_minutes = 121
    elif buy_strat_freq == '1d':
        test_strat_delay_minutes = 721
    else:
        test_strat_delay_minutes = 30

    test_txns_on_yn             = self.st_pair.buy_test_txns.test_txns_on_yn

    # Elapsed Since Last Product & Strat & Freq Buy
    test_strat_elapsed = self.buy.trade_strat_perf['T'].strat_last_elapsed
    if self.buy.test_txn_yn == 'Y':
        msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {test_strat_elapsed} / {test_strat_delay_minutes} ago minutes...'
        self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)
        self.buy.all_live_or_test.append(f'{buy_strat_name} - {buy_strat_freq} - test : strat_last_elapsed {test_strat_elapsed:>5} / {test_strat_delay_minutes:>5}')

        if test_strat_delay_minutes != 0 and test_strat_elapsed < test_strat_delay_minutes:
            msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {test_strat_elapsed} minutes ago, waiting until {test_strat_delay_minutes} minutes, switching to test_txn_yn = Y...'
            self.buy.all_denies.append(msg)  # Keep for on-screen display
            msg = f'{prod_id} last strat {buy_strat_name} - {buy_strat_freq} buy was {test_strat_elapsed} / {test_strat_delay_minutes} ago minutes...'
            self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

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
            msg = f'{prod_id} has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... skipping buy'
            self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

            self.buy.setting_name = 'self.buy.prc_range_pct'
            self.buy.setting_value = self.buy.prc_range_pct
            self.buy.buy_stat_name = 'self.buy.prc_range_pct'
            self.buy.buy_stat_value = self.buy.prc_range_pct

            self.buy.test_fnc_name = sys._getframe().f_code.co_name
            self.buy.test_msg = msg
            self.set_deny_mode()

#<=====>#
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
        print(f'...selling less {trade_size:>.8f} than coinbase allows {base_size_min}...exiting...')
        beep()
        beep()
        beep()
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

        beep()
    if self.buy.buy_yn == 'Y':
        if self.buy.trade_size == self.buy.quote_size_min:
            affordable_trade_size = min(self.budget.spendable_amt, self.buy.target_trade_size)
            minimum_viable_trade = self.buy.quote_size_min * 2  # Must be at least 2x minimum to be meaningful
            
            msg = f'{self.buy.prod_id} ==> {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} - trade_size : {self.buy.trade_size} == quote_size_min : {self.buy.quote_size_min} ...'
            
            if affordable_trade_size >= minimum_viable_trade:
                # We can afford a meaningful position - execute partial live trade
                self.buy.trade_size = affordable_trade_size
                position_reduction_pct = round((affordable_trade_size / self.buy.target_trade_size) * 100, 1)
                msg = f'{self.buy.quote_curr_symb} => PARTIAL POSITION SIZING => target: ${self.buy.target_trade_size:.2f}, affordable: ${affordable_trade_size:.2f} ({position_reduction_pct}%), executing live partial trade'
                self.buy.all_boosts.append(msg)
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)
                
                if hasattr(self.buy, 'all_denies'):
                    if not self.buy.all_denies:
                        self.buy.all_denies = []
                    self.buy.all_denies.append(f'Position sized down from ${self.buy.target_trade_size:.2f} to ${affordable_trade_size:.2f} due to budget constraints')
                
            elif self.st_pair.buy_test_txns.test_txns_on_yn == 'N':
                # Can't afford meaningful position and test mode disabled - deny the trade
                self.buy.buy_deny_yn = 'Y'
                denial_msg = f'Insufficient funds for meaningful position: available ${affordable_trade_size:.2f} < minimum viable ${minimum_viable_trade:.2f}'
                self.buy.all_denies.append(denial_msg)
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + denial_msg)
                
            else:
                # Can't afford meaningful position - switch to test mode as last resort
                self.buy.trade_size = self.buy.target_trade_size
                msg = f'{self.buy.quote_curr_symb} => budget funding => balance : {self.budget.bal_avail:>.2f}, reserve amount : {self.budget.reserve_amt:.2f}, spendable amount : {self.budget.spendable_amt:.2f}, insufficient for meaningful position (need ${minimum_viable_trade:.2f}), switching to test...'
                self.buy.all_cancels.append(msg)
                self.buy.test_reason = msg
                self.buy.test_txn_yn = 'Y'
                self.buy.all_live_or_test.append(f'buy_yn : {self.buy.buy_yn}, test_txn_yn : {self.buy.test_txn_yn}, buy_deny_yn : {self.buy.buy_deny_yn} ==> ' + msg)

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
    
    return True  # Success - test buy operation completed

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====> 