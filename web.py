#<=====>#
# Description
#<=====>#

#<=====>#
# Known To Do List
#<=====>#

#<=====>#
# Imports - Common Modules
#<=====>#
from datetime import datetime
import pytz
# Get the current time in UTC with timezone awareness
#utc_time = datetime.now(pytz.utc)

from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from flask import Flask
#from flask import redirect
from flask import render_template
#from flask import request
from markupsafe import Markup
#from requests.exceptions import ConnectionError
#from requests.exceptions import SSLError

import calendar
import decimal
#import errno
#import json
#import logging
# import os
import pandas as pd
#import pymysql as mysql
import re
#import requests
import sys
import os
import time
import traceback
import warnings

warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

#<=====>#
# Imports - Download Modules
#<=====>#



#<=====>#
# Imports - Shared Library
#<=====>#
#shared_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SHARED_LIBS'))
#if shared_libs_path not in sys.path:
#	sys.path.append(shared_libs_path)


#<=====>#
# Imports - Local Library
#<=====>#
local_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'libs'))
if local_libs_path not in sys.path:
	sys.path.append(local_libs_path)

from libs.lib_common                        import *

from libs.bot_common                        import *
from libs.bot_db_read                       import db


#<=====>#
# Variables
#<=====>#
lib_name      = 'web'
log_name      = 'web'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 0


#<=====>#
# Assignments Pre
#<=====>#

#<=====>#
# Classes
#<=====>#

#<=====>#
# Functions
#<=====>#

#<=====>#

def build_topnav():

	s = ""
	s += "select distinct prod_id as mkt "
	s += "  from cbtrade.poss "
	s += "  order by prod_id "
	try:
		mkt_data = db.sel(s)
	except:
		print(s)
		raise
	else:
		pass

	s = ""
	s += "select distinct date_format(pos_end_dttm,'%Y-%m-%d') as cdt "
	s += "  from cbtrade.poss  "
	s += "  order by 1 desc"
	try:
		date_data = db.sel(s)
	except:
		print(s)
		raise
	else:
		pass

	s = ""
	s = s + "select distinct date_format(pos_end_dttm,'%Y') as cy "
	s = s + "  , date_format(pos_end_dttm,'%m') as cm "
	s = s + "  , date_format(pos_end_dttm,'%M') as mn "
	s = s + "  from cbtrade.poss "
	s = s + "  order by 1 desc, 2 desc "
	try:
		month_data = db.seld(s)
	except:
		print(s)
		raise
	else:
		pass

	s = ""
	s += "select distinct date_format(pos_end_dttm,'%Y') as cy  "
	s += "  from cbtrade.poss "
	s += "  order by 1"
	try:
		year_data = db.sel(s)
	except:
		print(s)
		raise
	else:
		pass

	mkt_dd = ""
	mkt_dd = mkt_dd + "<select id='mkts' onchange=" + chr(34) + "window.open(this.value,'_self');" + chr(34) + ">"
	mkt_dd = mkt_dd + "<option value='#'>Choose Market</option>"
	if mkt_data:
		for mkt in mkt_data:
			if mkt is not None:
				mkt = mkt.replace('-','_')
				mkt_dd = mkt_dd + "<option value='/market_" + mkt + "'>" + mkt + "</option>"
	mkt_dd = mkt_dd + "</select>"

	s_dt_dd = ""
	s_dt_dd = s_dt_dd + "<select id='sales_dt_dd' onchange=" + chr(34) + "window.open(this.value,'_self');" + chr(34) + ">"
	s_dt_dd = s_dt_dd + "<option value='#'>Choose Date</option>"
	if date_data:
		for cdt in date_data:
			if cdt is not None:
				s_dt_dd = s_dt_dd + "<option value='/sales_dt_" + cdt + "'>" + cdt + "</option>"
	s_dt_dd = s_dt_dd + "</select>"

	s_m_dd = ""
	s_m_dd = s_m_dd + "<select id='sales_m_dd' onchange=" + chr(34) + "window.open(this.value,'_self');" + chr(34) + ">"
	s_m_dd = s_m_dd + "<option value='#'>Choose Month</option>"
	if month_data:
		for row in month_data:
			if row['cy'] is not None:
				s_m_dd = s_m_dd + "<option value='/sales_month_" + row['cy'] + "_" + row['cm'] + "'>" + row['cy'] + " " + row['mn'] + "</option>"
	s_m_dd = s_m_dd + "</select>"

	s_y_dd = ""
	s_y_dd = s_y_dd + "<select id='sales_y_dd' onchange=" + chr(34) + "window.open(this.value,'_self');" + chr(34) + ">"
	s_y_dd = s_y_dd + "<option value='#'>Choose Year</option>"
	if year_data:
		for cy in year_data:
			if cy is not None:
				s_y_dd = s_y_dd + "<option value='/sales_year_" + cy + "'>" + cy + "</option>"
	s_y_dd = s_y_dd + "</select>"

	html = ""
	html += "<table class='nav'>"
	html += "<thead>"
	html += "  <tr><th class='nav2' width='*'>Navs</th></tr>"
	html += "</thead>"
	html += "<tbody>"

	# Home
	html = build_topnav_link( in_str='Home', in_url='home.htm',  in_html=html)

	# Quick Looks
	html = build_topnav_title(in_str='Quick Looks', in_html=html)
	html = build_topnav_link( in_str='Balances',    in_url='balances.htm',  in_html=html)
	html = build_topnav_link( in_str='Open Poss',   in_url='open_poss.htm', in_html=html)
	html = build_topnav_link( in_str='Buys - Recent',   in_url='buys_recent.htm', in_html=html)
	html = build_topnav_link( in_str='Sells - Recent',   in_url='sells_recent.htm', in_html=html)
	html = build_topnav_link( in_str='Markets',     in_url='markets.htm',   in_html=html)
	html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;'>" + mkt_dd + "</td></tr>"

	# Sales Summary
	html = build_topnav_title(in_str='Sales Summary', in_html=html)
	html = build_topnav_link( in_str='All',    in_url='sales_all.htm',  in_html=html)
	html = build_topnav_link( in_str='Today',   in_url='sales_today.htm', in_html=html)
	html = build_topnav_link( in_str='Yesterday',     in_url='sales_yesterday.htm',   in_html=html)
#	html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;' onclick=" + chr(34) + "window.open('/sales_all.htm','_self');" + chr(34) + "><a href='/sales_all.htm'>All</a></td></tr>"
#	html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;' onclick=" + chr(34) + "window.open('/sales_today.htm','_self');" + chr(34) + "><a href='/sales_today.htm'>Today</a></td></tr>"
#	html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;' onclick=" + chr(34) + "window.open('/sales_yesterday.htm','_self');" + chr(34) + "><a href='/sales_yesterday.htm'>Yesterday</a></td></tr>"
	html += "  <tr>"
	html += "    <td>"
	html += "      <table width='100%' border=0 style='background-color:#0000ff;'>"
	html += "        <tr>"
	html += "          <td class='dud' style='text-align:left;'>Past</td>"
	html += "          <td>"
	html += "            <table width='100%' border=0 border=0 style='background-color:#0000ff;'>"
	html += "              <tr>"
	for x in (3,7,14,30):
		html += "            <td class='nav' style='vertical-align:top;text-align:left;' onclick=" + chr(34) + "window.open('/sales_{}d.htm','_self');".format(x) + chr(34) + "><a href='/sales_{}d.htm'>{}</a></td>".format(x,x)
	html += "                <td class='nav' style='vertical-align:top;text-align:left;' onclick=" + chr(34) + "window.open('/sales_all.htm','_self');" + chr(34) + "><a href='/sales_all.htm'>*</a></td>"
	html += "              </tr>"
	html += "            </table>"
	html += "          </td>"
	html += "          <td class='dud' style='text-align:left'>Days</td>"
	html += "        </tr>"
	html += "      </table>"
	html += "    </td>"
	html += "  </tr>"

	# Sales By Date
	html = build_topnav_title(in_str='Sales By Date', in_html=html)
	html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;'>" + s_dt_dd + "</td></tr>"
	html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;'>" + s_m_dd + "</td></tr>"
	html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;'>" + s_y_dd + "</td></tr>"


	# Best
	html = build_topnav_link( in_str='Buy Strats',       in_url='best_strats.htm',        in_html=html)
	html = build_topnav_link( in_str='Buy Markets',      in_url='best_markets.htm',       in_html=html)

	# Worst
	html = build_topnav_link( in_str='Worst Strats',       in_url='worst_strats.htm',        in_html=html)
	html = build_topnav_link( in_str='Worst Markets',      in_url='worst_markets.htm',       in_html=html)


	# Buy Strats
	html = build_topnav_title(in_str='Buy Strats',             in_html=html)
	html = build_topnav_link( in_str='Buy Strats Today',       in_url='buy_strats_today.htm',       in_html=html)
	html = build_topnav_link( in_str='Buy Strats All',         in_url='buy_strats_all.htm',         in_html=html)
	html = build_topnav_link( in_str='Buy Strats Prods Today', in_url='buy_strats_prods_today.htm', in_html=html)
	html = build_topnav_link( in_str='Buy Strats Prods All',   in_url='buy_strats_prods_all.htm',   in_html=html)

	# Sell Strats
	html = build_topnav_title(in_str='Sell Strats',             in_html=html)
	html = build_topnav_link( in_str='Sell Strats Today',       in_url='sell_strats_today.htm',       in_html=html)
	html = build_topnav_link( in_str='Sell Strats All',         in_url='sell_strats_all.htm',         in_html=html)
	html = build_topnav_link( in_str='Sell Strats Prods Today', in_url='sell_strats_prods_today.htm', in_html=html)
	html = build_topnav_link( in_str='Sell Strats Prods All',   in_url='sell_strats_prods_all.htm',   in_html=html)

	# Misc
	html = build_topnav_title(in_str='Misc', in_html=html)
	html = build_topnav_link(in_str='DB Size', in_url='db_size.htm', in_html=html)

	html += "</tbody>"
	html += "</table>"

	html = Markup(html)

	return html

#<=====>#

def build_topnav_title(in_str, in_html):
	html = in_html
	html += "<tr>"
	html += "<th class='nav' style='vertical-align:top;text-align:left;'>"
	html += "{}".format(in_str)
	html += "</th>"
	html += "</tr>"
	return html

#<=====>#

def build_topnav_link(in_str, in_url, in_html):
	html = in_html
	html += "<tr>"
	html += "<td "
	html += "  class='nav' "
	html += "  style='vertical-align:top;text-align:left;' "
	html += "  onclick={}window.open('/{}','_self');{}>".format('"', in_url,'"')
	html += "<a href='/{}'>{}</a>".format(in_url, in_str)
	html += "</td>"
	html += "</tr>"
	return html

#<=====>#

def html_up_add(u=None) -> str:
	if not u:
		u = ""
		u = "<table width=100%><tr><td width=100%>"
	return u

#<=====>#

def html_down_add(d=None) -> str:
	if not d:
		d = ""
		d = "</td></td></table>"
	return d

#<=====>#

def html_h1_add(t, m=None, u=None, d=None) -> str:
	if not u: html_up_add()
	if not d: html_down_add()
	if m:
		m = '{}<hr><h1>{}</h1>'.format(m, t)
	else:
		m = '<br><hr><h1>{}</h1>'.format(t)

	return m, u, d

#<=====>#

def html_h2_add(t, m=None, u=None, d=None) -> str:
	if not u: html_up_add()
	if not d: html_down_add()
	if m:
		m = '{}<hr><h2>{}</h2>'.format(m, t)
	else:
		m = '<br><hr><h2>{}</h2>'.format(t)

	return m, u, d

#<=====>#

def html_h3_add(t, m=None, u=None, d=None) -> str:
	if not u: html_up_add()
	if not d: html_down_add()
	if m:
		m = '{}<hr><h3>{}</h3>'.format(m, t)
	else:
		m = '<br><hr><h3>{}</h3>'.format(t)

	return m, u, d

#<=====>#

def html_add(more, m=None, u=None, d=None) -> str:
	if not u: html_up_add()
	if not d: html_down_add()
	if mid:
		m = '{}{}'.format(m, more)
	else:
		m = more
	return m, u, d

#<=====>#

def html_comb(m=None, u=None, d=None) -> str:
	html = ''
	if u:
		html = '{}{}'.format(html, u)
	if m:
		html = '{}{}'.format(html, m)
	if d:
		html = '{}{}'.format(html, d)

	html = Markup(html)

	return html

#<=====>#

def frmt_sci_not_tf(s):
	# Regular expression to identify scientific notation
	scientific_notation_pattern = re.compile(r'^[+-]?\d+(\.\d+)?[eE][+-]?\d+$')
	return bool(scientific_notation_pattern.match(str(s)))

#<=====>#

def frmt_sci_not_2_dec(s):
	s = str(s)
	if frmt_sci_not_tf(s):
		# Convert to float
		num = float(s)
		# Get the number of decimal places
		decimal_places = get_decimal_places(s)
		# Use format to display the correct number of decimals
		formatted_number = f"{num:.{decimal_places + abs(int(s.split('e')[-1]))}f}"
		f = formatted_number.rstrip('0').rstrip('.') if '.' in formatted_number else formatted_number
		return f
	else:
		return s  # Return the original string if not in scientific notation

#<=====>#

def get_decimal_places(s):
	s = str(s)
	# Regular expression to capture the number of decimal places in the scientific notation
	match = re.match(r'^[+-]?\d+(\.\d+)?[eE][+-]?\d+$', s)
	if match:
		decimal_part = match.group(1)
		if decimal_part:
			return len(decimal_part) - 1  # Subtract 1 to account for the dot
	return 0

#<=====>#

def build_data_display(data, table_id='first'):

	html = ''

	if not data:
		return html

	if not isinstance(data, list):
		return html

	# get first dict from list to grab keys as headers
	first_d = data[0]
	if isinstance(first_d, dict):
		headers = list(first_d.keys())

	rows = data

#	re_ptn_isnumeric = re.compile(r'^[$]?[-+]?[0-9\,]*\.?[0-9]+$')
#	re_ptn_lowercase = re.compile('[a-z]+')
#	re_ptn_uppercase = re.compile('[A-Z0-9]+')
	re_prod_id       = re.compile(r'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$')
#	re_symb       = re.compile(r'^[a-zA-Z0-9]+$')

	html = ""
	html += "<html>"
	html += "<body>"
#	html += "<table border=1 style='background-color:#000000' id='{}'>".format(table_id)
	html += "<table border=1 id='{}'>".format(table_id)
	html += "<thead>"

	#headers
	html += "<tr>"
	head_cnt = 0
	for header in headers:
		html += "<th class='dt' onclick={}sortTable('{}',{});{}>{}</th>".format('"', table_id, head_cnt, '"', header)
		head_cnt += 1
	html += "</tr>"
	html += "</thead>"
	html += "<tbody>"

#	x = 0
#	if x:
#		print('when x is 0 it evals as True')
#	else:
#		print('when x is 0 it evals as False')

	#contents
	for row in rows:
		html += "<tr class='dt'>"
		for k in row:
			v = row[k]

#			if k =='win_cnt':
#				print(f'win_cnt ({type(row[k])}): {row[k]}')

			if isinstance(v, decimal.Decimal):
				if v == int(v):
					v = int(v)
				else:
					v = float(v)

