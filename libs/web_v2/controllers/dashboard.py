# Dashboard Controller - Time-based Performance Views
from libs.web_v2.models.base import BaseModel
from typing import Dict, Any, List
from datetime import date


class DashboardController(BaseModel):
    """Controller for main dashboard and time-based views"""
    
    def get_period_summary(self, period: str = 'today') -> Dict[str, Any]:
        """Get summary for a specific time period"""
        start_date, end_date = self.get_date_range(period)
        
        # Use Unix timestamp-based date filtering for accuracy
        sql = f"""
        SELECT 
            'Live Trading' as category,
            COUNT(p.pos_id) as total_positions,
            SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as losses,
            ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 2) as win_rate,
            ROUND(SUM(p.gain_loss_amt), 2) as total_pnl,
            ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN p.gain_loss_amt ELSE 0 END), 2) as total_gains,
            ROUND(ABS(SUM(CASE WHEN p.gain_loss_amt < 0 THEN p.gain_loss_amt ELSE 0 END)), 2) as total_losses,
            ROUND(SUM(p.fees_cnt_tot), 2) as total_fees,
            ROUND(AVG((p.pos_end_unix - p.pos_begin_unix) / 3600), 2) as avg_hours_held
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat = 'CLOSE'
        AND FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') >= '{start_date}'
        AND FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') <= '{end_date}'
        """
        
        results = self.execute_query(sql, f"Period Summary - {period}")
        return results[0] if results else {}
    
    def get_period_by_market(self, period: str = 'today') -> List[Dict[str, Any]]:
        """Get performance broken down by market for a time period"""
        start_date, end_date = self.get_date_range(period)
        
        sql = f"""
        SELECT 
            p.prod_id,
            COUNT(p.pos_id) as positions,
            SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as losses,
            ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 1) as win_rate,
            ROUND(SUM(p.gain_loss_amt), 2) as total_pnl,
            ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 4) as gain_pct,
            ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100 / 
                  AVG((p.pos_end_unix - p.pos_begin_unix) / 3600), 6) as pct_per_hour
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat = 'CLOSE'
        AND FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') >= '{start_date}'
        AND FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') <= '{end_date}'
        GROUP BY p.prod_id
        ORDER BY total_pnl DESC
        """
        
        return self.execute_query(sql, f"Period by Market - {period}")
    
    def get_open_positions_summary(self) -> Dict[str, Any]:
        """Get summary of current open positions"""
        sql = """
        SELECT 
            COUNT(p.pos_id) as total_open,
            SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as currently_winning,
            SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as currently_losing,
            ROUND(SUM(p.tot_out_cnt), 2) as total_invested,
            ROUND(SUM(p.val_tot), 2) as current_value,
            ROUND(SUM(p.gain_loss_amt), 2) as unrealized_pnl,
            ROUND(AVG((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600), 2) as avg_hours_held
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat IN ('OPEN', 'SELL')
        """
        
        results = self.execute_query(sql, "Open Positions Summary")
        return results[0] if results else {}
    
    def get_recent_activity(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent trading activity"""
        sql = f"""
        SELECT 
            p.pos_id,
            p.prod_id,
            p.pos_stat,
            ROUND(p.gain_loss_amt, 2) as pnl,
            ROUND((p.pos_end_unix - p.pos_begin_unix) / 3600, 1) as hours_held,
            FROM_UNIXTIME(COALESCE(p.pos_end_unix, UNIX_TIMESTAMP()), '%Y-%m-%d %H:%i') as last_update,
            p.buy_strat_name,
            p.buy_strat_freq
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        ORDER BY COALESCE(p.pos_end_unix, p.pos_begin_unix) DESC
        LIMIT {limit}
        """
        
        return self.execute_query(sql, "Recent Activity")
    
    def get_dashboard_data(self, periods: List[str] = None) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        if periods is None:
            periods = ['today', 'week', 'month', 'year']
        
        dashboard_data = {
            'periods': {},
            'open_summary': self.get_open_positions_summary(),
            'recent_activity': self.get_recent_activity()
        }
        
        for period in periods:
            dashboard_data['periods'][period] = {
                'summary': self.get_period_summary(period),
                'by_market': self.get_period_by_market(period)
            }
        
        return dashboard_data
