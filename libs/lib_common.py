#<=====>#
# Import All Scope
#<=====>#
import_all_func_list = []

import_all_func_list.append("AttrDict")
import_all_func_list.append("AttrDictConv")
import_all_func_list.append("AttrDictUpd")


import_all_func_list.append("format_disp_age")
import_all_func_list.append("format_disp_age2")
import_all_func_list.append("dict_2_obj")
import_all_func_list.append("short_link")

# screen
import_all_func_list.append("clear_screen")

# strings
import_all_func_list.append("lpad")
import_all_func_list.append("rpad")
import_all_func_list.append("cpad")
import_all_func_list.append("left")
import_all_func_list.append("right")
import_all_func_list.append("mid")

# performance timers
import_all_func_list.append("temp_timing_begin")
import_all_func_list.append("temp_timing_end")
import_all_func_list.append("temp_timer_begin")
import_all_func_list.append("temp_timer_end")

# function standards
import_all_func_list.append("func_begin")
import_all_func_list.append("func_end")

# date & time
import_all_func_list.append("calc_elapsed")
import_all_func_list.append("now_utc_get")
import_all_func_list.append("now_utc_ts_get")

# audio queues & sounds
import_all_func_list.append("play_file")
import_all_func_list.append("play_cash")
import_all_func_list.append("play_doh")
import_all_func_list.append("play_thunder")
import_all_func_list.append("play_sw_theme")
import_all_func_list.append("play_sw_imperial_march")
import_all_func_list.append("play_beep")
import_all_func_list.append("beep")
import_all_func_list.append("speak")
import_all_func_list.append("speak_async")

# variable type helpers
import_all_func_list.append("dec_2_float")
import_all_func_list.append("int2tf")
import_all_func_list.append("tf2int")
import_all_func_list.append("dec")
import_all_func_list.append("dec_prec")
import_all_func_list.append("is_odd")
import_all_func_list.append("is_even")
import_all_func_list.append("tf")
import_all_func_list.append("AllHaveVal")
import_all_func_list.append("HasVal")
import_all_func_list.append("IsEnglish")
import_all_func_list.append("getRaw")

# dictionary tools
import_all_func_list.append("dict_of_dicts_sort")
import_all_func_list.append("DictKeyValIfElse")
import_all_func_list.append("DictKeyValFill")
import_all_func_list.append("DictKeyVal")
import_all_func_list.append("DictKeyDel")
import_all_func_list.append("DictKeyValMult")
import_all_func_list.append("DictContainsKeys")
import_all_func_list.append("DictValCheck")
import_all_func_list.append("AllHaveVal")

# printing stuff
import_all_func_list.append("print_adv")
import_all_func_list.append("print_func_name")
import_all_func_list.append("print_line")
import_all_func_list.append("print_obj")
import_all_func_list.append("prt_dttm_get")

# json tools
import_all_func_list.append("json_safe")
import_all_func_list.append("json_file_read")
import_all_func_list.append("json_file_write")

# files and logging
import_all_func_list.append("dir_val")
import_all_func_list.append("file_write")
import_all_func_list.append("logit")
import_all_func_list.append("dttm_get")

__all__ = import_all_func_list

#<=====>#
# Imports - Common Modules
#<=====>#

# from collections         import OrderedDict
from datetime            import datetime as dt
# from glob                import glob
# from importlib           import util
# from math                import ceil
# from math                import floor
# from operator            import itemgetter, getitem
import sys, os
from pprint              import pformat
from pprint              import pprint
from termcolor           import colored
from termcolor           import cprint
# from web3                import Web3
# from web3                import exceptions as w3exceptions
# from web3.middleware     import geth_poa_middleware
# from websockets          import connect as ws_connect
from termcolor           import colored
# import asyncio
import beepy
import datetime
import decimal
import errno
import json
# import logging
# import math
# import numpy as np
import sys
import os
import pyttsx3
# import re
# import requests
import sys
import time
import traceback
# import websockets
import winsound

import concurrent.futures

# from bs4 import BeautifulSoup as bsp
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager

#shared_libs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SHARED_LIBS'))
#if shared_libs_path not in sys.path:
#	sys.path.append(shared_libs_path)

#<=====>#
# Imports - Download Modules
#<=====>#

#<=====>#
# Imports - Unsure if used/needed
#<=====>#

#<=====>#
# Imports - Recently Removed
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


#<=====>#
# Variables
#<=====>#
lib_name            = 'lib_common'
log_name            = 'lib_common'
verbosity           = 1
lib_debug_lvl       = 1
lib_display_lvl     = 1

#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#

class AttrDict(dict):
	def __getattr__(self, item):
		return self[item]
	def __setattr__(self, key, value):
		self[key] = value

#<=====>#

class EmptyObject:
	pass

#<=====>#

#class AttrDict(dict):
#	def __getattr__(self, item):
#		return self[item]
#	def __setattr__(self, key, value):
#		self[key] = value

#<=====>#
# Functions
#<=====>#

class AttrDict(dict):
	def __getattr__(self, item):
		return self[item]
	def __setattr__(self, key, value):
		self[key] = value

