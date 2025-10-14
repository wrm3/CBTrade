#<=====>#
# Description
#<=====>#



#<=====>#
# To Do List
#<=====>#



#<=====>#
# Variables
#<=====>#
lib_name      = 'mkt_base'
log_name      = 'mkt_base'


#<=====>#
# Imports - Public
#<=====>#
import sys
import time
import traceback

from datetime import (
    datetime as dt
    , timezone
)
from decimal import Decimal
from fstrent_colors import *
from pprint import pprint
from typing import Dict, List, Optional, Any, TypeAlias

#<=====>#
# Imports - Project
#<=====>#
from libs.common import (
    AttrDict
    , AttrDictEnh
    , beep
    , print_adv
    , fatal_error_exit
    , dttm_get
    , dttm_unix
    , print_adv
    , format_disp_age2
    , get_unix_timestamp
    , speak
    , speak_async
    , narc
)
from libs.trade_strat_perfs_base import trade_strat_perfs_get_all
from libs.coinbase_handler import cb
from libs.reports_base import report_sells_recent
from libs.strat_base import buy_strats_get
from libs.theme import *

#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#


@narc(1)
def mkt_new(self, mkt_symb:str):
    if self.debug_tf: G(f'==> mkt_base.mkt_new()')
    self.mkt                           = AttrDict()

#    self.mkt.class_name                = 'MARKET'
    self.mkt.symb                      = mkt_symb
    self.mkt.fpath                     = self.st_bot.trade_markets[mkt_symb].settings_fpath

    self.st_debug                      = self.debug_settings_get()
    self.st_bot                        = self.bot_settings_get()
    self.st_mkt                        = self.mkt_settings_get(mkt_symb=mkt_symb)

    self.mkt.buy_strats                = self.buy_strats_get()

    self.budget_new(mkt_symb=mkt_symb)

    self.mkt.refresh_wallet_tf         = True

    self.wallet_refresh(force_tf=True)

    self.budget_refresh()

    self.budget_reserves_calc()

#<=====>#


@narc(1)
def mkt_pairs_list_get(self):
    if self.debug_tf: G(f'==> mkt_base.mkt_pairs_list_get()')
    """🔴 CONFIGURATION - Extracted from cls_bot.py (~25 lines)

    Orchestrate market pair selection for trading

    HIGH RISK: Controls which pairs are traded
    - Manages buy and sell pair selection
    - Handles different trading modes
    - Applies final database filtering
    - Determines trading scope
    """
    self.mkt.loop_pairs       = []
    self.mkt.buy_pairs        = []
    self.mkt.sell_pairs       = []

    if self.mode in ('buy', 'full'):
        self.mkt.buy_pairs = self.mkt_pairs_list_buy_get()
        self.mkt.loop_pairs.extend(self.mkt.buy_pairs)
        # Buy pairs added to loop - run silently during normal operation
        self.mkt.loop_pairs = list(set(self.mkt.loop_pairs))
        # Duplicates removed from loop pairs - run silently during normal operation
        hmsg = f'buy self.mkts ({len(self.mkt.buy_pairs)}) :'
        self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
        prt_cols(self.mkt.buy_pairs, cols=10)
        self.chrt.chart_bottom(len_cnt=260)
        print_adv()

    if self.mode in ('sell', 'full'):
        self.mkt.sell_pairs = self.mkt_pairs_list_sell_get()
        self.mkt.loop_pairs.extend(self.mkt.sell_pairs)
        # Sell pairs added to loop - run silently during normal operation
        self.mkt.loop_pairs = list(set(self.mkt.loop_pairs))
        # Duplicates removed from loop pairs - run silently during normal operation
        hmsg = f'sell self.mkts ({len(self.mkt.sell_pairs)}) :'
        self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
        prt_cols(self.mkt.sell_pairs, cols=10)
        self.chrt.chart_bottom(len_cnt=260)
        print_adv()

    stable_pairs         = self.st_mkt.pairs.stable_pairs
    err_pairs            = self.st_mkt.pairs.err_pairs
    ban_pairs            = self.st_mkt.pairs.ban_pairs
    hell_no_pairs        = err_pairs + ban_pairs
    if self.mkt.loop_pairs:
        pairs_before_db_filter = len(self.mkt.loop_pairs)
        self.mkts                 = self.cbtrade_db.db_pairs_loop_get(mode=self.mode, loop_pairs=self.mkt.loop_pairs, stable_pairs=stable_pairs, err_pairs=hell_no_pairs)
    else:
        self.mkts                 = []

    self.mkt.loop_pairs = self.mkts

