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
import os
import sys
import time
import traceback
import uuid
from datetime import (
    datetime as dt
    , datetime
    , timedelta
    , timezone
)
from decimal import Decimal
from fstrent_colors import *
from pprint import pprint
from typing import Dict, List, Optional, Any, TypeAlias

#<=====>#
# Imports - Project
#<=====>#
# from libs.buy_base import *
# from libs.pos_base import *
# from libs.sell_base import *
from libs.common import (
    AttrDict
    , AttrDictConv
    , AttrDictEnh
    , beep
    , DictKey
    , dttm_get
    , dttm_unix
    , fatal_error_exit
    , format_disp_age2
    , format_disp_age3
    , narc
    , play_cash
    , play_thunder
    , print_adv
    , speak
)
from libs.coinbase_handler import cb
from libs.db_mysql.ohlcv.db_main import OHLCV_DB
from libs.settings_base import pair_settings_get
from libs.strat_base import buy_strats_get, buy_strats_avail_get
from libs.ta_base import ta_main_new
from libs.theme import *
from libs.trade_perfs_base import trade_perfs_get
from libs.trade_strat_perfs_base import trade_strat_perfs_get, trade_strat_perfs_get_all
# from libs.workflow_base import buy_ords_check, sell_ords_check 


#<=====>#
# Variables
#<=====>#
lib_name      = 'pair_base'
log_name      = 'pair_base'

# <=====>#
# Assignments Pre
# <=====>#



#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#


@narc(1)
def pair_new(self, pair_dict:AttrDict):
    if self.debug_tf: B(f'pair_base.pair_new() ==> {pair_dict.prod_id}')
    self.pair                      = AttrDict()
#    self.pair.class_name           = 'PAIR'
    for k, v in pair_dict.items():
        self.pair[k] = v
    self.prod_id                   = self.pair.prod_id
    self.pair.symb                 = self.mkt.symb
    self.st_pair                   = self.pair_settings_get(self.st_mkt, self.prod_id)
    self.pair.buy_strats           = self.buy_strats_get()
    self.pair.show_buy_header_tf   = True

#<=====>#


@narc(1)
def pair_timing_check(self):
    # B(f'pair_base.pair_timing_check: {self.prod_id}')
    if self.debug_tf: B(f'pair_base.pair_timing_check: {self.prod_id}')
    prod_id = self.prod_id

    buy_process_tf = False
    sell_process_tf = False

    sql_get = f"""
    select * from mkt_checks where prod_id = '{prod_id}'
    """
    # print(sql_get)

    check_data = self.cbtrade_db.seld(sql_get)
    # print(f'pair_base.pair_timing_check => check_data ({type(check_data)}): {check_data}')
    if not check_data:
        # Y(f"Warning: No buy_check_data found for {prod_id}. Rebuilding...")
        sql = f"""
        insert into mkt_checks (prod_id, buy_check_guid, buy_check_unix, sell_check_guid, sell_check_unix) values ('{prod_id}', '{self.bot_guid}', '{dttm_unix()}', '{self.bot_guid}', '{dttm_unix()}')
        """
        self.cbtrade_db.ins_one(sql)
        check_data = self.cbtrade_db.db_mkt_checks_get(prod_id)
        # print(f'pair_base.pair_timing_check => check_data ({type(check_data)}): {check_data}')
    if isinstance(check_data, list):
        check_data = check_data[0]

    check_data = AttrDict(check_data)
    # print(f'check_data: {check_data}')

    self.pair.buy_check_dttm    = check_data.buy_check_dttm
    self.pair.buy_check_unix    = check_data.buy_check_unix
    self.pair.buy_check_guid    = check_data.buy_check_guid
    # calculate elapsed time
    self.pair.buy_check_elapsed = round((dttm_unix() - self.pair.buy_check_unix) / 60, 2)
    self.pair.buy_check_dttm    = self.pair.buy_check_dttm.replace(tzinfo=timezone.utc)

    self.pair.sell_check_dttm    = check_data.sell_check_dttm
    self.pair.sell_check_unix    = check_data.sell_check_unix
    self.pair.sell_check_guid    = check_data.sell_check_guid
    # calculate elapsed time
    self.pair.sell_check_elapsed = round((dttm_unix() - self.pair.sell_check_unix) / 60, 2)

    # 🚨 CRITICAL FIX: Proper GUID-based race condition prevention
    if self.pair.buy_check_elapsed:
        if self.debug_tf: C(f"==> pair_base.pair_timing_check => buy check elapsed={self.pair.buy_check_elapsed}")
        if self.pair.buy_check_elapsed > 5:  # Increased from 3 to 5 minutes
            # 🔒 CRITICAL: Check if this bot owns the lock OR can claim it
            if (self.pair.buy_check_guid == self.bot_guid or 
                self.pair.buy_check_elapsed > 10):  # Allow takeover after 10 minutes
                # Claim/renew the lock BEFORE processing
                self.cbtrade_db.db_mkt_checks_buy_upd(prod_id, self.bot_guid)
                buy_process_tf = True
                if self.debug_tf: C(f"==> {self.prod_id} BUY LOCK CLAIMED by {self.bot_guid[:8]}")
            else:
                if self.debug_tf: C(f"==> {self.prod_id} BUY LOCK OWNED by {self.pair.buy_check_guid[:8]}, skipping")

    if self.pair.sell_check_elapsed:
        if self.debug_tf: C(f"==> pair_base.pair_timing_check => sell check elapsed={self.pair.sell_check_elapsed}")
        if self.pair.sell_check_elapsed > 5:  # Increased from 3 to 5 minutes
            # 🔒 CRITICAL: Check if this bot owns the lock OR can claim it
            if (self.pair.sell_check_guid == self.bot_guid or 
                self.pair.sell_check_elapsed > 10):  # Allow takeover after 10 minutes
                # Claim/renew the lock BEFORE processing
                self.cbtrade_db.db_mkt_checks_sell_upd(prod_id, self.bot_guid)
                sell_process_tf = True
                if self.debug_tf: C(f"==> {self.prod_id} SELL LOCK CLAIMED by {self.bot_guid[:8]}")
            else:
                if self.debug_tf: C(f"==> {self.prod_id} SELL LOCK OWNED by {self.pair.sell_check_guid[:8]}, skipping")

    hmsg = ""
    hmsg += f"{'prod_id':^20} | "
    hmsg += f"{'dttm':^20} | "
    hmsg += f"{'buy_check_guid':^40} | "
    hmsg += f"{'buy_elapsed':^12} | "
    hmsg += f"{'buy_check_dttm':^20} | "
    hmsg += f"{'buy_process_tf':^15} | "
    hmsg += f"{'sell_check_guid':^40} | "
    hmsg += f"{'sell_elapsed':^12} | "
    hmsg += f"{'sell_check_dttm':^20} | "
    hmsg += f"{'sell_process_tf':^15} | "

    msg = ''
    msg += f'{self.prod_id:^20} | '
    msg += f'{dttm_get():^20} | '
    msg += f'{self.pair.buy_check_guid:^40} | '
    msg += f'{self.pair.buy_check_elapsed:^12} | '
    msg += f'{self.pair.buy_check_dttm.strftime('%Y-%m-%d %H:%M:%S'):^20} | '
    msg += f'{buy_process_tf:^15} | '
    msg += f'{self.pair.sell_check_guid:^40} | '
    msg += f'{self.pair.sell_check_elapsed:^12} | '
    msg += f'{self.pair.sell_check_dttm.strftime('%Y-%m-%d %H:%M:%S'):^20} | '
    msg += f'{sell_process_tf:^15} |'

    # print(hmsg)
    # print(msg)

    self.chrt.chart_headers(in_str=hmsg, bold=True, align='left', len_cnt=260)
    self.chrt.chart_row(msg, bold=True, len_cnt=260)
    self.chrt.chart_bottom(bold=True, len_cnt=260)

    return buy_process_tf, sell_process_tf

