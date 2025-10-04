#<=====>#
# Description
#
# This module implements the NWE 3‑Row trading strategy. It uses the Nadaraya‑Watson Envelope
# (NWE) indicator along with its rate of change (ROC) and color conditions to generate buy and sell signals.
#
# The strategy signals a buy when three consecutive candles show a green NWE color and positive ROC,
# and a sell when three consecutive candles show a red NWE color and negative ROC. Additional checks 
# (including Heikin‑Ashi candle confirmation across multiple timeframes) are applied to further validate signals.
#<=====>#


#<=====>#
# Known To Do List
#
# - Verify integration with the overall trading bot.
# - Consider additional risk management parameters.
# - Fine‑tune thresholds and conditions based on backtesting.
# - Confirm that requiring both 'color' and 'ha_color' to be green on the sell side is intended.
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
from scipy.ndimage import gaussian_filter1d  # used for Gaussian smoothing

#<=====>#
# Variables
#<=====>#
lib_name = 'bot_strat_nwe_3row'
log_name = 'bot_strat_nwe_3row'


#<=====>#
# Strategy Settings Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_nwe_3row(st):
    """
    Define and assign settings for the NWE 3‑Row buy strategy.
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
    st['strats']['nwe_3row'] = sst
    return st

#<=====>#

# @safe_execute()
@narc(1)
def buy_strat_nwe_3row(buy, ta, st_pair, curr_prc=None):
    """
    NWE 3‑Row Buy Strategy:
    
    - Evaluates the NWE indicator across multiple timeframes.
    - Checks that the NWE color is green in the current, previous, and two periods ago.
    - Ensures that the NWE ROC is positive in the current and previous period.
    - Confirms that both the overall 'color' and the Heikin‑Ashi 'ha_color' are green.
    - Sets the buy signal if all conditions are met.
    
    Returns:
        Updated buy object and TA dictionary.
    """

    # STRAT NWE 3 In A Row
    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.nwe_3row.src
    bandwidth = st_pair.strats.nwe_3row.bandwidth
    mult = st_pair.strats.nwe_3row.mult

    # Use Gaussian smoothing to calculate the NWE line.
    h = bandwidth
    source = df[src].values
    nwe = gaussian_filter1d(source, sigma=h, mode='nearest')

    df['nwe_line'] = nwe
    df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)

    # Determine the NWE trend color.
    df['nwe_color'] = np.where(df['nwe_line'] > df['nwe_line'].shift(1), 'green', 'red')

    # Generate 3‑row buy signals based on consecutive NWE colors and ROC conditions,
    # along with overall 'color' and 'ha_color' being green.
    df['nwe_3row_buy_signal'] = (
        (df['nwe_color'] == 'green') &
        (df['nwe_color'].shift(1) == 'green') &
        (df['nwe_color'].shift(2) == 'green') &
        (df['nwe_roc'] >= 0) &
        (df['nwe_roc'].shift(1) >= 0) &
        (df['color'] == 'green') &
        (df['ha_color'] == 'green')
    ).astype(int)

    # Record buy history based on the signals found.
    buy_hist = []
    if df.get('nwe_3row_buy_signal', pd.Series()).any():
        signal_times = df[df['nwe_3row_buy_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            buy_hist.append(signal_time)

    # Set the current buy signal status.
    buy_now = df['nwe_3row_buy_signal'].iloc[-1] if 'nwe_3row_buy_signal' in df.columns else 0

    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_type = 'up'
        buy.buy_strat_name = 'nwe_3row'
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
def sell_strat_nwe_3row(mkt, pos, ta, st_pair, curr_prc=None):
    """
    NWE 3‑Row Sell Strategy:
    
    - Evaluates the NWE indicator and its ROC.
    - Checks that the NWE color is red for the current, previous, and two periods ago.
    - Sets a sell signal if the 3‑row sell condition is met and then calls additional exit logic.
    
    Returns:
        Updated market object, position object, and TA dictionary.
    
    Note: The conditions require both 'color' and 'ha_color' to be green on a sell,
          which may be intentional if looking for a divergence.
    """

    # STRAT NWE 3 In A Row
    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.nwe_3row.src
    bandwidth = st_pair.strats.nwe_3row.bandwidth
    mult = st_pair.strats.nwe_3row.mult

    # Use Gaussian smoothing to calculate the NWE line.
    h = bandwidth
    source = df[src].values
    nwe = gaussian_filter1d(source, sigma=h, mode='nearest')

    df['nwe_line'] = nwe
    df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)

    # Determine the NWE trend color.
    df['nwe_color'] = np.where(df['nwe_line'] > df['nwe_line'].shift(1), 'green', 'red')

    # Generate 3‑row sell signals based on consecutive NWE colors and ROC conditions.
    # Note: The conditions also require that both 'color' and 'ha_color' are green.
    df['nwe_3row_sell_signal'] = (
        (df['nwe_color'] == 'red') &
        (df['nwe_color'].shift(1) == 'red') &
        (df['nwe_color'].shift(2) == 'red') &
        (df['nwe_roc'] <= 0) &
        (df['nwe_roc'].shift(1) <= 0) &
        (df['color'] == 'red') &
        (df['ha_color'] == 'red')
    ).astype(int)

    # Record sell history based on the signals found.
    sell_hist = []
    # Defensive: build mask explicitly and validate length to avoid Pandas take() segfaults
    if 'nwe_3row_sell_signal' in df.columns:
        mask = (df['nwe_3row_sell_signal'].astype('int16') == 1)
        if mask.shape[0] == df.shape[0] and mask.any():
            signal_times = df.index[mask].tolist()
        else:
            signal_times = []
    else:
        mask = None
        signal_times = []
        for signal_time in signal_times:
            sell_hist.append(signal_time)

    # Set the current sell signal status.
    sell_now = int(df['nwe_3row_sell_signal'].iloc[-1]) if 'nwe_3row_sell_signal' in df.columns else 0

    if sell_now:
        pos.sell_yn = 'Y'
        pos.hodl_yn = 'N'
        pos.sell_strat_type = 'strat'
        pos.sell_strat_name = 'nwe_3row'
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
# (Default run code, if this module is executed as a standalone script)
