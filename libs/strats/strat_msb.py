#<=====>#
# Description
#
# Market Structure Break Strategy
# Identifies key market structure levels with volume validation
# Combines order block theory with liquidity grabs
#<=====>#

#<=====>#
# Known To Do List
#
# - Optimize liquidity zone detection parameters
# - Add order block confirmation from higher timeframes
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
lib_name = 'bot_strat_msb'
log_name = 'bot_strat_msb'

#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()

@narc(1)
def settings_msb(st):
    """Define Market Structure Break settings"""
    sst = {
        "use_yn": "Y",
        "freqs": ["1h", "4h", "1d"],
        "liquidity_window": 20,
        "volatility_threshold": 0.03,
        "volume_confirmation": 1.5,
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
    st['strats']['msb'] = sst
    return st

# @safe_execute()

@narc(1)
def ta_add_msb(df: pd.DataFrame, params) -> pd.DataFrame:
    """Add MSB indicators to DataFrame"""

    # Liquidity zones using volume profile
    df['vol_profile'] = df['volume'].rolling(params['liquidity_window']).mean()
    df['liq_high'] = df['high'].rolling(params['liquidity_window']).max()
    df['liq_low'] = df['low'].rolling(params['liquidity_window']).min()
    df['atr'] = pta.atr(df['high'], df['low'], df['close'], length=14)
    return df

# @safe_execute()

@narc(1)
def buy_strat_msb(buy, ta, st_pair, curr_prc=None):
    """Market Structure Break Buy Strategy"""

    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df
    strat_params = st_pair.strats.msb
    
    # Calculate indicators
    df = ta_add_msb(df, {
        'liquidity_window': strat_params.liquidity_window,
        'volatility_threshold': strat_params.volatility_threshold,
        'volume_confirmation': strat_params.volume_confirmation
    })
    
    # Generate buy signal
    df['msb_buy_signal'] = (
        (df['close'] > df['liq_high']) &
        (df['volume'] > df['vol_profile'] * strat_params.volume_confirmation) &
        (df['atr'] > df['close'] * strat_params.volatility_threshold) &
        (df['color'] == 'green')
    )
    
    # Record history and set flags
    buy_hist = df[df['msb_buy_signal']].index.tolist()
    buy_now = df['msb_buy_signal'].iloc[-1]
    
    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_name = 'msb'
    else:
        buy.buy_yn = 'N'
        buy.wait_yn = 'Y'
    buy.buy_hist = buy_hist
    
    ta[freq].df = df
    return buy, ta

# @safe_execute()

@narc(1)
def sell_strat_msb(mkt, pos, ta, st_pair, curr_prc=None):
    """Market Structure Break Sell Strategy"""

    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df
    strat_params = st_pair.strats.msb
    
    # Calculate indicators
    df = ta_add_msb(df, {
        'liquidity_window': strat_params.liquidity_window,
        'volatility_threshold': strat_params.volatility_threshold,
        'volume_confirmation': strat_params.volume_confirmation
    })
    
    # Generate sell signal 
    df['msb_sell_signal'] = (
        (df['close'] < df['liq_low']) &
        (df['volume'] > df['vol_profile'] * 0.8) &
        (df['atr'] > df['close'] * strat_params.volatility_threshold) &
        (df['color'] == 'red')
    )
    
    # Record history and set flags
    sell_hist = df[df['msb_sell_signal']].index.tolist()
    sell_now = df['msb_sell_signal'].iloc[-1]
    
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