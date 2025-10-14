#<=====>#
# Description
#<=====>#


#<=====>#
# Known To Do List
#<=====>#

 
#<=====>#
# Imports - Public
#<=====>#
from fstrent_colors import G

#<=====>#
# Imports - Project
#<=====>#
from libs.common import narc, AttrDict, beep
from libs.db_mysql.cbtrade.db_common import to_scalar_dict


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_buy_decisions'
log_name      = 'cbtrade.tbl_buy_decisions'


# <=====>#
# Assignments Pre
# <=====>#
debug_tf = False


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

@narc(1)
def db_buy_decisions_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_buy_decisions_exists()')
    """Check if the buy_decisions table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `buy_decisions` (
            `buy_dec_id` INT AUTO_INCREMENT PRIMARY KEY,
            `signal_id` INT NULL COMMENT 'Links to buy_signals.signal_id (logical FK, not constraint)',
            `actv_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `prod_id` VARCHAR(64),
            `symb` VARCHAR(64),
            `buy_yn` VARCHAR(1),
            `test_txn_yn` VARCHAR(1),
            `buy_deny_yn` VARCHAR(1),
            `buy_strat_type` VARCHAR(64),
            `buy_strat_name` VARCHAR(64),
            `buy_strat_freq` VARCHAR(64),
            `setting_name` VARCHAR(64),
            `setting_value` VARCHAR(64),
            `buy_stat_name` VARCHAR(64),
            `buy_stat_value` VARCHAR(64),
            `setting_name2` VARCHAR(64),
            `setting_value2` VARCHAR(64),
            `buy_stat_name2` VARCHAR(64),
            `buy_stat_value2` VARCHAR(64),
            `setting_name3` VARCHAR(64),
            `setting_value3` VARCHAR(64),
            `buy_stat_name3` VARCHAR(64),
            `buy_stat_value3` VARCHAR(64),
            `test_fnc_name` VARCHAR(64),
            `message` TEXT,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_signal_id (signal_id),
            INDEX idx_prod_strat (prod_id, buy_strat_name, buy_strat_freq),
            INDEX idx_test_deny (test_txn_yn, buy_deny_yn),
            INDEX idx_dlm_cleanup (dlm)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

@narc(1)
def db_buy_decisions_ins(self, in_data):
    """
    Insert a buy decision audit row into MySQL cbtrade.buy_decisions.
    Expects fields matching table columns; missing optional fields are inserted as NULL.
    
    Now includes signal_id (from buy_signals.signal_id) for forensic linkage.
    
    Raises:
        Exception: If insert fails - NO silent failures for forensic integrity
    """
    cols = [
        'signal_id','prod_id','symb','buy_yn','test_txn_yn','buy_deny_yn',
        'buy_strat_type','buy_strat_name','buy_strat_freq',
        'setting_name','setting_value','buy_stat_name','buy_stat_value',
        'setting_name2','setting_value2','buy_stat_name2','buy_stat_value2',
        'setting_name3','setting_value3','buy_stat_name3','buy_stat_value3',
        'test_fnc_name','message'
    ]
    sql = (
        "INSERT INTO buy_decisions (" + ",".join(cols) + ") "
        "VALUES (" + ",".join(["%s"]*len(cols)) + ")"
    )
    def getv(obj, key):
        try:
            return getattr(obj, key)
        except Exception:
            try:
                return obj.get(key)
            except Exception:
                return None
    vals = tuple(getv(in_data, c) for c in cols)
    
    # 🔴 NO TRY/CATCH - Let errors propagate for full script stop
    if hasattr(self, 'ins_one'):
        self.ins_one(sql, vals, exit_on_error=True)
    else:
        self.execute(sql, vals)

#<=====>#

@narc(1)
def db_buy_decisions_cleanup_old(self, days_to_keep=90):
    """
    Delete buy_decisions rows older than specified days for table size management.
    
    Args:
        days_to_keep: Number of days of history to retain (default: 90)
        
    Returns:
        int: Number of rows deleted
        
    Raises:
        Exception: If cleanup fails
    """
    sql = f'''
        DELETE FROM buy_decisions 
        WHERE dlm < DATE_SUB(NOW(), INTERVAL {days_to_keep} DAY)
    '''
    
    # 🔴 NO TRY/CATCH - Let errors propagate
    if hasattr(self, 'execute'):
        self.execute(sql)
        rows_deleted = self.__session.rowcount if hasattr(self, '_pooled_db_mysql__session') else 0
    else:
        rows_deleted = 0
    
    return rows_deleted

#<=====>#
