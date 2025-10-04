"""
SELL FLOW OVERVIEW (entry points and key computations)
======================================================

Primary entrypoints:
- sell_pos_logic(self): orchestrates sell decision pipeline for a single open position.
  * Calls sell_pos_stats_calc(self) to compute/refresh all price/percent/valuation stats.
  * Runs configured sell tests (e.g., ATR stop, trailing ATR, momentum, take-profit/stop-loss).
  * Persists updates at the designated commit points.

Core stats computation:
- sell_pos_stats_calc(self): single place for all canonical fields:
  * Price extremes: prc_high/prc_low tracked from current price (watermarks)
  * P/L amounts: val_curr, val_tot, gain_loss_amt and est variants, with peak/trough watermarks
  * P/L percents: prc_chg_pct from buy→current; prc_chg_pct_high watermark; prc_chg_pct_drop = curr − high
  * Percentage P&L (amount-based) and peak/trough estimates

Representative sell tests (invoked by sell_pos_logic):
- sell_pos_test_atr_stop(self): absolute ATR-based stop
- sell_pos_test_trailing_atr_stop(self): trailing ATR stop
- sell_pos_test_momentum_* (e.g., NWE exit): momentum/color-based exits
Each test updates: sell_yn/hodl_yn, sell_strat_type/name and emits details via disp_sell_pos_test_details().

Persistence:
- Commit points are performed after stats and test decisions are complete to avoid overwriting
  previously persisted peaks with zeros/defaults.

Note: Displays/logs show only actual values (no simulated cosmetics). Calculations are centralized
in sell_pos_stats_calc() to make auditing/modification straightforward.
"""
#<=====>#
# Description
#<=====>#


#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports - Public
#<=====>#
import decimal
import datetime
import json
import time
import os
import sys
import time
import tzlocal
import traceback
import uuid

from datetime import (
    datetime as dt
    , timedelta
    , timezone
)
from decimal import Decimal
from fstrent_colors import *
from pprint import pprint
from typing import Any, Dict, List, Optional, Union

#<=====>#
# Imports - Project
#<=====>#
from libs.common import (
    AttrDict, 
    AttrDictConv, 
    AttrDictEnh, 
    DictKey,
    beep, 
    dec,
    dttm_get,
    dttm_unix,
    calc_chg_pct,
    fatal_error_exit,
    format_disp_age, 
    format_disp_age2,
    get_unix_timestamp,
    narc,
    play_cash, 
    play_thunder,
    print_adv,
    speak
    )
from libs.coinbase_handler import cb
from libs.settings_base import Settings
from libs.strat_base import sell_strats_check
from libs.theme import *

#<=====>#
# Variables
#<=====>#
lib_name      = 'sell_base'
log_name      = 'sell_base'

#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#


@narc(1)
def disp_sell_header(self):
    if self.debug_tf: C(f'==> sell_base.disp_sell_header(pos_id={self.pos.pos_id})')
    """Display sell logic header with position columns"""
    
    hmsg = ""
    hmsg += f"{'pair':^12} | "
    hmsg += f"{'T':^1} | "
    hmsg += f"{'pos_id':^7} | "
    hmsg += f"{'buy_strat':^12} | "
    hmsg += f"{'freq':^5} | "
    hmsg += f"{'age':^10} | "
    hmsg += f"{'buy_val':^16} | "
    hmsg += f"{'curr_val':^16} | "
    hmsg += f"{'buy_prc':^15} | "
    hmsg += f"{'curr_prc':^15} | "
    hmsg += f"{'high_prc':^15} | "
    hmsg += f"{'prc_pct':^8} % | "
    hmsg += f"{'prc_top':^8} % | "
    hmsg += f"{'prc_drop':^8} % | "
    hmsg += f"$ {'net_est':^15} | "
    hmsg += f"$ {'net_est_high':^15}"
    hmsg += f"$ {'last_sell_sign':^20}"

    title_msg = f'* {self.pos.prod_id} * SELL LOGIC *'
    self.chrt.chart_top(in_str=title_msg, len_cnt=260, bold=True)
    self.chrt.chart_headers(in_str=hmsg, len_cnt=260, bold=True)

    self.pair.show_sell_header_tf = False

#<=====>#


@narc(1)
def disp_sell_pos(self):
    if self.debug_tf: C(f'==> sell_base.disp_sell_pos(pos_id={self.pos.pos_id})')
    """Display sell position information"""
    
    if self.pair.show_sell_header_tf:
        self.disp_sell_header()
        self.pair.show_sell_header_tf = False

    disp_age = format_disp_age(self.pos.age_mins)

    last_sell_sign = None
    last_sell_sign_str = ''
    if self.pos.sell_hist:
        last_sell_sign = max(self.pos.sell_hist)
        # If the timestamp is tz-naive, assume it's UTC
        if last_sell_sign.tzinfo is None:
            last_sell_sign = last_sell_sign.tz_localize('UTC')
        # Convert to local time for display only.
        local_tz = tzlocal.get_localzone()
        last_sell_sign_local = last_sell_sign.astimezone(local_tz)
        last_sell_sign_str = last_sell_sign_local.strftime('%Y-%m-%d %H:%M:%S')

    msg = ''
    msg += f'{self.pos.prod_id:<12}' + ' | '
    msg += f'{self.pos.test_txn_yn:^1}' + ' | '
    msg += f'{self.pos.pos_id:^7}' + ' | '
    msg += f'{self.pos.buy_strat_name:^12}' + ' | '
    msg += f'{self.pos.buy_strat_freq:^5}' + ' | '
    msg += f'{disp_age:>10}' + ' | '
    msg += f'{self.pos.tot_out_cnt:>16.8f}' + ' | '
    msg += f'{self.pos.val_curr:>15.8f}' + ' | '
    msg += f'{self.pos.prc_buy:>15.8f}' + ' | '
    msg += f'{self.pos.prc_curr:>15.8f}' + ' | '
    msg += f'{self.pos.prc_high:>15.8f}' + ' | '
    msg += f'{self.pos.prc_chg_pct:>8.2f} %' + ' | '
    msg += f'{self.pos.prc_chg_pct_high:>8.2f} %' + ' | '
    msg += f'{self.pos.prc_chg_pct_drop:>8.2f} %' + ' | '
    msg += f'$ {self.pos.gain_loss_amt:>15.8f}' + ' | '
    msg += f'$ {self.pos.gain_loss_amt_est_high:>15.8f}'
    msg += f'{last_sell_sign_str:>20}'

    msg = cs_pct_color(self.pos.prc_chg_pct, msg)
    self.chrt.chart_row(msg, len_cnt=260)

#<=====>#

# @safe_execute_silent(timing_threshold=5.0)  # 🔴 GILFOYLE: Silent sell force conditions display with color formatting

@narc(1)
def disp_sell_pos_forces(self):
    if self.debug_tf: C(f'==> sell_base.disp_sell_pos_forces(pos_id={self.pos.pos_id})')
    """Display sell force conditions"""
    
    if self.st_pair.sell.show_forces_yn == 'Y':
        for f in self.pos.sell_forces:
            if self.pos.prc_chg_pct > 0:
                msg = ''
                msg += self.spacer 
                msg += cs(f'==> SELL FORCE *', font_color='white', bg_color='green') 
                msg += ' ' 
                msg += cs(f, font_color='green')
                self.chrt.chart_row(msg, len_cnt=260)
            else:
                msg = ''
                msg += self.spacer 
                msg += cs(f'==> SELL FORCE *', font_color='white', bg_color='red') 
                msg += ' ' 
                msg += cs(f, font_color='red')
                self.chrt.chart_row(msg, len_cnt=260)
            self.pair.show_sell_header_tf = True

#<=====>#


@narc(1)
def disp_sell_pos_blocks(self):
    if self.debug_tf: C(f'==> sell_base.disp_sell_pos_blocks(pos_id={self.pos.pos_id})')
    """Display sell block conditions"""
    
    self.st_pair.sell.show_blocks_yn = self.st_pair.sell.show_blocks_yn

    if self.st_pair.sell.show_blocks_yn == 'Y':
        for b in self.pos.sell_blocks:
            if self.pos.prc_chg_pct > 0:
                msg = ''
                msg += self.spacer 
                msg += cs(f'==> SELL BLOCK *', font_color='white', bg_color='green') 
                msg += ' ' 
                msg += cs(b, font_color='green')
                self.chrt.chart_row(msg, len_cnt=260)
            else:
                msg = ''
                msg += self.spacer 
                msg += cs(f'==> SELL BLOCK *', font_color='white', bg_color='red') 
                msg += ' ' 
                msg += cs(b, font_color='red')
                self.chrt.chart_row(msg, len_cnt=260)
            self.pair.show_sell_header_tf = True

#<=====>#


