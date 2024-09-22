#<=====>#
# Import All Scope
#<=====>#

import_all_func_list = []
import_all_func_list.append("cb")
import_all_func_list.append("cb_bal_get")
import_all_func_list.append("cb_bid_ask_by_amt_get")
import_all_func_list.append("cb_bid_ask_get")
import_all_func_list.append("cb_candles_get")
import_all_func_list.append("cb_client_order_id")
import_all_func_list.append("cb_curr_shaper")
import_all_func_list.append("cb_mkt_prc_dec_calc")
import_all_func_list.append("cb_mkt_refresh")
import_all_func_list.append("cb_mkt_shaper")
import_all_func_list.append("cb_mkts_refresh")
import_all_func_list.append("cb_ord_get")
import_all_func_list.append("cb_ord_shaper")
import_all_func_list.append("cb_ords_refresh")
import_all_func_list.append("cb_wallet_refresh")
__all__ = import_all_func_list

#<=====>#
# Description
#<=====>#


#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Common Modules
#<=====>#
#from coinbase.rest import RESTClient as cbclient
from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient as cbclient

# from datetime import date
from datetime import datetime
from datetime import datetime as dt
# from datetime import timezone
# from datetime import tzinfo
# from datetime import timedelta
from dateutil import parser as dt_prsr
from pprint import pprint

# import ast
# import configparser
# import decimal
# import json
# import numpy as np
import sys
import os
import pandas as pd 
# import pandas_ta as pta 
import re
# import requests
# import schedule
# import sys
import time
# import traceback

import uuid

# import threading
# import time
# import json
# import os
# from datetime import datetime as dt
# from filelock import FileLock


#import warnings
#warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

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
from bot_db_read                   import *
from bot_db_write                  import *
from bot_secrets                   import secrets
from lib_colors                    import *

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_coinbase'
log_name      = 'bot_coinbase'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 2

#<=====>#
# Assignments Pre
#<=====>#

sc = secrets.settings_load()
#st = settings.settings_load()

cb = cbclient(api_key=sc.coinbase.api_key, api_secret=sc.coinbase.api_secret)

# # Initialize a lock for thread safety within the same process
# thread_lock = threading.Lock()

# # Path to the counter file and its lock
# counter_file = 'client_order_id_counter.txt'
# lock_file = 'client_order_id_counter.lock'

#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#



def cb_client_order_id():
	func_name = 'cb_client_order_id'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	client_order_id = str(uuid.uuid4())

	func_end(fnc)
	return client_order_id



# def cb_client_order_id():
# 	func_name = 'cb_client_order_id'
# 	func_str = f'{lib_name}.{func_name}()'
# #	G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

# 	# fix to prevent client _order_id from creating duplicates
# 	time.sleep(0.25)
# 	unixtime = int(dt.now().timestamp())
# 	# 1716634739
# #	client_order_id = mid(str(unixtime), 1, 8)
# 	client_order_id = unixtime - 1700000000
# 	client_order_id = str(client_order_id)


# 	func_end(fnc)
# 	return client_order_id


#chatgpt 01-mini's solution... 
#will repeat and overlap every 115 days 
# def load_state():
# 	if os.path.exists(state_file):
# 		with open(state_file, 'r') as f:
# 			return json.load(f)
# 	return {"last_time": 0, "counter": 0}
# def save_state(state):
# 	with open(state_file, 'w') as f:
# 		json.dump(state, f)
# def cb_client_order_id():
# 	func_name = 'cb_client_order_id'
# 	func_str = f'{lib_name}.{func_name}()'
# 	# G(func_str)
# 	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
# 	if lib_verbosity >= 2:
# 		print_func_name(func_str, adv=2)

# 	global cb_client_order_id_last_time
# 	global cb_client_order_id_counter

# 	with cb_client_order_id_lock:
# 		# Load the last state
# 		state = load_state()
# 		last_time = state["last_time"]
# 		counter = state["counter"]

# 		# Get current time in tenths of a second
# 		unixtime_tenths = int(time.time() * 10)

# 		if unixtime_tenths == last_time:
# 			counter += 1
# 			if counter >= 10:
# 				# If counter exceeds, wait for the next tenth of a second
# 				while unixtime_tenths == last_time:
# 					time.sleep(0.01)  # Sleep for 10ms
# 					unixtime_tenths = int(time.time() * 10)
# 				counter = 0
# 		else:
# 			last_time = unixtime_tenths
# 			counter = 0

# 		# Update the state
# 		state["last_time"] = last_time
# 		state["counter"] = counter
# 		save_state(state)

# 		# Generate 8-digit ID
# 		# Adjust the base subtraction to fit your specific epoch needs
# 		base_unixtime = 170000000  # Example base to keep the ID within 8 digits
# 		client_order_id_num = (unixtime_tenths - base_unixtime) * 10 + counter

# 		# Ensure it's 8 digits by taking the last 8 characters
# 		client_order_id = str(client_order_id_num).zfill(8)[-8:]

# 	func_end(fnc)
# 	return client_order_id

#<=====>#

# def cb_client_order_id():
#     func_name = 'cb_client_order_id'
#     func_str = f'{lib_name}.{func_name}()'
#     # G(func_str)
#     fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#     if lib_verbosity >= 2:
#         print_func_name(func_str, adv=2)