#<=====>#
# Functions
#<=====>#

# helpful regexp replace for converting sections of code 
# find: tkn\['(\w+)'\]
# repl: tkn.\1
def AttrDictConv(in_dict=None):
	func_name = 'AttrDictConv'
	out_attr_dict = AttrDict()
	'''
	Returns AttrDict from dict
	If No Dict is provided returns AttrDict
	'''
	try:
		if in_dict:
			if isinstance(in_dict, dict):
				for k in in_dict:
					v = in_dict[k]
					if isinstance(v, dict):
						v = AttrDictConv(v)
					out_attr_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return out_attr_dict

#<=====>#

def AttrDictUpd(in_attr_dict=None, in_dict=None):
	func_name = 'AttrDictUpd'
	if in_attr_dict and isinstance(in_attr_dict, AttrDict):
		out_attr_dict = in_attr_dict
	else:
		out_attr_dict = AttrDict()
	'''
	Returns in AttrDict with new keys added from in_dict
	If No Dict is provided returns AttrDict with keys added from in_dict
	'''
	try:
		if in_dict:
			if isinstance(in_dict, dict):
				for k in in_dict:
					v = in_dict[k]
					if isinstance(v, dict):
						v = AttrDictConv(v)
					out_attr_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return out_attr_dict

#<=====>#

# helpful regexp replace for converting sections of code 
# find: tkn\['(\w+)'\]
# repl: tkn.\1
#def AttrDictConv(in_dict=None):
#	out_attr_dict = AttrDict()
#	'''
#	Returns AttrDict from dict
#	If No Dict is provided returns AttrDict
#	'''
#	try:
#		if in_dict:
#			if isinstance(in_dict, dict):
#				for k in in_dict:
#					v = in_dict[k]
#					if isinstance(v, dict):
#						v = AttrDictConv(v)
#					out_attr_dict[k] = v
#	except Exception as e:
#		print('{} ==> errored... {}'.format(func_name, e))
#		traceback.print_exc()
#		traceback.print_stack()
#		print(type(e))
#		print(e)
#		print('k : {} ({})'.format(k, type(k)))
#		print('v : {} ({})'.format(v, type(v)))
#		print('in_dict : ({})'.format(type(in_dict)))
#		pprint(in_dict)
#		sys.exit()
#	return out_attr_dict

#<=====>#

#def AttrDictUpd(in_attr_dict=None, in_dict=None):
#	if in_attr_dict and isinstance(in_attr_dict, AttrDict):
#		out_attr_dict = in_attr_dict
#	else:
#		out_attr_dict = AttrDict()
#	'''
#	Returns in AttrDict with new keys added from in_dict
#	If No Dict is provided returns AttrDict with keys added from in_dict
#	'''
#	try:
#		if in_dict:
#			if isinstance(in_dict, dict):
#				for k in in_dict:
#					v = in_dict[k]
#					if isinstance(v, dict):
#						v = AttrDictConv(v)
#					out_attr_dict[k] = v
#	except Exception as e:
#		print('{} ==> errored... {}'.format(func_name, e))
#		traceback.print_exc()
#		traceback.print_stack()
#		print(type(e))
#		print(e)
#		print('k : {} ({})'.format(k, type(k)))
#		print('v : {} ({})'.format(v, type(v)))
#		print('in_dict : ({})'.format(type(in_dict)))
#		pprint(in_dict)
#		sys.exit()
#	return out_attr_dict

#<=====>#

def dict_of_dicts_sort(d:dict, k:str, typ='float', rev=False):
	# m = 'dict_of_dicts_sort(d=d, k={}, rev={})'
	# msg =m.format(k, rev)
#	print(msg)
	sorted_d  = {}
	vals_list = []
	pks_list  = []
	for pk in d:
		val = str(d[pk][k])
#		print('dict_of_dicts_sort => Step 1 - pk of all dicts in dict => : {}'.format(val))
		vals_list.append(val)
	sorted_vals_list = sorted(vals_list, reverse=rev)
#	print(sorted_vals_list)
	for val_tgt in sorted_vals_list:
		if typ == 'float': val_tgt = float(val_tgt)
		if typ == 'str': val_tgt = str(val_tgt)
		if typ == 'int': val_tgt = int(val_tgt)
#		print('dict_of_dicts_sort => Step 2 - val_tgt in sorted_vals_list => : {}'.format(val_tgt))
		for pk in d:
#			print('dict_of_dicts_sort => Step 3 - pk in d => : {}'.format(pk))
			val = d[pk][k]
#			print('dict_of_dicts_sort => Step 4 - val in d[pk][k] => : {}'.format(val))
			if val == val_tgt:
#				print('dict_of_dicts_sort => Step 5A - val : {} ({}) == val_tgt : {}  ({})'.format(val, val_tgt, type(val), type(val_tgt)))
				pks_list.append(pk)
#			else:
#				print('dict_of_dicts_sort => Step 5B - val : {} ({}) != val_tgt : {}  ({})'.format(val, type(val), val_tgt, type(val_tgt)))
#	print(pks_list)
	for pk in pks_list:
		sorted_d[pk] = d[pk]
	return sorted_d

	#<=====>#

