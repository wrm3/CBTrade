---
id: '000.1'
title: 'Piano Player Enhancement: Arbitrary Timeframes & Epoch Alignment'
type: task
status: pending
priority: high
feature: Core Engine Enhancement
subsystems:
  - Backtesting Engine
  - Multi-Timeframe OHLCV System
project_context: Enable the piano player to support arbitrary candle timeframes (3min, 7min, 89min, even 1 week) for machine learning and strategy discovery. Fix the critical "partial candle" problem that occurs with non-standard timeframes by aligning to Unix epoch instead of midnight.
dependencies: ['000']
assigned_agent: null
created_at: "2025-10-10T19:55:00Z"
started_at: null
completed_at: null
error_log: null
complexity_score: 7
expansion_decision: null
memory_consultation: null
story_points: 2
sprint: null
actual_effort: null
---

# Task 000.1: Piano Player Enhancement - Arbitrary Timeframes & Epoch Alignment

## Description
Enhance the `CandleBuilder` class to support arbitrary candle timeframes (not just predefined ones) and fix the critical "partial candle" problem by aligning candle boundaries to Unix epoch instead of midnight UTC.

## The Critical Problem with Current Implementation

### Issue 1: Hardcoded Timeframes Only

**Current Code (Lines 422-432):**
```python
def _freq_to_minutes(self, freq: str) -> int:
    """Convert frequency string to minutes."""
    mapping = {
        '1min': 1,
        '15min': 15,
        '30min': 30,
        '1h': 60,
        '4h': 240,
        '1d': 1440
    }
    return mapping.get(freq, 60)  # ❌ Returns 60 if not found!
```

**Problems:**
- Only supports 6 predefined frequencies
- Can't create 3min, 7min, 89min candles
- Can't create 1 week (10080 min) candles
- Silently defaults to 60min for unknown frequencies (BAD!)

### Issue 2: The "Partial Candle" Problem (CRITICAL!)

**Current Code (Lines 437-449):**
```python
def _get_candle_start_time(self, timestamp: pd.Timestamp) -> pd.Timestamp:
    if self.freq == '1d':
        # Daily candles start at midnight
        return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # ❌ PROBLEM: Aligns to midnight!
        minutes_since_midnight = timestamp.hour * 60 + timestamp.minute
        candle_number = minutes_since_midnight // self.freq_minutes
        start_minute = candle_number * self.freq_minutes
        
        start_hour = start_minute // 60
        start_min = start_minute % 60
        
        return timestamp.replace(hour=start_hour, minute=start_min, 
                                second=0, microsecond=0)
```

**Why This Is A Huge Problem:**

#### Example: 7-minute Candles with Midnight Alignment

**Math:**
- 1 day = 1440 minutes
- 1440 ÷ 7 = 205.714...
- Result: 205 full 7-minute candles (1435 minutes) + **5 minutes leftover**

**What Happens:**
```
Day 1:
00:00-00:07 ✓ Full 7min candle
00:07-00:14 ✓ Full 7min candle
00:14-00:21 ✓ Full 7min candle
...
23:45-23:52 ✓ Full 7min candle
23:52-23:59 ✓ Full 7min candle (last complete one)
23:59-00:00 ❌ PARTIAL! Only 1 minute!

Day 2:
00:00-00:07 ✓ Full 7min candle (resets!)
...
```

**The Problem:**
- Last "candle" of each day is NOT 7 minutes
- It's only 1 minute (or 5 minutes, or whatever's left)
- This creates FAKE candles with wrong OHLCV data
- Indicators calculated on these will be WRONG
- Trading signals will be INCORRECT

#### Real-World Impact Example:

**7-minute RSI calculation at 23:59:**
- Normal candles: 14 candles back = 98 minutes of data
- With partial: 14 candles back = 91 minutes + 1 minute partial = 92 minutes
- RSI calculation is now WRONG because data period is incorrect
- Buy/sell signals at day boundaries will be INACCURATE