@narc(1)
def disp_sell_pos_sells(self):
    if self.debug_tf: C(f'==> sell_base.disp_sell_pos_sells(pos_id={self.pos.pos_id})')
    """Display sell decision information"""
    
    if self.st_pair.sell.show_forces_yn == 'Y':
        for f in self.pos.sell_forces:
            if self.pos.prc_chg_pct > 0:
                msg = ''
                msg += self.spacer 
                msg += cs(f'==> SELL FORCE *', font_color='white', bg_color='green') 
                msg += ' ' 
                msg += cs(f, font_color='green')
                self.chrt.chart_row(msg, len_cnt=260)
            else:
                msg = ''
                msg += self.spacer 
                msg += cs(f'==> SELL FORCE *', font_color='white', bg_color='red') 
                msg += ' ' 
                msg += cs(f, font_color='red')
                self.chrt.chart_row(msg, len_cnt=260)
            self.pair.show_sell_header_tf = True

#<=====>#


@narc(1)
def disp_sell_pos_hodls(self):
    if self.debug_tf: C(f'==> sell_base.disp_sell_pos_hodls(pos_id={self.pos.pos_id})')
    """Display sell test/hold conditions"""
    
    if self.st_pair.sell.show_tests_yn == 'Y':
        for t in self.pos.sell_tests:
            if self.pos.prc_chg_pct > 0:
                msg = ''
                msg += self.spacer 
                msg += cs(f'==> SELL TEST *', font_color='white', bg_color='green') 
                msg += ' ' 
                msg += cs(t, font_color='green')
                self.chrt.chart_row(msg, len_cnt=260)
            else:
                msg = ''
                msg += self.spacer 
                msg += cs(f'==> SELL TEST *', font_color='white', bg_color='red') 
                msg += ' ' 
                msg += cs(t, font_color='red')
                self.chrt.chart_row(msg, len_cnt=260)
            self.pair.show_sell_header_tf = True

#<=====>#

@narc(1)
def disp_sell_pos_test_details(self, msg, all_sells, all_hodls):
    if self.debug_tf: C(f'==> sell_base.disp_sell_pos_test_details(msg={msg}, all_sells={all_sells}, all_hodls={all_hodls})')
    """Display detailed sell test results"""
    if (self.pos.sell_yn == 'Y' and self.pos.sell_block_yn == 'N') or self.st_pair.sell.show_tests_yn in ('Y','F'):
        for e in all_sells:
            if self.pos.prc_chg_pct > 0:
                e = self.spacer + cs('* ' + e, font_color='green')
                self.chrt.chart_row(e, len_cnt=260)
            else:
                e = self.spacer + cs('* ' + e, font_color='red')
                self.chrt.chart_row(e, len_cnt=260)
            self.show_sell_header_tf = True
        for e in all_hodls:
            e = self.spacer + cs('* ' + e, font_color='green', bg_color='white')
            self.chrt.chart_row(e, len_cnt=260)
            self.show_sell_header_tf = True

#<=====>#

@narc(1)
def sell_logic(self):
    if self.debug_tf: C(f'==> sell_base.sell_logic(prod_id={self.pair.prod_id})')

    prod_id = self.pair.prod_id
    self.pair.show_sell_header_tf = True
  
    self.pair.bal_cnt = cb.cb_bal_get(self.pair.base_curr_symb)

    for pos_data in self.pair.open_poss:
#            print_adv(2)
        pos_data = pos_data
        pos_data = AttrDict(pos_data)
        pos_id   = pos_data.pos_id
        
        pos_data['prc_curr'] = self.pair.prc_sell  # Use current live price

        if pos_data.pos_stat == 'OPEN':

            # Ensure canonical percent fields exist on loaded pos before first persist
            if 'prc_chg_pct' not in pos_data or pos_data.prc_chg_pct is None:
                pos_data.prc_chg_pct = 0
            if 'prc_chg_pct_high' not in pos_data or pos_data.prc_chg_pct_high is None:
                pos_data.prc_chg_pct_high = 0
            if 'prc_chg_pct_drop' not in pos_data or pos_data.prc_chg_pct_drop is None:
                pos_data.prc_chg_pct_drop = 0
            if self.debug_tf:
                for fld in ("prc_chg_pct", "prc_chg_pct_high", "prc_chg_pct_drop"):
                    val = pos_data.get(fld, None)
                    if val is None or not isinstance(val, (int, float)):
                        traceback.print_stack()
                        sys.exit(f"FATAL: Missing/invalid {fld} on pre-persist pos_data for {pos_id} ({self.pair.prod_id}); got {val}")

            # Do not persist pre-compute; avoid overwriting prior peaks with defaults
                
            self.sell_pos_new(pos_data)
            
            if self.debug_tf: C(f"==> sell_base.sell_logic - calling from sell_pos_logic()")
            
            # 🔒 CRITICAL: Check for lock verification failure
            if self.sell_pos_logic() == False:
                R(f"🚨 SELL LOGIC EXITING: Lock verification failed for {self.pair.prod_id}")
                return False  # Bubble up failure to skip entire pair
            
            if self.debug_tf: C(f"==> sell_base.sell_logic - returned from sell_pos_logic()")
            
            if self.pair.skip_to_next_tf:
                if self.debug_tf: C(f"==> sell_base.sell_logic - skipping to next tf")
                break
                
            if self.debug_tf: C(f"==> sell_base.sell_logic - calling from db_poss_insupd()")
            
            # Final guard prior to persist of updated pos
            if self.debug_tf:
                for fld in ("prc_chg_pct", "prc_chg_pct_high", "prc_chg_pct_drop"):
                    val = getattr(self.pos, fld, None)
                    if val is None or not isinstance(val, (int, float)):
                        traceback.print_stack()
                        sys.exit(f"FATAL: Missing/invalid {fld} before final persist for pos {self.pos.pos_id} ({self.pos.prod_id}); got {val}")

            self.cbtrade_db.db_poss_insupd(self.pos)

    self.chrt.chart_bottom(len_cnt=260, bold=True)
    print_adv()
    
    return True  # Success - sell logic completed

#<=====>#


@narc(1)
def sell_pos_new(self, pos_data):
    if self.debug_tf: C(f'==> sell_base.sell_pos_new(pos_id={pos_data.pos_id}, len(pos_data)={len(pos_data)})')
    self.pos                                = AttrDict()
#    self.pos.class_name                     = 'POS'
    for k, v in pos_data.items():
        self.pos[k] = v
    self.pos.age_mins = self.pos.new_age_mins
    self.pos.symb                           = self.mkt.symb
    self.pair.ta                            = self.pair.ta
    self.pos.prc_sell                       = self.pair.prc_sell
    self.pos.sell_yn                        = 'N'
    self.pos.hodl_yn                        = 'N'
    self.pos.sell_block_yn                  = 'N'
    self.pos.sell_force_yn                  = 'N'
    self.pos.sell_blocks                    = []
    self.pos.sell_forces                    = []
    self.pos.sell_tests                     = []
    self.pos.sell_test_sells                = []
    self.pos.sell_test_hodls                = []
#        self.pos.sell_signals                   = []
    self.pos.sell_strat_type                = ''
    self.pos.sell_strat_name                = ''
    self.pos.sell_strat_freq                = ''
    self.pos.reason                         = ''
    self.pos.sell_hist                      = []

    # Preserve existing canonical metrics from DB; do not reset to 0 here
    # Missing fields will be computed or defaulted later as needed

#<=====>#

