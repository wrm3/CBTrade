# CBTrade FINAL Dashboard - Proper Live/Test/All Separation
from flask import Flask, request
from libs.db_mysql.cbtrade.db_main import cbtrade_db as db

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Comprehensive dashboard with proper Live/Test/All separation"""
    try:
        # LIVE MONEY ONLY - Real Trading Data
        live_balance_sql = """
        SELECT 
            (SELECT COUNT(b.symb) FROM cbtrade.bals b WHERE b.ignore_tf = 0) as currencies,
            CONCAT('$ ', ROUND((SELECT SUM(b.curr_val_usd) FROM cbtrade.bals b WHERE b.ignore_tf = 0), 2)) as total_portfolio,
            CONCAT('$ ', ROUND((SELECT SUM(b.bal_avail * b.curr_prc_usd) FROM cbtrade.bals b WHERE b.ignore_tf = 0), 2)) as available_cash,
            CONCAT('$ ', ROUND((SELECT SUM(tot_out_cnt) FROM cbtrade.poss WHERE ignore_tf=0 AND pos_stat='OPEN' AND test_txn_yn='N'), 2)) as live_invested,
            CONCAT('$ ', ROUND((SELECT SUM(val_tot) FROM cbtrade.poss WHERE ignore_tf=0 AND pos_stat='OPEN' AND test_txn_yn='N'), 2)) as live_value,
            CONCAT('$ ', ROUND((SELECT SUM(tot_out_cnt) FROM cbtrade.poss WHERE ignore_tf=0 AND pos_stat='OPEN' AND test_txn_yn='Y'), 2)) as test_invested,
            CONCAT('$ ', ROUND((SELECT SUM(val_tot) FROM cbtrade.poss WHERE ignore_tf=0 AND pos_stat='OPEN' AND test_txn_yn='Y'), 2)) as test_value,
            (SELECT COUNT(*) FROM cbtrade.poss WHERE ignore_tf=0 AND pos_stat='OPEN' AND test_txn_yn='N') as live_positions,
            (SELECT COUNT(*) FROM cbtrade.poss WHERE ignore_tf=0 AND pos_stat='OPEN' AND test_txn_yn='Y') as test_positions
        """
        balance_data = db.seld(live_balance_sql)[0]
        
        # LIVE SUMMARY - All Time Performance
        live_summary_sql = """
        SELECT COUNT(p.pos_id) as tot_cnt,
               SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as win_cnt,
               SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as lose_cnt,
               ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 2) as win_pct,
               ROUND(SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 2) as lose_pct,
               ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN p.gain_loss_amt ELSE 0 END), 2) as gain_amt,
               ROUND(ABS(SUM(CASE WHEN p.gain_loss_amt < 0 THEN p.gain_loss_amt ELSE 0 END)), 2) as loss_amt,
               ROUND(SUM(p.gain_loss_amt), 2) as gain_loss_amt,
               ROUND(SUM(p.gain_loss_amt_net), 2) as gain_loss_amt_net,
               ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 2) as gain_loss_pct,
               ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100 / AVG((p.pos_end_unix - p.pos_begin_unix) / 3600), 8) as gain_loss_pct_hr,
               ROUND(AVG((p.pos_end_unix - p.pos_begin_unix) / 3600), 2) as age_hours,
               ROUND(SUM(p.tot_out_cnt), 2) as tot_out_cnt,
               ROUND(SUM(p.tot_in_cnt), 2) as tot_in_cnt,
               ROUND(SUM(p.fees_cnt_tot), 2) as fees_cnt_tot
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'N' AND p.pos_stat = 'CLOSE'
        """
        live_summary = db.seld(live_summary_sql)[0]
        
        # TEST SUMMARY - All Time Performance  
        test_summary_sql = """
        SELECT COUNT(p.pos_id) as tot_cnt,
               SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as win_cnt,
               SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as lose_cnt,
               ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 2) as win_pct,
               ROUND(SUM(p.gain_loss_amt), 2) as gain_loss_amt,
               ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 2) as gain_loss_pct,
               ROUND(SUM(p.tot_out_cnt), 2) as tot_out_cnt
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'Y' AND p.pos_stat = 'CLOSE'
        """
        test_summary = db.seld(test_summary_sql)[0] if db.seld(test_summary_sql) else {}
        
        # LIVE Open Positions by Market
        live_open_sql = """
        SELECT p.prod_id,
               COUNT(p.pos_id) as tot_cnt,
               SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as win_cnt,
               SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as lose_cnt,
               ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 1) as win_pct,
               ROUND(SUM(p.gain_loss_amt), 2) as gain_loss_amt,
               ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100, 2) as gain_loss_pct,
               ROUND(SUM(p.gain_loss_amt) / SUM(p.tot_out_cnt) * 100 / AVG((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600), 6) as gain_loss_pct_hr,
               ROUND(SUM(p.tot_out_cnt), 2) as tot_out_cnt,
               ROUND(SUM(p.val_tot), 2) as val_tot,
               'N' as test_txn_yn
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'N' AND p.pos_stat = 'OPEN'
        GROUP BY p.prod_id
        ORDER BY gain_loss_pct_hr DESC
        """
        live_open_data = db.seld(live_open_sql)
        
        # TEST Open Positions by Market
        test_open_sql = """
        SELECT p.prod_id,
               COUNT(p.pos_id) as tot_cnt,
               SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) as win_cnt,
               SUM(CASE WHEN p.gain_loss_amt <= 0 THEN 1 ELSE 0 END) as lose_cnt,
               ROUND(SUM(CASE WHEN p.gain_loss_amt > 0 THEN 1 ELSE 0 END) / COUNT(p.pos_id) * 100, 1) as win_pct,
               ROUND(SUM(p.gain_loss_amt), 2) as gain_loss_amt,
               ROUND(SUM(p.tot_out_cnt), 2) as tot_out_cnt,
               ROUND(SUM(p.val_tot), 2) as val_tot,
               'Y' as test_txn_yn
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'Y' AND p.pos_stat = 'OPEN'
        GROUP BY p.prod_id
        ORDER BY gain_loss_amt DESC
        """
        test_open_data = db.seld(test_open_sql)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CBTrade - Live/Test/All Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%); color: white; }}
        .container {{ display: flex; min-height: 100vh; }}
        
        .sidebar {{ width: 180px; background: rgba(0,0,0,0.4); backdrop-filter: blur(10px); padding: 12px; }}
        .nav-section {{ color: #fbbf24; margin: 12px 0 6px 0; font-size: 10px; text-transform: uppercase; font-weight: bold; }}
        .nav-link {{ display: block; padding: 4px 8px; color: #e2e8f0; text-decoration: none; border-radius: 3px; margin: 1px 0; font-size: 11px; }}
        .nav-link:hover {{ background: rgba(59, 130, 246, 0.5); }}
        
        .main {{ flex: 1; padding: 20px; }}
        .main h1 {{ color: #fbbf24; font-size: 1.8em; margin-bottom: 20px; }}
        
        .balance-card {{ background: rgba(255,255,255,0.95); border-radius: 8px; padding: 20px; margin: 15px 0; }}
        .balance-card h2 {{ color: #1e3a8a; margin-bottom: 15px; font-size: 16px; }}
        .balance-metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 15px; }}
        .balance-metric {{ text-align: center; background: #f8fafc; padding: 10px; border-radius: 6px; }}
        .balance-metric .value {{ font-size: 1.2em; font-weight: bold; color: #1e3a8a; }}
        .balance-metric .label {{ font-size: 0.8em; color: #64748b; }}
        
        .report-section {{ background: rgba(255,255,255,0.98); border-radius: 8px; margin: 15px 0; overflow: hidden; }}
        .report-section h2 {{ background: #1e40af; color: #fbbf24; padding: 10px 15px; margin: 0; font-size: 13px; text-transform: uppercase; }}
        .report-section table {{ width: 100%; border-collapse: collapse; }}
        .report-section th {{ background: #3730a3; color: white; padding: 6px 4px; font-size: 10px; text-align: center; border-right: 1px solid rgba(255,255,255,0.3); }}
        .report-section td {{ padding: 4px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; color: #1e293b; text-align: center; font-size: 11px; }}
        .report-section td:first-child {{ font-weight: bold; background: #f8fafc; }}
        
        .live-section {{ border-left: 4px solid #10b981; }}
        .test-section {{ border-left: 4px solid #f59e0b; }}
        .all-section {{ border-left: 4px solid #6366f1; }}
        
        .positive {{ background: #dcfce7 !important; color: #166534 !important; font-weight: bold; }}
        .negative {{ background: #fee2e2 !important; color: #dc2626 !important; font-weight: bold; }}
        .neutral {{ color: #6b7280; }}
        
        .summary-row {{ background: #1e40af !important; }}
        .summary-row td {{ color: white !important; font-weight: bold !important; border: 1px solid white !important; }}
        
        .live-badge {{ background: #10b981; color: white; padding: 2px 6px; border-radius: 3px; font-size: 9px; }}
        .test-badge {{ background: #f59e0b; color: white; padding: 2px 6px; border-radius: 3px; font-size: 9px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="nav-section">Navigation</div>
            <a href="/" class="nav-link">🏠 Home</a>
            
            <div class="nav-section">Quick Looks</div>
            <a href="/live_positions" class="nav-link">💰 Live Positions</a>
            <a href="/test_positions" class="nav-link">🧪 Test Positions</a>
            <a href="/balances" class="nav-link">💳 Balances</a>
            <a href="/markets" class="nav-link">🌐 Markets</a>
            
            <div class="nav-section">Performance</div>
            <a href="/live_performance" class="nav-link">📈 Live Performance</a>
            <a href="/test_performance" class="nav-link">🧪 Test Performance</a>
            <a href="/combined_performance" class="nav-link">📊 Combined</a>
            
            <div class="nav-section">Time Periods</div>
            <a href="/today" class="nav-link">📅 Today</a>
            <a href="/week" class="nav-link">📅 This Week</a>
            <a href="/month" class="nav-link">📅 This Month</a>
        </div>
        
        <div class="main">
            <h1>💰 CBTrade Live/Test Dashboard</h1>
            
            <!-- REAL MONEY OVERVIEW -->
            <div class="balance-card">
                <h2>💰 REAL MONEY OVERVIEW</h2>
                <div class="balance-metrics">
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('currencies', 0)}</div>
                        <div class="label">Currencies</div>
                    </div>
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('total_portfolio', '$ 0')}</div>
                        <div class="label">Total Portfolio</div>
                    </div>
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('available_cash', '$ 0')}</div>
                        <div class="label">Available Cash</div>
                    </div>
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('live_invested', '$ 0')}</div>
                        <div class="label">Live Invested</div>
                    </div>
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('live_value', '$ 0')}</div>
                        <div class="label">Live Value</div>
                    </div>
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('live_positions', 0)}</div>
                        <div class="label">Live Positions</div>
                    </div>
                </div>
            </div>
            
            <!-- TEST MONEY OVERVIEW -->
            <div class="balance-card">
                <h2>🧪 TEST TRADING OVERVIEW</h2>
                <div class="balance-metrics">
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('test_invested', '$ 0')}</div>
                        <div class="label">Test Invested</div>
                    </div>
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('test_value', '$ 0')}</div>
                        <div class="label">Test Value</div>
                    </div>
                    <div class="balance-metric">
                        <div class="value">{balance_data.get('test_positions', 0)}</div>
                        <div class="label">Test Positions</div>
                    </div>
                </div>
            </div>
            
            <!-- LIVE TRADING SUMMARY -->
            <div class="report-section live-section">
                <h2>💰 LIVE TRADING - ALL TIME SUMMARY</h2>
                <table>
                    <thead>
                        <tr>
                            <th>tot_cnt</th><th>win_cnt</th><th>lose_cnt</th><th>win_pct</th><th>lose_pct</th>
                            <th>gain_amt</th><th>loss_amt</th><th>gain_loss_amt</th><th>gain_loss_pct</th>
                            <th>gain_loss_pct_hr</th><th>avg_hours</th><th>tot_out_cnt</th><th>fees_cnt_tot</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="summary-row">
                            <td>{live_summary.get('tot_cnt', 0)}</td>
                            <td>{live_summary.get('win_cnt', 0)}</td>
                            <td>{live_summary.get('lose_cnt', 0)}</td>
                            <td>{live_summary.get('win_pct', 0):.1f}%</td>
                            <td>{live_summary.get('lose_pct', 0):.1f}%</td>
                            <td class="positive">${live_summary.get('gain_amt', 0):,.2f}</td>
                            <td class="negative">${live_summary.get('loss_amt', 0):,.2f}</td>
                            <td class="{'positive' if live_summary.get('gain_loss_amt', 0) > 0 else 'negative'}">${live_summary.get('gain_loss_amt', 0):,.2f}</td>
                            <td class="{'positive' if live_summary.get('gain_loss_pct', 0) > 0 else 'negative'}">{live_summary.get('gain_loss_pct', 0):.2f}%</td>
                            <td class="{'positive' if live_summary.get('gain_loss_pct_hr', 0) > 0 else 'negative'}">{live_summary.get('gain_loss_pct_hr', 0):.6f}%</td>
                            <td>{live_summary.get('age_hours', 0):.1f}</td>
                            <td>${live_summary.get('tot_out_cnt', 0):,.2f}</td>
                            <td>${live_summary.get('fees_cnt_tot', 0):,.2f}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <!-- LIVE OPEN POSITIONS BY MARKET -->
            <div class="report-section live-section">
                <h2>💰 LIVE OPEN POSITIONS - BY MARKET</h2>
                <table>
                    <thead>
                        <tr>
                            <th>prod_id</th><th>positions</th><th>currently_winning</th><th>currently_losing</th>
                            <th>win_pct</th><th>unrealized_pnl</th><th>gain_loss_pct</th><th>pct_per_hour</th>
                            <th>invested</th><th>current_value</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for market in live_open_data:
            pnl_class = "positive" if market.get('gain_loss_amt', 0) > 0 else "negative" if market.get('gain_loss_amt', 0) < 0 else ""
            win_class = "positive" if market.get('win_pct', 0) > 50 else "negative" if market.get('win_pct', 0) < 50 else ""
            hr_class = "positive" if market.get('gain_loss_pct_hr', 0) > 0 else "negative" if market.get('gain_loss_pct_hr', 0) < 0 else ""
            
            html += f"""
                        <tr>
                            <td><strong>{market.get('prod_id', '')}</strong></td>
                            <td>{market.get('tot_cnt', 0)}</td>
                            <td class="positive">{market.get('win_cnt', 0)}</td>
                            <td class="negative">{market.get('lose_cnt', 0)}</td>
                            <td class="{win_class}">{market.get('win_pct', 0):.1f}%</td>
                            <td class="{pnl_class}">${market.get('gain_loss_amt', 0):,.2f}</td>
                            <td class="{pnl_class}">{market.get('gain_loss_pct', 0):.2f}%</td>
                            <td class="{hr_class}">{market.get('gain_loss_pct_hr', 0):.6f}%</td>
                            <td>${market.get('tot_out_cnt', 0):,.2f}</td>
                            <td>${market.get('val_tot', 0):,.2f}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
            
            <!-- TEST OPEN POSITIONS BY MARKET -->
            <div class="report-section test-section">
                <h2>🧪 TEST OPEN POSITIONS - BY MARKET</h2>
                <table>
                    <thead>
                        <tr>
                            <th>prod_id</th><th>positions</th><th>currently_winning</th><th>currently_losing</th>
                            <th>win_pct</th><th>unrealized_pnl</th><th>invested</th><th>current_value</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for market in test_open_data:
            pnl_class = "positive" if market.get('gain_loss_amt', 0) > 0 else "negative" if market.get('gain_loss_amt', 0) < 0 else ""
            win_class = "positive" if market.get('win_pct', 0) > 50 else "negative" if market.get('win_pct', 0) < 50 else ""
            
            html += f"""
                        <tr>
                            <td><strong>{market.get('prod_id', '')}</strong> <span class="test-badge">TEST</span></td>
                            <td>{market.get('tot_cnt', 0)}</td>
                            <td class="positive">{market.get('win_cnt', 0)}</td>
                            <td class="negative">{market.get('lose_cnt', 0)}</td>
                            <td class="{win_class}">{market.get('win_pct', 0):.1f}%</td>
                            <td class="{pnl_class}">${market.get('gain_loss_amt', 0):,.2f}</td>
                            <td>${market.get('tot_out_cnt', 0):,.2f}</td>
                            <td>${market.get('val_tot', 0):,.2f}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return html
        
    except Exception as e:
        return f"<h1>Dashboard Error: {str(e)}</h1><pre>{type(e)}</pre>"

@app.route('/live_positions')
def live_positions():
    """Live positions only - real money"""
    try:
        sql = """
        SELECT p.pos_id, p.prod_id, p.buy_strat_name, p.buy_strat_freq,
               ROUND((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600, 1) as hours_held,
               ROUND(p.tot_out_cnt, 2) as invested,
               ROUND(p.val_tot, 2) as current_value,
               ROUND(p.gain_loss_amt, 2) as unrealized_pnl,
               ROUND(p.gain_loss_amt / p.tot_out_cnt * 100, 4) as unrealized_pct
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'N' AND p.pos_stat = 'OPEN'
        ORDER BY p.gain_loss_amt DESC
        """
        positions = db.seld(sql)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CBTrade - Live Positions</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%); color: white; }}
        h1 {{ color: #fbbf24; margin: 20px; }}
        .live-badge {{ background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }}
        table {{ background: white; color: black; margin: 20px; border-collapse: collapse; width: calc(100% - 40px); }}
        th {{ background: #10b981; color: white; padding: 10px 8px; text-align: center; }}
        td {{ padding: 8px; border: 1px solid #ddd; text-align: center; }}
        .positive {{ background: #dcfce7; color: #166534; font-weight: bold; }}
        .negative {{ background: #fee2e2; color: #dc2626; font-weight: bold; }}
        .nav {{ margin: 20px; }}
        .nav a {{ color: #e2e8f0; margin-right: 15px; }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">🏠 Dashboard</a>
        <a href="/live_positions"><strong>💰 Live Positions</strong></a>
        <a href="/test_positions">🧪 Test Positions</a>
    </div>
    
    <h1>💰 Live Trading Positions <span class="live-badge">REAL MONEY</span></h1>
    
    <table>
        <thead>
            <tr>
                <th>Position ID</th><th>Product</th><th>Strategy</th><th>Frequency</th>
                <th>Hours Held</th><th>Invested</th><th>Current Value</th><th>Unrealized P&L</th><th>Unrealized %</th>
            </tr>
        </thead>
        <tbody>
        """
        
        for pos in positions:
            pnl_class = "positive" if pos.get('unrealized_pnl', 0) > 0 else "negative" if pos.get('unrealized_pnl', 0) < 0 else ""
            
            html += f"""
            <tr>
                <td><strong>#{pos.get('pos_id', '')}</strong></td>
                <td><strong>{pos.get('prod_id', '')}</strong></td>
                <td>{pos.get('buy_strat_name', '')}</td>
                <td>{pos.get('buy_strat_freq', '')}</td>
                <td>{pos.get('hours_held', 0):.1f}h</td>
                <td>${pos.get('invested', 0):,.2f}</td>
                <td>${pos.get('current_value', 0):,.2f}</td>
                <td class="{pnl_class}">${pos.get('unrealized_pnl', 0):,.2f}</td>
                <td class="{pnl_class}">{pos.get('unrealized_pct', 0):.2f}%</td>
            </tr>
            """
        
        html += """
        </tbody>
    </table>
</body>
</html>
        """
        
        return html
        
    except Exception as e:
        return f"<h1>Live Positions Error: {str(e)}</h1>"

@app.route('/test_positions')
def test_positions():
    """Test positions only - training data"""
    try:
        sql = """
        SELECT p.pos_id, p.prod_id, p.buy_strat_name, p.buy_strat_freq,
               ROUND((UNIX_TIMESTAMP() - p.pos_begin_unix) / 3600, 1) as hours_held,
               ROUND(p.tot_out_cnt, 2) as invested,
               ROUND(p.val_tot, 2) as current_value,
               ROUND(p.gain_loss_amt, 2) as unrealized_pnl,
               ROUND(p.gain_loss_amt / p.tot_out_cnt * 100, 4) as unrealized_pct
        FROM cbtrade.poss p
        WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'Y' AND p.pos_stat = 'OPEN'
        ORDER BY p.gain_loss_amt DESC
        """
        positions = db.seld(sql)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CBTrade - Test Positions</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%); color: white; }}
        h1 {{ color: #fbbf24; margin: 20px; }}
        .test-badge {{ background: #f59e0b; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }}
        table {{ background: white; color: black; margin: 20px; border-collapse: collapse; width: calc(100% - 40px); }}
        th {{ background: #f59e0b; color: white; padding: 10px 8px; text-align: center; }}
        td {{ padding: 8px; border: 1px solid #ddd; text-align: center; }}
        .positive {{ background: #dcfce7; color: #166534; font-weight: bold; }}
        .negative {{ background: #fee2e2; color: #dc2626; font-weight: bold; }}
        .nav {{ margin: 20px; }}
        .nav a {{ color: #e2e8f0; margin-right: 15px; }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">🏠 Dashboard</a>
        <a href="/live_positions">💰 Live Positions</a>
        <a href="/test_positions"><strong>🧪 Test Positions</strong></a>
    </div>
    
    <h1>🧪 Test Trading Positions <span class="test-badge">TRAINING DATA</span></h1>
    
    <table>
        <thead>
            <tr>
                <th>Position ID</th><th>Product</th><th>Strategy</th><th>Frequency</th>
                <th>Hours Held</th><th>Invested</th><th>Current Value</th><th>Unrealized P&L</th><th>Unrealized %</th>
            </tr>
        </thead>
        <tbody>
        """
        
        for pos in positions:
            pnl_class = "positive" if pos.get('unrealized_pnl', 0) > 0 else "negative" if pos.get('unrealized_pnl', 0) < 0 else ""
            
            html += f"""
            <tr>
                <td><strong>#{pos.get('pos_id', '')}</strong></td>
                <td><strong>{pos.get('prod_id', '')}</strong></td>
                <td>{pos.get('buy_strat_name', '')}</td>
                <td>{pos.get('buy_strat_freq', '')}</td>
                <td>{pos.get('hours_held', 0):.1f}h</td>
                <td>${pos.get('invested', 0):,.2f}</td>
                <td>${pos.get('current_value', 0):,.2f}</td>
                <td class="{pnl_class}">${pos.get('unrealized_pnl', 0):,.2f}</td>
                <td class="{pnl_class}">{pos.get('unrealized_pct', 0):.2f}%</td>
            </tr>
            """
        
        html += """
        </tbody>
    </table>
</body>
</html>
        """
        
        return html
        
    except Exception as e:
        return f"<h1>Test Positions Error: {str(e)}</h1>"

if __name__ == '__main__':
    print("🎯 CBTrade FINAL Dashboard - Proper Live/Test/All Separation")
    print("📊 Main Dashboard:    http://127.0.0.1:8096/")
    print("💰 Live Positions:   http://127.0.0.1:8096/live_positions")
    print("🧪 Test Positions:   http://127.0.0.1:8096/test_positions")
    print("")
    print("✅ Live trades only (test_txn_yn='N') - REAL MONEY")
    print("✅ Test trades only (test_txn_yn='Y') - TRAINING DATA")
    print("✅ Proper data separation and accurate amounts")
    print("✅ Readable summary rows with proper contrast")
    
    app.run(host='0.0.0.0', debug=True, port=8096)
