#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from fstrent_tools import beep, print_adv
from libs.bot_common import freqs_get
from libs.bot_strat_common import disp_sell_tests, exit_if_logic
import traceback


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strat_imp_macd'
log_name      = 'bot_strat_imp_macd'


# <=====>#
# Assignments Pre
# <=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#



def buy_strat_settings_imp_macd(st):
    buy_strat_st = {
                    "use_yn": "Y",
                    "freqs": ["1d", "4h", "1h", "30min", "15min"],
                    "per_ma": 34,
                    "per_sign": 9,
                    "prod_ids": [],
                    "skip_prod_ids": [],
                    "tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
                    "boost_tests_min": {"15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11},
                    "show_tests_yn": "Y"
                    }
    st['buy']['strats']['imp_macd'] = buy_strat_st
    return st

#<=====>#

def sell_strat_settings_imp_macd(st):
    sell_strat_st = {
                    "exit_if_profit_yn": "Y",
                    "exit_if_profit_pct_min": 1,
                    "exit_if_loss_yn": "N",
                    "exit_if_loss_pct_max": 3,
                    "skip_prod_ids": [],
                    "tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
                    "show_tests_yn": "Y"
                    }
    st['sell']['strats']['imp_macd'] = sell_strat_st
    return st
#<=====>#

def buy_strat_imp_macd(buy, ta, pst):
    try:
        all_passes       = []
        all_fails        = []
        prod_id          = buy.prod_id
        buy.buy_yn       = 'Y'
        buy.wait_yn      = 'N'
        buy.show_tests_yn = buy.pst.buy.strats.imp_macd.show_tests_yn

        buy.rfreq        = buy.trade_strat_perf.buy_strat_freq
        freqs, faster_freqs     = freqs_get(buy.rfreq)

        # Impulse MACD + ATR
        # MACD > Signal
        m = '{} impulse macd > signal ==> macd : {:>5}, signal : {:>5}'
        msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['imp_macd']['ago0'], buy.ta[buy.rfreq]['imp_macd_sign']['ago0'])
        if buy.ta[buy.rfreq]['imp_macd']['ago0'] > buy.ta[buy.rfreq]['imp_macd_sign']['ago0']:
            all_passes.append(msg)
        else:
            buy.buy_yn  = 'N'
            all_fails.append(msg)


        # MACD Long Enter True
#        m = '{} impulse macd color must be lime or green ==> macd color : {:>5}'
        m = '{} impulse macd color must be lime ==> macd color : {:>5}'
        msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['Long_Enter']['ago0'])
#        if buy.ta[buy.rfreq]['imp_macd_color']['ago0'] in ('lime','green'):
        if buy.ta[buy.rfreq]['Long_Enter']['ago0']:
            all_passes.append(msg)
        else:
            buy.buy_yn  = 'N'
            all_fails.append(msg)


