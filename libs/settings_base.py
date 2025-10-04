#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports - Public
#<=====>#
import json
import os
import traceback
import sys
from datetime import datetime as dt, timezone
from fstrent_colors import *

#<=====>#
# Imports - Project
#<=====>#
from libs.common import AttrDict, AttrDictConv, dttm_get, beep, narc
from libs.strat_base import strat_settings_get

#<=====>#
# Variables
#<=====>#
lib_name      = 'settings_base'
log_name      = 'settings_base'

#<=====>#
# Assignments Pre
#<=====>#
debug_tf = False

#<=====>#
# Classes
#<=====>#

class Settings():

    def __init__(self, file_path='settings/settings.json', json_template=None):
        self.debug_tf = debug_tf
        if debug_tf: G(f'==> settings_base.Settings()')
        self.file_path = file_path
        self.json_template = {}
        if json_template: self.json_template = json_template
        try:
            self.kv = self.settings_load()
        except Exception as e:
            print(f"🔴 ERROR: Critical failure initializing Settings for {file_path}: {e}")
            # Use template as final fallback
            self.kv = AttrDictConv(d=self.json_template) if self.json_template else AttrDictConv(d={})

    #<=====>#

    @narc(1)
    def dir_val(self):
        if debug_tf: G(f'==> settings_base.dir_val()')
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        except (PermissionError, OSError, Exception) as e:
            print(f"🔴 ERROR: Unable to create directory for {self.file_path}: {e}")
            beep(3)  # Audio alert for immediate attention
            sys.exit(sys.exit(f'sys.exit from {__name__}'))  # 🔴 TERMINATE: Critical directory creation failure

    #<=====>#

    # This is settings_json instead of self.settings_json
    # in case the user wants to call the file_write to save 
    # the current settings back to the file
    @narc(1)
    def file_write(self, settings_json):
        if debug_tf: G(f'==> settings_base.file_write()')
        try:
            self.dir_val()
            with open(self.file_path, "w") as f:
                json.dump(settings_json, f, indent=4)
                f.close()
        except (PermissionError, OSError, Exception) as e:
            print(f"🔴 ERROR: Unable to write settings file {self.file_path}: {e}")
            beep(3)  # Audio alert for immediate attention
            sys.exit(sys.exit(f'sys.exit from {__name__}'))  # 🔴 TERMINATE: Critical file write failure

    #<=====>#

    @narc(1)
    def file_read(self):
        if debug_tf: G(f'==> settings_base.file_read()')
        try:
            with open(self.file_path) as f:
                st = json.load(f)
                f.close()
                return st
        except (FileNotFoundError, json.JSONDecodeError, PermissionError, Exception) as e:
            # Let the caller handle the exception
            raise e

    #<=====>#

    @narc(1)
    def get_ovrd(self, in_dict, in_key, def_val=None):
        if debug_tf: G(f'==> settings_base.get_ovrd()')

        out_val = def_val

        if isinstance(in_dict, (dict, AttrDict)):
            if in_key in in_dict or '***' in in_dict:
                if in_key in in_dict:
                    out_val = in_dict[in_key]
                else:
                    out_val = in_dict['***']

        return out_val

    #<=====>#

    @narc(1)
    def get_ovrd2(self, in_dict, in_key, in_key2, def_val=None):
        if debug_tf: G(f'==> settings_base.get_ovrd2()')

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

        return out_val

    #<=====>#

    @narc(1)
    def reload(self):
        if debug_tf: G(f'==> settings_base.reload()')
        try:
            self.kv = self.settings_load()
        except Exception as e:
            print(f"🔴 ERROR: Critical failure reloading Settings for {self.file_path}: {e}")
            # Keep existing kv or use template as fallback
            if not self.kv:
                self.kv = AttrDictConv(d=self.json_template) if self.json_template else AttrDictConv(d={})

        return self.kv

    #<=====>#

    @narc(1)
    def settings_load(self):
        if debug_tf: G(f'==> settings_base.settings_load()')
        try:
            self.kv = self.file_read()
            self.kv = AttrDictConv(d=self.kv)
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            # File doesn't exist or is corrupted, use template as fallback
            print(f"⚠️  Settings file {self.file_path} not found or corrupted, using template defaults")
            self.kv = AttrDictConv(d=self.json_template)
            # Write the template to file for future use
            self.file_write(self.json_template)

        return self.kv

