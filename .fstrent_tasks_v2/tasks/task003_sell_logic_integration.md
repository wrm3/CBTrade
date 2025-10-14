---
id: 003
title: 'Sell Logic Integration'
type: task
status: pending
priority: critical
feature: Core Engine
subsystems:
  - Backtesting Engine
  - Sell Logic
project_context: Integrate sell_strats_check() to detect exit signals for open positions with accurate P&L calculation
dependencies:
  - 001
  - 002
assigned_agent: null
created_at: "2025-10-10T18:40:00Z"
started_at: null
completed_at: null
error_log: null
complexity_score: 6
expansion_decision: null
memory_consultation: Reviewed sell_base.py - multiple exit types handled
story_points: 2
sprint: Phase 2a
---

# Task 003: Sell Logic Integration

## Description

Integrate `sell_strats_check()` from `libs/sell_base.py` to detect exit signals for open positions. Handles strategy exits, stop losses, take profits with accurate P&L calculation. Updates balance and closes positions.

**Location:** `libs/backtest_base.py` line 278 (TODO comment)

## Details

### Current State (TODO):
```python
# TODO: Integrate sell logic
# Check sell_strats_check() for each open position
# Handle stop loss, take profit, strategy exits
# Calculate P&L, update balance
```

### Required Implementation:

1. **Iterate Through Open Positions**:
   ```python
   for position in self.open_positions:
       # Check if should sell this position
   ```

2. **Call Sell Strategy Check**:
   ```python
   from libs.strat_base import sell_strats_check
   
   sell_signal = sell_strats_check(
       bot=self.bot,
       position=position,
       current_price=minute_bar['close_prc']
   )
   ```

3. **Check Stop Loss / Take Profit**:
   ```python
   # Stop loss check
   if 'stop_loss' in position and minute_bar['low_prc'] <= position['stop_loss']:
       exit_price = position['stop_loss']
       exit_reason = 'stop_loss'
       should_sell = True
   
   # Take profit check
   elif 'take_profit' in position and minute_bar['high_prc'] >= position['take_profit']:
       exit_price = position['take_profit']
       exit_reason = 'take_profit'
       should_sell = True
   
   # Strategy exit check
   elif sell_signal:
       exit_price = minute_bar['close_prc']
       exit_reason = sell_signal.reason
       should_sell = True
   ```

4. **Execute Sell and Calculate P&L**:
   ```python
   if should_sell:
       # Calculate P&L
       pnl = (exit_price - position['entry_price']) * position['size']
       pnl_pct = ((exit_price - position['entry_price']) / position['entry_price']) * 100
       
       # Update balance (add back proceeds)
       sale_proceeds = exit_price * position['size']
       self.current_balance += sale_proceeds
       
       # Record trade
       trade = {
           'prod_id': position['prod_id'],
           'strategy': position['strategy'],
           'entry_time': position['entry_time'],
           'entry_price': position['entry_price'],
           'exit_time': timestamp,
           'exit_price': exit_price,
           'exit_reason': exit_reason,
           'size': position['size'],
           'pnl': pnl,
           'pnl_pct': pnl_pct,
           'hold_time_minutes': (timestamp - position['entry_time']).total_seconds() / 60
       }
       
       self.closed_trades.append(trade)
       
       # Remove from open positions
       self.open_positions.remove(position)
   ```

5. **Handle All Exit Types**:
   - Strategy exit signal (indicator-based)
   - Stop loss hit (price dropped to stop level)
   - Take profit hit (price reached target)
   - Time-based exit (if strategy has max hold time)
   - Emergency exit (if strategy performance degrades)

### Integration Points:
- **Input:** Open positions (from Task 002), current price, bot state with indicators
- **Process:** Call `sell_strats_check()`, check stops, calculate P&L, close position
- **Output:** Closed trades with P&L, updated balance, updated open positions list
- **Used By:** Performance metrics calculation (already implemented)