#			if k =='win_cnt':
#				print(f'win_cnt ({type(row[k])}): {row[k]}')

#			if isinstance(v, (float, decimal.Decimal)):
#				try:
#					if frmt_sci_not_tf(v):
#						v = frmt_sci_not_2_dec(v)
#				except:
#					print('err...')
#					print(type(v))
#					print(v)
#					pass

			try:

				if 0 == 1:
					print('never going to give you up')

				# integer
				elif isinstance(v, int):
					html += build_td_int(v)

				# decimal
				elif isinstance(v, (float,decimal.Decimal)):
					html += build_td_dec(v)

				# datetime
				elif isinstance(v, datetime):
					html += build_td_str(str(v))

				# Logo Img
				elif isinstance(v, str) and v[-4:].lower() in ('.png','.jpg','.jpeg','.gif'):
					html += build_td_img(v)

				# URL
				elif isinstance(v, str) and v[:6].lower() in ('http:/','https:'):
					html += build_td_url(v)

				# URL
				elif isinstance(v, str) and v[:4].lower() in ('www.'):
					html += build_td_url(v)

				# USD
				elif isinstance(v, str) and k[-4:].lower() == '_usd' or str(v).find('$') >= 0:
					html += build_td_usd(v)

				# PERCENT
				elif isinstance(v, str) and k[-4:].lower() == '_pct' or str(v).find('%') >= 0:
					html += build_td_pct(v)

				# BOLD
				elif isinstance(v, str) and re_prod_id.match(str(v)):
					html += build_td_bold(v)

				# STR
				elif isinstance(v, str):
					html += build_td_str(v)

				# NULL
				elif v == 0:
					html += build_td_int(v)

				# NULL
				elif not v:
					html += build_td_str('')

				else:
					html += "<td class='dt' style='text-align:center'>" + str(v) + "</td>"

			except:
				traceback.print_exc()
				print(f'v ({type(v)}): {v}')
				pass

		html += "</tr>"

	html += "</tbody>"
	html += "</table>"
	html += "</body>"
	html += "</html>"

	html = html.replace('>None<','-')
	html = html.replace('0E-8','0')

	html = Markup(html)
	return html

#<=====>#

def build_sql_display(s, table_id='first'):
#	try:
#		rows, headers = db.curs(s)
#	except:
#		print(s)
#		raise
#	else:
##		print(headers)
##		print(rows)
#		pass

	data = db.seld(s)

	html = build_data_display(data, table_id)

#	logging.info(html)
	return html

#<=====>#

def build_sql_display_old(s, table_id='first'):

	html = ""
	html += "<html>"
	html += "<body>"
	html += "<table border=1 style='background-color:#000000' id='{}'>".format(table_id)
	html += "<thead>"

	try:
		rows, headers = db.curs(s)
	except:
		print(s)
		raise
	else:
#		print(headers)
#		print(rows)
		pass

#	re_ptn_isnumeric = re.compile('^[$]?[-+]?[0-9\,]*\.?[0-9]+$')
	re_ptn_isnumeric = re.compile(r'^[$]?[-+]?[0-9\,]*\.?[0-9]+$')
	re_ptn_lowercase = re.compile('[a-z]+')
#	re_prod_id       = re.compile('[a-zA-Z0-9]+\-[a-zA-Z0-9]+')
	re_prod_id       = re.compile(r'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$')
#	re_symb       = re.compile(r'^[a-zA-Z0-9]+$')

#	re_ptn_allcaps = re.compile('^[A-Z0-9\- ].*')
#	re_ptn_lower = re.compile('[a-z]+')
#	re_ptn_string = re.compile('^[a-zA-Z0-9\- ]+')

#headers
	html += "<tr>"
	head_cnt = 0
	for header in headers:
		html += "<th class='dt' onclick={}sortTable('{}',{});{}>{}</th>".format('"', table_id, head_cnt, '"', header)
		head_cnt += 1
	html += "</tr>"
	html += "</thead>"
	html += "<tbody>"

#contents
	for row in rows:
		html += "<tr class='dt'>"
		for col in row:
			if isinstance(col, decimal.Decimal):
				col = float(col)
#			col = str(col).replace('0E-8','0')
#			col = str(col).replace('0E-10','0')
#			col = str(col).replace('0E-12','0')
#			col = str(col).replace('0E-14','0')
#			col = str(col).replace('0E-16','0')

			if isinstance(col, (float, decimal.Decimal)):
				try:
					if frmt_sci_not_tf(col):
						col = frmt_sci_not_2_dec(col)
				except:
					print('err...')
					print(type(col))
					print(col)
					pass

			if 0 == 1:
				print('never going to give you up')

#			# Hide Zeroes
#			elif str(col) == "0":
#				html += "<td class='dt' style='text-align:right;background:transparent;border:0'></td>"
#
#			# Hide Zeroes
#			elif str(col) == "0.0":
#				html += "<td class='dt' style='text-align:right;background:transparent;border:0'></td>"
#
#			# Hide Zeroes
#			elif str(col) in ("0.00", "0.0000", "0.000000", "0.00000000", "0.0000000000" ,"0.000000000000", "0.00000000000000"):
#				html += "<td class='dt' style='text-align:right;background:transparent;border:0'></td>"
#
#			# Hide Nulls
#			elif str(col) == "None":
#				html += "<td class='dt' style='text-align:right;background:transparent;border:0'></td>"
#
#			# Hide Blanks
#			elif str(col) == "":
#				html += "<td class='dt' style='text-align:right;background:transparent;border:0'></td>"

			# Probably MC, TC or Pair
			elif re_prod_id.match(str(col)):
				html += "<td class='dt' style='text-align:center;color:#ffffff;background-color:#000000'>{}</td>".format(col)

			# Logo Img
			elif str(col).find('https://bittrexblobstorage.blob.core.windows.net') >= 0 and str(col).find('.png') >= 0:
				html += "<td class='dt' style='text-align:center;background:black'><img src='" + str(col) + "' width='25' height='25'></img></td>"

			# Contains a USD Amount
			elif str(col).find('$') >= 0:
				if str(col).find('-') >= 0:
					html += "<td class='dt' style='text-align:right;background:red;color:yellow'>"
					html += "<div style='float:left;width=10%;'>$</div>"
					html += "<div style='float:right;width=90%;'>"
					st	= str(col)
					st = st.replace('$','')
					st = st.replace(' ','')
					html += st
					html += "</div>"
					html += "</td>"
				else:
					html += "<td class='dt' style='text-align:right;background:green;color:yellow'>"
					html += "<div style='float:left;width=10%;'>$</div>"
					html += "<div style='float:right;width=90%;'>"
					st	= str(col)
					st = st.replace('$','')
					st = st.replace(' ','')
					html += st
					html += "</div>"
					html += "</td>"

			# Contains a Percent
			elif str(col).find('%') >= 0:
				if str(col).find('-') >= 0:
					html += "<td class='dt' style='text-align:right;background:red;color:yellow;'>" + str(col) + "</td>"
				else:
					html += "<td class='dt' style='text-align:right;background:green;color:yellow;'>" + str(col) + "</td>"

			# Probably MC, TC or Pair
			elif re_ptn_lowercase.search(str(col)) is None:
				html += "<td class='dt' style='text-align:center'>" + str(col) + "</td>"

			# Probably a String
			elif re_ptn_lowercase.search(str(col)):
				html += "<td class='dt' style='text-align:left'>" + str(col) + "</td>"

			# Number
			elif re_ptn_isnumeric.match(str(col)):
				html += "<td class='dt' style='text-align:right'>" + str(col) + "</td>"

			else:
				html += "<td class='dt' style='text-align:center'>" + str(col) + "</td>"
		html += "</tr>"

	html += "</tbody>"
	html += "</table>"
	html += "</body>"
	html += "</html>"

	html = html.replace('>None<','-')
	html = html.replace('0E-8','0')

	html = Markup(html)
#	logging.info(html)
	return html

#<=====>#

def build_td_int(v=None) -> str:
	if not v:
		return "<td></td>"
	else:
		html = "<td class='dt' style='text-align:left'>" + str(v) + "</td>"
	return html

#<=====>#

def build_td_dec(v=None) -> str:
	if not v:
		return "<td></td>"
	else:
		html = "<td class='dt' style='text-align:right'>" + str(v) + "</td>"
	return html

#<=====>#

def build_td_usd(v=None) -> str:
	if not v:
		return "<td></td>"
	else:
		html = ""
		if str(v).find('-') >= 0:
			html += "<td class='dt' style='text-align:right;background:red;color:yellow'>"
			html += "<div style='float:left;width=10%;'>$</div>"
			html += "<div style='float:right;width=90%;'>"
			st	= str(v)
			st = st.replace('$','')
			st = st.replace(' ','')
			html += st
			html += "</div>"
			html += "</td>"
		else:
			html += "<td class='dt' style='text-align:right;background:green;color:yellow'>"
			html += "<div style='float:left;width=10%;'>$</div>"
			html += "<div style='float:right;width=90%;'>"
			st	= str(v)
			st = st.replace('$','')
			st = st.replace(' ','')
			html += st
			html += "</div>"
			html += "</td>"
	return html

#<=====>#

def build_td_pct(v=None) -> str:
	if not v:
		return "<td></td>"
	else:
		html = ""
		if str(v).find('-') >= 0:
			html += "<td class='dt' style='text-align:right;background:red;color:yellow;'>"
			html += str(v)
			html += "</td>"
		else:
			html += "<td class='dt' style='text-align:right;background:green;color:yellow;'>"
			html += str(v)
			html += "</td>"
	return html

#<=====>#

def build_td_str(v=None) -> str:
	if not v:
		return "<td></td>"
	else:
		html = "<td class='dt' style='text-align:left'>" + str(v) + "</td>"
	return html

#<=====>#

def build_td_bold(v=None) -> str:
	if not v:
		return "<td></td>"
	else:
		html = ""
#		html += "<td class='dt' style='text-align:center;color:#ffffff;background-color:#000000'>"
		html += "<td class='dt' style='text-align:center;background:silver'>"
		html += "{}".format(v)
		html += "</td>"
	return html

#<=====>#

def build_td_img(v=None) -> str:
	if not v:
		return "<td></td>"
	else:
		html = ""
		html += "<td class='dt' style='text-align:center;background:black'>"
		html += "<a href='/{}'>{}</a>".format(v, v)
		html += "</td>"
	return html

#<=====>#

def build_td_url(v=None) -> str:
	if not v:
		return "<td></td>"
	else:
		html = ""
		html += "<td class='dt' style='text-align:center;background:black'>"
		html += "<img src='" + str(v) + "' width='25' height='25'></img>"
		html += "</td>"
	return html

#<=====>#

def add_bals_total(t='Total Balance', m=None, u=None, d=None) -> str:
	print(str(datetime.now()) + " add_bals_total(t, m, u, d, h)")
#	dt = datetime.now(pytz.utc).strftime('%Y-%m-%d')

	t = 'Total Balance'
	sql = " "
	sql += "select x.cnt "
	sql += "  , concat('$',' ', round(x.bal_val_usd,4)) as bal_val_usd "
	sql += "  , concat('$',' ', round(x.bot_val_usd,4)) as bot_val_usd "
	sql += "  , concat('$',' ', round(x.free_val_usd,4)) as free_val_usd"

	sql += "  , (select sum(tot_out_cnt) from cbtrade.poss where ignore_tf=0 and pos_stat='CLOSE') as tot_out"
	sql += "  , (select sum(tot_in_cnt) from cbtrade.poss where ignore_tf=0 and pos_stat='CLOSE') as tot_in"

	sql += "  , (select sum(tot_out_cnt) from cbtrade.poss where ignore_tf=0 and pos_stat='OPEN') as spent_open"
	sql += "  , (select sum(tot_in_cnt) from cbtrade.poss px join cbtrade.mkts m on m.prod_id = px.prod_id where px.ignore_tf=0 and px.pos_stat='OPEN') as value_open"
	sql += "  , (select sum(hold_cnt) * m.prc from cbtrade.poss px join cbtrade.mkts m on m.prod_id = px.prod_id where px.ignore_tf=0 and px.pos_stat='OPEN') as value_open"

	sql += "  from (select count(b.symb) as cnt "
	sql += "          , sum(b.bal_val_usd) as bal_val_usd "
	sql += "          , sum(b.bot_val_usd) as bot_val_usd "
	sql += "          , sum(b.free_val_usd) as free_val_usd "
	sql += "          from cbtrade.view_bals b "
	sql += "       ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	return m, u, d

#<=====>#

#When you are using Flask, it is generally a good practice to run the app in the debug mode.
#You can also control the port number. Make the following changes in your python file:
#app.run(debug=True, port=3134)
#Now run the code and go to http://localhost:3134 to see the output.
#If you want to make this application accessible externally using the IP address,
#then you need to tell Flask by specifying the host parameter. Make the following change in your python file:
#app.run(host='0.0.0.0', debug=True, port=3134)
#Run the code and go to http://x.x.x.x:3134 (replace x.x.x.x with the right IP address) to see your external web server live!

#template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#template_dir = os.path.join(template_dir, 'flask')
#template_dir = os.path.join(template_dir, 'templates')
## hard coded absolute path for testing purposes
#working = 'C:\Python34\pro\\frontend\\templates'
#print(working == template_dir)
#app = Flask(__name__, template_folder=template_dir)

app = Flask(__name__)

now = datetime.now()

#<=====>#

@app.route("/")
@app.route("/home.htm")
def home() -> str:
	print(str(datetime.now()) + " home()")
	tn = build_topnav()
#	dt = datetime.now(pytz.utc).strftime('%Y-%m-%d')

	m     = None
	u     = None
	d     = None

	pt    = 'Home'

	m, u, d = add_bals_total(t='Total Balance', m=m, u=u, d=d)

	t     = 'Sales Summary - All Time'
	sql = ""
	sql += "select x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  , concat(x.gain_loss_pct_hr * 24 * 30, ' %') as gain_loss_pct_month "
	sql += "  , concat(x.gain_loss_pct_hr * 24 * 365, ' %') as gain_loss_pct_year "
	sql += "  from (select count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt),2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net),2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100, 2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          from cbtrade.poss p "
	sql += "          where ignore_tf = 0 "
	sql += "          and test_tf = 0 "
	sql += "          order by gain_loss_pct_hr desc "
	sql += "       ) x "
	sql += "  "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Sales Summary By Status - All Time'
	sql = ""
	sql += "select x.pos_stat "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.pos_stat "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where ignore_tf = 0 "
	sql += "          and test_tf = 0 "
	sql += "          group by p.pos_stat "
	sql += "          ) x "
	sql += "  order by x.pos_stat desc "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)




	t     = 'Daily Sales Summary'
	sql = ""
	sql += "select x.dt "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  , concat(x.gain_loss_pct_hr * 24 * 30, ' %') as gain_loss_pct_month "
	sql += "  , concat(x.gain_loss_pct_hr * 24 * 365, ' %') as gain_loss_pct_year "
	sql += "  from (select date(p.pos_end_dttm) as dt "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt),2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net),2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100, 2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          from cbtrade.poss p "
	sql += "          where ignore_tf = 0 "
	sql += "          and test_tf = 0 "
	sql += "          and pos_stat = 'CLOSE' "
	sql += "          group by date(p.pos_end_dttm) "
	sql += "          order by date(p.pos_end_dttm) desc "
	sql += "       ) x "
	sql += "  "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)





