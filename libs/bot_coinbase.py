#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import os
import re
import traceback
import uuid
#from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient as cbclient
from coinbase.rest import RESTClient
from datetime import datetime
from dateutil import parser as dt_prsr
from dotenv import load_dotenv
from libs.bot_db_read import db_bals_get
from libs.bot_db_write import (
    db_bals_prc_mkt_upd, db_currs_prc_mkt_upd, db_currs_prc_stable_upd, db_tbl_bals_insupd, 
    db_tbl_currs_insupd, db_tbl_mkts_insupd, db_tbl_ords_insupd
)
from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
from libs.cls_settings import AttrDict
from libs.lib_common import dttm_get, func_begin, func_end, beep
from pprint import pprint
import pandas as pd
import time
from libs.lib_colors import G


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_coinbase'
log_name      = 'bot_coinbase'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 2


# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)


# Load environment variables from .env file
load_dotenv()
# Access environment variables
coinbase_api_key    = os.getenv('COINBASE_API_KEY')
coinbase_api_secret = os.getenv('COINBASE_API_SECRET')

cb = RESTClient(api_key=coinbase_api_key, api_secret=coinbase_api_secret)


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

def cb_client_order_id():
	func_name = 'cb_client_order_id'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	client_order_id = str(uuid.uuid4())

	func_end(fnc)
	return client_order_id

#<=====>#

# Function to fetch current positions
def cb_bal_get(symb):
	func_name = 'cb_bal_get'
	func_str = f'{lib_name}.{func_name}(symb={symb})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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

def cb_bid_ask_by_amt_get(pair, buy_sell_size):
	func_name = 'cb_bid_ask_by_amt_get'
	func_str = f'{lib_name}.{func_name}(mkt, buy_sell_size={buy_sell_size})'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prod_id = pair.prod_id
	bid_prc = pair.prc
	ask_prc = pair.prc

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
			except Exception as e:
#				traceback.print_exc()
#				print(type(e))
#				print(e)
#				print(dttm_get())
				if attempts >= 3:
					print(f'errored => cb.get_product_book(product_id={prod_id}, limit={limit})')
					print(f'attempt {attempts} of {max_attempts}, sleeping 1 seconds and then retrying')
				time.sleep(1)

		# if I believed that all the micro amounts before my target size 
		# might not be consumed before me, I would do a weighted average price
		for bid in bids:
			this_bid_size  = float(bid['size'])
			this_bid_prc   = float(bid['price'])
			cum_bids_size += this_bid_size
			if cum_bids_size > buy_sell_size:
				bid_prc = this_bid_prc
				break

		for ask in asks:
			this_ask_size  = float(bid['size'])
			this_ask_prc   = float(ask['price'])
			cum_asks_size += this_ask_size
			if cum_asks_size > buy_sell_size:
				ask_prc = this_ask_prc
				break

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
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 30 == 0:
			granularity  = 'THIRTY_MINUTE'
			req_secs     = 60 * 30
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 15 == 0:
			granularity  = 'FIFTEEN_MINUTE'
			req_secs     = 60 * 15
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 5 == 0:
			granularity  = 'FIVE_MINUTE'
			req_secs     = 60 * 5
			req_span     = req_rows_max * req_secs
		else:
			granularity  = 'ONE_MINUTE'
			req_secs     = 60 * 1
			req_span     = req_rows_max * req_secs

	elif rfreq_base == 'hour':
		if rfreq_mult % 24 == 0:
			granularity  = 'ONE_DAY'
			req_secs     = 24 * 60 * 60
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 6 == 0:
			granularity  = 'SIX_HOUR'
			req_secs     = 6 * 60 * 60
			req_span     = req_rows_max * req_secs
		elif rfreq_mult % 2 == 0:
			granularity  = 'TWO_HOUR'
			req_secs     = 2 * 60 * 60
			req_span     = req_rows_max * req_secs
		else:
			granularity  = 'ONE_HOUR'
			req_secs     = 1 * 60 * 60
			req_span     = req_rows_max * req_secs

	elif rfreq_base == 'day':
		granularity  = 'ONE_DAY'
		req_secs     = 24 * 60 * 60
		req_span     = req_rows_max * req_secs

	elif rfreq_base == 'week':
		granularity  = 'ONE_DAY'
		req_secs     = 24 * 60 * 60
		req_span     = req_rows_max * req_secs

	elif rfreq_base == 'month':
		granularity  = 'ONE_DAY'
		req_secs     = 24 * 60 * 60
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
	temp_end = temp_end - temp_end % 60 + req_secs

	ohlcv            = []
	row_cnt          = 0
	enough_tf        = False

	df = None

	req_cnt = 0
	while not enough_tf:

		temp_start        = temp_end - req_span

		est_rows = (temp_end - temp_start) / req_secs
		if est_rows >= 300:
			fix_rows = est_rows - 300
			fix_secs = fix_rows * secs
			temp_start += fix_secs
			temp_start = int(temp_start)
			est_rows = (temp_end - temp_start) / secs + 1

		req_cnt += 1

		r = None
		attempts = 0
		max_attempts = 10
		candles = None
		while r == None:
			try:
				attempts += 1
				time.sleep(0.25)
				# print(f'cb.get_candles(product_id={product_id}, temp_start={temp_start}, temp_end={temp_end}, granularity={granularity})')
				r = cb.get_candles(product_id, temp_start, temp_end, granularity)
				candles = r['candles']
			except Exception as e:
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
			x = x.to_dict()
			# print(f'candle : {x} ({type(x)})')
			for k in x:
				# print(f'k : {k} ({type(k)})')
				if k == 'start':
					x[k] = int(x[k])
				else:
					# print(f'k : {k}, x[k] : {x[k]} ({type(x[k])})')
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

	func_end(fnc)
	return df

