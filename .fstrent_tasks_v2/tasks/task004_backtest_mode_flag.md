---
id: 004
title: 'Backtest Mode Flag'
type: task
status: pending
priority: high
feature: Safety
subsystems:
  - Bot Core
  - Buy Logic
  - API Wrapper
project_context: Add backtest_mode flag to prevent real Coinbase API calls during backtests
dependencies:
  - 002
assigned_agent: null
created_at: "2025-10-10T18:40:00Z"
started_at: null
completed_at: null
error_log: null
complexity_score: 3
expansion_decision: null
memory_consultation: Simple flag check - minimal complexity
story_points: 1
sprint: Phase 2b
---

# Task 004: Backtest Mode Flag

## Description

Add `backtest_mode` flag to Bot class and modify `buy_live()` to prevent real Coinbase API calls during backtests. Simulates order fills instead of placing real orders. **Critical safety feature** to prevent accidental real trades during testing.

## Details

### Safety Requirement:
**MUST prevent ANY real Coinbase API calls when backtest_mode=True**

This includes:
- ❌ Real order placement (`buy_live()`, `sell_live()`)
- ❌ Real order cancellation
- ❌ Real order status checks
- ✅ Simulated order fills (instant, at current price)

### Required Implementation:

1. **Add Flag to Bot Class**:
   ```python
   # In libs/bot_base.py - BOT.__init__()
   
   class BOT:
       def __init__(self, mode='full'):
           self.backtest_mode = False  # Add this line
           # ... rest of init
   ```

2. **Modify buy_live() Function**:
   ```python
   # In libs/buy_base.py
   
   def buy_live(bo):
       """Execute buy order (real or simulated based on backtest_mode)"""
       
       # SAFETY CHECK: Prevent real orders in backtest mode
       if bo.bot.backtest_mode:
           # Simulate instant fill at current price
           simulated_order = {
               'order_id': f'BACKTEST_{timestamp}',
               'prod_id': bo.prod_id,
               'side': 'buy',
               'size': bo.trade_size,
               'price': bo.buy_prc,
               'filled_size': bo.trade_size,
               'status': 'filled',
               'created_at': timestamp,
               'filled_at': timestamp,
               'fees': 0.0  # Simplified for backtest
           }
           return simulated_order
       
       # Real order placement (live trading only)
       else:
           # Existing Coinbase API call
           order = coinbase_api.place_order(...)
           return order
   ```

3. **Modify sell_live() Function** (if exists):
   ```python
   # In libs/sell_base.py (or similar)
   
   def sell_live(position, price):
       """Execute sell order (real or simulated)"""
       
       if bot.backtest_mode:
           # Simulate instant fill
           simulated_order = {
               'order_id': f'BACKTEST_{timestamp}',
               'prod_id': position['prod_id'],
               'side': 'sell',
               'size': position['size'],
               'price': price,
               'filled_size': position['size'],
               'status': 'filled'
           }
           return simulated_order
       else:
           # Real Coinbase API call
           order = coinbase_api.place_order(...)
           return order
   ```

4. **Add Safety Warnings**:
   ```python
   # In libs/backtest_base.py - BacktestEngine.__init__()
   
   def __init__(self, bot_instance, ...):
       # CRITICAL: Set backtest mode to prevent real trades
       if not bot_instance.backtest_mode:
           logger.warning("⚠️  WARNING: backtest_mode=False! Setting to True for safety.")
           bot_instance.backtest_mode = True
       
       # Double-check it's set
       assert bot_instance.backtest_mode == True, "SAFETY: backtest_mode must be True!"
   ```

### Integration Points:
- **Input:** Bot instance (from BacktestEngine)
- **Process:** Check flag before API calls
- **Output:** Simulated orders (backtest) or real orders (live)
- **Used By:** Task 002 (buy logic), Task 003 (sell logic)

## Test Strategy

### Unit Tests:
1. **Test flag initialization**:
   - Create Bot instance
   - Set `backtest_mode = True`
   - Verify flag accessible

