# Three Candle Paradigms: The Complete Picture

**Date:** October 10, 2025  
**Status:** Architectural Vision Document  
**Purpose:** Explain the three candle approaches and when to use each

---

## The Vision

Our backtesting system will support **THREE different candle paradigms**, making it the most sophisticated and flexible backtesting platform in crypto.

---

## Paradigm 1: Standard Fixed Candles

### What It Is
Traditional exchange-style candles aligned to calendar boundaries (midnight for daily, hour boundaries for hourly, etc.)

### Example: 15-Minute Candles
```
00:00-00:15 [=====]
00:15-00:30       [=====]
00:30-00:45             [=====]
00:45-01:00                   [=====]
```

### Characteristics
- ✅ Matches exchange behavior exactly
- ✅ Industry standard (everyone understands it)
- ✅ Strategies can be validated against exchange data
- ❌ Creates partial candles for non-standard timeframes (7min, 23min, etc.)
- ❌ Limited to predefined timeframes

### When to Use
- **Exchange compatibility:** Need to match live exchange candles exactly
- **Standard strategies:** Most trading strategies expect this format
- **Comparison:** Validating against other platforms/exchanges
- **Common timeframes:** Using standard timeframes (5min, 15min, 1h, 4h, 1d)

### Implementation Status
✅ **COMPLETE** (Task 000) - Currently working for predefined timeframes

---

## Paradigm 2: Epoch-Aligned Fixed Candles

### What It Is
Fixed candles aligned to Unix epoch (1970-01-01 00:00:00 UTC) instead of calendar boundaries.

### Example: 7-Minute Candles
```
Standard (midnight aligned):
23:52-23:59 [=====]
23:59-00:00 [=] ❌ PARTIAL! (1 minute)
00:00-00:07 [=====]

Epoch-aligned:
23:54-00:01 [=====] ✅ FULL 7 MINUTES! (crosses midnight)
00:01-00:08       [=====] ✅ FULL 7 MINUTES!
00:08-00:15             [=====] ✅ FULL 7 MINUTES!
```

### Characteristics
- ✅ No partial candles EVER (for any timeframe)
- ✅ Supports arbitrary timeframes (3min, 7min, 89min, 1 week, etc.)
- ✅ Better for machine learning (consistent candle lengths)
- ✅ Can cross calendar boundaries (this is correct!)
- ⚠️ Doesn't match exchange candles exactly (different boundaries)
- ⚠️ Candles may not align with psychological price levels (round hours, etc.)

### When to Use
- **Machine learning:** Need consistent candle lengths for feature engineering
- **Strategy discovery:** Testing arbitrary timeframes to find optimal ones
- **Arbitrary timeframes:** Using non-standard timeframes (7min, 23min, 89min)
- **Accuracy over compatibility:** Need mathematically correct candles

### Implementation Status
⏳ **PENDING** (Task 000.1) - Estimated 4 hours

---

## Paradigm 3: Rolling Candles (Right-Handed)

### What It Is
Continuously updating window that is always centered on the current time. Every minute, the window "rolls forward."

### Example: 7-Minute Rolling Candles
```
At 10:00: [=====] (9:53-10:00)
At 10:01:  [=====] (9:54-10:01)
At 10:02:   [=====] (9:55-10:02)
At 10:03:    [=====] (9:56-10:03)
At 10:04:     [=====] (9:57-10:04)
```

### Characteristics
- ✅ Always full-length candles (never partial, never developing)
- ✅ Updates EVERY minute (most responsive)
- ✅ No calendar alignment issues
- ✅ Better for some indicators (smoother updates)
- ❌ ALL indicators become repainting
- ❌ 5x more candles (higher memory/CPU usage)
- ❌ Doesn't match ANY exchange behavior
- ❌ Harder to interpret (no clear boundaries)