#<=====>#


@narc(1)
def mkt_pairs_list_buy_get(self):
    if self.debug_tf: G(f'==> mkt_base.mkt_pairs_list_buy_get()')
    buy_pairs = []

    print_adv(2)
    self.chrt.chart_top(in_str='Buy Market Collection', len_cnt=260)

    if self.st_mkt.pairs.extra_pairs.vol_quote_24h.use_yn == 'Y':
        min_volume = self.st_mkt.pairs.extra_pairs.vol_quote_24h.min_volume
    else:
        min_volume = None

    # get self.mkts from settings
    spot_pairs  = self.st_mkt.pairs.trade_pairs
    if spot_pairs:
        self.mkts = list(set(spot_pairs))
        buy_pairs.extend(self.mkts)

    # Get The Markets with the best performance on the bot so far
    # By Gain Loss Percen Per Hour
    # Settings how many of these we will look at
    hmsg = 'self.mkts top bot gain loss percent per day performers'
    self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
    pct_min = self.st_mkt.pairs.extra_pairs.top_bot_perf.pct_min
    lmt_cnt = self.st_mkt.pairs.extra_pairs.top_bot_perf.cnt

    self.mkts = self.cbtrade_db.db_pairs_loop_top_perfs_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min, quote_curr_symb=self.mkt_symb)
    print(f'self.mkts ({type(self.mkts)}) ({len(self.mkts) if self.mkts else 0}): {self.mkts}')
    if self.mkts:
        if self.st_mkt.pairs.extra_pairs.top_bot_perf.use_yn == 'Y':
            hmsg = f'adding self.mkts top bot gain loss percent per day performers ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='WoG')
            buy_pairs.extend(self.mkts)
        elif self.st_mkt.pairs.extra_pairs.top_bot_perf.cnt > 0:
            hmsg = f'skipping self.mkts top bot gain loss percent per day performers ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='GoW')

    # Get The Markets with the best performance on the bot so far
    # By Gain Loss Amount Total
    # Settings how many of these we will look at
    hmsg = 'self.mkts top bot gain loss amount total performers'
    self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
    lmt_cnt = self.st_mkt.pairs.extra_pairs.top_bot_gains.cnt
    gain_min = self.st_mkt.pairs.extra_pairs.top_bot_gains.gain_min
    self.mkts = self.cbtrade_db.db_pairs_loop_top_gains_prod_ids_get(lmt=lmt_cnt, gain_min=gain_min, quote_curr_symb=self.mkt_symb)
    print(f'self.mkts ({type(self.mkts)}) ({len(self.mkts) if self.mkts else 0}): {self.mkts}')
    if self.mkts:
        if self.st_mkt.pairs.extra_pairs.top_bot_gains.use_yn == 'Y':
            hmsg = f'adding self.mkts top bot gain loss performers ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='WoG')
            buy_pairs.extend(self.mkts)
        elif self.st_mkt.pairs.extra_pairs.top_bot_gains.cnt > 0:
            hmsg = f'skipping self.mkts top bot gain loss performers ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='GoW')
 
    # Get The Markets with the top 24h price increase
    # Settings how many of these we will look at
    hmsg = 'self.mkts top 24h price increase'
    self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
    pct_min = self.st_mkt.pairs.extra_pairs.prc_pct_chg_24h.pct_min
    lmt_cnt = self.st_mkt.pairs.extra_pairs.prc_pct_chg_24h.cnt
    self.mkts = self.cbtrade_db.db_pairs_loop_top_prc_chg_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min, quote_curr_symb=self.mkt_symb, min_volume=min_volume)
    print(f'self.mkts ({type(self.mkts)}) ({len(self.mkts)}): {self.mkts}')
    if self.mkts:
        if self.st_mkt.pairs.extra_pairs.prc_pct_chg_24h.use_yn == 'Y':
            hmsg = f'adding self.mkts top price increases ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='WoG')
            buy_pairs.extend(self.mkts)
        elif self.st_mkt.pairs.extra_pairs.prc_pct_chg_24h.cnt > 0:
            hmsg = f'skipping self.mkts top price increases ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='GoW')

    # Get The Markets with the top 24h volume percent increase
    # Settings how many of these we will look at
    hmsg = 'self.mkts top 24h volume percent increase'
    self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
    lmt_cnt = self.st_mkt.pairs.extra_pairs.vol_pct_chg_24h.cnt
    self.mkts = self.cbtrade_db.db_pairs_loop_top_vol_chg_pct_prod_ids_get(lmt=lmt_cnt, quote_curr_symb=self.mkt_symb, min_volume=min_volume)
    print(f'self.mkts ({type(self.mkts)}) ({len(self.mkts)}): {self.mkts}')
    if self.mkts:
        if self.st_mkt.pairs.extra_pairs.vol_pct_chg_24h.use_yn == 'Y':
            hmsg = f'adding self.mkts highest volume increase ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='WoG')
            buy_pairs.extend(self.mkts)
        elif self.st_mkt.pairs.extra_pairs.vol_pct_chg_24h.cnt > 0:
            hmsg = f'skipping self.mkts highest volume increase ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='GoW')

    # Get The Markets that are marked as favorites on Coinbase
    hmsg = 'self.mkts watched markets'
    self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
    self.mkts = self.cbtrade_db.db_pairs_loop_watched_prod_ids_get(quote_curr_symb=self.mkt_symb)
    print(f'self.mkts ({type(self.mkts)}) ({len(self.mkts)}): {self.mkts}')
    if self.mkts:
        if self.st_mkt.pairs.extra_pairs.watched.use_yn == 'Y':
            hmsg = f'adding watched markets ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='WoG')
            buy_pairs.extend(self.mkts)
        else:
            hmsg = f'skipping watched markets ({len(self.mkts)}) :'
            self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
            prt_cols(self.mkts, cols=10, clr='GoW')

    # Also include markets with OPEN buy orders
    hmsg = 'self.mkts with OPEN buy orders'
    self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
    try:
        _open_bos = self.cbtrade_db.db_buy_ords_open_get()
    except Exception:
        _open_bos = []
    try:
        open_pairs = [
            (x.get('prod_id') if hasattr(x, 'get') else getattr(x, 'prod_id', None))
            for x in (_open_bos or [])
        ]
        open_pairs = [p for p in open_pairs if p]
    except Exception:
        open_pairs = []
    print(f'open_pairs ({type(open_pairs)}) ({len(open_pairs) if open_pairs else 0}): {open_pairs}')
    if open_pairs:
        self.chrt.chart_mid(in_str=f'adding markets from OPEN buy orders ({len(open_pairs)}) :', len_cnt=260)
        prt_cols(open_pairs, cols=10, clr='WoG')
        buy_pairs.extend(open_pairs)

    err_pairs            = self.st_mkt.pairs.err_pairs
    if buy_pairs:
        buy_pairs = [pair for pair in buy_pairs if pair not in err_pairs]

    return buy_pairs

