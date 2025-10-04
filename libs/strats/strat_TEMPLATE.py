# This template will use a RSI indicator as an example. The [Strategy Name] will be "RSI Basic", and the [Strategy Abbreviation] will be "rsi_basic". Remove this line when creating a new strategy.
#<=====>#
# Description - [rsi_basic] 
# 
# [RSI Basic] Strategy
# This strategy uses the [RSI] indicator(s) to determine buy and sell signals.
#<=====>#

#<=====>#
# Known To Do List
#
# - [List of known improvements or validations needed]
#<=====>#

#<=====>#
# Imports
#<=====>#
import sys
import numpy as np
import pandas as pd
import pandas_ta as pta
import traceback
from libs.common import beep, dttm_get, narc
from libs.common import print_adv
from libs.strats._strat_common import disp_sell_tests, exit_if_logic

#<=====>#
# Variables
#<=====>#
lib_name = 'bot_strat_[rsi_basic]'
log_name = 'bot_strat_[rsi_basic]'

#<=====>#
# Assignments Pre
#<=====>#
# (Any pre-assignments if needed)
strat_name = 'RSI Basic'
strat_abbreviation = 'rsi_basic'

#<=====>#
# Classes
#<=====>#
# (No custom classes are defined in this module)


#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_rsi_basic(st):
    """
    [Edit The Following As Appropriate]
    Define and assign the settings for the RSI Basic strategy.
    """
    # this is pretty much the standard and should not be changed..
    sst = {
        "use_yn": "Y",
        "freqs": ["1d", "4h", "1h", "30min", "15min"],
        "buy": {
            "prod_ids": [],
            "skip_prod_ids": [],
            "tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
            "boost_tests_min": {"15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11},
            "max_open_poss_cnt_live": {
                "***": 2,
                "BTC-USDC": 5,
                "ETH-USDC": 5,
                "SOL-USDC": 5,
                "XRP-USDC": 3
            },
            "max_open_poss_cnt_test": {
                "***": 2,
                "BTC-USDC": 5,
                "ETH-USDC": 5,
                "SOL-USDC": 5,
                "XRP-USDC": 3
            },
            "show_tests_yn": "Y"
        },
        "sell": {
            "exit_if_profit_yn": "Y",
            "exit_if_profit_pct_min": 1,
            "exit_if_loss_yn": "N",
            "exit_if_loss_pct_max": 3,
            "show_tests_yn": "Y"
        }
    }

    # Any settings that are required for the technical indicators should be added here... for example:
    sst["source"]          = 'close'
    sst["period"]          = 14
    sst["buy_rsi"]         = 25
    sst["sell_rsi"]        = 75

    st['strats']['rsi_basic'] = sst
    return st

#<=====>#

# @safe_execute()
@narc(1)
def ta_add_rsi(df: pd.DataFrame, src='close', per=14) -> pd.DataFrame:
    """Add strategy-specific indicators to DataFrame"""
    # Indicator calculations
    df['rsi'] = pta.rsi(df[src], length=per)
    return df

#<=====>#

# @safe_execute()
@narc(1)
def buy_strat_rsi_basic(buy, ta, st_pair, curr_prc=None):
    """
    [Edit The Following As Appropriate]
    RSI Basic Buy Strategy:
    
    - Calculates the [RSI] indicator.
    - Generates a buy signal if:
        1. The [RSI] crosses below the [buy_rsi] value.
    
    The function cleans up temporary columns and sets the buy signal status.
    """

    # STRAT RSI Basic
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df
    buy.buy_hist = []
    # To avoid potential division by zero, define a small epsilon. Add to a divisor if needed.
    eps = 1e-8

    # Set the current price
    df['curr_prc'] = df['close']
    if curr_prc:
        df['curr_prc'].iloc[-1] = curr_prc

    # -----------------------------
    # Strategy-specific Edits Begin here and can be added until 'Strategy-specific Edits End'
    # -----------------------------

    buy.buy_strat_type = 'up'
    buy.buy_strat_name = 'rsi_basic'
    buy.buy_strat_freq = freq

    # Get the strategy settings
    src = st_pair.strats.rsi_basic.source
    per = st_pair.strats.rsi_basic.period
    buy_rsi = st_pair.strats.rsi_basic.buy_rsi
    sell_rsi = st_pair.strats.rsi_basic.sell_rsi

    # Ensure the moving average periods do not exceed the available data length
    per = min(per, len(df))

    # Add Indicators Here
    df = ta_add_rsi(df, src=src, per=per)

    # Add Other Calculations Here.  Only adding to to delete later
    df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3

    # Final Buy Signal Condition
    # The buy signal now requires:
    # 1. rsi indicator to have been below the buy_rsi value in past 2 periods.
    # 2. rsi indicator to be above the buy_rsi value.
    df[f'{strat_abbreviation}_buy_signal'] = (
        (df['rsi'] > buy_rsi) & 
        ((df['rsi'].shift(1) < buy_rsi) & (df['rsi'].shift(2) < buy_rsi)) &
        (df['rsi'] < sell_rsi)
    )

    # Clean Up Temporary Columns
    for c in ('hlc3'):
        if c in df.columns:
            df.pop(c)

    # -----------------------------
    # Strategy-specific Edits End.  The remaing portions of this function do not change.
    # -----------------------------

    # Record buy history based on the signals found.
    buy_hist = []
    if df.get(f'{strat_abbreviation}_buy_signal', pd.Series()).any():
        signal_times = df[df[f'{strat_abbreviation}_buy_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            buy_hist.append(signal_time)

    # Set the current buy signal status
    buy_now = df[f'{strat_abbreviation}_buy_signal'].iloc[-1] if f'{strat_abbreviation}_buy_signal' in df.columns else 0

    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
    else:
        buy.buy_yn = 'N'
        buy.wait_yn = 'Y'
        buy.buy_strat_type = None
        buy.buy_strat_name = None
        buy.buy_strat_freq = None

    buy.buy_hist = buy_hist
    
    # Update the TA dictionary with the modified DataFrame.
    ta[freq].df = df

    return buy, ta

#<=====>#

# @safe_execute()
@narc(1)
def sell_strat_rsi_basic(mkt, pos, ta, st_pair, curr_prc=None):
    """
    [Edit The Following As Appropriate]
    RSI Basic Sell Strategy:
    
    - Calculates the RSI indicator based on settings
    - Generates a sell signal if:
        1. The RSI crosses above the sell_rsi value.
        2. The previous RSI was below (or equal to) the sell_rsi value.
    
    The function cleans up temporary columns and sets the sell signal status.
    """

    # STRAT RSI_BASIC
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df
    pos.sell_hist = []
    # To avoid potential division by zero, define a small epsilon. Add to a divisor if needed.
    eps = 1e-8

    # Set the current price
    df['curr_prc'] = df[src]
    if curr_prc:
        df['curr_prc'].iloc[-1] = curr_prc

    # -----------------------------
    # Strategy-specific Edits Begin here and can be added until 'Strategy-specific Edits End'
    # -----------------------------
    pos.sell_strat_type = 'up'
    pos.sell_strat_name = strat_abbreviation
    pos.sell_strat_freq = freq

    # Get the strategy settings
    src = st_pair.strats.rsi_basic.source
    per = st_pair.strats.rsi_basic.period
    buy_rsi = st_pair.strats.rsi_basic.buy_rsi
    sell_rsi = st_pair.strats.rsi_basic.sell_rsi

    # Ensure the moving average periods do not exceed the available data length
    per = min(per, len(df))

    # Add Indicators Here
    df = ta_add_rsi(df, src=src, per=per)

    # Add Other Calculations Here.  Only adding to to delete later
    df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3

    # Final Buy Signal Condition
    # The buy signal now requires:
    # 1. rsi indicator to have been below the buy_rsi value in past 2 periods.
    # 2. rsi indicator to be above the buy_rsi value.
    df[f'{strat_abbreviation}_sell_signal'] = (
        (df['rsi'] < sell_rsi) & 
        ((df['rsi'].shift(1) > sell_rsi) & (df['rsi'].shift(2) > sell_rsi)) &
        (df['rsi'] > buy_rsi)
    )

    # Clean Up Temporary Columns
    for c in ('hlc3'):
        if c in df.columns:
            df.pop(c)

    # -----------------------------
    # Strategy-specific Edits End.  The remaing portions of this function do not change.
    # -----------------------------

    # Record sell history based on the signals found.
    sell_hist = []
    if df.get(f'{strat_abbreviation}_sell_signal', pd.Series()).any():
        signal_times = df[df[f'{strat_abbreviation}_sell_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            sell_hist.append(signal_time)

    # Set the current sell signal status
    sell_now = df[f'{strat_abbreviation}_sell_signal'].iloc[-1] if f'{strat_abbreviation}_sell_signal' in df.columns else 0

    if sell_now:
        pos.sell_yn = 'Y'
        pos.hodl_yn = 'N'
        pos = exit_if_logic(pos=pos, st_pair=st_pair)
    else:
        pos.sell_yn = 'N'
        pos.hodl_yn = 'Y'
        pos.sell_strat_type = None
        pos.sell_strat_name = None
        pos.sell_strat_freq = None

    pos.sell_hist = sell_hist
    
    # Update the TA dictionary with the modified DataFrame.
    ta[freq].df = df

    return mkt, pos, ta


#<=====>#
# Post Variables
#<=====>#
# (Any post-run variables can be defined here)


#<=====>#
# Default Run
#<=====>#
# (Default run code, if this file is run as a standalone script)
#<=====>#

