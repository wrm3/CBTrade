#<=====>#
# Description - Coinbase Business Logic Functions
#<=====>#
# This module contains standalone business logic functions for Coinbase operations
# All functions can be imported directly: from libs.coinbase_handler import cb_wallet_refresh, cb_bal_get
#<=====>#

#<=====>#
# Imports - Public
#<=====>#
# Standard library imports
import certifi
import json
import os
import pandas as pd
import re
import requests.exceptions
import signal
import sys
import threading
import time
import traceback
import uuid

from fstrent_colors import *
from coinbase.rest import RESTClient
from datetime import datetime, timedelta, timezone
from datetime import datetime as dt
from dateutil import parser as dt_prsr
from dotenv import load_dotenv
from pprint import pprint

#<=====>#
# Imports - Project
#<=====>#
from libs.common import AttrDict
from libs.common import get_unix_timestamp
from libs.common import beep
from libs.common import dttm_get
from libs.common import narc
from libs.db_mysql.cbtrade.db_main import CBTRADE_DB
cbtrade_db = CBTRADE_DB()  # Create instance for backward compatibility
# from libs.db.ohlcv import protect_ohlcv_dataframe, safe_timestamp_conversion

#<=====>#
# Variables
#<=====>#

lib_name = 'coinbase_handler'
log_name = 'coinbase_handler'
debug_tf = False


#<=====>#
# Pre-Assigned Variables
#<=====>#

# Add SSL certificate path fix for Windows
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['SSL_CERT_FILE'] = certifi.where()

#<=====>#
# Classes
#<=====>#

