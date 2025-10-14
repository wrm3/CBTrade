#<=====>#
# Description
#<=====>#



#<=====>#
# To Do List
#<=====>#



#<=====>#
# Variables
#<=====>#
lib_name      = 'budget_base'
log_name      = 'budget_base'


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
from typing import Dict, List, Optional, Any, TypeAlias

#<=====>#
# Imports - Project
#<=====>#

from libs.coinbase_handler import cb
from libs.common import (
    AttrDict
    , AttrDictConv
    , AttrDictEnh
    , print_adv
    , fatal_error_exit
    , dttm_get
    , dttm_unix
    , print_adv
    , format_disp_age2
    , get_unix_timestamp
    , speak_async
    , narc
)
from libs.db_mysql.cbtrade.db_main import CBTRADE_DB
cbtrade_db = CBTRADE_DB()  # Create instance for backward compatibility
from libs.reports_base import report_sells_recent
from libs.settings_base import mkt_settings_get
from libs.strat_base import buy_strats_get
from libs.theme import *

#<=====>#c
# Classes
#<=====>#


#<=====>#c
# Functions
#<=====>#

@narc(1)
def budget_new(self, mkt_symb:str):
    if self.debug_tf: G(f'==> budget_base.budget_new()')
    self.budget                    = AttrDict()
    self.budget.mkt_symb           = mkt_symb
    self.budget.bal_avail                 = 0
    self.budget.spendable_amt             = 0
    self.budget.reserve_amt               = 0
    self.budget.reserve_locked_tf         = True
    self.wallet_refresh(force_tf=True)
    self.budget_refresh()
    self.budget_reserves_calc()

#<=====>#

@narc(1)
def wallet_refresh(self, force_tf=False):
    if self.debug_tf: G(f'==> budget_base.wallet_refresh() force_tf: {force_tf}')
    G(f'==> budget_base.wallet_refresh() force_tf: {force_tf}')

    if force_tf:
        self.cb.cb_wallet_refresh()
        self.budget.reserve_amt      = 0
        self.budget.bal_avail        = 0
        self.budget.spendable_amt    = 0
        self.budget.open_trade_amt   = 0

        # when/if we start trading  against btc, eth, sol and not just usdc
        # we will need to add a deduction for the amount outstanding on trades 
        # that used other currencies
        open_trade_amts = AttrDict()
        r = self.cbtrade_db.db_open_trade_amts_get()
        for x in r:
            x = AttrDict(x)
            # print(x)
            if x['base_curr_symb'] in ('BTC', 'ETH', 'SOL', 'USD', 'USDT', 'USDC'):
                open_trade_amts[x['base_curr_symb']] = x['open_trade_amt']
            x = None

        bals = self.cbtrade_db.db_bals_get(symb=self.mkt_symb)

        for bal in bals:
            print(f"bal: {bal}")
            bal = AttrDict(bal)
            curr = bal.symb
            # print(bal)
            if curr == self.mkt_symb:
                # print(f"curr {curr} == self.mkt_symb {self.mkt_symb}")
                self.budget.bal_avail = bal.bal_avail
                self.budget_reserves_calc()
                
                # Calculate spendable amount (only base reserve, no select_pair logic)
                self.budget.spendable_amt = self.budget.bal_avail - self.budget.reserve_amt
                
                if curr in open_trade_amts:
                    self.budget.open_trade_amt = open_trade_amts[curr]
                    self.budget.spendable_amt -= self.budget.open_trade_amt
                else:
                    self.budget.open_trade_amt = 0

    cnt = 0
    while self.budget.bal_avail == 0:
        cnt += 1
        msg = f'{self.budget.mkt_symb} bal_avail is 0, sleeping {cnt} seconds then refreshing wallet'
        print(msg)
        speak_async(msg)
        time.sleep(cnt)
        self.wallet_refresh(force_tf=True)

#<=====>#