#<=====>#
# Functions
#<=====>#

@narc(1)
def get_ovrd_value(in_data, k):
    if debug_tf: G(f'==> settings_base.get_ovrd_value()')
    """Get override value from settings configuration"""
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

@narc(1)
def resolve_settings(st, prod_id):
    if debug_tf: G(f'==> settings_base.resolve_settings()')
    """Resolve settings with product ID overrides"""
    resolved = {}
    for key, value in st.items():
        if isinstance(value, dict | AttrDict):
            resolved[key] = get_ovrd_value(value, prod_id)
        else:
            resolved[key] = value
    return resolved

#<=====>#

@narc(1)
def bot_settings_get(self):
    if debug_tf: G(f'==> settings_base.bot_settings_get()')
    """Get bot settings configuration"""
    bot_json = {
        "edited_yn": "N",
        "loop_secs": 15,
        "auto_loop_secs": 15,
        "speak_yn": "Y",
        "trade_markets": {
            "USDC": {"settings_fpath": "market_usdc.json"},
            "BTC": {"settings_fpath": "market_btc.json"},
            "ETH": {"settings_fpath": "market_eth.json"}
            },
        # 🔴 GILFOYLE'S PERFORMANCE TIMING SYSTEM CONFIGURATION
        "performance_timing_enabled": True,
        "performance_timing_detailed_reports": True,
        "performance_timing_bottleneck_threshold": 30.0
    }

    bot_settings = Settings('settings/bot.json', bot_json)
    bst = bot_settings.settings_load()
    return bst

#<=====>#

@narc(1)
def debug_settings_get(self):
    if debug_tf: G(f'==> settings_base.debug_settings_get()')
    """Get debug settings configuration"""
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
    return dst

#<=====>#
# BOT Instance Settings Methods
#<=====>#

