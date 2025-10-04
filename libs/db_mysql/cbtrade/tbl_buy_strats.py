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
lib_name      = 'cbtrade.tbl_buy_strats'
log_name      = 'cbtrade.tbl_buy_strats'


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
def db_buy_strats_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_buy_strats_exists()')
    """Check if the bals table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `buy_strats` (
            `buy_strat_id` INT AUTO_INCREMENT PRIMARY KEY,
            `buy_strat_type` VARCHAR(255),
            `buy_strat_name` VARCHAR(255),
            `buy_strat_freq` VARCHAR(255)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

@narc(1)
def db_buy_strats_get(self):
    sql = """
    select * 
      from buy_strats 
      where 1=1 
    """
    return self.seld(sql)

#<=====>#

@narc(1)
def db_buy_strats_insupd(self, in_data):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_buy_strats_insupd(in_data={in_data})')

    self.insupd_ez(self.db_name, "buy_strats", in_data, exit_on_error=True)

    # # Convert AttrDictEnh to regular dictionary with scalar values
    # simple_dict = {}
    # for key, value in in_data.__dict__.items():
    #     # Skip internal attributes and nested dictionaries/objects
    #     if not key.startswith('_') and not isinstance(value, (dict, list, set, tuple)):
    #         simple_dict[key] = value
            
    # self.insupd_ez(self.db_name, "buy_strats", simple_dict, exit_on_error=True)

#<=====>#
