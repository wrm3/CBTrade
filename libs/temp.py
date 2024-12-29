import time
import hmac
import hashlib
import base64
import json
import requests
import asyncio
import websockets
from typing import List, Dict, Any

# -----------------------
# API Client (REST)
# -----------------------
class APIClient:
    def __init__(self, api_key: str, api_secret: str, passphrase: str, base_url="https://api.coinbase.com/api/v3"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = base_url

    def _get_headers(self, method: str, path: str, body="") -> Dict[str, str]:
        timestamp = str(int(time.time()))
        message = timestamp + method + path + body
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature).decode()

        return {
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }

    def _request(self, method: str, endpoint: str, body=None):
        if body is None:
            body = {}
        path = endpoint
        url = self.base_url + path
        data = json.dumps(body) if body else ""

        headers = self._get_headers(method, path, data)
        if method == 'GET':
            resp = requests.get(url, headers=headers)
        elif method == 'POST':
            resp = requests.post(url, headers=headers, data=data)
        elif method == 'DELETE':
            resp = requests.delete(url, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")

        resp.raise_for_status()
        return resp.json()

    # ----- Public & Authenticated Endpoints -----
    
    def get_ohlcv(self, product_id: str, granularity: int = 300, start: str = None, end: str = None) -> Any:
        # Adjust endpoint and parameters according to the official Advanced Trade docs.
        # Example endpoint (not final): /products/{product_id}/candles
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        params["granularity"] = granularity
        
        # The official advanced trade might differ. Example:
        # GET /api/v3/brokerage/products/<product_id>/candles?granularity=<>&start=...&end=...
        q_string = "?" + "&".join(f"{k}={v}" for k,v in params.items()) if params else ""
        return self._request('GET', f'/brokerage/products/{product_id}/candles{q_string}')

    def place_market_order(self, product_id: str, side: str, size: float):
        # Example body for market order:
        # {
        #   "product_id": "<product_id>",
        #   "side": "BUY" or "SELL",
        #   "order_configuration": {
        #      "market_market_ioc": {
        #         "base_size": "<size>"
        #      }
        #   }
        # }
        # Check official docs for exact schema.
        
        order_body = {
            "product_id": product_id,
            "side": side.upper(),
            "order_configuration": {
                "market_market_ioc": {
                    "base_size": str(size)
                }
            }
        }
        return self._request('POST', '/brokerage/orders', order_body)

    def place_limit_order(self, product_id: str, side: str, size: float, limit_price: float, expire_seconds: int = None):
        # Example limit order with GTT (Good 'Til Time)
        # {
        #   "product_id": "<product_id>",
        #   "side": "BUY" or "SELL",
        #   "order_configuration": {
        #       "limit_limit_gtt": {
        #          "base_size": "<size>",
        #          "limit_price": "<price>",
        #          "post_only": False,
        #          "cancel_after_seconds": <expire_seconds>,
        #          "time_in_force": "GTT"
        #       }
        #    }
        # }
        order_config = {
            "limit_limit_gtt": {
                "base_size": str(size),
                "limit_price": str(limit_price),
                "post_only": False,
                "time_in_force": "GTT"
            }
        }
        if expire_seconds:
            order_config["limit_limit_gtt"]["cancel_after_seconds"] = expire_seconds

        order_body = {
            "product_id": product_id,
            "side": side.upper(),
            "order_configuration": order_config
        }
        return self._request('POST', '/brokerage/orders', order_body)

    def get_order_status(self, order_id: str):
        return self._request('GET', f'/brokerage/orders/historical/{order_id}')

    def list_orders(self, limit=100):
        # List historical orders
        return self._request('GET', f'/brokerage/orders/historical/batch?limit={limit}')

# -----------------------
# WebSocket Client
# -----------------------
class WebsocketClient:
    def __init__(self, api_key: str, api_secret: str, passphrase: str, channels: List[Dict[str, Any]], uri="wss://advanced-trade-ws.coinbase.com"):
        # Add rate limiting
        self.message_queue = asyncio.Queue()
        self.last_message_time = 0
        self.reconnect_delay = 1  # Start with 1 second delay
        self.max_reconnect_delay = 300  # Max 5 minutes
        
        # Add additional data storage
        self.trades = {}        # {product_id: [recent_trades]}
        self.balances = {}      # {currency: available_balance}
        self.positions = {}     # {product_id: position_data}
        
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.channels = channels
        self.uri = uri
        self._ws = None
        self._running = False

        # Data storage
        self.order_books = {}  # {product_id: {'bids': [...], 'asks': [...]}}
        self.prices = {}       # {product_id: current_price}
        self.candles = {}      # {product_id: [candle_data...]}
        self.order_updates = {}# {order_id: order_status}

    def _generate_signature(self):
        # Depending on Coinbase's WebSocket auth requirements
        timestamp = str(int(time.time()))
        message = timestamp + 'GET' + '/users/self/verify'
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature).decode()
        return timestamp, signature_b64

    def _build_auth_message(self):
        # Check official docs for exact auth payload for private channels
        timestamp, signature = self._generate_signature()
        return {
            "type": "subscribe",
            "signature": signature,
            "key": self.api_key,
            "passphrase": self.passphrase,
            "timestamp": timestamp,
            "channels": self.channels
        }

    async def _connect(self):
        self._ws = await websockets.connect(self.uri)
        sub_msg = self._build_auth_message()
        await self._ws.send(json.dumps(sub_msg))

    async def _handle_message(self, msg: dict):
        try:
            msg_type = msg.get('type')
            
            if msg_type == 'ticker':
                # Enhanced ticker handling
                product_id = msg['product_id']
                self.prices[product_id] = {
                    'price': msg['price'],
                    'bid': msg.get('best_bid'),
                    'ask': msg.get('best_ask'),
                    'volume_24h': msg.get('volume_24h'),
                    'timestamp': msg.get('timestamp')
                }
            
            elif msg_type == 'match' or msg_type == 'trade':
                # Handle individual trades
                product_id = msg['product_id']
                if product_id not in self.trades:
                    self.trades[product_id] = []
                self.trades[product_id].append(msg)
                # Keep only recent trades (e.g., last 1000)
                self.trades[product_id] = self.trades[product_id][-1000:]
                
            elif msg_type == 'balance':
                # Update account balances
                currency = msg['currency']
                self.balances[currency] = {
                    'available': msg['available'],
                    'hold': msg.get('hold', '0')
                }
                
            elif msg_type == 'error':
                # Handle error messages
                print(f"WebSocket Error: {msg.get('message')}")
                # Implement reconnection logic
                await self._handle_error(msg)
                
        except Exception as e:
            print(f"Error handling message: {e}")

    async def _handle_error(self, error_msg):
        # Implement exponential backoff
        await asyncio.sleep(self.reconnect_delay)
        self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
        await self._connect()

    async def listen(self):
        while self._running:
            try:
                await self._connect()
                async for message in self._ws:
                    # Rate limiting
                    current_time = time.time()
                    if current_time - self.last_message_time < 0.1:  # Max 10 messages per second
                        await asyncio.sleep(0.1)
                    self.last_message_time = current_time
                    
                    msg = json.loads(message)
                    await self._handle_message(msg)
            except websockets.exceptions.ConnectionClosed:
                if self._running:
                    await asyncio.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
            except Exception as e:
                print(f"WebSocket error: {e}")
                if self._running:
                    await asyncio.sleep(self.reconnect_delay)

    def stop(self):
        self._running = False
        if self._ws:
            asyncio.create_task(self._ws.close())

