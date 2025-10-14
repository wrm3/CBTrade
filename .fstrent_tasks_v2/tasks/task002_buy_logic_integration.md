---
id: 002
title: 'Buy Logic Integration'
type: task
status: pending
priority: critical
feature: Core Engine
subsystems:
  - Backtesting Engine
  - Buy Logic
project_context: Integrate buy_strats_check() to detect buy signals at exact minute conditions are met
dependencies:
  - 001
assigned_agent: null
created_at: "2025-10-10T18:40:00Z"
started_at: null
completed_at: null
error_log: null
complexity_score: 6
expansion_decision: null
memory_consultation: Reviewed buy_base.py functions - extensive logic already implemented
story_points: 3
sprint: Phase 2a
---

# Task 002: Buy Logic Integration

## Description

Integrate `buy_strats_check()` from `libs/buy_base.py` to detect buy signals at the exact minute conditions are met. Respects all buy denials, timing delays, budget constraints, test mode logic, and position sizing from the live trading system.

**Location:** `libs/backtest_base.py` line 263 (TODO comment)

## Details

### Current State (TODO):
```python
# TODO: Integrate buy logic
# Check buy_strats_check() for signals
# Respect all buy denials, timing delays, boosts
# Handle budget constraints
```

### Required Implementation:

1. **Check Budget Availability**:
   ```python
   if self.current_balance < minimum_trade_size:
       continue  # Skip if no budget
   ```

2. **Call Buy Strategy Check**:
   ```python
   from libs.strat_base import buy_strats_check
   
   # Prepare buy object (similar to live trading)
   buy_signals = buy_strats_check(
       bot=self.bot,
       prod_id=self.prod_id,
       current_price=minute_bar['close_prc']
   )
   ```

3. **Process Buy Signals**:
   - Filter for valid signals (not denied, not on cooldown)
   - Calculate trade size using `buy_size_budget_calc()`
   - Apply strategy-specific boosts (if applicable)
   - Respect 5x minimum trade size rule

4. **Execute Simulated Buy**:
   ```python
   if buy_signal_valid:
       position = {
           'prod_id': self.prod_id,
           'strategy': buy_signal.strat_name,
           'entry_time': timestamp,
           'entry_price': minute_bar['close_prc'],
           'size': trade_size,
           'entry_balance': self.current_balance
       }
       
       # Deduct from balance
       self.current_balance -= (trade_size * minute_bar['close_prc'])
       
       # Track position
       self.open_positions.append(position)
       self.orders.append({
           'type': 'buy',
           'timestamp': timestamp,
           'price': minute_bar['close_prc'],
           'size': trade_size,
           'strategy': buy_signal.strat_name
       })
   ```

5. **Handle All Buy Denials**:
   - Timing delays (product-level and strategy-level)
   - Open position limits
   - Test mode logic (if strategy hasn't proven profitability)
   - Market-specific denials
   - Strategy-specific denials

### Integration Points:
- **Input:** Bot state with indicators (from Task 001), current balance, open positions
- **Process:** Call `buy_strats_check()`, apply budget logic, create position
- **Output:** New open positions, updated balance, order history
- **Used By:** Task 003 (sell logic needs open positions)

## Test Strategy

### Unit Tests:
1. **Test buy signal detection**:
   - Mock indicator values that trigger buy
   - Call buy logic
   - Verify signal detected

2. **Test buy denials**:
   - Test timing delay denial (recent buy)
   - Test budget constraint denial (insufficient funds)
   - Test open position limit denial (too many open)
   - Verify no position opened when denied

3. **Test trade size calculation**:
   - Test minimum trade size enforcement (5x rule)
   - Test budget-constrained trade size
   - Test strategy boost application
   - Verify size calculations match live bot logic

### Integration Tests:
1. **Test first buy of backtest**:
   - Start with $10,000 balance
   - Run until first buy signal
   - Verify position opened correctly
   - Verify balance decremented

2. **Test multiple buys**:
   - Run for longer period
   - Verify multiple positions can open
   - Verify each deducts from balance
   - Verify position limit respected

3. **Test with real strategy**:
   - Use known strategy (e.g., `bb_bo`)
   - Run on known period with expected signals
   - Verify buy count in reasonable range
   - Verify entry prices match minute close prices

## Agent Notes

### Files to Modify:
- `libs/backtest_base.py` - Line 263, `process_minute()` method

### Files to Reference:
- `libs/buy_base.py` - `buy_strats_check()`, `buy_size_budget_calc()`, `buy_live()`
- `libs/strat_base.py` - `buy_strats_avail_get()` to get active strategies
- `libs/budget_base.py` - Budget calculation logic
- `libs/bot_base.py` - BOT class with all buy logic methods integrated

### Key Considerations:
- **Budget Tracking:** Must accurately track available balance
  - Deduct trade cost immediately on buy
  - Add back sale proceeds on sell (Task 003)
  
- **Position Tracking:** Need to track:
  - Entry time, entry price, size, strategy
  - Link to buy signal that triggered it
  - Available for sell logic to check

- **Buy Denials:** Many reasons buy can be denied:
  - Recent buy on same product (timing delay)
  - Recent buy with same strategy (strategy delay)
  - Too many open positions (global or per-strategy)
  - Test mode (strategy hasn't proven profitability)
  - Insufficient budget (can't afford 5x minimum)
  - Market-specific denial (e.g., high volatility)

- **Backtest Mode Flag:** Need to ensure `buy_live()` doesn't place real orders
  - Check `self.bot.backtest_mode == True`
  - Simulate fill instead of API call
  - Return simulated order result

### Complexity Analysis:
**Score: 6/10**
- **Moderate:** Call existing buy logic (not rewriting)
- **Complex:** Budget and position tracking
- **Moderate:** Handling all denial conditions
- **Moderate:** Trade size calculation with boosts

### Estimated Time: 1.5 hours
- 30 min: Study existing buy logic in live bot
- 45 min: Implement integration in backtest engine
- 15 min: Unit tests and validation

## Memory Context

**Historical Insights:** Buy logic extensively tested in live trading (10+ months).

**Related Work:**
- Buy logic includes 8+ denial categories
- Trade size boosting based on strategy performance
- Test mode graduation system (strategies must prove profitability)
- Recent changes: 5x minimum trade size enforcement, profitability threshold made configurable

**Known Challenges:**
- Budget tracking can be complex with multiple concurrent positions
- Buy denials need careful handling (don't want false signals)
- Trade size boosts can lead to very large positions for high performers
- Test mode logic needs to work in backtest context (no live performance data yet)

---

**Created:** 2025-10-10 18:40 UTC  
**Priority:** Critical (Blocks Task 003)  
**Complexity:** 6/10 (Budget tracking and signal detection)

