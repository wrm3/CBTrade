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
from libs.common import narc


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_buy_signals'
log_name      = 'cbtrade.tbl_buy_signals'


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
def db_buy_signals_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_buy_signals_exists()')
    """Check if the buy_signals table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `buy_signals` (
            `signal_id` INT AUTO_INCREMENT PRIMARY KEY,
            `prod_id` VARCHAR(64),
            `buy_strat_type` VARCHAR(64),
            `buy_strat_name` VARCHAR(64),
            `buy_strat_freq` VARCHAR(64),
            `event_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `test_txn_yn` CHAR(1),
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_prod_strat (prod_id, buy_strat_name, buy_strat_freq),
            INDEX idx_event_dttm (event_dttm),
            INDEX idx_dlm_cleanup (dlm)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

@narc(1)
def db_buy_signals_ins(self, in_data):
    """
    Insert a compact buy signal row into MySQL cbtrade.buy_signals.
    Expected keys: prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, event_dttm (optional), test_txn_yn
    
    Returns:
        int: The signal_id (AUTO_INCREMENT primary key) of the inserted row
        
    Raises:
        Exception: If insert fails - NO silent failures for forensic integrity
    """
    cols = [
        'prod_id','buy_strat_type','buy_strat_name','buy_strat_freq','event_dttm','test_txn_yn'
    ]
    sql = (
        "INSERT INTO buy_signals (" + ",".join(cols) + ") "
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
        signal_id = self.ins_one(sql, vals, exit_on_error=True)
    else:
        self.execute(sql, vals)
        signal_id = self.lastrowid if hasattr(self, 'lastrowid') else None
    
    if signal_id is None:
        raise Exception(f"🔴 CRITICAL: buy_signals insert failed to return signal_id for {getv(in_data, 'prod_id')}")
    
    return signal_id

#<=====>#

@narc(1)
def db_buy_signals_cleanup_old(self, days_to_keep=90):
    """
    Delete buy_signals rows older than specified days for table size management.
    
    Args:
        days_to_keep: Number of days of history to retain (default: 90)
        
    Returns:
        int: Number of rows deleted
        
    Raises:
        Exception: If cleanup fails
    """
    sql = f'''
        DELETE FROM buy_signals 
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
