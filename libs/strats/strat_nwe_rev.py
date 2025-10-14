#<=====>#
# Description
#
# This module implements the Nadaraya-Watson Reversal (NWE REV) trading strategy.
# It uses a smoothed NWE line (computed via a Gaussian filter) and detects trend
# reversals based on changes in the derivative of the NWE line. A reversal upward
# is interpreted as a bullish (buy) signal, and a reversal downward as a bearish (sell) signal.
#
# The strategy is designed to capture trend reversals by generating signals when the
# product of consecutive differences of the NWE line changes sign.
#<=====>#
 
#<=====>#
# Known To Do List
#
# - Validate and tune the reversal detection thresholds based on historical data.
# - Integrate additional risk management (e.g., stop-loss, trailing stops) if needed.
# - Confirm integration with overall trading bot infrastructure.
#<=====>#

#<=====>#
# Imports
#<=====>#
import sys
import numpy as np
import pandas as pd
import pandas_ta as pta
import traceback
from scipy.ndimage import gaussian_filter1d
from libs.common import beep, dttm_get, narc
from libs.common import print_adv
from libs.strats._strat_common import disp_sell_tests, exit_if_logic

#<=====>#
# Variables
#<=====>#
lib_name = 'bot_strat_nwe_rev'
log_name = 'bot_strat_nwe_rev'