**This affects EVERY non-standard timeframe:**
- 3min: 1440 ÷ 3 = 480 ✓ (perfectly divisible, OK)
- 5min: 1440 ÷ 5 = 288 ✓ (OK)
- 7min: 1440 ÷ 7 = 205.71... ❌ (5 min partial)
- 11min: 1440 ÷ 11 = 130.9... ❌ (10 min partial)
- 23min: 1440 ÷ 23 = 62.6... ❌ (14 min partial)
- 89min: 1440 ÷ 89 = 16.2... ❌ (11 min partial)

**Crypto exchanges do this wrong!** Most exchange APIs align non-standard timeframes to midnight, creating these partial candles.

---

## The Solution: Unix Epoch Alignment

### Concept
Instead of aligning to midnight each day, align ALL candles to Unix epoch (1970-01-01 00:00:00 UTC).

**Why This Works:**
- Unix epoch is a fixed point in time
- Calculate minutes since epoch
- Divide by candle minutes, round down
- Multiply back = candle start time
- **Result: ALL candles are always full-length, forever**

### Mathematical Proof

**For 7-minute candles:**

**Midnight alignment (WRONG):**
```
Minutes since midnight: 1437 (23:57)
Candle number: 1437 ÷ 7 = 205.28... → 205
Candle start: 205 × 7 = 1435 minutes (23:55)
Candle range: 23:55-00:00 (5 minutes) ❌ NOT 7 MINUTES!
```

**Epoch alignment (CORRECT):**
```
Timestamp: 2024-06-15 23:57:00 UTC
Minutes since epoch: 28,571,117
Candle number: 28,571,117 ÷ 7 = 4,081,588.14... → 4,081,588
Candle start: 4,081,588 × 7 = 28,571,116 minutes since epoch
Convert back: 2024-06-15 23:54:00 UTC
Candle range: 23:54-00:01 next day (7 minutes) ✓ FULL 7 MINUTES!
```

**Key Insight:** Candles can cross midnight! This is CORRECT behavior.

---

## Required Implementation Changes

### Change 1: Support Arbitrary Timeframes

**New `__init__` signature:**
```python
def __init__(self, freq: str, align_to_epoch: bool = True):
    """
    Initialize candle builder for any frequency.
    
    Args:
        freq: Frequency string like:
            - Named: '15min', '1h', '4h', '1d', '1w'
            - Minutes: '7min', '23min', '89min'
            - Direct integer: freq can be integer minutes
        align_to_epoch: If True, align to Unix epoch (default)
                       If False, align to midnight UTC (legacy mode)
    """
    self.freq = freq
    self.freq_minutes = self._parse_freq_to_minutes(freq)
    self.align_to_epoch = align_to_epoch
    self.epoch_start = pd.Timestamp('1970-01-01 00:00:00', tz='UTC')
    
    # Current developing candle
    self.current_candle = None
    self.current_candle_start = None
    
    # Last completed candle
    self.last_completed = None
```

**New `_parse_freq_to_minutes()`:**
```python
def _parse_freq_to_minutes(self, freq) -> int:
    """
    Parse frequency to minutes. Supports multiple formats.
    
    Supported formats:
        - String named: '15min', '1h', '4h', '1d', '1w'
        - String with number: '7min', '23min', '89min'
        - Integer: 7, 23, 89 (direct minutes)
    
    Examples:
        '15min' → 15
        '1h' → 60
        '4h' → 240
        '1d' → 1440
        '1w' → 10080
        '7min' → 7
        '89min' → 89
        7 → 7
        89 → 89
    """
    # If already integer, return it
    if isinstance(freq, int):
        if freq < 1 or freq > 10080:  # 1 min to 1 week
            raise ValueError(f"Frequency must be 1-10080 minutes, got {freq}")
        return freq
    
    # Named frequencies
    named = {
        '1min': 1,
        '5min': 5,
        '15min': 15,
        '30min': 30,
        '1h': 60,
        '2h': 120,
        '4h': 240,
        '6h': 360,
        '12h': 720,
        '1d': 1440,
        '1w': 10080
    }
    
    if freq in named:
        return named[freq]
    
    # Parse string like '7min', '23min', '89min'
    if freq.endswith('min'):
        try:
            minutes = int(freq[:-3])
            if minutes < 1 or minutes > 10080:
                raise ValueError(f"Frequency must be 1-10080 minutes, got {minutes}")
            return minutes
        except ValueError:
            raise ValueError(f"Invalid frequency format: {freq}")
    
    # Unknown format
    raise ValueError(f"Unknown frequency format: {freq}. Use '15min', '1h', '89min', or integer minutes.")
```

