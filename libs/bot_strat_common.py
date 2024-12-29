<<<<<<< Updated upstream
#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.bot_common import freqs_get
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_common import dttm_get, func_begin, func_end, print_adv, beep, speak
from libs.lib_colors import BoW
from libs.lib_colors import GoW
import traceback
import traceback
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_charts import chart_row
from libs.lib_colors import cs, cp, G
from libs.lib_common import dttm_get, func_begin, func_end, print_adv
from libs.lib_colors import BoW


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strats'
log_name      = 'bot_strats'


# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def disp_sell_tests(msg, mkt, pos, pst, all_sells, all_hodls):
	func_name = 'disp_sell_tests'
	func_str = f'{lib_name}.{func_name}(msg, mkt, pos, all_sells, all_hodls)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = pos.prod_id

	if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pst.sell.show_tests_yn in ('Y','F'):
		msg = '    ' + cs('==> ' + msg + f' {lib_name}.{func_name} * sell => {pos.sell_yn} * sell_block => {pos.sell_block_yn} * hodl => {pos.hodl_yn}', font_color='white', bg_color='blue')
		chart_row(msg, len_cnt=240)
		if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pst.sell.show_tests_yn in ('Y'):
			for e in all_sells:
				if pos.prc_chg_pct > 0:
					e = '    ' + cs('* ' + e, font_color='green')
					chart_row(e, len_cnt=240)
				else:
					e = '    ' + cs('* ' + e, font_color='red')
					chart_row(e, len_cnt=240)
				mkt.show_sell_header_tf = True
			for e in all_hodls:
				e = '    ' + cs('* ' + e, font_color='white', bg_color='green')
				chart_row(e, len_cnt=240)
				mkt.show_sell_header_tf = True
#			chart_row(f'sell_yn : {pos.sell_yn}, hodl_yn : {pos.hodl_yn}', len_cnt=240)

	func_end(fnc)
	return mkt

#<=====>#


