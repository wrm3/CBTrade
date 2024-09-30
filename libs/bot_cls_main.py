#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.bot_cls_market import MARKET
from libs.bot_coinbase import cb_mkts_refresh, cb_ord_get
from libs.bot_common import calc_chg_pct
from libs.bot_db_read import (
    db_buy_ords_open_get, db_mkt_sizing_data_get_by_uuid, db_pos_get_by_pos_id, 
    db_poss_sell_order_problems_get, db_sell_ords_get_by_uuid, db_sell_ords_open_get
)
from libs.bot_db_write import (
    db_buy_ords_stat_upd, db_table_csvs_dump, db_tbl_buy_ords_insupd, 
	db_tbl_poss_insupd, db_tbl_sell_ords_insupd
)
from libs.bot_reports import report_buys_recent, report_open_by_age, report_sells_recent
from libs.bot_settings import bot_settings_get, debug_settings_get, get_lib_func_secs_max, pair_settings_get
from libs.cls_settings import AttrDict
from libs.lib_charts import chart_bottom, chart_headers, chart_mid, chart_row, chart_top
from libs.lib_colors import G, WoB, cp, cs
from libs.lib_common import AttrDictConv, beep, dec_2_float, dttm_get, func_begin, func_end, print_adv, speak_async
from pprint import pprint
import sys
import time
import traceback


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_cls_main'
log_name      = 'bot_cls_main'
lib_secs_max  = 2

# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)
# print(f'{lib_name}, lib_secs_max : {lib_secs_max}')

bst, bot_settings = bot_settings_get()


#<=====>#
# Classes
#<=====>#

class BOT():

	def __init__(self, mode='full'):
		self.mode = mode
		self.fnc_secs_max              = 0.33
		self.dst, self.debug_settings = debug_settings_get()
		self.bst, self.settings         = bot_settings_get()

	#<=====>#

	def auto_loop(self):
		func_name = 'auto_loop'
		func_str = f'{lib_name}.{func_name}()'
		G(func_str)

		# this is here just to proof that sounds alerts will be heard
		if self.bst.speak_yn == 'Y': speak_async('Coinbase Trade Bot Online - Auto Mode')

		cnt = 0
		while True:
			try:
				cnt += 1
				t0 = time.perf_counter()

				self.bst = self.settings.reload()

				print_adv(2)
				chart_top(len_cnt=200)
				msg = f'<----- // ===== | == TOP == | ===== \\ ----->'
				chart_row(msg, len_cnt=200, align='center')
				chart_bottom(len_cnt=200)
				print_adv(2)

				cb_mkts_refresh()

				self.buy_ords_check()
				self.sell_ords_check()

				report_open_by_age()
				print_adv(3)

				report_buys_recent(cnt=20)
				print_adv(3)

				report_sells_recent(cnt=20)
				print_adv(3)

				# Dump CSVs of database tables for recovery
				if cnt == 1 or cnt % 10 == 0:
					db_table_csvs_dump()

				# End of Loop Display
				loop_secs = self.bst.auto_loop_secs

				print_adv(2)

				t1 = time.perf_counter()
				elapsed_seconds = round(t1 - t0, 2)

				WoB(f'{lib_name}.{func_name} ==> auto_loop() completed loop {cnt} in {elapsed_seconds} seconds. Looping in {loop_secs} seconds...')

				print_adv(2)
				chart_top(len_cnt=200)
				msg = f'<----- // ===== | == END == | ===== \\ ----->'
				chart_row(msg, len_cnt=200, align='center')
				chart_bottom(len_cnt=200)
				print_adv(2)

				time.sleep(loop_secs)

			except KeyboardInterrupt as e:
				print(f'{func_name} ==> keyed exit... {e}')
				sys.exit()

			except Exception as e:
				loop_secs = self.bst.loop_secs
				print(f'{func_name} ==> errored... {e}')
				print(dttm_get())
				traceback.print_exc()
				traceback.print_stack()
				print(type(e))
				print(e)
				print(f'sleeping {loop_secs} seconds and then restarting')
				time.sleep(loop_secs)

	#<=====>#

	def main_loop(self):
		func_name = 'main_loop'
		func_str = f'{lib_name}.{func_name}()'
