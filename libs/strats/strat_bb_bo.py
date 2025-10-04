#<=====>#
# Description
#
# This module implements a Bollinger Band Breakout (BB BO) trading strategy.
# It calculates Bollinger Bands using a given period and standard deviation,
# computes rate of change (ROC) for the upper and lower bands, and determines 
# whether the bands are expanding, contracting, or moving upward/downward.
#
# A buy signal is generated when the current price is above the upper Bollinger band
# and at least one of the previous three candles had a price below the upper band,
# with additional color conditions (both 'color' and 'ha_color' must be green).
# The sell strategy, in this implementation, is left empty.
#<=====>#


#<=====>#
# Known To Do List
#
# - Verify if the mismatched standard deviation (sd) between settings (2.1) and the
#   function default (2.5) is intentional.
# - Consider implementing a more detailed sell strategy if needed.
# - Integrate additional risk management features (e.g., stop-loss or trailing stops) if desired.
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
lib_name = 'bot_strat_bb_bo'
log_name = 'bot_strat_bb_bo'


#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_bb_bo(st):
    """
    Define and assign the settings for the Bollinger Band Breakout buy strategy.
    """
    sst = {
        "use_yn": "Y",
        "freqs": ["1d", "4h", "1h", "30min", "15min"],
        "src": 'close',
        "per": 21,
        "sd": 2.5,
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
    st['strats']['bb_bo'] = sst
    return st

#<=====>#

# @safe_execute()
@narc(1)
def buy_strat_bb_bo(buy, ta, st_pair, curr_prc=None):
    """
    Bollinger Band Breakout Buy Strategy:
    
    - Calculates Bollinger Bands using a specified period (per) and standard deviation (sd).
    - Computes the Rate of Change (ROC) for the upper and lower bands and identifies 
      whether the bands are expanding, contracting, or trending up/down.
    - Generates a buy signal when the current price is above the upper band and at least
      one of the previous three candles had a price below the upper band, and when both
      'color' and 'ha_color' are green.
      
    The function records a buy history based on the signal times and updates the buy signal.
    """

    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.bb_bo.src
    per = st_pair.strats.bb_bo.per
    sd = st_pair.strats.bb_bo.sd

    # Ensure the period does not exceed the number of available data points.
    per = min(per, len(df))

    # Set the current price.
    df['curr_prc'] = df['close']
    if curr_prc:
        df['curr_prc'].iloc[-1] = curr_prc

    # Calculate Bollinger Bands.
    bbands = pta.bbands(df['close'], length=per, std=sd)

    # Extract upper, lower, middle bands, band width, and band percentage.
    df[f'bb_bo_upper'] = bbands[f'BBU_{per}_{sd}']
    df[f'bb_bo_lower'] = bbands[f'BBL_{per}_{sd}']
    df[f'bb_bo_mid'] = bbands[f'BBM_{per}_{sd}']
    df[f'bb_bo_width'] = bbands[f'BBB_{per}_{sd}']
    df[f'bb_bo_pct'] = bbands[f'BBP_{per}_{sd}']

    # Calculate Rate of Change (ROC) for upper and lower bands (length=3).
    df[f'bb_bo_upper_roc'] = pta.roc(df[f'bb_bo_upper'], length=3)
    df[f'bb_bo_lower_roc'] = pta.roc(df[f'bb_bo_lower'], length=3)

    # Determine if bands are expanding or contracting.
    df[f'bb_bo_expanding'] = (df[f'bb_bo_upper_roc'] > 0) & (df[f'bb_bo_lower_roc'] < 0)
    df[f'bb_bo_contracting'] = (df[f'bb_bo_upper_roc'] < 0) & (df[f'bb_bo_lower_roc'] > 0)

    # Determine if bands are heading up or down.
    df[f'bb_bo_upwards'] = (df[f'bb_bo_upper_roc'] > 0) & (df[f'bb_bo_lower_roc'] > 0)
    df[f'bb_bo_downwards'] = (df[f'bb_bo_upper_roc'] < 0) & (df[f'bb_bo_lower_roc'] < 0)

    # Generate Buy Signal:
    # Current price must be above the upper band and at least one of the previous 3 candles had a price below the upper band.
    # Additionally, both the overall 'color' and the Heikin-Ashi 'ha_color' must be green.
    df[f'bb_bo_buy_signal'] = (
        (df['curr_prc'] > df[f'bb_bo_upper']) &
        (
            (df['curr_prc'].shift(1) < df[f'bb_bo_upper'].shift(1)) |
            (df['curr_prc'].shift(2) < df[f'bb_bo_upper'].shift(2)) |
            (df['curr_prc'].shift(3) < df[f'bb_bo_upper'].shift(3))
        ) &
        (df['color'] == 'green') &
        (df['ha_color'] == 'green')
    )

    # Record buy history based on signal times.
    buy_hist = []
    if df[f'bb_bo_buy_signal'].any():
        signal_times = df[df[f'bb_bo_buy_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            buy_hist.append(signal_time)

    # Determine current buy signal.
    buy_now = df[f'bb_bo_buy_signal'].iloc[-1]

    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_type = 'up'
        buy.buy_strat_name = 'bb_bo'
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
def sell_strat_bb_bo(mkt, pos, ta, st_pair, curr_prc=None):
    """
    Bollinger Band Breakout Sell Strategy:
    
    This strategy does not implement a sell signal.
    It simply sets the sell flag to 'N' and hold flag to 'Y'.
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
