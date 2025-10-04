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


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.db_reports'
log_name      = 'cbtrade.db_reports'


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

# def db_open_overview(self):
#     """Get overview of outstanding (open) positions"""
#     sql = """
#     select p.quote_curr_symb as symb
#       , p.test_txn_yn
#       , count(*) as closed
#       , sum(case when p.gain_loss_amt > 0 then 1 else 0 end) as close_win_cnt
#       , sum(case when p.gain_loss_amt <= 0 then 1 else 0 end) as close_loss_cnt
#       , sum(p.tot_out_cnt) as close_spent
#       , sum(case when p.gain_loss_amt > 0 then p.tot_out_cnt else 0 end) as close_win_spent
#       , sum(case when p.gain_loss_amt <= 0 then p.tot_out_cnt else 0 end) as close_loss_spent
#       , sum(p.gain_loss_amt) as close_gain_loss
#       , sum(case when p.gain_loss_amt > 0 then p.gain_loss_amt else 0 end) as close_gains
#       , sum(case when p.gain_loss_amt <= 0 then p.gain_loss_amt else 0 end) as close_losses
#       from poss p
#       where 1=1
#       and p.ignore_tf = 0
#       and p.pos_stat in ('OPEN','SELL')
#       group by p.quote_curr_symb, p.test_txn_yn
#     """
#     out_ovrs = self.seld(sql)
#     return out_ovrs

#<=====>#

# def db_closed_overview(self):
#     """Get overview of closed positions"""
#     sql = """
#     select p.quote_curr_symb as symb
#       , p.test_txn_yn
#       , count(*) as closed
#       , sum(case when p.gain_loss_amt > 0 then 1 else 0 end) as close_win_cnt
#       , sum(case when p.gain_loss_amt <= 0 then 1 else 0 end) as close_loss_cnt
#       , sum(p.tot_out_cnt) as close_spent
#       , sum(case when p.gain_loss_amt > 0 then p.tot_out_cnt else 0 end) as close_win_spent
#       , sum(case when p.gain_loss_amt <= 0 then p.tot_out_cnt else 0 end) as close_loss_spent
#       , sum(p.gain_loss_amt) as close_gain_loss
#       , sum(case when p.gain_loss_amt > 0 then p.gain_loss_amt else 0 end) as close_gains
#       , sum(case when p.gain_loss_amt <= 0 then p.gain_loss_amt else 0 end) as close_losses
#       from poss p
#       where 1=1
#       and p.ignore_tf = 0
#       and p.pos_stat not in ('OPEN','SELL')
#       group by p.quote_curr_symb, p.test_txn_yn
#     """
#     out_ovrs = self.seld(sql)
#     return out_ovrs

#<=====>#

@narc(1)
def db_closed_overview_recent_test(self, base_symb=None, quote_symb=None, prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None, lta=None, cnt=15):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_closed_overview_recent_test(base_symb={base_symb}, quote_symb={quote_symb}, prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta}, cnt={cnt})')

    """Get daily breakdown of recently closed TEST positions (last 7 days)"""
    sql = """
    select DATE(p.pos_end_dttm) as close_date
      , p.quote_curr_symb as symb
      , p.test_txn_yn
      , count(*) as closed
      , sum(case when p.gain_loss_amt > 0 then 1 else 0 end) as close_win_cnt
      , sum(case when p.gain_loss_amt <= 0 then 1 else 0 end) as close_loss_cnt
      , sum(p.tot_out_cnt) as close_spent
      , sum(case when p.gain_loss_amt > 0 then p.tot_out_cnt else 0 end) as close_win_spent
      , sum(case when p.gain_loss_amt <= 0 then p.tot_out_cnt else 0 end) as close_loss_spent
      , sum(p.gain_loss_amt) as close_gain_loss
      , sum(case when p.gain_loss_amt > 0 then p.gain_loss_amt else 0 end) as close_gains
      , sum(case when p.gain_loss_amt <= 0 then p.gain_loss_amt else 0 end) as close_losses
      from poss p
      where 1=1
      and p.pos_stat not in ('OPEN','SELL')
      and p.ignore_tf = 0
      and p.pos_end_dttm >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    """
    if base_symb:
        sql += f" and p.base_curr_symb = '{base_symb}' "
    if quote_symb:
        sql += f" and p.quote_curr_symb = '{quote_symb}' "
    if prod_id:
        sql += f" and p.prod_id = '{prod_id}' "
    if buy_strat_type:
        sql += f" and p.buy_strat_type = '{buy_strat_type}' "
    if buy_strat_name:
        sql += f" and p.buy_strat_name = '{buy_strat_name}' "
    if buy_strat_freq:
        sql += f" and p.buy_strat_freq = '{buy_strat_freq}' "
    sql += " and p.test_txn_yn = 'Y' "

    sql += " group by DATE(p.pos_end_dttm), p.quote_curr_symb "
    sql += " order by DATE(p.pos_end_dttm) DESC, p.quote_curr_symb "

    if cnt:
        sql += f" limit {cnt} "

    out_ovrs = self.seld(sql, always_list_yn='Y')
    return out_ovrs

