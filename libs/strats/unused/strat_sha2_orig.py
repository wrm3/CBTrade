#<=====>#
# Description
#
# Enhanced Double Smoothed Heiken Ashi (SHA) Strategy
#
# This module implements an enhanced version of the Double Smoothed Heiken Ashi trading strategy.
# Key improvements include:
# - Dynamic EMA lengths based on market volatility
# - Enhanced body/wick ratio analysis
# - Multi-timeframe confirmation
# - Momentum confirmation to reduce false signals
# - Progressive entry/exit based on candle growth patterns
#
# A buy signal is generated when:
# - Price is above both fast and slow SHA close
# - Candle bodies show strong growth pattern
# - Body/wick ratios indicate strong momentum
# - Higher timeframe confirms the trend
# - RSI confirms momentum
#<=====>#
 
#<=====>#
# Known To Do List
#
# - Validate the enhanced SHA calculations against historical performance
# - Fine-tune the dynamic parameter adjustment thresholds
# - Add more sophisticated exit strategies based on candle patterns
# - Implement position sizing based on signal strength
# - Add correlation-based filters for market conditions
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
lib_name = 'bot_strat_sha2'
log_name = 'bot_strat_sha2'

#<=====>#
# Functions
#<=====>#

# @safe_execute()
@narc(1)
def calculate_dynamic_lengths(df, base_length, volatility_window=20):
    """
    Calculate dynamic EMA lengths based on market volatility.
    Adjusts the base length up or down depending on ATR relative to its moving average.
    """
    # Calculate ATR
    atr = pta.atr(df['high'], df['low'], df['close'], length=volatility_window)
    atr_ma = atr.rolling(window=volatility_window).mean()
    
    # Calculate volatility ratio
    volatility_ratio = atr / atr_ma
    
    # Adjust length based on volatility
    # Higher volatility = shorter length, Lower volatility = longer length
    dynamic_length = base_length * (1 / volatility_ratio)
    
    # Constrain the length between 0.5x and 2x the base length
    dynamic_length = np.clip(dynamic_length, base_length * 0.5, base_length * 2)
    
    return dynamic_length.round().astype(int)

# @safe_execute()
@narc(1)
def analyze_candle_strength(df, prefix='sha'):
    """
    Enhanced analysis of candle strength based on body/wick ratios and growth patterns.
    Returns strength scores for bullish and bearish signals.
    """
    # Calculate body to wick ratios
    df[f'{prefix}_body_to_total_ratio'] = df[f'{prefix}_body'] / (df[f'{prefix}_high'] - df[f'{prefix}_low'])
    
    # Calculate momentum based on body growth
    df[f'{prefix}_body_momentum'] = (df[f'{prefix}_body'] / df[f'{prefix}_body'].shift(1) - 1) * 100
    
    # Calculate wick ratio (upper to lower)
    df[f'{prefix}_wick_ratio'] = df[f'{prefix}_wick_upper'] / df[f'{prefix}_wick_lower']
    
    # Calculate bullish strength score
    df[f'{prefix}_bull_strength'] = (
        (df[f'{prefix}_body_to_total_ratio'] * 0.4) +
        (df[f'{prefix}_body_momentum'] * 0.3) +
        (1 / df[f'{prefix}_wick_ratio'] * 0.3)  # Lower upper wick is bullish
    )
    
    # Calculate bearish strength score
    df[f'{prefix}_bear_strength'] = (
        (df[f'{prefix}_body_to_total_ratio'] * 0.4) +
        (-df[f'{prefix}_body_momentum'] * 0.3) +  # Negative momentum is bearish
        (df[f'{prefix}_wick_ratio'] * 0.3)  # Higher upper wick is bearish
    )
    
    return df

