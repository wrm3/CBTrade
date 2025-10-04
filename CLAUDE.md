# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CBTrade is a sophisticated cryptocurrency algorithmic trading bot built in Python that operates on the Coinbase Advanced Trader API. The system uses SQLite databases for data storage and employs multiple technical analysis strategies for automated trading decisions.

**Core Purpose**: Automate cryptocurrency trading on Coinbase spot markets using technical analysis strategies, with comprehensive position tracking, performance monitoring, and risk management.

## Key Architecture Components

### Database Architecture
- **Primary Database**: `db/cbtrade.db` (SQLite) - Core trading data including positions, orders, balances, and performance metrics
- **OHLCV Database**: `db/ohlcvs/` - Individual SQLite databases per trading pair for historical price data
- **Database Layer**: Uses custom SQLiteDB base class with schema management and connection handling
- **Key Tables**: `poss` (positions), `mkts` (markets), `buy_ords`/`sell_ords` (orders), `trade_perfs` (performance), `bals` (balances)

### Bot Architecture
- **Main Bot Class**: `libs/bot_base.py` - Central orchestrator inheriting from multiple base classes
- **Base Classes**: Modular architecture with `mkt_base`, `buy_base`, `sell_base`, `budget_base`, `pair_base`, etc.
- **Strategy System**: Plugin-based trading strategies in `libs/strats/` with template-driven development
- **Technical Analysis**: Pandas-based TA pipeline using pandas_ta library

### Strategy Framework
- **Location**: `libs/strats/` directory contains individual strategy files
- **Template**: Use `strat_TEMPLATE.py` as starting point for new strategies
- **Structure**: Each strategy implements `buy_strat_*` and `sell_strat_*` functions
- **Settings**: Strategy configurations in `settings_*` functions with frequency-based parameters
- **Common Functions**: Shared utilities in `_strat_common.py`

### Web Interface
- **Framework**: Flask-based web interface for monitoring and reporting
- **Entry Point**: `run_web.py` starts web server on port 8080
- **Templates**: HTML templates in `templates/` directory
- **Reports**: Comprehensive trading performance and position reporting

## Development Commands

### Running the Bot
```bash
# Manual trading mode (default)
python run_bot.py

# Automated trading mode  
python run_bot.py --auto

# Web interface (runs on http://localhost:8080)
python run_web.py
```

### Package Management
- **Tool**: Uses `pip` for dependency management
- **Config**: `requirements.txt` defines project dependencies
- **Python Version**: Requires Python 3.13+
- **Key Dependencies**: pandas, pandas-ta, coinbase-advanced-py, sqlite3, flask

### Database Operations
```python
# Database connections are handled automatically via:
from libs.db.cbtrade import CBTRADE_DB
from libs.db.ohlcv import OHLCV_DB

# Main database instance
cbtrade_db = CBTRADE_DB()

# OHLCV data access
ohlcv_db = OHLCV_DB()
```

## Critical Architecture Patterns

### Error Handling
- **Silent Killer Prevention**: Comprehensive exception handling with detailed logging
- **Critical Backup**: Automatic project backups on startup using `fstrent_bkitup`
- **Database Safety**: Connection retry logic and health monitoring

### Data Flow
1. **Market Data**: Coinbase API → Market objects → Database storage
2. **Technical Analysis**: OHLCV data → TA calculations → Strategy evaluation  
3. **Trading Decisions**: Strategy signals → Order placement → Position tracking
4. **Performance**: Trade results → Performance calculations → Reporting

### Configuration Management
- **Settings**: JSON configuration files in `settings/` directory
- **Environment**: `.env` file for API keys and database configuration
- **Strategy Config**: Each strategy defines its own settings structure

### Testing and Safety
- **Paper Trading**: `paper_trades_only_yn` setting prevents live trading
- **Position Limits**: Configurable maximum open positions per strategy/pair
- **Risk Management**: Stop-loss and take-profit mechanisms built into strategies

## Common Development Tasks

### Adding a New Trading Strategy
1. Copy `libs/strats/strat_TEMPLATE.py` to `libs/strats/strat_[name].py`
2. Implement `settings_[name]()`, `buy_strat_[name]()`, and `sell_strat_[name]()` functions
3. Add technical indicators in `ta_add_[indicator]()` functions
4. Test strategy logic and configure position limits

### Database Schema Updates
- Tables are auto-created via `get_required_tables()` in database classes
- Index definitions in `get_required_indexes()` for performance
- Use `insupd_ez()` for insert/update operations with validation

### Performance Optimization
- **Database Indexing**: Critical indexes on `prod_id`, `pos_stat`, `ord_stat` columns
- **Connection Management**: Thread-local SQLite connections with WAL mode
- **Data Efficiency**: Minimize database queries in trading loops

## Important File Locations
- **Main Entry**: `run_bot.py` - Bot startup and orchestration
- **Core Logic**: `libs/bot_base.py` - Main bot class with trading loops
- **Database**: `libs/db/cbtrade/db_main.py` - Database operations
- **Strategies**: `libs/strats/` - All trading strategy implementations
- **Configuration**: `settings/market_usdc.json` - Market and trading settings
- **Web Interface**: `run_web.py` and `libs/web.py` - Monitoring dashboard

## Security Notes
- API keys stored in `.env` file (not committed to repository)
- Database files contain sensitive trading data
- Paper trading mode should be enabled for development/testing
- Backup system creates timestamped project snapshots

## Dependencies and Environment
- **Python**: 3.13+ required
- **Key Libraries**: pandas, pandas-ta, numpy, sqlite3, flask, coinbase-advanced-py
- **Custom Packages**: fstrent-* packages for utilities (colors, charts, backup)
- **Development**: Uses pip for dependency management