#<=====>#


@narc(1)
def mkt_pairs_list_sell_get(self):
    if self.debug_tf: G(f'==> mkt_base.mkt_pairs_list_sell_get()')
    """🔴 CONFIGURATION - Extracted from cls_bot.py (~15 lines)
    
    Select trading pairs for sell operations
    
    MEDIUM RISK: Controls which pairs need sell processing
    - Gets pairs with open positions
    - Ensures all open positions are monitored
    - Critical for position management
    """
    self.chrt.chart_top(in_str='Sell Market Collection', len_cnt=260)

    sell_pairs = []

    # Get The Markets with Open Positions
    # They all need to be looped through buy/sell logic
    pairs = self.cbtrade_db.db_pairs_loop_poss_open_prod_ids_get(quote_curr_symb=self.mkt_symb)

    if pairs:
        pairs = list(set(pairs))
        hmsg = f'adding markets with open positions ({len(pairs)}) :'
        self.chrt.chart_mid(in_str=hmsg, len_cnt=260)
        prt_cols(pairs, cols=10)

        sell_pairs.extend(pairs)

    return sell_pairs

#<=====>#


@narc(1)
def mkt_main(self):
    if self.debug_tf: G(f'==> mkt_base.mkt_main()')
    """
    This method processes individual markets and calls mkt_pairs_loop().
    Part of the suspected 1200+ second performance bottleneck chain.
    """

    if self.mode in ('buy'):
        self.wallet_refresh()
        self.mkt_pairs_loop()
    elif self.mode in ('sell'):
        self.wallet_refresh()
        self.mkt_pairs_loop()
    else:
        self.wallet_refresh()
        self.mkt_pairs_loop()

    # self.budget.print()
    print_adv(3)


