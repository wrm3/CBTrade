# CBTrade System Architecture Registry

*Last Updated: 2025-07-29*

## Core Trading Subsystems

### Trading Engine
- **Components**: `run_bot.py`, `libs/bot_main.py`, `libs/bot_base.py`
- **Purpose**: Core trading loop, market scanning, and decision coordination
- **Dependencies**: Database Layer, API Integration, Strategy Framework
- **Interfaces**: Main bot entry point, market pair processing

### Strategy Framework  
- **Components**: `libs/strats/` directory (all strategy modules)
- **Purpose**: Algorithmic trading strategy implementations
- **Key Strategies**: Bollinger Bands (`strat_bb.py`), Breakouts (`strat_bb_bo.py`)
- **Dependencies**: Market Data, Technical Analysis, Risk Management
- **Interfaces**: Strategy execution, signal generation, position sizing

### Database Layer
- **Components**: `libs/db/` directory, SQLite databases in `db/`
- **Purpose**: Data persistence, performance tracking, order management
- **Key Modules**: `db_sqlite.py`, `cbtrade/db_main.py`, `ohlcv/db_main.py`
- **Dependencies**: None (foundational layer)
- **Interfaces**: CRUD operations, query optimization, backup systems

### API Integration
- **Components**: Coinbase API modules, market data handlers
- **Purpose**: External exchange communication and real-time data feeds
- **Dependencies**: Trading Engine, Database Layer
- **Interfaces**: Order execution, market data retrieval, account management

## Supporting Subsystems

### Risk Management
- **Components**: Position sizing logic, portfolio management
- **Purpose**: Capital allocation, risk assessment, stop-loss management
- **Dependencies**: Trading Engine, Database Layer, Strategy Framework
- **Interfaces**: Position validation, risk calculation, emergency controls

### Performance Analytics
- **Components**: Trade performance calculations, strategy metrics
- **Purpose**: Profitability analysis, strategy optimization, reporting
- **Dependencies**: Database Layer, Trading Engine
- **Interfaces**: Performance reporting, strategy comparison, optimization feedback

### Configuration Management
- **Components**: `settings/` directory, configuration files
- **Purpose**: Bot parameters, strategy settings, market configurations
- **Dependencies**: All subsystems (configuration provider)
- **Interfaces**: Settings validation, dynamic reconfiguration, defaults management

### Monitoring & Logging
- **Components**: Error logging, crash monitoring, backup systems
- **Purpose**: System health monitoring, error tracking, data protection
- **Dependencies**: All subsystems (monitoring overlay)
- **Interfaces**: Error collection, health reporting, backup automation

### Technical Analysis
- **Components**: Market indicators, price analysis, signal generation
- **Purpose**: Technical indicator calculations for strategy support
- **Dependencies**: Market Data, OHLCV Database
- **Interfaces**: Indicator calculations, signal processing, data aggregation

### OHLCV Data Management
- **Components**: `ohlcv/` database modules, price data storage
- **Purpose**: Historical price data management and retrieval
- **Dependencies**: API Integration, Database Layer
- **Interfaces**: Price data storage, historical analysis, data validation

---

## Integration Patterns

### Cross-Subsystem Dependencies
```
Trading Engine → Strategy Framework → Technical Analysis → OHLCV Data
             → API Integration → Market Data
             → Database Layer → Performance Analytics
             → Risk Management → Configuration Management
```

### Data Flow Patterns
1. **Market Data Flow**: API Integration → OHLCV Data → Technical Analysis → Strategy Framework
2. **Trade Execution Flow**: Strategy Framework → Risk Management → Trading Engine → API Integration
3. **Performance Flow**: Trading Engine → Database Layer → Performance Analytics → Monitoring

---
*This registry guides task creation by defining clear component boundaries and preventing cross-system complexity.* 