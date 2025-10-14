#<=====># 
# Description
# 
# RSI Divergence MACD Strategy
# Combines hidden bullish/bearish RSI divergences with MACD crossovers
# Includes volume confirmation and volatility-adjusted position sizing
#<=====>#

#<=====>#
# Known To Do List
#
# - Optimize divergence detection window sizes
# - Add multi-timeframe confirmation
# - Validate volume spike thresholds
#<=====>#
 
#<=====>#
# Imports
#<=====>#
import sys
import numpy as np
import pandas as pd
import pandas_ta as pta
import traceback
from scipy.signal import argrelextrema
from libs.common import beep, dttm_get, narc
from libs.common import print_adv
from libs.strats._strat_common import disp_sell_tests, exit_if_logic

#<=====>#
# Variables
#<=====>#
lib_name = 'bot_strat_rsi_div_macd'
log_name = 'bot_strat_rsi_div_macd'

#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_rsi_div_macd(st):
    """Define RSI Divergence MACD strategy settings"""
    sst = {
        "use_yn": "Y",
        "freqs": ["1h", "4h", "1d"],
        "rsi_period": 14,
        "macd_fast": 12,
        "macd_slow": 26,
        "divergence_window": 5,
        "volume_multiplier": 1.5,
        "max_volatility_pct": 5.0,
         "buy": {
            "prod_ids": [],
            "skip_prod_ids": [],
            "tests_min": {"***":15, "15min":13, "30min":11, "1h":9, "4h":7, "1d":5},
            "boost_tests_min": {"15min":21, "30min":13, "1h":8, "4h":5, "1d":3},
            "max_open_poss_cnt_live": {"***": 2, "BTC-USDC": 5},
            "max_open_poss_cnt_test": {"***": 3, "BTC-USDC": 9, "ETH-USDC": 9, "SOL-USDC": 9},
            "show_tests_yn": "Y"
            },
		"sell":{
            "exit_if_profit_yn": "N",
            "exit_if_profit_pct_min": 1,
            "exit_if_loss_yn": "N",
            "exit_if_loss_pct_max": 4,
            "show_tests_yn": "N"
            }
        }
    st['strats']['rsi_div_macd'] = sst
    return st

# @safe_execute()
@narc(1)
def detect_divergence(df, price_col='close', indicator_col='RSI', window=5):
    """Detect bullish/bearish divergences between price and indicator"""

    # Find local maxima/minima
    highs = argrelextrema(df[price_col].values, np.greater, order=window)[0]
    lows = argrelextrema(df[price_col].values, np.less, order=window)[0]
    
    # Initialize divergence columns
    df['bullish_div'] = False
    df['bearish_div'] = False
    
    # Bullish divergence (price lower lows, indicator higher lows)
    for i in range(1, len(lows)):
        curr_low = lows[i]
        prev_low = lows[i-1]
        
        if (df[price_col].iloc[curr_low] < df[price_col].iloc[prev_low] and
            df[indicator_col].iloc[curr_low] > df[indicator_col].iloc[prev_low]):
            df.loc[df.index[curr_low], 'bullish_div'] = True
            
    # Bearish divergence (price higher highs, indicator lower highs)
    for i in range(1, len(highs)):
        curr_high = highs[i]
        prev_high = highs[i-1]
        
        if (df[price_col].iloc[curr_high] > df[price_col].iloc[prev_high] and
            df[indicator_col].iloc[curr_high] < df[indicator_col].iloc[prev_high]):
            df.loc[df.index[curr_high], 'bearish_div'] = True
                
    return df

# @safe_execute()
@narc(1)
def ta_add_rsi_div_macd(df: pd.DataFrame, params) -> pd.DataFrame:
    """Add RSI and MACD indicators to DataFrame"""

    # Calculate RSI
    df['RSI'] = pta.rsi(df['close'], length=params['rsi_period'])
    
    # Calculate MACD with explicit column naming
    macd = pta.macd(df['close'], 
                    fast=params['macd_fast'],
                    slow=params['macd_slow'],
                    signal=9)
    # Directly assign column names to avoid index issues
    macd.columns = ['MACD', 'MACD_signal', 'MACD_hist']
    df = pd.concat([df, macd], axis=1)
    
    # Volume analysis
    df['vol_ma'] = df['volume'].rolling(window=14).mean()
    
    # Detect divergences
    df = detect_divergence(df, window=params['divergence_window'])
        
    return df

