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
from libs.common import narc, AttrDict, dttm_get, dttm_unix
from libs.db_mysql.cbtrade.db_common import to_scalar_dict


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_buy_ords'
log_name      = 'cbtrade.tbl_buy_ords'


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
def db_buy_ords_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_buy_ords_exists()')
    """Check if the buy_ords table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `buy_ords` (
            `bo_id` INT(11) PRIMARY KEY AUTO_INCREMENT,
            `test_txn_yn` CHAR(1) DEFAULT 'N',
            `base_symb` VARCHAR(64),
            `symb` VARCHAR(64),
            `prod_id` VARCHAR(64),
            `mkt_name` VARCHAR(64),
            `mkt_venue` VARCHAR(64),
            `buy_order_uuid` VARCHAR(64),
            `buy_client_order_id` VARCHAR(64),
            `pos_type` VARCHAR(64),
            `ord_stat` VARCHAR(64),
            `buy_strat_type` VARCHAR(64),
            `buy_strat_name` VARCHAR(64),
            `buy_strat_freq` VARCHAR(64),
            `buy_asset_type` VARCHAR(64),
            `buy_curr_symb` VARCHAR(64),
            `spend_curr_symb` VARCHAR(64),
            `fees_curr_symb` VARCHAR(64),
            `buy_cnt_est` DECIMAL(36,12) DEFAULT 0,
            `buy_cnt_act` DECIMAL(36,12) DEFAULT 0,
            `fees_cnt_act` DECIMAL(36,12) DEFAULT 0,
            `tot_out_cnt` DECIMAL(36,12) DEFAULT 0,
            `prc_buy_est` DECIMAL(36,12) DEFAULT 0,
            `prc_buy_act` DECIMAL(36,12) DEFAULT 0,
            `tot_prc_buy` DECIMAL(36,12) DEFAULT 0,
            `prc_buy_slip_pct` DECIMAL(36,12) DEFAULT 0,
            `ignore_tf` TINYINT DEFAULT 0,
            `reason` VARCHAR(1024),
            `note1` VARCHAR(1024),
            `note2` VARCHAR(1024),
            `note3` VARCHAR(1024),
            `buy_begin_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `buy_begin_unix` BIGINT DEFAULT 0,
            `buy_end_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `buy_end_unix` BIGINT DEFAULT 0,
            `elapsed_mins` INT(11) DEFAULT 0,
            `add_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `add_unix` BIGINT DEFAULT 0,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `dlm_unix` BIGINT DEFAULT 0,
            
            -- Secondary index for elapsed lookups
            KEY `idx_buyords_prod_keys_time` (`prod_id`, `buy_strat_type`, `buy_strat_name`, `buy_strat_freq`, `test_txn_yn`, `buy_begin_unix`),
            UNIQUE(`buy_order_uuid`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_buy_ords_trigs(self):
    # buy_ords
    return [
        "DROP TRIGGER IF EXISTS before_insert_buy_ords;",
        """
        CREATE TRIGGER before_insert_buy_ords BEFORE INSERT ON `buy_ords` FOR EACH ROW
        BEGIN
            SET NEW.buy_begin_unix = COALESCE(UNIX_TIMESTAMP(NEW.buy_begin_dttm),0);
            SET NEW.buy_end_unix   = COALESCE(UNIX_TIMESTAMP(NEW.buy_end_dttm),0);
            SET NEW.add_unix       = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix       = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_buy_ords;",
        """
        CREATE TRIGGER before_update_buy_ords BEFORE UPDATE ON `buy_ords` FOR EACH ROW
        BEGIN
            SET NEW.buy_begin_unix = COALESCE(UNIX_TIMESTAMP(NEW.buy_begin_dttm),0);
            SET NEW.buy_end_unix   = COALESCE(UNIX_TIMESTAMP(NEW.buy_end_dttm),0);
            SET NEW.dlm_unix       = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_buy_check_get(self, prod_id:str=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_buy_check_get(prod_id={prod_id})')
    """Get buy check data for market timing - READ ONLY
    Note: If no record exists, returns empty AttrDict.
    Caller must ensure record exists via db_mkt_checks_insupd() if needed.
    """

    sql = """
    select mc.buy_check_dttm, mc.buy_check_unix, mc.buy_check_guid 
      , (UNIX_TIMESTAMP() - mc.buy_check_unix) / 60 as elapsed_dttm
      , (UNIX_TIMESTAMP() - mc.buy_check_unix) / 60 as elapsed_unix 
      from mkt_checks mc 
      where 1=1
    """
    if prod_id:
        sql += f" and mc.prod_id = '{prod_id}' "

    buy_check_data_list = self.seld(sql)
    
    if buy_check_data_list:
        return buy_check_data_list
    else:
        return AttrDict()  # Return empty AttrDict if no data found

#<=====>#

@narc(1)
def db_buy_ords_get(self, client_order_id: str = None, uuid: str = None, prod_id: str = None, ord_stat: str = None):
    """Get buy orders with optional filters."""
    sql = """
    select bo.*
      , bo.elapsed_mins AS elapsed_dttm
      , (UNIX_TIMESTAMP() - bo.buy_begin_unix) / 60 AS elapsed_unix
      , COALESCE((UNIX_TIMESTAMP() - bo.buy_begin_unix) / 60, bo.elapsed_mins) AS elapsed
      from buy_ords bo
      where 1=1
      and bo.ignore_tf = 0
    """
    if client_order_id:
        sql += f" and bo.buy_client_order_id = '{client_order_id}' "
    if uuid:
        sql += f" and bo.buy_order_uuid = '{uuid}' "
    if prod_id:
        sql += f" and bo.prod_id = '{prod_id}' "
    if ord_stat:
        sql += f" and bo.ord_stat = '{ord_stat}' "
    return self.seld(sql)

#<=====>#

@narc(1)
def db_buy_ords_open_get(self):
    sql = """
    select bo.prod_id
      from buy_ords bo
      where 1=1
      and bo.ord_stat = 'OPEN'
      and bo.ignore_tf = 0
    """
    return self.seld(sql)

#<=====>#

@narc(1)
def db_buy_ords_insupd(self, in_data):
    """Insert or update buy_ords row (by bo_id or buy_order_uuid)."""
    simple_dict = to_scalar_dict(in_data)

    # 1) Primary key path
    try:
        bo_id = getattr(in_data, 'bo_id', None)
    except Exception:
        bo_id = in_data.get('bo_id') if hasattr(in_data, 'get') else None
    if bo_id:
        check_sql = "SELECT bo_id FROM buy_ords WHERE bo_id = %s"
        check = self.seld(check_sql, [bo_id])
        if check:
            where_dict = {'bo_id': bo_id}
            self.upd_ez(self.db_name, 'buy_ords', simple_dict, where_dict=where_dict)
            return

    # 2) Unique business key path
    try:
        buy_order_uuid = getattr(in_data, 'buy_order_uuid', None)
    except Exception:
        buy_order_uuid = in_data.get('buy_order_uuid') if hasattr(in_data, 'get') else None
    if buy_order_uuid:
        check_sql = "SELECT bo_id FROM buy_ords WHERE buy_order_uuid = %s"
        check = self.seld(check_sql, [buy_order_uuid])
        if check:
            where_dict = {'buy_order_uuid': buy_order_uuid}
            self.upd_ez(self.db_name, 'buy_ords', simple_dict, where_dict=where_dict)
            return

    # 3) Fallback insert-or-replace helper
    self.insupd_ez(self.db_name, 'buy_ords', simple_dict, exit_on_error=True)

#<=====>#

@narc(1)
def db_buy_ords_stat_upd(self, bo_id, ord_stat):
    """Update buy order status with timestamp maintenance."""
    current_time = dttm_get()
    current_unix = dttm_unix()
    sql = f"""update buy_ords set 
                    ord_stat = '{ord_stat}',
                    dlm = '{current_time}',
                    dlm_unix = {current_unix}
                  where bo_id = {bo_id}"""
    self.upd(sql)

#<=====>#

@narc(1)
def db_mkt_sizing_data_get_by_uuid(self, buy_order_uuid:str):
    if self.debug_tf: G(f"==> CBTRADE_DB.db_mkt_sizing_data_get_by_uuid(buy_order_uuid={buy_order_uuid})")
    """Get market sizing data for a buy order by UUID (joins with mkts table).

    Returns a list of dictionaries so callers can iterate safely even for a single row.
    """

    sql = """
        SELECT bo.*
             , m.base_curr_symb
             , m.base_size_incr
             , m.base_size_min
             , m.base_size_max
             , m.quote_curr_symb
             , m.quote_size_incr
             , m.quote_size_min
             , m.quote_size_max
          FROM buy_ords bo
          JOIN mkts m ON m.prod_id = bo.prod_id
         WHERE 1=1
           AND bo.buy_order_uuid = %s
           AND bo.ignore_tf = 0
    """

    rows = self.seld(sql, vals=(buy_order_uuid,), always_list_yn='Y')
    return rows

#<=====>#

# @narc(1)
# def db_buy_ords_insupd(self, in_data):
#     if self.debug_tf: G(f'==> CBTRADE_DB.db_buy_ords_insupd(in_data={in_data})')
#     # Delegate to tbl implementation
#     from libs.db_mysql.cbtrade.tbl_buy_ords import db_buy_ords_insupd as _impl
#     return _impl(self, in_data)

    # # Convert AttrDictEnh to regular dictionary with scalar values
    # simple_dict = {}
    # for key, value in in_data.__dict__.items():
    #     # Skip internal attributes and nested dictionaries/objects
    #     if not key.startswith('_') and not isinstance(value, (dict, list, set, tuple)):
    #         simple_dict[key] = value
            
    # self.insupd_ez(self.db_name, "buy_ords", simple_dict, exit_on_error=True)

#<=====>#

# @narc(1)
# def db_buy_ords_stat_upd(self, bo_id, ord_stat):
#     if self.debug_tf: G(f'==> CBTRADE_DB.db_buy_ords_stat_upd(bo_id={bo_id}, ord_stat={ord_stat})')
#     # Delegate to tbl implementation
#     from libs.db_mysql.cbtrade.tbl_buy_ords import db_buy_ords_stat_upd as _impl
#     return _impl(self, bo_id, ord_stat)

#<=====>#
