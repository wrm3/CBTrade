#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.bot_reports import report_buys_recent, report_open_by_gain, report_strats_best
from libs.bot_reports import report_open_by_age
from libs.bot_reports import report_open_by_prod_id
from libs.bot_reports import report_sells_recent
from libs.bot_settings import bot_settings_get
from libs.bot_settings import debug_settings_get
from libs.bot_settings import get_lib_func_secs_max
from libs.lib_common import clear_screen
from libs.lib_common import dttm_get
from libs.lib_common import func_begin
from libs.lib_common import func_end
from libs.lib_common import print_adv
from pprint import pprint
import pandas as pd
import sys
import time
import traceback
import warnings
warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)



#<=====>#
# Variables
#<=====>#
lib_name      = 'run_report'
log_name      = 'run_report'



# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)
# print(f'{lib_name}, lib_secs_max : {lib_secs_max}')


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

	bst, bot_setings = bot_settings_get()

	# this is for the disp.py bot only...
	upd_delay = 60

	cnt = 0
	while True:
		try:
			cnt += 1

			if cnt % 10 == 0:
				bst = bot_setings.reload()
				pprint(bst)

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

	func_end(fnc)

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	report_loop()


#<=====>#