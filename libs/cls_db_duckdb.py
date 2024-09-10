#<=====>#
# Imports
#<=====>#
import duckdb
from datetime import datetime
import traceback
import sys
import sqlparse
import pandas as pd

#<=====>#
# Variables
#<=====>#
lib_display_lvl = 0
lib_debug_lvl = 1

#<=====>#
# Classes
#<=====>#

class db_duckdb():

	def __init__(self, dbfile: str) -> None:
		self.dbfile = dbfile
		self.db = duckdb.connect(self.dbfile)
		self.conn = None

	def __open(self) -> None:
		try:
			self.conn = duckdb.connect(self.dbfile)
#			self.conn = self.connect(self.dbfile)
			self.__session = self.conn.cursor()
		except Exception as err:
			print(err)
			raise

	def __close(self) -> None:
		if self.__session:
			self.__session.close()
		if self.conn:
			self.conn.close()

	def pretty_print_sql(self, sql: str) -> None:
		formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
		print(formatted_sql)

	def curs(self, sql: str):
		data = None
		self.__open()
		self.__session.execute(sql)
		headers = [item[0] for item in self.__session.description]
		data = self.__session.fetchall()
		self.__close()
		return data, headers

	def cols(self, sql: str) -> list:
		self.__open()
		self.__session.execute(sql)
		headers = [item[0] for item in self.__session.description]
		self.__close()
		return headers

	def GoodValue(self, v=None):
		if isinstance(v, str):
			v = "'" + v + "'"
		elif isinstance(v, (int, float)):
			v = v
		elif isinstance(v, datetime):
			v = "'" + v.strftime('%Y-%m-%d %H:%M:%S') + "'"
		elif isinstance(v, dict):
			v = "'" + str(v) + "'"
		elif isinstance(v, list):
			v = ', '.join([str(i) for i in v])
			v = "'" + v + "'"
		elif isinstance(v, bytes):
			v = v.hex()
		return v

	def HasVal(self, v=None) -> bool:
		if v is None:
			return False
		if isinstance(v, str) and len(v) > 0:
			return True
		if isinstance(v, (dict, list, tuple)) and len(v) > 0:
			return True
		return v is not None and v != ''

	def sel(self, sql: str):
		try:
			result = None
			self.__open()
			self.__session.execute(sql)
			result = self.__session.fetchall()
			self.__close()
		except Exception as e:
			print('sel()')
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
		return result

	def seld(self, sql: str, always_list_yn='Y') -> list:
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


	def ins_one(self, sql: str) -> int:
		try:
			self.__open()
			self.__session.execute(sql)
			self.conn.commit()
			self.__close()
		except Exception as e:
			print('ins_one()')
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
			sys.exit()
	# I need to make this return the rowid or primary key generated

	def ins_many(self, sql: str, vals: list) -> int:
		try:
			self.__open()
			self.__session.executemany(sql, vals)
			self.conn.commit()
			self.__close()
		except Exception as e:
			print('ins_many()')
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
			sys.exit()

	def merge_df_into_table(self, df: pd.DataFrame, table_name: str, key_column: str):
		"""
		Merges the data from the given DataFrame into an existing DuckDB table.

		Parameters:
		df: pd.DataFrame
			The DataFrame containing data to merge.
		table_name: str
			The name of the existing DuckDB table to merge into.
		key_column: str
			The column name that will be used as the primary key for matching records.
		"""
		try:
			# Open the DuckDB connection
			self.__open()

			# Register the DataFrame in DuckDB
			self.conn.register('temp_df', df)

			# Construct the SQL for merging the data
			# Adjust the columns according to the DataFrame
			columns = df.columns.tolist()
			update_columns = ", ".join([f"{col} = source.{col}" for col in columns if col != key_column])
			insert_columns = ", ".join(columns)
			insert_values = ", ".join([f"source.{col}" for col in columns])

			sql = f'''
				MERGE INTO {table_name} AS target
				USING temp_df AS source
				ON target.{key_column} = source.{key_column}
				WHEN MATCHED THEN
					UPDATE SET {update_columns}
				WHEN NOT MATCHED THEN
					INSERT ({insert_columns}) VALUES ({insert_values});
			'''

			# Execute the SQL statement
			self.conn.execute(sql)
			self.conn.unregister('temp_df')

		except Exception as e:
			print("Error while merging DataFrame into table.")
			traceback.print_exc()
			print(e)
		finally:
			self.__close()


	def upd(self, sql: str) -> int:
		try:
			self.__open()
			self.__session.execute(sql)
			self.conn.commit()
			self.__close()
		except Exception as e:
			print('upd()')
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
			sys.exit()
		return self.__session.rowcount

	def delete(self, sql: str) -> int:
		try:
			self.__open()
			self.__session.execute(sql)
			self.conn.commit()
			self.__close()
		except Exception as e:
			print('delete()')
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
		return self.__session.rowcount

	def execute(self, sql: str) -> int:
		try:
			self.__open()
			self.__session.execute(sql)
			self.conn.commit()
			self.__close()
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
#		return self.__session.lastrowid

def test_main():
	pass

if __name__ == '__main__':
	test_main()