#		G(func_str)

		if self.mode == 'buy':
			mode_str = 'Buy Mode'
		elif self.mode == 'sell':
			mode_str = 'Sell Mode'
		else:
			mode_str = 'Full Mode'

		# this is here just to proof that sounds alerts will be heard
		if self.bst.speak_yn == 'Y': speak_async(f'Coinbase Trade Bot Online - {mode_str}')

		cnt = 0
		while True:
			try:
				cnt += 1
				t0 = time.perf_counter()

				self.bst = self.settings.reload()

				print_adv(2)
				chart_top(len_cnt=200)
				msg = f'<----- // ===== | == TOP == | ===== \\ ----->'
				chart_row(msg, len_cnt=200, align='center')
				chart_bottom(len_cnt=200)
				print_adv(2)

				self.markets_loop()

				# Dump CSVs of database tables for recovery
				if cnt == 1 or cnt % 10 == 0:
					db_table_csvs_dump()

				# End of Loop Display
				loop_secs = self.bst.loop_secs

				print_adv(2)

				t1 = time.perf_counter()
				elapsed_seconds = round(t1 - t0, 2)

				WoB(f'{lib_name}.{func_name} ==> completed {cnt} loop in {elapsed_seconds} seconds. Looping in {loop_secs} seconds...')

				print_adv(2)
				chart_top(len_cnt=200)
				msg = f'<----- // ===== | == END == | ===== \\ ----->'
				chart_row(msg, len_cnt=200, align='center')
				chart_bottom(len_cnt=200)
				print_adv(2)

				time.sleep(loop_secs)

			except KeyboardInterrupt as e:
				print(f'{func_name} ==> keyed exit... {e}')
				sys.exit()

			except Exception as e:
				loop_secs = self.bst.loop_secs
				print(f'{func_name} ==> errored... {e}')
				print(dttm_get())
				traceback.print_exc()
				traceback.print_stack()
				print(type(e))
				print(e)
				print(f'sleeping {loop_secs} seconds and then restarting')
				time.sleep(loop_secs)

	#<=====>#

	def markets_loop(self):
		func_name = 'markets_loop'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		t0 = time.perf_counter()

		for symb in self.bst.trade_markets:
			fpath = self.bst.trade_markets[symb]['settings_fpath']

			mkt = MARKET(symb=symb, fpath=fpath, mode=self.mode)
			mkt.main_loop()

		# end of Performance Timer for mkt loop
		t1 = time.perf_counter()
		secs = round(t1 - t0, 3)
		if secs > lib_secs_max:
			cp(f'mkt_loops - took {secs} seconds to complete...', font_color='white', bg_color='orangered')

		func_end(fnc)

	#<=====>#

	def main_performance(self):
		func_name = 'main_performance'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)


		func_end(fnc)

	#<=====>#

	def main_display(self):
		func_name = 'main_display'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)


		func_end(fnc)

	#<=====>#

	def buy_ords_check(self):
		func_name = 'buy_ords_check'
		func_str = f'{lib_name}.{func_name}()'
		lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		try:

			print_adv(2)
			chart_top(len_cnt=200)
			msg = f'* Buy Orders Check * {dttm_get()} *'
			chart_row(msg, len_cnt=200, align='center')

			bos = db_buy_ords_open_get()
			if bos:
				chart_mid(len_cnt=200)
				chart_headers(in_str='', len_cnt=200)

				bos_cnt = len(bos)
				cnt = 0
				for bo in bos:
					cnt += 1
					bo = dec_2_float(bo)
					bo = AttrDictConv(in_dict=bo)
					test_tf = bo.test_tf

					if test_tf == 0:
						ord_id = bo.buy_order_uuid
						o = cb_ord_get(order_id=ord_id)

						if o:
							o = dec_2_float(o)
							o = AttrDictConv(in_dict=o)

							if o.prod_id != bo.prod_id:
								print(func_str)
								print('error #1 !')
								beep(3)
								sys.exit()

							if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
								bo.buy_cnt_act                    = o.ord_filled_size
								bo.fees_cnt_act                   = o.ord_total_fees
								bo.tot_out_cnt                    = o.ord_total_value_after_fees
								bo.prc_buy_act                    = o.ord_average_filled_price # not sure this includes the fees
								bo.buy_end_dttm                   = o.ord_last_fill_time
								bo.tot_prc_buy                    = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
								if o.ord_settled:
									bo.ord_stat                   = 'FILL'
								bo.prc_buy_slip_pct               = round((bo.prc_buy_act - bo.prc_buy_est) / bo.prc_buy_est, 8)

								print(f'{cnt:>2} / {bos_cnt:>2}, prod_id : {bo.prod_id:<15}, bo_uuid : {bo.buy_order_uuid:<60}')

								db_tbl_buy_ords_insupd(bo)
								self.pos_open(bo.buy_order_uuid)

							elif o.ord_status == 'OPEN':
								print(o)
								print('WE NEED CODE HERE!!!')
