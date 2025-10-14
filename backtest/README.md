# Backtesting System

Comprehensive minute-by-minute multi-timeframe backtesting system for trading strategies.

---

## 📁 Quick Start

### 1. **Backfill Historical Data**
```bash
# Run from project root
uv run python backtest/backfill_ohlcv_btc.py
```

**What it does:**
- Downloads BTC-USDC 1-minute candles from June 1, 2022 to October 4, 2024
- ~1.2 million candles (~120 MB)
- Takes ~51 minutes (conservative rate to avoid API limits)
- Safe to run while trading bots are active

**Details:** See [docs/BACKFILL_GUIDE.md](docs/BACKFILL_GUIDE.md)

---

### 2. **Run Backtest**
```bash
# Run from project root
uv run python backtest/backtest_example.py
```

**What it does:**
- Simulates your strategies on historical data
- Tests buy/sell logic across market conditions
- Generates performance metrics
- Saves results to JSON

**Outputs:**
- Win rate, return %, max drawdown
- Sharpe ratio, profit factor
- Per-strategy breakdown
- Equity curve over time

---

## 📊 What This System Does

### Minute-by-Minute Simulation
Unlike standard backtesting libraries that only use closed candles, this system:

✅ **Simulates candle development** - Builds 5m, 15m, 1h, 4h, 1d candles minute-by-minute  
✅ **Handles repainting indicators** - Indicators recalculate as candles develop  
✅ **Multi-timeframe accuracy** - All timeframes stay in sync  
✅ **Uses your exact buy/sell logic** - No changes to strategy files  

**Result:** Realistic backtest results that reflect actual trading conditions

---

## 🗂️ Files in This Folder

```
backtest/
├── README.md                      # This file
├── backfill_ohlcv_btc.py         # Historical data download script
├── backtest_example.py            # Example backtest usage
└── docs/
    ├── REVOLUTIONARY_DESIGN.md   # 🔥 WHY this approach is revolutionary
    ├── VISUAL_COMPARISON.md      # 📊 Visual diagrams comparing approaches
    ├── BACKFILL_GUIDE.md         # Detailed backfill instructions
    ├── IMPLEMENTATION_PLAN.md    # Full system architecture & roadmap
    └── SUMMARY.md                # Quick reference guide
```

**Core Engine:** `libs/backtest_base.py` (in project libs folder)

---

## 🎯 Market Coverage

### BTC-USDC: June 2022 - October 2024 (~2.5 years)

```
2022 (Jun-Dec): Bear Market Tail
├─ $30k → $15.5k (-48% drop)
└─ Final capitulation phase

2023: Full Recovery + Sideways Chop
├─ $15.5k → $31k (100% gain)
├─ Mid-year consolidation ($25k-$31k)
└─ Range-bound testing

2024 (Jan-Oct): Bull Market
├─ ETF launch rally to $73k (new ATH)
└─ Current range ($60k-$70k)
```

**Why this period?**
- ✅ Tests strategies across bear, sideways, and bull markets
- ✅ Includes 2022 bear market (where most strategies fail)
- ✅ Recent enough to be relevant (modern market structure)
- ✅ Statistically significant (~1.2M data points)

---

## 🚀 Usage Examples

### Basic Backtest
```python
from libs.backtest_base import backtest_strategy
from libs.bot_base import BOT

bot = BOT()
bot.backtest_mode = True

results = backtest_strategy(
    bot_instance=bot,
    prod_id='BTC-USDC',
    start_date='2022-06-01',
    end_date='2024-10-04',
    starting_balance=10000.0
)

print(f"Total Return: {results['total_return_pct']:.2f}%")
print(f"Win Rate: {results['win_rate']:.2f}%")
print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
```

### Expected Output
```
================================================================================
BACKTEST RESULTS
================================================================================

Starting Balance: $10,000.00
Ending Balance: $12,450.50
Total Return: 24.51%

Total Trades: 156
Winning Trades: 98
Losing Trades: 58
Win Rate: 62.82%

Average Win: $87.32
Average Loss: $45.67
Profit Factor: 1.91

Max Drawdown: 12.34%
Sharpe Ratio: 1.45

Per-Strategy Breakdown:
  nwe_env: 45 trades, +8.2% return
  bb_bo:   32 trades, +5.1% return
  sha:     28 trades, +6.8% return
  ...
```

---

## 📚 Documentation

### For Backfilling Data
**[docs/BACKFILL_GUIDE.md](docs/BACKFILL_GUIDE.md)**
- Detailed backfill instructions
- Configuration options
- Troubleshooting
- Resume capability

