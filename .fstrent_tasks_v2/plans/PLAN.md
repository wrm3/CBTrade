# PRD: Minute-by-Minute Multi-Timeframe Backtesting System

**Version:** 1.0  
**Date:** October 10, 2025  
**Author:** fstrent (wmartel)  
**Status:** Phase 2 - Engine Integration

---

## 1. Product Overview

### 1.1 Document Title and Version
- **PRD:** CBTrade Backtesting Engine - Phase 2 Integration
- **Version:** 1.0
- **Scope Validation:** October 10, 2025

### 1.2 Product Summary

A revolutionary minute-by-minute multi-timeframe backtesting engine that accurately simulates how trading strategies with repainting indicators would have performed historically. Unlike standard backtesting libraries that only use closed candles, this system replays history minute-by-minute, building developing candles for all timeframes (5m, 15m, 1h, 4h, 1d) simultaneously.

The system integrates directly with existing live trading bot code (`libs/buy_base.py`, `libs/sell_base.py`, `libs/bot_ta.py`, `libs/strat_base.py`) requiring ZERO changes to strategy files. This ensures backtest results accurately reflect live trading behavior, including indicator repainting, mid-candle entries, and complex multi-timeframe logic.

### 1.3 Scope Validation Summary
- **Validated User Context:** Solo developer/trader (personal project)
- **Validated Complexity:** Advanced (multi-timeframe simulation, complex integration)
- **Validated Technical Scope:** Custom engine integration with existing codebase
- **Validated Feature Scope:** Core engine completion (3 integration TODOs)

---

## 2. Goals with Scope Boundaries

### 2.1 Business Goals
- Enable scientific strategy validation before risking real capital
- Identify top-performing strategies across different market conditions
- Find optimal parameter settings for each strategy
- Measure true risk metrics (max drawdown, loss rates) for portfolio management
- Build trader confidence through accurate historical performance data

### 2.2 User Goals
- Run backtests on 30+ existing strategies without modifying strategy code
- Get accurate performance metrics (return %, win rate, Sharpe ratio, max drawdown)
- Identify which strategies work in bear/sideways/bull markets
- Optimize strategy parameters using historical data
- Validate strategy performance before deploying to live trading

### 2.3 Explicit Non-Goals (Over-Engineering Prevention)
- ❌ **Machine learning integration** (future phase, not now)
- ❌ **Real-time paper trading** (separate project)
- ❌ **Multi-asset portfolio optimization** (future phase)
- ❌ **Cloud-based distributed backtesting** (single machine sufficient)
- ❌ **GUI/dashboard for backtest results** (JSON export sufficient)
- ❌ **Strategy refactoring or improvement** (test existing code as-is)
- ❌ **New indicator development** (use existing TA library)

---

## 3. User Personas & Access Scope

### 3.1 Validated User Types
- **Primary:** Solo trader/developer running local backtests

### 3.2 Scope-Appropriate Persona Details
- **Trader-Developer (fstrent)**: 
  - Runs 4 live trading bot instances (BTC/ETH/SOL/altcoins)
  - Has 30+ trading strategies in production
  - Needs to validate new strategies before deploying
  - Wants to optimize existing strategy parameters
  - Comfortable with Python, terminal commands, JSON output
  - No need for GUI or web interface

### 3.3 Access Control Scope
- **Access Model:** Single user, local filesystem access
- **Scope Justification:** Personal project, no multi-user or role-based access needed

---

## 4. Functional Requirements with Scope Validation

### 4.1 Core Engine Integration (Priority: CRITICAL) - [Scope: Essential]

**REQ-001: Technical Indicator Integration**
- **Location:** `libs/backtest_base.py` line 254
- **What:** Call `bot.ta_calc()` or equivalent for each timeframe with developing candles
- **Why:** Strategies need indicators (RSI, MACD, Bollinger Bands, etc.) calculated on current candle state
- **Acceptance:**
  - ✓ Indicators calculate using developing candles (not just closed)
  - ✓ All timeframes (5m, 15m, 1h, 4h, 1d) have indicators updated
  - ✓ Indicators stored in bot state for strategy access
  - ✓ Repainting behavior matches live trading

