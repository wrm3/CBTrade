#<=====>#
# Description
#
# This module implements a "DROP" trading strategy based on a price drop from the 24‑hour high.
# The strategy calculates the 24‑hour high and then determines a target price based on a drop 
# percentage. A buy signal is generated when the current price is above the target price while 
# at least one of the previous three candles had a price below the target, and when both the overall 
# color and the Heikin‑Ashi color are green.
#<=====>#

 
#<=====>#
# Known To Do List
#
# - Confirm that the intended drop percentage column is "drop_target_prc" and not "target_prc"
#   in the buy signal condition.
# - Verify if the "emax" settings (under 'sha') are meant to be part of this module.
# - Consider enhancing the sell strategy if exit logic is needed.
#<=====>#


#<=====>#
# Imports
#<=====>#
import numpy as np
import pandas as pd
import pandas_ta as pta
import sys
import traceback
from libs.common import beep, dttm_get, narc
from libs.common import print_adv
from libs.strats._strat_common import disp_sell_tests, exit_if_logic
from fstrent_colors import cs  # Imported but not used; ensure it is needed

#<=====>#
# Variables
#<=====>#
lib_name = 'bot_strat_drop'
log_name = 'bot_strat_drop'


#<=====>#
# Functions
#<=====>#

# @safe_execute_silent()
@narc(1)
def settings_drop(st):
    """
    Define and assign the settings for the DROP buy strategy.
    """
    sst = {
        "use_yn": "Y",
        "freqs": ["1d", "4h", "1h", "30min", "15min"],
        "src": 'close',
        "drop_pct": {
            "***": 4,
            "BTC-USDC": 4,
            "ETH-USDC": 4,
            "SOL-USDC": 4
        },
        "buy": {
            "prod_ids": [
                "BTC-USDC",
                "ETH-USDC",
                "SOL-USDC"
            ],
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
    st['strats']['drop'] = sst
    return st

#<=====>#

# @safe_execute()
@narc(1)
def buy_strat_drop(buy, ta, st_pair, curr_prc=None):
    """
    DROP Buy Strategy:
    
    - Dynamically calculates a 24‑hour high and derives a target price by reducing that high
      by a given drop percentage.
    - Generates a buy signal if the current price is above the target price and at least one
      of the previous three candles had a price below the target.
    - Requires that both the overall 'color' and the Heikin‑Ashi 'ha_color' are green.
    
    Records the buy history and updates the buy signal status.
    
    Note: There is a potential bug where the condition uses 'target_prc' instead of 'drop_target_prc'.
    """

    # STRAT DROP
    buy.buy_hist = []
    prod_id = buy.prod_id
    freq = buy.buy_strat_freq
    df = ta[freq].df

    src = st_pair.strats.drop.src
    drop_pct = st_pair.strats.drop.drop_pct

    # Set the current price.
    df['curr_prc'] = df['close']
    if curr_prc:
        df['curr_prc'].iloc[-1] = curr_prc

    # Dynamically calculate window size based on the candle frequency.
    # For example, if freq is '15min', then window_size becomes 96 (i.e. 24h / 15min).
    window_size = int(pd.Timedelta(hours=24) / pd.Timedelta(freq))
    df['high_24h'] = df['high'].rolling(window=window_size, min_periods=1).max()

    # Calculate the drop percentage (convert drop_pct into a decimal multiplier).
    drop_pct_dec = (100 - drop_pct) / 100

    # Calculate the target buy price based on the 24h high.
    df['drop_target_prc'] = df['high_24h'] * drop_pct_dec

    # Generate the buy signal:
    # • Current price must be above the target price.
    # • At least one of the previous 3 candles had a price below the target.
    # • Both 'color' and 'ha_color' must be green.
    df['drop_buy_signal'] = (
        (df['curr_prc'] > df['drop_target_prc']) & 
        (
            (df['curr_prc'].shift(1) < df['drop_target_prc'].shift(1)) |
            (df['curr_prc'].shift(2) < df['drop_target_prc'].shift(2)) |
            (df['curr_prc'].shift(3) < df['drop_target_prc'].shift(3))
        ) & 
        (df['color'] == 'green') &
        (df['ha_color'] == 'green')
    )

    # Record buy history based on signal times.
    buy_hist = []
    if df['drop_buy_signal'].any():
        signal_times = df[df['drop_buy_signal'] == 1].index.tolist()
        for signal_time in signal_times:
            buy_hist.append(signal_time)

    # Determine the current buy signal.
    buy_now = df['drop_buy_signal'].iloc[-1]

    if buy_now:
        buy.buy_yn = 'Y'
        buy.wait_yn = 'N'
        buy.buy_strat_type = 'dn'
        buy.buy_strat_name = 'drop'
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
def sell_strat_drop(mkt, pos, ta, st_pair, curr_prc=None):
    """
    DROP Sell Strategy:
    
    Currently, this strategy does not trigger any sell signals.
    It sets the sell flag to 'N' and the hold flag to 'Y'.
    """
    pos.sell_hist = []
    pos.sell_yn = 'N'
    pos.hodl_yn = 'Y'

    return mkt, pos, ta


#<=====>#
# Post Variables
#<=====>#
# (Define any post-run variables here if necessary)


#<=====>#
# Default Run
#<=====>#
# (Add any default run code here if this module is executed as a standalone script)
#<=====>#
