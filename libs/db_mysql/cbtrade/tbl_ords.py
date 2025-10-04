
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
lib_name      = 'cbtrade.tbl_ords'
log_name      = 'cbtrade.tbl_ords'


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
def db_ords_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_ords_exists()')
    """Check if the ords table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `ords` (
            `ord_id` INT(11) PRIMARY KEY AUTO_INCREMENT,
            `ord_uuid` VARCHAR(256),
            `mkt_id` INT(11),
            `pos_id` INT(11),
            `buy_order_id` INT(11),
            `sell_order_id` INT(11),
            `prod_id` VARCHAR(64),
            `ord_bs` VARCHAR(64),
            `ord_cfg` VARCHAR(1024),
            `ord_base_size` DECIMAL(36,12) DEFAULT 0,
            `ord_limit_prc` DECIMAL(36,12) DEFAULT 0,
            `ord_post_only` TINYINT DEFAULT 0,
            `ord_quote_size` DECIMAL(36,12) DEFAULT 0,
            `ord_stop_dir` VARCHAR(64),
            `ord_stop_prc` DECIMAL(36,12) DEFAULT 0,
            `ord_stop_trigger_prc` DECIMAL(36,12) DEFAULT 0,
            `ord_type` VARCHAR(64),
            `order_id` VARCHAR(64),
            `ord_product_id` VARCHAR(64),
            `ord_user_id` VARCHAR(64),
            `ord_order_configuration` VARCHAR(1024),
            `ord_side` VARCHAR(64),
            `ord_client_order_id` VARCHAR(64),
            `ord_status` VARCHAR(64),
            `ord_time_in_force` VARCHAR(64),
            `ord_created_time` TIMESTAMP,
            `ord_completion_percentage` DECIMAL(36,12) DEFAULT 0,
            `ord_filled_size` DECIMAL(36,12) DEFAULT 0,
            `ord_average_filled_price` DECIMAL(36,12) DEFAULT 0,
            `ord_fee` DECIMAL(36,12) DEFAULT 0,
            `ord_number_of_fills` INT(11),
            `ord_filled_value` DECIMAL(36,12) DEFAULT 0,
            `ord_pending_cancel` TINYINT DEFAULT 0,
            `ord_size_in_quote` TINYINT DEFAULT 0,
            `ord_total_fees` DECIMAL(36,12) DEFAULT 0,
            `ord_size_inclusive_of_fees` TINYINT DEFAULT 0,
            `ord_total_value_after_fees` DECIMAL(36,12) DEFAULT 0,
            `ord_trigger_status` VARCHAR(64),
            `ord_order_type` VARCHAR(64),
            `ord_reject_reason` VARCHAR(64),
            `ord_settled` TINYINT DEFAULT 0,
            `ord_product_type` VARCHAR(64),
            `ord_reject_message` VARCHAR(1024),
            `ord_cancel_message` VARCHAR(1024),
            `ord_order_placement_source` VARCHAR(64),
            `ord_outstanding_hold_amount` DECIMAL(36,12) DEFAULT 0,
            `ord_is_liquidation` TINYINT DEFAULT 0,
            `ord_last_fill_time` TIMESTAMP,
            `ord_edit_history` VARCHAR(1024),
            `ord_leverage` DECIMAL(36,12) DEFAULT 0,
            `ord_margin_type` VARCHAR(64),
            `ord_retail_portfolio_id` VARCHAR(64),
            `ignore_tf` TINYINT DEFAULT 0,
            `note1` VARCHAR(1024),
            `note2` VARCHAR(1024),
            `note3` VARCHAR(1024),
            `ord_begin_time` TIMESTAMP,
            `ord_begin_unix` BIGINT DEFAULT 0,
            `ord_end_time` TIMESTAMP,
            `ord_end_unix` BIGINT DEFAULT 0,
            `elapsed_mins` INT(11) DEFAULT 0,
            `add_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `add_unix` BIGINT DEFAULT 0,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `dlm_unix` BIGINT DEFAULT 0,
            UNIQUE(`ord_uuid`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_ords_trigs(self):
    # ords
    return [
        "DROP TRIGGER IF EXISTS before_insert_ords;",
        """
        CREATE TRIGGER before_insert_ords BEFORE INSERT ON `ords` FOR EACH ROW
        BEGIN
            SET NEW.add_unix = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            IF NEW.dlm_unix IS NOT NULL THEN
            SET NEW.dlm_unix = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
            END IF;
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_ords;",
        """
        CREATE TRIGGER before_update_ords BEFORE UPDATE ON `ords` FOR EACH ROW
        BEGIN
            SET NEW.add_unix = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            IF NEW.dlm_unix IS NOT NULL THEN
            SET NEW.dlm_unix = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
            END IF;
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_ords_get(self, prod_id:str=None, client_order_id:str=None, ord_uuid:str=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_ords_get(prod_id={prod_id}, client_order_id={client_order_id}, ord_uuid={ord_uuid})')
    """
    Get orders data.
    Args:
        prod_id: Product ID
        client_order_id: Client order ID
        ord_uuid: Order UUID
    """

    sql = f"""
    select * from ords 
      where 1=1 
    """
    if prod_id:
        sql += f"   and prod_id = '{prod_id}' "
    if client_order_id:
        sql += f"   and client_order_id = '{client_order_id}' "
    if ord_uuid:
        sql += f"   and ord_uuid = '{ord_uuid}' "

    return self.seld(sql)

#<=====>#

@narc(1)
def db_ords_insupd(self, in_data):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_ords_insupd(in_data={in_data})')
    print(f"db_ords_insupd() ==> ({type(in_data)}): {in_data}")
    if DictValCheck(in_data, ['ord_uuid']):
        # Use parameterized query instead of string interpolation
        check_sql = "SELECT * FROM ords WHERE ord_uuid = %s"
        check = self.seld(check_sql, [in_data.ord_uuid])
        if check:
            # 🚨 ALWAYS update dlm and dlm_unix on any order update
            in_data.dlm = dttm_get()
            in_data.dlm_unix = dttm_unix()
            
            where_dict = {}
            where_dict['ord_uuid'] = in_data.ord_uuid
            
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(in_data)
                    
            self.upd_ez(self.db_name, "ords", simple_dict, where_dict=where_dict)
            # print(f"✅ Updated ords for {in_data.ord_uuid}")
        else:
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(in_data)
                    
            self.insupd_ez(self.db_name, "ords", simple_dict, validate_columns=True)
            # print(f"✅ Inserted ords for {in_data.ord_uuid}")
    else:
        print(f"🔴 WARNING: db_ords_insupd() ==> is missing required field ord_uuid")

#<=====>#
