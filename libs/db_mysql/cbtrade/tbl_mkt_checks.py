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
from libs.common import narc, DictValCheck, dttm_get, dttm_unix
from libs.db_mysql.cbtrade.db_common import to_scalar_dict
from libs.common import AttrDict



#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_mkt_checks'
log_name      = 'cbtrade.tbl_mkt_checks'


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
def db_mkt_checks_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_mkt_checks_exists()')
    """Check if the mkt_checks table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `mkt_checks` (
            `prod_id` VARCHAR(64),
            `buy_check_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `buy_check_unix` BIGINT DEFAULT 0,
            `buy_check_guid` VARCHAR(64),
            `buy_check_elapsed_minutes` INT(11) DEFAULT 0,
            `sell_check_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `sell_check_unix` BIGINT DEFAULT 0,
            `sell_check_guid` VARCHAR(64),
            `sell_check_elapsed_minutes` INT(11) DEFAULT 0,
            `refresh_check_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `refresh_check_unix` BIGINT DEFAULT 0,
            `refresh_check_guid` VARCHAR(64),
            `refresh_check_elapsed_minutes` INT(11) DEFAULT 0,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `dlm_unix` BIGINT DEFAULT 0,
            UNIQUE(`prod_id`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_mkt_checks_trigs(self):
    # mkt_checks
    return [
        "DROP TRIGGER IF EXISTS before_insert_mkt_checks;",
        """
        CREATE TRIGGER before_insert_mkt_checks BEFORE INSERT ON `mkt_checks` FOR EACH ROW
        BEGIN
            SET NEW.buy_check_unix     = COALESCE(UNIX_TIMESTAMP(NEW.buy_check_dttm),0);
            SET NEW.sell_check_unix    = COALESCE(UNIX_TIMESTAMP(NEW.sell_check_dttm),0);
            SET NEW.refresh_check_unix = COALESCE(UNIX_TIMESTAMP(NEW.refresh_check_dttm),0);
            SET NEW.dlm_unix           = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_mkt_checks;",
        """
        CREATE TRIGGER before_update_mkt_checks BEFORE UPDATE ON `mkt_checks` FOR EACH ROW
        BEGIN
            SET NEW.buy_check_unix     = COALESCE(UNIX_TIMESTAMP(NEW.buy_check_dttm),0);
            SET NEW.sell_check_unix    = COALESCE(UNIX_TIMESTAMP(NEW.sell_check_dttm),0);
            SET NEW.refresh_check_unix = COALESCE(UNIX_TIMESTAMP(NEW.refresh_check_dttm),0);
            SET NEW.dlm_unix           = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_mkt_checks_get(self, prod_id:str=None):  # pyright: ignore[reportArgumentType]
    """Get buy/sell/refresh check data for market timing."""
    sql = """
    select prod_id
      , buy_check_dttm, buy_check_unix, buy_check_guid, (UNIX_TIMESTAMP() - buy_check_unix) / 60 as buy_elapsed_minutes
      , sell_check_dttm, sell_check_unix, sell_check_guid, (UNIX_TIMESTAMP() - sell_check_unix) / 60 as sell_elapsed_minutes
      , refresh_check_dttm, refresh_check_unix, refresh_check_guid, (UNIX_TIMESTAMP() - refresh_check_unix) / 60 as refresh_elapsed_minutes
      from mkt_checks mc 
      where 1=1
    """
    if prod_id:
        sql += f" and mc.prod_id = '{prod_id}' "
    rows = self.seld(sql)
    if rows:
        if prod_id:
            if isinstance(rows, list):
                rows = AttrDict(rows[0])
            else:
                rows = AttrDict(rows)
        return rows
    return AttrDict()

#<=====>#

@narc(1)
def db_mkt_checks_insupd(self, d):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_mkt_checks_insupd(d={d})')
    """Insert or update market check data with timestamp"""

    prod_id = d.prod_id
    if not prod_id:
        return None
    
    # MySQL upsert equivalent using ON DUPLICATE KEY UPDATE
    sql = f"""
    INSERT INTO mkt_checks (
        prod_id, buy_check_dttm, buy_check_unix, buy_check_guid,
        sell_check_dttm, sell_check_unix, sell_check_guid
    ) VALUES (
        '{prod_id}',
        NOW(), UNIX_TIMESTAMP(), '{d.get('buy_check_guid')}',
        NOW(), UNIX_TIMESTAMP(), '{d.get('sell_check_guid')}'
    )
    ON DUPLICATE KEY UPDATE
        buy_check_dttm = NOW(),
        buy_check_unix = UNIX_TIMESTAMP(),
        buy_check_guid = VALUES(buy_check_guid),
        sell_check_dttm = NOW(),
        sell_check_unix = UNIX_TIMESTAMP(),
        sell_check_guid = VALUES(sell_check_guid),
        dlm = NOW(),
        dlm_unix = UNIX_TIMESTAMP()
    """
    r = self.execute(sql)
    return r

#<=====>#

@narc(1)
def db_mkt_checks_buy_upd(self, prod_id, guid):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_mkt_checks_buy_upd(prod_id={prod_id}, guid={guid})')
    """
    Update market checks table with buy check information.
    Args:
        prod_id: Product ID to update
        guid: GUID for the buy check
    """
    sql = f"""
    update mkt_checks 
    set buy_check_dttm = '{dttm_get()}'
        , buy_check_unix = {dttm_unix()}
        , buy_check_guid = '{guid}' 
    where prod_id = '{prod_id}'
    """
    x = self.upd(sql)

#<=====>#

@narc(1)
def db_mkt_checks_sell_upd(self, prod_id, guid):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_mkt_checks_sell_upd(prod_id={prod_id}, guid={guid})')
    """
    Update market checks table with sell check information.
    Args:
        prod_id: Product ID to update
        guid: GUID for the sell check
    """
    sql = f"""
    update mkt_checks 
    set sell_check_dttm = '{dttm_get()}'
        , sell_check_unix = {dttm_unix()}
        , sell_check_guid = '{guid}' 
    where prod_id = '{prod_id}'
    """
    x = self.upd(sql)

#<=====>#
