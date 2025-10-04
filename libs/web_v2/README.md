# CBTrade Web Reporting v2.0 - Complete System Overhaul

🚀 **Complete replacement** for the old 3,391-line monolithic web system with a clean, fast, and maintainable architecture.

## 🎯 What You Asked For

✅ **Time-based Views**: Today, this week, this month, this year  
✅ **Balance Management**: Current balances with pocket/clips breakdown  
✅ **Out-of-Balance Detection**: Automatic variance detection and alerts  
✅ **Performance Drill-down**: By product, strategy, timeframe, or any combination  
✅ **Open Positions**: Real-time view of current positions with risk analysis  
✅ **Clean, Modern UI**: Simple design that's easy to extend  
✅ **Fast Performance**: Uses your existing performance tables for sub-second response  

## 🏗️ Clean Architecture

### Directory Structure
```
libs/web_v2/
├── __init__.py                    # Module init
├── routes.py                      # Clean Flask routes (200 lines vs 3,391!)
├── controllers/                   # Business logic (separated!)
│   ├── dashboard.py              # Time-based performance views
│   ├── balances.py               # Balance management & out-of-balance detection  
│   ├── performance.py            # Performance drill-down analysis
│   └── positions.py              # Open position management
├── models/
│   └── base.py                   # Clean data access patterns
└── templates/                    # Modern HTML templates
    ├── base.html                 # Clean, responsive base template
    ├── dashboard/home.html       # Main dashboard
    ├── balances/home.html        # Balance overview
    ├── performance/home.html     # Performance analysis
    └── positions/home.html       # Open positions
```

### Key Improvements

**📏 Size Reduction**: 3,391 lines → ~1,200 lines total (70% reduction!)  
**🚀 Performance**: Uses performance tables for sub-second response times  
**🧩 Modular**: Each controller handles one specific area  
**🎨 Modern UI**: Clean, responsive design with proper CSS  
**🔍 Smart Queries**: Optimized SQL using Unix timestamps for accuracy  
**📱 Mobile-Friendly**: Responsive design that works on all devices  

## 🚦 How to Use

### Start the New System
```bash
python run_web_v2.py
```

### Available URLs
```
Main Dashboard:       http://localhost:8080/
                     http://localhost:8080/dashboard

Time Periods:        http://localhost:8080/dashboard/today
                     http://localhost:8080/dashboard/week  
                     http://localhost:8080/dashboard/month
                     http://localhost:8080/dashboard/year

Balances:            http://localhost:8080/balances
Out-of-Balance:      http://localhost:8080/balances/out-of-balance
Pocket/Clips:        http://localhost:8080/balances/pocket-clips

Open Positions:      http://localhost:8080/positions
At-Risk Positions:   http://localhost:8080/positions/at-risk

Performance:         http://localhost:8080/performance
By Product:          http://localhost:8080/performance/by-product
By Strategy:         http://localhost:8080/performance/by-strategy
Drill-down:          http://localhost:8080/performance/drill-down

Health Check:        http://localhost:8080/health
```

### API Endpoints (JSON)
```
Dashboard Data:      http://localhost:8080/api/dashboard/today
Balance Summary:     http://localhost:8080/api/balances/summary
Open Positions:      http://localhost:8080/api/positions/open
```

## 🛠️ How to Extend (Easy!)

### Adding a New Report

1. **Add Controller Method**:
```python
# In libs/web_v2/controllers/dashboard.py
def get_my_new_report(self, param1=None):
    sql = """
    SELECT 
        column1,
        column2 
    FROM cbtrade.your_table 
    WHERE condition = %s
    """
    return self.execute_query(sql, "My New Report")
```

2. **Add Route**:
```python
# In libs/web_v2/routes.py
@app.route('/my-new-report')
def my_new_report():
    try:
        data = dashboard.get_my_new_report()
        return render_template('my_new_report.html', data=data)
    except Exception as e:
        return handle_error(e, 'My New Report')
```

3. **Add Template** (copy from existing templates and modify)

### Adding New Filters

1. **Update Controller**:
```python
def get_filtered_data(self, filter1=None, filter2=None):
    filters = ["base_condition = 1"]
    
    if filter1:
        filters.append(f"column1 = '{filter1}'")
    if filter2:
        filters.append(f"column2 = '{filter2}'")
        
    where_clause = " AND ".join(filters)
    # ... rest of SQL
```

2. **Update Route to Handle Parameters**:
```python
@app.route('/filtered-report')
def filtered_report():
    filter1 = request.args.get('filter1')
    filter2 = request.args.get('filter2')
    data = controller.get_filtered_data(filter1, filter2)
    # ... rest of route
```

## 🎨 UI Patterns

The new system uses consistent patterns you can follow:

### Card Layout
```html
<div class="card">
    <div class="card-header">
        <h2 class="card-title">Your Title</h2>
    </div>
    <div class="card-body">
        <!-- Content here -->
    </div>
</div>
```

### Metrics Display
```html
<div class="metric">
    <div class="metric-value positive">$1,234.56</div>
    <div class="metric-label">Your Metric</div>
</div>
```

### Data Tables
```html
<div class="table-container">
    <table class="table">
        <thead>
            <tr><th>Column 1</th><th class="text-right">Column 2</th></tr>
        </thead>
        <tbody>
            <tr><td>Data</td><td class="text-right positive">$123</td></tr>
        </tbody>
    </table>
</div>
```

### Color Classes
- `positive` - Green for gains/good values
- `negative` - Red for losses/bad values  
- `neutral` - Gray for neutral/zero values

## 🔧 Technical Features

### Auto-Refresh
- Dashboard: 30 seconds
- Positions: 30 seconds  
- Performance: 2 minutes
- Balances: 60 seconds

### Error Handling
- All endpoints have try/catch with proper error pages
- Database connection issues handled gracefully
- User-friendly error messages

### Performance Optimizations
- Uses your existing `trade_perfs` and `trade_strat_perfs` tables
- Unix timestamp-based calculations for accuracy
- Optimized queries with proper indexing
- Minimal database load

### Data Integrity
- Preserves all existing database tables (as requested)
- Uses existing data structures
- No destructive operations
- Safe for live trading system

## 🚀 Getting Started

1. **Backup complete** ✅ (you've already done this)
2. **Start new system**: `python run_web_v2.py`
3. **Open browser**: http://localhost:8080
4. **Explore**: Dashboard → Balances → Positions → Performance

The new system gives you everything you asked for in a clean, maintainable way that you can easily extend!