## Test Strategy

### Unit Tests:
1. **Test strategy exit detection**:
   - Mock position and indicator values that trigger exit
   - Call sell logic
   - Verify exit signal detected

2. **Test stop loss**:
   - Create position with stop loss
   - Set current price below stop
   - Verify position closed at stop price
   - Verify negative P&L calculated

3. **Test take profit**:
   - Create position with take profit
   - Set current price above target
   - Verify position closed at target price
   - Verify positive P&L calculated

4. **Test P&L calculation**:
   - Entry: $65,000 @ 0.1 BTC
   - Exit: $66,000 @ 0.1 BTC
   - Expected P&L: $100 (+1.54%)
   - Verify calculation accurate

### Integration Tests:
1. **Test complete buy-sell cycle**:
   - Start backtest with balance
   - Buy signal triggers (Task 002)
   - Position opened, balance decremented
   - Later, sell signal triggers (Task 003)
   - Position closed, P&L added to balance
   - Verify balance = starting + P&L

2. **Test multiple concurrent positions**:
   - Open 3 positions on different strategies
   - Close them at different times
   - Verify each P&L calculated correctly
   - Verify balance tracks all sales

3. **Test with real strategy**:
   - Use known strategy (e.g., `sha`)
   - Run on known period
   - Verify sell count matches buy count (eventually)
   - Verify no positions left open at end
   - Verify cumulative P&L makes sense

## Agent Notes

### Files to Modify:
- `libs/backtest_base.py` - Line 278, `process_minute()` method

### Files to Reference:
- `libs/sell_base.py` - `sell_strats_check()` and exit logic
- `libs/strat_base.py` - Strategy-specific exit conditions
- `libs/bot_base.py` - BOT class with all sell logic methods integrated

### Key Considerations:
- **P&L Accuracy:** Critical for performance metrics
  - Must account for exact entry and exit prices
  - Must track position size correctly
  - Must handle partial exits (if implemented)
  
- **Balance Updates:** Must be precise
  - Add back full sale proceeds (price × size)
  - Should end backtest with balance ≈ starting + total_pnl
  
- **Stop Loss vs Take Profit Priority:**
  - If both would trigger same minute, which executes first?
  - Typically check low (stop) before high (target)
  - Or use actual minute progression if available

- **Mid-Candle Exits:** 
  - Stop loss can trigger mid-candle (use candle's low)
  - Take profit can trigger mid-candle (use candle's high)
  - Strategy exit typically uses close price

- **Position Tracking:**
  - Remove from open_positions immediately on close
  - Add to closed_trades for metrics
  - Ensure no duplicate closes

### Complexity Analysis:
**Score: 6/10**
- **Moderate:** Call existing sell logic (not rewriting)
- **Complex:** Accurate P&L calculation
- **Moderate:** Multiple exit types (stop/target/strategy)
- **Simple:** Balance update straightforward

### Estimated Time: 1.0 hour
- 20 min: Study existing sell logic in live bot
- 30 min: Implement integration in backtest engine
- 10 min: Unit tests and P&L validation

## Memory Context

**Historical Insights:** Sell logic well-tested in live trading. P&L calculations verified accurate.

**Related Work:**
- Sell logic handles stop losses, take profits, strategy exits
- Some strategies have time-based exits (max hold period)
- P&L tracking feeds into strategy performance metrics
- Recent work: Trade size boosting based on historical P&L

**Known Challenges:**
- Ensuring stop losses trigger at correct price (candle low, not close)
- Take profits should trigger at candle high (if hit during minute)
- Some strategies don't set stops/targets (rely on indicator exits)
- Need to handle case where strategy wants to exit but price gaps past stop

---

**Created:** 2025-10-10 18:40 UTC  
**Priority:** Critical (Required for complete backtest cycle)  
**Complexity:** 6/10 (Position tracking and P&L calculation)

