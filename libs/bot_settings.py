#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.cls_settings import Settings, AttrDict, AttrDictConv


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_settings'
log_name      = 'bot_settings'


#<=====>#
# Assignments Pre
#<=====>#



#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

def debug_settings_get():
	debug_json = {
		"edited_yn": "N",
		"elapse_max": {
			"***": 0,
			"bot_cls_buy": 1,
			"bot_cls_main": 1,
			"bot_cls_sell": 1
		}
	}

	debug_settings = Settings('settings/debug.json', debug_json)
	dst = debug_settings.settings_load()
	return dst, debug_settings

#<=====>#

def get_lib_func_secs_max(lib_name=None, func_name=None):
	func_str = f'get_lib_func_secs_max(lib_name={lib_name}, func_name={func_name})'
	dst, debug_settings = debug_settings_get()
	if lib_name and func_name:
		lib_secs_max = debug_settings.get_ovrd2(in_dict=dst.elapse_max, in_key=lib_name, in_key2=func_name)
	elif lib_name:
		lib_secs_max = debug_settings.get_ovrd2(in_dict=dst.elapse_max, in_key=lib_name, in_key2=None)
	else:
		lib_secs_max = debug_settings.get_ovrd2(in_dict=dst.elapse_max, in_key=None, in_key2=None)
	return lib_secs_max

#<=====>#

def bot_settings_get():
	bot_json = {
		"edited_yn": "N",
		"loop_secs": 15,
		"auto_loop_secs": 15,
		"speak_yn": "Y",
		"trade_markets": {
			"USDC": {"settings_fpath": "market_usdc.json"},
			"BTC": {"settings_fpath": "market_btc.json"},
			"ETH": {"settings_fpath": "market_eth.json"}
			}
	}

	bot_settings = Settings('settings/bot.json', bot_json)
	bst = bot_settings.settings_load()
	return bst, bot_settings

#<=====>#

def get_ovrd_value(in_data, k):
	if isinstance(in_data, dict | AttrDict):
		if k in in_data:
			return in_data[k]
		elif '***' in in_data:
			return in_data['***']
		else:
			return {key: get_ovrd_value(value, k) for key, value in in_data.items()}
	elif isinstance(in_data, list):
		return [get_ovrd_value(item, k) for item in in_data]
	else:
		return in_data

#<=====>#

def resolve_settings(st, prod_id):
	resolved = {}
	for key, value in st.items():
		if isinstance(value, dict | AttrDict):
			resolved[key] = get_ovrd_value(value, prod_id)
		else:
			resolved[key] = value
	return resolved

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

