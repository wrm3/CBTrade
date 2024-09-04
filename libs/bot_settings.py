#<=====>#
# Description
#<=====>#


#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Common Modules
#<=====>#

#<=====>#
# Imports - Download Modules
#<=====>#


#<=====>#
# Imports - Shared Library
#<=====>#

from cls_settings import Settings
from pprint import pprint

#<=====>#
# Imports - Local Library
#<=====>#


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_settings'
log_name      = 'bot_settings'
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

def test_main(settings):
	st = settings.settings_load()
	pprint(st)

#<=====>#
# Post Variables
#<=====>#

settings_template_json = {
	"edited_yn": "N",
	"speak_yn": "Y",
	"loop_secs": 15,
	"portfoilio_id": "",
	"stable_coins": ["DAI","GUSD","PAX","PYUSD","USD","USDC","USDT"],
	"spot": {
		"trade_yn": "Y",
		"trade_live_yn": "Y",
		"trade_currs": ["USDC"],
		"mkts": {
			"trade_mkts": [
				"BTC-USDC",
				"ETH-USDC",
				"SOL-USDC"
			],
			"stable_mkts": ["DAI-USDC","GUSD-USDC","PAX-USDC","PYUSD-USDC","USDT-USDC"],
			"err_mkts": ["T-USDC","LIT-USDC"],
			"extra_mkts_watched_yn": "N",
			"extra_mkts_top_bot_perf_yn": "Y",
			"extra_mkts_top_bot_perf_cnt": 8,
			"extra_mkts_top_bot_perf_pct_min": 0,
			"extra_mkts_top_bot_gains_yn": "Y",
			"extra_mkts_top_bot_gains_cnt": 8,
			"extra_mkts_prc_pct_chg_24h_yn": "Y",
			"extra_mkts_prc_pct_chg_24h_cnt": 5,
			"extra_mkts_prc_pct_chg_24h_pct_min": 5,
			"extra_mkts_vol_quote_24h_yn": "N",
			"extra_mkts_vol_quote_24h_cnt": 5,
			"extra_mkts_vol_pct_chg_24h_yn": "N",
			"extra_mkts_vol_pct_chg_24h_cnt": 5
		},
		"buy": {
			"buying_on_yn": "Y",
			"force_all_tests_yn": "Y",
			"show_tests_yn": "N",
			"show_tests_min": 101,
			"save_files_yn": "N",
			"buy_limit_yn": "N",
			"allow_tests_yn": "Y",
			"mkts_open_max": 65,
			"reserve_amt": {
				"***": 0,
				"BTC": 1,
				"ETH": 1,
				"SOL": 1,
				"USDC": 100
				},
			"reserve_addtl_daily_amt": {
				"***": 0,
				"BTC": 0.01,
				"ETH": 0.01,
				"SOL": 0.01,
				"USDC": 10
				},
			"special_prod_ids": [
					"BTC-USDC",
					"ETH-USDC",
					"SOL-USDC",
					"SUI-USDC",
					"XRP-USDC"
					],
			"buy_delay_minutes": {
				"***": 5,
				"BTC-USDC": 3,
				"ETH-USDC": 3,
				"SOL-USDC": 3
			},
			"buy_strat_delay_minutes": {
				"***": 30,
				"BTC-USDC": 15,
				"ETH-USDC": 15,
				"SOL-USDC": 15,
				"15min": 8,
				"30min": 15,
				"1h": 30,
				"4h": 120,
				"1d": 720
			},
			"open_poss_cnt_max": {
				"***": 3,
				"BTC-USDC": 50,
				"ETH-USDC": 50,
				"SOL-USDC": 50
			},
			"strat_open_cnt_max": {
				"***": 1,
				"BTC-USDC": 10,
				"ETH-USDC": 10,
				"SOL-USDC": 10
			},
			"trade_size": {
				"***": 5,
				"BTC-USDC": 20,
				"ETH-USDC": 20,
				"SOL-USDC": 20
			},
			"trade_size_min_mult": {
				"***": 3,
				"BTC-USDC": 5,
				"ETH-USDC": 5,
				"SOL-USDC": 5
			},
			"strats": {
				"sha": {
					"use_yn": "Y",
					"freqs": ["1d","4h","1h","30min","15min"],
					"fast_sha_len1": 8,
					"fast_sha_len2": 8,
					"slow_sha_len1": 13,
					"slow_sha_len2": 13,
					"prod_ids": [],
					"prod_ids_skip": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
					"boost_tests_min": {"***": 31, "15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11}
				},
				"imp_macd": {
					"use_yn": "Y",
					"freqs": ["1d","4h","1h","30min","15min"],
					"per_ma": 34,
					"per_sign": 9,
					"prod_ids": [],
					"prod_ids_skip": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
					"boost_tests_min": {"***": 31, "15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11}
				},
				"emax": {
					"use_yn": "N",
					"freqs": ["1d","4h","1h","30min","15min"],
					"per_fast": 8,
					"per_mid": 13,
					"per_slow": 21,
					"prod_ids": [],
					"prod_ids_skip": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
					"boost_tests_min": {"***": 31, "15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11}
				},
				"bb_bo": {
					"use_yn": "Y",
					"freqs": ["1d","4h","1h","30min","15min"],
					"per": 21,
					"sd": 2.1,
					"prod_ids": [],
					"prod_ids_skip": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
					"boost_tests_min": {"***": 31, "15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11}
				},
				"bb": {
					"use_yn": "Y",
					"freqs": ["1d","4h","1h","30min","15min"],
					"inner_per": 34,
					"inner_sd": 2.3,
					"outer_per": 34,
					"outer_sd": 2.7,
					"prod_ids": [],
					"prod_ids_skip": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
					"boost_tests_min": {"***": 31, "15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11}
				},
				"drop": {
					"use_yn": "Y",
					"freqs": ["1d","4h","1h","30min","15min"],
					"drop_pct": {
						"***": 4,
						"BTC-USDC": 4,
						"ETH-USDC": 4,
						"SOL-USDC": 4
						},
					"prod_ids": ["BTC-USDC","ETH-USDC","SOL-USDC"],
					"prod_ids_skip": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
					"boost_tests_min": {"***": 31, "15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11}
				}
			}
		},
		"sell": {
			"selling_on_yn": "Y",
			"force_all_tests_yn": "Y",
			"show_tests_yn": "N",
			"show_tests_min": 101,
			"save_files_yn": "N",
			"sell_limit_yn": "N",
			"take_profit": {
				"hard_take_profit_yn": "Y",
				"hard_take_profit_pct": 25,
				"trailing_profit_yn": "Y",
				"trailing_profit_trigger_pct": 3
			},
			"stop_loss": {
				"hard_stop_loss_yn": "Y",
				"hard_stop_loss_pct": 7,
				"trailing_stop_loss_yn": "Y",
				"trailing_stop_loss_pct": 7,
				"atr_stop_loss_yn": "N",
				"atr_stop_loss_rfreq": "1d",
				"trailing_atr_stop_loss_yn": "N",
				"trailing_atr_stop_loss_pct": 70,
				"trailing_atr_stop_loss_rfreq": "1d"
			},
			"force_sell_all_yn": "N",
			"force_sell": {
				"prod_ids": [],
				"pos_ids": []
			},
			"never_sell_all_yn": "N",
			"never_sell": {
				"prod_ids": [],
				"pos_ids": []
			},
			"never_sell_loss_all_yn": "N",
			"never_sell_loss": {
				"prod_ids": [],
				"pos_ids": []
			},
			"strats": {
				"sha": {
					"exit_if_profit_yn": "Y",
					"exit_if_profit_pct_min": 3,
					"exit_if_loss_yn": "N",
					"exit_if_loss_pct_max": 3,
					"skip_prod_ids": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5}
				},
				"imp_macd": {
					"exit_if_profit_yn": "Y",
					"exit_if_profit_pct_min": 3,
					"exit_if_loss_yn": "N",
					"exit_if_loss_pct_max": 3,
					"skip_prod_ids": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5}
				},
				"bb_bo": {
					"exit_if_profit_yn": "Y",
					"exit_if_profit_pct_min": 3,
					"exit_if_loss_yn": "N",
					"exit_if_loss_pct_max": 3,
					"skip_prod_ids": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5}
				},
				"bb": {
					"exit_if_profit_yn": "Y",
					"exit_if_profit_pct_min": 3,
					"exit_if_loss_yn": "N",
					"exit_if_loss_pct_max": 3,
					"skip_prod_ids": [],
					"tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5}
				}
			},
			"rainy_day": {
				"pocket_pct": {
					"***": 3,
					"BTC-USDC": 50,
					"ETH-USDC": 50,
					"SOL-USDC": 50
				},
				"clip_pct": {
					"***": 0,
					"BTC-USDC": 5,
					"ETH-USDC": 5,
					"SOL-USDC": 5
				}
			}
		}
	}
}

settings = Settings('settings/settings.json', settings_template_json)

#<=====>#
# Default Run
#<=====>#

if __name__ == "__main__":
	test_main(settings)

#<=====>#