#<=====>#

def cb_curr_shaper(in_acct):
	func_name = 'cb_curr_shaper'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	prc_dec = 0

	for prc in (bid_prc, ask_prc):
		dec_str = str(prc).split('.')[1] if '.' in str(prc) else ''
		dec_str = dec_str.rstrip('0')
		if len(dec_str) > prc_dec:
			prc_dec = len(dec_str)

	func_end(fnc)
	return prc_dec

#<=====>#

def cb_mkt_refresh(prod_id, stable_coins=None):
	func_name = 'cb_mkt_refresh'
	func_str = f'{lib_name}.{func_name}(prod_id={prod_id})'
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	t0 = time.perf_counter()

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
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	out_mkt = AttrDict()

	try:
		out_mkt.mkt_name                            = in_mkt['product_id']
		out_mkt.prod_id                             = in_mkt['product_id']
		out_mkt.mkt_venue                           = in_mkt['product_venue']

		out_mkt.base_curr_name                      = in_mkt['base_name']
		out_mkt.base_curr_symb                      = in_mkt['base_display_symbol']
		out_mkt.base_size_incr                      = float(in_mkt['base_increment'])
		out_mkt.base_size_min                       = float(in_mkt['base_min_size'])
		out_mkt.base_size_max                       = float(in_mkt['base_max_size'])

		out_mkt.quote_curr_name                     = in_mkt['quote_name']
		out_mkt.quote_curr_symb                     = in_mkt['quote_name']
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
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	t0 = time.perf_counter()

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
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
	G(func_str)

	o = None
	time.sleep(0.25)

	r = None
	try:
		r = cb.get_order(order_id=order_id)
		r = r.to_dict()
	except Exception as e:
		print('get_order errored...')
		print(e)
#		beep()

	if r:
		if 'order' in r:
			if r['order']:
				o = r['order']
		else:
			print(f'{func_name} no order found for {order_id}')
			print(r)
#			beep()

		if o:
			o = cb_ord_shaper(o)
			db_tbl_ords_insupd(o)

	func_end(fnc)
	return o

#<=====>#

def cb_ord_shaper(in_ord):
	func_name = 'cb_ord_shaper'
	func_str = f'{lib_name}.{func_name}()'
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

	out_ord = AttrDict()

	out_ord.ord_uuid                    = in_ord['order_id']

	out_ord.prod_id                     = in_ord['product_id']
	out_ord.ord_bs                      = in_ord['side'].lower()

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

	if 'base_price' in ord_body:        out_ord.ord_base_size              = float(ord_body['base_size'])
	if 'quote_size' in ord_body:        out_ord.ord_quote_size             = float(ord_body['quote_size'])
	if 'limit_price' in ord_body:       out_ord.ord_limit_prc              = float(ord_body['limit_price'])
	if 'stop_direction' in ord_body:    out_ord.ord_stop_dir               = ord_body['stop_direction']
	if 'stop_price' in ord_body:        out_ord.ord_stop_prc               = float(ord_body['stop_price'])
	if 'stop_trigger_price' in ord_body:out_ord.ord_stop_trigger_prc       = float(ord_body['stop_trigger_price']   )
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
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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
	lib_secs_max = get_lib_func_secs_max(lib_name=lib_name, func_name=func_name)
	fnc = func_begin(func_name=func_name, func_str=func_str, logname=log_name, secs_max=lib_secs_max)
#	G(func_str)

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

	# this keeps colliding with other bots when 
	# they both hit here at the same time
	# this function should get moved to auto loop
	try:
		db_tbl_bals_insupd(all_bals)
		db_tbl_currs_insupd(all_currs)
		db_currs_prc_mkt_upd()
		db_bals_prc_mkt_upd()
	except Exception as e:
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		beep()
		pass


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