#<=====>#

@narc(1)
def verify_bot_lock(self, prod_id: str, operation: str = 'both') -> bool:
    """
    🔒 CRITICAL SECURITY FUNCTION: Verify this bot owns the processing lock
    
    This function provides a final verification before any critical trading operations
    to prevent race conditions and duplicate trades.
    
    Args:
        prod_id: Product ID to check (e.g., 'AVNT-USDC')
        operation: 'buy', 'sell', or 'both' (default: 'both')
    
    Returns:
        bool: True if this bot owns the required lock(s), False otherwise
    """
    if self.debug_tf: G(f'==> pair_base.verify_bot_lock({prod_id}, {operation})')
    
    sql_get = f"SELECT * FROM mkt_checks WHERE prod_id = '{prod_id}'"
    check_data = self.cbtrade_db.seld(sql_get)
    
    if not check_data:
        # No lock exists - this is suspicious for active trading
        Y(f"⚠️ WARNING: No market check record found for {prod_id} during lock verification!")
        return False
    
    if isinstance(check_data, list):
        check_data = check_data[0]
    
    check_data = AttrDict(check_data)
    
    # Check buy lock if required
    if operation in ('buy', 'both'):
        if check_data.buy_check_guid != self.bot_guid:
            if self.debug_tf: R(f"❌ BUY LOCK VERIFICATION FAILED: {prod_id} owned by {check_data.buy_check_guid[:8]}, not {self.bot_guid[:8]}")
            return False
    
    # Check sell lock if required  
    if operation in ('sell', 'both'):
        if check_data.sell_check_guid != self.bot_guid:
            if self.debug_tf: R(f"❌ SELL LOCK VERIFICATION FAILED: {prod_id} owned by {check_data.sell_check_guid[:8]}, not {self.bot_guid[:8]}")
            return False
    
    if self.debug_tf: G(f"✅ LOCK VERIFICATION PASSED: {prod_id} {operation} owned by {self.bot_guid[:8]}")
    return True

#<=====>#


