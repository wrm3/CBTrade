# Balances Controller - Balance Views with Pocket/Clips and Out-of-Balance Detection
from libs.web_v2.models.base import BaseModel
from typing import Dict, Any, List


class BalancesController(BaseModel):
    """Controller for balance management and analysis"""
    
    def get_current_balances(self) -> List[Dict[str, Any]]:
        """Get current balances using your proven working SQL pattern"""
        sql = """
        SELECT b.symb
            , ROUND(b.bal_tot, 8) as total_balance
            , case when b.symb = 'USDC' then 1 else b.curr_prc_usd end as price_usd
            , COALESCE(s.open_pos_cnt, 0) AS open_positions
            , COALESCE(s.closed_pos_cnt, 0) AS closed_positions
            , COALESCE(s.open_hold_cnt, 0) AS position_holdings
            , COALESCE(s.closed_hold_cnt, 0) AS closed_holdings
            , (b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) AS balance_variance
            , ROUND(b.curr_val_usd, 2) as value_usd
            , round(COALESCE(s.open_hold_cnt, 0) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end, 2) AS open_hold_value
            , round(COALESCE(s.closed_hold_cnt, 0) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end, 2) AS closed_hold_value
            , round((b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end, 2) AS variance_usd
            , CASE 
                WHEN ABS(b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) > 0.00001 
                THEN 'OUT_OF_BALANCE'
                ELSE 'BALANCED'
              END as balance_status
        FROM cbtrade.bals b
        LEFT JOIN (
            SELECT p.base_curr_symb AS symb
                , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END) AS open_pos_cnt
                , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.hold_cnt ELSE 0 END) AS open_hold_cnt
                , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) AS closed_pos_cnt
                , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.hold_cnt ELSE 0 END) AS closed_hold_cnt
            FROM cbtrade.poss p
            WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'N' AND p.quote_curr_symb = 'USDC'
            GROUP BY p.base_curr_symb
        ) s ON s.symb = b.symb
        WHERE b.bal_tot > 0
        ORDER BY value_usd DESC
        """
        
        return self.execute_query(sql, "Current Balances")
    
    def get_balance_summary(self) -> Dict[str, Any]:
        """Get overall balance summary using proven working SQL pattern"""
        
        # Use your proven working query pattern - aggregated summary
        sql = """
        SELECT 
            COUNT(b.symb) as total_currencies,
            ROUND(SUM(b.curr_val_usd), 2) as total_portfolio_value,
            ROUND(SUM(b.bal_avail * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end), 2) as available_value,
            ROUND(SUM(COALESCE(s.open_hold_cnt, 0) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end), 2) as total_invested,
            ROUND(SUM(COALESCE(s.closed_hold_cnt, 0) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end), 2) as closed_hold_value,
            SUM(COALESCE(s.open_pos_cnt, 0)) as total_open_positions,
            SUM(COALESCE(s.closed_pos_cnt, 0)) as total_closed_positions,
            ROUND(SUM((b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end), 2) as over_under_value,
            COUNT(CASE WHEN ABS(b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) > 0.00001 THEN 1 END) as out_of_balance_count
        FROM cbtrade.bals b
        LEFT JOIN (
            SELECT p.base_curr_symb AS symb
                , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END) AS open_pos_cnt
                , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.hold_cnt ELSE 0 END) AS open_hold_cnt
                , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) AS closed_pos_cnt
                , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.hold_cnt ELSE 0 END) AS closed_hold_cnt
            FROM cbtrade.poss p
            WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'N' AND p.quote_curr_symb = 'USDC'
            GROUP BY p.base_curr_symb
        ) s ON s.symb = b.symb
        WHERE b.bal_tot > 0
        """
        
        # Get pocket/clip summary separately to avoid complexity
        pocket_clip_sql = """
        SELECT 
            ROUND(SUM(p.pocket_cnt * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end), 2) as total_pocket_value,
            ROUND(SUM(p.clip_cnt * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end), 2) as total_clip_value
        FROM cbtrade.poss p
        JOIN cbtrade.bals b ON b.symb = p.base_curr_symb
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.pos_stat IN ('OPEN', 'SELL')
        """
        
        # Execute queries and combine
        balance_results = self.execute_query(sql, "Balance Summary")
        pocket_results = self.execute_query(pocket_clip_sql, "Pocket/Clip Summary")
        
        summary = balance_results[0] if balance_results else {}
        
        # Add pocket/clip data
        if pocket_results and pocket_results[0]:
            summary['total_pocket_value'] = pocket_results[0].get('total_pocket_value', 0.0)
            summary['total_clip_value'] = pocket_results[0].get('total_clip_value', 0.0)
        else:
            summary['total_pocket_value'] = 0.0
            summary['total_clip_value'] = 0.0
            
        # Calculate unrealized P&L separately
        pnl_sql = """
        SELECT ROUND(SUM(p.gain_loss_amt), 2) as unrealized_pnl
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'N' AND p.pos_stat IN ('OPEN', 'SELL')
        """
        pnl_results = self.execute_query(pnl_sql, "Unrealized PnL")
        summary['unrealized_pnl'] = pnl_results[0].get('unrealized_pnl', 0.0) if pnl_results else 0.0
        
        return summary
    
    def get_out_of_balance_items(self) -> List[Dict[str, Any]]:
        """Get items that are out of balance using proven working pattern"""
        sql = """
        SELECT b.symb
            , ROUND(b.bal_tot, 8) as exchange_balance
            , COALESCE(s.open_hold_cnt, 0) + COALESCE(s.closed_hold_cnt, 0) as calculated_balance
            , (b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) AS variance
            , round((b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end, 2) AS variance_usd
            , COALESCE(s.open_pos_cnt, 0) AS affecting_positions
            , case when b.symb = 'USDC' then 1 else b.curr_prc_usd end as price_usd
            , ROUND(b.curr_val_usd, 2) as current_value_usd
        FROM cbtrade.bals b
        LEFT JOIN (
            SELECT p.base_curr_symb AS symb
                , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END) AS open_pos_cnt
                , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.hold_cnt ELSE 0 END) AS open_hold_cnt
                , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) AS closed_pos_cnt
                , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.hold_cnt ELSE 0 END) AS closed_hold_cnt
            FROM cbtrade.poss p
            WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'N' AND p.quote_curr_symb = 'USDC'
            GROUP BY p.base_curr_symb
        ) s ON s.symb = b.symb
        WHERE b.bal_tot > 0
        AND ABS(b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) > 0.00001
        ORDER BY ABS(variance_usd) DESC
        """
        
        return self.execute_query(sql, "Out of Balance Items")
    
    def get_pocket_clip_breakdown(self) -> List[Dict[str, Any]]:
        """Get detailed pocket and clip breakdown by currency"""
        sql = """
        SELECT 
            p.base_curr_symb as symb,
            COUNT(p.pos_id) as open_positions,
            ROUND(SUM(p.pocket_cnt), 8) as total_pocket,
            ROUND(SUM(p.clip_cnt), 8) as total_clips,
            ROUND(SUM(p.hold_cnt), 8) as total_hold,
            
            -- USD values using your price pattern
            ROUND(SUM(p.pocket_cnt) * case when p.base_curr_symb = 'USDC' then 1 else b.curr_prc_usd end, 2) as pocket_value_usd,
            ROUND(SUM(p.clip_cnt) * case when p.base_curr_symb = 'USDC' then 1 else b.curr_prc_usd end, 2) as clip_value_usd,
            ROUND(SUM(p.hold_cnt) * case when p.base_curr_symb = 'USDC' then 1 else b.curr_prc_usd end, 2) as hold_value_usd,
            
            -- Percentages
            ROUND(SUM(p.pocket_cnt) / NULLIF(SUM(p.hold_cnt), 0) * 100, 2) as pocket_pct,
            ROUND(SUM(p.clip_cnt) / NULLIF(SUM(p.hold_cnt), 0) * 100, 2) as clip_pct,
            
            case when p.base_curr_symb = 'USDC' then 1 else b.curr_prc_usd end as price_usd
        FROM cbtrade.poss p
        JOIN cbtrade.bals b ON b.symb = p.base_curr_symb
        WHERE p.ignore_tf = 0 
        AND p.test_txn_yn = 'N'
        AND p.quote_curr_symb = 'USDC'
        AND p.pos_stat IN ('OPEN', 'SELL')
        GROUP BY p.base_curr_symb, b.curr_prc_usd
        HAVING SUM(p.pocket_cnt) > 0 OR SUM(p.clip_cnt) > 0
        ORDER BY hold_value_usd DESC
        """
        
        return self.execute_query(sql, "Pocket/Clip Breakdown")
    
    def get_balance_history_summary(self, days: int = 7) -> List[Dict[str, Any]]:
        """Balance history not available - timestamp column doesn't exist"""
        return []
    
    def get_balances_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive balance dashboard data"""
        return {
            'summary': self.get_balance_summary(),
            'balances': self.get_current_balances(),
            'out_of_balance': self.get_out_of_balance_items(),
            'pocket_clip_breakdown': self.get_pocket_clip_breakdown(),
            'recent_history': self.get_balance_history_summary()
        }