@narc(1)
def sell_pos_stats_calc(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_stats_calc(pos_id={getattr(self.pos, "pos_id", "?")})')

    all_sells   = []
    all_hodls   = []

    # Current notional value from live price
    self.pos.val_curr = round(float(self.pos.hold_cnt) * float(self.pos.prc_curr), 8)

    # Total current value (tot_in_cnt is accumulated proceeds from sells; add current holdings value)
    self.pos.val_tot  = round(float(self.pos.tot_in_cnt) + self.pos.val_curr, 8)

    # Dollar P&L vs total cost
    self.pos.gain_loss_amt     = round(self.pos.val_tot - float(self.pos.tot_out_cnt), 8)
    self.pos.gain_loss_amt_est = self.pos.gain_loss_amt

    # Percent change from buy to current
    self.pos.prc_chg_pct = calc_chg_pct(self.pos.prc_buy, self.pos.prc_curr, dec_prec=2)

    # Peak percent change from buy (track high watermark)
    if self.pos.prc_chg_pct > self.pos.prc_chg_pct_high:
        self.pos.prc_chg_pct_high = self.pos.prc_chg_pct
    
    # Percentage-point drop from peak P/L (curr% − high%)
    self.pos.prc_chg_pct_drop = round(self.pos.prc_chg_pct - self.pos.prc_chg_pct_high, 2)

    # Record price extremes - high
    if self.pos.prc_curr > self.pos.prc_high:
        self.pos.prc_high = self.pos.prc_curr

    # Record price extremes - low
    if self.pos.prc_curr < self.pos.prc_low:
        self.pos.prc_low = self.pos.prc_curr

    # Track peak/trough of estimated P&L
    if self.pos.gain_loss_amt_est > self.pos.gain_loss_amt_est_high:
        self.pos.gain_loss_amt_est_high = self.pos.gain_loss_amt_est

    # Track peak/trough of estimated P&L - low
    if self.pos.gain_loss_amt_est < self.pos.gain_loss_amt_est_low:
        self.pos.gain_loss_amt_est_low = self.pos.gain_loss_amt_est

    # Percentage P&L vs total cost
    self.pos.gain_loss_pct     = calc_chg_pct(self.pos.tot_out_cnt, self.pos.val_tot, dec_prec=4)
    self.pos.gain_loss_pct_est = self.pos.gain_loss_pct

    # Track peak/trough of estimated percentage P&L
    # if self.pos.gain_loss_pct > self.pos.gain_loss_pct_high:
    #     self.pos.gain_loss_pct_high = self.pos.gain_loss_pct
    if self.pos.gain_loss_pct_est > self.pos.gain_loss_pct_est_high:
        self.pos.gain_loss_pct_est_high = self.pos.gain_loss_pct_est

    # Track peak/trough of estimated percentage P&L - low
    # if self.pos.gain_loss_pct < self.pos.gain_loss_pct_low:
    #     self.pos.gain_loss_pct_low = self.pos.gain_loss_pct
    if self.pos.gain_loss_pct_est < self.pos.gain_loss_pct_est_low:
        self.pos.gain_loss_pct_est_low = self.pos.gain_loss_pct_est

    self.pos.prc_chg_pct_drop = round(self.pos.prc_chg_pct - self.pos.prc_chg_pct_high, 2)

    msg = ''
    msg += self.spacer 
    msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - NWE Exit', font_color='white', bg_color='blue')
    # self.chrt.chart_row(msg)
    self.disp_sell_pos_test_details(msg, all_sells, all_hodls)
    self.cbtrade_db.db_poss_insupd(self.pos)

#<=====>#

@narc(1)
def sell_pos_logic(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_logic(pos_id={self.pos.pos_id})')
   
    t0 = time.perf_counter()

    self.pair.skip_to_next_tf = False

    # self.pos.bal_cnt = cb.cb_bal_get(self.pair.base_curr_symb)
    # if self.pos.bal_cnt == 0:
    #     self.pos.bal_cnt = cb.cb_bal_get(self.pos.symb)

    self.pos.bal_cnt = self.pair.bal_cnt

    # print(f'sell_pos_logic() ==> self.pos.bal_cnt = {self.pos.bal_cnt}')

    # if self.pos.bal_cnt == 0:
    #     print(f' => {self.pos.prod_id} balance is {self.pos.bal_cnt}...')
    #     beep(3)
    #     # 🚨 DEBUGGING MODE: Hard exit with clear error details
    #     traceback.print_stack()
    #     sys.exit(f"POSITION BALANCE ERROR: {self.pos.prod_id} balance is {self.pos.bal_cnt} - cannot process sell for position {self.pos.pos_id}")

    # Centralized stats calculation
    self.sell_pos_stats_calc()

    # Debug-time guard before persisting: ensure canonical percent fields exist and are numeric
    if self.debug_tf:
        for fld in ("prc_chg_pct", "prc_chg_pct_high", "prc_chg_pct_drop"):
            val = getattr(self.pos, fld, None)
            if val is None or not isinstance(val, (int, float)):
                traceback.print_stack()
                sys.exit(f"FATAL: Missing/invalid {fld} before persist in sell_pos_logic for pos {self.pos.pos_id} ({self.pos.prod_id}); got {val}")

    self.disp_sell_pos()
    self.cbtrade_db.db_poss_check_last_dttm_upd(self.pos.pos_id)
    check_last_data = self.cbtrade_db.db_poss_check_last_dttm_get(self.pos.pos_id)
    # Extract only the datetime value from the tuple
    if isinstance(check_last_data, tuple) and len(check_last_data) >= 1:
        self.pos.check_last_dttm = check_last_data[0]
        self.pos.check_last_unix = check_last_data[1] if len(check_last_data) > 1 else None
    else:
        self.pos.check_last_dttm = check_last_data

    # Halt And Catch Fire
    sos = self.cbtrade_db.db_sell_ords_get(pos_id=self.pos.pos_id)
    if sos:
        print(f' => Halt & Catch Fire... Receovering...')
        if DictKey(sos, 'ta'): del self.pos['ta']
        if DictKey(sos, 'pair'): del self.pos['pair']
        if DictKey(sos, 'st'): del self.pos['st']
        print(f'existing sell order for pos : {self.pos.pos_id}')
        for so in sos:
            print(so)
            print('')
        traceback.print_stack()
        beep(3)

        self.pos.pos_stat = 'SELL'
        self.cbtrade_db.db_poss_insupd(self.pos)
        self.pos.sell_yn = 'N'
        return

        # # 🚨 DEBUGGING MODE: Hard exit with clear error details  
        # sys.exit(f"EXISTING SELL ORDER CONFLICT: Position {self.pos.pos_id} already has sell order(s) - requires manual investigation")
        # print('this seems to only be happening with the test orders...')
        # self.pair.skip_to_next_tf = True
        # print('attempting to skip to next pair...')

    # Forced Sell Logic
    if self.pos.sell_yn == 'N':
        self.sell_pos_forces()

    # Logic that will block the sell from happening
    if self.pos.sell_force_yn == 'N':
        self.sell_pos_blocks()

    # Sells Tests that don't require TA
    if self.pos.sell_yn == 'N':
        self.sell_pos_tests_before_ta()

    if self.pos.sell_yn == 'N':
        if not self.pair.ta:
            t0 = time.perf_counter()
            try:
#                    self.pair.ta = ta_main_new(self.pair, self.st_mkt)
                if not self.pair.ta:
                    WoR(f'{dttm_get()}  - Get TA ==> TA Errored and is None')
                    WoR(f'{dttm_get()}  - Get TA ==> TA Errored and is None')
                    WoR(f'{dttm_get()}  - Get TA ==> TA Errored and is None')

                elif self.pair.ta == 'Error!':
                    WoR(f'{dttm_get()}  - Get TA ==> {self.pos.prod_id} - close prices do not match')
                    WoR(f'{dttm_get()}  - Get TA ==> {self.pos.prod_id} - close prices do not match')
                    WoR(f'{dttm_get()}  - Get TA ==> {self.pos.prod_id} - close prices do not match')
                    self.pair.ta = None

            except Exception as e:
                print(f'{dttm_get()}  - Get TA ==> {self.pos.prod_id} = Error : ({type(e)}){e}')
                traceback.print_exc()
                beep(3)
                sys.exit(f"GET TA ERROR: {self.pos.prod_id} - terminating to preserve hard-crash diagnostics")
            t1 = time.perf_counter()
            secs = round(t1 - t0, 2)
            timing_data = {'Technical Analysis in Sell POS Logic': secs}
            self.pair.timings.append(timing_data)
            if secs >= 5:
                msg = cs(f'mkt_ta_main_new for {self.pos.prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
                self.chrt.chart_row(msg, len_cnt=260)
                self.chrt.chart_mid(len_cnt=260)

        ta_high = self.pos.prc_high
        if self.pair.ta and self.pos.age_mins >= 1440:
            ta_high = self.pair.ta['1d'].df['high'].iloc[-1]
        elif self.pair.ta and self.pos.age_mins >= 240:
            ta_high = self.pair.ta['4h'].df['high'].iloc[-1]
        elif self.pair.ta and self.pos.age_mins >= 60:
            ta_high = self.pair.ta['1h'].df['high'].iloc[-1]
        elif self.pair.ta and self.pos.age_mins >= 15:
            ta_high = self.pair.ta['15min'].df['high'].iloc[-1]
        elif self.pair.ta and self.pos.age_mins >= 5:
            ta_high = self.pair.ta['5min'].df['high'].iloc[-1]
        if ta_high > self.pos.prc_high:
            self.pos.prc_high = ta_high

    if self.pos.sell_yn == 'N' and self.pair.ta:
        if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> calling sell_pos_tests_after_ta(pos_id={self.pos.pos_id})')
        self.sell_pos_tests_after_ta()
        if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> returned from sell_pos_tests_after_ta(pos_id={self.pos.pos_id})')

    # Sell By Strat Logic - These do require TA
    if self.pos.sell_yn == 'N' and self.pair.ta:
        if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> calling sell_strats_check(pos_id={self.pos.pos_id})')
        self.pair, self.pos, self.pair.ta = self.sell_strats_check(self.pair, self.pos, self.pair.ta, self.st_pair)
        if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> returned from sell_strats_check(pos_id={self.pos.pos_id})')


    if self.debug_tf:
        # 🚨 ISOLATE THE EXACT EXIT POINT - Line by Line Debug
        print(f"🚨 DEBUG CHECKPOINT A: About to check debug_tf value")
        print(f"🚨 DEBUG CHECKPOINT B: debug_tf = {self.debug_tf}")
        print(f"🚨 DEBUG CHECKPOINT C: About to access self.pos.sell_yn")
        print(f"🚨 DEBUG CHECKPOINT D: self.pos.sell_yn = {self.pos.sell_yn}")
        print(f"🚨 DEBUG CHECKPOINT E: About to access self.pos.sell_force_yn")
        print(f"🚨 DEBUG CHECKPOINT F: self.pos.sell_force_yn = {self.pos.sell_force_yn}")
        print(f"🚨 DEBUG CHECKPOINT G: About to access self.pos.sell_block_yn")
        print(f"🚨 DEBUG CHECKPOINT H: self.pos.sell_block_yn = {self.pos.sell_block_yn}")
        print(f"🚨 DEBUG CHECKPOINT I: About to access self.pair.ta")
        print(f"🚨 DEBUG CHECKPOINT J: self.pair.ta = {type(self.pair.ta)}")
        print(f"🚨 DEBUG CHECKPOINT K: About to execute original debug line")
    
    if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> self.pos.sell_yn={self.pos.sell_yn}, self.pos.sell_force_yn={self.pos.sell_force_yn}, self.pos.sell_block_yn={self.pos.sell_block_yn}, self.pair.ta={type(self.pair.ta)}')
    if self.debug_tf: print(f"🚨 DEBUG CHECKPOINT L: Successfully completed debug line")
    if self.debug_tf: C(f"==> sell_base.sell_pos_logic - Made It Here 556")

    # This is a blocker that will only be checked for TA sells
    if self.pos.sell_yn == 'Y':
        if self.pos.sell_force_yn == 'N':
            if self.pos.sell_block_yn == 'N':
                if self.pair.ta:
                    if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> calling sell_pos_deny_nwe_green(pos_id={self.pos.pos_id})')
                    self.sell_pos_deny_nwe_green()
                    if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> calling sell_pos_deny_all_green(pos_id={self.pos.pos_id})')
                    self.sell_pos_deny_all_green()

    if self.debug_tf: C(f"==> sell_base.sell_pos_logic - Made It Here 574")

    # Finalize YesNos
    if self.pos.sell_force_yn == 'Y':
        self.pos.sell_yn = 'Y'
        self.pos.hodl_yn = 'N'
    elif self.pos.sell_block_yn == 'Y':
        self.pos.sell_yn = 'N'
        self.pos.hodl_yn = 'Y'
    elif self.pos.sell_yn == 'Y':
        self.pos.hodl_yn = 'N'
    else:
        self.pos.sell_yn = 'N'
        self.pos.hodl_yn = 'Y'

    if self.debug_tf: C(f"==> sell_base.sell_pos_logic - Made It Here 589")

    if self.pos.sell_yn == 'Y' and self.pos.sell_block_yn == 'N':
        if self.pos.test_txn_yn == 'N':
            if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> calling sell_pos_live(pos_id={self.pos.pos_id})')
            # 🔒 CRITICAL: Check for lock verification failure
            if self.sell_pos_live() == False:
                R(f"🚨 SELL POS LOGIC EXITING: Live lock verification failed for {self.pos.prod_id}")
                return False  # Bubble up failure to skip entire pair
            if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> returned from sell_pos_live(pos_id={self.pos.pos_id})')
            if self.pos.error_tf:
                play_thunder()
                self.pos.sell_yn = 'N'
                if self.st_pair.speak_yn == 'Y': speak(self.pos.reason)
            else:
                if self.pos.gain_loss_amt > 0:
                    msg = f'WIN, selling {self.pos.base_curr_symb} for {round(self.pos.gain_loss_amt_est,2)} dollars '
                    if self.st_pair.speak_yn == 'Y': speak(msg)
                    if self.pos.gain_loss_amt >= 1:
                        if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> calling play_cash(pos_id={self.pos.pos_id})')
                        play_cash()
                        if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> returned from play_cash(pos_id={self.pos.pos_id})')
                elif self.pos.gain_loss_amt < 0:
                    msg = f'LOSS, selling {self.pos.base_curr_symb} for {round(self.pos.gain_loss_amt_est,2)} dollars '
                    if self.st_pair.speak_yn == 'Y': speak(msg)
                    if self.pos.gain_loss_amt <= -1:
                        if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> calling play_thunder(pos_id={self.pos.pos_id})')
                        play_thunder()
                        if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> returned from play_thunder(pos_id={self.pos.pos_id})')

        elif self.pos.test_txn_yn == 'Y':
            if self.debug_tf: C(f'==> sell_base.sell_pos_logic() ==> calling sell_pos_test(pos_id={self.pos.pos_id})')
            # 🔒 CRITICAL: Check for lock verification failure
            if self.sell_pos_test() == False:
                R(f"🚨 SELL POS LOGIC EXITING: Test lock verification failed for {self.pos.prod_id}")
                return False  # Bubble up failure to skip entire pair

    self.cbtrade_db.db_poss_upd(self.pos) 

    if self.debug_tf: C(f"==> sell_base.sell_pos_logic - Made It Here 623")

    t1 = time.perf_counter()
    secs = round(t1 - t0, 3)
    timing_data = {f'sell_logic.sell_pos_logic({self.pos.pos_id})': secs}
    if self.debug_tf: C(f"==> sell_base.sell_pos_logic Made It Here 628 - timing_data={timing_data}")
    # self.pair.timings.append(timing_data)

    if self.debug_tf: C(f'==> leaving sell_base.sell_pos_logic() ==> Made It Here 634 END Leaving')
    
    return True  # Success - position sell logic completed

#<=====>#


@narc(1)
def sell_pos_blocks(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_blocks(pos_id={self.pos.pos_id})')
    # sell_block_selling_off
    if self.st_pair.sell.selling_on_yn == 'N':
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => selling_on_yn : {self.st_pair.sell.selling_on_yn}'
        self.pos.sell_blocks.append(msg)

    # sell_block_never_sell_loss_live_all(self):
    if self.pos.sell_block_yn == 'N' and self.pos.test_txn_yn == 'N' and self.st_pair.sell.never_sell_loss.live_all_yn == 'Y' and self.pos.prc_chg_pct < 0:
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => never_sell_loss.live_all_yn : {self.st_pair.sell.never_sell_loss.live_all_yn}'
        cs(msg, font_color='gold', bg_color='orangered')
        self.pos.sell_blocks.append(msg)

    # sell_block_never_sell_loss_all(self):
    if self.pos.sell_block_yn == 'N' and self.st_pair.sell.never_sell_loss.all_yn == 'Y' and self.pos.prc_chg_pct < 0:
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => never_sell_loss.all_yn : {self.st_pair.sell.never_sell_loss.all_yn}'
        self.pos.sell_blocks.append(msg)

    # sell_block_never_sell_loss_live_prod_id(self):
    if self.pos.sell_block_yn == 'N' and self.pos.test_txn_yn == 'N' and self.pos.prod_id in self.st_pair.sell.never_sell_loss.live_prod_ids and self.pos.prc_chg_pct < 0:
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => never_sell_loss.live_prod_ids : {self.pos.prod_id}'
        self.pos.sell_blocks.append(msg)

    # sell_block_never_sell_loss_prod_id(self):
    if self.pos.sell_block_yn == 'N' and self.pos.prod_id in self.st_pair.sell.never_sell_loss.prod_ids and self.pos.prc_chg_pct < 0:
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => never_sell_loss.prod_ids : {self.pos.prod_id}'
        self.pos.sell_blocks.append(msg)

    # sell_block_never_sell_loss_pos_id(self):
    if self.pos.sell_block_yn == 'N' and self.pos.pos_id in self.st_pair.sell.never_sell_loss.pos_ids and self.pos.prc_chg_pct < 0:
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => never_sell_loss.pos_ids : {self.pos.pos_id}'
        self.pos.sell_blocks.append(msg)

    if self.st_pair.sell.never_sell_loss.live_max_loss_usd_acceptable != 0:
        if self.pos.sell_block_yn == 'N' and self.pos.test_txn_yn == 'N' and self.pos.prc_chg_pct < 0 and self.pos.gain_loss_amt < abs(self.st_pair.sell.never_sell_loss.live_max_loss_usd_acceptable) * -1:
            # beep()
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => never_sell_loss.live_max_loss_usd_acceptable : {abs(self.st_pair.sell.never_sell_loss.live_max_loss_usd_acceptable) * -1}, loss : ${self.pos.gain_loss_amt:>.4f}'
            self.pos.sell_blocks.append(msg)

    # sell_block_never_sell_all(self):
    if self.pos.sell_block_yn == 'N' and self.st_pair.sell.never_sell.all_yn == 'Y':
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => never_sell.all_yn : {self.st_pair.sell.never_sell.all_yn}'
        self.pos.sell_blocks.append(msg)

    # sell_block_never_sell_prod_id(self):
    if self.pos.sell_block_yn == 'N' and self.pos.prod_id in self.st_pair.sell.never_sell.prod_ids:
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => never_sell.prod_ids : {self.pos.prod_id}'
        self.pos.sell_blocks.append(msg)

    # sell_block_never_sell_pos_id(self):
    if self.pos.sell_block_yn == 'N' and self.pos.pos_id in self.st_pair.sell.never_sell.pos_ids:
        self.pos.sell_block_yn = 'Y'
        msg = f'settings => never_sell.pos_ids : {self.pos.pos_id}'
        self.pos.sell_blocks.append(msg)
    # sell_block_price_range_extreme(self):
    # Market Price Range Looks Very Suspect
    if self.pos.sell_block_yn == 'N' and self.pair.prc_range_pct >= 5:
        self.pos.sell_block_yn = 'Y'
        msg = f'price range variance of {self.pair.prc_range_pct}, bid : {self.pair.prc_bid}, ask : {self.pair.prc_ask}, this price range looks sus... skipping sell'
        self.pos.sell_blocks.append(msg)

    self.disp_sell_pos_blocks()

#<=====>#


@narc(1)
def sell_pos_forces(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_forces(pos_id={self.pos.pos_id})')
    # sell_force_force_sell_db(self):
    if self.pos.force_sell_tf == 1:
        self.pos.sell_yn = 'Y'
        self.pos.sell_force_yn = 'Y'
        self.pos.hodl_yn = 'N'
        self.pos.sell_strat_type = 'force'
        self.pos.sell_strat_name  = 'forced sell'
        msg = f'db => position marked as force sell... poss.force_sell_tf : {self.pos.force_sell_tf}'
        self.pos.sell_forces.append(msg)
#            speak(msg)

    # sell_force_force_sell_all(self):
    if self.st_pair.sell.force_sell.all_yn == 'Y':
        self.pos.sell_yn = 'Y'
        self.pos.sell_force_yn = 'Y'
        self.pos.hodl_yn = 'N'
        self.pos.sell_strat_type = 'force'
        self.pos.sell_strat_name  = 'forced sell'
        msg = f'settings => force_sell.all_yn = {self.st_pair.sell.force_sell.all_yn}'
        self.pos.sell_forces.append(msg)

    # sell_force_force_sell_live_all(self):
    if self.st_pair.sell.force_sell.live_all_yn == 'Y' and self.pos.test_txn_yn == 'N':
        self.pos.sell_yn = 'Y'
        self.pos.sell_force_yn = 'Y'
        self.pos.hodl_yn = 'N'
        self.pos.sell_strat_type = 'force'
        self.pos.sell_strat_name  = 'forced sell L'
        msg = f'settings => force_sell.live_all_yn = {self.st_pair.sell.force_sell.live_all_yn}'
        self.pos.sell_forces.append(msg)

    # sell_force_force_sell_prod_id(self):
    if self.pos.prod_id in self.st_pair.sell.force_sell.prod_ids:
        self.pos.sell_yn = 'Y'
        self.pos.sell_force_yn = 'Y'
        self.pos.hodl_yn = 'N'
        self.pos.sell_strat_type = 'force'
        self.pos.sell_strat_name  = 'forced sell'
        msg = f'settings => force_sell.prod_ids = {self.pos.prod_id}'
        self.pos.sell_forces.append(msg)

    # sell_force_force_sell_id(self):
    if self.pos.pos_id in self.st_pair.sell.force_sell.pos_ids:
        self.pos.sell_yn = 'Y'
        self.pos.sell_force_yn = 'Y'
        self.pos.hodl_yn = 'N'
        self.pos.sell_strat_type = 'force'
        self.pos.sell_strat_name  = 'forced sell'
        msg = f'settings => force_sell.pos_ids = {self.pos.pos_id}'
        self.pos.sell_forces.append(msg)

    self.disp_sell_pos_forces()

#<=====>#


@narc(1)
def sell_pos_tests_before_ta(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_tests_before_ta(pos_id={self.pos.pos_id})')
    # Take Profits
    if self.pos.prc_chg_pct > 0:
        if self.pos.sell_yn == 'N':
            if self.st_pair.sell.take_profit.hard_take_profit_yn == 'Y':
                self.sell_pos_test_hard_profit()

        if self.pos.sell_yn == 'N':
            if self.st_pair.sell.take_profit.trailing_profit_yn == 'Y':
                self.sell_pos_test_trailing_profit()

    # Stop Loss
    if self.pos.prc_chg_pct < 0:
        if self.pos.sell_yn == 'N':
            if self.st_pair.sell.stop_loss.hard_stop_loss_yn == 'Y':
                self.sell_pos_test_hard_stop()

        if self.pos.sell_yn == 'N':
            if self.st_pair.sell.stop_loss.trailing_stop_loss_yn == 'Y':
                self.sell_pos_test_trailing_stop()

        if self.pos.sell_yn == 'N':
            if self.st_pair.sell.stop_loss.atr_stop_loss_yn == 'Y':
                self.sell_pos_test_atr_stop()

        if self.pos.sell_yn == 'N':
            if self.st_pair.sell.stop_loss.trailing_atr_stop_loss_yn == 'Y':
                self.sell_pos_test_trailing_atr_stop()

    if self.debug_tf: C(f'==> sell_base.sell_pos_tests_after_ta(pos_id={self.pos.pos_id})... leaving... ')


#<=====>#


@narc(1)
def sell_pos_tests_after_ta(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_tests_after_ta(pos_id={self.pos.pos_id})')
    if self.pos.sell_yn == 'N':
        if self.st_pair.sell.stop_loss.nwe_exit_yn == 'Y':
            self.sell_pos_test_nwe_exit()

#<=====>#


@narc(1)
def sell_pos_test_hard_profit(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_test_hard_profit(pos_id={self.pos.pos_id})')
    if self.pos.buy_strat_name not in self.st_pair.sell.take_profit.hard_profit_strats_skip:
        all_sells   = []
        all_hodls   = []

        if self.pos.prc_chg_pct >= self.st_pair.sell.take_profit.hard_profit_pct:
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'profit'
            self.pos.sell_strat_name = 'hard_profit'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...hard profit => curr : {self.pos.prc_chg_pct:>.2f}%, target : {self.st_pair.sell.take_profit.hard_profit_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
            all_sells.append(msg)
        else:
            msg = f'HODL COND: ...hard profit => curr : {self.pos.prc_chg_pct:>.2f}%, target : {self.st_pair.sell.take_profit.hard_profit_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
            all_hodls.append(msg)

        msg = ''
        msg += self.spacer 
        msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Hard Profit', font_color='white', bg_color='green')
        # self.chrt.chart_row(msg)
        self.disp_sell_pos_test_details(msg, all_sells, all_hodls)

#<=====>#


@narc(1)
def sell_pos_test_hard_stop(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_test_hard_stop(pos_id={self.pos.pos_id})')
    if self.pos.buy_strat_name not in self.st_pair.sell.stop_loss.hard_stop_loss_strats_skip:
        all_sells   = []
        all_hodls   = []

        # Diagnostic: show exact predicate inputs
        try:
            cfg_pct = abs(self.st_pair.sell.stop_loss.hard_stop_loss_pct)
        except Exception:
            cfg_pct = 0
        threshold_pct = cfg_pct * -1
        if self.debug_tf:
            C(f"HARD_STOP_DIAG pos_id={self.pos.pos_id} prod={self.pos.prod_id} strat={self.pos.buy_strat_name} freq={self.pos.buy_strat_freq} prc_chg_pct={self.pos.prc_chg_pct} threshold={threshold_pct} hard_stop_loss_yn={self.st_pair.sell.stop_loss.hard_stop_loss_yn} skip_list={self.st_pair.sell.stop_loss.hard_stop_loss_strats_skip} sell_block_yn={self.pos.sell_block_yn}")

        if self.pos.prc_chg_pct <= threshold_pct:
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'stop_loss'
            self.pos.sell_strat_name = 'hard_stop_loss'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...hard stop loss => curr : {self.pos.prc_chg_pct:>.2f}%, trigger : {self.st_pair.sell.stop_loss.hard_stop_loss_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
            all_sells.append(msg)
        else:
            # Do not clear fields if a different test has already set sell_yn='Y'
            if self.pos.sell_yn != 'Y':
                self.pos.sell_strat_type = ''
                self.pos.sell_strat_name = ''
                self.pos.sell_strat_freq = ''
            msg = f'HODL COND: ...hard stop loss => curr : {self.pos.prc_chg_pct:>.2f}%, trigger : {self.st_pair.sell.stop_loss.hard_stop_loss_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
            all_hodls.append(msg)

        msg = ''
        msg += self.spacer 
        msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Hard Stop Loss', font_color='white', bg_color='red')
        # self.chrt.chart_row(msg)
        self.disp_sell_pos_test_details(msg, all_sells, all_hodls)

#<=====>#


@narc(1)
def sell_pos_test_trailing_profit(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_test_trailing_profit(pos_id={self.pos.pos_id})')

    if self.pos.buy_strat_name not in self.st_pair.sell.take_profit.trailing_profit_strats_skip:
        all_sells   = []
        all_hodls   = []

        # Trailing Profit Logic
        if self.pos.prc_chg_pct > 0.5:
            max_drop_pct = -5
            if self.pos.prc_chg_pct_high >= self.st_pair.sell.take_profit.trailing_profit_trigger_pct:
                levels = self.st_pair.sell.take_profit.trailing_profit_levels
                for k in sorted(levels, reverse=True):
                    if self.pos.prc_chg_pct_high >= float(k):
                        max_drop_pct = -1 * levels[k]
                        # print(f"k : {k}, levels[k] : {levels[k]}, self.pos.prc_chg_pct_high : {self.pos.prc_chg_pct_high}, max_drop_pct : {max_drop_pct}")
                        break
                max_drop_pct = round(max_drop_pct, 2)

                # cp(f'max_drop_pct : {max_drop_pct}', 'green')
                if self.pos.prc_chg_pct_drop <= max_drop_pct:
                    self.pos.sell_yn = 'Y'
                    self.pos.hodl_yn = 'N'
                    self.pos.sell_strat_type = 'profit'
                    self.pos.sell_strat_name = 'trail_profit'
                    msg = ''
                    msg += self.spacer 
                    try:
                        price_drop_from_high = calc_chg_pct(self.pos.prc_high, self.pos.prc_curr, dec_prec=2)
                    except Exception:
                        price_drop_from_high = self.pos.prc_chg_pct_drop
                    msg += f'==> SELL COND: ...trailing profit => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {price_drop_from_high:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                    all_sells.append(msg)
                else:
                    try:
                        price_drop_from_high = calc_chg_pct(self.pos.prc_high, self.pos.prc_curr, dec_prec=2)
                    except Exception:
                        price_drop_from_high = self.pos.prc_chg_pct_drop
                    msg = f'HODL COND: ...trailing profit => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {price_drop_from_high:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                    all_hodls.append(msg)

                # print(msg)

                self.disp_sell_pos_test_details(msg, all_sells, all_hodls)

#<=====>#


@narc(1)
def sell_pos_test_trailing_stop(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_test_trailing_stop(pos_id={self.pos.pos_id})')
    if self.pos.buy_strat_name not in self.st_pair.sell.stop_loss.trailing_stop_loss_strats_skip:
        all_sells   = []
        all_hodls   = []

        stop_loss_pct = round(self.pos.prc_chg_pct_high - abs(self.st_pair.sell.stop_loss.trailing_stop_loss_pct), 2)
        if self.pos.prc_chg_pct < stop_loss_pct:
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'stop_loss'
            self.pos.sell_strat_name = 'trail_stop'
            msg = f'SELL COND: ...trailing stop loss => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, trigger : {self.st_pair.sell.stop_loss.trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
            all_sells.append(msg)
        else:
            self.pos.sell_strat_type = ''
            self.pos.sell_strat_name = ''
            self.pos.sell_strat_freq = ''
            msg = f'HODL COND: ...trailing stop loss => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, trigger : {self.st_pair.sell.stop_loss.trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
            all_hodls.append(msg)

        msg = ''
        msg += self.spacer 
        msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Trailing Stop Loss', font_color='white', bg_color='red')
        # self.chrt.chart_row(msg)
        self.disp_sell_pos_test_details(msg, all_sells, all_hodls)

#<=====>#

@narc(1)
def sell_pos_test_nwe_exit(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_test_nwe_exit(pos_id={self.pos.pos_id})')
    if self.pos.buy_strat_name not in self.st_pair.sell.stop_loss.nwe_exit_strats_skip:

        all_sells  = []
        all_hodls   = []

        freq = self.pos.buy_strat_freq

        if self.pair.ta and freq in self.pair.ta:
            nwe_color = self.pair.ta[freq]['nwe_color']['ago0']
            nwe_color_last = self.pair.ta[freq]['nwe_color']['ago1']

            nwe_color_5min = self.pair.ta['5min']['nwe_color']['ago0']
            nwe_color_15min = self.pair.ta['15min']['nwe_color']['ago0']
            nwe_color_30min = self.pair.ta['30min']['nwe_color']['ago0']
            nwe_color_1h = self.pair.ta['1h']['nwe_color']['ago0']
            nwe_color_4h = self.pair.ta['4h']['nwe_color']['ago0']

            nwe_color_5min_last = self.pair.ta['5min']['nwe_color']['ago1']
        else:
            # No TA data available - skip this test
            return
        
        if freq == '1d' and nwe_color == 'red' and nwe_color_last == 'red' and nwe_color_4h == 'red' and nwe_color_5min_last == 'red':
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'momentum'
            self.pos.sell_strat_name = 'nwe_exit'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...NWE Exit => nwe_color : {nwe_color}, nwe_color_last : {nwe_color_last}' + ', '
            msg = WoR(msg, print_tf=False)
            all_sells.append(msg)
        elif freq == '4h' and nwe_color == 'red' and nwe_color_last == 'red' and nwe_color_1h == 'red' and nwe_color_5min_last == 'red':
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'momentum'
            self.pos.sell_strat_name = 'nwe_exit'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...NWE Exit => nwe_color : {nwe_color}, nwe_color_last : {nwe_color_last}' + ', '
            msg = WoR(msg, print_tf=False)
            all_sells.append(msg)
        elif freq == '1h' and nwe_color == 'red' and nwe_color_last == 'red' and nwe_color_30min == 'red' and nwe_color_5min_last == 'red':
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'momentum'
            self.pos.sell_strat_name = 'nwe_exit'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...NWE Exit => nwe_color : {nwe_color}, nwe_color_last : {nwe_color_last}' + ', '
            msg = WoR(msg, print_tf=False)
            all_sells.append(msg)
        elif freq == '30min' and nwe_color == 'red' and nwe_color_last == 'red' and nwe_color_15min == 'red' and nwe_color_5min_last == 'red':
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'momentum'
            self.pos.sell_strat_name = 'nwe_exit'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...NWE Exit => nwe_color : {nwe_color}, nwe_color_last : {nwe_color_last}' + ', '
            msg = WoR(msg, print_tf=False)
            all_sells.append(msg)
        elif freq == '15min' and nwe_color == 'red' and nwe_color_last == 'red' and nwe_color_5min_last == 'red':
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'momentum'
            self.pos.sell_strat_name = 'nwe_exit'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...NWE Exit => nwe_color : {nwe_color}, nwe_color_last : {nwe_color_last}' + ', '
            msg = WoR(msg, print_tf=False)
            all_sells.append(msg)

#<=====>#


@narc(1)
def sell_pos_test_atr_stop(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_test_atr_stop(pos_id={self.pos.pos_id})')
    if self.pos.buy_strat_name not in self.st_pair.sell.stop_loss.atr_stop_loss_strats_skip:
        all_sells   = []
        all_hodls   = []

        freq = self.pos.buy_strat_freq

        if self.pair.ta and freq in self.pair.ta:
            atr_stop_long = self.pair.ta[freq]['atr_stop_long']['ago0']
            atr_stop_long_last = self.pair.ta[freq]['atr_stop_long']['ago1']
        else:
            # No TA data available - skip this test
            return

        if self.pos.prc_curr <= atr_stop_long:
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'stop_loss'
            self.pos.sell_strat_name = 'atr_stop'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...ATR Stop => prc_curr : {self.pos.prc_curr:>.2f}, atr_stop_long : {atr_stop_long:>.2f}' + ', '
            msg = WoR(msg, print_tf=False)
            all_sells.append(msg)
        else:
            msg = ''
            msg += self.spacer 
            msg += f'==> HODL COND: ...ATR Stop => prc_curr : {self.pos.prc_curr:>.2f}, atr_stop_long : {atr_stop_long:>.2f}' + ', '
            msg = WoG(msg, print_tf=False)
            all_hodls.append(msg)

        msg = ''
        msg += self.spacer 
        msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - ATR Stop', font_color='white', bg_color='magenta')
        # self.chrt.chart_row(msg)
        self.disp_sell_pos_test_details(msg, all_sells, all_hodls)

#<=====>#


@narc(1)
def sell_pos_test_trailing_atr_stop(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_test_trailing_atr_stop(pos_id={self.pos.pos_id})')
    if self.pos.buy_strat_name not in self.st_pair.sell.stop_loss.trailing_atr_stop_loss_strats_skip:
        all_sells   = []
        all_hodls   = []

        freq = self.pos.buy_strat_freq

        if self.pair.ta and freq in self.pair.ta:
            atr_stop_long = self.pair.ta[freq]['atr_stop_long']['ago0']
            atr_stop_long_last = self.pair.ta[freq]['atr_stop_long']['ago1']
        else:
            # No TA data available - skip this test
            return

        if self.pos.prc_curr <= atr_stop_long:
            self.pos.sell_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'stop_loss'
            self.pos.sell_strat_name = 'trail_atr_stop'
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL COND: ...trailing ATR Stop => prc_curr : {self.pos.prc_curr:>.2f}, atr_stop_long : {atr_stop_long:>.2f}' + ', '
            msg = WoR(msg, print_tf=False)
            all_sells.append(msg)
        else:
            msg = ''
            msg += self.spacer 
            msg += f'==> HODL COND: ...trailing ATR Stop => prc_curr : {self.pos.prc_curr:>.2f}, atr_stop_long : {atr_stop_long:>.2f}' + ', '
            msg = WoG(msg, print_tf=False)
            all_hodls.append(msg)

        msg = ''
        msg += self.spacer 
        msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Trailing ATR Stop', font_color='white', bg_color='cyan')
        # self.chrt.chart_row(msg)
        self.disp_sell_pos_test_details(msg, all_sells, all_hodls)

#<=====>#


@narc(1)
def sell_pos_deny_all_green(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_deny_all_green(pos_id={self.pos.pos_id})')
    '''
    "profit_saver": {
        "ha_green": {
            "use_yn": "Y",
            "prod_ids": [],
            "skip_prod_ids": [],
            "sell_strats": [],
            "skip_sell_strats": ["trail_profit"]
        },
        "nwe_green": {
            "use_yn": "Y",
            "prod_ids": [],
            "skip_prod_ids": [],
            "sell_strats": [],
            "skip_sell_strats": ["trail_profit"]
        }
    },
    '''

    if self.st_pair.sell.profit_saver.ha_green.use_yn == 'N':
        return

    if self.pos.prod_id in self.st_pair.sell.profit_saver.ha_green.prod_ids:
        return
    if self.pos.sell_strat_name in self.st_pair.sell.profit_saver.ha_green.skip_sell_strats:
        return

    if self.st_pair.sell.profit_saver.ha_green.prod_ids and self.pos.prod_id not in self.st_pair.sell.profit_saver.ha_green.prod_ids:
        return
    if self.st_pair.sell.profit_saver.ha_green.sell_strats and self.pos.sell_strat_name not in self.st_pair.sell.profit_saver.ha_green.sell_strats:
        return

    all_sells                 = []
    all_hodls                 = []
    rfreq                     = self.pos.buy_strat_freq

    if self.pair.ta:
        ha_color_5min = self.pair.ta['5min']['ha_color']['ago0']
        ha_color_15min = self.pair.ta['15min']['ha_color']['ago0']
        ha_color_30min = self.pair.ta['30min']['ha_color']['ago0']
        ha_color_1h = self.pair.ta['1h']['ha_color']['ago0']
        ha_color_4h = self.pair.ta['4h']['ha_color']['ago0']
        ha_color_1d = self.pair.ta['1d']['ha_color']['ago0']
    else:
        # No TA data available - skip this test
        return

    skip_checks = False
    if self.st_pair.sell.force_sell.all_yn == 'Y':
        skip_checks = True

    if self.pos.prod_id in self.st_pair.sell.force_sell.prod_ids:
        skip_checks = True

    if self.pos.pos_id in self.st_pair.sell.force_sell.pos_ids:
        skip_checks = True


    pass_msg = ''
    fail_msg = ''
    if not skip_checks:
        green_save = False

        if rfreq == '1d':
            fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
            if ha_color_1h == 'green' and ha_color_30min == 'green' and ha_color_15min == 'green' and ha_color_5min == 'green':
                pass_msg = ''
                pass_msg += self.spacer 
                pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                green_save = True
        elif rfreq == '4h':
            fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
            if ha_color_30min == 'green' and ha_color_15min == 'green' and ha_color_5min == 'green':
                pass_msg = ''
                pass_msg += self.spacer 
                pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                green_save = True
        elif rfreq == '1h':
            fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
            if ha_color_15min == 'green' and ha_color_5min == 'green':
                pass_msg = ''
                pass_msg += self.spacer 
                pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                green_save = True
        elif rfreq == '30min':
            fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {self.pos.sell_block_yn}'
            if ha_color_15min == 'green' and ha_color_5min == 'green':
                pass_msg = ''
                pass_msg += self.spacer 
                pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {self.pos.sell_block_yn}'
                green_save = True
        elif rfreq == '15min':
            fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
            if ha_color_5min == 'green':
                pass_msg = ''
                pass_msg += self.spacer 
                pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                green_save = True

        if green_save:
            self.pos.sell_block_yn = 'Y'
            all_hodls.append(pass_msg)
            self.pos.sell_blocks.append(pass_msg)
        else:
            fail_msg = ''
            fail_msg += self.spacer 
            fail_msg += f'==> CANCEL SELL: ALL CANDLES NOT GREEN ==> Allowing Sell...   5min : {ha_color_5min}, 15min : {ha_color_15min}, 30min : {ha_color_30min}, sell_block_yn : {self.pos.sell_block_yn}'
            all_sells.append(fail_msg)
            # speak(fail_msg)

    if self.pos.sell_block_yn == 'Y' or self.st_pair.sell.show_tests_yn in ('Y','F'):
        msg = ''
        msg += self.spacer 
        msg += f'==> SELL TESTS - {self.pos.prod_id} - All Green Candes...'
        # speak(msg)
        WoG(msg)
        if self.pos.sell_block_yn == 'Y' or self.st_pair.sell.show_tests_yn in ('Y'):
            for e in all_sells:
                if self.pos.prc_chg_pct > 0:
                    G(e)
                else:
                    R(e)
                self.show_sell_header_tf = True
            for e in all_hodls:
                WoG(e)
                self.show_sell_header_tf = True

#<=====>#


@narc(1)
def sell_pos_deny_nwe_green(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_deny_nwe_green(pos_id={self.pos.pos_id})')
    '''
    "profit_saver": {
        "ha_green": {
            "use_yn": "Y",
            "prod_ids": [],
            "skip_prod_ids": [],
            "sell_strats": [],
            "skip_sell_strats": ["trail_profit"]
        },
        "nwe_green": {
            "use_yn": "Y",
            "prod_ids": [],
            "skip_prod_ids": [],
            "sell_strats": [],
            "skip_sell_strats": ["trail_profit"]
        }
    },
    '''

    if self.st_pair.sell.profit_saver.nwe_green.use_yn == 'N':
        return

    if self.pos.prod_id in self.st_pair.sell.profit_saver.nwe_green.prod_ids:
        return
    if self.pos.sell_strat_name in self.st_pair.sell.profit_saver.nwe_green.skip_sell_strats:
        return

    if self.st_pair.sell.profit_saver.nwe_green.prod_ids and self.pos.prod_id not in self.st_pair.sell.profit_saver.nwe_green.prod_ids:
        return
    if self.st_pair.sell.profit_saver.nwe_green.sell_strats and self.pos.sell_strat_name not in self.st_pair.sell.profit_saver.nwe_green.sell_strats:
        return

    all_sells                 = []
    all_hodls                 = []
    rfreq                     = self.pos.buy_strat_freq

    if self.pair.ta:
        nwe_color_5min = self.pair.ta['5min']['nwe_color']['ago0']
        nwe_color_15min = self.pair.ta['15min']['nwe_color']['ago0']
        nwe_color_30min = self.pair.ta['30min']['nwe_color']['ago0']
        nwe_color_1h = self.pair.ta['1h']['nwe_color']['ago0']
        nwe_color_4h = self.pair.ta['4h']['nwe_color']['ago0']
        nwe_color_1d = self.pair.ta['1d']['nwe_color']['ago0']
    else:
        # No TA data available - skip this test
        return

    skip_checks = False
    if self.st_pair.sell.force_sell.all_yn == 'Y':
        skip_checks = True

    if self.pos.prod_id in self.st_pair.sell.force_sell.prod_ids:
        skip_checks = True

    if self.pos.pos_id in self.st_pair.sell.force_sell.pos_ids:
        skip_checks = True

    if not skip_checks:
        green_save = False

        pass_msg = ''
        pass_msg += self.spacer 
        pass_msg += f'==> SELL DENY * HODL * NWEs GREEN ==> OVERIDING SELL!!! '
        pass_msg += f', 5min : {nwe_color_5min} '
        pass_msg += f', 15min : {nwe_color_15min} '
        pass_msg += f', 30min : {nwe_color_30min} '
        pass_msg += f', 1h : {nwe_color_1h} '
        pass_msg += f'  4h : {nwe_color_4h} '
        pass_msg += f'  1d : {nwe_color_1d} '
        pass_msg += f', sell_block_yn : {self.pos.sell_block_yn}'

        fail_msg = ''
        fail_msg += self.spacer 
        fail_msg += f'==> SELL DENY * SELL * NWEs NOT GREEN ==> Allowing Sell...    '
        fail_msg += f', 5min : {nwe_color_5min} '
        fail_msg += f', 15min : {nwe_color_15min} '
        fail_msg += f', 30min : {nwe_color_30min} '
        fail_msg += f', 1h : {nwe_color_1h} '
        fail_msg += f'  4h : {nwe_color_4h} '
        fail_msg += f'  1d : {nwe_color_1d} '
        fail_msg += f', sell_block_yn : {self.pos.sell_block_yn}'

        if rfreq == '1d':
            msg = fail_msg
#                if nwe_color_1h == 'green' and (nwe_color_30min == 'green' or nwe_color_15min == 'green') and nwe_color_5min == 'green':
            if nwe_color_15min == 'green' and nwe_color_5min == 'green':
                msg = pass_msg
                green_save = True
        elif rfreq == '4h':
            msg = fail_msg
#                if nwe_color_30min == 'green' and nwe_color_15min == 'green' and nwe_color_5min == 'green':
            if nwe_color_15min == 'green' and nwe_color_5min == 'green':
                msg = pass_msg
                green_save = True
        elif rfreq == '1h':
            msg = fail_msg
            if nwe_color_15min == 'green' and nwe_color_5min == 'green':
                msg = pass_msg
                green_save = True
        elif rfreq == '30min':
            msg = fail_msg
            if nwe_color_5min == 'green':
                msg = pass_msg
                green_save = True
        elif rfreq == '15min':
            msg = fail_msg
            if nwe_color_5min == 'green':
                msg = pass_msg
                green_save = True

        if green_save:
            self.pos.sell_block_yn = 'Y'
            # all_hodls.append(msg)
            self.pos.sell_blocks.append(pass_msg)
        else:
            all_sells.append(fail_msg)
            # speak(msg)

    if self.pos.sell_block_yn == 'Y' or self.st_pair.sell.show_tests_yn in ('Y','F'):
        msg = ''
        msg += self.spacer 
        msg += f'==> SELL TESTS - {self.pos.prod_id} - All NWEs Green...'
        WoG(msg)
        if self.pos.sell_block_yn == 'Y' or self.st_pair.sell.show_tests_yn in ('Y'):
            for e in all_sells:
                if self.pos.prc_chg_pct > 0:
                    G(e)
                else:
                    R(e)
                self.show_sell_header_tf = True
            for e in all_hodls:
                WoG(e)
                self.show_sell_header_tf = True

#<=====>#


@narc(1)
def sell_pos_save(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_save(pos_id={self.pos.pos_id})')
    if self.pos.sell_yn == 'Y':
        if self.st_pair.sell.save_files_yn == 'Y':
            fname = f"saves/{self.pos.prod_id}_SELL_{dt.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.txt"
            self.writeit(fname, '=== MKT ===')
            for k in self.pair:
                self.writeit(fname, f'{k} : {self.pair[k]}'.format(k, self.pair[k]))
            self.writeit(fname, '')
            self.writeit(fname, '')
            self.writeit(fname, '=== POS ===')
            for k in self.pos:
                if isinstance(self.pos[k], (str, list, dict, float, int, decimal.Decimal, datetime, time)):
                    self.writeit(fname, f'{k} : {self.pos[k]}')
                else:
                    print(f'{k} : {type(self.pos[k])}')

#<=====>#


@narc(1)
def sell_pos_live(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_live(pos_id={self.pos.pos_id})')

    # 🔒 CRITICAL RACE CONDITION PREVENTION: Verify bot owns sell lock
    if not self.verify_bot_lock(self.pos.prod_id, 'sell'):
        R(f"❌ SELL LOCK VERIFICATION FAILED - Another bot owns {self.pos.prod_id} sell lock, ABORTING TRADE!")
        beep(5)
        return False  # Signal failure to bubble up and skip to next pair

    self.cbtrade_db.trade_strat_perfs_flag_upd(self.pos.prod_id, self.pos.buy_strat_type, self.pos.buy_strat_name, self.pos.buy_strat_freq)

    sell_data = self.cbtrade_db.db_sell_double_check_optimized(self.pos.pos_id)
    # db layer may return a list of rows; normalize to single dict row
    if isinstance(sell_data, list):
        sell_data = sell_data[0] if sell_data else None

    if sell_data and sell_data.get('pos_stat') != 'OPEN':
        print('another bot must have changed the position status since we started!!! SKIPPING SELL!!!')
        beep(3)
    elif sell_data and sell_data.get('so_id') is not None:
        print('another bot must have changed the position status since we started!!! SKIPPING SELL!!!')
        beep(3)
    else:

        if self.st_pair.sell.sell_limit_yn == 'N' and self.pair.mkt_limit_only_tf == 1:
            print(f'{self.pos.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')
            sell_cnt =self.cb.ord_mkt_sell_orig(self.pos, self.st_pair)

        elif self.st_pair.sell.sell_limit_yn == 'Y':
            sell_cnt =self.cb.ord_lmt_sell_open(self.pos) 

        else:
            sell_cnt =self.cb.ord_mkt_sell_orig(self.pos, self.st_pair)

        print(f'sell_pos_live() ==> before adjustment bal_cnt = {self.pair.bal_cnt}')
        self.pair.bal_cnt -= sell_cnt
        print(f'sell_pos_live() ==> post adjustment bal_cnt = {self.pair.bal_cnt}')

        # Update to Database
        print(f'sell_base.sell_pos_live() ==> self.cbtrade_db.db_poss_insupd() ==> {self.pos.prod_id}')
        self.pos.pos_stat = 'SELL'
        self.cbtrade_db.db_poss_insupd(self.pos)  # 🔴 GILFOYLE: ULTRA-OPTIMIZED (85-90% faster!)
        test_pos = self.cbtrade_db.db_poss_get(pos_id=self.pos.pos_id)
        if isinstance(test_pos, list):
            test_pos = test_pos[0]
        test_pos = AttrDict(test_pos)
        # pprint(test_pos)
        if test_pos.pos_stat != 'SELL':
            print(f'sell_base.sell_pos_live() ==> test_pos.pos_stat != SELL ==> {test_pos.pos_stat}')
            print(f'sell_base.sell_pos_live() ==> test_pos ==> {test_pos}')
            beep(10)
            sys.exit(f'sell_base.sell_pos_live() ==> test_pos.pos_stat != SELL ==> {test_pos.pos_stat}')

    return True  # Success - live sell operation completed

#<=====>#

@narc(1)
def sell_pos_test(self):
    if self.debug_tf: C(f'==> sell_base.sell_pos_test(pos_id={self.pos.pos_id})')
    
    # 🔒 CRITICAL RACE CONDITION PREVENTION: Verify bot owns sell lock
    # Even test trades affect statistics and performance metrics
    if not self.verify_bot_lock(self.pos.prod_id, 'sell'):
        R(f"❌ SELL LOCK VERIFICATION FAILED - Another bot owns {self.pos.prod_id} sell lock, ABORTING TEST TRADE!")
        beep(3)
        return False  # Signal failure to bubble up and skip to next pair

    self.cbtrade_db.trade_strat_perfs_flag_upd(self.pos.prod_id, self.pos.buy_strat_type, self.pos.buy_strat_name, self.pos.buy_strat_freq)

    so = AttrDict()
    so.test_txn_yn                 = self.pos.test_txn_yn
    so.symb                        = self.pos.symb
    so.prod_id                     = self.pos.prod_id
    so.pos_id                      = self.pos.pos_id
    so.sell_seq_nbr                = 1
    so.sell_order_uuid             = self.gen_guid()
    so.pos_type                    = 'SPOT'
    so.ord_stat                    = 'OPEN'
    so.sell_strat_type             = self.pos.sell_strat_type
    so.sell_strat_name             = self.pos.sell_strat_name
    so.sell_strat_freq             = self.pos.sell_strat_freq
    so.reason                      = self.pos.reason
    so.sell_begin_dttm             = dt.now(timezone.utc) # dt.now()
    so.sell_end_dttm               = dt.now(timezone.utc) # dt.now()

    # Set Unix timestamps for more accurate time tracking
    so.sell_begin_unix             = dttm_unix()
    so.sell_end_unix               = dttm_unix()

    so.sell_curr_symb              = self.pos.sell_curr_symb
    so.recv_curr_symb              = self.pos.recv_curr_symb
    so.fees_curr_symb              = self.pos.fees_curr_symb
    so.sell_cnt_est                = self.pos.hold_cnt
    so.sell_cnt_act                = self.pos.hold_cnt
    so.fees_cnt_act                = (self.pos.hold_cnt * self.pos.prc_sell) * 0.004
    so.tot_in_cnt                  = (self.pos.hold_cnt * self.pos.prc_sell) * 0.996
    so.prc_sell_est                = self.pos.prc_sell
    so.prc_sell_act                = self.pos.prc_sell
    so.prc_sell_tot                = self.pos.prc_sell
    so.prc_sell_slip_pct           = 0

    # Update to Database
    self.pos.pos_stat = 'SELL'
    self.cbtrade_db.db_poss_insupd(self.pos)

    print(f'sell_base.sell_pos_test() ==> self.cbtrade_db.db_poss_insupd() ==> {self.pos.prod_id}')
    self.cbtrade_db.db_sell_ords_insupd(so)

    test_pos = self.cbtrade_db.db_poss_get(pos_id=self.pos.pos_id)
    if isinstance(test_pos, list):
        test_pos = test_pos[0]
    test_pos = AttrDict(test_pos)
    # pprint(test_pos)
    if test_pos.pos_stat != 'SELL':
        print(f'sell_base.sell_pos_test() ==> test_pos.pos_stat != SELL ==> {test_pos.pos_stat}')
        print(f'sell_base.sell_pos_test() ==> test_pos ==> {test_pos}')
        beep(10)
        sys.exit(f'sell_base.sell_pos_test() ==> test_pos.pos_stat != SELL ==> {test_pos.pos_stat}')

    return True  # Success - test sell operation completed

#<=====>#
