# Rolling Candles Concept (Right-Handed Candles)

**Date:** October 10, 2025  
**Source:** User's Polars-based TA library project (in development)  
**Status:** FUTURE INTEGRATION - Document for reference  
**Priority:** Future enhancement after core backtesting complete

---

## What Are Rolling Candles?

**Traditional Fixed Candles:**
```
5-minute fixed candles:
10:00-10:05 [=====]
10:05-10:10       [=====]
10:10-10:15             [=====]
```

**Rolling Candles (Right-Handed):**
```
5-minute rolling window:
At 10:03: [=====] (9:58-10:03)
At 10:04:  [=====] (9:59-10:04)
At 10:05:   [=====] (10:00-10:05)
At 10:06:    [=====] (10:01-10:06)
```

**Key Concept:** Always at the END of the candle period. Every minute, the window "rolls forward" by 1 minute.

---

## Mathematical Definition

**For N-minute rolling candles at time T:**
- **Candle Start:** T - N minutes
- **Candle End:** T (current time)
- **Duration:** Always exactly N minutes
- **Updates:** Every single minute (not just at period boundaries)

**Example: 7-minute rolling candles**
```
Current Time | Candle Start | Candle End | Duration
-------------|--------------|------------|----------
10:00:00     | 9:53:00      | 10:00:00   | 7 minutes
10:01:00     | 9:54:00      | 10:01:00   | 7 minutes
10:02:00     | 9:55:00      | 10:02:00   | 7 minutes
10:03:00     | 9:56:00      | 10:03:00   | 7 minutes
...          | ...          | ...        | 7 minutes
```

**EVERY MINUTE:** The candle changes!

---

## Comparison: Three Candle Types

### 1. Standard Fixed Candles (Current Implementation)

**Alignment:** Period boundaries (midnight for daily, hour for hourly, etc.)

**Example: 7-minute candles at 10:03**
```
Current candle: 10:00-10:07 (still developing)
Updates: Only at 10:07, 10:14, 10:21, etc.
```

**Characteristics:**
- Candles complete at fixed boundaries
- Updates only at period boundaries
- Indicators stable between updates
- Standard exchange behavior

### 2. Epoch-Aligned Fixed Candles (Task 000.1)

**Alignment:** Unix epoch (1970-01-01 00:00:00 UTC)

**Example: 7-minute candles at 10:03**
```
Current candle: 9:59-10:06 (still developing, crosses 10:00!)
Updates: Only at specific epoch-aligned times
```

**Characteristics:**
- Candles complete at epoch boundaries
- No partial candles for non-divisible timeframes
- Updates only at calculated boundaries
- Better than standard for arbitrary timeframes

### 3. Rolling Candles (Future Integration)

**Alignment:** Current time (right-handed window)

**Example: 7-minute rolling candles at 10:03**
```
Current candle: 9:56-10:03 (ALWAYS complete!)
At 10:04: New candle is 9:57-10:04
At 10:05: New candle is 9:58-10:05
```

**Characteristics:**
- Candle "complete" every minute (rolls forward)
- ALWAYS full-length (never partial, never developing)
- Updates EVERY SINGLE MINUTE
- ALL indicators become repainting

---

## Impact on Technical Analysis

### The Fundamental Shift

**With Fixed Candles:**
- Some indicators repaint (during candle development)
- Some indicators don't repaint (only use closed candles)
- Clear distinction between developing vs complete candles

**With Rolling Candles:**
- **ALL INDICATORS REPAINT** (candle always changing)
- No such thing as "closed" candles
- Every minute is a new "complete" candle

### Indicators That Get BETTER

**Moving Averages:**
- Standard: Update only at period boundaries
- Rolling: Update every minute (smoother, more responsive)
- **Result:** Earlier trend detection, fewer whipsaws

**Bollinger Bands:**
- Standard: Bands jump at period boundaries
- Rolling: Bands adjust smoothly every minute
- **Result:** Better volatility tracking, smoother signals

**Volume-Weighted Indicators:**
- Standard: Volume aggregates at boundaries
- Rolling: Volume continuously updated
- **Result:** More accurate volume-price relationship

### Indicators That Get WORSE

**RSI (Relative Strength Index):**
- Standard: Clear overbought/oversold signals
- Rolling: Constantly fluctuating signals
- **Result:** More false signals, harder to trade

**MACD:**
- Standard: Clear crossovers at specific times
- Rolling: Crossovers can appear/disappear minute-to-minute
- **Result:** Whipsaws increase dramatically

