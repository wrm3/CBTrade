# Forensic Buy Decision Tracking System

**Date:** October 10, 2025  
**Purpose:** Link buy_signals and buy_decisions for comprehensive forensic analysis of trading decisions

## 🎯 System Overview

### **What This Enables:**
1. **Forensic Analysis**: Trace why trades were denied, delayed, or executed
2. **Live vs Test Investigation**: Understand strategy graduation patterns
3. **Strategy Optimization**: Identify bottlenecks in buy logic
4. **Historical Linkage**: Connect lightweight signals to detailed decision audits

### **Architecture:**
```
buy_decision_log() called:
    ↓
1. Insert to buy_signals (compact event) → Returns signal_id
    ↓
2. Store signal_id in self.buy.buy_signal_id
    ↓
3. Insert to buy_decisions (detailed audit) WITH signal_id linkage
```

---

## 📋 Database Schema Changes

### **buy_signals Table (Enhanced)**

**Added Indexes:**
```sql
INDEX idx_prod_strat (prod_id, buy_strat_name, buy_strat_freq)  -- Fast lookups by strategy
INDEX idx_event_dttm (event_dttm)                                -- Time-based queries
INDEX idx_dlm_cleanup (dlm)                                      -- Cleanup performance
```

**Existing Structure:**
- `signal_id` INT AUTO_INCREMENT PRIMARY KEY
- `prod_id`, `buy_strat_type`, `buy_strat_name`, `buy_strat_freq`
- `event_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `test_txn_yn` CHAR(1)
- `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

---

### **buy_decisions Table (Enhanced)**

**Added Column:**
```sql
`signal_id` INT NULL COMMENT 'Links to buy_signals.signal_id (logical FK, not constraint)'
```

**Added Indexes:**
```sql
INDEX idx_signal_id (signal_id)                                  -- Forensic linkage queries
INDEX idx_prod_strat (prod_id, buy_strat_name, buy_strat_freq)  -- Strategy analysis
INDEX idx_test_deny (test_txn_yn, buy_deny_yn)                  -- Decision outcome queries
INDEX idx_dlm_cleanup (dlm)                                      -- Cleanup performance
```

