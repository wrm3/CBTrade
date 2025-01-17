#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import decimal
import sys
import time
import traceback
import uuid
from datetime import datetime as dt
from datetime import datetime, timedelta
from pprint import pprint

from fstrent_colors import (
    B, G, M, R,
    BoW, GoW, MoW, RoW,
    WoB, WoG, WoM, WoR, YoK, 
    cp, cs
)
from fstrent_tools import (
    AttrDict, AttrDictConv, DictKey, beep, dec, dec_2_float, dttm_get,
    format_disp_age, format_disp_age2, play_cash,
    play_thunder, print_adv, speak
)
from libs.bot_coinbase import (
    cb, cb_bal_get, cb_bid_ask_by_amt_get, cb_client_order_id,
    cb_mkt_prc_dec_calc, cb_mkts_refresh, cb_ord_get, cb_wallet_refresh
)
from libs.bot_common import calc_chg_pct, freqs_get, writeit
from libs.bot_db_ohlcv import db_check_ohlcv_prod_id_table
from libs.bot_db_read import (
    db_bals_get, db_bot_spent, db_buy_check_get, 
    db_buy_ords_open_get, db_mkt_elapsed_get, 
    db_mkt_sizing_data_get_by_uuid, db_mkt_strat_elapsed_get,
    db_mkts_open_cnt_get, db_open_trade_amts_get, 
    db_pair_spent, db_pairs_loop_get, 
    db_pairs_loop_poss_open_prod_ids_get, db_pairs_loop_top_gains_prod_ids_get, 
    db_pairs_loop_top_perfs_prod_ids_get, db_pairs_loop_top_prc_chg_prod_ids_get,
    db_pairs_loop_top_vol_chg_pct_prod_ids_get, db_pairs_loop_top_vol_chg_prod_ids_get, 
    db_pairs_loop_watched_prod_ids_get, db_pos_get_by_pos_id, db_pos_open_get_by_prod_id,
    db_poss_check_last_dttm_get, db_poss_open_max_trade_size_get, 
    db_poss_sell_order_problems_get, db_sell_check_get, 
    db_sell_double_check, db_sell_ords_get_by_pos_id,
    db_sell_ords_get_by_uuid, db_sell_ords_open_get, 
    db_table_names_get, db_trade_strat_perf_get, 
    db_view_trade_perf_get_by_prod_id
)
from libs.bot_db_write import (
    db_buy_ords_stat_upd, db_mkt_checks_buy_upd, 
    db_mkt_checks_sell_upd, db_poss_check_last_dttm_upd, 
    db_poss_stat_upd, db_table_csvs_dump, 
    db_tbl_buy_ords_insupd, db_tbl_mkts_insupd,
    db_tbl_poss_insupd, db_tbl_sell_ords_insupd
)
from libs.bot_reports import (
    report_buys_recent, report_open_by_age,
    report_open_by_prod_id, report_open_live_by_gain, 
    report_open_test_by_gain, report_sells_recent, 
    report_strats_best
)
from libs.bot_settings import (
    bot_settings_get, debug_settings_get, resolve_settings
)
from libs.bot_strats import (
    buy_strat_settings_get, buy_strats_avail_get, buy_strats_check,
    buy_strats_deny, buy_strats_get, sell_strat_settings_get, sell_strats_check
)
from libs.bot_ta import ta_main_new
from libs.bot_theme import chrt, cs_pct_color, cs_pct_color_50
from libs.cls_settings import AttrDict, AttrDictConv, Settings


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_cls_main'
log_name      = 'bot_cls_main'

# <=====>#
# Assignments Pre
# <=====>#


#<=====>#
# Classes
#<=====>#

class BOT():

    def __init__(self, mode='full'):
        self.mode = mode
        self.fnc_secs_max              = 0.33
        self.settings_debug_get()
        self.settings_bot_get()
        self.bot_guid                  = self.gen_guid()
        self.budget                    = AttrDict()
        self.chrt                      = chrt
        self.spacer                    = cs(' ' * 4, font_color='white', bg_color='black')

    #<=====>#

    def gen_guid(self):
        return str(uuid.uuid4())

    #<=====>#

    def auto_loop(self):

        # this is here just to proof that sounds alerts will be heard
        if self.bst.speak_yn == 'Y': speak('Coinbase Trade Bot Online - Auto Mode')

        cnt = 0
        while True:
            try:
                cnt += 1
                t0 = time.perf_counter()

                self.settings_debug_get()
                self.settings_bot_get()

                print_adv(2)
                self.chrt.chart_top()
                msg = f'<----- // ===== | == TOP * ({cnt}) == | ===== \\ ----->'
                self.chrt.chart_row(msg, align='center')
                self.chrt.chart_bottom()
                print_adv(2)

                cb_mkts_refresh()

                self.buy_ords_check()
                self.sell_ords_check()

                report_strats_best(25, min_trades=5)
                report_strats_best(25, min_trades=8)
                report_strats_best(25, min_trades=13)
                report_strats_best(25, min_trades=21)

                # report_open_by_gain()
                # report_open_by_age()
                report_open_by_prod_id()

                report_open_test_by_gain()
                report_open_live_by_gain()

                report_buys_recent(5, test_yn='Y')
                report_sells_recent(5, test_yn='Y')

                report_buys_recent(25, test_yn='N')
                report_sells_recent(25, test_yn='N')

#                 report_open_by_age()
#                 print_adv(3)

#                 report_buys_recent(5, test_yn='Y')
#                 report_buys_recent(25, test_yn='N')
# #                report_buys_recent(cnt=20)
#                 print_adv(3)

#                 report_sells_recent(5, test_yn='Y')
#                 report_sells_recent(25, test_yn='N')
# #                report_sells_recent(cnt=20)

                print_adv(3)

                # Dump CSVs of database tables for recovery
                if cnt == 1 or cnt % 10 == 0:
                    db_table_csvs_dump()

                # End of Loop Display
                loop_secs = self.bst.auto_loop_secs

                print_adv(2)

                t1 = time.perf_counter()
                elapsed_seconds = round(t1 - t0, 2)

                WoB(f'==> auto_loop() completed loop {cnt} in {elapsed_seconds} seconds. Looping in {loop_secs} seconds...')

                print_adv(2)
                self.chrt.chart_top()
                msg = f'<----- // ===== | == END * ({cnt}) == | ===== \\ ----->'
                self.chrt.chart_row(msg, align='center')
                self.chrt.chart_bottom()
                print_adv(2)

                time.sleep(loop_secs)

            except KeyboardInterrupt as e:
                print(f' ==> keyed exit... {e}')
                sys.exit()

            except Exception as e:
                loop_secs = self.bst.loop_secs
                print(f' ==> errored... {e}')
                print(dttm_get())
                traceback.print_exc()
                traceback.print_stack()
                print(type(e))
                print(e)
                print(f'sleeping {loop_secs} seconds and then restarting')
                time.sleep(loop_secs)

    #<=====>#

    def main_loop(self):

        if self.mode == 'buy':
            mode_str = 'Buy Mode'
        elif self.mode == 'sell':
            mode_str = 'Sell Mode'
        else:
            mode_str = 'Full Mode'

        # this is here just to proof that sounds alerts will be heard
        if self.bst.speak_yn == 'Y': speak(f'Coinbase Trade Bot Online - {mode_str}')

        cnt = 0
        while True:
            try:
                cnt += 1
                t0 = time.perf_counter()

                self.settings_debug_get()
                self.settings_bot_get()

                print_adv(2)
                self.chrt.chart_top()
                msg = f'<----- // ===== | == TOP * ({cnt}) == | ===== \\ ----->'
                self.chrt.chart_row(msg, align='center')
                self.chrt.chart_bottom()
                print_adv(2)

                # USDC, USDT, USD, BTC, ETH
                for symb in self.bst.trade_markets:
                    mkt = self.mkt_new(symb=symb)
                    self.mkt_main()

                # Dump CSVs of database tables for recovery
                if self.mode == 'full' and cnt == 1 or cnt % 10 == 0:
                    db_table_csvs_dump()

                # End of Loop Display
                loop_secs = self.bst.loop_secs

                print_adv(2)

                t1 = time.perf_counter()
                elapsed_seconds = round(t1 - t0, 2)

                WoB(f' ==> completed {cnt} loop in {elapsed_seconds} seconds. Looping in {loop_secs} seconds...')

                print_adv(2)
                self.chrt.chart_top()
                msg = f'<----- // ===== | == END * ({cnt}) == | ===== \\ ----->'
                self.chrt.chart_row(msg, align='center')
                self.chrt.chart_bottom()
                print_adv(2)

                time.sleep(loop_secs)

            except KeyboardInterrupt as e:
                print(f' ==> keyed exit... {e}')
                sys.exit()

            except Exception as e:
                loop_secs = self.bst.loop_secs
                print(f' ==> errored... {e}')
                print(dttm_get())
                traceback.print_exc()
                print(type(e))
                print(e)
                print(f'sleeping {loop_secs} seconds and then restarting')
                time.sleep(loop_secs)

    #<=====>#

    # Function to fetch current positions
    def wallet_refresh(self, force_tf=False):

        if self.mkt.refresh_wallet_tf or force_tf:
            cb_wallet_refresh()
            self.mkt.refresh_wallet_tf = False

            self.budget[self.mkt.symb].reserve_amt      = 0
            self.budget[self.mkt.symb].bal_avail        = 0
            self.budget[self.mkt.symb].spendable_amt    = 0
            self.budget[self.mkt.symb].open_trade_amt   = 0

            # when/if we start trading  against btc, eth, sol and not just usdc
            # we will need to add a deduction for the amount outstanding on trades 
            # that used other currencies
            open_trade_amts = {}
            open_trade_amts = AttrDictConv(d=open_trade_amts)
            r = db_open_trade_amts_get()

            for x in r:
                x = AttrDictConv(d=x)
                x = dec_2_float(x)
                if x['base_curr_symb'] in ('BTC', 'ETH', 'USDT', 'USDC'):
                    open_trade_amts[x['base_curr_symb']] = x['open_trade_amt']

            bals = db_bals_get()
            for bal in bals:
                bal = dec_2_float(bal)
                bal = AttrDictConv(d=bal)
                curr = bal.curr
                if curr == self.mkt.symb:
                    self.budget[self.mkt.symb].bal_avail = bal.bal_avail
                    self.budget_res_amt_calc()
                    self.budget[self.mkt.symb].spendable_amt = self.budget[self.mkt.symb].bal_avail - self.budget[self.mkt.symb].reserve_amt 
                    if curr in open_trade_amts:
                        self.budget[self.mkt.symb].open_trade_amt = open_trade_amts[curr]
                        self.budget[self.mkt.symb].spendable_amt -= self.budget[self.mkt.symb].open_trade_amt
                    else:
                        self.budget[self.mkt.symb].open_trade_amt = 0


    #<=====>#

    def budget_refresh(self):

        '''
        "budget": {
            "max_tot_loss": -250.0,
            "spend_max_amt": 2100.0,
            "spend_up_max_pct": 50.00,
            "spend_dn_max_pct": 50.00,
            "spend_max_pcts": {
                "***": {"spend_up_max_pct": 80, "spend_dn_max_pct": 20},
                "BTC-USDC": {"spend_up_max_pct": 60, "spend_dn_max_pct": 40},
                "ETH-USDC": {"spend_up_max_pct": 60, "spend_dn_max_pct": 40},
                "SOL-USDC": {"spend_up_max_pct": 60, "spend_dn_max_pct": 40}
            },
            "mkt_shares": {
            "shares_or_pcts": "pct",
                "***": 1,
                "BTC-USDC": 20,
                "ETH-USDC": 20,
                "SOL-USDC": 20,
                "SUI-USDC": 3
            },
            "reserve_amt": 1000.0,
            "reserve_addtl_daily_amt": 5
        },
        '''

        bot_spent_data  = db_bot_spent(self.mkt.symb)
        if isinstance(bot_spent_data, list):
            if len(bot_spent_data) > 0:
                bot_spent_data = bot_spent_data[0]
#        pprint(bot_spent_data)
        if not bot_spent_data:
            bot_spent_data = AttrDict()
            bot_spent_data.symb         = self.mkt.symb
            bot_spent_data.open_cnt     = 0
            bot_spent_data.open_up_cnt  = 0
            bot_spent_data.open_dn_cnt  = 0
            bot_spent_data.open_up_pct  = 0
            bot_spent_data.open_dn_pct  = 0
            bot_spent_data.spent_amt    = 0
            bot_spent_data.spent_up_amt = 0
            bot_spent_data.spent_dn_amt = 0
            bot_spent_data.spent_up_pct = 0
            bot_spent_data.spent_dn_pct = 0

    # sql += "select x.symb "
    # sql += "  , x.open_cnt "
    # sql += "  , x.open_up_cnt "
    # sql += "  , x.open_dn_cnt "
    # sql += "  , round((x.open_up_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_up_pct "
    # sql += "  , round((x.open_dn_cnt / (x.open_up_cnt + x.open_dn_cnt)) * 100, 2) as open_dn_pct "
    # sql += "  , x.spent_amt "
    # sql += "  , x.spent_up_amt "
    # sql += "  , x.spent_dn_amt "
    # sql += "  , round((x.spent_up_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_up_pct "
    # sql += "  , round((x.spent_dn_amt / (x.spent_up_amt + x.spent_dn_amt)) * 100, 2) as spent_dn_pct "

        bot_spent_data  = dec_2_float(bot_spent_data)

        self.budget[self.mkt.symb].symb               = self.mkt.symb
        self.budget[self.mkt.symb].open_cnt           = db_mkts_open_cnt_get(mkt=self.mkt.symb)
        self.budget[self.mkt.symb].open_up_cnt        = 0
        self.budget[self.mkt.symb].open_dn_cnt        = 0
        self.budget[self.mkt.symb].open_up_pct        = 0
        self.budget[self.mkt.symb].open_dn_pct        = 0

        self.budget[self.mkt.symb].spend_max_amt      = self.mst.budget.spend_max_amt
        self.budget[self.mkt.symb].spend_up_max_pct   = self.mst.budget.spend_up_max_pct
        self.budget[self.mkt.symb].spend_dn_max_pct   = self.mst.budget.spend_up_max_pct
        self.budget[self.mkt.symb].spend_up_max_amt   = self.budget[self.mkt.symb].spend_up_max_pct / 100 * self.budget[self.mkt.symb].spend_max_amt
        self.budget[self.mkt.symb].spend_dn_max_amt   = self.budget[self.mkt.symb].spend_dn_max_pct / 100 * self.budget[self.mkt.symb].spend_max_amt

        self.budget[self.mkt.symb].open_amt           = bot_spent_data['open_cnt']
        self.budget[self.mkt.symb].open_up_amt        = bot_spent_data['open_up_cnt']
        self.budget[self.mkt.symb].open_dn_amt        = bot_spent_data['open_dn_cnt']
        self.budget[self.mkt.symb].open_up_pct        = bot_spent_data['open_up_pct']
        self.budget[self.mkt.symb].open_dn_pct        = bot_spent_data['open_dn_pct']

        self.budget[self.mkt.symb].spent_amt          = bot_spent_data['spent_amt']
        self.budget[self.mkt.symb].spent_pct          = round((bot_spent_data['spent_amt'] / self.budget[self.mkt.symb].spend_max_amt) * 100)

        self.budget[self.mkt.symb].spent_up_amt       = bot_spent_data['spent_up_amt']
        self.budget[self.mkt.symb].spent_dn_amt       = bot_spent_data['spent_dn_amt']
        self.budget[self.mkt.symb].spent_up_pct       = 0
        self.budget[self.mkt.symb].spent_dn_pct       = 0
        if self.budget[self.mkt.symb].spent_amt > 0:
            self.budget[self.mkt.symb].spent_up_pct       = round((bot_spent_data['spent_up_amt'] / self.budget[self.mkt.symb].spent_amt) * 100)
            self.budget[self.mkt.symb].spent_dn_pct       = round((bot_spent_data['spent_dn_amt'] / self.budget[self.mkt.symb].spent_amt) * 100)

        self.budget[self.mkt.symb].spendable_up_amt   = min(self.budget[self.mkt.symb].spendable_amt, (self.budget[self.mkt.symb].spend_up_max_amt - self.budget[self.mkt.symb].spent_up_amt))
        self.budget[self.mkt.symb].spendable_dn_amt   = min(self.budget[self.mkt.symb].spendable_amt, (self.budget[self.mkt.symb].spend_up_max_amt - self.budget[self.mkt.symb].spent_dn_amt))

        # cp('************************************************************************************','black','yellow')
        # speak(f'check screen now {self.mkt.symb}!!!')
        # print('400')
        # pprint(bot_spent_data)
        # pprint(self.budget[self.mkt.symb])
        # speak(f'check screen now {self.mkt.symb}!!!')
        # cp('************************************************************************************','black','yellow')



    #<=====>#

    def budget_res_amt_calc(self):

        day = dt.now().day
        min_reserve_amt                = self.mst.budget.reserve_amt
        daily_reserve_amt              = self.mst.budget.reserve_addtl_daily_amt
        tot_daily_reserve_amt          = day * daily_reserve_amt

        if self.budget[self.mkt.symb].reserve_locked_tf:
            self.budget[self.mkt.symb].reserve_amt    = tot_daily_reserve_amt + min_reserve_amt
        else:
            self.budget[self.mkt.symb].reserve_amt    = min_reserve_amt


    #<=====>#

    def prt_cols(self, l, cols=10, clr='WoG'):
        col_cnt = 0
        s = ''
        for x in l:
            col_cnt += 1
            if clr == 'WoG':
                s += cs(text=f'{x:<15}', font_color='white', bg_color='green')
            elif clr == 'GoW':
                s += cs(text=f'{x:<15}', font_color='green', bg_color='white')
            if col_cnt % cols == 0:
                self.chrt.chart_row(s)
                s = ''
                col_cnt = 0
            elif col_cnt == len(l):
                s += ''
            else:
                s += ' | '
        if col_cnt > 0 and col_cnt < cols:
            self.chrt.chart_row(s)


#<=====>#

    def ohlcv_tables_check(self):

        table_names = db_table_names_get()
        for m in self.mkt.loop_pairs:
            prod_id = m['prod_id']
            table_name = f'ohlcv_{prod_id}'.replace('-','_')
            if table_name not in table_names:
                db_check_ohlcv_prod_id_table(prod_id)


    #<=====>#

    def settings_debug_get(self):
        self.dst = debug_settings_get()[0]

    #<=====>#

    def settings_bot_get(self):
        self.bst = bot_settings_get()[0]

    #<=====>#

    def settings_mkt_get(self):
    #    print(f'settings_mkt_get({symb})')
        if self.mkt.symb == 'USDC':
            st = {
                "edited_yn": "Y",
                "upd_msg": "These settings are from 2024-10-02 11:15am",
                "trade_yn": "Y",
                "trade_live_yn": "Y",
                "paper_trades_only_yn": "Y",
                "stable_coins": ["DAI", "GUSD", "PAX", "PYUSD", "USD", "USDC", "USDT"],
                "speak_yn": "Y",
                "loop_secs": 15,
                "budget": {
                    "max_tot_loss": -250.0,
                    "spend_max_amt": 2100.0,
                    "spend_up_max_pct": 50.00,
                    "spend_dn_max_pct": 50.00,
                    "spend_max_pcts": {
                        "***": {"spend_up_max_pct": 80,"spend_dn_max_pct": 20},
                        "BTC-USDC": {"spend_up_max_pct": 60,"spend_dn_max_pct": 40},
                        "ETH-USDC": {"spend_up_max_pct": 60,"spend_dn_max_pct": 40},
                        "SOL-USDC": {"spend_up_max_pct": 60,"spend_dn_max_pct": 40}
                    },
                    "mkt_shares": {
                        "shares_or_pcts": "pct",
                        "***": 1,
                        "BTC-USDC": 20,
                        "ETH-USDC": 20,
                        "SOL-USDC": 20,
                        "SUI-USDC": 3
                    },
                    "reserve_amt": 100.0,
                    "reserve_addtl_daily_amt": 5
                },
                "pairs": {
                    "trade_pairs": [
                        "BTC-USDC",
                        "ETH-USDC",
                        "SOL-USDC",
                        "SUI-USDC"
                    ],
                    "stable_pairs": [
                        "DAI-USDC",
                        "GUSD-USDC",
                        "PAX-USDC",
                        "PYUSD-USDC",
                        "USDT-USDC"
                    ],
                    "err_pairs": [
                        "DAI-USDC",
                        "MATIC-USDC",
                        "MKR-USDC"
                    ],
                    "extra_pairs_watched_yn": "N",
                    "extra_pairs_top_bot_perf_yn": "Y",
                    "extra_pairs_top_bot_perf_cnt": 10,
                    "extra_pairs_top_bot_perf_pct_min": 0.1,
                    "extra_pairs_top_bot_gains_yn": "Y",
                    "extra_pairs_top_bot_gains_cnt": 20,
                    "extra_pairs_prc_pct_chg_24h_yn": "Y",
                    "extra_pairs_prc_pct_chg_24h_cnt": 5,
                    "extra_pairs_prc_pct_chg_24h_pct_min": 3,
                    "extra_pairs_vol_quote_24h_yn": "N",
                    "extra_pairs_vol_quote_24h_cnt": 3,
                    "extra_pairs_vol_pct_chg_24h_yn": "N",
                    "extra_pairs_vol_pct_chg_24h_cnt": 3
                },
                "buy_test_txns": {
                    "test_txns_on_yn": "N",
                    "test_txns_min": 3,
                    "test_txns_max": 20
                },
                "buy": {
                    "buying_on_yn": "Y",
                    "show_tests_yn": "N",
                    "show_tests_min": 101,
                    "save_files_yn": "N",
                    "buy_limit_yn": "N",
                    "show_boosts_yn": "N",
                    "mkts_open_max": 100,
                    "trade_strat_perf_recent_cnt": 50,
                    "special_prod_ids": [
                        "BTC-USDC",
                        "ETH-USDC",
                        "SOL-USDC",
                        "SUI-USDC"
                    ],
                    "buy_delay_minutes": {
                        "***": 5,
                        "BTC-USDC": 1,
                        "ETH-USDC": 1,
                        "SOL-USDC": 1
                    },
                    "buy_strat_delay_minutes": {
                        "15min": 8,
                        "30min": 15,
                        "1h": 30,
                        "4h": 120,
                        "1d": 720
                    },
                    "open_poss_cnt_max": {
                        "***": 5,
                        "BTC-USDC": 40,
                        "ETH-USDC": 40,
                        "SOL-USDC": 40
                    },
                    "strat_open_cnt_max": {
                        "***": 1,
                        "BTC-USDC": 5,
                        "ETH-USDC": 5,
                        "SOL-USDC": 5
                    },
                    "trade_size": {
                        "***": 10,
                        "BTC-USDC": 50,
                        "ETH-USDC": 50,
                        "SOL-USDC": 50
                    },
                    "trade_size_min_mult": {
                        "***": 5,
                        "BTC-USDC": 20,
                        "ETH-USDC": 20,
                        "SOL-USDC": 20
                    },
                    "trade_size_max": {
                        "***": 25,
                        "BTC-USDC": 100,
                        "ETH-USDC": 100,
                        "SOL-USDC": 100,
                        "SUI-USDC": 50
                    },
                    "strats": {}
                },
                "sell": {
                    "selling_on_yn": "Y",
                    "show_blocks_yn": "N",
                    "show_forces_yn": "Y",
                    "show_tests_yn": "N",
                    "save_files_yn": "N",
                    "sell_limit_yn": "N",
                    "take_profit": {
                        "hard_take_profit_yn": "Y",
                        "hard_take_profit_pct": 100,
                        "hard_take_profit_strats_skip": [],
                        "trailing_profit_yn": "Y",
                        "trailing_profit_trigger_pct": 3,
                        "trailing_profit_strats_skip": [],
                        "trailing_profit_levels": {
                            "89": 8.00,
                            "55": 7.00,
                            "34": 6.00,
                            "21": 5.00,
                            "13": 4.00,
                            "8": 3.00,
                            "5": 2.00,
                            "3": 1.00,
                            "2": 0.66,
                            "1": 0.33
                        }
                    },
                    "stop_loss": {
                        "hard_stop_loss_yn": "Y",
                        "hard_stop_loss_pct": 11,
                        "hard_stop_loss_strats_skip": [],
                        "trailing_stop_loss_yn": "N",
                        "trailing_stop_loss_pct": 10,
                        "trailing_stop_loss_strats_skip": [],
                        "nwe_exit_yn": "N",
                        "nwe_exit_strats_skip": [],
                        "atr_stop_loss_yn": "N",
                        "atr_stop_loss_rfreq": "1d",
                        "atr_stol_loss_strats_skip": [],
                        "trailing_atr_stop_loss_yn": "N",
                        "trailing_atr_stop_loss_pct": 70,
                        "trailing_atr_stop_loss_rfreq": "1d",
                        "trailing_atr_stop_loss_strats_skip": []
                    },
                    "force_sell": {
                        "all_yn": "N",
                        "live_all_yn": "N",
                        "prod_ids": ["CBETH-USDC", "LSETH-USDC", "MSOL-USDC", "WAMPL-USDC", "WAXL-USDC", "WBTC-USDC", "WCFG-USDC", "MATIC-USDC"],
                        "pos_ids": []
                    },
                    "never_sell": {
                        "all_yn": "N",
                        "prod_ids": [],
                        "pos_ids": []
                    },
                    "never_sell_loss": {
                        "all_yn": "Y",
                        "live_all_yn": "Y",
                        "prod_ids": ["BTC-USDC", "ETH-USDC", "SOL-USDC", "SUI-USDC"],
                        "pos_ids": []
                    },
                    "strats": {},
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
                    "rainy_day": {
                        "pocket_pct": {"***": 10, "BTC-USDC": 50, "ETH-USDC": 50, "SOL-USDC": 50},
                        "clip_pct": {"***": 0, "BTC-USDC": 5, "ETH-USDC": 5, "SOL-USDC": 5}
                        }
                    }
                }

        elif self.mkt.symb == 'BTC':
            st = {}

        elif self.mkt.symb == 'ETH':
            st = {}

        st = buy_strat_settings_get(st)
        st = sell_strat_settings_get(st)

