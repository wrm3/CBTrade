#<=====>#
# Description
#
# This module implements a Bollinger Band (BB) trading strategy.
# It calculates two sets of Bollinger Bands (inner and outer) using specified
# periods and standard deviations. The strategy computes the Rate of Change (ROC)
# for both inner and outer bands and derives signals based on price action relative
# to these bands and additional color conditions.
# 
# A buy signal is generated when:
#   - The current price is above the inner lower band,
#   - And at least one of the previous three candles had a price below the outer lower band,
#   - And both the overall 'color' and the Heikin-Ashi 'ha_color' are green.
#
# The sell strategy is currently a placeholder and does not generate any sell signals.
#<=====>#


#<=====>#
# Known To Do List
#
# - Verify that the use of inner and outer bands (and the corresponding parameters)
#   meets your strategy requirements.
# - Consider enhancing the sell strategy if needed.
# - Integrate additional risk management (e.g., stop-loss or trailing stops) if desired.
#<=====>#


#<=====>#
# Imports
#<=====>#
import numpy as np
import pandas as pd
import pandas_ta as pta
import sys
import traceback
from libs.common import beep, dttm_get, narc
from libs.common import print_adv
from libs.strats._strat_common import disp_sell_tests, exit_if_logic

#<=====>#
# Variables
#<=====>#
lib_name = 'bot_strat_bb'
log_name = 'bot_strat_bb'


