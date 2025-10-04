# Positions Controller - Open Position Management
from libs.web_v2.models.base import BaseModel
from typing import Dict, Any, List, Optional


class PositionsController(BaseModel):
    """Controller for open position management and analysis"""
    
    def get_open_positions(self, sort_by: str = 'pnl_desc') -> List[Dict[str, Any]]:
        """Get all open positions with detailed information"""
        
        # Define sort options
        sort_options = {
            'pnl_desc': 'p.gain_loss_amt DESC',
            'pnl_asc': 'p.gain_loss_amt ASC', 
            'age_desc': '(UNIX_TIMESTAMP() - p.pos_begin_unix) DESC',
            'age_asc': '(UNIX_TIMESTAMP() - p.pos_begin_unix) ASC',
            'invested_desc': 'p.tot_out_cnt DESC',
            'invested_asc': 'p.tot_out_cnt ASC',
            'product': 'p.prod_id, p.gain_loss_amt DESC',
            'strategy': 'p.buy_strat_name, p.buy_strat_freq, p.gain_loss_amt DESC'
        }
        
        order_clause = sort_options.get(sort_by, sort_options['pnl_desc'])
        
        sql = f"""
        SELECT 
            p.pos_id,
            p.prod_id,
            p.buy_strat_name,
            p.buy_strat_freq,
            
            -- Timing information
            FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d %H:%i') as opened_at,
            ROUND((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600, 1) as hours_held,
            ROUND((UNIX_TIMESTAMP() - p.pos_begin_unix) / 86400, 1) as days_held,
            
            -- Financial details
            ROUND(p.tot_out_cnt, 2) as invested,
            ROUND(p.val_tot, 2) as current_value, 
            ROUND(p.gain_loss_amt, 2) as unrealized_pnl,
            ROUND(p.gain_loss_amt / p.tot_out_cnt * 100, 4) as unrealized_pct,
            ROUND(p.fees_cnt_tot, 2) as fees_paid,
            
            -- Holdings breakdown
            ROUND(p.hold_cnt, 8) as total_holdings,
            ROUND(p.pocket_cnt, 8) as pocket_amount,
            ROUND(p.clip_cnt, 8) as clip_amount,
            ROUND(p.pocket_cnt / NULLIF(p.hold_cnt, 0) * 100, 2) as pocket_pct,
            ROUND(p.clip_cnt / NULLIF(p.hold_cnt, 0) * 100, 2) as clip_pct,
            
            -- Trading activity
            p.sell_order_cnt,
            p.sell_order_attempt_cnt,
            CASE WHEN p.sell_order_attempt_cnt > 0 
                 THEN ROUND(p.sell_order_cnt / p.sell_order_attempt_cnt * 100, 1)
                 ELSE 0 END as sell_success_rate,
            
            -- Status indicators
            CASE 
                WHEN p.gain_loss_amt > 0 THEN 'WINNING'
                WHEN p.gain_loss_amt < 0 THEN 'LOSING' 
                ELSE 'BREAKEVEN'
            END as status,
            
            CASE 
                WHEN (UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600 > 168 THEN 'LONG_HOLD'  -- > 7 days
                WHEN (UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600 > 24 THEN 'EXTENDED'   -- > 1 day
                ELSE 'RECENT'
            END as age_category,
            
            p.test_txn_yn
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat = 'OPEN'
        ORDER BY {order_clause}
        """
        
        return self.execute_query(sql, f"Open Positions - {sort_by}")
    
    def get_open_positions_summary_by_product(self) -> List[Dict[str, Any]]:
        """Get open positions summarized by product"""
        sql = """
        SELECT 
            p.prod_id,
            COUNT(p.pos_id) as open_count,
            ROUND(SUM(p.tot_out_cnt), 2) as total_invested,
            ROUND(SUM(p.val_tot), 2) as current_value,
            ROUND(SUM(p.gain_loss_amt), 2) as total_unrealized_pnl,
            ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 4) as unrealized_pct,
            
            -- Win/loss status
            SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as currently_winning,
            SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as currently_losing,
            ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 1) as winning_pct,
            
            -- Age analysis
            ROUND(AVG((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600), 1) as avg_hours_held,
            ROUND(MIN((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600), 1) as newest_hours,
            ROUND(MAX((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600), 1) as oldest_hours,
            
            -- Holdings
            ROUND(SUM(p.pocket_cnt), 8) as total_pocket,
            ROUND(SUM(p.clip_cnt), 8) as total_clips
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat = 'OPEN'
        GROUP BY p.prod_id
        ORDER BY total_unrealized_pnl DESC
        """
        
        return self.execute_query(sql, "Open Positions by Product")
    
    def get_open_positions_by_strategy(self) -> List[Dict[str, Any]]:
        """Get open positions summarized by strategy"""
        sql = """
        SELECT 
            p.buy_strat_name,
            p.buy_strat_freq,
            COUNT(p.pos_id) as open_count,
            COUNT(DISTINCT p.prod_id) as markets_active,
            ROUND(SUM(p.tot_out_cnt), 2) as total_invested,
            ROUND(SUM(p.gain_loss_amt), 2) as total_unrealized_pnl,
            ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 4) as unrealized_pct,
            
            -- Performance indicators
            SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as winning_positions,
            ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 1) as winning_rate,
            
            -- Age information
            ROUND(AVG((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600), 1) as avg_hours_held,
            
            -- Most recent activity
            MAX(FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d %H:%i')) as last_opened
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat = 'OPEN'
        GROUP BY p.buy_strat_name, p.buy_strat_freq
        ORDER BY total_unrealized_pnl DESC
        """
        
        return self.execute_query(sql, "Open Positions by Strategy")
    
    def get_positions_at_risk(self, loss_threshold: float = -5.0, age_threshold_hours: int = 24) -> List[Dict[str, Any]]:
        """Get positions that might need attention (losing money or held too long)"""
        sql = f"""
        SELECT 
            p.pos_id,
            p.prod_id,
            p.buy_strat_name,
            p.buy_strat_freq,
            FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d %H:%i') as opened_at,
            ROUND((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600, 1) as hours_held,
            ROUND(p.tot_out_cnt, 2) as invested,
            ROUND(p.gain_loss_amt, 2) as unrealized_pnl,
            ROUND(p.gain_loss_amt / p.tot_out_cnt * 100, 4) as unrealized_pct,
            
            -- Risk indicators
            CASE 
                WHEN p.gain_loss_amt / p.tot_out_cnt * 100 < {loss_threshold} THEN 'HIGH_LOSS'
                WHEN (UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600 > {age_threshold_hours * 7} THEN 'VERY_OLD'  -- 7x threshold
                WHEN (UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600 > {age_threshold_hours} THEN 'OLD'
                ELSE 'MODERATE_LOSS'
            END as risk_category,
            
            p.sell_order_attempt_cnt,
            p.sell_order_cnt
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat = 'OPEN'
        AND (
            p.gain_loss_amt / p.tot_out_cnt * 100 < {loss_threshold}
            OR (UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600 > {age_threshold_hours}
        )
        ORDER BY p.gain_loss_amt ASC, (UNIX_TIMESTAMP() - p.pos_begin_unix) DESC
        """
        
        return self.execute_query(sql, "Positions At Risk")
    
    def get_recent_position_activity(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recently opened positions"""
        sql = f"""
        SELECT 
            p.pos_id,
            p.prod_id,
            p.buy_strat_name,
            p.buy_strat_freq,
            FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d %H:%i') as opened_at,
            ROUND((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600, 1) as hours_ago,
            ROUND(p.tot_out_cnt, 2) as invested,
            ROUND(p.gain_loss_amt, 2) as current_pnl,
            ROUND(p.gain_loss_amt / p.tot_out_cnt * 100, 4) as current_pct,
            CASE 
                WHEN p.gain_loss_amt > 0 THEN 'WINNING'
                WHEN p.gain_loss_amt < 0 THEN 'LOSING'
                ELSE 'BREAKEVEN'
            END as status
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat = 'OPEN'
        ORDER BY p.pos_begin_unix DESC
        LIMIT {limit}
        """
        
        return self.execute_query(sql, "Recent Position Activity")
    
    def get_positions_dashboard(self, sort_by: str = 'pnl_desc') -> Dict[str, Any]:
        """Get comprehensive positions dashboard"""
        return {
            'open_positions': self.get_open_positions(sort_by),
            'by_product': self.get_open_positions_summary_by_product(), 
            'by_strategy': self.get_open_positions_by_strategy(),
            'at_risk': self.get_positions_at_risk(),
            'recent_activity': self.get_recent_position_activity()
        }
