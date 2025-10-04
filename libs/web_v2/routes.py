# Clean Flask Routes - CBTrade Web v2.0
from flask import Flask, render_template, request, jsonify
from libs.web_v2.controllers.dashboard import DashboardController
from libs.web_v2.controllers.balances import BalancesController  
from libs.web_v2.controllers.performance import PerformanceController
from libs.web_v2.controllers.positions import PositionsController
import traceback


# Initialize Flask app (templates now in standard location)
app = Flask(__name__)

# Initialize controllers
dashboard = DashboardController()
balances = BalancesController()
performance = PerformanceController()
positions = PositionsController()


def handle_error(e, endpoint_name):
    """Standard error handling for all endpoints"""
    print(f"Error in {endpoint_name}: {e}")
    traceback.print_exc()
    return render_template('error.html', 
                         error_message=f"An error occurred in {endpoint_name}",
                         error_details=str(e))


# =============================================================================
# DASHBOARD ROUTES
# =============================================================================

@app.route('/')
@app.route('/dashboard')
def dashboard_home():
    """Main dashboard - what happened today, week, month, year"""
    try:
        data = dashboard.get_dashboard_data(['today', 'week', 'month', 'year'])
        return render_template('dashboard/home.html', 
                             title='CBTrade Dashboard',
                             data=data)
    except Exception as e:
        return handle_error(e, 'Dashboard Home')


@app.route('/dashboard/<period>')
def dashboard_period(period):
    """Specific time period dashboard"""
    try:
        valid_periods = ['today', 'yesterday', 'week', 'month', 'year', 'last_7_days', 'last_30_days']
        if period not in valid_periods:
            period = 'today'
            
        data = {
            'period': period,
            'summary': dashboard.get_period_summary(period),
            'by_market': dashboard.get_period_by_market(period)
        }
        return render_template('dashboard/period.html',
                             title=f'CBTrade - {period.title()}',
                             data=data)
    except Exception as e:
        return handle_error(e, f'Dashboard {period}')


# =============================================================================
# BALANCE ROUTES  
# =============================================================================

@app.route('/balances')
def balances_home():
    """Balance overview with pocket/clips and out-of-balance detection"""
    try:
        data = balances.get_balances_dashboard()
        return render_template('balances/home.html',
                             title='Account Balances',
                             data=data)
    except Exception as e:
        return handle_error(e, 'Balances Home')


@app.route('/balances/out-of-balance')
def balances_out_of_balance():
    """Focus view for out-of-balance items"""
    try:
        data = {
            'summary': balances.get_balance_summary(),
            'out_of_balance': balances.get_out_of_balance_items()
        }
        return render_template('balances/out_of_balance.html',
                             title='Out of Balance Items',
                             data=data)
    except Exception as e:
        return handle_error(e, 'Out of Balance')


@app.route('/balances/pocket-clips')
def balances_pocket_clips():
    """Detailed pocket and clips breakdown"""
    try:
        data = {
            'summary': balances.get_balance_summary(),
            'breakdown': balances.get_pocket_clip_breakdown()
        }
        return render_template('balances/pocket_clips.html',
                             title='Pocket & Clips Breakdown',
                             data=data)
    except Exception as e:
        return handle_error(e, 'Pocket Clips')


# =============================================================================
# POSITION ROUTES
# =============================================================================

@app.route('/positions')
def positions_home():
    """Open positions overview"""
    try:
        sort_by = request.args.get('sort', 'pnl_desc')
        data = positions.get_positions_dashboard(sort_by)
        return render_template('positions/home.html',
                             title='Open Positions',
                             data=data,
                             current_sort=sort_by)
    except Exception as e:
        return handle_error(e, 'Positions Home')