@narc(1)
def pair_init(self):
    if self.debug_tf: B(f'pair_base.pair_init() ==> {self.prod_id}')
    self.pair.mkt_id                    = 0
    self.pair.mkt_name                  = ''
    self.pair.mkt_venue                 = ''
    self.pair.base_curr_symb            = ''
    self.pair.base_curr_name            = ''
    self.pair.base_size_incr            = 0
    self.pair.base_size_min             = 0
    self.pair.base_size_max             = 0
    self.pair.quote_curr_symb           = ''
    self.pair.quote_curr_name           = ''
    self.pair.quote_size_incr           = 0
    self.pair.quote_size_min            = 0
    self.pair.quote_size_max            = 0
    self.pair.mkt_status_tf             = ''
    self.pair.mkt_view_only_tf          = False
    self.pair.mkt_watched_tf            = False
    self.pair.mkt_is_disabled_tf        = False
    self.pair.mkt_new_tf                = False
    self.pair.mkt_cancel_only_tf        = False
    self.pair.mkt_limit_only_tf         = False
    self.pair.mkt_post_only_tf          = False
    self.pair.mkt_trading_disabled_tf   = False
    self.pair.mkt_auction_mode_tf       = False
    self.pair.prc                       = 0
    self.pair.prc_ask                   = 0
    self.pair.prc_buy                   = 0
    self.pair.prc_bid                   = 0
    self.pair.prc_sell                  = 0
    self.pair.prc_mid_mkt               = 0
    self.pair.prc_pct_chg_24h           = 0
    self.pair.vol_24h                   = 0
    self.pair.vol_base_24h              = 0
    self.pair.vol_quote_24h             = 0
    self.pair.vol_pct_chg_24h           = 0
    self.pair.ignore_tf                 = False
    self.pair.note1                     = ''
    self.pair.note2                     = ''
    self.pair.note3                     = ''
    # self.add_dttm                  = ''
    # self.dlm                       = ''
    # self.add_unix                  = 0
    # self.dlm_unix                  = 0

#<=====>#

@narc(1)
def pair_main(self):
    if self.debug_tf: B(f'pair_base.pair_main() ==> {self.prod_id}')
    prod_id = self.prod_id

    self.disp_pair_header()

    # This is only for disp_pair
    self.mkts_tot = len(self.mkt.loop_pairs)

    # lets Avoid Trading Stable Coins Against One Another
    if self.pair.base_curr_symb in self.st_pair.stable_coins:
        # print(f'return 515 pair_main(prod_id={prod_id}) - self.base_curr_symb in self.st_pair.stable_coins')
        return

    # build the market
    self.pair_build()

    # If timing checks indicate no processing this cycle, skip logic to avoid accessing unset fields
    if (self.mode == 'buy' and not getattr(self, 'buy_process_tf', False)) \
       or (self.mode == 'sell' and not getattr(self, 'sell_process_tf', False)) \
       or (self.mode == 'full' and not (getattr(self, 'buy_process_tf', False) or getattr(self, 'sell_process_tf', False))):
        return

    # process the market
    self.pair_logic()  # 🔒 Lock verification happens inside, skips operations if needed

    print_adv(2)

#<=====>#

@narc(1)
def pair_build(self):
    if self.debug_tf: B(f'pair_base.pair_build() ==> {self.prod_id}')
    prod_id = self.prod_id

    self.buy_process_tf, self.sell_process_tf = self.pair_timing_check()
    if self.debug_tf: B(f'pair_base.pair_build() ==> {self.prod_id} - buy_process_tf={self.buy_process_tf}, sell_process_tf={self.sell_process_tf}')

    if self.mode == 'buy' and not self.buy_process_tf:
        # print(f'pair_base.pair_build() ==> {self.prod_id} - buy_process_tf={self.buy_process_tf}, sell_process_tf={self.sell_process_tf}')
        return
    elif self.mode == 'sell' and not self.sell_process_tf:
        # print(f'pair_base.pair_build() ==> {self.prod_id} - buy_process_tf={self.buy_process_tf}, sell_process_tf={self.sell_process_tf}')
        return
    elif self.mode == 'full' and not self.buy_process_tf and not self.sell_process_tf:
        # print(f'pair_base.pair_build() ==> {self.prod_id} - buy_process_tf={self.buy_process_tf}, sell_process_tf={self.sell_process_tf}')
        return

    # Get pair data from database
    pair_data  = self.cbtrade_db.db_mkts_get(prod_id=self.prod_id)[0]
    # print(f'pair_data: {pair_data}')
    for key, value in pair_data.items():
        if DictKey(self, key):
            # print(f'key: {key}, value: {value}')
            self[key] = value

    # Extract base and quote currencies from prod_id
    if self.prod_id and '-' in self.prod_id:
        parts = self.prod_id.split('-')
        self.base_currency  = parts[0]
        self.quote_currency = parts[1] if len(parts) > 1 else ''

    # Estimate the true buy/sell prices by looking at the order book
    pricing_cnt = self.st_pair.buy.trade_size
    max_poss_open_trade_size = self.cbtrade_db.db_poss_open_max_trade_size_get(prod_id)
    if max_poss_open_trade_size:
        if max_poss_open_trade_size > pricing_cnt:
            pricing_cnt = max_poss_open_trade_size


    # Get pricing data
    self.pair.prc_mkt              = self.pair.prc
    bid_prc, ask_prc               = self.cb.cb_bid_ask_by_amt_get(pair=self.pair, buy_sell_size=pricing_cnt)
    self.pair.prc_bid              = bid_prc
    self.pair.prc_ask              = ask_prc
    self.pair.prc_dec              = self.cb.cb_mkt_prc_dec_calc(self.pair.prc_bid, self.pair.prc_ask)
    self.pair.prc_buy              = self.pair.prc_ask
    self.pair.prc_sell             = self.pair.prc_bid

    # temo_data = self.to_dict()
    # for k,v in temo_data.items():
    #     print(f'{k:>20} : {v}')

    self.pair.prc_range_pct        = ((self.pair.prc_buy - self.pair.prc_sell) / self.pair.prc) * 100
    self.pair.prc_buy_diff_pct     = ((self.pair.prc - self.pair.prc_buy) / self.pair.prc) * 100
    self.pair.prc_sell_diff_pct    = ((self.pair.prc - self.pair.prc_sell) / self.pair.prc) * 100

    # Market Performance
    self.pair.buy_strats           = self.buy_strats_get()

    # Market Performance
    self.pair.trade_perfs          = self.trade_perfs_get_by_prod_id(prod_id=prod_id)

    # Market Strat Performances
    self.pair.trade_strat_perfs    = self.trade_strat_perfs_get_all(prod_id=prod_id, buy_strats=self.pair.buy_strats)

    self.pair.show_buy_header_tf = True
    self.pair.timings = []