#<=====>#


@narc(1)
def mkt_pairs_loop(self):
    if self.debug_tf: G(f'==> mkt_base.mkt_pairs_loop()')
    pairs_loop_start = time.perf_counter()

    self.wallet_refresh()

    t = f'Markets Loop : {self.mkt_symb}'
    # if self.mode == 'buy':
    #     if self.budget.spent_amt >= self.budget.spend_max_amt:
    #         msg = cs(f'We have spent our entire {self.mkt_symb} budget... spent : {self.budget.spent_amt} / {self.budget.spend_max_amt} max...', 'white', 'red')
    #         print(msg)
    #         self.disp_mkt_budget(budget=self.mkt_budget, title=t, footer=msg)
    #         report_sells_recent(cnt=20)
    #         time.sleep(30)
    #         # 🚨 TRADING SYSTEM: Budget exhausted but continue monitoring for sells/position management
    #         print(f"💰 BUDGET EXHAUSTED: {self.mkt_symb} spending limit reached - continuing monitoring mode")
    #         # DON'T RETURN - keep running for position management and sells
    #     else:
    #         msg = cs(f'We have more {self.mkt_symb} budget to spend... spent : {self.budget.spent_amt} / {self.budget.spend_max_amt} max...', 'white', 'red')
    #         print(msg)
    #         self.disp_mkt_budget(budget=self.mkt_budget, title=t, footer=msg)

    cnt = 0
    # loop through all self.mkts for buy/sell logic

    self.mkt_pairs_list_get()

    loop_pairs_sorted = sorted(self.mkt.loop_pairs, key=lambda x: x['gain_loss_pct_hr'], reverse=True)
    self.mkt.loop_pairs = loop_pairs_sorted

    self.mkt.dttm_start_loop = dttm_get()
    self.mkt.start_loop_dttm = dt.now(timezone.utc)

    self.mkt.start_loop_unix = get_unix_timestamp()
    self.mkt.t_loop = time.perf_counter()

    total_pairs = len(self.mkt.loop_pairs) if hasattr(self, 'loop_pairs') else 0
    
    pair_processing_start = time.perf_counter()
    for pair_dict in self.mkt.loop_pairs:
        pair_start = time.perf_counter()

        cnt += 1
        self.mkt.cnt = cnt
        pair_dict = AttrDict(pair_dict)
        self.prod_id = pair_dict.prod_id

        # if self.st_mkt.speak_pairs:
        #     if self.prod_id in self.st_mkt.speak_pairs:
        #        speak_async(f'Now processing {self.prod_id} pair...')

        self.mkt.t_now = time.perf_counter()
        self.mkt.t_elapse = self.mkt.t_now - self.mkt.t_loop
        self.mkt.loop_age = format_disp_age2(self.mkt.t_elapse)

        self.disp_upcoming_pairs()

        prod_id = pair_dict.prod_id
        self.pair_new(pair_dict=pair_dict)
        self.pair_main()

        pair_end = time.perf_counter()
        pair_time = round(pair_end - pair_start, 2)
        
        if pair_time > 30:  # If a single pair takes more than 30 seconds
            WoB(f'🔴 PAIR WARNING: {self.prod_id} took {pair_time}s (>30s)')

        # sys.exit()

    pair_processing_end = time.perf_counter()
    pair_processing_time = round(pair_processing_end - pair_processing_start, 2)
    
    avg_pair_time = round(pair_processing_time / total_pairs, 2) if total_pairs > 0 else 0
    WoB(f'🔴 PERFORMANCE: {total_pairs} pairs in {pair_processing_time}s (avg: {avg_pair_time}s/pair)')

    t = f'Markets Loop : {self.mkt_symb}'

    if self.mode == 'buy':
        if self.budget.spent_amt >= self.budget.spend_max_amt:
            msg = cs(f'We have spent our entire {self.mkt_symb} budget... spent : {self.budget.spent_amt} / {self.budget.spend_max_amt} max...', 'white', 'red')
        else:
            msg = cs(f'We have more {self.mkt_symb} budget to spend... spent : {self.budget.spent_amt} / {self.budget.spend_max_amt} max...', 'white', 'red')
        print(msg)
        self.disp_mkt_budget(budget=self.mkt_budget, title=t, footer=msg)

        # if self.budget.spent_amt >= self.budget.spend_max_amt:
        #     report_sells_recent(cnt=20)
        #     time.sleep(30)
        #     # 🚨 TRADING SYSTEM: Budget exhausted - continue monitoring instead of silent exit
        #     print(f"💰 END-OF-LOOP BUDGET CHECK: {self.mkt_symb} spending limit reached - continuing for position management")
        #     # DON'T RETURN - keep the 24/7 system running

    pairs_loop_end = time.perf_counter()
    pairs_loop_total = round(pairs_loop_end - pairs_loop_start, 2)
    
    # 🔴 PERFORMANCE CRITICAL: Report total pairs loop time
    if pairs_loop_total > 120:  # If pairs loop takes more than 2 minutes
        WoB(f'🔴 GILFOYLE PAIRS LOOP WARNING: {self.mkt_symb} pairs loop took {pairs_loop_total}s (>120s)')

