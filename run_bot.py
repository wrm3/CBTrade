#!/usr/bin/env python3
#<=====>#
# Description
#<=====>#
"""
Author: FSTrent
"""

#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Common Modules
#<=====>#
import argparse
import os
import sys
import traceback
import time
from datetime import datetime
import atexit
import faulthandler
import warnings
import pandas as pd


#<=====>#
# Imports - Project
#<=====>#
# Now import common which might use fstrent_colors
from libs.common import beep, narc, dttm_get, beep


#<=====>#
# Back Up Project
#<=====>#
# Never remove this CRITICAL backup code 
from fstrent_bkitup import backup_project as bp
bp(__file__, additional_paths=['libs', '.cursor/rules', '.fstrent_tasks_v2', 'settings/market_usdc.json'], output_dir='bkups')



#<=====>#
# Set Up
#<=====>#
# Add the current directory to Python path for imports
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())


#<=====>#
# Variables
#<=====>#
lib_name = 'run_bot'
log_name = 'run_bot'


#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def initialize_bot():
    """Initialize BOT."""
    print("Initializing MySQL databases...")
    
    # Now import and initialize BOT with MySQL databases
    print("Initializing BOT class...")
    from libs.bot_base import BOT
    
    # Create BOT instance with MySQL database connections
    print("Creating BOT instance with MySQL databases...")
    bot = BOT()
    
    print("BOT initialization successful!")
    return bot

#<=====>#

def run_trading_mode(bot, auto_mode: bool = False):
    """Run trading operations with minimal error handling."""
    
    if auto_mode:
        bot.auto_loop()
    else:
        bot.main_loop()

#<=====>#

def main():
    parser = argparse.ArgumentParser(description='CBTrade Automated Trading Bot')
    parser.add_argument('--auto', action='store_true', help='Run in automated trading mode')
    parser.add_argument('--manual', action='store_true', help='Run in manual mode (default)')
    args = parser.parse_args()

    import certifi
    print("Certificate path:", certifi.where())
    print("File exists:", os.path.exists(certifi.where()))

    # Enable low-level crash diagnostics
    try:
        faulthandler.enable()
    except Exception:
        pass

    # Suppress known noisy FutureWarnings from pandas chained fills in strategy code
    try:
        warnings.simplefilter("ignore", category=FutureWarning)
    except Exception:
        pass

    # Force numpy dtype backend to avoid PyArrow/extension blocks causing C-level crashes in pandas
    try:
        pd.options.mode.dtype_backend = "numpy"
    except Exception:
        pass

    # Last-chance exception hook to surface silent exits
    def _last_chance_excepthook(exctype, value, tb):
        try:
            print("\n=== Unhandled exception ===")
            print(f"Type: {exctype.__name__}")
            print(f"Message: {value}")
            traceback.print_tb(tb)
            beep(3)
        except Exception:
            pass
        # Re-raise to preserve exit semantics
        sys.__excepthook__(exctype, value, tb)

    sys.excepthook = _last_chance_excepthook

    # atexit marker so we know we reached process teardown
    atexit.register(lambda: print(f"atexit: process shutting down {dttm_get()}"))

    try:
        run_trading_mode(bot, auto_mode=args.auto)
    except SystemExit as e:
        print(f"SystemExit code={e.code}")
        raise
    except KeyboardInterrupt:
        print("\nTrading bot stopped by user (Ctrl+C)")
    except BaseException as e:
        print(f"FATAL (top-level): {type(e).__name__}: {e}")
        traceback.print_exc()
        raise
    finally:
        print("\nClosing database connections...")
        try:
            if hasattr(bot, 'cbtrade_db'):
                bot.cbtrade_db.close_connection()
                print("Database connections closed safely")
        except Exception as e:
            print(f"Warning during cleanup: {e}")
            traceback.print_exc()
        
        print("CBTrade Automated Trading Bot shutdown complete")

#<=====>#
# Post Variables
#<=====>#

# Simple initialization with no error handling wrapper
bot = initialize_bot()

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    main()

#<=====>#