#        pprint(st)

        self.mkt_settings = Settings(f'settings/market_{self.mkt.symb.lower()}.json', st)
        self.mst = self.mkt_settings.settings_load()
        self.mst = AttrDictConv(d=self.mst)

    #<=====>#

    def settings_pair_get(self):
        self.settings_mkt_get()
        prod_id = self.pair.prod_id.upper()
        pst = resolve_settings(self.mst, prod_id)
        pst = AttrDictConv(d=pst)
        self.pst = pst

    #<=====>#

    def mkt_new(self, symb):

        self.mkt                           = AttrDict()

        self.mkt.class_name                = 'MARKET'
        self.mkt.symb                      = symb
        self.mkt.fpath                     = self.bst.trade_markets[symb]['settings_fpath']
        self.settings_debug_get()
        self.settings_bot_get()
        self.settings_mkt_get()

        self.mkt.buy_strats                = buy_strats_get()

        self.budget[self.mkt.symb]                    = AttrDict()
        self.budget[self.mkt.symb].bal_avail          = 0
        self.budget[self.mkt.symb].spendable_amt      = 0
        self.budget[self.mkt.symb].reserve_amt        = 0
        self.budget[self.mkt.symb].reserve_locked_tf         = True

        self.mkt.refresh_wallet_tf         = True
        self.wallet_refresh(force_tf=True)
        self.budget_refresh()
        self.budget_res_amt_calc()


    #<=====>#

    def mkt_pairs_list_get(self):

        self.mkt.loop_pairs       = []
        self.mkt.buy_pairs        = []
        self.mkt.sell_pairs       = []

        if self.mode in ('buy', 'full'):
            self.mkt.buy_pairs = self.mkt_pairs_list_buy_get()
            self.mkt.loop_pairs.extend(self.mkt.buy_pairs)
            hmsg = f'buy self.mkts ({len(self.mkt.buy_pairs)}) :'
            self.chrt.chart_mid(in_str=hmsg)
            self.prt_cols(self.mkt.buy_pairs, cols=10)
            self.chrt.chart_bottom()
            print_adv()

        if self.mode in ('sell', 'full'):
            self.mkt.sell_pairs = self.mkt_pairs_list_sell_get()
            self.mkt.loop_pairs.extend(self.mkt.sell_pairs)
            hmsg = f'sell self.mkts ({len(self.mkt.sell_pairs)}) :'
            self.chrt.chart_mid(in_str=hmsg)
            self.prt_cols(self.mkt.sell_pairs, cols=10)
            self.chrt.chart_bottom()
            print_adv()

#        cb_ords_refresh(loop_mkts=self.mkt.loop_pairs)

        stable_pairs         = self.mst.pairs.stable_pairs
        err_pairs            = self.mst.pairs.err_pairs
        if self.mkt.loop_pairs:
            self.mkts                 = db_pairs_loop_get(mode=self.mode, loop_pairs=self.mkt.loop_pairs, stable_pairs=stable_pairs, err_pairs=err_pairs)
            self.mkts                 = dec_2_float(self.mkts)
            # print('self.mkts:')
            # print(self.mkts)
        else:
            self.mkts                 = []
            # Iterates through the self.mkts returned from MySQL and converts all decimals to floats
            # This is faster than making everything be done in decimals (which I would prefer)
        self.mkt.loop_pairs       = self.mkts


    #<=====>#

    def mkt_pairs_list_buy_get(self):

        buy_pairs = []

        print_adv(2)
        self.chrt.chart_top(in_str='Buy Market Collection')

        # get self.mkts from settings
        spot_pairs  = self.mst.pairs.trade_pairs
        if spot_pairs:
            self.mkts = list(set(spot_pairs))
            buy_pairs.extend(self.mkts)

        # Get The Markets with the best performance on the bot so far
        # By Gain Loss Percen Per Hour
        # Settings how many of these we will look at
        pct_min    = self.mst.pairs.extra_pairs_top_bot_perf_pct_min
        lmt_cnt    = self.mst.pairs.extra_pairs_top_bot_perf_cnt
        self.mkts       = db_pairs_loop_top_perfs_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min, quote_curr_symb=self.mkt.symb)
#        print(f'extra_pairs_top_bot_perf_yn : {self.mst.pairs.extra_pairs_top_bot_perf_yn}')
#        print(self.mkts)
        if self.mkts:
            if self.mst.pairs.extra_pairs_top_bot_perf_yn == 'Y':
                hmsg = f'adding self.mkts top bot gain loss percent per day performers ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='WoG')
                buy_pairs.extend(self.mkts)
            elif self.mst.pairs.extra_pairs_top_bot_perf_cnt > 0:
                hmsg = f'skipping self.mkts top bot gain loss percent per day performers ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='GoW')

        # Get The Markets with the best performance on the bot so far
        # By Gain Loss Amount Total
        # Settings how many of these we will look at
        lmt_cnt    = self.mst.pairs.extra_pairs_top_bot_gains_cnt
        self.mkts       = db_pairs_loop_top_gains_prod_ids_get(lmt=lmt_cnt, quote_curr_symb=self.mkt.symb)
#        print(f'extra_pairs_top_bot_perf_yn : {self.mst.pairs.extra_pairs_top_bot_gains_yn}')
#        print(self.mkts)
        if self.mkts:
            if self.mst.pairs.extra_pairs_top_bot_gains_yn == 'Y':
                hmsg = f'adding self.mkts top bot gain loss performers ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='WoG')
                buy_pairs.extend(self.mkts)
            elif self.mst.pairs.extra_pairs_top_bot_gains_cnt > 0:
                hmsg = f'skipping self.mkts top bot gain loss performers ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='GoW')

        # Get The Markets with the top 24h price increase
        # Settings how many of these we will look at
        pct_min    = self.mst.pairs.extra_pairs_prc_pct_chg_24h_pct_min
        lmt_cnt    = self.mst.pairs.extra_pairs_prc_pct_chg_24h_cnt
        self.mkts       = db_pairs_loop_top_prc_chg_prod_ids_get(lmt=lmt_cnt, pct_min=pct_min, quote_curr_symb=self.mkt.symb)
        if self.mkts:
            if self.mst.pairs.extra_pairs_prc_pct_chg_24h_yn == 'Y':
                hmsg = f'adding self.mkts top price increases ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='WoG')
                buy_pairs.extend(self.mkts)
            elif self.mst.pairs.extra_pairs_prc_pct_chg_24h_cnt > 0:
                hmsg = f'skipping self.mkts top price increases ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='GoW')

        # Get The Markets with the top 24h volume increase
        # Settings how many of these we will look at
        lmt_cnt    = self.mst.pairs.extra_pairs_vol_quote_24h_cnt
        self.mkts       = db_pairs_loop_top_vol_chg_prod_ids_get(lmt=lmt_cnt, quote_curr_symb=self.mkt.symb)
        if self.mkts:
            if self.mst.pairs.extra_pairs_vol_quote_24h_yn == 'Y':
                hmsg = f'adding self.mkts highest volume ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='WoG')
                buy_pairs.extend(self.mkts)
            elif self.mst.pairs.extra_pairs_vol_quote_24h_cnt > 0:
                hmsg = f'skipping self.mkts highest volume ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='GoW')

        # Get The Markets with the top 24h volume percent increase
        # Settings how many of these we will look at
        lmt_cnt    = self.mst.pairs.extra_pairs_vol_pct_chg_24h_cnt
        self.mkts       = db_pairs_loop_top_vol_chg_pct_prod_ids_get(lmt=lmt_cnt, quote_curr_symb=self.mkt.symb)
        if self.mkts:
            if self.mst.pairs.extra_pairs_vol_pct_chg_24h_yn == 'Y':
                hmsg = f'adding self.mkts highest volume increase ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='WoG')
                buy_pairs.extend(self.mkts)
            elif self.mst.pairs.extra_pairs_vol_pct_chg_24h_cnt > 0:
                hmsg = f'skipping self.mkts highest volume increase ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='GoW')

        # Get The Markets that are marked as favorites on Coinbase
        self.mkts       = db_pairs_loop_watched_prod_ids_get(quote_curr_symb=self.mkt.symb)
        if self.mkts:
            if self.mst.pairs.extra_pairs_watched_yn == 'Y':
                hmsg = f'adding watched markets ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='WoG')
                buy_pairs.extend(self.mkts)
            else:
                hmsg = f'skipping watched markets ({len(self.mkts)}) :'
                self.chrt.chart_mid(in_str=hmsg)
                self.prt_cols(self.mkts, cols=10, clr='GoW')

        return buy_pairs

    #<=====>#

    def mkt_pairs_list_sell_get(self):

        self.chrt.chart_top(in_str='Sell Market Collection')

        sell_pairs = []

        # Get The Markets with Open Positions
        # They all need to be looped through buy/sell logic
        pairs       = db_pairs_loop_poss_open_prod_ids_get(quote_curr_symb=self.mkt.symb)
        if pairs:
            pairs = list(set(pairs))
            hmsg = f'adding markets with open positions ({len(pairs)}) :'
            self.chrt.chart_mid(in_str=hmsg)
            self.prt_cols(pairs, cols=10)

            sell_pairs.extend(pairs)

        return sell_pairs

    #<=====>#

    def mkt_main(self):

        if self.mode in ('buy'):
            report_buys_recent(cnt=5, test_yn='Y')
            report_buys_recent(cnt=25, test_yn='N')
            print_adv(3)
            self.wallet_refresh()
            self.mkt_pairs_loop()
            print_adv(3)
            report_buys_recent(cnt=5, test_yn='Y')
            report_buys_recent(cnt=25, test_yn='N')
            print_adv(3)

        elif self.mode in ('sell'):
            report_sells_recent(cnt=5, test_yn='Y')
            report_sells_recent(cnt=25, test_yn='N')
            print_adv(3)
            self.wallet_refresh()
            self.mkt_pairs_loop()
            print_adv(3)
            report_open_by_age()
            print_adv(3)
            report_sells_recent(cnt=5, test_yn='Y')
            report_sells_recent(cnt=25, test_yn='N')
            print_adv(3)

        else:
            report_buys_recent(cnt=5, test_yn='Y')
            report_buys_recent(cnt=25, test_yn='N')
            print_adv(3)
            report_sells_recent(cnt=5, test_yn='Y')
            report_sells_recent(cnt=25, test_yn='N')
            print_adv(3)
            self.wallet_refresh()
            self.mkt_pairs_loop()
            print_adv(3)
            report_open_by_age()
            print_adv(3)
            report_buys_recent(cnt=5, test_yn='Y')
            report_buys_recent(cnt=25, test_yn='N')
            print_adv(3)
            report_sells_recent(cnt=5, test_yn='Y')
            report_sells_recent(cnt=25, test_yn='N')
            print_adv(3)


    #<=====>#

    def mkt_pairs_loop(self):

        self.budget_refresh()

        t = f'Markets Loop : {self.mkt.symb}'
        if self.mode == 'buy':
            if self.budget[self.mkt.symb].spent_amt >= self.budget[self.mkt.symb].spend_max_amt:
                msg = cs(f'We have spent our entire {self.mkt.symb} budget... spent : {self.budget[self.mkt.symb].spent_amt} / {self.budget[self.mkt.symb].spend_max_amt} max...', 'white', 'red')
                print(msg)
                self.disp_budget2(budget=self.budget[self.mkt.symb], title=t, footer=msg)
                report_sells_recent(cnt=20)
                time.sleep(30)
                return
            else:
                msg = cs(f'We have more {self.mkt.symb} budget to spend... spent : {self.budget[self.mkt.symb].spent_amt} / {self.budget[self.mkt.symb].spend_max_amt} max...', 'white', 'red')
                print(msg)
                self.disp_budget2(budget=self.budget[self.mkt.symb], title=t, footer=msg)

        cnt = 0
        # loop through all self.mkts for buy/sell logic

        self.mkt_pairs_list_get()

        self.mkt.dttm_start_loop = dttm_get()
        self.mkt.start_loop_dttm = dt.now().replace(microsecond=0)
        self.mkt.t_loop = time.perf_counter()

#        if self.mode not in ('sell'):
        self.ohlcv_tables_check()

        for pair_dict in self.mkt.loop_pairs:
            cnt += 1
            pair_dict = dec_2_float(pair_dict)
            pair_dict = AttrDictConv(d=pair_dict)

            self.mkt.t_now = time.perf_counter()
            self.mkt.t_elapse = self.mkt.t_now - self.mkt.t_loop
            self.mkt.cnt = cnt
            self.mkt.loop_age = format_disp_age2(self.mkt.t_elapse)

            title_msg = f'prod_id : {pair_dict.prod_id}, bot_mode : {self.mode}, bot_guid : {self.bot_guid}'
            self.disp_budget2(title=title_msg, budget=self.budget[self.mkt.symb])



            # List the order of the upcoming pairs
            # print(self.mkt.loop_pairs)
            self.chrt.chart_mid(in_str='Upcoming Markets')
            self.mkt.loop_pairs_list = []
            not_yet = True
            for pd in self.mkt.loop_pairs:
                pd = AttrDictConv(d=pd)
                if not_yet:
                    if pd.prod_id == pair_dict.prod_id:
                        self.mkt.loop_pairs_list.append(pd.prod_id)
                        not_yet = False
                else:
                    self.mkt.loop_pairs_list.append(pd.prod_id)
                    # break
            temp_str = ''
            true_len = 0
            for prod in self.mkt.loop_pairs_list:
                if true_len + len(prod) + 2 > 248:
                    self.chrt.chart_row(in_str=temp_str)
                    temp_str = ''
                    true_len = 0
                else:
                    temp_str += cs(f'{prod}', font_color='green') + ', '
                    true_len += len(prod) + 2
            if len(temp_str) > 0:
                temp_str = temp_str[:-2]
                self.chrt.chart_row(in_str=temp_str)
            # self.prt_cols(l=self.mkt.loop_pairs_list, cols=12, clr='WoG')
            self.chrt.chart_bottom()