#     with thread_lock:
#         # Use FileLock for process-safe locking
#         with FileLock(lock_file):
#             # If the counter file does not exist, initialize it
#             if not os.path.exists(counter_file):
#                 with open(counter_file, 'w') as f:
#                     f.write('0')

#             # Read the current counter value
#             with open(counter_file, 'r') as f:
#                 try:
#                     counter = int(f.read().strip())
#                 except ValueError:
#                     counter = 0  # Reset counter if file is corrupted

#             # Increment the counter
#             counter += 1

#             # Ensure the counter wraps around if it exceeds 99,999,999
#             if counter > 99999999:
#                 counter = 1  # Reset to 1 or any other desired behavior

#             # Write the updated counter back to the file
#             with open(counter_file, 'w') as f:
#                 f.write(str(counter))

#     # Format the counter as an 8-digit string with leading zeros
#     client_order_id = str(counter).zfill(8)

#     func_end(fnc)
#     return client_order_id

#<=====>#

# Function to fetch current positions
def cb_bal_get(symb):
	func_name = 'cb_bal_get'
	func_str = f'{lib_name}.{func_name}(symb={symb})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	accts = []
	has_next = True
	cursor = None
	while has_next:
		if cursor:
			time.sleep(0.25)
			r = cb.get_accounts(limit=250, cursor=cursor)
		else:
			time.sleep(0.25)
			r = cb.get_accounts(limit=250)
		more_accts = r['accounts']
		accts.extend(more_accts)
		has_next = r['has_next']
		cursor = r['cursor']

	bal = 0
	for acct in accts:
		if acct['currency'] == symb:
			bal = float(acct['available_balance']['value'])

	func_end(fnc)
	return bal

#<=====>#

'''
coinbase.rest.products.get_best_bid_ask(self, 
	product_ids: List[str] | None = None, 
	**kwargs)→ Dict[str, Any][source]
Get Best Bid/Ask
[GET] https://api.coinbase.com/api/v3/brokerage/best_bid_ask
Description: Get the best bid/ask for all products. A subset of all products can be returned instead by using the product_ids input.
Read more on the official documentation: Get Best Bid/Ask
https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getproductbook

product_ids (str or list of str) List of product IDs to return.
	None or 'BTC-USD' or ['BTC-USD','ETH-USD']

'''

def cb_bid_ask_by_amt_get(mkt, buy_sell_size):
	func_name = 'cb_bid_ask_by_amt_get'
	func_str = f'{lib_name}.{func_name}(mkt, buy_sell_size={buy_sell_size})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	prod_id = mkt.prod_id
	bid_prc = mkt.prc
	ask_prc = mkt.prc

	try:

		bid_prc, ask_prc = cb_bid_ask_get(prod_id)
		cum_bids_size = 0
		cum_asks_size = 0

		limit = 60
		max_attempts = 3
		attempts = 0
		r = None
		while r == None:
			try:
				attempts += 1
				time.sleep(0.25)
				r = cb.get_product_book(product_id=prod_id, limit=limit)
				bids = r['pricebook']['bids']
				asks = r['pricebook']['asks']
#			except Exception as e:
			except Exception:
#				traceback.print_exc()
#				print(type(e))
#				print(e)
#				print(dttm_get())
				if attempts >= 3:
					print(f'errored => cb.get_product_book(product_id={prod_id}, limit={limit})')
					print(f'attempt {attempts} of {max_attempts}, sleeping 1 seconds and then retrying')
				time.sleep(1)
#				break

#		pprint(r)
#		https://api.coinbase.com/api/v3/brokerage/product_book
#		{
#			'pricebook': {
#				'asks': [
#					{'price': '3.1597', 'size': '62.38'},
#					{'price': '3.1598', 'size': '1330.2'},
#					{'price': '3.16', 'size': '1520.5'},
#					{'price': '3.166', 'size': '13.53'},
#					{'price': '3.1661', 'size': '0.47'},
#					{'price': '3.1667', 'size': '1.5'},
#					{'price': '3.1682', 'size': '0.03'},
#					{'price': '3.1683', 'size': '0.03'},
#					{'price': '3.1684', 'size': '0.03'},
#					{'price': '3.1685', 'size': '0.03'},
#					...
#					],
#				'bids': [
#					{'price': '3.1284', 'size': '0.47'},
#					{'price': '3.1283', 'size': '0.03'},
#					{'price': '3.1282', 'size': '0.03'},
#					{'price': '3.1281', 'size': '0.03'},
#					{'price': '3.128', 'size': '0.03'},
#					{'price': '3.1279', 'size': '0.03'},
#					{'price': '3.1278', 'size': '0.03'},
#					{'price': '3.1277', 'size': '0.03'},
#					{'price': '3.1276', 'size': '62.74'},
#					{'price': '3.1275', 'size': '0.03'},
#					...
#					],
#				'product_id': 'BIT-USDC',
#				'time': '2024-07-12T14:07:16.804930Z'
#				}
#			}

		# if I believed that all the micro amounts before my target size 
		# might not be consumed before me, I would do a weighted average price
		for bid in bids:
			this_bid_size  = float(bid['size'])
			this_bid_prc   = float(bid['price'])
			cum_bids_size += this_bid_size
#			print(f"cum_bids_size : {cum_bids_size}, this_bid_size : {this_bid_size}', this_bid_prc : {this_bid_prc}")
			if cum_bids_size > buy_sell_size:
				bid_prc = this_bid_prc
				break

		for ask in asks:
			this_ask_size  = float(bid['size'])
			this_ask_prc   = float(ask['price'])
			cum_asks_size += this_ask_size
