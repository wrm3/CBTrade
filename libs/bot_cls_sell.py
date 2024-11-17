#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_cls_sell'
log_name      = 'bot_cls_sell'
lib_secs_max  = 1

# <=====>#
# Assignments Pre
# <=====>#

from libs.bot_settings import debug_settings_get, get_lib_func_secs_max
dst, debug_settings = debug_settings_get()
lib_secs_max = get_lib_func_secs_max(lib_name=lib_name)


#<=====>#
# Classes
#<=====>#

class POS(AttrDict):

	def __init__(pos, mkt, pair, pos_data, ta, mst, pst):

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