#            pair = PAIR(self.mkt=self.mkt, pair_dict=pair_dict, mode=self.mode)
            self.pair_new(pair_dict=pair_dict) 
            self.pair_main()

        t = f'Markets Loop : {self.mkt.symb}'

        if self.mode == 'buy':
            if self.budget[self.mkt.symb].spent_amt >= self.budget[self.mkt.symb].spend_max_amt:
                msg = cs(f'We have spent our entire {self.mkt.symb} budget... spent : {self.budget[self.mkt.symb].spent_amt} / {self.budget[self.mkt.symb].spend_max_amt} max...', 'white', 'red')
            else:
                msg = cs(f'We have more {self.mkt.symb} budget to spend... spent : {self.budget[self.mkt.symb].spent_amt} / {self.budget[self.mkt.symb].spend_max_amt} max...', 'white', 'red')
            print(msg)
            self.disp_budget2(budget=self.budget[self.mkt.symb], title=t, footer=msg)

            if self.budget[self.mkt.symb].spent_amt >= self.budget[self.mkt.symb].spend_max_amt:
                report_sells_recent(cnt=20)
                time.sleep(30)
                return


    #<=====>#

    def pair_new(self, pair_dict):

        self.pair                      = AttrDict()

        self.pair.class_name           = 'PAIR'
        for k, v in pair_dict.items():
            self.pair[k] = v
        self.pair.symb                 = self.mkt.symb
        self.settings_debug_get()
        self.settings_bot_get()
        self.settings_mkt_get()
        self.settings_pair_get()
        self.pair.buy_strats           = buy_strats_get()
        self.pair.show_buy_header_tf   = True


    #<=====>#

    def pair_main(self):

        prod_id = self.pair.prod_id

        if self.mode in ('buy','full'):
            buy_check_dttm, buy_check_guid, buy_check_elapsed = db_buy_check_get(prod_id)

            msg = ''
            msg += f'{self.pair.prod_id:>15}'
            msg += f', {dttm_get()}'
            msg += f', bot_guid: {self.bot_guid}'
            msg += f', buy_check_guid : {buy_check_guid}'
            msg += f', buy_check_elapsed : {buy_check_elapsed}'
            msg += f', buy_check_dttm : {buy_check_dttm}'
            msg += f', self.pair.buy_check_dttm : {self.pair.buy_check_dttm}'
            msg += f', self.mkt.start_loop_dttm : {self.mkt.start_loop_dttm}'

            if not self.pair.buy_check_dttm:
                print(f'setting buy_check_dttm...')
                self.pair.buy_check_dttm = buy_check_dttm

            # if buy_check_dttm >= self.mkt.start_loop_dttm:
            #     print_adv()
            #     YoK(f'another bot with mode buy has updated {prod_id} market since starting..., old : {self.pair.check_mkt_dttm}, new : {buy_check_dttm}, start : {self.mkt.start_loop_dttm}  skipping...')
            #     # return self.mkt
            #     return

            if buy_check_dttm >= self.mkt.start_loop_dttm and buy_check_guid != self.bot_guid:
                # print(msg)
                YoK(f'1 - another bot with mode {self.mode} has updated {prod_id} market since starting..., old : {self.pair.check_mkt_dttm}, start : {self.mkt.start_loop_dttm}, bot_guid: {self.bot_guid}, mkt_check_guid : {buy_check_guid}')
                # return self.mkt
                return
            elif buy_check_elapsed < 2 and buy_check_guid != self.bot_guid:
                # print(msg)
                YoK(f'2 - another bot with mode {self.mode} has updated {prod_id} market {buy_check_elapsed:>5.2f} minutes ago, bot_guid: {self.bot_guid}, mkt_check_guid : {buy_check_guid}')
                # return self.mkt
                return

            db_mkt_checks_buy_upd(prod_id, self.bot_guid)

        if self.mode in ('sell','full'):
            sell_check_dttm, sell_check_guid, sell_check_elapsed = db_sell_check_get(prod_id)

            msg = ''
            msg += f'{self.pair.prod_id:>15}'
            msg += f', {dttm_get()}'
            msg += f', bot_guid: {self.bot_guid}'
            msg += f', sell_check_guid : {sell_check_guid}'
            msg += f', sell_check_elapsed : {sell_check_elapsed}'
            msg += f', sell_check_dttm : {sell_check_dttm}'
            msg += f', self.pair.sell_check_dttm : {self.pair.sell_check_dttm}'
            msg += f', self.mkt.start_loop_dttm : {self.mkt.start_loop_dttm}'

            if not self.pair.sell_check_dttm:
                self.pair.sell_check_dttm = sell_check_dttm

            if sell_check_dttm >= self.mkt.start_loop_dttm and sell_check_guid != self.bot_guid:
                print(msg)
                YoK(f'1 - another bot with mode {self.mode} has updated {prod_id} market since starting...')
                YoK(f'1 - old : {self.pair.check_mkt_dttm}, new : {sell_check_dttm}, start : {self.mkt.start_loop_dttm}')
                YoK(f'1 - bot_guid: {self.bot_guid}, mkt_check_guid : {sell_check_guid}, skipping...')
                # return self.mkt
                return
            elif sell_check_elapsed < 2 and sell_check_guid != self.bot_guid:
                print(msg)
                YoK(f'2 - another bot with mode {self.mode} has updated {prod_id} market {sell_check_elapsed:>5.2f} minutes ago')
                YoK(f'2 - bot_guid: {self.bot_guid}, mkt_check_guid : {sell_check_guid}, skipping...')
                # return self.mkt
                return

            db_mkt_checks_sell_upd(prod_id, self.bot_guid)

        # formatting the mkt
        prod_id = self.pair.prod_id

        # This is only for disp_pair
        self.mkts_tot = len(self.mkt.loop_pairs)
        # lets Avoid Trading Stable Coins Against One Another
        if self.pair.base_curr_symb in self.pst.stable_coins:
                return

        # build Out Everything We Will Need in the Market
        print_adv(2)

        title_msg = f'* Pair Summary * {prod_id} * {dttm_get()} * {self.mkt.dttm_start_loop} * {self.mkt.loop_age} * {self.mkt.cnt}/{len(self.mkt.loop_pairs)} *'
        self.chrt.chart_top(bold=True)
        self.chrt.chart_mid(in_str=title_msg, bold=True)

        # build the market
        self.pair_build()

        # process the market
        self.pair_logic()

        print_adv(2)

        # return self.mkt
        return

    #<=====>#

    def pair_build(self):

        prod_id = self.pair.prod_id

        # Estimate the true buy/sell prices by looking at the order book
        pricing_cnt                    = self.pst.buy.trade_size
        max_poss_open_trade_size       = float(db_poss_open_max_trade_size_get(prod_id))
        if max_poss_open_trade_size:
            if max_poss_open_trade_size > pricing_cnt:
                pricing_cnt = max_poss_open_trade_size

        self.pair.prc_mkt              = self.pair.prc
        bid_prc, ask_prc               = cb_bid_ask_by_amt_get(pair=self.pair, buy_sell_size=pricing_cnt)
        self.pair.prc_bid              = bid_prc
        self.pair.prc_ask              = ask_prc
        self.pair.prc_dec              = cb_mkt_prc_dec_calc(self.pair.prc_bid, self.pair.prc_ask)
        self.pair.prc_buy              = round(self.pair.prc_ask, self.pair.prc_dec)
        self.pair.prc_sell             = round(self.pair.prc_bid, self.pair.prc_dec)
        self.pair.prc_range_pct        = ((self.pair.prc_buy - self.pair.prc_sell) / self.pair.prc) * 100
        self.pair.prc_buy_diff_pct     = ((self.pair.prc - self.pair.prc_buy) / self.pair.prc) * 100
        self.pair.prc_sell_diff_pct    = ((self.pair.prc - self.pair.prc_sell) / self.pair.prc) * 100

        # Market Performance
        self.pair_trade_perf_get()

        # get default settings
        self.pair.trade_perf.restricts_buy_delay_minutes   = self.pst.buy.buy_delay_minutes
        self.pair.trade_perf.restricts_open_poss_cnt_max   = self.pst.buy.open_poss_cnt_max

        # Market Strat Performances
        self.pair.trade_strat_perfs    = []
        # Market Strategy Performance
        for strat in self.pair.buy_strats:
            strat = self.pair.buy_strats[strat]
            strat = dec_2_float(strat)
            strat = AttrDictConv(d=strat)
            trade_strat_perf = self.pair_trade_strat_perf_get(strat.buy_strat_type, strat.buy_strat_name, strat.buy_strat_freq)
            self.pair.trade_strat_perfs.append(trade_strat_perf)
        trade_strat_perfs_sorted = sorted(self.pair.trade_strat_perfs, key=lambda x: x["gain_loss_amt"], reverse=True)
        self.pair.trade_strat_perfs = trade_strat_perfs_sorted


    #<=====>#

    def pair_trade_perf_get(self):

        symb = self.pair.symb
        prod_id = self.pair.prod_id

        # Build to Defaults
        trade_perf = {}
        trade_perf['symb']                          = symb
        trade_perf['prod_id']                       = prod_id
        trade_perf['tot_cnt']                       = 0
        trade_perf['win_cnt']                       = 0
        trade_perf['lose_cnt']                      = 0
        trade_perf['win_pct']                       = 0
        trade_perf['lose_pct']                      = 0
        trade_perf['age_mins']                      = 0
        trade_perf['age_hours']                     = 0
        trade_perf['bo_elapsed']                    = 9999
        trade_perf['pos_elapsed']                   = 9999
        trade_perf['last_elapsed']                  = 0
        trade_perf['tot_out_cnt']                   = 0
        trade_perf['tot_in_cnt']                    = 0
        trade_perf['buy_fees_cnt']                  = 0
        trade_perf['sell_fees_cnt_tot']             = 0
        trade_perf['fees_cnt_tot']                  = 0
        trade_perf['buy_cnt']                       = 0
        trade_perf['sell_cnt_tot']                  = 0
        trade_perf['hold_cnt']                      = 0
        trade_perf['pocket_cnt']                    = 0
        trade_perf['clip_cnt']                      = 0
        trade_perf['sell_order_cnt']                = 0
        trade_perf['sell_order_attempt_cnt']        = 0
        trade_perf['val_curr']                      = 0
        trade_perf['val_tot']                       = 0
        trade_perf['win_amt']                       = 0
        trade_perf['lose_amt']                      = 0
        trade_perf['gain_loss_amt']                 = 0
        trade_perf['gain_loss_amt_net']             = 0
        trade_perf['gain_loss_pct']                 = 0
        trade_perf['gain_loss_pct_hr']              = 0
        trade_perf['gain_loss_pct_day']             = 0
        trade_perf = AttrDictConv(d=trade_perf)

        # Get From Database
        tp = db_view_trade_perf_get_by_prod_id(prod_id)
        tp = dec_2_float(tp)
        tp = AttrDictConv(d=tp)
        if tp:
            for k in tp:
                if tp[k]:
                    trade_perf[k] = tp[k]

        # Get elapsed minues since last buy
        r = db_mkt_elapsed_get(prod_id)
        trade_perf.bo_elapsed   = r[0]
        trade_perf.pos_elapsed  = r[1]
        trade_perf.last_elapsed = r[2]

        # Get count of open positions
        open_poss = db_pos_open_get_by_prod_id(prod_id)
        trade_perf.open_poss_cnt = len(open_poss)

        self.pair.trade_perf = trade_perf



    #<=====>#

    def pair_trade_strat_perf_get(self, buy_strat_type, buy_strat_name, buy_strat_freq):

        symb = self.pair.symb
        prod_id = self.pair.prod_id

        trade_strat_perf = {}
        trade_strat_perf['symb']                = symb
        trade_strat_perf['prod_id']             = prod_id
        trade_strat_perf['buy_strat_type']      = buy_strat_type
        trade_strat_perf['buy_strat_name']      = buy_strat_name
        trade_strat_perf['buy_strat_freq']      = buy_strat_freq
        trade_strat_perf['tot_cnt']             = 0
        trade_strat_perf['open_cnt']            = 0
        trade_strat_perf['close_cnt']           = 0
        trade_strat_perf['win_cnt']             = 0
        trade_strat_perf['lose_cnt']            = 0
        trade_strat_perf['win_pct']             = 0
        trade_strat_perf['lose_pct']            = 0
        trade_strat_perf['age_hours']           = 0
        trade_strat_perf['tot_out_cnt']         = 0
        trade_strat_perf['tot_in_cnt']          = 0
        trade_strat_perf['fees_cnt_tot']        = 0
        trade_strat_perf['val_curr']            = 0
        trade_strat_perf['val_tot']             = 0
        trade_strat_perf['gain_loss_amt']       = 0
        trade_strat_perf['gain_loss_pct']       = 0
        trade_strat_perf['gain_loss_pct_hr']    = 0
        trade_strat_perf['gain_loss_pct_day']   = 0
        trade_strat_perf['strat_bo_elapsed']    = 9999
        trade_strat_perf['strat_pos_elapsed']   = 9999
        trade_strat_perf['strat_last_elapsed']  = 9999

        trade_strat_perf = AttrDictConv(d=trade_strat_perf)

        recent_cnt = self.pst.buy.trade_strat_perf_recent_cnt

        msp = db_trade_strat_perf_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, recent_cnt)
        if msp:
            for k in msp:
                if msp[k]:
                    trade_strat_perf[k] = msp[k]

        trade_strat_perf.restricts_buy_strat_delay_minutes = self.mkt_settings.get_ovrd(self.pst.buy.buy_strat_delay_minutes, in_key=buy_strat_freq)
        r = db_mkt_strat_elapsed_get(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq)
        trade_strat_perf.strat_bo_elapsed   = r[0]
        trade_strat_perf.strat_pos_elapsed  = r[1]
        trade_strat_perf.strat_last_elapsed = r[2]

        return trade_strat_perf

    #<=====>#

    def pair_logic(self):

        mkt_logic_t0 = time.perf_counter()

        try:
            prod_id      = self.pair.prod_id

            if self.mode in ('buy','full'):
                self.pair = buy_strats_avail_get(self.pair, self.pst)
 
            self.pair.timings  = []

            # Market Technical Analysis
            self.pair.ta = None
            # adding this to attempt to speed up sell loop, by not calling for TA when we are not going to sell
            if self.mode in ('buy','full', 'sell'):
                t0 = time.perf_counter()
                try:
                    self.pair.ta = ta_main_new(self.pair, self.pst)
                    if not self.pair.ta:
                        WoR(f'{dttm_get()}  - Get TA ==> TA Errored and is None')
                        return
                    if self.pair.ta == 'Error!':
                        WoR(f'{dttm_get()}  - Get TA ==> {prod_id} - close prices do not match')
                        return
                except Exception as e:
                    print(f'{dttm_get()}  - Get TA ==> {prod_id} = Error : ({type(e)}){e}')
                    traceback.print_exc()
                    traceback.print_stack()
                    print_adv()
                    print(f'')
                    beep(3)
                    pass
                t1 = time.perf_counter()
                secs = round(t1 - t0, 2)
                timing_data = {'Technical Analysis': secs}
                self.pair.timings.append(timing_data)


            # Market Summary
            t0 = time.perf_counter()
            try:
                self.disp_pair()
            except Exception as e:
                print(f'{dttm_get()}  - Market Summary ==> {prod_id} = Error : ({type(e)}){e}')
                traceback.print_exc()
                traceback.print_stack()
                print_adv()
                print(f' - disp_pair')
                beep(3)
                pass
            t1 = time.perf_counter()
            secs = round(t1 - t0, 3)
            timing_data = {'Market Summary': secs}
            self.pair.timings.append(timing_data)

            # Market Buy Logic
            if self.mode in ('buy','full'):
                self.pair_logic_buy()

            # Market Sell Logic
            if self.mode in ('sell','full'):
                self.pair_logic_sell()

            # Market Database Insert
            t0 = time.perf_counter()
            db_tbl_mkts_insupd([self.pair])
            t1 = time.perf_counter()
            secs = round(t1 - t0, 2)
            timing_data = {'Market Database Insert': secs}
            self.pair.timings.append(timing_data)

        except Exception as e:
            print(f' ==> errored 2... {e}')

            print(dttm_get())
            traceback.print_exc()
            traceback.print_stack()
            print(type(e))
            print(e)
            print(f'prod_id : {self.pair.prod_id}')
            print_adv()
            print(f' -  end')
            beep(3)
            pass

        mkt_logic_t1 = time.perf_counter()
        secs = round(mkt_logic_t1 - mkt_logic_t0, 2)
        timing_data = {'Total Time': secs}
        self.pair.timings.append(timing_data)

        self.chrt.chart_mid(in_str='Timings')
        for x in self.pair.timings:
            for k,v in x.items():
                msg = cs(f'actv : {k:>50}, elapsed : {v:>6.2f}', font_color='white', bg_color='black')
                self.chrt.chart_row(in_str=msg)
        self.chrt.chart_bottom()


    #<=====>#

    def pair_logic_buy(self):

        prod_id = self.pair.prod_id

        t0 = time.perf_counter()
        if self.pst.buy.buying_on_yn == 'Y' and prod_id in self.mkt.buy_pairs:
            try:
                self.buy_new()
                self.buy_main() 
            except Exception as e:
                print(f'{dttm_get()}  - Buy Logic ==> {prod_id} = Error : ({type(e)}){e}')
                traceback.print_exc()
                traceback.print_stack()
                print_adv()
                print(f' - buy_logic')
                beep(3)
                pass
        t1 = time.perf_counter()
        secs = round(t1 - t0, 2)
        timing_data = {'Buy Logic': secs}
        self.pair.timings.append(timing_data)
        if secs >= 5:
            msg = cs(f'buy_logic for {prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')


    #<=====>#

    def pair_logic_sell(self):

        prod_id = self.pair.prod_id

        t0 = time.perf_counter()
        if self.pst.sell.selling_on_yn == 'Y':
            try:
                self.pair.open_poss = db_pos_open_get_by_prod_id(prod_id)
                if len(self.pair.open_poss) > 0:
                    self.sell_logic()
            except Exception as e:
                print(f'{dttm_get()}  - Sell Logic ==> {prod_id} = Error : ({type(e)}){e}')
                traceback.print_exc()
                traceback.print_stack()
                print_adv()
                print(f' -  sell_logic')
                beep(3)
                pass
        t1 = time.perf_counter()
        secs = round(t1 - t0, 2)
        timing_data = {'Sell Logic': secs}
        self.pair.timings.append(timing_data)


    #<=====>#

    def buy_new(self):

        self.buy                            = AttrDict()
        for k, v in self.pair.items():
            self.buy[k] = v
        self.buy.class_name                 = 'BUY'
        self.buy.symb                       = self.mkt.symb
        self.buy.trade_perf                 = self.pair.trade_perf
        self.buy.trade_strat_perfs          = self.pair.trade_strat_perfs
        self.buy.ta                         = self.pair.ta
        self.buy.buy_strats                 = buy_strats_get()
        self.buy.reserve_locked_tf          = True
        self.buy.show_buy_header_tf         = True
        self.buy.test_txn_yn                = 'N'
        self.buy.test_reason                = ''
        self.buy.buy_signals                = []
        self.buy.reason                     = ''
        self.buy.buy_yn                     = '*'
        self.buy.buy_deny_yn                = 'N'
        self.buy.wait_yn                    = 'Y'

        self.disp_buy_header()


    #<=====>#

    def buy_main(self):

        if self.buy.prod_id == 'BTC-USDC':
            speak("BTC - buy logic")
        elif self.buy.prod_id == 'ETH-USDC':
            speak("ETH - buy logic")    
        elif self.buy.prod_id == 'SOL-USDC':
            speak("SOL - buy logic")    
        elif self.buy.prod_id == 'SUI-USDC':
            speak("SUI - buy logic")    
        elif self.buy.prod_id == 'XRP-USDC':
            speak("XRP - buy logic")        


        # Returns
        # skip buy logic if the prod_id not in the buy_pairs (ie it has positions to sell)
        if self.buy.prod_id not in self.mkt.buy_pairs:
            msg = f'{self.buy.prod_id} not in buy_pairs, bypassing buy logic...'
            self.chrt.chart_row(in_str=msg, font_color='red', bg_color='white')
            return

        # skip buy logic if ta is not present
        if not self.buy.ta:
            msg = f'{self.buy.prod_id} was not successful collecting ta, bypassing buy logic...'
            self.chrt.chart_row(in_str=msg, font_color='red', bg_color='white')
            return

        self.buy_logic_mkt_boosts()

        # loop throug all buy tests
        for trade_strat_perf in self.buy.trade_strat_perfs:
#            self.chrt.chart_mid(font_color='blue', bg_color='white')
#            print_adv(2)
#            print(trade_strat_perf)

#            time.sleep(0.1)
            self.buy.trade_strat_perf                          = trade_strat_perf

            # format trade_strat_perf
            self.buy.trade_strat_perf                          = dec_2_float(self.buy.trade_strat_perf)
            self.buy.trade_strat_perf                          = AttrDictConv(d=self.buy.trade_strat_perf)

            # set default values
            self.buy.buy_yn                   = 'N'
            self.buy.buy_deny_yn              = 'N'
            self.buy.wait_yn                  = 'Y'
            self.buy.show_tests_yn            = 'N'

            self.buy.all_passes                 = []
            self.buy.all_fails                  = []
            self.buy.all_boosts                 = []
            self.buy.all_limits                 = []
            self.buy.all_denies                 = []
            self.buy.all_cancels                = []
            self.buy.all_test_reasons           = []
            self.buy.all_maxes                  = []

            # default trade size & open position max
            self.buy.trade_strat_perf.trade_size                    = self.pst.buy.trade_size
            self.buy.trade_strat_perf.restricts_strat_open_cnt_max  = self.pst.buy.strat_open_cnt_max 

            # get strat performance boots
            # adjusts trade size & open position max
            self.buy_logic_strat_boosts()

            self.buy.pst = self.pst
            # perform buy strategy checks
            self.buy, self.pair.ta = buy_strats_check(self.buy, self.pair.ta, self.pst)
            del self.buy['pst']

            # print(f'self.buy.all_passes       : {self.buy.all_passes}')
            # print(f'self.buy.all_fails        : {self.buy.all_fails}')
            # print(f'self.buy.all_boosts       : {self.buy.all_boosts}')
            # print(f'self.buy.all_limits       : {self.buy.all_limits}')
            # print(f'self.buy.all_denies       : {self.buy.all_denies}')
            # print(f'self.buy.all_cancels      : {self.buy.all_cancels}')
            # print(f'self.buy.all_test_reasons : {self.buy.all_test_reasons}')
            # print(f'self.buy.all_maxes        : {self.buy.all_maxes}')

            # display
            self.disp_buy()

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
                    self.buy = buy_strats_deny(self.buy)

                if self.buy.buy_deny_yn == 'N':
                    self.buy_size_budget_calc()

            dttm = dttm_get()

            special_prod_ids = self.pst.buy.special_prod_ids
            if self.buy.prod_id in special_prod_ids:
                if self.buy.test_txn_yn == 'Y':
                    print(cs(f'{self.buy.prod_id} in specials, flipping from test to live!!!', 'white', 'green'))
                    self.buy.test_txn_yn = 'N'


            if self.buy.buy_yn == 'Y':
#                msg = f'bot.buy_logic !!! * buy_yn : {self.buy.buy_yn} * buy_deny_yn : {self.buy.buy_deny_yn} * test_txn_yn : {self.buy.test_txn_yn}'
#                self.chrt.chart_row(in_str=msg, font_color='white', bg_color='magenta')

                if self.mst.paper_trades_only_yn == 'Y':
                    self.buy.test_txn_yn = 'Y'
                    self.buy.test_reason = f"paper_trades_only_yn = {self.mst.paper_trades_only_yn}"


                if self.buy.test_txn_yn == 'Y':
                    self.disp_budget()

                if self.buy.test_txn_yn == 'Y':
                    if self.buy.buy_deny_yn == 'N':
                        if self.pst.buy_test_txns.test_txns_on_yn == 'Y':
                            self.buy.show_buy_header_tf = True
                            txt = '!!! BUY * TEST * !!!'
                            m = self.spacer + cs('{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f} * STRAT: {}', font_color='white', bg_color='green')
                            msg = m.format(dttm, txt, self.buy.prc_buy, self.buy.trade_strat_perf.trade_size, self.budget[self.mkt.symb].bal_avail, self.buy.buy_strat_name)
                            self.chrt.chart_row(in_str=msg, font_color='white', bg_color='green')
                            self.chrt.chart_row(in_str=msg, font_color='white', bg_color='green')
                            self.chrt.chart_row(in_str=msg, font_color='white', bg_color='green')
                            self.buy_test()
                            msg = f'test buying {self.buy.base_curr_symb} for {self.buy.trade_strat_perf.trade_size} {self.buy.quote_curr_symb} with strategy {self.buy.buy_strat_name} on the {self.buy.buy_strat_freq} timeframe'
                            self.buy.all_test_reasons.append(msg)

                else:
                    if self.buy.buy_deny_yn == 'N':
                        self.buy_live()
                        self.buy.show_buy_header_tf = True
                        txt = '!!! BUY !!!'
                        m = self.spacer + cs('{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f} * STRAT: {}', font_color='white', bg_color='green')
                        msg = m.format(dttm, txt, self.buy.prc_buy, self.buy.trade_strat_perf.trade_size, self.budget[self.mkt.symb].bal_avail, self.buy.buy_strat_name)
                        self.chrt.chart_row(in_str=msg, font_color='white', bg_color='green')
                        self.chrt.chart_row(in_str=msg, font_color='white', bg_color='green')
                        self.chrt.chart_row(in_str=msg, font_color='white', bg_color='green')
    #                    symb = prod_id.split(',')[0]
                        msg = f'buying {self.buy.base_curr_symb} for {self.buy.trade_strat_perf.trade_size} {self.buy.quote_curr_symb} with strategy {self.buy.buy_strat_name} on the {self.buy.buy_strat_freq} timeframe'
                        self.chrt.chart_row(in_str=msg, font_color='white', bg_color='green')

                        if self.pst.speak_yn == 'Y': speak(msg)

                        self.buy.trade_perf.bo_elapsed        = 0
                        self.buy.trade_perf.pos_elapsed       = 0
                        self.buy.trade_perf.last_elapsed      = 0
                        self.buy.trade_perf.open_poss_cnt     += 1

                        self.budget[self.mkt.symb].bal_avail                -= self.buy.trade_strat_perf.trade_size
                        self.budget[self.mkt.symb].spendable_amt            -= self.buy.trade_strat_perf.trade_size

                        msg = f'{self.buy.quote_curr_symb} * Balance : ${self.budget[self.mkt.symb].bal_avail:>.2f} * Reserve : ${self.budget[self.mkt.symb].reserve_amt:>.2f} * Spendable : ${self.budget[self.mkt.symb].spendable_amt:>.2f} * '
                        self.chrt.chart_row(in_str=msg, font_color='white', bg_color='green')

            elif self.buy.buy_yn == 'N' :
                txt = '!!! WAIT !!!'
                m = self.spacer + cs('{} * {} * CURR: ${:>16.8f} * SIZE: ${:>16.8f} * BAL: ${:>16.8f}', font_color='white', bg_color='black')
                msg = m.format(dttm, txt, self.buy.prc_buy, self.buy.trade_strat_perf.trade_size, self.budget[self.mkt.symb].bal_avail)
#                self.chrt.chart_row(in_str=msg, font_color='blue', bg_color='white')

            self.disp_buy_passes()
            self.disp_buy_fails()
            self.disp_buy_boosts()
            self.disp_buy_limits()
            self.disp_buy_denies()
            self.disp_buy_cancels()
            self.disp_buy_maxes()
            self.disp_buy_test_reasons()

            self.buy_save()

            # self.chrt.chart_row(in_str=f' ==> {self.buy.buy_strat_name} {self.buy.buy_strat_freq} ==> self.buy_yn : {self.buy.buy_yn}, self.buy_deny_yn : {self.buy.buy_deny_yn}, self.buy.wait_yn : {self.buy.wait_yn}, self.buy.test_txn_yn : {self.buy.test_txn_yn}, self.buy.test_reason : {self.buy.test_reason}')

        self.chrt.chart_mid(bold=True)


        # fix me
        # this should return self.mkt & self.pair, if anything in self.pair is even changed... 
