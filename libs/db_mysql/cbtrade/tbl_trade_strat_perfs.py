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
from libs.common import (
    narc
    , AttrDict
    , get_unix_timestamp
    , DictValCheck
    , dttm_get
    , dttm_unix
)
from libs.db_mysql.cbtrade.db_common import to_scalar_dict

#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_trade_strat_perfs'
log_name      = 'cbtrade.tbl_trade_strat_perfs'


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
def db_trade_strat_perfs_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_strat_perfs_exists()')
    """Check if the trade_strat_perfs table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `trade_strat_perfs` (
            `base_symb` VARCHAR(20),
            `quote_symb` VARCHAR(20),
            `prod_id` VARCHAR(50),
            `lta` VARCHAR(10),
            `buy_strat_type` VARCHAR(50),
            `buy_strat_name` VARCHAR(50),
            `buy_strat_freq` VARCHAR(50),
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
            -- Persist last strat event timestamps instead of elapsed
            `last_buy_strat_bo_dttm` TIMESTAMP NULL,
            `last_buy_strat_bo_unix` BIGINT DEFAULT 0,
            `last_buy_strat_pos_dttm` TIMESTAMP NULL,
            `last_buy_strat_pos_unix` BIGINT DEFAULT 0,
            `last_buy_strat_dttm` TIMESTAMP NULL,
            `last_buy_strat_unix` BIGINT DEFAULT 0,
            `needs_recalc_yn` VARCHAR(1) DEFAULT 'N',
            `last_upd_dttm` VARCHAR(30),
            `last_upd_unix` INT DEFAULT (UNIX_TIMESTAMP()),
            `add_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `add_unix` BIGINT DEFAULT 0,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `dlm_unix` BIGINT DEFAULT 0,
            
            -- Secondary indexes for common access patterns
            KEY `idx_tsp_prod` (`prod_id`),
            KEY `idx_tsp_prod_lta_day` (`prod_id`, `lta`, `gain_loss_pct_day`),
            KEY `idx_tsp_prod_keys` (`prod_id`, `buy_strat_type`, `buy_strat_name`, `buy_strat_freq`),
            KEY `idx_tsp_prod_lastupd` (`prod_id`, `last_upd_unix`),

            PRIMARY KEY (`prod_id`, `lta`, `buy_strat_type`, `buy_strat_name`, `buy_strat_freq`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_trade_strat_perfs_trigs(self):
    # bals
    return [
        "DROP TRIGGER IF EXISTS before_insert_trade_strat_perfs;",
        """
        CREATE TRIGGER before_insert_trade_strat_perfs BEFORE INSERT ON `trade_strat_perfs` FOR EACH ROW
        BEGIN
            SET NEW.last_upd_unix = COALESCE(UNIX_TIMESTAMP(NEW.last_upd_dttm),0);
            SET NEW.add_unix    = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix    = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_trade_strat_perfs;",
        """
        CREATE TRIGGER before_update_trade_strat_perfs BEFORE UPDATE ON `trade_strat_perfs` FOR EACH ROW
        BEGIN
            SET NEW.last_upd_unix = COALESCE(UNIX_TIMESTAMP(NEW.last_upd_dttm),0);
            SET NEW.add_unix    = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix    = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_trade_strat_perfs_get(self, base_symb=None, quote_symb=None, prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None, lta=None, min_trades=0, force_recalc=False):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_strat_perfs_get(base_symb={base_symb}, quote_symb={quote_symb}, prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta}, min_trades={min_trades}, force_recalc={force_recalc})')

    """
    Get all strategy performances for a product
    Args:
        prod_id: Product ID string
        buy_strat_type: Buy strategy type string
        buy_strat_name: Buy strategy name string
        buy_strat_freq: Buy strategy frequency string
        lta: Optional long-term average filter
    """
    
    # 🔧 CRITICAL FIX: Use same LTA default logic as recalc function to prevent LTA mismatch
    # When lta='' (empty string), default to 'A' to match recalc function behavior
    if lta == '':
        lta = 'A'
    
    # Ensure table exists before querying
    self.execute(self.db_trade_strat_perfs_exists())
    sql = """
    select * 
      from trade_strat_perfs 
      where 1=1
    """
    
    # Build parameter list
    params = []
    
    if quote_symb:
        sql += " and quote_symb = %s "
        params.append(quote_symb)
    if base_symb:
        sql += " and base_symb = %s "
        params.append(base_symb)
    if prod_id:
        sql += " and prod_id = %s "
        params.append(prod_id)
    if buy_strat_type:
        sql += " and buy_strat_type = %s "
        params.append(buy_strat_type)
    if buy_strat_name:
        sql += " and buy_strat_name = %s "
        params.append(buy_strat_name)
    if buy_strat_freq:
        sql += " and buy_strat_freq = %s "
        params.append(buy_strat_freq)
    if lta:
        sql += " and lta = %s "
        params.append(lta)
    if min_trades:
        sql += " and tot_cnt >= %s "
        params.append(min_trades)

    trade_strat_perfs = []

    rows = self.seld(sql, params, always_list_yn='Y')

    if rows:
        for row in rows:
            strat_perf = AttrDict(row)
            
            # Calculate age like the trade_perfs pattern
            now_unix = get_unix_timestamp()
            strat_perf.age_hours = (now_unix - strat_perf.last_upd_unix) / 3600 if strat_perf.last_upd_unix else 999
            
            # Apply the same pattern as trade_perfs: refresh if older than 24 hours OR if data is empty
            if strat_perf.age_hours > 24 or strat_perf.needs_recalc_yn == 'Y':
                if self.debug_tf: G(f"🔄 tbl_trade_strat_perfs.db_trade_strat_perfs_get() ==> {strat_perf.prod_id} Strategy performance for {strat_perf.buy_strat_type} {strat_perf.buy_strat_name} {strat_perf.buy_strat_freq} {strat_perf.lta} is stale ({strat_perf.age_hours:.1f}h old), recalculating...")
                # Trigger recalculation for this specific strategy
                fresh_perf = self.db_trade_strat_perfs_recalc_single(strat_perf.prod_id, strat_perf.buy_strat_type, strat_perf.buy_strat_name, strat_perf.buy_strat_freq, strat_perf.lta)
                if fresh_perf:
                    strat_perf = fresh_perf
            
            trade_strat_perfs.append(strat_perf)
    
    return trade_strat_perfs

#<=====>#

@narc(1)
def db_trade_strat_perfs_recalc_single(self, prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_strat_perfs_recalc_single(prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta})')
    """
    Internal method to calculate performance for a single LTA type
    """

    # time.sleep(0.5)

    t_start = time.time()

    # Call stored procedure - FAIL HARD if SP doesn't work, no fallback
    self.execute(
        "CALL sp_trade_strat_perfs_recalc(%s,%s,%s,%s,%s)",
        [prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta]
    )
    t_end = time.time()
    elapsed = t_end - t_start
    msg = f"sp_trade_strat_perfs_recalc({prod_id}, {buy_strat_type}, {buy_strat_name}, {buy_strat_freq}, {lta}) took {elapsed:.2f} seconds"
    print(msg)


    rows = self.seld(
        "SELECT * FROM trade_strat_perfs WHERE prod_id = %s AND buy_strat_type = %s AND buy_strat_name = %s AND buy_strat_freq = %s AND lta = %s",
        [prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta], always_list_yn='Y'
    )
    if rows:
        return AttrDict(rows[0])
    else:
        raise Exception(f"sp_trade_strat_perfs_recalc({prod_id},{buy_strat_type},{buy_strat_name},{buy_strat_freq},{lta}) executed but returned no data")


    # sql_str1 = ""
    # sql_str2 = ""
    # if lta:
    #     if lta == 'L':
    #         sql_str1 = """
    #           and p.test_txn_yn = 'N'
    #         """
    #         sql_str2 = """
    #           and b.test_txn_yn = 'N'
    #         """
    #     elif lta == 'T':
    #         sql_str1 = """
    #           and p.test_txn_yn = 'Y'
    #         """
    #         sql_str2 = """
    #           and b.test_txn_yn = 'Y'
    #         """

    # # Build SQL query using parameterized queries instead of f-strings
    # sql = """
    # SELECT SUBSTRING_INDEX(%s, '-', 1) as base_symb
    #   , SUBSTRING_INDEX(%s, '-', -1) as quote_symb
    #   , %s as prod_id

    #   , %s as lta
    #   , %s as buy_strat_type
    #   , %s as buy_strat_name
    #   , %s as buy_strat_freq

    #   , NOW() as last_upd_dttm
    #   , UNIX_TIMESTAMP() as last_upd_unix

    #   , count(p.pos_id) as tot_cnt
    #   , coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then 1 else 0 end), 0) as tot_open_cnt
    #   , coalesce(sum(case when p.pos_stat = 'CLOSE' then 1 else 0 end), 0) as tot_close_cnt

    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end), 0) as win_cnt
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt and p.pos_stat in ('OPEN','SELL') then 1 else 0 end), 0) as win_open_cnt
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt and p.pos_stat = 'CLOSE' then 1 else 0 end), 0) as win_close_cnt

    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end), 0) as lose_cnt
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt and p.pos_stat in ('OPEN','SELL') then 1 else 0 end), 0) as lose_open_cnt
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt and p.pos_stat = 'CLOSE' then 1 else 0 end), 0) as lose_close_cnt

    #   , round(coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 0), 2) as win_pct
    #   , round(coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 0), 2) as win_open_pct
    #   , round(coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 0), 2) as win_close_pct

    #   , round(coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 0), 2) as lose_pct
    #   , round(coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 0), 2) as lose_open_pct
    #   , round(coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 0), 2) as lose_close_pct

    #   , coalesce(sum(p.age_mins), 0) as age_mins
    #   , round(coalesce(sum(p.age_mins) / 60.0, 0), 2) as age_hours

    #   , round(coalesce(sum(p.tot_out_cnt), 0), 16) as tot_out_cnt
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end), 0), 16) as tot_out_open_cnt
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end), 0), 16) as tot_out_close_cnt

    #   , round(coalesce(sum(p.tot_in_cnt), 0), 16) as tot_in_cnt
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_in_cnt else 0 end), 0), 16) as tot_in_open_cnt
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.tot_in_cnt else 0 end), 0), 16) as tot_in_close_cnt

    #   , round(coalesce(sum(p.buy_fees_cnt), 0), 16) as buy_fees_cnt
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.buy_fees_cnt else 0 end), 0), 16) as buy_fees_open_cnt
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.buy_fees_cnt else 0 end), 0), 16) as buy_fees_close_cnt

    #   , round(coalesce(sum(p.sell_fees_cnt_tot), 0), 16) as sell_fees_cnt_tot
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.sell_fees_cnt_tot else 0 end), 0), 16) as sell_fees_open_cnt_tot
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.sell_fees_cnt_tot else 0 end), 0), 16) as sell_fees_close_cnt_tot

    #   , round(coalesce(sum(p.fees_cnt_tot), 0), 16) as fees_cnt_tot
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.fees_cnt_tot else 0 end), 0), 16) as fees_open_cnt_tot
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.fees_cnt_tot else 0 end), 0), 16) as fees_close_cnt_tot

    #   , round(coalesce(sum(p.buy_cnt), 0), 16) as buy_cnt
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.buy_cnt else 0 end), 0), 16) as buy_open_cnt
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.buy_cnt else 0 end), 0), 16) as buy_close_cnt

    #   , round(coalesce(sum(p.sell_cnt_tot), 0), 16) as sell_cnt_tot
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.sell_cnt_tot else 0 end), 0), 16) as sell_open_cnt_tot
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.sell_cnt_tot else 0 end), 0), 16) as sell_close_cnt_tot

    #   , round(coalesce(sum(p.hold_cnt), 0), 16) as hold_cnt
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.hold_cnt else 0 end), 0), 16) as hold_open_cnt
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.hold_cnt else 0 end), 0), 16) as hold_close_cnt

    #   , round(coalesce(sum(p.pocket_cnt), 0), 16) as pocket_cnt
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.pocket_cnt else 0 end), 0), 16) as pocket_open_cnt
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.pocket_cnt else 0 end), 0), 16) as pocket_close_cnt

    #   , round(coalesce(sum(p.clip_cnt), 0), 16) as clip_cnt
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.clip_cnt else 0 end), 0), 16) as clip_open_cnt
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.clip_cnt else 0 end), 0), 16) as clip_close_cnt

    #   , coalesce(sum(p.sell_order_cnt), 0) as sell_order_cnt
    #   , coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.sell_order_cnt else 0 end), 0) as sell_order_open_cnt
    #   , coalesce(sum(case when p.pos_stat = 'CLOSE' then p.sell_order_cnt else 0 end), 0) as sell_order_close_cnt
    #   , coalesce(sum(p.sell_order_attempt_cnt), 0) as sell_order_attempt_cnt
    #   , coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.sell_order_attempt_cnt else 0 end), 0) as sell_order_attempt_open_cnt
    #   , coalesce(sum(case when p.pos_stat = 'CLOSE' then p.sell_order_attempt_cnt else 0 end), 0) as sell_order_attempt_close_cnt

    #   , round(coalesce(sum(p.val_curr), 0), 16) as val_curr
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.val_curr else 0 end), 0), 16) as val_open_curr
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.val_curr else 0 end), 0), 16) as val_close_curr
    #   , round(coalesce(sum(p.val_tot), 0), 16) as val_tot
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.val_tot else 0 end), 0), 16) as val_open_tot
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.val_tot else 0 end), 0), 16) as val_close_tot
      
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then p.val_tot else 0 end), 16) as win_amt
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt and p.pos_stat in ('OPEN','SELL') then p.val_tot else 0 end), 16) as win_open_amt
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt and p.pos_stat = 'CLOSE' then p.val_tot else 0 end), 16) as win_close_amt

    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end), 0) as lose_amt
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt and p.pos_stat in ('OPEN','SELL') then 1 else 0 end), 0) as lose_open_amt
    #   , coalesce(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt and p.pos_stat = 'CLOSE' then 1 else 0 end), 0) as lose_close_cnt

    #   , round(coalesce(sum(p.gain_loss_amt), 0), 16) as gain_loss_amt
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end), 0), 16) as gain_loss_open_amt
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end), 0), 16) as gain_loss_close_amt

    #   , round(coalesce(sum(p.gain_loss_amt_net), 0), 16) as gain_loss_amt_net
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt_net else 0 end), 0), 16) as gain_loss_open_amt_net
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt_net else 0 end), 0), 16) as gain_loss_close_amt_net

    #   , round(coalesce(sum(p.gain_loss_amt) * 100.0 / sum(p.tot_out_cnt), 0), 2) as gain_loss_pct
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end), 0), 2) as gain_loss_open_pct
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end), 0), 2) as gain_loss_close_pct

    #   , round(coalesce(sum(p.gain_loss_amt) * 100.0 / sum(p.tot_out_cnt), 0), 2) as gain_loss_pct
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end), 0), 2) as gain_loss_open_pct
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end), 0), 2) as gain_loss_close_pct

    #   , round(coalesce(sum(p.gain_loss_amt) * 100.0 / sum(p.tot_out_cnt) / (sum(p.age_mins) / 60.0), 0), 16) as gain_loss_pct_hr
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end) / (sum(p.age_mins) / 60.0), 0), 16) as gain_loss_open_pct_hr
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end) / (sum(p.age_mins) / 60.0), 0), 16) as gain_loss_close_pct_hr

    #   , round(coalesce(sum(p.gain_loss_amt) * 100.0 / sum(p.tot_out_cnt) / (sum(p.age_mins) / 60.0) * 24, 0), 16) as gain_loss_pct_day
    #   , round(coalesce(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end) / (sum(p.age_mins) / 60.0) * 24, 0), 16) as gain_loss_open_pct_day
    #   , round(coalesce(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end) / (sum(p.age_mins) / 60.0) * 24, 0), 16) as gain_loss_close_pct_day

    #   , FROM_UNIXTIME(COALESCE((select max(b.buy_begin_unix)
    #                                         from buy_ords b 
    #                                         where b.prod_id = %s 
    #                                         and b.buy_strat_type = %s 
    #                                         and b.buy_strat_name = %s 
    #                                         and b.buy_strat_freq = %s 
    #                                         and (CASE WHEN %s = 'L' THEN b.test_txn_yn = 'N'
    #                                              WHEN %s = 'T' THEN b.test_txn_yn = 'Y'
    #                                              ELSE 1=1 END)
    #                                         ),0)) as last_buy_strat_bo_dttm
    #   , COALESCE((select max(b.buy_begin_unix) from buy_ords b where b.prod_id = %s and b.buy_strat_type = %s and b.buy_strat_name = %s and b.buy_strat_freq = %s and (CASE WHEN %s = 'L' THEN b.test_txn_yn = 'N' WHEN %s = 'T' THEN b.test_txn_yn = 'Y' ELSE 1=1 END)),0) as last_buy_strat_bo_unix
    #   , FROM_UNIXTIME(COALESCE((select max(p.pos_begin_unix) 
    #                                         from poss p 
    #                                         where p.prod_id = %s 
    #                                         and p.buy_strat_type = %s 
    #                                         and p.buy_strat_name = %s 
    #                                         and p.buy_strat_freq = %s 
    #                                         and (CASE WHEN %s = 'L' THEN p.test_txn_yn = 'N'
    #                                              WHEN %s = 'T' THEN p.test_txn_yn = 'Y'
    #                                              ELSE 1=1 END)
    #                                         ),0)) as last_buy_strat_pos_dttm
    #   , COALESCE((select max(p.pos_begin_unix) from poss p where p.prod_id = %s and p.buy_strat_type = %s and p.buy_strat_name = %s and p.buy_strat_freq = %s and (CASE WHEN %s = 'L' THEN p.test_txn_yn = 'N' WHEN %s = 'T' THEN p.test_txn_yn = 'Y' ELSE 1=1 END)),0) as last_buy_strat_pos_unix
    #   , FROM_UNIXTIME(GREATEST(
    #         COALESCE((SELECT MAX(p.pos_begin_unix) FROM poss p WHERE p.prod_id = %s AND p.buy_strat_type = %s AND p.buy_strat_name = %s AND p.buy_strat_freq = %s AND (CASE WHEN %s = 'L' THEN p.test_txn_yn = 'N' WHEN %s = 'T' THEN p.test_txn_yn = 'Y' ELSE 1=1 END)),0),
    #         COALESCE((SELECT MAX(b.buy_begin_unix) FROM buy_ords b WHERE b.prod_id = %s AND b.buy_strat_type = %s AND b.buy_strat_name = %s AND b.buy_strat_freq = %s AND (CASE WHEN %s = 'L' THEN b.test_txn_yn = 'N' WHEN %s = 'T' THEN b.test_txn_yn = 'Y' ELSE 1=1 END)),0)
    #     )) AS last_buy_strat_dttm
    #   , GREATEST(
    #         COALESCE((SELECT MAX(p.pos_begin_unix) FROM poss p WHERE p.prod_id = %s AND p.buy_strat_type = %s AND p.buy_strat_name = %s AND p.buy_strat_freq = %s AND (CASE WHEN %s = 'L' THEN p.test_txn_yn = 'N' WHEN %s = 'T' THEN p.test_txn_yn = 'Y' ELSE 1=1 END)),0),
    #         COALESCE((SELECT MAX(b.buy_begin_unix) FROM buy_ords b WHERE b.prod_id = %s AND b.buy_strat_type = %s AND b.buy_strat_name = %s AND b.buy_strat_freq = %s AND (CASE WHEN %s = 'L' THEN b.test_txn_yn = 'N' WHEN %s = 'T' THEN b.test_txn_yn = 'Y' ELSE 1=1 END)),0)
    #     ) AS last_buy_strat_unix

    #   , 'N' as needs_recalc_yn
    # FROM poss p 
    # WHERE p.ignore_tf = 0 
    #   AND p.prod_id = %s
    #   AND p.buy_strat_type = %s
    #   AND p.buy_strat_name = %s
    #   AND p.buy_strat_freq = %s
    # """
    
    # if lta:
    #     if lta == 'L':
    #         sql += " AND p.test_txn_yn = 'N'"
    #     elif lta == 'T':
    #         sql += " AND p.test_txn_yn = 'Y'"
        
    # # Create parameter list for the SQL query
    # # Each %s placeholder needs a corresponding parameter
    # params = [
    #     prod_id, prod_id, prod_id,  # For the first three %s placeholders (base_symb, quote_symb, prod_id)
    #     lta, buy_strat_type, buy_strat_name, buy_strat_freq,  # For lta, buy_strat_type, buy_strat_name, buy_strat_freq
        
    #     # For the first subquery (strat_bo_elapsed)
    #     prod_id, buy_strat_type, buy_strat_name, buy_strat_freq,
    #     lta, lta,  # For the CASE statement in the first subquery
        
    #     # For the second subquery (strat_pos_elapsed)
    #     prod_id, buy_strat_type, buy_strat_name, buy_strat_freq,
    #     lta, lta,  # For the CASE statement in the second subquery
        
    #     # For the third subquery (first part of strat_last_elapsed)
    #     prod_id, buy_strat_type, buy_strat_name, buy_strat_freq,
    #     lta, lta,  # For the CASE statement in the third subquery
        
    #     # For the fourth subquery (second part of strat_last_elapsed)
    #     prod_id, buy_strat_type, buy_strat_name, buy_strat_freq,
    #     lta, lta,  # For the CASE statement in the fourth subquery
        
    #     # For the main WHERE clause
    #     prod_id, buy_strat_type, buy_strat_name, buy_strat_freq
    # ]
    
    # # Execute the calculation query with parameters - using always_list_yn='Y' to get dict result
    # result = self.seld(sql, params, always_list_yn='Y')
    # if self.debug_tf: print(f"==> db_trade_strat_perfs_recalc_single() ==> result={result}")

    # if not result:
    #     if self.debug_tf: G(f"🔍 No position data found for {prod_id} {buy_strat_type} {buy_strat_name} {buy_strat_freq} {lta}")
    #     return AttrDict()

    # if isinstance(result, list):
    #     result = result[0]

    # trade_strat_perf = AttrDict(result)

    # trade_strat_perf.last_upd_dttm = dttm_get()
    # trade_strat_perf.last_upd_unix = dttm_unix()
    # trade_strat_perf.needs_recalc_yn = 'N'

    # # Save the calculated performance (SAME AS WORKING PATTERN)
    # self.db_trade_strat_perfs_insupd(trade_strat_perf)

    # return trade_strat_perf

