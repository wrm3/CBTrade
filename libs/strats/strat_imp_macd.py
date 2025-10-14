#<=====>#
# Description
# 
# This module implements an impulse MACD trading strategy. It defines both the buy
# and sell logic, using a modified MACD indicator (with SMMA and ZLEMA) along with
# ATR-based filtering to avoid false signals and to ensure adequate market volatility.
#
# The indicator produces impulse signals that are further filtered by momentum,
# color conditions, and a minimum spread relative to the ATR.
#
# https://www.youtube.com/watch?v=oyepJ4zUbLE
#
#<=====>#
 

#<=====>#
# Known To Do List
#
# - Verify integration with stop-loss and take-profit logic (if needed).
# - Review parameter defaults for various frequencies and assets.
# - Ensure consistent logging and alerting across the module.
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
lib_name      = 'bot_strat_imp_macd'
log_name      = 'bot_strat_imp_macd'


#<=====>#
# Assignments Pre
#<=====>#
# (Any pre-assignments if needed)


#<=====>#
# Classes
#<=====>#
# (No custom classes are defined in this module)


#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_imp_macd(st):
    """
    Define and assign the settings for the impulse MACD buy strategy.
    """
    sst = {
        "use_yn": "Y",
        "freqs": ["1d", "4h", "1h", "30min", "15min"],
        "src": 'close',
        "per_ma": 34,
        "per_sign": 9,
        "filter_strength": True,
        "filter_period": 25,
        "threshold": 0.5,
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
    st['strats']['imp_macd'] = sst
    return st

#<=====>#

# @safe_execute()
@narc(1)
def buy_strat_imp_macd(buy, ta, st_pair, curr_prc=None):
    """
    Impulse MACD Buy Strategy:
    
    - Calculates the impulse MACD indicator using SMMA and ZLEMA.
    - Applies a momentum filter based on the histogram.
    - Uses an ATR-based spread condition to ensure sufficient market volatility.
    - Generates a buy signal if:
        1. The MACD crosses above its signal.
        2. The momentum filter condition is met.
        3. The MACD bar color is either 'lime' or 'green'.
        4. Both the general color and the Heikin-Ashi (HA) color are green.
        5. The MACD and its signal are separated by at least 3% (relative condition).
        6. The spread exceeds 3% of the ATR.
    
    The function cleans up temporary columns and sets the buy signal status.
    """

    # STRAT IMP_MACD
    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.imp_macd.src
    per_ma = st_pair.strats.imp_macd.per_ma
    per_sign = st_pair.strats.imp_macd.per_sign
    filter_strength = st_pair.strats.imp_macd.filter_strength
    filter_period = st_pair.strats.imp_macd.filter_period
    threshold = st_pair.strats.imp_macd.threshold

    # Ensure the moving average periods do not exceed the available data length
    per_ma = min(per_ma, len(df))
    per_sign = min(per_sign, len(df))

    # Set the current price
    df['curr_prc'] = df['close']
    if curr_prc:
        df['curr_prc'].iloc[-1] = curr_prc

    # -----------------------------
    # Helper Functions
    # -----------------------------
    def calc_smma(src, length):
        """
        Calculate the Smoothed Moving Average (SMMA) of the series.
        The first value is the simple moving average over the first 'length' values.
        """
        smma = np.zeros_like(src)
        smma[0] = np.mean(src[:length])
        for i in range(1, len(src)):
            smma[i] = (smma[i - 1] * (length - 1) + src.iloc[i]) / length
        return smma

    def calc_zlema(src, per):
        """
        Calculate the Zero-Lag EMA (ZLEMA) of the series.
        """
        ema1 = pta.ema(src, length=per)
        ema2 = pta.ema(ema1, length=per)
        d = ema1 - ema2
        return ema1 + d

    def calc_atr(df, period=14):
        """
        Calculate the Average True Range (ATR) for the dataframe.
        ATR is based on the True Range (TR):
            TR = max( high - low, abs(high - previous close), abs(low - previous close) )
        Then ATR is the rolling mean of TR over 'period' bars.
        """
        high = df['high']
        low = df['low']
        close = df['close']
        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period, min_periods=period).mean()
        return atr

    # -----------------------------
    # Calculate the Indicator Components
    # -----------------------------
    df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3

    df['hi'] = calc_smma(df['high'], per_ma)
    df['lo'] = calc_smma(df['low'], per_ma)
    df['mi'] = calc_zlema(df['hlc3'], per_ma)

    # Calculate md: if mi > hi then md = mi - hi; if mi < lo then md = mi - lo; otherwise, 0.
    df['md'] = np.where(df['mi'] > df['hi'], df['mi'] - df['hi'],
                            np.where(df['mi'] < df['lo'], df['mi'] - df['lo'], 0))
    df['sb'] = pta.sma(df['md'], length=per_sign)
    df['sh'] = df['md'] - df['sb']

    # Determine the color for the MACD bar (used for plotting or filtering)
    df['mdc'] = np.where(df['hlc3'] > df['mi'],
                            np.where(df['hlc3'] > df['hi'], 'lime', 'green'),
                            np.where(df['hlc3'] < df['lo'], 'red', 'orange'))

    # Save the impulse MACD components into clearly named columns for later use
    df['imp_mid'] = 0
    df['imp_macd'] = df['md']
    df['imp_macd_hist'] = df['sh']
    df['imp_macd_sign'] = df['sb']
    df['imp_macd_color'] = df['mdc']

    # -----------------------------
    # Additional Filters
    # -----------------------------
    # Momentum filter: require the histogram’s absolute value to be above an average threshold.
    df['hist_avg'] = df['sh'].rolling(window=filter_period, min_periods=filter_period).mean().abs()
    df['momentum_filter'] = (df['sh'].abs() > df['hist_avg'] * threshold) if filter_strength else True

    # -----------------------------
    # ATR-Based Filtering
    # -----------------------------
    # Calculate the ATR (using a 14-period by default; adjust as needed)
    df['atr'] = calc_atr(df, period=14)
    # Compute the spread between MACD and its signal
    df['spread'] = df['md'] - df['sb']
    # Define the minimum spread as 3% of the ATR value.
    min_spread_pct = 3  # 3%
    df['min_spread'] = df['atr'] * (min_spread_pct / 100.0)
    # Create a boolean condition for the ATR-based spread requirement.
    atr_condition = (df['spread'] > df['min_spread'])

    # -----------------------------
    # Define Other Entry/Exit Conditions (if needed)
    # -----------------------------
    df['Long_Enter'] = ((df['md'] > df['sb']) & (df['md'].shift(1) <= df['sb'].shift(1)) & df['momentum_filter']) & (df['mdc'] == 'lime')
    df['Long_Exit'] = ((df['md'] < df['sb']) & (df['md'].shift(1) >= df['sb'].shift(1)))
    df['Short_Enter'] = ((df['md'] < df['sb']) & (df['md'].shift(1) >= df['sb'].shift(1)) & df['momentum_filter']) & (df['mdc'] == 'red')
    df['Short_Exit'] = ((df['md'] > df['sb']) & (df['md'].shift(1) <= df['sb'].shift(1)))

    # -----------------------------
    # Final Buy Signal Condition
    # -----------------------------
    # To avoid potential division by zero, define a small epsilon.
    eps = 1e-8

    # The buy signal now requires:
    # 1. MACD crossing above the signal.
    # 2. The previous MACD was below (or equal to) the signal.
    # 3. The momentum filter condition is met.
    # 4. The MACD color is 'lime' or 'green'.
    # 5. Both the general color and the Heikin-Ashi (HA) color are green.
    # 6. The MACD and its signal are separated by at least 3% (relative condition).
    # 7. The spread (absolute difference) is above 3% of the ATR.
    df['imp_macd_buy_signal'] = (
        (df['md'] > df['sb']) & 
        (df['md'].shift(1) <= df['sb'].shift(1)) & 
        (df['momentum_filter']) & 
        ((df['mdc'] == 'lime') | (df['mdc'] == 'green')) & 
        (df['color'] == 'green') & 
        (df['ha_color'] == 'green') &
        (((df['md'] - df['sb']) / (df['sb'].abs() + eps)) > 0.03) &
        (atr_condition)
    )

    # -----------------------------
    # Clean Up Temporary Columns
    # -----------------------------
    for c in ('hlc3', 'hi', 'lo', 'mi', 'md', 'sb', 'sh', 'mdc', 'hist_avg', 'momentum_filter',
                'Long_Enter', 'Long_Exit', 'Short_Enter', 'Short_Exit', 'atr', 'spread', 'min_spread'):
        if c in df.columns:
            df.pop(c)

    # Record buy history based on the signals found.
    buy_hist = []
    # Defensive: build explicit mask to avoid boolean-take segfaults
    if 'imp_macd_buy_signal' in df.columns:
        mask = df['imp_macd_buy_signal'].astype('int8') == 1
        if mask.shape[0] == df.shape[0] and mask.any():
            signal_times = df.index[mask].tolist()
        else:
            signal_times = []
    else:
        signal_times = []
        for signal_time in signal_times:
            buy_hist.append(signal_time)

    # Set the current buy signal status
    buy_now = int(df['imp_macd_buy_signal'].iloc[-1]) if 'imp_macd_buy_signal' in df.columns else 0

    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_type = 'up'
        buy.buy_strat_name = 'imp_macd'
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
def sell_strat_imp_macd(mkt, pos, ta, st_pair, curr_prc=None):
    """
    Impulse MACD Sell Strategy:
    
    - Calculates the impulse MACD indicator using SMMA and ZLEMA.
    - Applies a momentum filter based on the histogram.
    - Uses an ATR-based spread condition to ensure sufficient market volatility.
    - Generates a sell signal if:
        1. The MACD crosses below its signal.
        2. The previous MACD was above (or equal to) the signal.
        3. The momentum filter condition is met.
        4. The MACD color is 'red' or 'orange'.
        5. Both the general color and the Heikin-Ashi (HA) color are red.
        6. The MACD and its signal are separated by at least 3% (in the negative direction).
        7. The spread (absolute difference) is below -3% of the ATR.
    
    The function cleans up temporary columns and sets the sell signal status.
    """

    # STRAT IMP_MACD
    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.imp_macd.src
    per_ma = st_pair.strats.imp_macd.per_ma
    per_sign = st_pair.strats.imp_macd.per_sign
    filter_strength = st_pair.strats.imp_macd.filter_strength
    filter_period = st_pair.strats.imp_macd.filter_period
    threshold = st_pair.strats.imp_macd.threshold

    # Ensure the moving average periods do not exceed the available data length
    per_ma = min(per_ma, len(df))
    per_sign = min(per_sign, len(df))

    # Set the current price
    df['curr_prc'] = df[src]
    if curr_prc:
        df['curr_prc'].iloc[-1] = curr_prc

    # -----------------------------
    # Helper Functions
    # -----------------------------
    def calc_smma(src, length):
        """
        Calculate the Smoothed Moving Average (SMMA) of the series.
        """
        smma = np.zeros_like(src)
        smma[0] = np.mean(src[:length])
        for i in range(1, len(src)):
            smma[i] = (smma[i - 1] * (length - 1) + src.iloc[i]) / length
        return smma

    def calc_zlema(src, per):
        """
        Calculate the Zero-Lag EMA (ZLEMA) of the series.
        """
        ema1 = pta.ema(src, length=per)
        ema2 = pta.ema(ema1, length=per)
        d = ema1 - ema2
        return ema1 + d

    def calc_atr(df, period=14):
        """
        Calculate the Average True Range (ATR) for the dataframe.
        """
        high = df['high']
        low = df['low']
        close = df['close']
        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period, min_periods=period).mean()
        return atr

    # -----------------------------
    # Calculate the Indicator Components
    # -----------------------------
    df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3

    df['hi'] = calc_smma(df['high'], per_ma)
    df['lo'] = calc_smma(df['low'], per_ma)
    df['mi'] = calc_zlema(df['hlc3'], per_ma)

    # Calculate md: if mi > hi then md = mi - hi; if mi < lo then md = mi - lo; otherwise, 0.
    df['md'] = np.where(df['mi'] > df['hi'], df['mi'] - df['hi'],
                            np.where(df['mi'] < df['lo'], df['mi'] - df['lo'], 0))
    df['sb'] = pta.sma(df['md'], length=per_sign)
    df['sh'] = df['md'] - df['sb']

    # Determine the color for the MACD bar (used for plotting or filtering)
    df['mdc'] = np.where(df['hlc3'] > df['mi'],
                            np.where(df['hlc3'] > df['hi'], 'lime', 'green'),
                            np.where(df['hlc3'] < df['lo'], 'red', 'orange'))

    # Save the impulse MACD components into clearly named columns for later use
    df['imp_mid'] = 0
    df['imp_macd'] = df['md']
    df['imp_macd_hist'] = df['sh']
    df['imp_macd_sign'] = df['sb']
    df['imp_macd_color'] = df['mdc']

    # -----------------------------
    # Additional Filters
    # -----------------------------
    # Momentum filter: require the histogram’s absolute value to be above an average threshold.
    df['hist_avg'] = df['sh'].rolling(window=filter_period, min_periods=filter_period).mean().abs()
    df['momentum_filter'] = (df['sh'].abs() > df['hist_avg'] * threshold) if filter_strength else True

    # -----------------------------
    # ATR-Based Filtering
    # -----------------------------
    # Calculate the ATR (using a 14-period by default; adjust as needed)
    df['atr'] = calc_atr(df, period=14)
    # Compute the spread between MACD and its signal
    df['spread'] = df['md'] - df['sb']
    # Define the minimum spread as 3% of the ATR value.
    min_spread_pct = 3  # 3%
    df['min_spread'] = df['atr'] * (min_spread_pct / 100.0)
    # For sell signals, ensure that the negative spread (sb - md) is sufficiently large.
    atr_condition_sell = (df['spread'] < -df['min_spread'])

    # -----------------------------
    # Define Other Entry/Exit Conditions (if needed)
    # -----------------------------
    df['Long_Enter'] = ((df['md'] > df['sb']) & (df['md'].shift(1) <= df['sb'].shift(1)) & df['momentum_filter']) & (df['mdc'] == 'lime')
    df['Long_Exit'] = ((df['md'] < df['sb']) & (df['md'].shift(1) >= df['sb'].shift(1)))
    df['Short_Enter'] = ((df['md'] < df['sb']) & (df['md'].shift(1) >= df['sb'].shift(1)) & df['momentum_filter']) & (df['mdc'] == 'red')
    df['Short_Exit'] = ((df['md'] > df['sb']) & (df['md'].shift(1) <= df['sb'].shift(1)))

    # -----------------------------
    # Final Sell Signal Condition
    # -----------------------------
    # To avoid potential division by zero, define a small epsilon.
    eps = 1e-8

    # The sell signal now requires:
    # 1. MACD crossing below the signal.
    # 2. The previous MACD was above (or equal to) the signal.
    # 3. The momentum filter condition is met.
    # 4. The MACD color is 'red' or 'orange'.
    # 5. Both the general color and the Heikin-Ashi (HA) color are red.
    # 6. The MACD and its signal are separated by at least 3% (in the negative direction).
    # 7. The spread (absolute difference) is below -3% of the ATR.
    df['imp_macd_sell_signal'] = (
        (df['md'] < df['sb']) & 
        (df['md'].shift(1) >= df['sb'].shift(1)) & 
        ((df['mdc'] == 'red') | (df['mdc'] == 'orange')) & 
        (df['color'] == 'red') & 
        (df['ha_color'] == 'red') &
        (((df['md'] - df['sb']) / (df['sb'].abs() + eps)) < -0.03) &
        (atr_condition_sell)
    )

    # -----------------------------
    # Clean Up Temporary Columns
    # -----------------------------
    for c in ('hlc3', 'hi', 'lo', 'mi', 'md', 'sb', 'sh', 'mdc', 'hist_avg', 'momentum_filter',
                'Long_Enter', 'Long_Exit', 'Short_Enter', 'Short_Exit', 'atr', 'spread', 'min_spread'):
        if c in df.columns:
            df.pop(c)

    # Record sell history based on the signals found.
    sell_hist = []
    if df.get('imp_macd_sell_signal', pd.Series()).any():
        signal_times = df[df['imp_macd_sell_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            sell_hist.append(signal_time)

    # Set the current sell signal status
    sell_now = df['imp_macd_sell_signal'].iloc[-1] if 'imp_macd_sell_signal' in df.columns else 0

    if sell_now:
        pos.sell_yn = 'Y'
        pos.hodl_yn = 'N'
        pos.sell_strat_type = 'up'
        pos.sell_strat_name = 'imp_macd'
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
# (Default run code, if this file is run as a standalone script)
#<=====>#

