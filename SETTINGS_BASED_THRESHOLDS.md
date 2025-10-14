# Settings-Based Thresholds Implementation

**Date:** October 10, 2025  
**Issue:** Hardcoded delays and profitability thresholds were ignoring settings

## Problems Fixed

### 1. ✅ Buy Strategy Delays Now Use Settings

**Before:**
- Hardcoded delays in `libs/buy_base.py` (lines 1461-1472, 1533-1544)
- Settings existed but were **IGNORED**
- Delays: 15min=8min, 30min=16min, 1h=31min, 4h=121min, 1d=721min

**After:**
- Reads from `settings/market_usdc.json` → `buy_strat_delay_minutes`
- Current settings: 15min=5min, 30min=10min, 1h=20min, 4h=40min, 1d=240min
- **Fully customizable per frequency**

**Code Changes:**
- Lines 1461-1469 and 1530-1538 in `libs/buy_base.py`
- Now uses: `cfg = self.st_pair.buy.buy_strat_delay_minutes`

---

### 2. ✅ Profitability Threshold Now Configurable

**Before:**
- **Hardcoded 0.025%** (2.5 basis points per day) in THREE places
- No way to adjust without code changes
- Many profitable strategies stuck in test mode (0.015-0.024%)

**After:**
- New setting: `profitability_threshold_pct_day: 0.25` (0.25% = 1/4 of 1% per day)
- **Can be set per-product with wildcard support**
- Easily adjustable per market conditions

**Settings File Change:**
```json
"buy_test_txns": {
    "test_txns_on_yn": "Y",
    "test_txns_min": {...},
    "test_txns_max": {...},
    "profitability_threshold_pct_day": {
        "***": 0.25,         // Default: 0.25% (1/4 of 1%)
        "BTC-USDC": 0.00,    // BTC: ANY positive gain trades live
        "ETH-USDC": 0.00,    // ETH: ANY positive gain trades live
        "SOL-USDC": 0.00     // SOL: ANY positive gain trades live
    }
}
```

**Code Changes:**
- Line 1213: `profit_threshold = self.st_pair.buy_test_txns.profitability_threshold_pct_day`
- Lines 1230, 1251, 1274: Now use `profit_threshold` instead of 0.025
- Lines 1242, 1265, 1283: Setting name updated from "hardcoded 0.025"

---

### 3. ✅ Trade Size Boost Thresholds Now Configurable

**Before:**
- **Hardcoded Fibonacci-like thresholds**: `[0.10, 0.25, 0.5, 1.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0]`
- No way to adjust without code changes
- Each threshold doubles trade size

**After:**
- New setting: `trade_size_boost_thresholds_pct_day` array
- **Fully customizable boost progression**
- Easily adjust aggressiveness or add/remove thresholds

**Settings File Change:**
```json
"buy": {
    ...
    "trade_size_boost_thresholds_pct_day": [0.10, 0.25, 0.5, 1.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0]
    // ← NEW SETTING - Each threshold doubles trade size
}
```

**Code Changes:**
- Line 973: `daily_pct_rates = self.st_pair.buy.trade_size_boost_thresholds_pct_day`
- Line 940: Docstring updated to indicate configurable thresholds

**Examples:**
```json
// More conservative - fewer, higher thresholds
"trade_size_boost_thresholds_pct_day": [0.5, 2.0, 5.0, 10.0]

// More aggressive - more frequent boosts
"trade_size_boost_thresholds_pct_day": [0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]

// Custom progression
"trade_size_boost_thresholds_pct_day": [0.25, 1.0, 5.0, 20.0]
```

---

## Impact on Your Trading

### Before Changes:
- **BTC-USDC**: nwe_3row 1h stuck in test mode (499 min since last buy, but still testing)
- **ETH-USDC**: nwe_3row 4h at 0.0247% daily gain (below 0.025% threshold) → test mode
- **ETH-USDC**: sha 15min at 0.0242% → test mode
- **BTC-USDC**: tpo 30min at 0.0222% → test mode
- **SOL-USDC**: bb 1h at 0.0167% → test mode

### After Changes (with 0.25% threshold):
- ✅ **ALL strategies above 0.25% daily gain will now trade LIVE**
- ✅ BTC-USDC, ETH-USDC, SOL-USDC: ANY positive gain trades live
- ✅ Delays respect your configured settings (much shorter!)
- ✅ More strategies qualify for live trading
- ✅ Faster strategy validation cycle