#			print(f"cum_asks_size : {cum_asks_size}, this_ask_size : {this_ask_size}', this_ask_prc : {this_ask_prc}")
			if cum_asks_size > buy_sell_size:
				ask_prc = this_ask_prc
				break

#		print(f'{prod_id} ==> bid : {bid_prc:>.8f}, ask : {ask_prc:>.8f}, buy_sell_size : {buy_sell_size:>.8f}')

	except Exception as e:
		print(f'{dttm_get()} {func_name} - Market Summary ==> {prod_id} = Error : ({type(e)}){e}')
		traceback.print_exc()
#		beep(3)
		pass

	func_end(fnc)
	return bid_prc, ask_prc

#<=====>#

def cb_bid_ask_get(prod_id):
	func_name = 'cb_bid_ask_get'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	r = cb.get_best_bid_ask([prod_id])
	bid_prc = float(r['pricebooks'][0]['bids'][0]['price'])
	ask_prc = float(r['pricebooks'][0]['asks'][0]['price'])

	func_end(fnc)
	return bid_prc, ask_prc

#<=====>#

'''
Market Data
coinbase.rest.market_data.get_candles(self, 
	product_id: str, 
	start: str, 
	end: str, 
	granularity: str, 
	**kwargs)→ Dict[str, Any][source]
Get Product Candles
[GET] https://api.coinbase.com/api/v3/brokerage/products/{product_id}/candles
Description: Get rates for a single product by product ID, grouped in buckets.
Read more on the official documentation: Get Product Candles
https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getcandles

* product_id (str) The trading pair to get information for.
	example : 'BTC-USD'
* start (str/int?) Timestamp for starting range of aggregations, in UNIX time.
* end (str/int?) Timestamp for ending range of aggregations, in UNIX time.
* granularity (str) The time slice value for each candle.
	None, 'UNKNOWN_GRANULARITY', 'ONE_MINUTE', 'FIVE_MINUTE', 'FIFTEEN_MINUTE', 'THIRTY_MINUTE'
	'ONE_HOUR', 'TWO_HOUR', 'SIX_HOUR', 'ONE_DAY'
'''
def cb_candles_get(product_id, start = None, end = None, rfreq = None, granularity = None, min_rows = 299):
	func_name = 'cb_candles_get'
	func_str = f'{lib_name}.{func_name}(product_id : {product_id}, start : {start}, end : {end}, rfreq : {rfreq}, min_rows : {min_rows})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	secs = 0
	now = int(round(datetime.now().timestamp()))

	# cb has a limit or max 300 rows
	req_rows_max = 300

	# defaults
	granularity = 'ONE_MINUTE'
	secs = 60 * 1
	req_span = req_rows_max * secs

	rfreq_mult = 1
	rfreq_base = 'minute'
	# Regular expression pattern
	re_pattern = re.compile(r'(\d+)([a-zA-Z]+)')
	match = re_pattern.match(rfreq)
	if match:
		rfreq_mult = int(match.group(1))
		rfreq_base = match.group(2)

	if rfreq_base in ('min','T'): rfreq_base = 'minute'
	if rfreq_base in ('H','h'):   rfreq_base = 'hour'
	if rfreq_base in ('D','d'):   rfreq_base = 'day'
	if rfreq_base in ('W','w'):   rfreq_base = 'week'
	if rfreq_base in ('M'):       rfreq_base = 'month'

	if rfreq_base == 'minute':
		if rfreq_mult % 60 == 0:
			granularity  = 'ONE_HOUR'
			req_secs     = 60 * 60
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 30 == 0:
			granularity  = 'THIRTY_MINUTE'
			req_secs     = 60 * 30
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 15 == 0:
			granularity  = 'FIFTEEN_MINUTE'
			req_secs     = 60 * 15
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 5 == 0:
			granularity  = 'FIVE_MINUTE'
			req_secs     = 60 * 5
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs
		else:
			granularity  = 'ONE_MINUTE'
			req_secs     = 60 * 1
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs

	elif rfreq_base == 'hour':
		if rfreq_mult % 24 == 0:
			granularity  = 'ONE_DAY'
			req_secs     = 24 * 60 * 60
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 6 == 0:
			granularity  = 'SIX_HOUR'
			req_secs     = 6 * 60 * 60
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 2 == 0:
			granularity  = 'TWO_HOUR'
			req_secs     = 2 * 60 * 60
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs
		else:
			granularity  = 'ONE_HOUR'
			req_secs     = 1 * 60 * 60
			# rfreq_secs    = req_secs * rfreq_mult
			req_span     = req_rows_max * req_secs

	elif rfreq_base == 'day':
		granularity  = 'ONE_DAY'
		req_secs     = 24 * 60 * 60
		# rfreq_secs   = req_secs * rfreq_mult
		req_span     = req_rows_max * req_secs

	elif rfreq_base == 'week':
		granularity  = 'ONE_DAY'
		req_secs     = 24 * 60 * 60
		# rfreq_secs   = req_secs * rfreq_mult
		req_span     = req_rows_max * req_secs

	elif rfreq_base == 'month':
		granularity  = 'ONE_DAY'
		req_secs     = 24 * 60 * 60
		# rfreq_secs    = req_secs * rfreq_mult
		req_span     = req_rows_max * req_secs

	mode = None
	if start and end and min_rows:
		mode = 'both'
	elif start and end:
		mode = 'range'
	elif min_rows:
		mode = 'rows'

	temp_end = now
	if end: temp_end = end

	# dropping seconds from time