# -----------------------
# Combined Wrapper
# -----------------------
class CoinbaseAdvancedTradeWrapper:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_client = APIClient(api_key, api_secret, passphrase)
        self.websocket_client = None
        self.loop = asyncio.get_event_loop()

    def start_websocket(self, product_ids: List[str]):
        # Define channels you want to subscribe to:
        # "level2" for order books
        # "ticker" for price changes
        # "user" for order updates (private channel)
        # "candles" for OHLC data if supported
        channels = [
            {"name": "level2", "product_ids": product_ids},
            {"name": "ticker", "product_ids": product_ids},
            {"name": "user"},  # authenticated user channel for your own orders
            {"name": "candles", "product_ids": product_ids, "interval": "ONE_MINUTE"} # adjust interval as needed
        ]

        self.websocket_client = WebsocketClient(
            self.api_client.api_key,
            self.api_client.api_secret,
            self.api_client.passphrase,
            channels
        )
        # Run websocket in background
        self.loop.create_task(self.websocket_client.listen())

    def get_order_status(self, order_id: str):
        return self.api_client.get_order_status(order_id)

    def get_order_book(self, product_id: str):
        if self.websocket_client:
            return self.websocket_client.order_books.get(product_id)
        return None

    def place_market_order(self, product_id: str, side: str, size: float):
        return self.api_client.place_market_order(product_id, side, size)

    def place_limit_order(self, product_id: str, side: str, size: float, price: float, expire_seconds: int = None):
        return self.api_client.place_limit_order(product_id, side, size, price, expire_seconds)

    def get_prices(self):
        if self.websocket_client:
            return self.websocket_client.prices
        return {}

    def get_candles(self, product_id: str):
        if self.websocket_client:
            return self.websocket_client.candles.get(product_id, [])
        return []

    def get_ohlcv_history(self, product_id: str, granularity=300, start=None, end=None):
        return self.api_client.get_ohlcv(product_id, granularity, start, end)

    def get_my_order_updates(self):
        if self.websocket_client:
            return self.websocket_client.order_updates
        return {}

    def get_account_balances(self):
        """Get current account balances"""
        if self.websocket_client:
            return self.websocket_client.balances
        return {}

    def get_recent_trades(self, product_id: str, limit: int = 100):
        """Get recent trades for a product"""
        if self.websocket_client:
            trades = self.websocket_client.trades.get(product_id, [])
            return trades[-limit:]
        return []

    def get_position(self, product_id: str):
        """Get current position for a product"""
        if self.websocket_client:
            return self.websocket_client.positions.get(product_id)
        return None

    async def wait_for_order_fill(self, order_id: str, timeout: float = 60.0):
        """Wait for an order to be filled with timeout"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if order_id in self.websocket_client.order_updates:
                status = self.websocket_client.order_updates[order_id].get('status')
                if status in ['filled', 'canceled', 'expired', 'rejected']:
                    return self.websocket_client.order_updates[order_id]
            await asyncio.sleep(0.1)
        raise TimeoutError(f"Order {order_id} did not complete within {timeout} seconds")

# -----------------------
# Example Usage
# -----------------------
if __name__ == "__main__":
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    PASSPHRASE = "your_passphrase"
    PRODUCT_IDS = ["BTC-USD", "ETH-USD"]

    wrapper = CoinbaseAdvancedTradeWrapper(API_KEY, API_SECRET, PASSPHRASE)

    # Start the websocket (in background)
    wrapper.start_websocket(PRODUCT_IDS)

    # Place a market order (example)
    # Note: This is a real trading action if you put real credentials and a funded account.
    # TEST THIS ON SANDBOX OR WITH CAUTION.
    # response = wrapper.place_market_order("BTC-USD", "BUY", 0.001)
    # print(response)

    # Get historical OHLCV data
    historical_candles = wrapper.get_ohlcv_history("BTC-USD", granularity=300)
    print("Historical Candles:", historical_candles)

    # You would need to run the event loop to keep the websocket alive:
    # If you're using Python 3.7+, you can do something like:
    try:
        wrapper.loop.run_forever()
    except KeyboardInterrupt:
        if wrapper.websocket_client:
            wrapper.websocket_client.stop()
        wrapper.loop.stop()