#<=====>#


@narc(1)
def disp_upcoming_pairs(self):
    if self.debug_tf: G(f'==> mkt_base.disp_upcoming_pairs()')
    """🔴 CONFIGURATION - Extracted from cls_bot.py (~25 lines)
    
    Display upcoming trading pairs in terminal
    
    LOW RISK: Display utility for user interface
    - Shows upcoming pairs in formatted display
    - Respects show_upcoming_yn setting
    - Integrates with chart system for output
    """
    if self.st_mkt.show_upcoming_yn == 'Y':
        # List the order of the upcoming pairs
        # print(self.mkt.loop_pairs)
        print_adv(2)
        chrt.chart_top(in_str='Upcoming Pairs', len_cnt=260)
        self.mkt.loop_pairs_list = []
        not_yet = True
        for pd in self.mkt.loop_pairs:
            pd = AttrDict(pd)
            if not_yet:
                if pd.prod_id == self.prod_id:
                    self.mkt.loop_pairs_list.append(pd.prod_id)
                    not_yet = False
            else:
                self.mkt.loop_pairs_list.append(pd.prod_id)
                # break
        temp_str = ''
        true_len = 0
        for prod in self.mkt.loop_pairs_list:
            if true_len + len(prod) + 2 > 248:
                chrt.chart_row(in_str=temp_str, len_cnt=260)
                temp_str = ''
                true_len = 0
            else:
                temp_str += cs(f'{prod}', font_color='green') + ', '
                true_len += len(prod) + 2
        if len(temp_str) > 0:
            temp_str = temp_str[:-2]
            chrt.chart_row(in_str=temp_str, len_cnt=260)
        # self.prt_cols(l=self.mkt.loop_pairs_list, cols=12, clr='WoG')
        chrt.chart_bottom(len_cnt=260)
        print_adv(1)

#<=====>#


@narc(1)
def update_pricing_data(self, price_data: Dict[str, Decimal]):
    if self.debug_tf: G(f'==> mkt_base.update_pricing_data()')
    """
    Update market pricing data from API response.
    
    Args:
        price_data: Dictionary containing price information
    """
    self.prc = price_data.get('prc', self.prc)
    self.prc_ask = price_data.get('prc_ask', self.prc_ask)
    self.prc_buy = price_data.get('prc_buy', self.prc_buy)
    self.prc_bid = price_data.get('prc_bid', self.prc_bid)
    self.prc_sell = price_data.get('prc_sell', self.prc_sell)
    self.prc_mid_mkt = price_data.get('prc_mid_mkt', self.prc_mid_mkt)
    self.prc_pct_chg_24h = price_data.get('prc_pct_chg_24h', self.prc_pct_chg_24h)
    
    # Update cache and timestamp
    self.price_cache.update(price_data)
    self.price_last_update = dttm_unix()

