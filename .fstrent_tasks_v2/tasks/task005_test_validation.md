---
id: 005
title: 'Test & Validation'
type: task
status: pending
priority: high
feature: Quality Assurance
subsystems:
  - All
project_context: Run backtests on known periods and validate results match expected behavior
dependencies:
  - 001
  - 002
  - 003
  - 004
assigned_agent: null
created_at: "2025-10-10T18:40:00Z"
started_at: null
completed_at: null
error_log: null
complexity_score: 5
expansion_decision: null
memory_consultation: No previous backtest validation found - first time implementing
story_points: 3
sprint: Phase 2b
---

# Task 005: Test & Validation

## Description

Run comprehensive backtests on known historical periods and validate results match expected behavior. Verify win rates, returns, and trade counts are reasonable. Fix any bugs discovered during testing. This is the validation phase to prove the backtest engine produces accurate results.

## Details

### Test Scenarios:

#### Scenario 1: Single Strategy, Short Period (Baseline)
**Goal:** Prove engine works end-to-end without errors

**Setup:**
```python
results = backtest_strategy(
    bot_instance=bot,
    prod_id='BTC-USDC',
    start_date='2024-01-01',
    end_date='2024-01-31',  # 1 month
    starting_balance=10000.0,
    strategy_name='bb_bo'  # Bollinger Band Breakout
)
```

**Expected Results:**
- ✓ Backtest completes without crashes
- ✓ At least 10+ trades executed
- ✓ Win rate between 40-70% (reasonable range)
- ✓ Return between -10% and +30% (reasonable for 1 month)
- ✓ Max drawdown < 20%
- ✓ All trades have valid entry/exit prices
- ✓ Final balance = starting + total P&L

**Validation Checks:**
```python
assert results['total_trades'] >= 10, "Too few trades"
assert 40 <= results['win_rate'] <= 70, "Win rate out of range"
assert -10 <= results['total_return_pct'] <= 30, "Return out of range"
assert results['max_drawdown'] < 20, "Drawdown too large"
assert len(results['closed_trades']) == results['total_trades'], "Trade count mismatch"
```

#### Scenario 2: All Strategies, Medium Period (Comprehensive)
**Goal:** Verify all strategies can be tested simultaneously

**Setup:**
```python
results = backtest_strategy(
    bot_instance=bot,
    prod_id='BTC-USDC',
    start_date='2024-04-01',
    end_date='2024-06-30',  # Q2 2024
    starting_balance=10000.0,
    strategy_name=None  # All strategies
)
```