**Support/Resistance:**
- Standard: Clear pivot points at candle boundaries
- Rolling: Support/resistance zones constantly shifting
- **Result:** Harder to identify key levels

### Why Some Indicators Flip

**The Psychology Factor:**
- Standard candles: Traders make decisions at boundaries (human behavior)
- Rolling candles: No boundaries = no collective decision points
- Market moves are partially CAUSED by fixed candle boundaries

**Example:**
- At 10:00, 1h candle closes
- Thousands of traders' algorithms trigger
- Price moves because of the boundary
- Rolling candles miss this phenomenon!

---

## Use Cases for Rolling Candles

### 1. High-Frequency Trading
**Why:** Need immediate response to changing conditions
**Benefit:** Don't wait for candle completion
**Trade-off:** More noise, more trades

### 2. Machine Learning Feature Engineering
**Why:** Create smoother, more continuous features
**Benefit:** Better input data for ML models
**Trade-off:** More computational cost

### 3. Volatility Analysis
**Why:** Track volatility continuously, not discretely
**Benefit:** More accurate volatility measurements
**Trade-off:** Harder to compare to standard analysis

### 4. Strategy Discovery
**Why:** Test if strategies work better with continuous updates
**Benefit:** Find strategies that don't rely on boundaries
**Trade-off:** Results may not match live trading (if exchanges use fixed)

### 5. Indicator Comparison
**Why:** Understand which indicators are robust to repainting
**Benefit:** Find indicators that work regardless of candle type
**Trade-off:** More testing required

---

## Implementation Considerations

### Performance Impact

**Memory:**
```
Standard 5min candles:  1 candle per 5 minutes = 12 per hour
Rolling 5min candles:   1 candle per 1 minute = 60 per hour
Ratio: 5x more data!
```

**Computation:**
```
Standard: Calculate indicators at boundaries (12 times/hour)
Rolling: Calculate indicators EVERY minute (60 times/hour)
Ratio: 5x more calculations!
```

**Storage:**
```
For 1 day of 5min data:
Standard: 288 candles
Rolling: 1,440 candles (5x more)
```

### Polars Integration Benefits

**Why Polars?**
- **Speed:** Rust-based, much faster than Pandas
- **Memory:** More efficient memory usage
- **Lazy:** Can defer calculations until needed
- **Parallel:** Native parallel processing

**For Rolling Candles:**
```python
# Pseudocode for Polars rolling candles
df = pl.scan_parquet('ohlcv_1min.parquet')

# Create rolling 5min candles
rolling = df.rolling(
    index_column='timestamp',
    period='5m',
    closed='right'  # Right-handed window
).agg([
    pl.col('open_prc').first().alias('open'),
    pl.col('high_prc').max().alias('high'),
    pl.col('low_prc').min().alias('low'),
    pl.col('close_prc').last().alias('close'),
    pl.col('volume').sum().alias('volume')
])

# Calculate indicators on rolling candles
with_indicators = rolling.pipe(
    calculate_rsi,
    calculate_macd,
    calculate_bb
)
```

