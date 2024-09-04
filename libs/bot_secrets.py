#<=====>#
# Description
#<=====>#


#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Common Modules
#<=====>#
import sys
import os
from pprint import pprint

#<=====>#
# Imports - Download Modules
#<=====>#


#<=====>#
# Imports - Shared Library
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

from cls_settings import Settings
from lib_common                    import *

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_secrets'
log_name      = 'bot_secrets'
lib_verbosity = 1
lib_debug_lvl = 1

#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def test_main(secrets):
	sc = secrets.settings_load()
	pprint(sc)

#<=====>#
# Post Variables
#<=====>#

secrets_template_json = {
	"edited_yn": "N",
	"coinbase": {
	"api_key": "",
	"api_secret": "",
		"portfolio_name": ""
		},
	"chatgpt": {
		"key": ""
		},
	"mysql": {
		"host": "localhost",
		"port": 3306,
		"db": "cbtrade",
		"user": "cbtrade",
		"pw": "cbtrade"
		}
	}

secrets = Settings('settings/secrets.json', secrets_template_json)

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	test_main(secrets)

#<=====>#