#	t     = 'Open Positions Summary - Current'
#	sql = ""
#	sql += "select x.pos_stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , x.win_cnt "
#	sql += "  , x.lose_cnt "
#	sql += "  , concat(x.win_pct, ' %') as win_pct "
#	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
#	sql += "  , x.age_hours "
#	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
#	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
#	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
#	sql += "  , concat('$ ', x.val_curr) as val_curr "
#	sql += "  , concat('$ ', x.val_tot) as val_tot "
#	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
#	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
#	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
#	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
#	sql += "  from (select p.pos_stat "
#	sql += "          , count(p.pos_id) as tot_cnt  "
#	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
#	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
#	sql += "          , sum(p.age_mins) as age_mins "
#	sql += "          , sum(p.age_mins) / 60 as age_hours "
#	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
#	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
#	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
#	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
#	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
#	sql += "          , sum(p.buy_cnt) as buy_cnt "
#	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
#	sql += "          , sum(p.hold_cnt) as hold_cnt "
#	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
#	sql += "          , sum(p.clip_cnt) as clip_cnt "
#	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
#	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
#	sql += "          , round(sum(p.val_curr), 2) as val_curr "
#	sql += "          , round(sum(p.val_tot), 2) as val_tot "
#	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
#	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
#	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
#	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
#	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
#	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
#	sql += "          , p.test_tf "
#	sql += "          from cbtrade.poss p "
#	sql += "          where ignore_tf = 0 "
#	sql += "          and test_tf = 0 "
#	sql += "          group by p.pos_stat "
#	sql += "          ) x "
#	sql += "  where x.pos_stat = 'OPEN' "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Closed Positions Summary - Today'
	sql = ""
	sql += "select x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.pos_stat "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt),2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net),2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100, 2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          and test_tf = 0 "
	sql += "          and date(p.pos_end_dttm) = UTC_DATE() "
	sql += "          group by p.pos_stat "
	sql += "          ) x "
	sql += "  where x.pos_stat = 'CLOSE' "
#	sql += "  order by x.dt desc "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Closed Positions Wins & Losses Summary - Today'
	sql = ""
	sql += "select x.pos_stat "
	sql += "  , x.win_loss "
	sql += "  , x.tot_cnt "
#	sql += "  , x.win_cnt "
#	sql += "  , x.lose_cnt "
#	sql += "  , concat(x.win_pct, ' %') as win_pct "
#	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.pos_stat "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , case when p.val_tot > p.tot_out_cnt then 'WIN' else 'LOSS' end as win_loss  "
#	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
#	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt),2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net),2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100, 2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          and test_tf = 0 "
	sql += "          and date(p.pos_end_dttm) = UTC_DATE() "
	sql += "          group by p.pos_stat "
	sql += "                 , case when p.val_tot > p.tot_out_cnt then 'WIN' else 'LOSS' end "
	sql += "          ) x "
	sql += "  where x.pos_stat = 'CLOSE' "
	sql += "  order by x.win_loss desc "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Closed Positions Product Summary - Current'
	sql = ""
	sql += "select x.prod_id "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.prod_id "
	sql += "          , p.pos_stat "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          and test_tf = 0 "
	sql += "          and p.pos_stat = 'CLOSE' "
	sql += "          group by p.prod_id, p.pos_stat "
	sql += "          ) x "
	sql += "  order by x.prod_id "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Closed Positions - Today'
	sql = ""
	sql += "select x.pos_id"
	sql += "  , x.prod_id"
#	sql += "  , x.pos_stat"
	sql += "  , x.pos_begin_dttm"
#	sql += "  , x.pos_end_dttm"
#	sql += "  , x.dt"
#	sql += "  , x.age_mins"
	sql += "  , x.age_hours"
	sql += "  , concat('$ ', x.tot_out_cnt) as spend "
#	sql += "  , concat('$ ', x.tot_in_cnt) as recvd "
#	sql += "  , concat('$ ', x.buy_fees_cnt) as buy_fees_cnt "
#	sql += "  , concat('$ ', x.sell_fees_cnt_tot) as sell_fees_cnt_tot "
#	sql += "  , concat('$ ', x.fees_cnt_tot) as fees "
#	sql += "  , x.buy_cnt"
#	sql += "  , x.sell_cnt_tot"
#	sql += "  , x.hold_cnt"
#	sql += "  , x.pocket_cnt"
#	sql += "  , x.clip_cnt"
#	sql += "  , concat(x.pocket_pct, ' %') as pocket_pct "
#	sql += "  , concat(x.clip_pct, ' %') as clip_pct "
#	sql += "  , x.sell_order_cnt "
#	sql += "  , x.sell_order_attempt_cnt "
	sql += "  , concat('$ ', round(x.prc_buy,6)) as prc_buy "
	sql += "  , concat('$ ', round(x.prc_curr,6)) as prc_curr "
	sql += "  , concat('$ ', round(x.prc_high,6)) as prc_high "
#	sql += "  , concat('$ ', round(x.prc_low,6)) as prc_low "
	sql += "  , concat(round(x.prc_chg_pct,2), ' %') as 'prc chg %' "
	sql += "  , concat(round(x.prc_chg_pct_high,2), ' %') as 'prc high %' "
#	sql += "  , concat(round(x.prc_chg_pct_low,2), ' %') as 'prc low %' "
	sql += "  , concat(round(x.prc_chg_pct_drop,2), ' %') as 'prc drop %' "
#	sql += "  , concat('$ ', round(x.prc_sell_avg,6)) as prc_sell_avg "
	sql += "  , concat('$ ', round(x.val_curr,4)) as val_curr "
	sql += "  , concat('$ ', round(x.val_tot,4)) as val_tot "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est,4)) as 'gain est' "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est_high,4)) as 'gain est high' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_est_low,4)) 'gain est low' "
	sql += "  , concat('$ ', round(x.gain_loss_amt,4)) as 'gain' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_net,4)) as 'gain net' "
	sql += "  , concat(round(x.gain_loss_pct_est,3), ' %') as 'gain % est' "
	sql += "  , concat(round(x.gain_loss_pct_est_high,3), ' %') as 'gain % est high' "
#	sql += "  , concat(round(x.gain_loss_pct_est_low,3), ' %') as 'gain % est low' "
	sql += "  , concat(round(x.gain_loss_pct,3), ' %') as 'gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr,8), ' %') as 'hourly gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr * 24,8), ' %') as 'daily gain %' "
#	sql += "  , x.buy_strat_type"
	sql += "  , x.buy_strat_name"
	sql += "  , x.buy_strat_freq"
#	sql += "  , x.sell_strat_type"
	sql += "  , x.sell_strat_name"
#	sql += "  , x.sell_strat_freq"
#	sql += "  , x.bo_id"
#	sql += "  , x.bo_uuid"
#	sql += "  , x.buy_curr_symb"
#	sql += "  , x.spend_curr_symb"
#	sql += "  , x.sell_curr_symb"
#	sql += "  , x.recv_curr_symb"
#	sql += "  , x.fees_curr_symb"
#	sql += "  , x.test_tf"
	sql += "  from cbtrade.view_pos x "
	sql += "  where x.pos_stat = 'CLOSE' "
	sql += "  and x.dt = UTC_DATE() "
	sql += "  order by x.prod_id, x.pos_id "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Open Positions Wins & Losses Summary - Today'
	sql = ""
	sql += "select x.pos_stat "
	sql += "  , x.win_loss "
	sql += "  , x.tot_cnt "
#	sql += "  , x.win_cnt "
#	sql += "  , x.lose_cnt "
#	sql += "  , concat(x.win_pct, ' %') as win_pct "
#	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.pos_stat "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , case when p.val_tot > p.tot_out_cnt then 'WIN' else 'LOSS' end as win_loss  "
#	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
#	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt),2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net),2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100, 2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          and test_tf = 0 "
#	sql += "          and date(p.pos_end_dttm) = UTC_DATE() "
	sql += "          group by p.pos_stat "
	sql += "                 , case when p.val_tot > p.tot_out_cnt then 'WIN' else 'LOSS' end "
	sql += "          ) x "
	sql += "  where x.pos_stat in ('OPEN','SELL') "
	sql += "  order by x.win_loss desc "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Open Positions Product Summary - Current'
	sql = ""
	sql += "select x.prod_id "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.prod_id "
	sql += "          , p.pos_stat "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          and test_tf = 0 "
	sql += "          group by p.prod_id, p.pos_stat "
	sql += "          ) x "
	sql += "  where x.pos_stat = 'OPEN' "
	sql += "  order by x.prod_id "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Open Positions - Current'
	sql = ""
	sql += "select x.pos_id"
	sql += "  , x.prod_id"
#	sql += "  , x.pos_stat"
	sql += "  , x.pos_begin_dttm"
#	sql += "  , x.pos_end_dttm"
#	sql += "  , x.dt"
#	sql += "  , x.age_mins"
	sql += "  , x.age_hours"
	sql += "  , concat('$ ', x.tot_out_cnt) as spend "
#	sql += "  , concat('$ ', x.tot_in_cnt) as recvd "
#	sql += "  , concat('$ ', x.buy_fees_cnt) as buy_fees_cnt "
#	sql += "  , concat('$ ', x.sell_fees_cnt_tot) as sell_fees_cnt_tot "
#	sql += "  , concat('$ ', x.fees_cnt_tot) as fees "
#	sql += "  , x.buy_cnt"
#	sql += "  , x.sell_cnt_tot"
#	sql += "  , x.hold_cnt"
#	sql += "  , x.pocket_cnt"
#	sql += "  , x.clip_cnt"
#	sql += "  , concat(x.pocket_pct, ' %') as pocket_pct "
#	sql += "  , concat(x.clip_pct, ' %') as clip_pct "
#	sql += "  , x.sell_order_cnt "
#	sql += "  , x.sell_order_attempt_cnt "
	sql += "  , concat('$ ', round(x.prc_buy,6)) as prc_buy "
	sql += "  , concat('$ ', round(x.prc_curr,6)) as prc_curr "
	sql += "  , concat('$ ', round(x.prc_high,6)) as prc_high "
#	sql += "  , concat('$ ', round(x.prc_low,6)) as prc_low "
	sql += "  , concat(round(x.prc_chg_pct,2), ' %') as 'prc chg %' "
	sql += "  , concat(round(x.prc_chg_pct_high,2), ' %') as 'prc high %' "
#	sql += "  , concat(round(x.prc_chg_pct_low,2), ' %') as 'prc low %' "
	sql += "  , concat(round(x.prc_chg_pct_drop,2), ' %') as 'prc drop %' "
#	sql += "  , concat('$ ', round(x.prc_sell_avg,6)) as prc_sell_avg "
	sql += "  , concat('$ ', round(x.val_curr,4)) as val_curr "
	sql += "  , concat('$ ', round(x.val_tot,4)) as val_tot "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est,4)) as 'gain est' "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est_high,4)) as 'gain est high' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_est_low,4)) 'gain est low' "
	sql += "  , concat('$ ', round(x.gain_loss_amt,4)) as 'gain' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_net,4)) as 'gain net' "
	sql += "  , concat(round(x.gain_loss_pct_est,3), ' %') as 'gain % est' "
	sql += "  , concat(round(x.gain_loss_pct_est_high,3), ' %') as 'gain % est high' "
#	sql += "  , concat(round(x.gain_loss_pct_est_low,3), ' %') as 'gain % est low' "
	sql += "  , concat(round(x.gain_loss_pct,3), ' %') as 'gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr,8), ' %') as 'hourly gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr * 24,8), ' %') as 'daily gain %' "
#	sql += "  , x.buy_strat_type"
	sql += "  , x.buy_strat_name"
	sql += "  , x.buy_strat_freq"
#	sql += "  , x.sell_strat_type"
#	sql += "  , x.sell_strat_name"
#	sql += "  , x.sell_strat_freq"
#	sql += "  , x.bo_id"
#	sql += "  , x.bo_uuid"
#	sql += "  , x.buy_curr_symb"
#	sql += "  , x.spend_curr_symb"
#	sql += "  , x.sell_curr_symb"
#	sql += "  , x.recv_curr_symb"
#	sql += "  , x.fees_curr_symb"
#	sql += "  , x.test_tf"
	sql += "  from cbtrade.view_pos x "
	sql += "  where x.pos_stat = 'OPEN' "
	sql += "  order by x.prod_id, x.pos_id "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/balances.htm")
def balances() -> str:
	print(str(datetime.now()) + " balances()")
	tn = build_topnav()

	m   = None
	u    = None
	d  = None

	pt = 'My Balances'

	m, u, d = add_bals_total(t='Total Balance', m=m, u=u, d=d)


	t = 'Current Balances - Order by Balance'
	sql = "  "
	sql += "select b.symb "
	sql += "  , coalesce(p.open_cnt, 0) as open_cnt "
	sql += "  , coalesce(p.close_cnt, 0) as close_cnt  "
	sql += "  , b.bal_avail as bal_cnt "
	sql += "  , coalesce(p.need_open_cnt, 0) as need_open_cnt "
	sql += "  , coalesce(p.need_hold_cnt, 0) as need_hold_cnt "
	sql += "  , case when b.symb in ('USD','USDC') then 1 else m.prc end as prc "
	sql += "  , coalesce((p.need_open_cnt + p.need_hold_cnt),0) as need_cnt_tot "
	sql += "  , b.bal_avail - coalesce((p.need_open_cnt + p.need_hold_cnt),0) as unknown_cnt "
	sql += "  , concat('$',' ', round(b.bal_avail * m.prc, 2)) as bal_val "
	sql += "  , concat('$',' ', coalesce(round(p.gain_loss_amt, 2), 0)) as gain_loss_amt "
	sql += "  , concat('$',' ', coalesce(round((p.need_open_cnt * m.prc), 2), 0)) as need_open_val "
	sql += "  , concat('$',' ', coalesce(round((p.need_hold_cnt * m.prc), 2), 0)) as need_hold_val "
	sql += "  , concat('$',' ', (b.bal_avail - coalesce((p.need_open_cnt + p.need_hold_cnt),0)) * m.prc) as unknown_val "
	sql += "  from cbtrade.bals b "
	sql += "  left outer join (select p.prod_id "
	sql += "                     , p.base_curr_symb "
	sql += "                       , p.quote_curr_symb "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' then 1 else 0 end) as open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' and gain_loss_amt_est >= 0 then 1 else 0 end) as win_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' and gain_loss_amt_est < 0 then 1 else 0 end) as lose_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'CLOSE' then 1 else 0 end) as close_cnt "