# @safe_execute()
@narc(1)
def buy_strat_rsi_div_macd(buy, ta, st_pair, curr_prc=None):
    """RSI Divergence MACD Buy Strategy"""

    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df.copy()  # Use copy to avoid index manipulation
    strat_params = st_pair.strats.rsi_div_macd
    
    # Calculate indicators
    df = ta_add_rsi_div_macd(df, {
        'rsi_period': strat_params.rsi_period,
        'macd_fast': strat_params.macd_fast,
        'macd_slow': strat_params.macd_slow,
        'divergence_window': strat_params.divergence_window
    })
    
    # Generate buy signal with NaN handling
    df['rsi_div_macd_buy_signal'] = (
        (df['bullish_div'].fillna(False).infer_objects(copy=False)) &
        (df['MACD'] > df['MACD_signal']) &
        (df['volume'] > df['vol_ma'] * strat_params.volume_multiplier) &
        (df['color'] == 'green')
    )
    
    # Record history and set flags
    buy_hist = df[df['rsi_div_macd_buy_signal']].index.tolist()
    buy_now = df['rsi_div_macd_buy_signal'].iloc[-1]
    
    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_name = 'rsi_div_macd'
    else:
        buy.buy_yn = 'N'
        buy.wait_yn = 'Y'
    buy.buy_hist = buy_hist
    
    ta[freq].df = df
    return buy, ta

# @safe_execute()
@narc(1)
def sell_strat_rsi_div_macd(mkt, pos, ta, st_pair, curr_prc=None):
    """RSI Divergence MACD Sell Strategy"""

    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df.copy()  # Use copy to avoid index manipulation
    strat_params = st_pair.strats.rsi_div_macd
    
    # Recalculate indicators for sell strategy
    df = ta_add_rsi_div_macd(df, {
        'rsi_period': strat_params.rsi_period,
        'macd_fast': strat_params.macd_fast,
        'macd_slow': strat_params.macd_slow,
        'divergence_window': strat_params.divergence_window
    })
    
    # Generate sell signal with NaN handling
    df['rsi_div_macd_sell_signal'] = (
        (df['bearish_div'].fillna(False).infer_objects(copy=False)) &
        (df['MACD'] < df['MACD_signal']) &
        (df['volume'] > df['vol_ma'] * 0.8) &
        (df['color'] == 'red')
    )
    
    # Record history and set flags
    sell_hist = df[df['rsi_div_macd_sell_signal']].index.tolist()
    sell_now = df['rsi_div_macd_sell_signal'].iloc[-1]
    
    if sell_now:
        pos.sell_yn = 'Y'
        pos.hodl_yn = 'N'
        pos = exit_if_logic(pos, st_pair)
    else:
        pos.sell_yn = 'N'
        pos.hodl_yn = 'Y'
    pos.sell_hist = sell_hist
    
    ta[freq].df = df
    return mkt, pos, ta

#<=====>#
# Helper Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def error_handler(e, obj, lib_name):
    """Standard error handling"""
    traceback.print_exc()
    print(f"Error in {lib_name}: {str(e)}")
    print_adv(3)
    beep()
    if hasattr(obj, 'buy_yn'):
        obj.buy_yn = 'N'
        obj.wait_yn = 'Y'
    if hasattr(obj, 'sell_yn'):
        obj.sell_yn = 'N'
        obj.hodl_yn = 'Y'

#<=====>#
# Post Variables
#<=====>#
# (Any post-run variables can be defined here)

#<=====>#
# Default Run
#<=====>#
# (Default run code if this module is executed as a standalone script)
#<=====>#