@narc(1)
def budget_refresh(self):
    if self.debug_tf: G(f'==> budget_base.budget_refresh()')
    # print(f"🔍 budget_refresh START: bal_avail = ${self.bal_avail}")
    # print(f"🔍 st_mkt.budget = {self.st_mkt.budget}")
    
    # Add this debug HERE to see when it gets zeroed:
    # print(f"🔍 BEFORE variable resets: bal_avail = ${self.bal_avail}")

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
        "spend_pair_max": {
            "***": 25,
            "BTC-USDC": 1000,
            "ETH-USDC": 1000,
            "SOL-USDC": 1000
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

    self.budget.symb         = self.mkt.symb
    self.budget.open_cnt     = 0
    self.budget.open_up_cnt  = 0
    self.budget.open_dn_cnt  = 0
    self.budget.open_up_pct  = 0
    self.budget.open_dn_pct  = 0
    self.budget.spent_amt    = 0
    self.budget.spent_up_amt = 0
    self.budget.spent_dn_amt = 0
    self.budget.spent_up_pct = 0
    self.budget.spent_dn_pct = 0

    sql = f"""
    select p.buy_strat_type, count(p.pos_id) as open_cnt, sum(p.tot_out_cnt) as spent_amt
        from poss p
        where p.quote_curr_symb = '{self.mkt.symb}'
        and p.pos_stat in ('OPEN','SELL')
        and p.ignore_tf = 0
        and p.test_txn_yn = 'N'
        group by p.buy_strat_type
    """
    open_data = self.cbtrade_db.seld(sql, always_list_yn='Y')
    if open_data:
        for x in open_data:
            # print(type(x))
            # print(x)
            x = AttrDict(x)
            if x.buy_strat_type == 'up':
                self.budget.open_up_cnt += x.open_cnt
                self.budget.spent_up_amt += x.spent_amt
            elif x.buy_strat_type == 'dn':
                self.budget.open_dn_cnt += x.open_cnt
                self.budget.spent_dn_amt += x.spent_amt
            self.budget.open_cnt += x.open_cnt
            self.budget.spent_amt += x.spent_amt
            x = None

    self.budget.spend_max_amt      = self.st_mkt.budget.spend_max_amt
    # print(f"🔍 spend_max_amt = ${self.spend_max_amt}")
    self.budget.spend_up_max_pct   = self.st_mkt.budget.spend_up_max_pct
    self.budget.spend_dn_max_pct   = self.st_mkt.budget.spend_up_max_pct
    self.budget.spend_up_max_amt   = self.budget.spend_up_max_pct / 100 * self.budget.spend_max_amt
    self.budget.spend_dn_max_amt   = self.budget.spend_dn_max_pct / 100 * self.budget.spend_max_amt

    # 🔴 GILFOYLE: Calculate undesignated pair budget limits
    self.budget.undesignated_max_pct = self.st_mkt.budget.get('undesignated_max_pct', 10.0)
    self.budget.undesignated_max_spend = self.budget.spend_max_amt * (self.budget.undesignated_max_pct / 100)
    self.budget.undesignated_pair_max_pct = self.st_mkt.budget.get('undesignated_pair_max_pct', 10.0)
    self.budget.undesignated_individual_max = self.budget.undesignated_max_spend * (self.budget.undesignated_pair_max_pct / 100)
    
    # Query database for current undesignated spending
    designated_pairs = self.st_mkt.pairs.trade_pairs  # List of designated pairs
    if designated_pairs:
        designated_pairs_str = "','".join(designated_pairs)
        sql = f"""
            SELECT COALESCE(SUM(p.tot_out_cnt * p.prc_buy), 0) as undesignated_spend
            FROM poss p
            WHERE p.quote_curr_symb = '{self.mkt_symb}'
              AND p.pos_stat IN ('OPEN','SELL')
              AND p.prod_id NOT IN ('{designated_pairs_str}')
              AND p.test_txn_yn = 'N'
              AND p.ignore_tf = 0
        """
        result = self.cbtrade_db.seld(sql, always_list_yn='Y')
        self.budget.undesignated_current_spend = float(result[0]['undesignated_spend']) if result and result[0]['undesignated_spend'] else 0.0
    else:
        # No designated pairs defined, all pairs are undesignated
        self.budget.undesignated_current_spend = self.budget.open_trade_amt
    
    print(f"🔍 budget_refresh UNDESIGNATED: max_pct={self.budget.undesignated_max_pct}%, max_spend=${self.budget.undesignated_max_spend:.2f}, current_spend=${self.budget.undesignated_current_spend:.2f}, individual_max=${self.budget.undesignated_individual_max:.2f}")

    self.budget.spent_pct          = round((self.budget.spent_amt / self.budget.spend_max_amt) * 100)

    self.budget.spent_up_pct       = 0
    self.budget.spent_dn_pct       = 0
    if self.budget.spent_amt > 0:
        self.budget.spent_up_pct   = round((self.budget.spent_up_amt / self.budget.spent_amt) * 100)
        self.budget.spent_dn_pct   = round((self.budget.spent_dn_amt / self.budget.spent_amt) * 100)

    self.budget.spendable_up_amt   = min(self.budget.spendable_amt, (self.budget.spend_up_max_amt - self.budget.spent_up_amt))
    self.budget.spendable_dn_amt   = min(self.budget.spendable_amt, (self.budget.spend_up_max_amt - self.budget.spent_dn_amt))

    # Add this debug AFTER to see if resets affected it:
    # print(f"🔍 AFTER variable resets: bal_avail = ${self.bal_avail}")

#<=====>#

@narc(1)
def budget_reserves_calc(self):
    if self.debug_tf: G(f'==> budget_base.budget_reserves_calc()')
    # print(f"🔍 budget_reserves_calc START: bal_avail = ${self.bal_avail}")
    day                            = dt.now(timezone.utc).day
    min_reserve_amt                = self.st_mkt.budget.reserve_amt
    daily_reserve_amt              = self.st_mkt.budget.reserve_addtl_daily_amt
    tot_daily_reserve_amt          = day * daily_reserve_amt

    if self.budget.reserve_locked_tf:
        self.budget.reserve_amt           = tot_daily_reserve_amt + min_reserve_amt
    else:
        self.budget.reserve_amt           = min_reserve_amt
    # print(f"🔍 reserve_amt = ${self.reserve_amt}")
    # print(f"🔍 spendable_amt = ${self.spendable_amt}")
    # print(f"🔍 budget_reserves_calc END: bal_avail = ${self.bal_avail}")
    # print(f"🔍 budget_reserves_calc END: spendable_amt = ${self.spendable_amt}")

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
#     """Print formatted data attributes"""
    
#     data = self.to_dict()
    
#     print('')
#     C(f"=========== MKT_BUDGET Data for {self.mkt_symb:^5} ============")
#     print('')
#     # Core balance info
#     Y(f"💰 Balance Information:")
#     print(f"  Available Balance:     ${data.get('bal_avail', 0):,.2f}")
#     print(f"  Spendable Amount:      ${data.get('spendable_amt', 0):,.2f}")
#     print(f"  Reserve Amount:        ${data.get('reserve_amt', 0):,.2f}")
#     print(f"  Reserve Locked:        {data.get('reserve_locked_tf', False)}")
#     print(f"  Open Trade Amount:     ${data.get('open_trade_amt', 0):,.2f}")
    
#     # Spending limits
#     Y(f"📊 Spending Limits:")
#     print(f"  Max Spend Amount:      ${data.get('spend_max_amt', 0):,.2f}")
#     print(f"  Up Max Percentage:     {data.get('spend_up_max_pct', 0):,.1f}%")
#     print(f"  Down Max Percentage:   {data.get('spend_dn_max_pct', 0):,.1f}%")
#     print(f"  Up Max Amount:         ${data.get('spend_up_max_amt', 0):,.2f}")
#     print(f"  Down Max Amount:       ${data.get('spend_dn_max_amt', 0):,.2f}")
    
#     # Current usage
#     Y(f"📈 Current Usage:")
#     print(f"  Total Open Count:      {data.get('open_cnt', 0)}")
#     print(f"  Open Up Count:         {data.get('open_up_cnt', 0)}")
#     print(f"  Open Down Count:       {data.get('open_dn_cnt', 0)}")
#     print(f"  Total Spent:           ${data.get('spent_amt', 0):,.2f} ({data.get('spent_pct', 0)}%)")
#     print(f"  Spent Up:              ${data.get('spent_up_amt', 0):,.2f} ({data.get('spent_up_pct', 0)}%)")
#     print(f"  Spent Down:            ${data.get('spent_dn_amt', 0):,.2f} ({data.get('spent_dn_pct', 0)}%)")
    
#     # Available spending
#     Y(f"💵 Available Spending:")
#     print(f"  Spendable Up Amount:   ${data.get('spendable_up_amt', 0):,.2f}")
#     print(f"  Spendable Down Amount: ${data.get('spendable_dn_amt', 0):,.2f}")
    
#     # Additional data (if any)
#     Y(f"📋 Other Data:")
#     for key, value in data.items():
#         if key not in [
#             'mkt_symb', 'bal_avail', 'spendable_amt', 'reserve_amt', 'reserve_locked_tf',
#             'open_trade_amt', 'spend_max_amt', 'spend_up_max_pct', 'spend_dn_max_pct',
#             'spend_up_max_amt', 'spend_dn_max_amt', 'open_cnt', 'open_up_cnt', 'open_dn_cnt',
#             'spent_amt', 'spent_pct', 'spent_up_amt', 'spent_up_pct', 'spent_dn_amt',
#             'spent_dn_pct', 'spendable_up_amt', 'spendable_dn_amt', 'symb'
#         ]:
#             if isinstance(value, (int, float)):
#                 if isinstance(value, float) and value >= 1:
#                     print(f"  {key}: {value:,.2f}")
#                 else:
#                     print(f"  {key}: {value}")
#             else:
#                 print(f"  {key}: {value}")
    
#     C(f"{'=' * 50}")
#     print('')

#<=====>#

@narc(1)
def disp_budget(self): 
    if self.debug_tf: G(f'==> budget_base.disp_budget()')
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
    hmsg += f"$ {'spend_max':^12} | "
    hmsg += f"{'spent_pct':^12} % | "
    hmsg += f"$ {'spent_up_amt':^12} | "
    hmsg += f"$ {'spent_up_max':^12} | "
    hmsg += f"{'up_pct':^12} % | "
    hmsg += f"$ {'spent_dn_amt':^12} | "
    hmsg += f"$ {'spent_dn_max':^12} | "
    hmsg += f"{'dn_pct':^12} %"
    self.chrt.chart_headers(in_str=hmsg, len_cnt=260)

    disp_font_color = 'white'
    disp_bg_color   = 'green'
    if self.budget.spent_pct >= 100 or self.budget.spent_up_pct >= 100 or self.budget.pair_spent_pct >= 100:
        disp_bg_color = 'red'

    msg = ""
    msg += self.spacer + "| "
    msg += cs(f"{'mkt':<5}", font_color='white', bg_color='green') + " | "
    msg += cs(f"$ {self.buy.trade_size:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.bal_avail:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.reserve_amt:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spendable_amt:>9.2f}", "white", "green") + " | "
    if self.budget.reserve_locked_tf:
        msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
    else:
        msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
    msg += cs(f"$ {self.budget.spent_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spend_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.spent_pct:>12.2f} %", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spent_up_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spend_up_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.spent_up_pct:>12.2f} %", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spent_dn_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spend_dn_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.spent_dn_pct:>12.2f} %", "white", "green")
    self.chrt.chart_row(in_str=msg, len_cnt=260, font_color=disp_font_color, bg_color=disp_bg_color)

    disp_font_color = 'white'
    disp_bg_color   = 'green'
    if self.budget.pair_spent_pct >= 100 or self.budget.pair_spent_up_pct >= 100 or self.budget.pair_spent_dn_pct >= 100:
        disp_bg_color = 'red'

    msg = ""
    msg += self.spacer + "| "
    msg += cs(f"{'pair':<5}", font_color='white', bg_color='green') + " | "
    msg += cs(f"$ {self.buy.trade_size:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.bal_avail:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.reserve_amt:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spendable_amt:>9.2f}", "white", "green") + " | "
    if self.buy.reserve_locked_tf:
        msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
    else:
        msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
    msg += cs(f"$ {self.budget.pair_spent_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spend_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.pair_spent_pct:>12.2f} %", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spent_up_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spend_up_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.pair_spent_up_pct:>12.2f} %", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spent_dn_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spend_dn_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.pair_spent_dn_pct:>12.2f} %", "white", "green")
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

