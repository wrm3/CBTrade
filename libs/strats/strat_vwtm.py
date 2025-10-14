#<=====>#
# Description
#
# Volume-Weighted Trend Momentum Strategy
# Combines Elder Ray Index, Vortex Indicator, and Volume-Weighted Momentum
# Specifically designed for Bitcoin's volatility and volume patterns
#<=====>#
 
#<=====>#
# Known To Do List
#
# - Optimize EMA periods for different market conditions
# - Add volatility-based position sizing
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
lib_name = 'bot_strat_vwtm'
log_name = 'bot_strat_vwtm'

#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_vwtm(st):
    """Define VWTM strategy settings"""
    sst = {
        "use_yn": "Y",
        "freqs": ["1h", "4h", "1d"],
        "ema_period": 20,
        "vortex_period": 14,
        "volume_ma_window": 50,
        "bull_power_threshold": 0.5,
        "volume_multiplier": 1.8,
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
    st['strats']['vwtm'] = sst
    return st

# @safe_execute()
@narc(1)
def ta_add_vwtm(df: pd.DataFrame, params) -> pd.DataFrame:
    """Add VWTM indicators to DataFrame"""

    # Elder Ray Index
    ema = pta.ema(df['close'], length=params['ema_period'])
    df['bull_power'] = df['high'] - ema
    df['bear_power'] = df['low'] - ema
    
    # Vortex Indicator with correct column names
    vortex_period = params['vortex_period']
    vortex = pta.vortex(
        df['high'], df['low'], df['close'], 
        length=vortex_period
    )
    # Correct column names for pandas_ta vortex
    df['vtxp'] = vortex[f'VTXP_{vortex_period}']  # Positive Trend
    df['vtxm'] = vortex[f'VTXM_{vortex_period}']  # Negative Trend
    
    # Volume Weighted Momentum
    df['vwma'] = (df['volume'] * df['close']).rolling(
        params['volume_ma_window']).mean() / df['volume'].rolling(
        params['volume_ma_window']).mean()
    
    # Volume Spike Detection
    df['vol_ma'] = df['volume'].rolling(params['volume_ma_window']).mean()
   
    return df

# @safe_execute()
@narc(1)
def buy_strat_vwtm(buy, ta, st_pair, curr_prc=None):
    """VWTM Buy Strategy"""

    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df
    strat_params = st_pair.strats.vwtm
    
    # Calculate indicators
    df = ta_add_vwtm(df, {
        'ema_period': strat_params.ema_period,
        'vortex_period': strat_params.vortex_period,
        'volume_ma_window': strat_params.volume_ma_window
    })
    
    # Generate buy signal with correct references
    df['vwtm_buy_signal'] = (
        (df['bull_power'] > strat_params.bull_power_threshold) &
        (df['vtxp'] > df['vtxm']) &  # Use correct column names
        (df['volume'] > df['vol_ma'] * strat_params.volume_multiplier) &
        (df['vwma'] > df['vwma'].shift(1)) &
        (df['color'] == 'green')
    )
    
    # Record history and set flags
    buy_hist = df[df['vwtm_buy_signal']].index.tolist()
    buy_now = df['vwtm_buy_signal'].iloc[-1]
    
    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_name = 'vwtm'
    else:
        buy.buy_yn = 'N'
        buy.wait_yn = 'Y'
    buy.buy_hist = buy_hist
    
    ta[freq].df = df
    return buy, ta

# @safe_execute()
@narc(1)
def sell_strat_vwtm(mkt, pos, ta, st_pair, curr_prc=None):
    """VWTM Sell Strategy"""

    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df
    strat_params = st_pair.strats.vwtm
    
    # Calculate indicators
    df = ta_add_vwtm(df, {
        'ema_period': strat_params.ema_period,
        'vortex_period': strat_params.vortex_period,
        'volume_ma_window': strat_params.volume_ma_window
    })
    
    # Generate sell signal
    df['vwtm_sell_signal'] = (
        (df['bear_power'] < -strat_params.bull_power_threshold) &
        (df['vtxm'] > df['vtxp']) &
        (df['volume'] > df['vol_ma'] * 1.5) &
        (df['vwma'] < df['vwma'].shift(1)) &
        (df['color'] == 'red')
    )
    
    # Record history and set flags
    sell_hist = df[df['vwtm_sell_signal']].index.tolist()
    sell_now = df['vwtm_sell_signal'].iloc[-1]
    
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