#<=====>#

@narc(1)
def db_trade_strat_perfs_recalc(self, prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_strat_perfs_recalc(prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta})')
    """
    Recalculate strategy performance metrics for a specific strategy
    When lta='' or None, creates all three record types (L, T, A) to ensure comprehensive coverage
    """
    
    # 🔧 CRITICAL FIX: When lta is empty, create all three record types by calling self recursively
    if lta == '' or lta is None:
        if self.debug_tf: G(f"🔄 Creating L, T, and A records for {prod_id} {buy_strat_type} {buy_strat_name} {buy_strat_freq}")
        
        # Create Live record (L)
        live_result = self.db_trade_strat_perfs_recalc(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, 'L')
        
        # Create Test record (T) 
        test_result = self.db_trade_strat_perfs_recalc(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, 'T')
        
        # Create All record (A)
        all_result = self.db_trade_strat_perfs_recalc(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, 'A')
        
        # Return the 'A' (All) record since it contains comprehensive data
        return all_result

#<=====>#

@narc(1)
def db_trade_strat_perfs_insupd(self, trade_strat_perf):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_strat_perfs_insupd(trade_strat_perf={trade_strat_perf})')
    if DictValCheck(trade_strat_perf, ['prod_id', 'buy_strat_type', 'buy_strat_name', 'buy_strat_freq', 'lta']):
        # Use parameterized query instead of string interpolation
        check_sql = """SELECT * FROM trade_strat_perfs 
                        WHERE prod_id = %s 
                        AND buy_strat_type = %s 
                        AND buy_strat_name = %s 
                        AND buy_strat_freq = %s 
                        AND lta = %s"""
        check = self.seld(check_sql, [
            trade_strat_perf.prod_id,
            trade_strat_perf.buy_strat_type,
            trade_strat_perf.buy_strat_name,
            trade_strat_perf.buy_strat_freq,
            trade_strat_perf.lta
        ])
        if check:
            # 🚨 ALWAYS update dlm and dlm_unix on any trade strategy performance update
            trade_strat_perf.dlm = dttm_get()
            trade_strat_perf.dlm_unix = dttm_unix()
            
            where_dict = {}
            where_dict['prod_id'] = trade_strat_perf.prod_id
            where_dict['buy_strat_type'] = trade_strat_perf.buy_strat_type
            where_dict['buy_strat_name'] = trade_strat_perf.buy_strat_name
            where_dict['buy_strat_freq'] = trade_strat_perf.buy_strat_freq
            where_dict['lta'] = trade_strat_perf.lta
            
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(trade_strat_perf)
                    
            self.upd_ez(self.db_name, "trade_strat_perfs", simple_dict, where_dict=where_dict)
            # print(f"✅ Updated trade_strat_perfs for {trade_strat_perf.prod_id} {trade_strat_perf.buy_strat_type} {trade_strat_perf.buy_strat_name} {trade_strat_perf.buy_strat_freq} {trade_strat_perf.lta}")
        else:
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(trade_strat_perf)
                    
            self.insupd_ez(self.db_name, "trade_strat_perfs", simple_dict, validate_columns=True)
            # print(f"✅ Inserted trade_strat_perfs for {trade_strat_perf.prod_id} {trade_strat_perf.buy_strat_type} {trade_strat_perf.buy_strat_name} {trade_strat_perf.buy_strat_freq} {trade_strat_perf.lta}")
    else:
        print(f"🔴 WARNING: trade_strat_perfs_insupd() ==> {trade_strat_perf.get('prod_id')} {trade_strat_perf.get('buy_strat_type')} {trade_strat_perf.get('buy_strat_name')} {trade_strat_perf.get('buy_strat_freq')} {trade_strat_perf.get('lta')} is missing required fields")

#<=====>#

@narc(1)
def trade_strat_perfs_flag_upd(self, prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, lta=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.trade_strat_perfs_flag_upd(prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta})')
    """
    Update strategy performance after a buy operation
    """
    # 🚨 Include timestamp updates in trade strategy performance flag updates
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
