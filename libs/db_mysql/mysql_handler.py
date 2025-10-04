#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
# Standard library imports
import datetime
import time
import sys
import traceback
import os
import platform
import random
import subprocess
from typing import List, Dict, Any, Optional, Tuple, Union

# Third-party imports
import aiomysql
import pymysql
import sqlparse
from fstrent_colors import G

from libs.common import dttm_get, beep, AttrDict, AttrDictConv, narc


#<=====>#
# Variables
#<=====>#
lib_display_lvl = 0
lib_debug_lvl = 1

#<=====>#

#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#

class MySQLDB:
    """
    Clean MySQL database interface for CBTrade
    """

#<=====>#

    def __init__(self, db_host: str, db_port: int, db_name: str, db_user: str, db_pw: str, auto_schema: bool = False):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_pw = db_pw
        self.auto_schema = auto_schema
        self.conn = None
        self._connection = None
        
        if auto_schema and self._has_schema_definition():
            if not self.ensure_schema_ready(verbose=False):
                raise Exception(f"Database schema initialization failed for {db_name}")

    #<=====>#
    # Windows service helper
    #<=====>#
    def _try_start_service_and_wait(self, service_name: str = 'MySQL80', total_wait_s: int = 60):
        try:
            if platform.system() != 'Windows':
                return
            # Attempt start via sc; if that fails, try net start
            try:
                subprocess.run(['sc', 'start', service_name], capture_output=True, text=True, timeout=10)
            except Exception:
                try:
                    subprocess.run(['net', 'start', service_name], capture_output=True, text=True, timeout=10)
                except Exception:
                    pass
            # Poll for RUNNING status
            deadline = time.time() + total_wait_s
            attempt = 0
            while time.time() < deadline:
                attempt += 1
                try:
                    q = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True, timeout=5)
                    out = (q.stdout or '').upper()
                    if 'RUNNING' in out:
                        return
                except Exception:
                    pass
                # small sleep between polls
                time.sleep(3)
        except Exception:
            # Never raise from helper
            pass

#<=====>#
    def _service_start_guard(self, total_wait_s: int = 120):
        """Windows-only: single-process guarded service start with wait."""
        try:
            if platform.system() != 'Windows':
                return
            lock_dir = os.environ.get('TEMP', os.getcwd())
            lock_path = os.path.join(lock_dir, 'cbtrade_mysql80.lock')
            got_lock = False
            try:
                # best-effort lock
                fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                got_lock = True
            except FileExistsError:
                # another process is handling service start
                return
            # try to start and wait
            self._try_start_service_and_wait('MySQL80', total_wait_s=total_wait_s)
        except Exception:
            pass
        finally:
            if 'got_lock' in locals() and got_lock:
                try:
                    os.remove(lock_path)
                except Exception:
                    pass

#<=====>#

    @narc(1)
    def _has_schema_definition(self) -> bool:
        """Check if this instance has schema methods overridden"""
        try:
            required_tables = self.get_required_tables()
            return bool(required_tables)
        except:
            return False

#<=====>#

    @narc(1)
    def __open(self):
        try:
            self.conn = pymysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                read_timeout=30,
                write_timeout=30,
                autocommit=True
            )
            self.__connection = self.conn
            self.__session = self.conn.cursor()
            # Set the session time zone to UTC
            self.__session.execute("SET time_zone = '+00:00';")
            # Mitigation for MySQL 8.0.4x utf8mb4_0900 bug paths during heavy aggregates
            try:
                self.__session.execute("SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;")
                self.__session.execute("SET collation_connection = 'utf8mb4_general_ci';")
            except Exception:
                pass
            self.__session.execute("SET GLOBAL log_bin_trust_function_creators = 1;")
        except (pymysql.Error, pymysql.Warning) as err:
            # If server not reachable, attempt to start service and retry once
            if isinstance(err, pymysql.OperationalError) and err.args and err.args[0] in (2003, 2006, 2013):
                self._try_start_service_and_wait('MySQL80', total_wait_s=90)
                # jittered pause to allow service warm-up
                try:
                    time.sleep(random.uniform(1.0, 3.0))
                except Exception:
                    pass
                # retry once, with guarded second retry on failure
                try:
                    self.conn = pymysql.connect(
                        host=self.db_host, 
                        port=self.db_port, 
                        db=self.db_name, 
                        user=self.db_user, 
                        password=self.db_pw,
                        connect_timeout=10,
                        read_timeout=30,
                        write_timeout=30,
                        autocommit=True
                    )
                except (pymysql.Error, pymysql.Warning):
                    try:
                        time.sleep(random.uniform(2.0, 5.0))
                    except Exception:
                        pass
                    self.conn = pymysql.connect(
                        host=self.db_host, 
                        port=self.db_port, 
                        db=self.db_name, 
                        user=self.db_user, 
                        password=self.db_pw,
                        connect_timeout=10,
                        read_timeout=30,
                        write_timeout=30,
                        autocommit=True
                    )
                self.__connection = self.conn
                self.__session = self.conn.cursor()
                self.__session.execute("SET time_zone = '+00:00';")
                try:
                    self.__session.execute("SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;")
                    self.__session.execute("SET collation_connection = 'utf8mb4_general_ci';")
                except Exception:
                    pass
                self.__session.execute("SET GLOBAL log_bin_trust_function_creators = 1;")
            else:
                print(f"MySQL connection error: {err}")
                raise

