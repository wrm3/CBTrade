#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import aiomysql
import pymysql as mysql
import sqlparse
import datetime
import sys
import traceback


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

class db_mysql(object):

#<=====>#

	def __init__(self, db_host, db_port, db_name, db_user, db_pw):
		self.db_host = db_host
		self.db_port = db_port
		self.db_name = db_name
		self.db_user = db_user
		self.db_pw   = db_pw
		self.conn   = None
#		self.conn   = mysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
#		self.curs   = None
#		self.conn   = mysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)

#<=====>#

	def __open(self):
		try:
			self.conn = mysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			self.__connection = self.conn
			self.__session = self.conn.cursor()
		except (mysql.Error, mysql.Warning) as err:
			print(err)
			raise

#<=====>#

	def __opend(self):
		try:
			self.conn = mysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			self.__connection = self.conn
			self.__session = self.conn.cursor(mysql.cursors.DictCursor)
		except (mysql.Error, mysql.Warning) as err:
			print(err)
			raise

#<=====>#

	def __close(self):
		self.__session.close()
		self.__connection.close()

#<=====>#

	def pretty_print_sql(self, sql: str) -> None:
		formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
		print(formatted_sql)

#<=====>#

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

	def cols(self, sql):
		# data = None
		self.__open()
		self.__session.execute(sql)
		headers = [item[0] for item in self.__session.description]
		self.__close()
		return headers

#<=====>#

	def table_cols(self, table):
		cols = []
		try:
			sql = "select *  from {} ".format(table)
			cols = self.cols(sql)
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
			raise
		return cols

#<=====>#

	def GoodValue(self, v=None):
		if isinstance(v, str):
			v = "'" + v + "'"
		elif isinstance(v, (int, float)):
			v = v
		elif isinstance(v, datetime):
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

	def sel(self, sql):
		try:
			result = None
			self.__open()
			self.__session.execute(sql)
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
				result = [item[0] for item in self.__session.fetchall()][0]
			# cols = 1 and rows = 0 => Good
			elif number_rows == 0 and number_columns == 1:
				result = None
			else:
				result = [item[0] for item in self.__session.fetchall()]
			self.__close()
		except Exception as e:
			print('sel()')
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
		return result

#<=====>#

	def seld(self, sql, always_list_yn='Y'):
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

	def ins_one(self, sql, vals=None, exit_on_error=True):
		try:
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
			if exit_on_error: sys.exit()
		return self.__session.lastrowid

#<=====>#

	def ins_many(self, sql, vals, exit_on_error=True):
		try:
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
			if exit_on_error: sys.exit()
		return self.__session.rowcount

#<=====>#

	def upd(self, sql, vals=None, exit_on_error=True):
		try:
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
			if exit_on_error: sys.exit()
		return update_rows

#<=====>#

	def delete(self, sql):
		try:
			self.__open()
			self.__session.execute(sql)
			self.__connection.commit()
			# Obtain rows affected
			delete_rows = self.__session.rowcount
			self.__close()
		except Exception as e:
			print('delt()')
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
		return delete_rows

#<=====>#

	def execute(self, sql):
		try:
			self.__open()
			self.__session.execute(sql)
			self.__connection.commit()
			self.__close()
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			self.pretty_print_sql(sql)
		return self.__session.lastrowid

#<=====>#

	def seld_ez(self, schema, table, col_list=None, where_dict=None):
		try:
			x = -1
			sql1 = "select"
			sql2 = "*"
			sql3 = "from {}.{}".format(schema, table)
			sql4 = ""
			if self.HasVal(col_list):
				first_yn = 'Y'
				for c in col_list:
					if first_yn == 'Y':
						sql2 += " " + c
						first_yn = 'N'
					else:
						sql2 += ", " + c
			else:
				sql2 = " * "
			if self.HasVal(where_dict):
				first_yn = 'Y'
				for k in where_dict:
					v = self.GoodValue(where_dict[k])
					if self.HasVal(v):
						w = 'and '
						if first_yn == 'Y':
							w = 'where '
							first_yn = 'N'
						sql += "{} {} = {} ".format(w, k, v)

			sql = sql1 + " " + sql2 + " " + sql3 + " " + sql4
			x = self.seld(sql)
		except Exception as e:
			print('seld_ez()')
			traceback.print_exc()
			print(type(e))
			print(e)
			print(schema)
			print(table)
			print(col_list)
			print(where_dict)
		return x

