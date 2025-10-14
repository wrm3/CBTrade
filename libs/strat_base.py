#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#

 

#<=====>#
# Imports - Public
#<=====>#
import sys
import traceback
from fstrent_colors import *
from pprint import pprint

#<=====>#
# Imports - Project
#<=====>#
from libs.common                       import AttrDict, narc
from libs.strats.strat_bb              import settings_bb, buy_strat_bb, sell_strat_bb
from libs.strats.strat_bb_bo           import settings_bb_bo, buy_strat_bb_bo, sell_strat_bb_bo
from libs.strats.strat_drop            import settings_drop, buy_strat_drop, sell_strat_drop
from libs.strats.strat_imp_macd        import settings_imp_macd, buy_strat_imp_macd, sell_strat_imp_macd
from libs.strats.strat_nwe_3row        import settings_nwe_3row, buy_strat_nwe_3row, sell_strat_nwe_3row
from libs.strats.strat_nwe_env         import settings_nwe_env, buy_strat_nwe_env, sell_strat_nwe_env
from libs.strats.strat_nwe_rev         import settings_nwe_rev, buy_strat_nwe_rev, sell_strat_nwe_rev
from libs.strats.strat_sha             import settings_sha, buy_strat_sha, sell_strat_sha
from libs.strats.strat_tpo             import settings_tpo, buy_strat_tpo, sell_strat_tpo
from libs.strats.strat_vidya           import settings_vidya, buy_strat_vidya, sell_strat_vidya
from libs.strats.strat_ht              import settings_ht, buy_strat_ht, sell_strat_ht
from libs.strats.strat_msb             import settings_msb, buy_strat_msb, sell_strat_msb
from libs.strats.strat_rsi_div_macd    import settings_rsi_div_macd, buy_strat_rsi_div_macd, sell_strat_rsi_div_macd
from libs.strats.strat_st_atr          import settings_st_atr, buy_strat_st_atr, sell_strat_st_atr
from libs.strats.strat_vwmacd          import settings_vwmacd, buy_strat_vwmacd, sell_strat_vwmacd
from libs.strats.strat_vwtm            import settings_vwtm, buy_strat_vwtm, sell_strat_vwtm

#ADD_NEW_STARTS_HERE


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strats'
log_name      = 'bot_strats'


# <=====>#
# Assignments Pre
# <=====>#



#<=====>#
# Notes
#<=====>#
#ADD_NEW_STARTS_HERE
# New Strat Add Section
# Need to also insert into buy_strats table
# Need to also add to settings buy & sell sections...
# SELECT * FROM buy_strats;
# insert into buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc) values ('up', 'nwe', 'nadaraya-watson estimator');


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

