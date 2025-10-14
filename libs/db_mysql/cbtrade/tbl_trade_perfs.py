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
import time

#<=====>#
# Imports - Project
#<=====>#
from libs.common import narc, AttrDict, get_unix_timestamp, DictValCheck, dttm_get, dttm_unix
from libs.db_mysql.cbtrade.db_common import to_scalar_dict


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_trade_perfs'
log_name      = 'cbtrade.tbl_trade_perfs'


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
def db_trade_perfs_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_perfs_exists()')
    """Check if the trade_perfs table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `trade_perfs` (
            `base_symb` VARCHAR(20),
            `quote_symb` VARCHAR(20),
            `prod_id` VARCHAR(50),
            `lta` VARCHAR(10),
            `tot_cnt` INT DEFAULT 0,
            `tot_open_cnt` INT DEFAULT 0,
            `tot_close_cnt` INT DEFAULT 0,
            `win_cnt` INT DEFAULT 0,
            `win_open_cnt` INT DEFAULT 0,
            `win_close_cnt` INT DEFAULT 0,
            `lose_cnt` INT DEFAULT 0,
            `lose_open_cnt` INT DEFAULT 0,
            `lose_close_cnt` INT DEFAULT 0,
            `win_pct` DECIMAL(36,12) DEFAULT 0.0,
            `win_open_pct` DECIMAL(36,12) DEFAULT 0.0,
            `win_close_pct` DECIMAL(36,12) DEFAULT 0.0,
            `lose_pct` DECIMAL(36,12) DEFAULT 0.0,
            `lose_open_pct` DECIMAL(36,12) DEFAULT 0.0,
            `lose_close_pct` DECIMAL(36,12) DEFAULT 0.0,
            `age_mins` DECIMAL(36,12) DEFAULT 0.0,
            `age_hours` DECIMAL(36,12) DEFAULT 0.0,
            `tot_out_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `tot_out_open_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `tot_out_close_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `tot_in_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `tot_in_open_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `tot_in_close_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `buy_fees_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `buy_fees_open_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `buy_fees_close_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `sell_fees_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `sell_fees_open_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `sell_fees_close_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `fees_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `fees_open_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `fees_close_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `buy_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `buy_open_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `buy_close_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `sell_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `sell_open_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `sell_close_cnt_tot` DECIMAL(36,12) DEFAULT 0.0,
            `hold_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `hold_open_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `hold_close_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `pocket_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `pocket_open_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `pocket_close_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `clip_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `clip_open_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `clip_close_cnt` DECIMAL(36,12) DEFAULT 0.0,
            `sell_order_cnt` INT DEFAULT 0,
            `sell_order_open_cnt` INT DEFAULT 0,
            `sell_order_close_cnt` INT DEFAULT 0,
            `sell_order_attempt_cnt` INT DEFAULT 0,
            `sell_order_attempt_open_cnt` INT DEFAULT 0,
            `sell_order_attempt_close_cnt` INT DEFAULT 0,
            `val_curr` DECIMAL(36,12) DEFAULT 0.0,
            `val_open_curr` DECIMAL(36,12) DEFAULT 0.0,
            `val_close_curr` DECIMAL(36,12) DEFAULT 0.0,
            `val_tot` DECIMAL(36,12) DEFAULT 0.0,
            `val_open_tot` DECIMAL(36,12) DEFAULT 0.0,
            `val_close_tot` DECIMAL(36,12) DEFAULT 0.0,
            `win_amt` DECIMAL(36,12) DEFAULT 0.0,
            `win_open_amt` DECIMAL(36,12) DEFAULT 0.0,
            `win_close_amt` DECIMAL(36,12) DEFAULT 0.0,
            `lose_amt` DECIMAL(36,12) DEFAULT 0.0,
            `lose_open_amt` DECIMAL(36,12) DEFAULT 0.0,
            `lose_close_amt` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_amt` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_open_amt` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_close_amt` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_amt_net` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_open_amt_net` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_close_amt_net` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_pct` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_open_pct` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_close_pct` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_pct_hr` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_open_pct_hr` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_close_pct_hr` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_pct_day` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_open_pct_day` DECIMAL(36,12) DEFAULT 0.0,
            `gain_loss_close_pct_day` DECIMAL(36,12) DEFAULT 0.0,
            `last_buy_bo_dttm` TIMESTAMP NULL,
            `last_buy_bo_unix` BIGINT DEFAULT 0,
            `last_buy_pos_dttm` TIMESTAMP NULL,
            `last_buy_pos_unix` BIGINT DEFAULT 0,
            `last_buy_dttm` TIMESTAMP NULL,
            `last_buy_unix` BIGINT DEFAULT 0,
            `needs_recalc_yn` VARCHAR(1) DEFAULT 'N',
            `last_upd_dttm` VARCHAR(30),
            `last_upd_unix` INT DEFAULT (UNIX_TIMESTAMP()),
            `add_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `add_unix` BIGINT DEFAULT 0,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `dlm_unix` BIGINT DEFAULT 0,
            PRIMARY KEY (`prod_id`, `lta`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_trade_perfs_trigs(self):
    # bals
    return [
        "DROP TRIGGER IF EXISTS before_insert_trade_perfs;",
        """
        CREATE TRIGGER before_insert_trade_perfs BEFORE INSERT ON `trade_perfs` FOR EACH ROW
        BEGIN
            SET NEW.last_upd_unix = COALESCE(UNIX_TIMESTAMP(NEW.last_upd_dttm),0);
            SET NEW.add_unix    = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix    = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_trade_perfs;",
        """
        CREATE TRIGGER before_update_trade_perfs BEFORE UPDATE ON `trade_perfs` FOR EACH ROW
        BEGIN
            SET NEW.last_upd_unix = COALESCE(UNIX_TIMESTAMP(NEW.last_upd_dttm),0);
            SET NEW.add_unix    = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix    = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_pairs_loop_top_perfs_prod_ids_get(self, lmt=None, pct_min=0, quote_curr_symb=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_pairs_loop_top_perfs_prod_ids_get(lmt={lmt}, pct_min={pct_min}, quote_curr_symb={quote_curr_symb})')
    sql = " "
    sql += "select tp.prod_id "
    sql += "  from trade_perfs tp "
    sql += "   where tp.lta = 'A'  "  # Use 'All' data to match view_mkt_perf behavior
    if quote_curr_symb:
        sql += f"  and tp.quote_symb = '{quote_curr_symb}' "
    if pct_min > 0:
        sql += f"  and tp.gain_loss_pct > {pct_min} "
    else:
        sql += "  and tp.gain_loss_pct > 0 "
    sql += "  order by tp.gain_loss_pct desc "
    if lmt:
        sql += "  limit {} ".format(lmt)

    rows = self.seld(sql, always_list_yn='Y')
    mkts = [row['prod_id'] for row in rows] if rows else []
    return mkts

#<=====>#

@narc(1)
def db_pairs_loop_top_gains_prod_ids_get(self, lmt=None, gain_min=0, quote_curr_symb=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_pairs_loop_top_gains_prod_ids_get(lmt={lmt}, gain_min={gain_min}, quote_curr_symb={quote_curr_symb})')
    sql = " "
    sql += "select tp.prod_id "
    sql += "  from trade_perfs tp "
    sql += "   where tp.lta = 'A'  "  # Use 'All' data to match view_mkt_perf behavior
    if quote_curr_symb:
        sql += f"  and tp.quote_symb = '{quote_curr_symb}' "
    sql += "  and tp.gain_loss_amt >= {} ".format(gain_min)
    sql += "  order by tp.gain_loss_amt desc "
    if lmt:
        sql += "  limit {} ".format(lmt)

    rows = self.seld(sql, always_list_yn='Y')
    mkts = [row['prod_id'] for row in rows] if rows else []
    return mkts

#<=====>#

@narc(1)
def db_trade_perfs_get(self, base_symb=None, quote_symb=None, prod_id=None, lta=None, min_trades=0, force_recalc=False):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_perfs_get(base_symb={base_symb}, quote_symb={quote_symb}, prod_id={prod_id}, lta={lta}, min_trades={min_trades}, force_recalc={force_recalc})')
    """
    Get all trade performances for a product
    Args:
        prod_id: Product ID string
        lta: Optional long-term average filter
    """
    
    # 🔧 CRITICAL FIX: Use same LTA default logic as recalc function to prevent LTA mismatch
    # When lta='' (empty string), default to 'A' to match recalc function behavior
    if lta == '':
        lta = 'A'
    
    # Ensure table exists before querying
    self.execute(self.db_trade_perfs_exists())
    sql = """
    select * 
      from trade_perfs 
      where 1=1
    """
    if quote_symb:
        sql += f" and quote_symb = '{quote_symb}' "
    if base_symb:
        sql += f" and base_symb = '{base_symb}' "
    if prod_id:
        sql += f" and prod_id = '{prod_id}' "
    if lta:
        sql += f" and lta = '{lta}' "
    if min_trades:
        sql += f" and tot_cnt >= {min_trades} "

    trade_perfs = []

    rows = self.seld(sql, always_list_yn='Y')
    if not rows:
        process_list = self.db_prod_ids_traded(base_symb=base_symb, quote_symb=quote_symb, prod_id=prod_id, lta=lta)
        if process_list:
            for row_data in process_list:
                row_prod_id = row_data['prod_id']
                self.db_trade_perfs_recalc(prod_id=row_prod_id, lta=lta)
                r = self.seld(sql, always_list_yn='Y')
                if r:
                    for x in r:
                        trade_perfs.append(AttrDict(x))

    if rows:
        for row in rows:
            trade_perf = AttrDict(row)
            
            # Calculate age like the trade_perfs pattern
            now_unix = get_unix_timestamp()
            trade_perf.age_hours = (now_unix - trade_perf.last_upd_unix) / 3600 if trade_perf.last_upd_unix else 999
            
            # Apply the same pattern as trade_strat_perfs: refresh if older than 24 hours OR if data is empty OR if needs_recalc_yn flag is set
            if trade_perf.age_hours > 24 or trade_perf.tot_cnt == 0 or trade_perf.needs_recalc_yn == 'Y':
                print(f"🔄 Trade performance is stale ({trade_perf.age_hours:.1f}h old), recalculating...")
                # Trigger recalculation for the specific L/T/A row we are inspecting
                fresh_perf = self.db_trade_perfs_recalc(prod_id=trade_perf.prod_id, lta=trade_perf.lta)
                if fresh_perf:
                    trade_perf = fresh_perf
            
            trade_perfs.append(trade_perf)
    
    return trade_perfs

#<=====>#

@narc(1)
def db_trade_perfs_recalc_single(self, prod_id, lta):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_perfs_recalc_single(prod_id={prod_id}, lta={lta})')
    """
    Internal method to calculate performance for a single LTA type
    """

    # time.sleep(0.5)

    t_start = time.time()
    # Call stored procedure - FAIL HARD if SP doesn't work, no fallback
    self.execute("CALL sp_trade_perfs_recalc(%s,%s)", [prod_id, lta])
    t_end = time.time()
    elapsed = t_end - t_start
    msg = f"sp_trade_perfs_recalc({prod_id}, {lta}) took {elapsed:.2f} seconds"
    print(msg)

    rows = self.seld("SELECT * FROM trade_perfs WHERE prod_id = %s AND lta = %s", [prod_id, lta], always_list_yn='Y')
    if rows:
        return AttrDict(rows[0])
    else:
        raise Exception(f"sp_trade_perfs_recalc({prod_id},{lta}) executed but returned no data")

#<=====>#

@narc(1)
def db_trade_perfs_recalc(self, prod_id, lta=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_perfs_recalc(prod_id={prod_id}, lta={lta})')
    """
    Recalculate trade performance metrics for a specific product
    When lta='' or None, creates all three record types (L, T, A) to ensure comprehensive coverage
    """
    
    # When lta is empty, create all three record types (L, T, A) via single SP call
    if lta == '' or lta is None:
        print(f"🔄 Creating L, T, and A records (SP bulk) for {prod_id}")
        self.execute("CALL sp_trade_perfs_recalc(%s,%s)", [prod_id, None])
        # Return the 'A' record as before
        rows = self.seld("SELECT * FROM trade_perfs WHERE prod_id = %s AND lta = %s", [prod_id, 'A'], always_list_yn='Y')
        if rows:
            return AttrDict(rows[0])
        else:
            raise Exception(f"sp_trade_perfs_recalc({prod_id},NULL) executed but A record not found")

    # 🔧 CRITICAL FIX: When lta is empty, create all three record types by calling self recursively
    return self.db_trade_perfs_recalc_single(prod_id, lta)

#<=====>#

@narc(1)
def db_trade_perfs_insupd(self, trade_perf):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_perfs_insupd(trade_perf={trade_perf})')
    if DictValCheck(trade_perf, ['prod_id', 'lta']):
        # Use parameterized query instead of string interpolation
        check_sql = "SELECT * FROM trade_perfs WHERE prod_id = %s AND lta = %s"
        check = self.seld(check_sql, [trade_perf.prod_id, trade_perf.lta])
        if check:
            # 🚨 ALWAYS update dlm and dlm_unix on any trade performance update
            trade_perf.dlm = dttm_get()
            trade_perf.dlm_unix = dttm_unix()
            
            where_dict = {}
            where_dict['prod_id'] = trade_perf.prod_id
            where_dict['lta'] = trade_perf.lta
            
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(trade_perf)
                    
            self.upd_ez(self.db_name, "trade_perfs", simple_dict, where_dict=where_dict)
            # print(f"✅ Updated trade_perfs for {trade_perf.prod_id} {trade_perf.lta}")
        else:
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(trade_perf)
                    
            self.insupd_ez(self.db_name, "trade_perfs", simple_dict, validate_columns=True)
            # print(f"✅ Inserted trade_perfs for {trade_perf.prod_id} {trade_perf.lta}")
    else:
        print(f"🔴 WARNING: trade_perfs_insupd() ==> {trade_perf.get('prod_id')} {trade_perf.get('lta')} is missing required fields")

#<=====>#

@narc(1)
def trade_perfs_flag_upd(self, prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.trade_perfs_flag_upd(prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta})')
    """
    Update strategy performance after a buy operation
    """
    # 🚨 Include timestamp updates in trade performance flag updates
    current_time = dttm_get()
    current_unix = dttm_unix()
    
    sql = f"""
        update trade_strat_perfs 
            set needs_recalc_yn = 'Y',
                dlm = '{current_time}',
                dlm_unix = {current_unix}
            where prod_id = '{prod_id}' 
            and buy_strat_type = '{buy_strat_type}' 
            and buy_strat_name = '{buy_strat_name}' 
            and buy_strat_freq = '{buy_strat_freq}' 
            and lta = '{lta}'
        """
    self.execute(sql)

#<=====>#

