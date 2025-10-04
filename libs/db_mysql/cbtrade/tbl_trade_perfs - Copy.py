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
            `bo_elapsed` DECIMAL(36,12) DEFAULT 9999.0,
            `pos_elapsed` DECIMAL(36,12) DEFAULT 9999.0,
            `last_elapsed` DECIMAL(36,12) DEFAULT 9999.0,
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
def db_trade_perfs_get(self, base_symb:str=None, quote_symb:str=None, prod_id:str=None, lta:str=None, min_trades:int=0, force_recalc:bool=False):
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
            
            # Apply the same pattern as trade_strat_perfs: refresh if older than 24 hours OR if data is empty
            if trade_perf.age_hours > 24 or trade_perf.tot_cnt == 0:
                print(f"🔄 Trade performance is stale ({trade_perf.age_hours:.1f}h old), recalculating...")
                # Trigger recalculation for the specific L/T/A row we are inspecting
                fresh_perf = self.db_trade_perfs_recalc(trade_perf.prod_id, trade_perf.lta)
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

    time.sleep(0.5)

    sql_str1 = ""
    sql_str2 = ""
    if lta:
        if lta == 'L':
            sql_str1 = """
              and p.test_txn_yn = 'N'
            """
            sql_str2 = """
              and b.test_txn_yn = 'N'
            """
        elif lta == 'T':
            sql_str1 = """
              and p.test_txn_yn = 'Y'
            """
            sql_str2 = """
              and b.test_txn_yn = 'Y'
            """

    # Build SQL query using the EXACT SAME PATTERN as working db_trade_strat_perfs_recalc
    sql = f"""
    SELECT SUBSTRING_INDEX(prod_id, '-', 1) as base_symb
      , SUBSTRING_INDEX(prod_id, '-', -1) as quote_symb
      , '{prod_id}' as prod_id

      , '{lta}' as lta

      , NOW() as last_upd_dttm
      , UNIX_TIMESTAMP() as last_upd_unix

      , count(p.pos_id) as tot_cnt
      , sum(case when p.pos_stat in ('OPEN','SELL') then 1 else 0 end) as tot_open_cnt
      , sum(case when p.pos_stat = 'CLOSE' then 1 else 0 end) as tot_close_cnt

      , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt
      , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt and p.pos_stat in ('OPEN','SELL') then 1 else 0 end) as win_open_cnt
      , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt and p.pos_stat = 'CLOSE' then 1 else 0 end) as win_close_cnt

      , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt
      , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt and p.pos_stat in ('OPEN','SELL') then 1 else 0 end) as lose_open_cnt
      , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt and p.pos_stat = 'CLOSE' then 1 else 0 end) as lose_close_cnt

      , round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 2) as win_pct
      , round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 2) as win_open_pct
      , round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 2) as win_close_pct

      , round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 2) as lose_pct
      , round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 2) as lose_open_pct
      , round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) * 100.0 / count(p.pos_id), 2) as lose_close_pct

      , sum(p.age_mins) as age_mins
      , round(sum(p.age_mins) / 60.0, 2) as age_hours

      , round(sum(p.tot_out_cnt), 2) as tot_out_cnt
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end), 2) as tot_out_open_cnt
      , round(sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end), 2) as tot_out_close_cnt

      , round(sum(p.tot_in_cnt), 2) as tot_in_cnt
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_in_cnt else 0 end), 2) as tot_in_open_cnt
      , round(sum(case when p.pos_stat = 'CLOSE' then p.tot_in_cnt else 0 end), 2) as tot_in_close_cnt

      , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.buy_fees_cnt else 0 end), 2) as buy_fees_open_cnt
      , round(sum(case when p.pos_stat = 'CLOSE' then p.buy_fees_cnt else 0 end), 2) as buy_fees_close_cnt

      , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.sell_fees_cnt_tot else 0 end), 2) as sell_fees_open_cnt_tot
      , round(sum(case when p.pos_stat = 'CLOSE' then p.sell_fees_cnt_tot else 0 end), 2) as sell_fees_close_cnt_tot

      , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.fees_cnt_tot else 0 end), 2) as fees_open_cnt_tot
      , round(sum(case when p.pos_stat = 'CLOSE' then p.fees_cnt_tot else 0 end), 2) as fees_close_cnt_tot

      , round(sum(p.buy_cnt), 2) as buy_cnt
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.buy_cnt else 0 end), 2) as buy_open_cnt
      , round(sum(case when p.pos_stat = 'CLOSE' then p.buy_cnt else 0 end), 2) as buy_close_cnt

      , round(sum(p.sell_cnt_tot), 2) as sell_cnt_tot
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.sell_cnt_tot else 0 end), 2) as sell_open_cnt_tot
      , round(sum(case when p.pos_stat = 'CLOSE' then p.sell_cnt_tot else 0 end), 2) as sell_close_cnt_tot

      , round(sum(p.hold_cnt), 2) as hold_cnt
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.hold_cnt else 0 end), 2) as hold_open_cnt
      , round(sum(case when p.pos_stat = 'CLOSE' then p.hold_cnt else 0 end), 2) as hold_close_cnt

      , round(sum(p.pocket_cnt), 2) as pocket_cnt
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.pocket_cnt else 0 end), 2) as pocket_open_cnt
      , round(sum(case when p.pos_stat = 'CLOSE' then p.pocket_cnt else 0 end), 2) as pocket_close_cnt

      , round(sum(p.clip_cnt), 2) as clip_cnt
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.clip_cnt else 0 end), 2) as clip_open_cnt
      , round(sum(case when p.pos_stat = 'CLOSE' then p.clip_cnt else 0 end), 2) as clip_close_cnt

      , sum(p.sell_order_cnt) as sell_order_cnt
      , sum(case when p.pos_stat in ('OPEN','SELL') then p.sell_order_cnt else 0 end) as sell_order_open_cnt
      , sum(case when p.pos_stat = 'CLOSE' then p.sell_order_cnt else 0 end) as sell_order_close_cnt
      , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt
      , sum(case when p.pos_stat in ('OPEN','SELL') then p.sell_order_attempt_cnt else 0 end) as sell_order_attempt_open_cnt
      , sum(case when p.pos_stat = 'CLOSE' then p.sell_order_attempt_cnt else 0 end) as sell_order_attempt_close_cnt

      , round(sum(p.val_curr), 2) as val_curr
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.val_curr else 0 end), 2) as val_open_curr
      , round(sum(case when p.pos_stat = 'CLOSE' then p.val_curr else 0 end), 2) as val_close_curr
      , round(sum(p.val_tot), 2) as val_tot
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.val_tot else 0 end), 2) as val_open_tot
      , round(sum(case when p.pos_stat = 'CLOSE' then p.val_tot else 0 end), 2) as val_close_tot
      
      , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then p.val_tot else 0 end) as win_amt
      , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt and p.pos_stat in ('OPEN','SELL') then p.val_tot else 0 end) as win_open_amt
      , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt and p.pos_stat = 'CLOSE' then p.val_tot else 0 end) as win_close_amt

      , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_amt
      , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt and p.pos_stat in ('OPEN','SELL') then 1 else 0 end) as lose_open_amt
      , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt and p.pos_stat = 'CLOSE' then 1 else 0 end) as lose_close_amt

      , round(sum(p.gain_loss_amt), 2) as gain_loss_amt
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end), 2) as gain_loss_open_amt
      , round(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end), 2) as gain_loss_close_amt

      , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt_net else 0 end), 2) as gain_loss_open_amt_net
      , round(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt_net else 0 end), 2) as gain_loss_close_amt_net

      , round(sum(p.gain_loss_amt) * 100.0 / sum(p.tot_out_cnt), 4) as gain_loss_pct
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end), 4) as gain_loss_open_pct
      , round(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end), 4) as gain_loss_close_pct

      , round(sum(p.gain_loss_amt) * 100.0 / sum(p.tot_out_cnt), 4) as gain_loss_pct
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end), 4) as gain_loss_open_pct
      , round(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end), 4) as gain_loss_close_pct

      , round(sum(p.gain_loss_amt) * 100.0 / sum(p.tot_out_cnt) / (sum(p.age_mins) / 60.0), 8) as gain_loss_pct_hr
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end) / (sum(p.age_mins) / 60.0), 8) as gain_loss_open_pct_hr
      , round(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end) / (sum(p.age_mins) / 60.0), 8) as gain_loss_close_pct_hr

      , round(sum(p.gain_loss_amt) * 100.0 / sum(p.tot_out_cnt) / (sum(p.age_mins) / 60.0) * 24, 8) as gain_loss_pct_day
      , round(sum(case when p.pos_stat in ('OPEN','SELL') then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat in ('OPEN','SELL') then p.tot_out_cnt else 0 end) / (sum(p.age_mins) / 60.0) * 24, 8) as gain_loss_open_pct_day
      , round(sum(case when p.pos_stat = 'CLOSE' then p.gain_loss_amt else 0 end) * 100.0 / sum(case when p.pos_stat = 'CLOSE' then p.tot_out_cnt else 0 end) / (sum(p.age_mins) / 60.0) * 24, 8) as gain_loss_close_pct_day

      , UNIX_TIMESTAMP() - coalesce(
                                        (select max(b.buy_begin_unix) 
                                            from buy_ords b 
                                            where b.prod_id = '{prod_id}' 
                                            {sql_str2}
                                            )
                                        , 0) as bo_elapsed
      , UNIX_TIMESTAMP() - coalesce(
                                        (select max(p.pos_begin_unix) 
                                            from poss p 
                                            where p.prod_id = '{prod_id}' 
                                            {sql_str1}
                                            )
                                        , 0) as pos_elapsed
      , UNIX_TIMESTAMP() - GREATEST(
                                        COALESCE(
                                            (SELECT MAX(p.pos_begin_unix) 
                                             FROM poss p 
                                             WHERE p.prod_id = '{prod_id}' 
                                             {sql_str1}), 
                                            0
                                        ), 
                                        COALESCE(
                                            (SELECT MAX(b.buy_begin_unix) 
                                             FROM buy_ords b 
                                             WHERE b.prod_id = '{prod_id}' 
                                             {sql_str2}), 
                                            0
                                        )
                                    ) as last_elapsed

    FROM poss p 
    WHERE p.ignore_tf = 0 
      AND p.prod_id = '{prod_id}'
    """
    
    if lta:
        if lta == 'L':
            sql += " AND p.test_txn_yn = 'N'"
        elif lta == 'T':
            sql += " AND p.test_txn_yn = 'Y'"
        # For 'A' or None, include all rows (no filter)
        
    # print(sql)

    # Execute the calculation query (SAME AS WORKING db_trade_strat_perfs_recalc)
    result = self.seld(sql, always_list_yn='Y')
    
    if not result:
        print(f"🔍 No position data found for {prod_id} {lta}")
        return AttrDict()

    if isinstance(result, list):
        result = result[0]

    trade_perf = AttrDict(result)

    trade_perf.last_upd_dttm = dttm_get()
    trade_perf.last_upd_unix = dttm_unix()
    trade_perf.needs_recalc_yn = 'N'

    # Save the calculated performance (SAME AS WORKING PATTERN)
    self.db_trade_perfs_insupd(trade_perf)

    print(f"✅ Calculated trade_perf for {prod_id} {lta}")
    return trade_perf

#<=====>#

@narc(1)
def db_trade_perfs_recalc(self, prod_id, lta=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_trade_perfs_recalc(prod_id={prod_id}, lta={lta})')
    """
    Recalculate trade performance metrics for a specific product
    When lta='' or None, creates all three record types (L, T, A) to ensure comprehensive coverage
    """
    
    # 🔧 CRITICAL FIX: When lta is empty, create all three record types (L, T, A)
    if lta == '' or lta is None:
        print(f"🔄 Creating L, T, and A records for {prod_id}")
        
        # Create Live record (L)
        live_result = self.db_trade_perfs_recalc_single(prod_id, 'L')
        self.db_trade_perfs_insupd(live_result)

        # Create Test record (T)
        test_result = self.db_trade_perfs_recalc_single(prod_id, 'T')
        self.db_trade_perfs_insupd(test_result)
        
        # Create All record (A)
        all_result = self.db_trade_perfs_recalc_single(prod_id, 'A')
        self.db_trade_perfs_insupd(all_result)

        # Return the 'A' (All) record since it contains comprehensive data
        return all_result

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

