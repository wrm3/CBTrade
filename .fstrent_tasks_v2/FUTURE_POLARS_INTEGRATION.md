# Future Polars TA Library Integration

**Date:** October 10, 2025  
**Status:** Planning Document  
**Priority:** After core backtesting complete

---

## Overview

User is developing a separate Polars-based Technical Analysis library that will eventually integrate with this backtesting system. This document tracks the integration plan and key concepts.

---

## Polars TA Library Features (User's External Project)

### 1. Epoch-Aligned Candles
- Fixed candles aligned to Unix epoch
- No partial candles for arbitrary timeframes
- Same as Task 000.1 in this project

### 2. Rolling Candles (Right-Handed)
- Continuously updating window
- Always at current time (right-handed)
- All indicators become repainting
- 5x more data but smoother updates

### 3. Polars Performance
- Rust-based (faster than Pandas)
- Lazy evaluation (compute only what's needed)
- Parallel processing (multi-core)
- Memory efficient (streaming)

---

## Integration Points

### What We Have
- `CandleBuilder` class (standard fixed candles)
- `BacktestEngine` with minute-by-minute replay
- PandasTA integration for indicators
- Bot structure with `bot.pair.ta[freq]`

### What We'll Add (When Ready)
- `RollingCandleBuilder` class
- Polars TA function integration
- Candle type selection API
- Hybrid Pandas/Polars support

---

## Architecture Vision

### Three Candle Paradigms

**1. Standard Fixed (CURRENT)**
```python
engine.initialize_candles(['15min', '1h'], candle_type='standard')
# Matches exchanges exactly
```

**2. Epoch-Aligned (Task 000.1 - 4 hours)**
```python
engine.initialize_candles([7, 23, 89], candle_type='epoch_aligned')
# Arbitrary timeframes, no partials
```

**3. Rolling (FUTURE - 20 hours after Polars TA ready)**
```python
engine.initialize_candles(['15min', '1h'], candle_type='rolling')
# Continuous updates, always complete
```

---

## Documentation References

### Created Documents
1. **`.fstrent_tasks_v2/memory/ROLLING_CANDLES_CONCEPT.md`**
   - Complete explanation of rolling candles
   - Impact on indicators
   - Use cases and trade-offs
   - Performance considerations
   - Integration planning

2. **`.fstrent_tasks_v2/memory/PARTIAL_CANDLE_PROBLEM.md`**
   - Why midnight alignment creates partials
   - Which timeframes affected
   - Mathematical proof of epoch solution
   - Industry comparison

3. **`.fstrent_tasks_v2/memory/THREE_CANDLE_PARADIGMS.md`**
   - Complete comparison of all three approaches
   - When to use each one
   - Real-world scenarios
   - Implementation roadmap

---

## Integration Timeline

### Now
- [x] Document rolling candles concept
- [x] Document three paradigms
- [x] Add notes to Task 000.1

### Core Backtesting Phase (Next 2 weeks)
- [ ] Complete Task 000.1 (epoch alignment)
- [ ] Complete Tasks 002-005 (core backtesting)
- [ ] Validate standard fixed candles work perfectly

### Polars TA Development (User's External Project - 2-4 months)
- [ ] User develops Polars TA library
- [ ] Implements rolling candles in Polars
- [ ] Performance testing and optimization
- [ ] API design finalization

### Integration Phase (After Polars TA Complete - 2-3 weeks)
- [ ] Create `RollingCandleBuilder` class
- [ ] Integrate Polars TA functions
- [ ] Add candle type selection API
- [ ] Comparison testing (fixed vs rolling)
- [ ] Performance benchmarking
- [ ] Documentation and examples

---

## Notes for Future Implementation

### When Polars TA Library is Ready

**Questions to Ask:**
- What's the API design?
- Performance characteristics observed?
- Which indicators work best with rolling?
- Any surprising findings?
- Recommended default settings?

**Integration Checklist:**
- [ ] Review Polars TA architecture
- [ ] Design RollingCandleBuilder
- [ ] Plan bot.pair.ta structure changes
- [ ] Update strategy API
- [ ] Create migration guide
- [ ] Performance test with real data
- [ ] Compare results
- [ ] Update documentation

---

## Key Insights Documented

### User's Critical Insights

**1. Partial Candle Problem:**
> "huge issue with crypto... timeframes not divisible into hour/day create partial candles at midnight boundaries"

**Solution 1:** Epoch alignment (Task 000.1)  
**Solution 2:** Rolling candles (Polars TA)

**2. Rolling Candles Concept:**
> "right handed candles... we are always at the end of the candle regardless of the timeframe... so if we are doing 5min timeframe and the current time is 10:03am the candle start is 9:58"

**Impact:** All indicators repaint, some get better, some get worse

---

## Estimated Effort (When Ready)

**Rolling Candles Integration:**
- RollingCandleBuilder class: 4 hours
- BacktestEngine integration: 4 hours
- Testing and validation: 8 hours
- Documentation: 4 hours
- **Total: 20 hours (10 story points)**

---

## Success Criteria

### For Integration
- [ ] Can create rolling candles for any timeframe
- [ ] Updates every minute (piano player compatible)
- [ ] Performance acceptable (<2x slowdown vs fixed)
- [ ] Strategy can select candle type
- [ ] Indicators work on both Pandas and Polars
- [ ] Clear documentation of differences
- [ ] Comparison examples (fixed vs rolling results)

---

## Related Tasks

- **Task 000:** Piano Player (COMPLETE)
- **Task 000.1:** Epoch Alignment (PENDING - 4 hours)
- **Task 001:** TA Integration (COMPLETE)
- **Future:** Rolling Candles Integration (20 hours)

---

**This is forward-thinking architecture!** 

We're documenting now so integration is smooth when the time comes. The three-paradigm approach will make this the most sophisticated backtesting platform in crypto! 🚀

