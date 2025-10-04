#<=====>#
# Description
# 
# Volume-Weighted MACD Strategy
# Combines MACD crossovers with volume confirmation and volatility-adjusted stops
# Uses volume spikes to validate trend direction changes
#<=====>#

#<=====>#
# Known To Do List
#
# - Optimize volume threshold ratios per market
# - Add higher timeframe confirmation
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
lib_name = 'bot_strat_vwmacd'
log_name = 'bot_strat_vwmacd'

#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_vwmacd(st):
    """Define VWMACD strategy settings"""
    sst = {
        "use_yn": "Y",
        "freqs": ["15min", "30min", "1h", "4h", "1d"],
        "macd_fast": 12,
        "macd_slow": 26,
        "volume_ma_window": 20,
        "volume_threshold": 1.2,
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
    st['strats']['vwmacd'] = sst
    return st

# @safe_execute()
@narc(1)
def ta_add_vwmacd(df: pd.DataFrame, params) -> pd.DataFrame:
    """Add VWMACD indicators to DataFrame"""

    # Calculate MACD with dynamic column names
    macd_fast = params['macd_fast']
    macd_slow = params['macd_slow']
    macd = pta.macd(df['close'], fast=macd_fast, slow=macd_slow)
    
    # Generate dynamic column names
    macd_col = f"MACD_{macd_fast}_{macd_slow}_9"
    macds_col = f"MACDs_{macd_fast}_{macd_slow}_9"
    macdh_col = f"MACDh_{macd_fast}_{macd_slow}_9"
    
    df[macd_col] = macd[macd_col]
    df[macds_col] = macd[macds_col]
    df[macdh_col] = macd[macdh_col]
    
    df['volume_ma'] = df['volume'].rolling(window=params['volume_ma_window']).mean()
    df['atr'] = pta.atr(df['high'], df['low'], df['close'], length=14)
    return df

# @safe_execute()
@narc(1)
def buy_strat_vwmacd(buy, ta, st_pair, curr_prc=None):
    """VWMACD Buy Strategy"""

    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df
    strat_params = st_pair.strats.vwmacd
    
    # Calculate indicators
    df = ta_add_vwmacd(df, {
        'macd_fast': strat_params.macd_fast,
        'macd_slow': strat_params.macd_slow,
        'volume_ma_window': strat_params.volume_ma_window
    })
    
    # Get dynamic column names
    macd_fast = strat_params.macd_fast
    macd_slow = strat_params.macd_slow
    macd_col = f"MACD_{macd_fast}_{macd_slow}_9"
    macds_col = f"MACDs_{macd_fast}_{macd_slow}_9"
    macdh_col = f"MACDh_{macd_fast}_{macd_slow}_9"

    # Generate buy signal with dynamic columns
    df['vwmacd_buy_signal'] = (
        (df[macd_col] > df[macds_col]) &
        (df['volume'] > df['volume_ma'] * strat_params.volume_threshold) &
        (df[macdh_col] > 0) &
        (df['color'] == 'green')
    )
    
    # Record history and set flags
    buy_hist = df[df['vwmacd_buy_signal']].index.tolist()
    buy_now = df['vwmacd_buy_signal'].iloc[-1]
    
    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_name = 'vwmacd'
    else:
        buy.buy_yn = 'N'
        buy.wait_yn = 'Y'
    buy.buy_hist = buy_hist
    
    ta[freq].df = df
    return buy, ta

# @safe_execute()
@narc(1)
def sell_strat_vwmacd(mkt, pos, ta, st_pair, curr_prc=None):
    """VWMACD Sell Strategy"""

    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df
    strat_params = st_pair.strats.vwmacd
    
    # Calculate indicators
    df = ta_add_vwmacd(df, {
        'macd_fast': strat_params.macd_fast,
        'macd_slow': strat_params.macd_slow,
        'volume_ma_window': strat_params.volume_ma_window
    })
    
    # Generate sell signal
    df['vwmacd_sell_signal'] = (
        (df['MACD_12_26_9'] < df['MACDs_12_26_9']) &
        (df['volume'] > df['volume_ma'] * 0.8) &
        (df['color'] == 'red')
    )
    
    # Record history and set flags
    sell_hist = df[df['vwmacd_sell_signal']].index.tolist()
    sell_now = df['vwmacd_sell_signal'].iloc[-1]
    
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