#<=====>#


@narc(1)
def update_market_status(self, status_data: Dict[str, Any]):
    if self.debug_tf: G(f'==> mkt_base.update_market_status()')
    """
    Update market status flags from API response.
    
    Args:
        status_data: Dictionary containing market status information
    """
    self.mkt_status_tf = status_data.get('mkt_status_tf', self.mkt_status_tf)
    self.mkt_view_only_tf = status_data.get('mkt_view_only_tf', self.mkt_view_only_tf)
    self.mkt_watched_tf = status_data.get('mkt_watched_tf', self.mkt_watched_tf)
    self.mkt_is_disabled_tf = status_data.get('mkt_is_disabled_tf', self.mkt_is_disabled_tf)
    self.mkt_new_tf = status_data.get('mkt_new_tf', self.mkt_new_tf)
    self.mkt_cancel_only_tf = status_data.get('mkt_cancel_only_tf', self.mkt_cancel_only_tf)
    self.mkt_limit_only_tf = status_data.get('mkt_limit_only_tf', self.mkt_limit_only_tf)
    self.mkt_post_only_tf = status_data.get('mkt_post_only_tf', self.mkt_post_only_tf)
    self.mkt_trading_disabled_tf = status_data.get('mkt_trading_disabled_tf', self.mkt_trading_disabled_tf)
    self.mkt_auction_mode_tf = status_data.get('mkt_auction_mode_tf', self.mkt_auction_mode_tf)
    
    # Update cache and timestamp
    self.status_cache.update(status_data)
    self.status_last_update = dt.utcnow()

#<=====>#


@narc(1)
def is_trading_enabled(self) -> bool:
    if self.debug_tf: G(f'==> mkt_base.is_trading_enabled()')
    """
    Check if trading is currently enabled for this market.
    
    Returns:
        bool: True if trading is enabled, False otherwise
    """
    return (
        not self.mkt_is_disabled_tf and
        not self.mkt_trading_disabled_tf and
        not self.mkt_cancel_only_tf and
        self.mkt_status_tf.upper() in ['ONLINE', 'ACTIVE']
    )

#<=====>#


@narc(1)
def calculate_spread_percentage(self) -> float:
    if self.debug_tf: G(f'==> mkt_base.calculate_spread_percentage()')
    """
    Calculate the current bid-ask spread percentage.
    
    Returns:
        float: Spread percentage (0.0 to 100.0)
    """
    if self.prc_ask > 0 and self.prc_bid > 0:
        spread = float(self.prc_ask - self.prc_bid)
        mid_price = float(self.prc_ask + self.prc_bid) / 2
        if mid_price > 0:
            self.spread_percentage = (spread / mid_price) * 100
            return self.spread_percentage
    return 0.0

#<=====>#


@narc(1)
def get_all_product_ids(self):
    if self.debug_tf: G(f'==> mkt_base.get_all_product_ids()')
    """🔴 CONFIGURATION - Extracted from cls_bot.py (~8 lines)
    
    Get all product IDs from all markets
    
    LOW RISK: Simple data aggregation utility
    - Collects product IDs from market loop pairs
    - Removes duplicates and returns clean list
    - Used by OHLCV table management
    """
    prod_ids = []
    if self.mkt.loop_pairs:  # Check if loop_pairs exists and is not None/empty
        for m in self.mkt.loop_pairs:
            prod_id = m['prod_id']
            if prod_id not in prod_ids:
                prod_ids.append(prod_id)
    return prod_ids

#<=====>#

# def to_dict(self):
#     """Override to_dict for bot-specific attributes"""

#     simple_types = (int, float, str, list, dict, tuple, bool, AttrDict)
#     data_dict = AttrDict()

#     for k, v in self.items():
#         # print(f'k: {k}, {type(v)} v: {v}')
#         if isinstance(v, simple_types):
#             data_dict[k] = v

#     return data_dict

#<=====>#

# def print(self):
#     """Print formatted PAIR data attributes"""
    
#     data = self.to_dict()
    
#     print('')
#     C(f"========== MKT Data ==========")
#     print('')
    
#     for key, value in data.items():
#         print(f'{key:<25}: {type(value):<15} {value:<}')

#     C(f"{'=' * 50}")
#     print('')

#<=====>#