**REQ-002: Buy Logic Integration**
- **Location:** `libs/backtest_base.py` line 263
- **What:** Integrate `buy_strats_check()` from `libs/buy_base.py`
- **Why:** Need to detect buy signals from all active strategies
- **Acceptance:**
  - ✓ All buy denials respected (timing delays, test mode, budget constraints)
  - ✓ Buy signals trigger at correct minute (mid-candle)
  - ✓ Trade size calculated using `buy_size_budget_calc()`
  - ✓ Position opened with correct entry price (current minute's close)
  - ✓ Budget decremented appropriately

**REQ-003: Sell Logic Integration**
- **Location:** `libs/backtest_base.py` line 278
- **What:** Integrate `sell_strats_check()` from `libs/sell_base.py`
- **Why:** Need to detect exit signals (strategy exits, stop losses, take profits)
- **Acceptance:**
  - ✓ Sell signals trigger at correct minute (mid-candle)
  - ✓ Position closed with correct exit price
  - ✓ P&L calculated accurately
  - ✓ Budget incremented with sale proceeds
  - ✓ Position tracking updated

### 4.2 Backtest Mode Flag (Priority: HIGH) - [Scope: Essential]

**REQ-004: Prevent Real API Calls**
- **What:** Add `backtest_mode` flag to BOT class
- **Why:** Prevent actual Coinbase API order placement during backtests
- **Files Affected:**
  - `libs/bot_base.py` (BOT class initialization)
  - `libs/buy_base.py` (`buy_live()` function)
  - `libs/bot_coinbase.py` (API call wrappers)
- **Acceptance:**
  - ✓ `bot.backtest_mode = True` prevents all real API calls
  - ✓ Simulated order fills instead of real orders
  - ✓ No impact on live trading when `backtest_mode = False`

### 4.3 Performance Metrics (Priority: HIGH) - [Scope: Essential]

**REQ-005: Calculate Standard Metrics**
- **Already Implemented:** `libs/backtest_base.py` lines 290-342
- **Metrics:**
  - Total return (%)
  - Win rate (%)
  - Profit factor
  - Max drawdown (%)
  - Sharpe ratio
  - Average win/loss ($)
  - Total trades count
- **Output:** JSON file with all metrics

**REQ-006: Strategy-Specific Breakdown**
- **What:** Per-strategy performance metrics
- **Why:** Identify best/worst performing strategies
- **Acceptance:**
  - ✓ Each strategy's trade count, return %, win rate
  - ✓ Sortable by performance
  - ✓ Included in JSON output

### 4.4 Scope Compliance Validation
- ✓ All requirements align with "engine integration" scope
- ✓ No over-engineering beyond scope validation
- ✓ Complexity matches developer's comfort level
- ✓ Technical approach matches single-user deployment
- ✓ No unnecessary features (GUI, cloud, ML, etc.)

---

## 5. User Experience with Scope Constraints

### 5.1 Entry Points & Scope-Appropriate Flow
- **Primary:** Command-line script execution
- **Input:** Product ID, start date, end date, starting balance
- **Output:** Console progress + JSON results file

### 5.2 Core Experience within Scope

**Step 1: Run Backtest Command**
```bash
uv run python backtest/backtest_example.py
```

**Step 2: See Progress Output**
```
Processing: BTC-USDC 2024-01-01 to 2024-01-31
Total Minutes: 44,640
Progress: [████████████████████] 100%
Elapsed: 45 seconds
```

**Step 3: Review Results**
```
BACKTEST RESULTS
─────────────────────────
Starting Balance: $10,000.00
Ending Balance: $11,250.50
Total Return: 12.51%

Total Trades: 45
Win Rate: 64.4%
Max Drawdown: -5.2%
Sharpe Ratio: 1.8

Results saved to: backtest_results_BTC-USDC_2024-01-01_2024-01-31.json
```

**Step 4: Analyze JSON Output**
- Open JSON file in text editor or Python
- Review equity curve, per-strategy breakdown
- Compare multiple backtest runs

### 5.3 Advanced Features & Scope Boundaries
- ✅ **Multiple strategies:** Test all strategies in single run
- ✅ **Date range selection:** Any period with available data
- ✅ **JSON export:** Complete results for external analysis
- ❌ **GUI:** Not in scope (command-line sufficient)
- ❌ **Real-time visualization:** Not in scope (review after completion)
- ❌ **Parameter optimization:** Future phase (manual testing for now)

### 5.4 UI/UX Aligned with Scope
- **Console output:** Simple progress bar and summary table
- **JSON files:** Machine-readable for scripting/analysis
- **No GUI:** Developer comfortable with command-line tools

---

## 6. Narrative with Scope Context

**Trader discovers new strategy idea:**  
fstrent reviews trading patterns and has an idea for a new Bollinger Band breakout variant. Before coding it up and risking real money, he wants to test a similar existing strategy on historical data.

**Running the backtest:**  
He opens a terminal, navigates to the project directory, and runs:
```bash
uv run python backtest/backtest_example.py
```

The system loads 1.76M minutes of BTC-USDC data from the database and begins replaying history minute-by-minute. Every minute, it:
1. Updates all developing candles (5m, 15m, 1h, 4h, 1d)
2. Recalculates indicators (repainting as they would live)
3. Checks for buy signals from all 30+ strategies
4. Checks for sell signals on open positions
5. Tracks portfolio value and updates equity curve

**Progress feedback:**  
A simple progress bar shows completion percentage and estimated time remaining. On his modest laptop, it processes ~600 minutes per second, so testing 6 months of data takes about 2 minutes.

**Reviewing results:**  
The backtest completes and displays a summary table showing total return, win rate, max drawdown, and other key metrics. The `bb_bo` (Bollinger Band Breakout) strategy had a 64% win rate and 18.5% return over the period - impressive!

**Deeper analysis:**  
He opens the JSON results file to see the detailed equity curve and per-strategy breakdown. He notices the strategy performed well in the bull market (Q1 2024) but struggled in sideways consolidation (Q2 2024). This insight helps him decide to only activate this strategy when his broader market regime filter indicates uptrend conditions.

**Confident deployment:**  
Armed with accurate historical performance data, he confidently adds the strategy to his live trading bot, knowing it aligns with his risk tolerance and has proven profitability across diverse market conditions.

---

## 7. Success Metrics Aligned with Scope

### 7.1 User-Centric Metrics
- **Time to first backtest:** < 5 minutes from command execution
- **Backtest speed:** > 500 minutes/second processing rate
- **Result accuracy:** Matches live trading within 2% variance
- **Developer satisfaction:** Can test ideas before deploying live

### 7.2 Business Metrics
- **Strategy validation:** All 30+ strategies testable
- **Risk reduction:** Catch unprofitable strategies before losses
- **Capital efficiency:** Deploy funds to proven strategies only
- **Confidence building:** Historical data validates strategy viability

### 7.3 Technical Metrics
- **Processing speed:** ~600 minutes/second on 2024 laptop
- **Memory usage:** < 2GB RAM for 1-year backtest
- **Disk I/O:** Efficient database queries, no unnecessary reads
- **Code reuse:** 100% of existing strategy code works without changes

---

## 8. Technical Considerations with Scope Validation

### 8.1 Scope-Validated Affected Subsystems
- **Primary subsystems** (aligned with complexity scope):
  - Backtesting Engine (`libs/backtest_base.py`) - Core integration needed
  - Buy Logic (`libs/buy_base.py`) - Add `backtest_mode` flag
  - Sell Logic (`libs/sell_base.py`) - Add `backtest_mode` flag
  - Bot Core (`libs/bot_base.py`) - Add `backtest_mode` flag
  
- **Secondary subsystems** (validated against integration scope):
  - Technical Indicators (`libs/bot_ta.py`) - Already compatible (no changes)
  - Strategy Management (`libs/strat_base.py`) - Already compatible (no changes)
  - OHLCV Database (`ohlcv.ohlcv_BTC_USDC`) - Read-only access (no changes)

### 8.2 Integration Points within Scope
- **Database:** Read-only queries to `ohlcv.ohlcv_BTC_USDC` table (1.76M rows)
- **Strategies:** Import all strategy files from `libs/strats/` (30+ files)
- **Indicators:** Call `bot_ta.py` functions with developing candle data
- **Buy/Sell Logic:** Call existing functions with `backtest_mode=True`

### 8.3 Data Storage & Privacy Aligned with Scope
- **Input:** Historical OHLCV data (public market data, no privacy concerns)
- **Output:** JSON files saved locally (no cloud storage needed)
- **Privacy:** Single user, local filesystem, no data sharing

### 8.4 Scalability & Performance within Scope
- **Current:** ~600 minutes/second on single machine
- **Target:** ~1000 minutes/second after optimization
- **Scale:** Sufficient for 3+ years of minute data
- **No distributed computing needed:** Single-threaded adequate for scope

### 8.5 Scope-Identified Challenges
- **Challenge 1:** Indicator state management
  - **Risk:** Indicators need different history lengths (50-200 bars)
  - **Solution:** Build complete history before signaling strategies
  - **Within scope:** Use existing TA library functions

- **Challenge 2:** Budget tracking complexity
  - **Risk:** Multiple strategies competing for same budget
  - **Solution:** Respect existing budget allocation logic from live bot
  - **Within scope:** No changes to budget calculation code

- **Challenge 3:** Execution timing precision
  - **Risk:** Must track exact minute of signal for accurate entry price
  - **Solution:** Use timestamp from minute bar, not candle close
  - **Within scope:** Already designed in `CandleBuilder` class

---

## 9. Milestones & Sequencing with Scope Integration

### 9.1 Scope-Validated Project Estimate
- **Size:** Small-Medium (3 integration points + testing)
- **Time:** 6-8 hours development + 2-4 hours testing

### 9.2 Team Size & Composition for Scope
- **Solo developer:** fstrent (full-stack capability)
- **Resources:** Existing codebase, documentation, 1.76M data rows ready

### 9.3 Scope-Phased Delivery

**Phase 2a: Core Integration** (4 hours - Current Phase)
- Complete REQ-001: TA indicator integration (TODO line 254)
- Complete REQ-002: Buy logic integration (TODO line 263)  
- Complete REQ-003: Sell logic integration (TODO line 278)
- Add REQ-004: `backtest_mode` flag to prevent real orders
- **Deliverable:** Working backtest engine that processes data without errors

**Phase 2b: Testing & Validation** (2-4 hours)
- Run backtests on known periods (Jan 2024, Jun 2024)
- Validate results match expected behavior
- Fix any bugs discovered during testing
- Document any edge cases or limitations
- **Deliverable:** Validated backtest results matching live trading behavior

**Phase 3: Strategy Analysis** (Future - 8-12 hours)
- Backtest all 30+ strategies on full historical data
- Generate performance comparison reports
- Identify top 5 performing strategies
- Document strategy strengths/weaknesses by market regime
- **Deliverable:** Strategy performance analysis report

**Phase 4: Parameter Optimization** (Future - 16-24 hours)
- Implement grid search over parameter ranges
- Test parameter combinations for each strategy
- Implement walk-forward testing methodology
- Validate parameters don't overfit historical data
- **Deliverable:** Optimized parameter settings for each strategy

---

## 10. User Stories with Scope Validation

### 10.1 Core Integration User Stories (Essential Scope)

**US-001: TA Indicator Calculation**
- **ID:** US-001
- **Scope:** Essential (REQ-001)
- **Description:** As a trader, I want indicators to calculate on developing candles so that backtest signals match live trading repainting behavior.
- **Acceptance Criteria:**
  - ✓ RSI calculates correctly on developing 15min candle
  - ✓ MACD calculates correctly on developing 1h candle
  - ✓ Bollinger Bands calculate correctly on developing 4h candle
  - ✓ Moving averages calculate correctly on developing 1d candle
  - ✓ All indicators accessible to strategy buy/sell logic

**US-002: Buy Signal Detection**
- **ID:** US-002
- **Scope:** Essential (REQ-002)
- **Description:** As a trader, I want buy signals to trigger at the exact minute conditions are met so that entry prices match real-world execution.
- **Acceptance Criteria:**
  - ✓ `buy_strats_check()` called every minute during backtest
  - ✓ Buy signals respect timing delays (15min, 1h, etc.)
  - ✓ Buy signals respect budget constraints
  - ✓ Buy signals respect test mode vs live mode logic
  - ✓ Entry price equals current minute's close price
  - ✓ Position opened and tracked in backtest state

**US-003: Sell Signal Detection**
- **ID:** US-003
- **Scope:** Essential (REQ-003)
- **Description:** As a trader, I want sell signals to trigger at the exact minute conditions are met so that exit prices and P&L match reality.
- **Acceptance Criteria:**
  - ✓ `sell_strats_check()` called every minute for open positions
  - ✓ Strategy exit signals trigger correctly
  - ✓ Stop loss triggers if price hits stop level
  - ✓ Take profit triggers if price hits target
  - ✓ Exit price equals current minute's close price
  - ✓ P&L calculated correctly (exit price - entry price)
  - ✓ Position closed and removed from tracking

### 10.2 Testing & Validation User Stories (Essential Scope)

**US-004: Single Strategy Backtest**
- **ID:** US-004
- **Scope:** Essential (Testing)
- **Description:** As a trader, I want to test a single strategy on a known time period so that I can validate the engine works correctly.
- **Acceptance Criteria:**
  - ✓ Can specify strategy name (e.g., "bb_bo")
  - ✓ Can specify date range (e.g., "2024-01-01" to "2024-01-31")
  - ✓ Backtest completes without errors
  - ✓ Performance metrics output to console
  - ✓ Results saved to JSON file

**US-005: All Strategies Backtest**
- **ID:** US-005
- **Scope:** Essential (Testing)
- **Description:** As a trader, I want to test all strategies simultaneously so that I can compare their performance.
- **Acceptance Criteria:**
  - ✓ All 30+ strategies from `libs/strats/` tested
  - ✓ Per-strategy performance breakdown in results
  - ✓ Can identify best/worst performing strategies
  - ✓ Total portfolio metrics calculated

**US-006: Result Validation**
- **ID:** US-006
- **Scope:** Essential (Testing)
- **Description:** As a trader, I want backtest results to match live trading behavior so that I can trust the performance metrics.
- **Acceptance Criteria:**
  - ✓ Win rate matches expected range for known strategies
  - ✓ Return % reasonable for given market conditions
  - ✓ Trade count matches expected signal frequency
  - ✓ No impossible results (>1000% returns, <0% losses, etc.)

---

## 11. Scope Validation & Change Management

### 11.1 Scope Validation Checklist
- [x] All requirements align with "core engine integration" scope
- [x] No over-engineering beyond essential functionality
- [x] Complexity matches single-user developer comfort level
- [x] Technical approach matches local deployment scope
- [x] No GUI, cloud, or ML features (explicitly out of scope)

### 11.2 Scope Change Process
- **Change Request:** Create new task in `.fstrent_tasks/tasks/` with justification
- **Impact Assessment:** Evaluate effect on timeline and complexity
- **Approval Required:** Self-approval (solo project) + document rationale
- **Documentation Update:** Update this PRD and PROJECT_CONTEXT.md

### 11.3 Approved Scope Boundaries
- ✅ **Core engine:** TA integration, buy logic, sell logic
- ✅ **Testing:** Validation on known periods
- ✅ **Output:** JSON files with performance metrics
- ❌ **Parameter optimization:** Future phase (not Phase 2)
- ❌ **Walk-forward testing:** Future phase (not Phase 2)
- ❌ **GUI/dashboard:** Never in scope (command-line sufficient)
- ❌ **Cloud deployment:** Never in scope (local sufficient)
- ❌ **Machine learning:** Future consideration (not current scope)

---

**This PRD defines the exact scope for completing the revolutionary backtesting engine integration, enabling accurate strategy validation before risking real capital.** 🎯