#<=====>#

	def ins_ez(self, schema, table, in_dict, exit_on_error=True):
		try:
			x = -1
			# vals = []
			sql1 = "insert into {}.{} (".format(schema, table)
			sql2 = ""
			sql3 = ") values ("
			sql4 = ""
			sql5 = ")"
			for k in in_dict:
				v = self.GoodValue(in_dict[k])
				if self.HasVal(v):
					sql2 += "{}, ".format(k)
					sql4 += "{}, ".format(v)
			sql2 = sql2[0:len(sql2)-2]
			sql4 = sql4[0:len(sql4)-2]
			if self.HasVal(sql2) and self.HasVal(sql4):
				sql = sql1 + " " + sql2 + " " + sql3 + " " + sql4 + " " + sql5
#				x = self.ins_one(sql, vals)
				x = self.ins_one(sql)
		except Exception as e:
			print('ins_ez()')
			traceback.print_exc()
			print(type(e))
			print(e)
			print(schema)
			print(table)
			print(in_dict)
			if exit_on_error: sys.exit()
		return x

#<=====>#

	def insupd_ez(self, schema, table, in_dict, exit_on_error=True):
		x = -1
		try:
			# vals = []
			sql  = ""
			sql1 = "insert into {}.{} (".format(schema, table)
			sql2 = ""
			sql3 = ") values ("
			sql4 = ""
			sql5 = ") on duplicate key update "
			sql6 = ""
			for k in in_dict:
				v = self.GoodValue(in_dict[k])
				if self.HasVal(v):
					sql2 += "{}, ".format(k)
					sql4 += "{}, ".format(v)
					sql6 += "{} = values({}), ".format(k, k)
			sql2 = sql2[0:len(sql2)-2]
			sql4 = sql4[0:len(sql4)-2]
			sql6 = sql6[0:len(sql6)-2]
			if self.HasVal(sql2) and self.HasVal(sql4) and self.HasVal(sql6):
				sql = sql1 + " " + sql2 + " " + sql3 + " " + sql4 + " " + sql5 + " " + sql6
				x = self.ins_one(sql)
#			self.pretty_print_sql(sql)
		except Exception as e:
			print('insupd_ez()')
			traceback.print_exc()
			print(type(e))
			print(e)
			print(schema)
			print(table)
			print(in_dict)
			print(sql1)
			print(sql2)
			print(sql3)
			print(sql4)
			print(sql5)
			print(sql6)
			self.pretty_print_sql(sql)
			if exit_on_error: sys.exit()
		return x

#<=====>#

	def upd_ez(self, schema, table, in_dict, where_dict=None, exit_on_error=True):
		try:
			x = -1
			sql1 = "update {}.{} ".format(schema, table)
			sql2 = ""
			sql3 = ""
			first_yn = 'Y'
			for k in in_dict:
				if self.HasVal(in_dict[k]):
					v = self.GoodValue(in_dict[k])
					if first_yn == 'Y':
						first_yn = 'N'
						sql2 += "set {} = {} ".format(k, v)
					else:
						sql2 += ", {} = {} ".format(k, v)
			if self.HasVal(where_dict):
				first_yn = 'Y'
				for k in where_dict:
					if self.HasVal(v):
						v = self.GoodValue(where_dict[k])
						w = 'and'
						if first_yn == 'Y':
							first_yn = 'N'
							w = 'where'
						sql3 += "{} {} = {} ".format(w, k, v)
			sql = sql1 + " " + sql2 + " " + sql3
			x = self.upd(sql)
		except Exception as e:
			print('upd_ez()')
			traceback.print_exc()
			print(type(e))
			print(e)
			print(schema)
			print(table)
			print(in_dict)
			print(where_dict)
			if exit_on_error: sys.exit()
		return x

#<=====>#

	def del_ez(self, schema, table, where_dict=None, exit_on_error=True):
		try:
			x = -1
			sql = f"delete from {schema}.{table}"
			x = None
			if where_dict:
				first_yn = 'Y'
				# vals = []
				for k in where_dict:
					v = self.GoodValue(where_dict[k])
					if self.HasVal(v):
						w = 'and'
						if first_yn == 'Y':
							w = 'where'
							first_yn = 'N'
						sql += "{} {} = {} ".format(w, k, v)
			x = self.seld(sql)
		except Exception as e:
			print('del_ez()')
			traceback.print_exc()
			print(type(e))
			print(e)
			print(schema)
			print(table)
			print(where_dict)
		return x