#<=====>#

@narc(1)
def db_closed_overview_recent_live(self, base_symb=None, quote_symb=None, prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None, lta=None, cnt=15):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_closed_overview_recent_live(base_symb={base_symb}, quote_symb={quote_symb}, prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta}, cnt={cnt})')
    """Get daily breakdown of recently closed LIVE positions (last 7 days)"""
    sql = """
    select DATE(p.pos_end_dttm) as close_date
      , p.quote_curr_symb as symb
      , p.test_txn_yn
      , count(*) as closed
      , sum(case when p.gain_loss_amt > 0 then 1 else 0 end) as close_win_cnt
      , sum(case when p.gain_loss_amt <= 0 then 1 else 0 end) as close_loss_cnt
      , sum(p.tot_out_cnt) as close_spent
      , sum(case when p.gain_loss_amt > 0 then p.tot_out_cnt else 0 end) as close_win_spent
      , sum(case when p.gain_loss_amt <= 0 then p.tot_out_cnt else 0 end) as close_loss_spent
      , sum(p.gain_loss_amt) as close_gain_loss
      , sum(case when p.gain_loss_amt > 0 then p.gain_loss_amt else 0 end) as close_gains
      , sum(case when p.gain_loss_amt <= 0 then p.gain_loss_amt else 0 end) as close_losses
      from poss p
      where 1=1
      and p.pos_stat not in ('OPEN','SELL')
      and p.ignore_tf = 0
      and p.test_txn_yn = 'N'
      and p.pos_end_dttm >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    """
    if base_symb:
        sql += f" and p.base_curr_symb = '{base_symb}' "
    if quote_symb:
        sql += f" and p.quote_curr_symb = '{quote_symb}' "
    if prod_id:
        sql += f" and p.prod_id = '{prod_id}' "
    if buy_strat_type:
        sql += f" and p.buy_strat_type = '{buy_strat_type}' "

    if buy_strat_name:
        sql += f" and p.buy_strat_name = '{buy_strat_name}' "
    if buy_strat_freq:
        sql += f" and p.buy_strat_freq = '{buy_strat_freq}' "
    sql += " and p.test_txn_yn = 'N' "

    sql += " group by DATE(p.pos_end_dttm), p.quote_curr_symb "
    sql += " order by DATE(p.pos_end_dttm) DESC, p.quote_curr_symb "

    if cnt:
        sql += f" limit {cnt} "

    out_ovrs = self.seld(sql, always_list_yn='Y')
    # print(out_ovrs)
    return out_ovrs

#<=====>#

@narc(1)
def db_strats_w_stats_get_all(self):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_strats_w_stats_get_all()')
    """Get all strategies with comprehensive statistics"""
    sql = ""
    sql += " select p.buy_strat_type "
    sql += "   , p.buy_strat_name "
    sql += "   , p.buy_strat_freq "
    sql += "   , count(*) as cnt "
    sql += "  from poss p "
    sql += "  where 1=1 "
    sql += "  and ignore_tf = 0 "
    sql += "  group by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
    sql += "  order by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
    strats = self.seld(sql)
    return strats

#<=====>#

@narc(1)
def db_strats_perf_get_all(self, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_strats_perf_get_all(buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq})')
    """Get performance metrics for all strategies with optional filtering"""
    sql = "select p.prod_id as mkt "
    sql += "  , p.pos_stat "
    sql += "  , sum(case when p.gain_loss_amt > 0 then 1 else 0 end)                         as win_cnt "
    sql += "  , sum(case when p.gain_loss_amt <= 0 then 1 else 0 end)                        as loss_cnt "
    sql += "  , sum(p.sell_order_cnt)                                                        as sell_cnt "
    sql += "  , sum(p.sell_order_attempt_cnt)                                                as sell_attempts "
    sql += "  , round(sum(p.tot_out_cnt),2)                                                  as spent_amt "
    sql += "  , round(sum(p.tot_in_cnt),2)                                                   as recv_amt "
    sql += "  , round(sum(case when p.gain_loss_amt > 0  then p.gain_loss_amt else 0 end),2) as win_amt "
    sql += "  , round(sum(case when p.gain_loss_amt <= 0 then p.gain_loss_amt else 0 end),2) as loss_amt "
    sql += "  , sum(p.hold_cnt)                                                              as hold_cnt "
    sql += "  , round(sum(p.hold_cnt) * m.prc,2)                                             as hold_amt "
    sql += "  , sum(p.pocket_cnt)                                                            as pocket_cnt "
    sql += "  , round(sum(p.pocket_cnt) * m.prc,2)                                           as pocket_amt "
    sql += "  , sum(p.clip_cnt)                                                              as clip_cnt "
    sql += "  , round(sum(p.clip_cnt) * m.prc,2)                                             as clip_amt "
    sql += "  , round(sum(p.val_curr),2)                                                     as val_curr "
    sql += "  , round(sum(p.val_tot),2)                                                      as val_tot "
    sql += "  , round(sum(p.buy_fees_cnt),2)                                                 as fees_buy "
    sql += "  , round(sum(p.sell_fees_cnt_tot),2)                                            as fees_sell "
    sql += "  , round(sum(p.fees_cnt_tot),2)                                                 as fees_tot "
    sql += "  , round(sum(p.gain_loss_amt),2)                                                as gain_loss_amt "
    sql += "  , round(sum(p.gain_loss_amt_est_high),2)                                       as gain_loss_amt_est_high "
    sql += "  from poss p "
    sql += "  join mkts m on m.prod_id = p.prod_id "
    sql += "  where 1=1 "
    sql += "  and p.ignore_tf = 0 "
    if buy_strat_type:
        sql += f"  and p.buy_strat_type = '{buy_strat_type}' "
    if buy_strat_name:
        sql += f"  and p.buy_strat_name = '{buy_strat_name}' "
    if buy_strat_freq:
        sql += f"  and p.buy_strat_freq = '{buy_strat_freq}' "
    sql += "  group by p.prod_id, p.pos_stat  "
    sql += "  order by p.prod_id, p.pos_stat desc "

    mkts = self.seld(sql)
    return mkts