#<=====>#

    @narc(1)
    def __opend(self):
        try:
            self.conn = pymysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                read_timeout=30,
                write_timeout=30,
                autocommit=True
            )
            self.__connection = self.conn
            self.__session = self.conn.cursor(pymysql.cursors.DictCursor)
            self.__session.execute("SET time_zone = '+00:00';")
            try:
                self.__session.execute("SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;")
                self.__session.execute("SET collation_connection = 'utf8mb4_general_ci';")
            except Exception:
                pass
            self.__session.execute("SET GLOBAL log_bin_trust_function_creators = 1;")
        except (pymysql.Error, pymysql.Warning) as err:
            if isinstance(err, pymysql.OperationalError) and err.args and err.args[0] in (2003, 2006, 2013):
                self._try_start_service_and_wait('MySQL80', total_wait_s=90)
                try:
                    time.sleep(random.uniform(1.0, 3.0))
                except Exception:
                    pass
                try:
                    self.conn = pymysql.connect(
                        host=self.db_host, 
                        port=self.db_port, 
                        db=self.db_name, 
                        user=self.db_user, 
                        password=self.db_pw,
                        connect_timeout=10,
                        read_timeout=30,
                        write_timeout=30,
                        autocommit=True
                    )
                except (pymysql.Error, pymysql.Warning):
                    try:
                        time.sleep(random.uniform(2.0, 5.0))
                    except Exception:
                        pass
                    self.conn = pymysql.connect(
                        host=self.db_host, 
                        port=self.db_port, 
                        db=self.db_name, 
                        user=self.db_user, 
                        password=self.db_pw,
                        connect_timeout=10,
                        read_timeout=30,
                        write_timeout=30,
                        autocommit=True
                    )
                self.__connection = self.conn
                self.__session = self.conn.cursor(pymysql.cursors.DictCursor)
                self.__session.execute("SET time_zone = '+00:00';")
                try:
                    self.__session.execute("SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;")
                    self.__session.execute("SET collation_connection = 'utf8mb4_general_ci';")
                except Exception:
                    pass
                self.__session.execute("SET GLOBAL log_bin_trust_function_creators = 1;")
            else:
                print(f"MySQL connection error: {err}")
                raise

#<=====>#

    @narc(1)
    def __close(self):
        self.__session.close()
        self.__connection.close()
        
#<=====>#

    @narc(1)
    def get_connection(self):
        if self._connection is None or not self._connection.open:
            try:
                self._connection = pymysql.connect(
                    host=self.db_host,
                    port=self.db_port,
                    user=self.db_user,
                    password=self.db_pw,
                    database=self.db_name,
                    connect_timeout=10,
                    read_timeout=30,
                    write_timeout=30,
                    autocommit=True
                )
                with self._connection.cursor() as cursor:
                    cursor.execute("SET time_zone = '+00:00';")
                    try:
                        cursor.execute("SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;")
                        cursor.execute("SET collation_connection = 'utf8mb4_general_ci';")
                    except Exception:
                        pass
                    cursor.execute("SET GLOBAL log_bin_trust_function_creators = 1;")
            except pymysql.MySQLError as e:
                print(f"MySQL connection error: {e}")
                raise
        return self._connection
        
#<=====>#

    @narc(1)
    def close_connection(self):
        if self._connection and self._connection.open:
            self._connection.close()
            self._connection = None
            
#<=====>#

    @narc(1)
    def execute_query(self, query: str, params: Optional[Tuple] = None, dictionary: bool = False):
        conn = self.get_connection()
        cursor_type = pymysql.cursors.DictCursor if dictionary else pymysql.cursors.Cursor
        with conn.cursor(cursor_type) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
            
#<=====>#

    @narc(1)
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                rows_affected = cursor.execute(query, params)
                return rows_affected
        except pymysql.OperationalError as e:
            if e.args and e.args[0] in (2006, 2013, 2003):
                # try to revive service and retry once
                try:
                    self._try_start_service_and_wait('MySQL80', total_wait_s=60)
                except Exception:
                    pass
                conn = self.get_connection()
                with conn.cursor() as cursor:
                    rows_affected = cursor.execute(query, params)
                    return rows_affected
            else:
                raise

#<=====>#

    @narc(1)
    def get_required_tables(self) -> Dict[str, str]:
        return {}
        
#<=====>#

    @narc(1)
    def get_required_indexes(self) -> List[str]:
        return []
        
#<=====>#

    @narc(1)
    def ensure_schema_ready(self, verbose: bool = False) -> bool:
        # Simplified for brevity; would contain logic to create tables/indexes
        return True
        
#<=====>#

    @narc(1)
    def pretty_print_sql(self, sql: str) -> None:
        formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        print(formatted_sql)

#<=====>#

    @narc(1)
    def curs(self, sql):
        data = None
        self.__open()
        self.__session.execute(sql)
        number_columns = len(self.__session.description)
        headers = [item[0] for item in self.__session.description]
        number_rows = self.__session.rowcount
        if number_rows == 1 and number_columns == 1:
            data = self.__session.fetchone()[0]
        elif number_rows >= 1 and number_columns > 1:
            data = [item for item in self.__session.fetchall()]
        else:
            data = [item[0] for item in self.__session.fetchall()]
        self.__close()
        return data, headers

#<=====>#

    @narc(1)
    def cols(self, sql):
        # data = None
        self.__open()
        self.__session.execute(sql)
        headers = [item[0] for item in self.__session.description]
        self.__close()
        return headers