#<=====>#

	async def sel_async(self, sql, vals=None, exit_on_error=True):
		try:
			r = None
			conn = await aiomysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			cur = await conn.cursor()
			if vals:
				await cur.execute(sql, vals)
			else:
				await cur.execute(sql)
#			print(cur.description)
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
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			print('exiting...')
			if exit_on_error: sys.exit()
		return r

#<=====>#

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

	async def seld_async(self, sql, vals=None, exit_on_error=True):
		try:
			r = None
			conn = await aiomysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			cur = await conn.cursor(aiomysql.DictCursor)
			if vals:
				await cur.execute(sql, vals)
			else:
				await cur.execute(sql)
#			print(cur.description)
			row_cnt = cur.rowcount
			col_cnt = len(cur.description)
			if row_cnt == 0 and col_cnt == 0:
				r = {}
			elif row_cnt == 1:
				r = await cur.fetchall()
			else:
				r = await cur.fetchall()
			await cur.close()
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			print('exiting...')
			if exit_on_error: sys.exit()
		return r

#<=====>#

	async def ins_one_async(self, sql, vals=None, exit_on_error=True):
		try:
			r = None
			conn = await aiomysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			cur = await conn.cursor()
			if vals:
				await cur.execute(sql, vals)
			else:
				await cur.execute(sql)
#			print(cur.description)
			r = cur.lastrowid
			await cur.close()
			await conn.commit()
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			print('exiting...')
			if exit_on_error: sys.exit()
		return r

#<=====>#

	async def ins_many_async(self, sql, vals, exit_on_error=True):
		try:
			r = None
			conn = await aiomysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			cur = await conn.cursor()
			if vals:
				await cur.executemany(sql, vals)
			else:
				await cur.execute(sql)
#			print(cur.description)
			r = cur.rowcount
			await cur.close()
			await conn.commit()
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			print('exiting...')
			if exit_on_error: sys.exit()
		return r

#<=====>#

	async def upd_async(self, sql, vals=None, exit_on_error=True):
		try:
			r = None
			conn = await aiomysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			cur = await conn.cursor()
			if vals:
				await cur.execute(sql, vals)
			else:
				await cur.execute(sql)
#			print(cur.description)
			r = cur.rowcount
			await cur.close()
			await conn.commit()
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			print('exiting...')
			if exit_on_error: sys.exit()
		return r

#<=====>#

	async def delete_async(self, sql, vals=None, exit_on_error=True):
		try:
			r = None
			conn = await aiomysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			cur = await conn.cursor()
			if vals:
				await cur.execute(sql, vals)
			else:
				await cur.execute(sql)
			print(cur.description)
			r = cur.rowcount
			await cur.close()
			await conn.commit()
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			print('exiting...')
			if exit_on_error: sys.exit()
		return r

#<=====>#

	async def execute_async(self, sql, vals=None, exit_on_error=True):
		try:
			r = None
			conn = await aiomysql.connect(host=self.db_host, port=self.db_port, db=self.db_name, user=self.db_user, password=self.db_pw)
			cur = await conn.cursor()
			if vals:
				await cur.execute(sql, vals)
			else:
				await cur.execute(sql)
			print(cur.description)
			r = cur.rowcount
			await cur.close()
			await conn.commit()
		except Exception as e:
			traceback.print_exc()
			print(type(e))
			print(e)
			print('exiting...')
			if exit_on_error: sys.exit()
		return r

#<=====>#

#	def insert_one(self, sql, vals):
#		self.__open()
#		self.__session.execute(sql, vals)
#		self.__connection.commit()
#		self.__close()
#		return self.__session.lastrowid
#	## End def insert

#<=====>#

#	def insert_many(self, sql, vals):
#		self.__open()
#		self.__session.executemany(sql, vals)
#		self.__connection.commit()
#		self.__close()
#		return self.__session.rowcount
#	## End def insert

#<=====>#

#	def delete(self, sql):
#		self.__open()
#		self.__session.execute(sql)
#		self.__connection.commit()
#		# Obtain rows affected
#		delete_rows = self.__session.rowcount
#		self.__close()
#		return delete_rows

#<=====>#

#	def exe(self, sql):
#		self.__open()
#		self.__session.execute(sql)
#		self.__connection.commit()
#		self.__close()
#		return self.__session.lastrowid
#	## End def execute

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