#         # MACD Line Should Be Green or Lime
# #        m = '{} impulse macd color must be lime or green ==> macd color : {:>5}'
#         m = '{} impulse macd color must be lime ==> macd color : {:>5}'
#         msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['imp_macd_color']['ago0'])
# #        if buy.ta[buy.rfreq]['imp_macd_color']['ago0'] in ('lime','green'):
#         if buy.ta[buy.rfreq]['imp_macd_color']['ago0'] in ('lime'):
#             all_passes.append(msg)
#         else:
#             buy.buy_yn  = 'N'
#             all_fails.append(msg)

        # MACD & Signal Should Be Sufficiently Appart and Not Hugging
        spread = buy.ta[buy.rfreq]['imp_macd']['ago0'] - buy.ta[buy.rfreq]['imp_macd_sign']['ago0']
        min_spread_pct = 5
        min_spread = buy.ta[buy.rfreq]['atr']['ago0'] * (min_spread_pct/100)
        m = '{} impulse macd_signal > atr_low * 0.0{} ==> macd : {:>5}, sign : {:>5}, spread : {:>5}, min_spread_pct : {:>5}, min_spread : {:>5}'
        msg = m.format(buy.rfreq, min_spread_pct, buy.ta[buy.rfreq]['imp_macd']['ago0'], buy.ta[buy.rfreq]['imp_macd_sign']['ago0'], spread, min_spread_pct, min_spread)
        if spread > min_spread:
            all_passes.append(msg)
        else:
            buy.buy_yn  = 'N'
            all_fails.append(msg)


        spread = buy.ta[buy.rfreq]['imp_macd']['ago0'] - buy.ta[buy.rfreq]['imp_macd_sign']['ago0']
        min_spread_pct = 5
        min_spread = buy.ta[buy.rfreq]['atr']['ago0'] * (min_spread_pct/100)
        m = '{} impulse macd_signal > atr_low * 0.0{} ==> macd : {:>5}, sign : {:>5}, spread : {:>5}, min_spread_pct : {:>5}, min_spread : {:>5}'
        msg = m.format(buy.rfreq, min_spread_pct, buy.ta[buy.rfreq]['imp_macd']['ago0'], buy.ta[buy.rfreq]['imp_macd_sign']['ago0'], spread, min_spread_pct, min_spread)
        if spread > min_spread:
            all_passes.append(msg)
        else:
            buy.buy_yn  = 'N'
            all_fails.append(msg)


        # Current Candle is Green
        ago_list = ['ago0']
        for freq in freqs:
            for ago in ago_list:
                color = buy.ta[freq]['color'][ago]
                msg = f'{freq} {ago} candles == green : {color}'
                if color == 'green':
                    all_passes.append(msg)
                else:
                    buy.buy_yn  = 'N'
                    all_fails.append(msg)

        # Heikin Ashi Candles - Multi Timeframe - Candles Are Green
        ago_list = ['ago0','ago1']
        for freq in faster_freqs:
            for ago in ago_list:
                ha_color = buy.ta[freq]['ha_color'][ago]
                msg = f'{freq} {ago} Heikin Ashi candles == green : {ha_color}'
                if ha_color == 'green':
                    all_passes.append(msg)
                else:
                    buy.buy_yn  = 'N'
                    all_fails.append(msg)

        # Nadaraya-Watson Estimator - Estimated Is Green
        ago_list = ['ago0','ago1']
        for ago in ago_list:
            m = '{} Nadaraya-Watson Estimator color {} == green : {}'
            msg = m.format(freq, ago, buy.ta[buy.rfreq]['nwe_color'][ago])
            if buy.ta[freq]['ha_color'][ago] == 'green':
                all_passes.append(msg)
            else:
                buy.buy_yn  = 'N'
                all_fails.append(msg)

        if buy.buy_yn == 'Y':
            buy.wait_yn = 'N'
            buy.buy_strat_type  = 'up'
            buy.buy_strat_name  = 'imp_macd'
            buy.buy_strat_freq  = buy.rfreq
        else:
            buy.wait_yn = 'Y'

        # buy.trade_strat_perf.pass_cnt     = len(all_passes)
        # buy.trade_strat_perf.fail_cnt     = len(all_fails)
        # buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
        # buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
        buy.all_passes   = all_passes
        buy.all_fails    = all_fails
        buy.buy_yn       = buy.buy_yn
        buy.wait_yn      = buy.wait_yn

    except Exception as e:
        traceback.print_exc()
        print_adv(3)
        beep()
        buy.buy_yn  = 'N'
        buy.wait_yn = 'Y'

    buy.buy_yn  = buy.buy_yn
    buy.wait_yn = buy.wait_yn

    return buy, ta

#<=====>#

def sell_strat_imp_macd(mkt, pos, ta, pst):
    try:
        all_sells  = []
        all_hodls   = []

        freq = pos.buy_strat_freq

        # MACD Long Exit True
        imp_macd_long_exit = ta[freq]['Long_Exit']['ago0']
        if imp_macd_long_exit:
            msg = f'SELL COND: {freq} impulse macd ==> Long_Exit : {imp_macd_long_exit:>5}'
            all_sells.append(msg)
        else:
            msg = f'HODL COND: {freq} impulse macd ==> Long_Exit : {imp_macd_long_exit:>5}'
            all_hodls.append(msg)

        # Impulse MACD + ATR
        # MACD > Signal
        imp_macd_curr      = ta[freq]['imp_macd']['ago0']
        imp_macd_sign_curr = ta[freq]['imp_macd_sign']['ago0']
        if imp_macd_curr < imp_macd_sign_curr:
            msg = f'SELL COND: {freq} impulse macd < signal ==> macd : {imp_macd_curr:>5}, signal : {imp_macd_sign_curr:>5}'
            all_sells.append(msg)
        else:
            msg = f'HODL COND: {freq} impulse macd > signal ==> macd : {imp_macd_curr:>5}, signal : {imp_macd_sign_curr:>5}'
            all_hodls.append(msg)

        # MACD Line Should Be Green or Lime
        imp_macd_color = ta[freq]['imp_macd_color']['ago0']
        if imp_macd_color in ('red','orange'):
            imp_macd_color_ok_tf = True
            msg = f'SELL COND: {freq} impulse macd color must be lime or green ==> macd color : {imp_macd_color:>5}'
            all_sells.append(msg)
        else:
            imp_macd_color_ok_tf = False
            msg = f'HODL COND: {freq} impulse macd color must be lime or green ==> macd color : {imp_macd_color:>5}'
            all_hodls.append(msg)

        if imp_macd_curr and imp_macd_color_ok_tf:
            pos.sell_yn  = 'Y'

        if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
        msg = '    SELL TESTS - Impluse MACD'
        mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, pst=pst, all_sells=all_sells, all_hodls=all_hodls)


        pos = exit_if_logic(pos=pos, pst=pst)


        if pos.sell_yn == 'Y':
            pos.sell_strat_type = 'strat'
            pos.sell_strat_name = 'imp_macd'
            pos.sell_strat_freq = freq
            pos.hodl_yn = 'N'
        else:
            pos.sell_yn = 'N'
            pos.hodl_yn = 'Y'

    except Exception as e:
        traceback.print_exc()
        traceback.print_stack()
        print_adv(2)
        pass

    
    return mkt, pos, ta

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

