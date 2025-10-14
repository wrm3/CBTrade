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
from fstrent_colors import cs
from libs.bot_common import freqs_get
from libs.bot_strat_common import disp_sell_tests, exit_if_logic
import traceback



#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strat_drop'
log_name      = 'bot_strat_drop'


# <=====>#
# Assignments Pre
# <=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#



def buy_strat_settings_drop(st):
    buy_strat_st = {
                    "use_yn": "Y",
                    "freqs": ["1d", "4h", "1h", "30min", "15min"],
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
                    "skip_prod_ids": [],
                    "tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
                    "boost_tests_min": {"15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11},
                    "show_tests_yn": "Y"
                    }
    st['buy']['strats']['drop'] = buy_strat_st
    return st

#<=====>#

def sell_strat_settings_drop(st):
    sell_strat_st = {
                    "exit_if_profit_yn": "Y",
                    "exit_if_profit_pct_min": 1,
                    "exit_if_loss_yn": "N",
                    "exit_if_loss_pct_max": 3,
                    "skip_prod_ids": [],
                    "tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
                    "show_tests_yn": "Y"
                    }
    st['sell']['strats']['drop'] = sell_strat_st
    return st

#<=====>#

def buy_strat_settings_emax(st):
    buy_strat_st = {
                    "use_yn": "N",
                    "freqs": ["1d", "4h", "1h", "30min", "15min"],
                    "per_fast": 8,
                    "per_mid": 13,
                    "per_slow": 21,
                    "prod_ids": [],
                    "skip_prod_ids": [],
                    "tests_min": {"***": 15, "15min": 13, "30min": 11, "1h": 9, "4h": 7, "1d": 5},
                    "boost_tests_min": {"15min": 27, "30min": 23, "1h": 19, "4h": 15, "1d": 11},
                    "show_tests_yn": "Y"
                    }
    st['buy']['strats']['sha'] = buy_strat_st
    return st

#<=====>#

# Drop
def buy_strat_drop(buy, ta, pst):
    try:
        all_passes       = []
        all_fails        = []
        prod_id          = buy.prod_id
        buy.buy_yn       = 'Y'
        buy.wait_yn      = 'N'
        buy.show_tests_yn = buy.pst.buy.strats.drop.show_tests_yn

        buy.rfreq = buy.trade_strat_perf.buy_strat_freq
        freqs, faster_freqs     = freqs_get(buy.rfreq)
        freqs = ['5min','15min']
        faster_freqs = ['5min']

        # Price has recent x% drop below recent high
        max24 = buy.ta['1h']['max24']['ago0']
        drop_pct     = buy.pst.buy.strats.drop.drop_pct
        drop_pct_dec = (100-drop_pct) / 100
        target_prc   = max24 * drop_pct_dec

        # if prod_id == 'BTC-USDC' and buy.rfreq == '1h':
        #     ago_list = ['ago0','ago1','ago2','ago3']
        #     dipped_tf = False
        #     for ago in ago_list:
        #         prc_drop_pct = round(((buy.prc_buy - max24) / max24) * 100, 2)
        #         if buy.prc_buy < target_prc:
        #             dipped_tf = True

        #     if dipped_tf:
        #         msg = f'    * RESERVES UNLOCKED * : recent ({ago}) current price {buy.prc_buy:>.8f} below {drop_pct:>.2f}% below max24 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
        #         BoW(msg)
        #         if buy.budget.reserve_locked_tf:
        #             buy.budget.reserve_locked_tf = False
        #             speak('UNLOCKING RESERVES')
        #     else:
        #         msg = f'    * RESERVES LOCKED * : recent ({ago}) current price {buy.prc_buy:>.8f} below {drop_pct:>.2f}% below max24 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
        #         GoW(msg)
        #         if not buy.budget.reserve_locked_tf:
        #            buy.budget.reserve_locked_tf = True

        ago_list = ['ago0','ago1','ago2','ago3']
        dipped_tf = False
        for ago in ago_list:
            prc_drop_pct = round(((buy.prc_buy - max24) / max24) * 100, 2)
            msg = f'recent ({ago}) current price {buy.prc_buy:>.8f} below {drop_pct:>.2f}% below max30 : {max24:>.8f} target_prc : {target_prc:>.8f} prc_drop_pct : {prc_drop_pct:>.2f}%'
            if buy.prc_buy < target_prc:
                dipped_tf = True
                all_passes.append(msg)
            else:
                all_fails.append(msg)
        if not dipped_tf:
            buy.buy_yn  = 'N'


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
            buy.buy_strat_type  = 'dn'
            buy.buy_strat_name  = 'drop'
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

def sell_strat_drop(mkt, pos, ta, pst):
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
        msg = '    SELL TESTS - Drop'
        mkt = disp_sell_tests(msg=msg, mkt=mkt, pos=pos, pst=pst, all_sells=all_sells, all_hodls=all_hodls)

        exit_if_profit_yn      = pst.sell.strats.drop.exit_if_profit_yn
        exit_if_profit_pct_min = pst.sell.strats.drop.exit_if_profit_pct_min
        exit_if_loss_yn        = pst.sell.strats.drop.exit_if_loss_yn
        exit_if_loss_pct_max   = abs(pst.sell.strats.drop.exit_if_loss_pct_max) * -1
        if pos.sell_yn == 'Y':
            if pos.prc_chg_pct > 0:
                if exit_if_profit_yn == 'Y':
                    if pos.prc_chg_pct < exit_if_profit_pct_min:
                        msg = ''
                        msg += '    ' 
                        msg += cs(f'==> exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...', font_color='blue', bg_color='white')
                        print(msg)
                        pos.sell_yn = 'N'
                        pos.hodl_yn = 'Y'
                elif exit_if_profit_yn == 'N':
                    msg = ''
                    msg += '    ' 
                    msg += cs(f'==> exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...', font_color='blue', bg_color='white')
                    if pst.sell.show_tests_yn == 'Y':
                        print(msg)
                    pos.sell_yn = 'N'
                    pos.hodl_yn = 'Y'
            elif pos.prc_chg_pct <= 0:
                if exit_if_loss_yn == 'Y':
                    if pos.prc_chg_pct > exit_if_loss_pct_max:
                        msg = ''
                        msg += '    ' 
                        msg += cs(f'==> exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...', font_color='blue', bg_color='white')
                        print(msg)
                        print(msg)
                        pos.sell_yn = 'N'
                        pos.hodl_yn = 'Y'
                elif exit_if_loss_yn == 'N':
                    msg = ''
                    msg += '    ' 
                    msg += cs(f'==> exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...', font_color='blue', bg_color='white')
                    if pst.sell.show_tests_yn == 'Y':
                        print(msg)
                    pos.sell_yn = 'N'
                    pos.hodl_yn = 'Y'

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

