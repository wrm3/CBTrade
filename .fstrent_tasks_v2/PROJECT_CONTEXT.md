# Project Context: CBTrade Backtesting System

**Project:** Minute-by-Minute Multi-Timeframe Backtesting Engine  
**Owner:** fstrent (wmartel)  
**Started:** October 10, 2025  
**Status:** Phase 2 - Core Engine Integration

---

## Mission

Build a **revolutionary minute-by-minute multi-timeframe backtesting system** that accurately simulates how repainting indicators and multi-timeframe strategies would have performed historically, using the exact buy/sell logic from the live trading bot.

---

## Current Phase: Engine Integration

**What We're Building:**
- Complete the core BacktestEngine by wiring up technical indicator calculation, buy logic, and sell logic
- Enable accurate simulation of strategy performance on 3+ years of BTC-USDC historical data
- Provide foundation for strategy optimization and walk-forward testing

**Success Criteria:**
- All strategies from `libs/strats/` can be backtested
- Results accurately reflect live trading conditions (repainting indicators, mid-candle entries)
- Performance metrics (return %, win rate, drawdown, Sharpe ratio) generated
- Zero changes required to existing strategy files

---

## Why This Matters

**Problem:** Standard backtesting libraries fail for our strategies because:
1. ❌ They don't simulate indicator repainting (use only closed candles)
2. ❌ They can't handle mid-candle entries (our signals fire during candle development)
3. ❌ They struggle with multi-timeframe synchronization (5m, 15m, 1h, 4h, 1d)

**Solution:** Minute-by-minute replay that builds developing candles for all timeframes simultaneously, allowing indicators to repaint exactly as they do in live trading.

**Impact:** 
- Know which strategies actually work before risking real money
- Find optimal settings for each strategy scientifically
- Measure true risk (drawdown, loss rates) for portfolio management
- Build confidence through accurate historical performance

---

## What's Already Complete

✅ **Phase 1: Data Backfilling** (100% Complete)
- 1,757,005 candles loaded (June 2022 - Oct 2025)
- Covers bear market, sideways, and bull market conditions
- UTC timestamps, DST-safe, no gaps

✅ **Framework Architecture** (100% Complete)
- `BacktestEngine` class with minute-by-minute simulation loop
- `CandleBuilder` class for multi-timeframe candle development
- Performance metrics calculation framework
- Equity curve tracking system

✅ **Documentation** (100% Complete)
- Revolutionary design explained (`backtest/docs/REVOLUTIONARY_DESIGN.md`)
- Visual comparisons (`backtest/docs/VISUAL_COMPARISON.md`)
- Implementation roadmap (`backtest/docs/IMPLEMENTATION_PLAN.md`)

---

## What's In Progress

🟡 **Phase 2: Core Engine Wiring** (33% Complete)
- 3 critical integration points remain (TODOs in `libs/backtest_base.py`)
- Once complete, can run actual backtests on historical data

---

## Technical Context

**Core Files:**
- `libs/backtest_base.py` - Main backtesting engine (needs 3 TODOs completed)
- `libs/buy_base.py` - Buy logic (needs `backtest_mode` flag)
- `libs/sell_base.py` - Sell logic (needs `backtest_mode` flag)
- `libs/bot_ta.py` - Technical indicators (already works)
- `libs/strat_base.py` - Strategy management (already works)

**Database:**
- `ohlcv.ohlcv_BTC_USDC` table: 1.76M rows of 1-minute OHLCV data
- Can build any higher timeframe (5m, 15m, 1h, 4h, 1d) from this base data

**Strategy Files (All Ready for Backtesting):**
- `libs/strats/strat_bb.py` - Bollinger Bands
- `libs/strats/strat_bb_bo.py` - Bollinger Band Breakout
- `libs/strats/strat_sha.py` - SHA (Simple Heikin-Ashi)
- `libs/strats/strat_drop.py` - Drop strategy
- `libs/strats/strat_imp_macd.py` - Improved MACD
- `libs/strats/strat_nwe_*.py` - New Entry strategies (3row, env, rev)
- Plus 20+ more strategies ready to test

---

## Project Constraints

**What We Will NOT Change:**
- ❌ No modifications to existing strategy files (`libs/strats/*.py`)
- ❌ No changes to core buy/sell logic (just add `backtest_mode` flag)
- ❌ No changes to indicator calculations (`libs/bot_ta.py`)
- ❌ No changes to database schema

**Why:** The goal is to test OUR EXACT STRATEGIES as they run live, not create new idealized versions.

**What We Will Add:**
- ✅ Integration layer in `BacktestEngine` to call existing functions
- ✅ `backtest_mode` flag to prevent real API calls
- ✅ Simulated order fills and position tracking
- ✅ Performance metrics and reporting

---

## Success Metrics

**Immediate (This Phase):**
- [ ] Can run `backtest_strategy('BTC-USDC', '2024-01-01', '2024-01-31')` without errors
- [ ] Get performance metrics output (return %, win rate, etc.)
- [ ] Results saved to JSON file

**Near-Term (Next 2 Phases):**
- [ ] Backtest all 30+ strategies on BTC-USDC historical data
- [ ] Identify top 5 performing strategies
- [ ] Find optimal settings for each strategy

**Long-Term (Phases 4-6):**
- [ ] Walk-forward testing to prove strategies adapt to changing markets
- [ ] Multi-strategy portfolio optimization
- [ ] Automated strategy selection based on market regime

---

## Timeline Context

**Started:** October 4, 2025 (data backfilling)  
**Current:** October 10, 2025 (engine integration)  
**Target:** October 17, 2025 (first working backtest results)  

**Total Investment So Far:**
- Data collection: ~6 hours (including CSV approach)
- Framework design: ~8 hours
- Documentation: ~4 hours
- **Total: ~18 hours** (spread over 6 days)

**Remaining Estimate:** ~6-8 hours for engine integration + testing

---

## Related Projects

**Active Projects:**
1. **Live Trading Bot** (`run_bot.py`) - 4 instances running BTC/ETH/SOL markets
2. **Web Dashboard** (`cbtrade_web_v2.py`) - Performance monitoring
3. **Backtesting System** (THIS PROJECT) - Strategy validation

**These Must Coexist:**
- Backtesting must NOT interfere with live trading
- Backtesting uses separate OHLCV database (read-only)
- Backtesting never touches live trading database (cbtrade.*)

---

## Key Stakeholders

**Primary:** fstrent (wmartel) - Creator, developer, trader  
**Users:** fstrent (solo project)  
**Beneficiaries:** Future AI agents learning from this revolutionary approach

---

**This project is the foundation for scientific strategy development and portfolio optimization.** 🚀