### When to Use
- **High-frequency strategies:** Need immediate response to changing conditions
- **Continuous analysis:** Want smooth, uninterrupted indicator updates
- **Indicator research:** Understanding which indicators are robust to repainting
- **ML feature engineering:** Need continuously updated features
- **Volatility tracking:** Want moment-to-moment volatility measurements

### Implementation Status
🔮 **FUTURE** - After user's Polars TA library complete (3-6 months, 10 story points)

---

## Comparison Matrix

| Feature | Standard Fixed | Epoch-Aligned | Rolling |
|---------|---------------|---------------|---------|
| **Partial Candles** | Yes (for odd timeframes) | Never | Never |
| **Arbitrary Timeframes** | No | Yes | Yes |
| **Exchange Matching** | Exact | Approximate | No |
| **Update Frequency** | At boundaries | At boundaries | Every minute |
| **Repainting** | Some indicators | Some indicators | ALL indicators |
| **Memory Usage** | 1x | 1x | 5x |
| **CPU Usage** | 1x | 1x | 5x |
| **Complexity** | Simple | Simple | Complex |
| **Industry Standard** | Yes | No | No |

---

## Real-World Scenarios

### Scenario 1: Validating a New Strategy

**Goal:** Backtest a strategy that uses 15min and 1h candles, then deploy to exchange

**Best Choice:** **Standard Fixed Candles**

**Why:**
- Matches exchange behavior exactly
- Can validate backtest results against exchange
- Strategy will behave identically in live trading
- Standard timeframes work perfectly

**Code:**
```python
engine = BacktestEngine(bot, db_ohlcv)
engine.initialize_candle_builders(['15min', '1h'], align_to_epoch=False)
# Standard alignment, matches exchanges
```

---

### Scenario 2: ML Strategy Discovery Across All Timeframes

**Goal:** Test 100 different timeframes to find the optimal one for a strategy

**Best Choice:** **Epoch-Aligned Fixed Candles**

**Why:**
- Can test 7min, 13min, 89min, etc. (any timeframe!)
- No partial candles (accurate results)
- Consistent candle lengths (fair comparison)
- After finding optimal timeframe, can approximate with standard

**Code:**
```python
# Test every Fibonacci timeframe
fib_timeframes = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

for tf in fib_timeframes:
    engine = BacktestEngine(bot, db_ohlcv)
    engine.initialize_candle_builders([tf], align_to_epoch=True)
    results = engine.run_backtest(...)
    print(f"{tf}min: {results['annual_return']}%")
```

---

### Scenario 3: Indicator Robustness Research

**Goal:** Understand which indicators work well regardless of repainting

**Best Choice:** **Rolling Candles**

**Why:**
- ALL indicators repaint with rolling candles
- If indicator still works, it's truly robust
- Can identify indicators that rely on boundaries vs those that don't
- Better understanding of indicator behavior

**Code:**
```python
# Test indicator with both candle types
fixed_results = test_indicator_with_candle_type('rsi', 'fixed')
rolling_results = test_indicator_with_candle_type('rsi', 'rolling')

robustness = correlation(fixed_results, rolling_results)
print(f"RSI robustness score: {robustness}")
```

---

### Scenario 4: High-Frequency Trading Development

**Goal:** Develop a strategy that responds to market changes within seconds

**Best Choice:** **Rolling Candles**

**Why:**
- Updates every minute (most responsive)
- Don't need to wait for candle completion
- Can react to changing conditions immediately
- Better for short-term trading

**Code:**
```python
engine = BacktestEngine(bot, db_ohlcv)
engine.initialize_candle_builders(
    ['5min', '15min'],
    candle_type='rolling'
)
# Strategy gets updates every single minute
```

---

### Scenario 5: Multi-Strategy Portfolio Testing

**Goal:** Test 10 different strategies with different timeframe preferences

**Best Choice:** **ALL THREE PARADIGMS!**

**Why:**
- Some strategies work better with standard
- Some strategies work better with epoch-aligned
- Some strategies work better with rolling
- Need to test each strategy with its optimal candle type

