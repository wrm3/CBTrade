#<=====>#
# Description
#<=====>#


#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Public
#<=====>#
import time
from fstrent_colors import G


#<=====>#
# Imports - Project
#<=====>#
from libs.common import (
    AttrDict
    , AttrDictConv
    , dttm_get
    , dttm_unix
    , get_unix_timestamp
    , narc
)


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.db_read'
log_name      = 'cbtrade.db_read'


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
def db_sell_ords_problems_get(self, prod_id=None):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_sell_ords_problems_get(prod_id={prod_id})')
    """Get positions with sell order problems"""

    sql = """
        WITH SellOrderStats AS (
            SELECT 
                pos_id, 
                COUNT(*) AS sell_order_count 
            FROM sell_ords
            GROUP BY pos_id
        )
        SELECT 
            'pos.pos_stat = OPEN but there is a sell order(s) on sell_ords' AS reason,
            p.pos_id, 
            p.prod_id, 
            p.pos_stat, 
            p.test_txn_yn, 
            so.so_id
        FROM poss p
        LEFT JOIN sell_ords so ON so.pos_id = p.pos_id
        LEFT JOIN SellOrderStats sos ON p.pos_id = sos.pos_id
        WHERE p.ignore_tf = 0 
        AND p.pos_stat = 'OPEN' 
        AND sos.sell_order_count > 0

        UNION ALL

        SELECT 
            'multiple sell orders' AS reason,
            p.pos_id, 
            p.prod_id, 
            p.pos_stat, 
            p.test_txn_yn, 
            so.so_id
        FROM poss p
        LEFT JOIN sell_ords so ON so.pos_id = p.pos_id
        LEFT JOIN SellOrderStats sos ON p.pos_id = sos.pos_id
        WHERE p.ignore_tf = 0 
        AND sos.sell_order_count > 1;
        """

    problems_data = self.seld(sql)
    return problems_data
        
#<=====>#

@narc(1)
def db_sell_double_check(self, pos_id):
    if self.debug_tf: G(f'==> CBTRADE_DB.db_sell_double_check(pos_id={pos_id})')
    """Double check sell order status for a position"""
    sql = ""
    sql += " select p.pos_stat "
    sql += "   , so.so_id "
    sql += "  from poss p "
    sql += "  left outer join sell_ords so on so.pos_id = p.pos_id "
    sql += "  where 1=1 "
    sql += f" and p.pos_id = {pos_id} "

    sell_data = self.seld(sql)
    if sell_data:
        return sell_data
    return sell_data
#<=====>#
