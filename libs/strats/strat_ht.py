#<=====>#
# Description
#
# Hull Moving Average Trend Strategy
# Uses HMA for trend direction with ATR volatility bands
# Incorporates fractal breakout entries and momentum confirmation
#<=====>#

#<=====>#
# Known To Do List
#
# - Optimize fractal detection window
# - Add multi-timeframe confirmation
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
lib_name = 'bot_strat_ht'
log_name = 'bot_strat_ht'

#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_ht(st):
    """Define Hull Trend strategy settings"""
    sst = {
        "use_yn": "Y",
        "freqs": ["1h", "4h", "1d"],
        "hull_period": 20,
        "atr_multiplier": 1.5,
        "momentum_window": 14,
        "fractal_length": 3,
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
    st['strats']['ht'] = sst
    return st

# @safe_execute()
@narc(1)
def ta_add_ht(df: pd.DataFrame, params) -> pd.DataFrame:
    """Add Hull Trend indicators to DataFrame"""

    df['HMA'] = pta.hma(df['close'], length=params['hull_period'])
    df['ATR'] = pta.atr(df['high'], df['low'], df['close'], length=14)
    df['upper_band'] = df['HMA'] + (df['ATR'] * params['atr_multiplier'])
    df['lower_band'] = df['HMA'] - (df['ATR'] * params['atr_multiplier'])
    df['momentum'] = pta.roc(df['HMA'], length=params['momentum_window'])
    return df

# @safe_execute()
@narc(1)
def buy_strat_ht(buy, ta, st_pair, curr_prc=None):
    """Hull Trend Buy Strategy"""

    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df
    strat_params = st_pair.strats.ht
    
    # Calculate indicators
    df = ta_add_ht(df, {
        'hull_period': strat_params.hull_period,
        'atr_multiplier': strat_params.atr_multiplier,
        'momentum_window': strat_params.momentum_window,
        'fractal_length': strat_params.fractal_length
    })
    
    # Fractal breakout detection
    df['fractal_high'] = df['high'].rolling(strat_params.fractal_length, center=True).max()
    df['fractal_low'] = df['low'].rolling(strat_params.fractal_length, center=True).min()
    
    # Generate buy signal
    df['hull_buy_signal'] = (
        (df['close'] > df['upper_band']) &
        (df['momentum'] > 0) &
        (df['close'] > df['fractal_high'].shift(1)) &
        (df['color'] == 'green')
    )
    
    # Record history and set flags
    buy_hist = df[df['hull_buy_signal']].index.tolist()
    buy_now = df['hull_buy_signal'].iloc[-1]
    
    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_name = 'ht'
    else:
        buy.buy_yn = 'N'
        buy.wait_yn = 'Y'
    buy.buy_hist = buy_hist
    
    ta[freq].df = df
    return buy, ta

# @safe_execute()
@narc(1)
def sell_strat_ht(mkt, pos, ta, st_pair, curr_prc=None):
    """Hull Trend Sell Strategy"""

    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df
    strat_params = st_pair.strats.ht
    
    # Calculate indicators
    df = ta_add_ht(df, {
        'hull_period': strat_params.hull_period,
        'atr_multiplier': strat_params.atr_multiplier,
        'momentum_window': strat_params.momentum_window,
        'fractal_length': strat_params.fractal_length
    })
    
    # Generate sell signal
    df['hull_sell_signal'] = (
        (df['close'] < df['lower_band']) &
        (df['momentum'] < 0) &
        (df['close'] < df['fractal_low'].shift(1)) &
        (df['color'] == 'red')
    )
    
    # Record history and set flags
    sell_hist = df[df['hull_sell_signal']].index.tolist()
    sell_now = df['hull_sell_signal'].iloc[-1]
    
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