#<=====>#

@narc(1)
def pair_logic(self):
    if self.debug_tf: B(f'pair_base.pair_logic() ==> {self.prod_id}')
    prod_id      = self.prod_id

    if self.mode in ('buy','full'):
        self.buy_strats = self.buy_strats_avail_get(prod_id, self.st_pair)

    # Market Technical Analysis
    self.pair.ta = None
    try:
        # Only log prices if already populated by pair_build; avoid AttributeError on first cycle
        # if hasattr(self.pair, 'prc_mkt') and hasattr(self.pair, 'prc_bid') and hasattr(self.pair, 'prc_ask'):
        #     print(f'pair_base.pair_logic() ==> {self.prod_id} - self.pair.prc_mkt={self.pair.prc_mkt}, self.pair.prc_bid={self.pair.prc_bid}, self.pair.prc_ask={self.pair.prc_ask}')
        # First: Get fresh data and technical analysis
        self.pair.ta = ta_main_new(self.pair, st_pair=self.st_pair)
        if not self.pair.ta:
            WoR(f'{dttm_get()}  - Get TA ==> TA Errored and is None')
            return True  # 🔒 SUCCESS: Valid skip due to TA error (not a lock issue)
        if self.pair.ta == 'Error!':
            WoR(f'{dttm_get()}  - Get TA ==> {prod_id} - close prices do not match')
            return True  # 🔒 SUCCESS: Valid skip due to TA error (not a lock issue)

        # # Second: Display OHLCV status AFTER fresh data is available
        # ohlcv_db = OHLCV_DB(prod_id=prod_id)
        # ohlcv_db.db_ohlcv_candle_status_display(display_enabled=True)
    except SystemExit:
        raise  # 🚨 NEVER catch SystemExit - let it pass through
    except BaseException as e:
        print(f"\n🚨 ERROR in pair_logic() ==> {prod_id}")
        print(f"🚨 ERROR_TYPE: {type(e).__name__}")
        print(f"🚨 ERROR_MESSAGE: {str(e)}")
        print(f"🚨 FULL_TRACEBACK:")
        traceback.print_exc()
        sys.exit(f"FATAL ERROR: {type(e).__name__}: {str(e)}")

    # self.chrt.chart_bottom(len_cnt=260)

    self.disp_pair()
 
    # Market Buy Logic
    if self.mode in ('buy','full') and prod_id in self.mkt.buy_pairs:
        # 🔒 CRITICAL: If lock verification fails, skip to next pair entirely
        if self.pair_logic_buy() == False:
            R(f"🚨 SKIPPING TO NEXT PAIR: Buy lock verification failed for {prod_id}")
            return  # Exit pair_main() → market loop continues to next pair

    # Market Sell Logic
    if self.mode in ('sell','full'):
        # 🔒 CRITICAL: If lock verification fails, skip to next pair entirely  
        if self.pair_logic_sell() == False:
            R(f"🚨 SKIPPING TO NEXT PAIR: Sell lock verification failed for {prod_id}")
            return  # Exit pair_main() → market loop continues to next pair

    pair_context = {
        'pair': self.pair,
        'st_pair': self.st_pair,
        'st_mkt': self.st_mkt,
        'bot_guid': self.bot_guid
    }
    
    # Trace buy_ords_check with granular detail
    self.buy_ords_check(prod_id=prod_id, pair_context=pair_context)

    # Trace sell_ords_check with granular detail
    self.sell_ords_check(prod_id=prod_id, pair_context=pair_context)

    self.cbtrade_db.db_mkts_insupd(self.pair)
    # if self.st_pair.show_timings_yn == 'Y':
    #     title_msg = f'* {self.prod_id} * Timings *'
    #     self.chrt.chart_top(in_str=title_msg, bold=True)
    #     for x in self.timings:
    #         for k,v in x.items():
    #             msg = cs(f'actv : {k:>50}, elapsed : {v:>6.2f}', font_color='white', bg_color='black')
    #             self.chrt.chart_row(in_str=msg)

    #     self.chrt.chart_bottom()
    print_adv()

#<=====>#


@narc(1)
def pair_logic_buy(self):
    if self.debug_tf: B(f'pair_base.pair_logic_buy() ==> {self.prod_id}')
    prod_id = self.prod_id

    t0 = time.perf_counter()
    if self.st_pair.buy.buying_on_yn == 'Y' and prod_id in getattr(self.mkt, 'buy_pairs', []):
        self.buy_new()
        # 🔒 CRITICAL: Check for lock verification failure
        if self.buy_main() == False:
            R(f"🚨 BUY MAIN FAILED: Lock verification failed for {prod_id}")
            return False  # Bubble up failure to skip entire pair
    
    return True  # Success - continue with pair processing