### Change 2: Unix Epoch Alignment

**New `_get_candle_start_time()`:**
```python
def _get_candle_start_time(self, timestamp: pd.Timestamp) -> pd.Timestamp:
    """
    Get the start time of the candle this minute belongs to.
    
    Uses epoch alignment by default to ensure all candles are full-length.
    Can optionally use midnight alignment for compatibility.
    """
    if self.align_to_epoch:
        # ✅ CORRECT: Align to Unix epoch
        # Calculate minutes since epoch
        minutes_since_epoch = int((timestamp - self.epoch_start).total_seconds() / 60)
        
        # Calculate which candle this minute belongs to
        candle_number = minutes_since_epoch // self.freq_minutes
        
        # Calculate candle start in minutes since epoch
        candle_start_minutes = candle_number * self.freq_minutes
        
        # Convert back to timestamp
        return self.epoch_start + pd.Timedelta(minutes=candle_start_minutes)
    
    else:
        # Legacy midnight alignment (can create partial candles!)
        if self.freq_minutes == 1440:  # Daily
            return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # Align to midnight (WARNING: creates partial candles for non-divisible freqs)
            minutes_since_midnight = timestamp.hour * 60 + timestamp.minute
            candle_number = minutes_since_midnight // self.freq_minutes
            start_minute = candle_number * self.freq_minutes
            
            start_hour = start_minute // 60
            start_min = start_minute % 60
            
            return timestamp.replace(hour=start_hour, minute=start_min, 
                                    second=0, microsecond=0)
```

### Change 3: BacktestEngine Integration

**Update `initialize_candle_builders()`:**
```python
def initialize_candle_builders(self, freqs: List, align_to_epoch: bool = True):
    """
    Initialize candle builders for multiple frequencies.
    
    Args:
        freqs: List of frequencies. Can be:
            - Strings: ['15min', '1h', '4h', '1d']
            - Integers: [7, 23, 89, 1440]
            - Mixed: ['15min', 89, '1h', 7]
        align_to_epoch: If True, align all candles to Unix epoch
    """
    self.candle_builders = {}
    self.completed_candles = {}
    
    for freq in freqs:
        # Convert to string key for storage
        if isinstance(freq, int):
            freq_key = f'{freq}min'
        else:
            freq_key = freq
            
        self.candle_builders[freq_key] = CandleBuilder(freq, align_to_epoch)
        self.completed_candles[freq_key] = pd.DataFrame()
```

---

## Machine Learning Use Case

**Why This Matters for ML:**

User wants to test EVERY possible timeframe to discover optimal ones:
```python
# Test all timeframes from 1 minute to 1 week
all_timeframes = list(range(1, 10081))  # 1 to 10080 minutes

# Or specific Fibonacci sequence
fib_timeframes = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]

# Or specific interesting ones
ml_timeframes = [7, 13, 17, 23, 37, 47, 59, 71, 89, 97]  # Prime numbers
```

**Strategy Discovery:**
- Test strategy on 7min candles → 15% annual return
- Test strategy on 13min candles → 18% annual return
- Test strategy on 23min candles → 22% annual return ← OPTIMAL!