#        return self.mkt, buy
        return

    #<=====>#

    def buy_logic_mkt_boosts(self):

        # get default open position max for strat
        # add double override logic strat + prod
        # fixme
        self.buy.trade_perf.restricts_open_poss_cnt_max = self.pst.buy.open_poss_cnt_max 

        # Open Position Count Checks Performance Based
        # Boost allowed max positions based upon past performance
        if self.buy.trade_perf.tot_cnt >= 5 and self.buy.trade_perf.gain_loss_pct_day > 0.1:
            self.buy.trade_perf.restricts_open_poss_cnt_max *= 2
            if self.pst.buy.show_boosts_yn == 'Y':
                msg = f'{self.buy.prod_id} has {self.buy.trade_perf.tot_cnt} trades with performance {self.buy.trade_perf.gain_loss_pct_day:>.8f} % < 0 % boosting allowed open pos ... '
                self.buy.all_boosts.append(msg)

    #<=====>#

    def buy_logic_strat_boosts(self):

        prod_id                       = self.buy.prod_id
        self.buy.buy_strat_type       = self.buy.trade_strat_perf.buy_strat_type
        self.buy.buy_strat_name       = self.buy.trade_strat_perf.buy_strat_name
        self.buy.buy_strat_freq       = self.buy.trade_strat_perf.buy_strat_freq

        # get default open position max for strat
        # add double override logic strat + prod
        # fixme
        self.buy.trade_strat_perf.restricts_strat_open_cnt_max = self.pst.buy.strat_open_cnt_max 

        # Open Position Count Checks Performance Based
        # Boost allowed max positions based upon past performance
        if self.buy.trade_strat_perf.tot_cnt >= 25 and self.buy.trade_strat_perf.gain_loss_pct_day > 1:
            self.buy.trade_strat_perf.restricts_strat_open_cnt_max *= 2
            if self.pst.buy.show_boosts_yn == 'Y':
                msg = f'{self.buy.prod_id} {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} has {self.buy.trade_strat_perf.tot_cnt} trades with performance {self.buy.trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % boosting allowed open pos ... '
                self.buy.all_boosts.append(msg)

        # get default open position max for strat
        # Assign Min Value For New Market + Strat with little history or poor performance
        trade_size                 = self.buy.quote_size_min * self.pst.buy.trade_size_min_mult
        tests_min                  = self.pst.buy.strats[self.buy.buy_strat_name].tests_min[self.buy.buy_strat_freq] 
        boost_tests_min            = self.pst.buy.strats[self.buy.buy_strat_name].boost_tests_min[self.buy.buy_strat_freq] 

        # give default value to strat with some history and positive impact
        if self.buy.trade_strat_perf.tot_cnt >= tests_min and self.buy.trade_strat_perf.gain_loss_pct_day > 0:
            trade_size             = self.pst.buy.trade_size 
        # give default value to strat with some history and positive impact
        elif self.buy.trade_strat_perf.tot_cnt >= 5 and self.buy.trade_strat_perf.win_pct >= 75:
            trade_size             = self.pst.buy.trade_size 

        # Kid has potential, lets give it a little more earlier
        if self.buy.trade_strat_perf.tot_cnt >= 3 and self.buy.trade_strat_perf.gain_loss_pct_day > 0.003125:
            trade_size             *= 2
        # Boost those with proven track records
        if self.buy.trade_strat_perf.tot_cnt >= tests_min and self.buy.trade_strat_perf.gain_loss_pct_day > 0.0625:
            trade_size             *= 2
        # Boost those with proven track records
        if self.buy.trade_strat_perf.tot_cnt >= boost_tests_min and self.buy.trade_strat_perf.gain_loss_pct_day > 0.125:
            trade_size             *= 2
        # Boost those with proven track records
        if self.buy.trade_strat_perf.tot_cnt >= boost_tests_min and self.buy.trade_strat_perf.gain_loss_pct_day > 0.25:
            trade_size             *= 2
        # Boost those with proven track records
        if self.buy.trade_strat_perf.tot_cnt >= boost_tests_min and self.buy.trade_strat_perf.gain_loss_pct_day > 0.5:
            trade_size             *= 2
        # Boost those with proven track records
        if self.buy.trade_strat_perf.tot_cnt >= boost_tests_min and self.buy.trade_strat_perf.gain_loss_pct_day > 1:
            trade_size             *= 2
        # Boost those with proven track records
        if self.buy.trade_strat_perf.tot_cnt >= boost_tests_min and self.buy.trade_strat_perf.gain_loss_pct_day > 2:
            trade_size             *= 2

        if self.pst.buy.show_boosts_yn == 'Y':
            msg = f'{self.buy.prod_id} {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} has {self.buy.trade_strat_perf.tot_cnt} trades with performance {self.buy.trade_strat_perf.gain_loss_pct_day:>.8f} % < 0 % setting trade_size ${trade_size} ... '
            self.buy.all_boosts.append(msg)

        if trade_size > self.pst.buy.trade_size_max:
            msg = f'{self.buy.prod_id} {self.buy.buy_strat_name} - {self.buy.buy_strat_freq} setting trade_size ${trade_size} to cap max ${self.pst.buy.trade_size_max}... '
            trade_size = self.pst.buy.trade_size_max
            self.buy.all_boosts.append(msg)

        # assign final trade_size
        self.buy.trade_strat_perf.trade_size = trade_size

    #<=====>#

    def buy_logic_deny(self):
        pass

    #<=====>#

    def buy_logic_mkt_deny(self):
        pass

    #<=====>#

    def buy_logic_strat_deny(self):

        prod_id              = self.buy.prod_id
        prod_open_poss_cnt   = self.buy.trade_perf.open_poss_cnt
        strat_open_poss_cnt  = self.buy.trade_strat_perf.open_cnt
        buy_strat_type       = self.buy.trade_strat_perf.buy_strat_type
        buy_strat_name       = self.buy.trade_strat_perf.buy_strat_name
        buy_strat_freq       = self.buy.trade_strat_perf.buy_strat_freq
        total_trades_cnt     = self.buy.trade_strat_perf.tot_cnt
        gain_loss_pct_day    = self.buy.trade_strat_perf.gain_loss_pct_day

        mkts_open_cnt        = db_mkts_open_cnt_get(mkt=self.mkt.symb)

        special_prod_ids     = self.pst.buy.special_prod_ids
        test_txns_on_yn      = self.pst.buy_test_txns.test_txns_on_yn
        test_txns_min        = self.pst.buy_test_txns.test_txns_min
        test_txns_max        = self.pst.buy_test_txns.test_txns_max
        mkts_open_max        = self.pst.buy.mkts_open_max
        self.buy.test_txn_yn = 'N'

        self.buy.buy_deny_yn               = 'N'

        if self.pst.buy.buying_on_yn == 'N' :
            msg = f'buying has been turned off in settings...'
            self.buy.all_denies.append(msg)
            self.buy.buy_deny_yn = 'Y'
            return

        if test_txns_on_yn == 'Y' and total_trades_cnt <= test_txns_min:
            msg = f'{self.buy.prod_id} {buy_strat_name} - {buy_strat_freq} has {total_trades_cnt} trades  setting test mode ... '
            self.buy.all_test_reasons.append(msg)
            self.buy.test_reason = msg
            self.buy.test_txn_yn = 'Y'
        elif test_txns_on_yn == 'Y' and total_trades_cnt <= test_txns_max and gain_loss_pct_day < 0:
            msg = f'{self.buy.prod_id} {buy_strat_name} - {buy_strat_freq} has {total_trades_cnt} trades with performance {gain_loss_pct_day:>.8f} % < 0 % setting test mode... '
            self.buy.all_test_reasons.append(msg)
            self.buy.test_reason = msg
            self.buy.test_txn_yn = 'Y'
        elif test_txns_on_yn == 'Y' and total_trades_cnt > test_txns_max and gain_loss_pct_day < 0:
            msg = f'{self.buy.prod_id} {buy_strat_name} - {buy_strat_freq} has {total_trades_cnt} trades with performance {gain_loss_pct_day:>.8f} % < 0 % reducing allowed open pos, max pos 1 ... '
            self.buy.all_limits.append(msg)
            self.buy.trade_strat_perf.restricts_strat_open_cnt_max = 1
            self.buy.test_reason = msg
            self.buy.test_txn_yn = 'Y'
        elif gain_loss_pct_day < 0:
            msg = f'{self.buy.prod_id} {buy_strat_name} - {buy_strat_freq} has {total_trades_cnt} trades with performance {gain_loss_pct_day:>.8f} % < 0 % reducing allowed open pos, max pos 1 ... '
            self.buy.all_test_reasons.append(msg)
            self.buy.test_reason = msg
            self.buy.trade_strat_perf.restricts_strat_open_cnt_max = 1
            self.buy.test_txn_yn = 'Y'


        # Market Is Set To Sell Immediately
        if prod_id in self.pst.sell.force_sell.prod_ids:
            msg = f'{self.buy.prod_id} is in the forced_sell.prod_ids settings, and would instantly sell...'
            self.buy.all_denies.append(msg)
            self.buy.buy_deny_yn = 'Y'


        if self.buy.test_txn_yn == 'N':

            # Elapsed Since Last Market Buy
            if self.buy.trade_perf.restricts_buy_delay_minutes != 0 and self.buy.trade_perf.last_elapsed <= self.buy.trade_perf.restricts_buy_delay_minutes:
                msg = f'{self.buy.prod_id} last market buy was {self.buy.trade_perf.last_elapsed} minutes ago, waiting until {self.buy.trade_perf.restricts_buy_delay_minutes} minutes...'
                self.buy.all_denies.append(msg)
                self.buy.buy_deny_yn = 'Y'

            # open position counts in this market
            if mkts_open_cnt >= mkts_open_max:
                msg = f'{self.buy.prod_id} maxed out {self.mkt.symb} market, {mkts_open_cnt} of max : {mkts_open_max}...'
                self.buy.all_denies.append(msg)
                self.buy.buy_deny_yn = 'Y'
                if test_txns_on_yn == 'Y':
                    self.buy.test_txn_yn = 'Y'
                    self.buy.test_reason = f'flipping to test since {msg}'

            # Open Position Count Checks
            if prod_open_poss_cnt >= self.buy.trade_perf.restricts_open_poss_cnt_max:
                msg = f'{self.buy.prod_id} maxed out {prod_open_poss_cnt} allowed positions in this product, max : {self.buy.trade_perf.restricts_open_poss_cnt_max}, bypassing buy logic...'
                self.buy.all_limits.append(msg)
                self.buy.buy_deny_yn = 'Y'
                if test_txns_on_yn == 'Y':
                    self.buy.test_txn_yn = 'Y'
                    self.buy.test_reason = f'flipping to test since {msg}'

            # Max Positions by Strat
            if strat_open_poss_cnt >= self.buy.trade_strat_perf.restricts_strat_open_cnt_max:
                msg = f'{self.buy.prod_id} {buy_strat_name} - {buy_strat_freq} has {self.buy.trade_strat_perf.open_cnt} open with max {self.buy.trade_strat_perf.restricts_strat_open_cnt_max} in this strat... '
                self.buy.all_maxes.append(msg)
                self.buy.buy_deny_yn = 'Y'
                if test_txns_on_yn == 'Y':
                    self.buy.test_txn_yn = 'Y'
                    self.buy.test_reason = f'flipping to test since {msg}'


            # Market Is Set To Limit Only on Coinbase
            if self.buy.mkt_limit_only_tf == 1:
                msg = f'{self.buy.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!'
                self.buy.all_denies.append(msg)
                self.buy.buy_deny_yn = 'Y'
                if test_txns_on_yn == 'Y':
                    self.buy.test_txn_yn = 'Y'
                    self.buy.test_reason = msg

            # Very Large Bid Ask Spread
            if self.buy.prc_range_pct >= 2:
                msg = f'has a price range variance of {self.buy.prc_range_pct}, this price range looks like trouble... skipping buy'
                self.buy.all_denies.append(msg)
                self.buy.buy_deny_yn = 'Y'
                if test_txns_on_yn == 'Y':
                    self.buy.test_txn_yn = 'Y'
                    self.buy.test_reason = msg

        # this keeps the test trades from firing every loop... it was making hundreds of test trades
        # time delay between same prod_id & strat buy in minutes..
        if self.buy.trade_strat_perf.restricts_buy_strat_delay_minutes != 0 and self.buy.trade_strat_perf.strat_last_elapsed < self.buy.trade_strat_perf.restricts_buy_strat_delay_minutes:
            msg = f'{self.buy.prod_id} last strat {buy_strat_name} - {self.buy.trade_strat_perf.buy_strat_freq} buy was {self.buy.trade_strat_perf.strat_last_elapsed} minutes ago, waiting until {self.buy.trade_strat_perf.restricts_buy_strat_delay_minutes} minutes...'
            self.buy.all_denies.append(msg)
            self.buy.buy_deny_yn = 'Y'


    #<=====>#

    def buy_size_budget_calc(self):

        self.budget[self.mkt.symb].pair_spent_amt            = 0
        self.budget[self.mkt.symb].pair_spent_up_amt         = 0
        self.budget[self.mkt.symb].pair_spent_dn_amt         = 0
        self.budget[self.mkt.symb].pair_spent_pct            = 0
        self.budget[self.mkt.symb].pair_spent_up_pct         = 0
        self.budget[self.mkt.symb].pair_spent_dn_pct         = 0

        self.budget[self.mkt.symb].tot_shares = 0
        # print(type(self.mst))
        # pprint(self.mst)
        # print(type(self.mst.budget))
        # pprint(self.mst.budget)
        # print(type(self.mst.budget.mkt_shares))
        # pprint(self.mst.budget.mkt_shares)
        if self.mst.budget.mkt_shares.shares_or_pcts == 'shares':
            for x in self.mkt.loop_pairs:
                prod_id = x['prod_id']
                if prod_id in self.mst.budget.mkt_shares:
                    self.budget[self.mkt.symb].tot_shares += self.mst.budget.mkt_shares[prod_id] 
                else:
                    self.budget[self.mkt.symb].tot_shares += self.mst.budget.mkt_shares['***'] 

            self.budget[self.mkt.symb].pair_spend_max_amt        = self.budget[self.mkt.symb].spend_max_amt * (self.pst.budget.mkt_shares / self.budget[self.mkt.symb].tot_shares)
            self.budget[self.mkt.symb].pair_spend_up_max_amt     = self.budget[self.mkt.symb].pair_spend_max_amt * (self.pst.budget.spend_up_max_pct / self.budget[self.mkt.symb].tot_shares)
            self.budget[self.mkt.symb].pair_spend_dn_max_amt     = self.budget[self.mkt.symb].pair_spend_max_amt * (self.pst.budget.spend_dn_max_pct / self.budget[self.mkt.symb].tot_shares)
        else:
            self.budget[self.mkt.symb].pair_spend_max_amt        = self.budget[self.mkt.symb].spend_max_amt * (self.pst.budget.mkt_shares / 100)
            self.budget[self.mkt.symb].pair_spend_up_max_amt     = self.budget[self.mkt.symb].pair_spend_max_amt * (self.pst.budget.spend_up_max_pct / 100)
            self.budget[self.mkt.symb].pair_spend_dn_max_amt     = self.budget[self.mkt.symb].pair_spend_max_amt * (self.pst.budget.spend_dn_max_pct / 100)

        # Get Pair Data
        pair_spent_data                = db_pair_spent(self.buy.prod_id)
        pair_spent_data                = dec_2_float(pair_spent_data)
        pair_spent_data                = AttrDictConv(d=pair_spent_data)

        # cp('************************************************************************************','black','yellow')
        # speak('check screen now!!!')
        # print('2176')
        # print(pair_spent_data)
        # speak('check screen now!!!')
        # speak('check screen now!!!')
        # cp('************************************************************************************','black','yellow')

        if pair_spent_data:
            self.budget[self.mkt.symb].pair_open_cnt             = pair_spent_data.open_cnt
            self.budget[self.mkt.symb].pair_open_up_cnt          = pair_spent_data.open_up_cnt
            self.budget[self.mkt.symb].pair_open_dn_cnt          = pair_spent_data.open_dn_cnt
            self.budget[self.mkt.symb].pair_open_dn_pct          = pair_spent_data.open_up_pct
            self.budget[self.mkt.symb].pair_open_dn_pct          = pair_spent_data.open_dn_pct

            self.budget[self.mkt.symb].pair_spent_amt            = pair_spent_data.spent_amt
            self.budget[self.mkt.symb].pair_spent_pct            = round((self.budget[self.mkt.symb].pair_spent_amt / self.budget[self.mkt.symb].pair_spend_max_amt) * 100, 2)
            self.budget[self.mkt.symb].pair_spent_up_amt         = pair_spent_data.spent_up_amt
            self.budget[self.mkt.symb].pair_spent_up_pct         = round((self.budget[self.mkt.symb].pair_spent_up_amt / self.budget[self.mkt.symb].pair_spend_up_max_amt) * 100, 2)
            self.budget[self.mkt.symb].pair_spent_dn_amt         = pair_spent_data.spent_dn_amt
            self.budget[self.mkt.symb].pair_spent_dn_pct         = round((self.budget[self.mkt.symb].pair_spent_dn_amt / self.budget[self.mkt.symb].pair_spend_dn_max_amt) * 100, 2)

        color_changed_tf = False
        disp_font_color = 'white'
        disp_bg_color   = 'red'
        # adjust the strat trade size based upon spendable amt
        self.buy.trade_strat_perf.target_trade_size = self.buy.trade_strat_perf.trade_size

        self.buy.trade_strat_perf.trade_size = self.buy.quote_size_min
        while self.buy.trade_strat_perf.trade_size <= self.buy.trade_strat_perf.target_trade_size - 1:
            if not color_changed_tf:
                if self.buy.trade_strat_perf.trade_size > self.buy.quote_size_min:
                    disp_bg_color   = 'blue'
                    color_changed_tf = True

            # General Spending
            if self.budget[self.mkt.symb].spent_amt + self.buy.trade_strat_perf.trade_size + self.buy.quote_size_min > self.budget[self.mkt.symb].spend_max_amt:
                msg = f'mkt.budget.spent_amt : {self.budget[self.mkt.symb].spent_amt:>12.6f} + trade_size  : {self.buy.trade_strat_perf.trade_size:>12.6f} + quote_size_min  : {self.buy.quote_size_min:>12.6f} + > self.budget[self.mkt.symb].spend_max_amt : {self.budget[self.mkt.symb].spend_max_amt:>12.6f}'
                self.buy.all_maxes.append(msg)
                break

            # Pair Spending
            if self.budget[self.mkt.symb].pair_spent_amt + self.buy.trade_strat_perf.trade_size + self.buy.quote_size_min > self.budget[self.mkt.symb].pair_spend_max_amt:
                msg = f'mkt.budget.pair_spent_amt : {self.budget[self.mkt.symb].pair_spent_amt:>12.6f} + trade_size : {self.buy.trade_strat_perf.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget[self.mkt.symb].pair_spend_max_amt : {self.budget[self.mkt.symb].pair_spend_max_amt:>12.6f}'
                self.buy.all_maxes.append(msg)
                break

            # Up Strategies
            if self.buy.trade_strat_perf.buy_strat_type == 'up':

                # General Up Strategy Spending
                if self.budget[self.mkt.symb].spent_up_amt + self.buy.trade_strat_perf.trade_size + self.buy.quote_size_min > self.budget[self.mkt.symb].spend_up_max_amt:
                    msg = f'mkt.budget.spent_up_amt : {self.budget[self.mkt.symb].spent_up_amt:>12.6f} + trade_size : {self.buy.trade_strat_perf.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget[self.mkt.symb].spend_up_max_amt : {self.budget[self.mkt.symb].spend_up_max_amt:>12.6f}'
                    msg = cs(msg, font_color=disp_font_color, bg_color=disp_bg_color)
                    self.buy.all_maxes.append(msg)
                    break

                # Pair Up Strategy Spending
                if self.budget[self.mkt.symb].pair_spent_up_amt + self.buy.trade_strat_perf.trade_size + self.buy.quote_size_min > self.budget[self.mkt.symb].pair_spend_up_max_amt:
                    msg = f'mkt.budget.pair_spent_up_amt : {self.budget[self.mkt.symb].pair_spent_up_amt:>12.6f} + trade_size : {self.buy.trade_strat_perf.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget[self.mkt.symb].pair_spend_up_max_amt : {self.budget[self.mkt.symb].pair_spend_up_max_amt:>12.6f}'
                    self.buy.all_maxes.append(msg)
                    break

            # Down Strategies
            if self.buy.trade_strat_perf.buy_strat_type == 'dn':

                # General Dn Strategy Spending
                if self.budget[self.mkt.symb].spent_dn_amt + self.buy.trade_strat_perf.trade_size + self.buy.quote_size_min > self.budget[self.mkt.symb].spend_dn_max_amt:
                    msg = f'mkt.budget.spent_dn_amt : {self.budget[self.mkt.symb].spent_dn_amt:>12.6f} + trade_size : {self.buy.trade_strat_perf.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget[self.mkt.symb].spend_dn_max_amt : {self.budget[self.mkt.symb].spend_dn_max_amt:>12.6f}'
                    self.buy.all_maxes.append(msg)
                    break

                # Pair Dn Strategy Spending
                if self.budget[self.mkt.symb].pair_spent_dn_amt + self.buy.trade_strat_perf.trade_size + self.buy.quote_size_min > self.budget[self.mkt.symb].pair_spend_dn_max_amt:
                    msg = f'mkt.budget.pair_spent_dn_amt : {self.budget[self.mkt.symb].pair_spent_dn_amt:>12.6f} + trade_size : {self.buy.trade_strat_perf.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget[self.mkt.symb].pair_spend_dn_max_amt : {self.budget[self.mkt.symb].pair_spend_dn_max_amt:>12.6f}'
                    self.buy.all_maxes.append(msg)
                    break

            # Available Funds
            if self.buy.trade_strat_perf.trade_size + self.buy.quote_size_min > self.budget[self.mkt.symb].spendable_amt:
                msg = f'trade_size : {self.buy.trade_strat_perf.trade_size:>12.6f} + quote_size_min : {self.buy.quote_size_min:>12.6f} + > self.budget[self.mkt.symb].spendable_amt : {self.budget[self.mkt.symb].spendable_amt:>12.6f}'
                self.buy.all_maxes.append(msg)
                break

            self.buy.trade_strat_perf.trade_size += self.buy.quote_size_min

        # deny if trade size exceeds spendable amt
        if self.buy.trade_strat_perf.trade_size == self.buy.quote_size_min:
            self.buy.buy_deny_yn = 'Y'
            msg = f'{self.buy.quote_curr_symb} => budget funding => balance : {self.budget[self.mkt.symb].bal_avail:>.2f}, reserve amount : {self.budget[self.mkt.symb].reserve_amt:>.2f}, spendable amount : {self.budget[self.mkt.symb].spendable_amt:>.2f}, trade_size of {self.buy.trade_strat_perf.trade_size:>.2f}...'
            self.buy.all_cancels.append(msg)
            self.buy.test_reason = msg
            self.buy.test_txn_yn = 'Y'


    #<=====>#

    def buy_save(self):

        # Save Files
        if self.buy.buy_yn == 'Y':
            if self.pst.buy.save_files_yn == 'Y':
                fname = f"saves/{self.buy.prod_id}_BUY_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt"
                writeit(fname, '=== MKT ===')
                for k in self.buy:
                    if isinstance(self.buy[k], [str, list, dict, float, int, decimal.Decimal, datetime, time]):
                        writeit(fname, f'{k} : {self.buy[k]}')
                    else:
                        print(f'{k} : {type(self.buy[k])}')


    #<=====>#

    def buy_live(self):

        if self.pst.buy.buy_limit_yn == 'Y':
            try:
                self.ord_lmt_buy_open()
            except Exception as e:
                print(f' ==> errored... {e}')
                print(dttm_get())
                traceback.print_exc()
                traceback.print_stack()
                print(type(e))
                print(e)
                print(f' ==> buy limit order failed, attempting market... {e}')
                beep(3)
                sys.exit()
                # self.ord_mkt_buy(mkt, trade_strat_perf)
                self.ord_mkt_buy_orig()
        else:
            # self.ord_mkt_buy(mkt, trade_strat_perf)
            self.ord_mkt_buy_orig()


    #<=====>#

    def buy_test(self):

        bo = AttrDict()
        bo.test_txn_yn               = 'Y'
        bo.symb                  = self.buy.symb
        bo.prod_id               = self.buy.prod_id
        bo.buy_order_uuid        = self.gen_guid()
        bo.pos_type              = 'SPOT'
        bo.ord_stat              = 'OPEN'
        bo.buy_strat_type        = self.buy.trade_strat_perf.buy_strat_type
        bo.buy_strat_name        = self.buy.trade_strat_perf.buy_strat_name
        bo.buy_strat_freq        = self.buy.trade_strat_perf.buy_strat_freq
        bo.reason                = self.buy.reason
        bo.buy_begin_dttm        = dt.now()
        bo.buy_end_dttm          = dt.now()
        bo.buy_curr_symb         = self.buy.base_curr_symb
        bo.spend_curr_symb       = self.buy.quote_curr_symb
        bo.fees_curr_symb        = self.buy.quote_curr_symb
        bo.buy_cnt_est           = (self.buy.trade_strat_perf.target_trade_size * 0.996) / self.buy.prc_buy
        bo.buy_cnt_act           = (self.buy.trade_strat_perf.target_trade_size * 0.996) / self.buy.prc_buy
        bo.fees_cnt_act          = (self.buy.trade_strat_perf.target_trade_size * 0.004) / self.buy.prc_buy
        bo.tot_out_cnt           = self.buy.trade_strat_perf.target_trade_size
        bo.prc_buy_est           = self.buy.prc_buy
        bo.prc_buy_est           = self.buy.prc_buy
        bo.tot_prc_buy           = self.buy.prc_buy
        bo.prc_buy_slip_pct      = 0

        print(bo)

        db_tbl_buy_ords_insupd(bo)
#        time.sleep(.33)


    #<=====>#

    def sell_logic(self):

        prod_id = self.pair.prod_id
        self.pair.show_sell_header_tf = True

        sell_check_dttm = db_sell_check_get(prod_id)

        for pos_data in self.pair.open_poss:
