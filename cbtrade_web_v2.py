# CBTrade Web v2.0 - Working Simple Version  
from flask import Flask, jsonify, render_template_string, request
from libs.web_v2.controllers.balances import BalancesController
from libs.web_v2.controllers.dashboard import DashboardController
from libs.web_v2.controllers.performance import PerformanceController
from libs.web_v2.controllers.positions import PositionsController

app = Flask(__name__)

# Initialize all controllers
balances_controller = BalancesController()
dashboard_controller = DashboardController()
performance_controller = PerformanceController()
positions_controller = PositionsController()

@app.route('/')
def home():
    """Simple home page"""
    try:
        balance_summary = balances_controller.get_balance_summary()
        open_summary = dashboard_controller.get_open_positions_summary()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CBTrade v2.0 - Working!</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .metric {{ display: inline-block; margin: 20px; padding: 20px; border: 1px solid #ccc; }}
                .positive {{ color: green; }}
                .negative {{ color: red; }}
                .neutral {{ color: gray; }}
            </style>
        </head>
        <body>
            <h1>🎉 CBTrade Web v2.0 - WORKING!</h1>
            
            <h2>💰 Portfolio Summary</h2>
            <div class="metric">
                <strong>Total Portfolio:</strong><br>
                ${balance_summary.get('total_portfolio_value', 0):,.2f}
            </div>
            <div class="metric">
                <strong>Available Cash:</strong><br>
                ${balance_summary.get('available_value', 0):,.2f}
            </div>
            <div class="metric">
                <strong>Open Positions:</strong><br>
                {balance_summary.get('total_open_positions', 0)}
            </div>
            <div class="metric">
                <strong>Out-of-Balance Items:</strong><br>
                <span class="{'negative' if balance_summary.get('out_of_balance_count', 0) > 0 else 'positive'}">
                    {balance_summary.get('out_of_balance_count', 0)}
                </span>
            </div>
            
            <h2>📈 Position Summary</h2>
            <div class="metric">
                <strong>Total Invested:</strong><br>
                ${open_summary.get('total_invested', 0):,.2f}
            </div>
            <div class="metric">
                <strong>Current Value:</strong><br>
                ${open_summary.get('current_value', 0):,.2f}
            </div>
            <div class="metric">
                <strong>Unrealized P&L:</strong><br>
                <span class="{'positive' if open_summary.get('unrealized_pnl', 0) > 0 else 'negative' if open_summary.get('unrealized_pnl', 0) < 0 else 'neutral'}">
                    ${open_summary.get('unrealized_pnl', 0):,.2f}
                </span>
            </div>
            <div class="metric">
                <strong>Avg Hold Time:</strong><br>
                {open_summary.get('avg_hours_held', 0):.1f} hours
            </div>
            
            <h2>🔗 Navigation</h2>
            <p>
                <a href="/balances">View Balances</a> | 
                <a href="/positions">Open Positions</a> | 
                <a href="/api/summary">JSON Data</a>
            </p>
        </body>
        </html>
        """
        return html
        
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1><pre>{type(e)}</pre>"

@app.route('/api/summary')
def api_summary():
    """JSON summary for testing"""
    try:
        balance_summary = balances_controller.get_balance_summary()
        return jsonify(balance_summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/balances')
def balances_full():
    """Complete balance management view"""
    try:
        balance_data = balances_controller.get_balances_dashboard()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CBTrade - Account Balances</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .nav {{ margin-bottom: 20px; }}
                .nav a {{ margin-right: 15px; color: blue; text-decoration: none; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ccc; text-align: center; }}
                .positive {{ color: green; font-weight: bold; }}
                .negative {{ color: red; font-weight: bold; }}
                .neutral {{ color: gray; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
                th {{ background-color: #f0f0f0; }}
                .alert {{ background-color: #ffe6e6; border: 1px solid red; padding: 15px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/">🏠 Dashboard</a>
                <a href="/balances"><strong>💰 Balances</strong></a>
                <a href="/positions">📈 Positions</a>
                <a href="/performance">📊 Performance</a>
                <a href="/time/today">📅 Today</a>
                <a href="/time/week">📅 Week</a>
                <a href="/time/month">📅 Month</a>
            </div>
            
            <h1>💰 Account Balances</h1>
            
            <!-- Portfolio Summary -->
            <div style="border: 2px solid #333; padding: 20px; margin: 20px 0;">
                <h2>Portfolio Summary</h2>
                <div class="metric">
                    <strong>Total Value:</strong><br>
                    ${balance_data['summary'].get('total_portfolio_value', 0):,.2f}
                </div>
                <div class="metric">
                    <strong>Available Cash:</strong><br>
                    ${balance_data['summary'].get('available_value', 0):,.2f}
                </div>
                <div class="metric">
                    <strong>Invested:</strong><br>
                    ${balance_data['summary'].get('total_invested', 0):,.2f}
                </div>
                <div class="metric">
                    <strong>Open Positions:</strong><br>
                    {balance_data['summary'].get('total_open_positions', 0)}
                </div>
                <div class="metric">
                    <strong>Pocket Value:</strong><br>
                    ${balance_data['summary'].get('total_pocket_value', 0):,.2f}
                </div>
                <div class="metric">
                    <strong>Clip Value:</strong><br>
                    ${balance_data['summary'].get('total_clip_value', 0):,.2f}
                </div>
                <div class="metric">
                    <strong>Out-of-Balance:</strong><br>
                    <span class="{'negative' if balance_data['summary'].get('out_of_balance_count', 0) > 0 else 'positive'}">
                        {balance_data['summary'].get('out_of_balance_count', 0)} items
                    </span>
                </div>
            </div>
        """
        
        # Out-of-balance alert
        if balance_data['out_of_balance'] and len(balance_data['out_of_balance']) > 0:
            html += f"""
            <div class="alert">
                <h3>⚠️ OUT-OF-BALANCE ALERT</h3>
                <p><strong>{len(balance_data['out_of_balance'])} currencies have balance discrepancies!</strong></p>
                <table>
                    <tr><th>Currency</th><th>Exchange Balance</th><th>Calculated</th><th>Variance</th><th>USD Impact</th></tr>
            """
            for item in balance_data['out_of_balance'][:10]:
                variance_color = "positive" if item.get('variance', 0) > 0 else "negative" if item.get('variance', 0) < 0 else "neutral"
                html += f"""
                    <tr>
                        <td><strong>{item.get('symb')}</strong></td>
                        <td>{item.get('exchange_balance', 0):.8f}</td>
                        <td>{item.get('calculated_balance', 0):.8f}</td>
                        <td class="{variance_color}">{item.get('variance', 0):.8f}</td>
                        <td class="{variance_color}">${item.get('variance_usd', 0):,.2f}</td>
                    </tr>
                """
            html += "</table></div>"
        
        # Current balances table
        html += """
            <h2>Current Balances</h2>
            <table>
                <tr>
                    <th>Currency</th>
                    <th>Total Balance</th>
                    <th>Position Holdings</th>
                    <th>Variance</th>
                    <th>USD Value</th>
                    <th>Open Pos</th>
                    <th>Status</th>
                </tr>
        """
        
        for bal in balance_data['balances'][:20]:
            status_color = "red" if bal.get('balance_status') == 'OUT_OF_BALANCE' else "green"
            variance_color = "positive" if bal.get('balance_variance', 0) > 0 else "negative" if bal.get('balance_variance', 0) < 0 else "neutral"
            html += f"""
                <tr>
                    <td><strong>{bal.get('symb')}</strong></td>
                    <td>{bal.get('total_balance', 0):.8f}</td>
                    <td>{bal.get('position_holdings', 0):.8f}</td>
                    <td class="{variance_color}">{bal.get('balance_variance', 0):.8f}</td>
                    <td>${bal.get('value_usd', 0):,.2f}</td>
                    <td>{bal.get('open_positions', 0)}</td>
                    <td style="color: {status_color}"><strong>{bal.get('balance_status', 'UNKNOWN')}</strong></td>
                </tr>
            """
        
        html += "</table></body></html>"
        return html
        
    except Exception as e:
        return f"<h1>Balances Error: {str(e)}</h1><pre>{type(e)}</pre>"

@app.route('/positions')
def positions_view():
    """Open positions view"""
    try:
        positions_data = positions_controller.get_positions_dashboard()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CBTrade - Open Positions</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .nav {{ margin-bottom: 20px; }}
                .nav a {{ margin-right: 15px; color: blue; text-decoration: none; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ccc; text-align: center; }}
                .positive {{ color: green; font-weight: bold; }}
                .negative {{ color: red; font-weight: bold; }}
                .neutral {{ color: gray; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
                th {{ background-color: #f0f0f0; }}
                .alert {{ background-color: #fff3cd; border: 1px solid orange; padding: 15px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/">🏠 Dashboard</a>
                <a href="/balances">💰 Balances</a>
                <a href="/positions"><strong>📈 Positions</strong></a>
                <a href="/performance">📊 Performance</a>
                <a href="/time/today">📅 Today</a>
                <a href="/time/week">📅 Week</a>
                <a href="/time/month">📅 Month</a>
            </div>
            
            <h1>📈 Open Positions</h1>
            
            <!-- Positions Summary by Product -->
            <h2>Summary by Product</h2>
            <table>
                <tr>
                    <th>Product</th>
                    <th>Count</th>
                    <th>Invested</th>
                    <th>Current Value</th>
                    <th>Unrealized P&L</th>
                    <th>Win/Lose</th>
                    <th>Avg Age (hrs)</th>
                </tr>
        """
        
        for product in positions_data['by_product'][:15]:
            pnl_color = "positive" if product.get('total_unrealized_pnl', 0) > 0 else "negative" if product.get('total_unrealized_pnl', 0) < 0 else "neutral"
            html += f"""
                <tr>
                    <td><strong>{product.get('prod_id')}</strong></td>
                    <td>{product.get('open_count', 0)}</td>
                    <td>${product.get('total_invested', 0):,.2f}</td>
                    <td>${product.get('current_value', 0):,.2f}</td>
                    <td class="{pnl_color}">${product.get('total_unrealized_pnl', 0):,.2f}</td>
                    <td><span class="positive">{product.get('currently_winning', 0)}</span> / <span class="negative">{product.get('currently_losing', 0)}</span></td>
                    <td>{product.get('avg_hours_held', 0):.1f}h</td>
                </tr>
            """
        
        # At-risk positions alert
        if positions_data['at_risk'] and len(positions_data['at_risk']) > 0:
            html += f"""
            </table>
            <div class="alert">
                <h3>⚠️ POSITIONS NEEDING ATTENTION</h3>
                <p><strong>{len(positions_data['at_risk'])} positions may need attention (losing >5% or held >24h)</strong></p>
                <table>
                    <tr><th>Position</th><th>Product</th><th>Strategy</th><th>P&L</th><th>%</th><th>Hold Time</th><th>Risk</th></tr>
            """
            for pos in positions_data['at_risk'][:10]:
                html += f"""
                    <tr>
                        <td><strong>#{pos.get('pos_id')}</strong></td>
                        <td>{pos.get('prod_id')}</td>
                        <td>{pos.get('buy_strat_name')}-{pos.get('buy_strat_freq')}</td>
                        <td class="negative">${pos.get('unrealized_pnl', 0):,.2f}</td>
                        <td class="negative">{pos.get('unrealized_pct', 0):.2f}%</td>
                        <td>{pos.get('hours_held', 0):.1f}h</td>
                        <td>{pos.get('risk_category', '').replace('_', ' ')}</td>
                    </tr>
                """
            html += "</table></div>"
        
        html += "</body></html>"
        return html
        
    except Exception as e:
        return f"<h1>Positions Error: {str(e)}</h1><pre>{type(e)}</pre>"

@app.route('/performance')
def performance_view():
    """Performance analysis view"""
    try:
        test_mode = request.args.get('test_mode', 'N')
        perf_data = performance_controller.get_performance_dashboard(test_mode)
        
        mode_name = "Live Trading" if test_mode == 'N' else "Test Mode" if test_mode == 'Y' else "All Trades"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CBTrade - Performance Analysis</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .nav {{ margin-bottom: 20px; }}
                .nav a {{ margin-right: 15px; color: blue; text-decoration: none; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ccc; text-align: center; }}
                .positive {{ color: green; font-weight: bold; }}
                .negative {{ color: red; font-weight: bold; }}
                .neutral {{ color: gray; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
                th {{ background-color: #f0f0f0; }}
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/">🏠 Dashboard</a>
                <a href="/balances">💰 Balances</a>
                <a href="/positions">📈 Positions</a>
                <a href="/performance"><strong>📊 Performance</strong></a> |
                <a href="/performance?test_mode=N">Live</a>
                <a href="/performance?test_mode=Y">Test</a>
            </div>
            
            <h1>📊 Performance Analysis - {mode_name}</h1>
            
            <!-- Overall Performance -->
            <div style="border: 2px solid #333; padding: 20px; margin: 20px 0;">
                <h2>Overall Performance</h2>
                <div class="metric">
                    <strong>Total Positions:</strong><br>
                    {perf_data['overall'].get('total_positions', 0)}
                </div>
                <div class="metric">
                    <strong>Win Rate:</strong><br>
                    <span class="{'positive' if perf_data['overall'].get('win_rate', 0) > 50 else 'negative'}">
                        {perf_data['overall'].get('win_rate', 0):.1f}%
                    </span>
                </div>
                <div class="metric">
                    <strong>Total P&L:</strong><br>
                    <span class="{'positive' if perf_data['overall'].get('total_pnl', 0) > 0 else 'negative' if perf_data['overall'].get('total_pnl', 0) < 0 else 'neutral'}">
                        ${perf_data['overall'].get('total_pnl', 0):,.2f}
                    </span>
                </div>
                <div class="metric">
                    <strong>ROI:</strong><br>
                    <span class="{'positive' if perf_data['overall'].get('return_on_investment', 0) > 0 else 'negative' if perf_data['overall'].get('return_on_investment', 0) < 0 else 'neutral'}">
                        {perf_data['overall'].get('return_on_investment', 0):.2f}%
                    </span>
                </div>
            </div>
            
            <!-- Performance by Product -->
            <h2>Performance by Product</h2>
            <table>
                <tr>
                    <th>Product</th>
                    <th>Positions</th>
                    <th>Win Rate</th>
                    <th>Total P&L</th>
                    <th>ROI %</th>
                    <th>%/Hour</th>
                </tr>
        """
        
        for product in perf_data['by_product'][:15]:
            pnl_color = "positive" if product.get('total_pnl', 0) > 0 else "negative" if product.get('total_pnl', 0) < 0 else "neutral"
            win_color = "positive" if product.get('win_rate', 0) > 50 else "negative" if product.get('win_rate', 0) < 50 else "neutral"
            html += f"""
                <tr>
                    <td><strong>{product.get('prod_id')}</strong></td>
                    <td>{product.get('total_positions', 0)}</td>
                    <td class="{win_color}">{product.get('win_rate', 0) or 0:.1f}%</td>
                    <td class="{pnl_color}">${product.get('total_pnl', 0):,.2f}</td>
                    <td class="{pnl_color}">{product.get('roi_pct', 0) or 0:.2f}%</td>
                    <td class="{pnl_color}">{product.get('pct_per_hour', 0) or 0:.4f}%</td>
                </tr>
            """
        
        html += "</table></body></html>"
        return html
        
    except Exception as e:
        return f"<h1>Performance Error: {str(e)}</h1><pre>{type(e)}</pre>"

@app.route('/time/<period>')
def time_period_view(period):
    """Time-based performance views"""
    try:
        valid_periods = ['today', 'yesterday', 'week', 'month', 'year', 'last_7_days', 'last_30_days']
        if period not in valid_periods:
            period = 'today'
            
        summary = dashboard_controller.get_period_summary(period)
        by_market = dashboard_controller.get_period_by_market(period)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CBTrade - {period.title()} Performance</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .nav {{ margin-bottom: 20px; }}
                .nav a {{ margin-right: 15px; color: blue; text-decoration: none; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; border: 1px solid #ccc; text-align: center; }}
                .positive {{ color: green; font-weight: bold; }}
                .negative {{ color: red; font-weight: bold; }}
                .neutral {{ color: gray; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
                th {{ background-color: #f0f0f0; }}
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/">🏠 Dashboard</a>
                <a href="/balances">💰 Balances</a>
                <a href="/positions">📈 Positions</a>
                <a href="/performance">📊 Performance</a> |
                <a href="/time/today">📅 Today</a>
                <a href="/time/week">📅 Week</a>
                <a href="/time/month">📅 Month</a>
                <a href="/time/year">📅 Year</a>
            </div>
            
            <h1>📅 {period.title()} Performance</h1>
            
            <!-- Period Summary -->
            <div style="border: 2px solid #333; padding: 20px; margin: 20px 0;">
                <h2>{period.title()} Summary</h2>
                <div class="metric">
                    <strong>Positions:</strong><br>
                    {summary.get('total_positions', 0)}
                </div>
                <div class="metric">
                    <strong>Wins:</strong><br>
                    <span class="positive">{summary.get('wins', 0)}</span>
                </div>
                <div class="metric">
                    <strong>Losses:</strong><br>
                    <span class="negative">{summary.get('losses', 0)}</span>
                </div>
                <div class="metric">
                    <strong>Win Rate:</strong><br>
                    <span class="{'positive' if summary.get('win_rate', 0) > 50 else 'negative' if summary.get('win_rate', 0) < 50 else 'neutral'}">
                        {summary.get('win_rate', 0):.1f}%
                    </span>
                </div>
                <div class="metric">
                    <strong>Total P&L:</strong><br>
                    <span class="{'positive' if summary.get('total_pnl', 0) > 0 else 'negative' if summary.get('total_pnl', 0) < 0 else 'neutral'}">
                        ${summary.get('total_pnl', 0):,.2f}
                    </span>
                </div>
                <div class="metric">
                    <strong>Avg Hold:</strong><br>
                    {summary.get('avg_hours_held', 0):.1f}h
                </div>
            </div>
            
            <!-- Performance by Market -->
            <h2>{period.title()} Performance by Market</h2>
            <table>
                <tr>
                    <th>Market</th>
                    <th>Positions</th>
                    <th>Wins</th>
                    <th>Win Rate</th>
                    <th>Total P&L</th>
                    <th>Gain %</th>
                    <th>%/Hour</th>
                </tr>
        """
        
        for market in by_market[:20]:
            pnl_color = "positive" if market.get('total_pnl', 0) > 0 else "negative" if market.get('total_pnl', 0) < 0 else "neutral"
            win_color = "positive" if market.get('win_rate', 0) > 50 else "negative" if market.get('win_rate', 0) < 50 else "neutral"
            html += f"""
                <tr>
                    <td><strong>{market.get('prod_id')}</strong></td>
                    <td>{market.get('positions', 0)}</td>
                    <td>{market.get('wins', 0)}</td>
                    <td class="{win_color}">{market.get('win_rate', 0) or 0:.1f}%</td>
                    <td class="{pnl_color}">${market.get('total_pnl', 0):,.2f}</td>
                    <td class="{pnl_color}">{market.get('gain_pct', 0) or 0:.2f}%</td>
                    <td class="{pnl_color}">{market.get('pct_per_hour', 0) or 0:.4f}%</td>
                </tr>
            """
        
        html += "</table></body></html>"
        return html
        
    except Exception as e:
        return f"<h1>{period.title()} Error: {str(e)}</h1><pre>{type(e)}</pre>"

if __name__ == '__main__':
    print("🚀 CBTrade Web v2.0 - Complete Working System")
    print("📊 Dashboard:     http://127.0.0.1:8095/")
    print("💰 Balances:     http://127.0.0.1:8095/balances") 
    print("📈 Positions:    http://127.0.0.1:8095/positions")
    print("📊 Performance:  http://127.0.0.1:8095/performance")
    print("📅 Today:        http://127.0.0.1:8095/time/today")
    print("📅 This Week:    http://127.0.0.1:8095/time/week")
    print("📅 This Month:   http://127.0.0.1:8095/time/month")
    print("📅 This Year:    http://127.0.0.1:8095/time/year")
    print("🔗 JSON API:     http://127.0.0.1:8095/api/summary")
    app.run(host='0.0.0.0', debug=True, port=8095)
