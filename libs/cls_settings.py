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
import json
import os
import traceback
from datetime import datetime as dt

# Local imports 
from fstrent_tools import AttrDict, AttrDictConv

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

class Settings():

    def __init__(self, file_path='settings/settings.json', json_template=None):
        self.file_path = file_path
        self.json_template = {}
        if json_template: self.json_template = json_template
        self.kv = self.settings_load()

    #<=====>#

    def dir_val(self):
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        except Exception as e:
            traceback.print_exc()
            traceback.print_stack()
            print(f'error creating {self.file_path} .... ')

    #<=====>#

    # This is settings_json instead of self.settings_json
    # in case the user wants to call the file_write to save 
    # the current settings back to the file
    def file_write(self, settings_json):
        try:
            self.dir_val()
            with open(self.file_path, "w") as f:
                json.dump(settings_json, f, indent=4)
                f.close()
        except Exception as e:
            traceback.print_exc()
            traceback.print_stack()
            print(f'error writing {self.file_path} file.... ')

    #<=====>#

    def file_read(self):
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
        try:
            out_val = def_val

            if isinstance(in_dict, (dict, AttrDict)):
                if in_key in in_dict or '***' in in_dict:
                    if in_key in in_dict:
                        out_val = in_dict[in_key]
                    else:
                        out_val = in_dict['***']

        except Exception as e:
            traceback.print_exc()
            traceback.print_stack()
            exit()

        return out_val

    #<=====>#

    def get_ovrd2(self, in_dict, in_key, in_key2, def_val=None):
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
            traceback.print_exc()
            traceback.print_stack()
            exit()

        return out_val

    #<=====>#

    def reload(self):
        try:
            self.kv = self.settings_load()
        except Exception as e:
            traceback.print_exc()
            traceback.print_stack()
            exit()

        return self.kv

    #<=====>#

    def settings_load(self):
        try:
            self.kv = self.file_read()
            self.kv = AttrDictConv(d=self.kv)
        except Exception as e:
            traceback.print_exc()
            traceback.print_stack()
            exit()

        return self.kv

#<=====>#
# Functions
#<=====>#


#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
