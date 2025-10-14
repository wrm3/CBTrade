#<=====>#
# Description
#<=====>#
"""
🔧 OHLCV UNIFIED DATABASE MODULE
CBTrade Centralized OHLCV Operations - MySQL Implementation
 
This module provides OHLCV operations for trading pair data:
- Database operations (MySQL) 
- Single table per trading pair with freq column to differentiate timeframes
- Proper MySQL timestamp handling with Unix timestamp synchronization
- Timestamp corruption protection via triggers
- Data processing and validation

Author: MySQL implementation with improved error handling
Priority: CRITICAL - Prevent data destruction
"""

#<=====>#
# Imports - Public
#<=====>#
import os
import sys
import numpy as np
import pandas as pd
import re
import sqlparse
import time
import traceback
from datetime import datetime as dt, timezone, timedelta
from dotenv import load_dotenv
from fstrent_colors import *
from fstrent_charts import *
from pathlib import Path

#<=====>#
# Imports - Project  
#<=====>#
from libs.common import dttm_get, narc, beep, print_adv
from libs.theme import chrt
from libs.db_mysql.mysql_handler import MySQLDB

#<=====>#
# Environment & Database Setup
#<=====>#

# Load environment variables from .env file
load_dotenv()

# Get MySQL connection details from environment
db_host = os.getenv('DB_OHLCV_HOST', 'localhost')
db_port = int(os.getenv('DB_OHLCV_PORT', '3306'))
db_name = os.getenv('DB_OHLCV_NAME', 'ohlcv')
db_user = os.getenv('DB_OHLCV_USER', 'ohlcv')
db_pw = os.getenv('DB_OHLCV_PW', 'ohlcv')

# Create global database connection for module-level functions
db_ohlcv = MySQLDB(db_host=db_host, db_port=db_port, db_name=db_name, db_user=db_user, db_pw=db_pw)

#<=====>#
# Helper Functions
#<=====>#

@narc(1)
def db_safe_string(in_str):
    """Sanitize strings for database operations"""
    # Regular expression pattern to match allowed characters
    allowed_chars_pattern = r"[^a-zA-Z0-9\s\.,;:'\"?!@#\$%\^&\*\(\)_\+\-=\[\]\{\}<>\/\\]"
    # Replace characters not in the allowed set with an empty string
    out_str = re.sub(allowed_chars_pattern, '', in_str)
    return out_str

#<=====>#
# Classes
#<=====>#