#	sql += "--                     , sum(case when p.pos_stat = 'CLOSE' and gain_loss_amt_est > 0  then 1 else 0 end) as win_close_cnt "
#	sql += "--                     , sum(case when p.pos_stat = 'CLOSE' and gain_loss_amt_est < 0 then 1 else 0 end) as lose_close_cnt "
#	sql += "--                     , count(p.age_mins) as age_mins "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' then p.buy_cnt else 0 end) as need_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'CLOSE' then p.hold_cnt else 0 end) as need_hold_cnt "
	sql += "                       , sum(p.pocket_cnt) as pocket_cnt "
	sql += "                       , sum(p.clip_cnt) as clip_cnt "
	sql += "                       , sum(p.gain_loss_amt) as gain_loss_amt "
	sql += "                       , sum(p.hold_cnt) * m.prc as hold_val "
	sql += "                       , sum(p.pocket_cnt) * m.prc as pocket_val "
	sql += "                       , sum(p.clip_cnt) * m.prc as clip_val "
	sql += "                       from cbtrade.poss p  "
	sql += "                       left outer join (select m.prod_id, m.base_curr_symb as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' "
	sql += "                                        union  "
	sql += "                                        select m.prod_id, 'ETH2' as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' and m.base_curr_symb = 'ETH' "
	sql += "                                        ) m on m.prod_id = p.prod_id "
	sql += "                       where 1=1 "
	sql += "                       and p.ignore_tf = 0 "
	sql += "                       and test_tf = 0 "
	sql += "                       group by p.prod_id, p.base_curr_symb, p.quote_curr_symb "
	sql += "                       order by p.prod_id, p.base_curr_symb, p.quote_curr_symb "
	sql += "                       ) p on p.base_curr_symb = b.symb  "
	sql += "  left outer join (select m.base_curr_symb as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' "
	sql += "                   union select 'USDC' as symb, 1 as prc "
	sql += "                   union select 'USD' as symb, 1 as prc "
	sql += "                   union select 'ETH2' as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' and m.base_curr_symb = 'ETH' "
	sql += "                   ) m on m.symb = b.symb "
	sql += "  where 1=1 "
	sql += "  order by b.bal_avail * m.prc desc "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t = 'Current Balance - Order by Symbol'
	sql = "  "
	sql += "select b.symb "
	sql += "  , coalesce(p.open_cnt, 0) as open_cnt "
	sql += "  , coalesce(p.close_cnt, 0) as close_cnt  "
	sql += "  , b.bal_avail as bal_cnt "
	sql += "  , coalesce(p.need_open_cnt, 0) as need_open_cnt "
	sql += "  , coalesce(p.need_hold_cnt, 0) as need_hold_cnt "
	sql += "  , case when b.symb in ('USD','USDC') then 1 else m.prc end as prc "
	sql += "  , coalesce((p.need_open_cnt + p.need_hold_cnt),0) as need_cnt_tot "
	sql += "  , b.bal_avail - coalesce((p.need_open_cnt + p.need_hold_cnt),0) as unknown_cnt "
	sql += "  , concat('$',' ', round(b.bal_avail * m.prc, 2)) as bal_val "
	sql += "  , concat('$',' ', coalesce(round(p.gain_loss_amt, 2), 0)) as gain_loss_amt "
	sql += "  , concat('$',' ', coalesce(round((p.need_open_cnt * m.prc), 2), 0)) as need_open_val "
	sql += "  , concat('$',' ', coalesce(round((p.need_hold_cnt * m.prc), 2), 0)) as need_hold_val "
	sql += "  , concat('$',' ', (b.bal_avail - coalesce((p.need_open_cnt + p.need_hold_cnt),0)) * m.prc) as unknown_val "
	sql += "  from cbtrade.bals b "
	sql += "  left outer join (select p.prod_id "
	sql += "                     , p.base_curr_symb "
	sql += "                       , p.quote_curr_symb "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' then 1 else 0 end) as open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' and gain_loss_amt_est >= 0 then 1 else 0 end) as win_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' and gain_loss_amt_est < 0 then 1 else 0 end) as lose_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'CLOSE' then 1 else 0 end) as close_cnt "
#	sql += "--                     , sum(case when p.pos_stat = 'CLOSE' and gain_loss_amt_est > 0  then 1 else 0 end) as win_close_cnt "
#	sql += "--                     , sum(case when p.pos_stat = 'CLOSE' and gain_loss_amt_est < 0 then 1 else 0 end) as lose_close_cnt "
#	sql += "--                     , count(p.age_mins) as age_mins "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' then p.buy_cnt else 0 end) as need_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'CLOSE' then p.hold_cnt else 0 end) as need_hold_cnt "
	sql += "                       , sum(p.pocket_cnt) as pocket_cnt "
	sql += "                       , sum(p.clip_cnt) as clip_cnt "
	sql += "                       , sum(p.gain_loss_amt) as gain_loss_amt "
	sql += "                       , sum(p.hold_cnt) * m.prc as hold_val "
	sql += "                       , sum(p.pocket_cnt) * m.prc as pocket_val "
	sql += "                       , sum(p.clip_cnt) * m.prc as clip_val "
	sql += "                       from cbtrade.poss p  "
	sql += "                       left outer join (select m.prod_id, m.base_curr_symb as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' "
	sql += "                                        union  "
	sql += "                                        select m.prod_id, 'ETH2' as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' and m.base_curr_symb = 'ETH' "
	sql += "                                        ) m on m.prod_id = p.prod_id "
	sql += "                       where 1=1 "
	sql += "                       and p.ignore_tf = 0 "
	sql += "                       and test_tf = 0 "
	sql += "                       group by p.prod_id, p.base_curr_symb, p.quote_curr_symb "
	sql += "                       order by p.prod_id, p.base_curr_symb, p.quote_curr_symb "
	sql += "                       ) p on p.base_curr_symb = b.symb  "
	sql += "  left outer join (select m.base_curr_symb as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' "
	sql += "                   union select 'USDC' as symb, 1 as prc "
	sql += "                   union select 'USD' as symb, 1 as prc "
	sql += "                   union select 'ETH2' as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' and m.base_curr_symb = 'ETH' "
	sql += "                   ) m on m.symb = b.symb "
	sql += "  where 1=1 "
	sql += "  order by b.symb "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t = 'Current Balances - Order by Free Balance'
	sql = "  "
	sql += "select b.symb "
	sql += "  , coalesce(p.open_cnt, 0) as open_cnt "
	sql += "  , coalesce(p.close_cnt, 0) as close_cnt  "
	sql += "  , b.bal_avail as bal_cnt "
	sql += "  , coalesce(p.need_open_cnt, 0) as need_open_cnt "
	sql += "  , coalesce(p.need_hold_cnt, 0) as need_hold_cnt "
	sql += "  , case when b.symb in ('USD','USDC') then 1 else m.prc end as prc "
	sql += "  , coalesce((p.need_open_cnt + p.need_hold_cnt),0) as need_cnt_tot "
	sql += "  , b.bal_avail - coalesce((p.need_open_cnt + p.need_hold_cnt),0) as unknown_cnt "
	sql += "  , concat('$',' ', round(b.bal_avail * m.prc, 2)) as bal_val "
	sql += "  , concat('$',' ', coalesce(round(p.gain_loss_amt, 2), 0)) as gain_loss_amt "
	sql += "  , concat('$',' ', coalesce(round((p.need_open_cnt * m.prc), 2), 0)) as need_open_val "
	sql += "  , concat('$',' ', coalesce(round((p.need_hold_cnt * m.prc), 2), 0)) as need_hold_val "
	sql += "  , concat('$',' ', (b.bal_avail - coalesce((p.need_open_cnt + p.need_hold_cnt),0)) * m.prc) as unknown_val "
	sql += "  from cbtrade.bals b "
	sql += "  left outer join (select p.prod_id "
	sql += "                     , p.base_curr_symb "
	sql += "                       , p.quote_curr_symb "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' then 1 else 0 end) as open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' and gain_loss_amt_est >= 0 then 1 else 0 end) as win_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' and gain_loss_amt_est < 0 then 1 else 0 end) as lose_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'CLOSE' then 1 else 0 end) as close_cnt "
#	sql += "--                     , sum(case when p.pos_stat = 'CLOSE' and gain_loss_amt_est > 0  then 1 else 0 end) as win_close_cnt "
#	sql += "--                     , sum(case when p.pos_stat = 'CLOSE' and gain_loss_amt_est < 0 then 1 else 0 end) as lose_close_cnt "
#	sql += "--                     , count(p.age_mins) as age_mins "
	sql += "                       , sum(case when p.pos_stat = 'OPEN' then p.buy_cnt else 0 end) as need_open_cnt "
	sql += "                       , sum(case when p.pos_stat = 'CLOSE' then p.hold_cnt else 0 end) as need_hold_cnt "
	sql += "                       , sum(p.pocket_cnt) as pocket_cnt "
	sql += "                       , sum(p.clip_cnt) as clip_cnt "
	sql += "                       , sum(p.gain_loss_amt) as gain_loss_amt "
	sql += "                       , sum(p.hold_cnt) * m.prc as hold_val "
	sql += "                       , sum(p.pocket_cnt) * m.prc as pocket_val "
	sql += "                       , sum(p.clip_cnt) * m.prc as clip_val "
	sql += "                       from cbtrade.poss p  "
	sql += "                       left outer join (select m.prod_id, m.base_curr_symb as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' "
	sql += "                                        union  "
	sql += "                                        select m.prod_id, 'ETH2' as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' and m.base_curr_symb = 'ETH' "
	sql += "                                        ) m on m.prod_id = p.prod_id "
	sql += "                       where 1=1 "
	sql += "                       and p.ignore_tf = 0 "
	sql += "                       and test_tf = 0 "
	sql += "                       group by p.prod_id, p.base_curr_symb, p.quote_curr_symb "
	sql += "                       order by p.prod_id, p.base_curr_symb, p.quote_curr_symb "
	sql += "                       ) p on p.base_curr_symb = b.symb  "
	sql += "  left outer join (select m.base_curr_symb as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' "
	sql += "                   union select 'USDC' as symb, 1 as prc "
	sql += "                   union select 'USD' as symb, 1 as prc "
	sql += "                   union select 'ETH2' as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' and m.base_curr_symb = 'ETH' "
	sql += "                   ) m on m.symb = b.symb "
	sql += "  where 1=1 "
	sql += "  order by (b.bal_avail - coalesce((p.need_open_cnt + p.need_hold_cnt),0)) * m.prc desc "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/open.htm")
@app.route("/open_poss.htm")
def open_poss() -> str:
	print(str(datetime.now()) + " open_poss()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Open Positions'

	t     = 'Open Positions - Summary - New'
	sql = " "
	sql += "select (select concat('$',' ', round(bal_avail,6)) from cbtrade.bals b where b.symb = 'USDC') as avail "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as fees_val_tot "
	sql += "  , concat('$',' ', x.sell_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_loss_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  and p.pos_stat in ('OPEN','SELL') "
	sql += "  group by p.pos_stat "
	sql += "  order by p.pos_stat "
	sql += "  ) x "
	sql += "order by 1 desc, 2 desc "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Open Positions - Market Summaries - Winners - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as fees_val_tot "
	sql += "  , concat('$',' ', x.sell_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "          and ignore_tf = 0 "
	sql += "          and test_tf = 0 "
	sql += "  and p.pos_stat in ('OPEN','SELL') "
	sql += "  and p.sell_val > p.buy_val "
	sql += "  group by p.prod_id, p.pos_stat "
	sql += "  order by p.prod_id, p.pos_stat "
	sql += "  ) x "
	sql += "order by 16 desc "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)


	t     = 'Open Positions - Current - Winners - New'
	sql = ""
	sql += "select x.pos_id"
	sql += "  , x.prod_id"
#	sql += "  , x.pos_stat"
	sql += "  , x.pos_begin_dttm"
#	sql += "  , x.pos_end_dttm"
#	sql += "  , x.dt"
#	sql += "  , x.age_mins"
	sql += "  , x.age_hours"
	sql += "  , concat('$ ', x.tot_out_cnt) as spend "
#	sql += "  , concat('$ ', x.tot_in_cnt) as recvd "
#	sql += "  , concat('$ ', x.buy_fees_cnt) as buy_fees_cnt "
#	sql += "  , concat('$ ', x.sell_fees_cnt_tot) as sell_fees_cnt_tot "
#	sql += "  , concat('$ ', x.fees_cnt_tot) as fees "
#	sql += "  , x.buy_cnt"
#	sql += "  , x.sell_cnt_tot"
#	sql += "  , x.hold_cnt"
#	sql += "  , x.pocket_cnt"
#	sql += "  , x.clip_cnt"
#	sql += "  , concat(x.pocket_pct, ' %') as pocket_pct "
#	sql += "  , concat(x.clip_pct, ' %') as clip_pct "
#	sql += "  , x.sell_order_cnt "
#	sql += "  , x.sell_order_attempt_cnt "
	sql += "  , concat('$ ', round(x.prc_buy,6)) as prc_buy "
	sql += "  , concat('$ ', round(x.prc_curr,6)) as prc_curr "
	sql += "  , concat('$ ', round(x.prc_high,6)) as prc_high "
#	sql += "  , concat('$ ', round(x.prc_low,6)) as prc_low "
	sql += "  , concat(round(x.prc_chg_pct,2), ' %') as 'prc chg %' "
	sql += "  , concat(round(x.prc_chg_pct_high,2), ' %') as 'prc high %' "
#	sql += "  , concat(round(x.prc_chg_pct_low,2), ' %') as 'prc low %' "
	sql += "  , concat(round(x.prc_chg_pct_drop,2), ' %') as 'prc drop %' "
#	sql += "  , concat('$ ', round(x.prc_sell_avg,6)) as prc_sell_avg "
	sql += "  , concat('$ ', round(x.val_curr,4)) as val_curr "
	sql += "  , concat('$ ', round(x.val_tot,4)) as val_tot "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est,4)) as 'gain est' "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est_high,4)) as 'gain est high' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_est_low,4)) 'gain est low' "
	sql += "  , concat('$ ', round(x.gain_loss_amt,4)) as 'gain' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_net,4)) as 'gain net' "
	sql += "  , concat(round(x.gain_loss_pct_est,3), ' %') as 'gain % est' "
	sql += "  , concat(round(x.gain_loss_pct_est_high,3), ' %') as 'gain % est high' "
#	sql += "  , concat(round(x.gain_loss_pct_est_low,3), ' %') as 'gain % est low' "
	sql += "  , concat(round(x.gain_loss_pct,3), ' %') as 'gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr,8), ' %') as 'hourly gain %' "
#	sql += "  , x.buy_strat_type"
	sql += "  , x.buy_strat_name"
	sql += "  , x.buy_strat_freq"
#	sql += "  , x.sell_strat_type"
#	sql += "  , x.sell_strat_name"
#	sql += "  , x.sell_strat_freq"
#	sql += "  , x.bo_id"
#	sql += "  , x.bo_uuid"
#	sql += "  , x.buy_curr_symb"
#	sql += "  , x.spend_curr_symb"
#	sql += "  , x.sell_curr_symb"
#	sql += "  , x.recv_curr_symb"
#	sql += "  , x.fees_curr_symb"
#	sql += "  , x.test_tf"
	sql += "  from cbtrade.view_pos x "
	sql += "  where x.pos_stat = 'OPEN' "
	sql += "  and x.prc_chg_pct > 0 "
	sql += "  order by x.prod_id, x.pos_id "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)



	t     = 'Open Positions - Current - New'
	sql = ""
	sql += "select x.pos_id"
	sql += "  , x.prod_id"
#	sql += "  , x.pos_stat"
	sql += "  , x.pos_begin_dttm"
