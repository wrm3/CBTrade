import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

class PhemexClient:
    def __init__(self, api_key, api_secret, testnet=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.phemex.com"  # Live instance by default
        if testnet:
            self.base_url = "https://testnet-api.phemex.com"

    def _generate_signature(self, method, endpoint, params=None):
        timestamp = int(time.time() * 1000)
        params = params or {}
        params['api_key'] = self.api_key
        params['timestamp'] = timestamp

        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        signature_payload = f"{method}{endpoint}{query_string}"
        
        signature = hmac.new(self.api_secret.encode('utf-8'), signature_payload.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature, timestamp

    def _send_request(self, method, endpoint, params=None):
        params = params or {}
        signature, timestamp = self._generate_signature(method, endpoint, params)
        params['api_key'] = self.api_key
        params['timestamp'] = timestamp
        params['signature'] = signature

        url = f"{self.base_url}{endpoint}"
        
        if method == 'GET':
            response = requests.get(url, params=params)
        elif method == 'POST':
            response = requests.post(url, json=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()

    def place_long(self, symbol, quantity, leverage, price=None):
        endpoint = "/orders"
        params = {
            "symbol": symbol,
            "clOrdID": f"long_{int(time.time())}",
            "side": "Buy",
            "orderQty": quantity,
            "ordType": "Market" if price is None else "Limit",
            "leverage": leverage,
        }
        if price is not None:
            params["priceEp"] = int(price * 10000)  # Phemex uses scaled prices

        return self._send_request('POST', endpoint, params)

    def place_short(self, symbol, quantity, leverage, price=None):
        endpoint = "/orders"
        params = {
            "symbol": symbol,
            "clOrdID": f"short_{int(time.time())}",
            "side": "Sell",
            "orderQty": quantity,
            "ordType": "Market" if price is None else "Limit",
            "leverage": leverage,
        }
        if price is not None:
            params["priceEp"] = int(price * 10000)  # Phemex uses scaled prices

        return self._send_request('POST', endpoint, params)

    def cancel_position(self, symbol, order_id):
        endpoint = f"/orders/cancel"
        params = {
            "symbol": symbol,
            "orderID": order_id,
        }
        return self._send_request('POST', endpoint, params)

    def get_positions(self, symbol):
        endpoint = f"/accounts/positions"
        params = {"currency": symbol}
        return self._send_request('GET', endpoint, params)

    def get_available_funds(self):
        endpoint = "/accounts/accountPositions"
        response = self._send_request('GET', endpoint)
        
        # Extract USDT balance from the response
        for currency in response['data']:
            if currency['currency'] == 'USDT':
                available_balance = float(currency['balanceEv']) / 1e8  # Convert from 8 decimal places
                return available_balance
        
        return 0  # Return 0 if USDT balance is not found

def test_minimal_positions(api_key, api_secret, testnet=False):
    client = PhemexClient(api_key, api_secret, testnet)
    symbol = "BTCUSD"
    minimal_quantity = 1  # Adjust this based on Phemex's minimum order size for BTC
    leverage = 1  # Using minimal leverage

    try:
        # Get available funds
        available_funds = client.get_available_funds()
        print(f"Available USDT balance: {available_funds}")

        # Place a minimal long position
        print("Placing minimal long position...")
        long_order = client.place_long(symbol, quantity=minimal_quantity, leverage=leverage)
        print("Long order placed:", long_order)
        
        # Wait for the order to be filled (in a real scenario, you'd implement proper order status checking)
        time.sleep(5)
        
        # Switch to a minimal short position
        print("Switching to minimal short position...")
        short_order = client.place_short(symbol, quantity=minimal_quantity*2, leverage=leverage)  # *2 to close long and open short
        print("Short order placed:", short_order)
        
        # Wait for the order to be filled
        time.sleep(5)
        
        # Cancel the short position
        print("Canceling the short position...")
        cancel_result = client.cancel_position(symbol, short_order['data']['orderID'])
        print("Position cancelled:", cancel_result)
        
        # Get current positions
        positions = client.get_positions("BTC")
        print("Current positions after cancellation:", positions)

        # Get available funds again
        available_funds = client.get_available_funds()
        print(f"Available USDT balance after operations: {available_funds}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    api_key = "your_api_key"
    api_secret = "your_api_secret"
    
    # Set testnet to False for live trading (use with caution!)
    test_minimal_positions(api_key, api_secret, testnet=True)