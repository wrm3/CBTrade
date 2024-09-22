#<=====>#
# Import All Scope
#<=====>#

import_all_func_list = []
import_all_func_list.append("buy_log")
import_all_func_list.append("sell_log")
__all__ = import_all_func_list

#<=====>#
# Description
#<=====>#


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
import sys
import os
import pandas as pd 
import warnings

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

from lib_common                    import *

from bot_common                    import *

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_logs'
log_name      = 'bot_logs'
lib_verbosity = 0
lib_debug_lvl = 0
lib_secs_max  = 2

#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def buy_log(msg):
	func_name = 'buy_log'
	func_str = f'{lib_name}.{func_name}(msg)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	dt_str  = dt.now().strftime('%Y_%m_%d')
	logfile = f"logs_buy/{dt_str}_buy_log.txt"
	wmsg    = f'{dttm_get()} ==> {msg}'
	file_write(logfile, wmsg)

	func_end(fnc)

#<=====>#

def sell_log(msg):
	func_name = 'sell_log'
	func_str = f'{lib_name}.{func_name}(msg)'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	dt_str  = dt.now().strftime('%Y_%m_%d')
	logfile = f"logs_sell/{dt_str}_sell_log.txt"
	wmsg    = f'{dttm_get()} ==> {msg}'
	file_write(logfile, wmsg)

	func_end(fnc)


#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#
