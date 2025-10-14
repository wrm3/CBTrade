# Backtesting System Implementation Plan

## Overview

This document outlines the implementation plan for a **minute-by-minute multi-timeframe backtesting system** for your trading strategies. This system will accurately simulate how your repainting indicators and multi-timeframe logic would have performed historically.

---

## Architecture

### Core Components

1. **`libs/backtest_base.py`** (NEW)
   - `BacktestEngine` class: Main backtesting engine
   - `backtest_strategy()`: Entry point function
   - Minute-by-minute simulation loop
   - Multi-timeframe candle builder
   - Integration with existing buy/sell logic
   - Performance metrics calculation

2. **`libs/bot_db_ohlcv.py`** (EXISTING)
   - Already has OHLCV data storage
   - Will need data backfilling functions
   - Minute-by-minute data retrieval

3. **`libs/buy_base.py` / `libs/sell_base.py`** (EXISTING)
   - NO CHANGES NEEDED to core logic
   - Just need `backtest_mode` flag to prevent real API calls
   - All existing buy/sell conditions work as-is

4. **`libs/strat_base.py`** (EXISTING)
   - NO CHANGES NEEDED
   - All strategies work as-is in backtest mode

---

## Implementation Phases

### Phase 1: Data Backfilling (Days 1-3)

**Goal:** Fill OHLCV database with historical minute data

**Tasks:**
1. Create `backfill_ohlcv.py` script
2. Use Coinbase API to fetch historical minute candles
3. Start with limited pairs: BTC-USDC, ETH-USDC, SOL-USDC
4. Fetch 6-12 months of data per pair
5. Store in existing OHLCV database structure

**Estimated API Calls:**
- Per pair: ~6 months × 30 days × 24 hours × 60 minutes = ~260,000 candles
- Coinbase API limits: 300 candles per request
- ~867 API calls per pair × 3 pairs = ~2,600 total API calls
- Rate limit: 10 requests/second = ~4-5 minutes total download time

**Commands to Run:**
```bash
# Backfill BTC-USDC for 6 months
uv run python backfill_ohlcv.py BTC-USDC --days=180

# Backfill all test pairs
uv run python backfill_ohlcv.py BTC-USDC ETH-USDC SOL-USDC --days=180
```

**Validation:**
- Verify no gaps in minute data
- Check data consistency (OHLC relationships)
- Ensure all timeframes can be derived from 1-minute data

---

### Phase 2: Core Backtesting Engine (Days 4-7)

**Goal:** Build the minute-by-minute simulation loop

**Tasks:**
1. Implement `BacktestEngine` class in `libs/backtest_base.py`
2. Create multi-timeframe candle builder
   - Takes 1-minute candles as input
   - Builds developing 5min, 15min, 1h, 4h, 1d candles
   - Simulates how candles form over time (critical for repainting indicators)
3. Integrate with existing `Bot` class
4. Add `backtest_mode` flag throughout codebase
5. Implement portfolio tracking (cash + positions)

**Key Logic:**
```python
# For each minute timestamp:
for current_minute in all_minutes:
    # 1. Update all developing candles
    candles_1m, candles_5m, candles_15m, ... = build_multi_tf_candles(current_minute)
    
    # 2. Update technical indicators (TA will recalculate based on developing candles)
    bot.update_indicators(candles)
    
    # 3. Check sell signals first (existing positions)
    for position in open_positions:
        sell_signal = sell_strats_check(bot, position)
        if sell_signal:
            close_position(position)
    
    # 4. Check buy signals (if we have budget)
    buy_signal = buy_strats_check(bot, prod_id)
    if buy_signal and has_budget():
        open_position(buy_signal)
```

**Testing:**
```bash
# Test 1 day of BTC-USDC
uv run python test_backtest_engine.py BTC-USDC --start=2024-10-01 --end=2024-10-02

# Test 1 week
uv run python test_backtest_engine.py BTC-USDC --start=2024-10-01 --end=2024-10-08
```

---

### Phase 3: Integration with Existing Logic (Days 8-10)

**Goal:** Ensure backtest engine uses actual buy/sell logic