#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_nwe_rev(st):
    """
    Define and assign the settings for the NWE REV buy strategy.
    """
    sst = {
        "use_yn": "Y",
        "freqs": ["1d", "4h", "1h", "30min", "15min"],
        "src": 'close',
        "bandwidth": 8,
        "mult": 3,
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
    st['strats']['nwe_rev'] = sst
    return st

#<=====>#

# @safe_execute()
@narc(1)
def buy_strat_nwe_rev(buy, ta, st_pair, curr_prc=None):
    """
    NWE REV Buy Strategy:
    
    - Computes the NWE line using Gaussian smoothing on the source price data.
    - Calculates the NWE rate of change (ROC) and determines the trend color.
    - Computes the derivative of the NWE line and detects reversal points.
         • A bullish reversal (reversal_up) is detected when the product of the current and previous differences is negative and the previous difference is negative.
    - Generates a buy signal if the current reversal buy signal (or the previous one, if the current is absent) indicates a bullish trend,
      and if the overall conditions (NWE trend is green, and both 'color' and 'ha_color' are green) are met.
    - Records buy history and sets the buy signal flag accordingly.
    
    Returns:
        Updated buy object and TA dictionary.
    """

    # STRAT NWE Reversal
    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.nwe_rev.src
    bandwidth = st_pair.strats.nwe_rev.bandwidth
    mult = st_pair.strats.nwe_rev.mult

    # --- Calculate the NWE Line, ROC, and Trend Color ---
    h = bandwidth
    source = df[src].values
    nwe = gaussian_filter1d(source, sigma=h, mode='nearest')
    df['nwe_line'] = nwe
    df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)
    df['nwe_color'] = np.where(df['nwe_line'] > df['nwe_line'].shift(1), 'green', 'red')
    
    # --- Calculate the Reversal Signals ---
    df['nwe_diff'] = df['nwe_line'].diff()
    df['nwe_diff_last'] = df['nwe_diff'].shift(1)
    df['reversal'] = (df['nwe_diff'] * df['nwe_diff_last'] < 0)
    df['reversal_up'] = df['reversal'] & (df['nwe_diff_last'] < 0)
    df['reversal_down'] = df['reversal'] & (df['nwe_diff_last'] > 0)
    df['nwe_rev_buy_signal'] = df['reversal_up'].astype(int)
    
    # Generate a 3‑row style buy signal:
    # A buy signal is triggered if the current or previous reversal buy signal is 1,
    # and the overall NWE trend is green, as well as both 'color' and 'ha_color' being green.
    df['nwe_rev_buy_signal'] = (
        ((df['nwe_rev_buy_signal'] == 1) | (df['nwe_rev_buy_signal'].shift(1) == 1)) &
        (df['nwe_color'] == 'green') &
        (df['color'] == 'green') &
        (df['ha_color'] == 'green')
    ).astype(int)
    
    # Record buy history based on the reversal buy signals.
    buy_hist = []
    if df.get('nwe_rev_buy_signal', pd.Series()).any():
        signal_times = df[df['nwe_rev_buy_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            buy_hist.append(signal_time)
    
    # Set the current buy signal status.
    buy_now = df['nwe_rev_buy_signal'].iloc[-1] if 'nwe_rev_buy_signal' in df.columns else 0
    
    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_type = 'dn'
        buy.buy_strat_name = 'nwe_rev'
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
def sell_strat_nwe_rev(mkt, pos, ta, st_pair, curr_prc=None):
    """
    NWE REV Sell Strategy:
    
    - Computes the NWE line using Gaussian smoothing and its ROC.
    - Determines the NWE trend color.
    - Computes the derivative of the NWE line and detects downward reversal points.
         • A bearish reversal (reversal_down) is detected when the product of the current and previous differences is negative and the previous difference is positive.
    - Generates a sell signal if the current (or previous) reversal sell signal is 1,
      and if the overall conditions (NWE trend is red, and both 'color' and 'ha_color' are red) are met.
    - Records sell history and sets the sell signal flag accordingly.
    - Calls additional exit logic.
    
    Returns:
        Updated market object, position object, and TA dictionary.
    """

    # STRAT NWE ENV
    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.nwe_rev.src
    bandwidth = st_pair.strats.nwe_rev.bandwidth
    mult = st_pair.strats.nwe_rev.mult

    # --- Calculate the NWE Line, ROC, and Trend Color ---
    h = bandwidth
    source = df[src].values
    nwe = gaussian_filter1d(source, sigma=h, mode='nearest')
    df['nwe_line'] = nwe
    df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)
    df['nwe_color'] = np.where(df['nwe_line'] > df['nwe_line'].shift(1), 'green', 'red')
    
    # --- Calculate the Reversal Signals (Sell Side) ---
    df['nwe_diff'] = df['nwe_line'].diff()
    df['nwe_diff_last'] = df['nwe_diff'].shift(1)
    df['reversal'] = (df['nwe_diff'] * df['nwe_diff_last'] < 0)
    df['reversal_down'] = df['reversal'] & (df['nwe_diff_last'] > 0)
    df['nwe_rev_sell_signal'] = df['reversal_down'].astype(int)
    
    # Generate a 3‑row style sell signal:
    # A sell signal is triggered if the current or previous reversal sell signal is 1,
    # and the overall NWE trend is red, and both overall 'color' and 'ha_color' are red.
    df['nwe_rev_sell_signal'] = (
        ((df['nwe_rev_sell_signal'] == 1) | (df['nwe_rev_sell_signal'].shift(1) == 1)) &
        (df['nwe_color'] == 'red') &
        (df['color'] == 'red') &
        (df['ha_color'] == 'red')
    ).astype(int)
    
    # Record sell history based on the reversal sell signals.
    sell_hist = []
    if df.get('nwe_rev_sell_signal', pd.Series()).any():
        signal_times = df[df['nwe_rev_sell_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            sell_hist.append(signal_time)
    
    # Set the current sell signal status.
    sell_now = df['nwe_rev_sell_signal'].iloc[-1] if 'nwe_rev_sell_signal' in df.columns else 0
    
    if sell_now:
        pos.sell_yn = 'Y'
        pos.hodl_yn = 'N'
        pos.sell_strat_type = 'strat'
        pos.sell_strat_name = 'nwe_rev'
        pos.sell_strat_freq = freq
        pos = exit_if_logic(pos=pos, st_pair=st_pair)
    else:
        pos.sell_yn = 'N'
        pos.hodl_yn = 'Y'
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
# (Default run code if this module is executed as a standalone script)
#<=====>#

