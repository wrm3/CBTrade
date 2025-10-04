# Performance Controller - Drill-down Performance Analysis
from libs.web_v2.models.base import BaseModel
from typing import Dict, Any, List, Optional


class PerformanceController(BaseModel):
    """Controller for performance analysis and drill-down views"""
    
    def get_overall_performance(self, test_mode: str = 'N') -> Dict[str, Any]:
        """Get overall performance summary"""
        test_filter = f"AND p.test_txn_yn = '{test_mode}'" if test_mode in ['Y', 'N'] else ""
        
        sql = f"""
        SELECT 
            '{test_mode}' as mode,
            COUNT(p.pos_id) as total_positions,
            SUM(CASE WHEN p.pos_stat = 'OPEN' THEN 1 ELSE 0 END) as open_positions,
            SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) as closed_positions,
            
            -- Closed position metrics
            SUM(CASE WHEN p.pos_stat = 'CLOSE' AND p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN p.pos_stat = 'CLOSE' AND p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as losses,
            ROUND(SUM(CASE WHEN p.pos_stat = 'CLOSE' AND p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / 
                  SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) * 100, 2) as win_rate,
            
            -- Financial metrics
            ROUND(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt ELSE 0 END), 2) as total_realized_pnl,
            ROUND(SUM(CASE WHEN p.pos_stat = 'OPEN' THEN p.gain_loss_amt ELSE 0 END), 2) as total_unrealized_pnl,
            ROUND(SUM(p.gain_loss_amt), 2) as total_pnl,
            ROUND(SUM(p.tot_out_cnt), 2) as total_invested,
            ROUND(SUM(p.fees_cnt_tot), 2) as total_fees,
            
            -- Performance ratios
            ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 4) as return_on_investment,
            ROUND(AVG(CASE WHEN p.pos_stat = 'CLOSE' 
                      THEN (p.pos_end_unix - p.pos_begin_unix) / 3600 
                      ELSE (UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600 END), 2) as avg_hold_hours,
                      
            -- Recent activity (last 24h)
            SUM(CASE WHEN p.pos_stat = 'CLOSE' 
                     AND FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') = CURDATE() 
                THEN 1 ELSE 0 END) as positions_closed_today
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        {test_filter}
        """
        
        results = self.execute_query(sql, f"Overall Performance - {test_mode}")
        return results[0] if results else {}
    
    def get_performance_by_product(self, test_mode: str = 'N', min_positions: int = 5) -> List[Dict[str, Any]]:
        """Get performance broken down by product"""
        test_filter = f"AND p.test_txn_yn = '{test_mode}'" if test_mode in ['Y', 'N'] else ""
        
        sql = f"""
        SELECT 
            p.prod_id,
            COUNT(p.pos_id) as total_positions,
            SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) as closed_positions,
            SUM(CASE WHEN p.pos_stat = 'OPEN' THEN 1 ELSE 0 END) as open_positions,
            
            -- Closed performance
            SUM(CASE WHEN p.pos_stat = 'CLOSE' AND p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN p.pos_stat = 'CLOSE' AND p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as losses,
            ROUND(SUM(CASE WHEN p.pos_stat = 'CLOSE' AND p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / 
                  NULLIF(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END), 0) * 100, 1) as win_rate,
            
            ROUND(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt ELSE 0 END), 2) as realized_pnl,
            ROUND(SUM(CASE WHEN p.pos_stat = 'OPEN' THEN p.gain_loss_amt ELSE 0 END), 2) as unrealized_pnl,
            ROUND(SUM(p.gain_loss_amt), 2) as total_pnl,
            
            -- Performance metrics
            ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 4) as roi_pct,
            ROUND(AVG(CASE WHEN p.pos_stat = 'CLOSE' 
                      THEN (p.pos_end_unix - p.pos_begin_unix) / 3600 
                      ELSE NULL END), 2) as avg_hold_hours_closed,
            
            -- Rate-based performance
            ROUND(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt ELSE 0 END) / 
                  SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.tot_out_cnt ELSE 0 END) * 100 / 
                  NULLIF(AVG(CASE WHEN p.pos_stat = 'CLOSE' 
                             THEN (p.pos_end_unix - p.pos_begin_unix) / 3600 
                             ELSE NULL END), 0), 6) as pct_per_hour
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        {test_filter}
        GROUP BY p.prod_id
        HAVING COUNT(p.pos_id) >= {min_positions}
        ORDER BY total_pnl DESC
        """
        
        return self.execute_query(sql, f"Performance by Product - {test_mode}")
    
    def get_performance_by_strategy(self, test_mode: str = 'N', min_positions: int = 5) -> List[Dict[str, Any]]:
        """Get performance broken down by strategy"""
        test_filter = f"AND p.test_txn_yn = '{test_mode}'" if test_mode in ['Y', 'N'] else ""
        
        sql = f"""
        SELECT 
            p.buy_strat_name,
            p.buy_strat_freq,
            COUNT(p.pos_id) as total_positions,
            COUNT(DISTINCT p.prod_id) as markets_traded,
            SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) as closed_positions,
            
            -- Performance metrics
            SUM(CASE WHEN p.pos_stat = 'CLOSE' AND p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as wins,
            ROUND(SUM(CASE WHEN p.pos_stat = 'CLOSE' AND p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / 
                  NULLIF(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END), 0) * 100, 1) as win_rate,
            
            ROUND(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt ELSE 0 END), 2) as realized_pnl,
            ROUND(SUM(CASE WHEN p.pos_stat = 'OPEN' THEN p.gain_loss_amt ELSE 0 END), 2) as unrealized_pnl,
            ROUND(SUM(p.gain_loss_amt), 2) as total_pnl,
            
            -- Strategy effectiveness
            ROUND(AVG(CASE WHEN p.pos_stat = 'CLOSE' 
                      THEN (p.pos_end_unix - p.pos_begin_unix) / 3600 
                      ELSE NULL END), 2) as avg_hold_hours,
            ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 4) as roi_pct,
            
            -- Most recent activity
            MAX(CASE WHEN p.pos_stat = 'CLOSE' 
                THEN FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d %H:%i') 
                ELSE FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d %H:%i') END) as last_activity
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        {test_filter}
        GROUP BY p.buy_strat_name, p.buy_strat_freq
        HAVING COUNT(p.pos_id) >= {min_positions}
        ORDER BY total_pnl DESC
        """
        
        return self.execute_query(sql, f"Performance by Strategy - {test_mode}")
    
    def get_performance_by_timeframe(self, test_mode: str = 'N') -> List[Dict[str, Any]]:
        """Get performance broken down by time periods"""
        test_filter = f"AND p.test_txn_yn = '{test_mode}'" if test_mode in ['Y', 'N'] else ""
        
        sql = f"""
        SELECT 
            'Today' as period,
            FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') as date_key,
            COUNT(p.pos_id) as positions,
            SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as wins,
            ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 1) as win_rate,
            ROUND(SUM(p.gain_loss_amt), 2) as total_pnl,
            ROUND(AVG((p.pos_end_unix - p.pos_begin_unix) / 3600), 2) as avg_hours
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.pos_stat = 'CLOSE'
        {test_filter}
        AND FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d')
        ORDER BY date_key DESC
        LIMIT 30
        """
        
        return self.execute_query(sql, f"Performance by Timeframe - {test_mode}")
    
    def get_drill_down_performance(self, 
                                 product: Optional[str] = None, 
                                 strategy: Optional[str] = None, 
                                 strategy_freq: Optional[str] = None,
                                 start_date: Optional[str] = None,
                                 end_date: Optional[str] = None,
                                 test_mode: str = 'N') -> List[Dict[str, Any]]:
        """Get detailed drill-down performance with multiple filters"""
        
        filters = ["p.ignore_tf = 0"]
        
        if test_mode in ['Y', 'N']:
            filters.append(f"p.test_txn_yn = '{test_mode}'")
            
        if product:
            filters.append(f"p.prod_id = '{product}'")
            
        if strategy:
            filters.append(f"p.buy_strat_name = '{strategy}'")
            
        if strategy_freq:
            filters.append(f"p.buy_strat_freq = '{strategy_freq}'")
            
        if start_date:
            filters.append(f"FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d') >= '{start_date}'")
            
        if end_date:
            filters.append(f"FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') <= '{end_date}'")
        
        where_clause = " AND ".join(filters)
        
        sql = f"""
        SELECT 
            p.pos_id,
            p.prod_id,
            p.pos_stat,
            p.buy_strat_name,
            p.buy_strat_freq,
            FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d %H:%i') as start_time,
            CASE WHEN p.pos_stat = 'CLOSE' 
                 THEN FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d %H:%i') 
                 ELSE 'OPEN' END as end_time,
            ROUND((COALESCE(p.pos_end_unix, UNIX_TIMESTAMP()) - p.pos_begin_unix) / 3600, 2) as hours_held,
            ROUND(p.tot_out_cnt, 2) as invested,
            ROUND(p.val_tot, 2) as current_value,
            ROUND(p.gain_loss_amt, 2) as pnl,
            ROUND(p.gain_loss_amt / p.tot_out_cnt * 100, 4) as roi_pct,
            ROUND(p.pocket_cnt, 8) as pocket,
            ROUND(p.clip_cnt, 8) as clips,
            p.test_txn_yn
        FROM cbtrade.poss p
        WHERE {where_clause}
        ORDER BY p.pos_begin_unix DESC
        LIMIT 500
        """
        
        return self.execute_query(sql, "Drill-down Performance")
    
    def get_performance_dashboard(self, test_mode: str = 'N') -> Dict[str, Any]:
        """Get comprehensive performance dashboard"""
        return {
            'overall': self.get_overall_performance(test_mode),
            'by_product': self.get_performance_by_product(test_mode),
            'by_strategy': self.get_performance_by_strategy(test_mode),
            'by_timeframe': self.get_performance_by_timeframe(test_mode)
        }