#<=====>#

@narc(1)
def db_poss_open_recent_get(self, lmt=None, test_yn='N'):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_poss_open_recent_get(lmt={lmt}, test_yn={test_yn})')
    """Get recent open positions with optional limit"""
    sql = ""
    sql += " select p.* "
    sql += " from poss p "
    sql += " where p.pos_stat in ('OPEN', 'SELL') "
    sql += " and p.ignore_tf = 0 "
    if test_yn == 'N':
        sql += " and p.test_txn_yn = 'N' "
    elif test_yn == 'Y':
        sql += " and p.test_txn_yn = 'Y' "
    sql += " order by p.pos_begin_dttm desc "
    if lmt:
        sql += f" limit {lmt} "

    poss_data = self.seld(sql)
    return poss_data

#<=====>#

@narc(1)
def db_poss_closed_recent_get(self, base_symb=None, quote_symb=None, prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None, lta=None, lmt=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_poss_closed_recent_get(base_symb={base_symb}, quote_symb={quote_symb}, prod_id={prod_id}, buy_strat_type={buy_strat_type}, buy_strat_name={buy_strat_name}, buy_strat_freq={buy_strat_freq}, lta={lta}, lmt={lmt})')
    """Get recent closed positions with optional limit"""

    if lta:
        if lta in ('Y','N'):
            if lta == 'Y':
                lta = 'T'
            elif lta == 'N':
                lta = 'L'

    sql = ""
    sql += " select p.* "
    sql += " from poss p "
    sql += " where p.pos_stat = 'CLOSE' "
    sql += " and p.ignore_tf = 0 "
    if base_symb:
        sql += f" and p.base_curr_symb = '{base_symb}' "
    if quote_symb:
        sql += f" and p.quote_curr_symb = '{quote_symb}' "
    if prod_id:
        sql += f" and p.prod_id = '{prod_id}' "
    if buy_strat_type:
        sql += f" and p.buy_strat_type = '{buy_strat_type}' "
    if buy_strat_name:
        sql += f" and p.buy_strat_name = '{buy_strat_name}' "
    if buy_strat_freq:
        sql += f" and p.buy_strat_freq = '{buy_strat_freq}' "
    if lta == 'L':
        sql += " and p.test_txn_yn = 'N' "
    elif lta == 'T':
        sql += " and p.test_txn_yn = 'Y' "
    sql += " order by p.pos_end_dttm desc "
    if lmt:
        sql += f" limit {lmt} "

    poss_data = self.seld(sql)
    return poss_data

#<=====>#

@narc(1)
def db_poss_open_get(self, base_symb=None, quote_symb=None, prod_id=None, test_only_yn='N', live_only_yn='N'):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_poss_open_get(base_symb={base_symb}, quote_symb={quote_symb}, prod_id={prod_id}, test_only_yn={test_only_yn}, live_only_yn={live_only_yn})')
    """Get open positions with filtering options"""

    sql = ""
    sql += " select p.* "
    sql += " from poss p "
    sql += " where p.pos_stat in ('OPEN', 'SELL') "
    sql += " and p.ignore_tf = 0 "
    
    if base_symb:
        sql += f" and p.base_curr_symb = '{base_symb}' "
    
    if quote_symb:
        sql += f" and p.quote_curr_symb = '{quote_symb}' "
    
    if prod_id:
        sql += f" and p.prod_id = '{prod_id}' "
    
    if test_only_yn == 'Y':
        sql += " and p.test_txn_yn = 'Y' "
    elif live_only_yn == 'Y':
        sql += " and p.test_txn_yn = 'N' "
    
    sql += " order by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_id asc "

    poss_data = self.seld(sql)
    return poss_data

#<=====>#
