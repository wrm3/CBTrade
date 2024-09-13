#<=====>#
# Description
#<=====>#


#<=====>#
# Import All
#<=====>#



#<=====>#
# Imports - Common Modules
#<=====>#

import sys
import os
import pytz
import sys
import time
import traceback
from datetime            import datetime
from pprint              import pprint


#<=====>#
# Imports - Download Modules
#<=====>#



#<=====>#
# Imports - Shared Library
#<=====>#
#shared_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SHARED_LIBS'))
#if shared_libs_path not in sys.path:
#	sys.path.append(shared_libs_path)



#<=====>#
# Imports - Local Library
#<=====>#
local_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'libs'))
if local_libs_path not in sys.path:
	sys.path.append(local_libs_path)

from libs.lib_charts                   import *
from libs.lib_common                   import *
from libs.lib_colors                   import *
from libs.lib_strings                  import *

from libs.bot_reports                   import *
from libs.bot_common                    import *
from libs.bot_db_read                   import *
from libs.bot_settings                  import settings
from libs.bot_theme                     import *
#from bot                               import bot


#<=====>#
# Variables
#<=====>#
lib_name      = 'run_report'
log_name      = 'run_report'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 0


#<=====>#
# Assignments Pre
#<=====>#



#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

def report_loop():
	func_name = 'report_loop'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name)
#	G(func_str)

	st = settings.reload()

	# this is for the disp.py bot only...
	upd_delay = 60

	cnt = 0
	while True:
		try:
			cnt += 1

			if cnt % 10 == 0:
				st = settings.reload()
				pprint(st)

			clear_screen()

			report_open_by_age()
			report_open_by_gain()
			report_open_by_prod_id()

			report_strats_best(25, min_trades=3)
			report_strats_best(25, min_trades=10)

			report_buys_recent(25, test_yn='Y')
			report_sells_recent(25, test_yn='Y')

			report_buys_recent(25, test_yn='N')
			report_sells_recent(25, test_yn='N')

			print_adv(2)
			print(f'{dttm_get()} updating every {upd_delay} seconds...')
			time.sleep(upd_delay)

		except KeyboardInterrupt as e:
			print(f'{func_name} ==> keyed exit... {e}')
			sys.exit()

		except Exception as e:
			print(f'{func_name} ==> errored... {e}')
			print(dttm_get())
			traceback.print_exc()
			print(type(e))
			print(e)
			print(f'sleeping {upd_delay} seconds and then restarting')
			time.sleep(upd_delay)


#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	report_loop()


#<=====>#