class CoinbaseAPI:
    """
    Clean class-based interface to Coinbase Advanced Trade API
    Handles all direct REST API communication
    """
    
    def __init__(self, api_key=None, api_secret=None):
        """Initialize the Coinbase API client"""
        # Load environment variables
        load_dotenv()
        
        # Use provided credentials or environment variables
        self.api_key = api_key or os.getenv('COINBASE_API_KEY')
        self.api_secret = api_secret or os.getenv('COINBASE_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("Coinbase API key and secret must be provided via parameters or environment variables")
        
        # Initialize REST client
        self.client = RESTClient(api_key=self.api_key, api_secret=self.api_secret)

    #<=====>#

    @narc(1)
    def load_debug_performance_settings(self):
        if debug_tf: Y(f'coinbase_handler.load_debug_performance_settings()')
        """Load performance debugging thresholds from settings"""
        try:
            with open('settings/debug.json', 'r') as f:
                debug_settings = json.load(f)
            return debug_settings.get('performance_thresholds', {
                'show_optimization_messages': False,
                'show_on_slow_performance': True,
                'balance_cache_threshold': 1.0
            })
        except Exception as e:
            print(f"WARNING: Could not load debug settings: {e}")
            return {
                'show_optimization_messages': False,
                'show_on_slow_performance': True,
                'balance_cache_threshold': 1.0
            }

    # <=====>#

    @narc(1)
    def gen_client_order_id(self):
        if debug_tf: Y(f'coinbase_handler.gen_client_order_id()')
        """Generate a new client order ID"""
        return str(uuid.uuid4())

    # <=====>#

    @narc(1)
    def _log_api_error(self, method_name, exception, params=None):
        if debug_tf: Y(f'coinbase_handler._log_api_error()')
        """Log API errors with context"""
        error_msg = f"""
=== COINBASE API ERROR ===
File: {__file__}
Method: {method_name}
Timestamp: {dttm_get()}
Exception Type: {type(exception).__name__}
Exception Message: {str(exception)}
Parameters: {params or 'None'}
Full Traceback:
{traceback.format_exc()}
========================
"""
        print(error_msg)
        beep(3)  # Audio alert for immediate attention


    # <=====>#
    # Network Resilience Methods
    # <=====>#
    
    @narc(1)
    def _execute_with_timeout(self, operation_func, timeout_seconds=30.0, operation_name="unknown"):
        if debug_tf: Y(f'coinbase_handler._execute_with_timeout()')
        """
        Execute operation with timeout to prevent silent socket hangs
        
        🔧 GILFOYLE'S ANTI-HANG SYSTEM:
        - Prevents silent socket hangs that bypass retry logic
        - Forces timeout after specified seconds (default: 30s)
        - Raises TimeoutError if operation takes too long
        - Works on Windows using threading approach
        
        Args:
            operation_func: Function to execute with timeout
            timeout_seconds: Maximum seconds to wait (default: 30.0)
            operation_name: Name for logging purposes
            
        Returns:
            Result of operation_func
            
        Raises:
            TimeoutError: If operation exceeds timeout
        """
        result = [None]
        exception = [None]
        
        def target():
            try:
                result[0] = operation_func()
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout=timeout_seconds)
        
        if thread.is_alive():
            # Thread is still running - operation timed out
            timeout_msg = f"⏰ COINBASE API TIMEOUT: {operation_name} exceeded {timeout_seconds}s limit"
            print(timeout_msg)
            raise TimeoutError(f"Operation '{operation_name}' timed out after {timeout_seconds} seconds")
        
        if exception[0]:
            raise exception[0]
            
        return result[0]
    
    @narc(1)
    def _execute_with_retry(self, operation_func, operation_name, max_retries=3, base_delay=1.0, max_delay=30.0, operation_params=None):
        if debug_tf: Y(f'coinbase_handler._execute_with_retry()')
        """
        Execute API operations with exponential backoff retry for connection errors
        
        🔧 GILFOYLE'S CONNECTION RESILIENCE SYSTEM:
        - Automatically retries on ConnectionError, Timeout, ChunkedEncodingError
        - Uses exponential backoff: 1s, 2s, 4s delays (configurable)
        - Does NOT retry on authentication, validation, or business logic errors
        - Provides detailed logging for troubleshooting
        - Maximum delay cap prevents excessive wait times
        
        Args:
            operation_func: The API method to execute
            operation_name: Name of the operation for logging
            max_retries: Maximum number of retry attempts (default: 3)
            base_delay: Initial delay between retries in seconds (default: 1.0)
            max_delay: Maximum delay between retries in seconds (default: 30.0)
            operation_params: Dict of parameters for logging purposes
            
        Returns:
            Result of the operation function
            
        Raises:
            The final exception if all retries fail
        """
        last_exception = None
        operation_params = operation_params or {}
        
        for attempt in range(max_retries + 1):  # +1 for initial attempt
            try:
                # Execute the operation with timeout protection to prevent silent hangs
                return self._execute_with_timeout(
                    operation_func=operation_func,
                    timeout_seconds=30.0,
                    operation_name=operation_name
                )
                
            except (requests.exceptions.ConnectionError, 
                    requests.exceptions.Timeout,
                    requests.exceptions.ChunkedEncodingError,
                    TimeoutError) as e:
                
                last_exception = e
                
                # Don't retry on the final attempt
                if attempt == max_retries:
                    break
                    
                # Calculate delay with exponential backoff
                delay = min(base_delay * (2 ** attempt), max_delay)
                
                # Log retry attempt
                retry_msg = f"""
🔄 COINBASE API RETRY #{attempt + 1}/{max_retries}
Operation: {operation_name}
Error: {type(e).__name__}: {str(e)}
Retrying in {delay:.1f} seconds...
Parameters: {operation_params}
"""
                print(retry_msg)
                
                # Wait before retry
                time.sleep(delay)
                
            except Exception as e:
                # Don't retry on non-connection errors (auth, validation, etc.)
                self._log_api_error(operation_name, e, operation_params)
                raise
        
        # All retries failed - log and raise the final exception
        final_error_msg = f"""
❌ COINBASE API RETRY EXHAUSTED
Operation: {operation_name}
Attempts: {max_retries + 1}
Final Error: {type(last_exception).__name__}: {str(last_exception)}
Parameters: {operation_params}
"""
        print(final_error_msg)
        self._log_api_error(f"{operation_name}_final_failure", last_exception, operation_params)
        raise last_exception

    @narc(1)
    def _execute_with_backoff_forever(self, operation_func, operation_name, base_delay=1.0, max_delay=300.0, operation_params=None):
        if debug_tf: Y(f'coinbase_handler._execute_with_backoff_forever()')
        """
        Execute API operations with incremental backoff that caps at max_delay, then continues forever.

        - Uses exponential backoff (1s, 2s, 4s, ...), capped at max_delay (default 300s = 5 minutes)
        - Beeps when delay exceeds 60 seconds
        - Never stops retrying until the operation succeeds
        - Intended for information requests only (NOT order placement)
        """
        attempt = 0
        operation_params = operation_params or {}
        while True:
            try:
                return self._execute_with_timeout(
                    operation_func=operation_func,
                    timeout_seconds=30.0,
                    operation_name=operation_name
                )
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.ChunkedEncodingError,
                    requests.exceptions.HTTPError,
                    TimeoutError) as e:
                # For HTTPError, only block specific 4xx errors that are definitely not retryable
                if isinstance(e, requests.exceptions.HTTPError):
                    if hasattr(e, 'response') and e.response is not None:
                        status_code = e.response.status_code
                        # Only block these specific 4xx errors - others might be temporary
                        if status_code in [400, 403]:  # Bad Request, Forbidden - 401 can be temporary
                            self._log_api_error(operation_name, e, operation_params)
                            raise
                        # 404, 429, and other 4xx errors will be retried (might be temporary)
                # Compute backoff
                delay = min(base_delay * (2 ** attempt), max_delay)
                attempt += 1
                msg = f"""
🔄 COINBASE API RETRY (infinite)
Operation: {operation_name}
Error: {type(e).__name__}: {str(e)}
Next retry in {delay:.1f} seconds (cap {max_delay}s)
Parameters: {operation_params}
"""
                print(msg)
                if delay >= 60.0:
                    try:
                        beep()
                    except Exception:
                        pass
                time.sleep(delay)
            except Exception as e:
                # Non-connection related errors should surface immediately
                self._log_api_error(operation_name, e, operation_params)
                raise

    #<=====>#

    @narc(1)
    def shape_curr(self, in_acct):
        if debug_tf: Y(f'coinbase_handler.shape_curr()')
        """Shape currency/account data from Coinbase API format to business format"""
        out_curr = AttrDict()
        out_curr.curr_uuid            = in_acct['uuid']
        out_curr.symb                 = in_acct['currency']
        out_curr.name                 = in_acct['currency']
        out_curr.bal_avail            = float(in_acct['available_balance']['value'])
        out_curr.bal_hold             = float(in_acct['hold']['value'])
        out_curr.bal_tot              = out_curr.bal_avail + out_curr.bal_hold

        out_curr.create_dttm          = None
        out_curr.update_dttm          = None
        out_curr.delete_dttm          = None

        if in_acct['created_at']:
            try:
                # Try with microseconds first
                out_curr.create_dttm = datetime.strptime(in_acct['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                try:
                    # Fallback to format without microseconds
                    out_curr.create_dttm = datetime.strptime(in_acct['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                except Exception as e:
                    print(f"FATAL: Could not parse created_at '{in_acct['created_at']}' for account {in_acct.get('uuid', 'unknown')}: {e}")
                    raise
        
        if in_acct['updated_at']:
            try:
                out_curr.update_dttm = datetime.strptime(in_acct['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                try:
                    out_curr.update_dttm = datetime.strptime(in_acct['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
                except Exception as e:
                    print(f"Warning: Could not parse updated_at '{in_acct['updated_at']}' for account {in_acct.get('uuid', 'unknown')}: {e}")
                    out_curr.update_dttm = None
        
        if in_acct['deleted_at']:
            try:
                out_curr.delete_dttm = datetime.strptime(in_acct['deleted_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                try:
                    out_curr.delete_dttm = datetime.strptime(in_acct['deleted_at'], "%Y-%m-%dT%H:%M:%SZ")
                except Exception as e:
                    print(f"FATAL: Could not parse deleted_at '{in_acct['deleted_at']}' for account {in_acct.get('uuid', 'unknown')}: {e}")
                    raise

        out_curr.rp_id                = in_acct['retail_portfolio_id']
        out_curr.default_tf           = in_acct['default']
        out_curr.ready_tf             = in_acct['ready']
        out_curr.active_tf            = in_acct['active']

        return out_curr

    #<=====>#

    @narc(1)
    def shape_mkt(self, in_mkt):
        if debug_tf: Y(f'coinbase_handler.shape_mkt()')
        """Shape market/product data from Coinbase API format to business format"""
        out_mkt = AttrDict()

        
        # # Convert Product object to dict if needed
        # if hasattr(in_mkt, 'to_dict'):
        #     in_mkt = in_mkt.to_dict()
        # elif not isinstance(in_mkt, dict):
        #     print(f"Warning: Unexpected input type: {type(in_mkt)}")
        #     return None

        # pprint(in_mkt)

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
                out_mkt.prc = -1
                out_mkt.prc_ask = -1
                out_mkt.prc_buy = -1
                out_mkt.prc_bid = -1
                out_mkt.prc_sell = -1
            else:
                out_mkt.prc      = float(in_mkt['price'])
                out_mkt.prc_ask  = float(in_mkt['price'])
                out_mkt.prc_buy  = float(in_mkt['price'])
                out_mkt.prc_bid  = float(in_mkt['price'])
                out_mkt.prc_sell = float(in_mkt['price'])

            # if in_mkt['price_ask'] == '':
            #     out_mkt.prc = -1
            #     out_mkt.prc_ask = -1
            #     out_mkt.prc_buy = -1
            # else:
            #     out_mkt.prc_ask  = float(in_mkt['price_ask'])
            #     out_mkt.prc_buy  = float(in_mkt['price_ask'])

            # if in_mkt['price_bid'] == '':
            #     out_mkt.prc_bid = -1
            #     out_mkt.prc_sell = -1
            # else:
            #     out_mkt.prc_bid  = float(in_mkt['price_bid'])
            #     out_mkt.prc_sell = float(in_mkt['price_bid'])

            if in_mkt['mid_market_price'] == '':
                out_mkt.prc_mid_mkt = -1
            elif in_mkt['mid_market_price']:
                out_mkt.prc_mid_mkt = float(in_mkt['mid_market_price'])
            else:
                out_mkt.prc_mid_mkt = out_mkt.prc

            if in_mkt['price_percentage_change_24h'] == '':
                out_mkt.prc_pct_chg_24h = 0
            elif in_mkt['price_percentage_change_24h']:
                out_mkt.prc_pct_chg_24h = float(in_mkt['price_percentage_change_24h'])
            else:
                out_mkt.prc_pct_chg_24h = 0

            # Handle volume fields with safer checks
            if in_mkt['volume_24h']:
                out_mkt.vol_24h = float(in_mkt['volume_24h'])
            else:
                out_mkt.vol_24h = 0

            if 'volume_base_24h' in in_mkt and in_mkt['volume_base_24h']:
                out_mkt.vol_base_24h = float(in_mkt['volume_base_24h'])
            else:
                out_mkt.vol_base_24h = out_mkt.vol_24h

            if 'volume_quote_24h' in in_mkt and in_mkt['volume_quote_24h']:
                out_mkt.vol_quote_24h = float(in_mkt['volume_quote_24h'])
            else:
                out_mkt.vol_quote_24h = out_mkt.vol_24h * out_mkt.prc

            if 'volume_percentage_change_24h' in in_mkt and in_mkt['volume_percentage_change_24h']:
                out_mkt.vol_pct_chg_24h = float(in_mkt['volume_percentage_change_24h'])
            else:
                out_mkt.vol_pct_chg_24h = 0

        except Exception as e:
            print(f'{out_mkt.prod_id} shape_mkt errored : {e}')
            print("Full market data:")
            pprint(in_mkt)
            raise

        return out_mkt

    #<=====>#

    @narc(1)
    def shape_ord(self, in_ord):
        if debug_tf: Y(f'coinbase_handler.shape_ord()')
        """Shape order data from Coinbase API format to business format"""
        out_ord = AttrDict()

        out_ord.ord_uuid = in_ord['order_id']
        out_ord.prod_id = in_ord['product_id']
        out_ord.ord_bs = in_ord['side'].lower()

        # Initialize order configuration fields
        out_ord.ord_base_size = None
        out_ord.ord_end_time = None
        out_ord.ord_limit_prc = None
        out_ord.ord_post_only = None
        out_ord.ord_quote_size = None
        out_ord.ord_stop_dir = None
        out_ord.ord_stop_prc = None
        out_ord.ord_stop_trigger_prc = None

        # Parse order configuration
        for ord_type in in_ord['order_configuration']:
            ord_body = in_ord['order_configuration'][ord_type]
            out_ord.ord_type = ord_type

            if 'base_size' in ord_body:        out_ord.ord_base_size = float(ord_body['base_size'])
            if 'quote_size' in ord_body:       out_ord.ord_quote_size = float(ord_body['quote_size'])
            if 'limit_price' in ord_body:      out_ord.ord_limit_prc = float(ord_body['limit_price'])
            if 'stop_direction' in ord_body:   out_ord.ord_stop_dir = ord_body['stop_direction']
            if 'stop_price' in ord_body:       out_ord.ord_stop_prc = float(ord_body['stop_price'])
            if 'stop_trigger_price' in ord_body: out_ord.ord_stop_trigger_prc = float(ord_body['stop_trigger_price'])
            if 'post_only' in ord_body:        out_ord.ord_post_only = ord_body['post_only']
            if 'end_time' in ord_body:         out_ord.ord_end_time = int(ord_body['end_time'])

        # Map all other order fields
        out_ord.order_id = in_ord['order_id']
        out_ord.ord_product_id = in_ord['product_id']
        out_ord.ord_user_id = in_ord['user_id']
        out_ord.ord_order_configuration = str(in_ord['order_configuration']).replace("'","")
        out_ord.ord_side = in_ord['side']
        out_ord.ord_client_order_id = in_ord['client_order_id']
        out_ord.ord_status = in_ord['status']
        out_ord.ord_time_in_force = in_ord['time_in_force']

        if in_ord['created_time']:
            out_ord.ord_created_time = datetime.strptime(in_ord['created_time'], "%Y-%m-%dT%H:%M:%S.%fZ")

        out_ord.ord_completion_percentage = float(in_ord['completion_percentage'])
        out_ord.ord_filled_size = float(in_ord['filled_size'])
        out_ord.ord_average_filled_price = float(in_ord['average_filled_price'])
        out_ord.ord_fee = in_ord['fee'] if in_ord['fee'] != '' else None
        out_ord.ord_number_of_fills = int(in_ord['number_of_fills'])
        out_ord.ord_filled_value = float(in_ord['filled_value'])
        out_ord.ord_pending_cancel = in_ord['pending_cancel']
        out_ord.ord_size_in_quote = in_ord['size_in_quote']
        out_ord.ord_total_fees = float(in_ord['total_fees'])
        out_ord.ord_size_inclusive_of_fees = in_ord['size_inclusive_of_fees']
        out_ord.ord_total_value_after_fees = float(in_ord['total_value_after_fees'])
        out_ord.ord_trigger_status = in_ord['trigger_status']
        out_ord.ord_order_type = in_ord['order_type']
        out_ord.ord_reject_reason = in_ord['reject_reason']
        out_ord.ord_settled = in_ord['settled']
        out_ord.ord_product_type = in_ord['product_type']
        out_ord.ord_reject_message = in_ord['reject_message']
        out_ord.ord_cancel_message = in_ord['cancel_message']
        out_ord.ord_order_placement_source = in_ord['order_placement_source']
        out_ord.ord_outstanding_hold_amount = float(in_ord['outstanding_hold_amount'])
        out_ord.ord_is_liquidation = in_ord['is_liquidation']

        out_ord.ord_last_fill_time = None
        if in_ord['last_fill_time']:
            out_ord.ord_last_fill_time = datetime.fromisoformat(in_ord['last_fill_time'])

        out_ord.ord_edit_history = ', '.join(in_ord['edit_history']).replace("'","")
        out_ord.ord_leverage = in_ord['leverage'] if in_ord['leverage'] != '' else None
        out_ord.ord_margin_type = in_ord['margin_type']
        out_ord.ord_retail_portfolio_id = in_ord['retail_portfolio_id']

        return out_ord

    #<=====>#

    @narc(1)
    def cb_wallet_refresh(self):
        if debug_tf: Y(f'coinbase_handler.cb_wallet_refresh()')
        # print('coinbase_handler.cb_wallet_refresh()')
        """Business logic for comprehensive wallet refresh with database operations"""
        accts = []
        has_next = True
        cursor = None
        
        while has_next:
            cnt = 0
            r = None
            
            while cnt < 10 and not r:
                try:
                    if cursor:
                        r = self.get_accounts(limit=250, cursor=cursor)
                    else:
                        r = self.get_accounts(limit=250)
                    
                    # 🔴 CRITICAL: Convert Coinbase SDK object to dict (like original July 9th code)
                    if r and not isinstance(r, dict):
                        r = r.to_dict()
                        
                except Exception as e:
                    print(f'🔴 COINBASE API RETRY: get_accounts failed, attempt {cnt + 1}/10: {e}')
                    beep(3)
                    cnt += 1
                    sleep_cnt = cnt * cnt
                    time.sleep(sleep_cnt)
                    
            if r:
                more_accts = r['accounts']
                accts.extend(more_accts)
                has_next = r['has_next']
                cursor = r['cursor']
            else:
                print('no accounts found')
                break

        all_currs = []
        all_bals = []
        
        for acct in accts:
            curr = self.shape_curr(acct)
            if (acct['active'] and float(acct['available_balance']['value']) > 0):
                all_bals.append(curr)
            all_currs.append(curr)

        # print(f'cb_wallet_refresh() => all_bals: {len(all_bals)}')
        # print(f'cb_wallet_refresh() => all_currs: {len(all_currs)}')

        # Business logic: Database operations with error handling
        try:
            # print('cb_wallet_refresh() => db_bals_insupd')
            for bal in all_bals:
                cbtrade_db.db_bals_insupd(bal)
            # print('cb_wallet_refresh() => db_currs_insupd')
            for curr in all_currs:
                cbtrade_db.db_currs_insupd(curr)
            # Wallet refresh completed successfully - run silently
            # print('cb_wallet_refresh() => db_bals_prc_mkt_upd')
            cbtrade_db.db_bals_prc_mkt_upd()
        except Exception as e:
            print(f'🔴 CRITICAL DATABASE FAILURE in cb_wallet_refresh: {e}')
            beep(3)
            sys.exit(f"CRITICAL DATABASE FAILURE EXIT - Function: cb_wallet_refresh, Reason: {str(e)}")

        return all_bals, all_currs

    #<=====>#

    @narc(1)
    def cb_mkt_refresh(self, prod_id, stable_coins=None):
        if debug_tf: Y(f'coinbase_handler.cb_mkt_refresh() ==> {prod_id}')
        """Business logic for refreshing single market data with database operations"""
        time.sleep(0.25)
        
        r = self._execute_with_backoff_forever(
            operation_func=lambda: self.get_product(product_id=prod_id),
            operation_name="get_product",
            base_delay=1.0,
            max_delay=300.0,
            operation_params={"product_id": prod_id}
        )

        add_tf = False
        prod = r
        if prod and not prod['view_only']:
            if not prod['is_disabled']:
                if prod['status'] == 'online':
                    if not prod['trading_disabled']:
                        add_tf = True
        
        if add_tf:
            mkt = self.shape_mkt(prod)
            print(f'cb_mkt_refresh({prod_id}) => about to insert mkt')
            # Update market data in database
            cbtrade_db.db_mkts_insupd(mkt)
            print('cb_mkt_refresh() => db_currs_prc_mkt_upd 1()')
            
            # Update all market prices in balances
            cbtrade_db.db_bals_prc_mkt_upd()  # Now works correctly since BOT inherits from CBTRADE_DB

            if stable_coins:
                if isinstance(stable_coins, str):
                    temp = []
                    temp.append(stable_coins)
                    stable_coins = temp
                if isinstance(stable_coins, list):
                    # Note: stable coin pricing updates handled by view-based architecture
                    pass

            print('cb_mkt_refresh() => Real-time pricing via currs view')
            return mkt
        
        return None

    #<=====>#

    @narc(1)
    def cb_mkts_refresh(self, quote_symb:str=None, stable_coins=None):
        if debug_tf: Y(f'coinbase_handler.cb_mkts_refresh() ==> {quote_symb}')
        Y(f'coinbase_handler.cb_mkts_refresh() ==> {quote_symb}')
        """Business logic for refreshing all markets data with database operations"""
        time.sleep(0.25)
        
        # Use infinite backoff for information requests (resilient reconnect)
        r = self._execute_with_backoff_forever(
            operation_func=lambda: self.get_products(),
            operation_name="get_products",
            base_delay=1.0,
            max_delay=300.0,
            operation_params={"quote_symb": quote_symb}
        )
        
        # 🔴 CRITICAL: Convert Coinbase SDK object to dict (like original July 9th code)
        if not isinstance(r, dict):
            r = r.to_dict()

        all_mkts = []
        for prod in r['products']:
            add_tf = False
            if prod['quote_currency_id'] == quote_symb:
                if not prod['view_only']:
                    if not prod['is_disabled']:
                        if prod['status'] == 'online':
                            if not prod['trading_disabled']:
                                add_tf = True
            if add_tf:
                mkt = self.shape_mkt(prod)
                all_mkts.append(mkt)

        Y(f'coinbase_handler.cb_mkts_refresh() ==> {quote_symb} - db_mkts_insupd - inserting {len(all_mkts)} markets')
        for mkt in all_mkts:
            cbtrade_db.db_mkts_insupd(mkt)

        Y(f'coinbase_handler.cb_mkts_refresh() ==> {quote_symb} - db_bals_prc_mkt_upd - updating prices')
        # print('cb_mkts_refresh() => db_currs_prc_mkt_upd 1()')
        cbtrade_db.db_bals_prc_mkt_upd()

        if stable_coins:
            if isinstance(stable_coins, str):
                temp = []
                temp.append(stable_coins)
                stable_coins = temp
            if isinstance(stable_coins, list):
                # Note: stable coin pricing updates handled by view-based architecture
                pass

        Y(f'coinbase_handler.cb_mkts_refresh() ==> {quote_symb} - returning {len(all_mkts)} markets')
        return all_mkts

    #<=====>#

    @narc(1)
    def cb_ords_refresh(self, loop_mkts, all_tf=False):
        if debug_tf: Y(f'coinbase_handler.cb_ords_refresh() ==> {loop_mkts}')
        """Business logic for refreshing orders data with database operations"""
        all_ords = []
        
        for prod_id in loop_mkts:
            try:
                limit = 10
                ords = []
                has_next = True
                cursor = None
                
                while (has_next or all_tf):
                    try:
                        if cursor:
                            time.sleep(0.25)
                            r = self.list_orders(product_id=prod_id, limit=limit, cursor=cursor)
                        else:
                            time.sleep(0.25)
                            r = self.list_orders(product_id=prod_id, limit=limit)
                        
                        # 🔴 CRITICAL: Convert Coinbase SDK object to dict (like original July 9th code)
                        if not isinstance(r, dict):
                            r = r.to_dict()
                        
                        more_ords = r['orders']
                        ords.extend(more_ords)
                        cursor = r['cursor']
                        has_next = r['has_next']
                        
                        if all_tf and not has_next:
                            break
                        elif not all_tf and len(ords) >= limit:
                            break
                            
                    except Exception as e:
                        print(f'🔴 COINBASE API ERROR in cb_ords_refresh for {prod_id}: {e}')
                        beep(3)
                        break

                for o in ords:
                    o = self.shape_ord(o)
                    all_ords.append(o)
                    
            except Exception as e:
                print(f'🔴 COINBASE API ERROR processing orders for {prod_id}: {e}')
                beep(3)
                continue

        try:
            cbtrade_db.db_ords_insupd(all_ords)
        except Exception as e:
            print(f'🔴 DATABASE ERROR in cb_ords_refresh: {e}')
            beep(3)

        return all_ords

    # <=====>#
    
    @narc(1)
    def get_accounts(self, limit=250, cursor=None):
        if debug_tf: Y(f'coinbase_handler.get_accounts()')
        """Get all accounts with pagination support"""
        try:
            if cursor:
                return self.client.get_accounts(limit=limit, cursor=cursor)
            else:
                return self.client.get_accounts(limit=limit)
        except Exception as e:
            self._log_api_error("get_accounts", e, {"limit": limit, "cursor": cursor})
            raise
    
    #<=====>#

    @narc(1)
    def cb_bal_get(self, symb):
        if debug_tf: Y(f'coinbase_handler.cb_bal_get() ==> {symb}')
        Y(f'coinbase_handler.cb_bal_get() ==> {symb}')
        """
        Business logic for resilient balance fetching with infinite backoff retry
        Will retry indefinitely until Coinbase connectivity is restored
        CRITICAL: Balance data must be accurate for trading decisions
        """
        
        def _get_balance_operation():
            accts = []
            has_next = True
            cursor = None
            
            while has_next:
                if cursor:
                    time.sleep(0.25)
                    r = self.get_accounts(limit=250, cursor=cursor)
                else:
                    time.sleep(0.25)
                    r = self.get_accounts(limit=250)
                
                # 🔴 CRITICAL: Convert Coinbase SDK object to dict (like original July 9th code)
                if not isinstance(r, dict):
                    r = r.to_dict()
                    
                more_accts = r['accounts']
                accts.extend(more_accts)
                has_next = r['has_next']
                cursor = r['cursor']

            bal = 0
            for acct in accts:
                if acct['currency'] == symb:
                    bal = float(acct['available_balance']['value'])
            
            return bal
        
        # Use infinite backoff for balance data (critical for trading)
        # This prevents bots from thinking they have $0 when API is temporarily down
        bal = self._execute_with_backoff_forever(
            operation_func=_get_balance_operation,
            operation_name=f"cb_bal_get({symb})",
            base_delay=1.0,
            max_delay=300.0,  # Cap at 5 minutes like other critical info requests
            operation_params={"symb": symb}
        )
        
        return bal
    # <=====>#
    
    @narc(1)
    def get_products(self):
        if debug_tf: Y(f'coinbase_handler.get_products()')
        """Get all trading products/markets"""
        try:
            return self.client.get_products()
        except Exception as e:
            # Let caller decide retry policy; we only log here
            self._log_api_error("get_products", e)
            raise

    # <=====>#

    @narc(1)
    def get_product(self, product_id):
        if debug_tf: Y(f'coinbase_handler.get_product() ==> {product_id}')
        """Get specific product details"""
        try:
            return self.client.get_product(product_id=product_id)
        except Exception as e:
            # Info request: caller chooses backoff policy; we only log
            self._log_api_error("get_product", e, {"product_id": product_id})
            raise

    # <=====>#

    @narc(1)
    def get_best_bid_ask(self, product_ids):
        if debug_tf: Y(f'coinbase_handler.get_best_bid_ask() ==> {product_ids}')
        """Get best bid and ask for products with infinite backoff retry
        CRITICAL: Pricing data is essential for trading decisions - never give up"""
        
        def _get_best_bid_ask_operation():
            return self.client.get_best_bid_ask(product_ids=product_ids)
        
        # Use infinite backoff for pricing data (critical for trading)
        # Pricing failures should not crash bots - wait for connectivity restoration
        return self._execute_with_backoff_forever(
            operation_func=_get_best_bid_ask_operation,
            operation_name="get_best_bid_ask",
            base_delay=1.0,
            max_delay=300.0,  # Cap at 5 minutes
            operation_params={"product_ids": product_ids}
        )

    #<=====>#

    @narc(1)
    def cb_mkt_prc_dec_calc(self, bid_prc, ask_prc):
        if debug_tf: Y(f'coinbase_handler.cb_mkt_prc_dec_calc()')
        """Calculate price decimal places for market formatting"""
        prc_dec = 0

        for prc in (bid_prc, ask_prc):
            dec_str = str(prc).split('.')[1] if '.' in str(prc) else ''
            dec_str = dec_str.rstrip('0')
            if len(dec_str) > prc_dec:
                prc_dec = len(dec_str)

        return prc_dec

    #<=====>#

    @narc(1)
    def cb_bid_ask_get(self, prod_id):
        if debug_tf: Y(f'coinbase_handler.cb_bid_ask_get() ==> {prod_id}')
        """Get bid/ask prices for a product"""
        r = self.get_best_bid_ask([prod_id])
        
        # 🔴 CRITICAL: Convert Coinbase SDK object to dict (like original July 9th code)
        if not isinstance(r, dict):
            r = r.to_dict()
            
        bid_prc = float(r['pricebooks'][0]['bids'][0]['price'])
        ask_prc = float(r['pricebooks'][0]['asks'][0]['price'])
        return bid_prc, ask_prc

    #<=====>#

    @narc(1)
    def cb_bid_ask_by_amt_get(self, pair, buy_sell_size):
        if debug_tf: Y(f'coinbase_handler.cb_bid_ask_by_amt_get() ==> {pair.prod_id}')
        """Get bid/ask prices by amount with infinite backoff retry for order book analysis
        CRITICAL: Order book data essential for optimal pricing - never give up"""

        prod_id = pair.prod_id
        bid_prc = pair.prc_bid
        ask_prc = pair.prc_ask

        # print(f'cb_bid_ask_by_amt_get: {prod_id} {bid_prc}, {ask_prc}, {buy_sell_size}')
        try:
            bid_prc, ask_prc = self.cb_bid_ask_get(prod_id)
            cum_bids_size = 0
            cum_asks_size = 0

            limit = 60
            
            def _get_order_book_operation():
                time.sleep(0.25)
                r = self.get_product_book(product_id=prod_id, limit=limit)
                
                # 🔴 CRITICAL: Convert Coinbase SDK object to dict (like original July 9th code)
                if not isinstance(r, dict):
                    r = r.to_dict()
                    
                return r['pricebook']['bids'], r['pricebook']['asks']
            
            # Use infinite backoff for order book data (critical for optimal pricing)
            # Order book failures should not crash bots - wait for connectivity restoration
            bids, asks = self._execute_with_backoff_forever(
                operation_func=_get_order_book_operation,
                operation_name=f"get_product_book({prod_id})",
                base_delay=1.0,
                max_delay=300.0,  # Cap at 5 minutes
                operation_params={"product_id": prod_id, "limit": limit}
            )

            # Business logic: Calculate cumulative order book depth
            for bid in bids:
                this_bid_size = float(bid['size'])
                this_bid_prc = float(bid['price'])
                cum_bids_size += this_bid_size
                if cum_bids_size > buy_sell_size:
                    bid_prc = this_bid_prc
                    break

            for ask in asks:
                this_ask_size = float(ask['size'])
                this_ask_prc = float(ask['price'])
                cum_asks_size += this_ask_size
                if cum_asks_size > buy_sell_size:
                    ask_prc = this_ask_prc
                    break

        except Exception as e:
            print(f'🔴 COINBASE API ERROR in cb_bid_ask_by_amt_get for {prod_id}: {e}')
            beep(3)

        return bid_prc, ask_prc

    # <=====>#

    @narc(1)
    def get_product_book(self, product_id, limit=None):
        """Get order book for product"""
        try:
            return self.client.get_product_book(product_id=product_id, limit=limit)
        except Exception as e:
            self._log_api_error("get_product_book", e, {"product_id": product_id, "limit": limit})
            raise

    # <=====>#

    @narc(1)
    def get_candles(self, product_id, start, end, granularity):
        if debug_tf: Y(f'coinbase_handler.get_candles() ==> {product_id}')
        """Get candlestick data for product"""
        try:
            return self.client.get_candles(product_id, start, end, granularity)
        except Exception as e:
            self._log_api_error("get_candles", e, {
                "product_id": product_id, 
                "start": start, 
                "end": end, 
                "granularity": granularity
            })
            raise
    #<=====>#

    @narc(1)
    def cb_candles_get(self, product_id, start=None, end=None, rfreq=None, granularity=None, min_rows=299):
        if debug_tf: Y(f'coinbase_handler.cb_candles_get() ==> {product_id}')
        """Get candlestick data with comprehensive business logic"""
        secs = 0
        now = int(round(datetime.now(timezone.utc).timestamp()))

        # cb has a limit or max 300 rows
        req_rows_max = 300

        # defaults
        granularity = 'ONE_MINUTE'
        secs = 60 * 1
        req_secs = secs  # Initialize req_secs to default value
        req_span = req_rows_max * secs

        rfreq_mult = 1
        rfreq_base = 'minute'
        
        # Parse frequency string
        if rfreq:
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

            # Set granularity based on frequency
            if rfreq_base == 'minute':
                if rfreq_mult % 60 == 0:
                    granularity = 'ONE_HOUR'
                    req_secs = 60 * 60
                    req_span = req_rows_max * req_secs
                elif rfreq_mult % 30 == 0:
                    granularity = 'THIRTY_MINUTE'
                    req_secs = 60 * 30
                    req_span = req_rows_max * req_secs
                elif rfreq_mult % 15 == 0:
                    granularity = 'FIFTEEN_MINUTE'
                    req_secs = 60 * 15
                    req_span = req_rows_max * req_secs
                elif rfreq_mult % 5 == 0:
                    granularity = 'FIVE_MINUTE'
                    req_secs = 60 * 5
                    req_span = req_rows_max * req_secs
                else:
                    granularity = 'ONE_MINUTE'
                    req_secs = 60 * 1
                    req_span = req_rows_max * req_secs

            elif rfreq_base == 'hour':
                if rfreq_mult % 24 == 0:
                    granularity = 'ONE_DAY'
                    req_secs = 24 * 60 * 60
                    req_span = req_rows_max * req_secs
                elif rfreq_mult % 6 == 0:
                    granularity = 'SIX_HOUR'
                    req_secs = 6 * 60 * 60
                    req_span = req_rows_max * req_secs
                elif rfreq_mult % 2 == 0:
                    granularity = 'TWO_HOUR'
                    req_secs = 2 * 60 * 60
                    req_span = req_rows_max * req_secs
                else:
                    granularity = 'ONE_HOUR'
                    req_secs = 1 * 60 * 60
                    req_span = req_rows_max * req_secs

            elif rfreq_base in ['day', 'week', 'month']:
                granularity = 'ONE_DAY'
                req_secs = 24 * 60 * 60
                req_span = req_rows_max * req_secs

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

        ohlcv = []
        row_cnt = 0
        enough_tf = False
        df = None
        req_cnt = 0
        
        while not enough_tf:
            temp_start = temp_end - req_span

            est_rows = (temp_end - temp_start) / req_secs
            if est_rows >= 300:
                fix_rows = est_rows - 300
                fix_secs = fix_rows * secs
                temp_start += fix_secs
                temp_start = int(temp_start)
                est_rows = (temp_end - temp_start) / secs + 1

            req_cnt += 1

            # Use infinite backoff for candles data (information request, not trading)
            # This prevents bot crashes when Coinbase has connectivity issues
            candles = None
            
            def _get_candles_operation():
                time.sleep(0.25)
                r = self.get_candles(product_id, temp_start, temp_end, granularity)
                # 🔴 CRITICAL: Convert Coinbase SDK object to dict (like original July 9th code)
                if not isinstance(r, dict):
                    r = r.to_dict()
                return r['candles']
            
            candles = self._execute_with_backoff_forever(
                operation_func=_get_candles_operation,
                operation_name=f"get_candles({product_id})",
                base_delay=1.0,
                max_delay=300.0,  # Cap at 5 minutes like other info requests
                operation_params={
                    "product_id": product_id, 
                    "temp_start": temp_start, 
                    "temp_end": temp_end, 
                    "granularity": granularity
                }
            )

            no_more_candles = False
            if not candles:
                no_more_candles = True
            
            # Debug: report raw candle count returned by API for this window
            try:
                _candle_cnt = len(candles) if candles else 0
                _win_start = dt.fromtimestamp(int(temp_start), timezone.utc).isoformat()
                _win_end = dt.fromtimestamp(int(temp_end), timezone.utc).isoformat()
                # print(f"[OHLCV-API] {product_id} rfreq={rfreq or 'n/a'} gran={granularity} window={_win_start}→{_win_end} candles={_candle_cnt}")
            except Exception:
                pass
                
            for x in candles:
                if isinstance(x, pd.DataFrame):
                    x = x.to_dict()
                if not isinstance(x, dict):
                    x = x.to_dict()
                    
                for k in x.keys():
                    if k == 'start':
                        x[k] = int(x[k])
                    else:
                        x[k] = float(x[k])
                x['timestamp'] = x['start']
                ohlcv.append(x)

            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Apply timestamp protection if available
            try:
                source_name = f"API-{product_id}-{rfreq}"
                # Clean, standard pandas - no magic functions
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                df.set_index('timestamp', inplace=True)
                # Basic validation if needed
                df = df.dropna()  # Remove any NaN values
            except ImportError:
                # Fallback if ohlcv module not available
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                df.set_index('timestamp', inplace=True)

            d = {
                "open": "first", 
                "high": "max", 
                "low": "min", 
                "close": "last", 
                "volume": "sum"
            }

            if rfreq:
                df = df.resample(rfreq).agg(d)
            df.dropna()

            row_cnt = len(df)
            # Debug: report resampled dataframe row count
            # try:
            #     WoM(f"[OHLCV-DF] {product_id} rfreq={rfreq or 'n/a'} rows={row_cnt}")
            # except Exception:
            #     pass
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

            temp_start = temp_start - req_span
            temp_end = temp_end - req_span

        return df
    
    # <=====>#
    # Order Methods
    # <=====>#
    
    @narc(1)
    def list_orders(self, product_id=None, limit=None, cursor=None):
        if debug_tf: Y(f'coinbase_handler.list_orders() ==> {product_id}')
        """List orders with optional filtering and connection retry logic"""
        
        def _list_orders_operation():
            return self.client.list_orders(
                product_id=product_id,
                limit=limit,
                cursor=cursor
            )
        
        return self._execute_with_retry(
            operation_func=_list_orders_operation,
            operation_name="list_orders",
            operation_params={"product_id": product_id, "limit": limit, "cursor": cursor}
        )
    
    @narc(1)
    def get_order(self, order_id):
        if debug_tf: Y(f'coinbase_handler.get_order() ==> {order_id}')
        """Get order details by order ID with connection retry logic"""
        
        def _get_order_operation():
            r = self.client.get_order(order_id)
            return r
        
        r = self._execute_with_retry(
            operation_func=_get_order_operation,
            operation_name="get_order",
            operation_params={"order_id": order_id}
        )
        return r

    #<=====>#

    @narc(1)
    def cb_ord_get_shaped(self, order_id):
        if debug_tf: Y(f'coinbase_handler.cb_ord_get_shaped() ==> {order_id}')
        """
        Business logic for getting order details with proper shaping
        This is what flow_main.py should call instead of cb_ord_get() directly
        
        Returns shaped order object with standardized field names like:
        - ord_status (instead of status)
        - ord_completion_percentage (instead of completion_percentage)
        - etc.
        """
        
        o = None
        
        # 🔴 CRITICAL: Add timeout protection like original cb_ord_get
        time.sleep(0.25)
        
        try:
            # Use timeout protection to prevent hanging (like original)
            response = self._execute_with_timeout(
                lambda: self.get_order(order_id),
                timeout_seconds=30.0,
                operation_name=f"get_order({order_id})"
            )
            
            if response:
                # 🔴 CRITICAL: Convert Coinbase SDK object to dict (like original July 9th code)
                if not isinstance(response, dict):
                    response = response.to_dict()
                
                if 'order' in response:
                    raw_order = response['order']
                else:
                    raw_order = response
                    
                if raw_order:
                    # Shape the order data to standardized format
                    o = self.shape_ord(raw_order)
                else:
                    
                    # Optionally save to database (like original cb_ord_get did)
                    try:
                        cbtrade_db.db_ords_insupd(o)
                    except Exception as db_e:
                        print(f'🔴 DB WARNING: Failed to save order {order_id}: {db_e}')
                        # Don't fail the entire operation for DB issues
                        
        except TimeoutError as te:
            print(f'🔴 COINBASE API TIMEOUT in cb_ord_get_shaped for order {order_id}: {te}')
            beep(3)
        except Exception as e:
            print(f'🔴 COINBASE API ERROR in cb_ord_get_shaped for order {order_id}: {e}')
            beep(3)
            
        return o

    #<=====>#

    @narc(1)
    def cb_ord_get(self, order_id):
        if debug_tf: Y(f'coinbase_handler.cb_ord_get() ==> {order_id}')
        """Get order details - backward compatibility wrapper"""
        response = self.get_order(order_id)
        if response and 'order' in response:
            return response['order']
        return response

    # <=====>#

    @narc(1)
    def cancel_orders(self, order_ids):
        if debug_tf: Y(f'coinbase_handler.cancel_orders() ==> {order_ids}')
        """Cancel multiple orders by order IDs with timeout protection"""
        
        def _cancel_orders_operation():
            return self.client.cancel_orders(order_ids=order_ids)
        
        return self._execute_with_timeout(
            operation_func=_cancel_orders_operation,
            timeout_seconds=30.0,
            operation_name=f"cancel_orders({order_ids})"
        )
    
    # <=====>#
    
    @narc(1)
    def create_order(self, client_order_id, product_id, side, order_configuration):
        if debug_tf: Y(f'coinbase_handler.create_order() ==> {client_order_id}')
        """Create a new order with connection retry logic"""
        
        def _create_order_operation():
            return self.client.create_order(
                client_order_id=client_order_id,
                product_id=product_id,
                side=side,
                order_configuration=order_configuration
            )
        
        return self._execute_with_retry(
            operation_func=_create_order_operation,
            operation_name="create_order",
            operation_params={"client_order_id": client_order_id, "product_id": product_id, "side": side, "order_configuration": order_configuration}
        )

    # <=====>#

    @narc(1)
    def market_buy(self, product_id, quote_size):
        if debug_tf: Y(f'coinbase_handler.market_buy() ==> {product_id}')
        """Place market buy order"""
        try:
            return self.client.fiat_market_buy(product_id, quote_size)
        except Exception as e:
            self._log_api_error("market_buy", e, {"product_id": product_id, "quote_size": quote_size})
            raise

    #<=====>#

    @narc(1)
    def ord_mkt_buy(self):
        if debug_tf: Y(f'coinbase_handler.ord_mkt_buy()')
        """Market buy order with business logic"""
        
        prod_id = self.buy.prod_id
        spend_amt = str(self.buy.trade_size)
        self.buy.refresh_wallet_tf = True

        # Use API client for order placement
        order = self.market_buy(prod_id, spend_amt)
        self.buy.refresh_wallet_tf = True
        time.sleep(0.33)

        ord_id = order.id

        # Get order details using shaped version for consistency
        o = self.cb_ord_get_shaped(ord_id)
        time.sleep(0.33)

        bo = None
        if o:
            bo = AttrDict()
            bo.prod_id = self.buy.prod_id
            bo.symb = self.buy.symb
            bo.pos_type = 'SPOT'
            bo.ord_stat = 'OPEN'
            bo.buy_strat_type = self.buy.buy_strat_type
            bo.buy_strat_name = self.buy.buy_strat_name
            bo.buy_strat_freq = self.buy.buy_strat_freq
            # Live orders must be consistent: test flags indicate LIVE
            bo.test_txn_yn = 'N'
            bo.buy_order_uuid = ord_id
            bo.buy_begin_dttm = dt.now(timezone.utc)
            bo.buy_curr_symb = self.buy.base_curr_symb
            bo.spend_curr_symb = self.buy.quote_curr_symb
            bo.fees_curr_symb = self.buy.quote_curr_symb
            bo.buy_cnt_est = (self.buy.trade_size * 0.996) / self.buy.prc_buy
            bo.prc_buy_est = self.buy.prc_buy
            bo.note = self.buy.note
            bo.note2 = self.buy.note2
            bo.note3 = self.buy.note3
            cbtrade_db.db_buy_ords_insupd(bo)
            time.sleep(.33)
        else:
            print(f'🔴 TRADING FAILURE: ord_mkt_buy API call returned None for {prod_id}')
            beep(3)
            sys.exit(f"TRADING FAILURE EXIT - Function: ord_mkt_buy, Reason: API call returned None")

    #<=====>#

    @narc(1)
    def ord_mkt_buy_orig(self):
        if debug_tf: Y(f'coinbase_handler.ord_mkt_buy_orig()')
        """Original market buy order - trading core function"""

        order_uuid = None
        client_order_id       = cb.gen_client_order_id()
        prod_id               = self.buy.prod_id
        spend_amt             = self.buy.trade_size
        self.buy.refresh_wallet_tf    = True

        oc = {}
        oc['market_market_ioc'] = {}
        oc['market_market_ioc']['quote_size'] = str(spend_amt)

        o = cb.create_order(
                client_order_id = client_order_id, 
                product_id = prod_id, 
                side = 'BUY', 
                order_configuration = oc
                )
        print(type(o))
        print(o)
        if not isinstance(o, dict):
            o = o.to_dict()

        self.buy.refresh_wallet_tf       = True
        time.sleep(0.25)

        bo = None
        if o:
            if 'success' in o:
                if o['success']:
                    bo = AttrDict()
                    bo.prod_id               = self.buy.prod_id
                    bo.symb                  = self.buy.symb
                    bo.pos_type              = 'SPOT'
                    bo.ord_stat              = 'OPEN'
                    bo.buy_strat_type        = self.buy.buy_strat_type
                    bo.buy_strat_name        = self.buy.buy_strat_name
                    bo.buy_strat_freq        = self.buy.buy_strat_freq
                    # Live orders must be consistent: test flags indicate LIVE
                    bo.test_txn_yn           = 'N'
                    bo.buy_order_uuid        = o['success_response']['order_id']
                    order_uuid               = o['success_response']['order_id']
                    bo.buy_client_order_id   = o['success_response']['client_order_id']
                    bo.buy_begin_dttm        = dt.now(timezone.utc) # dt.now()
                    bo.buy_curr_symb         = self.buy.base_curr_symb
                    bo.spend_curr_symb       = self.buy.quote_curr_symb
                    bo.fees_curr_symb        = self.buy.quote_curr_symb
                    bo.buy_cnt_est           = (spend_amt * 0.996) / self.buy.prc_buy
                    bo.prc_buy_est           = self.buy.prc_buy
                    bo.note                  = self.buy.note
                    bo.note2                 = self.buy.note2
                    bo.note3                 = self.buy.note3
                    cbtrade_db.db_buy_ords_insupd(bo)
                    time.sleep(.25)
                else:
                    error_msg = f"""
    === CRITICAL TRADING FAILURE ===
    File: {os.path.basename(__file__)}
    Function: {sys._getframe().f_code.co_name}
    Timestamp: {dt.now(timezone.utc)}
    Issue: Order creation failed - success=False
    Product ID: {prod_id}
    Spend Amount: {spend_amt}
    Order Response: {o}
    ====================================
    """
                    print(error_msg)
                    beep(3)  # Audio alert for immediate attention
                    sys.exit(f"TRADING FAILURE EXIT - File: {os.path.basename(__file__)}, Function: {sys._getframe().f_code.co_name}, Reason: ord_mkt_buy_orig success=False")
            else:
                error_msg = f"""
    === CRITICAL TRADING FAILURE ===
    File: {os.path.basename(__file__)}
    Function: {sys._getframe().f_code.co_name}
    Timestamp: {dt.now(timezone.utc)}
    Issue: Order response missing 'success' key
    Product ID: {prod_id}
    Spend Amount: {spend_amt}
    Order Response: {o}
    ====================================
    """
                print(error_msg)
                beep(3)  # Audio alert for immediate attention
                sys.exit(f"TRADING FAILURE EXIT - File: {os.path.basename(__file__)}, Function: {sys._getframe().f_code.co_name}, Reason: ord_mkt_buy_orig missing success key")
        else:
            error_msg = f"""
    === CRITICAL TRADING FAILURE ===
    File: {os.path.basename(__file__)}
    Function: {sys._getframe().f_code.co_name}
    Timestamp: {dt.now(timezone.utc)}
    Issue: Order object is None - API call failed
    Product ID: {prod_id}
    Spend Amount: {spend_amt}
    ====================================
    """
            print(error_msg)
            beep(3)  # Audio alert for immediate attention
            sys.exit(f"TRADING FAILURE EXIT - File: {os.path.basename(__file__)}, Function: {sys._getframe().f_code.co_name}, Reason: ord_mkt_buy_orig API call returned None")
        return order_uuid

    #<=====>#

    # API method aliases for backward compatibility
    @narc(1)
    def api_market_buy(self, product_id, quote_size):
        if debug_tf: Y(f'coinbase_handler.api_market_buy() ==> {product_id}')
        """Market buy alias"""
        return self.market_buy(product_id, quote_size)

    #<=====>#

    @narc(1)
    def api_market_buy_orig(self, product_id, quote_size):
        if debug_tf: Y(f'coinbase_handler.api_market_buy_orig() ==> {product_id}')
        """Market buy original alias"""
        client_order_id = self.gen_client_order_id()
        oc = {'market_market_ioc': {'quote_size': str(quote_size)}}
        return self.create_order(client_order_id, product_id, 'BUY', oc)


#<=====>#

    @narc(1)
    def backfill_db_from_api(self, start_date: str = '2024-12-27', limit_per_batch: int = 2000, sleep_sec: float = 0.6, include_test: bool = False):
        if debug_tf: Y(f"coinbase_handler.backfill_db_from_api(start_date={start_date}, limit_per_batch={limit_per_batch}, include_test={include_test})")
        """Backfill cbtrade.ords (database) by querying the Coinbase API for UUIDs found in buy_ords/sell_ords since start_date.

        Default is LIVE-only (test_txn_yn='N'). If include_test=True, will also attempt test rows.
        """

        # Collect buy UUIDs missing in ords
        sql_buy = ""
        sql_buy += "select bo.buy_order_uuid as ord_uuid, bo.buy_begin_dttm as begin_dttm "
        sql_buy += "  from cbtrade.buy_ords bo "
        sql_buy += "  left join cbtrade.ords o on o.ord_uuid = bo.buy_order_uuid "
        sql_buy += f" where bo.buy_begin_dttm >= '{start_date}' "
        if not include_test:
            sql_buy += "   and bo.test_txn_yn = 'N' "
        sql_buy += "   and bo.buy_order_uuid is not null and bo.buy_order_uuid <> '' "
        sql_buy += "   and o.ord_uuid is null "
        sql_buy += f" order by bo.buy_begin_dttm asc limit {int(limit_per_batch)}"

        # Collect sell UUIDs missing in ords
        sql_sell = ""
        sql_sell += "select so.sell_order_uuid as ord_uuid, so.sell_begin_dttm as begin_dttm "
        sql_sell += "  from cbtrade.sell_ords so "
        sql_sell += "  left join cbtrade.ords o on o.ord_uuid = so.sell_order_uuid "
        sql_sell += f" where so.sell_begin_dttm >= '{start_date}' "
        if not include_test:
            sql_sell += "   and so.test_txn_yn = 'N' "
        sql_sell += "   and so.sell_order_uuid is not null and so.sell_order_uuid <> '' "
        sql_sell += "   and o.ord_uuid is null "
        sql_sell += f" order by so.sell_begin_dttm asc limit {int(limit_per_batch)}"

        miss_buy = cbtrade_db.seld(sql_buy, always_list_yn='Y')
        miss_sell = cbtrade_db.seld(sql_sell, always_list_yn='Y')

        # Collect with timestamps for deterministic ordering
        rows = []
        for r in (miss_buy or []):
            try:
                u = r.get('ord_uuid')
                d = r.get('begin_dttm')
                if u:
                    rows.append((d, u))
            except Exception:
                pass
        for r in (miss_sell or []):
            try:
                u = r.get('ord_uuid')
                d = r.get('begin_dttm')
                if u:
                    rows.append((d, u))
            except Exception:
                pass

        # Sort by begin_dttm asc (None last), then deduplicate preserving order
        rows.sort(key=lambda t: (t[0] is None, t[0]))
        seen, uuids_unique = set(), []
        for _, u in rows:
            if u not in seen:
                seen.add(u)
                uuids_unique.append(u)

        if not uuids_unique:
            print(f"ORDS BACKFILL: no missing UUIDs since {start_date}")
            return 0

        ok, fail, not_found, skipped_existing = 0, 0, 0, 0
        for ord_uuid in uuids_unique:
            try:
                # Do not overwrite existing rows
                chk = cbtrade_db.seld("select ord_uuid from cbtrade.ords where ord_uuid = %s", [ord_uuid])
                if chk:
                    skipped_existing += 1
                    continue
                # Call API directly first to reduce noisy logging/beeps, then shape
                o = None
                try:
                    resp = cb.get_order(ord_uuid)
                    if resp and not isinstance(resp, dict):
                        resp = resp.to_dict()
                    raw_order = resp['order'] if resp and 'order' in resp else resp
                    o = cb.shape_ord(raw_order) if raw_order else None
                except Exception as inner:
                    msg = str(inner)
                    if '404' in msg or 'NOT_FOUND' in msg:
                        not_found += 1
                        time.sleep(max(0.05, float(sleep_sec)))
                        continue
                    # Fallback to shaped helper if other error types
                    try:
                        o = self.cb_ord_get_shaped(ord_uuid)
                    except Exception:
                        pass
                if o:
                    cbtrade_db.db_ords_insupd(o)
                    ok += 1
                else:
                    fail += 1
                time.sleep(max(0.05, float(sleep_sec)))
            except Exception as e:
                fail += 1
                if debug_tf:
                    print(f"ORDS BACKFILL ERROR for {ord_uuid}: {e}")
                time.sleep(max(0.05, float(sleep_sec)))

        print(f"ORDS BACKFILL: upserted={ok}, skipped_existing={skipped_existing}, not_found={not_found}, failed={fail}, examined={len(uuids_unique)} (since {start_date}, include_test={include_test})")
        return ok

    # Backward compatible alias
    def backfill_ords_from_db(self, start_date: str = '2024-12-27', limit_per_batch: int = 2000, sleep_sec: float = 0.6, include_test: bool = False):
        return self.backfill_db_from_api(start_date=start_date, limit_per_batch=limit_per_batch, sleep_sec=sleep_sec, include_test=include_test)

#<=====>#

    @narc(1)
    def cb_sell_base_size_calc(self, pos_data, st_pair, prc_sell, init_sell_cnt):
        if debug_tf: Y(f'coinbase_handler.cb_sell_base_size_calc() ==> {pos_data.prod_id}')
        sell_cnt_max     = init_sell_cnt

        pos_data.pocket_pct            = st_pair.sell.rainy_day.pocket_pct
        pos_data.clip_pct              = st_pair.sell.rainy_day.clip_pct
        pos_data.prc_sell              = prc_sell

        if round(sell_cnt_max,8) > round(pos_data.hold_cnt,8):
            print(f'...selling more {sell_cnt_max:>.8f} than we are position is holding {pos_data.hold_cnt:>.8f} onto...exiting...')
            beep(3)
            pos_data.sell_cnt = 0
            return pos_data  # ← Return pos_data, not None

        if round(sell_cnt_max,8) > round(pos_data.bal_cnt,8):
            print(f'...selling more {sell_cnt_max:>.8f} than we the wallet balance {pos_data.bal_cnt:>.8f}...')
            print(f'...RETRYING BALANCE FETCH - balance data may be stale...')
            
            # 🔄 FORCE FRESH BALANCE FETCH - API may have failed earlier
            fresh_bal = self.cb_bal_get(pos_data.buy_curr_symb)
            print(f'...fresh balance fetched: {fresh_bal:>.8f} (was {pos_data.bal_cnt:>.8f})...')
            
            # Update position with fresh balance
            pos_data.bal_cnt = fresh_bal
            
            # Update balance table with fresh data
            try:
                b = AttrDict()
                b.symb = pos_data.buy_curr_symb
                b.bal = fresh_bal
                cbtrade_db.db_bals_insupd([b])
                print(f'...balance table updated for {pos_data.buy_curr_symb}...')
            except Exception as e:
                print(f'...WARNING: Could not update balance table: {e}...')
            
            # Re-check with fresh balance
            if round(sell_cnt_max,8) > round(pos_data.bal_cnt,8):
                print(f'...STILL INSUFFICIENT after fresh fetch: selling {sell_cnt_max:>.8f} > balance {pos_data.bal_cnt:>.8f}...exiting...')
                beep(3)
                pos_data.sell_cnt = 0
                return pos_data  # ← Return pos_data, not None
            else:
                print(f'...balance RECOVERED: {pos_data.bal_cnt:>.8f} is now sufficient for {sell_cnt_max:>.8f}...continuing...')
                beep(1)  # Success sound

        if pos_data.prc_chg_pct > 0 and pos_data.pocket_pct > 0:
            sell_cnt_max -= sell_cnt_max * (pos_data.pocket_pct / 100) * (pos_data.prc_chg_pct/100)

        if pos_data.prc_chg_pct < 0 and pos_data.clip_pct > 0:
            sell_cnt_max -= sell_cnt_max * (pos_data.clip_pct / 100) * (abs(pos_data.prc_chg_pct)/100)

        sell_blocks = int(sell_cnt_max / pos_data.base_size_incr)
        sell_cnt_max = sell_blocks * pos_data.base_size_incr

        if sell_cnt_max < pos_data.base_size_min:
            print(f'...selling less {sell_cnt_max:>.8f} than coinbase allows {pos_data.base_size_min}...exiting...')
            beep(3)
            pos_data.sell_cnt = 0
            return pos_data

        if sell_cnt_max > pos_data.base_size_max:
            sell_cnt_max = pos_data.base_size_max
        pos_data.sell_cnt = sell_cnt_max
        return pos_data

    # <=====>#

    @narc(1)
    def market_sell(self, product_id, base_size):
        if debug_tf: Y(f'coinbase_handler.market_sell() ==> {product_id}')
        """Place market sell order"""
        try:
            return self.client.fiat_market_sell(product_id, base_size)
        except Exception as e:
            self._log_api_error("market_sell", e, {"product_id": product_id, "base_size": base_size})
            raise

    #<=====>#

    @narc(1)
    def api_market_sell(self, product_id, base_size):
        if debug_tf: Y(f'coinbase_handler.api_market_sell() ==> {product_id}')
        """Market sell alias"""
        return self.market_sell(product_id, base_size)

    #<=====>#

    @narc(1)
    def api_market_sell_orig(self, product_id, base_size):
        if debug_tf: Y(f'coinbase_handler.api_market_sell_orig() ==> {product_id}')
        """Market sell original alias"""
        client_order_id = self.gen_client_order_id()
        oc = {'market_market_ioc': {'base_size': f'{base_size:>.8f}'}}
        return self.create_order(client_order_id, product_id, 'SELL', oc)

    #<=====>#

    @narc(1)
    def ord_mkt_sell(self, pos):
        if debug_tf: Y(f'coinbase_handler.ord_mkt_sell() ==> {pos.prod_id}')
        """Market sell order with business logic"""
        
        prod_id = pos.prod_id
        sell_cnt = str(pos.trade_size)

        # Use API client for order placement
        order = self.market_sell(prod_id, sell_cnt)
        time.sleep(.33)

        ord_id = order.id

        self.pos.pos_stat = 'SELL'
        cbtrade_db.db_poss_insupd(pos)
        time.sleep(.33)

        # Get order details using shaped version for consistency
        o = self.cb_ord_get_shaped(ord_id)
        time.sleep(.33)

        so = None
        if o:
            so = AttrDict()
            so.prod_id = pos.prod_id
            so.symb = pos.symb
            so.pos_type = 'SPOT'
            so.sell_order_uuid = ord_id
            so.sell_begin_dttm = dt.now(timezone.utc)
            so.sell_curr_symb = pos.base_curr_symb
            so.sell_cnt_est = pos.trade_size
            so.recv_curr_symb = pos.quote_curr_symb
            so.recv_cnt_est = pos.trade_size * pos.prc_sell
            so.fees_curr_symb = pos.quote_curr_symb
            so.prc_sell_est = pos.prc_sell
            cbtrade_db.db_sell_ords_insupd(so)
            time.sleep(.33)
            cbtrade_db.db_poss_insupd(pos)
            time.sleep(.33)
        else:
            cbtrade_db.db_poss_insupd(pos)
            print(f'🔴 TRADING FAILURE: ord_mkt_sell API call returned None for {prod_id}')
            beep(3)
            sys.exit(f"TRADING FAILURE EXIT - Function: ord_mkt_sell, Reason: API call returned None")

    #<=====>#

    @narc(1)
    def ord_mkt_sell_orig(self, pos, st_pair):
        if debug_tf: Y(f'coinbase_handler.ord_mkt_sell_orig() ==> {pos.prod_id}')
        """Original market sell order - trading core function"""

        # pprint(pos)  # debug only

        client_order_id       = cb.gen_client_order_id()
        prod_id               = pos.prod_id
        prc_sell              = pos.prc_sell
        init_sell_cnt         = pos.hold_cnt

        pos = self.cb_sell_base_size_calc(pos, st_pair, prc_sell, init_sell_cnt)

        if pos.sell_cnt == 0:
            pos.symb = 'USDC'
            pos.pos_stat = 'ERR'
            pos.ignore_tf = 1
            pos.error_tf = 1
            pos.sell_yn = 'N'
            pos.reason = f'there are not enough {pos.buy_curr_symb} to complete this sale...'
            cbtrade_db.db_poss_upd(pos)
        else:
            oc = {}
            oc['market_market_ioc'] = {}
            oc['market_market_ioc']['base_size'] = f'{pos.sell_cnt:>.8f}'

            o = cb.create_order(
                    client_order_id = client_order_id, 
                    product_id = prod_id, 
                    side = 'SELL', 
                    order_configuration = oc
                    )
            print(type(o))
            print(o)
            if not isinstance(o, dict):
                o = o.to_dict()

            pos.refresh_wallet_tf       = True
            time.sleep(0.25)

            so = None
            if o:
                if 'success' in o:
                    if o['success']:
                        so = AttrDict()
                        so.pos_id                = pos.pos_id
                        so.symb                  = pos.symb
                        so.prod_id               = pos.prod_id
                        so.pos_type              = 'SPOT'
                        so.ord_stat              = 'OPEN'
                        so.sell_order_uuid       = o['success_response']['order_id']
                        so.sell_client_order_id  = o['success_response']['client_order_id']
                        so.sell_begin_dttm       = dt.now(timezone.utc) # dt.now()
                        so.sell_strat_type       = pos.sell_strat_type
                        so.sell_strat_name       = pos.sell_strat_name
                        so.sell_curr_symb        = pos.base_curr_symb
                        so.recv_curr_symb        = pos.quote_curr_symb
                        so.fees_curr_symb        = pos.quote_curr_symb
                        so.sell_cnt_est          = pos.sell_cnt
                        so.prc_sell_est          = pos.prc_sell
                        cbtrade_db.db_sell_ords_insupd(so)
                        time.sleep(.25)
                        pos.pos_stat = 'SELL'
                        cbtrade_db.db_poss_upd(pos)
    #                        db_poss_stat_upd(pos_id=self.pos.pos_id, pos_stat='SELL')
                    else:
                        error_msg = f"""
    === CRITICAL TRADING FAILURE ===
    File: {os.path.basename(__file__)}
    Function: {sys._getframe().f_code.co_name}
    Timestamp: {dt.now(timezone.utc)}
    Issue: Order creation failed - success=False
    Product ID: {prod_id}
    Position ID: {pos.pos_id}
    Sell Count: {pos.sell_cnt}
    Order Response: {o}
    ====================================
    """
                        print(error_msg)
                        beep(3)  # Audio alert for immediate attention
                        sys.exit(f"TRADING FAILURE EXIT - File: {os.path.basename(__file__)}, Function: {sys._getframe().f_code.co_name}, Reason: ord_mkt_sell_orig success=False")
                else:
                    error_msg = f"""
    === CRITICAL TRADING FAILURE ===
    File: {os.path.basename(__file__)}
    Function: {sys._getframe().f_code.co_name}
    Timestamp: {dt.now(timezone.utc)}
    Issue: Order response missing 'success' key
    Product ID: {prod_id}
    Position ID: {pos.pos_id}
    Sell Count: {pos.sell_cnt}
    Order Response: {o}
    ====================================
    """
                    print(error_msg)
                    beep(3)  # Audio alert for immediate attention
                    sys.exit(f"TRADING FAILURE EXIT - File: {os.path.basename(__file__)}, Function: {sys._getframe().f_code.co_name}, Reason: ord_mkt_sell_orig missing success key")
            else:
                error_msg = f"""
    === CRITICAL TRADING FAILURE ===
    File: {os.path.basename(__file__)}
    Function: {sys._getframe().f_code.co_name}
    Timestamp: {dt.now(timezone.utc)}
    Issue: Order object is None - API call failed
    Product ID: {prod_id}
    Position ID: {pos.pos_id}
    Sell Count: {pos.sell_cnt}
    ====================================
    """
                print(error_msg)
                beep(3)  # Audio alert for immediate attention
                sys.exit(f"TRADING FAILURE EXIT - File: {os.path.basename(__file__)}, Function: {sys._getframe().f_code.co_name}, Reason: ord_mkt_sell_orig API call returned None")

        return pos.sell_cnt

    # <=====>#

    @narc(1)
    def limit_buy(self, product_id, base_size, limit_price, client_order_id=None, post_only=False):
        if debug_tf: Y(f'coinbase_handler.limit_buy() ==> {product_id}')
        """Place limit buy order"""
        try:
            if not client_order_id:
                client_order_id = self.gen_client_order_id()
            
            order_config = {
                'limit_limit_gtc': {
                    'base_size': f'{base_size:>.8f}',
                    'limit_price': f'{limit_price:>.8f}',
                    'post_only': post_only
                }
            }
            
            return self.create_order(client_order_id, product_id, 'BUY', order_config)
        except Exception as e:
            self._log_api_error("limit_buy", e, {
                "product_id": product_id,
                "base_size": base_size,
                "limit_price": limit_price,
                "post_only": post_only
            })
            raise

    #<=====>#

    @narc(1)
    def ord_lmt_buy_open(self):
        if debug_tf: Y(f'coinbase_handler.ord_lmt_buy_open() ==> {self.buy.prod_id}')
        """Limit buy order with business logic"""
        
        prod_id = self.buy.prod_id
        spend_amt = float(self.buy.trade_size)
        limit_price = self.buy.prc_buy
        buy_cnt = spend_amt / limit_price

        # Use API client for order placement
        o = self.limit_buy(product_id=prod_id, base_size=buy_cnt, limit_price=limit_price)

        print(o)
        self.buy.refresh_wallet_tf = True
        time.sleep(0.25)

        if o:
            if isinstance(o, dict) and 'success' in o and o['success']:
                buy_order_uuid = o['success_response']['order_id']
                buy_client_order_id = o['success_response']['client_order_id']
            else:
                buy_order_uuid = o.id
                buy_client_order_id = o.client_order_id

            bo = None
            if buy_order_uuid:
                bo = AttrDict()
                bo.prod_id = self.buy.prod_id
                bo.symb = self.buy.symb
                bo.pos_type = 'SPOT'
                bo.ord_stat = 'OPEN'
                bo.buy_strat_type = self.buy.buy_strat_type
                bo.buy_strat_name = self.buy.buy_strat_name
                bo.buy_strat_freq = self.buy.buy_strat_freq
                bo.buy_order_uuid = buy_order_uuid
                bo.buy_client_order_id = buy_client_order_id
                bo.buy_begin_dttm = dt.now(timezone.utc)
                bo.buy_begin_unix = get_unix_timestamp()
                bo.buy_curr_symb = self.buy.base_curr_symb
                bo.spend_curr_symb = self.buy.quote_curr_symb
                bo.fees_curr_symb = self.buy.quote_curr_symb
                bo.buy_cnt_est = (spend_amt * 0.996) / self.buy.prc_buy
                bo.prc_buy_est = self.buy.prc_buy
                bo.note = self.buy.note
                bo.note2 = self.buy.note2
                bo.note3 = self.buy.note3
                cbtrade_db.db_buy_ords_insupd(bo)
                time.sleep(.25)
                self.buy.refresh_wallet_tf = True
            else:
                print(f'🔴 TRADING FAILURE: ord_lmt_buy_open buy_order_uuid is None for {prod_id}')
                beep(3)
                sys.exit(f"TRADING FAILURE EXIT - Function: ord_lmt_buy_open, Reason: buy_order_uuid is None")
        else:
            print(f'🔴 TRADING FAILURE: ord_lmt_buy_open API call returned None for {prod_id}')
            beep(3)
            sys.exit(f"TRADING FAILURE EXIT - Function: ord_lmt_buy_open, Reason: API call returned None")

    #<=====>#

    @narc(1)
    def api_limit_buy(self, product_id, base_size, limit_price):
        if debug_tf: Y(f'coinbase_handler.api_limit_buy() ==> {product_id}')
        """Limit buy alias"""
        return self.limit_buy(product_id, base_size, limit_price)

    # <=====>#

    @narc(1)
    def limit_sell(self, product_id, base_size, limit_price, client_order_id=None, post_only=False):
        if debug_tf: Y(f'coinbase_handler.limit_sell() ==> {product_id}')
        """Place limit sell order"""
        try:
            if not client_order_id:
                client_order_id = self.gen_client_order_id()
            
            order_config = {
                'limit_limit_gtc': {
                    'base_size': f'{base_size:>.8f}',
                    'limit_price': f'{limit_price:>.8f}',
                    'post_only': post_only
                }
            }
            
            return self.create_order(client_order_id, product_id, 'SELL', order_config)
        except Exception as e:
            self._log_api_error("limit_sell", e, {
                "product_id": product_id,
                "base_size": base_size,
                "limit_price": limit_price,
                "post_only": post_only
            })
            raise

    #<=====>#

    @narc(1)
    def ord_lmt_sell_open(self):
        if debug_tf: Y(f'coinbase_handler.ord_lmt_sell_open() ==> {self.sell.prod_id}')
        """Limit sell order with business logic"""
        
        prod_id = self.sell.prod_id
        sell_cnt = float(self.sell.trade_size)
        limit_price = self.sell.prc_sell

        # Use API client for order placement
        o = self.limit_sell(product_id=prod_id, base_size=sell_cnt, limit_price=limit_price)

        print(o)
        time.sleep(0.25)

        self.pos.pos_stat = 'SELL'
        if o:
            if isinstance(o, dict) and 'success' in o and o['success']:
                sell_order_uuid = o['success_response']['order_id']
                sell_client_order_id = o['success_response']['client_order_id']
            else:
                sell_order_uuid = o.id
                sell_client_order_id = o.client_order_id

            so = None
            if sell_order_uuid:
                so = AttrDict()
                so.prod_id = self.sell.prod_id
                so.symb = self.sell.symb
                so.pos_type = 'SPOT'
                so.sell_order_uuid = sell_order_uuid
                so.sell_client_order_id = sell_client_order_id
                so.sell_begin_dttm = dt.now(timezone.utc)
                so.sell_curr_symb = self.sell.base_curr_symb
                so.sell_cnt_est = self.sell.trade_size
                so.recv_curr_symb = self.sell.quote_curr_symb
                so.recv_cnt_est = self.sell.trade_size * self.sell.prc_sell
                so.fees_curr_symb = self.sell.quote_curr_symb
                so.prc_sell_est = self.sell.prc_sell
                cbtrade_db.db_sell_ords_insupd(so)
                time.sleep(.25)
                cbtrade_db.db_poss_insupd(self.pos)
                time.sleep(.25)
            else:
                cbtrade_db.db_poss_insupd(self.pos)
                print(f'🔴 TRADING FAILURE: ord_lmt_sell_open sell_order_uuid is None for {prod_id}')
                beep(3)
                sys.exit(f"TRADING FAILURE EXIT - Function: ord_lmt_sell_open, Reason: sell_order_uuid is None")
        else:
            cbtrade_db.db_poss_insupd(self.pos)
            print(f'🔴 TRADING FAILURE: ord_lmt_sell_open API call returned None for {prod_id}')
            beep(3)
            sys.exit(f"TRADING FAILURE EXIT - Function: ord_lmt_sell_open, Reason: API call returned None")

        return sell_cnt

    #<=====>#

    @narc(1)
    def api_limit_sell(self, product_id, base_size, limit_price):
        if debug_tf: Y(f'coinbase_handler.api_limit_sell() ==> {product_id}')
        """Limit sell alias"""
        return self.limit_sell(product_id, base_size, limit_price)

#<=====>#
# Functions
#<=====>#

def test_main():
    """Test the CoinbaseAPI class with retry functionality demonstration"""
    try:
        api = CoinbaseAPI()
        print("✅ CoinbaseAPI initialized successfully")
        print("🔧 Network resilience features enabled:")
        print("   - Automatic retry on connection errors")
        print("   - Exponential backoff (1s, 2s, 4s)")
        print("   - Maximum 3 retry attempts")
        print("   - Detailed retry logging")
        
        # Test getting products (uses retry logic)
        products_response = api.get_products()
        if hasattr(products_response, 'to_dict'):
            products = products_response.to_dict()
        else:
            products = products_response
        print(f"✅ Retrieved {len(products.get('products', []))} products")
        
        # Test best bid/ask (uses retry logic)
        print("✅ Testing network resilience on price data...")
        bid_ask = api.get_best_bid_ask(['BTC-USD'])
        print("✅ Price data retrieved successfully with retry protection")
        

        """Test the coinbase handler functions"""

        print("✅ Testing coinbase handler functions...")
        
        # Test balance fetching
        bal = api.cb_bal_get('USDC')
        print(f"✅ USDC balance: {bal}")
        
        # Test market refresh
        mkts = api.cb_mkts_refresh()
        print(f"✅ Retrieved {len(mkts)} markets")
        
        print("✅ All handler functions working correctly")
        
    except Exception as e:
        print(f"❌ Handler test failed: {e}")

#<=====>#
# Post Assignment
#<=====>#

cb = CoinbaseAPI()

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    test_main()

#<=====>#