#	print('temp_end     2A : {}'.format(datetime.fromtimestamp(temp_end)))
	temp_end = temp_end - temp_end % 60 + req_secs
#	print('temp_end     2B : {}'.format(datetime.fromtimestamp(temp_end)))

#	# aligning?
#	print('temp_end   3A : {}'.format(datetime.fromtimestamp(temp_end)))
#	temp_end = temp_end - temp_end % secs + secs
#	print('temp_end   3B : {}'.format(datetime.fromtimestamp(temp_end)))
#	temp_start        = temp_end - req_span + secs
#	est_rows = (temp_end - temp_start) / secs
#	print('est_rows   3C : {}'.format(est_rows))

	ohlcv            = []
	row_cnt          = 0
	# last_row_cnt     = 0
	enough_tf        = False

	df = None

	req_cnt = 0
	while not enough_tf:

		temp_start        = temp_end - req_span

#		m = 'product_id : {}, rfreq_mult : {}, rfreq_base : {}, rfreq_secs : {}, granularity : {}, min_rows : {}, row_cnt : {}, now : {}, req_span : {}, temp_start : {}, temp_end : {}, temp_start : {}, temp_end : {}'
#		msg = m.format(product_id, rfreq_mult, rfreq_base, rfreq_secs, granularity, min_rows, row_cnt, now, req_span, temp_start, temp_end, datetime.fromtimestamp(temp_start), datetime.fromtimestamp(temp_end))
#		print(msg)

		est_rows = (temp_end - temp_start) / req_secs
#		print('temp_start   4A : {} {}'.format(temp_start, datetime.fromtimestamp(temp_start)))
#		print('temp_end     4A : {} {}'.format(temp_start, datetime.fromtimestamp(temp_end)))
#		print('est_rows     4A : {}'.format(est_rows))
		if est_rows >= 300:
			fix_rows = est_rows - 300
			fix_secs = fix_rows * secs
			temp_start += fix_secs
			temp_start = int(temp_start)
			est_rows = (temp_end - temp_start) / secs + 1
#			print('temp_start   4B : {} {}'.format(temp_start, datetime.fromtimestamp(temp_start)))
#			print('temp_end     4B : {} {}'.format(temp_start, datetime.fromtimestamp(temp_end)))
#			print('est_rows     4A : {}'.format(est_rows))

		# temp_start_str    = str(temp_start)
		# temp_end_str      = str(temp_end)

		req_cnt += 1

#		print('temp_start   5 : {}'.format(datetime.fromtimestamp(temp_start)))
#		print('temp_end     5 : {}'.format(datetime.fromtimestamp(temp_end)))

		r = None
		attempts = 0
		max_attempts = 10
		candles = None
		while r == None:
			try:
				attempts += 1
				time.sleep(0.25)
				r = cb.get_candles(product_id, temp_start, temp_end, granularity)
				candles = r['candles']
#			except Exception as e:
			except Exception:
#				traceback.print_exc()
#				print(type(e))
#				print(e)
#				print(dttm_get())
				if attempts <= max_attempts:
					print(f'errored => cb.get_candles(product_id={product_id}, temp_start={temp_start}, temp_end={temp_end}, granularity={granularity})')
					print(f'attempt {attempts} of {max_attempts}, sleeping 1 seconds and then retrying')
					time.sleep(1)
				else:
					print(f'attempt {attempts} of {max_attempts}, failed to get candles, exiting...')
					func_end(fnc)
					df = pd.DataFrame
					return df

		no_more_candles = False
		if not candles:
			no_more_candles = True
		for x in candles:
#			print(x)
			for k in x:
				if k == 'start':
					x[k] = int(x[k])
				else:
					x[k] = float(x[k])
			x['timestamp'] = x['start']
			ohlcv.append(x)

		df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
		df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
		df.set_index('timestamp', inplace=True)

		d = {
				"open": "first", 
				"high": "max", 
				"low": "min", 
				"close": "last", 
				"volume": "sum"
			}

		roffset = None
		if roffset:
			df = df.resample(rfreq, offset=roffset).agg(d)
		else:
			df = df.resample(rfreq).agg(d)
		df.dropna()

		row_cnt = len(df)
		if mode == 'both':
			if temp_start <= start and row_cnt >= min_rows:
				enough_tf = True
			if no_more_candles:
				print(f'found no more {rfreq} candles, returning {len(df)} candles... ')
				enough_tf = True
		elif mode == 'range':
			if temp_start <= start:
				enough_tf = True
			if no_more_candles:
				print(f'found no more {rfreq} candles, returning {len(df)} candles... ')
				enough_tf = True
		elif mode == 'rows':
			if row_cnt >= min_rows:
				enough_tf = True
			if no_more_candles:
				print(f'found no more {rfreq} candles, returning {len(df)} candles... ')
				enough_tf = True

		temp_start        = temp_start - req_span
		temp_end          = temp_end   - req_span
		# last_row_cnt      = row_cnt

	func_end(fnc)
	return df

#<=====>#

def cb_curr_shaper(in_acct):
	func_name = 'cb_curr_shaper'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

