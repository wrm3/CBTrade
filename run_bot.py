#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
# Standard library imports
import argparse
import sys
import traceback

# Third-party imports
import pandas as pd

# Local imports
from fstrent_colors import cs
from fstrent_tools import dttm_get
from libs.bot_cls_main import BOT

# <=====>#
# Variables
# <=====>#
lib_name = 'run_bot'
log_name = 'run_bot'

# <=====>#
# Assignments Pre
# <=====>#


# <=====>#
# Classes
# <=====>#


# <=====>#
# Functions
# <=====>#


def main(bot):

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process command line arguments.")

    # Add the argument 'action' which can be 'a', 'b', 'f', 's'
    parser.add_argument(
        'action', 
        nargs='?', 
        choices=['a', 'auto', 'b', 'buy', 'f', 'full', 's', 'sell'], 
        help="Specify 'a', 'b', 'f', 's' for specific actions..."
        )

    # Parse the arguments
    args = parser.parse_args()

    msg = 'you can add command line arguments to this bot. default if f for full. b for buy only. s for sell only. a for auto only...'
    msg = cs(msg, font_color='purple')

    # Perform actions based on the arguments
    if args.action in ('s', 'sell'):
        bot.mode = 'sell'
        bot.main_loop()
    elif args.action in ('b', 'buy'):
        bot.mode = 'buy'
        bot.main_loop()
    elif args.action in ('a', 'auto'):
        bot.mode = 'auto'
        bot.auto_loop()
    else:
        bot.mode = 'full'
        bot.main_loop()


# <=====>#
# Post Variables
# <=====>#

bot = BOT()


# <=====>#
# Default Run
# <=====>#

if __name__ == "__main__":
    main(bot)


# <=====>#

'''
                "AAVE-USDC",
                "ADA-USDC",
                "AKT-USDC",
                "ALGO-USDC",
                "APT-USDC",
                "AR-USDC",
                "ARB-USDC",
                "ATOM-USDC",
                "AVAX-USDC",
                "BADGER-USDC",
                "BEAM-USDC",
                "BNB-USDC",
                "BNX-USDC",
                "BONK-USDC",
                "BTC-USDC",
                "BTT-USDC",
                "DOGE-USDC",
                "DOT-USDC",
                "DYP-USDC",
                "ETH-USDC",
                "FET-USDC",
                "FIL-USDC",
                "FLOW-USDC",
                "FTM-USDC",
                "FX-USDC",
                "GAL-USDC",
                "GFI-USDC",
                "GLM-USDC",
                "GRT-USDC",
                "HBAR-USDC",
                "HNT-USDC",
                "HONEY-USDC",
                "ICP-USDC",
                "IMX-USDC",
                "INJ-USDC",
                "JASMY-USDC",
                "JUP-USDC",
                "KLAY-USDC",
                "LDO-USDC",
                "LINK-USDC",
                "MATH-USDC",
                "MATIC-USDC",
                "MKR-USDC",
                "MNDE-USDC",
                "NEAR-USDC",
                "OMNI-USDC",
                "ONDO-USDC",
                "OP-USDC",
                "PEPE-USDC",
                "PYTH-USDC",
                "RENDER-USDC",
                "RNDR-USDC",
                "SEI-USDC",
                "SHIB-USDC",
                "SHPING-USDC",
                "SOL-USDC",
                "STRK-USDC",
                "STX-USDC",
                "SUI-USDC",
                "SUKU-USDC",
                "SWFTC-USDC",
                "TIA-USDC",
                "TNSR-USDC",
                "TON-USDC",
                "TRB-USDC",
                "TVK-USDC",
                "UMA-USDC",
                "UNI-USDC",
                "VET-USDC",
                "W-USDC",
                "WIF-USDC",
                "XRP-USDC"
'''

'''
                "ADA-USDC",
                "AVAX-USDC",
                "BONK-USDC",
                "BTC-USDC",
                "DOGE-USDC",
                "ETH-USDC",
                "LDO-USDC",
                "MATIC-USDC",
                "OMNI-USDC",
                "RNDR-USDC",
                "SHIB-USDC",
                "SOL-USDC",
                "UNI-USDC",
                "WIF-USDC"
'''

'''
                "ADA-USDC",
                "AVAX-USDC",
                "BADGER-USDC",
                "BNB-USDC",
                "BONK-USDC",
                "BTC-USDC",
                "DOGE-USDC",
                "DOT-USDC",
                "ETH-USDC",
                "HONEY-USDC",
                "ICP-USDC",
                "JASMY-USDC",
                "LDO-USDC",
                "MATIC-USDC",
                "OMNI-USDC",
                "RNDR-USDC",
                "SHIB-USDC",
                "SOL-USDC",
                "SUI-USDC",
                "TON-USDC",
                "UNI-USDC",
                "WIF-USDC",
                "XRP-USDC"

                "AAVE-USDC",
                "ADA-USDC",
                "ALGO-USDC",
                "ATOM-USDC",
                "AVAX-USDC",
                "BADGER-USDC",
                "BNB-USDC",
                "BONK-USDC",
                "BTC-USDC",
                "DOGE-USDC",
                "DOT-USDC",
                "ETH-USDC",
                "FTM-USDC",
                "HBAR-USDC",
                "HNT-USDC",
                "HONEY-USDC",
                "ICP-USDC",
                "JASMY-USDC",
                "LDO-USDC",
                "OMNI-USDC",
                "POL-USDC",
                "RNDR-USDC",
                "SHIB-USDC",
                "SOL-USDC",
                "SUI-USDC",
                "TON-USDC",
                "UNI-USDC",
                "WIF-USDC",
                "XRP-USDC"

                
'''