def format_disp_age(age_mins, fmt_style=1):
	# func_name = 'format_disp_age'
	# func_str = f'{lib_name}.{func_name}(age_mins={age_mins})'

	age_days    = age_mins // (24 * 60)
	age_hours   = (age_mins // 60) % 24
	age_minutes = age_mins % 60

	if fmt_style == 1:	
		if age_mins < 60:
			disp_age = f"{'':>3} {'':>2} {age_minutes:>2}"
		elif age_mins >= 60 and age_mins < 600:
			disp_age = f"{'':>3} {age_hours:>2}:{age_minutes:>02}"
		elif age_mins >= 600 and age_days < 1:
			disp_age = f"{'':>3} {age_hours:>02}:{age_minutes:>02}"
		else:
			disp_age = f"{age_days:>3} {age_hours:02}:{age_minutes:02}"
	elif fmt_style == 2:
		disp_age = ''
		if age_days > 0:
			disp_age += f"{age_days}:"
		if age_hours > 0:
			disp_age += f"{age_hours}:"
		if age_minutes >= 0:
			disp_age += f"{age_minutes}"

	return disp_age

	#<=====>#

def format_disp_age2(in_age_secs):
	in_age_secs = int(in_age_secs)	
	age_days    = in_age_secs // (24 * 60 * 60)
	age_hours   = (in_age_secs // (60 * 60)) % 24
	age_minutes = (in_age_secs // 60) % 60
	age_secs    = in_age_secs % 60

	disp_age = ''
	if age_days > 0:
		disp_age += f"{age_days} "
	if age_hours > 0:
		disp_age += f"{age_hours}:"
	if age_minutes >= 0:
		disp_age += f"{age_minutes}:"
	if age_secs >= 0:
		disp_age += f"{age_secs}"

	return disp_age

#<=====>#

def is_even(number: int) -> bool:
	return number % 2 == 0

#<=====>#

def is_odd(number: int) -> bool:
	return number % 2 != 0

#<=====>#

def dec_2_float(in_data):
	func_name = 'dec_2_float'
	'''
	Cycles Through Dict Keys And Converts decimal.Decimal to float
	'''
	try:
		if isinstance(in_data, decimal.Decimal):
			return float(in_data)
		elif isinstance(in_data, list):
			return [dec_2_float(item) for item in in_data]
		elif isinstance(in_data, dict):
			return {key: dec_2_float(value) for key, value in in_data.items()}
		else:
			return in_data
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('in_data : ({})'.format(type(in_data)))
		pprint(in_data)
		sys.exit()

#<=====>#

def DictKeyValIfElse(in_dict, k, d):
	func_name = 'DictKeyValIfElse'
	'''
	Returns Value If Key Is Present
	Else Returns Default
	'''
	try:
		if k in in_dict:
			v = in_dict[k]
		else:
			v = d
		if not v:
			v = d
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return v

#<=====>#

def DictKeyValFill(in_dict, k, v):
	func_name = 'DictKeyValFill'
	'''
	Builds Key If Absent
	Checks Value of Key
	If No Value, populates with default
	'''
	try:
		if k not in in_dict:
			in_dict[k] = v
		if not DictKeyVal(in_dict, k):
			in_dict[k] = v
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('v : {} ({})'.format(v, type(v)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return in_dict[k]

#<=====>#

def DictKeyVal(in_dict, k):
	func_name = 'DictKeyVal'
	'''
	Returns Boolean if key in in_dict and has value using HaveValue function
	'''
	try:
#		if not isinstance(in_dict, dict):
#			print(func_name)
#			print('k : {} ({})'.format(k, type(k)))
#			print('in_dict : ({})'.format(type(in_dict)))
#			pprint(in_dict)
		resp = False
		if k in in_dict:
			if HasVal(in_dict[k]):
				resp = True
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return resp

#<=====>#

def DictKeyDel(in_dict, k):
	func_name = 'DictKeyDel'
	'''
	Deletes key if in in_dict
	'''
	try:
		if k in in_dict:
			del in_dict[k]
	except Exception as e:
		print('{} ==> errored... {}'.format(func_name, e))
		traceback.print_exc()
		traceback.print_stack()
		print(type(e))
		print(e)
		print('k : {} ({})'.format(k, type(k)))
		print('in_dict : ({})'.format(type(in_dict)))
		pprint(in_dict)
		sys.exit()
	return in_dict

#<=====>#

def DictKeyValMult(in_dict, ks):
	'''
	Returns Boolean if all key in ks return True using DictKeyVal function
	'''
	resp = True
	for k in ks:
		if k not in in_dict:
			resp = False
			break
		elif not DictKeyVal(in_dict, k):
			resp = False
			break
	return resp

#<=====>#

def DictContainsKeys(in_dict={}, ks=[]):
	'''
	Returns Boolean if all keys in ks are keys in in_dict.
	ks - either a single key or list of keys
	DOES NOT check values of those keys, just if keys are present
	'''
#	print('DictContainsKeys(in_dict, ks={})'.format(ks))
#	resp = in_dict.keys() >= ks
#	print(resp)
	s = set(ks)
	resp = s.issubset(in_dict.keys())
	return resp

#<=====>#

def DictValCheck(in_dict={}, ks=[], show_yn='N'):
	'''
	Returns Boolean to verify all values in dict have value using HaveValue function
	ks - allows specified keys to be returned
	'''
	if HasVal(ks):
#		print('DictValCheck(in_dict, ks={}, show_yn={})'.format(ks, show_yn))
		resp = True
		if isinstance(ks, list):
			for k in ks:
				if k in in_dict:
					v = in_dict[k]
					if not HasVal(v):
						if show_yn == 'Y':
							print('{} : {}'.format(k,v))
						resp=False
				else:
					resp = False
					return resp
		elif isinstance(ks, str):
			if ks in in_dict:
				v = in_dict[ks]
				if not HasVal(v):
					if show_yn == 'Y':
						print('{} : {}'.format(ks,v))
					resp=False
			else:
				resp = False
				return resp
	return resp

#<=====>#

def AllHaveVal(vals=None, itemize_yn='N'):
	'''
	Returns Boolean if all vals have value using HaveValue function
	itemize_yn - prints while validating
	'''
	resp = True
	if isinstance(vals, list):
		for x in vals:
			r = HasVal(x)
			if itemize_yn == 'Y':
				print('r : {}, x : {}'.format(r, x))
			if r is False:
				resp = False
	else:
		resp = HasVal(vals)
	return resp

#<=====>#

def HasVal(val=None):
	'''
	Returns Boolean if val has value (is not null or empty)
	I created this after finding a situation where "if val:" was not working as I had thought
	Now I have forgotten which scenario this was needed for and I over use this in this project
	It was definitely something unique like the response to a function from a web3 contract, post data cleanup...
	'''
	if val is None:
		return False
	elif isinstance(val, str) and len(val) > 0:
		return True
	elif isinstance(val, dict) and len(val) > 0:
		return True
	elif isinstance(val, list) and len(val) > 0:
		return True
	elif isinstance(val, tuple) and len(val) > 0:
		return True
	elif val is not None and val != '':
		return True
	else:
		return False

#<=====>#

def IsEnglish(s):
	try:
		s.encode(encoding='utf-8').decode('ascii')
	except UnicodeDecodeError:
		return False
	else:
		return True

#<=====>#

def int2tf(val):
	if val == 1:
		val = True
	else:
		val = 0
	return val

#<=====>#

def tf2int(val):
	if val:
		val = int(1)
	else:
		val = int(0)
	return val

#<=====>#

def dec(val):
	if val is None:
		val = decimal.Decimal(0)
	else:
		val = decimal.Decimal(str(val))
	return val

#<=====>#

#def dec_prec(val, prec=28):
#	# Save the current precision
#	orig_prec = decimal.getcontext().prec
#	# Set the new precision
#	decimal.getcontext().prec = prec
#	# Convert the number to Decimal
#	d = decimal.Decimal(val)
#	# Reset the precision to its original value
#	decimal.getcontext().prec = orig_prec
#	return d

def dec_prec(number, prec=28):
	with decimal.localcontext() as ctx:
		ctx.prec = prec
		d = decimal.Decimal(number)
		pprint(d)
		return d

#<=====>#

#def dec_round(val, digs=0):
#	try:
#		if val is None:
#			val = dec(0)
#			return val
#		val = dec(val)
#		print('val    : {} ({})'.format(val, type(val)))
#		digs = abs(dec(digs)) * -1
#		print('digs   : {} ({})'.format(digs, type(digs)))
#		digits = dec(10) ** digs
#		print('digits : {} ({})'.format(digits, type(digits)))
#		val.quantize(digits)
#		print('val    : {} ({})'.format(val, type(val)))
#	except Exception as e:
#		print('{} ==> errored... {}'.format('dec_round', e))
#		traceback.print_exc()
#		print(type(e))
#		print(e)
#		print('val    : {} ({})'.format(val, type(val)))
#		print('digs   : {} ({})'.format(digs, type(digs)))
#		print('digits : {} ({})'.format(digits, type(digits)))
#		sys.exit()
#
#	return val

#<=====>#

def tf(val):
	if val == 1:
		tf = True
	else:
		tf = False
	return tf

#<=====>#

def lpad(in_str, length, pad_char):
	out_str = in_str.rjust(length, pad_char)
	return out_str

#<=====>#

def rpad(in_str, length, pad_char):
	out_str = in_str.ljust(length, pad_char)
	return out_str

#<=====>#

def cpad(in_str, length, pad_char):
	out_str = in_str.center(length, pad_char)
	return out_str

#<=====>#

def left(in_str, length):
	out_str = in_str[0:length]
	return out_str

#<=====>#

def right(in_str, length):
	out_str = in_str[length*-1:]
	return out_str

#<=====>#

def mid(in_str, start_position, length):
	out_str = in_str[start_position:length+1]
	return out_str

#<=====>#

def dir_val(directory_string):
	"""
	Check if a directory exists. If it doesn't, then create it.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	"""
	if not os.path.exists(os.path.dirname(directory_string)):
		try:
			os.makedirs(os.path.dirname(directory_string))
			print("Successfully created '{}' file directory".format(directory_string))
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

#<=====>#

def file_write(fullfilename, msg):
	# func_name = 'file_write'
	dir_val(fullfilename)
	with open(fullfilename, 'a') as FileWriter:
		if isinstance(msg, str):
			if msg == '':
				FileWriter.writelines('\n')
			else:
				FileWriter.writelines(dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' ==> ' + msg)
		else:
			FileWriter.writelines(str(dt.now()) + ' ')
			FileWriter.writelines('\n')
			FileWriter.write(pformat(msg))
		FileWriter.writelines('\n')
		FileWriter.close()
	return

#<=====>#

def logit(logname, msg):
	dttm_now = dt.now().strftime('%Y_%m_%d')
	logfile = 'logs/' + dttm_now+ '_' + logname + '.log'

	dir_val(logfile)
	with open(logfile, 'a') as LogWriter:
		if isinstance(msg, str):
			if msg == '':
				LogWriter.writelines('\n')
			else:
				LogWriter.writelines(dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' ==> ' + msg)
		else:
			LogWriter.write(pformat(msg))
		LogWriter.writelines('\n')
		LogWriter.close()

	return

#<=====>#

def json_safe(in_data, depth=0):
	depth += 1
	out_data = in_data
#	print('in_data : [{}]   ({})  ===>  {}'.format(depth, type(in_data), in_data))

	if isinstance(in_data, list):
		for x in in_data:
			x = json_safe(x, depth)

	elif isinstance(in_data, dict):
		for x in in_data:
			in_data[x] = json_safe(in_data[x], depth)

	elif isinstance(in_data, decimal.Decimal):
		out_data = float(in_data)

	else:
		out_data = in_data

#	print('depth : {}'.format(depth))

	return out_data

#<=====>#

def json_file_read(directory_string, default_json_content=None):
	"""
	Get the contents of a JSON file. If it doesn't exist,
	create and populate it with specified or default JSON content.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	:param default_json_content: The content to populate a non-existing JSON file with
	:type default_json_content: dict, list
	"""
#	print(directory_string)
	dir_val(directory_string)
	try:
		with open(directory_string) as file:
			file_content = json.load(file)
			file.close()
			return file_content
	except (IOError, json.decoder.JSONDecodeError):
		with open(directory_string, "w") as file:
			if default_json_content is None:
				default_json_content = {}
			json.dump(default_json_content, file, indent=4)
			file.close()
			return default_json_content

#<=====>#

def json_file_write(directory_string, json_content):
	"""
	Get the contents of a JSON file. If it doesn't exist,
	create and populate it with specified or default JSON content.
	:param directory_string: The relative directory string (ex: settings/secrets.json)
	:type directory_string: str
	:param json_content: The content to populate a non-existing JSON file with
	:type json_content: dict
	"""
	dir_val(directory_string)
	with open(directory_string, "w") as file:
		json.dump(json_content, file, indent=4)
		file.close()

#<=====>#

def dict_2_obj(in_dict, i=0):
	out_obj = EmptyObject()
	for k in in_dict:
		v = in_dict[k]
		print('{} => k : {}, v : ({}) {}'.format('    '*i, k, type(v), v))
		if isinstance(v, dict):
			i += 1
			v = dict_2_obj(v)
		setattr(out_obj, k, v)
	return out_obj

#<=====>#

def ObjAttrGet(in_obj={}, attr='', default=None):
	'''
	Returns an attribute value from object if it HasVal else default
	'''
	resp = default
	if hasattr(in_obj, attr):
		v = getattr(in_obj, attr)
		if HasVal(v):
			resp = v
	return resp

#<=====>#

def temp_timing_begin(func_name, logname='', log_yn='Y', min_yn='N'):
	f = {}
	t0              = time.perf_counter()
	strt_dttm       = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	f['func_name']  = func_name
	f['logname']    = logname
	f['log_yn']     = log_yn
	f['min_yn']     = min_yn
	f['t0']         = t0
	f['strt_dttm']  = strt_dttm
	msg = "{:<50} begins at {}".format(func_name, strt_dttm)
	if log_yn == 'Y': logit(logname, msg)
	if min_yn == 'N': print(msg)
	return f

#<=====>#

def temp_timing_end(f):
	t1 = time.perf_counter()
	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t0              = f['t0']
	func_name       = f['func_name']
	logname         = f['logname']
	log_yn          = f['log_yn']
	min_yn          = f['min_yn']
	f['t1']         = t1
	f['end_dttm']   = end_dttm
	secs = round(t1 - t0, 3)
	f['secs']       = secs
	m = "{:<50} completed at {}, taking {:>7.3f} seconds..."
	msg = m.format(func_name, end_dttm, secs)
	if log_yn == 'Y': logit(logname, msg)
	if min_yn != 'Y': print(msg)
	return f

#<=====>#

def temp_timer_begin(nm):
	t = {}
	t['name']  = nm
	t0              = time.perf_counter()
	t['t0']         = t0
	strt_dttm       = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t['strt_dttm']  = strt_dttm
	msg = "{} begins at {}".format(nm, strt_dttm)
	print(msg)
	return t

#<=====>#

def temp_timer_end(t):

	t1 = time.perf_counter()
	t['t1']         = t1

	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t['end_dttm']   = end_dttm

	t0              = t['t0']
	nm              = t['name']

	secs = round(t1 - t0, 3)
	t['secs']       = secs

	m = "{} completed at {}, taking {} seconds..."
	msg = m.format(nm, end_dttm, secs)
	print(msg)

	return t

#<=====>#

def utc_now():
	import datetime
	utc_now = datetime.datetime.now(datetime.UTC)
	return utc_now

#<=====>#

def dttm_get():
	dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return dttm_str

#<=====>#

def dttm_get():
	dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return dttm_str

#<=====>#

def now_utc_get():
	now_utc = dt.now(datetime.timezone.utc)
	return now_utc

#<=====>#

def now_utc_ts_get():
	now_utc_ts = dt.now(datetime.timezone.utc).timestamp()
	return now_utc_ts

#<=====>#

def calc_elapsed(dttm_new, dttm_old, interval='seconds'):
#	print('dttm_new : {} ({})'.format(dttm_new, type(dttm_new)))
#	print('dttm_old : {} ({})'.format(dttm_old, type(dttm_old)))
	if interval == 'seconds':
		elapsed = (dttm_new - dttm_old).total_seconds()
	elif interval == 'minutes':
		elapsed = (dttm_new - dttm_old).total_seconds() / 60
	elif interval == 'hours':
		elapsed = (dttm_new - dttm_old).total_seconds() / (60 * 60)
	elif interval == 'days':
		elapsed = (dttm_new - dttm_old).total_seconds() / (60 * 60 * 24)
	return elapsed

#<=====>#

def getRaw(nbr, dec):
	r = int(nbr * 10 ** dec)
	return r

#<=====>#

def get_now():

#	now = dt.fromtimestamp(time.time())
	now = dt.now().replace(microsecond=0)

	return now

#<=====>#

def dict_upd(d, e, k, v):
	func_name = 'dict_upd'
	func_str = ' * {}.{}(d, e={}, k={}, v={})'.format(lib_name, func_name, e, k, v)
	print(func_str)

	if not e in d: d[e] = {}
	d[e][k] = v

	return d

#<=====>#

def prt_dttm_get():
	prt_dttm    = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	return prt_dttm

#<=====>#

def plogit(logname, epoch, msg=None, printyn='Y', logyn='Y'):

#	print('plogit - begin')

	dttm_now = dt.now().strftime('%Y_%m_%d')
	prt_dttm_now = dt.now().strftime('%Y-%m-%d %H:%M:%S')

	logfile = 'logs/' + dttm_now + '_' + logname + '.log'

	dir_val(logfile)
	with open(logfile, 'a') as LogWriter:
		if isinstance(msg, str):
			if msg == '':
				if printyn == 'Y': print('')
				if logyn == 'Y': LogWriter.writelines('\n')
			else:
				m = '{} ({}) ==> {}'
				fmsg = m.format(prt_dttm_now, epoch, msg)
				if printyn == 'Y': print(fmsg)
				if logyn == 'Y': LogWriter.writelines(fmsg)
		else:
			if printyn == 'Y': print(pformat(msg))
			if logyn == 'Y': LogWriter.write(pformat(msg))
		LogWriter.writelines('\n')
		LogWriter.close()

#	print('plogit - end')

	return

#<=====>#

def file_write(fullfilename, msg):
	# func_name = 'file_write'
	dir_val(fullfilename)
	with open(fullfilename, 'a') as FileWriter:
		if isinstance(msg, str):
			if msg == '':
				FileWriter.writelines('\n')
			else:
				FileWriter.writelines(msg)
		else:
			FileWriter.writelines(str(dt.now()) + ' ')
			FileWriter.writelines('\n')
			FileWriter.write(pformat(msg))
		FileWriter.writelines('\n')
		FileWriter.close()
	return

#<=====>#

def sleep_until(dttm):
	func_name = 'sleep_until'
	func_str = ' * {}.{}(dttm={})'.format(lib_name, func_name, dttm)
	print(func_str)

	cnt = 0

	now = get_now()
	while now <= dttm:
		now = get_now()
		cnt += 1
		time.sleep(1)
#		print(cnt)

#<=====>#

def sleep(sec):
	func_name = 'sleep_until'
	func_str = ' * {}.{}(dttm={})'.format(lib_name, func_name, sec)
	print(func_str)

	time.sleep(sec)

#<=====>#

def print_dict(d, debug_lvl=lib_debug_lvl):
	func_name = 'print_dict'
	func_str = ' * {}.{}(d)'.format(lib_name, func_name)
	fnc = func_begin(func_name, log_name, debug_lvl)

	if debug_lvl >= 1: print(func_str)

	print('')
	print('')
	print(json.dumps(d, indent=4))
	print(d)
	print('')
	print('')

	fnc = func_end(fnc, debug_lvl=lib_debug_lvl)
	return


#<=====>#

def print_obj(obj):
	obj_list = {}
	for attr, value in obj.__dict__.items():
		obj_list[attr] = value
	print(obj_list)

#<=====>#

def beep_old():
	frequency = 2500  # Set Frequency To 2500 Hertz
	duration = 1000  # Set Duration To 1000 ms == 1 second
	winsound.Beep(frequency, duration)

#<=====>#

def beep(reps=1):
	for _ in range(0, reps-1, 1):
		cprint('beep()!!!', 'white', 'on_red')
		cprint('beep()!!!', 'white', 'on_red')
		cprint('beep()!!!', 'white', 'on_red')
#		print('\a', end='', flush=True)
		play_beep(frequency=2500,duration=1000, reps=reps)

#<=====>#

def beep_error():
	beepy.beep(sound='error')

#<=====>#

def play_beep(frequency=1000, duration=1000, reps=1):
	"""
	Used to play a beep sound
	:param frequency: The frequency of the beep
	:type frequency: int
	:param duration: The duration of the beep
	:type duration: int
	"""
	if winsound is None:
		print(f'play_beep(frequnecy={frequency}, duration={duration}, reps={reps}')
		return
	for _ in range(0, reps-1, 1):
		winsound.Beep(frequency, duration)

#<=====>#

def play_sw_theme():
#	print('play_sw_theme()')
	"""
	Used to play the Star Wars theme song
	"""
	if winsound is None:
		print('Sound is off, you are missing SW Theme')
		return
	play_beep(1046, 880)
	play_beep(1567, 880)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1174, 55)
	play_beep(2093, 880)
	time.sleep(0.3)
	play_beep(1567, 600)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1174, 55)
	play_beep(2093, 880)
	time.sleep(0.3)
	play_beep(1567, 600)
	play_beep(1396, 55)
	play_beep(1318, 55)
	play_beep(1396, 55)
	play_beep(1174, 880)

#<=====>#

def play_sw_imperial_march():
	"""
	Used to play the Star Wars Imperial March song
	"""
	if winsound is None:
		print('Sound is off, you are missing SW Imperial March')
		return
	play_beep(440, 500)
	play_beep(440, 500)
	play_beep(440, 500)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 600)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 1000)
	time.sleep(0.2)
	play_beep(659, 500)
	play_beep(659, 500)
	play_beep(659, 500)
	play_beep(698, 375)
	play_beep(523, 150)
	play_beep(415, 600)
	play_beep(349, 375)
	play_beep(523, 150)
	play_beep(440, 1000)

#<=====>#

def play_file(f):
	winsound.PlaySound(f, winsound.SND_FILENAME)

#<=====>#

def play_cash():
	print('play_cash()')
	play_file('sounds/cashreg.wav')

#<=====>#

def play_doh():
	print('play_doh()')
	play_file('sounds/DOH!.WAV')

#<=====>#

def play_thunder():
	print('play_thunder()')
	play_file('sounds/thunder.wav')

#<=====>#

#def speak(tempmessage):
#	print(f'speaking : {tempmessage}...')
#	engine = pyttsx3.init()
#	engine.say(tempmessage)
#	voices = engine.getProperty('voices')
#	engine.setProperty('voice', voices[1].id) #changing index changes voices but ony 0 and 1 are working here
#	engine.setProperty('rate',120)  #120 words per minute
#	engine.setProperty('volume',0.9)
#	engine.runAndWait()

#<=====>#

def speak(tempmessage):
	print(f'speaking : {tempmessage}...')
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[0].id)  # changing index changes voices but only 0 and 1 are working here
	engine.setProperty('rate', 120)  # 120 words per minute
	engine.setProperty('volume', 0.9)
	engine.say(tempmessage)
	engine.runAndWait()