**Code:**
```python
strategies = [
    ('momentum', 'standard', ['15min', '1h']),
    ('mean_reversion', 'epoch_aligned', [7, 23]),  # Odd timeframes
    ('scalping', 'rolling', ['5min', '15min']),
]

results = {}
for name, candle_type, timeframes in strategies:
    engine = BacktestEngine(bot, db_ohlcv)
    if candle_type == 'rolling':
        engine.initialize_rolling_candles(timeframes)
    else:
        align_to_epoch = (candle_type == 'epoch_aligned')
        engine.initialize_candle_builders(timeframes, align_to_epoch)
    
    results[name] = engine.run_backtest(strategy)
```

---

## The Partial Candle Problem (The Original Insight)

### What User Discovered

> "huge issue with crypto... timeframes not divisible into hour/day create partial candles at midnight boundaries"

**This is a problem most crypto platforms have!**

### Three Solutions

**1. Ignore non-standard timeframes (Most Exchanges)**
- Only offer 5min, 15min, 30min, 1h, 4h, 1d
- Avoid the problem by not supporting 7min, 23min, etc.
- **Limitation:** Can't discover optimal timeframes

**2. Epoch alignment (Our Task 000.1)**
- Support any timeframe
- Align to Unix epoch
- **Result:** No partial candles, but different boundaries than exchanges

**3. Rolling candles (Future Integration)**
- Redefine what a "candle" is
- Always full-length by design
- **Result:** No boundaries at all, continuous updates

**We're implementing solutions 2 & 3!** (And keeping #1 for compatibility)

---

## Performance Implications

### Memory Usage Example: 1 Day of Data

**5-Minute Timeframe:**
```
Standard Fixed:   288 candles (1 per 5 minutes)
Epoch-Aligned:    288 candles (same, just different boundaries)
Rolling:          1,440 candles (1 per minute)
Ratio:            1x : 1x : 5x
```

**Storage for 1 year of 5min data:**
```
Standard:   105,120 candles × 40 bytes = 4.2 MB
Rolling:    525,600 candles × 40 bytes = 21 MB
```

### CPU Usage Example: Indicator Calculation

**RSI-14 on 5-minute candles for 1 hour:**
```
Standard:     Calculate 12 times (once per candle)
Epoch-Aligned: Calculate 12 times (once per candle)
Rolling:      Calculate 60 times (once per minute)
Ratio:        1x : 1x : 5x
```

### Optimization: Polars Lazy Evaluation

**With Polars TA Library:**
- Only calculate what's accessed (lazy evaluation)
- Parallel processing (multi-core)
- Memory-efficient streaming
- **Result:** Rolling candles become feasible!

---

## Integration Architecture

### Option 1: Unified Interface (Recommended)

```python
class BacktestEngine:
    def initialize_candles(
        self,
        timeframes: List[Union[str, int]],
        candle_type: str = 'standard',  # 'standard' | 'epoch_aligned' | 'rolling'
        align_to_epoch: bool = None  # Override for 'standard'
    ):
        """
        Initialize any combination of candle types.
        
        Examples:
            # Standard (exchange-compatible)
            engine.initialize_candles(['15min', '1h'], candle_type='standard')
            
            # Epoch-aligned (arbitrary timeframes, no partials)
            engine.initialize_candles([7, 23, 89], candle_type='epoch_aligned')
            
            # Rolling (continuous updates)
            engine.initialize_candles(['15min', '1h'], candle_type='rolling')
            
            # Mixed (advanced)
            engine.add_candles(['15min'], candle_type='standard')
            engine.add_candles([7, 23], candle_type='epoch_aligned')
            engine.add_candles(['5min'], candle_type='rolling')
        """
```

### Storage Structure