**Expected Results:**
- ✓ All 30+ strategies tested
- ✓ Per-strategy breakdown available
- ✓ Total trades = sum of all strategy trades
- ✓ No duplicate trades (same strategy shouldn't open twice simultaneously)
- ✓ Budget never goes negative
- ✓ No more than N positions open at once (respect limits)

**Validation Checks:**
```python
assert 'strategy_breakdown' in results
assert len(results['strategy_breakdown']) >= 30, "Not all strategies tested"
assert results['total_trades'] == sum(s['trades'] for s in results['strategy_breakdown'].values())
assert min(results['equity_curve'], key=lambda x: x['equity'])['equity'] >= 0, "Balance went negative!"
```

#### Scenario 3: Known Bull Market Period (Performance Check)
**Goal:** Verify strategies show positive performance in bull market

**Setup:**
```python
results = backtest_strategy(
    bot_instance=bot,
    prod_id='BTC-USDC',
    start_date='2024-01-01',
    end_date='2024-03-31',  # Q1 2024 - ATH run
    starting_balance=10000.0
)
```

**Expected Results:**
- ✓ Positive total return (bull market should be profitable)
- ✓ Win rate > 50% (momentum strategies excel in uptrends)
- ✓ Max drawdown < 15% (strong uptrend has small pullbacks)
- ✓ Most strategies show positive returns

**Validation Checks:**
```python
assert results['total_return_pct'] > 0, "Should be profitable in bull market"
assert results['win_rate'] > 50, "Win rate should be >50% in uptrend"
profitable_strats = [s for s in results['strategy_breakdown'].values() if s['return_pct'] > 0]
assert len(profitable_strats) > len(results['strategy_breakdown']) / 2, "Most strategies should profit"
```

#### Scenario 4: Known Sideways Period (Stress Test)
**Goal:** Verify strategies handle consolidation (harder for trend-following)

**Setup:**
```python
results = backtest_strategy(
    bot_instance=bot,
    prod_id='BTC-USDC',
    start_date='2024-05-01',
    end_date='2024-07-31',  # Q2/Q3 2024 - consolidation
    starting_balance=10000.0
)
```

**Expected Results:**
- ✓ Lower win rate (sideways is harder)
- ✓ More losing trades (whipsaws common)
- ✓ Lower total return (consolidation less profitable)
- ✓ Some strategies may have negative returns (acceptable)

**Validation Checks:**
```python
assert results['win_rate'] < 60, "Sideways should have lower win rate"
assert results['total_return_pct'] < 10, "Consolidation less profitable"
# Don't assert positive return - sideways can be unprofitable
```

#### Scenario 5: Long Period (Robustness Check)
**Goal:** Verify engine can handle large datasets without issues

**Setup:**
```python
results = backtest_strategy(
    bot_instance=bot,
    prod_id='BTC-USDC',
    start_date='2022-06-01',
    end_date='2024-10-04',  # Full dataset (~2.5 years)
    starting_balance=10000.0
)
```

**Expected Results:**
- ✓ Completes without memory issues
- ✓ Processing speed reasonable (~500+ min/sec)
- ✓ Equity curve shows progression over time
- ✓ Total return reflects market movement
- ✓ Drawdown periods align with known crashes

**Validation Checks:**
```python
assert results['total_trades'] > 100, "Should have many trades over 2.5 years"
assert len(results['equity_curve']) > 1000, "Should have equity data"
# Market context: 2022 bear → 2023 recovery → 2024 bull
# Expect overall positive return
```

### Bug Categories to Watch For:

1. **Data Issues**:
   - Missing candles causing gaps
   - Timestamp alignment errors
   - Indicator calculation failures (NaN values)

2. **Logic Issues**:
   - Buy signals not triggering
   - Sell signals not triggering
   - Duplicate positions opened
   - Positions never closed

3. **Calculation Issues**:
   - Incorrect P&L calculation
   - Budget tracking errors (goes negative)
   - Trade size calculation errors
   - Win rate calculation wrong

4. **Performance Issues**:
   - Too slow (< 100 min/sec)
   - Memory leaks
   - Database query inefficiency

## Test Strategy

### Phase 1: Smoke Tests (30 min)
- Run Scenario 1 (single strategy, short period)
- Fix any immediate crashes
- Verify basic output format

### Phase 2: Comprehensive Testing (1-2 hours)
- Run all 5 scenarios
- Document any bugs found
- Fix critical bugs
- Re-test after fixes

### Phase 3: Manual Validation (30-60 min)
- Open JSON results files
- Spot-check trades for reasonableness
- Review equity curve for anomalies
- Compare metrics to expected ranges
- Validate against known market events

### Phase 4: Edge Case Testing (30 min)
- Test with no trades (super conservative settings)
- Test with many simultaneous positions
- Test with insufficient starting balance
- Test with single day of data
- Test with missing data periods

## Agent Notes

### Files to Modify:
- **None** (this is testing existing code)
- May create `backtest/test_backtest.py` for automated tests

### Files to Reference:
- `backtest/backtest_example.py` - Main entry point
- `libs/backtest_base.py` - Core engine
- `backtest/docs/REVOLUTIONARY_DESIGN.md` - Expected behavior

### Key Considerations:
- **Test Data:** Use real historical data (already loaded)
  - 1.76M rows of BTC-USDC 1-minute data
  - June 2022 - Oct 2025
  - Covers bear, sideways, bull markets

- **Expected Behavior:** What's "reasonable"?
  - Win rate: 45-65% (most strategies)
  - Monthly return: -5% to +15% (depends on market)
  - Max drawdown: 5-20% (strategy-dependent)
  - Trade frequency: 1-5 per day (varies by strategy)

- **Known Market Events to Validate Against:**
  - June 2022: Crash to $17k (bear market bottom)
  - Jan 2024: ETF launch rally (bullish)
  - March 2024: New ATH at $73k (peak bull)
  - May-Aug 2024: Consolidation $60-70k (sideways)

- **Bug Documentation:**
  - Record ALL bugs found (even if fixed)
  - Document fix for future reference
  - Add to task notes or create bug log

- **Performance Targets:**
  - Processing speed: >500 minutes/second
  - Memory usage: <2GB for full backtest
  - No memory leaks (stable over long runs)

### Complexity Analysis:
**Score: 5/10**
- **Moderate:** Multiple test scenarios
- **Complex:** Bug diagnosis and fixing
- **Moderate:** Manual validation and spot-checking
- **Simple:** Running scripts straightforward

### Estimated Time: 2-3 hours
- 30 min: Smoke tests (Scenario 1)
- 1 hour: Comprehensive tests (Scenarios 2-5)
- 30-60 min: Manual validation and spot-checking
- 30 min: Edge case testing
- Buffer for bug fixes as needed

## Memory Context

**Historical Insights:** No previous backtesting validation. First implementation.

**Related Work:**
- Live trading bot has 10+ months of real performance data
- Can compare backtest results to live results for validation
- Known strategy performance: some profitable, some unprofitable
- User has domain expertise in crypto trading (knows what's realistic)

**Known Challenges:**
- First time running minute-by-minute backtests (no baseline)
- Don't know how long it will take (processing speed unknown)
- Don't know what win rates to expect (no historical benchmark)
- May discover edge cases not anticipated in design

**Success Criteria (User Confidence):**
```
User will trust backtests if:
✓ Results match their intuition from live trading
✓ Profitable strategies in backtest are profitable live
✓ Unprofitable strategies in backtest are unprofitable live
✓ Trade frequency and win rates match expectations
✓ Engine runs fast enough for iterative testing
```

---

**Created:** 2025-10-10 18:40 UTC  
**Priority:** High (Validation required before production use)  
**Complexity:** 5/10 (Multiple test scenarios and bug diagnosis)

