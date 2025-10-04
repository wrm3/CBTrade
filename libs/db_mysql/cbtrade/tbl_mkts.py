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
import traceback

#<=====>#
# Imports - Project
#<=====>#
from libs.common import narc, DictValCheck, dttm_get, dttm_unix
from libs.db_mysql.cbtrade.db_common import to_scalar_dict
from libs.common import AttrDict


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.tbl_mkts'
log_name      = 'cbtrade.tbl_mkts'


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
def db_mkts_exists(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_mkts_exists()')
    """Check if the mkts table exists"""
    sql = '''
        CREATE TABLE IF NOT EXISTS `mkts` (
            `mkt_id` INT AUTO_INCREMENT PRIMARY KEY,
            `mkt_name` VARCHAR(64),
            `prod_id` VARCHAR(64),
            `mkt_venue` VARCHAR(64),
            `base_curr_symb` VARCHAR(64),
            `base_curr_name` VARCHAR(64),
            `base_size_incr` DECIMAL(36, 12),
            `base_size_min` DECIMAL(36, 12),
            `base_size_max` DECIMAL(36, 12),
            `quote_curr_symb` VARCHAR(64),
            `quote_curr_name` VARCHAR(64),
            `quote_size_incr` DECIMAL(36, 12),
            `quote_size_min` DECIMAL(36, 12),
            `quote_size_max` DECIMAL(36, 12),
            `mkt_status_tf` VARCHAR(64),
            `mkt_view_only_tf` TINYINT DEFAULT 0,
            `mkt_watched_tf` TINYINT DEFAULT 0,
            `mkt_is_disabled_tf` TINYINT DEFAULT 0,
            `mkt_new_tf` TINYINT DEFAULT 0,
            `mkt_cancel_only_tf` TINYINT DEFAULT 0,
            `mkt_limit_only_tf` TINYINT DEFAULT 0,
            `mkt_post_only_tf` TINYINT DEFAULT 0,
            `mkt_trading_disabled_tf` TINYINT DEFAULT 0,
            `mkt_auction_mode_tf` TINYINT DEFAULT 0,
            `prc` DECIMAL(36, 12),
            `prc_ask` DECIMAL(36, 12),
            `prc_buy` DECIMAL(36, 12),
            `prc_bid` DECIMAL(36, 12),
            `prc_sell` DECIMAL(36, 12),
            `prc_mid_mkt` DECIMAL(36, 12),
            `prc_pct_chg_24h` DECIMAL(36, 12),
            `vol_24h` DECIMAL(36, 12),
            `vol_base_24h` DECIMAL(36, 12),
            `vol_quote_24h` DECIMAL(36, 12),
            `vol_pct_chg_24h` DECIMAL(36, 12),
            `ignore_tf` TINYINT DEFAULT 0,
            `note1` TEXT,
            `note2` TEXT,
            `note3` TEXT,
            `add_dttm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `add_unix` BIGINT DEFAULT 0,
            `dlm` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `dlm_unix` BIGINT DEFAULT 0,
            UNIQUE KEY `mkts_uk1` (`prod_id`)
        ) ENGINE=InnoDB;
    '''
    return sql

#<=====>#

def db_mkts_trigs(self):
    # mkts
    return [
        "DROP TRIGGER IF EXISTS before_insert_mkts;",
        """
        CREATE TRIGGER before_insert_mkts BEFORE INSERT ON `mkts` FOR EACH ROW
        BEGIN
            SET NEW.add_unix = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
        "DROP TRIGGER IF EXISTS before_update_mkts;",
        """
        CREATE TRIGGER before_update_mkts BEFORE UPDATE ON `mkts` FOR EACH ROW
        BEGIN
            SET NEW.add_unix = COALESCE(UNIX_TIMESTAMP(NEW.add_dttm),0);
            SET NEW.dlm_unix = COALESCE(UNIX_TIMESTAMP(NEW.dlm),0);
        END;
        """,
    ]

#<=====>#

@narc(1)
def db_mkts_get(self, base_symb=None, quote_symb=None, prod_id=None):
    sql = """
    select * 
      from mkts
      where 1=1
      and ignore_tf = 0
    """
    if base_symb:
        sql += f" and base_curr_symb = '{base_symb}' "
    if quote_symb:
        sql += f" and quote_curr_symb = '{quote_symb}' "
    if prod_id:
        sql += f" and prod_id = '{prod_id}' "
    sql += " order by prod_id "
    resp = []
    rows = self.seld(sql, always_list_yn='Y')
    if not rows:
        return resp
    for x in rows:
        resp.append(AttrDict(x))
    return resp

#<=====>#

@narc(1)
def db_mkts_open_cnt_get(self, mkt=None, quote_symb=None, prod_id=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_mkts_open_cnt_get(mkt={mkt}, quote_symb={quote_symb}, prod_id={prod_id})')
    """Get count of open markets by market filter - RESTORED ORIGINAL SIGNATURE"""

    sql = """
    select count(*) as open_cnt 
      from mkts m 
      where m.ignore_tf = 0 
      and m.mkt_status_tf = 'online' 
      and m.mkt_view_only_tf = 0 
      and m.mkt_is_disabled_tf = 0 
      and m.mkt_cancel_only_tf = 0 
      and m.mkt_limit_only_tf = 0 
      and m.mkt_post_only_tf = 0 
      and m.mkt_trading_disabled_tf = 0 
      and m.mkt_auction_mode_tf = 0 
    """
    # Support original calling pattern with mkt parameter
    if mkt:
        sql += f" and m.quote_curr_symb = '{mkt}' "
    if quote_symb:
        sql += f" and m.quote_curr_symb = '{quote_symb}' "
    if prod_id:
        sql += f" and m.prod_id = '{prod_id}' "

    open_cnt_data = self.seld(sql)

    if open_cnt_data:
        if isinstance(open_cnt_data, list):
            open_cnt_data = open_cnt_data[0]
        if isinstance(open_cnt_data, dict):
            open_cnt_data = open_cnt_data['open_cnt']
            return open_cnt_data
    else:
        return 0

#<=====>#

@narc(1)
def db_mkt_prc_get(self, prod_id):
    sql = f"""
    select prc 
      from mkts 
      where prod_id = '{prod_id}'
    """
    prc = self.seld(sql)
    if not prc:
        prc = 0.0
    return float(prc)

#<=====>#

@narc(1)
def db_pairs_loop_top_prc_chg_prod_ids_get(self, lmt=None, pct_min=0, quote_curr_symb=None, min_volume=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_pairs_loop_top_prc_chg_prod_ids_get(lmt={lmt}, pct_min={pct_min}, quote_curr_symb={quote_curr_symb}, min_volume={min_volume})')
    """Get top price change product IDs by 24h percentage change"""

    sql = ""
    sql += " select prod_id "
    sql += "   from mkts m  "
    sql += "   where 1=1  "
    if quote_curr_symb:
        if quote_curr_symb == 'BTC':
            sql += f"  and (quote_curr_symb = 'BTC' OR quote_curr_symb = 'Bitcoin') "
        elif quote_curr_symb == 'ETH':
            sql += f"  and (quote_curr_symb = 'ETH' OR quote_curr_symb = 'Ethereum') "
        elif quote_curr_symb == 'USD':
            sql += f"  and (quote_curr_symb = 'USD' OR quote_curr_symb = 'US Dollar') "
        elif quote_curr_symb == 'USDC':
            sql += f"  and (quote_curr_symb = 'USDC' OR quote_curr_symb = 'USDCoin') "
        else:
            sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
    if min_volume:
        sql += "  and m.vol_quote_24h >= {} ".format(min_volume)
    sql += "   and m.prc_pct_chg_24h > 0 "
    sql += f"   and m.prc_pct_chg_24h > {pct_min} "
    sql += "   and mkt_status_tf             = 'online' "
    sql += "   and mkt_view_only_tf          = 0 "
    sql += "   and mkt_is_disabled_tf        = 0 "
    sql += "   and mkt_cancel_only_tf        = 0 "
    sql += "   and mkt_limit_only_tf         = 0 "
    sql += "   and mkt_post_only_tf          = 0 "
    sql += "   and mkt_trading_disabled_tf   = 0 "
    sql += "   and mkt_auction_mode_tf       = 0 "
    sql += "   order by prc_pct_chg_24h desc "

    if lmt:
        sql += f"  limit {lmt} "

    rows = self.seld(sql, always_list_yn='Y')
    if rows is None:
        return []
    else:
        return [row['prod_id'] for row in rows]

#<=====>#

@narc(1)
def db_pairs_loop_top_vol_chg_prod_ids_get(self, lmt=None, pct_min=0, quote_curr_symb=None, min_volume=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_pairs_loop_top_vol_chg_prod_ids_get(lmt={lmt}, pct_min={pct_min}, quote_curr_symb={quote_curr_symb}, min_volume={min_volume})')
    """Get top volume change product IDs by 24h percentage change"""

    sql = ""
    sql += " select prod_id "
    sql += "   from mkts m  "
    sql += "   where 1=1  "
    if quote_curr_symb:
        if quote_curr_symb == 'BTC':
            sql += f"  and (quote_curr_symb = 'BTC' OR quote_curr_symb = 'Bitcoin') "
        elif quote_curr_symb == 'ETH':
            sql += f"  and (quote_curr_symb = 'ETH' OR quote_curr_symb = 'Ethereum') "
        elif quote_curr_symb == 'USD':
            sql += f"  and (quote_curr_symb = 'USD' OR quote_curr_symb = 'US Dollar') "
        elif quote_curr_symb == 'USDC':
            sql += f"  and (quote_curr_symb = 'USDC' OR quote_curr_symb = 'USD Coin') "
        else:
            sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
    if min_volume:
        sql += "  and m.vol_quote_24h >= {} ".format(min_volume)
    if pct_min:
        sql += f"   and m.vol_pct_chg_24h > {pct_min} "
    else:
        sql += "   and m.vol_pct_chg_24h > 0 "
    sql += "   and mkt_status_tf             = 'online' "
    sql += "   and mkt_view_only_tf          = 0 "
    sql += "   and mkt_is_disabled_tf        = 0 "
    sql += "   and mkt_cancel_only_tf        = 0 "
    sql += "   and mkt_limit_only_tf         = 0 "
    sql += "   and mkt_post_only_tf          = 0 "
    sql += "   and mkt_trading_disabled_tf   = 0 "
    sql += "   and mkt_auction_mode_tf       = 0 "
    sql += "   order by vol_pct_chg_24h desc "

    if lmt:
        sql += f"  limit {lmt} "

    rows = self.seld(sql, always_list_yn='Y')
    
    if rows is None:
        return []
    else:
        return [row['prod_id'] for row in rows]

#<=====>#

@narc(1)
def db_pairs_loop_top_vol_chg_pct_prod_ids_get(self, lmt=None, quote_curr_symb=None, min_volume=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_pairs_loop_top_vol_chg_pct_prod_ids_get(lmt={lmt}, quote_curr_symb={quote_curr_symb}, min_volume={min_volume})')
    """Get top volume change percentage product IDs"""

    sql = ""
    sql += " select prod_id  "
    sql += "   from mkts m "
    sql += "   where 1=1  "
    if quote_curr_symb:
        sql += f"  and quote_curr_symb = '{quote_curr_symb}' "
    if min_volume:
        sql += "  and m.vol_quote_24h >= {} ".format(min_volume)
    sql += "   and mkt_status_tf             = 'online' "
    sql += "   and mkt_view_only_tf          = 0 "
    sql += "   and mkt_is_disabled_tf        = 0 "
    sql += "   and mkt_cancel_only_tf        = 0 "
    sql += "   and mkt_limit_only_tf         = 0 "
    sql += "   and mkt_post_only_tf          = 0 "
    sql += "   and mkt_trading_disabled_tf   = 0 "
    sql += "   and mkt_auction_mode_tf       = 0 "
    sql += "   order by vol_pct_chg_24h desc "

    if lmt:
        sql += "  limit {} ".format(lmt)

    print(f"==> db_pairs_loop_top_vol_chg_pct_prod_ids_get() sql: {sql}")

    rows = self.seld(sql, always_list_yn='Y')

    if rows is None:
        return []
    else:
        return [row['prod_id'] for row in rows]

#<=====>#

@narc(1)
def db_pairs_loop_watched_prod_ids_get(self, quote_curr_symb=None, min_volume=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_pairs_loop_watched_prod_ids_get(quote_curr_symb={quote_curr_symb}, min_volume={min_volume})')
    """Get watched product IDs based on market flags"""

    sql = ""
    sql += " select m.prod_id "
    sql += "   from mkts m "
    sql += "   where m.ignore_tf = 0 "
    if quote_curr_symb:
        if quote_curr_symb == 'BTC':
            sql += f"  and (m.quote_curr_symb = 'BTC' OR m.quote_curr_symb = 'Bitcoin') "
        elif quote_curr_symb == 'ETH':
            sql += f"  and (m.quote_curr_symb = 'ETH' OR m.quote_curr_symb = 'Ethereum') "
        elif quote_curr_symb == 'USD':
            sql += f"  and (m.quote_curr_symb = 'USD' OR m.quote_curr_symb = 'US Dollar') "
        elif quote_curr_symb == 'USDC':
            sql += f"  and (m.quote_curr_symb = 'USDC' OR m.quote_curr_symb = 'USD Coin') "
        else:
            sql += f"  and m.quote_curr_symb = '{quote_curr_symb}' "
    if min_volume:
        sql += "  and m.vol_quote_24h >= {} ".format(min_volume)
    sql += "   and m.mkt_watched_tf = 1 "
    sql += "   order by m.prod_id "

    rows = self.seld(sql, always_list_yn='Y')

    if rows is None:
        return []
    else:
        return [row['prod_id'] for row in rows]

#<=====>#

@narc(1)
def db_pairs_loop_get(self, mode='full', loop_pairs=None, stable_pairs=None, err_pairs=None, quote_curr_symb=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_pairs_loop_get(mode={mode}, loop_pairs={loop_pairs}, stable_pairs={stable_pairs}, err_pairs={err_pairs}, quote_curr_symb={quote_curr_symb})')
    sql = """
    select distinct m.mkt_id 
      , m.mkt_name 
      , m.prod_id 
      , m.prc 
      , m.prc_ask 
      , m.prc_buy 
      , m.prc_bid 
      , m.prc_sell 
      , m.prc_mid_mkt 
      , m.prc_pct_chg_24h 
      , m.vol_24h 
      , m.vol_base_24h 
      , m.vol_quote_24h 
      , m.vol_pct_chg_24h 

      , coalesce(tp.tot_cnt, 0) as tot_cnt 
      , coalesce(tp.win_cnt, 0) as win_cnt 
      , coalesce(tp.lose_cnt, 0) as lose_cnt 
      , coalesce(tp.win_pct, 0) as win_pct 
      , coalesce(tp.lose_pct, 0) as lose_pct 
      , coalesce(tp.tot_in_cnt, 0) as tot_in_cnt 
      , coalesce(tp.buy_fees_cnt, 0) as buy_fees_cnt 
      , coalesce(tp.sell_fees_cnt_tot, 0) as sell_fees_cnt_tot 
      , coalesce(tp.fees_cnt_tot, 0) as fees_cnt_tot 
      , coalesce(tp.buy_cnt, 0) as buy_cnt 
      , coalesce(tp.sell_cnt_tot, 0) as sell_cnt_tot 
      , coalesce(tp.hold_cnt, 0) as hold_cnt 
      , coalesce(tp.pocket_cnt, 0) as pocket_cnt 
      , coalesce(tp.clip_cnt, 0) as clip_cnt 
      , coalesce(tp.sell_order_cnt, 0) as sell_order_cnt 
      , coalesce(tp.sell_order_attempt_cnt, 0) as sell_order_attempt_cnt 
      , coalesce(tp.val_curr, 0) as val_curr 
      , coalesce(tp.val_tot, 0) as val_tot 
      , coalesce(tp.win_amt, 0) as win_amt 
      , coalesce(tp.lose_amt, 0) as lose_amt 
      , coalesce(tp.gain_loss_amt, 0) as gain_loss_amt 
      , coalesce(tp.gain_loss_amt_net, 0) as gain_loss_amt_net 
      , coalesce(tp.gain_loss_pct, 0) as gain_loss_pct 
      , coalesce(tp.gain_loss_pct_hr, 0) as gain_loss_pct_hr 

      , m.base_curr_symb 
      , m.base_curr_name 
      , m.base_size_incr 
      , m.base_size_min 
      , m.base_size_max 

      , m.quote_curr_symb 
      , m.quote_curr_name 
      , m.quote_size_incr 
      , m.quote_size_min 
      , m.quote_size_max 
      , m.mkt_status_tf 

      , m.mkt_view_only_tf 
      , m.mkt_watched_tf 
      , m.mkt_is_disabled_tf 
      , m.mkt_new_tf 
      , m.mkt_cancel_only_tf 
      , m.mkt_limit_only_tf 
      , m.mkt_post_only_tf 
      , m.mkt_trading_disabled_tf 
      , m.mkt_auction_mode_tf 

      , mc.buy_check_dttm 
      , mc.sell_check_dttm 
      , mc.buy_check_unix 
      , mc.sell_check_unix 

      , m.note1 
      , m.note2 
      , m.note3 
      , m.add_dttm 
      , m.dlm 

      , coalesce( floor( (unix_timestamp() - coalesce(tp.last_upd_unix,0)) / 60 ), 9999) as age_mins 
      , coalesce( (unix_timestamp() - coalesce(tp.last_upd_unix,0)) / 3600.0, 9999) as age_hours 

      from mkts m 
      left outer join trade_perfs tp on tp.prod_id = m.prod_id and tp.lta = 'A' 
      left outer join mkt_checks mc on mc.prod_id = m.prod_id 
      where m.ignore_tf = 0 
      and m.mkt_status_tf = 'online' 
      and m.mkt_view_only_tf = 0 
      and m.mkt_is_disabled_tf = 0 
      and m.mkt_cancel_only_tf = 0 
      and m.mkt_post_only_tf = 0 
      and m.mkt_trading_disabled_tf = 0 
      and m.mkt_auction_mode_tf = 0 
    """
    
    if quote_curr_symb:
        sql += f"  and m.quote_curr_symb = '{quote_curr_symb}' "
    sql += "  and m.mkt_limit_only_tf = 0 "
    if loop_pairs:
        loop_pairs_str = "'" + "', '".join(loop_pairs) + "'"
        sql += "   and m.prod_id in ({}) ".format(loop_pairs_str)
    if stable_pairs:
        stable_pairs_str = "'" + "', '".join(stable_pairs) + "'"
        sql += "   and m.prod_id not in ({}) ".format(stable_pairs_str)
    if err_pairs:
        err_pairs_str = "'" + "', '".join(err_pairs) + "'"
        sql += "   and m.prod_id not in ({}) ".format(err_pairs_str)

    if mode == 'sell':
        sql += "   order by (select sum(p.tot_out_cnt) from poss p where p.prod_id = m.prod_id and p.pos_stat = 'OPEN') desc "
    else:
        sql += "   order by coalesce(tp.gain_loss_pct_hr, 0) desc "

    mkts = self.seld(sql)

    return mkts

#<=====>#

@narc(1)
def db_mkts_insupd(self, in_data):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_mkts_insupd(in_data={in_data})')
    if DictValCheck(in_data, ['prod_id']):
        # Use parameterized query instead of string interpolation
        check_sql = "SELECT * FROM mkts WHERE prod_id = %s"
        check = self.seld(check_sql, [in_data.prod_id])
        if check:
            # 🚨 ALWAYS update dlm and dlm_unix on any market update
            in_data.dlm = dttm_get()
            in_data.dlm_unix = dttm_unix()
            
            where_dict = {}
            where_dict['prod_id'] = in_data.prod_id
            
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(in_data)
                    
            self.upd_ez(self.db_name, "mkts", simple_dict, where_dict=where_dict)
            # print(f"✅ Updated mkts for {in_data.prod_id}")
        else:
            # Convert to simple dictionary with only scalar values
            simple_dict = to_scalar_dict(in_data)
                    
            self.insupd_ez(self.db_name, "mkts", simple_dict, validate_columns=True)
            # print(f"✅ Inserted mkts for {in_data.prod_id}")
    else:
        print(in_data)
        traceback.print_stack()
        print(f"🔴 WARNING: db_mkts_insupd() ==> {in_data.prod_id} is missing required fields")

#<=====>#