@narc(1)
def mkt_settings_get(self, mkt_symb:str):
    if debug_tf: G(f'==> settings_base.mkt_settings_get()')
    """🔴 MASSIVE USDC MARKET CONFIGURATION - Extracted from cls_bot.py (~260 lines)"""
    # print(f'settings_mkt_get({symb})')
    base_st = {
        "edited_yn": "Y",
        "upd_msg": "These settings are from 2024-10-02 11:15am",
        "trade_yn": "Y",
        "trade_live_yn": "Y",
        "paper_trades_only_yn": "Y",
        "speak_pairs": [],
        "stable_coins": ["DAI","GUSD","PAX","PYUSD","USD","USDC","USDT"],
        "speak_yn": "Y",
        "show_timings_yn": "N",
        "show_upcoming_yn": "N",
        "loop_secs": 15,
        "budget": {
            "max_tot_loss": -250.0,
            "spend_max_amt": 10000.0,
            "spend_up_max_pct": 60.0,
            "spend_dn_max_pct": 60.0,
            "spend_max_pcts": {
                "***": {"spend_up_max_pct":60.0,"spend_dn_max_pct":40.0},
                "BTC-USDC": {"spend_up_max_pct":65.0,"spend_dn_max_pct":65.0},
                "ETH-USDC": {"spend_up_max_pct":65.0,"spend_dn_max_pct":65.0},
                "SOL-USDC": {"spend_up_max_pct":65.0,"spend_dn_max_pct":65.0}
                },
            "spend_pair_max": {
                "***": 300,
                "BTC-USDC": 5000,
                "ETH-USDC": 5000,
                "SOL-USDC": 5000
                },
            "mkt_shares": {
                "shares_or_pcts": "pct",
                "***": 4,
                "BTC-USDC": 50,
                "ETH-USDC": 30,
                "SOL-USDC": 30
                },
            "reserve_amt": 500.0,
            "reserve_addtl_daily_amt": 0
            },
        "pairs": {
            "trade_pairs": [
                "BTC-USDC",
                "ETH-USDC",
                "PAXG-USDC",
                "SOL-USDC"
                ],
            "trade_pairs_bk1": [],
            "trade_pairs_bk2": [],
            "trade_pairs_bk3": [],
            "trade_pairs_bk4": [],
            "stable_pairs": ["DAI-USDC","GUSD-USDC","PAX-USDC","PYUSD-USDC","USDT-USDC"],
            "ban_pairs": [],
            "err_pairs": [],
            "extra_pairs": {
                "watched": {
                    "use_yn": "N"
                    },
                "top_bot_perf": {
                    "use_yn": "Y",
                    "cnt": 7,
                    "pct_min": 0.02
                    },
                "top_bot_gains": {
                    "use_yn": "Y",
                    "cnt": 7,
                    "gain_min": 10
                    },
                "prc_pct_chg_24h": {
                    "use_yn": "Y",
                    "cnt": 5,
                    "pct_min": 3
                    },
                "vol_quote_24h": {
                    "use_yn": "Y",
                    "min_volume": 50000000
                    },
                "vol_pct_chg_24h": {
                    "use_yn": "Y",
                    "cnt": 5
                    }
                }
            },
        "buy_test_txns": {
            "test_txns_on_yn": "Y",
            "test_txns_min": {
                "***": 3,
                "BTC-USDC": 1,
                "ETH-USDC": 1,
                "SOL-USDC": 1
                },
            "test_txns_max": {
                "***": 21,
                "BTC-USDC": 5,
                "ETH-USDC": 5,
                "SOL-USDC": 5
                }
            },
        "buy": {
            "buying_on_yn": "Y",
            "show_tests_yn": "Y",
            "show_boosts_yn": "N",
            "show_tests_min": 50,
            "save_files_yn": "N",
            "buy_limit_yn": "N",
            "mkts_open_max": 1000,
            "trade_strat_perf_recent_cnt": 50,
            "special_prod_ids": ["BTC-USDC","ETH-USDC","SOL-USDC"],
            "buy_delay_minutes": {
                "***": 5,
                "BTC-USDC": 3,
                "ETH-USDC": 3,
                "SOL-USDC": 3
                },
            "buy_strat_delay_minutes": {
                "***": 30,
                "15min": 8,
                "30min": 16,
                "1h": 31,
                "4h": 121,
                "1d": 721
                },
            "open_poss_cnt_max": {
                "***": 15,
                "BTC-USDC": 60,
                "ETH-USDC": 60,
                "SOL-USDC": 60
                },
            "open_test_poss_cnt_max": {
                "***": 60,
                "BTC-USDC": 240,
                "ETH-USDC": 240,
                "SOL-USDC": 240
                },
            "strat_open_cnt_max": {
                "***": 1,
                "BTC-USDC": 3,
                "ETH-USDC": 3,
                "SOL-USDC": 3
                },
            "strat_open_test_cnt_max": {
                "***": 2,
                "BTC-USDC": 5,
                "ETH-USDC": 5,
                "SOL-USDC": 5,
                "IMX-USDC": 3
                },
            "trade_size": {
                "***": 5,
                "BTC-USDC": 25,
                "ETH-USDC": 25,
                "SOL-USDC": 25
                },
            "trade_size_min_mult": {
                "***": 2,
                "BTC-USDC": 10,
                "ETH-USDC": 10,
                "SOL-USDC": 10
                },
            "trade_size_max": {
                "***": 25,
                "BTC-USDC": 400,
                "ETH-USDC": 400,
                "SOL-USDC": 400
                }
            },
        "sell": {
            "selling_on_yn": "Y",
            "show_blocks_yn": "N",
            "show_forces_yn": "N",
            "show_tests_yn": "N",
            "save_files_yn": "N",
            "sell_limit_yn": "N",
            "take_profit": {
                "hard_take_profit_yn": "N",
                "hard_take_profit_pct": 33,
                "hard_take_profit_strats_skip": ["nwe_3row","nwe_env","nwe_rev"],
                "trailing_profit_yn": "Y",
                "trailing_profit_trigger_pct": {
                    "***": 5,
                    "BTC-USDC": 4,
                    "ETH-USDC": 4,
                    "SOL-USDC": 4
                },
                "trailing_profit_strats_skip": [],
                "trailing_profit_levels": {"89":4.50,"55":4.00,"34":3.50,"21":3.00,"13":2.50,"8":2.00,"5":1.00,"3":0.60,"2":0.40,"1":0.20}
            },
            "stop_loss": {
                "hard_stop_loss_yn": "Y",
                "hard_stop_loss_pct": 7,
                "hard_stop_loss_strats_skip": [],
                "trailing_stop_loss_yn": "Y",
                "trailing_stop_loss_pct": 8,
                "trailing_stop_loss_strats_skip": [],
                "nwe_exit_yn": "N",
                "nwe_exit_strats_skip": ["bb","drop","bb_bo","sha","imp_macd","nwe_3row","nwe_env","nwe_rev"],
                "atr_stop_loss_yn": "N",
                "atr_stop_loss_rfreq": "1d",
                "atr_stol_loss_strats_skip": ["nwe_3row","nwe_env","nwe_rev"],
                "trailing_atr_stop_loss_yn": "N",
                "trailing_atr_stop_loss_pct": 70,
                "trailing_atr_stop_loss_rfreq": "1d",
                "trailing_atr_stop_loss_strats_skip": ["nwe_3row","nwe_env","nwe_rev"]
            },
            "force_sell": {
                "all_yn": "N",
                "live_all_yn": "N",
                "prod_ids": [],
                "pos_ids": []
            },
            "never_sell": {
                "all_yn": "N",
                "prod_ids": [],
                "pos_ids": []
            },
            "never_sell_loss": {
                "all_yn": "Y",
                "live_all_yn": "Y",
                "live_max_loss_usd_acceptable": 1,
                "live_prod_ids": ["BTC-USDC","ETH-USDC","SOL-USDC"],
                "prod_ids": [],
                "pos_ids": []
            },
            "profit_saver": {
                "ha_green": {
                    "use_yn": "Y",
                    "prod_ids": [],
                    "skip_prod_ids": [],
                    "sell_strats": [],
                    "skip_sell_strats": ["trail_profit"]
                },
                "nwe_green": {
                    "use_yn":"Y",
                    "prod_ids":[],
                    "skip_prod_ids":[],
                    "sell_strats":[],
                    "skip_sell_strats":["trail_profit"]
                    }
            },
            "rainy_day": {
                "pocket_pct": {"***":20,"BTC-USDC":50,"ETH-USDC":50,"SOL-USDC":50},
                "clip_pct": {"***":0,"BTC-USDC":20,"ETH-USDC":20,"SOL-USDC":20}
            }
        },
        "strats": {},
    }

    if mkt_symb == 'USDC':
        st = base_st

    elif mkt_symb == 'BTC':
        st = base_st

    elif mkt_symb == 'ETH':
        st = base_st
    
    elif mkt_symb == 'SOL':
        st = base_st
    
    else:
        # Default empty settings for unsupported symbols
        print(f"⚠️  WARNING: No specific settings found for symbol '{mkt_symb}', using empty defaults")
        st = {
            "strats": {}  # Required key for strategy functions
        }

    st = self.strat_settings_get(st)

    settings_mkt = Settings(f'settings/market_{mkt_symb.lower()}.json', st)
    st_mkt = settings_mkt.settings_load()
    st_mkt = AttrDict(st_mkt)

    return st_mkt

#<=====>#

# @safe_execute_critical(timing_threshold=15.0)  # 🔴 GILFOYLE: CRITICAL pair settings resolution with market overrides - exit on failure
@narc(1)
def pair_settings_get(self, st_mkt, prod_id):
    if debug_tf: G(f'==> settings_base.pair_settings_get()')
    """Get pair-specific settings by resolving market settings with product ID overrides"""
    prod_id = prod_id.upper()
    st_pair = resolve_settings(st_mkt, prod_id)
    st_pair = AttrDictConv(d=st_pair)
    return st_pair

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
