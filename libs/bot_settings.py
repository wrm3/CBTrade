#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.cls_settings import Settings


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

def mkt_settings_get(symb):
	symb = symb.upper()
	if symb == 'USDC':
		settings_template_json = {
			"edited_yn": "Y",
			"speak_yn": "Y",
			"loop_secs": 15,
			"portfoilio_id": "2b69eba6-6232-57fa-84cf-578586216e3d",
			"stable_coins": [
				"DAI",
				"GUSD",
				"PAX",
				"PYUSD",
				"USD",
				"USDC",
				"USDT"
			],
			"trade_yn": "Y",
			"trade_live_yn": "Y",
			"budget": {
				"max_tot_loss": -250.0,
				"spend_max_amt": 2100.0,
				"spend_up_max_pct": 50.00,
				"spend_dn_max_pct": 50.00,
				"spend_max_pcts": {
					"***": {
						"spend_up_max_pct": 80,
						"spend_dn_max_pct": 20
					},
					"BTC-USDC": {
						"spend_up_max_pct": 60,
						"spend_dn_max_pct": 40
					},
					"ETH-USDC": {
						"spend_up_max_pct": 60,
						"spend_dn_max_pct": 40
					},
					"SOL-USDC": {
						"spend_up_max_pct": 60,
						"spend_dn_max_pct": 40
					}
				},
				"mkt_shares": {
					"***": 1,
					"BTC-USDC": 20,
					"ETH-USDC": 20,
					"SOL-USDC": 20,
					"SUI-USDC": 3
				},
				"reserve_amt": 100.0,
				"reserve_addtl_daily_amt": 5
			},
			"pairs": {
				"trade_pairs": [
					"BTC-USDC",
					"ETH-USDC",
					"SOL-USDC",
					"SUI-USDC"
				],
				"stable_pairs": [
					"DAI-USDC",
					"GUSD-USDC",
					"PAX-USDC",
					"PYUSD-USDC",
					"USDT-USDC"
				],
				"err_pairs": [
					"DAI-USDC",
					"MATIC-USDC",
					"MKR-USDC"
				],
				"extra_pairs_watched_yn": "N",
				"extra_pairs_top_bot_perf_yn": "Y",
				"extra_pairs_top_bot_perf_cnt": 10,
				"extra_pairs_top_bot_perf_pct_min": 0.1,
				"extra_pairs_top_bot_gains_yn": "Y",
				"extra_pairs_top_bot_gains_cnt": 20,
				"extra_pairs_prc_pct_chg_24h_yn": "Y",
				"extra_pairs_prc_pct_chg_24h_cnt": 5,
				"extra_pairs_prc_pct_chg_24h_pct_min": 3,
				"extra_pairs_vol_quote_24h_yn": "N",
				"extra_pairs_vol_quote_24h_cnt": 3,
				"extra_pairs_vol_pct_chg_24h_yn": "N",
				"extra_pairs_vol_pct_chg_24h_cnt": 3
			},
			"buy": {
				"buying_on_yn": "Y",
				"force_all_tests_yn": "Y",
				"show_tests_yn": "N",
				"show_tests_min": 101,
				"save_files_yn": "N",
				"buy_limit_yn": "N",
				"show_boosts_yn": "N",
				"allow_tests_yn": "N",
				"mkts_open_max": 100,
				"special_prod_ids": [
					"BTC-USDC",
					"ETH-USDC",
					"SOL-USDC",
					"SUI-USDC"
				],
				"buy_delay_minutes": {
					"***": 5,
					"BTC-USDC": 1,
					"ETH-USDC": 1,
					"SOL-USDC": 1
				},
				"buy_strat_delay_minutes": {
					"15min": 8,
					"30min": 15,
					"1h": 30,
					"4h": 120,
					"1d": 720
				},
				"open_poss_cnt_max": {
					"***": 5,
					"BTC-USDC": 40,
					"ETH-USDC": 40,
					"SOL-USDC": 40
				},
				"strat_open_cnt_max": {
					"***": 1,
					"BTC-USDC": 5,
					"ETH-USDC": 5,
					"SOL-USDC": 5
				},
				"trade_size": {
					"***": 10,
					"BTC-USDC": 50,
					"ETH-USDC": 50,
					"SOL-USDC": 50
				},
				"trade_size_min_mult": {
					"***": 5,
					"BTC-USDC": 20,
					"ETH-USDC": 20,
					"SOL-USDC": 20
				},
				"strats": {
					"sha": {
						"use_yn": "Y",
						"freqs": [
							"1d",
							"4h",
							"1h",
							"30min",
							"15min"
						],
						"fast_sha_len1": 8,
						"fast_sha_len2": 8,
						"slow_sha_len1": 13,
						"slow_sha_len2": 13,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"imp_macd": {
						"use_yn": "Y",
						"freqs": [
							"1d",
							"4h",
							"1h",
							"30min",
							"15min"
						],
						"per_ma": 34,
						"per_sign": 9,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"emax": {
						"use_yn": "N",
						"freqs": [
							"1d",
							"4h",
							"1h",
							"30min",
							"15min"
						],
						"per_fast": 8,
						"per_mid": 13,
						"per_slow": 21,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"bb_bo": {
						"use_yn": "Y",
						"freqs": [
							"1d",
							"4h",
							"1h",
							"30min",
							"15min"
						],
						"per": 21,
						"sd": 2.1,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"bb": {
						"use_yn": "Y",
						"freqs": [
							"1d",
							"4h",
							"1h",
							"30min",
							"15min"
						],
						"inner_per": 34,
						"inner_sd": 2.3,
						"outer_per": 34,
						"outer_sd": 2.7,
						"prod_ids": [],
						"prod_ids_skip": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					},
					"drop": {
						"use_yn": "Y",
						"freqs": [
							"1d",
							"4h",
							"1h",
							"30min",
							"15min"
						],
						"drop_pct": {
							"***": 4,
							"BTC-USDC": 4,
							"ETH-USDC": 4,
							"SOL-USDC": 4
						},
						"prod_ids": [
							"BTC-USDC",
							"ETH-USDC",
							"SOL-USDC"
						],
						"prod_ids_skip": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						},
						"boost_tests_min": {
							"15min": 27,
							"30min": 23,
							"1h": 19,
							"4h": 15,
							"1d": 11
						}
					}
				}
			},
			"sell": {
				"selling_on_yn": "Y",
				"force_all_tests_yn": "Y",
				"show_blocks_yn": "N",
				"show_forces_yn": "Y",
				"show_tests_yn": "N",
				"show_tests_min": 101,
				"save_files_yn": "N",
				"sell_limit_yn": "N",
				"take_profit": {
					"hard_take_profit_yn": "Y",
					"hard_take_profit_pct": 100,
					"trailing_profit_yn": "Y",
					"trailing_profit_trigger_pct": 3
				},
				"stop_loss": {
					"hard_stop_loss_yn": "Y",
					"hard_stop_loss_pct": 11,
					"trailing_stop_loss_yn": "N",
					"trailing_stop_loss_pct": 10,
					"atr_stop_loss_yn": "N",
					"atr_stop_loss_rfreq": "1d",
					"trailing_atr_stop_loss_yn": "N",
					"trailing_atr_stop_loss_pct": 70,
					"trailing_atr_stop_loss_rfreq": "1d"
				},
				"force_sell_all_yn": "N",
				"force_sell": {
					"prod_ids": [
						"CBETH-USDC",
						"LSETH-USDC",
						"MSOL-USDC",
						"WAMPL-USDC",
						"WAXL-USDC",
						"WBTC-USDC",
						"WCFG-USDC",
						"MATIC-USDC"
					],
					"pos_ids": [
						2741,
						3044
					]
				},
				"never_sell_all_yn": "N",
				"never_sell": {
					"prod_ids": [],
					"pos_ids": []
				},
				"never_sell_loss_all_yn": "Y",
				"never_sell_loss": {
					"prod_ids": [
						"BTC-USDC",
						"ETH-USDC",
						"SOL-USDC"
					],
					"pos_ids": []
				},
				"strats": {
					"sha": {
						"exit_if_profit_yn": "Y",
						"exit_if_profit_pct_min": 1,
						"exit_if_loss_yn": "N",
						"exit_if_loss_pct_max": 3,
						"skip_prod_ids": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						}
					},
					"imp_macd": {
						"exit_if_profit_yn": "Y",
						"exit_if_profit_pct_min": 1,
						"exit_if_loss_yn": "N",
						"exit_if_loss_pct_max": 3,
						"skip_prod_ids": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						}
					},
					"bb_bo": {
						"exit_if_profit_yn": "Y",
						"exit_if_profit_pct_min": 1,
						"exit_if_loss_yn": "N",
						"exit_if_loss_pct_max": 3,
						"skip_prod_ids": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						}
					},
					"bb": {
						"exit_if_profit_yn": "Y",
						"exit_if_profit_pct_min": 1,
						"exit_if_loss_yn": "N",
						"exit_if_loss_pct_max": 3,
						"skip_prod_ids": [],
						"tests_min": {
							"15min": 13,
							"30min": 11,
							"1h": 9,
							"4h": 7,
							"1d": 5
						}
					}
				},
				"rainy_day": {
					"pocket_pct": {
						"***": 10,
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

	elif symb == 'BTC':
		settings_template_json = {}

	elif symb == 'ETH':
		settings_template_json = {}

	mkt_settings = Settings(f'settings/market_{symb}.json', settings_template_json)
	mst = mkt_settings.settings_load()
	return mst, mkt_settings

#<=====>#

def get_ovrd_value(in_data, k):
	if isinstance(in_data, dict):
		if k in in_data:
			return in_data[k]
		elif '***' in in_data:
			return in_data['***']
		else:
			return {k: get_ovrd_value(v, k) for k, v in in_data.items()}
	elif isinstance(in_data, list):
		return [get_ovrd_value(item, k) for item in in_data]
	else:
		return in_data

#<=====>#

def resolve_settings(st, prod_id):
	return get_ovrd_value(st, prod_id)

#<=====>#

def pair_settings_get(symb, prod_id):
	symb = symb.upper()
	prod_id = prod_id.upper()
	r = mkt_settings_get(symb)
	mst = r[0]
	pst = resolve_settings(mst, prod_id)
	return pst

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

