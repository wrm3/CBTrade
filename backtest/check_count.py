#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libs.bot_db_ohlcv import db_ohlcv
result = db_ohlcv.seld("SELECT COUNT(*) as cnt FROM ohlcv_BTC_USDC WHERE freq='1min'")
print(f"Current count: {result[0]['cnt']:,} candles")