**Why NO Foreign Key Constraint?**
- User requested: "FK for linking but don't complicate clearing tables"
- Allows TRUNCATE operations without cascade complexity
- Maintains logical relationship for queries without enforcement overhead
- NULL signal_id allowed for resilience (though shouldn't occur with new code)

---

## 🔧 Code Changes

### **1. libs/db_mysql/cbtrade/tbl_buy_signals.py**

**Enhanced db_buy_signals_ins():**
```python
def db_buy_signals_ins(self, in_data):
    """
    Returns:
        int: The signal_id (AUTO_INCREMENT primary key)
        
    Raises:
        Exception: If insert fails - NO silent failures
    """
    # ... insert logic ...
    
    # 🔴 NO TRY/CATCH - Let errors propagate
    if hasattr(self, 'ins_one'):
        signal_id = self.ins_one(sql, vals, exit_on_error=True)
    else:
        self.execute(sql, vals)
        signal_id = self.lastrowid
    
    if signal_id is None:
        raise Exception("🔴 CRITICAL: buy_signals insert failed")
    
    return signal_id
```

**Added db_buy_signals_cleanup_old():**
```python
def db_buy_signals_cleanup_old(self, days_to_keep=90):
    """Delete rows older than 90 days for table size management"""
    sql = f'''
        DELETE FROM buy_signals 
        WHERE dlm < DATE_SUB(NOW(), INTERVAL {days_to_keep} DAY)
    '''
    # Returns: Number of rows deleted
```

---

### **2. libs/db_mysql/cbtrade/tbl_buy_decisions.py**

**Enhanced db_buy_decisions_ins():**
```python
def db_buy_decisions_ins(self, in_data):
    """
    Now includes signal_id for forensic linkage.
    
    Raises:
        Exception: If insert fails - NO silent failures
    """
    cols = [
        'signal_id',  # ← NEW: First column for forensic linkage
        'prod_id','symb','buy_yn','test_txn_yn','buy_deny_yn',
        # ... rest of columns ...
    ]
    
    # 🔴 NO TRY/CATCH - Let errors propagate
    if hasattr(self, 'ins_one'):
        self.ins_one(sql, vals, exit_on_error=True)
    else:
        self.execute(sql, vals)
```

**Added db_buy_decisions_cleanup_old():**
```python
def db_buy_decisions_cleanup_old(self, days_to_keep=90):
    """Delete rows older than 90 days for table size management"""
    sql = f'''
        DELETE FROM buy_decisions 
        WHERE dlm < DATE_SUB(NOW(), INTERVAL {days_to_keep} DAY)
    '''
    # Returns: Number of rows deleted
```

---

### **3. libs/db_mysql/cbtrade/db_main.py**

**Registered Cleanup Functions:**
```python
# tbl_buy_decisions
from libs.db_mysql.cbtrade.tbl_buy_decisions import (
    db_buy_decisions_exists
    , db_buy_decisions_ins
    , db_buy_decisions_cleanup_old  # ← NEW
)
db_buy_decisions_cleanup_old = db_buy_decisions_cleanup_old

# tbl_buy_signals
from libs.db_mysql.cbtrade.tbl_buy_signals import (
    db_buy_signals_exists
    , db_buy_signals_ins
    , db_buy_signals_cleanup_old  # ← NEW
)
db_buy_signals_cleanup_old = db_buy_signals_cleanup_old
```

---

### **4. libs/buy_base.py**

**Enhanced buy_decision_log():**
```python
def buy_decision_log(self) -> None:
    """
    Centralized function to log buy decisions with forensic linkage.
    
    Raises:
        Exception: If either insert fails - NO silent failures
    """
    # Ensure event timestamp exists
    if not getattr(self.buy, 'event_dttm', None):
        self.buy.event_dttm = dttm_get()
    
    # Insert signal - RETURNS signal_id for forensic linkage
    # 🔴 NO TRY/CATCH - Let errors propagate
    signal_id = self.cbtrade_db.db_buy_signals_ins(self.buy)
    
    # Store signal_id in buy object for decisions table
    self.buy.buy_signal_id = signal_id  # ← NEW: Stored for db_buy_decisions_ins

    # Insert decision with signal_id linkage
    # 🔴 NO TRY/CATCH - Let errors propagate
    self.cbtrade_db.db_buy_decisions_ins(self.buy)
```

**Key Changes:**
- Removed all `try/except/pass` blocks - errors now propagate
- Captures `signal_id` return value
- Stores in `self.buy.buy_signal_id` for decisions insert
- Full script stop on any insert failure

---

### **5. libs/bot_base.py**

**Bot Startup Cleanup:**
```python
def __init__(self, mode='full'):
    # ... initialization ...
    self.cbtrade_db = CBTRADE_DB()
    
    # 🧹 FORENSIC TABLE CLEANUP: Delete rows older than 90 days
    # Prevents tables from growing unbounded
    try:
        signals_deleted = self.cbtrade_db.db_buy_signals_cleanup_old(days_to_keep=90)
        decisions_deleted = self.cbtrade_db.db_buy_decisions_cleanup_old(days_to_keep=90)
        if signals_deleted > 0 or decisions_deleted > 0:
            print(f"🧹 Forensic Cleanup: Deleted {signals_deleted} old signals, {decisions_deleted} old decisions")
    except Exception as e:
        print(f"⚠️  Forensic cleanup warning: {e}")
        # Don't fail bot startup if cleanup fails
    
    # ... rest of initialization ...
```

**Cleanup Behavior:**
- Runs EVERY bot startup
- Deletes rows with `dlm` > 90 days old
- Maintains 3 months of forensic history
- Non-blocking (warns but doesn't stop bot if cleanup fails)

---

## 🔍 Forensic Query Examples

### **1. Find All Decisions for a Specific Signal**
```sql
SELECT 
    s.signal_id,
    s.prod_id,
    s.buy_strat_name,
    s.buy_strat_freq,
    s.event_dttm,
    d.buy_yn,
    d.test_txn_yn,
    d.buy_deny_yn,
    d.test_fnc_name,
    d.message
FROM buy_signals s
LEFT JOIN buy_decisions d ON s.signal_id = d.signal_id
WHERE s.signal_id = 12345;
```

### **2. Analyze Why Strategy Stuck in Test Mode**
```sql
SELECT 
    s.prod_id,
    s.buy_strat_name,
    s.buy_strat_freq,
    d.test_fnc_name,
    d.message,
    COUNT(*) as denial_count,
    MIN(s.event_dttm) as first_attempt,
    MAX(s.event_dttm) as last_attempt
FROM buy_signals s
JOIN buy_decisions d ON s.signal_id = d.signal_id
WHERE d.test_txn_yn = 'Y'
  AND d.buy_deny_yn = 'N'  -- Approved as test
  AND s.prod_id = 'BTC-USDC'
  AND s.buy_strat_name = 'nwe_3row'
  AND s.event_dttm > DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY s.prod_id, s.buy_strat_name, s.buy_strat_freq, d.test_fnc_name, d.message
ORDER BY denial_count DESC;
```

### **3. Compare Live vs Test Decisions**
```sql
SELECT 
    s.prod_id,
    s.buy_strat_name,
    SUM(CASE WHEN d.test_txn_yn = 'N' AND d.buy_deny_yn = 'N' THEN 1 ELSE 0 END) as live_approved,
    SUM(CASE WHEN d.test_txn_yn = 'Y' AND d.buy_deny_yn = 'N' THEN 1 ELSE 0 END) as test_approved,
    SUM(CASE WHEN d.buy_deny_yn = 'Y' THEN 1 ELSE 0 END) as denied,
    COUNT(*) as total_signals
FROM buy_signals s
JOIN buy_decisions d ON s.signal_id = d.signal_id
WHERE s.event_dttm > DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY s.prod_id, s.buy_strat_name
ORDER BY live_approved DESC;
```

### **4. Find Most Common Denial Reasons**
```sql
SELECT 
    d.test_fnc_name,
    LEFT(d.message, 100) as message_preview,
    COUNT(*) as occurrence_count,
    COUNT(DISTINCT s.prod_id) as products_affected
FROM buy_signals s
JOIN buy_decisions d ON s.signal_id = d.signal_id
WHERE d.buy_deny_yn = 'Y'
  AND s.event_dttm > DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY d.test_fnc_name, LEFT(d.message, 100)
ORDER BY occurrence_count DESC
LIMIT 10;
```

### **5. Strategy Graduation Timeline**
```sql
SELECT 
    s.prod_id,
    s.buy_strat_name,
    s.buy_strat_freq,
    MIN(CASE WHEN d.test_txn_yn = 'Y' THEN s.event_dttm END) as first_test,
    MAX(CASE WHEN d.test_txn_yn = 'Y' THEN s.event_dttm END) as last_test,
    MIN(CASE WHEN d.test_txn_yn = 'N' AND d.buy_deny_yn = 'N' THEN s.event_dttm END) as first_live,
    COUNT(CASE WHEN d.test_txn_yn = 'Y' THEN 1 END) as test_count,
    COUNT(CASE WHEN d.test_txn_yn = 'N' AND d.buy_deny_yn = 'N' THEN 1 END) as live_count
FROM buy_signals s
JOIN buy_decisions d ON s.signal_id = d.signal_id
GROUP BY s.prod_id, s.buy_strat_name, s.buy_strat_freq
HAVING first_live IS NOT NULL
ORDER BY first_live DESC;
```

---

## 🚨 Critical Behavior Changes

### **Error Handling: NO MORE SILENT FAILURES**

**Before:**
```python
try:
    self.cbtrade_db.db_buy_signals_ins(self.buy)
except Exception:
    pass  # Silent failure - continues execution
```

**After:**
```python
# 🔴 NO TRY/CATCH - Errors propagate and STOP the bot
signal_id = self.cbtrade_db.db_buy_signals_ins(self.buy)
```

**Impact:**
- ✅ Forensic integrity: No missing signal/decision linkages
- ✅ Immediate error detection: Database issues caught immediately
- ⚠️  Bot will stop on insert failures (by design - user requested)
- ⚠️  Ensure database connectivity is stable before restart

---

## 📊 Table Size Management

### **Automatic Cleanup:**
- **When:** Every bot startup
- **What:** Deletes rows where `dlm > 90 days` old
- **Retention:** 3 months of forensic history
- **Impact:** Prevents unbounded table growth

### **Manual Cleanup (if needed):**
```python
# Via Python
bot.cbtrade_db.db_buy_signals_cleanup_old(days_to_keep=60)  # Keep 60 days
bot.cbtrade_db.db_buy_decisions_cleanup_old(days_to_keep=60)

# Via SQL
DELETE FROM buy_signals WHERE dlm < DATE_SUB(NOW(), INTERVAL 60 DAY);
DELETE FROM buy_decisions WHERE dlm < DATE_SUB(NOW(), INTERVAL 60 DAY);
```

### **Monitoring Table Sizes:**
```sql
-- Check current row counts
SELECT 
    'buy_signals' as table_name,
    COUNT(*) as total_rows,
    COUNT(CASE WHEN dlm > DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as last_30_days,
    COUNT(CASE WHEN dlm > DATE_SUB(NOW(), INTERVAL 90 DAY) THEN 1 END) as last_90_days
FROM buy_signals
UNION ALL
SELECT 
    'buy_decisions' as table_name,
    COUNT(*) as total_rows,
    COUNT(CASE WHEN dlm > DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as last_30_days,
    COUNT(CASE WHEN dlm > DATE_SUB(NOW(), INTERVAL 90 DAY) THEN 1 END) as last_90_days
FROM buy_decisions;
```

---

## 🔄 Migration Instructions

### **Step 1: Apply Schema Changes**

**Option A: Let Bot Create Tables (Recommended)**
```bash
# Bot will automatically create tables with new schema on startup
# Existing tables will NOT be modified (CREATE TABLE IF NOT EXISTS)
uv run python run_bot.py
```

**Option B: Manual Schema Update (For Existing Tables)**
```sql
-- Add signal_id column to buy_decisions
ALTER TABLE buy_decisions 
  ADD COLUMN signal_id INT NULL COMMENT 'Links to buy_signals.signal_id (logical FK, not constraint)' 
  AFTER buy_dec_id;

-- Add indexes to buy_signals
CREATE INDEX idx_prod_strat ON buy_signals (prod_id, buy_strat_name, buy_strat_freq);
CREATE INDEX idx_event_dttm ON buy_signals (event_dttm);
CREATE INDEX idx_dlm_cleanup ON buy_signals (dlm);

-- Add indexes to buy_decisions
CREATE INDEX idx_signal_id ON buy_decisions (signal_id);
CREATE INDEX idx_prod_strat ON buy_decisions (prod_id, buy_strat_name, buy_strat_freq);
CREATE INDEX idx_test_deny ON buy_decisions (test_txn_yn, buy_deny_yn);
CREATE INDEX idx_dlm_cleanup ON buy_decisions (dlm);
```

---

### **Step 2: Truncate Existing Data (User Requested)**

**⚠️  WARNING: This deletes ALL historical forensic data!**

```sql
-- Truncate both tables to start fresh with new linkage system
TRUNCATE TABLE buy_decisions;
TRUNCATE TABLE buy_signals;

-- Verify tables are empty
SELECT COUNT(*) FROM buy_signals;    -- Should be 0
SELECT COUNT(*) FROM buy_decisions;  -- Should be 0
```

**Why Truncate?**
- User requested: "We can truncate the tables after we code this new functionality"
- Existing rows have `signal_id = NULL` (no linkage)
- Fresh start ensures all new rows have proper forensic linkage
- Indexes will be more efficient without legacy NULL data

---

### **Step 3: Restart Bot and Verify**

```bash
# Start bot - will run cleanup on startup (should be instant for empty tables)
uv run python run_bot.py
```

**Expected Output:**
```
🧹 Forensic Cleanup: Deleted 0 old buy_signals, 0 old buy_decisions (>90 days)
```

**Verify Forensic Linkage:**
```sql
-- After bot runs for a few minutes, verify signal_id linkage:
SELECT 
    COUNT(*) as total_decisions,
    COUNT(signal_id) as decisions_with_signal_id,
    COUNT(*) - COUNT(signal_id) as null_signal_ids
FROM buy_decisions;

-- Expected: null_signal_ids = 0 (all decisions have signal_id)
```

---

## 🎯 Success Metrics

### **Forensic System Health Check:**
```sql
-- 1. Check that ALL decisions have signal_id linkage
SELECT 
    CASE 
        WHEN COUNT(*) = COUNT(signal_id) THEN '✅ PASS: All decisions linked'
        ELSE CONCAT('❌ FAIL: ', COUNT(*) - COUNT(signal_id), ' decisions missing signal_id')
    END as linkage_status
FROM buy_decisions;

-- 2. Check that all signal_ids are valid
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '✅ PASS: All signal_ids valid'
        ELSE CONCAT('❌ FAIL: ', COUNT(*), ' orphaned signal_ids')
    END as validity_status
FROM buy_decisions d
LEFT JOIN buy_signals s ON d.signal_id = s.signal_id
WHERE d.signal_id IS NOT NULL 
  AND s.signal_id IS NULL;

-- 3. Check retention policy working (after 91+ days)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '✅ PASS: No data older than 90 days'
        ELSE CONCAT('⚠️  WARNING: ', COUNT(*), ' rows older than 90 days')
    END as retention_status
FROM (
    SELECT dlm FROM buy_signals WHERE dlm < DATE_SUB(NOW(), INTERVAL 90 DAY)
    UNION ALL
    SELECT dlm FROM buy_decisions WHERE dlm < DATE_SUB(NOW(), INTERVAL 90 DAY)
) old_data;
```

---

## 📚 Files Modified

1. **libs/db_mysql/cbtrade/tbl_buy_signals.py**
   - Added indexes to schema
   - Enhanced `db_buy_signals_ins()` to return signal_id and raise errors
   - Added `db_buy_signals_cleanup_old()` for 90-day retention

2. **libs/db_mysql/cbtrade/tbl_buy_decisions.py**
   - Added `signal_id` column with indexes to schema
   - Enhanced `db_buy_decisions_ins()` to include signal_id and raise errors
   - Added `db_buy_decisions_cleanup_old()` for 90-day retention

3. **libs/db_mysql/cbtrade/db_main.py**
   - Registered cleanup functions for both tables

4. **libs/buy_base.py**
   - Enhanced `buy_decision_log()` to capture and store signal_id
   - Removed all try/except/pass error suppression

5. **libs/bot_base.py**
   - Added startup cleanup calls in `__init__()`
   - Runs 90-day retention on every bot start

---

## 🚀 Benefits Delivered

### **Forensic Capabilities:**
- ✅ Link every decision to its originating signal
- ✅ Trace denial reasons through complete audit trail
- ✅ Analyze strategy graduation patterns
- ✅ Identify bottlenecks in buy logic
- ✅ Compare live vs test decision patterns

### **System Health:**
- ✅ No silent failures - immediate error detection
- ✅ Automatic table size management (90-day retention)
- ✅ Efficient queries via comprehensive indexing
- ✅ Clean forensic data for analysis

### **Maintenance:**
- ✅ Zero-touch cleanup (runs on startup)
- ✅ No foreign key cascade complications
- ✅ Easy manual truncation for testing
- ✅ Clear error messages for troubleshooting

---

**Summary:** Your forensic system is now production-ready with complete signal-to-decision linkage, automatic cleanup, and zero tolerance for silent failures. After truncating the tables and restarting the bot, every buy decision will have full forensic traceability for the next 90 days of operation.

