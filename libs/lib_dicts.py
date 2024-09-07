#<=====>#
# Import All Scope
#<=====>#
import_all_func_list = []
import_all_func_list.append("AttrDict")
import_all_func_list.append("AttrDictConv")
import_all_func_list.append("AttrDictUpd")
import_all_func_list.append("DictContainsKeys")
import_all_func_list.append("DictKeyValIfElse")
import_all_func_list.append("DictKeyValFill")
import_all_func_list.append("DictKeyVal")
import_all_func_list.append("DictKeyValMult")
import_all_func_list.append("DictKeyDel")
import_all_func_list.append("DictValCheck")
import_all_func_list.append("dec_2_float")
import_all_func_list.append("dict_of_dicts_sort")
__all__ = import_all_func_list

#<=====>#
# Imports - Common Modules
#<=====>#
from datetime            import datetime as dt
from pprint              import pformat
from pprint              import pprint
from termcolor           import colored
from termcolor           import cprint
import beepy
import concurrent.futures
import datetime
import decimal
import errno
import json
import os
import pyttsx3
import sys
import sys, os
import time
import traceback
import winsound

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
lib_name            = 'lib_dicts'
log_name            = 'lib_dicts'

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
# Assignments Post
#<=====>#


#<=====>#
# Default Run
#<=====>#


#<=====>#


