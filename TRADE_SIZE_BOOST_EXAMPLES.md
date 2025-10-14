# Trade Size Boost System Examples

**Date:** October 10, 2025  
**Setting:** `trade_size_boost_thresholds_pct_day` in `settings/market_usdc.json`

## How It Works

**Each threshold doubles the trade size!**

Starting from a base trade size, every threshold exceeded doubles your position size for that strategy.

---

## Current Default (Fibonacci-like Progression)

```json
"trade_size_boost_thresholds_pct_day": [0.10, 0.25, 0.5, 1.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0]
```

### Example: Strategy performs at 2.5% daily gain

| Threshold | Daily Gain | Passes? | Trade Size |
|-----------|------------|---------|------------|
| Start     | -          | -       | **$10** (base) |
| 0.10%     | 2.5% > 0.10% | ✅ | **$20** (2x) |
| 0.25%     | 2.5% > 0.25% | ✅ | **$40** (4x) |
| 0.5%      | 2.5% > 0.5%  | ✅ | **$80** (8x) |
| 1.0%      | 2.5% > 1.0%  | ✅ | **$160** (16x) |
| 3.0%      | 2.5% < 3.0%  | ❌ | **$160** (stops) |

**Result:** $10 → $160 (16x boost) for 2.5% daily performer

---

## Conservative Example

```json
"trade_size_boost_thresholds_pct_day": [0.5, 2.0, 5.0, 10.0]
```

### Same Strategy: 2.5% daily gain

| Threshold | Daily Gain | Passes? | Trade Size |
|-----------|------------|---------|------------|
| Start     | -          | -       | **$10** (base) |
| 0.5%      | 2.5% > 0.5%  | ✅ | **$20** (2x) |
| 2.0%      | 2.5% > 2.0%  | ✅ | **$40** (4x) |
| 5.0%      | 2.5% < 5.0%  | ❌ | **$40** (stops) |

**Result:** $10 → $40 (4x boost) for 2.5% daily performer

**Much safer!** Requires higher performance for big position sizes.

---

## Aggressive Example

```json
"trade_size_boost_thresholds_pct_day": [0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]
```

### Same Strategy: 2.5% daily gain

| Threshold | Daily Gain | Passes? | Trade Size |
|-----------|------------|---------|------------|
| Start     | -          | -       | **$10** (base) |
| 0.05%     | 2.5% > 0.05% | ✅ | **$20** (2x) |
| 0.10%     | 2.5% > 0.10% | ✅ | **$40** (4x) |
| 0.20%     | 2.5% > 0.20% | ✅ | **$80** (8x) |
| 0.40%     | 2.5% > 0.40% | ✅ | **$160** (16x) |
| 0.80%     | 2.5% > 0.80% | ✅ | **$320** (32x) |
| 1.60%     | 2.5% > 1.60% | ✅ | **$640** (64x) |
| 3.20%     | 2.5% < 3.20% | ❌ | **$640** (stops) |

**Result:** $10 → $640 (64x boost) for 2.5% daily performer

**Very aggressive!** Smaller thresholds = faster growth = MUCH larger positions!

---

## Comparison Table

For a strategy with **2.5% daily gain** and **$10 base trade size**:

| Profile | Thresholds | Final Trade Size | Boost Factor |
|---------|-----------|------------------|--------------|
| **Very Conservative** | `[1.0, 5.0, 20.0]` | **$40** | 4x |
| **Conservative** | `[0.5, 2.0, 5.0, 10.0]` | **$40** | 4x |
| **Balanced** | `[0.10, 0.25, 0.5, 1.0, 3.0, ...]` | **$160** | 16x |
| **Aggressive** | `[0.05, 0.10, 0.20, 0.40, 0.80, ...]` | **$640** | 64x |
| **Very Aggressive** | `[0.02, 0.05, 0.10, 0.20, 0.50, ...]` | **$1,280** | 128x |

---

## Real-World Strategy Examples

Based on your actual strategies:

| Strategy | Freq | Daily Gain | Balanced Boost | Aggressive Boost | Conservative Boost |
|----------|------|------------|----------------|------------------|-------------------|
| **BTC drop** | 4h | **3.93%** | $320 (32x) | $1,280 (128x) | $80 (8x) |
| **BTC drop** | 1h | **3.24%** | $320 (32x) | $1,280 (128x) | $80 (8x) |
| **BTC imp_macd** | 1h | **4.19%** | $640 (64x) | $2,560 (256x) | $80 (8x) |
| **ETH nwe_3row** | 4h | **0.0247%** | $20 (2x) | $20 (2x) | $10 (1x) |
| **SOL nwe_env** | 1d | **0.3527%** | $80 (8x) | $160 (16x) | $20 (2x) |

**Note:** These are multipliers from your base trade size setting!

---

## Risk Management Considerations

### 🎯 Conservative Approach (Recommended for Beginning)
- **Fewer thresholds** = Slower growth
- **Higher thresholds** = Only proven winners get big positions
- **Example:** `[0.5, 2.0, 5.0, 10.0]`

### ⚖️ Balanced Approach (Current Default)
- **Fibonacci-like** = Natural growth pattern
- **Moderate thresholds** = Rewards good performers reasonably
- **Example:** `[0.10, 0.25, 0.5, 1.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0]`

### 🚀 Aggressive Approach (Higher Risk/Reward)
- **Many thresholds** = Fast growth
- **Low thresholds** = Even modest performers get boosted
- **Example:** `[0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]`

### ⚠️ Important Caveats

1. **Past performance ≠ Future results**
   - A strategy with 5% daily gain can suddenly stop working
   - Large positions = Large losses if strategy breaks

2. **Trade Size Max Still Applies**
   - Your `trade_size_max` setting (e.g., $400) caps all boosts
   - Even 1000x boost can't exceed your max

3. **Budget Constraints**
   - Total spendable amount limits all trades
   - High boosts may exhaust budget quickly

4. **Market Conditions Change**
   - Bull market strategies may fail in bear markets
   - Adjust thresholds based on market regime

---

## Quick Reference Card

**Formula:** `Final Size = Base Size × 2^(number of thresholds passed)`

| Thresholds Passed | Multiplier | Example ($10 base) |
|-------------------|------------|-------------------|
| 0 | 1x | $10 |
| 1 | 2x | $20 |
| 2 | 4x | $40 |
| 3 | 8x | $80 |
| 4 | 16x | $160 |
| 5 | 32x | $320 |
| 6 | 64x | $640 |
| 7 | 128x | $1,280 |
| 8 | 256x | $2,560 |
| 9 | 512x | $5,120 |
| 10 | 1024x | $10,240 |

**Remember:** More thresholds = Exponential growth!

---

## Recommended Starting Point

If you're unsure, start **conservative** and gradually increase:

**Week 1:**
```json
"trade_size_boost_thresholds_pct_day": [1.0, 5.0]
```

**Week 2-4:** (if strategies stable)
```json
"trade_size_boost_thresholds_pct_day": [0.5, 2.0, 5.0]
```

**Month 2+:** (if confident)
```json
"trade_size_boost_thresholds_pct_day": [0.10, 0.25, 0.5, 1.0, 3.0, 5.0]
```

Monitor your actual position sizes and adjust accordingly!

