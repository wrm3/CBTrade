#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import traceback
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.lib_charts import chart_row
from libs.lib_colors import cs
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

def sell_strats_avail_get(mkt):
	func_name = 'sell_strats_avail_get'
	func_str = f'{lib_name}.{func_name}(mkt)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	func_end(fnc)
	return mkt

#<=====>#

def sell_strats_check(mkt, pos, ta):
	func_name = 'sell_strats_check'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)


	# Strategy Exit - Smoothed Heikin Ashi
	if pos.sell_yn == 'N':
		if pos.buy_strat_name == 'sha':
			mkt, pos = sell_strat_sha(mkt, pos, ta)
			sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": pos.sell_yn, "hodl_yn": pos.hodl_yn}
			pos.sell_signals.append(sell_signal)

	# Strategy Exit - Impulse MACD
	if pos.sell_yn == 'N':
		if pos.buy_strat_name == 'imp_macd':
			mkt, pos = sell_strat_imp_macd(mkt, pos, ta)
			sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": pos.sell_yn, "hodl_yn": pos.hodl_yn}
			pos.sell_signals.append(sell_signal)

	# Strategy Exit - Bollinger Band
	if pos.sell_yn == 'N':
		if pos.buy_strat_name == 'bb':
			mkt, pos = sell_strat_bb(mkt, pos, ta)
			sell_signal = {"pos_id": pos.pos_id, "sell_strat_type": pos.sell_strat_type, "sell_strat_name": pos.sell_strat_name, "sell_yn": pos.sell_yn, "hodl_yn": pos.hodl_yn}
			pos.sell_signals.append(sell_signal)

	func_end(fnc)
	return mkt, pos

#<=====>#

def disp_sell_tests(msg, mkt, pos, all_sells, all_hodls):
	func_name = 'disp_sell_tests'
	func_str = f'{lib_name}.{func_name}(msg, mkt, pos, all_sells, all_hodls)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = pos.prod_id

	if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pos.mst.show_tests_yn in ('Y','F'):
		msg = '    ' + cs('==> ' + msg + f' * sell => {pos.sell_yn} * sell_block => {pos.sell_block_yn} * hodl => {pos.hodl_yn}', font_color='white', bg_color='blue')
		chart_row(msg, len_cnt=240)
		if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pos.mst.show_tests_yn in ('Y'):
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
			chart_row(f'sell_yn : {pos.sell_yn}, hodl_yn : {pos.hodl_yn}', len_cnt=240)

	func_end(fnc)
	return mkt

#<=====>#