**Tasks:**
1. Add `backtest_mode` flag to `Bot` class
2. Modify API calls to be skipped in backtest mode
3. Ensure `buy_main()` works in backtest without real orders
4. Ensure `sell_strats_check()` works with simulated positions
5. Test mode vs deny mode logic (should work as-is)
6. Budget calculations (should work as-is)

**Changes to Existing Code:**
```python
# In buy_base.py - buy_live() function
def buy_live(bo):
    if bo.bot.backtest_mode:
        # Don't actually place order
        # Just record the trade signal
        return simulate_order_fill(bo)
    else:
        # Existing real order logic
        return place_real_order(bo)

# In bot_base.py - BOT class
class BOT:
    def __init__(self):
        self.backtest_mode = False  # Add this flag
        # ... rest of initialization
```

**Testing:**
```bash
# Run backtest with all strategies
uv run python backtest_example.py

# Should show buy/sell signals from existing strats
# Without placing real orders
```

---

### Phase 4: Performance Metrics & Reporting (Days 11-13)

**Goal:** Calculate standard backtesting metrics

**Tasks:**
1. Implement metrics calculation functions:
   - Total return (%)
   - Win rate (%)
   - Average win/loss ($)
   - Profit factor
   - Max drawdown (%)
   - Sharpe ratio
   - Number of trades
2. Generate equity curve (balance over time)
3. Per-strategy performance breakdown
4. Export results to JSON/CSV
5. Create visualization (optional)

**Output Format:**
```json
{
  "prod_id": "BTC-USDC",
  "start_date": "2024-04-01",
  "end_date": "2024-10-01",
  "starting_balance": 10000.0,
  "ending_balance": 12450.50,
  "total_return_pct": 24.51,
  "total_trades": 156,
  "winning_trades": 98,
  "losing_trades": 58,
  "win_rate": 62.82,
  "avg_win": 87.32,
  "avg_loss": -45.67,
  "profit_factor": 1.91,
  "max_drawdown": -12.34,
  "sharpe_ratio": 1.45,
  "equity_curve": [
    {"timestamp": "2024-04-01T00:00:00Z", "equity": 10000.0},
    ...
  ],
  "strategy_breakdown": {
    "nwe_env": {"trades": 45, "return_pct": 8.2},
    "bb_bo": {"trades": 32, "return_pct": 5.1},
    ...
  }
}
```

---

### Phase 5: Strategy Optimization (Days 14-20)

**Goal:** Find optimal settings for each strategy

**Tasks:**
1. Create parameter grid for each strategy
2. Implement grid search backtesting
3. Rank parameter combinations by performance
4. Generate optimization report
5. Save optimal settings to strategy configs

**Example:**
```python
# Optimize RSI strategy parameters
param_grid = {
    'rsi_period': [10, 14, 20, 25],
    'rsi_buy_threshold': [25, 30, 35],
    'rsi_sell_threshold': [65, 70, 75],
}

# Run backtest for each combination
best_params = optimize_strategy('sha', param_grid, prod_id='BTC-USDC')

# Output:
# Best parameters for 'sha' on BTC-USDC:
#   rsi_period: 14
#   rsi_buy_threshold: 30
#   rsi_sell_threshold: 70
#   Total return: 28.5%
#   Win rate: 65.2%
```

**Commands:**
```bash
# Optimize single strategy
uv run python optimize_strategy.py --strategy=sha --pair=BTC-USDC

# Optimize all strategies
uv run python optimize_all_strategies.py --pairs=BTC-USDC,ETH-USDC,SOL-USDC
```

---

### Phase 6: Walk-Forward Testing (Days 21-25)

**Goal:** Prevent overfitting, validate on unseen data

**Tasks:**
1. Implement walk-forward analysis
2. Train on historical data (in-sample)
3. Test on recent data (out-of-sample)
4. Compare in-sample vs out-of-sample performance
5. Flag strategies that overfit

**Walk-Forward Schedule:**
```
Train Period 1: Jan-Jun 2024 → Test Period 1: Jul 2024
Train Period 2: Feb-Jul 2024 → Test Period 2: Aug 2024
Train Period 3: Mar-Aug 2024 → Test Period 3: Sep 2024
Train Period 4: Apr-Sep 2024 → Test Period 4: Oct 2024
```

