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

#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_currs'
log_name      = 'cbtrade.tbl_currs'


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
def db_currs_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_currs_exists()')
    """Check if the currs table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `currs` (
            `curr_id` INT(11) PRIMARY KEY AUTO_INCREMENT,
            `symb` VARCHAR(64),
            `name` VARCHAR(64),
            `curr_uuid` VARCHAR(64),
            `prc_usd` DECIMAL(36,12) DEFAULT 0,
            `create_dttm` TIMESTAMP,
            `update_dttm` TIMESTAMP,
            `delete_dttm` TIMESTAMP,
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
            UNIQUE(`curr_uuid`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_currs_trigs(self):
    # currs
    return [
        "DROP TRIGGER IF EXISTS before_insert_currs;",
        """
        CREATE TRIGGER before_insert_currs BEFORE INSERT ON `currs` FOR EACH ROW
        BEGIN
            SET NEW.create_unix = COALESCE(UNIX_TIMESTAMP(NEW.create_dttm),0);
            SET NEW.update_unix = COALESCE(UNIX_TIMESTAMP(NEW.update_dttm),0);
            SET NEW.delete_unix = COALESCE(UNIX_TIMESTAMP(NEW.delete_dttm),0);
            SET NEW.add_unix    = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix    = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_currs;",
        """
        CREATE TRIGGER before_update_currs BEFORE UPDATE ON `currs` FOR EACH ROW
        BEGIN
            SET NEW.create_unix = COALESCE(UNIX_TIMESTAMP(NEW.create_dttm),0);
            SET NEW.update_unix = COALESCE(UNIX_TIMESTAMP(NEW.update_dttm),0);
            SET NEW.delete_unix = COALESCE(UNIX_TIMESTAMP(NEW.delete_dttm),0);
            SET NEW.dlm_unix    = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_currs_get(self, symb:str=None):  # pyright: ignore[reportArgumentType]
    sql = """
    select *
      from currs
      where 1=1
    """
    if symb:
        sql += f" and symb = '{symb}' "
    return self.seld(sql)

#<=====>#

@narc(1)
def db_currs_insupd(self, in_data):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_currs_insupd(in_data={in_data})')
    if DictValCheck(in_data, ['symb','curr_uuid']):
        check_sql = f"""select * 
                          from currs 
                          where symb = '{in_data.symb}' 
                          and curr_uuid = '{in_data.curr_uuid}' 
                          """
        check = self.seld(check_sql)
        if check:
            # 🚨 ALWAYS update dlm and dlm_unix on any currency update
            in_data.dlm = dttm_get()
            in_data.dlm_unix = dttm_unix()
            
            where_dict = {}
            where_dict['symb'] = in_data.symb
            where_dict['curr_uuid'] = in_data.curr_uuid
            
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(in_data)
                    
            self.upd_ez(self.db_name, "currs", simple_dict, where_dict=where_dict)
            # print(f"✅ Updated currs for {in_data.symb}")
        else:
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(in_data)
                    
            self.insupd_ez(self.db_name, "currs", simple_dict, validate_columns=True)
            # print(f"✅ Inserted currs for {in_data.symb}")
    else:
        print(f"🔴 WARNING: db_currs_insupd() ==> {in_data.get('symb')} is missing required fields")

#<=====>#

@narc(1)
def db_currs_prc_upd(self, symb:str, prc_usd:float):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_currs_prc_upd(symb={symb}, prc_usd={prc_usd})')
    """
    Update currency price in USD.
    Args:
        prc_usd: Price in USD
        symb: Currency symbol
    """
    # 🚨 Include timestamp updates in currency price updates
    current_time = dttm_get()
    current_unix = dttm_unix()
    
    sql = f"""update currs 
              set prc_usd = {prc_usd},
                  dlm = '{current_time}',
                  dlm_unix = {current_unix}
              where symb = '{symb}'"""
    self.upd(sql)

#<=====>#

@narc(1)
def db_currs_prc_stable_upd(self, stable_symbs:list=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_currs_prc_stable_upd(stable_symbs={stable_symbs})')
    """
    Update stable currency prices to 1.00 USD.
    Args:
        stable_symbs: List of stable coin symbols
    """
    if stable_symbs is None:
        stable_symbs = ['USDC', 'USDT', 'DAI', 'USD', 'PAX', 'BUSD', 'UST', 'USDP', 'GUSD', 'TUSD']
    
    # 🚨 Include timestamp updates in stable currency price updates
    current_time = dttm_get()
    current_unix = dttm_unix()
    
    for s in stable_symbs:
        sql = f"""update currs 
                  set prc_usd = 1.00,
                      dlm = '{current_time}',
                      dlm_unix = {current_unix}
                  where symb = '{s}'"""
        self.upd(sql)

#<=====>#

@narc(1)
def db_currs_prc_mkt_upd(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_currs_prc_mkt_upd()')
    """
    Update currency prices from market data.
    """
    # 🚨 Include timestamp updates in currency market price updates
    current_time = dttm_get()
    current_unix = dttm_unix()
    
    sql = f"""update currs 
              set prc_usd = coalesce((select m.prc 
                                      from mkts m 
                                      where m.base_curr_symb = currs.symb 
                                      and m.quote_curr_symb = 'USD'),0),
                  dlm = '{current_time}',
                  dlm_unix = {current_unix}"""
    self.execute(sql)

#<=====>#