#	voices = engine.getProperty("voices")
#	for voice in voices:
#		print(voice)

#<=====>#

def speak_async(tempmessage):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		future = executor.submit(speak, tempmessage)
		return future

#<=====>#

def func_begin(func_name, func_str, logname, secs_max=0.33):
	# this_func = 'func_begin'
	# this_str = f'{lib_name}.{this_func}(func_name={func_name}, func_str={func_str}, logname={logname}, secs_max={secs_max})'
#	G(this_str)

	fnc = {}
	t0                = time.perf_counter()
	strt_dttm         = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	fnc['func_name']  = func_name
	fnc['func_str']   = func_str
	fnc['logname']    = logname
	fnc['strt_dttm']  = strt_dttm
	fnc['end_dttm']   = None
	fnc['t0']         = t0
	fnc['t1']         = None
	fnc['secs']       = 0
	fnc['secs_max']   = secs_max

	return fnc

#<=====>#

def func_end(fnc):
	# this_func = 'func_end'
	# this_str = f'{lib_name}.{this_func}(fnc)'
#	G(this_str)

	t0              = fnc['t0']
	func_name       = fnc['func_name']
	func_str        = fnc['func_str']
	# logname         = fnc['logname']
	secs_max        = fnc['secs_max']
	strt_dttm       = fnc['strt_dttm']
	end_dttm        = dt.now().strftime('%Y-%m-%d %H:%M:%S')
	t1              = time.perf_counter()
	secs            = round(t1 - t0, 3)
	fnc['t1']       = t1
	fnc['end_dttm'] = end_dttm
	fnc['secs']     = secs

	if secs > secs_max:
		msg = f"{func_name:<35} began at {strt_dttm} completed at {end_dttm}, taking {secs} seconds... max : {secs_max} * {func_str}"
		cprint(msg, 'black', 'on_yellow')

	return fnc

