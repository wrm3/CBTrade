#<=====>#
# Description
#<=====>#

#<=====>#
# Known To Do List
#<=====>#

#<=====>#
# Imports - Common Modules
#<=====>#
from datetime import datetime as dt
from datetime import timedelta
from pprint import pprint
import os
import pandas as pd 
import sys
import time
import traceback
import warnings
import uuid
import argparse
warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

#<=====>#
# Imports - Download Modules
#<=====>#

#<=====>#
# Imports - Shared Library
#<=====>#
# shared_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SHARED_LIBS'))
# if shared_libs_path not in sys.path:
# 	sys.path.append(shared_libs_path)

#<=====>#
# Imports - Local Library
#<=====>#
local_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'libs'))
if local_libs_path not in sys.path:
	sys.path.append(local_libs_path)

from libs.bot_cls_main                 import BOT

from libs.lib_common                   import *


#<=====>#
# Variables
#<=====>#
lib_name      = 'run_bot'
log_name      = 'run_bot'
lib_secs_max  = 10

#<=====>#
# Assignments Pre
#<=====>#



#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#



def main(bot):
	func_name = 'main'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	# G(func_str)

	# Set up argument parser
	parser = argparse.ArgumentParser(description="Process command line arguments.")
	
	# Add the argument 'action' which can be 's' or 'b'
	parser.add_argument('action', nargs='?', choices=['s', 'b'], help="Specify 's' or 'b' for specific actions")
	
	# Parse the arguments
	args = parser.parse_args()
	
	# Perform actions based on the arguments
	if args.action == 's':
		bot.bot_sell()
	elif args.action == 'b':
		bot.bot_buy()
	else:
		bot.bot()


#<=====>#
# Post Variables
#<=====>#

bot = BOT()


#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	main(bot)


#<=====>#

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