class OHLCV_DB:
    """
    🔧 MySQL OHLCV database handler for trading pair data
    
    Features:
    - Single table per trading pair with freq column
    - Consistent timeframe handling
    - Proper upsert operations for data integrity
    - No data truncation - preserves existing records
    - Unix timestamp synchronization with datetime fields
    """
    
    # Supported timeframes
    TIMEFRAMES = {
        '1min': {'seconds': 59, 'table': 'ohlcv'},
        '3min': {'seconds': 179, 'table': 'ohlcv'},
        '5min': {'seconds': 299, 'table': 'ohlcv'},
        '15min': {'seconds': 899, 'table': 'ohlcv'},
        '30min': {'seconds': 1799, 'table': 'ohlcv'},
        '1h': {'seconds': 3599, 'table': 'ohlcv'},
        '4h': {'seconds': 14399, 'table': 'ohlcv'},
        '1d': {'seconds': 86399, 'table': 'ohlcv'}
    }

    def __init__(self, prod_id):
        """
        Initialize OHLCV database handler for specific trading pair
        
        Args:
            prod_id: Trading pair (e.g., 'BTC-USDC')
        """
        self.prod_id = prod_id
        self.safe_prod_id = prod_id.replace('-', '_')
        self.table_name = f"ohlcv_{self.safe_prod_id}"
        
        # Use global database connection
        self.db = db_ohlcv
        
        # Ensure the table exists for this trading pair
        self._ensure_table_exists()

    #<=====>#

    @narc(1)
    def _ensure_table_exists(self):
        """Create the OHLCV table if it doesn't exist"""
        # Check if table exists
        sql = f"""
        SELECT COUNT(*) 
        FROM information_schema.TABLES 
        WHERE table_schema = '{db_name}' 
        AND table_name = '{self.table_name}'
        """
        table_exists = self.db.sel(sql) > 0
        
        if not table_exists:
            # Create table if it doesn't exist
            print(f"Creating OHLCV table {self.table_name} for {self.prod_id}")
            
            sql = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                timestamp TIMESTAMP NOT NULL,
                freq VARCHAR(64) NOT NULL,
                open DECIMAL(36, 12),
                high DECIMAL(36, 12),
                low DECIMAL(36, 12),
                close DECIMAL(36, 12),
                volume DECIMAL(36, 12),
                start_dttm TIMESTAMP,
                end_dttm TIMESTAMP,
                upd_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                dlm TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                start_unix BIGINT DEFAULT 0,
                end_unix BIGINT DEFAULT 0,
                upd_unix BIGINT DEFAULT 0,
                dlm_unix BIGINT DEFAULT 0,
                PRIMARY KEY (freq, timestamp)
            )
            """
            self.db.execute(sql)
            
            # Create triggers for timestamp synchronization
            self._create_triggers()

    #<=====>#

    @narc(1)
    def _create_triggers(self):
        """Create triggers to synchronize Unix timestamps and datetime fields"""
        # Check for insert trigger
        sql = f"""
        SELECT COUNT(*) 
        FROM information_schema.TRIGGERS 
        WHERE event_object_schema = '{db_name}' 
        AND event_object_table = '{self.table_name}'
        AND trigger_name = 'before_insert_{self.table_name}'
        """
        insert_trigger_exists = self.db.sel(sql) > 0
        
        # Check for update trigger
        sql = f"""
        SELECT COUNT(*) 
        FROM information_schema.TRIGGERS 
        WHERE event_object_schema = '{db_name}' 
        AND event_object_table = '{self.table_name}'
        AND trigger_name = 'before_update_{self.table_name}'
        """
        update_trigger_exists = self.db.sel(sql) > 0
        
        try:
            # Create INSERT trigger if needed
            if not insert_trigger_exists:
                print(f"Creating INSERT trigger for {self.table_name}")
                sql = f"""
                CREATE TRIGGER before_insert_{self.table_name} 
                BEFORE INSERT ON {self.table_name} 
                FOR EACH ROW 
                BEGIN 
                    -- Set Unix timestamp first if not already set
                    IF NEW.start_unix = 0 AND NEW.start_dttm IS NOT NULL THEN
                        SET NEW.start_unix = UNIX_TIMESTAMP(NEW.start_dttm);
                    END IF;
                    
                    IF NEW.end_unix = 0 AND NEW.end_dttm IS NOT NULL THEN
                        SET NEW.end_unix = UNIX_TIMESTAMP(NEW.end_dttm);
                    END IF;
                    
                    IF NEW.upd_unix = 0 AND NEW.upd_dttm IS NOT NULL THEN
                        SET NEW.upd_unix = UNIX_TIMESTAMP(NEW.upd_dttm);
                    END IF;
                    
                    IF NEW.dlm_unix = 0 AND NEW.dlm IS NOT NULL THEN
                        SET NEW.dlm_unix = UNIX_TIMESTAMP(NEW.dlm);
                    END IF;
                    
                    -- Then derive datetime from Unix timestamp
                    IF NEW.start_unix > 0 AND NEW.start_dttm IS NULL THEN
                        SET NEW.start_dttm = FROM_UNIXTIME(NEW.start_unix);
                    END IF;
                    
                    IF NEW.end_unix > 0 AND NEW.end_dttm IS NULL THEN
                        SET NEW.end_dttm = FROM_UNIXTIME(NEW.end_unix);
                    END IF;
                    
                    IF NEW.upd_unix > 0 AND NEW.upd_dttm IS NULL THEN
                        SET NEW.upd_dttm = FROM_UNIXTIME(NEW.upd_unix);
                    END IF;
                    
                    IF NEW.dlm_unix > 0 AND NEW.dlm IS NULL THEN
                        SET NEW.dlm = FROM_UNIXTIME(NEW.dlm_unix);
                    END IF;
                END
                """
                self.db.execute(sql)
            
            # Create UPDATE trigger if needed
            if not update_trigger_exists:
                print(f"Creating UPDATE trigger for {self.table_name}")
                sql = f"""
                CREATE TRIGGER before_update_{self.table_name} 
                BEFORE UPDATE ON {self.table_name} 
                FOR EACH ROW 
                BEGIN 
                    -- Set Unix timestamp first if not already set
                    IF NEW.start_unix = 0 AND NEW.start_dttm IS NOT NULL THEN
                        SET NEW.start_unix = UNIX_TIMESTAMP(NEW.start_dttm);
                    END IF;
                    
                    IF NEW.end_unix = 0 AND NEW.end_dttm IS NOT NULL THEN
                        SET NEW.end_unix = UNIX_TIMESTAMP(NEW.end_dttm);
                    END IF;
                    
                    IF NEW.upd_unix = 0 AND NEW.upd_dttm IS NOT NULL THEN
                        SET NEW.upd_unix = UNIX_TIMESTAMP(NEW.upd_dttm);
                    END IF;
                    
                    IF NEW.dlm_unix = 0 AND NEW.dlm IS NOT NULL THEN
                        SET NEW.dlm_unix = UNIX_TIMESTAMP(NEW.dlm);
                    END IF;
                    
                    -- Then derive datetime from Unix timestamp
                    IF NEW.start_unix > 0 AND NEW.start_dttm IS NULL THEN
                        SET NEW.start_dttm = FROM_UNIXTIME(NEW.start_unix);
                    END IF;
                    
                    IF NEW.end_unix > 0 AND NEW.end_dttm IS NULL THEN
                        SET NEW.end_dttm = FROM_UNIXTIME(NEW.end_unix);
                    END IF;
                    
                    IF NEW.upd_unix > 0 AND NEW.upd_dttm IS NULL THEN
                        SET NEW.upd_dttm = FROM_UNIXTIME(NEW.upd_unix);
                    END IF;
                    
                    IF NEW.dlm_unix > 0 AND NEW.dlm IS NULL THEN
                        SET NEW.dlm = FROM_UNIXTIME(NEW.dlm_unix);
                    END IF;
                END
                """
                self.db.execute(sql)
                
        except Exception as e:
            if "Trigger already exists" in str(e):
                pass  # Silently continue if trigger already exists
            else:
                print(f"Error creating triggers: {e}")
                traceback.print_exc()

    #<=====>#

    @narc(1)
    def load_ohlcv_data(self, timeframe, limit=500, start_date=None, end_date=None):
        """
        🔽 Load OHLCV data from MySQL table into DataFrame
        
        Args:
            timeframe (str): '1min', '3min', '5min', etc.
            limit (int, optional): Maximum number of records to return
            start_date (str, optional): Start date filter (YYYY-MM-DD format)
            end_date (str, optional): End date filter (YYYY-MM-DD format)
            
        Returns:
            pd.DataFrame: OHLCV data with proper datetime columns
            
        Example:
            df = db.load_ohlcv_data('1min', limit=1000)
            df = db.load_ohlcv_data('1h', start_date='2025-01-01')
        """
        if timeframe not in self.TIMEFRAMES:
            raise ValueError(f"Invalid timeframe '{timeframe}'. Must be one of: {list(self.TIMEFRAMES.keys())}")
        
        # Build SQL query
        sql = f"""
        SELECT * FROM {self.table_name} 
        WHERE freq = '{timeframe}'
        """
        
        # Add date filters
        if start_date:
            sql += f" AND start_dttm >= '{start_date}'"
        if end_date:
            sql += f" AND start_dttm <= '{end_date}'"
        
        # Order by timestamp
        sql += " ORDER BY timestamp DESC"
        
        # Add limit (default 500)
        if not limit:
            limit = 500
        sql += f" LIMIT {limit}"
        
        try:
            # Get data from database
            result = self.db.seld(sql)

            if not result:
                return pd.DataFrame()  # Empty DataFrame if no results

            # Defensive: sanitize records to plain python scalars to avoid pandas dtype segfaults
            # (bytes → str, Decimal → float, numpy scalar → python scalar)
            try:
                from decimal import Decimal
                import numpy as _np
            except Exception:
                Decimal = None  # type: ignore
                _np = None  # type: ignore

            rows = []
            for rec in result:
                clean = {}
                for k, v in rec.items():
                    if v is None:
                        clean[k] = None
                    elif Decimal is not None and isinstance(v, Decimal):
                        clean[k] = float(v)
                    elif isinstance(v, (bytes, bytearray)):
                        try:
                            clean[k] = v.decode('utf-8', 'ignore')
                        except Exception:
                            clean[k] = str(v)
                    elif _np is not None and isinstance(v, _np.generic):
                        clean[k] = v.item()
                    else:
                        clean[k] = v
                rows.append(clean)

            # Convert to DataFrame
            df = pd.DataFrame.from_records(rows)
            # Normalize column dtypes to avoid extension blocks
            for c in list(df.columns):
                if c.lower() in ('open','high','low','close','volume','curr_prc','atr') or c.endswith(('_prc','_val')):
                    df[c] = pd.to_numeric(df[c], errors='coerce').astype('float64')

            # Convert timestamp columns to datetime objects (coerce bad rows rather than error)
            for col in ['timestamp', 'start_dttm', 'end_dttm', 'upd_dttm', 'dlm']:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce', utc=False)

            # Set timestamp as index if present
            if 'timestamp' in df.columns:
                df = df.set_index('timestamp')

            # Final guard: ensure index is a DatetimeIndex and drop NaT rows
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index, errors='coerce')
            df = df[~df.index.isna()]

            return df
            
        except Exception as e:
            print(f"❌ Error loading {timeframe} data: {e}")
            traceback.print_exc()
            return pd.DataFrame()  # Return empty DataFrame on error

    #<=====>#

    @narc(1)
    def save_ohlcv_data(self, freq, df):
        """
        Save OHLCV DataFrame to MySQL database with proper upsert handling
        
        BEHAVIOR:
        - Preserves ALL existing data in table
        - Updates any duplicate timestamps (forming candles)
        - Inserts new timestamps that don't exist
        - NO truncation of existing data
        
        Args:
            freq: Timeframe (e.g., '1min', '5min')
            df: pandas.DataFrame with OHLCV data and datetime index
            
        Returns:
            dict: Statistics about the operation
        """
        if df.empty:
            return {'inserted': 0, 'updated': 0, 'total_processed': 0}
        
        # Pre-clean: drop any rows with index before 2017-01-01 (or NaT)
        try:
            MIN_IDX_TS = pd.Timestamp('2017-01-01 00:00:00')
            if isinstance(df.index, pd.DatetimeIndex):
                _orig = len(df)
                df = df.loc[(~df.index.isna()) & (df.index >= MIN_IDX_TS)]
                _dropped = _orig - len(df)
                if _dropped > 0:
                    print(f"⚠️ Dropped {_dropped} rows with timestamps < 2017-01-01 from incoming df for {self.prod_id} {freq}")
        except Exception:
            pass


        # Make a copy to avoid modifying the original and cap to last 500 rows
        df_prep = df.tail(500).copy()
        
        # Ensure we have a datetime index
        if not isinstance(df_prep.index, pd.DatetimeIndex):
            raise ValueError("DataFrame must have a DatetimeIndex")
        
        # Add timeframe identifier
        df_prep['freq'] = freq
        
        # Add datetime columns
        df_prep['start_dttm'] = df_prep.index
        
        # Calculate end times based on frequency
        freq_seconds = self.TIMEFRAMES[freq]['seconds']
        end_times = df_prep.index + pd.Timedelta(seconds=freq_seconds)
        df_prep['end_dttm'] = end_times
        
        # Add Unix timestamps for accurate time handling
        df_prep['start_unix'] = df_prep.index.astype('int64') // 10**9
        df_prep['end_unix'] = end_times.astype('int64') // 10**9
        df_prep['upd_unix'] = int(time.time())

        # Reset index to prepare for database insertion
        df_prep = df_prep.reset_index().rename(columns={'index': 'timestamp'})
        
        # Validate timestamps: drop invalid/epoch rows (<2017 or NaT); halt only if all invalid
        try:
            MIN_TS = pd.Timestamp('2017-01-01 00:00:00')
            required_cols = ['timestamp', 'start_dttm', 'end_dttm']
            for col in required_cols:
                if col not in df_prep.columns:
                    raise ValueError(f"Missing required time column: {col}")
            bad_mask = (
                df_prep['timestamp'].isna() |
                df_prep['start_dttm'].isna() |
                df_prep['end_dttm'].isna() |
                (df_prep['timestamp'] < MIN_TS) |
                (df_prep['start_dttm'] < MIN_TS) |
                (df_prep['end_dttm'] < MIN_TS)
            )
            if bad_mask.any():
                cols_dbg = ['timestamp','start_dttm','end_dttm','start_unix','end_unix','freq']
                cols_dbg = [c for c in cols_dbg if c in df_prep.columns]
                print(f"⚠️ Invalid/epoch timestamps detected for {self.prod_id} {freq}. Dropping {int(bad_mask.sum())} row(s).")
                try:
                    print("── offending rows (up to 5) ──")
                    print(df_prep.loc[bad_mask, cols_dbg].head(5))
                except Exception:
                    pass
                df_prep = df_prep.loc[~bad_mask]
                if df_prep.empty:
                    print(f"❌ FATAL: All rows invalid after drop for {self.prod_id} {freq}; nothing to save.")
                    traceback.print_stack()
                    sys.exit(1)
        except Exception as _vex:
            print(f"❌ FATAL: Validation failure while checking timestamps: {_vex}")
            traceback.print_exc()
            sys.exit(1)
        
        # Convert to records for database insertion
        records = df_prep.to_dict(orient='records')

        # Fix: Check records before calling:
        if not records:
            print(f"⚠️ No records to save for {self.table_name}, skipping...")
            beep()
            return {'inserted': 0, 'updated': 0, 'total_processed': 0}

        # Insert/update records in database
        try:
            # Let the MySQL handler do the upsert handling
            db_tbl_insupd(self.table_name, records, exit_on_error=True)
            
            return {
                'inserted': len(records),  # Can't differentiate inserts vs updates here
                'updated': 0,
                'total_processed': len(records)
            }
        except Exception as e:
            print(f"❌ FATAL: Error saving {freq} data to {self.table_name}: {e}")
            try:
                sample = records[:3]
                print(f"Sample failing payload (first 3): {sample}")
            except Exception:
                pass
            traceback.print_exc()
            sys.exit(1)

    #<=====>#

    @narc(1)
    def db_ohlcv_prod_id_freqs(self):
        """
        🔧 Get frequency summary for a trading pair
        
        Returns:
            List of dictionaries with frequency data in the format ta_ohlcv expects:
            [{'freq': '1min', 'last_start_dttm': datetime_obj, 'last_start_unix': timestamp}, ...]
        """
        sql = f"""
        SELECT DISTINCT freq
          , MAX(start_dttm) AS last_start_dttm
          , UNIX_TIMESTAMP(MAX(start_dttm)) AS last_start_unix
        FROM {self.table_name}
        GROUP BY freq
        """
        
        try:
            result = self.db.seld(sql)
            return result if result else []
        except Exception as e:
            print(f"Error getting frequency data: {e}")
            return []

    #<=====>#

    @narc(1)
    def get_latest_timestamp(self, freq):
        """
        Get the latest timestamp for a specific timeframe
        
        Args:
            freq: Timeframe (e.g., '1min', '5min')
            
        Returns:
            datetime or None: Latest timestamp in the table
        """
        sql = f"""
        SELECT MAX(timestamp) as latest_timestamp
        FROM {self.table_name}
        WHERE freq = '{freq}'
        """
        
        try:
            result = self.db.seld(sql)
            
            if result and isinstance(result, dict) and result.get('latest_timestamp'):
                return result['latest_timestamp']
            return None
        except Exception as e:
            print(f"Error getting latest timestamp: {e}")
            return None

    #<=====>#

    @narc(1)
    def get_record_count(self, freq):
        """
        Get total number of records for a timeframe
        
        Args:
            freq: Timeframe (e.g., '1min', '5min')
            
        Returns:
            int: Number of records in table
        """
        sql = f"""
        SELECT COUNT(*) as count 
        FROM {self.table_name}
        WHERE freq = '{freq}'
        """
        
        try:
            result = self.db.sel(sql)
            return result if result else 0
        except Exception as e:
            print(f"Error getting record count: {e}")
            return 0

    #<=====>#

    @narc(1)
    def get_timeframe_summary(self):
        """
        Get summary statistics for all timeframes
        
        Returns:
            dict: Summary stats per timeframe
        """
        summary = {}
        
        for freq in self.TIMEFRAMES.keys():
            try:
                # Get latest timestamp and count in one query for efficiency
                sql = f"""
                SELECT 
                    COUNT(*) as count,
                    MAX(timestamp) as latest_timestamp
                FROM {self.table_name}
                WHERE freq = '{freq}'
                """
                result = self.db.seld(sql)
                
                if result and isinstance(result, dict):
                    summary[freq] = {
                        'count': result.get('count', 0),
                        'latest_timestamp': result.get('latest_timestamp'),
                        'table_name': self.table_name
                    }
                else:
                    summary[freq] = {
                        'count': 0,
                        'latest_timestamp': None,
                        'table_name': self.table_name
                    }
            except Exception as e:
                summary[freq] = {
                    'count': 0,
                    'latest_timestamp': None,
                    'error': str(e),
                    'table_name': self.table_name
                }
        
        return summary

    #<=====>#

    @narc(1)
    def db_ohlcv_candle_status_display(self, display_enabled=True, ta_frames: dict | None = None):
        """
        🔧 EXPECTED FUNCTION NAME - Wrapper for restored age display
        This is the function name that pair_base.py expects to call
        
        Args:
            display_enabled: Whether to print status (default: True)
        """
        self.display_candle_status_with_age(self.prod_id, display_enabled, ta_frames=ta_frames)

    #<=====>#

    @narc(1)
    def display_candle_status_with_age(self, prod_id, display_enabled=True, ta_frames: dict | None = None):
        """
        🔧 MySQL OHLCV AGE DISPLAY FUNCTION 
        Display OHLCV candle status with data age for all timeframes
        
        Args:
            prod_id: Trading pair identifier
            display_enabled: Whether to print status (default: True)
        """
        if not display_enabled:
            return
        
        tmsg = f'{prod_id} - OHLCV STATUS WITH AGE'
        print_adv()
        chrt.chart_top(tmsg, len_cnt=260, align='left')
        # Ensure we're using the same product ID format
        if prod_id != self.prod_id:
            safe_prod_id = prod_id.replace('-', '_')
            table_name = f"ohlcv_{safe_prod_id}"
        else:
            table_name = self.table_name
            
        # print(f"🔧 OHLCV STATUS WITH AGE: {prod_id}")
        
        try:
            # Check if table exists
            sql = f"""
            SELECT COUNT(*) 
            FROM information_schema.TABLES 
            WHERE table_schema = '{db_name}' 
            AND table_name = '{table_name}'
            """
            table_exists = self.db.sel(sql) > 0
            
            if not table_exists:
                print(f"❌ NO TABLE: {prod_id} - {table_name}")
                return
            
            # Standard timeframes to check
            timeframes = ['1min', '3min', '5min', '15min', '30min', '1h', '4h', '1d']
            current_time = time.time()

            # Baseline recency from finest timeframe (1min)
            try:
                sql_latest_1m = f"""
                SELECT UNIX_TIMESTAMP(MAX(timestamp)) AS latest_1m_unix
                FROM {table_name}
                WHERE freq = '1min'
                """
                latest_1m_row = self.db.seld(sql_latest_1m)
                if isinstance(latest_1m_row, list):
                    latest_1m_row = latest_1m_row[0] if latest_1m_row else {}
                latest_1m_unix = int(latest_1m_row.get('latest_1m_unix') or 0)
            except Exception:
                latest_1m_unix = 0
            
            hmsg = ""
            hmsg += f"{'TIMEFRAME':^10} | "
            hmsg += f"{'RECORDS':^8} | "
            hmsg += f"{'TA(≤500)':^8} | "
            hmsg += f"{'LAST UPDATE':^20} | "
            hmsg += f"{'AGE':^15} | "
            hmsg += f"{'CLOSE PRICE':^25} | "
            hmsg += f"{'STATUS':^10}"
            # print(hmsg)
            chrt.chart_headers(in_str=hmsg, bold=True, align='left', len_cnt=260)

            for timeframe in timeframes:
                # Get record count, latest timestamp, and close price in one query
                sql = f"""
                SELECT 
                    COUNT(*) as count, 
                    MAX(timestamp) as latest_timestamp,
                    (SELECT close FROM {table_name} WHERE freq = '{timeframe}' ORDER BY timestamp DESC LIMIT 1) as latest_close,
                    UNIX_TIMESTAMP(MAX(timestamp)) as unix_timestamp
                FROM {table_name}
                WHERE freq = '{timeframe}'
                """
                
                result = self.db.seld(sql)
                # Normalize DB return shape (may be list of one row)
                if isinstance(result, list):
                    result = result[0] if result else {}
                
                if not result or not isinstance(result, dict):
                    msg = f"   {timeframe:<10} | {'NO DATA':<8} | {'N/A':<19} | {'N/A':<15} | {'N/A':>25} | ❌ MISSING"
                    continue
                    
                count = result.get('count', 0)
                # Determine TA display count: prefer provided TA frame length if available
                display_count = None
                if ta_frames and timeframe in ta_frames and hasattr(ta_frames[timeframe], '__len__'):
                    try:
                        display_count = min(len(ta_frames[timeframe]), 500)
                    except Exception:
                        display_count = None
                # Fallback to min(DB count, cap) when TA not provided
                if display_count is None:
                    display_count = min(int(count or 0), 500)
                latest_timestamp = result.get('latest_timestamp')
                latest_close = result.get('latest_close')
                unix_timestamp = result.get('unix_timestamp')
                
                if count == 0:
                    msg = f"   {timeframe:<10} | {0:<8} | {0:<8} | {'NO DATA':<19} | {'N/A':<15} | {'N/A':>25} | ❌ EMPTY"
                    continue
                
                # AGE is measured against latest 1min timestamp so all frames
                # share the same recency during forming
                age_basis_unix = latest_1m_unix if latest_1m_unix > 0 else int(unix_timestamp or 0)

                if age_basis_unix:
                    # Calculate age
                    age_seconds = current_time - age_basis_unix
                    
                    # Format age display
                    if age_seconds < 60:
                        age_display = f"{age_seconds:.0f}s"
                        age_status = "🟢 FRESH"
                    elif age_seconds < 3600:  # Less than 1 hour
                        age_display = f"{age_seconds/60:.1f}m"
                        age_status = "🟡 RECENT" if age_seconds < 1800 else "🟠 AGING"
                    elif age_seconds < 86400:  # Less than 1 day
                        age_display = f"{age_seconds/3600:.1f}h"
                        age_status = "🟠 OLD"
                    else:  # More than 1 day
                        age_display = f"{age_seconds/86400:.1f}d"
                        age_status = "🔴 STALE"
                    
                    # Format last update time
                    last_update = latest_timestamp.strftime('%Y-%m-%d %H:%M:%S') if hasattr(latest_timestamp, 'strftime') else str(latest_timestamp)
                    
                    # Display with appropriate color coding based on age
                    try:
                        if latest_close is not None:
                            price_display = f"{float(latest_close):>25.16f}"
                        else:
                            price_display = f"{'N/A':>25}"
                            
                        msg = f"   {timeframe:<10} | {count:<8} | {display_count:<8} | {last_update:<19} | {age_display:<15} | {price_display} | {age_status}"
                    except Exception as e:
                        msg = f"   {timeframe:<10} | {count:<8} | {display_count:<8} | {last_update:<19} | {age_display:<15} | {'ERROR':>25} | {age_status}"
                else:
                    msg = f"{timeframe:<10} | {count:<8} | {display_count:<8} | {'NULL TIMESTAMP':<19} | {'N/A':<15} | {'N/A':>25} | ❌ CORRUPT"

                chrt.chart_row(msg, bold=True, len_cnt=260)
            chrt.chart_bottom(bold=True, len_cnt=260)
                
        except Exception as e:
            print(f"❌ ERROR: Could not display age status for {prod_id}: {e}")
            traceback.print_exc()

    #<=====>#

    @narc(1)
    def display_comprehensive_age_status(self, prod_ids=None, display_enabled=True):
        """
        🔧 COMPREHENSIVE AGE STATUS DISPLAY
        Display OHLCV age status for multiple trading pairs
        
        Args:
            prod_ids: List of trading pairs (None for all available)
            display_enabled: Whether to print status (default: True)
        """
        if not display_enabled:
            return
            
        if prod_ids is None:
            # Get all available OHLCV tables from database
            sql = """
            SELECT table_name 
            FROM information_schema.TABLES 
            WHERE table_schema = %s
            AND table_name LIKE 'ohlcv_%'
            """
            results = self.db.seld(sql, (db_name,))
            
            if results:
                prod_ids = []
                for row in results:
                    table_name = row['table_name']
                    if table_name.startswith('ohlcv_'):
                        # Convert table name back to product ID
                        prod_id = table_name[6:].replace('_', '-').upper()
                        prod_ids.append(prod_id)
        
        if not prod_ids:
            print("❌ NO PAIRS: No OHLCV tables found")
            return
        
        print(f"🔧 COMPREHENSIVE OHLCV AGE STATUS for {len(prod_ids)} pairs")
        print("=" * 100)
        
        for i, prod_id in enumerate(sorted(prod_ids)):
            db = OHLCV_DB(prod_id)  # Create new instance for each product ID
            db.display_candle_status_with_age(prod_id, display_enabled=True)
            if i < len(prod_ids) - 1:  # Don't print separator after last pair
                print()
        
        print("=" * 100)

#<=====>#
# Helper Functions from cls_bot_db_ohlcv.py
#<=====>#

@narc(1)
def db_tbl_del(table_name):
    """Delete all records from a table"""
    sql = f"DELETE FROM {table_name}"
    db_ohlcv.execute(sql)

#<=====>#

@narc(1)
def db_tbl_insupd(table_name, in_data, rat_on_extra_cols_yn='N', exit_on_error=True):
    """
    Insert or update records in a table with upsert handling
    
    Args:
        table_name: Table to insert/update
        in_data: Dictionary or list of dictionaries with data
        rat_on_extra_cols_yn: Whether to report extra columns not in table
        exit_on_error: Whether to exit on error
    """
    tbl_cols = db_ohlcv.table_cols(table=table_name)
    data_cols = []
    ins_data = []

    if isinstance(in_data, dict):
        if in_data:
            ins_type = 'one'
            if 'add_dttm' in in_data: del in_data['add_dttm']
            if 'dlm' in in_data: del in_data['dlm']
            for k in in_data:
                if k in tbl_cols:
                    data_cols.append(k)
            for k in in_data:
                if k in tbl_cols:
                    ins_data.append(in_data[k])
                else:
                    if rat_on_extra_cols_yn == 'Y':
                        print(f'column : {k} not defined in table {table_name}...')

    # received a list of dictionaries
    elif isinstance(in_data, list):
        ins_data = []
        if in_data:
            if isinstance(in_data[0], dict):
                ins_type = 'many'
                # populating data_cols with all the distinct columns names 
                # from data and checking against table
                for r in in_data:
                    if 'add_dttm' in r: del r['add_dttm']
                    if 'dlm' in r: del r['dlm']
                    for k in r:
                        if k not in data_cols:
                            if k in tbl_cols:
                                data_cols.append(k)
                            else:
                                if table_name not in ('currs'):
                                    if rat_on_extra_cols_yn == 'Y':
                                        print(f'column : {k} not defined in table {table_name}...')
                # looping through data to standardize for inserts
                for r in in_data:
                    ins_dict = {}
                    # prepopulate with None, which will become null 
                    for k in data_cols: ins_dict[k] = None
                    # assign actual values from data when present
                    for k in r:
                        if k in tbl_cols:
                            ins_dict[k] = r[k]
                    # preparing list of the dict values for the insert
                    ins_list = []
                    for k in data_cols:
                        ins_list.append(ins_dict[k])
                    # adding the row list to the big list for inserts
                    ins_data.append(ins_list)

    if not data_cols:
        print(f"⚠️ No valid columns/data to insert for table {table_name}")
        beep()
        return

    sql1 = f" INSERT INTO {table_name} ( "
    sql2 = ", ".join(data_cols)
    sql3 = " ) VALUES ( "
    sql4 = ', '.join(['%s'] * len(data_cols))
    sql5 = " ) ON DUPLICATE KEY UPDATE  "

    col1 = data_cols[0]
    sql6 = f' {col1} = VALUES({col1})'
    for col in data_cols:
        if col != col1:
            sql6 += f', {col} = VALUES({col})'

    sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6

    try:
        if ins_type == 'one':
            db_ohlcv.ins_one(sql=sql, vals=ins_data, exit_on_error=exit_on_error)
        else:
            db_ohlcv.ins_many(sql=sql, vals=ins_data, exit_on_error=exit_on_error)
    except Exception as e:
        print(f"Error in db_tbl_insupd: {e}")
        if exit_on_error:
            raise

#<=====>#

@narc(1)
def db_ohlcv_prod_id_freqs(prod_id):
    """
    Get frequency summary for a trading pair
    
    Args:
        prod_id: Trading pair (e.g., 'BTC-USDC')
    
    Returns:
        List of dictionaries with frequency data
    """
    safe_prod_id = prod_id.replace('-', '_')
    
    sql = f"""
    SELECT DISTINCT freq,
      MAX(start_dttm) as last_start_dttm,
      UNIX_TIMESTAMP(MAX(start_dttm)) as last_start_unix
    FROM ohlcv_{safe_prod_id}
    GROUP BY freq
    """
    
    try:
        last_dttms = db_ohlcv.seld(sql)
        return last_dttms if last_dttms else []
    except Exception as e:
        print(f"Error getting frequency data: {e}")
        return []

#<=====>#

@narc(1)
def db_ohlcv_freq_get(prod_id, freq, lmt=500):
    """
    Get OHLCV data for a specific pair and frequency
    
    Args:
        prod_id: Trading pair (e.g., 'BTC-USDC')
        freq: Timeframe (e.g., '1min', '5min')
        lmt: Maximum number of records to return
        
    Returns:
        List of dictionaries with OHLCV data
    """
    safe_prod_id = prod_id.replace('-', '_')
    
    sql = f"""
    SELECT * 
    FROM ohlcv_{safe_prod_id}
    WHERE freq = '{freq}'
    ORDER BY timestamp DESC
    LIMIT {lmt}
    """
    
    try:
        ohlcv = db_ohlcv.seld(sql)
        return ohlcv if ohlcv else []
    except Exception as e:
        print(f"Error getting OHLCV data: {e}")
        return []

#<=====>#

@narc(1)
def db_check_ohlcv_prod_id_table(prod_id):
    """
    Check if OHLCV table exists for a trading pair and create it if needed
    
    Args:
        prod_id: Trading pair (e.g., 'BTC-USDC')
    """
    # This function is now integrated into the OHLCV_DB._ensure_table_exists method
    # Just create an instance to ensure the table exists
    db = OHLCV_DB(prod_id)
    return True

#<=====>#

@narc(1)
def db_tbl_ohlcv_prod_id_insupd(prod_id, freq, in_df):
    """
    Insert/update OHLCV data for a specific pair and frequency
    
    Args:
        prod_id: Trading pair (e.g., 'BTC-USDC')
        freq: Timeframe (e.g., '1min', '5min')
        in_df: pandas DataFrame with OHLCV data
    """
    db = OHLCV_DB(prod_id)
    return db.save_ohlcv_data(freq, in_df)

#<=====>#

@narc(1)
def db_tbl_ohlcv_prod_id_insupd_many(prod_id, in_dfs):
    """
    Insert/update OHLCV data for a specific pair with multiple frequencies
    
    Args:
        prod_id: Trading pair (e.g., 'BTC-USDC')
        in_dfs: Dictionary of DataFrames keyed by frequency
    """
    db = OHLCV_DB(prod_id)
    all_results = {'inserted': 0, 'updated': 0, 'total_processed': 0}
    
    for freq, df in in_dfs.items():
        results = db.save_ohlcv_data(freq, df)
        all_results['inserted'] += results['inserted']
        all_results['updated'] += results['updated']
        all_results['total_processed'] += results['total_processed']
    
    return all_results

#<=====>#

@narc(1)
def db_ohlcv_table_names_get():
    """
    Get all OHLCV table names from database
    
    Returns:
        List of table names
    """
    sql = """
    SELECT CONCAT(table_schema, '.', table_name) as table_name
    FROM information_schema.TABLES
    WHERE table_schema = %s
    AND table_name LIKE 'ohlcv_%'
    """
    
    try:
        results = db_ohlcv.seld(sql, (db_name,))
        table_names = [row['table_name'] for row in results]
        return table_names
    except Exception as e:
        print(f"Error getting table names: {e}")
        return []

#<=====>#

@narc(1)
def db_ohlcv_dump(prod_id, freq='1min'):
    """
    Dump OHLCV data to CSV file
    
    Args:
        prod_id: Trading pair (e.g., 'BTC-USDC')
        freq: Timeframe (e.g., '1min', '5min')
    """
    safe_prod_id = prod_id.replace('-', '_')
    table_name = f"ohlcv_{safe_prod_id}"
    
    sql = f"""
    SELECT timestamp, freq, open, high, low, close, volume, 
           start_dttm, end_dttm, upd_dttm, dlm
    FROM {table_name}
    WHERE freq = '{freq}'
    """
    
    try:
        results = db_ohlcv.seld(sql)
        df = pd.DataFrame(results)
        
        # Create directory if it doesn't exist
        os.makedirs('ohlcv', exist_ok=True)
        
        csv_fname = f'ohlcv/{table_name}_table.csv'
        df.to_csv(csv_fname, index=True)
        print(f'{csv_fname:<60} saved...')
    except Exception as e:
        print(f"Error dumping OHLCV data: {e}")

#<=====>#
# Factory Functions
#<=====>#

@narc(1)
def create_ohlcv_db(prod_id):
    """
    Factory function to create OHLCV database instance
    
    Args:
        prod_id: Trading pair (e.g., 'BTC-USDC')
        
    Returns:
        OHLCV_DB: Initialized database instance
    """
    return OHLCV_DB(prod_id)

#<=====>#
# Convenience Functions for Age Display
#<=====>#

@narc(1)
def show_ohlcv_age(prod_id):
    """
    🔧 CONVENIENCE FUNCTION - Show OHLCV data age for specific pair
    
    Args:
        prod_id: Trading pair identifier (e.g., 'BTC-USDC')
        
    Usage:
        from libs.db_mysql.ohlcv.db_main import show_ohlcv_age
        show_ohlcv_age('BTC-USDC')
    """
    ohlcv_db = OHLCV_DB(prod_id)
    ohlcv_db.display_candle_status_with_age(prod_id)

#<=====>#

@narc(1)
def show_all_ohlcv_age(prod_ids=None):
    """
    🔧 CONVENIENCE FUNCTION - Show OHLCV data age for all pairs
    
    Args:
        prod_ids: List of trading pairs (None for all available)
        
    Usage:
        from libs.db_mysql.ohlcv.db_main import show_all_ohlcv_age
        show_all_ohlcv_age()  # All pairs
        show_all_ohlcv_age(['BTC-USDC', 'ETH-USDC'])  # Specific pairs
    """
    # Create a temporary instance to access the comprehensive display
    temp_db = OHLCV_DB('BTC-USDC')  # Dummy instance for method access
    temp_db.display_comprehensive_age_status(prod_ids)

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
    # Test the MySQL OHLCV structure
    print("🔧 Testing MySQL OHLCV Database Structure...")
    
    # Create test database for BTC-USDC
    db = create_ohlcv_db('BTC-USDC')
    
    # Show timeframe summary
    summary = db.get_timeframe_summary()
    print(f"\n📊 Timeframe Summary for {db.prod_id}:")
    for freq, stats in summary.items():
        count = stats.get('count', 0)
        latest = stats.get('latest_timestamp', 'None')
        print(f"  {freq:>6}: {count:>6} records | Latest: {latest}")
    
    print("\n✅ MySQL OHLCV Database structure ready!")
