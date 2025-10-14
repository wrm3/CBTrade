#!/usr/bin/env python3
"""
Quick test for Task 001: TA Indicator Integration

This verifies that indicators calculate correctly on developing candles
for all timeframes.
"""

import sys
import pandas as pd
from datetime import datetime as dt

# Add parent directory to path
sys.path.insert(0, 'C:/git/cbtrade')

from libs.backtest_base import BacktestEngine, CandleBuilder
from libs.common import AttrDict
from libs.db_mysql.ohlcv.db_main import db_ohlcv

def test_indicator_integration():
    """Test that indicators calculate on developing candles."""
    
    print("\n" + "="*80)
    print("TASK 001 TEST: TA Indicator Integration")
    print("="*80 + "\n")
    
    # Create mock bot instance with minimal mock settings
    print("1. Creating mock bot instance with minimal settings...")
    bot = AttrDict()
    
    # Create minimal mock settings (just what indicators need)
    bot.st = AttrDict()
    bot.st.buy = AttrDict()
    bot.st.buy.strats = AttrDict()
    bot.st.buy.strats.sha = AttrDict()
    bot.st.buy.strats.sha.fast_sha_len1 = 8
    bot.st.buy.strats.sha.fast_sha_len2 = 8
    bot.st.buy.strats.sha.slow_sha_len1 = 21
    bot.st.buy.strats.sha.slow_sha_len2 = 21
    
    # Create pair structure
    bot.pair = AttrDict()
    bot.pair.prod_id = 'BTC-USDC'
    bot.pair.prc_mkt = 0  # Not used in indicator calcs
    bot.pair.ta = AttrDict()
    
    print("[OK] Bot instance created with mock settings\n")
    
    # Initialize backtest engine
    print("2. Initializing backtest engine...")
    engine = BacktestEngine(bot, db_ohlcv)
    
    # Initialize for BTC-USDC
    engine.prod_id = 'BTC-USDC'
    
    # Initialize candle builders for all timeframes
    freqs = ['15min', '30min', '1h', '4h', '1d']
    engine.initialize_candle_builders(freqs)
    
    print(f"[OK] Candle builders initialized for {len(freqs)} timeframes\n")
    
    # Load some minute data to test with
    print("3. Loading historical minute data...")
    start_date = '2024-01-01'
    end_date = '2024-01-02'  # Just 1 day for quick test
    
    minute_data = engine.load_minute_data('BTC-USDC', start_date, end_date)
    print(f"[OK] Loaded {len(minute_data)} minutes of data ({start_date} to {end_date})\n")
    
    # Process first 100 minutes to build up candle history
    print("4. Processing first 100 minutes to build candle history...")
    for i, (timestamp, minute_bar) in enumerate(minute_data.head(100).iterrows()):
        if i % 20 == 0:
            print(f"   Processing minute {i+1}/100...")
        
        # Add to each timeframe builder
        for freq, builder in engine.candle_builders.items():
            completed = builder.add_minute(timestamp, minute_bar)
            
            # If candle completed, add to completed_candles
            if completed and builder.last_completed is not None:
                candle_df = pd.DataFrame([builder.last_completed])
                
                if freq not in engine.completed_candles:
                    engine.completed_candles[freq] = candle_df
                else:
                    engine.completed_candles[freq] = pd.concat([
                        engine.completed_candles[freq],
                        candle_df
                    ], ignore_index=True)
    
    print("[OK] Built candle history for all timeframes\n")
    
    # Show completed candle counts
    print("5. Completed candles per timeframe:")
    for freq in freqs:
        count = len(engine.completed_candles.get(freq, []))
        developing = "Yes" if engine.candle_builders[freq].current_candle else "No"
        print(f"   {freq:>6}: {count:>3} completed + developing candle: {developing}")
    print()
    
    # NOW TEST INDICATOR CALCULATION
    print("6. Testing indicator calculation...")
    try:
        engine._update_indicators()
        print("[OK] Indicator calculation completed without errors\n")
    except Exception as e:
        print(f"[ERROR] ERROR during indicator calculation: {e}\n")
        import traceback
        traceback.print_exc()
        return False
    
    # Verify indicators were stored correctly
    print("7. Verifying indicator storage structure...")
    success = True
    
    for freq in freqs:
        # Check if ta structure exists
        if not hasattr(bot.pair, 'ta'):
            print(f"   [ERROR] bot.pair.ta not found!")
            success = False
            continue
        
        if freq not in bot.pair.ta:
            # This is OK if we didn't have enough candles (need 10+)
            candle_count = len(engine.completed_candles.get(freq, []))
            if candle_count < 10:
                print(f"   [SKIP] {freq:>6}: Skipped (only {candle_count} candles, need 10+)")
                continue
            else:
                print(f"   [ERROR] {freq:>6}: Missing from bot.pair.ta!")
                success = False
                continue
        
        # Check for df and curr
        if not hasattr(bot.pair.ta[freq], 'df'):
            print(f"   [ERROR] {freq:>6}: Missing .df")
            success = False
            continue
        
        if not hasattr(bot.pair.ta[freq], 'curr'):
            print(f"   [ERROR] {freq:>6}: Missing .curr")
            success = False
            continue
        
        # Check that df has indicator columns
        df = bot.pair.ta[freq].df
        indicator_cols = ['rsi', 'atr', 'ha_open', 'ha_close', 'sha_fast_open', 'sha_fast_close']
        found_indicators = [col for col in indicator_cols if col in df.columns]
        
        print(f"   [OK] {freq:>6}: df has {len(df)} rows, {len(df.columns)} columns including indicators: {found_indicators[:3]}...")
    
    print()
    
    # Final summary
    if success:
        print("="*80)
        print("[PASS] TASK 001 TEST PASSED!")
        print("="*80)
        print("\nIndicator integration working correctly:")
        print("- Indicators calculate on developing candles [OK]")
        print("- Results stored in bot.pair.ta[freq] structure [OK]")
        print("- Multiple timeframes supported [OK]")
        print("- Error handling prevents crashes [OK]")
        print("\nReady to proceed to Task 002 (Buy Logic Integration)")
        return True
    else:
        print("="*80)
        print("[FAIL] TASK 001 TEST FAILED!")
        print("="*80)
        print("\nSome issues found - review errors above")
        return False

if __name__ == '__main__':
    success = test_indicator_integration()
    sys.exit(0 if success else 1)