#<=====>#


@narc(1)
def pair_logic_sell(self):
    if self.debug_tf: B(f'pair_base.pair_logic_sell() ==> {self.prod_id}')
    prod_id = self.prod_id

    # self.debug_tf = True
    t0 = time.perf_counter()
    if self.st_pair.sell.selling_on_yn == 'Y':

        # Use db_poss_open_get_by_prod_id() instead of db_poss_get() because it includes new_age_mins calculation
        live_poss, test_poss, all_poss = self.cbtrade_db.db_poss_open_get_by_prod_id(prod_id=prod_id)
        # self.pair.open_poss = all_poss  # Use all open positions (live + test)

        self.pair.open_poss = []
        for pos in live_poss:
            pos = AttrDict(pos)
            self.pair.open_poss.append(pos)
        for pos in test_poss:
            pos = AttrDict(pos)
            self.pair.open_poss.append(pos)

        if self.debug_tf: B(f'pair_base.pair_logic_sell() ==> self.pair.open_poss: {len(self.pair.open_poss)}')

        if len(self.pair.open_poss) > 0:
            # 🔒 CRITICAL: Check for lock verification failure
            if self.sell_logic() == False:
                R(f"🚨 SELL MAIN FAILED: Lock verification failed for {prod_id}")
                return False  # Bubble up failure to skip entire pair
        else:
            WoR(f'{dttm_get()}  - No open positions found for {prod_id}')
    # self.debug_tf = False
    
    return True  # Success - continue with pair processing

#<=====>#


@narc(1)
def disp_pair_header(self):
    print_adv(2)
    if self.debug_tf: B(f'pair_base.disp_pair_header() ==> {self.prod_id}')
    # Market Basics
    prod_id = self.prod_id
    title_msg = f'* {prod_id} * Trade Pair * {dttm_get()} * {self.bot_guid} * {self.mkt.dttm_start_loop} * {self.mkt.loop_age} * {self.mkt.cnt}/{len(self.mkt.loop_pairs)} *'
    self.chrt.chart_top(bold=True, len_cnt=260)
    self.chrt.chart_headers(in_str=title_msg, bold=True, align='center', len_cnt=260)
    self.chrt.chart_mid(bold=True, len_cnt=260)

#<=====>#


@narc(1)
def disp_pair(self):
    if self.debug_tf: B(f'pair_base.disp_pair() ==> {self.prod_id}')
    self.disp_pair_summary()
    self.disp_pair_stats()
    self.disp_mkt_budget(title='Market Budget', budget=self.budget)
    self.disp_pair_ta_stats()
    self.disp_pair_performance()

#<=====>#


@narc(1)
def disp_pair_summary(self):
    if self.debug_tf: B(f'pair_base.disp_pair_summary() ==> {self.prod_id}')
    # Market Basics
    prod_id = self.prod_id

    # Budget spendable amount available - run silently during normal operation
    
    # print('')
    # print('budget:')
    # pprint(self.budget)
    # print('')

    title_msg = f'* {prod_id} * Pair Summary *'
    print_adv()
    self.chrt.chart_top(in_str=title_msg, bold=True, len_cnt=260)

    # Prices & Balances
    hmsg = ""
    hmsg += f"$ {'price':^15} | "
    hmsg += f"{'prc_chg':^10} % | "
    hmsg += f"$ {'buy_prc':^15} | "
    hmsg += f"$ {'sell_prc':^15} | "
    hmsg += f"{'buy_var':^10} % | "
    hmsg += f"{'sell_var':^10} % | "
    hmsg += f"{'spread_pct':^10} % | "
    hmsg += f"$ {'usdc bal':^9} | "
    hmsg += f"$ {'reserve':^9} | "
    hmsg += f"$ {'available':^9} | "
    hmsg += f"{'reserves state':^15} | "

    msg = ""
    if self.pair.prc_pct_chg_24h < 0:
        msg += cs(f"$ {self.pair.prc_mkt:>15.8f}", 'white', 'red') + " | "
        msg += cs(f"{self.pair.prc_pct_chg_24h:>10.4f} %", 'white', 'red') + " | "
    elif self.pair.prc_pct_chg_24h > 0:
        msg += cs(f"$ {self.pair.prc_mkt:>15.8f}", 'white', 'green') + " | "
        msg += cs(f"{self.pair.prc_pct_chg_24h:>10.4f} %", 'white', 'green') + " | "
    else:
        msg += f"$ {self.pair.prc_mkt:>15.8f} | "
        msg += f"{self.pair.prc_pct_chg_24h:>10.4f} % | "

    msg += f"$ {self.pair.prc_buy:>15.8f} | "
    msg += f"$ {self.pair.prc_sell:>15.8f} | "
    msg += f"{self.pair.prc_buy_diff_pct:>10.4f} % | "
    msg += f"{self.pair.prc_sell_diff_pct:>10.4f} % | "

    if self.pair.prc_range_pct < 0:
        msg += cs(f"{self.pair.prc_range_pct:>10.4f} %", 'white', 'red') + " | "
    elif self.pair.prc_range_pct > 0:
        msg += cs(f"{self.pair.prc_range_pct:>10.4f} %", 'white', 'green') + " | "
    else:
        msg += f"{self.pair.prc_range_pct:>10.4f} %" + " | "

    msg += cs(f"$ {self.budget.bal_avail:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.reserve_amt:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spendable_amt:>9.2f}", "white", "green") + " | "
    if self.budget.reserve_locked_tf:
        msg += cs(f"{'LOCKED':^15}", "yellow", "magenta") + " | "
    else:
        msg += cs(f"{'UNLOCKED':^15}", "magenta", "yellow") + " | "
    self.chrt.chart_headers(in_str=hmsg, bold=True, len_cnt=260)
    self.chrt.chart_row(in_str=msg, len_cnt=260)
    self.chrt.chart_bottom(bold=True, len_cnt=260)
    print_adv()
    
    # # Display sell performance summary if available
    # self.disp_sell_performance_summary()

