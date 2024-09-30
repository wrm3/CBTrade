#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
import json
from datetime import datetime as dt
import os
import traceback


#<=====>#
# Variables
#<=====>#
lib_name      = 'cls_settings'

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

class Settings():

	def __init__(self, file_path='settings/settings.json', json_template=None):
		self.file_path = file_path
		self.json_template = {}
		if json_template: self.json_template = json_template
		self.kv = self.settings_load()

	# converts the dictionary recursively to new class AttrDict
	# AttrDict gives the following new way to access the dict
	# st['key_name_1']['key_name_2']
	# this now will also work as above
	# st.key_name_1.key_name_2
	# nothing special just found I could type faster this way
	def AttrDictConv(self, in_dict=None):
		func_name = f'{lib_name}.AttrDictConv(in_dict)'
		out_attr_dict = AttrDict()
		try:
			if in_dict:
				if isinstance(in_dict, dict):
					for k in in_dict:
						v = in_dict[k]
						if isinstance(v, dict):
							v = self.AttrDictConv(v)
						out_attr_dict[k] = v
		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			print(f'in_dict      : {in_dict}')
			exit()

		return out_attr_dict

	#<=====>#

	# if you have an existing AttrDict and need to merge it with
	# another AttrDict or dict, this will update the keys & values
	# from the in_dict
	def AttrDictUpd(self, in_attr_dict=None, in_dict=None):
		func_name = f'{lib_name}.AttrDictUpd(in_attr_dict, in_dict)'

		try:
			if in_attr_dict:
				if isinstance(in_attr_dict, AttrDict):
					out_attr_dict = in_attr_dict
				elif isinstance(in_attr_dict, dict):
					out_attr_dict = self.AttrDictConv(in_dict=in_attr_dict)
			else:
				out_attr_dict = AttrDict()

			if in_dict:
				if isinstance(in_dict, (dict,AttrDict)):
					for k in in_dict:
						v = in_dict[k]
						if isinstance(v, dict):
							v = self.AttrDictConv(v)
						out_attr_dict[k] = v
		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			print(f'in_attr_dict : {in_attr_dict}')
			print(f'in_dict      : {in_dict}')
			print(f'k            : {k} ({type(k)})')
			print(f'v            : {v} ({type(v)})')
			exit()

		return out_attr_dict

	#<=====>#

	def dir_val(self):
		func_name = f'{lib_name}.dir_val()'
		try:
			os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			print(f'error creating {self.file_path} .... ')

	#<=====>#

	# This is settings_json instead of self.settings_json
	# in case the user wants to call the file_write to save 
	# the current settings back to the file
	def file_write(self, settings_json):
		func_name = f'{lib_name}.file_write(settings_json)'
		try:
			self.dir_val()
			with open(self.file_path, "w") as f:
				json.dump(settings_json, f, indent=4)
				f.close()
		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			print(f'error writing {self.file_path} file.... ')

	#<=====>#

	def file_read(self):
		func_name = f'{lib_name}.file_read()'
		try:
			with open(self.file_path) as f:
				st = json.load(f)
				f.close()
				return st

		except (json.decoder.JSONDecodeError):
			bk_name = self.file_path.replace('.json', f"_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}_bk.json")
			os.rename(self.file_path, bk_name)
			self.file_write(self.json_template)
			print(f'The was an error reading your settings file. This is usually a typo error that broke the JSON format ...')
			print(f'Your file settings were backed up to this file : {bk_name} ...')
			print(f'A new {self.file_path} was created, please correct the file before continuing...')
			exit()

		except (IOError):
			self.file_write(self.json_template)
			print(f'The {self.file_path} file was not found...')
			print(f'A new {self.file_path} was created...')
			print(f'Please complete the {self.file_path} before continuing...')
			exit()

	#<=====>#

	def get_ovrd(self, in_dict, in_key, def_val=None):
		func_name = f'{lib_name}.get_ovrd(in_dict, in_key={in_key}, def_val={def_val})'

		try:
			out_val = def_val

			if isinstance(in_dict, (dict, AttrDict)):
				if in_key in in_dict or '***' in in_dict:
					if in_key in in_dict:
						out_val = in_dict[in_key]
					else:
						out_val = in_dict['***']

		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			exit()

		return out_val

	#<=====>#

	def get_ovrd2(self, in_dict, in_key, in_key2, def_val=None):
		func_name = f'{lib_name}.get_ovrd(in_dict, in_key={in_key}, in_key2={in_key2}, def_val={def_val})'

		try:
			out_val = def_val

			if isinstance(in_dict, (dict, AttrDict)):
				if in_key in in_dict or '***' in in_dict:
					if in_key in in_dict:
						out_val = in_dict[in_key]
					else:
						out_val = in_dict['***']

			if isinstance(out_val, (dict, AttrDict)):
				if in_key2 in out_val or '***' in out_val:
					if in_key2 in out_val:
						out_val = out_val[in_key2]
					else:
						out_val = out_val['***']

		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			exit()

		return out_val

	#<=====>#

	def reload(self):
		func_name = f'{lib_name}.reload()'

		try:
			self.kv = self.settings_load()
		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			exit()

		return self.kv

	#<=====>#

	def settings_load(self):
		func_name = f'{lib_name}.settings_load()'

		try:
			self.kv = self.file_read()
			self.kv = self.AttrDictConv(in_dict=self.kv)
		except Exception as e:
			print(f'{func_name} ==> errored... {type(e)} {e}')
			traceback.print_exc()
			traceback.print_stack()
			exit()

		return self.kv

#<=====>#
# Functions
#<=====>#

def test_main():
	pass


#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