#            print_adv(2)
            pos_data = dec_2_float(pos_data)
            pos_data = AttrDictConv(d=pos_data)
            pos_id = pos_data.pos_id
            if pos_data.pos_stat == 'OPEN':
                try:
                    sell_check_dttm, sell_check_guid, sell_check_elapsed = db_sell_check_get(prod_id)
                    msg = ''
                    msg += f'{self.pair.prod_id:>15}'
                    msg += f', {dttm_get()}'
                    msg += f', bot_guid: {self.bot_guid}'
                    msg += f', sell_check_guid : {sell_check_guid}'
                    msg += f', sell_check_elapsed : {sell_check_elapsed}'
                    msg += f', sell_check_dttm : {sell_check_dttm}'
                    msg += f', self.pair.sell_check_dttm : {self.pair.sell_check_dttm}'
                    msg += f', self.mkt.start_loop_dttm : {self.mkt.start_loop_dttm}'
                    if sell_check_guid != self.bot_guid:
                        print(msg)
                        YoK(f'2 - another bot with mode sell has updated {prod_id} market since starting..., bot_guid : {self.bot_guid}, mkt_check_guid : {sell_check_guid}  skipping...')
#                        beep()
#                        speak('sell_guid preventing double processing...')
                        break

                    self.pos_upd(pos=pos_data)
                    self.sell_pos_new(pos_data)
                    self.sell_pos_logic()
                    if self.pair.skip_to_next_tf:
                        break
                    db_tbl_poss_insupd(self.pos)
                    # self.chrt.chart_mid()
                except Exception as e:
                    print(f'{dttm_get()}  {prod_id} {pos_id}==> errored : ({type(e)}) {e}')
                    traceback.print_exc()
                    traceback.print_stack()
                    pass

        self.chrt.chart_mid(bold=True)


    #<=====>#

    def sell_pos_new(self, pos_data):

        self.pos                                = AttrDict()
        self.pos.class_name                     = 'POS'
        for k, v in pos_data.items():
            self.pos[k] = v
        self.pos.age_mins = self.pos.new_age_mins
        self.pos.symb                           = self.mkt.symb
        self.pos.sell_yn                        = 'N'
        self.pos.sell_block_yn                  = 'N'
        self.pos.hodl_yn                        = 'N'
        self.pair.ta                             = self.pair.ta
        self.pos.sell_prc                       = self.pair.prc_sell
        self.pos.sell_yn                        = 'N'
        self.pos.hodl_yn                        = 'Y'
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


    #<=====>#

    def sell_pos_logic(self):

        t0 = time.perf_counter()

        self.pair.skip_to_next_tf = False

        self.pos.bal_cnt = cb_bal_get(self.pair.base_curr_symb)
        if self.pos.bal_cnt == 0:
            self.pos.bal_cnt = cb_bal_get(self.pos.symb)
        if self.pos.bal_cnt == 0:
            print(f' => {self.pos.prod_id} balance is {self.pos.bal_cnt}...')
            beep(3)
            sys.exit()

        self.disp_sell_pos()
        db_poss_check_last_dttm_upd(self.pos.pos_id)
        self.pos.check_last_dttm = db_poss_check_last_dttm_get(self.pos.pos_id)

        # Halt And Catch Fire
        sos = db_sell_ords_get_by_pos_id(self.pos.pos_id)
        if sos:
            print(f' => Halt & Catch Fire...')
            if DictKey(sos, 'ta'): del self.pos['ta']
            if DictKey(sos, 'pair'): del self.pos['pair']
            if DictKey(sos, 'st'): del self.pos['st']
            print(f'existing sell order for pos : {self.pos.pos_id}')
            for so in sos:
                print(so)
                print('')
            beep(1)
            print('this seems to only be happening with the test orders...')
            self.pair.skip_to_next_tf = True
            print('attempting to skip to next pair...')

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
#                    self.pair.ta = ta_main_new(self.pair, self.mst)
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
                    pass
                t1 = time.perf_counter()
                secs = round(t1 - t0, 2)
                timing_data = {'Technical Analysis in Sell POS Logic': secs}
                self.pair.timings.append(timing_data)
                if secs >= 5:
                    msg = cs(f'mkt_ta_main_new for {self.pos.prod_id} - took {secs} seconds...', font_color='yellow', bg_color='orangered')
                    self.chrt.chart_row(msg)
                    self.chrt.chart_mid()

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
#                print(f'ta_high : {ta_high}')
                # this is not enough, it will only get called if we do TA
                # it will only go back 5 minutes, even if we were offline for hours/days and its an old pos
                # we have already calculated everything against this the before hitting the sell logic
                # it will be on table for the next time in bot_cls_pair.pos_upd

        if self.pos.sell_yn == 'N' and self.pair.ta:
            self.sell_pos_tests_after_ta()

        # Sell By Strat Logic - These do require TA
        if self.pos.sell_yn == 'N' and self.pair.ta:
            self.pair, self.pos, self.pair.ta = sell_strats_check(self.pair, self.pos, self.pair.ta, self.pst)

        # This is a blocker that will only be checked for TA sells
        if self.pos.sell_yn == 'Y':
            if self.pos.sell_force_yn == 'N':
                if self.pos.sell_block_yn == 'N':
                    if self.pair.ta:
                        self.sell_pos_deny_nwe_green()
                        self.sell_pos_deny_all_green()

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

        if self.pos.sell_yn == 'Y' and self.pos.sell_block_yn == 'N':
            if self.pos.test_txn_yn == 'N':
                self.sell_pos_live()
                if self.pos.error_tf:
                    play_thunder()
                    self.pos.sell_yn = 'N'
                    if self.pst.speak_yn == 'Y': speak(self.pos.reason)
                else:
                    if self.pos.gain_loss_amt > 0:
                        msg = f'WIN, selling {self.pos.base_curr_symb} for {round(self.pos.gain_loss_amt_est,2)} dollars '
                        if self.pst.speak_yn == 'Y': speak(msg)
                        if self.pos.gain_loss_amt >= 1:
                            play_cash()
                    elif self.pos.gain_loss_amt < 0:
                        msg = f'LOSS, selling {self.pos.base_curr_symb} for {round(self.pos.gain_loss_amt_est,2)} dollars '
                        if self.pst.speak_yn == 'Y': speak(msg)
                        if self.pos.gain_loss_amt <= -1:
                            play_thunder()

            elif self.pos.test_txn_yn == 'Y':
                self.sell_pos_test()

#        self.sell_pos_save()

        t1 = time.perf_counter()
        secs = round(t1 - t0, 3)
        timing_data = {f'sell_logic, sell_pos_logic({self.pos.pos_id})': secs}
        self.pair.timings.append(timing_data)