2. **Test simulated buy**:
   - Set `backtest_mode = True`
   - Call `buy_live()`
   - Verify returns simulated order
   - Verify NO real API call made

3. **Test simulated sell**:
   - Set `backtest_mode = True`
   - Call `sell_live()`
   - Verify returns simulated order
   - Verify NO real API call made

### Safety Tests (CRITICAL):
1. **Test backtest engine forces flag**:
   - Create Bot with `backtest_mode = False`
   - Initialize BacktestEngine with this bot
   - Verify BacktestEngine sets flag to True
   - Verify assertion passes

2. **Test flag prevents real orders**:
   - Mock Coinbase API
   - Set `backtest_mode = True`
   - Trigger buy signal
   - Verify Coinbase API NOT called
   - Verify simulated order returned

3. **Test live trading still works**:
   - Set `backtest_mode = False`
   - Trigger buy signal (in test environment!)
   - Verify real order path executes
   - (Don't actually place real order in test!)

## Agent Notes

### Files to Modify:
- `libs/bot_base.py` - Add `self.backtest_mode = False` to `BOT.__init__()`
- `libs/buy_base.py` - Modify `buy_live()` to check flag
- `libs/sell_base.py` - Modify `sell_live()` to check flag (if exists)
- `libs/backtest_base.py` - Add safety assertion in `BacktestEngine.__init__()`

### Files to Reference:
- `libs/bot_coinbase.py` - See where API calls happen
- `libs/buy_base.py` - Current `buy_live()` implementation
- Live trading flow to understand order placement

### Key Considerations:
- **Absolute Safety:** This is THE most critical safety feature
  - Prevents accidentally placing real $65,000 BTC orders during testing
  - Must have multiple layers of protection
  - Assertions to catch programming errors

- **Simulated Order Format:** Must match real order structure
  - Strategies may check order fields
  - Need 'status': 'filled', 'filled_size', etc.
  - Keep it simple but sufficient

- **Fees:** Real orders have fees, backtests might skip
  - Could add 0.6% fee to simulated orders for realism
  - Or start with 0% and add later if needed

- **Slippage:** Real orders may have slippage (price moved)
  - Backtests assume instant fill at desired price
  - Could add random slippage for realism later
  - Start simple: instant fill at exact price

- **Testing:** Cannot test real order prevention without risking real order!
  - Use mocks to verify API not called
  - Manual code review critical
  - Maybe add "test" mode separate from "backtest" mode?

### Complexity Analysis:
**Score: 3/10**
- **Simple:** Just a flag check
- **Simple:** Simulated order is just a dict
- **Critical:** But safety is absolutely essential
- **Simple:** Minimal code changes

### Estimated Time: 0.5 hours
- 15 min: Add flag to Bot class and buy/sell functions
- 10 min: Add safety assertions in BacktestEngine
- 5 min: Unit tests for flag check

## Memory Context

**Historical Insights:** Live trading bot has run 10+ months without accidental order issues.

**Related Work:**
- Recent incidents where AI accidentally killed all Python processes
- Need multiple safety layers to prevent catastrophic mistakes
- The user EXPLICITLY cares about safety (runs income-generating system)

**Known Challenges:**
- Simulated orders need to look "real enough" for strategy logic
- Testing real order prevention is hard (can't risk real order)
- Need to maintain this safety as code evolves

**Safety Priority:**
```
┌────────────────────────────────────────┐
│  CRITICAL SAFETY RULE:                 │
│  NO REAL ORDERS DURING BACKTESTS       │
│  EVER. PERIOD.                         │
│                                        │
│  Multiple checks:                      │
│  1. Bot.backtest_mode flag             │
│  2. BacktestEngine assertion           │
│  3. buy_live() checks flag             │
│  4. sell_live() checks flag            │
└────────────────────────────────────────┘
```

---

**Created:** 2025-10-10 18:40 UTC  
**Priority:** High (Safety critical)  
**Complexity:** 3/10 (Simple flag check, but safety-critical)