def exit_if_logic(pos, pst):
	func_name = 'exit_if_logic'
	func_str = f'{lib_name}.{func_name}(pos, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)


	exit_if_profit_yn      = pst.sell.strats[pos.buy_strat_name].exit_if_profit_yn
	exit_if_profit_pct_min = pst.sell.strats[pos.buy_strat_name].exit_if_profit_pct_min
	exit_if_loss_yn        = pst.sell.strats[pos.buy_strat_name].exit_if_loss_yn
	exit_if_loss_pct_max   = abs(pst.sell.strats[pos.buy_strat_name].exit_if_loss_pct_max) * -1

	if pos.sell_yn == 'Y':
		if pos.prc_chg_pct > 0:
			if exit_if_profit_yn == 'Y':
				if pos.prc_chg_pct < exit_if_profit_pct_min:
					msg = ''
					msg += '    ' 
					msg += cs(f'==> exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...', font_color='blue', bg_color='white')
					print(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif exit_if_profit_yn == 'N':
				msg = ''
				msg += '    ' 
				msg += cs(f'==> exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...', font_color='blue', bg_color='white')
				if pst.sell.show_tests_yn == 'Y':
					print(msg)
				pos.sell_yn = 'N'
				pos.hodl_yn = 'Y'
		elif pos.prc_chg_pct <= 0:
			if exit_if_loss_yn == 'Y':
				if pos.prc_chg_pct > exit_if_loss_pct_max:
					msg = ''
					msg += '    ' 
					msg += cs(f'==> exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...', font_color='blue', bg_color='white')
					print(msg)
					print(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif exit_if_loss_yn == 'N':
				msg = ''
				msg += '    ' 
				msg += cs(f'==> exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...', font_color='blue', bg_color='white')
				if pst.sell.show_tests_yn == 'Y':
					print(msg)
				pos.sell_yn = 'N'
				pos.hodl_yn = 'Y'

	func_end(fnc)
	return pos

#<=====>#

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

=======
#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.bot_common import freqs_get
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_common import dttm_get, func_begin, func_end, print_adv, beep, speak
from libs.lib_colors import BoW
from libs.lib_colors import GoW
import traceback
import traceback
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_charts import chart_row
from libs.lib_colors import cs, cp, G
from libs.lib_common import dttm_get, func_begin, func_end, print_adv
from libs.lib_colors import BoW


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strats'
log_name      = 'bot_strats'


# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def disp_sell_tests(msg, mkt, pos, pst, all_sells, all_hodls):
	func_name = 'disp_sell_tests'
	func_str = f'{lib_name}.{func_name}(msg, mkt, pos, all_sells, all_hodls)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = pos.prod_id

	if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pst.sell.show_tests_yn in ('Y','F'):
		msg = '    ' + cs('==> ' + msg + f' {lib_name}.{func_name} * sell => {pos.sell_yn} * sell_block => {pos.sell_block_yn} * hodl => {pos.hodl_yn}', font_color='white', bg_color='blue')
		chart_row(msg, len_cnt=240)
		if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pst.sell.show_tests_yn in ('Y'):
			for e in all_sells:
				if pos.prc_chg_pct > 0:
					e = '    ' + cs('* ' + e, font_color='green')
					chart_row(e, len_cnt=240)
				else:
					e = '    ' + cs('* ' + e, font_color='red')
					chart_row(e, len_cnt=240)
				mkt.show_sell_header_tf = True
			for e in all_hodls:
				e = '    ' + cs('* ' + e, font_color='white', bg_color='green')
				chart_row(e, len_cnt=240)
				mkt.show_sell_header_tf = True
#			chart_row(f'sell_yn : {pos.sell_yn}, hodl_yn : {pos.hodl_yn}', len_cnt=240)

	func_end(fnc)
	return mkt

#<=====>#


def exit_if_logic(pos, pst):
	func_name = 'exit_if_logic'
	func_str = f'{lib_name}.{func_name}(pos, pst)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)


	exit_if_profit_yn      = pst.sell.strats[pos.buy_strat_name].exit_if_profit_yn
	exit_if_profit_pct_min = pst.sell.strats[pos.buy_strat_name].exit_if_profit_pct_min
	exit_if_loss_yn        = pst.sell.strats[pos.buy_strat_name].exit_if_loss_yn
	exit_if_loss_pct_max   = abs(pst.sell.strats[pos.buy_strat_name].exit_if_loss_pct_max) * -1

	if pos.sell_yn == 'Y':
		if pos.prc_chg_pct > 0:
			if exit_if_profit_yn == 'Y':
				if pos.prc_chg_pct < exit_if_profit_pct_min:
					msg = ''
					msg += '    ' 
					msg += cs(f'==> exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...', font_color='blue', bg_color='white')
					print(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif exit_if_profit_yn == 'N':
				msg = ''
				msg += '    ' 
				msg += cs(f'==> exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...', font_color='blue', bg_color='white')
				if pst.sell.show_tests_yn == 'Y':
					print(msg)
				pos.sell_yn = 'N'
				pos.hodl_yn = 'Y'
		elif pos.prc_chg_pct <= 0:
			if exit_if_loss_yn == 'Y':
				if pos.prc_chg_pct > exit_if_loss_pct_max:
					msg = ''
					msg += '    ' 
					msg += cs(f'==> exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...', font_color='blue', bg_color='white')
					print(msg)
					print(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif exit_if_loss_yn == 'N':
				msg = ''
				msg += '    ' 
				msg += cs(f'==> exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...', font_color='blue', bg_color='white')
				if pst.sell.show_tests_yn == 'Y':
					print(msg)
				pos.sell_yn = 'N'
				pos.hodl_yn = 'Y'

	func_end(fnc)
	return pos

#<=====>#

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

>>>>>>> Stashed changes