#        return self.pair, pos, self.pair.ta

    #<=====>#

    def sell_pos_blocks(self):

        # sell_block_selling_off
        if self.pst.sell.selling_on_yn == 'N':
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => selling_on_yn : {self.pst.sell.selling_on_yn}'
            self.pos.sell_blocks.append(msg)

        # sell_block_never_sell_loss_live_all(self):
        elif self.pos.test_txn_yn == 'N' and self.pst.sell.never_sell_loss.live_all_yn == 'Y' and self.pos.prc_chg_pct < 0:
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => never_sell_loss.live_all_yn : {self.pst.sell.never_sell_loss.live_all_yn}'
            cs(msg, font_color='gold', bg_color='orangered')
            self.pos.sell_blocks.append(msg)

        # sell_block_never_sell_loss_all(self):
        elif self.pst.sell.never_sell_loss.all_yn == 'Y' and self.pos.prc_chg_pct < 0:
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => never_sell_loss.all_yn : {self.pst.sell.never_sell_loss.all_yn}'
            self.pos.sell_blocks.append(msg)

        # sell_block_never_sell_loss_prod_id(self):
        elif self.pos.prod_id in self.pst.sell.never_sell_loss.prod_ids and self.pos.prc_chg_pct < 0:
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => never_sell_loss.prod_ids : {self.pos.prod_id}'
            self.pos.sell_blocks.append(msg)

        # sell_block_never_sell_loss_pos_id(self):
        elif self.pos.pos_id in self.pst.sell.never_sell_loss.pos_ids and self.pos.prc_chg_pct < 0:
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => never_sell_loss.pos_ids : {self.pos.pos_id}'
            self.pos.sell_blocks.append(msg)

        # sell_block_never_sell_all(self):
        elif self.pst.sell.never_sell.all_yn == 'Y':
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => never_sell.all_yn : {self.pst.sell.never_sell.all_yn}'
            self.pos.sell_blocks.append(msg)

        # sell_block_never_sell_prod_id(self):
        elif self.pos.prod_id in self.pst.sell.never_sell.prod_ids:
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => never_sell.prod_ids : {self.pos.prod_id}'
            self.pos.sell_blocks.append(msg)

        # sell_block_never_sell_pos_id(self):
        elif self.pos.pos_id in self.pst.sell.never_sell.pos_ids:
            self.pos.sell_block_yn = 'Y'
            msg = f'settings => never_sell.pos_ids : {self.pos.pos_id}'
            self.pos.sell_blocks.append(msg)

        # sell_block_price_range_extreme(self):
        # Market Price Range Looks Very Suspect
        elif self.pair.prc_range_pct >= 5:
            self.pos.sell_block_yn = 'Y'
            msg = f'price range variance of {self.pair.prc_range_pct}, bid : {self.pos.prc_bid}, ask : {self.pos.prc_ask}, this price range looks sus... skipping sell'
            self.pos.sell_blocks.append(msg)

        self.disp_sell_pos_blocks()


    #<=====>#

    def sell_pos_forces(self):

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
        if self.pst.sell.force_sell.all_yn == 'Y':
            self.pos.sell_yn = 'Y'
            self.pos.sell_force_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'force'
            self.pos.sell_strat_name  = 'forced sell'
            msg = f'settings => force_sell.all_yn = {self.pst.sell.force_sell.all_yn}'
            self.pos.sell_forces.append(msg)

        # sell_force_force_sell_live_all(self):
        if self.pst.sell.force_sell.live_all_yn == 'Y' and self.pos.test_txn_yn == 'N':
            self.pos.sell_yn = 'Y'
            self.pos.sell_force_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'force'
            self.pos.sell_strat_name  = 'forced sell L'
            msg = f'settings => force_sell.live_all_yn = {self.pst.sell.force_sell.live_all_yn}'
            self.pos.sell_forces.append(msg)


        # sell_force_force_sell_prod_id(self):
        if self.pos.prod_id in self.pst.sell.force_sell.prod_ids:
            self.pos.sell_yn = 'Y'
            self.pos.sell_force_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'force'
            self.pos.sell_strat_name  = 'forced sell'
            msg = f'settings => force_sell.prod_ids = {self.pos.prod_id}'
            self.pos.sell_forces.append(msg)

        # sell_force_force_sell_id(self):
        if self.pos.pos_id in self.pst.sell.force_sell.pos_ids:
            self.pos.sell_yn = 'Y'
            self.pos.sell_force_yn = 'Y'
            self.pos.hodl_yn = 'N'
            self.pos.sell_strat_type = 'force'
            self.pos.sell_strat_name  = 'forced sell'
            msg = f'settings => force_sell.pos_ids = {self.pos.pos_id}'
            self.pos.sell_forces.append(msg)

        self.disp_sell_pos_forces()


    #<=====>#

    def sell_pos_tests_before_ta(self):

        # Take Profits
        if self.pos.prc_chg_pct > 0:
            if self.pos.sell_yn == 'N':
                if self.pst.sell.take_profit.hard_take_profit_yn == 'Y':
                    self.sell_pos_test_hard_profit()

            if self.pos.sell_yn == 'N':
                if self.pst.sell.take_profit.trailing_profit_yn == 'Y':
                    self.sell_pos_test_trailing_profit()

        # Stop Loss
        if self.pos.prc_chg_pct < 0:
            if self.pos.sell_yn == 'N':
                if self.pst.sell.stop_loss.hard_stop_loss_yn == 'Y':
                    self.sell_pos_test_hard_stop()

            if self.pos.sell_yn == 'N':
                if self.pst.sell.stop_loss.trailing_stop_loss_yn == 'Y':
                    self.sell_pos_test_trailing_stop()

            if self.pos.sell_yn == 'N':
                if self.pst.sell.stop_loss.atr_stop_loss_yn == 'Y':
                    self.sell_pos_test_atr_stop()

            if self.pos.sell_yn == 'N':
                if self.pst.sell.stop_loss.trailing_atr_stop_loss_yn == 'Y':
                    self.sell_pos_test_trailing_atr_stop()


    #<=====>#

    def sell_pos_tests_after_ta(self):

        if self.pos.sell_yn == 'N':
            if self.pst.sell.stop_loss.nwe_exit_yn == 'Y':
                self.sell_pos_test_nwe_exit()


    #<=====>#

    def sell_pos_test_hard_profit(self):

        if self.pos.buy_strat_name not in self.pst.sell.take_profit.hard_take_profit_strats_skip:
            all_sells   = []
            all_hodls   = []

            # Hard Take Profit Logic
            if self.pos.prc_chg_pct >= self.pst.sell.take_profit.hard_take_profit_pct:
                self.pos.sell_yn = 'Y'
                self.pos.hodl_yn = 'N'
                self.pos.sell_strat_type = 'profit'
                self.pos.sell_strat_name = 'hard_profit'
                msg = f'SELL COND: ...hard profit pct => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, take_profit : {self.pst.sell.take_profit.hard_take_profit_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                all_sells.append(msg)
            else:
                msg = f'HODL COND: ...hard profit => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, take_profit : {self.pst.sell.take_profit.hard_take_profit_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                # all_hodls.append(msg)

            msg = ''
            msg += self.spacer 
            msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Hard Take Profit', font_color='white', bg_color='green')
            self.chrt.chart_row(msg)
            self.disp_sell_pos_test_details(msg, all_sells, all_hodls)


    #<=====>#

    def sell_pos_test_hard_stop(self):

        if self.pos.buy_strat_name not in self.pst.sell.stop_loss.hard_stop_loss_strats_skip:
            all_sells   = []
            all_hodls   = []

            # Hard Stop Loss Logic
            if self.pos.prc_chg_pct <= abs(self.pst.sell.stop_loss.hard_stop_loss_pct) * -1:
                self.pos.sell_yn = 'Y'
                self.pos.hodl_yn = 'N'
                self.pos.sell_strat_type = 'stop_loss'
                self.pos.sell_strat_name = 'hard_stop_loss'
                msg = ''
                msg += self.spacer 
                msg += f'==> SELL COND: ...hard stop loss => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, stop_loss : {self.pst.sell.stop_loss.hard_stop_loss_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                all_sells.append(msg)
            else:
                self.pos.sell_yn = 'N'
                msg = ''
                msg += f'==> HODL COND: ...hard stop loss => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, stop_loss : {self.pst.sell.stop_loss.hard_stop_loss_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                # all_hodls.append(msg)

            msg = ''
            msg += self.spacer 
            msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Hard Stop Loss', font_color='white', bg_color='red')
            self.chrt.chart_row(msg)
            self.disp_sell_pos_test_details(msg, all_sells, all_hodls)


    #<=====>#

    def sell_pos_test_trailing_profit(self):

        if self.pos.buy_strat_name not in self.pst.sell.take_profit.trailing_profit_strats_skip:
            all_sells   = []
            all_hodls   = []

            # Trailing Profit Logic
            if self.pos.prc_chg_pct > 0.5:
                max_drop_pct = -5
                if self.pos.prc_chg_pct_high >= self.pst.sell.take_profit.trailing_profit_trigger_pct:
                    levels = self.pst.sell.take_profit.trailing_profit_levels
                    for k in sorted(levels, reverse=True):
                        if self.pos.prc_chg_pct_high >= float(k):
                            max_drop_pct = -1 * levels[k]
                            # print(f"k : {k}, levels[k] : {levels[k]}, self.pos.prc_chg_pct_high : {self.pos.prc_chg_pct_high}, max_drop_pct : {max_drop_pct}")
                            break
                    max_drop_pct = round(max_drop_pct, 2)

                    if self.pos.prc_chg_pct_drop <= max_drop_pct:
                        self.pos.sell_yn = 'Y'
                        self.pos.hodl_yn = 'N'
                        self.pos.sell_strat_type = 'profit'
                        self.pos.sell_strat_name = 'trail_profit'
                        msg = ''
                        msg += self.spacer 
                        msg += f'==> SELL COND: ...trailing profit => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                        all_sells.append(msg)
                    else:
                        msg = f'HODL COND: ...trailing profit => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, max_drop : {max_drop_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                        # all_hodls.append(msg)

            msg = ''
            msg += self.spacer 
            msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Trailing Profit', font_color='white', bg_color='green')
            self.chrt.chart_row(msg)
            self.disp_sell_pos_test_details(msg, all_sells, all_hodls)


    #<=====>#

    def sell_pos_test_trailing_stop(self):

        if self.pos.buy_strat_name not in self.pst.sell.stop_loss.trailing_stop_loss_strats_skip:
            all_sells   = []
            all_hodls   = []

            stop_loss_pct = round(self.pos.prc_chg_pct_high - abs(self.pst.sell.stop_loss.trailing_stop_loss_pct), 2)
            if self.pos.prc_chg_pct < stop_loss_pct:
                self.pos.sell_yn = 'Y'
                self.pos.hodl_yn = 'N'
                self.pos.sell_strat_type = 'stop_loss'
                self.pos.sell_strat_name = 'trail_stop'
                msg = f'SELL COND: ...trailing stop loss => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, trigger : {self.pst.sell.stop_loss.trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                all_sells.append(msg)
            else:
                msg = f'HODL COND: ...trailing stop loss => curr : {self.pos.prc_chg_pct:>.2f}%, high : {self.pos.prc_chg_pct_high:>.2f}%, drop : {self.pos.prc_chg_pct_drop:>.2f}%, trigger : {self.pst.sell.stop_loss.trailing_stop_loss_pct:>.2f}%, stop : {stop_loss_pct:>.2f}%, sell_yn : {self.pos.sell_yn}'
                # all_hodls.append(msg)

            msg = ''
            msg += self.spacer 
            msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Trailing Stop Loss', font_color='white', bg_color='red')
            self.chrt.chart_row(msg)
            self.disp_sell_pos_test_details(msg, all_sells, all_hodls)


    #<=====>#

    def sell_pos_test_nwe_exit(self):

        if self.pos.buy_strat_name not in self.pst.sell.stop_loss.nwe_exit_strats_skip:

            all_sells  = []
            all_hodls   = []

            freq = self.pos.buy_strat_freq

            nwe_color        = self.pair.ta[freq]['nwe_color']['ago0']
            nwe_color_last   = self.pair.ta[freq]['nwe_color']['ago1']

            nwe_color_5min  = self.pair.ta['5min']['nwe_color']['ago0']
            nwe_color_15min = self.pair.ta['15min']['nwe_color']['ago0']
            nwe_color_30min = self.pair.ta['30min']['nwe_color']['ago0']
            nwe_color_1h    = self.pair.ta['1h']['nwe_color']['ago0']
            nwe_color_4h    = self.pair.ta['4h']['nwe_color']['ago0']

            nwe_color_5min_last  = self.pair.ta['5min']['nwe_color']['ago1']

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

            else:
                msg = ''
                msg += self.spacer 
                msg += f'==> HODL COND: ...NWE Exit loss => nwe_color : {nwe_color}, nwe_color_last : {nwe_color_last}' + ', '
                msg = WoG(msg, print_tf=False)

            msg = ''
            msg += self.spacer 
            msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - NWE Exit', font_color='white', bg_color='blue')
            self.chrt.chart_row(msg)
            self.disp_sell_pos_test_details(msg, all_sells, all_hodls)

    #<=====>#

    def sell_pos_test_atr_stop(self):

        if self.pos.buy_strat_name not in self.pst.sell.stop_loss.atr_stop_loss_strats_skip:
            all_sells   = []
            all_hodls   = []

            # Trailing Stop Loss Logic
            atr_rfreq        = self.pst.sell.stop_loss.atr_stop_loss_rfreq
            atr              = self.pair.ta[atr_rfreq]['atr']['ago0']
            atr_stop_loss    = self.pos.prc_buy - atr

            if self.pos.sell_prc < atr_stop_loss:
                self.pos.sell_yn = 'Y'
                self.pos.hodl_yn = 'N'
                self.pos.sell_strat_type = 'stop_loss'
                self.pos.sell_strat_name = 'atr_stop'
                msg = ''
                msg += self.spacer 
                msg += f'==> SELL COND: ...ATR stop loss => curr : {self.pos.sell_prc:>.8f}, atr : {atr:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {self.pos.sell_yn}'
                all_sells.append(msg)
            else:
                msg = ''
                msg += self.spacer 
                msg += f'==> HODL COND: ...ATR stop loss => curr : {self.pos.sell_prc:>.8f}, atr : {atr:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {self.pos.sell_yn}'
                # all_hodls.append(msg)

            msg = ''
            msg += self.spacer 
            msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - ATR Stop Loss', font_color='white', bg_color='red')
            self.chrt.chart_row(msg)
            self.disp_sell_pos_test_details(msg, all_sells, all_hodls)


    #<=====>#

    def sell_pos_test_trailing_atr_stop(self):

        if self.pos.buy_strat_name not in self.pst.sell.stop_loss.trailing_atr_stop_loss_strats_skip:
            all_sells   = []
            all_hodls   = []

            # Trailing Stop Loss Logic
            atr_rfreq         = self.pst.sell.stop_loss.trailing_atr_stop_loss_rfreq
            atr_pct           = self.pst.sell.stop_loss.trailing_atr_stop_loss_pct
            atr               = self.pair.ta[atr_rfreq]['atr']['ago0']
            atr_pct_mult      = atr_pct / 100
            atr_reduce        = atr * atr_pct_mult
            atr_stop_loss     = self.pos.prc_high - atr_reduce

            if self.pos.sell_prc < atr_stop_loss:
                self.pos.sell_yn = 'Y'
                self.pos.hodl_yn = 'N'
                self.pos.sell_strat_type = 'stop_loss'
                self.pos.sell_strat_name = 'trail_atr_stop'
                msg = ''
                msg += self.spacer 
                msg += f'==> SELL COND: ...ATR trailing stop loss => curr : {self.pos.sell_prc:>.8f}, atr : {atr:>.8f}, atr_pct : {atr_pct:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {self.pos.sell_yn}'
                # all_hodls.append(msg)
            else:
                msg = ''
                msg += self.spacer 
                msg += f'==> HODL COND: ...ATR trailing stop loss => curr : {self.pos.sell_prc:>.8f}, atr : {atr:>.8f}, atr_pct : {atr_pct:>.8f}, atr_stop : {atr_stop_loss:>.8f}, sell_yn : {self.pos.sell_yn}'
                all_sells.append(msg)

            msg = ''
            msg += self.spacer 
            msg += cs(f'==> SELL TESTS - {self.pos.prod_id} - Trailing ATR Stop Loss', font_color='white', bg_color='red')
            self.chrt.chart_row(msg)
            self.disp_sell_pos_test_details(msg, all_sells, all_hodls)


    #<=====>#

    def sell_pos_deny_all_green(self):

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
        
        if self.pst.sell.profit_saver.ha_green.use_yn == 'N':
            return

        if self.pos.prod_id in self.pst.sell.profit_saver.ha_green.prod_ids:
            return
        if self.pos.sell_strat_name in self.pst.sell.profit_saver.ha_green.skip_sell_strats:
            return

        if self.pst.sell.profit_saver.ha_green.prod_ids and self.pos.prod_id not in self.pst.sell.profit_saver.ha_green.prod_ids:
            return
        if self.pst.sell.profit_saver.ha_green.sell_strats and self.pos.sell_strat_name not in self.pst.sell.profit_saver.ha_green.sell_strats:
            return

        all_sells                 = []
        all_hodls                 = []
        rfreq                     = self.pos.buy_strat_freq
        freqs, faster_freqs       = freqs_get(rfreq)

        ha_color_5min  = self.pair.ta['5min']['ha_color']['ago0']
        ha_color_15min = self.pair.ta['15min']['ha_color']['ago0']
        ha_color_30min = self.pair.ta['30min']['ha_color']['ago0']
        ha_color_1h    = self.pair.ta['1h']['ha_color']['ago0']
        ha_color_4h    = self.pair.ta['4h']['ha_color']['ago0']
        ha_color_1d    = self.pair.ta['1d']['ha_color']['ago0']

        skip_checks = False
        if self.pst.sell.force_sell.all_yn == 'Y':
            skip_checks = True

        if self.pos.prod_id in self.pst.sell.force_sell.prod_ids:
            skip_checks = True

        if self.pos.pos_id in self.pst.sell.force_sell.pos_ids:
            skip_checks = True

        if not skip_checks:
            green_save = False

            if rfreq == '1d':
                fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                if ha_color_4h == 'green':
                    if (ha_color_30min == 'green' or ha_color_15min == 'green') and ha_color_5min == 'green':
                        pass_msg = ''
                        pass_msg += self.spacer 
                        pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   1d : {ha_color_1d}, 4h : {ha_color_4h}, 30min : {ha_color_30min}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                        green_save = True
            elif rfreq == '4h':
                fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                if ha_color_1h == 'green':
                    if ha_color_15min == 'green' and ha_color_5min == 'green':
                        pass_msg = ''
                        pass_msg += self.spacer 
                        pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   4h : {ha_color_4h}, 1h : {ha_color_1h}, 15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                        green_save = True
            elif rfreq == '1h':
                fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                if ha_color_30min == 'green':
                    if ha_color_5min == 'green':
                        pass_msg = ''
                        pass_msg += self.spacer 
                        pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   1h : {ha_color_1h}, 30min : {ha_color_30min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                        green_save = True
            elif rfreq == '30min':
                fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {self.pos.sell_block_yn}'
                if ha_color_15min == 'green':
                    if ha_color_5min == 'green':
                        pass_msg = ''
                        pass_msg += self.spacer 
                        pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   30min : {ha_color_30min}, 15min : {ha_color_15min}, sell_block_yn : {self.pos.sell_block_yn}'
                        green_save = True
            elif rfreq == '15min':
                fail_msg = f'SELL DENY * SELL * ALL CANDLES NOT GREEN ==> Allowing Sell...   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                if ha_color_5min == 'green':
                    if ha_color_5min == 'green':
                        pass_msg = ''
                        pass_msg += self.spacer 
                        pass_msg += f'==> SELL DENY * HODL * ALL CANDLES GREEN ==> OVERIDING SELL!!!   15min : {ha_color_15min}, 5min : {ha_color_5min}, sell_block_yn : {self.pos.sell_block_yn}'
                        green_save = True

            if green_save:
                self.pos.sell_block_yn = 'Y'
                all_hodls.append(pass_msg)
            else:
                fail_msg = ''
                fail_msg += self.spacer 
                fail_msg += f'==> CANCEL SELL: ALL CANDLES NOT GREEN ==> Allowing Sell...   5min : {ha_color_5min}, 15min : {ha_color_15min}, 30min : {ha_color_30min}, sell_block_yn : {self.pos.sell_block_yn}'
                all_sells.append(fail_msg)

        print(f' - sell_block_yn : {self.pos.sell_block_yn}, show_tests_yn : {self.pst.sell.show_tests_yn}')
        if self.pos.sell_block_yn == 'Y' or self.pst.sell.show_tests_yn in ('Y','F'):
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL TESTS - {self.pos.prod_id} - All Green Candes...'
            WoG(msg)
            if self.pos.sell_block_yn == 'Y' or self.pst.sell.show_tests_yn in ('Y'):
                for e in all_sells:
                    if self.pos.prc_chg_pct > 0:
                        G(e)
                    else:
                        R(e)
                    self.pair.show_sell_header_tf = True
                for e in all_hodls:
                    WoG(e)
                    self.pair.show_sell_header_tf = True

    #<=====>#

    def sell_pos_deny_nwe_green(self):

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
        
        if self.pst.sell.profit_saver.nwe_green.use_yn == 'N':
            return

        if self.pos.prod_id in self.pst.sell.profit_saver.nwe_green.prod_ids:
            return
        if self.pos.sell_strat_name in self.pst.sell.profit_saver.nwe_green.skip_sell_strats:
            return

        if self.pst.sell.profit_saver.nwe_green.prod_ids and self.pos.prod_id not in self.pst.sell.profit_saver.nwe_green.prod_ids:
            return
        if self.pst.sell.profit_saver.nwe_green.sell_strats and self.pos.sell_strat_name not in self.pst.sell.profit_saver.nwe_green.sell_strats:
            return


        all_sells                 = []
        all_hodls                 = []
        rfreq                     = self.pos.buy_strat_freq
        freqs, faster_freqs       = freqs_get(rfreq)

        nwe_color_5min  = self.pair.ta['5min']['nwe_color']['ago0']
        nwe_color_15min = self.pair.ta['15min']['nwe_color']['ago0']
        nwe_color_30min = self.pair.ta['30min']['nwe_color']['ago0']
        nwe_color_1h    = self.pair.ta['1h']['nwe_color']['ago0']
        nwe_color_4h    = self.pair.ta['4h']['nwe_color']['ago0']
        nwe_color_1d    = self.pair.ta['1d']['nwe_color']['ago0']

        skip_checks = False
        if self.pst.sell.force_sell.all_yn == 'Y':
            skip_checks = True

        if self.pos.prod_id in self.pst.sell.force_sell.prod_ids:
            skip_checks = True

        if self.pos.pos_id in self.pst.sell.force_sell.pos_ids:
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

            # msg_tail = ''
            # msg_tail += cs(f' 5min : {nwe_color_5min}', font_color="white", bg_color=nwe_color_5min) + ', '
            # msg_tail += cs(f' 15min : {nwe_color_15min} ', font_color="white", bg_color=nwe_color_15min) + ', '
            # msg_tail += cs(f' 30min : {nwe_color_30min} ', font_color="white", bg_color=nwe_color_30min) + ', '
            # msg_tail += cs(f' 1h : {nwe_color_1h} ', font_color="white", bg_color=nwe_color_1h) + ', '
            # msg_tail += cs(f' 4h : {nwe_color_4h} ', font_color="white", bg_color=nwe_color_4h) + ', '
            # msg_tail += cs(f' 1d : {nwe_color_1d} ', font_color="white", bg_color=nwe_color_1d)


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
            else:
                all_sells.append(msg)

        print(f' - sell_block_yn : {self.pos.sell_block_yn}, show_tests_yn : {self.pst.sell.show_tests_yn}')
        if self.pos.sell_block_yn == 'Y' or self.pst.sell.show_tests_yn in ('Y','F'):
            msg = ''
            msg += self.spacer 
            msg += f'==> SELL TESTS - {self.pos.prod_id} - All NWEs Green...'
            WoG(msg)
            if self.pos.sell_block_yn == 'Y' or self.pst.sell.show_tests_yn in ('Y'):
                for e in all_sells:
                    if self.pos.prc_chg_pct > 0:
                        G(e)
                    else:
                        R(e)
                    self.pair.show_sell_header_tf = True
                for e in all_hodls:
                    WoG(e)
                    self.pair.show_sell_header_tf = True


    #<=====>#

    def sell_pos_save(self):

        if self.pos.sell_yn == 'Y':
            if self.pst.sell.save_files_yn == 'Y':
                fname = f"saves/{self.pos.prod_id}_SELL_{dt.now().strftime('%Y%m%d_%H%M%S')}.txt"
                writeit(fname, '=== MKT ===')
                for k in self.pair:
                    writeit(fname, f'{k} : {self.pair[k]}'.format(k, self.pair[k]))
                writeit(fname, '')
                writeit(fname, '')
                writeit(fname, '=== POS ===')
                for k in self.pos:
                    if isinstance(self.pos[k], [str, list, dict, float, int, decimal.Decimal, datetime, time]):
                        writeit(fname, f'{k} : {self.pos[k]}')
                    else:
                        print(f'{k} : {type(self.pos[k])}')


    #<=====>#

    def sell_pos_live(self):

        sell_data = db_sell_double_check(self.pos.pos_id)
        if sell_data and sell_data['pos_stat'] != 'OPEN':
            print('another bot must have changed the position status since we started!!! SKIPPING SELL!!!')
            beep(3)
        elif sell_data and sell_data['so_id'] is not None:
            print('another bot must have changed the position status since we started!!! SKIPPING SELL!!!')
            beep(3)
        else:
#            db_tbl_poss_insupd(self.pos)
            if self.pst.sell.sell_limit_yn == 'N' and self.pair.mkt_limit_only_tf == 1:
                print(f'{self.pos.prod_id} has been set to limit orders only, we cannot market buy/sell right now!!!')
                self.ord_mkt_sell_orig()
            elif self.pst.sell.sell_limit_yn == 'Y':
                try:
                    self.ord_lmt_sell_open() 
                except Exception as e:
                    print(f' ==> errored... {e}')
                    print(dttm_get())
                    traceback.print_exc()
                    traceback.print_stack()
                    print(type(e))
                    print(e)
                    print(f' ==> sell limit order failed, attempting market... {e}')
                    beep(3)
                    sys.exit()
                    self.ord_mkt_sell_orig()
            else:
                self.ord_mkt_sell_orig()
            # Update to Database
            db_tbl_poss_insupd(self.pos)


    #<=====>#

    def sell_pos_test(self):

        so = AttrDict()
        so.test_txn_yn                     = self.pos.test_txn_yn
        so.symb                        = self.pos.symb
        so.prod_id                     = self.pos.prod_id
#        so.mkt_name                    = self.mkt_name
        so.pos_id                      = self.pos.pos_id
        so.sell_seq_nbr                = 1
        so.sell_order_uuid             = self.gen_guid()    
        so.pos_type                    = 'SPOT'
        so.ord_stat                    = 'OPEN'
        so.sell_strat_type             = self.pos.sell_strat_type
        so.sell_strat_name             = self.pos.sell_strat_name
        so.sell_strat_freq             = self.pos.sell_strat_freq
        so.reason                      = self.pos.reason
        so.sell_begin_dttm             = dt.now()    
        so.sell_end_dttm               = dt.now()    
        so.sell_curr_symb              = self.pos.sell_curr_symb
        so.recv_curr_symb              = self.pos.recv_curr_symb    
        so.fees_curr_symb              = self.pos.fees_curr_symb
        so.sell_cnt_est                = self.pos.hold_cnt
        so.sell_cnt_act                = self.pos.hold_cnt
        so.fees_cnt_act                = (self.pos.hold_cnt * self.pos.sell_prc) * 0.004
        so.tot_in_cnt                  = (self.pos.hold_cnt * self.pos.sell_prc) * 0.996
        so.prc_sell_est                = self.pos.sell_prc
        so.prc_sell_act                = self.pos.sell_prc
        so.prc_sell_tot                = self.pos.sell_prc
        so.prc_sell_slip_pct           = 0

        # Update to Database
        self.pos.pos_stat = 'SELL'
        # Moving the update to the POSS table first, because when separated in many bots
        # sell_check_loop kept detecting this as an error... finging sell order OPEN
        # and pos_stat = OPEN instead of the desired SELL

#        print(f' db_tbl_poss_insupd(self.pos)')
        db_tbl_poss_insupd(self.pos)

#        print(f' self.pos.pos_stat : {self.pos.pos_stat}')
        db_tbl_sell_ords_insupd(so)

#        print(f' db_pos_get_by_pos_id({self.pos.pos_id})')
#        p = db_pos_get_by_pos_id(self.pos.pos_id)
#        pprint(p)

#        print(f' db_pos_get_by_pos_id({self.pos.pos_id}, {self.pos.pos_stat})')
        db_poss_stat_upd(self.pos.pos_id, self.pos.pos_stat)

#        print(f' db_pos_get_by_pos_id({self.pos.pos_id})')
#        p = db_pos_get_by_pos_id(self.pos.pos_id)
#        pprint(p)


    #<=====>#

    def buy_ords_check(self):

        buy_order_header_yn = 'Y'

        try:

            so = None
            o = None

            print_adv(2)
            self.chrt.chart_top()
            msg = f'* Buy Orders Check * {dttm_get()} *'
            self.chrt.chart_row(msg, align='center')

            bos = db_buy_ords_open_get()
            if bos:
                print(f' ==> {len(bos)} buy orders to check...')
                self.chrt.chart_mid()

                bos_cnt = len(bos)
                cnt = 0
                for bo in bos:
                    cnt += 1
                    bo = dec_2_float(bo)
                    bo = AttrDictConv(d=bo)

                    o = None

                    test_txn_yn = bo.test_txn_yn
                    ord_id = bo.buy_order_uuid

                    if test_txn_yn == 'Y':
                        bo.ord_stat = 'FILL'
                        db_tbl_buy_ords_insupd(bo)
                        self.pos_open(bo.buy_order_uuid)

                    elif test_txn_yn == 'N':

                        try:
                            o = cb_ord_get(order_id=ord_id)
                        except Exception as e:
                            
                            traceback.print_exc()
                            traceback.print_stack()
                            print(f'bo : {bo}')
#                            beep(2)
                            continue


                        if o:
                            o = dec_2_float(o)
                            o = AttrDictConv(d=o)

                            if o.prod_id != bo.prod_id:
                                print('error #1 !')
                                beep(3)
                                sys.exit()

                            if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
                                bo.buy_cnt_act                    = o.ord_filled_size
                                bo.fees_cnt_act                   = o.ord_total_fees
                                bo.tot_out_cnt                    = o.ord_total_value_after_fees
                                bo.prc_buy_act                    = o.ord_average_filled_price # not sure this includes the fees
                                bo.buy_end_dttm                   = o.ord_last_fill_time
                                bo.tot_prc_buy                    = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
                                if o.ord_settled:
                                    bo.ord_stat                   = 'FILL'
                                bo.prc_buy_slip_pct               = round((bo.prc_buy_act - bo.prc_buy_est) / bo.prc_buy_est, 8)


                                db_tbl_buy_ords_insupd(bo)
                                self.pos_open(bo.buy_order_uuid)

                            elif o.ord_status == 'OPEN':
                                print('')
                                print(o)

                                print('')
                                print(bo)

                                print('WE NEED CODE HERE #1!!!')
                                beep(10)
                                # sys.exit()
                                if o.ord_filled_size == 0:
                                    print(f'attempting to cancel order {bo.buy_order_uuid}... ')
                                    r = cb.cancel_orders([str(bo.buy_order_uuid)])
                                    print(r)
                                    time.sleep(1)
                                    o = cb_ord_get(order_id=ord_id)
                                    print(o)
                                    beep(10)
                                    sys.exit()
                                    # depending on results or get_order status 
                                    # update bo to cancelled
                                    # if counts are too small to sell, it becomes pocket/clip

                            else:
                                print('error #2 !')
#                                beep(3)
                                db_buy_ords_stat_upd(bo_id=bo.bo_id, ord_stat='ERR')

                    if buy_order_header_yn == 'Y':
                        buy_order_header_yn = 'N'
                        hmsg = ''
                        hmsg += f"{'bo_id':^7}" + " | "
                        hmsg += f"{'T':^1}" + " | "  
                        hmsg += f"{'prod_id':^12}" + " | "  
                        hmsg += f"{'ord_stat':^8}" + " | "  
                        hmsg += f"{'buy_strat_name':^16}" + " | "  
                        hmsg += f"{'buy_strat_freq':^16}" + " | "  
                        hmsg += f"{'elapsed':^7}" + " | "  
                        hmsg += f"{'buy_cnt_act':^18}" + " | "  
                        hmsg += f"{'tot_out_cnt':^18}" + " | "  
                        hmsg += f"{'prc_buy_act':^18}" + " | "  
                        hmsg += f"{'tot_prc_buy':^18}" + " | "  
                        hmsg += f"{'prc_buy_slip_pct':^18}" + " | "  
                        self.chrt.chart_headers(in_str=hmsg, align='left')

                    msg = ''
                    msg += f"{bo.bo_id:^7}" + " | "
                    msg += f"{bo.test_txn_yn:^1}" + " | "
                    msg += f"{bo.prod_id:^12}" + " | "
                    msg += f"{bo.ord_stat:^8}" + " | "
                    msg += f"{bo.buy_strat_name:^16}" + " | "
                    msg += f"{bo.buy_strat_freq:^16}" + " | "
                    msg += f"{bo.elapsed:^7}" + " | "
                    msg += f"{bo.buy_cnt_act:>18.12f}" + " | "
                    msg += f"{bo.tot_out_cnt:>18.12f}" + " | "
                    msg += f"{bo.prc_buy_act:>18.12f}" + " | "
                    msg += f"{bo.tot_prc_buy:>18.12f}" + " | "
                    msg += f"{bo.prc_buy_slip_pct:>18.12f}" + " | "
                    self.chrt.chart_row(in_str=msg, align='left')

            self.chrt.chart_bottom()
            print_adv(2)

        except Exception as e:
            
            traceback.print_exc()
            traceback.print_stack()
            print(f'so : {bo}')
            print(f'ord_id : {ord_id}')
            print(f'o : {o}')
            sys.exit()


    #<=====>#

    def sell_ords_check(self):

        sell_order_header_yn = 'Y'

        try:

            print_adv(2)
            self.chrt.chart_top()
            msg = f'* Sell Orders Checks * {dttm_get()} *'
            self.chrt.chart_row(msg, align='center')

            so = None
            o = None

            cnt = 0

            iss = db_poss_sell_order_problems_get()
            if iss:
                for i in iss:
                    print_adv()
                    print(i)
                beep(3)
#                sys.exit()

            sos = db_sell_ords_open_get()
            if sos:
                print(f' ==> {len(sos)} sell orders to check...')
                self.chrt.chart_mid()

                sos_cnt = len(sos)
                for so in sos:
                    o = None
                    cnt += 1
                    so = dec_2_float(so)
                    so = AttrDictConv(d=so)

                    test_txn_yn = so.test_txn_yn
                    ord_id = so.sell_order_uuid

                    if test_txn_yn == 'Y':
                        so.ord_stat = 'FILL'
                        db_tbl_sell_ords_insupd(so)
                        self.pos_close(so.pos_id, so.sell_order_uuid)

                    elif test_txn_yn == 'N':
                        try:
                            o = cb_ord_get(order_id=ord_id)
                        except Exception as e:
                            
                            traceback.print_exc()
                            traceback.print_stack()
                            print(f'so : {so}')
#                            beep(2)
                            continue

                        if o:
                            o = dec_2_float(o)
                            o = AttrDictConv(d=o)
                            if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
                                so.sell_cnt_act                    = o.ord_filled_size
                                so.fees_cnt_act                    = o.ord_total_fees
                                so.tot_in_cnt                      = o.ord_total_value_after_fees
                                so.prc_sell_act                    = o.ord_average_filled_price # not sure this includes the fees
                                so.sell_end_dttm                   = o.ord_last_fill_time
                                so.prc_sell_tot                    = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
                                if o.ord_settled:
                                    so.ord_stat                    = 'FILL'
                                so.prc_sell_slip_pct              = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 10) * 100
                                db_tbl_sell_ords_insupd(so)
                                self.pos_close(so.pos_id, so.sell_order_uuid)

                            elif o.ord_status == 'OPEN':
                                print('')
                                print(o)

                                print('')
                                print(so)

                                print('WE NEED CODE HERE #1 !!!')
                                beep(10)
                                # sys.exit()
                                if so.elapsed > 3 and o.ord_filled_size == 0:
                                    print(f'attempting to cancel order {so.sell_order_uuid}... ')
                                    r = cb.cancel_orders([str(so.sell_order_uuid)])
                                    print(r)
                                    time.sleep(1)
                                    o = cb_ord_get(order_id=ord_id)
                                    print(o)
                                    beep(10)
                                    sys.exit()
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
                                    # sys.exit()

                                    db_tbl_sell_ords_insupd(so)
        # this needs to be added when we add in support for limit orders
        #                        else:
        #                            r = cb_ord_cancel_orders(order_ids=[ord_id])
        #                            db_sell_ords_stat_upd(so_id=so.so_id, ord_stat='CANC')
        #                            db_poss_err_upd(pos_id=so.pos_id, pos_stat='OPEN')
                            else:
                                pprint(o)
                                print('WE NEED CODE HERE #1 !!!')
                                beep(10)
                                sys.exit()
                                db_sell_ords_stat_upd(so_id=so.so_id, ord_stat='ERR')
                                db_poss_err_upd(pos_id=so.pos_id, pos_stat='OPEN')

                    if sell_order_header_yn == 'Y':
                        sell_order_header_yn = 'N'
                        hmsg = ''
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
#                        hmsg += f"{'sell_cnt_est':^18}" + " | "  
                        hmsg += f"{'sell_cnt_act':^20}" + " | "  
                        hmsg += f"{'tot_in_cnt':^18}" + " | "  
#                        hmsg += f"{'prc_sell_est':^18}" + " | "  
                        hmsg += f"{'prc_sell_act':^18}" + " | "  
                        hmsg += f"{'prc_sell_tot':^18}" + " | "  
                        hmsg += f"{'prc_sell_slip_pct':^18}" + " | "  
                        self.chrt.chart_headers(in_str=hmsg, align='left')

                    msg = ''
                    msg += f"{so.so_id:^7}" + " | "
                    msg += f"{so.pos_id:^7}" + " | "
                    msg += f"{so.test_txn_yn:^1}" + " | "
                    msg += f"{so.prod_id:^12}" + " | "
                    msg += f"{so.ord_stat:^8}" + " | "
                    msg += f"{so.buy_strat_name:^16}" + " | "
                    msg += f"{so.buy_strat_freq:^16}" + " | "
                    msg += f"{so.sell_strat_name:^16}" + " | "
                    msg += f"{so.sell_strat_freq or '':^16}" + " | "
                    msg += f"{so.elapsed:^7}" + " | "
#                    msg += f"{so.sell_cnt_est:>18.12f}" + " | "
                    msg += f"{so.sell_cnt_act:>20.12f}" + " | "
                    msg += f"{so.tot_in_cnt:>18.12f}" + " | "
