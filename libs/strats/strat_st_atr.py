#<=====>#
# Description
#
# Supertrend ATR Strategy
# Combines Supertrend indicator with ATR-based volatility bands
# Buy when price crosses above Supertrend line and volatility is expanding
# Sell when price crosses below Supertrend line with confirmation from ATR bands
#<=====>#

#<=====>#
# Known To Do List
# - Optimize ATR period and multiplier values
# - Add volatility contraction/expansion detection
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
lib_name = 'bot_strat_st_atr'
log_name = 'bot_strat_st_atr'

#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_st_atr(st):
    sst = {
        "use_yn": "Y",
        "freqs": ["1d", "4h", "1h", "30min", "15min"],
        "atr_period": 14,
        "supertrend_mult": 3.0,
        "volatility_threshold": 0.02,
        "buy": {
            "prod_ids": [],
            "skip_prod_ids": [],
            "tests_min": {"***":15, "15min":13, "30min":11, "1h":9, "4h":7, "1d":5},
            "boost_tests_min": {"15min":21, "30min":13, "1h":8, "4h":5, "1d":3},
            "max_open_poss_cnt_live": {"***": 2, "BTC-USDC": 5},
            "max_open_poss_cnt_test": {"***":3,"BTC-USDC":9,"ETH-USDC":9,"SOL-USDC":9},
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
    st['strats']['st_atr'] = sst
    return st

# @safe_execute()
@narc(1)
def ta_add_st_atr(df: pd.DataFrame, mult=3.0, period=14):
    """🔴 PREVENT DUPLICATE COLUMNS"""
    # Check if SuperTrend indicators already exist to prevent duplicates
    supertrend_col = f'SUPERT_{period}_{mult}'
    
    if supertrend_col not in df.columns:
        supertrend = pta.supertrend(df['high'], df['low'], df['close'], 
                                   length=period, multiplier=mult)
        df = pd.concat([df, supertrend], axis=1)
    
    if 'atr' not in df.columns:
        df['atr'] = pta.atr(df['high'], df['low'], df['close'], length=period)
    
    if 'volatility_ratio' not in df.columns:
        df['volatility_ratio'] = df['atr'] / df['close'].rolling(50).mean()
    
    return df

# @safe_execute()
@narc(1)
def buy_strat_st_atr(buy, ta, st_pair, curr_prc=None):
    """🔴 FIXED: Handle duplicate columns by ensuring Series access"""

    freq = buy.buy_strat_freq
    df = ta[freq].df
    df = ta_add_st_atr(df, 
                                st_pair.strats.st_atr.supertrend_mult,
                                st_pair.strats.st_atr.atr_period)
    
    # Ensure we get Series, not DataFrame (in case of duplicate columns)
    close_series = df['close']
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]  # Take first column if duplicate
        
    supertrend_series = df['SUPERT_14_3.0']
    if isinstance(supertrend_series, pd.DataFrame):
        supertrend_series = supertrend_series.iloc[:, 0]  # Take first column if duplicate
        
    supertrend_dir_series = df['SUPERTd_14_3.0']
    if isinstance(supertrend_dir_series, pd.DataFrame):
        supertrend_dir_series = supertrend_dir_series.iloc[:, 0]  # Take first column if duplicate
        
    volatility_series = df['volatility_ratio']
    if isinstance(volatility_series, pd.DataFrame):
        volatility_series = volatility_series.iloc[:, 0]  # Take first column if duplicate
    
    # Buy conditions using Series (not DataFrame columns to avoid alignment issues)
    df['st_buy_signal'] = (
        (close_series > supertrend_series) &
        (supertrend_dir_series == 1) &
        (volatility_series > st_pair.strats.st_atr.volatility_threshold) &
        (df['color'] == 'green')
    )
    
    buy = _set_buy_signals(df, buy, 'st_buy_signal', 'st_atr')
    ta[freq].df = df
        
    return buy, ta

# @safe_execute()
@narc(1)
def sell_strat_st_atr(mkt, pos, ta, st_pair, curr_prc=None):
    """🔴 FIXED: Handle duplicate columns by ensuring Series access"""

    freq = pos.buy_strat_freq
    df = ta[freq].df
    df = ta_add_st_atr(df, 
                                st_pair.strats.st_atr.supertrend_mult,
                                st_pair.strats.st_atr.atr_period)
    
    # Ensure we get Series, not DataFrame (in case of duplicate columns)
    close_series = df['close']
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]  # Take first column if duplicate
        
    supertrend_series = df['SUPERT_14_3.0']
    if isinstance(supertrend_series, pd.DataFrame):
        supertrend_series = supertrend_series.iloc[:, 0]  # Take first column if duplicate
        
    supertrend_dir_series = df['SUPERTd_14_3.0']
    if isinstance(supertrend_dir_series, pd.DataFrame):
        supertrend_dir_series = supertrend_dir_series.iloc[:, 0]  # Take first column if duplicate
    
    # Sell conditions using Series (not DataFrame columns to avoid alignment issues)
    df['st_sell_signal'] = (
        (close_series < supertrend_series) &
        (supertrend_dir_series == -1) &
        (df['color'] == 'red')
    )
    
    pos = _set_sell_signals(df, pos, 'st_sell_signal', 'st_atr')
    ta[freq].df = df
        
    return mkt, pos, ta

#<=====>#
# Helper Functions - Reverted to Simple Original Approach
#<=====>#
# @safe_execute_silent()
@narc(1)
def _set_buy_signals(df, obj, signal_col, strat_name):
    obj.buy_hist = df[df[signal_col]].index.tolist()
    obj.buy_yn = 'Y' if df[signal_col].iloc[-1] else 'N'
    obj.wait_yn = 'N' if obj.buy_yn == 'Y' else 'Y'
    obj.buy_strat_name = strat_name
    return obj

# @safe_execute_silent()
@narc(1)
def _set_sell_signals(df, obj, signal_col, strat_name):
    obj.sell_hist = df[df[signal_col]].index.tolist()
    obj.sell_yn = 'Y' if df[signal_col].iloc[-1] else 'N'
    obj.hodl_yn = 'N' if obj.sell_yn == 'Y' else 'Y' 
    obj.sell_strat_name = strat_name
    return obj

# @safe_execute_silent()
@narc(1)
def error_handler(e, obj, lib_name):
    traceback.print_exc()
    print(f"Error in {lib_name}: {e}")
    print_adv(3)
    beep()
    obj.buy_yn = 'N' if hasattr(obj, 'buy_yn') else 'N'
    obj.wait_yn = 'Y' if hasattr(obj, 'wait_yn') else 'Y' 