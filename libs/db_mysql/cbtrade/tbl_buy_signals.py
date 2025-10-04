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
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

@narc(1)
def db_buy_signals_ins(self, in_data):
    """
    Insert a compact buy signal row into MySQL cbtrade.buy_signals.
    Expected keys: prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, event_dttm (optional), test_txn_yn
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
    try:
        if hasattr(self, 'ins_one'):
            self.ins_one(sql, vals, exit_on_error=False)
        else:
            self.execute(sql, vals)
    except Exception:
        pass

#<=====>#
