# CBTrade Project File Registry

*Last Updated: 2025-07-29*

## fstrent_tasks_v2 System Files

| File | Purpose | Dependencies | Notes |
|---|---|-----|----|
| `TASKS.md` | Master task checklist and status tracking | All task files | Primary control interface |
| `PROJECT_CONTEXT.md` | Project mission and current phase context | None | Guides all task creation |
| `SUBSYSTEMS.md` | Component architecture registry | None | Defines system boundaries |
| `FILE_REGISTRY.md` | Project structure documentation | None | This file |

## Task Management Structure

| Directory/File | Purpose | Key Components | Integrations |
|----|---|----|-----|
| `tasks/` | Active task files | task{id}_name.md format | Synchronized with TASKS.md |
| `memory/tasks/` | Archived completed tasks | Historical task files | Referenced for context |
| `memory/TASKS_LOG.md` | Chronological task archive log | Append-only history | Memory consultation |
| `plans/` | Active PRDs and planning | PLAN.md, feature plans | Task generation source |
| `plans/features/` | Feature-specific PRDs | Detailed specifications | Subsystem integration |
| `memory/plans/` | Archived planning documents | Historical PRDs | Planning context |
| `memory/PLANS_LOG.md` | Chronological plan archive log | Planning history | Prevents duplication |

## Core Trading System Structure

| Directory | Purpose | Key Files | Integration Points |
|----|----|----|-----|
| `libs/` | Core trading libraries | bot_main.py, strategies | All subsystems |
| `libs/db/` | Database layer | SQLite modules, CRUD ops | Data persistence |
| `libs/strats/` | Trading strategies | Strategy implementations | Trading engine |
| `settings/` | Configuration files | JSON settings | System configuration |
| `db/` | Database files | SQLite databases | Data storage |
| `bkups/` | Backup archives | System backups | Data protection |

## Trading System Architecture

| Component | Files | Purpose | Dependencies |
|----|----|---|-----|
| Trading Engine | `run_bot.py`, `libs/bot_main.py` | Core automation | All subsystems |
| Strategy Framework | `libs/strats/*.py` | Algorithm implementation | Technical analysis |
| Database Layer | `libs/db/*.py`, SQLite files | Data persistence | None (foundational) |
| API Integration | Coinbase modules | Exchange communication | Trading engine |
| Risk Management | Position sizing, portfolio | Capital protection | Trading engine |
| Performance Analytics | Trade metrics, reporting | Strategy optimization | Database layer |

## Development Tools & Utilities

| Tool | Function | Usage Context | Dependencies |
|----|----|---|-----|
| `fstrent_tasks_v2` | Task management system | Development workflow | All files |
| Backup system | Data protection | Regular archival | All databases |
| Error monitoring | System health | Production monitoring | All components |
| Strategy testing | Algorithm validation | Development phase | Strategy framework |

## Architecture Notes

- **Core System**: SQLite-based cryptocurrency trading automation
- **Data Flow**: API → Database → Strategies → Trading Engine → API
- **Integration Points**: Coinbase Pro API, SQLite databases, JSON configuration
- **Deployment Structure**: Single-machine Python application with automated trading

---
*This registry maintains awareness of project structure for effective task management and system navigation.* 