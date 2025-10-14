#<=====>#  
# Description - Backtesting Framework
# 
# Event-driven minute-by-minute backtesting system that:
# 1. Replays historical minute data chronologically
# 2. Builds multi-timeframe candles as they would develop in real-time
# 3. Runs full buy/sell logic with all denial checks, boosts, and timing
# 4. Handles indicator repainting correctly
# 5. Tracks realistic budget allocation and position sizing
#<=====>#

#<=====>#
# Imports
#<=====>#
import sys
import traceback
from datetime import datetime as dt, timezone, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from fstrent_colors import cs
from libs.common import (
    AttrDict, AttrDictConv, narc, dttm_unix, dttm_get, print_adv
)

#<=====>#
# Variables
#<=====>#
lib_name = 'backtest_base'
log_name = 'backtest_base'

#<=====>#
# Classes
#<=====>#

class BacktestEngine:
    """
    Event-driven backtesting engine that replays historical data minute-by-minute
    to simulate real trading conditions including indicator repainting.
    """
    
    def __init__(self, bot_instance, ohlcv_db):
        """
        Initialize backtest engine with bot instance and OHLCV database connection.
        
        Args:
            bot_instance: The main bot instance with all trading logic
            ohlcv_db: Database connection to OHLCV historical data
        """
        self.bot = bot_instance
        self.ohlcv_db = ohlcv_db
        
        # Backtest state
        self.current_minute = None
        self.prod_id = None
        self.start_date = None
        self.end_date = None
        
        # Multi-timeframe candle builders
        self.candle_builders = {}  # {freq: CandleBuilder}
        self.completed_candles = {}  # {freq: DataFrame}
        
        # Position tracking
        self.open_positions = []
        self.closed_positions = []
        self.orders = []
        
        # Performance tracking
        self.equity_curve = []
        self.starting_balance = 0
        self.current_balance = 0
        
        # Strategy performance tracking (mirrors live system)
        self.strategy_stats = {}
        
    def load_minute_data(self, prod_id: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load 1-minute OHLCV data from database for backtest period.
        
        Args:
            prod_id: Product ID (e.g., 'BTC-USDC')
            start_date: Start date 'YYYY-MM-DD'
            end_date: End date 'YYYY-MM-DD'
            
        Returns:
            DataFrame with 1-minute OHLCV data
        """
        # Table name is based on product ID with underscores (e.g., ohlcv_BTC_USDC)
        table_name = f"ohlcv_{prod_id.replace('-', '_')}"
        
        sql = f"""
        SELECT 
            start_dttm as candle_begin_dttm
            , open_prc
            , high_prc
            , low_prc
            , close_prc
            , volume
        FROM {table_name}
        WHERE freq = '1min'
        AND start_dttm >= '{start_date}'
        AND start_dttm <= '{end_date} 23:59:59'
        ORDER BY start_dttm ASC
        """
        
        result = self.ohlcv_db.seld(sql)
        
        if not result:
            raise ValueError(f"No minute data found for {prod_id} in table {table_name} between {start_date} and {end_date}")
        
        df = pd.DataFrame(result)
        df['candle_begin_dttm'] = pd.to_datetime(df['candle_begin_dttm'])
        df.set_index('candle_begin_dttm', inplace=True)
        
        return df
    
    def initialize_candle_builders(self, freqs: List[str]):
        """
        Initialize candle builders for each timeframe.
        
        Args:
            freqs: List of frequencies ['15min', '30min', '1h', '4h', '1d']
        """
        for freq in freqs:
            self.candle_builders[freq] = CandleBuilder(freq)
            self.completed_candles[freq] = pd.DataFrame()
    
    def run_backtest(
        self, 
        prod_id: str, 
        start_date: str, 
        end_date: str,
        starting_balance: float = 10000.0,
        freqs: List[str] = ['15min', '30min', '1h', '4h', '1d']
    ) -> Dict:
        """
        Main backtest execution - replays minute data chronologically.
        
        Args:
            prod_id: Product to backtest
            start_date: Start date 'YYYY-MM-DD'
            end_date: End date 'YYYY-MM-DD'
            starting_balance: Starting capital
            freqs: Timeframes to test
            
        Returns:
            Dictionary with backtest results
        """
        print(f"\n{'='*80}")
        print(f"BACKTEST START: {prod_id} from {start_date} to {end_date}")
        print(f"{'='*80}\n")
        
        # Setup
        self.prod_id = prod_id
        self.start_date = start_date
        self.end_date = end_date
        self.starting_balance = starting_balance
        self.current_balance = starting_balance
        
        # Load minute data
        print("Loading minute data...")
        minute_data = self.load_minute_data(prod_id, start_date, end_date)
        print(f"Loaded {len(minute_data)} minutes of data")
        
        # Initialize candle builders
        self.initialize_candle_builders(freqs)
        
        # Replay each minute chronologically
        total_minutes = len(minute_data)
        for idx, (timestamp, minute_bar) in enumerate(minute_data.iterrows()):
            
            if idx % 1000 == 0:
                pct = (idx / total_minutes) * 100
                print(f"Progress: {idx}/{total_minutes} ({pct:.1f}%) - Date: {timestamp}")
            
            self.current_minute = timestamp
            
            # Process this minute
            self._process_minute(timestamp, minute_bar)
        
        # Calculate final results
        results = self._calculate_results()
        
        print(f"\n{'='*80}")
        print(f"BACKTEST COMPLETE")
        print(f"{'='*80}\n")
        
        return results
    
    def _process_minute(self, timestamp: pd.Timestamp, minute_bar: pd.Series):
        """
        Process a single minute of data - core backtest logic.
        
        This is where we:
        1. Update all timeframe candles with the new minute
        2. Check if any candles completed
        3. Update technical indicators
        4. Run buy logic (if applicable)
        5. Run sell logic (if have positions)
        6. Update position tracking
        """
        
        # 1. Update all candle builders with this minute's data
        for freq, builder in self.candle_builders.items():
            candle_completed = builder.add_minute(timestamp, minute_bar)
            
            if candle_completed:
                # A candle for this timeframe just completed
                completed_candle = builder.get_completed_candle()
                self._add_completed_candle(freq, completed_candle)
        
        # 2. Check if we have enough data to start trading
        if not self._has_minimum_data():
            return
        
        # 3. Update technical indicators for all timeframes
        self._update_indicators()
        
        # 4. Run sell logic first (manage existing positions)
        if self.open_positions:
            self._run_sell_logic(timestamp, minute_bar)
        
        # 5. Run buy logic (check for new entries)
        self._run_buy_logic(timestamp, minute_bar)
        
        # 6. Track equity
        self._update_equity(timestamp, minute_bar)
    
    def _add_completed_candle(self, freq: str, candle: Dict):
        """Add a completed candle to the historical data for this timeframe."""
        if self.completed_candles[freq].empty:
            self.completed_candles[freq] = pd.DataFrame([candle])
        else:
            self.completed_candles[freq] = pd.concat([
                self.completed_candles[freq],
                pd.DataFrame([candle])
            ], ignore_index=True)
    
    def _has_minimum_data(self) -> bool:
        """Check if we have minimum required candles to start trading."""
        # Need at least 100 candles on longest timeframe (1d) before starting
        if '1d' in self.completed_candles:
            return len(self.completed_candles['1d']) >= 100
        return False
    
    def _update_indicators(self):
        """
        Calculate technical indicators for all timeframes.
        
        This mimics what happens in real trading - indicators recalculate
        as new candles complete, which is crucial for testing repainting indicators.
        """
        from libs.bot_ta import ta_add_indicators
        
        # For each timeframe, build DataFrame and calculate indicators
        for freq, builder in self.candle_builders.items():
            try:
                # Build DataFrame from completed + current developing candle
                candles_list = []
                
                # Add all completed candles from this freq
                if freq in self.completed_candles and len(self.completed_candles[freq]) > 0:
                    candles_list = self.completed_candles[freq].to_dict('records')
                
                # Add the current developing candle
                if builder.current_candle is not None:
                    candles_list.append(builder.current_candle)
                
                # Skip if not enough history yet (need at least 10 candles for indicators)
                if len(candles_list) < 10:
                    continue
                
                # Convert to DataFrame with correct column names for indicators
                df = pd.DataFrame(candles_list)
                if 'timestamp' in df.columns:
                    df.set_index('timestamp', inplace=True)
                
                # Call indicator calculation function from bot_ta.py
                # Note: ta_add_indicators expects columns: open, high, low, close, volume
                # And it needs settings (st) and prc_mkt
                if hasattr(self.bot, 'st') and hasattr(self.bot, 'pair'):
                    st = self.bot.st
                    prc_mkt = self.bot.pair.prc_mkt if hasattr(self.bot.pair, 'prc_mkt') else 0
                    
                    df = ta_add_indicators(df, st, prc_mkt, freq)
                    
                    # Store indicators in bot.pair.ta structure (matching live trading)
                    if not hasattr(self.bot, 'pair'):
                        self.bot.pair = AttrDict()
                    if not hasattr(self.bot.pair, 'ta'):
                        self.bot.pair.ta = AttrDict()
                    if not freq in self.bot.pair.ta:
                        self.bot.pair.ta[freq] = AttrDict()
                    
                    # Store the full DataFrame with indicators
                    self.bot.pair.ta[freq].df = df
                    
                    # Also store current row values (matching live bot structure)
                    # This is what strategies actually check
                    self.bot.pair.ta[freq].curr = AttrDict()
                    for col in df.columns:
                        self.bot.pair.ta[freq].curr[col] = df[col].iloc[-1]
                
            except Exception as e:
                # Don't crash backtest on indicator errors - just log and continue
                print(f"Warning: Indicator calculation error for {freq}: {e}")
                traceback.print_exc()
                continue
    
    def _run_buy_logic(self, timestamp: pd.Timestamp, current_price: pd.Series):
        """
        Run the full buy logic from buy_base.py.
        
        This should replicate buy_main() but in backtest mode.
        """
        # TODO: 
        # 1. Setup buy object (similar to buy_new())
        # 2. Loop through strategies
        # 3. Run buy_strats_check()
        # 4. Apply all denial/boost logic
        # 5. Check budget constraints
        # 6. If buy signal, create simulated order
        pass
    
    def _run_sell_logic(self, timestamp: pd.Timestamp, current_price: pd.Series):
        """
        Run the full sell logic for open positions.
        
        This should replicate sell logic but in backtest mode.
        """
        # TODO:
        # 1. For each open position
        # 2. Run sell_strats_check()
        # 3. Apply stop loss / take profit logic
        # 4. If sell signal, close position
        pass
    
    def _update_equity(self, timestamp: pd.Timestamp, current_price: pd.Series):
        """Track equity curve by marking open positions to market."""
        current_equity = self.current_balance
        
        # Add unrealized P&L from open positions
        for pos in self.open_positions:
            unrealized_pnl = (current_price['close_prc'] - pos['buy_price']) * pos['size']
            current_equity += unrealized_pnl
        
        self.equity_curve.append({
            'timestamp': timestamp,
            'equity': current_equity,
            'balance': self.current_balance,
            'num_positions': len(self.open_positions)
        })
    
    def _calculate_results(self) -> Dict:
        """Calculate final backtest metrics."""
        
        results = {
            'starting_balance': self.starting_balance,
            'ending_balance': self.current_balance,
            'total_return_pct': ((self.current_balance - self.starting_balance) / self.starting_balance) * 100,
            'total_trades': len(self.closed_positions),
            'winning_trades': len([p for p in self.closed_positions if p['pnl'] > 0]),
            'losing_trades': len([p for p in self.closed_positions if p['pnl'] < 0]),
            'win_rate': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'profit_factor': 0,
            'max_drawdown': 0,
            'sharpe_ratio': 0,
            'equity_curve': self.equity_curve,
            'closed_positions': self.closed_positions
        }
        
        if results['total_trades'] > 0:
            results['win_rate'] = (results['winning_trades'] / results['total_trades']) * 100
            
            wins = [p['pnl'] for p in self.closed_positions if p['pnl'] > 0]
            losses = [p['pnl'] for p in self.closed_positions if p['pnl'] < 0]
            
            if wins:
                results['avg_win'] = np.mean(wins)
            if losses:
                results['avg_loss'] = np.mean(losses)
            
            if results['avg_loss'] != 0:
                results['profit_factor'] = abs(results['avg_win'] / results['avg_loss'])
        
        # Calculate max drawdown
        equity_series = pd.Series([e['equity'] for e in self.equity_curve])
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max
        results['max_drawdown'] = drawdown.min() * 100
        
        return results


class CandleBuilder:
    """
    Builds higher timeframe candles from minute data in real-time.
    
    This simulates how candles develop during live trading, which is crucial
    for testing indicator repainting behavior.
    """
    
    def __init__(self, freq: str):
        """
        Initialize candle builder for a specific frequency.
        
        Args:
            freq: Frequency like '15min', '30min', '1h', '4h', '1d'
        """
        self.freq = freq
        self.freq_minutes = self._freq_to_minutes(freq)
        
        # Current developing candle
        self.current_candle = None
        self.current_candle_start = None
        
        # Last completed candle
        self.last_completed = None
    
    def _freq_to_minutes(self, freq: str) -> int:
        """Convert frequency string to minutes."""
        mapping = {
            '1min': 1,
            '15min': 15,
            '30min': 30,
            '1h': 60,
            '4h': 240,
            '1d': 1440
        }
        return mapping.get(freq, 60)
    
    def _get_candle_start_time(self, timestamp: pd.Timestamp) -> pd.Timestamp:
        """Get the start time of the candle this minute belongs to."""
        
        if self.freq == '1d':
            # Daily candles start at midnight
            return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # Intraday candles - round down to nearest freq interval
            minutes_since_midnight = timestamp.hour * 60 + timestamp.minute
            candle_number = minutes_since_midnight // self.freq_minutes
            start_minute = candle_number * self.freq_minutes
            
            start_hour = start_minute // 60
            start_min = start_minute % 60
            
            return timestamp.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
    
    def add_minute(self, timestamp: pd.Timestamp, minute_bar: pd.Series) -> bool:
        """
        Add a minute bar to the developing candle.
        
        Args:
            timestamp: Timestamp of this minute
            minute_bar: OHLCV data for this minute
            
        Returns:
            True if a candle completed, False otherwise
        """
        candle_start = self._get_candle_start_time(timestamp)
        
        # Check if we're starting a new candle
        if self.current_candle_start is None or candle_start > self.current_candle_start:
            # Save the previous candle if it exists
            if self.current_candle is not None:
                self.last_completed = self.current_candle.copy()
            
            # Start new candle
            self.current_candle_start = candle_start
            self.current_candle = {
                'timestamp': candle_start,
                'open': minute_bar['open_prc'],
                'high': minute_bar['high_prc'],
                'low': minute_bar['low_prc'],
                'close': minute_bar['close_prc'],
                'volume': minute_bar['volume']
            }
            
            # Return True if we just completed a candle
            return self.last_completed is not None
        
        else:
            # Update the current developing candle
            self.current_candle['high'] = max(self.current_candle['high'], minute_bar['high_prc'])
            self.current_candle['low'] = min(self.current_candle['low'], minute_bar['low_prc'])
            self.current_candle['close'] = minute_bar['close_prc']
            self.current_candle['volume'] += minute_bar['volume']
            
            return False
    
    def get_completed_candle(self) -> Dict:
        """Get the last completed candle."""
        return self.last_completed
    
    def get_current_developing_candle(self) -> Dict:
        """Get the current developing (incomplete) candle."""
        return self.current_candle


#<=====>#
# Functions
#<=====>#

@narc(1)
def backtest_strategy(
    bot_instance,
    prod_id: str,
    start_date: str,
    end_date: str,
    starting_balance: float = 10000.0,
    strategy_name: Optional[str] = None
) -> Dict:
    """
    Run backtest for a single product and optional specific strategy.
    
    Args:
        bot_instance: Bot instance with all trading logic
        prod_id: Product to backtest (e.g., 'BTC-USDC')
        start_date: Start date 'YYYY-MM-DD'
        end_date: End date 'YYYY-MM-DD'
        starting_balance: Starting capital
        strategy_name: Optional - test only one strategy
        
    Returns:
        Dictionary with results
    """
    # Import the shared OHLCV database connection
    from libs.db_mysql.ohlcv.db_main import db_ohlcv
    
    # Initialize backtest engine
    engine = BacktestEngine(bot_instance, db_ohlcv)
    
    # Run backtest
    results = engine.run_backtest(
        prod_id=prod_id,
        start_date=start_date,
        end_date=end_date,
        starting_balance=starting_balance
    )
    
    return results


@narc(1)
def optimize_strategy_parameters(
    bot_instance,
    prod_id: str,
    strategy_name: str,
    param_ranges: Dict,
    start_date: str,
    end_date: str,
    optimization_metric: str = 'sharpe_ratio'
) -> Dict:
    """
    Optimize strategy parameters using grid search or similar.
    
    Args:
        bot_instance: Bot instance
        prod_id: Product to optimize on
        strategy_name: Strategy to optimize
        param_ranges: Dict of parameter names to ranges
        start_date: Training period start
        end_date: Training period end
        optimization_metric: Metric to optimize ('sharpe_ratio', 'total_return', 'win_rate')
        
    Returns:
        Dict with best parameters and performance
    """
    
    # TODO: Implement parameter optimization
    # 1. Generate parameter combinations from ranges
    # 2. Run backtest for each combination
    # 3. Rank by optimization metric
    # 4. Return best parameters
    
    pass


@narc(1)
def walk_forward_optimization(
    bot_instance,
    prod_id: str,
    strategy_name: str,
    param_ranges: Dict,
    total_start: str,
    total_end: str,
    train_months: int = 6,
    test_months: int = 1
) -> Dict:
    """
    Walk-forward optimization to avoid overfitting.
    
    Args:
        bot_instance: Bot instance
        prod_id: Product to optimize
        strategy_name: Strategy to optimize
        param_ranges: Parameter ranges to test
        total_start: Overall start date
        total_end: Overall end date
        train_months: Months in training window
        test_months: Months in test window
        
    Returns:
        Dict with walk-forward results
    """
    
    # TODO: Implement walk-forward optimization
    # 1. Split time period into train/test windows
    # 2. Optimize on train, test on following period
    # 3. Roll forward and repeat
    # 4. Aggregate out-of-sample results
    
    pass


#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#