# @safe_execute_silent()
@narc(1)
def settings_sha(st):
    """
    Define and assign the settings for the Enhanced Double Smoothed Heiken Ashi (SHA) buy strategy.
    """
    sst = {
        "use_yn": "Y",
        "freqs": ["1d", "4h", "1h", "30min", "15min"],
        "src": 'close',
        "fast_sha_len1": 8,
        "fast_sha_len2": 8,
        "slow_sha_len1": 13,
        "slow_sha_len2": 13,
        "volatility_window": 20,
        "rsi_length": 14,
        "rsi_threshold": 55,
        "bull_strength_threshold": 0.6,
        "bear_strength_threshold": 0.6,
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
    st['strats']['sha2'] = sst
    return st

# @safe_execute()
@narc(1)
def ta_add_sha(df: pd.DataFrame, prc_mkt, sha_len1=5, sha_len2=8, tag=None) -> pd.DataFrame:
    """
    Enhanced Smoothed Heiken Ashi (SHA) calculation with dynamic parameters.
    """
    # Calculate dynamic lengths based on market volatility
    dynamic_len1 = calculate_dynamic_lengths(df, sha_len1)
    dynamic_len2 = calculate_dynamic_lengths(df, sha_len2)
    
    # Original SHA calculations with dynamic lengths
    df['ema_open'] = df['open'].ewm(span=dynamic_len1, adjust=False).mean()
    df['ema_close'] = df['close'].ewm(span=dynamic_len1, adjust=False).mean()
    df['ema_high'] = df['high'].ewm(span=dynamic_len1, adjust=False).mean()
    df['ema_low'] = df['low'].ewm(span=dynamic_len1, adjust=False).mean()
    
    # Calculate Heikin-Ashi Close
    df['ha_ema_close'] = (df['ema_open'] + df['ema_high'] + df['ema_low'] + df['ema_close']) / 4
    
    # Initialize HA_Open
    df['ha_ema_open'] = np.nan
    df.at[df.index[0], 'ha_ema_open'] = (df.at[df.index[0], 'ema_open'] + df.at[df.index[0], 'ema_close']) / 2
    
    # Calculate HA_Open iteratively
    for i in range(1, len(df)):
        df.at[df.index[i], 'ha_ema_open'] = (df.at[df.index[i-1], 'ha_ema_open'] + df.at[df.index[i-1], 'ha_ema_close']) / 2
    
    # Calculate HA_High and HA_Low
    df['ha_ema_high'] = df[['ema_high', 'ha_ema_open', 'ha_ema_close']].max(axis=1)
    df['ha_ema_low'] = df[['ema_low', 'ha_ema_open', 'ha_ema_close']].min(axis=1)
    
    # Calculate final smoothed HA values with dynamic second smoothing
    df['sha_open'] = df['ha_ema_open'].ewm(span=dynamic_len2, adjust=False).mean()
    df['sha_close'] = df['ha_ema_close'].ewm(span=dynamic_len2, adjust=False).mean()
    df['sha_high'] = df['ha_ema_high'].ewm(span=dynamic_len2, adjust=False).mean()
    df['sha_low'] = df['ha_ema_low'].ewm(span=dynamic_len2, adjust=False).mean()
    
    # Enhanced candle analysis
    df = analyze_candle_strength(df, prefix='sha')
    
    # Add RSI for momentum confirmation
    df['rsi'] = pta.rsi(df['close'], length=14)
    
    # Determine if market price is above or below the SHA close
    df['prc_abv_sha'] = prc_mkt > df['sha_close']
    df['prc_bel_sha'] = prc_mkt < df['sha_close']
    
    if tag:
        # Copy columns with tag
        columns_to_copy = [
            'sha_open', 'sha_close', 'sha_high', 'sha_low',
            'sha_body_to_total_ratio', 'sha_body_momentum', 'sha_wick_ratio',
            'sha_bull_strength', 'sha_bear_strength',
            'prc_abv_sha', 'prc_bel_sha'
        ]
        
        for col in columns_to_copy:
            df[f'{col}{tag}'] = df[col]
            df.pop(col)
    
    # Remove intermediate columns
    columns_to_remove = [
        'ema_open', 'ema_close', 'ema_high', 'ema_low',
        'ha_ema_open', 'ha_ema_close', 'ha_ema_high', 'ha_ema_low'
    ]
    for col in columns_to_remove:
        df.pop(col)
    
    return df

# @safe_execute()
@narc(1)
def buy_strat_sha(buy, ta, st_pair, curr_prc=None):
    """
    Enhanced Double Smoothed Heiken Ashi (SHA) Buy Strategy with multi-timeframe confirmation
    and progressive entry based on signal strength.
    """
    try:
        buy.buy_hist = []
        prod_id = buy.prod_id
        freq = buy.buy_strat_freq
        df = ta[freq].df
        
        # Get settings
        src = st_pair.strats.sha2.src
        fast_sha_len1 = st_pair.strats.sha2.fast_sha_len1
        fast_sha_len2 = st_pair.strats.sha2.fast_sha_len2
        slow_sha_len1 = st_pair.strats.sha2.slow_sha_len1
        slow_sha_len2 = st_pair.strats.sha2.slow_sha_len2
        rsi_threshold = st_pair.strats.sha2.rsi_threshold
        bull_strength_threshold = st_pair.strats.sha2.bull_strength_threshold
        
        # Set current price
        df['curr_prc'] = df[src]
        if curr_prc:
            df['curr_prc'].iloc[-1] = curr_prc
        
        # Calculate SHA indicators for both timeframes
        df = ta_add_sha(df, curr_prc, sha_len1=fast_sha_len1, sha_len2=fast_sha_len2, tag='_fast')
        df = ta_add_sha(df, curr_prc, sha_len1=slow_sha_len1, sha_len2=slow_sha_len2, tag='_slow')
        
        # Generate enhanced buy signal
        df['sha_buy_signal'] = (
            # Price above both fast and slow SHA
            (df['prc_abv_sha_fast']) &
            (df['prc_abv_sha_slow']) &
            
            # Strong bullish momentum in both timeframes
            (df['sha_bull_strength_fast'] > bull_strength_threshold) &
            (df['sha_bull_strength_slow'] > bull_strength_threshold) &
            
            # RSI confirms momentum
            (df['rsi'] > rsi_threshold) &
            
            # Trend alignment between timeframes
            (df['sha_body_momentum_fast'] > 0) &
            (df['sha_body_momentum_slow'] > 0)
        )
        
        # Record buy history
        buy_hist = []
        if df['sha_buy_signal'].any():
            signal_times = df[df['sha_buy_signal'] == 1].index.tolist()
            for signal_time in signal_times:
                buy_hist.append(signal_time)
        
        # Set current buy signal status
        buy_now = df['sha_buy_signal'].iloc[-1]
        
        if buy_now:
            buy.buy_yn = 'Y'
            buy.wait_yn = 'N'
            buy.buy_strat_type = 'up'
            buy.buy_strat_name = 'sha2'
            buy.buy_strat_freq = freq
        else:
            buy.buy_yn = 'N'
            buy.wait_yn = 'Y'
        buy.buy_hist = buy_hist
        
        # Update TA dictionary
        ta[freq].df = df
        
    except Exception as e:
        error_msg = f"""
=== CRITICAL SHA2 BUY STRATEGY EXCEPTION ===
File: {__file__}
Function: {sys._getframe().f_code.co_name}
Strategy: Enhanced Double Smoothed Heiken Ashi Buy Signal Generation
Product ID: {prod_id if 'prod_id' in locals() else 'Unknown'}
Frequency: {freq if 'freq' in locals() else 'Unknown'}
Timestamp: {dttm_get()}
Exception Type: {type(e).__name__}
Exception Message: {str(e)}
Critical Impact: Enhanced SHA buy signal calculation failure - no buy signals generated
Full Traceback:
{traceback.format_exc()}
Stack Trace:
{traceback.format_stack()}
=================================================
"""
        print(error_msg)
        beep(3)  # Audio alert for immediate attention
        if hasattr(buy, 'buy_yn'):
            buy.buy_yn = 'N'
            buy.wait_yn = 'Y'
    
    return buy, ta

# @safe_execute()
@narc(1)
def sell_strat_sha(mkt, pos, ta, st_pair, curr_prc=None):
    """
    Enhanced Double Smoothed Heiken Ashi (SHA) Sell Strategy with progressive exit
    based on signal strength and multi-timeframe confirmation.
    """
    try:
        pos.sell_hist = []
        prod_id = pos.prod_id
        freq = pos.buy_strat_freq
        df = ta[freq].df
        
        # Get settings
        src = st_pair.strats.sha2.src
        fast_sha_len1 = st_pair.strats.sha2.fast_sha_len1
        fast_sha_len2 = st_pair.strats.sha2.fast_sha_len2
        slow_sha_len1 = st_pair.strats.sha2.slow_sha_len1
        slow_sha_len2 = st_pair.strats.sha2.slow_sha_len2
        bear_strength_threshold = st_pair.strats.sha2.bear_strength_threshold
        
        # Set current price
        df['curr_prc'] = df[src]
        if curr_prc:
            df['curr_prc'].iloc[-1] = curr_prc
        
        # Calculate SHA indicators for both timeframes
        df = ta_add_sha(df, curr_prc, sha_len1=fast_sha_len1, sha_len2=fast_sha_len2, tag='_fast')
        df = ta_add_sha(df, curr_prc, sha_len1=slow_sha_len1, sha_len2=slow_sha_len2, tag='_slow')
        
        # Generate enhanced sell signal
        df['sha_sell_signal'] = (
            # Price below both fast and slow SHA
            (df['prc_bel_sha_fast']) &
            (df['prc_bel_sha_slow']) &
            
            # Strong bearish momentum in both timeframes
            (df['sha_bear_strength_fast'] > bear_strength_threshold) &
            (df['sha_bear_strength_slow'] > bear_strength_threshold) &
            
            # Trend alignment between timeframes
            (df['sha_body_momentum_fast'] < 0) &
            (df['sha_body_momentum_slow'] < 0)
        )
        
        # Record sell history
        sell_hist = []
        if df['sha_sell_signal'].any():
            signal_times = df[df['sha_sell_signal'] == 1].index.tolist()
            for signal_time in signal_times:
                sell_hist.append(signal_time)
        
        # Set current sell signal status
        sell_now = df['sha_sell_signal'].iloc[-1]
        
        if sell_now:
            pos.sell_yn = 'Y'
            pos.hodl_yn = 'N'
            pos.sell_strat_type = 'up'
            pos.sell_strat_name = 'sha2'
            pos.sell_strat_freq = freq
            pos = exit_if_logic(pos=pos, st_pair=st_pair)
        else:
            pos.sell_yn = 'N'
            pos.hodl_yn = 'Y'
        pos.sell_hist = sell_hist
        
        # Update TA dictionary
        ta[freq].df = df
        
    except Exception as e:
        error_msg = f"""
=== CRITICAL SHA2 SELL STRATEGY EXCEPTION ===
File: {__file__}
Function: {sys._getframe().f_code.co_name}
Strategy: Enhanced Double Smoothed Heiken Ashi Sell Signal Generation
Product ID: {pos.prod_id if hasattr(pos, 'prod_id') else 'Unknown'}
Frequency: {pos.buy_strat_freq if hasattr(pos, 'buy_strat_freq') else 'Unknown'}
Timestamp: {dttm_get()}
Exception Type: {type(e).__name__}
Exception Message: {str(e)}
Critical Impact: Enhanced SHA sell signal calculation failure - positions may not close properly
Full Traceback:
{traceback.format_exc()}
Stack Trace:
{traceback.format_stack()}
=================================================
"""
        print(error_msg)
        beep(3)  # Audio alert for immediate attention
        if hasattr(pos, 'sell_yn'):
            pos.sell_yn = 'N'
            pos.hodl_yn = 'Y'
    
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