#<=====>#

    @narc(1)
    def table_cols(self, table):
        cols = []
        sql = ""
        try:
            # Check if table is a string or an object
            if not isinstance(table, str):
                # If it's an AttrDict or dictionary, it's likely a data object being passed incorrectly
                print(f"WARNING: table_cols received non-string table parameter: {type(table)}")
                # Try to convert to string representation for debugging
                table_str = str(table)
                print(f"Table content: {table_str[:100]}...")  # Show first 100 chars
                raise ValueError(f"table_cols requires a string table name, got {type(table)}")
                
            # Fix: Don't use string formatting for table names
            # Instead, use backticks to quote identifiers properly
            if '.' in table:
                parts = table.split('.')
                if len(parts) == 2:
                    schema, tbl = parts
                    # Check if schema is the same as the database name
                    if schema == self.db_name:
                        sql = f"SELECT * FROM `{tbl}` LIMIT 0"
                    else:
                        sql = f"SELECT * FROM `{schema}`.`{tbl}` LIMIT 0"
                else:
                    # Handle case with more than one dot
                    sql = f"SELECT * FROM `{table}` LIMIT 0"
            else:
                # Just use the table name without schema
                sql = f"SELECT * FROM `{table}` LIMIT 0"
                
            # Try to get columns directly
            try:
                cols = self.cols(sql)
            except Exception as col_error:
                print(f"Error getting columns with direct query: {col_error}")
                
                # Try a fallback approach - get columns from information_schema
                try:
                    print(f"Trying fallback method to get columns for table '{table}'")
                    fallback_sql = f"""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = %s 
                    AND TABLE_SCHEMA = %s
                    """
                    self.__opend()
                    self.__session.execute(fallback_sql, (table, self.db_name))
                    cols = [row[0] for row in self.__session.fetchall()]
                    self.__close()
                    print(f"Fallback method retrieved {len(cols)} columns for table '{table}'")
                except Exception as fallback_error:
                    print(f"Fallback method also failed: {fallback_error}")
                    # Return empty list as last resort
                    cols = []
                    raise col_error
        except Exception as e:
            print(f"Error in table_cols for table '{table}': {type(e).__name__}: {str(e)}")
            if sql:
                self.pretty_print_sql(sql)
            # Don't raise the exception, just return empty columns
            cols = []
            
        return cols

#<=====>#

    @narc(1)
    def GoodValue(self, v=None):
        if isinstance(v, str):
            v = "'" + v + "'"
        elif isinstance(v, (int, float)):
            v = v
        elif isinstance(v, datetime.datetime):
            v = v.strftime('%Y-%m-%d %H:%M:%S')
            v = "'" + v + "'"
        elif isinstance(v, dict):
            v = str(v)
            v = "'" + v + "'"
        elif isinstance(v, list):
            v = ', '.join(v)
            v = v[0:len(v)-2]
            v = "'" + v + "'"
        elif isinstance(v, bytes):
            v = v.hex()
        return v

#<=====>#

    @narc(1)
    def HasVal(self, v=None):
        if v is None:
            return False
        elif isinstance(v, str) and len(v) > 0:
            return True
        elif isinstance(v, dict) and len(v) > 0:
            return True
        elif isinstance(v, list) and len(v) > 0:
            return True
        elif isinstance(v, tuple) and len(v) > 0:
            return True
        elif v is not None and v != '':
            return True
        else:
            return False

