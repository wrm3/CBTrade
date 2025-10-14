# PRD: Emergency MySQL Reversion for CBTrade Trading Bot Recovery

## 1. Product Overview

### 1.1 Document Title and Version
- PRD: Emergency MySQL Reversion for CBTrade Trading Bot Recovery
- Version: 1.0 (Critical Recovery)

### 1.2 Product Summary
This is an urgent recovery operation to restore the CBTrade trading bot that has been offline for 50 days due to SQLite concurrent write failures. The system must be reverted from SQLite back to MySQL to handle multiple AI bot concurrent writes that have been causing database lock failures and preventing trading operations.

**CRITICAL BUSINESS IMPACT**: 50 days of missed trading during record market highs, resulting in massive financial losses. Immediate restoration is required to resume automated trading operations.

## 2. Goals

### 2.1 Business Goals
- **URGENT**: Restore trading bot operations within 48-72 hours maximum
- Eliminate SQLite concurrent write failures that caused 50-day outage
- Restore reliable database operations for multiple concurrent AI trading bots
- Resume automated trading to capture current market opportunities
- Prevent further financial losses from system downtime

### 2.2 User Goals
- Get trading bot back online immediately to resume automated trading
- Restore database reliability for concurrent AI bot operations
- Maintain all existing trading data and performance history
- Resume profit generation from automated trading strategies

### 2.3 Non-Goals
- Performance optimization (focus on reliability first)
- New feature development (recovery only)
- Code refactoring beyond database layer changes
- UI/UX improvements (command-line focus)

## 3. User Personas

### 3.1 Key User Types
- Emergency recovery operator (immediate restoration)
- Trading system operator (ongoing operations)

### 3.2 Basic Persona Details
- **Emergency Recovery Operator**: Technical user focused on immediate system restoration with minimal risk
- **Trading System Operator**: Daily user requiring reliable 24/7 automated trading operations

### 3.3 Role-Based Access
- **Emergency Recovery**: Full database and system access for immediate restoration
- **Trading Operations**: Standard trading system access once restored

## 4. Functional Requirements

- **MySQL Database Restoration** (Priority: Critical)
  - Recreate cbtrade MySQL databases with proper users
  - Convert all SQLite table schemas to MySQL equivalents
  - Restore triggers for dlm and dlm_unix timestamp columns

- **Database Layer Migration** (Priority: Critical)
  - Mirror libs/db/ structure in libs/db_mysql/ with MySQL implementations
  - Maintain identical method signatures for seamless integration
  - Use existing mysql_handler.py as proven foundation

- **Concurrent Write Support** (Priority: Critical)
  - MySQL InnoDB engine for proper concurrent write handling
  - Connection pooling and transaction management
  - Eliminate SQLite WAL mode limitations

- **Data Migration** (Priority: High)
  - Migrate existing SQLite data back to MySQL tables
  - Validate data integrity during migration
  - Preserve trading history and performance data

- **System Integration** (Priority: High)
  - Update database imports to use MySQL handlers
  - Maintain backward compatibility with existing code
  - Test concurrent bot operations

## 5. User Experience

### 5.1 Entry Points & First-Time User Flow
- Execute emergency database restoration scripts
- Validate MySQL connectivity and schema creation
- Test basic trading bot functionality before full deployment

### 5.2 Core Experience
- **Database Creation**: Automated MySQL database and schema creation
- **Data Migration**: Safe transfer of existing SQLite data to MySQL
- **System Testing**: Validation of concurrent write operations
- **Bot Restoration**: Resume trading bot operations with monitoring

### 5.3 Advanced Features & Edge Cases
- Rollback procedures if MySQL restoration fails
- Data validation and integrity checks
- Performance monitoring for concurrent operations
- Emergency shutdown procedures if issues arise

### 5.4 UI/UX Highlights
- Command-line interface for database operations
- Clear status reporting during migration process
- Error handling with detailed diagnostics
- Validation confirmation before committing changes

## 6. Narrative
The trading system operator executes the emergency MySQL restoration process, which recreates the MySQL databases, migrates the table schemas, and transfers existing trading data. The system validates concurrent write capabilities and resumes automated trading operations, immediately restoring income generation that was lost during the 50-day SQLite outage.

