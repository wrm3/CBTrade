#<=====>#
# Description
#
# This module implements the Nadaraya-Watson Envelope (NWE ENV) trading strategy.
# It uses a smoothed NWE line (obtained via a Gaussian filter) and an envelope 
# derived from the mean absolute error (MAE) to generate buy and sell signals.
#
# A buy signal is generated when the price breaches below the lower envelope
# and then recovers, provided that the overall trend (as indicated by a general 
# color indicator) is green. Conversely, a sell signal is generated when the price
# breaches above the upper envelope and then recovers, with the overall trend red.
#<=====>#


#<=====>#
# Known To Do List
#
# - Validate the envelope breach and recovery conditions with additional testing.
# - Fine-tune the multiplier and bandwidth parameters for different markets.
# - Integrate additional risk management (e.g., stop-loss or trailing stops) if needed.
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
lib_name = 'bot_strat_nwe_env'
log_name = 'bot_strat_nwe_env'


#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_nwe_env(st):
    """
    Define and assign the settings for the NWE ENV buy strategy.
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
    st['strats']['nwe_env'] = sst
    return st

#<=====>#

# @safe_execute()
@narc(1)
def ta_add_nwe_env(df: pd.DataFrame, src='close', mult=3.0) -> pd.DataFrame:
    """
    Add the NWE Envelope indicator and related signals to the DataFrame.
    
    This function calculates the mean absolute error (MAE) between the source price
    and the previously computed NWE line, and uses this to define upper and lower bands.
    It then detects breaches of the envelope and determines the corresponding buy and sell signals.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame with an existing 'nwe_line' column.
        src (str): The source column name for price data (default: 'close').
        mult (float): Multiplier for calculating the envelope width (default: 3.0).
    
    Returns:
        pd.DataFrame: The DataFrame with added columns:
                      'nwe_mae', 'nwe_upper', 'nwe_lower',
                      'nwe_env_buy_breach', 'nwe_env_buy_breach_depth',
                      'nwe_env_buy_signal', 'nwe_env_sell_breach',
                      'nwe_env_sell_breach_height', 'nwe_env_sell_signal'.
    """

    source = df[src].values
    nwe = df['nwe_line']
    
    # Compute the MAE between the price and the NWE line, then derive the envelope bands.
    mae = np.mean(np.abs(source - nwe)) * mult
    df['nwe_mae'] = mae
    df['nwe_upper'] = df['nwe_line'] + mae
    df['nwe_lower'] = df['nwe_line'] - mae

    # Detect a buy breach: when the low is below the lower envelope.
    df['nwe_env_buy_breach'] = (
        (df['low'] < df['nwe_lower']) |
        (df['low'].shift(1) < df['nwe_lower'].shift(1))
    )
    # Calculate a per-row breach depth safely (avoid heavy apply + reindexing)
    # Use the current low as the depth when a breach is present, else NaN
    df[src] = pd.to_numeric(df[src], errors='coerce')
    df['nwe_env_buy_breach_depth'] = np.where(df['nwe_env_buy_breach'], df['low'].values, np.nan)
    # Generate buy signal: breach occurred and price recovers above the breach depth,
    # with the overall trend (color) green.
    df['nwe_env_buy_signal'] = (
        (df['nwe_env_buy_breach']) &
        (df['color'] == 'green') &
        (df[src] > df['nwe_env_buy_breach_depth'].fillna(df[src]).infer_objects(copy=False))
    )
    
    # Detect a sell breach: when the price is above the upper envelope.
    df['nwe_env_sell_breach'] = (
        (df[src] > df['nwe_upper']) |
        (df[src].shift(1) > df['nwe_upper'].shift(1))
    )
    # Calculate the breach height (highest price during a breach).
    df['nwe_env_sell_breach_height'] = df.apply(
        lambda row: df[src][df[src] > df['nwe_upper']].max() if row['nwe_env_sell_breach'] else None,
        axis=1
    )
    # Generate sell signal: breach occurred and price recovers below the breach height,
    # with the overall trend (color) red.
    df['nwe_env_sell_signal'] = (
        (df['nwe_env_sell_breach']) &
        (df['color'] == 'red') &
        (df[src] < df['nwe_env_sell_breach_height'].fillna(df[src]).infer_objects(copy=False))
    )

    return df

#<=====>#

# @safe_execute()
@narc(1)
def buy_strat_nwe_env(buy, ta, st_pair, curr_prc=None):
    """
    NWE ENV Buy Strategy:
    
    - Evaluates the NWE Envelope indicator signals from the TA dictionary.
    - Checks for a breach of the lower envelope and a subsequent recovery above the breach depth.
    - Confirms that the overall trend (indicated by 'nwe_color') is green.
    - Sets the buy signal if all conditions are met.
    
    Returns:
        Updated buy object and TA dictionary.
    """

    # STRAT NWE Envelope Bands
    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.nwe_env.src
    bandwidth = st_pair.strats.nwe_env.bandwidth
    mult = st_pair.strats.nwe_env.mult

    # Use Gaussian smoothing to calculate the NWE line.
    h = bandwidth
    source = df[src].values
    nwe = gaussian_filter1d(source, sigma=h, mode='nearest')

    df['nwe_line'] = nwe
    df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)

    # Determine the NWE trend color.
    df['nwe_color'] = np.where(df['nwe_line'] > df['nwe_line'].shift(1), 'green', 'red')

    source = df[src].values
    nwe = df['nwe_line']
    
    # Compute the MAE between the price and the NWE line, then derive the envelope bands.
    mae = np.mean(np.abs(source - nwe)) * mult
    df['nwe_mae'] = mae
    df['nwe_upper'] = df['nwe_line'] + mae
    df['nwe_lower'] = df['nwe_line'] - mae

    # Detect a buy breach: when the low is below the lower envelope.
    df['nwe_env_buy_breach'] = (
        (df['low'] < df['nwe_lower']) |
        (df['low'].shift(1) < df['nwe_lower'].shift(1)) |
        (df['low'].shift(2) < df['nwe_lower'].shift(2))
    )

    # Calculate the breach depth (lowest price during a breach).
    df['nwe_env_buy_breach_depth'] = df.apply(
        lambda row: df[src][df[src] < df['nwe_lower']].min() if row['nwe_env_buy_breach'] else None,
        axis=1
    )

    # Generate 3‑row buy signals based on consecutive NWE colors and ROC conditions,
    # along with overall 'color' and 'ha_color' being green.
    df['nwe_env_buy_signal'] = (
        (df['nwe_env_buy_breach']) &
        (df[src] > df['nwe_env_buy_breach_depth'].fillna(df[src])) &
        (df['nwe_color'] == 'green') &
        (df['nwe_roc'] > 0) &
        (df['color'] == 'green') &
        (df['ha_color'] == 'green')
    ).astype(int)

    # Record buy history based on the signals found.
    buy_hist = []
    if df.get('nwe_env_buy_signal', pd.Series()).any():
        signal_times = df[df['nwe_env_buy_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            buy_hist.append(signal_time)

    # Set the current buy signal status.
    buy_now = df['nwe_env_buy_signal'].iloc[-1] if 'nwe_env_buy_signal' in df.columns else 0

    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_type = 'dn'
        buy.buy_strat_name = 'nwe_env'
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
def sell_strat_nwe_env(mkt, pos, ta, st_pair, curr_prc=None):
    """
    NWE ENV Sell Strategy:
    
    - Evaluates the NWE Envelope indicator signals from the TA dictionary.
    - Checks for a breach of the upper envelope and a subsequent recovery below the breach height.
    - Confirms that the overall trend (indicated by 'nwe_color') is red.
    - Sets the sell signal if the conditions are met and calls additional exit logic.
    
    Returns:
        Updated market object, position object, and TA dictionary.
    """

    # STRAT NWE ENV
    pos.sell_hist = []
    prod_id = pos.prod_id
    freq = pos.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.nwe_env.src
    bandwidth = st_pair.strats.nwe_env.bandwidth
    mult = st_pair.strats.nwe_env.mult

    # Use Gaussian smoothing to calculate the NWE line.
    h = bandwidth
    source = df[src].values
    nwe = gaussian_filter1d(source, sigma=h, mode='nearest')

    df['nwe_line'] = nwe
    df['nwe_roc'] = pta.roc(df['nwe_line'], length=3)

    # Determine the NWE trend color.
    df['nwe_color'] = np.where(df['nwe_line'] > df['nwe_line'].shift(1), 'green', 'red')

    source = df[src].values
    nwe = df['nwe_line']
    
    # Compute the MAE between the price and the NWE line, then derive the envelope bands.
    mae = np.mean(np.abs(source - nwe)) * mult
    df['nwe_mae'] = mae
    df['nwe_upper'] = df['nwe_line'] + mae
    df['nwe_lower'] = df['nwe_line'] - mae

    # Detect a sell breach: when the price is above the upper envelope.
    df['nwe_env_sell_breach'] = (
        (df[src] > df['nwe_upper']) |
        (df[src].shift(1) > df['nwe_upper'].shift(1)) |
        (df[src].shift(2) > df['nwe_upper'].shift(2))
    )

    # Calculate a per-row breach height safely (avoid heavy apply + reindexing)
    # Use the current price as the height when a breach is present, else NaN
    df['nwe_env_sell_breach_height'] = np.where(df['nwe_env_sell_breach'], df[src].values, np.nan)
    # Generate sell signal: breach occurred and price recovers below the breach height,
    # with the overall trend (color) red.
    df['nwe_env_sell_signal'] = (
        (df['nwe_env_sell_breach']) &
        (df[src] < df['nwe_env_sell_breach_height'].fillna(df[src])) &
        (df['nwe_color'] == 'red') &
        (df['nwe_roc'] < 0) &
        (df['color'] == 'red') &
        (df['ha_color'] == 'red')
    ).astype(int)

    # Record sell history based on the signals found.
    sell_hist = []
    if df.get('nwe_env_sell_signal', pd.Series()).any():
        signal_times = df[df['nwe_env_sell_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            sell_hist.append(signal_time)

    # Set the current sell signal status.
    sell_now = df['nwe_env_sell_signal'].iloc[-1] if 'nwe_env_sell_signal' in df.columns else 0

    if sell_now:
        pos.sell_yn = 'Y'
        pos.hodl_yn = 'N'
        pos.sell_strat_type = 'strat'
        pos.sell_strat_name = 'nwe_env'
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