```python
bot.pair.ta = {
    # Standard candles
    'standard_15min': AttrDict(df=..., curr=...),
    'standard_1h': AttrDict(df=..., curr=...),
    
    # Epoch-aligned candles
    'epoch_7min': AttrDict(df=..., curr=...),
    'epoch_23min': AttrDict(df=..., curr=...),
    
    # Rolling candles
    'rolling_15min': AttrDict(df=..., curr=...),
    'rolling_1h': AttrDict(df=..., curr=...),
}

# Strategy accesses appropriate type
if strategy.prefers_rolling:
    df = bot.pair.ta['rolling_15min'].df
else:
    df = bot.pair.ta['standard_15min'].df
```

---

## Implementation Roadmap

### Phase 1: Foundation ✅ (COMPLETE)
- [x] Standard fixed candles for predefined timeframes
- [x] Piano player minute-by-minute replay
- [x] TA indicator integration

### Phase 2: Arbitrary Timeframes ⏳ (Task 000.1 - 4 hours)
- [ ] Parse arbitrary frequency formats
- [ ] Implement epoch alignment
- [ ] Support 1min through 1 week timeframes
- [ ] Test with non-standard timeframes (7min, 23min, 89min)

### Phase 3: Core Backtesting (Tasks 002-005 - 5-6 hours)
- [ ] Buy logic integration
- [ ] Sell logic integration
- [ ] Backtest mode flag (safety)
- [ ] Testing and validation

### Phase 4: Polars TA Library 🔮 (External - User's Project)
- [ ] User develops Polars-based TA library
- [ ] Implement rolling candle calculations
- [ ] Performance testing
- [ ] API design

### Phase 5: Rolling Candles Integration 🔮 (Future - 20 hours)
- [ ] Create `RollingCandleBuilder` class
- [ ] Integrate with `BacktestEngine`
- [ ] Update indicator pipeline
- [ ] Comparison testing
- [ ] Documentation and examples

---

## Success Criteria

### For Standard Fixed (Phase 1)
- [x] Matches exchange candles exactly
- [x] Works with all predefined timeframes
- [x] Indicators calculate correctly

### For Epoch-Aligned (Phase 2)
- [ ] No partial candles for any timeframe
- [ ] Supports 1min through 1 week
- [ ] Can parse arbitrary formats (7min, 89, '1w')
- [ ] Math proven correct (crossing boundaries OK)

### For Rolling (Phase 5)
- [ ] Updates every minute
- [ ] Always full-length candles
- [ ] Efficient performance (Polars optimization)
- [ ] Strategy API for candle type selection
- [ ] Comparison tests (fixed vs rolling results)

---

## Key Decisions

### Decision: Default Candle Type
**Choice:** Standard Fixed

**Rationale:**
- Most strategies expect standard candles
- Matches exchange behavior
- Industry standard
- Other types are opt-in for advanced users

### Decision: Support All Three Paradigms
**Choice:** Yes (eventually)

**Rationale:**
- Different use cases need different approaches
- Gives users maximum flexibility
- Positions us as most advanced backtesting platform
- Research value (understanding indicator behavior)

### Decision: Implementation Order
**Choice:** Standard → Epoch-Aligned → Rolling

**Rationale:**
- Standard needed for basic functionality
- Epoch-aligned needed for ML/strategy discovery
- Rolling is advanced feature (requires Polars TA)

---

## Summary

**Current State:**
- ✅ Standard fixed candles working (Task 000)
- ✅ Documentation complete for all three paradigms

**Near Future (1 week):**
- ⏳ Epoch-aligned fixed candles (Task 000.1 - 4 hours)
- ⏳ Core backtesting complete (Tasks 002-005 - 5-6 hours)

**Far Future (3-6 months):**
- 🔮 Polars TA library integration
- 🔮 Rolling candles support
- 🔮 All three paradigms available

**The Vision:**
> The most flexible and sophisticated backtesting platform in crypto, supporting three different candle paradigms for different use cases: standard (exchange compatibility), epoch-aligned (arbitrary timeframes), and rolling (continuous updates).

**We're not just building a backtester - we're building a research platform!** 🚀