@narc(1)
def disp_budgetX(self):
    if self.debug_tf: G(f'==> budget_base.disp_budgetX()')
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
    hmsg += f"$ {'spend_max':^12} | "
    hmsg += f"{'spent_pct':^12} % | "
    hmsg += f"$ {'spent_up_amt':^12} | "
    hmsg += f"$ {'spent_up_max':^12} | "
    hmsg += f"{'up_pct':^12} % | "
    hmsg += f"$ {'spent_dn_amt':^12} | "
    hmsg += f"$ {'spent_dn_max':^12} | "
    hmsg += f"{'dn_pct':^12} %"
    self.chrt.chart_headers(in_str=hmsg, len_cnt=260)

    disp_font_color = 'white'
    disp_bg_color   = 'green'
    if self.budget.spent_pct >= 100 or self.budget.spent_up_pct >= 100 or self.budget.pair_spent_pct >= 100:
        disp_bg_color = 'red'

    msg = ""
    msg += self.spacer + "| "
    msg += cs(f"{'mkt':<5}", font_color='white', bg_color='green') + " | "
    msg += cs(f"$ {self.buy.trade_size:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.bal_avail:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.reserve_amt:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spendable_amt:>9.2f}", "white", "green") + " | "
    if self.budget.reserve_locked_tf:
        msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
    else:
        msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
    msg += cs(f"$ {self.budget.spent_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spend_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.spent_pct:>12.2f} %", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spent_up_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spend_up_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.spent_up_pct:>12.2f} %", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spent_dn_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spend_dn_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.spent_dn_pct:>12.2f} %", "white", "green")
    self.chrt.chart_row(in_str=msg, len_cnt=260, font_color=disp_font_color, bg_color=disp_bg_color)

    disp_font_color = 'white'
    disp_bg_color   = 'green'
    if self.budget.pair_spent_pct >= 100 or self.budget.pair_spent_up_pct >= 100 or self.budget.pair_spent_dn_pct >= 100:
        disp_bg_color = 'red'

    msg = ""
    msg += self.spacer + "| "
    msg += cs(f"{'pair':<5}", font_color='white', bg_color='green') + " | "
    msg += cs(f"$ {self.buy.trade_size:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.bal_avail:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.reserve_amt:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.spendable_amt:>9.2f}", "white", "green") + " | "
    if self.buy.reserve_locked_tf:
        msg += cs(f"{'LOCKED':^14}", "yellow", "magenta") + " | "
    else:
        msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow") + " | "
    msg += cs(f"$ {self.budget.pair_spent_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spend_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.pair_spent_pct:>12.2f} %", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spent_up_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spend_up_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.pair_spent_up_pct:>12.2f} %", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spent_dn_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.pair_spend_dn_max_amt:>12.6f}", "white", "green") + " | "
    msg += cs(f"{self.budget.pair_spent_dn_pct:>12.2f} %", "white", "green")
    self.chrt.chart_row(in_str=msg, len_cnt=260, font_color=disp_font_color, bg_color=disp_bg_color)

    # Market Basics
    prod_id = self.buy.prod_id

    # Prices & Balances
    hmsg = ""

    # msg = ""
    # self.chrt.chart_headers(in_str=hmsg, bold=True)
    # self.chrt.chart_row(in_str=msg)
    # self.chrt.chart_mid(bold=True)

