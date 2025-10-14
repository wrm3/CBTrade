#!/usr/bin/env python3
"""
Manual Wallet Balance Refresh Script
Calls the bot's wallet refresh functionality to sync balances from Coinbase API
"""

import os
import sys
from datetime import datetime, timezone

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))

from libs.coinbase_handler import CoinbaseAPI
from libs.db_mysql.cbtrade.db_main import CBTRADE_DB

def main():
    print("=" * 80)
    print("WALLET BALANCE REFRESH UTILITY")
    print("=" * 80)
    print(f"Started at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    # Initialize database connection
    print("[*] Initializing database connection...")
    db = CBTRADE_DB()
    
    # Initialize Coinbase API
    print("[*] Initializing Coinbase API connection...")
    cb = CoinbaseAPI()
    
    # Get current MOODENG balance before refresh
    print("\n[BEFORE REFRESH]")
    sql = "SELECT symb, bal_tot, bal_avail, update_dttm FROM bals WHERE symb = 'MOODENG'"
    before = db.seld(sql)
    if before:
        print(f"  MOODENG Balance: {before[0]['bal_tot']} (updated: {before[0]['update_dttm']})")
    else:
        print("  MOODENG Balance: No record found")
    
    # Perform wallet refresh
    print("\n[REFRESHING] Calling Coinbase API wallet refresh...")
    try:
        cb.cb_wallet_refresh()
        print("[SUCCESS] Wallet refresh completed!")
    except Exception as e:
        print(f"[ERROR] Wallet refresh failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Get MOODENG balance after refresh
    print("\n[AFTER REFRESH]")
    after = db.seld(sql)
    if after:
        print(f"  MOODENG Balance: {after[0]['bal_tot']} (updated: {after[0]['update_dttm']})")
        
        # Show change
        if before and after:
            before_bal = float(before[0]['bal_tot'])
            after_bal = float(after[0]['bal_tot'])
            if before_bal != after_bal:
                change = after_bal - before_bal
                print(f"  Change: {change:+.6f} MOODENG")
            else:
                print("  No change in balance")
    else:
        print("  MOODENG Balance: No record found")
    
    # Show all balances with values
    print("\n[ALL NON-ZERO BALANCES]")
    sql_all = """
        SELECT symb, bal_tot, bal_avail, curr_val_usd, update_dttm
        FROM bals 
        WHERE bal_tot > 0
        ORDER BY curr_val_usd DESC
        LIMIT 20
    """
    all_bals = db.seld(sql_all)
    if all_bals:
        print(f"  {'Symbol':<12} {'Balance':<18} {'Value USD':<15} {'Updated'}")
        print(f"  {'-'*12} {'-'*18} {'-'*15} {'-'*19}")
        for bal in all_bals:
            print(f"  {bal['symb']:<12} {float(bal['bal_tot']):>18.6f} ${float(bal['curr_val_usd']):>13.2f} {bal['update_dttm']}")
    
    print("\n" + "=" * 80)
    print(f"Completed at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)

if __name__ == "__main__":
    main()

