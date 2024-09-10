#<=====>#
# Description
#<=====>#


#<=====>#
# Import All
#<=====>#

import_all_func_list = []
#import_all_func_list.append("db_table_names_get")
__all__ = import_all_func_list

#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Common Modules
#<=====>#
# import pandas as pd
import sys
import os
import re
import time
import duckdb
import pandas as pd

#<=====>#
# Imports - Download Modules
#<=====>#


#<=====>#
# Imports - Shared Library
#<=====>#
# shared_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SHARED_LIBS'))
# if shared_libs_path not in sys.path:
# 	sys.path.append(shared_libs_path)


#<=====>#
# Imports - Local Library
#<=====>#
local_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'libs'))
if local_libs_path not in sys.path:
	sys.path.append(local_libs_path)

from cls_db_duckdb                 import db_duckdb

from lib_common                    import *

#<=====>#
# Variables
#<=====>#
lib_name      = 'lib_duckdb'
log_name      = 'lib_duckdb'
lib_verbosity = 1
lib_debug_lvl = 1
verbosity     = 1
debug_lvl     = 1
lib_secs_max  = 0.33
lib_secs_max  = 10

#<=====>#
# Assignments Pre
#<=====>#

ddb = db_duckdb('duckdb.ddb')

# https://duckdb.org/docs/data/json/overview
# https://duckdb.org/docs/api/python/overview



# converting data from mysql to duckdb
# https://duckdb.org/docs/extensions/mysql.html

# connect & reading from mysql
'''
ATTACH 'host=localhost user=root port=0 database=mysql' AS mysqldb (TYPE MYSQL);
USE mysqldb;
'''

conn = duckdb.connect('ohlcv/ohlcv_test.ddb')
cur = conn.cursor()
cur.execute("create table if not exists ohlcv (timestamp timestamp, open real, high real, low real, close real, vol real);")
cur.execute("insert into ohlcv (timestamp, open, high, low, close, vol) values (current_timestamp, 2, 5, 1, 3, 100);")
cur.commit()
cur.close()
conn.close()

# duckdb.sql - also work instead of doing all the cursor above
# conn.sql - also work instead of doing all the cursor above

duckdb.read_csv('test.csv')
duckdb.sql('select * from test.csv')
print(duckdb.sql('select * from "test.csv" where age > 40'))

# what is a parquet file? also works with those aside from csv

df = pd.read_csv("test.csv")
print(duckdb.sql('select * from df where age > 40'))


# select directly from data in a pandas dataframe
r = duckdb.sql('select * from df where age > 40').fetchall()
# gives back a list of the values of the columns.  ie list of lists



r = duckdb.sql('select * from df where age > 40').df()
# gives back a pandas dataframe

r = duckdb.sql('select * from df where age > 40').pl()
# gives back a polars dataframe

r = duckdb.sql('select * from df where age > 40').fetchnumpy()
# gives back a numpy format, dict of columns with lists of the values...

# creates new database
conn = duckdb.connect('somedb.ddb')
# creates table from select csv
conn.sql('create table if not exists csv_data as select * from "data.csv";')
conn.commit()
conn.close()

# creates new database
conn = duckdb.connect('somedb.ddb')
# creates table from df
conn.register('pd_data', df)


# complex query returned as df
conn = duckdb.connect('mydb.ddb')
query = """
with filtered_data as (select job, avg(age) as avg_age, from people where age > 25 group by job), 
job_counts as (select job, count(*) as count from eope group by job)
select fd.joob, fd.avg_age, jc.count
from filtered data fd
join jo_counts c on fd.job = fc.job
where jc.count > 1
order by fd.avg_age desc
"""
print(conn.sql(query).df())
conn.commit()
conn.close()

#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#



#<=====>#


#<=====>#
# Post Variables
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#
