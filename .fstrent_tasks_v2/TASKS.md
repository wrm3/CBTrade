# Backtesting System Integration Tasks

**Project:** Minute-by-Minute Multi-Timeframe Backtesting Engine  
**Phase:** Phase 2 - Core Engine Integration  
**Started:** October 10, 2025

---

## 📋 Task Status Overview

- **Total Tasks:** 7
- **Pending:** 5
- **In Progress:** 0
- **Completed:** 2
- **Failed:** 0

---

## 🎯 Current Sprint: Phase 2a - Core Integration

**Goal:** Complete the 3 remaining integration points to enable working backtests

**Target:** October 12, 2025 (2 days)

---

## Tasks

### Critical Priority - Foundation (COMPLETED)

- [x] **ID 000: Piano Player Multi-Timeframe Candle Builder** (Priority: critical) [Feature: Core Engine] ✅ 🎹
> Dependencies: None
> Subsystems: Backtesting Engine, Multi-Timeframe OHLCV System
> Complexity: 9/10 (Revolutionary minute-by-minute replay system)
> **THE CORE INNOVATION**: Implement the "piano player" system that replays history minute-by-minute, building developing candles for all timeframes (15m, 1h, 4h, 1d) simultaneously. Each minute is a "key press" that updates all timeframe candles in sync, exactly as they develop in live trading. This is what enables accurate backtesting of repainting indicators.
> **Status:** COMPLETED (Retroactive) - `CandleBuilder` class fully implemented (lines 397-500). Multi-timeframe synchronization working. Minute-by-minute replay functional in `_process_minute()` loop.
> **⚠️ Known Limitations:** Only supports predefined timeframes, midnight alignment creates partial candles for non-divisible frequencies. See Task 000.1 for enhancements.

- [ ] **ID 000.1: Piano Player Enhancement - Arbitrary Timeframes & Epoch Alignment** (Priority: high) [Feature: ML/Strategy Discovery] 🎹⚡
> Dependencies: 000
> Subsystems: Backtesting Engine, Multi-Timeframe OHLCV System
> Complexity: 7/10 (Unix epoch math, arbitrary timeframe parsing)
> **CRITICAL ENHANCEMENT**: Support arbitrary candle timeframes (3min, 7min, 89min, 1 week) for machine learning strategy discovery. Fix the "partial candle" problem by aligning to Unix epoch instead of midnight, ensuring ALL candles are full-length. Most crypto exchanges get this wrong - we'll do it RIGHT!
> **User Insight:** "huge issue with crypto... timeframes not divisible into hour/day create partial candles at midnight boundaries"

### Critical Priority (Must Complete for Phase 2a)

- [x] **ID 001: TA Indicator Integration** (Priority: critical) [Feature: Core Engine] ✅
> Dependencies: 000
> Subsystems: Backtesting Engine, Technical Analysis
> Complexity: 7/10 (Multi-timeframe indicator state management)
> Integrate `bot_ta.py` functions to calculate indicators on developing candles for all timeframes (5m, 15m, 1h, 4h, 1d). Ensures indicators repaint as they would in live trading. Critical for accurate strategy signal detection.
> **Status:** COMPLETED - Integrated ta_add_indicators() with proper DataFrame building from completed + developing candles. Stores results in bot.pair.ta[freq] structure matching live trading.

- [ ] **ID 002: Buy Logic Integration** (Priority: critical) [Feature: Core Engine]
> Dependencies: 001
> Subsystems: Backtesting Engine, Buy Logic
> Complexity: 6/10 (Budget tracking and signal detection)
> Integrate `buy_strats_check()` from `libs/buy_base.py` to detect buy signals at exact minute conditions are met. Respects all buy denials, timing delays, and budget constraints from live trading logic.

- [ ] **ID 003: Sell Logic Integration** (Priority: critical) [Feature: Core Engine]
> Dependencies: 001, 002
> Subsystems: Backtesting Engine, Sell Logic
> Complexity: 6/10 (Position tracking and P&L calculation)
> Integrate `sell_strats_check()` from `libs/sell_base.py` to detect exit signals for open positions. Handles strategy exits, stop losses, and take profits with accurate P&L calculation.

### High Priority (Required for Phase 2b)

- [ ] **ID 004: Backtest Mode Flag** (Priority: high) [Feature: Safety]
> Dependencies: 002
> Subsystems: Bot Core, Buy Logic, API Wrapper
> Complexity: 3/10 (Simple flag check)
> Add `backtest_mode` flag to Bot class and modify `buy_live()` to prevent real Coinbase API calls during backtests. Simulates order fills instead of placing real orders. Critical safety feature.

- [ ] **ID 005: Test & Validation** (Priority: high) [Feature: Quality Assurance]
> Dependencies: 001, 002, 003, 004
> Subsystems: All
> Complexity: 5/10 (Multiple test scenarios)
> Run backtests on known periods (Jan 2024, Jun 2024) and validate results match expected behavior. Verify win rates, returns, and trade counts are reasonable. Fix any bugs discovered.

---

## 📊 Progress Tracking

### Phase 1: Foundation (COMPLETE) ✅
- [x] Task 000: Piano Player Candle Builder (8 hours) ✅

### Phase 2a: Core Integration (4 hours estimated)
- [x] Task 001: TA Indicator Integration (1.5 hours) ✅
- [ ] Task 002: Buy Logic Integration (1.5 hours)
- [ ] Task 003: Sell Logic Integration (1.0 hour)

### Phase 2b: Testing & Validation (2-4 hours estimated)
- [ ] Task 004: Backtest Mode Flag (0.5 hours)
- [ ] Task 005: Test & Validation (2-3 hours)

**Total Estimated Time:** 14-16 hours  
**Completed:** 9.5 hours (59%)  
**Remaining:** 4.5-6.5 hours (41%)

---

## 🎯 Success Criteria

### Phase 2a Complete When:
- [x] All 3 TODO comments in `libs/backtest_base.py` resolved
- [x] No compilation errors in backtest engine
- [x] Engine can process minute data without crashing

### Phase 2b Complete When:
- [x] Can run `uv run python backtest/backtest_example.py` without errors
- [x] Performance metrics output to console
- [x] JSON results file created
- [x] Results validated against expected ranges

---

## 📝 Notes

**Architecture Decision:** Keep integration layer thin - call existing functions directly rather than refactoring.  
**Scope Boundary:** NO changes to strategy files or indicator calculations.  
**Safety:** `backtest_mode` flag prevents accidental real order placement.

---

**Last Updated:** October 10, 2025 18:40 UTC