#<=====>#

def short_link(url, display_text):
	# Use the OSC 8 escape sequence to start the hyperlink
	# Then use the ST escape to stop it.
	return(f'\033]8;;{url}\033\\{display_text}\033]8;;\033\\')

#<=====>#

def print_clickable_link(url, display_text):
	# Use the OSC 8 escape sequence to start the hyperlink
	# Then use the ST escape to stop it.
	print(f'\033]8;;{url}\033\\{display_text}\033]8;;\033\\')

#<=====>#

def print_adv(adv=1):
	while adv > 0:
		adv -= 1
		print('')

#<=====>#

def print_func_name(func_name, adv=0, clr='white', bgclr='on_blue'):
	dttm_str = dttm_get()
	if adv > 0: print_adv(adv)
	s = '{}  ===>  {}'.format(dttm_str, func_name)
	cprint(s, clr, bgclr)

#<=====>#

def print_line(char='-', cnt=10, clr='white', bgclr='on_black'):
	s = char * cnt
	cprint(s, clr, bgclr)

#<=====>#

def print_obj(in_obj):
	#https://pythonexamples.org/convert-python-class-object-to-json/
	jsonStr = json.dumps(in_obj.__dict__)
	print(jsonStr)



#<=====>#






#<=====>#

def debug_display_func_name(func_name, debug_show_lvl=0, debug_lvl=lib_debug_lvl):

	if debug_show_lvl <= debug_lvl:
		prt_dttm_now = dt.now().strftime('%Y-%m-%d %H:%M:%S')
		m = '{} ==> {}'
		msg = m.format(prt_dttm_now, func_name)
		print(msg)

	return

