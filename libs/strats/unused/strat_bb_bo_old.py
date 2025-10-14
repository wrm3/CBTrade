#<=====>#
# Description
#<=====>#


 
#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from libs.common import beep, print_adv
from libs.bot_common import freqs_get
from libs.bot_strat_common import disp_sell_tests, exit_if_logic
import traceback

#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strat_bb_bo'
log_name      = 'bot_strat_bb_bo'


# <=====>#
# Assignments Pre
# <=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#


#<=====>#


def buy_strat_settings_bb_bo(st):
    buy_strat_st = {
                    "use_yn": "Y",
                    "freqs": ["1d", "4h", "1h", "30min", "15min"],
                    "per": 21,
                    "sd": 2.1,
                    "prod_ids": [],
                    "skip_prod_ids": [],
                    "tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
                    "boost_tests_min": {"15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11},
                    "show_tests_yn": "Y"
                    }
    st['buy']['strats']['bb_bo'] = buy_strat_st
    return st

#<=====>#

def sell_strat_settings_bb_bo(st):
    sell_strat_st = {
                    "exit_if_profit_yn": "Y",
                    "exit_if_profit_pct_min": 1,
                    "exit_if_loss_yn": "N",
                    "exit_if_loss_pct_max": 3,
                    "skip_prod_ids": [],
                    "tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
                    "show_tests_yn": "Y"
                    }
    st['sell']['strats']['bb_bo'] = sell_strat_st
    return st

#<=====>#

# Bollinger Band Breakout
def buy_strat_bb_bo(buy, ta, pst):
    try:
        all_passes       = []
        all_fails        = []
        prod_id          = buy.prod_id
        buy.buy_yn           = 'Y'
        buy.wait_yn          = 'N'
        buy.show_tests_yn = buy.pst.buy.strats.bb_bo.show_tests_yn

        buy.rfreq = buy.trade_strat_perf.buy_strat_freq
        freqs, faster_freqs     = freqs_get(buy.rfreq)

#        # General Trend
#        check_list = ['sma100']
#        for x in check_list:
#            sma = ta[rfreq][x]['ago0']
#            msg = f'{rfreq} Current Price : {buy.prc_buy:>.8f} must be above current {x} : {sma}'
#            if not sma:
#                buy.buy_yn  = 'N'
#                all_fails.append(msg)
#            elif buy.prc_buy > sma:
#                all_passes.append(msg)
#            else:
#                buy.buy_yn  = 'N'
#                all_fails.append(msg)

        # Current High Above Inner BB Lower
        m = 'current {} high : {:>.8f} above bb upper : {:>.8f}'
        msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['high']['ago0'], buy.ta[buy.rfreq]['bb_upper_bb_bo']['ago0'])
        if buy.ta[buy.rfreq]['high']['ago0'] > buy.ta[buy.rfreq]['bb_upper_bb_bo']['ago0']:
            all_passes.append(msg)
        else:
            buy.buy_yn  = 'N'
            all_fails.append(msg)

        # Current Close Above Inner BB Lower
        m = 'pervious {} close : {:>.8f} above bb upper : {:>.8f}'
        msg = m.format(buy.rfreq, buy.ta[buy.rfreq]['close']['ago1'], buy.ta[buy.rfreq]['bb_upper_bb_bo']['ago1'])
        if buy.ta[buy.rfreq]['close']['ago1'] > buy.ta[buy.rfreq]['bb_upper_bb_bo']['ago1']:
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

        if buy.buy_yn == 'Y':
            buy.wait_yn = 'N'
            buy.buy_strat_type  = 'up'
            buy.buy_strat_name  = 'bb_bo'
            buy.buy_strat_freq  = buy.rfreq
        else:
            buy.wait_yn = 'Y'

        buy.trade_strat_perf.pass_cnt     = len(all_passes)
        buy.trade_strat_perf.fail_cnt     = len(all_fails)
        buy.trade_strat_perf.total_cnt    = buy.trade_strat_perf.pass_cnt + buy.trade_strat_perf.fail_cnt
        buy.trade_strat_perf.pass_pct     = round((buy.trade_strat_perf.pass_cnt / buy.trade_strat_perf.total_cnt) * 100, 2)
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

def sell_strat_bb_bo(mkt, pos, ta, pst):
    try:
        sell_prc    = mkt.prc_sell
        all_sells   = []
        all_hodls   = []

        rfreq = pos.buy_strat_freq
        freq = pos.buy_strat_freq

        age_mins          = pos.age_mins
        if freq == '15min':
            min_mins = 15
        elif freq == '30min':
            min_mins = 30
        elif freq == '1h':
            min_mins = 60
        elif freq == '4h':
            min_mins = 240
        elif freq == '1d':
            min_mins = 1440

        if age_mins > min_mins and pos.gain_loss_pct_est < -3:
            msg = f'SELL COND: {rfreq} pos.gain_loss_pct_est < -3 : {pos.gain_loss_pct_est}'
            pos.sell_yn  = 'Y'
            all_sells.append(msg)
        else:
            pos.sell_yn  = 'N'

        if pos.sell_yn == 'Y': pos.hodl_yn = 'N'
        msg = '    SELL TESTS - Bollinger Bands Breakout'
        mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, pst=pst, all_sells=all_sells, all_hodls=all_hodls)

        exit_if_profit_yn      = pst.sell.strats.drop.exit_if_profit_yn
        exit_if_profit_pct_min = pst.sell.strats.drop.exit_if_profit_pct_min
        exit_if_loss_yn        = pst.sell.strats.drop.exit_if_loss_yn
        exit_if_loss_pct_max   = abs(pst.sell.strats.drop.exit_if_loss_pct_max) * -1

        pos = exit_if_logic(pos=pos, pst=pst)

        if pos.sell_yn == 'Y':
            pos.sell_strat_type = 'strat'
            pos.sell_strat_name = pos.buy_strat_name
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