#<=====>#

    @narc(1)
    def test_connection(self, verbose: bool = False) -> bool:
        """Lightweight connectivity check using a simple SELECT 1.
        Keeps the persistent connection open for reuse.
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                _ = cursor.fetchall()
            return True
        except Exception as e:
            if verbose:
                print(f"MySQL test_connection failed: {e}")
            return False

#<=====>#

#    def exe(self, sql):
#        self.__open()
#        self.__session.execute(sql)
#        self.__connection.commit()
#        self.__close()
#        return self.__session.lastrowid
#    ## End def execute

#<=====>#

    @narc(1)
    def execute(self, sql, vals=None):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            try:
                self.__open()
                if vals:
                    self.__session.execute(sql, vals)
                else:
                    self.__session.execute(sql)
                self.__connection.commit()
                self.__close()
            except pymysql.OperationalError as e:
                # Handle server gone away / lost connection
                if e.args and e.args[0] in (2006, 2013, 2003):
                    try:
                        self._try_start_service_and_wait('MySQL80', total_wait_s=60)
                    except Exception:
                        pass
                    # retry once
                    self.__open()
                    if vals:
                        self.__session.execute(sql, vals)
                    else:
                        self.__session.execute(sql)
                    self.__connection.commit()
                    self.__close()
                else:
                    raise
        except Exception as e:
            # Check if the error is "Trigger already exists"
            if "Trigger already exists" in str(e):
                # Silently ignore this specific error
                pass
            else:
                # For other errors, print the traceback and details
                traceback.print_exc()
                print(f"Error in execute(): {e}")
                self.pretty_print_sql(sql)
                print(f"Values: {vals}")
                # Re-raise the exception for other errors
                raise e
        return self.__session.lastrowid

#<=====>#

    @narc(1)
    async def execute_async(self, sql, vals=None, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            r = None
            conn = await aiomysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                autocommit=True
            )
            cur = await conn.cursor()
            if vals:
                await cur.execute(sql, vals)
            else:
                await cur.execute(sql)
            
            r = cur.rowcount
            await cur.close()
            await conn.close()
        except Exception as e:
            traceback.print_exc()
            print(f"Error in execute_async(): {e}\nSQL: {sql}\nVals: {vals}")
            if exit_on_error: sys.exit(f"sys.exit from execute_async()")
        return r

#<=====>#

    @narc(1)
    def sel(self, sql, always_list_yn='N'):
        try:
            result = None
            self.__open()
            # Proactively ensure connection is alive
            try:
                if hasattr(self, 'conn') and self.conn:
                    self.conn.ping(reconnect=True)
            except Exception:
                # If ping fails, reopen
                self.__close()
                self.__open()

            # First attempt
            try:
                self.__session.execute(sql)
            except pymysql.OperationalError as e:
                # Lost connection or server gone away → one safe retry for reads
                if e.args and e.args[0] in (2006, 2013):
                    try:
                        self.__close()
                    except Exception:
                        pass
                    time.sleep(0.25)
                    self.__open()
                    if hasattr(self, 'conn') and self.conn:
                        try:
                            self.conn.ping(reconnect=True)
                        except Exception:
                            pass
                    self.__session.execute(sql)
                else:
                    raise
            number_rows = self.__session.rowcount
            number_columns = len(self.__session.description)
            if 1 == 2: pass
            # cols > 1 and rows > 1 => Good
            elif number_rows > 1 and number_columns > 1:
                result = [item for item in self.__session.fetchall()]
            # cols > 1 and rows = 1 => Good
            elif number_rows >= 1 and number_columns > 1:
                result = [item for item in self.__session.fetchall()][0]
            # cols > 1 and rows = 0 => Good
            elif number_rows == 0 and number_columns > 1:
                result = None
            # cols = 1 and rows > 1 => Good
            elif number_rows > 1 and number_columns == 1:
                result = [item[0] for item in self.__session.fetchall()]
            # cols = 1 and rows = 1 => Good
            elif number_rows == 1 and number_columns == 1:
                if always_list_yn == 'Y':
                    result = [item[0] for item in self.__session.fetchall()]
                else:
                    result = [item[0] for item in self.__session.fetchall()][0]
            # cols = 1 and rows = 0 => Good
            elif number_rows == 0 and number_columns == 1:
                result = None
            else:
                result = [item[0] for item in self.__session.fetchall()]
            self.__close()
        except Exception as e:
            import sys
            import inspect
            
            print("\n" + "="*80)
            print("FATAL DATABASE ERROR in sel()")
            print(f"Error type: {type(e)}")
            print(f"Error message: {e}")
            
            # Print immediate traceback for the exception
            traceback.print_exc()
            
            # Get and print caller information
            print("\nCALLER STACK TRACE:")
            caller_frames = inspect.stack()[1:] # Skip current frame
            for i, frame_info in enumerate(caller_frames[:8]): # Limit to 8 frames
                frame = frame_info.frame
                code = frame.f_code
                print(f"{i+1}. {code.co_filename}:{frame.f_lineno} in {code.co_name}")
                
                # Try to find SQL-related context variables in the frame
                locals_dict = frame.f_locals
                for var_name, var_value in locals_dict.items():
                    if isinstance(var_value, str) and ('SELECT' in var_value or 'INSERT' in var_value or 
                                                      'UPDATE' in var_value or 'DELETE' in var_value):
                        print(f"   Possible SQL in variable '{var_name}': {var_value[:80]}...")
            
            print("\nCURRENT SQL:")
            self.pretty_print_sql(sql)
            print("="*80)
            print("\nFATAL ERROR: Terminating script due to database error")
            sys.exit(1)
        return result

#<=====>#

    @narc(1)
    async def sel_async(self, sql, vals=None, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            r = None
            conn = await aiomysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                autocommit=True
            )
            cur = await conn.cursor()
            if vals:
                await cur.execute(sql, vals)
            else:
                await cur.execute(sql)
            
            row_cnt = cur.rowcount
            col_cnt = len(cur.description)
            if row_cnt == 0 and col_cnt == 0:
                r = []
            elif row_cnt == 1 and col_cnt == 1:
                r = await cur.fetchone()[0]
            elif row_cnt >= 1 and col_cnt > 1:
                x = await cur.fetchall()
                r = [item for item in x]
            else:
                x = await cur.fetchall()
                r = [item[0] for item in x]
            await cur.close()
            await conn.close()
        except Exception as e:
            traceback.print_exc()
            print(f"Error in sel_async(): {e}\nSQL: {sql}\nVals: {vals}")
            if exit_on_error: sys.exit(f"sys.exit from sel_async()")
        return r

#<=====>#

    @narc(1)
    def seld(self, sql, vals=None, always_list_yn='Y'):
        """
        Select query that returns results as dictionaries
        
        Args:
            sql: SQL query string
            vals: Parameter values for the query
            always_list_yn: 'Y' to always return a list (legacy parameter)
        """
        try:
            result = None
            self.__opend()
            # Proactively ensure connection is alive
            try:
                if hasattr(self, 'conn') and self.conn:
                    self.conn.ping(reconnect=True)
            except Exception:
                # If ping fails, reopen
                self.__close()
                self.__opend()

            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            # Attempt with guarded retries + final fail-fast
            attempts = [
                (0.5, False),        # quick retry
                (random.uniform(1.0, 3.0), True),
                (random.uniform(2.0, 5.0), False),
            ]
            last_err = None
            for delay, try_start in attempts:
                try:
                    if vals:
                        self.__session.execute(sql, vals)
                    else:
                        self.__session.execute(sql)
                    last_err = None
                    break
                except pymysql.OperationalError as e:
                    last_err = e
                    code = e.args[0] if e.args else None
                    if code in (2003, 2006, 2013):
                        try:
                            self.__close()
                        except Exception:
                            pass
                        if try_start:
                            self._service_start_guard(total_wait_s=120)
                        time.sleep(delay)
                        self.__opend()
                        try:
                            if hasattr(self, 'conn') and self.conn:
                                self.conn.ping(reconnect=True)
                        except Exception:
                            pass
                        continue
                    raise
                except (ConnectionRefusedError, ConnectionResetError):
                    last_err = sys.exc_info()[1]
                    try:
                        self.__close()
                    except Exception:
                        pass
                    self._service_start_guard(total_wait_s=120)
                    time.sleep(delay)
                    self.__opend()
                    continue
            if last_err is not None:
                raise last_err
                
            number_rows = self.__session.rowcount
            # Handle empty result sets where description is None
            if self.__session.description is None:
                number_columns = 0
                result = []
                return result
            else:
                number_columns = len(self.__session.description)
            if 1 == 2: pass
            # cols > 1 and rows > 1 => Good
            elif number_rows > 1 and number_columns > 1:
                result = [item for item in self.__session.fetchall()]
            # cols > 1 and rows = 1 => Good
            elif number_rows == 1 and number_columns > 1:
                result = [item for item in self.__session.fetchall()][0]
            # cols > 1 and rows = 0 => Good
            elif number_rows == 0 and number_columns > 1:
                result  = None
            # cols = 1 and rows > 1 => Good
            elif number_rows > 1 and number_columns == 1:
                result = [item for item in self.__session.fetchall()]
            # cols = 1 and rows = 1 => Good
            elif number_rows == 1 and number_columns == 1:
                result = [item for item in self.__session.fetchall()][0]
            # cols = 1 and rows = 0 => Good
            elif number_rows == 0 and number_columns == 1:
                result = None
            else:
                result = [item[0] for item in self.__session.fetchall()]
            if always_list_yn == 'Y':
                if isinstance(result, list):
                    pass
                elif isinstance(result, dict):
                    r = []
                    r.append(result)
                    result = r
                else:
                    result  = []
            self.__close()
            if isinstance(result, (list, dict)):
                result = AttrDictConv(result, dec2float_yn='Y')
        except Exception as e:
            import sys
            import inspect
            
            print("\n" + "="*80)
            print("FATAL DATABASE ERROR in seld()")
            print(f"Error type: {type(e)}")
            print(f"Error message: {e}")
            
            # Print immediate traceback for the exception
            traceback.print_exc()
            
            # Get and print caller information
            print("\nCALLER STACK TRACE:")
            caller_frames = inspect.stack()[1:] # Skip current frame
            for i, frame_info in enumerate(caller_frames[:8]): # Limit to 8 frames
                frame = frame_info.frame
                code = frame.f_code
                print(f"{i+1}. {code.co_filename}:{frame.f_lineno} in {code.co_name}")
                
                # Try to find SQL-related context variables in the frame
                locals_dict = frame.f_locals
                for var_name, var_value in locals_dict.items():
                    if isinstance(var_value, str) and ('SELECT' in var_value or 'INSERT' in var_value or 
                                                       'UPDATE' in var_value or 'DELETE' in var_value):
                        print(f"   Possible SQL in variable '{var_name}': {var_value[:80]}...")
            
            print("\nCURRENT SQL:")
            self.pretty_print_sql(sql)
            print(f"Values: {vals}")
            print("="*80)
            print("\nFATAL ERROR: Terminating script due to database error")
            sys.exit(1)
        return result

#<=====>#

    @narc(1)
    def seld_ez(self, schema, table, col_list=None, where_dict=None):
        try:
            x = -1
            sql1 = "select"
            sql2 = "*"
            sql3 = "from {}.{}".format(schema, table)
            sql4 = ""
            if col_list:
                first_yn = 'Y'
                for c in col_list:
                    if first_yn == 'Y':
                        sql2 += " " + c
                        first_yn = 'N'
                    else:
                        sql2 += ", " + c
            else:
                sql2 = " * "

            if where_dict:
                first_yn = 'Y'
                for k in where_dict:
                    v = self.GoodValue(where_dict[k])
                    if self.HasVal(v):
                        w = 'and '
                        if first_yn == 'Y':
                            w = 'where '
                            first_yn = 'N'
                        sql4 += "{} {} = {} ".format(w, k, v)

            sql = sql1 + " " + sql2 + " " + sql3 + " " + sql4
            x = self.seld(sql)
        except Exception as e:
            import sys
            import inspect
            
            print("\n" + "="*80)
            print("FATAL DATABASE ERROR in seld_ez()")
            print(f"Error type: {type(e)}")
            print(f"Error message: {e}")
            
            # Print immediate traceback for the exception
            traceback.print_exc()
            
            # Get and print caller information
            print("\nCALLER STACK TRACE:")
            caller_frames = inspect.stack()[1:] # Skip current frame
            for i, frame_info in enumerate(caller_frames[:8]): # Limit to 8 frames
                frame = frame_info.frame
                code = frame.f_code
                print(f"{i+1}. {code.co_filename}:{frame.f_lineno} in {code.co_name}")
                
                # Try to find SQL-related context variables in the frame
                locals_dict = frame.f_locals
                for var_name, var_value in locals_dict.items():
                    if isinstance(var_value, str) and ('SELECT' in var_value or 'INSERT' in var_value or 
                                                      'UPDATE' in var_value or 'DELETE' in var_value):
                        print(f"   Possible SQL in variable '{var_name}': {var_value[:80]}...")
            
            print("\nCONTEXT VALUES:")
            print(f"Schema: {schema}")
            print(f"Table: {table}")
            print(f"Columns: {col_list}")
            print(f"Where conditions: {where_dict}")
            print("="*80)
            print("\nFATAL ERROR: Terminating script due to database error")
            sys.exit(1)
        return x


#<=====>#

    @narc(1)
    async def seld_async(self, sql, vals=None, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            r = None
            conn = await aiomysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                autocommit=True
            )
            cur = await conn.cursor(aiomysql.DictCursor)
            if vals:
                await cur.execute(sql, vals)
            else:
                await cur.execute(sql)
            
            row_cnt = cur.rowcount
            col_cnt = len(cur.description)
            if row_cnt == 0 and col_cnt == 0:
                r = {}
            elif row_cnt == 1:
                r = await cur.fetchall()
            else:
                r = await cur.fetchall()
            await cur.close()
            await conn.close()
        except Exception as e:
            traceback.print_exc()
            print(f"Error in seld_async(): {e}\nSQL: {sql}\nVals: {vals}")
            if exit_on_error: sys.exit(f"sys.exit from seld_async()")
        return r

#<=====>#

    @narc(1)
    async def seld_async(self, sql, always_list_yn='Y'):
        try:
            result = None
            self.__opend()
            self.__session.execute(sql)
            number_rows = self.__session.rowcount
            number_columns = len(self.__session.description)
            if 1 == 2: pass
            # cols > 1 and rows > 1 => Good
            elif number_rows > 1 and number_columns > 1:
                result = [item for item in self.__session.fetchall()]
            # cols > 1 and rows = 1 => Good
            elif number_rows == 1 and number_columns > 1:
                result = [item for item in self.__session.fetchall()][0]
            # cols > 1 and rows = 0 => Good
            elif number_rows == 0 and number_columns > 1:
                result  = None
            # cols = 1 and rows > 1 => Good
            elif number_rows > 1 and number_columns == 1:
                result = [item for item in self.__session.fetchall()]
            # cols = 1 and rows = 1 => Good
            elif number_rows == 1 and number_columns == 1:
                result = [item for item in self.__session.fetchall()][0]
            # cols = 1 and rows = 0 => Good
            elif number_rows == 0 and number_columns == 1:
                result = None
            else:
                result = [item[0] for item in self.__session.fetchall()]
            if always_list_yn == 'Y':
                if isinstance(result, list):
                    pass
                elif isinstance(result, dict):
                    r = []
                    r.append(result)
                    result = r
                else:
                    result  = []
            self.__close()
        except Exception as e:
            print('seld()')
            traceback.print_exc()
            print(type(e))
            print(e)
            self.pretty_print_sql(sql)
        return result

#<=====>#

    @narc(1)
    def ins_ez(self, schema, table, in_dict, exit_on_error=True):
        """Insert a record with schema specified"""
        full_table = f"{schema}.{table}"
        cols = self.table_cols(full_table)
        valid_dict = {k: v for k, v in in_dict.items() if k in cols}

        columns = ", ".join([f"`{k}`" for k in valid_dict.keys()])
        values_placeholder = ", ".join(["%s"] * len(valid_dict))

        sql = f"INSERT INTO {full_table} ({columns}) VALUES ({values_placeholder})"
        
        try:
            return self.execute_update(sql, tuple(valid_dict.values()))
        except pymysql.MySQLError as e:
            print(f"Error in ins_ez(): {e}\nSQL: {sql}\nVals: {valid_dict}")
            if exit_on_error:
                sys.exit(f"sys.exit from ins_ez()")
            raise

#<=====>#

    @narc(1)
    def ins_one(self, sql, vals=None, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            self.__open()
            if vals:
                self.__session.execute(sql, vals)
            else:
                self.__session.execute(sql)
            self.__connection.commit()
            self.__close()
        except Exception as e:
            print('ins_one()')
            traceback.print_exc()
            print(type(e))
            print(e)
            self.pretty_print_sql(sql)
            print(vals)
            if exit_on_error: sys.exit(f"sys.exit from ins_one()")
        return self.__session.lastrowid


#<=====>#

    @narc(1)
    async def ins_one_async(self, sql, vals=None, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            r = None
            conn = await aiomysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                autocommit=True
            )
            cur = await conn.cursor()
            if vals:
                await cur.execute(sql, vals)
            else:
                await cur.execute(sql)
            
            r = cur.lastrowid
            await cur.close()
            await conn.close()
        except Exception as e:
            traceback.print_exc()
            print(f"Error in ins_one_async(): {e}\nSQL: {sql}\nVals: {vals}")
            if exit_on_error: sys.exit(f"sys.exit from ins_one_async()")
        return r

#<=====>#

    @narc(1)
    def ins_many(self, sql, vals, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            self.__open()
            self.__session.executemany(sql, vals)
            self.__connection.commit()
            self.__close()
        except Exception as e:
            print('ins_many()')
            traceback.print_exc()
            print(type(e))
            print(e)
            self.pretty_print_sql(sql)
            print(vals)
            if exit_on_error: sys.exit(f"sys.exit from {__name__}")
        return self.__session.rowcount

#<=====>#

    @narc(1)
    async def ins_many_async(self, sql, vals, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            r = None
            conn = await aiomysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                autocommit=True
            )
            cur = await conn.cursor()
            if vals:
                await cur.executemany(sql, vals)
            else:
                await cur.execute(sql)
            
            r = cur.rowcount
            await cur.close()
            await conn.close()
        except Exception as e:
            traceback.print_exc()
            print(f"Error in ins_many_async(): {e}\nSQL: {sql}\nVals: {vals}")
            if exit_on_error: sys.exit(f"sys.exit from ins_many_async()")
        return r


#<=====>#

    @narc(1)
    def insupd_ez(self, schema, table, in_dict, exit_on_error=True, validate_columns=True):
        """Hybrid: Original MySQL upsert logic + cached column validation"""
        try:
            # Optional cached column validation (fast after first call)
            if validate_columns and hasattr(self, 'table_cols'):
                try:
                    cols = self.table_cols(table)
                    # Filter out invalid columns and class_name
                    filtered_dict = {k: v for k, v in in_dict.items() 
                                   if k != 'class_name' and (not cols or k in cols)}
                except Exception:
                    # If validation fails, use original dict but exclude class_name
                    filtered_dict = {k: v for k, v in in_dict.items() if k != 'class_name'}
            else:
                # No validation, just exclude class_name
                filtered_dict = {k: v for k, v in in_dict.items() if k != 'class_name'}
            
            # Original MySQL upsert logic (fast)
            sql1 = f"INSERT INTO {schema}.{table} ("
            sql2 = ""
            sql3 = ") VALUES ("
            sql4 = ""
            sql5 = ") ON DUPLICATE KEY UPDATE "
            sql6 = ""
            
            for k, v in filtered_dict.items():
                try:
                    if self.HasVal(v):  # Check original value, not formatted value
                        good_val = self.GoodValue(v)
                        sql2 += f"{k}, "
                        sql4 += f"{good_val}, "
                        sql6 += f"{k} = VALUES({k}), "
                except Exception as field_error:
                    print(f"Error processing field '{k}' with value '{v}' (type: {type(v)}): {field_error}")
                    # Skip this field and continue
                    
            if sql2 and sql4 and sql6:
                sql2 = sql2[:-2]  # Remove trailing ", "
                sql4 = sql4[:-2]
                sql6 = sql6[:-2]
                sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6
                return self.ins_one(sql)
            else:
                print(f"WARNING: No valid data to insert/update in {schema}.{table}")
                return 0
                
        except Exception as e:
            print(f'Error in insupd_ez(): {e}')
            print(f'Schema: {schema}, Table: {table}')
            if exit_on_error:
                sys.exit(f"sys.exit from insupd_ez()")
            return -1

#<=====>#

    @narc(1)
    def upd(self, sql, vals=None, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            self.__open()
            if vals:
                self.__session.execute(sql, vals)
            else:
                self.__session.execute(sql)
            self.__connection.commit()
            # Obtain rows affected
            update_rows = self.__session.rowcount
            self.__close()
        except Exception as e:
            print('upd()')
            traceback.print_exc()
            print(type(e))
            print(e)
            self.pretty_print_sql(sql)
            print(vals)
            if exit_on_error: sys.exit(f"sys.exit from upd()")
        return update_rows


#<=====>#

    @narc(1)
    def upd_ez(self, schema, table, in_dict=None, where_dict=None, exit_on_error=True):
        """Update records based on a where clause with schema specified"""
        # Check if in_dict is actually the table parameter (common error)
        if isinstance(in_dict, (dict, AttrDict)) and where_dict is None and isinstance(table, str):
            # This is the correct usage
            pass
        elif isinstance(table, (dict, AttrDict)) and in_dict is None:
            # The table parameter is actually the data to update
            # This is likely an error in the calling code
            print(f"ERROR: upd_ez called with incorrect parameter order. 'table' contains data object.")
            print(f"Attempting to fix by swapping parameters...")
            # Swap parameters to fix the issue
            in_dict = table
            table = schema
            schema = self.db_name  # Use the database name from the connection
            print(f"Fixed parameters: schema={schema}, table={table}, data has {len(in_dict.keys() if hasattr(in_dict, 'keys') else [])} fields")
        
        # Don't use schema prefix if it's the same as the database name
        if schema == self.db_name:
            full_table = f"`{table}`"
        else:
            full_table = f"`{schema}`.`{table}`"
            
        # Get table columns
        try:
            cols = self.table_cols(table)  # Just use table name without schema
        except Exception as e:
            print(f"Error getting table columns: {e}")
            cols = []  # Fallback to empty column list
            
        # Filter out class_name and invalid columns (cached validation)
        valid_set_dict = {k: v for k, v in in_dict.items() if k != 'class_name' and (not cols or k in cols)} if in_dict else {}
        valid_where_dict = {k: v for k, v in where_dict.items() if k != 'class_name' and (not cols or k in cols)} if where_dict else {}

        set_placeholder = ", ".join([f"`{k}` = %s" for k in valid_set_dict.keys()])
        
        if valid_set_dict:
            if valid_where_dict:
                where_placeholder = " AND ".join([f"`{k}` = %s" for k in valid_where_dict.keys()])
                sql = f"UPDATE {full_table} SET {set_placeholder} WHERE {where_placeholder}"
                params = tuple(valid_set_dict.values()) + tuple(valid_where_dict.values())
            else:
                sql = f"UPDATE {full_table} SET {set_placeholder}"
                params = tuple(valid_set_dict.values())
            
            try:
                return self.execute_update(sql, params)
            except pymysql.MySQLError as e:
                print(f"Error in upd_ez(): {e}\nSQL: {sql}\nVals: {params}")
                if exit_on_error:
                    sys.exit(f"sys.exit from upd_ez()")
                raise
        else:
            print(f"WARNING: No valid columns to update in {full_table}")
            return 0

#<=====>#

    @narc(1)
    async def upd_async(self, sql, vals=None, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            r = None
            conn = await aiomysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                autocommit=True
            )
            cur = await conn.cursor()
            if vals:
                await cur.execute(sql, vals)
            else:
                await cur.execute(sql)
            
            r = cur.rowcount
            await cur.close()
            await conn.close()
        except Exception as e:
            traceback.print_exc()
            print(f"Error in upd_async(): {e}\nSQL: {sql}\nVals: {vals}")
            if exit_on_error: sys.exit(f"sys.exit from upd_async()")
        return r

#<=====>#

    @narc(1)
    def delete(self, sql):
        try:
            self.__open()
            self.__session.execute(sql)
            self.__connection.commit()
            # Obtain rows affected
            delete_rows = self.__session.rowcount
            self.__close()
        except Exception as e:
            import sys
            import inspect
            
            print("\n" + "="*80)
            print("FATAL DATABASE ERROR in delete()")
            print(f"Error type: {type(e)}")
            print(f"Error message: {e}")
            
            # Print immediate traceback for the exception
            traceback.print_exc()
            
            # Get and print caller information
            print("\nCALLER STACK TRACE:")
            caller_frames = inspect.stack()[1:] # Skip current frame
            for i, frame_info in enumerate(caller_frames[:8]): # Limit to 8 frames
                frame = frame_info.frame
                code = frame.f_code
                print(f"{i+1}. {code.co_filename}:{frame.f_lineno} in {code.co_name}")
                
                # Try to find SQL-related context variables in the frame
                locals_dict = frame.f_locals
                for var_name, var_value in locals_dict.items():
                    if isinstance(var_value, str) and ('SELECT' in var_value or 'INSERT' in var_value or 
                                                      'UPDATE' in var_value or 'DELETE' in var_value):
                        print(f"   Possible SQL in variable '{var_name}': {var_value[:80]}...")
            
            print("\nCURRENT SQL:")
            self.pretty_print_sql(sql)
            print("="*80)
            print("\nFATAL ERROR: Terminating script due to database error")
            sys.exit(1)
        return delete_rows
             
            
#<=====>#

    @narc(1)
    def del_ez(self, schema, table, where_dict=None, exit_on_error=True):
        """Delete records based on a where clause with schema specified"""
        full_table = f"{schema}.{table}"
        cols = self.table_cols(full_table)
        valid_where_dict = {k: v for k, v in where_dict.items() if k in cols} if where_dict else {}

        if valid_where_dict:
            where_placeholder = " AND ".join([f"`{k}` = %s" for k in valid_where_dict.keys()])
            sql = f"DELETE FROM {full_table} WHERE {where_placeholder}"
            params = tuple(valid_where_dict.values())
        else:
            # WARNING: This will delete ALL records in the table!
            sql = f"DELETE FROM {full_table}"
            params = None
        
        try:
            return self.execute_update(sql, params)
        except pymysql.MySQLError as e:
            print(f"Error in del_ez(): {e}\nSQL: {sql}\nVals: {params}")
            if exit_on_error:
                sys.exit(f"sys.exit from del_ez()")
            raise

#<=====>#

    @narc(1)
    async def delete_async(self, sql, vals=None, exit_on_error=True):
        try:
            # Convert ? placeholders to %s for MySQL
            sql = sql.replace('?', '%s')
            
            r = None
            conn = await aiomysql.connect(
                host=self.db_host, 
                port=self.db_port, 
                db=self.db_name, 
                user=self.db_user, 
                password=self.db_pw,
                connect_timeout=10,
                autocommit=True
            )
            cur = await conn.cursor()
            if vals:
                await cur.execute(sql, vals)
            else:
                await cur.execute(sql)
            
            r = cur.rowcount
            await cur.close()
            await conn.close()
        except Exception as e:
            traceback.print_exc()
            print(f"Error in delete_async(): {e}\nSQL: {sql}\nVals: {vals}")
            if exit_on_error: sys.exit(f"sys.exit from delete_async()")
        return r

#<=====>#

#    def insert_one(self, sql, vals):
#        self.__open()
#        self.__session.execute(sql, vals)
#        self.__connection.commit()
#        self.__close()
#        return self.__session.lastrowid
#    ## End def insert

#<=====>#

#    def insert_many(self, sql, vals):
#        self.__open()
#        self.__session.executemany(sql, vals)
#        self.__connection.commit()
#        self.__close()
#        return self.__session.rowcount
#    ## End def insert

#<=====>#

#    def delete(self, sql):
#        self.__open()
#        self.__session.execute(sql)
#        self.__connection.commit()
#        # Obtain rows affected
#        delete_rows = self.__session.rowcount
#        self.__close()
#        return delete_rows

#<=====>#
# Functions
#<=====>#

def test_main():
    pass

#<=====>#
# Assignments Post
#<=====>#


#<=====>#
# Default Run
#<=====>#

if __name__ == '__main__':
    test_main()

#<=====>#