#<=====>#

def banner_display(e, msg):

	plogit('pcp', e, '')
	plogit('pcp', e, '')
	m = '#<==|===||====|||=== ({}) - {:<20} ===|||====||===|==>#'
	msg = m.format(e, msg)
	plogit('pcp', e, msg)

	return

#<=====>#

def clear_screen():
	if os.name == 'nt':
		os.system('cls')
#	if os.name == 'posix':
#		os.system('clear')

#<=====>#

def section_header(
	txt
	, l=100
	, clr=''
	, bgclr=''
	, before_ln_adv = 2
	, after_ln_adv = 0
	, show_dttm_yn = 'Y'
	, center_yn = 'N'
	, display_lvl=lib_display_lvl
	, debug_lvl=lib_debug_lvl
	):
	func_name = 'section_header(display_text=' + str(txt) +', clr=' + str(clr) +', bgclr=' + str(bgclr) +', display_lvl=' + str(display_lvl) +', debug_lvl=' + str(debug_lvl) +')'
	if debug_lvl >= 2: print(func_name)

	if center_yn == 'Y': txt = txt.center(l)

	if display_lvl >= 1: 
		if before_ln_adv > 0: pa(before_ln_adv)
#		pb(c='*', l=l, fgclr='blue')

		dttm_str = ''
		if show_dttm_yn == 'Y':
			dttm_str = dt.now().strftime('%Y-%m-%d %H:%M:%S') + ' '

		if clr not in ('grey','red','green','yellow','blue','magenta','cyan','white'): clr = ''

		if bgclr not in ('on_grey','on_red','on_green','on_yellow','on_blue','on_magenta','on_cyan','on_white'): bgclr = ''

		if clr != '' and bgclr != '':
			cprint(dttm_str + txt, clr, bgclr)
		elif clr != '':
			cprint(dttm_str + txt, clr)
		else:
			print(dttm_str + txt)

#		pb(c='*', l=l, fgclr='blue')
		if after_ln_adv > 0: pa(after_ln_adv)

	return

#<=====>#

def pa(r=1):
	cnt = 0
	while cnt < r:
		print('')
		cnt += 1
	return

#<=====>#

def pb(c='*', l=235, fgclr='', bgclr=''):
	txt = c*l
	if fgclr not in ('grey','red','green','yellow','blue','magenta','cyan','white'): fgclr = ''
	if bgclr not in ('on_grey','on_red','on_green','on_yellow','on_blue','on_magenta','on_cyan','on_white'): bgclr = ''
	if fgclr != '' and bgclr != '':
		cprint(txt, fgclr, bgclr)
	elif fgclr != '':
		cprint(txt, fgclr)
	else:
		print(txt)
	return

#<=====>#
# Assignments Post
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#