#<=====>#

@narc(1)
def disp_mkt_budget(self, title=None, budget=None, footer=None):
    if self.debug_tf: G(f'==> budget_base.disp_mkt_budget()')
    if title:
        self.chrt.chart_top(in_str=title, len_cnt=260)
    else:
        self.chrt.chart_top(len_cnt=260)

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
    self.chrt.chart_headers(in_str=hmsg, len_cnt=260)

    msg = ""
    msg += f"{self.budget.symb:^6}" + " | "
    msg += f"${self.budget.spent_amt:>12.4f}" + " | "
    msg += f"${self.budget.spend_max_amt:>12.4f}" + " | "
    msg += f"{self.budget.spent_pct:>12.2f} %" + " | "
    msg += f"${self.budget.spent_up_amt:>12.4f}" + " | "
    msg += f"{self.budget.spent_up_pct:>12.2f} %" + " | "
    msg += f"${self.budget.spent_dn_amt:>12.4f}" + " | "
    msg += f"{self.budget.spent_dn_pct:>12.2f} %" + " | "
    msg += cs(f"$ {self.budget.bal_avail:>9.2f}", "white", "green") + " | "
    msg += cs(f"$ {self.budget.reserve_amt:>9.2f}", "white", "green") + " | "
    if self.budget.spendable_amt > 0:
        msg += cs(f"$ {self.budget.spendable_amt:>12.5f}", "white", "green") + " | "
    else:
        msg += cs(f"$ {self.budget.spendable_amt:>12.5f}", "white", "red") + " | "
    if self.budget.spendable_up_amt > 0:
        msg += cs(f"$ {self.budget.spendable_up_amt:>12.5f}", "white", "green") + " | "
    else:
        msg += cs(f"$ {self.budget.spendable_up_amt:>12.5f}", "white", "red") + " | "
    if self.budget.spendable_dn_amt > 0:
        msg += cs(f"$ {self.budget.spendable_dn_amt:>12.5f}", "white", "green") + " | "
    else:
        msg += cs(f"$ {self.budget.spendable_dn_amt:>12.5f}", "white", "red") + " | "
    if self.budget.reserve_locked_tf:
        msg += cs(f"{'LOCKED':^14}", "yellow", "magenta")
    else:
        msg += cs(f"{'UNLOCKED':^14}", "magenta", "yellow")
    self.chrt.chart_row(in_str=msg, len_cnt=260)

    if footer:
        self.chrt.chart_mid(len_cnt=260)
        self.chrt.chart_row(in_str=footer, len_cnt=260)

    self.chrt.chart_bottom(in_str='', len_cnt=260, bold=True)
    print_adv()

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    pass

#<=====>#