## 7. Success Metrics

### 7.1 User-Centric Metrics
- Trading bot restored to operational status within 72 hours
- Zero data loss during migration process
- Concurrent write operations function without failures
- Automated trading resumes with full functionality

### 7.2 Business Metrics
- Resume daily trading income generation
- Eliminate database-related system downtime
- Restore 24/7 automated trading capability
- Prevent continued financial losses from outage

### 7.3 Technical Metrics
- MySQL concurrent write operations succeed 100%
- Database connection stability >99.9%
- No SQLite-related lock failures
- Trading bot uptime >99% post-restoration

## 8. Technical Considerations

### 8.1 Affected Subsystems
- **Primary subsystems** (directly modified/extended):
  - Database Layer: Complete MySQL restoration and SQLite replacement
  - Trading Engine: Database connection updates for MySQL integration
  - API Integration: Database write operations for trade data

- **Secondary subsystems** (indirectly affected):
  - Performance Analytics: Database query optimization for MySQL
  - Configuration Management: Database connection settings updates
  - Monitoring & Logging: Database health monitoring adjustments

### 8.2 Integration Points
- MySQL InnoDB engine for concurrent write support
- Existing mysql_handler.py proven codebase as foundation
- Connection pooling for multiple AI bot concurrent access
- Transaction management for data integrity

### 8.3 Data Storage & Privacy
- Local MySQL databases for complete data control
- Encrypted database credentials and connection strings
- Automated backup systems for data protection
- No external dependencies or cloud services

### 8.4 Scalability & Performance
- MySQL InnoDB engine optimized for concurrent operations
- Connection pooling to handle multiple AI bot connections
- Index optimization for trading query performance
- Resource monitoring for database performance

### 8.5 Potential Challenges
- Data migration complexity from SQLite to MySQL
- Schema conversion from SQLite types to MySQL types
- Concurrent access testing and validation
- Time pressure for immediate restoration

## 9. Milestones & Sequencing

### 9.1 Project Estimate
- Critical: Emergency restoration (48-72 hours maximum)

### 9.2 Team Size & Composition
- Emergency Recovery: 1 person (Developer/Operator)

### 9.3 Suggested Phases
- **Phase 1**: Database Infrastructure (0-24 hours)
  - Key deliverables: MySQL database created, schemas converted, basic connectivity
- **Phase 2**: Data Migration and Integration (24-48 hours)
  - Key deliverables: Data migrated, system integration, basic testing
- **Phase 3**: Validation and Deployment (48-72 hours)
  - Key deliverables: Concurrent write testing, trading bot restoration, monitoring

## 10. User Stories

### 10.1 Emergency Database Restoration
- **ID**: US-001
- **Description**: As a trading system operator, I need to restore MySQL database immediately so that my trading bots can resume operations after 50 days of SQLite failures.
- **Acceptance Criteria**:
  - MySQL cbtrade database created with proper users
  - All table schemas converted from SQLite to MySQL equivalents
  - Database connectivity validated and tested

### 10.2 Concurrent Write Operations
- **ID**: US-002
- **Description**: As a trading system operator, I need concurrent write operations to work reliably so that multiple AI bots can write trade data simultaneously without failures.
- **Acceptance Criteria**:
  - Multiple AI bots can write to database concurrently without locks
  - No SQLite WAL mode limitations or write failures
  - Transaction integrity maintained across concurrent operations

### 10.3 Data Migration and Integrity
- **ID**: US-003
- **Description**: As a trading system operator, I need all existing trading data migrated safely so that I don't lose 50 days of accumulated trading history and performance data.
- **Acceptance Criteria**:
  - All SQLite data successfully migrated to MySQL
  - Data integrity validation confirms no data loss
  - Trading history and performance metrics preserved

### 10.4 Trading Bot Restoration
- **ID**: US-004
- **Description**: As a trading system operator, I need my trading bots to resume operations immediately so that I can start generating trading income again after massive losses.
- **Acceptance Criteria**:
  - Trading bots connect to MySQL databases successfully
  - Automated trading operations resume without errors
  - Income generation restored to pre-outage levels

---
*This emergency PRD guides the critical MySQL restoration to get the trading bot back online and resume income generation after 50 days of costly downtime.* 