### For System Architecture
**[docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)**
- Complete 6-phase implementation plan
- Technical architecture details
- Future roadmap (optimization, walk-forward testing)
- Data requirements

### For Quick Reference
**[docs/SUMMARY.md](docs/SUMMARY.md)**
- System overview
- How it works
- Why this approach
- Next steps

---

## 🔧 Configuration

### Backfill Speed (backfill_ohlcv_btc.py)
```python
# Line 44: Adjust API rate limiting
SLEEP_BETWEEN_REQUESTS = 0.75  # Default (safe with active bots)
# 0.75 = ~51 minutes total
# 0.5  = ~34 minutes total
# 0.1  = ~7 minutes total (risky!)
```

### Backtest Date Range (backtest_example.py)
```python
# Change these lines to test different periods:
start_date = end_date - timedelta(days=180)  # 6 months
# Or specific dates:
start_date = datetime(2022, 6, 1)
end_date = datetime(2024, 10, 4)
```

---

## ⚠️ Important Notes

### Before Running Backfill:
1. ✅ Ensure your `.env` file has correct `DB_OHLCV_*` credentials
2. ✅ Make sure OHLCV database is accessible
3. ✅ Have ~120 MB disk space available
4. ✅ Script is safe to run while trading bots are active (0.75s rate limit)

### Before Running Backtest:
1. ✅ Backfill data must be complete (run `backfill_ohlcv_btc.py` first)
2. ✅ Your bot class must support `backtest_mode` flag
3. ✅ Backtests simulate trades - no real money involved

---

## 🐛 Troubleshooting

### "No data in database"
```bash
# Run backfill first:
uv run python backtest/backfill_ohlcv_btc.py
```

### "Import errors from libs/"
```bash
# Both scripts add parent directory to path automatically
# Just run from project root:
uv run python backtest/backfill_ohlcv_btc.py
uv run python backtest/backtest_example.py
```

### "API rate limit errors"
```bash
# Increase sleep time in backfill_ohlcv_btc.py:
SLEEP_BETWEEN_REQUESTS = 1.5  # Slower, safer
```

### Backfill interrupted
```bash
# Just re-run - it will resume automatically:
uv run python backtest/backfill_ohlcv_btc.py
```

---

## 📈 Next Steps

### Phase 1: Validate System ✅
1. ✅ Backfill BTC-USDC data
2. ✅ Run test backtest (1 week)
3. ✅ Verify results make sense

### Phase 2: Full Backtest
1. Run 2.5-year backtest (June 2022 - Oct 2024)
2. Analyze strategy performance
3. Identify which strategies work best

### Phase 3: Strategy Optimization (Future)
1. Grid search optimal parameters per strategy
2. Walk-forward validation
3. Out-of-sample testing

### Phase 4: Additional Pairs (Future)
1. Backfill ETH-USDC, SOL-USDC
2. Compare strategy performance across pairs
3. Portfolio-level analysis

---

## 💡 Why This Approach is Optimal

### Problem 1: Repainting Indicators
**Issue:** Most indicators (MA, BB, etc.) change as new data comes in  
**Standard Libraries:** Only use closed candles → unrealistic results  
**This System:** Simulates minute-by-minute → accurate repainting

### Problem 2: Multi-Timeframe Logic
**Issue:** Your strategies check 5m, 15m, 1h, 4h, 1d timeframes simultaneously  
**Standard Libraries:** Struggle with multi-TF coordination  
**This System:** Builds all timeframes in sync → accurate signals

### Problem 3: Complex Buy/Sell Logic
**Issue:** Your logic includes test mode, budgets, denials, boosts, sizing  
**Standard Libraries:** Can't handle this complexity  
**This System:** Uses your EXACT code → perfect replication

---

## 🤝 Questions?

**Q: Can I run backfill while my bots are trading?**  
A: Yes! 0.75s sleep is specifically designed to not interfere.

**Q: Can I pause and resume backfilling?**  
A: Yes! Press Ctrl+C, then re-run. It detects existing data.

**Q: How do I backfill other pairs?**  
A: Copy `backfill_ohlcv_btc.py`, change `PROD_ID = 'ETH-USDC'`

**Q: Can I test just one strategy?**  
A: Yes! See `backtest_single_strategy()` in `backtest_example.py`

**Q: Why June 2022 start date?**  
A: Captures bear market tail, which is critical for realistic testing.

---

**Ready to start?**

```bash
# Step 1: Backfill data (~51 minutes)
uv run python backtest/backfill_ohlcv_btc.py

# Step 2: Run backtest
uv run python backtest/backtest_example.py
```

Then review your strategy performance and optimize! 📊