**Benefits:**
- Single pass through data
- Lazy evaluation (only compute what's needed)
- Parallel processing (fast!)
- Memory efficient (streaming)

### Integration with Current Backtesting System

**Architecture Options:**

**Option 1: Separate Column Sets (Recommended)**
```python
# In BacktestEngine
self.candle_types = {
    'fixed_15min': CandleBuilder('15min', align_to_epoch=True),
    'fixed_1h': CandleBuilder('1h', align_to_epoch=True),
    'rolling_15min': RollingCandleBuilder('15min'),
    'rolling_1h': RollingCandleBuilder('1h')
}

# In bot.pair.ta structure
bot.pair.ta['fixed_15min'].df  # Standard fixed candles
bot.pair.ta['rolling_15min'].df  # Rolling candles

# Strategy can choose which to use
if strategy.prefers_rolling:
    df = bot.pair.ta['rolling_15min'].df
else:
    df = bot.pair.ta['fixed_15min'].df
```

**Option 2: Hybrid Approach**
```python
# Both candle types in same DataFrame
df = pd.DataFrame({
    'timestamp': ...,
    
    # Fixed candles (existing)
    'open_15m_fixed': ...,
    'high_15m_fixed': ...,
    'low_15m_fixed': ...,
    'close_15m_fixed': ...,
    'volume_15m_fixed': ...,
    
    # Rolling candles (new)
    'open_15m_rolling': ...,
    'high_15m_rolling': ...,
    'low_15m_rolling': ...,
    'close_15m_rolling': ...,
    'volume_15m_rolling': ...,
    
    # Indicators calculated on both
    'rsi_14_fixed': ...,
    'rsi_14_rolling': ...,
    'macd_fixed': ...,
    'macd_rolling': ...
})
```

**Option 3: Strategy-Time Selection**
```python
# Strategy specifies candle type at initialization
strategy = Strategy(
    name='my_strategy',
    candle_type='rolling',  # or 'fixed'
    timeframes=['15min', '1h']
)

# Backtester builds appropriate candles
engine.initialize_for_strategy(strategy)
```

---

## Testing Requirements

### Comparison Tests

**Test 1: Same Indicator, Different Candles**
```python
def test_rsi_fixed_vs_rolling():
    # Calculate RSI on fixed 15min candles
    rsi_fixed = calculate_rsi(fixed_candles, period=14)
    
    # Calculate RSI on rolling 15min candles
    rsi_rolling = calculate_rsi(rolling_candles, period=14)
    
    # Compare behavior
    assert rsi_rolling.std() > rsi_fixed.std()  # Rolling should be noisier
    assert len(rsi_rolling) > len(rsi_fixed)    # More data points
```

**Test 2: Strategy Performance Comparison**
```python
def test_strategy_fixed_vs_rolling():
    # Run strategy on fixed candles
    results_fixed = backtest(strategy, candle_type='fixed')
    
    # Run same strategy on rolling candles
    results_rolling = backtest(strategy, candle_type='rolling')
    
    # Document differences
    print(f"Fixed:   {results_fixed.annual_return}%")
    print(f"Rolling: {results_rolling.annual_return}%")
    print(f"Trades:  {results_fixed.num_trades} vs {results_rolling.num_trades}")
```

**Test 3: Indicator Robustness**
```python
def test_indicator_robustness():
    """
    Which indicators work well regardless of candle type?
    """
    indicators = ['rsi', 'macd', 'bb', 'ema', 'sma', 'atr', 'obv']
    
    for indicator in indicators:
        fixed_results = backtest_with_indicator(indicator, 'fixed')
        rolling_results = backtest_with_indicator(indicator, 'rolling')
        
        robustness_score = correlation(fixed_results, rolling_results)
        print(f"{indicator}: {robustness_score:.2f}")
```

---

## Future Integration Plan

### Phase 1: Documentation (Current)
- [x] Document rolling candles concept
- [x] Explain difference from fixed candles
- [x] Identify impact on indicators
- [x] Note performance considerations

### Phase 2: Polars TA Library Development (External Project)
- [ ] User develops Polars-based TA library
- [ ] Implement rolling candle calculations
- [ ] Implement epoch-aligned fixed candles
- [ ] Test both approaches
- [ ] Compare performance vs PandasTA

### Phase 3: Integration Planning (Future)
- [ ] Design integration architecture
- [ ] Choose column approach (separate vs hybrid)
- [ ] Plan backward compatibility
- [ ] Design strategy selection API

### Phase 4: Implementation (Future)
- [ ] Create `RollingCandleBuilder` class
- [ ] Integrate with `BacktestEngine`
- [ ] Update indicator calculation pipeline
- [ ] Add strategy candle-type selection

### Phase 5: Testing & Validation (Future)
- [ ] Comparison tests (fixed vs rolling)
- [ ] Strategy performance analysis
- [ ] Indicator robustness testing
- [ ] Performance benchmarking

### Phase 6: Documentation & Examples (Future)
- [ ] Tutorial: When to use rolling candles
- [ ] Example strategies for rolling candles
- [ ] Performance optimization guide
- [ ] Migration guide for existing strategies

---

## Key Decisions for Future

### Decision 1: Default Behavior
**Question:** Should backtester default to fixed or rolling candles?

**Recommendation:** Default to fixed candles (industry standard)
- Most strategies expect fixed candles
- Matches live exchange behavior
- Rolling candles opt-in for advanced users

### Decision 2: Indicator Calculation
**Question:** Calculate indicators on both candle types automatically?

**Options:**
- A) Calculate on all types (expensive but convenient)
- B) Calculate only on requested type (efficient)
- C) Lazy calculation (best of both)

**Recommendation:** Option C (lazy calculation)
- Only calculate when accessed
- Cache results
- Polars naturally supports this

### Decision 3: Strategy API
**Question:** How do strategies specify candle type?