#<=====>#


@narc(1)
def disp_sell_performance_summary(self):
    if self.debug_tf: B(f'pair_base.disp_sell_performance_summary() ==> {self.prod_id}')
    """
    Display sell logic performance summary after pair summary self.chrt.chart_bottom
    """
        
    data = self.sell_performance_data
    
    # Only show if detailed summary is warranted
    if not data.get('show_detailed', False):
        return
        
    from libs.theme import WoB, WoR
    
    print_adv()  # Add spacing before performance summary
    
    
    # TA performance stats if available
    if 'ta_stats' in data:
        ta = data['ta_stats']

#<=====>#


@narc(1)
def disp_pair_stats(self):
    if self.debug_tf: B(f'pair_base.disp_pair_stats() ==> {self.prod_id}')
    # print(f'self.trade_perfs: {self.trade_perfs}')

    # Market Basics
    prod_id = self.prod_id

    hmsg = ""
    hmsg += f"{'trades':^9} | "
    hmsg += f"{'wins':^9} | "
    hmsg += f"{'lose':^9} | "
    hmsg += f"{'win_pct':^9} % | "
    hmsg += f"{'lose_pct':^9} % | "
    hmsg += f"$ {'win_amt':^9} | "
    hmsg += f"$ {'lose_amt':^9} | "
    hmsg += f"$ {'spent':^9} | "
    hmsg += f"$ {'recv':^9} | "
    hmsg += f"$ {'hold':^9} | "
    hmsg += f"$ {'val':^9} | "
    hmsg += f"$ {'gain_amt':^9} | "
    hmsg += f"{'gain_pct':^9} % | "
    hmsg += f"{'gain_hr':^9} % | "
    hmsg += f"{'gain_day':^9} % | "
    hmsg += f"{'elapsed':^9} | "

    msg = ''
    tp = self.pair.trade_perfs['A']  # Extract to avoid f-string quote conflicts
    msg += f'{tp.tot_cnt:>9}' + ' | '
    msg += cs(f'{tp.win_cnt:>9}', font_color='white', bg_color='green') + ' | '
    msg += cs(f'{tp.lose_cnt:>9}', font_color='white', bg_color='red') + ' | '
    msg += cs(f'{tp.win_pct:>9.2f} %', font_color='white', bg_color='green') + ' | '
    msg += cs(f'{tp.lose_pct:>9.2f} %', font_color='white', bg_color='red') + ' | '
    msg += cs(f'$ {tp.win_amt:>9.4f}', font_color='white', bg_color='green') + ' | '
    msg += cs(f'$ {tp.lose_amt:>9.4f}', font_color='white', bg_color='red') + ' | '
    msg += f'$ {tp.tot_out_cnt:>9.4f}' + ' | '
    msg += f'$ {tp.tot_in_cnt:>9.4f}' + ' | '
    msg += f'$ {tp.val_curr:>9.4f}' + ' | '
    msg += f'$ {tp.val_tot:>9.4f}' + ' | '
    if tp.gain_loss_amt > 0:
        msg += cs(f'$ {tp.gain_loss_amt:>9.4f}', font_color='white', bg_color='green') + ' | '
        msg += cs(f'{tp.gain_loss_pct:>9.4f} %', font_color='white', bg_color='green') + ' | '
        msg += cs(f'{tp.gain_loss_pct_hr:>9.4f} %', font_color='white', bg_color='green') + ' | '
        msg += cs(f'{tp.gain_loss_pct_day:>9.4f} %', font_color='white', bg_color='green') + ' | '
    else:
        msg += cs(f'$ {tp.gain_loss_amt:>9.4f}', font_color='white', bg_color='red') + ' | '
        msg += cs(f'{tp.gain_loss_pct:>9.4f} %', font_color='white', bg_color='red') + ' | '
        msg += cs(f'{tp.gain_loss_pct_hr:>9.4f} %', font_color='white', bg_color='red') + ' | '
        msg += cs(f'{tp.gain_loss_pct_day:>9.4f} %', font_color='white', bg_color='red') + ' | '
    msg += f'{tp.last_elapsed:>9}' + ' | '

    title_msg = f'* {prod_id} * Market Stats *'
    self.chrt.chart_top(in_str=title_msg, bold=True, len_cnt=260)
    self.chrt.chart_headers(in_str=hmsg, bold=True, len_cnt=260)
    self.chrt.chart_row(msg, len_cnt=260)

    self.chrt.chart_bottom(bold=True, len_cnt=260)
    print_adv()

#<=====>#


