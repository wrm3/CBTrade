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
from libs.common import DictValCheck, dttm_get, dttm_unix
from libs.db_mysql.cbtrade.db_common import to_scalar_dict


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_bals'
log_name      = 'cbtrade.tbl_bals'


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
def db_bals_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_bals_exists()')
    """Check if the bals table exists"""

    sql = '''
        CREATE TABLE IF NOT EXISTS `bals` (
            `bal_id` INT(11) PRIMARY KEY AUTO_INCREMENT,
            `curr_uuid` VARCHAR(64),
            `symb` VARCHAR(64),
            `name` VARCHAR(64),
            `bal_avail` DECIMAL(36,12) DEFAULT 0,
            `bal_hold` DECIMAL(36,12) DEFAULT 0,
            `bal_tot` DECIMAL(36,12) DEFAULT 0,
            `rp_id` VARCHAR(64),
            `default_tf` TINYINT DEFAULT 0,
            `active_tf` TINYINT DEFAULT 0,
            `ready_tf` TINYINT DEFAULT 0,
            `create_dttm` TIMESTAMP,
            `update_dttm` TIMESTAMP,
            `delete_dttm` TIMESTAMP,
            `curr_prc_usd` DECIMAL(36,12) DEFAULT 0,
            `curr_val_usd` DECIMAL(36,12) DEFAULT 0,
            `ignore_tf` TINYINT DEFAULT 0,
            `note1` VARCHAR(1024),
            `note2` VARCHAR(1024),
            `note3` VARCHAR(1024),
            `create_unix` BIGINT DEFAULT 0,
            `update_unix` BIGINT DEFAULT 0,
            `delete_unix` BIGINT DEFAULT 0,
            `add_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `add_unix` BIGINT DEFAULT 0,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `dlm_unix` BIGINT DEFAULT 0,
            UNIQUE(`curr_uuid`),
            UNIQUE(`symb`,`rp_id`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_bals_trigs(self):
    # bals
    return [
        "DROP TRIGGER IF EXISTS before_insert_bals;",
        """
        CREATE TRIGGER before_insert_bals BEFORE INSERT ON `bals` FOR EACH ROW
        BEGIN
            SET NEW.create_unix = COALESCE(UNIX_TIMESTAMP(NEW.create_dttm),0);
            SET NEW.update_unix = COALESCE(UNIX_TIMESTAMP(NEW.update_dttm),0);
            SET NEW.delete_unix = COALESCE(UNIX_TIMESTAMP(NEW.delete_dttm),0);
            SET NEW.add_unix    = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix    = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_bals;",
        """
        CREATE TRIGGER before_update_bals BEFORE UPDATE ON `bals` FOR EACH ROW
        BEGIN
            SET NEW.create_unix = COALESCE(UNIX_TIMESTAMP(NEW.create_dttm),0);
            SET NEW.update_unix = COALESCE(UNIX_TIMESTAMP(NEW.update_dttm),0);
            SET NEW.delete_unix = COALESCE(UNIX_TIMESTAMP(NEW.delete_dttm),0);
            SET NEW.add_unix    = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix    = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_bals_get(self, symb:str=None):
    sql = """
    select symb, bal_avail 
        from bals
    """
    if symb:
        sql += f" where symb = '{symb}'"
    return self.seld(sql)

#<=====>#

@narc(1)
def db_bals_insupd(self, in_data):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_bals_insupd(in_data={in_data})')
    if DictValCheck(in_data, ['symb','bal_avail','curr_uuid','rp_id']):
        check_sql = f"""select * 
                            from bals 
                            where symb = '{in_data.symb}' 
                            and curr_uuid = '{in_data.curr_uuid}' 
                            and rp_id = '{in_data.rp_id}' 
                            """
        check = self.seld(check_sql)
        if check:
            # 🚨 ALWAYS update dlm and dlm_unix on any balance update
            in_data.dlm = dttm_get()
            in_data.dlm_unix = dttm_unix()
            
            where_dict = {}
            where_dict['symb'] = in_data.symb
            where_dict['curr_uuid'] = in_data.curr_uuid
            where_dict['rp_id'] = in_data.rp_id
            
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(in_data)
            
            self.upd_ez(self.db_name, "bals", simple_dict, where_dict=where_dict)
            # print(f"✅ Updated bals for {in_data.symb}")
        else:
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(in_data)
            
            self.insupd_ez(self.db_name, "bals", simple_dict, validate_columns=True)
            # print(f"✅ Inserted bals for {in_data.symb}")
    else:
        print('db_bals_insupd ERROR - Missing required fields: symb, bal_avail, curr_uuid, or rp_id')

#<=====>#

@narc(1)
def db_bals_prc_mkt_upd(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_bals_prc_mkt_upd()')
    """
    Update balance prices and values from market data.
    """

    sql = ""
    sql += "update bals "
    sql += "  set curr_prc_usd = coalesce((select prc "
    sql += "                               from mkts "
    sql += "                               where base_curr_symb = bals.symb "
    sql += "                               and quote_curr_symb = 'USDC'),0) "
    sql += "    , curr_val_usd = bal_tot * coalesce((select prc "
    sql += "                                         from mkts "
    sql += "                                         where base_curr_symb = bals.symb "
    sql += "                                         and quote_curr_symb = 'USDC'),0) "
    # 🚨 ALWAYS update dlm and dlm_unix on any balance market update
    sql += f"    , dlm = '{dttm_get()}' "
    sql += f"    , dlm_unix = {dttm_unix()} "
    x = self.upd(sql)

#<=====>#