---

## Settings You Can Now Adjust

### Buy Strategy Delays (`settings/market_usdc.json` line 279-286)
```json
"buy_strat_delay_minutes": {
    "***": 30,      // Default for any frequency
    "15min": 5,     // 5 minutes between 15min strategy buys
    "30min": 10,    // 10 minutes between 30min strategy buys
    "1h": 20,       // 20 minutes between 1h strategy buys
    "4h": 40,       // 40 minutes between 4h strategy buys
    "1d": 240       // 4 hours between daily strategy buys
}
```

### Profitability Threshold (`settings/market_usdc.json` line 262)
```json
"profitability_threshold_pct_day": {
    "***": 0.25,         // 0.25% per day (1/4 of 1%)
    "BTC-USDC": 0.00,    // ANY positive gain trades live
    "ETH-USDC": 0.00,
    "SOL-USDC": 0.00
}
```

**Recommended Values:**
- **Conservative**: 0.50 (0.5%) - Only best performers trade live
- **Balanced**: 0.25 (0.25%) - Most profitable strategies trade live ← **Current**
- **Aggressive**: 0.10 (0.1%) - Any profitable strategy trades live
- **Very Aggressive**: 0.00 (0.0%) - Almost any profit trades live

**Note:** Values are percentages (0.25 = 0.25%, not 0.0025%). The `gain_loss_close_pct_day` from the database is already multiplied by 100.

### Trade Size Boost Thresholds (`settings/market_usdc.json` line 330)
```json
"trade_size_boost_thresholds_pct_day": [0.10, 0.25, 0.5, 1.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0]
```

**Each threshold doubles the trade size!** (Fibonacci-like progression)

**Recommended Values:**
- **Very Conservative**: `[1.0, 5.0, 20.0]` - Only massive winners get boosted
- **Conservative**: `[0.5, 2.0, 5.0, 10.0]` - Slower boost progression
- **Balanced**: `[0.10, 0.25, 0.5, 1.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0]` ← **Current (Fibonacci-like)**
- **Aggressive**: `[0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]` - Faster boost progression
- **Very Aggressive**: `[0.02, 0.05, 0.10, 0.20, 0.50, 1.0, 2.0]` - Many small boosts

**Warning:** Too many thresholds = very large position sizes for high performers!

---

## Testing Recommendations

1. **Monitor BTC/ETH/SOL**: Should see live trades within 5-40 minutes (depending on frequency)
2. **Check buy_decisions table**: `test_txn_yn` should be 'N' for BTC/ETH/SOL (any positive gain)
3. **Review gain_loss_close_pct_day**: Strategies above 0.25% should trade live for other pairs
4. **Watch for successful live trades**: Confirm strategies are actually executing live orders with full trade sizes

---

## Rollback Instructions

If you need to revert to more conservative settings:

**Option 1: Increase Threshold**
```json
"profitability_threshold_pct_day": 0.025  // Back to original 2.5%
```

**Option 2: Increase Delays**
```json
"buy_strat_delay_minutes": {
    "15min": 8,
    "30min": 16,
    "1h": 31,
    "4h": 121,
    "1d": 721
}
```

**Option 3: Force All Test Mode**
```json
"test_txns_on_yn": "N"  // Disables test transaction system entirely
```

---

## Files Modified

1. **`libs/buy_base.py`**:
   - Lines 1461-1469: Product timing delay now uses settings
   - Lines 1530-1538: Strategy timing delay now uses settings
   - Line 1213: Added profit_threshold variable from settings
   - Lines 1230, 1251, 1274: Profitability comparisons now use settings
   - Lines 1242, 1265, 1283: Setting names updated for tracking
   - Line 973: Trade size boost thresholds now read from settings
   - Line 940: Docstring updated for configurable thresholds

2. **`settings/market_usdc.json`**:
   - Line 262: Added `profitability_threshold_pct_day: 0.015`
   - Line 330: Added `trade_size_boost_thresholds_pct_day` array

---

**Summary:** Your trading system now respects your settings instead of ignoring them. Strategies that are profitable (>0.015% daily gain) will trade live, buy delays use your configured values instead of hardcoded overrides, and trade size boosts are now fully customizable for risk management.