**This is IMPOSSIBLE without arbitrary timeframe support!**

---

## Testing Requirements

### Unit Tests

**Test 1: Parse Arbitrary Frequencies**
```python
def test_parse_freq_to_minutes():
    cb = CandleBuilder('7min')
    assert cb.freq_minutes == 7
    
    cb = CandleBuilder('89min')
    assert cb.freq_minutes == 89
    
    cb = CandleBuilder(23)
    assert cb.freq_minutes == 23
    
    cb = CandleBuilder('1w')
    assert cb.freq_minutes == 10080
```

**Test 2: Epoch Alignment (CRITICAL!)**
```python
def test_epoch_alignment_no_partial_candles():
    """
    Verify 7min candles with epoch alignment are ALWAYS 7 minutes.
    Test across midnight boundary.
    """
    cb = CandleBuilder('7min', align_to_epoch=True)
    
    # Test timestamp near midnight
    ts1 = pd.Timestamp('2024-06-15 23:54:00', tz='UTC')
    ts2 = pd.Timestamp('2024-06-15 23:57:00', tz='UTC')
    ts3 = pd.Timestamp('2024-06-16 00:00:00', tz='UTC')
    ts4 = pd.Timestamp('2024-06-16 00:01:00', tz='UTC')
    
    start1 = cb._get_candle_start_time(ts1)
    start2 = cb._get_candle_start_time(ts2)
    start3 = cb._get_candle_start_time(ts3)
    start4 = cb._get_candle_start_time(ts4)
    
    # All should be in same 7-minute candle that crosses midnight
    assert start1 == start2 == start3 == start4
    
    # Verify candle is exactly 7 minutes
    candle_end = start1 + pd.Timedelta(minutes=7)
    assert candle_end == start1 + pd.Timedelta(minutes=7)
```

**Test 3: Midnight Alignment (Legacy Mode)**
```python
def test_midnight_alignment_creates_partial():
    """
    Document that midnight alignment DOES create partial candles.
    This is expected legacy behavior.
    """
    cb = CandleBuilder('7min', align_to_epoch=False)
    
    # Last minute of day
    ts = pd.Timestamp('2024-06-15 23:59:00', tz='UTC')
    start = cb._get_candle_start_time(ts)
    
    # Should align to 23:55 (last full 7min in day)
    # But this creates a 4-minute candle (23:55-23:59)
    # This is the PROBLEM we're documenting
    assert start.hour == 23
    assert start.minute == 52  # Actually 23:52 is last full 7min boundary before midnight
```

**Test 4: All Standard Timeframes Still Work**
```python
def test_standard_timeframes():
    """Verify standard timeframes still work correctly."""
    for freq in ['1min', '5min', '15min', '30min', '1h', '4h', '1d', '1w']:
        cb = CandleBuilder(freq)
        assert cb.freq_minutes > 0
```

### Integration Tests

**Test with Real BTC Data:**
- Load 1 week of BTC 1min data
- Build 7min candles with epoch alignment
- Build 7min candles with midnight alignment
- Compare:
  - Epoch: All candles exactly 7 minutes ✓
  - Midnight: Last candle of each day is partial ❌
- Verify epoch alignment produces correct OHLCV values

---

## Acceptance Criteria

- [ ] `CandleBuilder` accepts integer minutes (7, 23, 89)
- [ ] `CandleBuilder` accepts string format ('7min', '89min')
- [ ] `CandleBuilder` accepts named formats ('1w', '1d', '4h')
- [ ] `CandleBuilder` supports 1 minute through 1 week (10080 min)
- [ ] Epoch alignment is DEFAULT behavior
- [ ] Epoch alignment produces ZERO partial candles
- [ ] Epoch-aligned candles can cross midnight boundaries
- [ ] Legacy midnight alignment available with flag
- [ ] Unit tests verify no partial candles with epoch alignment
- [ ] Unit tests document partial candles with midnight alignment
- [ ] Integration test with real BTC data confirms accuracy
- [ ] Documentation updated with alignment explanation
- [ ] `BacktestEngine` can initialize arbitrary timeframe lists