#                    msg += f"{so.prc_sell_est:>18.12f}" + " | "
                    msg += f"{so.prc_sell_act:>18.12f}" + " | "
                    msg += f"{so.prc_sell_tot:>18.12f}" + " | "
                    msg += f"{so.prc_sell_slip_pct:>18.12f}" + " | "
                    self.chrt.chart_row(in_str=msg, align='left')

            self.chrt.chart_bottom()
            print_adv(2)

        except Exception as e:
            
            traceback.print_exc()
            traceback.print_stack()
            print(f'so : {so}')
            print(f'ord_id : {ord_id}')
            print(f'o : {o}')
            sys.exit()


    #<=====>#

    # buy limit orders
    def cb_buy_base_size_calc(self, buy_prc, spend_amt, base_size_incr, base_size_min, base_size_max):

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

    def cb_sell_base_size_calc(self, init_sell_cnt):

        sell_cnt_max     = dec(init_sell_cnt)

        self.pos.pocket_pct            = self.pst.sell.rainy_day.pocket_pct
        self.pos.clip_pct              = self.pst.sell.rainy_day.clip_pct
        self.pos.sell_prc              = self.pair.prc_sell

        if round(sell_cnt_max,8) > dec(round(self.pos.hold_cnt,8)):
            print(f'...selling more {sell_cnt_max:>.8f} than we are position is holding {self.pos.hold_cnt:>.8f} onto...exiting...')
            beep(3)
            self.pos.sell_cnt = 0
            return

        if round(sell_cnt_max,8) > dec(round(self.pos.bal_cnt,8)):
            print(f'...selling more {sell_cnt_max:>.8f} than we the wallet balance {self.pos.bal_cnt:>.8f}...exiting...')
            beep(3)
            self.pos.sell_cnt = 0
            return

        if self.pos.prc_chg_pct > 0 and self.pos.pocket_pct > 0:
            sell_cnt_max -= sell_cnt_max * (dec(self.pos.pocket_pct) / 100) * (dec(self.pos.prc_chg_pct)/100)

        if self.pos.prc_chg_pct < 0 and self.pos.clip_pct > 0:
            sell_cnt_max -= sell_cnt_max * (dec(self.pos.clip_pct) / 100) * (abs(dec(self.pos.prc_chg_pct))/100)

        sell_blocks = int(sell_cnt_max / dec(self.pair.base_size_incr))
        sell_cnt_max = sell_blocks * dec(self.pair.base_size_incr)

        if sell_cnt_max < dec(self.pair.base_size_min):
            print(f'...selling less {sell_cnt_max:>.8f} than coinbase allows {self.pair.base_size_min}...exiting...')
            beep(3)
            self.pos.sell_cnt = 0
            return

        if sell_cnt_max > dec(self.pair.base_size_max):
            sell_cnt_max = dec(self.pair.base_size_max)

        self.pos.sell_cnt = sell_cnt_max


    #<=====>#

    def pos_open(self, buy_order_uuid):

        bos = db_mkt_sizing_data_get_by_uuid(buy_order_uuid)

        for bo in bos:
            bo = dec_2_float(bo)
            bo = AttrDictConv(d=bo)
            pos = AttrDict()
            pos.test_txn_yn                 = bo.test_txn_yn
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
            pos.pos_begin_dttm          = bo.buy_begin_dttm
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

            db_tbl_poss_insupd(pos)


    #<=====>#

    def pos_upd(self, pos):

        self.settings_mkt_get()

        pos.prc_curr         = self.pair.prc_sell

        if pos.pos_stat not in ('OPEN'):
            print(f'pos.pos_stat : {pos.pos_stat}')

        # Update Sell Price Highs & Lows
        if pos.prc_curr > pos.prc_high:
            pos.prc_high = pos.prc_curr
        if pos.prc_curr < pos.prc_low:
            pos.prc_low = pos.prc_curr

        # Update Price Change %
        pos.prc_chg_pct = calc_chg_pct(old_val=pos.prc_buy, new_val=pos.prc_curr, dec_prec=4)

        # Update Price Change % Highs & Lows
        if pos.prc_chg_pct > pos.prc_chg_pct_high: 
            pos.prc_chg_pct_high = pos.prc_chg_pct
        if pos.prc_chg_pct < pos.prc_chg_pct_low: 
            pos.prc_chg_pct_low  = pos.prc_chg_pct

        # Update Price Change Drop from Highest
        pos.prc_chg_pct_drop = round(pos.prc_chg_pct - pos.prc_chg_pct_high, 2)

        # Update Gain Loss Amt
        pos.val_curr          = pos.hold_cnt * pos.prc_curr
        pos.val_tot           = pos.tot_in_cnt + pos.val_curr
        pos.gain_loss_amt     = pos.val_tot - pos.tot_out_cnt
        pos.gain_loss_amt_est = pos.gain_loss_amt

        # Update Gain Loss % Highs & Lows
        if pos.gain_loss_amt_est > pos.gain_loss_amt_est_high:
            pos.gain_loss_amt_est_high = pos.gain_loss_amt_est
        if pos.gain_loss_amt_est < pos.gain_loss_amt_est_low:
            pos.gain_loss_amt_est_low  = pos.gain_loss_amt_est

        # gain_loss_pct_est is to capture the pct at the time we decide to sell and should not be updated after
        pos.gain_loss_pct     = calc_chg_pct(old_val=pos.tot_out_cnt, new_val=pos.val_tot, dec_prec=4)
        pos.gain_loss_pct_est = calc_chg_pct(old_val=pos.tot_out_cnt, new_val=pos.val_tot, dec_prec=4)

        # Update Gain Loss % Highs & Lows
        if pos.gain_loss_pct_est > pos.gain_loss_pct_est_high:
            pos.gain_loss_pct_est_high = pos.gain_loss_pct_est
        if pos.gain_loss_pct_est < pos.gain_loss_pct_est_low:
            pos.gain_loss_pct_est_low  = pos.gain_loss_pct_est

        # Update to Database
        db_tbl_poss_insupd(pos)


    #<=====>#

    def pos_close(self, pos_id, sell_order_uuid):

        pos = db_pos_get_by_pos_id(pos_id)
        pos = dec_2_float(pos)
        pos = AttrDictConv(d=pos)

        so  = db_sell_ords_get_by_uuid(sell_order_uuid)
        so  = dec_2_float(so)
        so  = AttrDictConv(d=so)

        pos.symb = pos.quote_curr_symb
        self.mkt_new(symb=pos.symb)
        self.pair_new(pair_dict=pos)
        self.settings_pair_get()
        prod_id    = pos.prod_id

#        pprint(so)

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

        # Finalize the Pocket & Clip Info
        if pos.prc_chg_pct > 0:
            pos.pocket_pct          = self.pst.sell.rainy_day.pocket_pct 
            pos.clip_pct            = self.pst.sell.rainy_day.clip_pct
            pos.pocket_cnt          = pos.hold_cnt
            pos.clip_cnt            = 0
        else:
            pos.pocket_pct          = self.pst.sell.rainy_day.pocket_pct
            pos.clip_pct            = self.pst.sell.rainy_day.clip_pct
            pos.pocket_cnt          = 0
            pos.clip_cnt            = pos.hold_cnt

        # Update to Database
        db_tbl_poss_insupd(pos)


    #<=====>#

    def disp_budget(self):
        # self.chrt.chart_mid(bold=True)

        hmsg = ""
        hmsg += f"    | "
        hmsg += f"{'lvl':<5} | "
        hmsg += f"$ {'size':^9} | "
        hmsg += f"$ {'balance':^9} | "
        hmsg += f"$ {'reserve':^9} | "
        hmsg += f"$ {'available':^9} | "
        hmsg += f"{'reserves state':^14} | "
        hmsg += f"$ {'spent':^12} | "
        hmsg += f"$ {'spent_max':^12} | "
        hmsg += f"{'spent_pct':^12} % | "
        hmsg += f"$ {'spent_up_amt':^12} | "
        hmsg += f"$ {'spent_up_max':^12} | "
        hmsg += f"{'up_pct':^12} % | "
        hmsg += f"$ {'spent_dn_amt':^12} | "
        hmsg += f"$ {'spent_dn_max':^12} | "
        hmsg += f"{'dn_pct':^12} %"
        self.chrt.chart_headers(in_str=hmsg)

        disp_font_color = 'white'
        disp_bg_color   = 'green'
        if self.budget[self.mkt.symb].spent_pct >= 100 or self.budget[self.mkt.symb].spent_up_pct >= 100 or self.budget[self.mkt.symb].pair_spent_pct >= 100:
            disp_bg_color = 'red'

        msg = ""
        msg += self.spacer + "| "
        msg += cs(f"{'mkt':<5}", font_color='white', bg_color='green') + " | "
        msg += cs(f"$ {self.buy.trade_strat_perf.trade_size:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].bal_avail:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].reserve_amt:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spendable_amt:>9.2f}", "white", "green") + " | "
        if self.budget[self.mkt.symb].reserve_locked_tf:
            msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
        else:
            msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spent_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spend_max_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"{self.budget[self.mkt.symb].spent_pct:>12.2f} %", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spent_up_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spend_up_max_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"{self.budget[self.mkt.symb].spent_up_pct:>12.2f} %", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spent_dn_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spend_dn_max_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"{self.budget[self.mkt.symb].spent_dn_pct:>12.2f} %", "white", "green")
        self.chrt.chart_row(in_str=msg, font_color=disp_font_color, bg_color=disp_bg_color)

        disp_font_color = 'white'
        disp_bg_color   = 'green'
        if self.budget[self.mkt.symb].pair_spent_pct >= 100 or self.budget[self.mkt.symb].pair_spent_up_pct >= 100 or self.budget[self.mkt.symb].pair_spent_dn_pct >= 100:
            disp_bg_color = 'red'

        msg = ""
        msg += self.spacer + "| "
        msg += cs(f"{'pair':<5}", font_color='white', bg_color='green') + " | "
        msg += cs(f"$ {self.buy.trade_strat_perf.trade_size:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].bal_avail:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].reserve_amt:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spendable_amt:>9.2f}", "white", "green") + " | "
        if self.buy.reserve_locked_tf:
            msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
        else:
            msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].pair_spent_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].pair_spend_max_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"{self.budget[self.mkt.symb].pair_spent_pct:>12.2f} %", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].pair_spent_up_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].pair_spend_up_max_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"{self.budget[self.mkt.symb].pair_spent_up_pct:>12.2f} %", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].pair_spent_dn_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].pair_spend_dn_max_amt:>12.6f}", "white", "green") + " | "
        msg += cs(f"{self.budget[self.mkt.symb].pair_spent_dn_pct:>12.2f} %", "white", "green")
        self.chrt.chart_row(in_str=msg, font_color=disp_font_color, bg_color=disp_bg_color)

        # Market Basics
        prod_id = self.buy.prod_id

        # Prices & Balances
        hmsg = ""

        # msg = ""
        # self.chrt.chart_headers(in_str=hmsg, bold=True)
        # self.chrt.chart_row(in_str=msg)
        # self.chrt.chart_mid(bold=True)


    #<=====>#

    def disp_budget2(self, budget=None, title=None, footer=None):
        print_adv(2)
        if title:
            self.chrt.chart_top(in_str=title)
        else:
            self.chrt.chart_top()

        hmsg = ""
        hmsg += f"{'symb':^6}" + " | "
        hmsg += f"${'spent_amt':^12}" + " | "
        hmsg += f"${'max_amt':^12}" + " | "
        hmsg += f"{'spent_pct':^12} %" + " | "
        hmsg += f"${'spent_up_amt':^12}" + " | "
        hmsg += f"{'spent_up_pct':^12} %" + " | "
        hmsg += f"${'spent_dn_amt':^12}" + " | "
        hmsg += f"{'spent_dn_pct':^12} %" + ' | '
        hmsg += f"$ {'usdc bal':^9}" + " | "
        hmsg += f"$ {'reserve':^9}" + " | "
        hmsg += f"$ {'free':^12}" + " | "
        hmsg += f"$ {'free_up':^12}" + " | "
        hmsg += f"$ {'free_dn':^12}" + " | "
        hmsg += f"{'reserves state':^14}"
        self.chrt.chart_headers(in_str=hmsg)

        msg = ""
        msg += f"{budget['symb']:^6}" + " | "
        msg += f"${budget['spent_amt']:>12.4f}" + " | "
        msg += f"${budget['spend_max_amt']:>12.4f}" + " | "
        msg += f"{budget['spent_pct']:>12.2f} %" + " | "
        msg += f"${budget['spent_up_amt']:>12.4f}" + " | "
        msg += f"{budget['spent_up_pct']:>12.2f} %" + " | "
        msg += f"${budget['spent_dn_amt']:>12.4f}" + " | "
        msg += f"{budget['spent_dn_pct']:>12.2f} %" + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].bal_avail:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].reserve_amt:>9.2f}", "white", "green") + " | "
        if self.budget[self.mkt.symb].spendable_amt > 0:
            msg += cs(f"$ {self.budget[self.mkt.symb].spendable_amt:>12.5f}", "white", "green") + " | "
        else:
            msg += cs(f"$ {self.budget[self.mkt.symb].spendable_amt:>12.5f}", "white", "red") + " | "
        if self.budget[self.mkt.symb].spendable_up_amt > 0:
            msg += cs(f"$ {self.budget[self.mkt.symb].spendable_up_amt:>12.5f}", "white", "green") + " | "
        else:
            msg += cs(f"$ {self.budget[self.mkt.symb].spendable_up_amt:>12.5f}", "white", "red") + " | "
        if self.budget[self.mkt.symb].spendable_dn_amt > 0:
            msg += cs(f"$ {self.budget[self.mkt.symb].spendable_dn_amt:>12.5f}", "white", "green") + " | "
        else:
            msg += cs(f"$ {self.budget[self.mkt.symb].spendable_dn_amt:>12.5f}", "white", "red") + " | "
        if self.budget[self.mkt.symb].reserve_locked_tf:
            msg += cs(f"{'LOCKED':^14}", "yellow", "magenta")
        else:
            msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow")
        self.chrt.chart_row(in_str=msg)

        if footer:
            self.chrt.chart_mid()
            self.chrt.chart_row(in_str=footer)

        self.chrt.chart_bottom(in_str='b')
#        print_adv(2)


    #<=====>#

    def disp_pair(self):
        self.disp_pair_summary()
        self.disp_pair_stats()
        self.disp_pair_ta_stats()
        self.disp_pair_performance()


    #<=====>#

    def disp_pair_summary(self):
        # Market Basics
        prod_id = self.pair.prod_id

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

        msg += cs(f"$ {self.budget[self.mkt.symb].bal_avail:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].reserve_amt:>9.2f}", "white", "green") + " | "
        msg += cs(f"$ {self.budget[self.mkt.symb].spendable_amt:>9.2f}", "white", "green") + " | "
        if self.budget[self.mkt.symb].reserve_locked_tf:
            msg += cs(f"{'LOCKED':^15}", "yellow", "magenta") + " | "
        else:
            msg += cs(f"{'UNLOCKED':^15}", "magenta", "yellow") + " | "
        self.chrt.chart_headers(in_str=hmsg, bold=True)
        self.chrt.chart_row(in_str=msg)
        self.chrt.chart_mid(bold=True)


    #<=====>#

    def disp_pair_stats(self):
        # Market Basics
        prod_id = self.pair.prod_id

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
        msg += f'{self.pair.trade_perf.tot_cnt:>9}' + ' | '
        msg += cs(f'{self.pair.trade_perf.win_cnt:>9}', font_color='white', bg_color='green') + ' | '
        msg += cs(f'{self.pair.trade_perf.lose_cnt:>9}', font_color='white', bg_color='red') + ' | '
        msg += cs(f'{self.pair.trade_perf.win_pct:>9.2f} %', font_color='white', bg_color='green') + ' | '
        msg += cs(f'{self.pair.trade_perf.lose_pct:>9.2f} %', font_color='white', bg_color='red') + ' | '
        msg += cs(f'$ {self.pair.trade_perf.win_amt:>9.4f}', font_color='white', bg_color='green') + ' | '
        msg += cs(f'$ {self.pair.trade_perf.lose_amt:>9.4f}', font_color='white', bg_color='red') + ' | '
        msg += f'$ {self.pair.trade_perf.tot_out_cnt:>9.4f}' + ' | '
        msg += f'$ {self.pair.trade_perf.tot_in_cnt:>9.4f}' + ' | '
        msg += f'$ {self.pair.trade_perf.val_curr:>9.4f}' + ' | '
        msg += f'$ {self.pair.trade_perf.val_tot:>9.4f}' + ' | '
        if self.pair.trade_perf.gain_loss_amt > 0:
            msg += cs(f'$ {self.pair.trade_perf.gain_loss_amt:>9.4f}', font_color='white', bg_color='green') + ' | '
            msg += cs(f'{self.pair.trade_perf.gain_loss_pct:>9.4f} %', font_color='white', bg_color='green') + ' | '
            msg += cs(f'{self.pair.trade_perf.gain_loss_pct_hr:>9.4f} %', font_color='white', bg_color='green') + ' | '
            msg += cs(f'{self.pair.trade_perf.gain_loss_pct_day:>9.4f} %', font_color='white', bg_color='green') + ' | '
        else:
            msg += cs(f'$ {self.pair.trade_perf.gain_loss_amt:>9.4f}', font_color='white', bg_color='red') + ' | '
            msg += cs(f'{self.pair.trade_perf.gain_loss_pct:>9.4f} %', font_color='white', bg_color='red') + ' | '
            msg += cs(f'{self.pair.trade_perf.gain_loss_pct_hr:>9.4f} %', font_color='white', bg_color='red') + ' | '
            msg += cs(f'{self.pair.trade_perf.gain_loss_pct_day:>9.4f} %', font_color='white', bg_color='red') + ' | '
        msg += f'{self.pair.trade_perf.last_elapsed:>9}' + ' | '

        title_msg = f'* Market Stats * {prod_id} *'
        self.chrt.chart_mid(in_str=title_msg, bold=True)
        self.chrt.chart_headers(in_str=hmsg, bold=True)
        self.chrt.chart_row(msg)

        self.chrt.chart_mid(bold=True)


    #<=====>#

    def disp_pair_ta_stats(self):
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

        prod_id = self.pair.prod_id
        if self.pair.ta:
            freq_disp = {}
            for freq in self.pair.ta:
                msg_tail = cs(f'{freq:>6}', font_color="white", bg_color='blue') + ' => '

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

            title_msg = f'* TA Stats * {prod_id} *'
            self.chrt.chart_mid(in_str=title_msg, bold=True)
            for freq in freq_disp:
                self.chrt.chart_row(freq_disp[freq])

            self.chrt.chart_mid(bold=True)


    #<=====>#

    def disp_pair_performance(self):
        # Market Basics
        prod_id = self.pair.prod_id

        hmsg = ""
        hmsg += f"{'strat':<15} | "
        hmsg += f"{'freq':<15} | "
        hmsg += f"{'total':^5} | "
        hmsg += f"{'open':^5} | "
        hmsg += f"{'close':^5} | "
        hmsg += f"{'wins':^5} | "
        hmsg += f"{'lose':^5} | "
        hmsg += f"{'win':^6} % | "
        hmsg += f"{'lose':^6} % | "
        hmsg += f"{'gain_amt':^10} | "
        hmsg += f"{'gain_pct':^10} % | "
        hmsg += f"{'gain_hr':^10} % | "
        hmsg += f"{'gain_day':^10} % | "
        hmsg += f"{'elapsed':^7} | "

        title_msg = '* Strategy Past Performance *'
        self.chrt.chart_mid(in_str=title_msg, bold=True)
        self.chrt.chart_headers(hmsg, bold=True)
        # print(len(self.pair.trade_strat_perfs))
        for x in self.pair.trade_strat_perfs:
            x = dec_2_float(x)
            x = AttrDictConv(d=x)

            if x.tot_cnt > 0:
                msg = ''
                msg += f'{x.buy_strat_name:<15} | '
                msg += f'{x.buy_strat_freq:<15} | '
                msg += f'{int(x.tot_cnt):>5} | '
                msg += f'{int(x.open_cnt):>5} | '
                msg += f'{int(x.close_cnt):>5} | '
                msg += f'{int(x.win_cnt):>5} | '
                msg += f'{int(x.lose_cnt):>5} | '
                msg += f'{x.win_pct:>6.2f} % | '
                msg += f'{x.lose_pct:>6.2f} % | '
                msg += f'{x.gain_loss_amt:>10.2f} | '
                msg += f'{x.gain_loss_pct:>10.2f} % | '
                msg += f'{x.gain_loss_pct_hr:>10.2f} % | '
                msg += f'{x.gain_loss_pct_day:>10.2f} % | '
                msg += f'{x.strat_last_elapsed:>7}' + ' | '
                msg  = cs_pct_color_50(pct=x.win_pct, msg=msg)
                self.chrt.chart_row(in_str=msg)
        self.chrt.chart_mid(bold=True)


    #<=====>#

    def disp_buy_header(self):
        hmsg = ""
        hmsg += f"{'mkt':<15} | "
        hmsg += f"{'strat':<15} | "
        hmsg += f"{'freq':<15} | "
        hmsg += f"{'total':^5} | "
        hmsg += f"{'open':^5} | "
        hmsg += f"{'close':^5} | "
        hmsg += f"{'wins':^5} | "
        hmsg += f"{'lose':^5} | "
        hmsg += f"{'win':^6} % | "
        hmsg += f"{'lose':^6} % | "
        hmsg += f"{'gain_amt':^10} | "
        hmsg += f"{'gain_pct':^10} % | "
        hmsg += f"{'gain_hr':^10} % | "
        hmsg += f"{'gain_day':^10} % | "
        hmsg += f"{'elapsed':<7} | "
        hmsg += f"{'trade_size':^16} | "

        title_msg = f'* BUY LOGIC * {self.buy.prod_id} *'
        self.chrt.chart_mid(in_str=title_msg, bold=True)
        self.chrt.chart_headers(in_str=hmsg, bold=True)
        self.buy.show_buy_header_tf = False


    #<=====>#

    def disp_buy(self):
        prod_id          = self.buy.prod_id

        if self.buy.show_buy_header_tf:
            self.disp_buy_header()
            self.buy.show_buy_header_tf = False

        msg1 = ''
        msg1 += f'{self.buy.trade_strat_perf.prod_id:<15}' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.buy_strat_name:<15}' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.buy_strat_freq:<15}' + ' | '
        msg1 += f'{int(self.buy.trade_strat_perf.tot_cnt):>5}' + ' | '
        msg1 += f'{int(self.buy.trade_strat_perf.open_cnt):^2}/{int(self.buy.trade_strat_perf.restricts_strat_open_cnt_max):^2}' + ' | '
        msg1 += f'{int(self.buy.trade_strat_perf.close_cnt):>5}' + ' | '
        msg1 += f'{int(self.buy.trade_strat_perf.win_cnt):>5}' + ' | '
        msg1 += f'{int(self.buy.trade_strat_perf.lose_cnt):>5}' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.win_pct:>6.2f} %' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.lose_pct:>6.2f} %' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.gain_loss_amt:>10.2f}' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.gain_loss_pct:>10.2f} %' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.gain_loss_pct_hr:>10.2f} %' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.gain_loss_pct_day:>10.2f} %' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.strat_last_elapsed:>7}' + ' | '
        msg1 += f'{self.buy.trade_strat_perf.trade_size:>16.8f}' + ' | '

        font_color = 'white'
        bg_color = 'black'

        if self.buy.trade_strat_perf.tot_cnt > 0:
            if self.buy.trade_strat_perf.tot_cnt > self.pst.buy_test_txns.test_txns_min:
                if self.buy.trade_strat_perf.gain_loss_pct_day > 0:
                    font_color = 'white'
                    bg_color = 'green'
                elif self.buy.trade_strat_perf.gain_loss_pct_day < 0:
                    font_color = 'white'
                    bg_color = 'red'
            else:
                if self.buy.trade_strat_perf.gain_loss_pct_day > 0:
                    font_color = 'green'
                    bg_color = 'black'
                elif self.buy.trade_strat_perf.gain_loss_pct_day < 0:
                    font_color = 'red'
                    bg_color = 'black'

        msg1 = cs(msg1, font_color=font_color, bg_color=bg_color)
        self.chrt.chart_row(msg1)


    #<=====>#

    def disp_buy_passes(self):
        if self.buy.buy_yn == 'Y' or self.buy.show_tests_yn in ('Y') or self.pst.buy.show_tests_yn == 'Y':
            for x in self.buy.all_passes:
                txt = cs('==> BUY STRAT TEST PASSES : ', font_color='white', bg_color='green')
                txt2 = cs(x, font_color='green')
                msg = self.spacer + f'{txt:<30} {txt2}' 
                self.chrt.chart_row(msg)
            self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_buy_fails(self):
        if self.buy.buy_yn == 'Y' or self.buy.show_tests_yn in ('Y') or self.pst.buy.show_tests_yn == 'Y':
            for x in self.buy.all_fails:
                txt = cs('==> BUY STRAT TEST FAILS : ', font_color='white', bg_color='red')
                txt2 = cs(x, font_color='red')
                msg = self.spacer + f'{txt:<30} {txt2}' 
                self.chrt.chart_row(msg)
            self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_buy_boosts(self):
        if self.pst.buy.show_boosts_yn == 'Y':
            for x in self.buy.all_boosts:
                txt = cs('==> BUY BOOSTS : ', font_color='white', bg_color='green')
                txt2 = cs(x, font_color='green')
                msg = self.spacer + f'{txt:<30} {txt2}' 
            self.chrt.chart_row(msg)
        self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_buy_limits(self):
        for x in self.buy.all_limits:
            txt = cs('==> BUY LIMITS : ', font_color='white', bg_color='red')
            txt2 = cs(x, font_color='red')
            msg = self.spacer + f'{txt:<30} {txt2}' 
            self.chrt.chart_row(msg)
        self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_buy_denies(self):
        for x in self.buy.all_denies:
            txt = cs('==> BUY DENIES : ', font_color='white', bg_color='red')
            txt2 = cs(x, font_color='red')
            msg = self.spacer + f'{txt:<30} {txt2}' 
            self.chrt.chart_row(msg)
        self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_buy_cancels(self):
        for x in self.buy.all_cancels:
            txt = cs('==> BUY CANCELS : ', font_color='white', bg_color='red')
            txt2 = cs(x, font_color='red')
            msg = self.spacer + f'{txt:<30} {txt2}' 
            self.chrt.chart_row(msg)
        self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_buy_maxes(self):
        for x in self.buy.all_maxes:
            txt = cs('==> BUY MAXES : ', font_color='white', bg_color='orange')
            txt2 = cs(x, font_color='orange')
            msg = self.spacer + f'{txt:<30} {txt2}' 
            self.chrt.chart_row(msg)
        self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_buy_test_reasons(self):
        for x in self.buy.all_test_reasons:
            txt = cs('==> BUY TEST MODE REASONS : ', font_color='white', bg_color='orange')
            txt2 = cs(x, font_color='red')
            msg = self.spacer + f'{txt:<30} {txt2}' 
            self.chrt.chart_row(msg)
        self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_sell_header(self):
        hmsg = ""
        hmsg += f"{'pair':^12} | "
        hmsg += f"{'T':^1} | "
        hmsg += f"{'pos_id':^6} | "
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
        hmsg += f"{'prc_low':^8} % | "
        hmsg += f"{'prc_drop':^8} % | "
        hmsg += f"$ {'net_est':^15} | "
        hmsg += f"$ {'net_est_high':^15}"

        title_msg = f'* SELL LOGIC * {self.pos.prod_id} *'
        self.chrt.chart_mid(in_str=title_msg, bold=True)
        self.chrt.chart_headers(in_str=hmsg, bold=True)

        self.pair.show_sell_header_tf = False


    #<=====>#

    def disp_sell_pos(self):
        if self.pair.show_sell_header_tf:
            self.disp_sell_header()
            self.pair.show_sell_header_tf = False

        disp_age = format_disp_age(self.pos.age_mins)

        msg = ''
        msg += f'{self.pos.prod_id:<12}' + ' | '
        msg += f'{self.pos.test_txn_yn:^1}' + ' | '
        msg += f'{self.pos.pos_id:^6}' + ' | '
        msg += f'{self.pos.buy_strat_name:^12}' + ' | '
        msg += f'{self.pos.buy_strat_freq:^5}' + ' | '
        msg += f'{disp_age:^10}' + ' | '
        msg += f'{self.pos.tot_out_cnt:>16.8f}' + ' | '
        msg += f'{self.pos.val_curr:>15.8f}' + ' | '
        msg += f'{self.pos.prc_buy:>15.8f}' + ' | '
        msg += f'{self.pos.prc_curr:>15.8f}' + ' | '
        msg += f'{self.pos.prc_high:>15.8f}' + ' | '
        msg += f'{self.pos.prc_chg_pct:>8.2f} %' + ' | '
        msg += f'{self.pos.prc_chg_pct_high:>8.2f} %' + ' | '
        msg += f'{self.pos.prc_chg_pct_low:>8.2f} %' + ' | '
        msg += f'{self.pos.prc_chg_pct_drop:>8.2f} %' + ' | '
        msg += f'$ {self.pos.gain_loss_amt:>15.8f}' + ' | '
        msg += f'$ {self.pos.gain_loss_amt_est_high:>15.8f}'

        msg = cs_pct_color(self.pos.prc_chg_pct, msg)
        self.chrt.chart_row(msg)


    #<=====>#

    def disp_sell_pos_forces(self):
        if self.pst.sell.show_forces_yn == 'Y':
            for f in self.pos.sell_forces:
                if self.pos.prc_chg_pct > 0:
                    msg = ''
                    msg += self.spacer 
                    msg += cs(f'==> SELL FORCE *', font_color='white', bg_color='green') 
                    msg += ' ' 
                    msg += cs(f, font_color='green')
                    self.chrt.chart_row(msg)
                else:
                    msg = ''
                    msg += self.spacer 
                    msg += cs(f'==> SELL FORCE *', font_color='white', bg_color='red') 
                    msg += ' ' 
                    msg += cs(f, font_color='red')
                    self.chrt.chart_row(msg)
                self.pair.show_sell_header_tf = True



    #<=====>#

    def disp_sell_pos_blocks(self):
        self.pst.sell.show_blocks_yn                   = self.pst.sell.show_blocks_yn

        if self.pst.sell.show_blocks_yn == 'Y':
            for b in self.pos.sell_blocks:
                if self.pos.prc_chg_pct > 0:
                    msg = ''
                    msg += self.space 
                    msg += cs(f'==> SELL BLOCK *', font_color='white', bg_color='green') 
                    msg += ' ' 
                    msg += cs(b, font_color='green')
                    self.chrt.chart_row(msg)
                else:
                    msg = ''
                    msg += self.spacer 
                    msg += cs(f'==> SELL BLOCK *', font_color='white', bg_color='red') 
                    msg += ' ' 
                    msg += cs(b, font_color='red')
                    self.chrt.chart_row(msg)
                self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_sell_pos_sells(self):
        if self.pst.sell.show_forces_yn == 'Y':
            for f in self.pos.sell_forces:
                if self.pos.prc_chg_pct > 0:
                    msg = ''
                    msg += self.spacer 
                    msg += cs(f'==> SELL FORCE *', font_color='white', bg_color='green') 
                    msg += ' ' 
                    msg += cs(f, font_color='green')
                    self.chrt.chart_row(msg)
                else:
                    msg = ''
                    msg += self.spacer 
                    msg += cs(f'==> SELL FORCE *', font_color='white', bg_color='red') 
                    msg += ' ' 
                    msg += cs(f, font_color='red')
                    self.chrt.chart_row(msg)
                self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_sell_pos_hodls(self):
        if self.pst.sell.show_tests_yn == 'Y':
            for t in self.pos.sell_tests:
                if self.pos.prc_chg_pct > 0:
                    msg = ''
                    msg += self.spacer 
                    msg += cs(f'==> SELL TEST *', font_color='white', bg_color='green') 
                    msg += ' ' 
                    msg += cs(t, font_color='green')
                    self.chrt.chart_row(msg)
                else:
                    msg = ''
                    msg += self.spacer 
                    msg += cs(f'==> SELL TEST *', font_color='white', bg_color='red') 
                    msg += ' ' 
                    msg += cs(t, font_color='red')
                    self.chrt.chart_row(msg)
                self.pair.show_sell_header_tf = True


    #<=====>#

    def disp_sell_pos_test_details(self, msg, all_sells, all_hodls):
        if (self.pos.sell_yn == 'Y' and self.pos.sell_block_yn == 'N') or self.pst.sell.show_tests_yn in ('Y','F'):
            for e in all_sells:
                if self.pos.prc_chg_pct > 0:
                    e = self.spacer + cs('* ' + e, font_color='green')
                    self.chrt.chart_row(e)
                else:
                    e = self.spacer + cs('* ' + e, font_color='red')
                    self.chrt.chart_row(e)
                self.pair.show_sell_header_tf = True
            for e in all_hodls:
                e = self.spacer + cs('* ' + e, font_color='green', bg_color='white')
                self.chrt.chart_row(e)
                self.pair.show_sell_header_tf = True


    #<=====>#

    def ord_mkt_buy(self):

        prod_id               = self.buy.prod_id
        spend_amt             = str(self.buy.trade_strat_perf.trade_size)
        self.buy.refresh_wallet_tf    = True

        order = cb.fiat_market_buy(prod_id, spend_amt)
        self.buy.refresh_wallet_tf       = True
        time.sleep(0.33)

        ord_id = order.id

        o = cb_ord_get(order_id=ord_id)
        time.sleep(0.33)

        bo = None
        if o:
            bo = AttrDict()
            bo.prod_id               = self.buy.prod_id
            bo.symb                  = self.buy.symb
            bo.pos_type              = 'SPOT'
            bo.ord_stat              = 'OPEN'
            bo.buy_strat_type        = self.buy.buy_strat_type
            bo.buy_strat_name        = self.buy.buy_strat_name
            bo.buy_strat_freq        = self.buy.buy_strat_freq
            bo.buy_order_uuid        = ord_id
            bo.buy_begin_dttm        = dt.now()
            bo.buy_curr_symb         = self.buy.base_curr_symb
            bo.spend_curr_symb       = self.buy.quote_curr_symb
            bo.fees_curr_symb        = self.buy.quote_curr_symb
            bo.buy_cnt_est           = (self.buy.trade_size * 0.996) / self.buy.prc_buy
            bo.prc_buy_est           = self.buy.prc_buy
            db_tbl_buy_ords_insupd(bo)
            time.sleep(.33)
        else:
            sys.exit()


    #<=====>#

    def ord_mkt_sell(self):

        prod_id               = self.pos.prod_id
        init_sell_cnt         = self.pos.hold_cnt

        end_time              = dt.now() + timedelta(minutes=5)
        end_time              = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        self.cb_sell_base_size_calc(init_sell_cnt)

        if self.pos.sell_cnt == 0:
            self.pos.symb = 'USDC'
            self.pos.pos_stat = 'ERR'
            self.pos.ignore_tf = 1
            self.pos.error_tf = 1
            self.pos.sell_yn = 'N'
            self.pos.reason = f'there are not enough {self.pos.buy_curr_symb} to complete this sale...'
            db_tbl_poss_insupd(self.pos)
        else:

            recv_amt = round(float(self.pos.sell_cnt) * float(self.pos.sell_prc),2)

            order = cb.fiat_market_sell(prod_id, recv_amt)
            self.pos.refresh_wallet_tf       = True
            time.sleep(0.33)

            ord_id = order.id
            o = cb_ord_get(order_id=ord_id)
            time.sleep(0.33)

            so = None
            if o:
                so = AttrDict()
                so.pos_id                = self.pos.pos_id
                so.symb                  = self.pos.symb
                so.prod_id               = self.pair.prod_id
                so.pos_type              = 'SPOT'
                so.ord_stat              = 'OPEN'
                so.sell_order_uuid       = ord_id
                so.sell_begin_dttm       = dt.now()
                so.sell_strat_type       = self.pos.sell_strat_type
                so.sell_strat_name       = self.pos.sell_strat_name
                so.sell_curr_symb        = self.pair.base_curr_symb
                so.recv_curr_symb        = self.pair.quote_curr_symb
                so.fees_curr_symb        = self.pair.quote_curr_symb
                so.sell_cnt_est          = self.pos.sell_cnt
                so.prc_sell_est          = self.pair.prc_sell
                db_tbl_sell_ords_insupd(so)
                time.sleep(.33)
                self.pos.pos_stat = 'SELL'
                db_tbl_poss_insupd(self.pos)