**Validation:**
- Out-of-sample return should be ≥70% of in-sample return
- Win rate should not drop by more than 10%
- Max drawdown should not increase by more than 50%

---

## Data Requirements

### Disk Space Estimate

**Per pair:**
- 1 minute × 6 months = ~260,000 candles
- Per candle: ~100 bytes (timestamp, O, H, L, C, V)
- **Total per pair: ~26 MB**

**3 pairs × 26 MB = ~78 MB total** (very manageable)

### API Rate Limits

**Coinbase Advanced Trade API:**
- Public endpoints: 10 requests/second
- For 2,600 API calls: ~4-5 minutes total
- No authentication required for public OHLCV data

### Database Schema (Already Exists)

Your OHLCV database already has the structure:
```sql
CREATE TABLE ohlcv_data (
    prod_id VARCHAR(20),
    timestamp BIGINT,
    timeframe VARCHAR(10),
    open DECIMAL(20,8),
    high DECIMAL(20,8),
    low DECIMAL(20,8),
    close DECIMAL(20,8),
    volume DECIMAL(20,8),
    PRIMARY KEY (prod_id, timestamp, timeframe)
);
```

We'll store 1-minute data and derive all other timeframes on-the-fly during backtesting.

---

## Advantages of This Approach

### 1. **Repainting Indicator Accuracy**
- Simulates minute-by-minute candle development
- Indicators recalculate as new minutes complete
- Reflects real trading conditions (not just closed candles)

### 2. **Multi-Timeframe Fidelity**
- Your strategies use 5m, 15m, 1h, 4h, 1d timeframes
- System builds developing candles for all timeframes simultaneously
- Accurate representation of how indicators repaint across timeframes

### 3. **No Code Changes Required**
- Existing buy/sell logic works as-is
- Just add `backtest_mode` flag to prevent real API calls
- All strategy files (`libs/strats/*.py`) work unchanged

### 4. **Realistic Budget Constraints**
- Uses actual `buy_size_budget_calc()` logic
- Respects test mode budget limits
- Simulates real position sizing

### 5. **Easy Strategy Optimization**
- Run same backtest with different strategy settings
- Find optimal parameters per strategy per pair
- Walk-forward validation prevents overfitting

---

## Expected Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Data Backfilling | 3 days | 6 months of minute data for 3 pairs |
| 2. Core Engine | 4 days | Working minute-by-minute simulation |
| 3. Integration | 3 days | Buy/sell logic integrated |
| 4. Metrics | 3 days | Performance reporting |
| 5. Optimization | 7 days | Optimal strategy settings |
| 6. Walk-Forward | 5 days | Out-of-sample validation |
| **TOTAL** | **25 days** | **Full backtesting system** |

---

## Next Steps

### Immediate Actions (You Choose):

**Option A: Start with Data Backfilling**
```bash
# Create backfill script first
# This is the foundation for everything else
```

**Option B: Create Test Backtest Loop First**
```bash
# Build the simulation logic
# Test with manual data before backfilling
```

**Option C: Review and Approve Plan**
```bash
# You review this plan
# Make any changes you want
# Then we proceed together
```

### My Recommendation:
I recommend **Option A** - start with data backfilling. Once we have 6 months of minute data for BTC-USDC, ETH-USDC, and SOL-USDC, we can incrementally build and test the backtesting engine against real historical data.

**First concrete step:**
```bash
# 1. Create backfill_ohlcv.py script
# 2. Test on 1 day of BTC-USDC data first
# 3. Then backfill full 6 months
# 4. Move to next pair
```

---

## Questions for You

1. **How far back do you want to backfill data?**
   - 6 months (recommended for initial testing)
   - 1 year (more comprehensive)
   - 2+ years (extensive but more API calls)

2. **Which pairs should we prioritize?**
   - Just BTC-USDC to start?
   - BTC-USDC, ETH-USDC, SOL-USDC?
   - More pairs?

3. **What metrics matter most to you?**
   - Total return %
   - Win rate %
   - Max drawdown %
   - Sharpe ratio
   - Something else?

4. **Should we proceed with Option A (data backfilling first)?**

---

Let me know your thoughts and we'll start building!
