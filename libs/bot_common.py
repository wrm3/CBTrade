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
import os
from fstrent_tools import AttrDictConv, print_adv, dir_val
from libs.bot_settings import debug_settings_get
from fstrent_colors import cs


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_common'
log_name      = 'bot_common'


# <=====>#
# Assignments Pre
# <=====>#

dst, debug_settings = debug_settings_get()

#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def calc_chg_pct(old_val, new_val, dec_prec=2):
    chg_pct = round((((new_val - old_val) / old_val) * 100), dec_prec)
    return chg_pct

#<=====>#

def freqs_get(rfreq):
    if rfreq == '1d':
        freqs = ['5min', '15min', '30min', '1h', '4h', '1d']
        faster_freqs = ['5min', '15min', '30min', '1h', '4h']
    elif rfreq == '4h':
        freqs = ['5min', '15min', '30min', '1h', '4h']
        faster_freqs = ['5min', '15min', '30min', '1h']
    elif rfreq == '1h':
        freqs = ['5min', '15min', '30min', '1h']
        faster_freqs = ['5min', '15min', '30min']
    elif rfreq == '30min':
        freqs = ['5min', '15min', '30min']
        faster_freqs = ['5min', '15min']
    elif rfreq == '15min':
        freqs = ['5min', '15min']
        faster_freqs = ['5min']

    return freqs, faster_freqs

#<=====>#

def prt_cols(l, cols=10, clr='WoG'):
    col_cnt = 0
    s = ''
    for x in l:
        col_cnt += 1
        if clr == 'WoG':
            s += cs(text=f'{x:<15}', font_color='white', bg_color='green')
        elif clr == 'GoW':
            s += cs(text=f'{x:<15}', font_color='green', bg_color='white')
        if col_cnt % cols == 0:
            print(s)
            s = ''
            col_cnt = 0
        elif col_cnt == len(l):
            s += ''
        else:
            s += ' | '
    if col_cnt > 0 and col_cnt < cols:
        print(s)
        print_adv()


#<=====>#

def writeit(fullfilename, msg):
    dir_val(fullfilename)
    with open(fullfilename, 'a') as fw:
        fw.writelines(msg)
        fw.writelines('\n')
        fw.close()
    return

#<=====>#

def json_load(fname, json_template=None):
    data = json_template

    if not json_template: json_template = {}
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            data = json.load(f)
            data = AttrDictConv(d=data)
    else:
        data = AttrDictConv(d=json_template)
        json_write(data, fname)

    return data

#<=====>#

def json_write(data, fname):
    with open(fname, 'w') as f:
        json.dump(data, f, indent=4)


#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