**Options:**
- A) Global setting (all strategies use same type)
- B) Strategy property (each strategy specifies)
- C) Per-timeframe setting (mix types in one strategy)

**Recommendation:** Option B (strategy property)
- Most flexible
- Clear intent
- Easy to A/B test

### Decision 4: Performance Trade-offs
**Question:** How to handle 5x data increase?

**Options:**
- A) Store all rolling candles (memory intensive)
- B) Calculate on-demand (CPU intensive)
- C) Hybrid (cache recent, calculate old)

**Recommendation:** Option C (hybrid approach)
- Cache last N periods of rolling candles
- Calculate on-demand for historical
- Let Polars lazy evaluation optimize

---

## Research Questions

### For User's Polars TA Library:

1. **Performance Benchmarks:**
   - How much faster is Polars vs Pandas for rolling calculations?
   - Memory usage comparison?
   - Optimal window sizes for performance?

2. **Indicator Behavior:**
   - Which indicators improve with rolling candles?
   - Which indicators degrade?
   - Can we quantify "robustness" to candle type?

3. **Strategy Discovery:**
   - Do certain strategy types work better with rolling candles?
   - Can ML models learn better from rolling vs fixed?
   - Are there patterns in which strategies prefer which type?

4. **Integration Patterns:**
   - Best way to integrate Polars with existing Pandas code?
   - Migration path from PandasTA to Polars TA?
   - Backward compatibility strategies?

---

## Related Concepts

### 1. Heikin-Ashi Candles
- Modified candles for smoothing price action
- Different OHLC calculation
- NOT the same as rolling (different math)

### 2. Renko Bricks
- Fixed-size price moves (not time-based)
- Removes time element entirely
- Even more different from standard

### 3. Point & Figure
- Another time-agnostic charting method
- Focus on significant price moves
- Different philosophy entirely

### 4. Tick Charts
- Fixed number of trades per candle
- Volume-based, not time-based
- Different from rolling (uses trade count)

**Rolling candles are unique:** Time-based like standard candles, but continuously updating window instead of fixed boundaries.

---

## Notes for Implementation

### When User's Polars TA Library is Ready:

**Integration Checklist:**
```markdown
- [ ] Review Polars TA library architecture
- [ ] Identify integration points with BacktestEngine
- [ ] Design RollingCandleBuilder class
- [ ] Plan bot.pair.ta structure changes
- [ ] Update strategy API for candle type selection
- [ ] Create migration guide for existing strategies
- [ ] Performance test with real BTC data
- [ ] Compare results: Fixed vs Epoch-aligned vs Rolling
- [ ] Document findings and recommendations
- [ ] Update all documentation with new capabilities
```

**Questions to Ask:**
```markdown
- [ ] API design decisions from Polars TA library?
- [ ] Performance characteristics observed?
- [ ] Which indicators work best with rolling?
- [ ] Any surprising findings?
- [ ] Recommended default settings?
- [ ] Memory/CPU optimization tips?
```

---

## User's Vision

> "right handed candles, or rolling candles... we are always at the end of the candle regardless of the timeframe used... so if we are doing 5min timeframe and the current time is 10:03am the candle start is 9:58... so we are never dealing with partial candles"

**Key Insight:** This completely eliminates the partial candle problem by redefining what a "candle" is!

**Three Solutions to Partial Candles:**
1. **Epoch Alignment** (Task 000.1): Fixed candles, no partials
2. **Rolling Candles** (This concept): Always full-length, always updating
3. **Both!** Use epoch-aligned when you want boundaries, rolling when you want continuous

**This gives us THREE candle paradigms:**
1. Standard fixed (for exchange compatibility)
2. Epoch-aligned fixed (for arbitrary timeframes without partials)
3. Rolling (for continuous, always-complete candles)

**We'll be the most sophisticated backtesting system in crypto!** 🚀

---

## Summary

**Current Status:** Documentation complete, ready for future integration

**Priority:** After core backtesting complete (Tasks 001-005)

**Dependencies:** 
- User's Polars TA library development
- Task 000.1 (Epoch alignment) completed first
- Core backtesting proven and working

**Expected Timeline:** 3-6 months after core backtesting complete

**Estimated Effort:** 
- RollingCandleBuilder class: 4 hours
- Integration with BacktestEngine: 4 hours
- Testing and validation: 8 hours
- Documentation: 4 hours
- **Total: 20 hours (10 story points)**

---

**This is forward-thinking architecture!** Documenting now ensures smooth integration when the Polars TA library is ready. 📝✅