---

## Files to Modify

**Primary:**
- `libs/backtest_base.py` - Lines 405-449 (CandleBuilder class)
  - Rewrite `__init__` to accept align_to_epoch parameter
  - Replace `_freq_to_minutes` with `_parse_freq_to_minutes`
  - Rewrite `_get_candle_start_time` with epoch alignment logic

**Testing:**
- `backtest/test_arbitrary_timeframes.py` (NEW) - Unit tests
- `backtest/test_epoch_alignment.py` (NEW) - Integration tests

**Documentation:**
- `backtest/docs/ARBITRARY_TIMEFRAMES.md` (NEW) - Explain the feature
- `backtest/docs/EPOCH_ALIGNMENT.md` (NEW) - Explain the partial candle problem

---

## Priority Justification

**HIGH Priority because:**
1. **Blocks ML Use Case:** Can't do strategy discovery without arbitrary timeframes
2. **Data Accuracy:** Current implementation would produce WRONG results for non-standard timeframes
3. **Affects All Future Work:** This is foundation-level functionality
4. **Crypto Industry Problem:** Most exchanges get this wrong - we can do it RIGHT

---

## Estimated Effort

**2 Story Points (4 hours)**

**Breakdown:**
- Code changes: 1.5 hours
  - Rewrite `_parse_freq_to_minutes`: 0.5h
  - Rewrite `_get_candle_start_time`: 0.5h
  - Update `initialize_candle_builders`: 0.25h
  - Testing & debugging: 0.25h

- Unit tests: 1 hour
  - Test frequency parsing
  - Test epoch alignment
  - Test midnight alignment (legacy)
  - Test edge cases

- Integration tests: 1 hour
  - Real BTC data test
  - Cross-midnight candles
  - Compare epoch vs midnight
  - Verify OHLCV accuracy

- Documentation: 0.5 hours
  - Update REVOLUTIONARY_DESIGN.md
  - Create ARBITRARY_TIMEFRAMES.md
  - Create EPOCH_ALIGNMENT.md

---

## User Quote (The Insight)

> "I belive that this is a huge issue with crypto, when you get outside of the normal candle timeframes... is that all of the ohclv that is not perfectly divisible into an hour or day etc... often has its start = to the that dat at midnite (utc often) and so as a result if the timeframe is not equally divisible you get blocks of time shorter than a full candlestick, have the value of a full candlestick"

**This is a CRITICAL insight that most backtesting systems get WRONG!** ✅

---

## Related Future Enhancement: Rolling Candles

**Note:** User is developing a Polars-based TA library that includes another solution to the partial candle problem: **Rolling Candles** (right-handed candles).

**See:** `.fstrent_tasks_v2/memory/ROLLING_CANDLES_CONCEPT.md`

**Key Difference:**
- **This task (000.1):** Fixed candles aligned to epoch (no partials)
- **Rolling candles:** Continuously updating window (always at current time)

**Example:**
```
Epoch-aligned 7min at 10:03:
  Candle: 9:59-10:06 (still developing, fixed boundary)

Rolling 7min at 10:03:
  Candle: 9:56-10:03 (complete window, updates every minute)
```

**Integration:** After this task and core backtesting complete, will integrate user's Polars TA library which supports both approaches.

**Three Paradigms:**
1. Standard fixed (exchange compatibility)
2. Epoch-aligned fixed (this task - no partials)
3. Rolling (future - continuous updates)

**We'll support all three!** 🎯

---

## Next Steps

1. Review and approve this task
2. Implement the changes in `libs/backtest_base.py`
3. Write comprehensive unit tests
4. Run integration tests with real BTC data
5. Update documentation
6. Test with ML strategy discovery use case

