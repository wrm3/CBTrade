import time
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
import os
from coinbase.websocket import WSUserClient
from datetime import datetime
from coinbase.rest import RESTClient
import asyncio

# Load environment variables
load_dotenv()
API_KEY = os.getenv('COINBASE_API_KEY')
SIGNING_KEY = os.getenv('COINBASE_API_SECRET')

class CustomWSUserClient(WSUserClient):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key=api_key, api_secret=api_secret)
        self.order_updates = {}
        self.tracked_orders = set()
        
    def on_message(self, msg):
        """Handle incoming WebSocket messages"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{'='*80}")
        print(f"[{current_time}] NEW WEBSOCKET MESSAGE")
        print(f"{'='*80}")
        
        try:
            # Parse message if it's a string
            data = json.loads(msg) if isinstance(msg, str) else msg
            
            # Log the raw message for debugging
            print("\nPARSED MESSAGE:")
            print(json.dumps(data, indent=2))
            
            channel = data.get('channel')
            events = data.get('events', [])
            
            if channel == "user":
                for event in events:
                    order_id = event.get('order_id')
                    if order_id:
                        if order_id not in self.order_updates:
                            self.order_updates[order_id] = []
                        self.order_updates[order_id].append(event)
                        print(f"\nORDER UPDATE - {event.get('type', 'unknown')}:")
                        print(f"Order ID: {order_id}")
                        print(f"Status: {event.get('status')}")
                        print(f"Side: {event.get('side')}")
                        print(f"Product: {event.get('product_id')}")
                        if 'price' in event:
                            print(f"Price: {event['price']}")
                        if 'size' in event:
                            print(f"Size: {event['size']}")
                        
        except Exception as e:
            print(f"Error processing message: {e}")
                    
    def on_error(self, error):
        """Handle WebSocket errors"""
        print(f"\nWebSocket Error: {error}")
        
    def on_close(self):
        """Handle WebSocket connection closing"""
        print("\nWebSocket Connection Closed")
        
    def on_open(self):
        """Handle WebSocket connection opening"""
        print("\nWebSocket Connection Opened")
        
    def track_order(self, order_id: str):
        """Track a specific order ID"""
        self.tracked_orders.add(order_id)
        
    def get_order_updates(self, order_id: str) -> List[Dict]:
        """Get updates for a specific order"""
        return self.order_updates.get(order_id, [])

class CoinbaseWebSocketManager:
    def __init__(self):
        self.ws_client = CustomWSUserClient(api_key=API_KEY, api_secret=SIGNING_KEY)
        self.rest_client = RESTClient(api_key=API_KEY, api_secret=SIGNING_KEY)
        self._running = False
        
    async def start(self):
        """Start the WebSocket connection"""
        self._running = True
        
        try:
            print("\nStarting WebSocket connection...")
            await asyncio.get_event_loop().run_in_executor(
                None, 
                self.ws_client.open
            )
            
            while self._running:
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        self.ws_client.run_forever_with_exception_check
                    )
                except Exception as e:
                    print(f"WebSocket error, attempting to reconnect: {e}")
                    await asyncio.sleep(5)
                    
        except Exception as e:
            print(f"Error in WebSocket manager: {e}")
            
    async def stop(self):
        """Stop the WebSocket connection"""
        self._running = False
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                self.ws_client.close
            )
        except Exception as e:
            print(f"Error closing WebSocket: {e}")
            
    def limit_buy(self, product_id: str, base_size: float, limit_price: float) -> Dict:
        """Place a limit buy order"""
        try:
            client_order_id = f"buy_{int(time.time()*1000)}"
            
            response = self.rest_client.limit_order_gtc(
                client_order_id=client_order_id,
                product_id=product_id,
                side='BUY',
                base_size=str(base_size),
                limit_price=str(limit_price)
            )
            
            if not isinstance(response, dict):
                response = response.__dict__
                
            if response and 'success_response' in response:
                order_id = response['success_response']['order_id']
                self.ws_client.track_order(order_id)
                print(f"\nOrder placed successfully:")
                print(f"Order ID: {order_id}")
                print(f"Product: {response['success_response']['product_id']}")
                print(f"Side: {response['success_response']['side']}")
                print(f"Size: {response['order_configuration']['limit_limit_gtc']['base_size']}")
                print(f"Price: {response['order_configuration']['limit_limit_gtc']['limit_price']}")
            return response
            
        except Exception as e:
            print(f"Error placing limit buy order: {e}")
            return None

# Example usage
if __name__ == "__main__":
    async def test():
        manager = CoinbaseWebSocketManager()
        
        # Start WebSocket connection
        ws_task = asyncio.create_task(manager.start())
        
        # Wait for connection
        await asyncio.sleep(5)
        
        try:
            # Place test order
            order = manager.limit_buy(
                product_id="BTC-USDC",
                base_size=0.00001,
                limit_price=10000
            )
            
            # Keep running to receive updates
            await asyncio.sleep(30)
            
        finally:
            await manager.stop()
            ws_task.cancel()
    
    asyncio.run(test())