#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_bb(st):
    """
    Define and assign the settings for the Bollinger Band (BB) buy strategy.
    """
    sst = {
        "use_yn": "Y",
        "freqs": ["1d", "4h", "1h", "30min", "15min"],
        "src": 'close',
        "inner_per": 34,
        "inner_sd": 2.2,
        "outer_per": 34,
        "outer_sd": 2.5,
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
    st['strats']['bb'] = sst
    return st

#<=====>#

# @safe_execute()
@narc(1)
def buy_strat_bb(buy, ta, st_pair, curr_prc=None):
    """
    Bollinger Band (BB) Buy Strategy:
    
    - Calculates two sets of Bollinger Bands: inner and outer.
    - Computes ROC for the inner and outer bands and determines whether the bands
      are expanding/contracting and trending.
    - Generates a buy signal when:
          * The current price is above the inner lower band.
          * At least one of the previous three candles had a price below the outer lower band.
          * Both the overall 'color' and the Heikin-Ashi 'ha_color' are green.
    
    Records the buy history and updates the buy signal status.
    """

    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.bb.src
    inner_per = st_pair.strats.bb.inner_per
    inner_sd = st_pair.strats.bb.inner_sd
    outer_per = st_pair.strats.bb.outer_per
    outer_sd = st_pair.strats.bb.outer_sd

    # Ensure the periods do not exceed the available data length.
    inner_per = min(inner_per, len(df))
    outer_per = min(outer_per, len(df))

    # Set the current price.
    df['curr_prc'] = df['close']
    if curr_prc:
        df['curr_prc'].iloc[-1] = curr_prc

    # Calculate Bollinger Bands for the inner and outer sets.
    inner_bbands = pta.bbands(df['close'], length=inner_per, std=inner_sd)
    outer_bbands = pta.bbands(df['close'], length=outer_per, std=outer_sd)

    # --- Inner Bands ---
    df[f'bb_inner_upper'] = inner_bbands[f'BBU_{inner_per}_{inner_sd}']
    df[f'bb_inner_lower'] = inner_bbands[f'BBL_{inner_per}_{inner_sd}']
    df[f'bb_inner_mid']   = inner_bbands[f'BBM_{inner_per}_{inner_sd}']
    df[f'bb_inner_width'] = inner_bbands[f'BBB_{inner_per}_{inner_sd}']
    df[f'bb_inner_pct']   = inner_bbands[f'BBP_{inner_per}_{inner_sd}']
    # Inner Bands ROC (length=3)
    df[f'bb_inner_upper_roc'] = pta.roc(df[f'bb_inner_upper'], length=3)
    df[f'bb_inner_lower_roc'] = pta.roc(df[f'bb_inner_lower'], length=3)
    # Inner Bands expansion/contraction and trend.
    df[f'bb_inner_expanding'] = (df[f'bb_inner_upper_roc'] > 0) & (df[f'bb_inner_lower_roc'] < 0)
    df[f'bb_inner_contracting'] = (df[f'bb_inner_upper_roc'] < 0) & (df[f'bb_inner_lower_roc'] > 0)
    df[f'bb_inner_upwards'] = (df[f'bb_inner_upper_roc'] > 0) & (df[f'bb_inner_lower_roc'] > 0)
    df[f'bb_inner_downwards'] = (df[f'bb_inner_upper_roc'] < 0) & (df[f'bb_inner_lower_roc'] < 0)

    # --- Outer Bands ---
    df[f'bb_outer_upper'] = outer_bbands[f'BBU_{outer_per}_{outer_sd}']
    df[f'bb_outer_lower'] = outer_bbands[f'BBL_{outer_per}_{outer_sd}']
    df[f'bb_outer_mid']   = outer_bbands[f'BBM_{outer_per}_{outer_sd}']
    df[f'bb_outer_width'] = outer_bbands[f'BBB_{outer_per}_{outer_sd}']
    df[f'bb_outer_pct']   = outer_bbands[f'BBP_{outer_per}_{outer_sd}']
    # Outer Bands ROC (length=3)
    df[f'bb_outer_upper_roc'] = pta.roc(df[f'bb_outer_upper'], length=3)
    df[f'bb_outer_lower_roc'] = pta.roc(df[f'bb_outer_lower'], length=3)
    # Outer Bands expansion/contraction and trend.
    df[f'bb_outer_expanding'] = (df[f'bb_outer_upper_roc'] > 0) & (df[f'bb_outer_lower_roc'] < 0)
    df[f'bb_outer_contracting'] = (df[f'bb_outer_upper_roc'] < 0) & (df[f'bb_outer_lower_roc'] > 0)
    df[f'bb_outer_upwards'] = (df[f'bb_outer_upper_roc'] > 0) & (df[f'bb_outer_lower_roc'] > 0)
    df[f'bb_outer_downwards'] = (df[f'bb_outer_upper_roc'] < 0) & (df[f'bb_outer_lower_roc'] < 0)

    # Generate the buy signal:
    # Current price must be above the inner lower band, and at least one of the previous 3 candles
    # had a price below the outer lower band; plus, overall trend conditions.
    df[f'bb_buy_signal'] = (
        (df['curr_prc'] > df[f'bb_inner_lower']) &
        (
            (df['curr_prc'].shift(1) < df[f'bb_outer_lower'].shift(1)) |
            (df['curr_prc'].shift(2) < df[f'bb_outer_lower'].shift(2)) |
            (df['curr_prc'].shift(3) < df[f'bb_outer_lower'].shift(3))
        ) &
        (df['color'] == 'green') &
        (df['ha_color'] == 'green')
    )

    # Record buy history from signal times.
    buy_hist = []
    if df[f'bb_buy_signal'].any():
        signal_times = df[df[f'bb_buy_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            buy_hist.append(signal_time)

    # Set current buy signal status.
    buy_now = df[f'bb_buy_signal'].iloc[-1]
    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_type = 'dn'
        buy.buy_strat_name = 'bb'
        buy.buy_strat_freq = freq
    else:
        buy.buy_yn = 'N'
        buy.wait_yn = 'Y'
    buy.buy_hist = buy_hist
    
    # Update the TA dictionary with the modified DataFrame.
    ta[freq].df = df

    return buy, ta

#<=====>#

# @safe_execute()
@narc(1)
def sell_strat_bb(mkt, pos, ta, st_pair, curr_prc=None):
    """
    Bollinger Band (BB) Sell Strategy:
    
    This strategy does not implement any sell logic. It sets the sell flag to 'N'
    and hold flag to 'Y' (i.e., no exit is triggered).
    """
    pos.sell_hist = []
    pos.sell_yn = 'N'
    pos.hodl_yn = 'Y'

    return mkt, pos, ta

#<=====>#
# Post Variables
#<=====>#
# (Define any post-run variables here if necessary)


#<=====>#
# Default Run
#<=====>#
# (Add any default run code here if this module is executed as a standalone script)
#<=====>#