@narc(1)
def disp_pair_ta_stats(self):
    if self.debug_tf: B(f'pair_base.disp_pair_ta_stats() ==> {self.prod_id}')
    '''
    # Up arrows
    print('↑')      # Basic up arrow
    print('⬆')      # Bold up arrow
    print('⇧')      # Outlined up arrow
    print('△')      # Triangle up
    print('▲')      # Filled triangle up

    # Down arrows  
    print('↓')      # Basic down arrow
    print('⬇')      # Bold down arrow
    print('⇩')      # Outlined down arrow
    print('▽')      # Triangle down
    print('▼')      # Filled triangle down
    '''

    prod_id = self.prod_id
    if self.pair.ta:
        freq_disp = {}
        for freq in self.pair.ta:
            msg_tail = cs(f'{freq:>6}', font_color="white", bg_color='blue') + ' => '

            # print(f'self.pair.ta[{freq}]: {self.pair.ta[freq]}')

            # candle

            # ha
            ha_color      = self.pair.ta[freq]['nwe_color']['ago0']
            ha_color_last = self.pair.ta[freq]['nwe_color']['ago1']
            ha_color_prev = self.pair.ta[freq]['nwe_color']['ago2']
            msg_tail += cs(f'HA', font_color="white", bg_color=ha_color) + ' | '
            msg_tail += cs(f'HA1', font_color="white", bg_color=ha_color_last) + ' | '
            msg_tail += cs(f'HA2', font_color="white", bg_color=ha_color_prev) + ' | '

            # sha fast
            sha_fast_color      = self.pair.ta[freq]['sha_fast_color']['ago0']
            sha_fast_color_last = self.pair.ta[freq]['sha_fast_color']['ago1']
            sha_fast_color_prev = self.pair.ta[freq]['sha_fast_color']['ago2']
            msg_tail += cs(f'FSHA', font_color="white", bg_color=sha_fast_color) + ' | '
            msg_tail += cs(f'FSHA1', font_color="white", bg_color=sha_fast_color_last) + ' | '
            msg_tail += cs(f'FSHA2', font_color="white", bg_color=sha_fast_color_prev) + ' | '

            # sha fast
            sha_slow_color      = self.pair.ta[freq]['sha_fast_color']['ago0']
            sha_slow_color_last = self.pair.ta[freq]['sha_fast_color']['ago1']
            sha_slow_color_prev = self.pair.ta[freq]['sha_fast_color']['ago2']
            msg_tail += cs(f'SSHA', font_color="white", bg_color=sha_slow_color) + ' | '
            msg_tail += cs(f'SSHA1', font_color="white", bg_color=sha_slow_color_last) + ' | '
            msg_tail += cs(f'SSHA2', font_color="white", bg_color=sha_slow_color_prev) + ' | '

            # macd
            mdc_color      = self.pair.ta[freq]['mdc']['ago0']
            mdc_color_last = self.pair.ta[freq]['mdc']['ago1']
            mdc_color_prev = self.pair.ta[freq]['mdc']['ago2']
            msg_tail += cs(f'imacd', font_color="white", bg_color=mdc_color) + ' | '
            msg_tail += cs(f'imacd', font_color="white", bg_color=mdc_color_last) + ' | '
            msg_tail += cs(f'imacd', font_color="white", bg_color=mdc_color_prev) + ' | '

            # nwe
            cnt = 0
            for ago in self.pair.ta[freq]['nwe_color']:
                nwe_color = self.pair.ta[freq]['nwe_color'][ago]
#                    nwe_diff_product = self.pair.ta[freq]['nwe_diff_product'][ago]
                nwe_roc = self.pair.ta[freq]['nwe_roc'][ago]
                msg_tail += cs(f'NWE', font_color="white", bg_color=nwe_color)
                if nwe_roc > 0:
                    msg_tail += cs(f'↑', font_color="white", bg_color='green')
                elif nwe_roc < 0:
                    msg_tail += cs(f'↓', font_color="white", bg_color='red')
                else:
                    msg_tail += cs(f'-', font_color="white", bg_color='blue')
                msg_tail += ' | '
                cnt += 1
                if cnt == 4: break

            freq_disp[freq] = msg_tail

        title_msg = f'* {prod_id} * TA Stats *'
        self.chrt.chart_top(in_str=title_msg, bold=True, len_cnt=260)
        for freq in freq_disp:
            self.chrt.chart_row(freq_disp[freq], len_cnt=260)

        self.chrt.chart_bottom(bold=True, len_cnt=260)
        print_adv()

#<=====>#

# @safe_execute_silent()  # 🔴 GILFOYLE: Silent display function