#								beep()

							else:
								print(func_str)
								print('error #2 !')
#								beep(3)
								db_buy_ords_stat_upd(bo_id=bo.bo_id, ord_stat='ERR')

					elif test_tf == 1:
						bo.ord_stat = 'FILL'
						db_tbl_buy_ords_insupd(bo)
						self.pos_open(bo.buy_order_uuid)

			chart_bottom(len_cnt=200)
			print_adv(2)

		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			print(f'so : {bo}')
			print(f'ord_id : {ord_id}')
			print(f'o : {o}')
			sys.exit()

		func_end(fnc)

	#<=====>#

	def sell_ords_check(self):
		func_name = 'sell_ords_check'
		func_str = f'{lib_name}.{func_name}()'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		try:

			print_adv(2)
			chart_top(len_cnt=200)
			msg = f'* Sell Orders Check * {dttm_get()} *'
			chart_row(msg, len_cnt=200, align='center')

			cnt = 0

			iss = db_poss_sell_order_problems_get()
			if iss:
				for i in iss:
					print(i)
				beep(10)
				sys.exit()

			sos = db_sell_ords_open_get()
			if sos:
				chart_mid(len_cnt=200)
				chart_headers(in_str='', len_cnt=200)

				sos_cnt = len(sos)
				for so in sos:
					cnt += 1
					so = dec_2_float(so)
					so = AttrDictConv(in_dict=so)

					print(so)

					test_tf = so.test_tf
					ord_id = so.sell_order_uuid

					if test_tf == 0:
						try:
							o = cb_ord_get(order_id=ord_id)
						except Exception as e:
							print(f'{func_name} ==> errored... {type(e)} {e}')
							traceback.print_exc()
							traceback.print_stack()
							print(f'so : {so}')
							beep()
							continue

						print(o)

						if o:
							o = dec_2_float(o)
							o = AttrDictConv(in_dict=o)
							if o.ord_status == 'FILLED' or o.ord_completion_percentage == '100.0' or o.ord_completion_percentage == 100.0:
								so.sell_cnt_act                    = o.ord_filled_size
								so.fees_cnt_act                    = o.ord_total_fees
								so.tot_in_cnt                      = o.ord_total_value_after_fees
								so.prc_sell_act                    = o.ord_average_filled_price # not sure this includes the fees
								so.sell_end_dttm                   = o.ord_last_fill_time
								so.tot_prc_buy                     = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
								if o.ord_settled:
									so.ord_stat                    = 'FILL'
								so.prc_sell_slip_pct              = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 8)
								print(f'{cnt:^4} / {sos_cnt:^4}, prod_id : {so.prod_id:<16}, pos_id : {so.pos_id:>7}, so_id : {so.so_id:>7}, so_uuid : {so.sell_order_uuid:<60}')
								db_tbl_sell_ords_insupd(so)
								self.pos_close(so.pos_id, so.sell_order_uuid)
							elif o.ord_status == 'OPEN':
								print(o)
								print('WE NEED CODE HERE #1 !!!')
								beep(10)
								sys.exit()

								if o.ord_filled_size > 0:
									so.sell_cnt_act                    = o.ord_filled_size
									so.fees_cnt_act                    = o.ord_total_fees
									so.tot_in_cnt                      = o.ord_total_value_after_fees
									so.prc_sell_act                    = o.ord_average_filled_price # not sure this includes the fees
									so.sell_end_dttm                   = o.ord_last_fill_time
									so.tot_prc_buy                     = round(o.ord_total_value_after_fees / o.ord_filled_size, 8)
									so.prc_sell_slip_pct               = round((so.prc_sell_act - so.prc_sell_est) / so.prc_sell_est, 8)
									print(f'{cnt:^4} / {sos_cnt:^4}, prod_id : {so.prod_id:<16}, pos_id : {so.pos_id:>7}, so_id : {so.so_id:>7}, so_uuid : {so.sell_order_uuid:<60}')
									beep(10)
									sys.exit()


									db_tbl_sell_ords_insupd(so)
		# this needs to be added when we add in support for limit orders
		#						else:
		#							r = cb_ord_cancel_orders(order_ids=[ord_id])
		#							db_sell_ords_stat_upd(so_id=so.so_id, ord_stat='CANC')
		#							db_poss_err_upd(pos_id=so.pos_id, pos_stat='OPEN')
							else:
								pprint(o)
								print('WE NEED CODE HERE #1 !!!')
								beep(10)
								sys.exit()
								db_sell_ords_stat_upd(so_id=so.so_id, ord_stat='ERR')
								db_poss_err_upd(pos_id=so.pos_id, pos_stat='OPEN')

					elif test_tf == 1:
						so.ord_stat = 'FILL'
						db_tbl_sell_ords_insupd(so)
						self.pos_close(so.pos_id, so.sell_order_uuid)

			chart_bottom(len_cnt=200)
			print_adv(2)

		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			print(f'so : {so}')
			print(f'ord_id : {ord_id}')
			print(f'o : {o}')
			sys.exit()

		func_end(fnc)

	#<=====>#

	def pos_open(self, buy_order_uuid):
		func_name = 'pos_open'
		func_str = f'{lib_name}.{func_name}(buy_order_uuid={buy_order_uuid})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		bos = db_mkt_sizing_data_get_by_uuid(buy_order_uuid)

		for bo in bos:
			bo = dec_2_float(bo)
			bo = AttrDictConv(in_dict=bo)
			pos = AttrDict()
			pos.test_tf                 = bo.test_tf
			pos.symb                    = bo.symb
			pos.prod_id                 = bo.prod_id
			pos.mkt_name                = bo.mkt_name
			pos.mkt_venue               = bo.mkt_venue
			pos.base_curr_symb          = bo.buy_curr_symb
			pos.base_size_incr          = bo.base_size_incr
			pos.base_size_min           = bo.base_size_min
			pos.base_size_max           = bo.base_size_max
			pos.quote_curr_symb         = bo.quote_curr_symb
			pos.quote_size_incr         = bo.quote_size_incr
			pos.quote_size_min          = bo.quote_size_min
			pos.quote_size_max          = bo.quote_size_max
			pos.pos_type                = bo.pos_type
			pos.pos_stat                = 'OPEN'
			pos.pos_begin_dttm          = bo.buy_begin_dttm
			pos.bo_id                   = bo.bo_id
			pos.bo_uuid                 = bo.buy_order_uuid
			pos.buy_strat_type          = bo.buy_strat_type
			pos.buy_strat_name          = bo.buy_strat_name
			pos.buy_strat_freq          = bo.buy_strat_freq
			pos.buy_curr_symb           = bo.buy_curr_symb
			pos.buy_cnt                 = bo.buy_cnt_act
			pos.spend_curr_symb         = bo.spend_curr_symb
			pos.fees_curr_symb          = bo.fees_curr_symb
			pos.buy_fees_cnt            = bo.fees_cnt_act
			pos.tot_out_cnt             = bo.tot_out_cnt
			pos.sell_curr_symb          = bo.buy_curr_symb
			pos.recv_curr_symb          = bo.spend_curr_symb
			pos.sell_order_cnt          = 0
			pos.sell_order_attempt_cnt  = 0
			pos.hold_cnt                = bo.buy_cnt_act
			pos.sell_cnt_tot            = 0
			pos.tot_in_cnt              = 0
			pos.sell_fees_cnt_tot       = 0
			pos.prc_buy                 = bo.tot_prc_buy
			pos.prc_curr                = bo.prc_buy_act
			pos.prc_high                = bo.prc_buy_act
			pos.prc_low                 = bo.prc_buy_act
			pos.prc_chg_pct             = 0
			pos.prc_chg_pct_high        = 0
			pos.prc_chg_pct_low         = 0
			pos.prc_chg_pct_drop        = 0

			pos.fees_cnt_tot            = bo.fees_cnt_act

			pos.gain_loss_amt_est       = 0
			pos.gain_loss_amt_est_low   = 0
			pos.gain_loss_amt_est_high  = 0
			pos.gain_loss_amt           = 0
			pos.gain_loss_amt_net       = 0

			pos.gain_loss_pct_est       = 0
			pos.gain_loss_pct_est_high  = 0
			pos.gain_loss_pct_est_low   = 0
			pos.gain_loss_pct           = 0

			db_tbl_poss_insupd(pos)

		func_end(fnc)

	#<=====>#

	def pos_upd(self, pos, mkt=None, so=None):
		func_name = 'pos_upd'
		func_str = f'{lib_name}.{func_name}(pos, mkt, so)'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
		G(func_str)

		pos.symb = 'USDC'
		self.pst = pair_settings_get(symb='USDC', prod_id = pos.prod_id)
		self.pst = AttrDictConv(in_dict=self.pst)
		prod_id    = pos.prod_id

		# Update Sell Sizing Info from Market
		if mkt:
			pos.base_size_incr   = mkt.base_size_incr
			pos.quote_size_incr  = mkt.quote_size_incr
			pos.quote_size_min   = mkt.quote_size_min
			pos.quote_size_max   = mkt.quote_size_max
			pos.base_size_min    = mkt.base_size_min
			pos.base_size_max    = mkt.base_size_max

		# Update Sell Price
		if so:
			pos.prc_curr         = so.prc_sell_act
		elif mkt:
			pos.prc_curr         = mkt.prc_sell
		else:
			print(func_str)
			print('we have neither so or mkt!!!')
			sys.exit()

		if pos.pos_stat not in ('OPEN'):
			print(f'pos.pos_stat : {pos.pos_stat}')

		# If we have a sell order we are closing the position
		if so:

			pos.pos_stat                              = 'CLOSE'
			pos.pos_end_dttm                          = so.sell_end_dttm
			pos.sell_order_cnt                        += 1
			pos.sell_order_attempt_cnt                += 1
			pos.hold_cnt                              -= so.sell_cnt_act
			pos.tot_in_cnt                            += so.tot_in_cnt
			pos.sell_cnt_tot                          += so.sell_cnt_act
			pos.fees_cnt_tot                          += so.fees_cnt_act
			pos.sell_fees_cnt_tot                     += so.fees_cnt_act
			pos.prc_sell_avg                          = round((pos.tot_in_cnt / pos.sell_cnt_tot), 8)

		if pos.pos_stat == 'SELL' and not so:
			print('pos_stat = SELL and no SO was given, so we cannot close the position...')
			beep()

		if pos.pos_stat not in ('OPEN'):
			print(f'pos.pos_stat : {pos.pos_stat}')

		# Update Sell Price Highs & Lows
		if pos.prc_curr > pos.prc_high: pos.prc_high = pos.prc_curr
		if pos.prc_curr < pos.prc_low: pos.prc_low = pos.prc_curr

		# Update Price Change %
		pos.prc_chg_pct = calc_chg_pct(old_val=pos.prc_buy, new_val=pos.prc_curr, dec_prec=4)
		# Update Price Change % Highs & Lows
		if pos.prc_chg_pct > pos.prc_chg_pct_high: pos.prc_chg_pct_high = pos.prc_chg_pct
		if pos.prc_chg_pct < pos.prc_chg_pct_low:  pos.prc_chg_pct_low  = pos.prc_chg_pct
		# Update Price Change Drop from Highest
		pos.prc_chg_pct_drop = round(pos.prc_chg_pct - pos.prc_chg_pct_high, 2)

		# Update Gain Loss Amt
		pos.val_curr          = pos.hold_cnt * pos.prc_curr
		pos.val_tot           = pos.val_curr + pos.tot_in_cnt

		# gain_loss_amt_est is to capture the pct at the time we decide to sell and should not be updated after
		if pos.pos_stat in ('OPEN'):
			pos.gain_loss_amt     = pos.val_tot - pos.tot_out_cnt
			pos.gain_loss_amt_est = pos.val_tot - pos.tot_out_cnt
			# Update Gain Loss % Highs & Lows
			if pos.gain_loss_amt_est > pos.gain_loss_amt_est_high: pos.gain_loss_amt_est_high = pos.gain_loss_amt_est
			if pos.gain_loss_amt_est < pos.gain_loss_amt_est_low:  pos.gain_loss_amt_est_low  = pos.gain_loss_amt_est
		elif pos.pos_stat in ('CLOSE'):
			pos.gain_loss_amt     = pos.val_tot - pos.tot_out_cnt
			pos.gain_loss_amt_net = pos.gain_loss_amt

		# gain_loss_pct_est is to capture the pct at the time we decide to sell and should not be updated after
		if pos.pos_stat in ('OPEN'):
			pos.gain_loss_pct      = calc_chg_pct(old_val=pos.tot_out_cnt, new_val=pos.val_tot, dec_prec=4)
			pos.gain_loss_pct_est  = pos.gain_loss_pct
			# Update Gain Loss % Highs & Lows
			if pos.gain_loss_pct_est > pos.gain_loss_pct_est_high: pos.gain_loss_pct_est_high = pos.gain_loss_pct_est
			if pos.gain_loss_pct_est < pos.gain_loss_pct_est_low:  pos.gain_loss_pct_est_low  = pos.gain_loss_pct_est
		elif pos.pos_stat in ('CLOSE'):
			# Need a Fix Here for CLOSE
			# Update Gain Loss %
			pos.gain_loss_pct = calc_chg_pct(old_val=pos.tot_out_cnt, new_val=pos.val_tot, dec_prec=4)

		# Finalize the Pocket & Clip Info
		if pos.pos_stat == 'CLOSE':
			if pos.prc_chg_pct > 0:
				pos.pocket_pct          = self.pst.sell.rainy_day.pocket_pct 
				pos.clip_pct            = self.pst.sell.rainy_day.clip_pct
				pos.pocket_cnt          = pos.hold_cnt
				pos.clip_cnt            = 0
			else:
				pos.pocket_pct          = self.pst.sell.rainy_day.pocket_pct
				pos.clip_pct            = self.pst.sell.rainy_day.clip_pct
				pos.pocket_cnt          = 0
				pos.clip_cnt            = pos.hold_cnt

		# Update to Database
		db_tbl_poss_insupd(pos)

		func_end(fnc)
		return pos

	#<=====>#

	def pos_close(self, pos_id, sell_order_uuid):
		func_name = 'pos_close'
		func_str = f'{lib_name}.{func_name}(pos_id={pos_id}, sell_order_uuid={sell_order_uuid})'
		fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#		G(func_str)

		pos = db_pos_get_by_pos_id(pos_id)
		pos = dec_2_float(pos)
		pos = AttrDictConv(in_dict=pos)

		so  = db_sell_ords_get_by_uuid(sell_order_uuid)
		so  = dec_2_float(so)
		so  = AttrDictConv(in_dict=so)

		pos = self.pos_upd(mkt=None, pos=pos, so=so)

		func_end(fnc)

#<=====>#
# Functions
#<=====>#

#<=====>#
# Post Variables
#<=====>#

bot = BOT()

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	bot.bot()

#<=====>#