def sell_strat_sha(mkt, pos, ta):
	func_name = 'sell_strat_sha'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		# only_exit_if_profit_yn = 'Y'
		sell_prc    = mkt.prc_sell
		all_sells  = []
		all_hodls   = []

		freq = pos.buy_strat_freq

		# Check if sha fast body is growing or shrinking
		sha_fast_body_shrinking_tf = True
		sha_fast_body_curr = ta[freq]['sha_fast_body']['ago0']
		sha_fast_body_last = ta[freq]['sha_fast_body']['ago1']
		sha_fast_body_prev = ta[freq]['sha_fast_body']['ago2']

		if sha_fast_body_curr <= sha_fast_body_last <= sha_fast_body_prev:
			sha_fast_body_shrinking_tf = True
		else:
			sha_fast_body_shrinking_tf = False

		if sha_fast_body_shrinking_tf:
			msg = f'SELL COND: {freq} sha fast body is shrinking - curr {sha_fast_body_curr:>.8f} <<< last {sha_fast_body_last:>.8f} <<<  prev {sha_fast_body_prev:>.8f}'
			all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} sha fast body not shrinking - curr {sha_fast_body_curr:>.8f} >>> last {sha_fast_body_last:>.8f} >>>  prev {sha_fast_body_prev:>.8f}'
			all_hodls.append(msg)

		# Check if sha slow body is growing or shrinking
		sha_slow_body_shrinking_tf = True
		sha_slow_body_curr = ta[freq]['sha_slow_body']['ago0']
		sha_slow_body_last = ta[freq]['sha_slow_body']['ago1']
		sha_slow_body_prev = ta[freq]['sha_slow_body']['ago2']

		if sha_slow_body_curr <= sha_slow_body_last <= sha_slow_body_prev:
			sha_slow_body_shrinking_tf = True
		else:
			sha_slow_body_shrinking_tf = False

		if sha_slow_body_shrinking_tf:
			msg = f'SELL COND: {freq} sha slow body is shrinking - curr {sha_slow_body_curr:>.8f} <<< last {sha_slow_body_last:>.8f} <<<  prev {sha_slow_body_prev:>.8f}'
			all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} sha slow body not shrinking - curr {sha_slow_body_curr:>.8f} >>> last {sha_slow_body_last:>.8f} >>>  prev {sha_slow_body_prev:>.8f}'
			all_hodls.append(msg)

		# check if sha fast upper wick larger than lower wick
		sha_fast_upper_wick_weakening_tf = True
		ago_list = ['ago0', 'ago1', 'ago2', 'ago3']
		temp_all_sells = []
		temp_all_hodls = []
		for ago in ago_list:
			sha_fast_wick_upper = ta[freq]['sha_fast_wick_upper'][ago]
			sha_fast_wick_lower = ta[freq]['sha_fast_wick_lower'][ago]
			if ago == 'ago0': ago_desc = 'curr'
			elif ago == 'ago1': ago_desc = 'last'
			elif ago == 'ago2': ago_desc = 'prev'
			else: ago = 'curr'
			if sha_fast_wick_upper <= sha_fast_wick_lower:
				msg = f'SELL COND: {freq} {ago_desc} smaller upper wick - upper {sha_fast_wick_upper:>.8f} <<< lower {sha_fast_wick_lower:>.8f}'
				temp_all_sells.append(msg)
			else:
				sha_fast_upper_wick_weakening_tf = False
				msg = f'HODL COND: {freq} {ago_desc} larger upper wick - upper {sha_fast_wick_upper:>.8f} >>> lower {sha_fast_wick_lower:>.8f}' 
				temp_all_hodls.append(msg)
			# Need 4 in a row for test2 to be True

		if sha_fast_upper_wick_weakening_tf:
			msg = f'SELL COND: {freq} smaller upper wick for 4 consecutive candles'
			all_sells.append(msg)
			for msg in temp_all_sells:
				all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} larger upper wick in last 4 consecutive candles'
			all_hodls.append(msg)
			for msg in temp_all_hodls:
				all_hodls.append(msg)

		# check if sha slow upper wick larger than lower wick
		sha_slow_upper_wick_weakening_tf = True
		ago_list = ['ago0', 'ago1', 'ago2', 'ago3']
		temp_all_sells = []
		temp_all_hodls = []
		for ago in ago_list:
			sha_slow_wick_upper = ta[freq]['sha_slow_wick_upper'][ago]
			sha_slow_wick_lower = ta[freq]['sha_slow_wick_lower'][ago]
			if ago == 'ago0': ago_desc = 'curr'
			elif ago == 'ago1': ago_desc = 'last'
			elif ago == 'ago2': ago_desc = 'prev'
			else: ago = 'curr'
			if sha_slow_wick_upper <= sha_slow_wick_lower:
				msg = f'SELL COND: {freq} {ago_desc} smaller upper wick - upper {sha_slow_wick_upper:>.8f} <<< lower {sha_slow_wick_lower:>.8f}'
				temp_all_sells.append(msg)
			else:
				sha_slow_upper_wick_weakening_tf = False
				msg = f'HODL COND: {freq} {ago_desc} larger upper wick - upper {sha_slow_wick_upper:>.8f} >>> lower {sha_slow_wick_lower:>.8f}' 
				temp_all_hodls.append(msg)
			# Need 4 in a row for test2 to be True

		if sha_slow_upper_wick_weakening_tf:
			msg = f'SELL COND: {freq} smaller upper wick for 4 consecutive candles'
			all_sells.append(msg)
			for msg in temp_all_sells:
				all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} larger upper wick in last 4 consecutive candles'
			all_hodls.append(msg)
			for msg in temp_all_hodls:
				all_hodls.append(msg)

		# check if the price is intersecting the sha fast candles
		sha_fast_close = ta[freq]['sha_fast_close']['ago0']
		if sell_prc < sha_fast_close:
			sell_prc_intersect_sha_fast_tf = True
			msg = f'SELL COND: {freq} curr_price : {sell_prc:>.8f} is be below sha_fast_close {sha_fast_close:>.8f}'
			all_sells.append(msg)
		else:
			sell_prc_intersect_sha_fast_tf = False
			msg = f'HODL COND: {freq} curr_price : {sell_prc:>.8f} is be above sha_fast_close {sha_fast_close:>.8f}'
			all_hodls.append(msg)

		# check if sha fast candles are reddening
		sha_fast_color_curr = ta[freq]['sha_fast_color']['ago0']
		sha_fast_color_last = ta[freq]['sha_fast_color']['ago1']
		sha_fast_color_prev = ta[freq]['sha_fast_color']['ago2']
		if sha_fast_color_curr == 'red' and sha_fast_color_last == 'red' and sha_fast_color_prev == 'red':
			sha_fast_reddening_tf = True
			msg = f'SELL COND: {freq} sha fast colors ==> curr : {sha_fast_color_curr:>5}, last : {sha_fast_color_last:>5}, prev : {sha_fast_color_prev:>5}'
			all_sells.append(msg)
		else:
			sha_fast_reddening_tf = False
			msg = f'HODL COND: {freq} sha fast colors ==> curr : {sha_fast_color_curr:>5}, last : {sha_fast_color_last:>5}, prev : {sha_fast_color_prev:>5}'
			# YES!!! Allow the green candles to override the price touch above!
			all_hodls.append(msg)

		# check if sha slow candles are reddening
		sha_slow_color_curr = ta[freq]['sha_slow_color']['ago0']
		sha_slow_color_last = ta[freq]['sha_slow_color']['ago1']
		sha_slow_color_prev = ta[freq]['sha_slow_color']['ago2']
		if sha_slow_color_curr == 'red' and sha_slow_color_last == 'red' and sha_slow_color_prev == 'red':
			# sha_slow_reddening_tf = True
			msg = f'SELL COND: {freq} sha slow colors ==> curr : {sha_slow_color_curr:>5}, last : {sha_slow_color_last:>5}, prev : {sha_slow_color_prev:>5}'
			all_sells.append(msg)
		else:
			# sha_slow_reddening_tf = False
			msg = f'HODL COND: {freq} sha slow colors ==> curr : {sha_slow_color_curr:>5}, last : {sha_slow_color_last:>5}, prev : {sha_slow_color_prev:>5}'
			# YES!!! Allow the green candles to override the price touch above!
			all_hodls.append(msg)

		if sha_fast_body_shrinking_tf and sha_fast_upper_wick_weakening_tf:
			pos.sell_yn  = 'Y'
		elif sha_fast_body_shrinking_tf and sha_slow_body_shrinking_tf:
			pos.sell_yn  = 'Y'
		elif sell_prc_intersect_sha_fast_tf and (sha_fast_body_shrinking_tf or sha_slow_body_shrinking_tf or sha_fast_reddening_tf):
			pos.sell_yn  = 'Y'

		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
		msg = '    SELL TESTS - Smoothed Heikin Ashi'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, all_sells=all_sells, all_hodls=all_hodls)

		exit_if_profit_yn      = pos.mst.sell.strats.sha.exit_if_profit_yn
		exit_if_profit_pct_min = pos.mst.sell.strats.sha.exit_if_profit_pct_min
		exit_if_loss_yn        = pos.mst.sell.strats.sha.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(pos.mst.sell.strats.sha.exit_if_loss_pct_max) * -1
		if pos.sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pos.mst.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif pos.prc_chg_pct <= 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pos.mst.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'

		if pos.sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'sha'
			pos.sell_strat_freq = pos.buy_strat_freq
			pos.hodl_yn = 'N'
		else:
			pos.sell_yn = 'N'
			pos.hodl_yn = 'Y'

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {pos.prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos

#<=====>#

def sell_strat_imp_macd(mkt, pos, ta):
	func_name = 'sell_strat_imp_macd'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		all_sells  = []
		all_hodls   = []

		freq = pos.buy_strat_freq

		# Impulse MACD + ATR
		# MACD > Signal
		imp_macd_curr      = ta[freq]['imp_macd']['ago0']
		imp_macd_sign_curr = ta[freq]['imp_macd_sign']['ago0']
		if imp_macd_curr < imp_macd_sign_curr:
			msg = f'SELL COND: {freq} impulse macd < signal ==> macd : {imp_macd_curr:>5}, signal : {imp_macd_sign_curr:>5}'
			all_sells.append(msg)
		else:
			msg = f'HODL COND: {freq} impulse macd > signal ==> macd : {imp_macd_curr:>5}, signal : {imp_macd_sign_curr:>5}'
			all_hodls.append(msg)

		# MACD Line Should Be Green or Lime
		imp_macd_color = ta[freq]['imp_macd_color']['ago0']
		if imp_macd_color in ('red','orange'):
			imp_macd_color_ok_tf = True
			msg = f'SELL COND: {freq} impulse macd color must be lime or green ==> macd color : {imp_macd_color:>5}'
			all_sells.append(msg)
		else:
			imp_macd_color_ok_tf = False
			msg = f'HODL COND: {freq} impulse macd color must be lime or green ==> macd color : {imp_macd_color:>5}'
			all_hodls.append(msg)

		if imp_macd_curr and imp_macd_color_ok_tf:
			pos.sell_yn  = 'Y'

		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
		msg = '    SELL TESTS - Impluse MACD'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, all_sells=all_sells, all_hodls=all_hodls)

		exit_if_profit_yn      = pos.mst.sell.strats.imp_macd.exit_if_profit_yn
		exit_if_profit_pct_min = pos.mst.sell.strats.imp_macd.exit_if_profit_pct_min
		exit_if_loss_yn        = pos.mst.sell.strats.imp_macd.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(pos.mst.sell.strats.imp_macd.exit_if_loss_pct_max) * -1
		if pos.sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pos.mst.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif pos.prc_chg_pct <= 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pos.mst.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'

		if pos.sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'imp_macd'
			pos.sell_strat_freq = freq
			pos.hodl_yn = 'N'
		else:
			pos.sell_yn = 'N'
			pos.hodl_yn = 'Y'

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {pos.prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos

#<=====>#

def sell_strat_bb_bo(mkt, pos, ta):
	func_name = 'sell_strat_bb_bo'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		sell_prc    = mkt.prc_sell
		all_sells   = []
		all_hodls   = []

		rfreq = pos.buy_strat_freq
		freq = pos.buy_strat_freq

		curr_bb_upper_inner    = ta[freq]['bb_lower_inner']['ago0']

		# General Trend
		sell_prc_intersects_bb_upper_inner_tf
		if sell_prc < curr_bb_upper_inner:
			sell_prc_intersects_bb_upper_inner_tf = True
			msg = f'SELL COND: {rfreq} current price : {sell_prc:>.8f} below bb upper inner : {curr_bb_upper_inner:>.8f}'
			all_sells.append(msg)
		else:
			sell_prc_intersects_bb_upper_inner_tf = False
			msg = f'HODL COND: {rfreq} current price : {sell_prc:>.8f} below bb upper inner : {curr_bb_upper_inner:>.8f}'
			all_hodls.append(msg)

		if sell_prc_intersects_bb_upper_inner_tf:
			pos.sell_yn = 'Y'
		else:
			pos.sell_yn  = 'N'

		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'

		msg = '    SELL TESTS - Bollinger Band Breakout'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, all_sells=all_sells, all_hodls=all_hodls)

		exit_if_profit_yn      = pos.mst.sell.strats.bb_bo.exit_if_profit_yn
		exit_if_profit_pct_min = pos.mst.sell.strats.bb_bo.exit_if_profit_pct_min
		exit_if_loss_yn        = pos.mst.sell.strats.bb_bo.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(pos.mst.sell.strats.bb_bo.exit_if_loss_pct_ma) * -1
		if pos.sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pos.mst.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif pos.prc_chg_pct <= 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pos.mst.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'

		if pos.sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'bb_bo'
			pos.sell_strat_freq = freq
			pos.hodl_yn = 'N'
		else:
			pos.sell_yn = 'N'
			pos.hodl_yn = 'Y'

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {pos.prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos

#<=====>#

def sell_strat_bb(mkt, pos, ta):
	func_name = 'sell_strat_bb'
	func_str = f'{lib_name}.{func_name}(mkt, pos, ta)'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	try:
		sell_prc    = mkt.prc_sell
		all_sells   = []
		all_hodls   = []

		rfreq = pos.buy_strat_freq
		freq = pos.buy_strat_freq

		curr_bb_lower_outer   = ta[freq]['bb_lower_outer']['ago0']
		age_mins          = pos.age_mins
		if freq == '15min':
			min_mins = 15
		elif freq == '30min':
			min_mins = 30
		elif freq == '1h':
			min_mins = 60
		elif freq == '4h':
			min_mins = 240
		elif freq == '1d':
			min_mins = 1440

		if age_mins > min_mins and sell_prc < curr_bb_lower_outer:
			bb_downward_spiral_tf = True
			msg = f'SELL COND: {rfreq} current price : {sell_prc:>.8f} below bb lower outer : {curr_bb_lower_outer:>.8f} and gain_pct < 0 : {pos.gain_loss_pct_est}'
			all_sells.append(msg)
		else:
			bb_downward_spiral_tf = False
			msg = f'HODL COND: {rfreq} current price : {sell_prc:>.8f} above bb lower outer : {curr_bb_lower_outer:>.8f} and gain_pct < 0 : {pos.gain_loss_pct_est}'
			all_hodls.append(msg)

		if bb_downward_spiral_tf:
			pos.sell_yn  = 'Y'
		else:
			pos.sell_yn  = 'N'

		if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
		msg = '    SELL TESTS - Bollinger Band'
		mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, all_sells=all_sells, all_hodls=all_hodls)

		exit_if_profit_yn      = pos.mst.sell.strats.bb.exit_if_profit_yn
		exit_if_profit_pct_min = pos.mst.sell.strats.bb.exit_if_profit_pct_min
		exit_if_loss_yn        = pos.mst.sell.strats.bb.exit_if_loss_yn
		exit_if_loss_pct_max   = abs(pos.mst.sell.strats.bb.exit_if_loss_pct_max) * -1
		if pos.sell_yn == 'Y':
			if pos.prc_chg_pct > 0:
				if exit_if_profit_yn == 'Y':
					if pos.prc_chg_pct < exit_if_profit_pct_min:
						msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_profit_yn == 'N':
					msg = f'    * exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...'
					if pos.mst.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'
			elif pos.prc_chg_pct <= 0:
				if exit_if_loss_yn == 'Y':
					if pos.prc_chg_pct > exit_if_loss_pct_max:
						msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % > exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...'
						BoW(msg)
						pos.sell_yn = 'N'
						pos.hodl_yn = 'Y'
				elif exit_if_loss_yn == 'N':
					msg = f'    * exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} -  cancelling sell...'
					if pos.mst.show_tests_yn == 'Y':
						BoW(msg)
					pos.sell_yn = 'N'
					pos.hodl_yn = 'Y'

		if pos.sell_yn == 'Y':
			pos.sell_strat_type = 'strat'
			pos.sell_strat_name = 'bb'
			pos.sell_strat_freq = freq
			pos.hodl_yn = 'N'
		else:
			pos.sell_yn = 'N'
			pos.hodl_yn = 'Y'

	except Exception as e:
		print(f'{dttm_get()} {func_name} ==> {pos.prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
		traceback.print_stack()
		print_adv(2)
		pass

	func_end(fnc)
	return mkt, pos

#<=====>#

# def sell_logic_ema_cross(st, mkt, pos):
# 	func_name = 'sell_logic_ema_cross'
# 	func_str = f'{lib_name}.{func_name}(mkt, ta, pos)'
# #	G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 
# 	prod_id     = mkt.prod_id
# 	sell_prc    = mkt.prc_sell
# 	all_sells   = []
# 	all_hodls   = []
# 	sell_yn     = 'N'
# 	hodl_yn     = 'Y'
# 	show_tests_yn         = pos.mst.sell.show_tests_yn

# #	# Exponential Moving Average Crosses
# #	if 1==1:
# #		if pos.prc_chg_pct > -5:
# #			msg = 'REQUIRE: current 1h ema5 :{:>.8f} >>> ema8:{:>.8f}'.format(mkt.ta_ema5_1h['ago0'], mkt.ta_ema8_1h['ago0'])
# #			if mkt.ta_ema5_abv_ema8_1h['ago0']:
# #				all_sells.append(msg)
# #			else:
# #				all_hodls.append(msg)
# #			msg = 'REQUIRE: current 1h ema8 :{:>.8f} >>> ema13:{:>.8f}'.format(mkt.ta_ema8_1h['ago0'], mkt.ta_ema13_1h['ago0'])
# #			if mkt.ta_ema8_abv_ema13_1h['ago0']:
# #				all_sells.append(msg)
# #			else:
# #				all_hodls.append(msg)
# #			msg = 'REQUIRE: current 1h ema13 :{:>.8f} >>> ema21:{:>.8f}'.format(mkt.ta_ema13_1h['ago0'], mkt.ta_ema21_1h['ago0'])
# #			if mkt.ta_ema13_abv_ema21_1h['ago0']:
# #				all_sells.append(msg)
# #			else:
# #				all_hodls.append(msg)
# #			if pos.buy_strat_name != 'bb' and not mkt.ta_ema5_abv_ema8_1h['ago0'] and not mkt.ta_ema8_abv_ema13_1h['ago0'] and not mkt.ta_ema13_abv_ema21_1h['ago0']:
# #				sell_yn  = 'Y'
# #				hodl_yn  = 'N'

# 	func_end(fnc)
# 	return mkt, pos, sell_yn, hodl_yn

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