@narc(1)
def buy_strats_get(self):
    if self.debug_tf: B(f'==> strat_base.buy_strats_get()')
    strats = {}
    #ADD_NEW_STARTS_HERE
    for freq in ['15min', '30min', '1h', '4h', '1d']:
        strats[f'nwe_3row_{freq}'] = {'prod_id': '', 'buy_strat_nick': f'nwe_3row_{freq}', 'buy_strat_type': 'up', 'buy_strat_name': 'nwe_3row', 'buy_strat_desc': 'Nadaraya-Watson Estimator - 3 Row',    'buy_strat_freq': freq}
        strats[f'sha_{freq}']      = {'prod_id': '', 'buy_strat_nick': f'sha_{freq}',      'buy_strat_type': 'up', 'buy_strat_name': 'sha',      'buy_strat_desc': 'Double Smoothed Heikin Ashi',          'buy_strat_freq': freq}
        strats[f'imp_macd_{freq}'] = {'prod_id': '', 'buy_strat_nick': f'imp_macd_{freq}', 'buy_strat_type': 'up', 'buy_strat_name': 'imp_macd', 'buy_strat_desc': 'Impulse MACD',                         'buy_strat_freq': freq}
        strats[f'bb_bo_{freq}']    = {'prod_id': '', 'buy_strat_nick': f'bb_bo_{freq}',    'buy_strat_type': 'up', 'buy_strat_name': 'bb_bo',    'buy_strat_desc': 'Bollinger Band Breakout',              'buy_strat_freq': freq}
        strats[f'tpo_{freq}']      = {'prod_id': '', 'buy_strat_nick': f'tpo_{freq}',      'buy_strat_type': 'up', 'buy_strat_name': 'tpo',      'buy_strat_desc': 'Two-Pole Oscillator',                  'buy_strat_freq': freq}
        strats[f'vidya_{freq}']    = {'prod_id': '', 'buy_strat_nick': f'vidya_{freq}',    'buy_strat_type': 'up', 'buy_strat_name': 'vidya',    'buy_strat_desc': 'Vidya',                                'buy_strat_freq': freq}

        strats[f'nwe_env_{freq}']  = {'prod_id': '', 'buy_strat_nick': f'nwe_env_{freq}',  'buy_strat_type': 'dn', 'buy_strat_name': 'nwe_env',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Envelope', 'buy_strat_freq': freq}
        strats[f'nwe_rev_{freq}']  = {'prod_id': '', 'buy_strat_nick': f'nwe_rev_{freq}',  'buy_strat_type': 'dn', 'buy_strat_name': 'nwe_rev',  'buy_strat_desc': 'Nadaraya-Watson Estimator - Reversal', 'buy_strat_freq': freq}
        strats[f'bb_{freq}']       = {'prod_id': '', 'buy_strat_nick': f'bb_{freq}',       'buy_strat_type': 'dn', 'buy_strat_name': 'bb',       'buy_strat_desc': 'Bollinger Band',                       'buy_strat_freq': freq}
        strats[f'drop_{freq}']     = {'prod_id': '', 'buy_strat_nick': f'drop_{freq}',     'buy_strat_type': 'dn', 'buy_strat_name': 'drop',     'buy_strat_desc': 'Big Dip Strat',                        'buy_strat_freq': freq}

        strats[f'ht_{freq}']           = {'prod_id': '', 'buy_strat_nick': f'ht_{freq}',           'buy_strat_type': 'dn', 'buy_strat_name': 'ht',           'buy_strat_desc': 'Hulle Trend',                'buy_strat_freq': freq}
        strats[f'msb_{freq}']          = {'prod_id': '', 'buy_strat_nick': f'msb_{freq}',          'buy_strat_type': 'dn', 'buy_strat_name': 'msb',          'buy_strat_desc': 'Market Structure Break',     'buy_strat_freq': freq}
        strats[f'rsi_div_macd_{freq}'] = {'prod_id': '', 'buy_strat_nick': f'rsi_div_macd_{freq}', 'buy_strat_type': 'dn', 'buy_strat_name': 'rsi_div_macd', 'buy_strat_desc': 'RSI Divergence MACD',        'buy_strat_freq': freq}
        strats[f'st_atr_{freq}']       = {'prod_id': '', 'buy_strat_nick': f'st_atr_{freq}',       'buy_strat_type': 'dn', 'buy_strat_name': 'st_atr',       'buy_strat_desc': 'Supertrend ATR',             'buy_strat_freq': freq}
        strats[f'vwmacd_{freq}']       = {'prod_id': '', 'buy_strat_nick': f'vwmacd_{freq}',       'buy_strat_type': 'dn', 'buy_strat_name': 'vwmacd',       'buy_strat_desc': 'Volume Weighted MACD',       'buy_strat_freq': freq}
        strats[f'vwtm_{freq}']         = {'prod_id': '', 'buy_strat_nick': f'vwtm_{freq}',         'buy_strat_type': 'dn', 'buy_strat_name': 'vwtm',         'buy_strat_desc': 'Volume Weighted Trend',       'buy_strat_freq': freq}
    return strats

#<=====>#

@narc(1)
def strat_settings_get(self, st):
    if self.debug_tf: B(f'==> strat_base.strat_settings_get()')
    #ADD_NEW_STARTS_HERE
    st = settings_sha(st)
    st = settings_nwe_3row(st)
    st = settings_nwe_env(st)
    st = settings_nwe_rev(st)
    st = settings_imp_macd(st)
    st = settings_bb_bo(st)
    st = settings_bb(st)
    st = settings_drop(st)
    st = settings_tpo(st)
    st = settings_vidya(st)

    st = settings_ht(st)
    st = settings_msb(st)
    st = settings_rsi_div_macd(st)
    st = settings_st_atr(st)
    st = settings_vwmacd(st)
    st = settings_vwtm(st)

    return st

#<=====>#

@narc(1)
def buy_strats_avail_get(self, prod_id, st_pair):
    if self.debug_tf: B(f'==> strat_base.buy_strats_avail_get(prod_id={prod_id}, st_pair)')

    buy_strats = AttrDict()

    # New Strat Add Section
    buy_strats.strat_sha_yn = 'N'
    if not st_pair.strats.sha.buy.prod_ids:
        buy_strats.strat_sha_yn = 'Y'
    elif prod_id in st_pair.strats.sha.buy.prod_ids:
        buy_strats.strat_sha_yn = 'Y'
    if st_pair.strats.sha.buy.skip_prod_ids:
        if prod_id in st_pair.strats.sha.buy.skip_prod_ids:
            buy_strats.strat_sha_yn = 'N'

    buy_strats.strat_nwe_3row_yn = 'N'
    if not st_pair.strats.nwe_3row.buy.prod_ids:
        buy_strats.strat_nwe_3row_yn = 'Y'
    elif prod_id in st_pair.strats.nwe_3row.buy.prod_ids:
        buy_strats.strat_nwe_3row_yn = 'Y'
    if st_pair.strats.nwe_3row.buy.skip_prod_ids:
        if prod_id in st_pair.strats.nwe_3row.buy.skip_prod_ids:
            buy_strats.strat_nwe_3row_yn = 'N'

    buy_strats.strat_nwe_env_yn = 'N'
    if not st_pair.strats.nwe_env.buy.prod_ids:
        buy_strats.strat_nwe_env_yn = 'Y'
    elif prod_id in st_pair.strats.nwe_env.buy.prod_ids:
        buy_strats.strat_nwe_env_yn = 'Y'
    if st_pair.strats.nwe_env.buy.skip_prod_ids:
        if prod_id in st_pair.strats.nwe_env.buy.skip_prod_ids:
            buy_strats.strat_nwe_env_yn = 'N'

    buy_strats.strat_nwe_rev_yn = 'N'
    if not st_pair.strats.nwe_rev.buy.prod_ids:
        buy_strats.strat_nwe_rev_yn = 'Y'
    elif prod_id in st_pair.strats.nwe_rev.buy.prod_ids:
        buy_strats.strat_nwe_rev_yn = 'Y'
    if st_pair.strats.nwe_rev.buy.skip_prod_ids:
        if prod_id in st_pair.strats.nwe_rev.buy.skip_prod_ids:
            buy_strats.strat_nwe_rev_yn = 'N'

    buy_strats.strat_imp_macd_yn = 'N'
    if not st_pair.strats.imp_macd.buy.prod_ids:
        buy_strats.strat_imp_macd_yn = 'Y'
    elif prod_id in st_pair.strats.imp_macd.buy.prod_ids:
        buy_strats.strat_imp_macd_yn = 'Y'
    if st_pair.strats.imp_macd.buy.skip_prod_ids:
        if prod_id in st_pair.strats.imp_macd.buy.skip_prod_ids:
            buy_strats.strat_imp_macd_yn = 'N'

    buy_strats.strat_drop_yn = 'N'
    if not st_pair.strats.drop.buy.prod_ids:
        buy_strats.strat_drop_yn = 'Y'
    elif prod_id in st_pair.strats.drop.buy.prod_ids:
        buy_strats.strat_drop_yn = 'Y'
    if st_pair.strats.drop.buy.skip_prod_ids:
        if prod_id in st_pair.strats.drop.buy.skip_prod_ids:
            buy_strats.strat_drop_yn = 'N'

    buy_strats.strat_bb_bo_yn = 'N'
    if not st_pair.strats.bb_bo.buy.prod_ids:
        buy_strats.strat_bb_bo_yn = 'Y'
    elif prod_id in st_pair.strats.bb_bo.buy.prod_ids:
        buy_strats.strat_bb_bo_yn = 'Y'
    if st_pair.strats.bb_bo.buy.skip_prod_ids:
        if prod_id in st_pair.strats.bb_bo.buy.skip_prod_ids:
            buy_strats.strat_bb_bo_yn = 'N'

    buy_strats.strat_bb_yn = 'N'
    if not st_pair.strats.bb.buy.prod_ids:
        buy_strats.strat_bb_yn = 'Y'
    elif prod_id in st_pair.strats.bb.buy.prod_ids:
        buy_strats.strat_bb_yn = 'Y'
    if st_pair.strats.bb.buy.skip_prod_ids:
        if prod_id in st_pair.strats.bb.buy.skip_prod_ids:
            buy_strats.strat_bb_yn = 'N'

    buy_strats.strat_tpo_yn = 'N'
    if not st_pair.strats.tpo.buy.prod_ids:
        buy_strats.strat_tpo_yn = 'Y'
    elif prod_id in st_pair.strats.tpo.buy.prod_ids:
        buy_strats.strat_tpo_yn = 'Y'
    if st_pair.strats.tpo.buy.skip_prod_ids:
        if prod_id in st_pair.strats.tpo.buy.skip_prod_ids:
            buy_strats.strat_tpo_yn = 'N'

    buy_strats.strat_vidya_yn = 'N'
    if not st_pair.strats.vidya.buy.prod_ids:
        buy_strats.strat_vidya_yn = 'Y'
    elif prod_id in st_pair.strats.vidya.buy.prod_ids:
        buy_strats.strat_vidya_yn = 'Y'
    if st_pair.strats.vidya.buy.skip_prod_ids:
        if prod_id in st_pair.strats.vidya.buy.skip_prod_ids:
            buy_strats.strat_vidya_yn = 'N'

    buy_strats.strat_ht_yn = 'N'
    if not st_pair.strats.ht.buy.prod_ids:
        buy_strats.strat_ht_yn = 'Y'
    elif prod_id in st_pair.strats.ht.buy.prod_ids:
        buy_strats.strat_ht_yn = 'Y'
    if st_pair.strats.ht.buy.skip_prod_ids:
        if prod_id in st_pair.strats.ht.buy.skip_prod_ids:
            buy_strats.strat_ht_yn = 'N'

    buy_strats.strat_msb_yn = 'N'
    if not st_pair.strats.msb.buy.prod_ids:
        buy_strats.strat_msb_yn = 'Y'
    elif prod_id in st_pair.strats.msb.buy.prod_ids:
        buy_strats.strat_msb_yn = 'Y'
    if st_pair.strats.msb.buy.skip_prod_ids:
        if prod_id in st_pair.strats.msb.buy.skip_prod_ids:
            buy_strats.strat_msb_yn = 'N'

    buy_strats.strat_rsi_div_macd_yn = 'N'
    if not st_pair.strats.rsi_div_macd.buy.prod_ids:
        buy_strats.strat_rsi_div_macd_yn = 'Y'
    elif prod_id in st_pair.strats.rsi_div_macd.buy.prod_ids:
        buy_strats.strat_rsi_div_macd_yn = 'Y'
    if st_pair.strats.rsi_div_macd.buy.skip_prod_ids:
        if prod_id in st_pair.strats.rsi_div_macd.buy.skip_prod_ids:
            buy_strats.strat_rsi_div_macd_yn = 'N'

    buy_strats.strat_st_atr_yn = 'N'
    if not st_pair.strats.st_atr.buy.prod_ids:
        buy_strats.strat_st_atr_yn = 'Y'
    elif prod_id in st_pair.strats.st_atr.buy.prod_ids:
        buy_strats.strat_st_atr_yn = 'Y'
    if st_pair.strats.st_atr.buy.skip_prod_ids:
        if prod_id in st_pair.strats.st_atr.buy.skip_prod_ids:
            buy_strats.strat_st_atr_yn = 'N'

    buy_strats.strat_vwmacd_yn = 'N'
    if not st_pair.strats.vwmacd.buy.prod_ids:
        buy_strats.strat_vwmacd_yn = 'Y'
    elif prod_id in st_pair.strats.vwmacd.buy.prod_ids:
        buy_strats.strat_vwmacd_yn = 'Y'
    if st_pair.strats.vwmacd.buy.skip_prod_ids:
        if prod_id in st_pair.strats.vwmacd.buy.skip_prod_ids:
            buy_strats.strat_vwmacd_yn = 'N'

    buy_strats.strat_vwtm_yn = 'N'
    if not st_pair.strats.vwtm.buy.prod_ids:
        buy_strats.strat_vwtm_yn = 'Y'
    elif prod_id in st_pair.strats.vwtm.buy.prod_ids:
        buy_strats.strat_vwtm_yn = 'Y'
    if st_pair.strats.vwtm.buy.skip_prod_ids:
        if prod_id in st_pair.strats.vwtm.buy.skip_prod_ids:
            buy_strats.strat_vwtm_yn = 'N'

    return buy_strats

#<=====>#

@narc(1)
def buy_strats_check(self, buy, ta, st_pair):
    if self.debug_tf: B(f'==> strat_base.buy_strats_check(buy={buy.prod_id}, ta=ta, st_pair=st_pair)')

    buy.buy_yn          = 'N'
    buy.wait_yn         = 'Y'
    freq                = buy.trade_strat_perf['A'].buy_strat_freq

    #ADD_NEW_STARTS_HERE

    # Buy Strategy - Double Smoothed Heikin Ashi
    if buy.trade_strat_perf['A'].buy_strat_name == 'sha':
        if buy.st_pair.strats.sha.use_yn == 'Y' and buy.strat_sha_yn == 'Y':
            if freq in buy.st_pair.strats.sha.freqs:

                    buy, ta = buy_strat_sha(buy, ta, st_pair)
                    buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                    buy.buy_signals.append(buy_signal)

    # Buy Strategy - Nadaraya-Waston 3Row
    elif buy.trade_strat_perf['A'].buy_strat_name == 'nwe_3row':
        if buy.st_pair.strats.nwe_3row.use_yn == 'Y' and buy.strat_nwe_3row_yn == 'Y':
            if freq in buy.st_pair.strats.nwe_3row.freqs:
                buy, ta = buy_strat_nwe_3row(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Nadaraya-Waston Envelope
    elif buy.trade_strat_perf['A'].buy_strat_name == 'nwe_env':
        if buy.st_pair.strats.nwe_env.use_yn == 'Y' and buy.strat_nwe_env_yn == 'Y':
            if freq in buy.st_pair.strats.nwe_env.freqs:
                buy, ta = buy_strat_nwe_env(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Nadaraya-Waston Reversal
    elif buy.trade_strat_perf['A'].buy_strat_name == 'nwe_rev':
        if buy.st_pair.strats.nwe_rev.use_yn == 'Y' and buy.strat_nwe_rev_yn == 'Y':
            if freq in buy.st_pair.strats.nwe_rev.freqs:
                buy, ta = buy_strat_nwe_rev(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Impulse MACD
    elif buy.trade_strat_perf['A'].buy_strat_name == 'imp_macd':
        if buy.st_pair.strats.imp_macd.use_yn == 'Y' and buy.strat_imp_macd_yn == 'Y':
            if freq in buy.st_pair.strats.imp_macd.freqs:
                buy, ta = buy_strat_imp_macd(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Bollinger Band Breakout
    elif buy.trade_strat_perf['A'].buy_strat_name == 'bb_bo':
        if buy.st_pair.strats.bb_bo.use_yn == 'Y' and buy.strat_bb_bo_yn == 'Y':
            if freq in buy.st_pair.strats.bb_bo.freqs:
                buy, ta = buy_strat_bb_bo(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Drop
    elif buy.trade_strat_perf['A'].buy_strat_name == 'drop':
        if buy.st_pair.strats.drop.use_yn == 'Y' and buy.strat_drop_yn == 'Y':
            if freq in buy.st_pair.strats.drop.freqs:
                buy, ta = buy_strat_drop(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Bollinger Band
    elif buy.trade_strat_perf['A'].buy_strat_name == 'bb':
        if buy.st_pair.strats.bb.use_yn == 'Y' and buy.strat_bb_yn == 'Y':
            if freq in buy.st_pair.strats.bb.freqs:
                buy, ta = buy_strat_bb(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Two-Pole Oscillator
    elif buy.trade_strat_perf['A'].buy_strat_name == 'tpo':
        if buy.st_pair.strats.tpo.use_yn == 'Y' and buy.strat_tpo_yn == 'Y':
            if freq in buy.st_pair.strats.tpo.freqs:
                buy, ta = buy_strat_tpo(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Vidya
    elif buy.trade_strat_perf['A'].buy_strat_name == 'vidya':
        if buy.st_pair.strats.vidya.use_yn == 'Y' and buy.strat_vidya_yn == 'Y':
            if freq in buy.st_pair.strats.vidya.freqs:
                buy, ta = buy_strat_vidya(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Hulle Trend
    elif buy.trade_strat_perf['A'].buy_strat_name == 'ht':
        if buy.st_pair.strats.ht.use_yn == 'Y' and buy.strat_ht_yn == 'Y':
            if freq in buy.st_pair.strats.ht.freqs:
                buy, ta = buy_strat_ht(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Market Structure Break
    elif buy.trade_strat_perf['A'].buy_strat_name == 'msb':
        if buy.st_pair.strats.msb.use_yn == 'Y' and buy.strat_msb_yn == 'Y':
            if freq in buy.st_pair.strats.msb.freqs:
                buy, ta = buy_strat_msb(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - RSI Divergence MACD
    elif buy.trade_strat_perf['A'].buy_strat_name == 'rsi_div_macd':
        if buy.st_pair.strats.rsi_div_macd.use_yn == 'Y' and buy.strat_rsi_div_macd_yn == 'Y':
            if freq in buy.st_pair.strats.rsi_div_macd.freqs:
                buy, ta = buy_strat_rsi_div_macd(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Supertrend ATR
    elif buy.trade_strat_perf['A'].buy_strat_name == 'st_atr':
        if buy.st_pair.strats.st_atr.use_yn == 'Y' and buy.strat_st_atr_yn == 'Y':
            if freq in buy.st_pair.strats.st_atr.freqs:
                buy, ta = buy_strat_st_atr(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Volume Weighted MACD
    elif buy.trade_strat_perf['A'].buy_strat_name == 'vwmacd':
        if buy.st_pair.strats.vwmacd.use_yn == 'Y' and buy.strat_vwmacd_yn == 'Y':
            if freq in buy.st_pair.strats.vwmacd.freqs:
                buy, ta = buy_strat_vwmacd(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

    # Buy Strategy - Volume Weighted Trend
    elif buy.trade_strat_perf['A'].buy_strat_name == 'vwtm':
        if buy.st_pair.strats.vwtm.use_yn == 'Y' and buy.strat_vwtm_yn == 'Y':
            if freq in buy.st_pair.strats.vwtm.freqs:
                buy, ta = buy_strat_vwtm(buy, ta, st_pair)
                buy_signal = {"prod_id": buy.prod_id, "buy_strat_type": buy.trade_strat_perf['A'].buy_strat_type, "buy_strat_name": buy.trade_strat_perf['A'].buy_strat_name, "buy_strat_freq": buy.trade_strat_perf['A'].buy_strat_freq, "buy_yn": buy.buy_yn, "wait_yn": buy.wait_yn}
                buy.buy_signals.append(buy_signal)

        else:
            buy.buy_yn = 'N'
            buy.wait_yn = 'Y'

    return buy, ta

#<=====>#

@narc(1)
def buy_strats_deny(self, buy):
    if self.debug_tf: B(f'==> strat_base.buy_strats_deny(buy={buy})')
    #ADD_NEW_STARTS_HERE

    # Strategy Exit - Smoothed Heikin Ashi
    if buy.trade_strat_perf['A'].buy_strat_name == 'sha':
        if buy.strat_sha_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - 3-Row Heikin Ashi
    elif buy.trade_strat_perf['A'].buy_strat_name == 'nwe_3row':
        if buy.strat_nwe_3row_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - Environment Heikin Ashi
    elif buy.trade_strat_perf['A'].buy_strat_name == 'nwe_env':
        if buy.strat_nwe_env_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - Reversal Heikin Ashi
    elif buy.trade_strat_perf['A'].buy_strat_name == 'nwe_rev':
        if buy.strat_nwe_rev_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - Impulse MACD
    elif buy.trade_strat_perf['A'].buy_strat_name == 'imp_macd':
        if buy.strat_imp_macd_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - Bollinger Band Breakout
    elif buy.trade_strat_perf['A'].buy_strat_name == 'bb_bo':
        if buy.strat_bb_bo_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - Bollinger Band
    elif buy.trade_strat_perf['A'].buy_strat_name == 'bb':
        if buy.strat_bb_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - Drop
    elif buy.trade_strat_perf['A'].buy_strat_name == 'drop':
        if buy.strat_drop_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - Two-Pole Oscillator
    elif buy.trade_strat_perf['A'].buy_strat_name == 'tpo':
        if buy.strat_tpo_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Strategy Exit - Vidya
    elif buy.trade_strat_perf['A'].buy_strat_name == 'vidya':
        if buy.strat_vidya_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Buy Strategy - Hulle Trend
    elif buy.trade_strat_perf['A'].buy_strat_name == 'ht':
        if buy.strat_ht_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Buy Strategy - Market Structure Break
    elif buy.trade_strat_perf['A'].buy_strat_name == 'msb':
        if buy.strat_msb_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Buy Strategy - RSI Divergence MACD
    elif buy.trade_strat_perf['A'].buy_strat_name == 'rsi_div_macd':
        if buy.strat_rsi_div_macd_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Buy Strategy - Supertrend ATR
    elif buy.trade_strat_perf['A'].buy_strat_name == 'st_atr':
        if buy.strat_st_atr_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Buy Strategy - Volume Weighted MACD
    elif buy.trade_strat_perf['A'].buy_strat_name == 'vwmacd':
        if buy.strat_vwmacd_yn == 'N':
            buy.buy_deny_yn = 'Y'

    # Buy Strategy - Volume Weighted Trend
    elif buy.trade_strat_perf['A'].buy_strat_name == 'vwtm':
        if buy.strat_vwtm_yn == 'N':
            buy.buy_deny_yn = 'Y'

    return buy

#<=====>#

@narc(1)
def sell_strats_check(self, mkt, pos, ta, st_pair):
    if self.debug_tf: B(f'==> strat_base.sell_strats_check(mkt={mkt.prod_id}, pos={pos.pos_id}, ta=ta, st_pair=st_pair)')
    #ADD_NEW_STARTS_HERE

    try:
        # Strategy Exit - Smoothed Heikin Ashi
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'sha':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_sha()')
                mkt, pos, ta = sell_strat_sha(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_sha()')

        # Strategy Exit - 3-Row Heikin Ashi
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'nwe_3row':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_nwe_3row()')
                mkt, pos, ta = sell_strat_nwe_3row(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_nwe_3row()')

        # Strategy Exit - Environment Heikin Ashi
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'nwe_env':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_nwe_env()')
                mkt, pos, ta = sell_strat_nwe_env(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_nwe_env()')

        # Strategy Exit - Reversal Heikin Ashi
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'nwe_rev':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_nwe_rev()')
                mkt, pos, ta = sell_strat_nwe_rev(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_nwe_rev()')

        # Strategy Exit - Impulse MACD
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'imp_macd':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_imp_macd()')
                mkt, pos, ta = sell_strat_imp_macd(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_imp_macd()')

        # Strategy Exit - Bollinger Band
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'bb':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_bb()')
                mkt, pos, ta = sell_strat_bb(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_bb()')

        # Strategy Exit - Bollinger Band Breakout
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'bb_bo':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_bb_bo()')
                mkt, pos, ta = sell_strat_bb_bo(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_bb_bo()')

        # Strategy Exit - Bollinger Band Breakout
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'drop':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_drop()')
                mkt, pos, ta = sell_strat_drop(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_drop()')

        # Strategy Exit - Two-Pole Oscillator
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'tpo':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_tpo()')
                mkt, pos, ta = sell_strat_tpo(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_tpo()')

        # Strategy Exit - Vidya
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'vidya':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_vidya()')
                mkt, pos, ta = sell_strat_vidya(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_vidya()')

        # Strategy Exit - Hulle Trend
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'ht':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_ht()')
                mkt, pos, ta = sell_strat_ht(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_ht()')

        # Strategy Exit - Market Structure Break
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'msb':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_msb()')
                mkt, pos, ta = sell_strat_msb(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_msb()')

        # Strategy Exit - RSI Divergence MACD
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'rsi_div_macd':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_rsi_div_macd()')
                mkt, pos, ta = sell_strat_rsi_div_macd(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_rsi_div_macd()')

        # Strategy Exit - Supertrend ATR
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'st_atr':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_st_atr()')
                mkt, pos, ta = sell_strat_st_atr(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_st_atr()')

        # Strategy Exit - Volume Weighted MACD
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'vwmacd':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_vwmacd()')
                mkt, pos, ta = sell_strat_vwmacd(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_vwmacd()')

        # Strategy Exit - Volume Weighted Trend
        if pos.sell_yn == 'N':
            if pos.buy_strat_name == 'vwtm':
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> calling sell_strat_vwtm()')
                mkt, pos, ta = sell_strat_vwtm(mkt, pos, ta, st_pair)
                if self.debug_tf: B(f'==> strat_base.sell_strats_check() ==> returning from sell_strat_vwtm()')


    except Exception as e:
        # 🚨 HARD CRASH DEBUGGING: Comprehensive failure information
        print(f"\n{'='*80}")
        print(f"🚨 CRITICAL SELL_STRATS_CHECK PROCESSING FAILURE")
        print(f"{'='*80}")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"\nFULL TRACEBACK:")
        traceback.print_exc()
        print(f"{'='*80}")
        sys.exit(f"SELL_STRATS_CHECK PROCESSING FAILURE EXIT - {type(e).__name__}: {str(e)}")

    if self.debug_tf: C(f'==> strat_base.sell_strats_check() 808 leaving...')

    return mkt, pos, ta

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