#                db_poss_stat_upd(pos_id=self.pos.pos_id, pos_stat='SELL')
            else:
                sys.exit()


    #<=====>#

    def ord_mkt_buy_orig(self):

        client_order_id       = cb_client_order_id()
        prod_id               = self.buy.prod_id
        spend_amt             = self.buy.trade_strat_perf.trade_size
        self.buy.refresh_wallet_tf    = True

        oc = {}
        oc['market_market_ioc'] = {}
        oc['market_market_ioc']['quote_size'] = str(spend_amt)

        o = cb.create_order(
                client_order_id = client_order_id, 
                product_id = prod_id, 
                side = 'BUY', 
                order_configuration = oc
                )
        print(o)
        # print(type(o))
        o = o.to_dict()
        # print(type(o))
        self.buy.refresh_wallet_tf       = True
        time.sleep(0.25)

        bo = None
        if o:
            if 'success' in o:
                if o['success']:
                    bo = AttrDict()
                    bo.prod_id               = self.buy.prod_id
                    bo.symb                  = self.buy.symb
                    bo.pos_type              = 'SPOT'
                    bo.ord_stat              = 'OPEN'
                    bo.buy_strat_type        = self.buy.buy_strat_type
                    bo.buy_strat_name        = self.buy.buy_strat_name
                    bo.buy_strat_freq        = self.buy.buy_strat_freq
                    bo.buy_order_uuid        = o['success_response']['order_id']
                    bo.buy_client_order_id   = o['success_response']['client_order_id']
                    bo.buy_begin_dttm        = dt.now()
                    bo.buy_curr_symb         = self.buy.base_curr_symb
                    bo.spend_curr_symb       = self.buy.quote_curr_symb
                    bo.fees_curr_symb        = self.buy.quote_curr_symb
                    bo.buy_cnt_est           = (spend_amt * 0.996) / self.buy.prc_buy
                    bo.prc_buy_est           = self.buy.prc_buy
                    db_tbl_buy_ords_insupd(bo)
                    time.sleep(.25)
                else:
                    sys.exit()
            else:
                sys.exit()
        else:
            sys.exit()


    #<=====>#

    def ord_mkt_sell_orig(self):

        client_order_id       = cb_client_order_id()
        prod_id               = self.pos.prod_id
        init_sell_cnt         = self.pos.hold_cnt

        self.cb_sell_base_size_calc(init_sell_cnt)

        if self.pos.sell_cnt == 0:
            self.pos.symb = 'USDC'
            self.pos.pos_stat = 'ERR'
            self.pos.ignore_tf = 1
            self.pos.error_tf = 1
            self.pos.sell_yn = 'N'
            self.pos.reason = f'there are not enough {self.pos.buy_curr_symb} to complete this sale...'
            db_tbl_poss_insupd(self.pos)
        else:
            oc = {}
            oc['market_market_ioc'] = {}
            oc['market_market_ioc']['base_size'] = f'{self.pos.sell_cnt:>.8f}'

            o = cb.create_order(
                    client_order_id = client_order_id, 
                    product_id = prod_id, 
                    side = 'SELL', 
                    order_configuration = oc
                    )
            print(o)
            # print(type(o))
            o = o.to_dict()
            # print(type(o))
            self.pos.refresh_wallet_tf       = True
            time.sleep(0.25)

            so = None
            if o:
                if 'success' in o:
                    if o['success']:
                        so = AttrDict()
                        so.pos_id                = self.pos.pos_id
                        so.symb                  = self.pos.symb
                        so.prod_id               = self.pair.prod_id
                        so.pos_type              = 'SPOT'
                        so.ord_stat              = 'OPEN'
                        so.sell_order_uuid       = o['success_response']['order_id']
                        so.sell_client_order_id  = o['success_response']['client_order_id']
                        so.sell_begin_dttm       = dt.now()
                        so.sell_strat_type       = self.pos.sell_strat_type
                        so.sell_strat_name       = self.pos.sell_strat_name
                        so.sell_curr_symb        = self.pair.base_curr_symb
                        so.recv_curr_symb        = self.pair.quote_curr_symb
                        so.fees_curr_symb        = self.pair.quote_curr_symb
                        so.sell_cnt_est          = self.pos.sell_cnt
                        so.prc_sell_est          = self.pair.prc_sell
                        db_tbl_sell_ords_insupd(so)
                        time.sleep(.25)
                        self.pos.pos_stat = 'SELL'
                        db_tbl_poss_insupd(self.pos)
#                        db_poss_stat_upd(pos_id=self.pos.pos_id, pos_stat='SELL')
                    else:
                        pprint(o)
                        beep(3)
                        print('exit on line 3451')
                        sys.exit()
                else:
                    beep(3)
                    print('exit on line 3458')
                    sys.exit()
            else:
                beep(3)
                print('exit on line 3465')
                sys.exit()


    #<=====>#

    def ord_lmt_buy_open(self):
        prod_id                   = self.buy.prod_id
        spend_amt                 = str(self.buy.trade_strat_perf.trade_size)
        limit_price               = self.buy.prc_buy
        method                    = 1

        buy_cnt                   = spend_amt / limit_price

        # limit_limit_gtc method - good till cancel
        if method == 1:
            client_order_id = self.gen_guid()
            oc = {}
            oc['limit_limit_gtc'] = {}
            oc['limit_limit_gtc']['base_size']    = f'{buy_cnt:>.8f}'
            oc['limit_limit_gtc']['limit_price']  = f'{limit_price:>.8f}'
            oc['limit_limit_gtc']['post_only']    = False
            time.sleep(0.5)
            o = self.cb.create_order(
                    client_order_id = client_order_id, 
                    product_id = prod_id, 
                    side = 'BUY', 
                    order_configuration = oc
                    )
            print(f'o : {o}')
        # limit_limit_gtd method - good till date
        elif method == 2:
            client_order_id = self.gen_guid()
            end_dttm = datetime.now(datetime.UTC) + timedelta(minutes=5)
            end_dttm_fmt = end_dttm.strftime("%Y-%m-%dT%H:%M:%SZ")
            oc = {}
            oc['limit_limit_gtd'] = {}
            oc['limit_limit_gtd']['base_size']    = f'{buy_cnt:>.8f}'
            oc['limit_limit_gtd']['limit_price']  = f'{limit_price:>.8f}'
            oc['limit_limit_gtd']['end_time']     = f'{end_dttm_fmt}'
            oc['limit_limit_gtd']['post_only']    = False
            time.sleep(0.5)
            o = self.cb.create_order(
                    client_order_id = client_order_id, 
                    product_id = prod_id, 
                    side = 'BUY', 
                    order_configuration = oc
                    )
            print(f'o : {o}')
        # this method uses coinbase_advanced_trader library
        else:
            client_order_id = self.gen_guid()
            o = cb.fiat_limit_buy(product_id=prod_id, fiat_amount=spend_amt, limit_price=limit_price)

        print(o)
        self.buy.refresh_wallet_tf       = True
        time.sleep(0.25)

        if o:
            if isinstance(o, dict) and 'success' in o and o['success']:
                buy_order_uuid        = o['success_response']['order_id']
                buy_client_order_id   = o['success_response']['client_order_id']
            else:
                buy_order_uuid         = o.id
                buy_client_order_id    = o.client_order_id

            bo = None
            if buy_order_uuid:
                bo = AttrDict()
                bo.prod_id               = self.buy.prod_id
                bo.symb                  = self.buy.symb
                bo.pos_type              = 'SPOT'
                bo.ord_stat              = 'OPEN'
                bo.buy_strat_type        = self.buy.buy_strat_type
                bo.buy_strat_name        = self.buy.buy_strat_name
                bo.buy_strat_freq        = self.buy.buy_strat_freq
                bo.buy_order_uuid        = buy_order_uuid
                bo.buy_client_order_id   = buy_client_order_id
                bo.buy_begin_dttm        = dt.now()
                bo.buy_curr_symb         = self.buy.base_curr_symb
                bo.spend_curr_symb       = self.buy.quote_curr_symb
                bo.fees_curr_symb        = self.buy.quote_curr_symb
                bo.buy_cnt_est           = (spend_amt * 0.996) / self.buy.prc_buy
                bo.prc_buy_est           = self.buy.prc_buy
                db_tbl_buy_ords_insupd(bo)
                time.sleep(.25)
            else:
                beep(3)
                print('exit on line 5092')
                sys.exit()
        else:
            beep(3)
            print('exit on line 5098')
            sys.exit()


    #<=====>#

    def ord_lmt_sell_open(self):

        # end_time              = dt.now() + timedelta(minutes=5)
        # end_time              = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        method                = 1
        prod_id               = self.pos.prod_id
        init_sell_cnt         = self.pos.hold_cnt
        limit_price           = self.pos.sell_prc

        self.cb_sell_base_size_calc(init_sell_cnt)

        if self.pos.sell_cnt == 0:
            self.pos.symb = 'USDC'
            self.pos.pos_stat = 'ERR'
            self.pos.ignore_tf = 1
            self.pos.error_tf = 1
            self.pos.sell_yn = 'N'
            self.pos.reason = f'there are not enough {self.pos.buy_curr_symb} to complete this sale...'
            db_tbl_poss_insupd(self.pos)
        else:
            # limit_limit_gtc method - good till cancel
            if method == 1:
                client_order_id = self.gen_guid()
                sell_cnt = self.pos.sell_cnt
                oc = {}
                oc['limit_limit_gtc'] = {}
                oc['limit_limit_gtc']['base_size']    = f'{sell_cnt:>.8f}'
                oc['limit_limit_gtc']['limit_price']  = f'{limit_price:>.8f}'
                oc['limit_limit_gtc']['post_only']    = False
                time.sleep(0.5)
                o = self.cb.create_order(
                        client_order_id = client_order_id, 
                        product_id = prod_id, 
                        side = 'SELL', 
                        order_configuration = oc
                        )
                print(f'o : {o}')
            # limit_limit_gtd method - good till date
            elif method == 2:
                client_order_id = self.gen_guid()
                sell_cnt = self.pos.sell_cnt
                end_dttm = datetime.now(datetime.UTC) + timedelta(minutes=5)
                end_dttm_fmt = end_dttm.strftime("%Y-%m-%dT%H:%M:%SZ")
                oc = {}
                oc['limit_limit_gtd'] = {}
                oc['limit_limit_gtd']['base_size']    = f'{sell_cnt:>.8f}'
                oc['limit_limit_gtd']['limit_price']  = f'{limit_price:>.8f}'
                oc['limit_limit_gtd']['end_time']     = f'{end_dttm_fmt}'
                oc['limit_limit_gtd']['post_only']    = False
                time.sleep(0.5)
                o = self.cb.create_order(
                        client_order_id = client_order_id, 
                        product_id = prod_id, 
                        side = 'SELL', 
                        order_configuration = oc
                        )
                print(f'o : {o}')
            # this method uses coinbase_advanced_trader library
            else:
                client_order_id = self.gen_guid()
                sell_cnt = round(float(self.pos.sell_cnt), 2)
                recv_amt = round(float(self.pos.sell_cnt) * float(limit_price), 2)
                o = cb.fiat_limit_sell(product_id=prod_id, fiat_amount=recv_amt, limit_price=limit_price)

            print(o)
            self.pos.refresh_wallet_tf       = True
            time.sleep(0.25)

            if o:
                if isinstance(o, dict) and 'success' in o and o['success']:
                    sell_order_uuid       = o['success_response']['order_id']
                    sell_client_order_id  = o['success_response']['client_order_id']
                else:
                    sell_order_uuid        = o.id
                    sell_client_order_id   = o.client_order_id

                so = None
                if sell_order_uuid:
                    so = AttrDict()
                    so.pos_id                = self.pos.pos_id
                    so.symb                  = self.pos.symb
                    so.prod_id               = self.pair.prod_id
                    so.pos_type              = 'SPOT'
                    so.ord_stat              = 'OPEN'
                    so.sell_order_uuid       = sell_order_uuid
                    so.sell_client_order_id  = sell_client_order_id
                    so.sell_begin_dttm       = dt.now()
                    so.sell_strat_type       = self.pos.sell_strat_type
                    so.sell_strat_name       = self.pos.sell_strat_name
                    so.sell_curr_symb        = self.pair.base_curr_symb
                    so.recv_curr_symb        = self.pair.quote_curr_symb
                    so.fees_curr_symb        = self.pair.quote_curr_symb
                    so.sell_cnt_est          = self.pos.sell_cnt
                    so.prc_sell_est          = self.pair.prc_sell
                    db_tbl_sell_ords_insupd(so)
                    time.sleep(.25)
                    self.pos.pos_stat = 'SELL'
                    db_tbl_poss_insupd(self.pos)
                else:
                    beep(3)
                    print('exit on line 5169')
                    sys.exit()
            else:
                beep(3)
                print('exit on line 5175')
                sys.exit()


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
