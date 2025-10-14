-- ============================================================================
-- FORENSIC SYSTEM SCHEMA MIGRATION
-- ============================================================================
-- Purpose: Add signal_id linkage and indexes to existing buy_signals/buy_decisions tables
-- Date: 2025-10-11
-- ============================================================================

USE cbtrade;

-- ============================================================================
-- STEP 1: Add signal_id column to buy_decisions
-- ============================================================================

-- Check if column already exists (safe to run multiple times)
SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'cbtrade' 
  AND TABLE_NAME = 'buy_decisions' 
  AND COLUMN_NAME = 'signal_id';

-- Add signal_id column if it doesn't exist
ALTER TABLE buy_decisions 
ADD COLUMN IF NOT EXISTS signal_id INT NULL 
  COMMENT 'Links to buy_signals.signal_id (logical FK, not constraint)' 
  AFTER buy_dec_id;

-- ============================================================================
-- STEP 2: Add indexes to buy_signals (if not already present)
-- ============================================================================

-- These are safe to run multiple times - will error if index exists but won't break anything
-- You can ignore "Duplicate key name" errors

-- Index for strategy lookups
CREATE INDEX IF NOT EXISTS idx_prod_strat 
  ON buy_signals (prod_id, buy_strat_name, buy_strat_freq);

-- Index for time-based queries
CREATE INDEX IF NOT EXISTS idx_event_dttm 
  ON buy_signals (event_dttm);

-- Index for cleanup performance
CREATE INDEX IF NOT EXISTS idx_dlm_cleanup 
  ON buy_signals (dlm);

-- ============================================================================
-- STEP 3: Add indexes to buy_decisions (if not already present)
-- ============================================================================

-- Index for forensic linkage queries
CREATE INDEX IF NOT EXISTS idx_signal_id 
  ON buy_decisions (signal_id);

-- Index for strategy analysis
CREATE INDEX IF NOT EXISTS idx_prod_strat 
  ON buy_decisions (prod_id, buy_strat_name, buy_strat_freq);

-- Index for decision outcome queries
CREATE INDEX IF NOT EXISTS idx_test_deny 
  ON buy_decisions (test_txn_yn, buy_deny_yn);

-- Index for cleanup performance
CREATE INDEX IF NOT EXISTS idx_dlm_cleanup 
  ON buy_decisions (dlm);

-- ============================================================================
-- STEP 4: Verify schema changes
-- ============================================================================

-- Check buy_decisions has signal_id column
SELECT 
    'buy_decisions signal_id column' as check_name,
    CASE 
        WHEN COUNT(*) = 1 THEN '✅ PASS'
        ELSE '❌ FAIL - Run ALTER TABLE again'
    END as status
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'cbtrade' 
  AND TABLE_NAME = 'buy_decisions' 
  AND COLUMN_NAME = 'signal_id';

-- Check buy_signals indexes
SELECT 
    'buy_signals indexes' as check_name,
    CASE 
        WHEN COUNT(DISTINCT INDEX_NAME) >= 4 THEN CONCAT('✅ PASS (', COUNT(DISTINCT INDEX_NAME), ' indexes)')
        ELSE CONCAT('⚠️  WARNING: Only ', COUNT(DISTINCT INDEX_NAME), ' indexes found')
    END as status
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'cbtrade' 
  AND TABLE_NAME = 'buy_signals'
  AND INDEX_NAME IN ('PRIMARY', 'idx_prod_strat', 'idx_event_dttm', 'idx_dlm_cleanup');

-- Check buy_decisions indexes
SELECT 
    'buy_decisions indexes' as check_name,
    CASE 
        WHEN COUNT(DISTINCT INDEX_NAME) >= 5 THEN CONCAT('✅ PASS (', COUNT(DISTINCT INDEX_NAME), ' indexes)')
        ELSE CONCAT('⚠️  WARNING: Only ', COUNT(DISTINCT INDEX_NAME), ' indexes found')
    END as status
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'cbtrade' 
  AND TABLE_NAME = 'buy_decisions'
  AND INDEX_NAME IN ('PRIMARY', 'idx_signal_id', 'idx_prod_strat', 'idx_test_deny', 'idx_dlm_cleanup');

-- ============================================================================
-- STEP 5 (OPTIONAL): Truncate tables to start fresh
-- ============================================================================

-- ⚠️  WARNING: This deletes ALL forensic history!
-- Uncomment these lines if you want to start with clean tables:

-- TRUNCATE TABLE buy_decisions;
-- TRUNCATE TABLE buy_signals;

-- ============================================================================
-- STEP 6: Verify table structure
-- ============================================================================

-- Show buy_decisions columns (should include signal_id)
DESCRIBE buy_decisions;

-- Show buy_signals columns
DESCRIBE buy_signals;

-- Show buy_decisions indexes
SHOW INDEX FROM buy_decisions;

-- Show buy_signals indexes
SHOW INDEX FROM buy_signals;

-- ============================================================================
-- COMPLETE!
-- ============================================================================
-- Next steps:
-- 1. Restart bot (will create forensic linkages going forward)
-- 2. Monitor for any insert errors
-- 3. Use forensic queries from FORENSIC_SYSTEM_IMPLEMENTATION.md
-- ============================================================================