#	sql += "  , x.pos_end_dttm"
#	sql += "  , x.dt"
#	sql += "  , x.age_mins"
	sql += "  , x.age_hours"
	sql += "  , concat('$ ', x.tot_out_cnt) as spend "
#	sql += "  , concat('$ ', x.tot_in_cnt) as recvd "
#	sql += "  , concat('$ ', x.buy_fees_cnt) as buy_fees_cnt "
#	sql += "  , concat('$ ', x.sell_fees_cnt_tot) as sell_fees_cnt_tot "
#	sql += "  , concat('$ ', x.fees_cnt_tot) as fees "
#	sql += "  , x.buy_cnt"
#	sql += "  , x.sell_cnt_tot"
#	sql += "  , x.hold_cnt"
#	sql += "  , x.pocket_cnt"
#	sql += "  , x.clip_cnt"
#	sql += "  , concat(x.pocket_pct, ' %') as pocket_pct "
#	sql += "  , concat(x.clip_pct, ' %') as clip_pct "
#	sql += "  , x.sell_order_cnt "
#	sql += "  , x.sell_order_attempt_cnt "
	sql += "  , concat('$ ', round(x.prc_buy,6)) as prc_buy "
	sql += "  , concat('$ ', round(x.prc_curr,6)) as prc_curr "
	sql += "  , concat('$ ', round(x.prc_high,6)) as prc_high "
#	sql += "  , concat('$ ', round(x.prc_low,6)) as prc_low "
	sql += "  , concat(round(x.prc_chg_pct,2), ' %') as 'prc chg %' "
	sql += "  , concat(round(x.prc_chg_pct_high,2), ' %') as 'prc high %' "
#	sql += "  , concat(round(x.prc_chg_pct_low,2), ' %') as 'prc low %' "
	sql += "  , concat(round(x.prc_chg_pct_drop,2), ' %') as 'prc drop %' "
#	sql += "  , concat('$ ', round(x.prc_sell_avg,6)) as prc_sell_avg "
	sql += "  , concat('$ ', round(x.val_curr,4)) as val_curr "
	sql += "  , concat('$ ', round(x.val_tot,4)) as val_tot "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est,4)) as 'gain est' "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est_high,4)) as 'gain est high' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_est_low,4)) 'gain est low' "
	sql += "  , concat('$ ', round(x.gain_loss_amt,4)) as 'gain' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_net,4)) as 'gain net' "
	sql += "  , concat(round(x.gain_loss_pct_est,3), ' %') as 'gain % est' "
	sql += "  , concat(round(x.gain_loss_pct_est_high,3), ' %') as 'gain % est high' "
#	sql += "  , concat(round(x.gain_loss_pct_est_low,3), ' %') as 'gain % est low' "
	sql += "  , concat(round(x.gain_loss_pct,3), ' %') as 'gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr,8), ' %') as 'hourly gain %' "
#	sql += "  , x.buy_strat_type"
	sql += "  , x.buy_strat_name"
	sql += "  , x.buy_strat_freq"
#	sql += "  , x.sell_strat_type"
#	sql += "  , x.sell_strat_name"
#	sql += "  , x.sell_strat_freq"
#	sql += "  , x.bo_id"
#	sql += "  , x.bo_uuid"
#	sql += "  , x.buy_curr_symb"
#	sql += "  , x.spend_curr_symb"
#	sql += "  , x.sell_curr_symb"
#	sql += "  , x.recv_curr_symb"
#	sql += "  , x.fees_curr_symb"
#	sql += "  , x.test_tf"
	sql += "  from cbtrade.view_pos x "
	sql += "  where x.pos_stat = 'OPEN' "
	sql += "  order by x.prod_id, x.pos_id "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)



#	t     = 'Open Positions - Market Summaries - New'
#	sql = " "
#	sql += "select x.prod_id "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as fees_val_tot "
#	sql += "  , concat('$',' ', x.sell_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.prod_id "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.sell_val > p.buy_val then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.sell_val < p.buy_val then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_tot) as fees_val_tot "
#	sql += "  , sum(p.buy_val) as buy_val_tot "
#	sql += "  , sum(p.recv) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  and p.pos_stat in ('OPEN','SELL') "
#	sql += "  group by p.prod_id, p.pos_stat "
#	sql += "  order by p.prod_id, p.pos_stat "
#	sql += "  ) x "
#	sql += "order by 1, 2 desc "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/buys.htm")
@app.route("/buys_recent.htm")
def buys_recent() -> str:
	print(str(datetime.now()) + " buys_recent()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Buys - Recent'

	t     = 'Recent Buys'
	sql = ""
	sql += "select x.pos_id"
	sql += "  , x.prod_id"
	sql += "  , x.pos_stat"
	sql += "  , x.pos_begin_dttm"
#	sql += "  , x.pos_end_dttm"
#	sql += "  , x.dt"
#	sql += "  , x.age_mins"
	sql += "  , x.age_hours"
#	sql += "  , x.buy_strat_type"
	sql += "  , x.buy_strat_name"
	sql += "  , x.buy_strat_freq"
	sql += "  , x.sell_strat_type"
	sql += "  , x.sell_strat_name"
#	sql += "  , x.sell_strat_freq"
	sql += "  , concat('$ ', x.tot_out_cnt) as spend "
#	sql += "  , concat('$ ', x.tot_in_cnt) as recvd "
#	sql += "  , concat('$ ', x.buy_fees_cnt) as buy_fees_cnt "
#	sql += "  , concat('$ ', x.sell_fees_cnt_tot) as sell_fees_cnt_tot "
#	sql += "  , concat('$ ', x.fees_cnt_tot) as fees "
#	sql += "  , x.buy_cnt"
#	sql += "  , x.sell_cnt_tot"
#	sql += "  , x.hold_cnt"
#	sql += "  , x.pocket_cnt"
#	sql += "  , x.clip_cnt"
#	sql += "  , concat(x.pocket_pct, ' %') as pocket_pct "
#	sql += "  , concat(x.clip_pct, ' %') as clip_pct "
#	sql += "  , x.sell_order_cnt "
#	sql += "  , x.sell_order_attempt_cnt "
	sql += "  , concat('$ ', round(x.prc_buy,6)) as prc_buy "
	sql += "  , concat('$ ', round(x.prc_curr,6)) as prc_curr "
	sql += "  , concat('$ ', round(x.prc_high,6)) as prc_high "
#	sql += "  , concat('$ ', round(x.prc_low,6)) as prc_low "
	sql += "  , concat(round(x.prc_chg_pct,2), ' %') as 'prc chg %' "
	sql += "  , concat(round(x.prc_chg_pct_high,2), ' %') as 'prc high %' "
#	sql += "  , concat(round(x.prc_chg_pct_low,2), ' %') as 'prc low %' "
	sql += "  , concat(round(x.prc_chg_pct_drop,2), ' %') as 'prc drop %' "
#	sql += "  , concat('$ ', round(x.prc_sell_avg,6)) as prc_sell_avg "
	sql += "  , concat('$ ', round(x.val_curr,4)) as val_curr "
	sql += "  , concat('$ ', round(x.val_tot,4)) as val_tot "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est,4)) as 'gain est' "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est_high,4)) as 'gain est high' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_est_low,4)) 'gain est low' "
	sql += "  , concat('$ ', round(x.gain_loss_amt,4)) as 'gain' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_net,4)) as 'gain net' "
	sql += "  , concat(round(x.gain_loss_pct_est,3), ' %') as 'gain % est' "
	sql += "  , concat(round(x.gain_loss_pct_est_high,3), ' %') as 'gain % est high' "
#	sql += "  , concat(round(x.gain_loss_pct_est_low,3), ' %') as 'gain % est low' "
	sql += "  , concat(round(x.gain_loss_pct,3), ' %') as 'gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr,8), ' %') as 'hourly gain %' "
#	sql += "  , x.bo_id"
#	sql += "  , x.bo_uuid"
#	sql += "  , x.buy_curr_symb"
#	sql += "  , x.spend_curr_symb"
#	sql += "  , x.sell_curr_symb"
#	sql += "  , x.recv_curr_symb"
#	sql += "  , x.fees_curr_symb"
#	sql += "  , x.test_tf"
	sql += "  from cbtrade.view_pos x "
	sql += "  where 1=1 "
	sql += "  order by x.pos_begin_dttm desc "
	sql += "  limit 50 "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sells.htm")
@app.route("/sells_recent.htm")
def sells_recent() -> str:
	print(str(datetime.now()) + " sells_recent()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Sells - Recent'

	t     = 'Recent Sells'
	sql = ""
	sql += "select x.pos_id"
	sql += "  , x.prod_id"
	sql += "  , x.pos_stat"
#	sql += "  , x.pos_begin_dttm"
	sql += "  , x.pos_end_dttm"
#	sql += "  , x.dt"
#	sql += "  , x.age_mins"
	sql += "  , x.age_hours"
#	sql += "  , x.buy_strat_type"
	sql += "  , x.buy_strat_name"
	sql += "  , x.buy_strat_freq"
	sql += "  , x.sell_strat_type"
	sql += "  , x.sell_strat_name"
#	sql += "  , x.sell_strat_freq"
	sql += "  , concat('$ ', x.tot_out_cnt) as spend "
#	sql += "  , concat('$ ', x.tot_in_cnt) as recvd "
#	sql += "  , concat('$ ', x.buy_fees_cnt) as buy_fees_cnt "
#	sql += "  , concat('$ ', x.sell_fees_cnt_tot) as sell_fees_cnt_tot "
#	sql += "  , concat('$ ', x.fees_cnt_tot) as fees "
#	sql += "  , x.buy_cnt"
#	sql += "  , x.sell_cnt_tot"
#	sql += "  , x.hold_cnt"
#	sql += "  , x.pocket_cnt"
#	sql += "  , x.clip_cnt"
#	sql += "  , concat(x.pocket_pct, ' %') as pocket_pct "
#	sql += "  , concat(x.clip_pct, ' %') as clip_pct "
#	sql += "  , x.sell_order_cnt "
#	sql += "  , x.sell_order_attempt_cnt "
	sql += "  , concat('$ ', round(x.prc_buy,6)) as prc_buy "
	sql += "  , concat('$ ', round(x.prc_curr,6)) as prc_curr "
	sql += "  , concat('$ ', round(x.prc_high,6)) as prc_high "
#	sql += "  , concat('$ ', round(x.prc_low,6)) as prc_low "
	sql += "  , concat(round(x.prc_chg_pct,2), ' %') as 'prc chg %' "
	sql += "  , concat(round(x.prc_chg_pct_high,2), ' %') as 'prc high %' "
#	sql += "  , concat(round(x.prc_chg_pct_low,2), ' %') as 'prc low %' "
	sql += "  , concat(round(x.prc_chg_pct_drop,2), ' %') as 'prc drop %' "
#	sql += "  , concat('$ ', round(x.prc_sell_avg,6)) as prc_sell_avg "
	sql += "  , concat('$ ', round(x.val_curr,4)) as val_curr "
	sql += "  , concat('$ ', round(x.val_tot,4)) as val_tot "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est,4)) as 'gain est' "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est_high,4)) as 'gain est high' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_est_low,4)) 'gain est low' "
	sql += "  , concat('$ ', round(x.gain_loss_amt,4)) as 'gain' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_net,4)) as 'gain net' "
	sql += "  , concat(round(x.gain_loss_pct_est,3), ' %') as 'gain % est' "
	sql += "  , concat(round(x.gain_loss_pct_est_high,3), ' %') as 'gain % est high' "
#	sql += "  , concat(round(x.gain_loss_pct_est_low,3), ' %') as 'gain % est low' "
	sql += "  , concat(round(x.gain_loss_pct,3), ' %') as 'gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr,8), ' %') as 'hourly gain %' "