#	{
#	'uuid': '96926e6f-cebd-5bca-aac7-023db531f19d',
#	'name': 'BTC Wallet',
#	'currency': 'BTC',
#	'available_balance': {
#		'value': '0.0130339181944456',
#		'currency': 'BTC'
#		},
#	'default': True,
#	'active': True,
#	'created_at': '2018-11-15T13:09:35.716Z', 
#	'updated_at': '2024-05-04T20:29:31.748Z', 
#	'deleted_at': None, 
#	'type': 'ACCOUNT_TYPE_CRYPTO', 
#	'ready': True, 
#	'hold': {
#		'value': '0', 
#		'currency': 'BTC'
#		}, 
#	'retail_portfolio_id': '2b69eba6-6232-57fa-84cf-578586216e3d'
#	}

	out_curr = AttrDict()
	out_curr.curr_uuid            = in_acct['uuid']
	out_curr.symb                 = in_acct['currency']
	out_curr.name                 = in_acct['currency']
	out_curr.bal_avail            = float(in_acct['available_balance']['value'])
	out_curr.bal_hold             = float(in_acct['hold']['value'])
	out_curr.bal_tot              = out_curr.bal_avail + out_curr.bal_hold

	out_curr.create_dttm          = dt_prsr.parser(in_acct['created_at'])
	out_curr.update_dttm          = dt_prsr.parser(in_acct['updated_at'])
	out_curr.delete_dttm          = dt_prsr.parser(in_acct['deleted_at'])

	out_curr.create_dttm          = None
	out_curr.update_dttm          = None
	out_curr.delete_dttm          = None

	if in_acct['created_at']:
		out_curr.create_dttm          = datetime.strptime(in_acct['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
	if in_acct['updated_at']:
		try:
			out_curr.update_dttm          = datetime.strptime(in_acct['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
		except:
			pass
	if in_acct['deleted_at']:
		out_curr.delete_dttm          = datetime.strptime(in_acct['deleted_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

	out_curr.rp_id                = in_acct['retail_portfolio_id']
	out_curr.default_tf           = in_acct['default']
	out_curr.ready_tf             = in_acct['ready']
	out_curr.active_tf            = in_acct['active']

	func_end(fnc)
	return out_curr

#<=====>#

def cb_mkt_prc_dec_calc(bid_prc, ask_prc):
	func_name = 'cb_mkt_prc_dec_calc'
	func_str = f'{lib_name}.{func_name}(bid_prc={bid_prc:>.8f}, ask_prc={ask_prc:>.8f})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	prc_dec = 0

	for prc in (bid_prc, ask_prc):
		dec_str = str(prc).split('.')[1] if '.' in str(prc) else ''
		dec_str = dec_str.rstrip('0')
		if len(dec_str) > prc_dec:
			prc_dec = len(dec_str)

#		print(f'prc_dec   ({type(prc_dec)}): {prc_dec}')

	func_end(fnc)
	return prc_dec

#<=====>#

def cb_mkt_refresh(prod_id, stable_coins=None):
	func_name = 'cb_mkt_refresh'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	t0 = time.perf_counter()

	# prods = []
	time.sleep(0.25)

	r = cb.get_product(product_id=prod_id)

	add_tf = False
	prod = r
	if not prod['view_only']:
		if not prod['is_disabled']:
			if prod['status'] == 'online':
				if not prod['trading_disabled']:
					add_tf = True
	if add_tf:
		mkt = cb_mkt_shaper(prod)

	db_tbl_mkts_insupd(mkt)
	db_currs_prc_mkt_upd()

	if stable_coins:
		if isinstance(stable_coins, str):
			temp = []
			temp.append(stable_coins)
			stable_coins = temp
		if isinstance(stable_coins, list):
			db_currs_prc_stable_upd(stable_symbs=stable_coins)

	db_currs_prc_mkt_upd()
	db_bals_prc_mkt_upd()

	t1 = time.perf_counter()
	elapsed_seconds = round(t1 - t0, 2)
	if elapsed_seconds >= 5:
		print(f'{func_str} in {elapsed_seconds} seconds...')

	func_end(fnc)
	return mkt

#<=====>#

def cb_mkt_shaper(in_mkt):
	func_name = 'cb_mkt_shaper'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

#	{
#	'product_id': 'BTC-USDC',
#	'price': '63404.17',
#	'price_percentage_change_24h': '0.40006954701961',
#	'volume_24h': '6066.37287309',
#	'volume_percentage_change_24h': '-61.01527052620745',
#	'base_increment': '0.00000001',
#	'quote_increment': '0.01',
#	'quote_min_size': '1',
#	'quote_max_size': '150000000',
#	'base_min_size': '0.00000001',
#	'base_max_size': '3400',
#	'base_name': 'Bitcoin',
#	'quote_name': 'USDC',
#	'watched': False,
#	'is_disabled': False,
#	'new': False,
#	'status': 'online',
#	'cancel_only': False,
#	'limit_only': False,
#	'post_only': False,
#	'trading_disabled': False,
#	'auction_mode': False,
#	'product_type': 'SPOT',
#	'quote_currency_id': 'USDC',
#	'base_currency_id': 'BTC',
#	'fcm_trading_session_details': None,
#	'mid_market_price': '',
#	'alias': 'BTC-USD',
#	'alias_to': [],
#	'base_display_symbol': 'BTC',
#	'quote_display_symbol': 'USD',
#	'view_only': False,
#	'price_increment': '0.01',
#	'display_name': 'BTC-USDC',
#	'product_venue': 'CBE',
#	'approximate_quote_24h_volume': '384633336.93'
#	}

	out_mkt = AttrDict()

	try:
		out_mkt.mkt_name                            = in_mkt['product_id']
		out_mkt.prod_id                             = in_mkt['product_id']
		out_mkt.mkt_venue                           = in_mkt['product_venue']

		out_mkt.base_curr_name                      = in_mkt['base_name']
		out_mkt.base_curr_symb                      = in_mkt['base_display_symbol']
#		out_mkt.base_curr_id                        = in_mkt['base_currency_id']
		out_mkt.base_size_incr                      = float(in_mkt['base_increment'])
		out_mkt.base_size_min                       = float(in_mkt['base_min_size'])
		out_mkt.base_size_max                       = float(in_mkt['base_max_size'])

		out_mkt.quote_curr_name                     = in_mkt['quote_name']
		out_mkt.quote_curr_symb                     = in_mkt['quote_name']
#		out_mkt.quote_curr_id                       = in_mkt['quote_currency_id']
		out_mkt.quote_size_incr                     = float(in_mkt['quote_increment'])
		out_mkt.quote_size_min                      = float(in_mkt['quote_min_size'])
		out_mkt.quote_size_max                      = float(in_mkt['quote_max_size'])

		out_mkt.mkt_status_tf                       = in_mkt['status']
		out_mkt.mkt_view_only_tf                    = in_mkt['view_only']
		out_mkt.mkt_watched_tf                      = in_mkt['watched']
		out_mkt.mkt_is_disabled_tf                  = in_mkt['is_disabled']
		out_mkt.mkt_new_tf                          = in_mkt['new']
		out_mkt.mkt_cancel_only_tf                  = in_mkt['cancel_only']
		out_mkt.mkt_limit_only_tf                   = in_mkt['limit_only']
		out_mkt.mkt_post_only_tf                    = in_mkt['post_only']
		out_mkt.mkt_trading_disabled_tf             = in_mkt['trading_disabled']
		out_mkt.mkt_auction_mode_tf                 = in_mkt['auction_mode']

		if in_mkt['price'] == '':
			out_mkt.prc                             = -1
		else:
			out_mkt.prc                             = float(in_mkt['price'])

		if in_mkt['mid_market_price'] == '':
			out_mkt.prc_mid_mkt                     = None
		else:
			out_mkt.prc_mid_mkt                     = float(in_mkt['mid_market_price'])

		if in_mkt['price_percentage_change_24h'] == '':
			out_mkt.prc_pct_chg_24h                 = None
		else:
			out_mkt.prc_pct_chg_24h                 = float(in_mkt['price_percentage_change_24h'])

		if in_mkt['volume_24h'] == '':
			out_mkt.vol_24h                         = None
		else:
			out_mkt.vol_24h                         = float(in_mkt['volume_24h'])

		if in_mkt['volume_24h'] == '':
			out_mkt.vol_base_24h                    = None
		else:
			out_mkt.vol_base_24h                    = float(in_mkt['volume_24h'])

		if in_mkt['approximate_quote_24h_volume'] == '':
			out_mkt.vol_quote_24h                   = None
		else:
			out_mkt.vol_quote_24h                   = float(in_mkt['approximate_quote_24h_volume'])

		if in_mkt['volume_percentage_change_24h'] == '':
			out_mkt.vol_pct_chg_24h                 = None
		else:
			out_mkt.vol_pct_chg_24h                 = float(in_mkt['volume_percentage_change_24h'])

	except Exception as e:
		print(f'{out_mkt.prod_id} cb_mkt_shaper errored : {e}')
		pprint(in_mkt)
		pass

	func_end(fnc)
	return out_mkt

#<=====>#

def cb_mkts_refresh(stable_coins=None):
	func_name = 'cb_mkts_refresh'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=2)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	t0 = time.perf_counter()

	# prods = []
	time.sleep(0.25)
	r = cb.get_products()

	all_mkts = []
	for prod in r['products']:
#		print(prod)
		add_tf = False
		if not prod['view_only']:
			if not prod['is_disabled']:
				if prod['status'] == 'online':
					if not prod['trading_disabled']:
						add_tf = True
		if add_tf:
			mkt = cb_mkt_shaper(prod)
			all_mkts.append(mkt)

	db_tbl_mkts_insupd(all_mkts)

	db_currs_prc_mkt_upd()
	db_bals_prc_mkt_upd()

	if stable_coins:
		if isinstance(stable_coins, str):
			temp = []
			temp.append(stable_coins)
			stable_coins = temp
		if isinstance(stable_coins, list):
			db_currs_prc_stable_upd(stable_symbs=stable_coins)

	db_currs_prc_mkt_upd()
	db_bals_prc_mkt_upd()

	t1 = time.perf_counter()
	elapsed_seconds = round(t1 - t0, 2)
	if elapsed_seconds >= 5:
		print(f'{func_str} in {elapsed_seconds} seconds...')

	func_end(fnc)

#<=====>#

# Function to fetch current positions
def cb_ord_get(order_id):
	func_name = 'cb_ord_get'
	func_str = f'{lib_name}.{func_name}(order_id={order_id})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1.5)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	o = None
	time.sleep(0.25)
	r = cb.get_order(order_id=order_id)
	if r:
		if 'order' in r:
			if r['order']:
				o = r['order']

	if o:
		o = cb_ord_shaper(o)
		db_tbl_ords_insupd(o)

	func_end(fnc)
	return o

#<=====>#

def cb_ord_shaper(in_ord):
	func_name = 'cb_ord_shaper'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

#	pprint(in_ord)

#	{
#	'order_id': 'bc5202fd-4c0b-4de0-a40a-6a450b3a8594',
#	'product_id': 'BTC-USD',
#	'user_id': '2b69eba6-6232-57fa-84cf-578586216e3d',
#	'order_configuration': {
#		'limit_limit_gtc': {
#			'base_size': '0.00048264',
#			'limit_price': '51279.56',
#			'post_only': False
#		}
#	},
#	'side': 'BUY',
#	'client_order_id': 'c09e846a-2187-410d-a524-1d800642277b',
#	'status': 'FILLED',
#	'time_in_force': 'GOOD_UNTIL_CANCELLED',
#	'created_time': '2024-02-14T11:24:43.833332Z', 
#	'completion_percentage': '100.00', 
#	'filled_size': '0.00048264', 
#	'average_filled_price': '51279.56', 
#	'fee': '', 
#	'number_of_fills': '1', 
#	'filled_value': '24.7495668384', 
#	'pending_cancel': False, 
#	'size_in_quote': False, 
#	'total_fees': '0.1484974010304', 
#	'size_inclusive_of_fees': False, 
#	'total_value_after_fees': '24.8980642394304', 
#	'trigger_status': 'INVALID_ORDER_TYPE', 
#	'order_type': 'LIMIT', 
#	'reject_reason': 'REJECT_REASON_UNSPECIFIED', 
#	'settled': True, 
#	'product_type': 'SPOT', 
#	'reject_message': '', 
#	'cancel_message': '', 
#	'order_placement_source': 'RETAIL_ADVANCED', 
#	'outstanding_hold_amount': '0', 
#	'is_liquidation': False, 
#	'last_fill_time': '2024-02-14T16:20:39.630553Z', 
#	'edit_history': [], 
#	'leverage': '', 
#	'margin_type': 'UNKNOWN_MARGIN_TYPE', 
#	'retail_portfolio_id': '2b69eba6-6232-57fa-84cf-578586216e3d'
#	}

#	print(in_ord)

	# fix
	# column : ord_limit_prc not defined in table ords...
	# column : ord_stop_dir not defined in table ords...
	# column : ord_stop_price not defined in table ords...
	# column : ord_stop_trigger_price not defined in table ords...
	# column : sell_fees_curr_symb not defined in table poss...

	out_ord = AttrDict()

	out_ord.ord_uuid                    = in_ord['order_id']

	out_ord.prod_id                     = in_ord['product_id']
	out_ord.ord_bs                      = in_ord['side'].lower()

	# : {'limit_limit_gtc': {'base_size': '0.00048264', 'limit_price': '51279.56', 'post_only': False}},		out_ord.ord_type                          = None
	# ord_cfg                             = str(in_ord['order_configuration']).replace("'","")

	out_ord.ord_base_size               = None
	out_ord.ord_end_time                = None
	out_ord.ord_limit_prc               = None
	out_ord.ord_post_only               = None
	out_ord.ord_quote_size              = None
	out_ord.ord_stop_dir                = None
	out_ord.ord_stop_prc                = None
	out_ord.ord_stop_trigger_prc        = None

	for x  in in_ord['order_configuration']:
		ord_type                        = x
		ord_body                        = in_ord['order_configuration'][x]
		out_ord.ord_type                = ord_type

	# fix base_price not poppulating on sell mrkt
	if 'base_price' in ord_body:        out_ord.ord_base_size              = float(ord_body['base_size'])
	if 'quote_size' in ord_body:        out_ord.ord_quote_size             = float(ord_body['quote_size'])
	if 'limit_price' in ord_body:       out_ord.ord_limit_prc            = float(ord_body['limit_price'])
	if 'stop_direction' in ord_body:    out_ord.ord_stop_dir         = ord_body['stop_direction']
	if 'stop_price' in ord_body:        out_ord.ord_stop_prc             = float(ord_body['stop_price'])
	if 'stop_trigger_price' in ord_body:out_ord.ord_stop_trigger_prc     = float(ord_body['stop_trigger_price']   )
	if 'post_only' in ord_body:         out_ord.ord_post_only              = ord_body['post_only']
	if 'end_time' in ord_body:          out_ord.ord_end_time               = int(ord_body['end_time'])

	out_ord.order_id                    = in_ord['order_id']
	out_ord.ord_product_id              = in_ord['product_id']
	out_ord.ord_user_id                 = in_ord['user_id']
	out_ord.ord_order_configuration     = str(in_ord['order_configuration']).replace("'","")
	out_ord.ord_side                    = in_ord['side']
	out_ord.ord_client_order_id         = in_ord['client_order_id']
	out_ord.ord_status                  = in_ord['status']
	out_ord.ord_time_in_force           = in_ord['time_in_force']

	out_ord.ord_created_time            = dt_prsr.parser()
	if in_ord['created_time']:
		out_ord.ord_created_time        = datetime.strptime(in_ord['created_time'], "%Y-%m-%dT%H:%M:%S.%fZ")

	out_ord.ord_completion_percentage   = float(in_ord['completion_percentage'])
	out_ord.ord_filled_size             = float(in_ord['filled_size'])
	out_ord.ord_average_filled_price    = float(in_ord['average_filled_price'])
	if in_ord['fee'] != '':
		out_ord.ord_fee                 = in_ord['fee']
	else:
		out_ord.ord_fee                 = None
	out_ord.ord_number_of_fills         = int(in_ord['number_of_fills'])
	out_ord.ord_filled_value            = float(in_ord['filled_value'])
	out_ord.ord_pending_cancel          = in_ord['pending_cancel']
	out_ord.ord_size_in_quote           = in_ord['size_in_quote']
	out_ord.ord_total_fees              = float(in_ord['total_fees'])
	out_ord.ord_size_inclusive_of_fees  = in_ord['size_inclusive_of_fees']
	out_ord.ord_total_value_after_fees  = float(in_ord['total_value_after_fees'])
	out_ord.ord_trigger_status          = in_ord['trigger_status']
	out_ord.ord_order_type              = in_ord['order_type']
	out_ord.ord_reject_reason           = in_ord['reject_reason']
	out_ord.ord_settled                 = in_ord['settled']
	out_ord.ord_product_type            = in_ord['product_type']
	out_ord.ord_reject_message          = in_ord['reject_message']
	out_ord.ord_cancel_message          = in_ord['cancel_message']
	out_ord.ord_order_placement_source  = in_ord['order_placement_source']
	out_ord.ord_outstanding_hold_amount = float(in_ord['outstanding_hold_amount'])
	out_ord.ord_is_liquidation          = in_ord['is_liquidation']

	out_ord.ord_last_fill_time          = None
	if in_ord['last_fill_time']:
		out_ord.ord_last_fill_time      = datetime.fromisoformat(in_ord['last_fill_time'])

	out_ord.ord_edit_history            = ', '.join(in_ord['edit_history']).replace("'","")
	if in_ord['leverage'] != '':
		out_ord.ord_leverage            = in_ord['leverage']
	else:
		out_ord.ord_leverage            = None
	out_ord.ord_margin_type             = in_ord['margin_type']
	out_ord.ord_retail_portfolio_id     = in_ord['retail_portfolio_id']

	func_end(fnc)
	return out_ord

#<=====>#

# Function to fetch current positions
def cb_ords_refresh(loop_mkts, all_tf=False):
	func_name = 'cb_ords_refresh'
	func_str = f'{lib_name}.{func_name}(loop_mkts, all_tf={all_tf})'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	t0 = time.perf_counter()

	all_ords = []

	for prod_id in loop_mkts:

		limit = 10
		ords = []
		has_next = True
		cursor = None
		while (has_next or all_tf):
			# t00 = time.perf_counter()
			if cursor:
				time.sleep(0.25)
				r = cb.list_orders(product_id=prod_id, limit=limit, cursor=cursor)
			else:
				time.sleep(0.25)
				r = cb.list_orders(product_id=prod_id, limit=limit)
			t01 = time.perf_counter()
			elapsed_seconds = round(t01 - t01, 2)
			print(f'{prod_id} in {elapsed_seconds} seconds...')

			more_ords = r['orders']
			ords.extend(more_ords)
			cursor = r['cursor']
			has_next = r['has_next']
			if all_tf and not has_next:
				break
			elif not all_tf and len(ords) >= limit:
				break

		for o in ords:
			o = cb_ord_shaper(o)
			all_ords.append(o)

	db_tbl_ords_insupd(all_ords)

	t1 = time.perf_counter()
	elapsed_seconds = round(t1 - t0, 2)
	if elapsed_seconds >= 5:
		print(f'{func_str} in {elapsed_seconds} seconds...')

	func_end(fnc)

#<=====>#

# Function to fetch current positions
def cb_wallet_refresh():
	func_name = 'cb_wallet_refresh'
	func_str = f'{lib_name}.{func_name}()'
#	G(func_str)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=1.5)
	if lib_verbosity >= 2: print_func_name(func_str, adv=2)

	t0 = time.perf_counter()

	accts = []
	has_next = True
	cursor = None
	while has_next:
		if cursor:
			time.sleep(0.25)
			r = cb.get_accounts(limit=250, cursor=cursor)
		else:
			time.sleep(0.25)
			r = cb.get_accounts(limit=250)
		more_accts = r['accounts']
		accts.extend(more_accts)
		has_next = r['has_next']
		cursor = r['cursor']

	all_currs = []
	all_bals  = []
	for acct in accts:
		curr = cb_curr_shaper(acct)
		if (acct['active'] and float(acct['available_balance']['value']) > 0):
			all_bals.append(curr)
		all_currs.append(curr)

	db_tbl_bals_insupd(all_bals)
	db_tbl_currs_insupd(all_currs)

	db_currs_prc_mkt_upd()
	db_bals_prc_mkt_upd()

	t1 = time.perf_counter()
	elapsed_seconds = round(t1 - t0, 2)
	if elapsed_seconds >= 5:
		print(f'{func_str} in {elapsed_seconds} seconds...')

	func_end(fnc)

#<=====>#

def test_main():
	r = cb.fiat_limit_sell("BTC-USDC", "11", price_multiplier="1.1")
	print(r)

#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	test_main()

#<=====>#