@narc(1)
def disp_pair_performance(self):
    if self.debug_tf: B(f'pair_base.disp_pair_performance() ==> {self.prod_id}')
    # Market Basics
    prod_id = self.prod_id

    hmsg = ""
    hmsg += f"{'strat':<15} | "
    hmsg += f"{'freq':<15} | "
    hmsg += f"{'total':^5} | "
    hmsg += f"{'open':^11} | "
    hmsg += f"{'open_test':^11} | "
    hmsg += f"{'open_live':^11} | "
    hmsg += f"{'close':^5} | "
    hmsg += f"{'wins':^5} | "
    hmsg += f"{'lose':^5} | "
    hmsg += f"{'win':^6} % | "
    hmsg += f"{'lose':^6} % | "
    hmsg += f"{'gain_amt':^10} | "
    hmsg += f"{'gain_pct':^10} % | "
    hmsg += f"{'gain_hr':^10} % | "
    hmsg += f"{'gain_day':^10} % | "
    hmsg += f"{'elapsed':^9} | "

    title_msg = f'* {prod_id} * Strategy Past Performance * Live + Test *'
    self.chrt.chart_top(in_str=title_msg, bold=True, len_cnt=260)
    self.chrt.chart_headers(hmsg, bold=True, len_cnt=260)

    for x in self.pair.trade_strat_perfs:
        x = AttrDict(x)

        if x.lta in ('L', 'T'):
            continue

        # Find T and L records from already-loaded self.pair.trade_strat_perfs (no DB call)
        t_record = next((tsp for tsp in self.pair.trade_strat_perfs 
                        if tsp.buy_strat_type == x.buy_strat_type 
                        and tsp.buy_strat_name == x.buy_strat_name 
                        and tsp.buy_strat_freq == x.buy_strat_freq 
                        and tsp.lta == 'T'), None)
        l_record = next((tsp for tsp in self.pair.trade_strat_perfs 
                        if tsp.buy_strat_type == x.buy_strat_type 
                        and tsp.buy_strat_name == x.buy_strat_name 
                        and tsp.buy_strat_freq == x.buy_strat_freq 
                        and tsp.lta == 'L'), None)
        test_tot_open_cnt = t_record.tot_open_cnt if t_record else 0
        live_tot_open_cnt = l_record.tot_open_cnt if l_record else 0

        if x.tot_cnt > 0:
            msg = ''
            msg += f'{x.buy_strat_name:<15} | '
            msg += f'{x.buy_strat_freq:<15} | '
            msg += f'{int(x.tot_cnt):>5} | '
            msg += f'{int(x.tot_open_cnt):>11} | '
            msg += f'{int(test_tot_open_cnt):>11} | '
            msg += f'{int(live_tot_open_cnt):>11} | '
            msg += f'{int(x.tot_close_cnt):>5} | '
            msg += f'{int(x.win_cnt):>5} | '
            msg += f'{int(x.lose_cnt):>5} | '
            msg += f'{x.win_pct:>6.2f} % | '
            msg += f'{x.lose_pct:>6.2f} % | '
            msg += f'{x.gain_loss_amt:>10.2f} | '
            msg += f'{x.gain_loss_pct:>10.2f} % | '
            msg += f'{x.gain_loss_pct_hr:>10.2f} % | '
            msg += f'{x.gain_loss_pct_day:>10.2f} % | '
            elapsed_seconds = int(dttm_unix()) - int(x.last_buy_strat_unix or 0)
            msg += f'{format_disp_age3(elapsed_seconds):>9}' + ' | '
            msg  = cs_pct_color_50(pct=x.win_pct, msg=msg)
            self.chrt.chart_row(in_str=msg, len_cnt=260)
    self.chrt.chart_bottom(bold=True, len_cnt=260)
    print_adv()

#<=====>#


# @narc(1)
# def display_strat_perf_summary(self, prod_id, lta=None):
#     if self.debug_tf: B(f'pair_base.display_strat_perf_summary() ==> {self.prod_id}')
#     """Display a summary of strategy performance for a product"""
#     strat_perfs = self.db_trade_strat_perfs_get_by_prod_id(prod_id, lta)
    
#     if not strat_perfs:
#         print(f"📊 No strategy performance data found for {prod_id}")
#         return
    
#     print(f"\n📊 Strategy Performance Summary for {prod_id}")
#     print("=" * 80)
    
#     for perf in strat_perfs:
#         print(f"\n🎯 {perf.buy_strat_name} ({perf.buy_strat_freq})")
#         print(f"   Total Trades: {perf.tot_cnt} | Open: {perf.tot_open_cnt} | Closed: {perf.tot_close_cnt}")
#         print(f"   Win Rate: {perf.win_pct}% ({perf.win_cnt}/{perf.tot_close_cnt})")
#         print(f"   Net Gain/Loss: {perf.gain_loss_amt_net:.6f}")
#         print(f"   Last Trade: {perf.strat_last_elapsed:.1f} minutes ago")

#<=====>#


# @narc(1)
# def pair_to_dict(self):
#     if self.debug_tf: B(f'pair_base.pair_to_dict() ==> {self.prod_id}')
#     """Override to_dict for bot-specific attributes"""

#     simple_types = (int, float, str, list, dict, tuple, bool, AttrDict)
#     data_dict = AttrDict()

#     for k, v in self.pair.items():
#         # print(f'k: {k}, {type(v)} v: {v}')
#         if isinstance(v, simple_types) and k not in ('bot_data', 'mkt_data', 'mkt_budget', 'st_bot', 'st_debug', 'st_mkt', 'st_pair'):
#             data_dict[k] = v

#     return data_dict

#<=====>#


# @narc(1)
# def pair_print(self):
#     if self.debug_tf: B(f'pair_base.pair_print() ==> {self.prod_id}')
#     """Print formatted PAIR data attributes"""
#     data = self.pair_to_dict()
#     print('')
#     C(f"========== PAIR Data for {self.prod_id:^12} ==========")
#     print('')
#     for key, value in data.items():
#         print(key, ' : ', value)
#         # print(f'{key:<25}: {type(value):<15} {value:<}')
#     C(f"{'=' * 50}")
#     print('')

#<=====>#
# Functions
#<=====>#



#<=====>#


