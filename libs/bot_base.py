# #<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports - Public
#<=====>#
import os
import sys
import time
import traceback
import uuid
from fstrent_colors import *
from pprint import pprint
from typing import Dict, List, Optional, Any, TypeAlias

#<=====>#
# Imports - Project
#<=====>#
from libs.common import (
    AttrDict
    , AttrDictEnh
    , calc_chg_pct
    , conv_utc_timestamp_to_unix
    , dec_2_float
    , speak
    , print_adv
    , narc
)
from libs.db_mysql.cbtrade.db_main import CBTRADE_DB
from libs.db_mysql.ohlcv.db_main import OHLCV_DB  # MySQL-only OHLCV
from libs.coinbase_handler import cb

from libs.mkt_base import *
from libs.budget_base import *
from libs.pair_base import *
from libs.buy_base import *
from libs.sell_base import *
from libs.reports_base import *
from libs.settings_base import *
from libs.strat_base import *
from libs.ta_base import *
from libs.theme import *
from libs.trade_perfs_base import *
from libs.trade_strat_perfs_base import *

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_base'
log_name      = 'bot_base'

# <=====>#
# Assignments Pre
# <=====>#
debug_tf = False

#<=====>#
# Classes
#<=====>#

class BOT(AttrDict):
    """
    Cryptocurrency Trading Bot Class
    """

    # budget_base.py
    budget_new                                             = budget_new
    budget_refresh                                         = budget_refresh
    budget_reserves_calc                                   = budget_reserves_calc
    wallet_refresh                                         = wallet_refresh
    disp_budget                                            = disp_budget
    disp_budgetX                                           = disp_budgetX
    disp_mkt_budget                                        = disp_mkt_budget

    # buy_base.py
    buy_strats_build                                       = buy_strats_build
    disp_buy_header                                        = disp_buy_header
    disp_buy                                               = disp_buy
    disp_buy_passes                                        = disp_buy_passes
    disp_buy_fails                                         = disp_buy_fails
    disp_buy_boosts                                        = disp_buy_boosts
    disp_buy_limits                                        = disp_buy_limits
    disp_buy_denies                                        = disp_buy_denies
    disp_buy_cancels                                       = disp_buy_cancels
    disp_buy_maxes                                         = disp_buy_maxes
    disp_buy_test_reasons                                  = disp_buy_test_reasons
    disp_buy_live_or_test                                  = disp_buy_live_or_test
    buy_new                                                = buy_new
    buy_decision_log                                       = buy_decision_log
    set_test_mode                                          = set_test_mode
    set_deny_mode                                          = set_deny_mode
    buy_main                                               = buy_main
    buy_logic_mkt_boosts                                   = buy_logic_mkt_boosts
    buy_logic_strat_boosts                                 = buy_logic_strat_boosts
    buy_logic_strat_boosts_position_max                    = buy_logic_strat_boosts_position_max
    buy_logic_strat_boosts_trade_size                      = buy_logic_strat_boosts_trade_size
    buy_logic_deny                                         = buy_logic_deny
    buy_logic_mkt_deny                                     = buy_logic_mkt_deny
    buy_logic_strat_deny                                   = buy_logic_strat_deny
    buy_logic_strat_deny_buying_on                         = buy_logic_strat_deny_buying_on
    buy_logic_strat_deny_force_sell                        = buy_logic_strat_deny_force_sell
    buy_logic_strat_deny_live                              = buy_logic_strat_deny_live
    buy_logic_strat_deny_live_paper_trades_mode            = buy_logic_strat_deny_live_paper_trades_mode
    buy_logic_strat_deny_live_test_mode_switch             = buy_logic_strat_deny_live_test_mode_switch
    buy_logic_strat_deny_live_market_open_position_limit   = buy_logic_strat_deny_live_market_open_position_limit
    buy_logic_strat_deny_live_strategy_open_position_limit = buy_logic_strat_deny_live_strategy_open_position_limit
    buy_logic_strat_deny_live_product_open_position_limit  = buy_logic_strat_deny_live_product_open_position_limit
    buy_logic_strat_deny_live_product_timing_delay         = buy_logic_strat_deny_live_product_timing_delay
    buy_logic_strat_deny_live_strategy_timing_delay        = buy_logic_strat_deny_live_strategy_timing_delay
    buy_logic_strat_deny_live_budget_pair_spending_limit   = buy_logic_strat_deny_live_budget_pair_spending_limit
    buy_logic_strat_deny_live_market_limit_only            = buy_logic_strat_deny_live_market_limit_only
    buy_logic_strat_deny_live_large_bid_ask_spread         = buy_logic_strat_deny_live_large_bid_ask_spread
    buy_logic_strat_deny_test                              = buy_logic_strat_deny_test
    buy_logic_strat_deny_test_strategy_open_position_limit = buy_logic_strat_deny_test_strategy_open_position_limit
    buy_logic_strat_deny_test_product_timing_delay         = buy_logic_strat_deny_test_product_timing_delay
    buy_logic_strat_deny_test_strategy_timing_delay        = buy_logic_strat_deny_test_strategy_timing_delay
    buy_logic_strat_deny_test_large_bid_ask_spread         = buy_logic_strat_deny_test_large_bid_ask_spread
    cb_buy_base_size_calc                                  = cb_buy_base_size_calc
    buy_size_budget_calc                                   = buy_size_budget_calc
    buy_save                                               = buy_save
    buy_live                                               = buy_live
    buy_test                                               = buy_test

    # mkt_base.py
    mkt_new                                                = mkt_new
    mkt_main                                               = mkt_main
    mkt_pairs_loop                                         = mkt_pairs_loop
    mkt_pairs_list_get                                     = mkt_pairs_list_get
    mkt_pairs_list_buy_get                                 = mkt_pairs_list_buy_get
    mkt_pairs_list_sell_get                                = mkt_pairs_list_sell_get
    disp_upcoming_pairs                                    = disp_upcoming_pairs
    update_pricing_data                                    = update_pricing_data
    update_market_status                                   = update_market_status
    is_trading_enabled                                     = is_trading_enabled
    calculate_spread_percentage                            = calculate_spread_percentage
    get_all_product_ids                                    = get_all_product_ids

    # pair_base.py
    pair_new                                               = pair_new
    pair_main                                              = pair_main
    pair_timing_check                                      = pair_timing_check
    verify_bot_lock                                        = verify_bot_lock
    pair_init                                              = pair_init
    pair_build                                             = pair_build
    pair_logic                                             = pair_logic
    pair_logic_buy                                         = pair_logic_buy
    pair_logic_sell                                        = pair_logic_sell
    disp_pair_header                                       = disp_pair_header
    disp_pair                                              = disp_pair
    disp_pair_summary                                      = disp_pair_summary
    disp_sell_performance_summary                          = disp_sell_performance_summary
    disp_pair_stats                                        = disp_pair_stats
    disp_pair_ta_stats                                     = disp_pair_ta_stats
    disp_pair_performance                                  = disp_pair_performance
    # display_strat_perf_summary                             = display_strat_perf_summary
    # pair_to_dict                                           = pair_to_dict
    # pair_print                                             = pair_print

    # sell_base.py
    sell_logic                                             = sell_logic
    sell_pos_new                                           = sell_pos_new
    sell_pos_logic                                         = sell_pos_logic
    sell_pos_blocks                                        = sell_pos_blocks
    sell_pos_forces                                        = sell_pos_forces
    sell_pos_tests_before_ta                               = sell_pos_tests_before_ta
    sell_pos_tests_after_ta                                = sell_pos_tests_after_ta
    sell_pos_test_hard_profit                              = sell_pos_test_hard_profit
    sell_pos_test_hard_stop                                = sell_pos_test_hard_stop
    sell_pos_test_trailing_profit                          = sell_pos_test_trailing_profit
    sell_pos_test_trailing_stop                            = sell_pos_test_trailing_stop
    sell_pos_test_nwe_exit                                 = sell_pos_test_nwe_exit
    sell_pos_test_atr_stop                                 = sell_pos_test_atr_stop
    sell_pos_test_trailing_atr_stop                        = sell_pos_test_trailing_atr_stop
    sell_pos_deny_all_green                                = sell_pos_deny_all_green
    sell_pos_deny_nwe_green                                = sell_pos_deny_nwe_green
    sell_pos_save                                          = sell_pos_save
    sell_pos_live                                          = sell_pos_live
    sell_pos_test                                          = sell_pos_test
    # sell_strats_check_optimized                            = sell_strats_check_optimized
    disp_sell_header                                       = disp_sell_header
    disp_sell_pos                                          = disp_sell_pos
    disp_sell_pos_forces                                   = disp_sell_pos_forces
    disp_sell_pos_blocks                                   = disp_sell_pos_blocks
    disp_sell_pos_sells                                    = disp_sell_pos_sells
    disp_sell_pos_hodls                                    = disp_sell_pos_hodls
    sell_pos_stats_calc                                    = sell_pos_stats_calc
    disp_sell_pos_test_details                             = disp_sell_pos_test_details
    # disp_sell_pos_test_details2                            = disp_sell_pos_test_details2
    # display_strategy_performance_summary                   = display_strategy_performance_summary

    # settings_base.py
    debug_settings_get                                     = debug_settings_get
    bot_settings_get                                       = bot_settings_get
    mkt_settings_get                                       = mkt_settings_get
    pair_settings_get                                      = pair_settings_get

    # strat_base.py
    buy_strats_get                                         = buy_strats_get
    strat_settings_get                                     = strat_settings_get
    buy_strats_avail_get                                   = buy_strats_avail_get
    buy_strats_check                                       = buy_strats_check
    buy_strats_deny                                        = buy_strats_deny
    sell_strats_check                                      = sell_strats_check

    # ta_base.py
    ta_main_new                                            = ta_main_new

    # trade_perfs_base.py
    trade_perfs_get                                        = trade_perfs_get
    trade_perfs_get_by_prod_id                             = trade_perfs_get_by_prod_id
    pair_trade_perf_buy_upd                                = pair_trade_perf_buy_upd
    pair_trade_perf_sell_upd                               = pair_trade_perf_sell_upd

    # trade_strat_perfs_base.py
    trade_strat_perfs_get_all                              = trade_strat_perfs_get_all
    pair_trade_strat_perf_sell_upd                         = pair_trade_strat_perf_sell_upd
    pair_trade_strat_perf_buy_upd                          = pair_trade_strat_perf_buy_upd
    pair_trade_strat_perf_sell_upd                         = pair_trade_strat_perf_sell_upd

    def __init__(self, mode='full'):
        self.debug_tf = debug_tf
        if self.debug_tf: C(f'==> bot_base.__init__()')
        self.bot_guid                  = self.gen_guid()
        self.cbtrade_db                = CBTRADE_DB()
        # self.ohlcv_db                  = OHLCV_DB()
        self.cb                        = cb

        self.mode                      = mode
        self.fnc_secs_max              = 0.33
        self.budget                    = AttrDict()
        self.mkt                       = AttrDict()
        self.pair                      = AttrDict()
        self.buy                       = AttrDict()
        self.pos                       = AttrDict()
        self.sell                      = AttrDict()
        self.chrt                      = chrt
        self.spacer                    = ' '  * 4
        self.st_debug                  = self.debug_settings_get()
        self.st_bot                    = self.bot_settings_get()
        self.chrt                      = chrt

        self.buy_strats_build()

    #<=====>#

    @narc(1)
    def gen_guid(self):
        if self.debug_tf: G(f'==> bot_base.gen_guid()')
        """Generate a unique GUID for BOT instance identification."""
        return str(uuid.uuid4())

    #<=====>#

    @narc(1)
    def compute_quote_balances_summary(self, currencies: List[str] | None = None):
        """
        Build per-quote-currency balance/allocations summary for USDC/BTC/ETH/SOL.

        For each currency C in currencies:
        - balance: bals.bal_tot where symb=C
        - usd_price: bals.curr_prc_usd (kept fresh via db_bals_prc_mkt_upd)
        - open holds of C by quote: sum(hold_cnt) from poss where pos_stat='OPEN' and buy_curr_symb=C grouped by quote_curr_symb
        - closed holds of C by quote: sum(hold_cnt) from poss where pos_stat='CLOSE' and buy_curr_symb=C grouped by quote_curr_symb
        - available_balance = balance - sum_open_holds - sum_closed_holds
        - usd valuations computed via usd_price
        """
        if currencies is None:
            currencies = ['USDC', 'BTC', 'ETH', 'SOL']

        # Ensure balances have USD pricing populated from markets (USDC-quoted)
        try:
            self.cbtrade_db.db_bals_prc_mkt_upd()
        except Exception:
            pass

        # Pull balances and USD prices
        cur_list = ",".join([f"'{c}'" for c in currencies])
        bal_sql = f"""
            select symb, coalesce(bal_tot,0) as bal_tot, coalesce(curr_prc_usd,0) as curr_prc_usd
              from bals 
             where symb in ({cur_list})
        """
        bals_rows = self.cbtrade_db.sel(bal_sql) if hasattr(self.cbtrade_db, 'sel') else self.cbtrade_db.seld(bal_sql)
        # Normalize rows into a list of dicts
        if isinstance(bals_rows, dict):
            bals_rows = [bals_rows]
        if isinstance(bals_rows, list) and bals_rows and not isinstance(bals_rows[0], dict):
            try:
                bals_rows = [
                    {'symb': r[0], 'bal_tot': r[1], 'curr_prc_usd': r[2]}
                    for r in bals_rows
                ]
            except Exception:
                bals_rows = []
        if not isinstance(bals_rows, list):
            bals_rows = []
        bal_map = {r.get('symb'): (float(r.get('bal_tot', 0) or 0), float(r.get('curr_prc_usd', 0) or 0)) for r in bals_rows}

        # Helper to fetch grouped sums for a given pos_stat
        def fetch_grouped_holds(pos_stat: str):
            data: Dict[str, Dict[str, float]] = {c: {q: 0.0 for q in currencies} for c in currencies}
            for c in currencies:
                sql = ""
                sql += "select quote_curr_symb as quote, coalesce(sum(hold_cnt),0) as cnt\n"
                sql += "  from poss\n"
                sql += " where ignore_tf = 0\n"
                sql += f"   and pos_stat = '{pos_stat}'\n"
                sql += f"   and buy_curr_symb = '{c}'\n"
                sql += f"   and quote_curr_symb in ({cur_list})\n"
                sql += " group by quote_curr_symb"
                rows = self.cbtrade_db.sel(sql) if hasattr(self.cbtrade_db, 'sel') else self.cbtrade_db.seld(sql)
                if isinstance(rows, dict):
                    rows = [rows]
                if isinstance(rows, list) and rows and not isinstance(rows[0], dict):
                    try:
                        rows = [{'quote': r[0], 'cnt': r[1]} for r in rows]
                    except Exception:
                        rows = []
                if isinstance(rows, list):
                    for r in rows:
                        q = r.get('quote') if isinstance(r, dict) else None
                        if q in data.get(c, {}):
                            try:
                                val = r.get('cnt', 0) if isinstance(r, dict) else 0
                                data[c][q] = float(val or 0)
                            except Exception:
                                data[c][q] = 0.0
            return data

        open_map  = fetch_grouped_holds('OPEN')
        close_map = fetch_grouped_holds('CLOSE')

        # Build output
        out: List[Dict[str, Any]] = []
        for c in currencies:
            balance, usd_price = bal_map.get(c, (0.0, 0.0))
            # Open positions: amount of currency C currently held as base across markets by quote
            balance_open_by_quote = {q: float(open_map.get(c, {}).get(q, 0.0)) for q in currencies}
            # Closed positions holds (pocket/clip) that still hold currency C as base
            hold_close_by_quote   = {q: float(close_map.get(c, {}).get(q, 0.0)) for q in currencies}

            balance_all_open = sum(balance_open_by_quote.values())
            hold_all_close   = sum(hold_close_by_quote.values())
            available_balance = max(balance - balance_all_open - hold_all_close, 0.0)

            row = {
                'quote_currency': c,
                'usd_price': round(usd_price, 8),
                'balance': round(balance, 12),
                'balance_value_usd': round(balance * usd_price, 2),
                # Per-quote breakdowns for open positions (currency C held as base)
                'balance_usdc_open_pos': round(balance_open_by_quote.get('USDC', 0.0), 12),
                'balance_btc_open_pos':  round(balance_open_by_quote.get('BTC', 0.0), 12),
                'balance_eth_open_pos':  round(balance_open_by_quote.get('ETH', 0.0), 12),
                'balance_sol_open_pos':  round(balance_open_by_quote.get('SOL', 0.0), 12),
                'balance_all_open_pos':  round(balance_all_open, 12),
                # Per-quote breakdowns for closed position holds
                'hold_count_usdc_close_pos': round(hold_close_by_quote.get('USDC', 0.0), 12),
                'hold_count_btc_close_pos':  round(hold_close_by_quote.get('BTC', 0.0), 12),
                'hold_count_eth_close_pos':  round(hold_close_by_quote.get('ETH', 0.0), 12),
                'hold_count_sol_close_pos':  round(hold_close_by_quote.get('SOL', 0.0), 12),
                'hold_count_all_close_pos':  round(hold_all_close, 12),
                # Available to spend and USD value
                'available_balance': round(available_balance, 12),
                'available_value_usd': round(available_balance * usd_price, 2),
            }
            out.append(row)

        return out

    #<=====>#

    @narc(1)
    def display_quote_balances_summary(self, overview: List[Dict[str, Any]]):
        """
        Pretty print the per-quote-currency balances/allocations summary.
        """
        if not overview:
            WoB("QUOTE BALANCES SUMMARY: No data")
            return

        self.chrt.chart_top(in_str='QUOTE BALANCES SUMMARY', len_cnt=260, bold=True)
        h = ""
        h += f"{'quote':^6} | "
        h += f"{'usd':^14} | "
        h += f"{'balance':^16} | "
        h += f"{'bal_usd':^10} | "
        h += f"{'avail':^16} | "
        h += f"{'avail_usd':^10} | "
        h += f"{'open USDC':^16} | {'open BTC':^16} | {'open ETH':^16} | {'open SOL':^16} | "
        h += f"{'hold USDC':^16} | {'hold BTC':^16} | {'hold ETH':^16} | {'hold SOL':^16}"
        self.chrt.chart_headers(in_str=h, len_cnt=260, bold=True)

        for r in overview:
            try:
                msg = ""
                msg += f"{r.get('quote_currency',''):>6} | "
                msg += f"{r.get('usd_price',0):>14.4f} | "
                msg += f"{r.get('balance',0):>16.12f} | "
                msg += f"{r.get('balance_value_usd',0):>10.2f} | "
                msg += f"{r.get('available_balance',0):>16.12f} | "
                msg += f"{r.get('available_value_usd',0):>10.2f} | "
                msg += f"{r.get('balance_usdc_open_pos',0):>16.12f} | "
                msg += f"{r.get('balance_btc_open_pos',0):>16.12f} | "
                msg += f"{r.get('balance_eth_open_pos',0):>16.12f} | "
                msg += f"{r.get('balance_sol_open_pos',0):>16.12f} | "
                msg += f"{r.get('hold_count_usdc_close_pos',0):>16.12f} | "
                msg += f"{r.get('hold_count_btc_close_pos',0):>16.12f} | "
                msg += f"{r.get('hold_count_eth_close_pos',0):>16.12f} | "
                msg += f"{r.get('hold_count_sol_close_pos',0):>16.12f}"
                self.chrt.chart_row(msg, len_cnt=260)
            except Exception:
                # Fall back to raw print for unexpected shapes
                pprint(r)

        self.chrt.chart_bottom(len_cnt=260)

    #<=====>#

    @narc(1)
    def auto_loop(self):
        if self.debug_tf: G(f'==> bot_base.auto_loop()')
        G(f'==> bot_base.auto_loop()')
        """
        🔴 GILFOYLE'S EXTRACTED Auto Trading Loop
        
        EXTRACTED from cls_bot.py lines 322-408
        
        This method contains:
        - Automated trading cycle logic
        - Order checking calls (buy_ords_check, sell_ords_check)
        - Report generation calls  
        - Error handling and recovery
        - Loop timing and sleep logic
        
        CRITICAL: Must maintain exact same behavior for live trading.
        """
        
        # Voice obeys settings; avoid COM/OOM failures
        speak('Coinbase Trade Bot Online - Auto Mode', speak_enabled=(getattr(self.st_bot, 'speak_yn', 'N') == 'Y'))

        cnt = 0
        while True:

            try:
                # 🚨 BULLETPROOF TRACING: Track exact crash location in auto_loop
                print(f"🔧 AUTO_LOOP_START: Beginning loop iteration {cnt + 1}")
                
                cnt += 1
                t0 = time.perf_counter()
                
                print(f"🔧 AUTO_LOOP_SETTINGS: Getting debug and bot settings")
                self.debug_settings_get()
                self.bot_settings_get()
                
                print(f"🔧 AUTO_LOOP_MARKETS: Processing {len(self.st_bot.trade_markets)} markets")
                # USDC, USDT, USD, BTC, ETH
                for symb in self.st_bot.trade_markets:
                    print(f"🔧 AUTO_LOOP_MARKET: Starting {symb} processing")


                    print_adv(2)
                    self.chrt.chart_top(len_cnt=260)
                    msg = f'<----- // ===== | == {symb:^5} TOP * ({cnt}) == | ===== \\ ----->'
                    self.chrt.chart_row(msg, len_cnt=260, align='center')
                    self.chrt.chart_bottom(len_cnt=260)
                    print_adv(2)

                    self.cb.cb_mkts_refresh(quote_symb=symb)

                    # self.buy_ords_check(prod_id=None, pair_context=None)

                    # print(f'report_strats_best(cnt=25, quote_symb={symb}, min_trades=5)')
                    report_strats_best(cnt=25, quote_symb=symb, min_trades=5)

                    # print(f'report_strats_best(cnt=25, quote_symb={symb}, min_trades=8)')
                    report_strats_best(cnt=25, quote_symb=symb, min_trades=8)

                    # print(f'report_strats_best(cnt=25, quote_symb={symb}, min_trades=13)')
                    report_strats_best(cnt=25, quote_symb=symb, min_trades=13)

                    # print(f'report_strats_best(cnt=25, quote_symb={symb}, min_trades=21)')
                    report_strats_best(cnt=25, quote_symb=symb, min_trades=21)

                    # report_open_by_gain()
                    # report_open_by_age()
                    # print(f'report_open_by_prod_id(quote_symb={symb})')
                    # report_open_by_prod_id(quote_symb=symb)

                    print(f'report_open_by_prod_id(quote_symb={symb}, test_only_yn="Y")')
                    report_open_by_prod_id(quote_symb=symb, test_only_yn="Y")

                    print(f'report_open_by_prod_id(quote_symb={symb}, live_only_yn="Y")')
                    report_open_by_prod_id(quote_symb=symb, live_only_yn="Y")

                    # print(f'report_open_by_prod_id(quote_symb={symb}, test_only_yn="Y", live_only_yn="Y")')
                    # report_open_by_prod_id(quote_symb=symb, test_only_yn="Y", live_only_yn="Y")

                    print(f'report_open_test_by_gain(quote_symb={symb})')
                    report_open_test_by_gain(quote_symb=symb)

                    print(f'report_open_live_by_gain(quote_symb={symb})')
                    report_open_live_by_gain(quote_symb=symb)

                    print(f'report_buys_recent(cnt=5, quote_symb={symb}, lta=T)')
                    report_buys_recent(cnt=5, quote_symb=symb, lta='T')

                    print(f'report_sells_recent(cnt=5, quote_symb={symb}, lta=T)')
                    report_sells_recent(cnt=5, quote_symb=symb, lta='T')

                    print(f'report_buys_recent(cnt=50, quote_symb={symb}, lta=L)')
                    report_buys_recent(cnt=50, quote_symb=symb, lta='L')

                    print(f'report_sells_recent(cnt=50, quote_symb={symb}, lta=L)')
                    report_sells_recent(cnt=50, quote_symb=symb, lta='L')

                    print(f'report_closed_overview_recent_test(quote_symb={symb})')
                    report_closed_overview_recent_test(quote_symb=symb)

                    print(f'report_closed_overview_recent_live(quote_symb={symb})')
                    report_closed_overview_recent_live(quote_symb=symb)

                    print(f'report_closed_overview(quote_symb={symb})')
                    report_closed_overview(quote_symb=symb)

                    print(f'report_open_overview(quote_symb={symb})')
                    report_open_overview(quote_symb=symb)

                    print_adv(2)
                    # Display per-quote-currency balance/allocations overview for USDC/BTC/ETH/SOL
                    try:
                        balances_overview = self.compute_quote_balances_summary()
                        self.display_quote_balances_summary(balances_overview)
                    except Exception as e:
                        WoB(f"QUOTE BALANCES SUMMARY ERROR: {e}")

                    print_adv(2)
                    self.chrt.chart_top(len_cnt=260)
                    msg = f'<----- // ===== | == {symb:^5} END * ({cnt}) == | ===== \\ ----->'
                    self.chrt.chart_row(msg, len_cnt=260, align='center')
                    self.chrt.chart_bottom(len_cnt=260)

                    print_adv(3)

                    # End of Loop Display
                    loop_secs = self.st_bot.auto_loop_secs

                    print_adv(2)

                    t1 = time.perf_counter()
                    elapsed_seconds = round(t1 - t0, 2)

                    WoB(f'==> {dttm_get()} auto_loop() completed loop {cnt} in {elapsed_seconds} seconds. Looping in {loop_secs} seconds...')
                    
                    print_adv(2)
                    time.sleep(loop_secs)
                    
            except Exception as e:
                # Simple error handling with full stack trace
                print(f"\n🚨 ERROR in auto_loop iteration {cnt}")
                print(f"🚨 ERROR_TYPE: {type(e).__name__}")
                print(f"🚨 ERROR_MESSAGE: {str(e)}")
                print(f"🚨 FULL_TRACEBACK:")
                traceback.print_exc()
                
                # Hard exit with error
                sys.exit(f"FATAL ERROR: {type(e).__name__}: {str(e)}")

    #<=====>#

    @narc(1)
    def main_loop(self):
        if self.debug_tf: G(f'==> bot_base.main_loop()')
        """
        🔴 GILFOYLE'S EXTRACTED Main Trading Loop
        
        EXTRACTED from cls_bot.py lines 331-402
        
        This is the TOP-LEVEL trading loop that:
        - Processes multiple markets (USDC, USDT, USD, BTC, ETH)
        - Calls mkt_main() for each market
        - Provides error handling and recovery
        - Tracks loop timing (TARGET: reduce from 1200+ to <300 seconds)
        
        PERFORMANCE CRITICAL: Primary suspected bottleneck location.
        """

        if self.mode == 'buy':
            mode_str = 'Buy Mode'
        elif self.mode == 'sell':
            mode_str = 'Sell Mode'
        else:
            mode_str = 'Full Mode'

        speak(f'Coinbase Trade Bot Online - {mode_str}', speak_enabled=(getattr(self.st_bot, 'speak_yn', 'N') == 'Y'))

        cnt = 0
        while True:
            cnt += 1
            t0 = time.perf_counter()

            self.st_debug = self.debug_settings_get()
            self.st_bot = self.bot_settings_get()

            print_adv(2)
            self.chrt.chart_top(len_cnt=260)
            msg = f'<----- // ===== | == TOP * Loop=({cnt}) * {dttm_get()}  == | ===== \\ ----->'
            self.chrt.chart_row(msg, len_cnt=260, align='center')
            self.chrt.chart_bottom(len_cnt=260)
            print_adv(2)

            markets_start = time.perf_counter()
            market_count = 0
            
            # USDC, USDT, USD, BTC, ETH
            for mkt_symb in self.st_bot.trade_markets:
                market_start = time.perf_counter()
                market_count += 1

                self.mkt_symb = mkt_symb

                print_adv(2)
                self.chrt.chart_top(len_cnt=260)
                msg = f'<----- // ===== | == * ({mkt_symb}) * == | ===== \\ ----->'
                self.chrt.chart_row(msg, len_cnt=260, align='center')
                self.chrt.chart_bottom(len_cnt=260)
                print_adv(2)

                self.mkt_new(mkt_symb=mkt_symb)
                self.mkt_main()

            # End of Loop Display
            loop_secs = self.st_bot.loop_secs

            print_adv(2)

            t1 = time.perf_counter()
            elapsed_seconds = round(t1 - t0, 2)


            print_adv(2)
            self.chrt.chart_top(len_cnt=260)
            msg = f'<----- // ===== | == END * Loop=({cnt}) * {dttm_get()} == | ===== \\ ----->'
            self.chrt.chart_row(msg, len_cnt=260, align='center')
            self.chrt.chart_bottom(len_cnt=260)
            print_adv(2)

            time.sleep(loop_secs)

    #<=====>#

    @narc(1)
    def buy_ords_check(self, prod_id=None, pair_context=None):
        if self.debug_tf: G(f'==> bot_base.buy_ords_check(prod_id={prod_id}, pair_context={pair_context})')
        """🚨 TASK 043 OPTIMIZED ORDER MANAGEMENT - Enhanced with prod_id filtering + pair context reuse

        Handles checking and processing buy orders for both test and live transactions.

        🚨 PERFORMANCE OPTIMIZATION:
        - Accepts prod_id parameter for targeted order processing
        - Uses optimized database functions with 90-95% fewer rows processed
        - CRITICAL FIX: Accepts pair_context to avoid recreating pair instances (eliminates 7s per order)
        - Maintains backward compatibility when prod_id=None and pair_context=None

        EXTREMELY HIGH RISK: Controls live money order processing
        - Polls Coinbase for order status updates
        - Processes order fills and position opening
        - Handles order cancellation and error recovery
        - Updates database with order status and transaction details

        Args:
            prod_id: Product ID to filter orders (e.g., 'BTC-USDC'). If None, processes all orders.
            pair_context: Dict with existing pair data to avoid recreation (pair, st_pair, settings, etc)
        """

        buy_order_header_yn = 'Y'

        so = None
        o = None

        print_adv(2)
        self.chrt.chart_top(len_cnt=260)
        # 🚨 TASK 043: Update display message to show filtering status
        if prod_id:
            msg = f'* Buy Orders Check ({prod_id}) * {dttm_get()} *'
        else:
            msg = f'* Buy Orders Check (ALL) * {dttm_get()} *'
        self.chrt.chart_row(msg, len_cnt=260, align='center')

        # 🚨 TASK 043 OPTIMIZATION: Use filtered query when prod_id provided
        if prod_id:
            bos = self.cbtrade_db.db_buy_ords_get(prod_id=prod_id, ord_stat='OPEN')
        else:
            bos = self.cbtrade_db.db_buy_ords_get(ord_stat='OPEN')
        if bos:
            print(f' ==> {len(bos)} buy orders to check...')
            self.chrt.chart_mid(len_cnt=260)

            bos_cnt = len(bos)
            cnt = 0
            for bo in bos:
                cnt += 1
                bo = dec_2_float(bo)
                bo = AttrDict(bo)

                o = None

                test_txn_yn = bo.test_txn_yn
                ord_id = bo.buy_order_uuid

                if test_txn_yn == 'Y':
                    bo.ord_stat = 'FILL'
                    self.cbtrade_db.db_buy_ords_insupd(bo)
                    # 🔴 OPTIMIZATION: Pass pair context to avoid recreation
                    self.pos_open(bo.buy_order_uuid, pair_context=pair_context)

                elif test_txn_yn == 'N':

                    # Fetch order details then shape. shape_ord expects a dict-like order, not UUID string
                    o_raw = cb.cb_ord_get_shaped(ord_id)  # already returns shaped object if successful
                    if o_raw:
                        o = o_raw
                    else:
                        # Fallback to manual fetch/shape if needed
                        try:
                            resp = cb.get_order(ord_id)
                            if resp and not isinstance(resp, dict):
                                resp = resp.to_dict()
                            raw_order = resp['order'] if resp and 'order' in resp else resp
                            o = cb.shape_ord(raw_order) if raw_order else None
                        except Exception:
                            o = None

                    if o:
                        o = dec_2_float(o)
                        o = AttrDict(o)

                        if o.prod_id != bo.prod_id:
                            print('error #1 !')
                            beep(3)
                            # 🚨 DEBUGGING MODE: Hard exit with clear error details
                            traceback.print_stack()
                            sys.exit(f"ORDER PRODUCT ID MISMATCH: API returned order for {o.prod_id} but expected {bo.prod_id} - buy_order_uuid: {bo.buy_order_uuid}")

                        if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
                            bo.buy_cnt_act                    = o.ord_filled_size
                            bo.fees_cnt_act                   = o.ord_total_fees
                            bo.tot_out_cnt                    = o.ord_total_value_after_fees
                            bo.prc_buy_act                    = o.ord_average_filled_price # not sure this includes the fees
                            bo.buy_end_dttm                   = o.ord_last_fill_time

                            # Set the unix timestamp for the buy end time
                            if hasattr(o, 'ord_last_fill_time_unix'):
                                # If the API provides a unix timestamp directly, use it
                                bo.buy_end_unix = o.ord_last_fill_time_unix
                            elif bo.buy_end_dttm:
                                # Otherwise convert from datetime
                                bo.buy_end_unix = conv_utc_timestamp_to_unix(bo.buy_end_dttm)

                            bo.tot_prc_buy                    = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
                            if o.ord_settled:
                                bo.ord_stat                   = 'FILL'
                            bo.prc_buy_slip_pct               = round((bo.prc_buy_act - bo.prc_buy_est) / bo.prc_buy_est, 8)


                            self.cbtrade_db.db_buy_ords_insupd(bo)
                            # 🔴 OPTIMIZATION: Pass pair context to avoid recreation
                            self.pos_open(bo.buy_order_uuid, pair_context=pair_context)

                        elif o.ord_status == 'OPEN':
                            print('')
                            print(bo)

                            print('WE NEED CODE HERE #1!!!')
                            beep(10)
                            # sys.exit(f"sys.exit from {__name__}")
                            if o.ord_filled_size == 0:
                                print(f'attempting to cancel order {bo.buy_order_uuid}... ')
                                r = cb.cancel_orders([str(bo.buy_order_uuid)])
                                print(r)
                                time.sleep(1)
                                o = cb.shape_ord(ord_id)
                                beep(10)
                                # 🚨 DEBUGGING MODE: Hard exit with clear error details
                                traceback.print_stack()
                                sys.exit(f"ORDER CANCELLATION ERROR: Failed to properly handle cancellation for buy_order_uuid {bo.buy_order_uuid} - requires manual investigation")
                                # depending on results or get_order status
                                # update bo to cancelled
                                # if counts are too small to sell, it becomes pocket/clip

                        else:
                            print('error #2 !')
    #                            beep(3)
                            self.cbtrade_db.db_buy_ords_stat_upd(bo_id=bo.bo_id, ord_stat='ERR')

                if buy_order_header_yn == 'Y':
                    buy_order_header_yn = 'N'
                    hmsg = ''
                    hmsg += f"{'#':^2}" + " | "
                    hmsg += f"{'bo_id':^7}" + " | "
                    hmsg += f"{'T':^1}" + " | "
                    hmsg += f"{'prod_id':^12}" + " | "
                    hmsg += f"{'ord_stat':^8}" + " | "
                    hmsg += f"{'buy_strat_name':^16}" + " | "
                    hmsg += f"{'buy_strat_freq':^16}" + " | "
                    hmsg += f"{'elapsed':^7}" + " | "
                    hmsg += f"{'buy_cnt_act':^18}" + " | "
                    hmsg += f"{'tot_out_cnt':^18}" + " | "
                    hmsg += f"{'prc_buy_act':^19}" + " | "
                    hmsg += f"{'tot_prc_buy':^19}" + " | "
                    hmsg += f"{'prc_buy_slip_pct':^6} %" + " | "
                    self.chrt.chart_headers(in_str=hmsg, len_cnt=260, align='left')

                msg = ''
                msg += f"{cnt:>2}" + " | "
                msg += f"{bo.bo_id:>7}" + " | "
                msg += f"{bo.test_txn_yn:^1}" + " | "
                msg += f"{bo.prod_id:<12}" + " | "
                msg += f"{bo.ord_stat:<8}" + " | "
                msg += f"{bo.buy_strat_name:<16}" + " | "
                msg += f"{bo.buy_strat_freq:<16}" + " | "
                msg += f"{int(bo.elapsed):>7}" + " | "
                msg += f"{bo.buy_cnt_act:>18.12f}" + " | "
                msg += f"{bo.tot_out_cnt:>18.12f}" + " | "
                msg += f"{bo.prc_buy_act:>19.12f}" + " | "
                msg += f"{bo.tot_prc_buy:>19.12f}" + " | "
                msg += f"{bo.prc_buy_slip_pct:>6.2f} %" + " | "
                self.chrt.chart_row(in_str=msg, len_cnt=260, align='left')

        self.chrt.chart_bottom(len_cnt=260)
        print_adv(2)

    #<=====>#

    @narc(1)
    def buy_ords_check_all(self):
        if self.debug_tf: G(f'==> bot_base.buy_ords_check_all()')
        """
        Legacy "process all" version modeled after cbtrade_2025_05_26.
        Scans ALL OPEN buy orders and advances them to FILL/pos_open.
        """
        buy_order_header_yn = 'Y'
        ord_id = None
        bo = None
        o = None

        try:
            so = None
            o = None

            print_adv(2)
            self.chrt.chart_top(len_cnt=260)
            msg = f"* Buy Orders Check (ALL) * {dttm_get()} *"
            self.chrt.chart_row(msg, len_cnt=260, align='center')

            bos = self.cbtrade_db.db_buy_ords_get(ord_stat='OPEN')

            # Normalize then sort by prod_id (robust to dict/AttrDict/tuple rows)
            rows_norm = []
            if bos:
                for r in bos:
                    try:
                        r = dec_2_float(r)
                        r = AttrDict(r if isinstance(r, dict) else r)
                    except Exception:
                        # If row is not dict-like, skip normalization but keep raw
                        pass
                    rows_norm.append(r)
                bos = sorted(rows_norm, key=lambda x: getattr(x, 'prod_id', '') or '')

            if bos:
                print(f" ==> {len(bos)} buy orders to check...")
                self.chrt.chart_mid(len_cnt=260)

                bos_cnt = len(bos)
                cnt = 0
                current_prod_id = None
                current_pair_loaded = False
                for bo in bos:
                    cnt += 1
                    # rows already normalized above, but keep safe conversion
                    try:
                        bo = AttrDict(dec_2_float(bo))
                    except Exception:
                        bo = AttrDict(bo)

                    o = None

                    test_txn_yn = bo.test_txn_yn
                    ord_id = bo.buy_order_uuid

                    # Build pair context lazily by prod_id to avoid repeated builds (if ever needed)
                    if bo.prod_id != current_prod_id:
                        current_prod_id = bo.prod_id
                        current_pair_loaded = False
                        # Attempt to prime market/pair settings for this prod_id (optional, safe failure)
                        try:
                            # Fetch mkts row for this prod_id
                            mk = self.cbtrade_db.seld(f"select * from mkts where prod_id = '{current_prod_id}' limit 1")
                            if isinstance(mk, list) and mk:
                                mk = mk[0]
                            if mk:
                                quote_symb = mk.get('quote_curr_symb')
                                if quote_symb and hasattr(self, 'mkt_new'):
                                    self.mkt_new(mkt_symb=quote_symb)
                                # If a dedicated pair settings loader exists, try to use it
                                if hasattr(self, 'pair_settings_get'):
                                    try:
                                        self.pair_settings_get()
                                    except Exception:
                                        pass
                                current_pair_loaded = True
                        except Exception:
                            # optional context; failures are acceptable here
                            pass

                    if test_txn_yn == 'Y':
                        if not bo.buy_order_uuid:
                            traceback.print_stack()
                            sys.exit(f"FATAL TEST ORDER MISSING UUID: bo_id={bo.bo_id} prod_id={bo.prod_id}")
                        bo.ord_stat = 'FILL'
                        self.cbtrade_db.db_buy_ords_insupd(bo)
                        self.pos_open(bo.buy_order_uuid, pair_context=None)

                    elif test_txn_yn == 'N':

                        # Prefer shaped getter; fallback to raw fetch + shape
                        try:
                            o_raw = cb.cb_ord_get_shaped(ord_id)
                            if o_raw:
                                o = o_raw
                            else:
                                resp = cb.get_order(ord_id)
                                if resp and not isinstance(resp, dict):
                                    resp = resp.to_dict()
                                raw_order = resp['order'] if resp and 'order' in resp else resp
                                o = cb.shape_ord(raw_order) if raw_order else None
                        except Exception:
                            traceback.print_exc()
                            traceback.print_stack()
                            print(f'bo : {bo}')
                            continue

                        if o:
                            o = dec_2_float(o)
                            o = AttrDict(o)

                            if o.prod_id != bo.prod_id:
                                print('error #1 !')
                                beep(3)
                                sys.exit(f"ORDER PRODUCT ID MISMATCH: API returned {o.prod_id} expected {bo.prod_id}")

                            if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
                                bo.buy_cnt_act      = o.ord_filled_size
                                bo.fees_cnt_act     = o.ord_total_fees
                                bo.tot_out_cnt      = o.ord_total_value_after_fees
                                bo.prc_buy_act      = o.ord_average_filled_price
                                bo.buy_end_dttm     = o.ord_last_fill_time

                                if hasattr(o, 'ord_last_fill_time_unix'):
                                    bo.buy_end_unix = o.ord_last_fill_time_unix
                                elif bo.buy_end_dttm:
                                    bo.buy_end_unix = conv_utc_timestamp_to_unix(bo.buy_end_dttm)

                                bo.tot_prc_buy = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
                                if o.ord_settled:
                                    bo.ord_stat = 'FILL'
                                bo.prc_buy_slip_pct = round((bo.prc_buy_act - bo.prc_buy_est) / bo.prc_buy_est, 8)

                                if not bo.buy_order_uuid:
                                    traceback.print_stack()
                                    sys.exit(f"FATAL LIVE ORDER MISSING UUID AT FILL: bo_id={bo.bo_id} prod_id={bo.prod_id}")
                                self.cbtrade_db.db_buy_ords_insupd(bo)
                                self.pos_open(bo.buy_order_uuid, pair_context=None)

                            elif o.ord_status == 'OPEN':
                                print('')
                                print(bo)
                                print('WE NEED CODE HERE #1!!!')
                                beep(10)
                                if o.ord_filled_size == 0:
                                    print(f"attempting to cancel order {bo.buy_order_uuid}... ")
                                    r = cb.cancel_orders([str(bo.buy_order_uuid)])
                                    print(r)
                                    time.sleep(1)
                                    o2 = cb.cb_ord_get_shaped(ord_id)
                                    print(o2)
                                    beep(10)
                                    sys.exit("ORDER CANCELLATION HANDLING NOT IMPLEMENTED")
                            else:
                                print('error #2 !')
                                self.cbtrade_db.db_buy_ords_stat_upd(bo_id=bo.bo_id, ord_stat='ERR')

                    if buy_order_header_yn == 'Y':
                        buy_order_header_yn = 'N'
                        hmsg = ''
                        hmsg += f"{'#':^2}" + " | "
                        hmsg += f"{'bo_id':^7}" + " | "
                        hmsg += f"{'T':^1}" + " | "
                        hmsg += f"{'prod_id':^12}" + " | "
                        hmsg += f"{'ord_stat':^8}" + " | "
                        hmsg += f"{'buy_strat_name':^16}" + " | "
                        hmsg += f"{'buy_strat_freq':^16}" + " | "
                        hmsg += f"{'elapsed':^7}" + " | "
                        hmsg += f"{'buy_cnt_act':^18}" + " | "
                        hmsg += f"{'tot_out_cnt':^18}" + " | "
                        hmsg += f"{'prc_buy_act':^19}" + " | "
                        hmsg += f"{'tot_prc_buy':^19}" + " | "
                        hmsg += f"{'prc_buy_slip_pct':^6} %" + " | "
                        self.chrt.chart_headers(in_str=hmsg, len_cnt=260, align='left')

                    msg = ''
                    msg += f"{cnt:>2}" + " | "
                    msg += f"{bo.bo_id:>7}" + " | "
                    msg += f"{bo.test_txn_yn:^1}" + " | "
                    msg += f"{bo.prod_id:<12}" + " | "
                    msg += f"{bo.ord_stat:<8}" + " | "
                    msg += f"{bo.buy_strat_name:<16}" + " | "
                    msg += f"{bo.buy_strat_freq:<16}" + " | "
                    msg += f"{int(getattr(bo,'elapsed',0)):>7}" + " | "
                    msg += f"{bo.buy_cnt_act:>18.12f}" + " | "
                    msg += f"{bo.tot_out_cnt:>18.12f}" + " | "
                    msg += f"{bo.prc_buy_act:>19.12f}" + " | "
                    msg += f"{bo.tot_prc_buy:>19.12f}" + " | "
                    msg += f"{bo.prc_buy_slip_pct:>6.2f} %" + " | "
                    self.chrt.chart_row(in_str=msg, len_cnt=260, align='left')

            self.chrt.chart_bottom(len_cnt=260)
            print_adv(2)

        except Exception as e:
            traceback.print_exc()
            traceback.print_stack()
            try:
                print(f'bo : {bo}')
                print(f'ord_id : {ord_id}')
                print(f'o : {o}')
            except Exception:
                pass
            sys.exit(f"FATAL buy_ords_check_all: {type(e).__name__}: {str(e)}")

    #<=====>#

    # @safe_execute()
    @narc(1)
    def pos_open(self, buy_order_uuid, pair_context=None):
        if self.debug_tf: G(f'==> bot_base.pos_open(buy_order_uuid={buy_order_uuid}, pair_context={pair_context})')
        # G(f'==> bot_base.pos_open(buy_order_uuid={buy_order_uuid}, pair_context={pair_context})')
        """🔴 CRITICAL POSITION CREATION - Extracted from cls_bot.py (~70 lines) + OPTIMIZED

        Handles automatic position opening when buy orders fill.

        🔴 PERFORMANCE OPTIMIZATION: Accepts pair_context to avoid recreating pair data
        - When called from pair context, uses existing pair/settings data (eliminates 7s overhead)
        - Falls back to legacy behavior when pair_context=None for backward compatibility

        EXTREMELY HIGH RISK: Creates new trading positions from buy order data
        - Maps complete buy order data to new position record
        - Sets up initial position tracking values
        - Initializes profit/loss tracking
        - Creates database position record

        Args:
            buy_order_uuid: UUID of filled buy order to create position from
            pair_context: Optional dict with existing pair data to avoid recreation
        """

        bos = self.cbtrade_db.db_mkt_sizing_data_get_by_uuid(buy_order_uuid)

        for bo in bos:
            bo = dec_2_float(bo)
            bo = AttrDict(bo)
            pos = AttrDict()
            pos.test_txn_yn             = bo.test_txn_yn
            pos.symb                    = bo.symb
            pos.prod_id                 = bo.prod_id
            pos.mkt_name                = bo.mkt_name
            pos.mkt_venue               = bo.mkt_venue
            pos.base_curr_symb          = bo.buy_curr_symb
            pos.base_size_incr          = bo.base_size_incr
            pos.base_size_min           = bo.base_size_min
            pos.base_size_max           = bo.base_size_max
            pos.quote_curr_symb         = bo.quote_curr_symb
            pos.quote_size_incr         = bo.quote_size_incr
            pos.quote_size_min          = bo.quote_size_min
            pos.quote_size_max          = bo.quote_size_max
            pos.pos_type                = bo.pos_type
            pos.pos_stat                = 'OPEN'
            pos.pos_begin_dttm          = bo.buy_end_dttm
            pos.pos_begin_unix          = bo.buy_end_unix
            pos.bo_id                   = bo.bo_id
            pos.bo_uuid                 = bo.buy_order_uuid
            pos.buy_strat_type          = bo.buy_strat_type
            pos.buy_strat_name          = bo.buy_strat_name
            pos.buy_strat_freq          = bo.buy_strat_freq
            pos.buy_curr_symb           = bo.buy_curr_symb
            pos.buy_cnt                 = bo.buy_cnt_act
            pos.spend_curr_symb         = bo.spend_curr_symb
            pos.fees_curr_symb          = bo.fees_curr_symb
            pos.buy_fees_cnt            = bo.fees_cnt_act
            pos.tot_out_cnt             = bo.tot_out_cnt
            pos.sell_curr_symb          = bo.buy_curr_symb
            pos.recv_curr_symb          = bo.spend_curr_symb
            pos.sell_order_cnt          = 0
            pos.sell_order_attempt_cnt  = 0
            pos.hold_cnt                = bo.buy_cnt_act
            pos.sell_cnt_tot            = 0
            pos.tot_in_cnt              = 0
            pos.sell_fees_cnt_tot       = 0
            pos.prc_buy                 = bo.tot_prc_buy
            pos.prc_curr                = bo.prc_buy_act
            pos.prc_high                = bo.prc_buy_act
            pos.prc_low                 = bo.prc_buy_act
            # Initialize canonical percent metrics to 0 at creation
            pos.prc_chg_pct             = 0
            pos.prc_chg_pct_high        = 0
            pos.prc_chg_pct_low         = 0
            pos.prc_chg_pct_drop        = 0

            pos.fees_cnt_tot            = bo.fees_cnt_act

            pos.gain_loss_amt_est       = 0
            pos.gain_loss_amt_est_low   = 0
            pos.gain_loss_amt_est_high  = 0
            pos.gain_loss_amt           = 0
            pos.gain_loss_amt_net       = 0

            pos.gain_loss_pct_est       = 0
            pos.gain_loss_pct_est_high  = 0
            pos.gain_loss_pct_est_low   = 0
            pos.gain_loss_pct           = 0

            # Debug-time guard: ensure canonical percent fields exist and are numeric
            if self.debug_tf:
                for fld in ("prc_chg_pct", "prc_chg_pct_high", "prc_chg_pct_drop"):
                    val = getattr(pos, fld, None)
                    if val is None or not isinstance(val, (int, float)):
                        traceback.print_stack()
                        sys.exit(f"FATAL: Missing/invalid {fld} on new pos init for {pos.prod_id}; got {val}")

            self.cbtrade_db.db_poss_insupd(pos)  # 🔴 GILFOYLE: NEW positions need INSERT, not UPDATE!

    #<=====>#

    @narc(1)
    def sell_ords_check(self, prod_id=None, pair_context=None):
        if self.debug_tf: G(f'==> bot_base.sell_ords_check(prod_id={prod_id}, pair_context)')
        """🚨 TASK 043 OPTIMIZED SELL ORDER MANAGEMENT - Enhanced with prod_id filtering + pair context reuse

        Handles checking and processing sell orders for both test and live transactions.

        🚨 PERFORMANCE OPTIMIZATION:
        - Accepts prod_id parameter for targeted order processing
        - Uses optimized database functions with 90-95% fewer rows processed
        - CRITICAL FIX: Accepts pair_context to avoid recreating pair instances (eliminates 7s per order)
        - Maintains backward compatibility when prod_id=None and pair_context=None

        EXTREMELY HIGH RISK: Controls live money sell order processing
        - Polls Coinbase for sell order status updates
        - Processes order fills and position closing
        - Handles complex partial fill scenarios
        - Handles order cancellation and error recovery
        - Updates database with sell order status and transaction details

        Args:
            prod_id: Product ID to filter orders (e.g., 'BTC-USDC'). If None, processes all orders.
            pair_context: Dict with existing pair data to avoid recreation (pair, st_pair, settings, etc)
        """

        sell_order_header_yn = 'Y'


        print_adv(2)
        self.chrt.chart_top(len_cnt=260)
        # 🚨 TASK 043: Update display message to show filtering status
        if prod_id:
            msg = f'* Sell Orders Check ({prod_id}) * {dttm_get()} *'
        else:
            msg = f'* Sell Orders Check (ALL) * {dttm_get()} *'
        self.chrt.chart_row(msg, len_cnt=260, align='center')

        so = None
        o = None

        cnt = 0

        # 🔴 GILFOYLE FIX: Only run system-wide integrity check when processing ALL orders (prod_id=None)
        # This prevents the cacophony of beeps when multiple bot instances check specific prod_ids
        if not prod_id:
            # System-wide check runs only once per cycle when prod_id=None (ALL orders)
            iss = self.cbtrade_db.db_poss_sell_order_problems_get()
            if iss:
                for i in iss:
                    print_adv()
                    print(i)
                beep(3)
        # When prod_id is specified, skip system-wide check to avoid duplicate beeping across bot instances

        # 🚨 TASK 043 OPTIMIZATION: Use filtered query when prod_id provided
        if prod_id:
            sos = self.cbtrade_db.db_sell_ords_get(prod_id=prod_id, ord_stat='open')
        else:
            sos = self.cbtrade_db.db_sell_ords_get(ord_stat='open')

        if sos:
            print(f' ==> {len(sos)} sell orders to check...')
            self.chrt.chart_mid(len_cnt=260)

            sos_cnt = len(sos)
            cnt = 0
            for so in sos:
                o = None
                cnt += 1
                so = dec_2_float(so)
                so = AttrDict(so)
                # print(f"==> bot_base.sell_ords_check Made It Here 1188 - so ({type(so)})={so}")
                if self.debug_tf: C(f"==> bot_base.sell_ords_check Made It Here 1188 - so={so}")
                test_txn_yn = so.test_txn_yn
                ord_id = so.sell_order_uuid

                if test_txn_yn == 'Y':
                    so.ord_stat = 'FILL'
                    self.cbtrade_db.db_sell_ords_insupd(so)
                    # 🔴 OPTIMIZATION: Pass pair context to avoid recreation
                    self.pos_close(so.pos_id, so.sell_order_uuid, pair_context=pair_context)

                elif test_txn_yn == 'N':
                    # Fetch order details then shape. shape_ord expects a dict-like order, not UUID string
                    o_raw = cb.cb_ord_get_shaped(ord_id)  # already returns shaped object if successful
                    if o_raw:
                        o = o_raw
                    else:
                        # Fallback to manual fetch/shape if needed
                        try:
                            resp = cb.get_order(ord_id)
                            if resp and not isinstance(resp, dict):
                                resp = resp.to_dict()
                            raw_order = resp['order'] if resp and 'order' in resp else resp
                            o = cb.shape_ord(raw_order) if raw_order else None
                        except Exception:
                            o = None

                    if o:
                        o = dec_2_float(o)
                        o = AttrDict(o)
                        if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
                            so.sell_cnt_act                    = o.ord_filled_size
                            so.fees_cnt_act                    = o.ord_total_fees
                            so.tot_in_cnt                      = o.ord_total_value_after_fees
                            so.prc_sell_act                    = o.ord_average_filled_price # not sure this includes the fees
                            so.sell_end_dttm                   = o.ord_last_fill_time
                            so.prc_sell_tot                    = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
                            if o.ord_settled:
                                so.ord_stat                    = 'FILL'
                            so.prc_sell_slip_pct               = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 10) * 100
                            self.cbtrade_db.db_sell_ords_insupd(so)
                            # 🔴 OPTIMIZATION: Pass pair context to avoid recreation
                            self.pos_close(so.pos_id, so.sell_order_uuid, pair_context=pair_context)

                        elif o.ord_status == 'OPEN':
                            print('')
                            print(so)

                            print('WE NEED CODE HERE #1 !!!')
                            beep(10)
                            # sys.exit(f"sys.exit from {__name__}")
                            if so.elapsed > 3 and o.ord_filled_size == 0:
                                print(f'attempting to cancel order {so.sell_order_uuid}... ')
                                r = cb.cancel_orders([str(so.sell_order_uuid)])
                                print(r)
                                time.sleep(1)
                                # Re-fetch latest state
                                o_raw = cb.cb_ord_get_shaped(ord_id)
                                if o_raw:
                                    o = o_raw
                                else:
                                    try:
                                        resp = cb.get_order(ord_id)
                                        if resp and not isinstance(resp, dict):
                                            resp = resp.to_dict()
                                        raw_order = resp['order'] if resp and 'order' in resp else resp
                                        o = cb.shape_ord(raw_order) if raw_order else None
                                    except Exception:
                                        o = None
                                beep(10)
                                # 🚨 DEBUGGING MODE: Hard exit with clear error details
                                traceback.print_stack()
                                sys.exit(f"SELL ORDER CANCELLATION ERROR: Failed to properly handle cancellation for sell_order_uuid {so.sell_order_uuid} - requires manual investigation")
                                # depending on results or get_order status
                                # update bo to cancelled
                                # update counts on poss if anything filled
                                # update status on poss depending

                            if so.elapsed > 5 and o.ord_filled_size > 0:
                                print(f'partially filled and cannot cancel order {so.sell_order_uuid}... ')
                                so.sell_cnt_act                    = o.ord_filled_size
                                so.fees_cnt_act                    = o.ord_total_fees
                                so.tot_in_cnt                      = o.ord_total_value_after_fees
                                so.prc_sell_act                    = o.ord_average_filled_price # not sure this includes the fees
                                so.sell_end_dttm                   = o.ord_last_fill_time
                                so.prc_sell_tot                    = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
                                so.prc_sell_slip_pct               = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 8)
                                print(f'{cnt:^4} / {sos_cnt:^4}, prod_id : {so.prod_id:<16}, pos_id : {so.pos_id:>7}, so_id : {so.so_id:>7}, so_uuid : {so.sell_order_uuid:<60}')
                                beep(10)
                                # sys.exit(f"sys.exit from {__name__}")

                                self.cbtrade_db.db_sell_ords_insupd(so)
        # this needs to be added when we add in support for limit orders
        #                        else:
        #                            r = cb_ord_cancel_orders(order_ids=[ord_id])
        #                            db_sell_ords_stat_upd(so_id=so.so_id, ord_stat='CANC')
        #                            db_poss_err_upd(pos_id=so.pos_id, pos_stat='OPEN')
                        elif o.ord_status == 'FAILED':
                            print('')
                            print(so)
                            self.pos.pos_stat = 'OPEN'
                            self.cbtrade_db.db_poss_insupd(self.pos)
                            so.ignore_tf = True
                            self.cbtrade_db.db_sell_ords_insupd(so)
                            # beep(10)
                            print('SELL ORDER FAILED !!! Resetting Position To OPEN')
                            return

                        else:
                            print('WE NEED CODE HERE #1 !!!')
                            beep(10)
                            print(o)
                            print(so)
                            # 🚨 DEBUGGING MODE: Hard exit with clear error details
                            traceback.print_stack()
                            sys.exit(f"UNHANDLED SELL ORDER SCENARIO: Sell order {so.sell_order_uuid} in unexpected state - needs code implementation")
                            self.cbtrade_db.db_sell_ords_insupd(so)
                            self.cbtrade_db.db_poss_err_upd(so.pos_id, 'OPEN')

                if sell_order_header_yn == 'Y':
                    sell_order_header_yn = 'N'
                    hmsg = ''
                    hmsg += f"{'#':^2}" + " | "
                    hmsg += f"{'so_id':^7}" + " | "
                    hmsg += f"{'pos_id':^7}" + " | "
                    hmsg += f"{'T':^1}" + " | "
                    hmsg += f"{'prod_id':^12}" + " | "
                    hmsg += f"{'ord_stat':^8}" + " | "
                    hmsg += f"{'buy_strat_name':^16}" + " | "
                    hmsg += f"{'buy_strat_freq':^16}" + " | "
                    hmsg += f"{'sell_strat_name':^16}" + " | "
                    hmsg += f"{'sell_strat_freq':^16}" + " | "
                    hmsg += f"{'elapsed':^7}" + " | "
    #                    hmsg += f"{'sell_cnt_est':^18}" + " | "
                    hmsg += f"{'sell_cnt_act':^20}" + " | "
                    hmsg += f"{'tot_in_cnt':^18}" + " | "
    #                    hmsg += f"{'prc_sell_est':^19}" + " | "
                    hmsg += f"{'prc_sell_act':^19}" + " | "
                    hmsg += f"{'prc_sell_tot':^19}" + " | "
                    hmsg += f"{'prc_sell_slip_pct':^6} %" + " | "
                    self.chrt.chart_headers(in_str=hmsg, len_cnt=260, align='left')

                # print(f"==> bot_base.sell_ords_check Made It Here 1295 - so ({type(so)})={so}")

                # Safely resolve strategy display fields; sell orders may not carry buy_* columns
                buy_strat_name = getattr(so, 'buy_strat_name', None)
                buy_strat_freq = getattr(so, 'buy_strat_freq', None)
                if not buy_strat_name or not buy_strat_freq:
                    try:
                        _pos_row = self.cbtrade_db.db_poss_get(pos_id=so.pos_id)
                        if isinstance(_pos_row, list) and _pos_row:
                            _pos_row = _pos_row[0]
                        if _pos_row:
                            _pos_row = dec_2_float(_pos_row)
                            buy_strat_name = buy_strat_name or _pos_row.get('buy_strat_name')
                            buy_strat_freq = buy_strat_freq or _pos_row.get('buy_strat_freq')
                    except Exception:
                        # Non-fatal: display defaults; core processing already handled above
                        buy_strat_name = buy_strat_name or ''
                        buy_strat_freq = buy_strat_freq or ''

                # Elapsed may be named 'elapsed' or 'elapsed_mins' depending on source
                elapsed = getattr(so, 'elapsed', None)
                if elapsed is None and hasattr(so, 'elapsed_mins'):
                    elapsed = so.elapsed_mins

                msg = ''
                msg += f"{cnt:>2}" + " | "
                msg += f"{so.so_id:>7}" + " | "
                msg += f"{so.pos_id:>7}" + " | "
                msg += f"{so.test_txn_yn:^1}" + " | "
                msg += f"{so.prod_id:<12}" + " | "
                msg += f"{so.ord_stat:<8}" + " | "
                msg += f"{(buy_strat_name or ''):<16}" + " | "
                msg += f"{(buy_strat_freq or ''):<16}" + " | "
                msg += f"{(so.sell_strat_name or ''):<16}" + " | "
                msg += f"{(so.sell_strat_freq or ''):<16}" + " | "
                msg += f"{(elapsed if elapsed is not None else 0):^7}" + " | "
    #                msg += f"{so.sell_cnt_est:>18.12f}" + " | "
                msg += f"{so.sell_cnt_act:>20.12f}" + " | "
                msg += f"{so.tot_in_cnt:>18.12f}" + " | "
    #                msg += f"{so.prc_sell_est:>19.12f}" + " | "
                msg += f"{so.prc_sell_act:>19.12f}" + " | "
                msg += f"{so.prc_sell_tot:>19.12f}" + " | "
                msg += f"{so.prc_sell_slip_pct:>6.2f}" + " | "
                self.chrt.chart_row(in_str=msg, len_cnt=260, align='left')

        self.chrt.chart_bottom(len_cnt=260)
        print_adv(2)

    #<=====>#

    @narc(1)
    def sell_ords_check_all(self):
        if self.debug_tf: G(f'==> bot_base.sell_ords_check_all()')
        """
        Legacy "process all" version modeled after cbtrade_2025_05_26.
        Scans ALL OPEN sell orders and advances them to FILL/pos_close.
        """
        sell_order_header_yn = 'Y'
        ord_id = None
        so = None
        o = None

        try:
            print_adv(2)
            self.chrt.chart_top(len_cnt=260)
            msg = f"* Sell Orders Check (ALL) * {dttm_get()} *"
            self.chrt.chart_row(msg, len_cnt=260, align='center')

            so = None
            o = None

            cnt = 0

            # System-wide integrity only on ALL
            try:
                iss = self.cbtrade_db.db_poss_sell_order_problems_get()
                if iss:
                    for i in iss:
                        print_adv()
                        print(i)
                    beep(3)
            except Exception:
                pass

            sos = self.cbtrade_db.db_sell_ords_get(ord_stat='open')

            # Normalize then sort by prod_id
            rows_norm = []
            if sos:
                for r in sos:
                    try:
                        r = dec_2_float(r)
                        r = AttrDict(r if isinstance(r, dict) else r)
                    except Exception:
                        pass
                    rows_norm.append(r)
                sos = sorted(rows_norm, key=lambda x: getattr(x, 'prod_id', '') or '')

            if sos:
                print(f" ==> {len(sos)} sell orders to check...")
                self.chrt.chart_mid(len_cnt=260)

                sos_cnt = len(sos)
                cnt = 0
                current_prod_id = None
                current_pair_loaded = False
                for so in sos:
                    o = None
                    cnt += 1
                    try:
                        so = AttrDict(dec_2_float(so))
                    except Exception:
                        so = AttrDict(so)

                    test_txn_yn = so.test_txn_yn
                    ord_id = so.sell_order_uuid

                    # Build pair context lazily by prod_id to avoid repeated builds (if needed by downstream logic)
                    if so.prod_id != current_prod_id:
                        current_prod_id = so.prod_id
                        current_pair_loaded = False
                        try:
                            mk = self.cbtrade_db.seld(f"select * from mkts where prod_id = '{current_prod_id}' limit 1")
                            if isinstance(mk, list) and mk:
                                mk = mk[0]
                            if mk:
                                quote_symb = mk.get('quote_curr_symb')
                                if quote_symb and hasattr(self, 'mkt_new'):
                                    self.mkt_new(mkt_symb=quote_symb)
                                if hasattr(self, 'pair_settings_get'):
                                    try:
                                        self.pair_settings_get()
                                    except Exception:
                                        pass
                                current_pair_loaded = True
                        except Exception:
                            pass

                    if test_txn_yn == 'Y':
                        if not so.sell_order_uuid:
                            traceback.print_stack()
                            sys.exit(f"FATAL TEST SELL ORDER MISSING UUID: so_id={so.so_id} pos_id={so.pos_id} prod_id={so.prod_id}")
                        so.ord_stat = 'FILL'
                        self.cbtrade_db.db_sell_ords_insupd(so)
                        self.pos_close(so.pos_id, so.sell_order_uuid, pair_context=None)

                    elif test_txn_yn == 'N':
                        try:
                            o_raw = cb.cb_ord_get_shaped(ord_id)
                            if o_raw:
                                o = o_raw
                            else:
                                resp = cb.get_order(ord_id)
                                if resp and not isinstance(resp, dict):
                                    resp = resp.to_dict()
                                raw_order = resp['order'] if resp and 'order' in resp else resp
                                o = cb.shape_ord(raw_order) if raw_order else None
                        except Exception as e:
                            traceback.print_exc()
                            traceback.print_stack()
                            print(f'so : {so}')
                            continue

                        if o:
                            o = dec_2_float(o)
                            o = AttrDict(o)
                            if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
                                so.sell_cnt_act = o.ord_filled_size
                                so.fees_cnt_act = o.ord_total_fees
                                so.tot_in_cnt   = o.ord_total_value_after_fees
                                so.prc_sell_act = o.ord_average_filled_price
                                so.sell_end_dttm = o.ord_last_fill_time
                                so.prc_sell_tot = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
                                if o.ord_settled:
                                    so.ord_stat = 'FILL'
                                so.prc_sell_slip_pct = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 10) * 100
                                if not so.sell_order_uuid:
                                    traceback.print_stack()
                                    sys.exit(f"FATAL LIVE SELL ORDER MISSING UUID AT FILL: so_id={so.so_id} pos_id={so.pos_id} prod_id={so.prod_id}")
                                self.cbtrade_db.db_sell_ords_insupd(so)
                                self.pos_close(so.pos_id, so.sell_order_uuid, pair_context=None)

                            elif o.ord_status == 'OPEN':
                                print('')
                                print(o)
                                print('')
                                print(so)
                                print('WE NEED CODE HERE #1 !!!')
                                beep(10)
                                if getattr(so, 'elapsed', 0) > 3 and o.ord_filled_size == 0:
                                    print(f"attempting to cancel order {so.sell_order_uuid}... ")
                                    r = cb.cancel_orders([str(so.sell_order_uuid)])
                                    print(r)
                                    time.sleep(1)
                                    o2 = cb.cb_ord_get_shaped(ord_id)
                                    print(o2)
                                    beep(10)
                                    sys.exit("SELL ORDER CANCELLATION HANDLING NOT IMPLEMENTED")
                                if getattr(so, 'elapsed', 0) > 5 and o.ord_filled_size > 0:
                                    print(f"partially filled and cannot cancel order {so.sell_order_uuid}... ")
                                    so.sell_cnt_act = o.ord_filled_size
                                    so.fees_cnt_act = o.ord_total_fees
                                    so.tot_in_cnt   = o.ord_total_value_after_fees
                                    so.prc_sell_act = o.ord_average_filled_price
                                    so.sell_end_dttm = o.ord_last_fill_time
                                    so.prc_sell_tot = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
                                    print(f"{cnt:^4} / {sos_cnt:^4}, prod_id : {so.prod_id:<16}, pos_id : {so.pos_id:>7}, so_id : {so.so_id:>7}, so_uuid : {so.sell_order_uuid:<60}")
                                    beep(10)
                                    self.cbtrade_db.db_sell_ords_insupd(so)
                            else:
                                pprint(o)
                                print('WE NEED CODE HERE #1 !!!')
                                beep(10)
                                sys.exit("UNEXPECTED SELL ORDER STATE")

                    if sell_order_header_yn == 'Y':
                        sell_order_header_yn = 'N'
                        hmsg = ''
                        hmsg += f"{'#':^2}" + " | "
                        hmsg += f"{'so_id':^7}" + " | "
                        hmsg += f"{'pos_id':^7}" + " | "
                        hmsg += f"{'T':^1}" + " | "
                        hmsg += f"{'prod_id':^12}" + " | "
                        hmsg += f"{'ord_stat':^8}" + " | "
                        hmsg += f"{'buy_strat_name':^16}" + " | "
                        hmsg += f"{'buy_strat_freq':^16}" + " | "
                        hmsg += f"{'sell_strat_name':^16}" + " | "
                        hmsg += f"{'sell_strat_freq':^16}" + " | "
                        hmsg += f"{'elapsed':^7}" + " | "
                        hmsg += f"{'sell_cnt_act':^20}" + " | "
                        hmsg += f"{'tot_in_cnt':^18}" + " | "
                        hmsg += f"{'prc_sell_act':^19}" + " | "
                        hmsg += f"{'prc_sell_tot':^19}" + " | "
                        hmsg += f"{'prc_sell_slip_pct':^6} %" + " | "
                        self.chrt.chart_headers(in_str=hmsg, len_cnt=260, align='left')

                    msg = ''
                    msg += f"{cnt:>2}" + " | "
                    msg += f"{so.so_id:>7}" + " | "
                    msg += f"{so.pos_id:>7}" + " | "
                    msg += f"{so.test_txn_yn:^1}" + " | "
                    msg += f"{so.prod_id:<12}" + " | "
                    msg += f"{so.ord_stat:<8}" + " | "
                    msg += f"{so.buy_strat_name:<16}" + " | "
                    msg += f"{so.buy_strat_freq:<16}" + " | "
                    msg += f"{so.sell_strat_name or '':<16}" + " | "
                    msg += f"{so.sell_strat_freq or '':<16}" + " | "
                    msg += f"{getattr(so,'elapsed',0):^7}" + " | "
                    msg += f"{so.sell_cnt_act:>20.12f}" + " | "
                    msg += f"{so.tot_in_cnt:>18.12f}" + " | "
                    msg += f"{so.prc_sell_act:>19.12f}" + " | "
                    msg += f"{so.prc_sell_tot:>19.12f}" + " | "
                    msg += f"{so.prc_sell_slip_pct:>6.2f}" + " | "
                    self.chrt.chart_row(in_str=msg, len_cnt=260, align='left')

            self.chrt.chart_bottom(len_cnt=260)
            print_adv(2)

        except Exception as e:
            traceback.print_exc()
            traceback.print_stack()
            try:
                if so:
                    print(f'so : {so}')
                if ord_id:
                    print(f'ord_id : {ord_id}')
                if o:
                    print(f'o : {o}')
            except Exception:
                pass
            sys.exit(f"FATAL sell_ords_check_all: {type(e).__name__}: {str(e)}")

    #<=====>#

    # @safe_execute()
    @narc(1)
    def pos_close(self, pos_id, sell_order_uuid, pair_context=None):
        if self.debug_tf: G(f'==> bot_base.pos_close(pos_id={pos_id}, sell_order_uuid={sell_order_uuid}, pair_context={pair_context})')
        speak(f'POS CLOSE - COME WATCH position {pos_id}')
        """🔴 CRITICAL POSITION CLOSURE - Extracted from cls_bot.py (~81 lines) + PERFORMANCE OPTIMIZED

        Handles final position closure when sell orders fill.

        🔴 CRITICAL PERFORMANCE OPTIMIZATION: Accepts pair_context to avoid recreating pair data
        - ELIMINATES 7s overhead: No more self.pair_new() and self.settings_pair_get() calls per order
        - When called from pair context, uses existing pair/settings data (MASSIVE performance gain)
        - Falls back to legacy behavior when pair_context=None for backward compatibility

        EXTREMELY HIGH RISK: Finalizes trade results and profit/loss calculations
        - Retrieves position and sell order data
        - Calculates final profit/loss amounts
        - Applies rainy day pocket/clip logic
        - Updates position status to CLOSE
        - Final database position record update

        Args:
            pos_id: Position ID to close
            sell_order_uuid: UUID of filled sell order
            pair_context: Optional dict with existing pair data to avoid recreation (eliminates 7s overhead!)
        """

        # Prevent duplicate processing - POSS Table
        pos = self.cbtrade_db.db_poss_get(pos_id=pos_id)
        if self.debug_tf: print(f"==> bot_base.pos_close Made It Here 1348 - pos {pos_id} ({type(pos)})={pos}")
        if isinstance(pos, list):
            pos = pos[0]
        pos = dec_2_float(pos)
        pos = AttrDict(pos)
        # pprint(pos)
        # Prevent duplicate processing - POSS Table
        # 🚨 CRITICAL FIX: Prevent multiple sell order processing for same position
        if pos.pos_stat == 'CLOSE':
            print(f'⚠️  RACE CONDITION PREVENTED: Position {pos_id} already CLOSED, skipping sell order {sell_order_uuid}')
            beep(4)
            return  # Exit early to prevent duplicate processing

        # Prevent duplicate processing - SELL_ORDS Table
        so  = self.cbtrade_db.db_sell_ords_get(uuid=sell_order_uuid)
        if self.debug_tf: print(f"==> bot_base.pos_close Made It Here 1355 - so {sell_order_uuid} ({type(so)})={so}")
        if isinstance(so, list):
            so = so[0]
        so  = dec_2_float(so)
        so  = AttrDict(so)
        # pprint(so)
        if self.debug_tf: C(f"==> bot_base.pos_close Made It Here 1355 - so ({type(so)})={so}")
        # # Prevent duplicate processing - SELL_ORDS Table
        # # 🚨 ADDITIONAL SAFEGUARD: Check if sell order already processed
        # if hasattr(so, 'ord_stat') and so.ord_stat == 'FILL':
        #     print(f'⚠️  DUPLICATE PROCESSING PREVENTED: Sell order {sell_order_uuid} already FILLED for position {pos_id}')
        #     beep(4)
        #     return  # Exit early to prevent duplicate processing

        pos.symb = pos.quote_curr_symb
        prod_id  = pos.prod_id

        # If we have a sell order we are closing the position
        pos.pos_stat                              = 'CLOSE'
        pos.pos_end_dttm                          = so.sell_end_dttm
        pos.sell_order_cnt                        += 1
        pos.sell_order_attempt_cnt                += 1
        pos.hold_cnt                              -= so.sell_cnt_act
        pos.tot_in_cnt                            += so.tot_in_cnt
        pos.sell_cnt_tot                          += so.sell_cnt_act
        pos.fees_cnt_tot                          += so.fees_cnt_act
        pos.sell_fees_cnt_tot                     += so.fees_cnt_act
        pos.prc_sell_avg                          = round((pos.tot_in_cnt / pos.sell_cnt_tot), 8)
        pos.prc_curr                              = so.prc_sell_tot

        # Update Sell Price Highs & Lows
        if so.prc_sell_tot > pos.prc_high:
            pos.prc_high = so.prc_sell_tot
        if so.prc_sell_tot < pos.prc_low:
            pos.prc_low = so.prc_sell_tot

        # Update Price Change %
        pos.prc_chg_pct = calc_chg_pct(old_val=pos.prc_buy, new_val=so.prc_sell_tot, dec_prec=4)

        # Update Price Change % Highs & Lows
        if pos.prc_chg_pct > pos.prc_chg_pct_high:
            pos.prc_chg_pct_high = pos.prc_chg_pct
        if pos.prc_chg_pct < pos.prc_chg_pct_low:
            pos.prc_chg_pct_low  = pos.prc_chg_pct

        # Update Price Change Drop from Highest
        pos.prc_chg_pct_drop = round(pos.prc_chg_pct - pos.prc_chg_pct_high, 2)

        # Update Gain Loss Amt
        pos.val_curr          = pos.hold_cnt * pos.prc_sell_avg
        pos.val_tot           = pos.hold_cnt * pos.prc_sell_avg
        pos.gain_loss_amt     = pos.tot_in_cnt - pos.tot_out_cnt + pos.val_curr
        pos.gain_loss_amt_net = pos.gain_loss_amt + pos.val_tot

        # gain_loss_pct_est is to capture the pct at the time we decide to sell and should not be updated after
        pos.gain_loss_pct = calc_chg_pct(old_val=pos.tot_out_cnt, new_val=pos.tot_in_cnt + pos.val_curr, dec_prec=4)

        # Finalize the Pocket & Clip Info using existing settings context
        if pos.prc_chg_pct > 0:
            pos.pocket_pct          = self.st_pair.sell.rainy_day.pocket_pct
            pos.clip_pct            = self.st_pair.sell.rainy_day.clip_pct
            pos.pocket_cnt          = pos.hold_cnt
            pos.clip_cnt            = 0
        else:
            pos.pocket_pct          = self.st_pair.sell.rainy_day.pocket_pct
            pos.clip_pct            = self.st_pair.sell.rainy_day.clip_pct
            pos.pocket_cnt          = 0
            pos.clip_cnt            = pos.hold_cnt

        # Update to Database
        self.cbtrade_db.db_poss_upd(pos)

        # Prepare data for cache update (non-blocking)
        pos_data = {
            'prod_id': pos.prod_id,
            'pos_id': pos.pos_id,
            'symb': pos.symb,
            'buy_strat_type': pos.buy_strat_type,
            'buy_strat_name': pos.buy_strat_name,
            'buy_strat_freq': pos.buy_strat_freq,
            'test_txn_yn': pos.test_txn_yn
        }

        sell_order_data = {
            'sell_order_uuid': sell_order_uuid,
            'sell_cnt_act': so.sell_cnt_act,
            'tot_in_cnt': so.tot_in_cnt,
            'prc_sell_act': so.prc_sell_act
        }

        # Determine live/test flag for cache updates
        if pos.test_txn_yn == 'Y':
            lta = 'T'
        else:
            lta = 'L'

        # Position close cache updates - run silently when everything works properly

        # Update trade performance cache for sell operations
        result2 = self.pair_trade_perf_sell_upd(pos.prod_id, lta)
        result1 = self.pair_trade_perf_sell_upd(pos.prod_id, 'A')

        # Update strategy performance cache for sell operations
        result3 = self.pair_trade_strat_perf_sell_upd(prod_id, pos.buy_strat_type, pos.buy_strat_name, pos.buy_strat_freq, lta)
        result4 = self.pair_trade_strat_perf_sell_upd(prod_id, pos.buy_strat_type, pos.buy_strat_name, pos.buy_strat_freq, 'A')


#<=====>#
# Functions
#<=====>#


#<=====>#
# Post Variables
#<=====>#

bot = BOT()


#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    bot.bot()

#<=====>#