#	sql += "  , x.bo_id"
#	sql += "  , x.bo_uuid"
#	sql += "  , x.buy_curr_symb"
#	sql += "  , x.spend_curr_symb"
#	sql += "  , x.sell_curr_symb"
#	sql += "  , x.recv_curr_symb"
#	sql += "  , x.fees_curr_symb"
#	sql += "  , x.test_tf"
	sql += "  from cbtrade.view_pos x "
	sql += "  where 1=1 "
	sql += "  order by x.pos_end_dttm desc "
	sql += "  limit 50 "
	h = build_sql_display_old(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/markets.htm")
def markets() -> str:
	print(str(datetime.now()) + " markets()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Markets'

	s = " "
	s += "select x.prod_id "
	s += "  , x.tot_cnt as 'tot#' "
	s += "  , format(floor(x.open_cnt),0) as open "
	s += "  , format(floor(x.close_cnt),0) as close "
	s += "  , format(floor(x.win_cnt),0) as wins "
	s += "  , format(floor(x.lose_cnt),0) as loss "
	s += "  , concat(win_pct, '%') as 'win%' "
	s += "  , concat('$',' ', x.prc) as prc "
	s += "  , concat('$',' ', x.fees_val_tot) as fees_tot "
	s += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	s += "  , concat('$',' ', x.recv_tot) as recv_tot "
	s += "  , concat('$',' ', x.pocket_val_tot) as pocket_tot "
	s += "  , concat('$',' ', x.clip_val_tot) as clip_tot "
	s += "  , concat('$',' ', x.sell_val_tot) as sell_tot "
	s += "  , format(floor(round(x.age_mins / x.tot_cnt)),0) as age_avg "
	s += "  , concat('$',' ', x.gain_amt) as gain_amt "
	s += "  , concat(x.gain_pct, ' %') as gain_pct "
	s += "  , concat(x.gain_pct_hr, ' %') as gain_pct_hr "
	s += "  , concat(x.prc_pct_chg_24h, ' %') as prc_chg_24h "
	s += "  , concat(x.vol_pct_chg_24h, ' %') as vol_chg_24h "
	s += "  , concat('$',' ', x.vol_base_24h) as vol_base_24h "
	s += "  , concat('$',' ', x.vol_quote_24h) as vol_quote_24h "
	s += "  from cbtrade.view_mkt_perf x "
	s += "  where 1=1 "
	s += "  {} "

	t     = 'Products - Winners - Ordered By gain_pct_hr'
	sql = s.format('  and x.sell_val_tot > x.buy_val_tot order by x.gain_pct_hr desc')
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Products - Winners'
	sql = s.format('  and x.sell_val_tot > x.buy_val_tot order by x.prod_id')
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Products - Losers'
	sql = s.format('  and x.sell_val_tot < x.buy_val_tot order by x.prod_id')
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Products - All Traded'
	sql = s.format('order by x.prod_id')
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/market_<mkt>")
def market(mkt) -> str:
	print(str(datetime.now()) + f" market({mkt})")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	mkt = mkt.replace('_','-')

	pt    = f'Market - {mkt}'

#	st    = 'Markets'
#	m, u, d = html_h2_add(t=st, m=m, u=u, d=d)

	s = " "
	s += "select x.prod_id "
	s += "  , x.tot_cnt as 'tot#' "
	s += "  , format(floor(x.open_cnt),0) as open "
	s += "  , format(floor(x.close_cnt),0) as close "
	s += "  , format(floor(x.win_cnt),0) as wins "
	s += "  , format(floor(x.lose_cnt),0) as loss "
	s += "  , concat(win_pct, '%') as 'win%' "
	s += "  , concat('$',' ', x.prc) as prc "
	s += "  , concat('$',' ', x.fees_val_tot) as fees_tot "
	s += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	s += "  , concat('$',' ', x.recv_tot) as recv_tot "
	s += "  , concat('$',' ', x.pocket_val_tot) as pocket_tot "
	s += "  , concat('$',' ', x.clip_val_tot) as clip_tot "
	s += "  , concat('$',' ', x.sell_val_tot) as sell_tot "
	s += "  , format(floor(round(x.age_mins / x.tot_cnt)),0) as age_avg "
	s += "  , concat('$',' ', x.gain_amt) as gain_amt "
	s += "  , concat(x.gain_pct, ' %') as gain_pct "
	s += "  , concat(x.gain_pct_hr, ' %') as gain_pct_hr "
	s += "  , concat(x.prc_pct_chg_24h, ' %') as prc_chg_24h "
	s += "  , concat(x.vol_pct_chg_24h, ' %') as vol_chg_24h "
	s += "  , concat('$',' ', x.vol_base_24h) as vol_base_24h "
	s += "  , concat('$',' ', x.vol_quote_24h) as vol_quote_24h "
	s += "  from cbtrade.view_mkt_perf x "
	s += "  where 1=1 "
	s += "  and x.prod_id = '{}' ".format(mkt)
	s += "  {} "

	t     = 'Products - Winners - Ordered By gain_pct_hr'
	sql = s.format('  and x.sell_val_tot > x.buy_val_tot order by x.gain_pct_hr desc')
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Products - Winners'
	sql = s.format('  and x.sell_val_tot > x.buy_val_tot order by x.prod_id')
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Products - Losers'
	sql = s.format('  and x.sell_val_tot < x.buy_val_tot order by x.prod_id')
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Products - All Traded'
	sql = s.format('order by x.prod_id')
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sales Display - All Trades - New'
	sql = " "
	sql += "select p.pos_id "
	sql += "  , p.prod_id "
	sql += "  , p.pos_stat "
#	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name as buy_strat "
	sql += "  , p.buy_strat_freq as freq "
	sql += "  , p.sell_strat_type  as sell_type "
	sql += "  , p.sell_strat_name as sell_strat "
#	sql += "  , p.sell_strat_freq "
	sql += "  , concat('$', ' ', round(p.prc_buy,2))    as buy_prc "
	sql += "  , concat('$', ' ', round(p.prc_sell,2))   as sell_prc "
	sql += "  , concat('$', ' ', round(p.prc_now,2))    as curr_prc "
	sql += "  , concat('$', ' ', round(p.buy_val,2))    as buy_val "
	sql += "  , concat('$', ' ', round(p.sell_val,2))   as sell_val "
	sql += "  , concat('$', ' ', round(p.recv,2))       as recv_val "
	sql += "  , concat('$', ' ', round(p.hold_val,2))   as hold_val "
	sql += "  , concat('$', ' ', round(p.pocket_val,2)) as pocket_val "
	sql += "  , concat('$', ' ', round(p.clip_val,2))   as clip_val "
	sql += "  , concat('$', ' ', round(p.buy_fees,2))   as buy_fees "
	sql += "  , concat('$', ' ', round(p.sell_fees,2))  as sell_fees "
	sql += "  , concat('$', ' ', round(p.fees_cnt_tot,2))   as fees_tot "
	sql += "  , p.pos_begin_dttm "
	sql += "  , p.pos_end_dttm "
	sql += "  , p.age_mins "
	sql += "  , concat('$', ' ', round(p.gain_amt,2))   as gain_amt "
	sql += "  , concat(p.gain_pct, ' %') as gain_pct "
	sql += "  , concat(p.gain_pct_hr, ' %') as gain_pct_hr "
	sql += "  from cbtrade.view_pos p "
	sql += "  where 1=1 "
#	sql += "  and p.pos_stat in ('CLOSE') "
	sql += "  and p.prod_id = '{}' ".format(mkt)
	sql += "  order by p.pos_end_dttm desc "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/best_strats")
def best_strats() -> str:
	print(str(datetime.now()) + f" best_strats()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None
	pt    = ''
	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/best_markets")
def best_markets() -> str:
	print(str(datetime.now()) + f" best_markets()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None
	pt    = ''
	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/worst_strats")
def worst_strats() -> str:
	print(str(datetime.now()) + f" worst_strats()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None
	pt    = ''
	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/worst_markets")
def worst_markets() -> str:
	print(str(datetime.now()) + f" worst_markets()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None
	pt    = ''
	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

def get_dt_clause(dt1='*', dt2='*') -> str:
	dt_clause = ''
	if dt1 == '*' and dt2 == '*':
		dt_clause = " "
#		print(dt_clause)
	elif dt1 == '*':
		dt_clause  = " and x.dt = str_to_date('{}','%Y-%m-%d')".format(dt2)
#		print(dt_clause)
	else:
		dt_clause   =  ""
		dt_clause   += " and x.dt >= str_to_date('{}','%Y-%m-%d')".format(dt1)
		dt_clause   += " and x.dt <= str_to_date('{}','%Y-%m-%d')".format(dt2)
#		print(dt_clause)
##	print(f'dt_clause : {dt_clause}')
	return dt_clause

#<=====>#

def get_dt_clause2(dt1='*', dt2='*') -> str:
	dt_clause = ''
	if dt1 == '*' and dt2 == '*':
		dt_clause = " "
#		print(dt_clause)
	elif dt1 == '*':
		dt_clause  = " and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt2)
#		print(dt_clause)
	else:
		dt_clause   =  ""
		dt_clause   += " and date(p.pos_end_dttm) >= str_to_date('{}','%Y-%m-%d')".format(dt1)
		dt_clause   += " and date(p.pos_end_dttm) <= str_to_date('{}','%Y-%m-%d')".format(dt2)
#		print(dt_clause)
##	print(f'dt_clause : {dt_clause}')
	return dt_clause

#<=====>#

def sales_disp_summary(prod_id=None, dt1='*', dt2='*') -> str:
	print('')
	print('sales_disp_summary(prod_id={}, dt1={}, dt2={})'.format(prod_id, dt1, dt2))

	dt_clause = get_dt_clause2(dt1, dt2) 

	sql = ""
	sql += "select x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  from (select count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          {} ".format(dt_clause)
	sql += "          ) x "
	sql += "  where 1=1 "
#	print(sql)
	h = build_sql_display(sql,'first')

	return h

#<=====>#

def sales_disp_dt_summary(dt1='*', dt2='*') -> str:
	print('')
	print('sales_disp_dt_summary(dt1={}, dt2={})'.format(dt1, dt2))

	dt_clause = get_dt_clause(dt1, dt2) 

	sql = ""
	sql += "select x.dt "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  from (select date(p.pos_end_dttm) as dt "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          group by date(p.pos_end_dttm) "
	sql += "          ) x "
	sql += "  where 1=1 "
	sql += "  {} ".format(dt_clause)
	sql += "  order by x.dt desc "
#	print(sql)
	h = build_sql_display(sql,'first')

	return h

#<=====>#

def sales_disp_mkt_summary(prod_id=None, dt1='*', dt2='*') -> str:
	print('')
	print('sales_disp_mkt_summary(prod_id={}, dt1={}, dt2={})'.format(prod_id, dt1, dt2))

	dt_clause = get_dt_clause2(dt1, dt2) 

	sql = ""
	sql += "select x.prod_id "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  from (select p.prod_id "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          {} ".format(dt_clause)
	sql += "          group by p.prod_id "
	sql += "          ) x "
	sql += "  where 1=1 "
	sql += "  order by x.prod_id "
#	print(sql)
	h = build_sql_display(sql,'first')

	return h

#<=====>#

def sales_disp_mkt_dt_summary(dt1='*', dt2='*') -> str:
	print('')
	print('sales_disp_mkt_dt_summary(dt1={}, dt2={})'.format(dt1, dt2))

	dt_clause = get_dt_clause(dt1, dt2) 

	sql = ""
	sql += "select x.prod_id "
	sql += "  , x.dt "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  from (select p.prod_id "
	sql += "          , date(p.pos_end_dttm) as dt "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          group by p.prod_id, date(p.pos_end_dttm) "
	sql += "          ) x "
	sql += "  where 1=1 "
	sql += "  {} ".format(dt_clause)
	sql += "  order by x.prod_id, x.dt "
#	print(sql)
	h = build_sql_display(sql,'first')

	return h

#<=====>#

def sales_disp_details(prod_id=None, pos_stat=None, dt1='*', dt2='*') -> str:
	print('')
	print('sales_disp_details(prod_id={}, dt1={}, dt2={})'.format(prod_id, dt1, dt2))

	dt_clause = get_dt_clause(dt1, dt2) 

	sql = ""
	sql += "select x.pos_id"
	sql += "  , x.prod_id"
	sql += "  , x.pos_stat"
#	sql += "  , x.pos_begin_dttm"
	sql += "  , x.pos_end_dttm"
#	sql += "  , x.dt"
#	sql += "  , x.age_mins"
	sql += "  , x.age_hours"
#	sql += "  , x.buy_strat_type"
	sql += "  , x.buy_strat_name"
	sql += "  , x.buy_strat_freq"
	sql += "  , x.sell_strat_type"
	sql += "  , x.sell_strat_name"
#	sql += "  , x.sell_strat_freq"
	sql += "  , concat('$ ', x.tot_out_cnt) as spend "
#	sql += "  , concat('$ ', x.tot_in_cnt) as recvd "
#	sql += "  , concat('$ ', x.buy_fees_cnt) as buy_fees_cnt "
#	sql += "  , concat('$ ', x.sell_fees_cnt_tot) as sell_fees_cnt_tot "
#	sql += "  , concat('$ ', x.fees_cnt_tot) as fees "
#	sql += "  , x.buy_cnt"
#	sql += "  , x.sell_cnt_tot"
#	sql += "  , x.hold_cnt"
#	sql += "  , x.pocket_cnt"
#	sql += "  , x.clip_cnt"
#	sql += "  , concat(x.pocket_pct, ' %') as pocket_pct "
#	sql += "  , concat(x.clip_pct, ' %') as clip_pct "
#	sql += "  , x.sell_order_cnt "
#	sql += "  , x.sell_order_attempt_cnt "
	sql += "  , concat('$ ', round(x.prc_buy,6)) as prc_buy "
	sql += "  , concat('$ ', round(x.prc_curr,6)) as prc_curr "
	sql += "  , concat('$ ', round(x.prc_high,6)) as prc_high "
#	sql += "  , concat('$ ', round(x.prc_low,6)) as prc_low "
	sql += "  , concat(round(x.prc_chg_pct,2), ' %') as 'prc chg %' "
	sql += "  , concat(round(x.prc_chg_pct_high,2), ' %') as 'prc high %' "
#	sql += "  , concat(round(x.prc_chg_pct_low,2), ' %') as 'prc low %' "
	sql += "  , concat(round(x.prc_chg_pct_drop,2), ' %') as 'prc drop %' "
#	sql += "  , concat('$ ', round(x.prc_sell_avg,6)) as prc_sell_avg "
	sql += "  , concat('$ ', round(x.val_curr,4)) as val_curr "
#	sql += "  , concat('$ ', round(x.val_tot,4)) as val_tot "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est,4)) as 'gain est' "
	sql += "  , concat('$ ', round(x.gain_loss_amt_est_high,4)) as 'gain est high' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_est_low,4)) 'gain est low' "
	sql += "  , concat('$ ', round(x.gain_loss_amt,4)) as 'gain' "
#	sql += "  , concat('$ ', round(x.gain_loss_amt_net,4)) as 'gain net' "
	sql += "  , concat(round(x.gain_loss_pct_est,3), ' %') as 'gain % est' "
	sql += "  , concat(round(x.gain_loss_pct_est_high,3), ' %') as 'gain % est high' "
#	sql += "  , concat(round(x.gain_loss_pct_est_low,3), ' %') as 'gain % est low' "
	sql += "  , concat(round(x.gain_loss_pct,3), ' %') as 'gain %' "
	sql += "  , concat(round(x.gain_loss_pct_hr,8), ' %') as 'hourly gain %' "
#	sql += "  , x.bo_id"
#	sql += "  , x.bo_uuid"
#	sql += "  , x.buy_curr_symb"
#	sql += "  , x.spend_curr_symb"
#	sql += "  , x.sell_curr_symb"
#	sql += "  , x.recv_curr_symb"
#	sql += "  , x.fees_curr_symb"
#	sql += "  , x.test_tf"
	sql += "  from cbtrade.view_pos x "
	sql += "  where 1=1 "
	if prod_id:
		sql += "  and x.prod_id = '{}' ".format(prod_id)
	if pos_stat:
		sql += "  and x.pos_stat = '{}' ".format(pos_stat)
	sql += "  {} ".format(dt_clause)
	sql += dt_clause
	sql += "  order by x.pos_end_dttm desc "
#	sql += "  limit 50 "
	h = build_sql_display_old(sql,'first')

	print(sql)
	h = build_sql_display(sql,'first')

	return h

#<=====>#

def sales_disp(dt1, dt2, pt, st) -> str:
	func_str = '{} sales_disp(dt1={}, dt2={}, pt={}, st={})'.format(str(datetime.now()), dt1, dt2, pt, st)
	print(func_str)
#	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Sales Display'

#	t     = 'Sales Display - Daily Summary - New'
#	t     = 'Sales Display - Market Summaries - Dates Combined - New'
#	t     = 'Sales Display - Market Summaries - Date Detailed - New'
#	t     = 'Sales - Details - Date Range'

	t     = 'Sales Summary - For Date Range'
	h = sales_disp_summary(dt1=dt1, dt2=dt2)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sales Summary - Per Date In Date Range'
	h = sales_disp_dt_summary(dt1=dt1, dt2=dt2)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sales Summary - Per Market Dates Combined In Date Range'
	h = sales_disp_mkt_summary(dt1=dt1, dt2=dt2)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sales Summary - Per Market Per Date In Date Range'
	h = sales_disp_mkt_dt_summary(dt1=dt1, dt2=dt2)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sales - Details - Date Range'
	h = sales_disp_details(prod_id=None, pos_stat='CLOSE', dt1=dt1, dt2=dt2)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return sh

#<=====>#

@app.route("/sales.htm")
@app.route("/sales_today.htm")
def sales_today() -> str:
	print(str(datetime.now()) + " sales_today()")
	tn = build_topnav()
	dt = datetime.now(pytz.utc).strftime('%Y-%m-%d')
	pt = 'Sales Summary Today {}'.format(dt)
	st = 'Sales Summary Today {}'.format(dt)
	sh = sales_disp(dt, dt, pt, st)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_yesterday.htm")
def sales_yesterday() -> str:
	print(str(datetime.now()) + " sales_yesterday()")
	tn = build_topnav()
	today = datetime.now(pytz.utc)
	one_day = timedelta(days=1)
	yesterday = today - one_day
	dt = yesterday.strftime('%Y-%m-%d')
	pt = 'Sales Summary - Yesterday - {}'.format(dt)
	st = 'Sales Summary - Yesterday - {}'.format(dt)
	sh = sales_disp(dt, dt, pt, st)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_<day_cnt>d.htm")
def sales_day_cntd(day_cnt) -> str:
	print("{} sales_{}d()".format(str(datetime.now()), day_cnt))
	tn = build_topnav()
	td = datetime.now(pytz.utc)
	days = timedelta(days=int(day_cnt)-1)
	sd = td - days
	dt1 = sd.strftime('%Y-%m-%d')
	dt2 = td.strftime('%Y-%m-%d')
	pt = 'Sales Summary - Last {} Days - {} - {}'.format(day_cnt, dt1, dt2)
	st = 'Sales Summary - Last {} Days - {} - {}'.format(day_cnt, dt1, dt2)
	sh = sales_disp(dt1, dt2, pt, st)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_all.htm")
def sales_all() -> str:
	print("sales_all()")
	tn = build_topnav()
	dt1 = '*'
	dt2 = '*'
	pt = 'Sales Report - All Time'
	st = 'Sales Summary - All Time'
	sh = sales_disp(dt1, dt2, pt, st)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_dt_<dt>")
def sales_dt(dt) -> str:
	print(str(datetime.now()) + " sales_dt()")
	tn = build_topnav()
	pt = 'Sales Report for {}'.format(dt)
	st = 'Sales Report for {}'.format(dt)
	sh = sales_disp(dt, dt, pt, st)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_month_<yr>_<m>")
def sales_month(yr,m) -> str:
	print(str(datetime.now()) + " sales_month()")
	tn = build_topnav()
	yr = int(yr)
	m = int(m)
	if yr < 2019 or yr > 2049:
		yr = date.today.year
	if m < 1 or m > 12:
		m = date.today.month
	dt1 = date(yr, m, 1)
	dt2 = date(yr, m, calendar.monthrange(yr, m)[-1])
	pt = 'Sales Report for {} - {}'.format(dt1, dt2)
	st = 'Sales Report for {} - {}'.format(dt1, dt2)
	sh = sales_disp(dt1, dt2, pt, st)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_year_<yr>")
def sales_yr(yr) -> str:
	print(str(datetime.now()) + " sales_year()")
	tn = build_topnav()
	yr = int(yr)
	if yr < 2019 or yr > 2049:
		yr = date.today.year
	dt1 = date(yr, 1, 1)
	dt2 = date(yr, 12, 31)
	pt = 'Sales Report for Year {}'.format(yr)
	st = 'Sales Report for Year {}'.format(yr)
	sh = sales_disp(dt1, dt2, pt, st)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

def sales_disp_strat_summary(dt1='*', dt2='*') -> str:
	print('')
	print('sales_disp_strat_summary(dt1={}, dt2={})'.format(dt1, dt2))

	dt_clause = get_dt_clause2(dt1, dt2) 
	print(f'dt_clause : {dt_clause}')

	sql = ""
	sql += "select x.buy_strat_type, x.buy_strat_name, x.buy_strat_freq "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          {} ".format(dt_clause)
	sql += "          group by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq "
	sql += "          ) x "
	sql += "  where 1=1 "
	sql += "  order by x.buy_strat_type "
	sql += "      , x.buy_strat_name "
	sql += "      , case  "
	sql += "          when x.buy_strat_freq = '15min' then 1  "
	sql += "          when x.buy_strat_freq = '30min' then 2 "
	sql += "          when x.buy_strat_freq = '1h' then 3 "
	sql += "          when x.buy_strat_freq = '4h' then 4 "
	sql += "          when x.buy_strat_freq = '1d' then 5 "
	sql += "        end "
#	print(sql)
	h = build_sql_display(sql,'first')

	return h

#<=====>#

def sales_disp_strat_mkt_summary(dt1='*', dt2='*') -> str:
	print('')
	print('sales_disp_strat_mkt_summary(dt1={}, dt2={})'.format(dt1, dt2))

	dt_clause = get_dt_clause2(dt1, dt2) 
	print(f'dt_clause : {dt_clause}')

	sql = ""
	sql += "select x.buy_strat_name "
	sql += "  , x.buy_strat_freq "
	sql += "  , x.prod_id "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.buy_strat_name "
	sql += "          , p.buy_strat_freq "
	sql += "          , p.prod_id "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          {} ".format(dt_clause)
	sql += "          group by p.prod_id, p.buy_strat_name, p.buy_strat_freq "
	sql += "          ) x "
	sql += "  where 1=1 "
	sql += "  order by x.buy_strat_name "
	sql += "      , case  "
	sql += "          when x.buy_strat_freq = '15min' then 1  "
	sql += "          when x.buy_strat_freq = '30min' then 2 "
	sql += "          when x.buy_strat_freq = '1h' then 3 "
	sql += "          when x.buy_strat_freq = '4h' then 4 "
	sql += "          when x.buy_strat_freq = '1d' then 5 "
	sql += "        end "
	sql += "      , x.prod_id "
	#	print(sql)
	h = build_sql_display(sql,'first')

	return h

#<=====>#

def sales_disp_mkt_strat_summary(dt1='*', dt2='*') -> str:
	print('')
	print('sales_disp_mkt_strat_summary(dt1={}, dt2={})'.format(dt1, dt2))

	dt_clause = get_dt_clause2(dt1, dt2) 
	print(f'dt_clause : {dt_clause}')

	sql = ""
	sql += "select x.buy_strat_name "
	sql += "  , x.buy_strat_freq "
	sql += "  , x.prod_id "
	sql += "  , x.tot_cnt "
	sql += "  , x.win_cnt "
	sql += "  , x.lose_cnt "
	sql += "  , concat(x.win_pct, ' %') as win_pct "
	sql += "  , concat(x.lose_pct, ' %') as lose_pct "
	sql += "  , x.age_hours "
	sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
	sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
	sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
	sql += "  , concat('$ ', x.val_curr) as val_curr "
	sql += "  , concat('$ ', x.val_tot) as val_tot "
	sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
	sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
	sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
	sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
	sql += "  from (select p.buy_strat_name "
	sql += "          , p.buy_strat_freq "
	sql += "          , p.prod_id "
	sql += "          , count(p.pos_id) as tot_cnt  "
	sql += "          , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "          , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "          , coalesce(round(sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
	sql += "          , coalesce(round(sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
	sql += "          , sum(p.age_mins) as age_mins "
	sql += "          , sum(p.age_mins) / 60 as age_hours "
	sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
	sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
	sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
	sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
	sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
	sql += "          , sum(p.buy_cnt) as buy_cnt "
	sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
	sql += "          , sum(p.hold_cnt) as hold_cnt "
	sql += "          , sum(p.pocket_cnt) as pocket_cnt "
	sql += "          , sum(p.clip_cnt) as clip_cnt "
	sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
	sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
	sql += "          , round(sum(p.val_curr), 2) as val_curr "
	sql += "          , round(sum(p.val_tot), 2) as val_tot "
	sql += "          , round(sum(case when p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
	sql += "          , round(sum(case when p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
	sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
	sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
	sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
	sql += "          , p.test_tf "
	sql += "          from cbtrade.poss p "
	sql += "          where p.ignore_tf = 0 "
	sql += "          {} ".format(dt_clause)
	sql += "          group by p.prod_id, p.buy_strat_name, p.buy_strat_freq "
	sql += "          ) x "
	sql += "  where 1=1 "
	sql += "  order by x.prod_id "
	sql += "      , x.buy_strat_name "
	sql += "      , case  "
	sql += "          when x.buy_strat_freq = '15min' then 1  "
	sql += "          when x.buy_strat_freq = '30min' then 2 "
	sql += "          when x.buy_strat_freq = '1h' then 3 "
	sql += "          when x.buy_strat_freq = '4h' then 4 "
	sql += "          when x.buy_strat_freq = '1d' then 5 "
	sql += "        end "
#	print(sql)
	h = build_sql_display(sql,'first')

	return h

#<=====>#

@app.route("/buy_strats_today.htm")
def buy_strats_today() -> str:
	print(str(datetime.now()) + " buy_strats_today()")
	tn = build_topnav()
	dt = datetime.now(pytz.utc).strftime('%Y-%m-%d')

	m     = None
	u     = None
	d     = None

	pt    = 'Buy Strats Performance'

	t     = 'Buy Strats - Summary - Today'
	h = sales_disp_strat_summary(dt1=dt, dt2=dt)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats - Strat Summary - Today'
	h = sales_disp_strat_mkt_summary(dt1=dt, dt2=dt)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats - Market Summary - Today'
	h = sales_disp_mkt_strat_summary(dt1=dt, dt2=dt)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)



#	t     = 'Buy Strats - Today - Type - New'
#	sql = " "
#	sql += "select x.buy_strat_type "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.buy_strat_type "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
#	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
#	sql += "  , sum(p.tot_in_cnt) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
#	sql += "  group by p.buy_strat_type, p.pos_stat "
#	sql += "  order by p.buy_strat_type, p.pos_stat "
#	sql += "  ) x "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)
#
#	t     = 'Buy Strats - Today  - Type & Name - New'
#	sql = " "
#	sql += "select x.buy_strat_type "
#	sql += "  , x.buy_strat_name "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.buy_strat_type "
#	sql += "  , p.buy_strat_name "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
#	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
#	sql += "  , sum(p.tot_in_cnt) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
#	sql += "  group by p.buy_strat_type, p.buy_strat_name, p.pos_stat "
#	sql += "  order by p.buy_strat_type, p.buy_strat_name, p.pos_stat "
#	sql += "  ) x "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)
#
#	t     = 'Buy Strats - Today  - Type & Name & Freq - New'
#	sql = " "
#	sql += "select x.buy_strat_type "
#	sql += "  , x.buy_strat_name "
#	sql += "  , x.buy_strat_freq "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.buy_strat_type "
#	sql += "  , p.buy_strat_name "
#	sql += "  , p.buy_strat_freq "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
#	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
#	sql += "  , sum(p.tot_in_cnt) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
#	sql += "  group by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat "
#	sql += "  order by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat "
#	sql += "  ) x "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)
#
#	t     = 'Buy Strats & Sell Strats - Today  - Type & Name & Freq - New'
#	sql = " "
#	sql += "select x.buy_strat_type "
#	sql += "  , x.buy_strat_name "
#	sql += "  , x.buy_strat_freq "
#	sql += "  , x.sell_strat_type "
#	sql += "  , x.sell_strat_name "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.buy_strat_type "
#	sql += "  , p.buy_strat_name "
#	sql += "  , p.buy_strat_freq "
#	sql += "  , p.sell_strat_type "
#	sql += "  , p.sell_strat_name "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
#	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
#	sql += "  , sum(p.tot_in_cnt) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
#	sql += "  group by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat, p.sell_strat_type, p.sell_strat_name "
#	sql += "  order by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat, p.sell_strat_type, p.sell_strat_name "
#	sql += "  ) x "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/buy_strats_all.htm")
def buy_strats_all() -> str:
	print(str(datetime.now()) + " buy_strats_all()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Buy Strats Performance'

	t     = 'Buy Strats - Summary - All'
	h = sales_disp_strat_summary(dt1='*', dt2='*')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats - Strat Summary - All'
	h = sales_disp_strat_mkt_summary(dt1='*', dt2='*')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats - Market Summary - All'
	h = sales_disp_mkt_strat_summary(dt1='*', dt2='*')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)




#	t     = 'Buy Strats - All - Type - New'
#	sql = " "
#	sql += "select x.buy_strat_type "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.buy_strat_type "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
#	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
#	sql += "  , sum(p.tot_in_cnt) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  group by p.buy_strat_type, p.pos_stat "
#	sql += "  order by p.buy_strat_type, p.pos_stat "
#	sql += "  ) x "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)
#
#	t     = 'Buy Strats - All - Type & Name - New'
#	sql = " "
#	sql += "select x.buy_strat_type "
#	sql += "  , x.buy_strat_name "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.buy_strat_type "
#	sql += "  , p.buy_strat_name "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
#	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
#	sql += "  , sum(p.tot_in_cnt) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  group by p.buy_strat_type, p.buy_strat_name, p.pos_stat "
#	sql += "  order by p.buy_strat_type, p.buy_strat_name, p.pos_stat "
#	sql += "  ) x "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)
#
#	t     = 'Buy Strats - All - Type & Name & Freq - New'
#	sql = " "
#	sql += "select x.buy_strat_type "
#	sql += "  , x.buy_strat_name "
#	sql += "  , x.buy_strat_freq "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.buy_strat_type "
#	sql += "  , p.buy_strat_name "
#	sql += "  , p.buy_strat_freq "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
#	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
#	sql += "  , sum(p.tot_in_cnt) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  group by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat "
#	sql += "  order by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat "
#	sql += "  ) x "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)
#
#	t     = 'Buy Strats & Sell Strats - All - Type & Name & Freq - New'
#	sql = " "
#	sql += "select x.buy_strat_type "
#	sql += "  , x.buy_strat_name "
#	sql += "  , x.buy_strat_freq "
#	sql += "  , x.sell_strat_type "
#	sql += "  , x.sell_strat_name "
#	sql += "  , x.stat "
#	sql += "  , x.tot_cnt "
#	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
#	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
#	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
#	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
#	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
#	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
#	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
#	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
#	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
#	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
#	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
#	sql += "  from ( "
#	sql += "select p.buy_strat_type "
#	sql += "  , p.buy_strat_name "
#	sql += "  , p.buy_strat_freq "
#	sql += "  , p.sell_strat_type "
#	sql += "  , p.sell_strat_name "
#	sql += "  , p.pos_stat as stat "
#	sql += "  , count(p.pos_id) as tot_cnt "
#	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
#	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
#	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
#	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
#	sql += "  , sum(p.tot_in_cnt) as recv_tot "
#	sql += "  , sum(p.pocket_val) as pocket_val_tot "
#	sql += "  , sum(p.clip_val) as clip_val_tot "
#	sql += "  , sum(p.sell_val) as sell_val_tot "
#	sql += "  , sum(p.age_mins) as age_mins "
#	sql += "  , sum(p.gain_amt) as gain_amt  "
#	sql += "  from view_pos p "
#	sql += "  where 1=1 "
#	sql += "  group by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat, p.sell_strat_type, p.sell_strat_name "
#	sql += "  order by p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat, p.sell_strat_type, p.sell_strat_name "
#	sql += "  ) x "
#	h = build_sql_display(sql,'first')
#	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
#	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/buy_strats_prods_today.htm")
def buy_strats_prods_today() -> str:
	print(str(datetime.now()) + " buy_strats_prods_today()")
	tn = build_topnav()
	dt = datetime.now(pytz.utc).strftime('%Y-%m-%d')

	m     = None
	u     = None
	d     = None

	pt    = 'Buy Strats Performance'

	t     = 'Buy Strats - Today - Type - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "  group by p.prod_id, p.buy_strat_type, p.pos_stat "
	sql += "  order by p.prod_id, p.buy_strat_type, p.pos_stat "
	sql += "  ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats - Today  - Type & Name - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "  group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.pos_stat "
	sql += "  order by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.pos_stat "
	sql += "  ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats - Today  - Type & Name & Freq - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.buy_strat_freq "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name "
	sql += "  , p.buy_strat_freq "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "  group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat "
	sql += "  order by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat "
	sql += "  ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats & Sell Strats - Today  - Type & Name & Freq - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.buy_strat_freq "
	sql += "  , x.sell_strat_type "
	sql += "  , x.sell_strat_name "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name "
	sql += "  , p.buy_strat_freq "
	sql += "  , p.sell_strat_type "
	sql += "  , p.sell_strat_name "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "  group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat, p.sell_strat_type, p.sell_strat_name "
	sql += "  order by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat, p.sell_strat_type, p.sell_strat_name "
	sql += "  ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/buy_strats_prods_all.htm")
def buy_strats_prods_all() -> str:
	print(str(datetime.now()) + " buy_strats_prods_all()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Buy Strats Performance'

	t     = 'Buy Strats - Today - Type - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  group by p.prod_id, p.buy_strat_type, p.pos_stat "
	sql += "  order by p.prod_id, p.buy_strat_type, p.pos_stat "
	sql += "  ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats - Today  - Type & Name - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.pos_stat "
	sql += "  order by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.pos_stat "
	sql += "  ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats - Today  - Type & Name & Freq - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.buy_strat_freq "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name "
	sql += "  , p.buy_strat_freq "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat "
	sql += "  order by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat "
	sql += "  ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Buy Strats & Sell Strats - Today  - Type & Name & Freq - New'
	sql = " "
	sql += "select x.prod_id "
	sql += "  , x.buy_strat_type "
	sql += "  , x.buy_strat_name "
	sql += "  , x.buy_strat_freq "
	sql += "  , x.sell_strat_type "
	sql += "  , x.sell_strat_name "
	sql += "  , x.stat "
	sql += "  , x.tot_cnt "
	sql += "  , format(floor(x.win_cnt),0) as win_cnt "
	sql += "  , format(floor(x.lose_cnt),0) as lose_cnt "
	sql += "  , concat(round(((win_cnt / tot_cnt) * 100), 2), '%') as win_pct "
	sql += "  , concat('$',' ', x.fees_val_tot) as sell_val_tot "
	sql += "  , concat('$',' ', x.buy_val_tot) as buy_val_tot "
	sql += "  , concat('$',' ', x.recv_tot) as recv_tot "
	sql += "  , concat('$',' ', x.pocket_val_tot) as pocket_val_tot "
	sql += "  , concat('$',' ', x.clip_val_tot) as clip_val_tot "
	sql += "  , format(floor(x.age_mins / x.tot_cnt),0) as age_mins_avg "
	sql += "  , concat('$',' ', x.gain_amt) as gain_amt "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100), 2), ' %') as gain_pct "
	sql += "  , concat(round((((sell_val_tot - buy_val_tot) / buy_val_tot) * 100) / (x.age_mins / 60), 8), ' %') as gain_pct_hr "
	sql += "  from ( "
	sql += "select p.prod_id "
	sql += "  , p.buy_strat_type "
	sql += "  , p.buy_strat_name "
	sql += "  , p.buy_strat_freq "
	sql += "  , p.sell_strat_type "
	sql += "  , p.sell_strat_name "
	sql += "  , p.pos_stat as stat "
	sql += "  , count(p.pos_id) as tot_cnt "
	sql += "  , sum(case when p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
	sql += "  , sum(case when p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
	sql += "  , sum(p.fees_cnt_tot) as fees_val_tot "
	sql += "  , sum(p.tot_out_cnt) as buy_val_tot "
	sql += "  , sum(p.tot_in_cnt) as recv_tot "
	sql += "  , sum(p.pocket_val) as pocket_val_tot "
	sql += "  , sum(p.clip_val) as clip_val_tot "
	sql += "  , sum(p.sell_val) as sell_val_tot "
	sql += "  , sum(p.age_mins) as age_mins "
	sql += "  , sum(p.gain_amt) as gain_amt  "
	sql += "  from view_pos p "
	sql += "  where 1=1 "
	sql += "  group by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat, p.sell_strat_type, p.sell_strat_name "
	sql += "  order by p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq, p.pos_stat, p.sell_strat_type, p.sell_strat_name "
	sql += "  ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sell_strats_today.htm")
def sell_strats_today() -> str:
	print(str(datetime.now()) + " sell_strats_today()")
	tn = build_topnav()
	dt = datetime.now(pytz.utc).strftime('%Y-%m-%d')

	m     = None
	u     = None
	d     = None

	pt    = 'Sell Strats Performance'

	t     = 'Sell Strats By Type'
	sql = ""
	sql += "select x.strat "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as strat "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
	sql += "    and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "    group by p.sell_strat_type "
	sql += "    order by p.sell_strat_type "
	sql += "    ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sell Strats By Name'
	sql = ""
	sql += "select x.strat "
	sql += "   , x.strat_name "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as strat "
	sql += "    , p.sell_strat_name as strat_name "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
	sql += "    and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "    group by p.sell_strat_type, p.sell_strat_name "
	sql += "    order by p.sell_strat_type, p.sell_strat_name "
	sql += "    ) x "
	h = build_sql_display(sql,100)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sell Strats vs Buy Strats By Name'
	sql = ""
	sql += "select x.sell_strat "
	sql += "   , x.sell_strat_name "
	sql += "   , x.buy_strat "
	sql += "   , x.buy_strat_name "
	sql += "   , x.stat "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as sell_strat "
	sql += "    , p.sell_strat_name as sell_strat_name "
	sql += "    , p.buy_strat_type  as buy_strat "
	sql += "    , p.buy_strat_name as buy_strat_name "
	sql += "    , p.pos_stat as stat "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
	sql += "    and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "    group by p.buy_strat_type, p.buy_strat_name, p.sell_strat_type, p.sell_strat_name, p.pos_stat "
	sql += "    order by p.pos_stat, p.sell_strat_type, p.sell_strat_name, p.buy_strat_type, p.buy_strat_name "
	sql += "    ) x "
	h = build_sql_display(sql,'third')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sell_strats_prods_today.htm")
def sell_strats_prods_today() -> str:
	print(str(datetime.now()) + " sell_strats_prods_today()")
	tn = build_topnav()
	dt = datetime.now(pytz.utc).strftime('%Y-%m-%d')

	m     = None
	u     = None
	d     = None

	pt    = 'Sell Strats Performance'

	t     = 'Sell Strats By Type'
	sql = ""
	sql += "select x.strat "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as strat "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
	sql += "    and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "    group by p.sell_strat_type "
	sql += "    order by p.sell_strat_type "
	sql += "    ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sell Strats By Name'
	sql = ""
	sql += "select x.strat "
	sql += "   , x.strat_name "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as strat "
	sql += "    , p.sell_strat_name as strat_name "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
	sql += "    and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "    group by p.sell_strat_type, p.sell_strat_name "
	sql += "    order by p.sell_strat_type, p.sell_strat_name "
	sql += "    ) x "
	h = build_sql_display(sql,100)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sell Strats vs Buy Strats By Name'
	sql = ""
	sql += "select x.sell_strat "
	sql += "   , x.sell_strat_name "
	sql += "   , x.buy_strat "
	sql += "   , x.buy_strat_name "
	sql += "   , x.stat "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as sell_strat "
	sql += "    , p.sell_strat_name as sell_strat_name "
	sql += "    , p.buy_strat_type  as buy_strat "
	sql += "    , p.buy_strat_name as buy_strat_name "
	sql += "    , p.pos_stat as stat "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
	sql += "    and date(p.pos_end_dttm) = str_to_date('{}','%Y-%m-%d')".format(dt)
	sql += "    group by p.buy_strat_type, p.buy_strat_name, p.sell_strat_type, p.sell_strat_name, p.pos_stat "
	sql += "    order by p.pos_stat, p.sell_strat_type, p.sell_strat_name, p.buy_strat_type, p.buy_strat_name "
	sql += "    ) x "
	h = build_sql_display(sql,'third')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sell_strats_all.htm")
def sell_strats_all() -> str:
	print(str(datetime.now()) + " sell_strats_all()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Sell Strats Performance'

	t     = 'Sell Strats By Type'
	sql = ""
	sql += "select x.strat "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as strat "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
#	sql += "    where p.pos_stat = 'CLOSE' "
	sql += "    group by p.sell_strat_type "
	sql += "    order by p.sell_strat_type "
	sql += "    ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sell Strats By Name'
	sql = ""
	sql += "select x.strat "
	sql += "   , x.strat_name "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as strat "
	sql += "    , p.sell_strat_name as strat_name "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
#	sql += "    where p.pos_stat = 'CLOSE' "
	sql += "    group by p.sell_strat_type, p.sell_strat_name "
	sql += "    order by p.sell_strat_type, p.sell_strat_name "
	sql += "    ) x "
	h = build_sql_display(sql,100)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sell Strats vs Buy Strats By Name'
	sql = ""
	sql += "select x.sell_strat "
	sql += "   , x.sell_strat_name "
	sql += "   , x.buy_strat "
	sql += "   , x.buy_strat_name "
	sql += "   , x.stat "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as sell_strat "
	sql += "    , p.sell_strat_name as sell_strat_name "
	sql += "    , p.buy_strat_type  as buy_strat "
	sql += "    , p.buy_strat_name as buy_strat_name "
	sql += "    , p.pos_stat as stat "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
#	sql += "    where p.pos_stat = 'CLOSE' "
	sql += "    group by p.buy_strat_type, p.buy_strat_name, p.sell_strat_type, p.sell_strat_name, p.pos_stat "
	sql += "    order by p.pos_stat, p.sell_strat_type, p.sell_strat_name, p.buy_strat_type, p.buy_strat_name "
	sql += "    ) x "
	h = build_sql_display(sql,'third')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sell_strats_prods_all.htm")
def sell_strats_prods_all() -> str:
	print(str(datetime.now()) + " sell_strats_prods_all()")
	tn = build_topnav()

	m     = None
	u     = None
	d     = None

	pt    = 'Sell Strats Performance'

	t     = 'Sell Strats By Type'
	sql = ""
	sql += "select x.strat "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as strat "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
#	sql += "    where p.pos_stat = 'CLOSE' "
	sql += "    group by p.sell_strat_type "
	sql += "    order by p.sell_strat_type "
	sql += "    ) x "
	h = build_sql_display(sql,'first')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sell Strats By Name'
	sql = ""
	sql += "select x.strat "
	sql += "   , x.strat_name "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as strat "
	sql += "    , p.sell_strat_name as strat_name "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
#	sql += "    where p.pos_stat = 'CLOSE' "
	sql += "    group by p.sell_strat_type, p.sell_strat_name "
	sql += "    order by p.sell_strat_type, p.sell_strat_name "
	sql += "    ) x "
	h = build_sql_display(sql,100)
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t     = 'Sell Strats vs Buy Strats By Name'
	sql = ""
	sql += "select x.sell_strat "
	sql += "   , x.sell_strat_name "
	sql += "   , x.buy_strat "
	sql += "   , x.buy_strat_name "
	sql += "   , x.stat "
	sql += "   , x.cnt "
	sql += "   , concat('$',' ', x.spent) as spent "
	sql += "   , concat('$',' ', x.recv) as recv "
	sql += "   , concat('$',' ', x.gain_loss_val_amt) as gain_loss_val_amt "
	sql += "   , concat('$',' ', x.spent_amt_avg) as spent_amt_avg "
	sql += "   , concat('$',' ', x.gain_loss_amt_avg) as gain_loss_amt_avg "
	sql += "   , concat(x.gain_loss_pct_avg, '%') as gain_loss_pct_avg "
	sql += "   , concat(gain_loss_pct, '%') as gain_loss_pct "
	sql += "from ( "
	sql += "  select p.sell_strat_type  as sell_strat "
	sql += "    , p.sell_strat_name as sell_strat_name "
	sql += "    , p.buy_strat_type  as buy_strat "
	sql += "    , p.buy_strat_name as buy_strat_name "
	sql += "    , p.pos_stat as stat "
	sql += "    , count(p.pos_id) as cnt "
	sql += "    , round(sum(p.tot_out_cnt),4) as spent "
	sql += "    , round(sum(p.val_tot),4) as recv "
#	sql += "    , round(sum(p.gain_loss_amt),4) as gain_loss_amt "
	sql += "    , round(sum(p.val_tot) - sum(p.tot_out_cnt),4) as gain_loss_val_amt "
#	sql += "    , round(avg(p.tot_out_cnt),4) as spend_amt_avg "
	sql += "    , round(avg(p.val_tot - p.tot_out_cnt),4) as spent_amt_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id),4) as gain_loss_amt_avg "
	sql += "    , round(((sum(p.val_tot) - sum(p.tot_out_cnt)) / count(p.pos_id) / avg(p.tot_out_cnt)),4) * 100 as gain_loss_pct_avg "
	sql += "    , round((sum(p.val_tot) - sum(p.tot_out_cnt)) / sum(p.tot_out_cnt),4) * 100 as gain_loss_pct "
	sql += "    from cbtrade.poss p "
	sql += "    where p.ignore_tf = 0 "
#	sql += "    where p.pos_stat = 'CLOSE' "
	sql += "    group by p.buy_strat_type, p.buy_strat_name, p.sell_strat_type, p.sell_strat_name, p.pos_stat "
	sql += "    order by p.pos_stat, p.sell_strat_type, p.sell_strat_name, p.buy_strat_type, p.buy_strat_name "
	sql += "    ) x "
	h = build_sql_display(sql,'third')
	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/db_size.htm")
def db_size() -> str:
	print(str(datetime.now()) + " db_size()")
	tn = build_topnav()

	m   = None
	u    = None
	d  = None

	pt = 'MySQL Database'

	st = 'MySQL Health Check'
	m, u, d = html_h2_add(t=st, m=m, u=u, d=d)

	t = 'MySQL DB Size'
	sql = " "
	sql +=  "SELECT x.table_schema as db_name,"
	sql +=  "	sum( data_length + index_length ) / 1024 / 1024 as db_size_mb,"
	sql +=  "	sum( data_free )/ 1024 / 1024 as free_size_mb "
	sql +=  "FROM information_schema.TABLES x "
#	sql +=  "WHERE x.table_schema = 'ctbot2021' "
	sql +=  "GROUP BY x.table_schema "
	h = build_sql_display(sql,'first')

	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	t = 'DB Size with Tables'
	sql = " "
	sql +=  "SELECT x.table_schema as db_name, x.table_name as table_name,"
	sql +=  "	sum( data_length + index_length ) / 1024 / 1024 as db_size_mb,"
	sql +=  "	sum( data_free )/ 1024 / 1024 as free_size_mb "
	sql +=  "FROM information_schema.TABLES x "
#	sql +=  "WHERE x.table_schema = 'ctbot2021' "
	sql +=  "GROUP BY x.table_schema, x.table_name"
	h = build_sql_display(sql,'second')

	m, u, d = html_h3_add(t=t, m=m, u=u, d=d)
	m, u, d = html_add(more=h, m=m, u=u, d=d)

	sh = html_comb(m=m, u=u, d=d)

	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

def main():
	while True:
		try:
			app.run(host='0.0.0.0', debug=True, port=8080)
		except KeyboardInterrupt as e:
			print('{} ==> keyed exit...')
			sys.exit()
		except Exception as e:
			print(dttm_get())
			traceback.print_exc()
			print(type(e))
			print(e)
			print('sleeping 60 then restarting...')
			time.sleep(60)

#<=====>#
# Post Variables
#<=====>#

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=8080)

#<=====>#