@app.route('/positions/at-risk')
def positions_at_risk():
    """Positions that need attention"""
    try:
        loss_threshold = float(request.args.get('loss_threshold', -5.0))
        age_threshold = int(request.args.get('age_threshold', 24))
        
        data = {
            'at_risk': positions.get_positions_at_risk(loss_threshold, age_threshold),
            'loss_threshold': loss_threshold,
            'age_threshold': age_threshold
        }
        return render_template('positions/at_risk.html',
                             title='Positions At Risk',
                             data=data)
    except Exception as e:
        return handle_error(e, 'Positions At Risk')


# =============================================================================
# PERFORMANCE ROUTES
# =============================================================================

@app.route('/performance')
def performance_home():
    """Overall performance analysis"""
    try:
        test_mode = request.args.get('test_mode', 'N')
        data = performance.get_performance_dashboard(test_mode)
        return render_template('performance/home.html',
                             title='Performance Analysis',
                             data=data,
                             test_mode=test_mode)
    except Exception as e:
        return handle_error(e, 'Performance Home')


@app.route('/performance/by-product')
def performance_by_product():
    """Performance breakdown by product"""
    try:
        test_mode = request.args.get('test_mode', 'N') 
        min_positions = int(request.args.get('min_positions', 5))
        
        data = {
            'by_product': performance.get_performance_by_product(test_mode, min_positions),
            'overall': performance.get_overall_performance(test_mode)
        }
        return render_template('performance/by_product.html',
                             title='Performance by Product',
                             data=data,
                             test_mode=test_mode)
    except Exception as e:
        return handle_error(e, 'Performance by Product')


@app.route('/performance/by-strategy') 
def performance_by_strategy():
    """Performance breakdown by strategy"""
    try:
        test_mode = request.args.get('test_mode', 'N')
        min_positions = int(request.args.get('min_positions', 5))
        
        data = {
            'by_strategy': performance.get_performance_by_strategy(test_mode, min_positions),
            'overall': performance.get_overall_performance(test_mode)
        }
        return render_template('performance/by_strategy.html',
                             title='Performance by Strategy', 
                             data=data,
                             test_mode=test_mode)
    except Exception as e:
        return handle_error(e, 'Performance by Strategy')


@app.route('/performance/drill-down')
def performance_drill_down():
    """Detailed drill-down performance analysis"""
    try:
        # Get filter parameters
        product = request.args.get('product')
        strategy = request.args.get('strategy')
        strategy_freq = request.args.get('strategy_freq')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        test_mode = request.args.get('test_mode', 'N')
        
        data = {
            'positions': performance.get_drill_down_performance(
                product=product,
                strategy=strategy, 
                strategy_freq=strategy_freq,
                start_date=start_date,
                end_date=end_date,
                test_mode=test_mode
            ),
            'filters': {
                'product': product,
                'strategy': strategy,
                'strategy_freq': strategy_freq, 
                'start_date': start_date,
                'end_date': end_date,
                'test_mode': test_mode
            }
        }
        return render_template('performance/drill_down.html',
                             title='Performance Drill-down',
                             data=data)
    except Exception as e:
        return handle_error(e, 'Performance Drill-down')


# =============================================================================
# API ENDPOINTS (JSON)
# =============================================================================

@app.route('/api/dashboard/<period>')
def api_dashboard_period(period):
    """JSON API for dashboard data"""
    try:
        data = dashboard.get_dashboard_data([period])
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/balances/summary')
def api_balances_summary():
    """JSON API for balance summary"""
    try:
        data = balances.get_balance_summary()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/positions/open')
def api_positions_open():
    """JSON API for open positions"""
    try:
        sort_by = request.args.get('sort', 'pnl_desc')
        data = positions.get_open_positions(sort_by)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================================================================
# UTILITY ROUTES
# =============================================================================

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    try:
        # Test database connectivity
        test_data = dashboard.get_period_summary('today')
        from datetime import date
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': date.today().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy', 
            'error': str(e)
        }), 500

@app.route('/test')
def test_page():
    """Simple test page to verify templates work"""
    try:
        return render_template('base.html')
    except Exception as e:
        return f"Template error: {str(e)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
