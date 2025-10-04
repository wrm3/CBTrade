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
from libs.common import narc, AttrDict, get_unix_timestamp, DictValCheck, dttm_get, dttm_unix
from libs.db_mysql.cbtrade.db_common import to_scalar_dict


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_sell_ords'
log_name      = 'cbtrade.tbl_sell_ords'


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
def db_sell_ords_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_sell_ords_exists()')
    """Check if the sell_ords table exists"""
    
    sql = '''
        CREATE TABLE IF NOT EXISTS `sell_ords` (
            `so_id` INT(11) PRIMARY KEY AUTO_INCREMENT,
            `test_txn_yn` CHAR(1) DEFAULT 'N',
            `base_symb` VARCHAR(64),
            `symb` VARCHAR(64),
            `prod_id` VARCHAR(64),
            `mkt_name` VARCHAR(64),
            `mkt_venue` VARCHAR(64),
            `pos_id` INT(11),
            `sell_seq_nbr` INT(11),
            `sell_order_uuid` VARCHAR(64),
            `sell_client_order_id` VARCHAR(64),
            `pos_type` VARCHAR(64),
            `ord_stat` VARCHAR(64),
            `sell_strat_type` VARCHAR(64),
            `sell_strat_name` VARCHAR(64),
            `sell_strat_freq` VARCHAR(64),
            `sell_asset_type` VARCHAR(64),
            `sell_curr_symb` VARCHAR(64),
            `recv_curr_symb` VARCHAR(64),
            `fees_curr_symb` VARCHAR(64),
            `sell_cnt_est` DECIMAL(36,12) DEFAULT 0,
            `sell_cnt_act` DECIMAL(36,12) DEFAULT 0,
            `fees_cnt_act` DECIMAL(36,12) DEFAULT 0,
            `tot_in_cnt` DECIMAL(36,12) DEFAULT 0,
            `prc_sell_est` DECIMAL(36,12) DEFAULT 0,
            `prc_sell_act` DECIMAL(36,12) DEFAULT 0,
            `prc_sell_tot` DECIMAL(36,12) DEFAULT 0,
            `prc_sell_slip_pct` DECIMAL(36,12) DEFAULT 0,
            `ignore_tf` TINYINT DEFAULT 0,
            `reason` VARCHAR(1024),
            `note1` VARCHAR(1024),
            `note2` VARCHAR(1024),
            `note3` VARCHAR(1024),
            `upd_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `sell_begin_dttm` TIMESTAMP,
            `sell_begin_unix` BIGINT DEFAULT 0,
            `sell_end_dttm` TIMESTAMP,
            `sell_end_unix` BIGINT DEFAULT 0,
            `elapsed_mins` INT(11) DEFAULT 0,
            `add_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `add_unix` BIGINT DEFAULT 0,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `dlm_unix` BIGINT DEFAULT 0,
            UNIQUE(`sell_order_uuid`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_sell_ords_trigs(self):
    # sell_ords
    return [
        "DROP TRIGGER IF EXISTS before_insert_sell_ords;",
        """
        CREATE TRIGGER before_insert_sell_ords BEFORE INSERT ON `sell_ords` FOR EACH ROW
        BEGIN
            SET NEW.sell_begin_unix = COALESCE(UNIX_TIMESTAMP(NEW.sell_begin_dttm),0);
            SET NEW.sell_end_unix   = COALESCE(UNIX_TIMESTAMP(NEW.sell_end_dttm),0);
            SET NEW.add_unix        = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix        = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_sell_ords;",
        """
        CREATE TRIGGER before_update_sell_ords BEFORE UPDATE ON `sell_ords` FOR EACH ROW
        BEGIN
            SET NEW.sell_begin_unix = COALESCE(UNIX_TIMESTAMP(NEW.sell_begin_dttm),0);
            SET NEW.sell_end_unix   = COALESCE(UNIX_TIMESTAMP(NEW.sell_end_dttm),0);
            SET NEW.dlm_unix        = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_sell_check_get(self, prod_id:str=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_sell_check_get(prod_id={prod_id})')
    """Get sell check data for market timing - READ ONLY
    Note: If no record exists, returns empty AttrDict.
    Caller must ensure record exists via db_mkt_checks_insupd() if needed.
    """

    sql = """
    select mc.sell_check_dttm, mc.sell_check_unix, mc.sell_check_guid 
      , (UNIX_TIMESTAMP() - mc.sell_check_unix) / 60 as elapsed_dttm
      , (UNIX_TIMESTAMP() - mc.sell_check_unix) / 60 as elapsed_unix 
      from mkt_checks mc 
      where 1=1
    """
    if prod_id:
        sql += f" and mc.prod_id = '{prod_id}' "

    sell_check_data_list = self.seld(sql)
    
    if sell_check_data_list:
        return sell_check_data_list
    else:
        return AttrDict()

#<=====>#

@narc(1)
def db_sell_ords_get(self, client_order_id:str=None, uuid:str=None, pos_id:str=None, prod_id:str=None, ord_stat:str=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_sell_ords_get(client_order_id={client_order_id}, uuid={uuid}, pos_id={pos_id}, prod_id={prod_id}, ord_stat={ord_stat})')
    """Get all open buy orders"""

    sql = """
    select so.*
      , so.elapsed_mins AS elapsed_dttm
      , (UNIX_TIMESTAMP() - so.sell_begin_unix) / 60 AS elapsed_unix
      , COALESCE((UNIX_TIMESTAMP() - so.sell_begin_unix) / 60, so.elapsed_mins) AS elapsed
      from sell_ords so 
      where 1=1 
      and so.ignore_tf = 0
    """
    if client_order_id:
        sql += f" and so.sell_client_order_id = '{client_order_id}' "
    if uuid:
        sql += f" and so.sell_order_uuid = '{uuid}' "
    if pos_id:
        sql += f" and so.pos_id = '{pos_id}' "
    if prod_id:
        sql += f" and so.prod_id = '{prod_id}' "
    if ord_stat:
        sql += f" and so.ord_stat = '{ord_stat}' "

    # print(f'db_sell_ords_get: {sql}')

    sell_ords_data = self.seld(sql, always_list_yn='Y')
    if self.debug_tf: print(f'db_sell_ords_get: {len(sell_ords_data)} records found')
    return sell_ords_data

#<=====>#

@narc(1)
def db_sell_ords_insupd(self, in_data):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_sell_ords_insupd(in_data={in_data})')


    self.insupd_ez(self.db_name, "sell_ords", in_data, exit_on_error=True)

    # Convert incoming object to a plain dict of scalar values.
    # IMPORTANT: AttrDict/AttrDictEnh store data in the mapping, not __dict__,
    # so use the shared helper to avoid producing an empty column set.
    # simple_dict = convert_to_scalar_dict(in_data)

    # self.insupd_ez(self.db_name, "sell_ords", simple_dict, exit_on_error=True)

#<=====>#
