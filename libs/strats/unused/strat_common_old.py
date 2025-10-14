#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#


 
#<=====>#
# Imports
#<=====>#
from libs.bot_theme import chart_row
from fstrent_colors import cs
from libs.bot_common import freqs_get


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_strats'
log_name      = 'bot_strats'


# <=====>#
# Assignments Pre
# <=====>#

spacer = cs(' ' * 4, font_color='white', bg_color='black')

#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#


def disp_sell_tests(msg, mkt, pos, pst, all_sells, all_hodls):
    prod_id = pos.prod_id
    if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pst.sell.show_tests_yn in ('Y','F'):
        msg = spacer + cs('==> ' + msg + f' * sell => {pos.sell_yn} * sell_block => {pos.sell_block_yn} * hodl => {pos.hodl_yn}', font_color='cyan', bg_color='black')
        chart_row(msg)
        if (pos.sell_yn == 'Y' and pos.sell_block_yn == 'N') or pst.sell.show_tests_yn in ('Y'):
            for e in all_sells:
                if pos.prc_chg_pct > 0:
                    e = spacer + cs('* ' + e, font_color='green')
                    chart_row(e)
                else:
                    e = spacer + cs('* ' + e, font_color='red')
                    chart_row(e)
                mkt.show_sell_header_tf = True
            for e in all_hodls:
                e = spacer + cs('* ' + e, font_color='white', bg_color='green')
                chart_row(e)
                mkt.show_sell_header_tf = True
#            chart_row(f'sell_yn : {pos.sell_yn}, hodl_yn : {pos.hodl_yn}')
    
    return mkt

#<=====>#


def exit_if_logic(pos, pst):
    exit_if_profit_yn      = pst.sell.strats[pos.buy_strat_name].exit_if_profit_yn
    exit_if_profit_pct_min = pst.sell.strats[pos.buy_strat_name].exit_if_profit_pct_min
    exit_if_loss_yn        = pst.sell.strats[pos.buy_strat_name].exit_if_loss_yn
    exit_if_loss_pct_max   = abs(pst.sell.strats[pos.buy_strat_name].exit_if_loss_pct_max) * -1

    if pos.sell_yn == 'Y':
        if pos.prc_chg_pct > 0:
            if exit_if_profit_yn == 'Y':
                if pos.prc_chg_pct < exit_if_profit_pct_min:
                    msg = ''
                    msg += spacer 
                    msg += cs(f'==> exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_profit_pct_min : {exit_if_profit_pct_min}, cancelling sell...', font_color='blue', bg_color='white')
                    print(msg)
                    pos.sell_yn = 'N'
                    pos.hodl_yn = 'Y'
            elif exit_if_profit_yn == 'N':
                msg = ''
                msg += spacer 
                msg += cs(f'==> exit_if_profit_yn : {exit_if_profit_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...', font_color='blue', bg_color='white')
                if pst.sell.show_tests_yn == 'Y':
                    print(msg)
                pos.sell_yn = 'N'
                pos.hodl_yn = 'Y'
        elif pos.prc_chg_pct <= 0:
            if exit_if_loss_yn == 'Y':
                if pos.prc_chg_pct > exit_if_loss_pct_max:
                    msg = ''
                    msg += spacer 
                    msg += cs(f'==> exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - pos.prc_chg_pct : {pos.prc_chg_pct} % < exit_if_loss_pct_max : {exit_if_loss_pct_max}, cancelling sell...', font_color='blue', bg_color='white')
                    print(msg)
                    print(msg)
                    pos.sell_yn = 'N'
                    pos.hodl_yn = 'Y'
            elif exit_if_loss_yn == 'N':
                msg = ''
                msg += spacer 
                msg += cs(f'==> exit_if_loss_yn : {exit_if_loss_yn}, {pos.buy_strat_name} {pos.buy_strat_freq} - cancelling sell...', font_color='blue', bg_color='white')
                if pst.sell.show_tests_yn == 'Y':
                    print(msg)
                pos.sell_yn = 'N'
                pos.hodl_yn = 'Y'

    
    return pos

#<=====>#

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#

