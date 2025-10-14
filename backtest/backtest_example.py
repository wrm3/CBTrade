#!/usr/bin/env python3
#<=====>#
# Backtesting Example Script
# 
# Demonstrates how to run backtests on trading strategies
#<=====>#

import sys
import os

# Add parent directory to path so we can import from libs
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from libs.backtest_base import backtest_strategy, BacktestEngine
from libs.bot_base import BOT  # Main bot class

def main():
    """
    Example: Backtest BTC-USDC strategies over 6 months
    """
    
    print("\n" + "="*80)
    print("BACKTESTING EXAMPLE")
    print("="*80 + "\n")
    
    # Initialize bot instance (in backtest mode)
    bot = BOT()
    bot.backtest_mode = True  # Flag to prevent real API calls
    
    # Define backtest parameters
    prod_id = 'BTC-USDC'
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 6 months back
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    starting_balance = 10000.0
    
    print(f"Product: {prod_id}")
    print(f"Period: {start_str} to {end_str}")
    print(f"Starting Balance: ${starting_balance:,.2f}")
    print(f"\n{'='*80}\n")
    
    # Run backtest
    results = backtest_strategy(
        bot_instance=bot,
        prod_id=prod_id,
        start_date=start_str,
        end_date=end_str,
        starting_balance=starting_balance
    )
    
    # Display results
    print("\n" + "="*80)
    print("BACKTEST RESULTS")
    print("="*80)
    
    print(f"\nStarting Balance: ${results['starting_balance']:,.2f}")
    print(f"Ending Balance: ${results['ending_balance']:,.2f}")
    print(f"Total Return: {results['total_return_pct']:.2f}%")
    print(f"\nTotal Trades: {results['total_trades']}")
    print(f"Winning Trades: {results['winning_trades']}")
    print(f"Losing Trades: {results['losing_trades']}")
    print(f"Win Rate: {results['win_rate']:.2f}%")
    print(f"\nAverage Win: ${results['avg_win']:.2f}")
    print(f"Average Loss: ${results['avg_loss']:.2f}")
    print(f"Profit Factor: {results['profit_factor']:.2f}")
    print(f"\nMax Drawdown: {results['max_drawdown']:.2f}%")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    
    print(f"\n{'='*80}\n")
    
    # Save results to file
    import json
    output_file = f"backtest_results_{prod_id}_{start_str}_{end_str}.json"
    with open(output_file, 'w') as f:
        # Convert equity curve to serializable format
        results_copy = results.copy()
        results_copy['equity_curve'] = [
            {
                'timestamp': str(e['timestamp']),
                'equity': e['equity'],
                'balance': e['balance'],
                'num_positions': e['num_positions']
            }
            for e in results['equity_curve']
        ]
        json.dump(results_copy, f, indent=2)
    
    print(f"Results saved to: {output_file}")


def backtest_multiple_pairs():
    """
    Example: Backtest multiple pairs (BTC, ETH, SOL)
    """
    
    pairs = ['BTC-USDC', 'ETH-USDC', 'SOL-USDC']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    bot = BOT()
    bot.backtest_mode = True
    
    all_results = {}
    
    for prod_id in pairs:
        print(f"\n{'='*80}")
        print(f"BACKTESTING {prod_id}")
        print(f"{'='*80}\n")
        
        results = backtest_strategy(
            bot_instance=bot,
            prod_id=prod_id,
            start_date=start_str,
            end_date=end_str,
            starting_balance=10000.0
        )
        
        all_results[prod_id] = results
        
        print(f"\n{prod_id} Results:")
        print(f"Total Return: {results['total_return_pct']:.2f}%")
        print(f"Win Rate: {results['win_rate']:.2f}%")
        print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY - ALL PAIRS")
    print(f"{'='*80}\n")
    
    for prod_id, results in all_results.items():
        print(f"{prod_id:12} | Return: {results['total_return_pct']:>7.2f}% | "
              f"Trades: {results['total_trades']:>4} | "
              f"Win Rate: {results['win_rate']:>5.2f}% | "
              f"Max DD: {results['max_drawdown']:>6.2f}%")


def backtest_single_strategy():
    """
    Example: Backtest only one strategy (e.g., 'nwe_env')
    """
    
    bot = BOT()
    bot.backtest_mode = True
    
    prod_id = 'BTC-USDC'
    strategy_name = 'nwe_env'
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 year
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    print(f"\nBacktesting strategy '{strategy_name}' on {prod_id}")
    print(f"Period: {start_str} to {end_str}\n")
    
    # TODO: Modify backtest_strategy to accept strategy_name filter
    results = backtest_strategy(
        bot_instance=bot,
        prod_id=prod_id,
        start_date=start_str,
        end_date=end_str,
        starting_balance=10000.0,
        strategy_name=strategy_name
    )
    
    print(f"\nStrategy '{strategy_name}' Performance:")
    print(f"Total Return: {results['total_return_pct']:.2f}%")
    print(f"Trades: {results['total_trades']}")
    print(f"Win Rate: {results['win_rate']:.2f}%")


if __name__ == '__main__':
    
    # Example 1: Single pair backtest
    main()
    
    # Example 2: Multiple pairs (uncomment to run)
    # backtest_multiple_pairs()
    
    # Example 3: Single strategy (uncomment to run)
    # backtest_single_strategy()