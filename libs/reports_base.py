#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
from datetime import datetime
import pandas as pd
import pytz

from fstrent_colors import *
from libs.common import (
    AttrDict
    , AttrDictEnh
    , format_disp_age
    , print_adv
    , narc
)
from libs.db_mysql.cbtrade.db_main import CBTRADE_DB
cbtrade_db = CBTRADE_DB()  # Create instance for backward compatibility

from libs.theme import (
    chart_bottom, chart_headers, chart_mid, 
    chart_row, chart_top,
    cs_pct_color, cs_pct_color_50, cs_pct_color_green_gradient
)

#<=====>#
# Variables
#<=====>#
lib_name      = 'reports_base'
log_name      = 'reports_base'


#<=====>#
# Assignments Pre
#<=====>#
debug_tf = False

#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

@narc(1)
def disp_recent(show_pos_close_header_yn='Y'):
    if debug_tf: G(f'==> reports_base.disp_recent()')
    print_adv(2)

    hmsg = ""
    hmsg += f"{'mkt':^16} | "
    hmsg += f"{'pos_id':^7} | "
    hmsg += f"{'strat':^10} | "
    hmsg += f"{'freq':^5} | "
    hmsg += f"{'sell':^14} | "
    hmsg += f"{'age':^10} | "
    hmsg += f"{'sold @ utc':^16} | "
    hmsg += f"{'buy_val':^17} | "
    hmsg += f"{'buy_prc':^15} | "
    hmsg += f"{'curr_prc':^15} | "
    hmsg += f"{'high_prc':^15} | "
    hmsg += f"{'gain_pct':^8} % | "
    hmsg += f"{'gain_est':^8} % | "
    hmsg += f"{'gain_top':^8} % | "
    hmsg += f"{'drop_pct':^8} % | "
    hmsg += f"{'gain_loss':^15} | "
    hmsg += f"{'gain_loss_est':^15} | "
    hmsg += f"{'gain_loss_high':^15}"

    title = 'Recently Closed Positions'
    show_pos_close_header_yn = 'Y'
    if show_pos_close_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg, align='center')
        chart_mid()
        show_pos_close_header_yn = 'N'

    poss = cbtrade_db.db_poss_close_recent_get(lmt=20)
    if poss:
        for pos in poss:
            pos = AttrDict(pos)
            if pos.test_txn_yn == 'N': pos.test_txn_yn = ''
            pos.pos_end_dttm = pos.pos_end_dttm.strftime('%m-%d-%Y %H:%M')
            disp_age = format_disp_age(pos.age_mins)

            msg = ''
            msg += f'{pos.prod_id:<16} | '
            msg += f'{pos.pos_id:^7} | '
            msg += f'{pos.buy_strat_name:>10} | '
            msg += f'{pos.buy_strat_freq:>5} | '
            msg += f'{pos.sell_strat_name:>14} | '
            msg += f'{disp_age:>10} | '
            msg += f"{pos.pos_end_dttm:>16} | "
            msg += f'$ {pos.tot_out_cnt:>15.8f} | '
            msg += f'{pos.prc_buy:>15.8f} | '
            msg += f'{pos.prc_curr:>15.8f} | '
            msg += f'{pos.prc_high:>15.8f} | '
            msg += f'{pos.gain_loss_pct:>8.2f} % | ' # Open Shows Estimates, Closed Shows Actual
            msg += f'{pos.gain_loss_pct_est:>8.2f} % | '  # Open Shows Estimates, Closed Shows Actual
            msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
            msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
            msg += f'{pos.gain_loss_amt:>15.8f} | '
            msg += f'{pos.gain_loss_amt_est:>15.8f} | '   # Open Shows Estimates, Closed Shows Actual
            msg += f'{pos.gain_loss_amt_est_high:>15.8f}'

            msg = cs_pct_color(pos.prc_chg_pct, msg)
            chart_row(in_str=msg)

    print_adv(2)

    hmsg = ''
    hmsg += f"{'mkt':^16} | "
    hmsg += f"{'pos_id':^7} | "
    hmsg += f"{'strat':^10} | "
    hmsg += f"{'freq':^10} | "
    hmsg += f"{'age':^10} | "
    hmsg += f"{'open @ est':^16} | "
    hmsg += f"{'buy_val':^17} | "
    hmsg += f"{'buy_prc':^15} | "
    hmsg += f"{'curr_prc':^15} | "
    hmsg += f"{'high_prc':^15} | "
    hmsg += f"{'gain_pct':^8} % | "
    hmsg += f"{'gain_top':^8} % | "
    hmsg += f"{'drop_pct':^8} % | "
    hmsg += f"{'gain_loss':^15} | "
    hmsg += f"{'gain_loss_high':^15}"

    title = 'Currently Open Positions - By Market'
    show_pos_close_header_yn = 'Y'
    if show_pos_close_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg, align='center')
        chart_mid()
        show_pos_close_header_yn = 'N'

    poss = cbtrade_db.db_poss_open_get(live_only_yn='Y')
    if poss:
        for pos in poss:
            pos = AttrDict(pos)
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            disp_age = format_disp_age(pos.age_mins)

            msg = ''
            msg += f'{pos.prod_id:<16} | '
            msg += f'{pos.pos_id:^6} | '
            msg += f'{pos.buy_strat_name:>10} | '
            msg += f'{pos.buy_strat_freq:>10} | '
            msg += f'{disp_age:>10} | '
            msg += f"{pos.pos_begin_dttm:>16} | "
            msg += f'$ {pos.tot_out_cnt:>15.8f} | '
            msg += f'{pos.prc_buy:>15.8f} | '
            msg += f'{pos.prc_curr:>15.8f} | '
            msg += f'{pos.prc_high:>15.8f} | '
            msg += f'{pos.gain_loss_pct:>8.2f} % | '
            msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
            msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
            msg += f'{pos.gain_loss_amt:>15.8f} | '
            msg += f'{pos.gain_loss_amt_est_high:>15.8f}'

            msg = cs_pct_color(pos.prc_chg_pct, msg)
            chart_row(in_str=msg)

    print_adv(2)

    hmsg = ''
    hmsg += f"{'mkt':^16} | "
    hmsg += f"{'pos_id':^6} | "
    hmsg += f"{'strat':^10} | "
    hmsg += f"{'freq':^10} | "
    hmsg += f"{'age':^10} | "
    hmsg += f"{'open @ est':^16} | "
    hmsg += f"{'buy_val':^17} | "
    hmsg += f"{'buy_prc':^15} | "
    hmsg += f"{'curr_prc':^15} | "
    hmsg += f"{'high_prc':^15} | "
    hmsg += f"{'gain_pct':^8} % | "
    hmsg += f"{'gain_top':^8} % | "
    hmsg += f"{'drop_pct':^8} % | "
    hmsg += f"{'gain_loss':^15} | "
    hmsg += f"{'gain_loss_high':^15}"

    title = 'Currently Open Positions - By Age Desc'
    show_pos_close_header_yn = 'Y'
    if show_pos_close_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg, align='center')
        chart_mid()
        show_pos_close_header_yn = 'N'

    if poss:
        poss_sorted = sorted(poss, key=lambda x: x["age_mins"], reverse=True)
        poss = poss_sorted

        for pos in poss:
            pos = AttrDict(pos)
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            disp_age = format_disp_age(pos.age_mins)

            msg = ''
            msg += f'{pos.prod_id:<16} | '
            msg += f'{pos.pos_id:^6} | '
            msg += f'{pos.buy_strat_name:>10} | '
            msg += f'{pos.buy_strat_freq:>10} | '
            msg += f'{disp_age:>10} | '
            msg += f"{pos.pos_begin_dttm:>16} | "
            msg += f'$ {pos.tot_out_cnt:>15.8f} | '
            msg += f'{pos.prc_buy:>15.8f} | '
            msg += f'{pos.prc_curr:>15.8f} | '
            msg += f'{pos.prc_high:>15.8f} | '
            msg += f'{pos.gain_loss_pct:>8.2f} % | '
            msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
            msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
            msg += f'{pos.gain_loss_amt:>15.8f} | '
            msg += f'{pos.gain_loss_amt_est_high:>15.8f}'

            msg = cs_pct_color(pos.prc_chg_pct, msg)
            chart_row(in_str=msg)


#<=====>#



#<=====>#

@narc(1)
def disp_open_overview(title, out_ovr, show_header_yn='Y'):
    if debug_tf: G(f'==> reports_base.disp_open_overview()')
    out_ovr = AttrDict(out_ovr)

# def disp_open_overview(quote_symb=None, lta=None, cnt=15):
    # out_ovrs = db.db_open_overview(quote_symb=quote_symb, lta=lta, cnt=cnt)

    hmsg = ''
    hmsg += f"{'mkt*':^14} | "
    hmsg += f"{'T':^1} | "
    hmsg += f"{'open':^9} | "
    hmsg += f"{'win_cnt':^9} | "
    hmsg += f"{'loss_cnt':^9} | "
    hmsg += f"$ {'spent':^12} | "
    hmsg += f"$ {'win_spent':^12} | "
    hmsg += f"$ {'loss_spent':^12} | "
    hmsg += f"$ {'gain_loss':^12} | "
    hmsg += f"$ {'gains':^12} | "
    hmsg += f"$ {'losses':^12} | "

    if show_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg)
        chart_mid()
        show_header_yn = 'N'

    msg = ''
    msg += f'{out_ovr.symb:<14} | '
    msg += f'{out_ovr.test_txn_yn:^1} | '
    msg += f'{out_ovr.open:^9} | '
    msg += f'{int(out_ovr.win_cnt):>9} | '
    msg += f'{int(out_ovr.loss_cnt):>9} | '
    msg += f'$ {out_ovr.spent:>12.2f} | '
    msg += f'$ {out_ovr.win_spent:>12.2f} | '
    msg += f'$ {out_ovr.loss_spent:>12.2f} | '

    if out_ovr.gain_loss > 0:
        msg += cs(f'$ {out_ovr.gain_loss:>12.2f}', "white", "green") + ' | '
    elif out_ovr.gain_loss < 0:
        msg += cs(f'$ {out_ovr.gain_loss:>12.2f}', "white", "red") + ' | '
    else:
        msg += f'{out_ovr.gain_loss:>12.2f} | '

    if out_ovr.gains > 0:
        msg += cs(f'$ {out_ovr.gains:>12.2f}', "white", "green") + ' | '
    else:
        msg += f'$ {out_ovr.gains:>12.2f} | '

    if out_ovr.losses < 0:
        msg += cs(f'$ {out_ovr.losses:>12.2f}', "white", "red") + ' | '
    else:
        msg += f'$ {out_ovr.losses:>12.2f} | '

    chart_row(msg)

#<=====>#

@narc(1)
def disp_close_overview(title, out_ovr, show_header_yn='Y'):
    if debug_tf: G(f'==> reports_base.disp_close_overview()')
    out_ovr = AttrDict(out_ovr)

    hmsg = ''
    hmsg += f"{'mkt*':^14} | "
    hmsg += f"{'T':^1} | "
    hmsg += f"{'open':^9} | "
    hmsg += f"{'win_cnt':^9} | "
    hmsg += f"{'loss_cnt':^9} | "
    hmsg += f"$ {'spent':^12} | "
    hmsg += f"$ {'win_spent':^12} | "
    hmsg += f"$ {'loss_spent':^12} | "
    hmsg += f"$ {'gain_loss':^12} | "
    hmsg += f"$ {'gains':^12} | "
    hmsg += f"$ {'losses':^12} | "

    if show_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg)
        chart_mid()
        show_header_yn = 'N'

    # print(out_ovr)

    msg = ''
    msg += f'{out_ovr.symb:<14} | '
    msg += f'{out_ovr.test_txn_yn:^1} | '
    msg += f'{out_ovr.closed:^9} | '
    msg += f'{int(out_ovr.close_win_cnt):>9} | '
    msg += f'{int(out_ovr.close_loss_cnt):>9} | '
    msg += f'$ {out_ovr.close_spent:>12.2f} | '
    msg += f'$ {out_ovr.close_win_spent:>12.2f} | '
    msg += f'$ {out_ovr.close_loss_spent:>12.2f} | '

    if out_ovr.close_gain_loss > 0:
        msg += cs(f'$ {out_ovr.close_gain_loss:>12.2f}', "white", "green") + ' | '
    elif out_ovr.close_gain_loss < 0:
        msg += cs(f'$ {out_ovr.close_gain_loss:>12.2f}', "white", "red") + ' | '
    else:
        msg += f'{out_ovr.close_gain_loss:>12.2f} | '

    if out_ovr.close_gains > 0:
        msg += cs(f'$ {out_ovr.close_gains:>12.2f}', "white", "green") + ' | '
    else:
        msg += f'$ {out_ovr.close_gains:>12.2f} | '

    if out_ovr.close_losses < 0:
        msg += cs(f'$ {out_ovr.close_losses:>12.2f}', "white", "red") + ' | '
    else:
        msg += f'$ {out_ovr.close_losses:>12.2f} | '

    chart_row(msg)



#<=====>#

@narc(1)
def disp_open_overview2(title, out_ovr, show_header_yn='Y'):
    if debug_tf: G(f'==> reports_base.disp_open_overview2()')
    out_ovr = AttrDict(out_ovr)

    hmsg = ''
    hmsg += f"{'mkt*':^14} | "
    hmsg += f"{'T':^1} | "
    hmsg += f"{'open':^9} | "
    hmsg += f"{'win_cnt':^9} | "
    hmsg += f"{'loss_cnt':^9} | "
    hmsg += f"$ {'spent':^12} | "
    hmsg += f"$ {'win_spent':^12} | "
    hmsg += f"$ {'loss_spent':^12} | "
    hmsg += f"$ {'gain_loss':^12} | "
    hmsg += f"$ {'gains':^12} | "
    hmsg += f"$ {'losses':^12} | "

    if show_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg)
        chart_mid()
        show_header_yn = 'N'

    msg = ''
    msg += f'{out_ovr.symb:<14} | '
    msg += f'{out_ovr.test_txn_yn:^1} | '
    msg += f'{out_ovr.open:^9} | '
    msg += f'{int(out_ovr.win_cnt):>9} | '
    msg += f'{int(out_ovr.loss_cnt):>9} | '
    msg += f'$ {out_ovr.spent:>12.2f} | '
    msg += f'$ {out_ovr.win_spent:>12.2f} | '
    msg += f'$ {out_ovr.loss_spent:>12.2f} | '

    if out_ovr.gain_loss > 0:
        msg += cs(f'$ {out_ovr.gain_loss:>12.2f}', "white", "green") + ' | '
    elif out_ovr.gain_loss < 0:
        msg += cs(f'$ {out_ovr.gain_loss:>12.2f}', "white", "red") + ' | '
    else:
        msg += f'{out_ovr.gain_loss:>12.2f} | '

    if out_ovr.gains > 0:
        msg += cs(f'$ {out_ovr.gains:>12.2f}', "white", "green") + ' | '
    else:
        msg += f'$ {out_ovr.gains:>12.2f} | '

    if out_ovr.losses < 0:
        msg += cs(f'$ {out_ovr.losses:>12.2f}', "white", "red") + ' | '
    else:
        msg += f'$ {out_ovr.losses:>12.2f} | '

    chart_row(msg)

#<=====>#

@narc(1)
def disp_close_overview2(title, out_ovr, show_header_yn='Y'):
    if debug_tf: G(f'==> reports_base.disp_close_overview2()')
    out_ovr = AttrDict(out_ovr)

    hmsg = ''
    hmsg += f"{'mkt*':^14} | "
    hmsg += f"{'T':^1} | "
    hmsg += f"{'open':^9} | "
    hmsg += f"{'win_cnt':^9} | "
    hmsg += f"{'loss_cnt':^9} | "
    hmsg += f"$ {'spent':^12} | "
    hmsg += f"$ {'win_spent':^12} | "
    hmsg += f"$ {'loss_spent':^12} | "
    hmsg += f"$ {'gain_loss':^12} | "
    hmsg += f"$ {'gains':^12} | "
    hmsg += f"$ {'losses':^12} | "

    if show_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg)
        chart_mid()
        show_header_yn = 'N'

    msg = ''
    msg += f'{out_ovr.symb:<14} | '
    msg += f'{out_ovr.test_txn_yn:^1} | '
    msg += f'{out_ovr.open:^9} | '
    msg += f'{int(out_ovr.win_cnt):>9} | '
    msg += f'{int(out_ovr.loss_cnt):>9} | '
    msg += f'$ {out_ovr.spent:>12.2f} | '
    msg += f'$ {out_ovr.win_spent:>12.2f} | '
    msg += f'$ {out_ovr.loss_spent:>12.2f} | '

    if out_ovr.gain_loss > 0:
        msg += cs(f'$ {out_ovr.gain_loss:>12.2f}', "white", "green") + ' | '
    elif out_ovr.gain_loss < 0:
        msg += cs(f'$ {out_ovr.gain_loss:>12.2f}', "white", "red") + ' | '
    else:
        msg += f'{out_ovr.gain_loss:>12.2f} | '

    if out_ovr.gains > 0:
        msg += cs(f'$ {out_ovr.gains:>12.2f}', "white", "green") + ' | '
    else:
        msg += f'$ {out_ovr.gains:>12.2f} | '

    if out_ovr.losses < 0:
        msg += cs(f'$ {out_ovr.losses:>12.2f}', "white", "red") + ' | '
    else:
        msg += f'$ {out_ovr.losses:>12.2f} | '

    chart_row(msg)


#<=====>#

@narc(1)
def disp_close_overview_daily(title, out_ovr, show_header_yn='Y'):
    if debug_tf: G(f'==> reports_base.disp_close_overview_daily()')
    out_ovr = AttrDict(out_ovr)

    hmsg = ''
    hmsg += f"{'date':^12} | "
    hmsg += f"{'mkt*':^8} | "
    hmsg += f"{'T':^1} | "
    hmsg += f"{'closed':^8} | "
    hmsg += f"{'win':^6} | "
    hmsg += f"{'loss':^6} | "
    hmsg += f"$ {'spent':^10} | "
    hmsg += f"$ {'w_spent':^10} | "
    hmsg += f"$ {'l_spent':^10} | "
    hmsg += f"$ {'gain_loss':^10} | "
    hmsg += f"$ {'gains':^10} | "
    hmsg += f"$ {'losses':^10} | "

    if show_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg)
        chart_mid()
        show_header_yn = 'N'

    # print(out_ovr)

    msg = ''
    # Ensure date renders correctly as YYYY-MM-DD and aligns to 12 chars
    _cd = out_ovr.close_date
    try:
        if hasattr(_cd, 'strftime'):
            # datetime/date object
            date_str = _cd.strftime('%Y-%m-%d')
        else:
            # string or other; trim to date part if includes time
            date_str = str(_cd)
            if len(date_str) >= 10:
                date_str = date_str[:10]
    except Exception:
        date_str = str(_cd)
    msg += f'{date_str:<12} | '
    msg += f'{out_ovr.symb:<8} | '
    msg += f'{out_ovr.test_txn_yn:^1} | '
    msg += f'{out_ovr.closed:^8} | '
    msg += f'{int(out_ovr.close_win_cnt):>6} | '
    msg += f'{int(out_ovr.close_loss_cnt):>6} | '
    msg += f'$ {out_ovr.close_spent:>10.2f} | '
    msg += f'$ {out_ovr.close_win_spent:>10.2f} | '
    msg += f'$ {out_ovr.close_loss_spent:>10.2f} | '

    if out_ovr.close_gain_loss > 0:
        msg += cs(f'$ {out_ovr.close_gain_loss:>10.2f}', "white", "green") + ' | '
    elif out_ovr.close_gain_loss < 0:
        msg += cs(f'$ {out_ovr.close_gain_loss:>10.2f}', "white", "red") + ' | '
    else:
        msg += f'$ {out_ovr.close_gain_loss:>10.2f} | '

    if out_ovr.close_gains > 0:
        msg += cs(f'$ {out_ovr.close_gains:>10.2f}', "white", "green") + ' | '
    else:
        msg += f'$ {out_ovr.close_gains:>10.2f} | '

    if out_ovr.close_losses < 0:
        msg += cs(f'$ {out_ovr.close_losses:>10.2f}', "white", "red") + ' | '
    else:
        msg += f'$ {out_ovr.close_losses:>10.2f} | '

    chart_row(msg)


#<=====>#

@narc(1)
def disp_pos_open(title, pos, show_pos_open_header_yn='Y'):
    if debug_tf: G(f'==> reports_base.disp_pos_open()')
    hmsg = ''
    hmsg += f"{'mkt*':^14} | "
    hmsg += f"{'T':^1} | "
    hmsg += f"{'pos_id':^7} | "
    hmsg += f"{'strat':^10} | "
    hmsg += f"{'freq':^10} | "
    hmsg += f"{'age':^10} | "
    hmsg += f"{'open @ est':^16} | "
    hmsg += f"{'buy_val':^17} | "
    hmsg += f"{'buy_prc':^15} | "
    hmsg += f"{'curr_prc':^15} | "
    hmsg += f"{'high_prc':^15} | "
    hmsg += f"{'gain_pct':^8} % | "
    hmsg += f"{'gain_top':^8} % | "
    hmsg += f"{'drop_pct':^8} % | "
    hmsg += f"{'gain_loss':^15} | "
    hmsg += f"{'gain_loss_high':^15}"

#    hmsg = cs(hmsg, font_color='white', bg_color='blue')

    if show_pos_open_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg)
        chart_mid()
        show_pos_open_header_yn = 'N'

    if pos.test_txn_yn == 'N': pos.test_txn_yn = ''

    msg = ''
    msg += f'{pos.prod_id:<14} | '
    msg += f'{pos.test_txn_yn:^1} | '
    msg += f'{pos.pos_id:^7} | '
    msg += f'{pos.buy_strat_name:>10} | '
    msg += f'{pos.buy_strat_freq:>10} | '
    msg += f'{pos.report_age:>10} | '
    msg += f"{pos.pos_begin_dttm:>16} | "
    msg += f'$ {pos.tot_out_cnt:>15.8f} | '
    msg += f'{pos.prc_buy:>15.8f} | '
    msg += f'{pos.prc_curr:>15.8f} | '
    msg += f'{pos.prc_high:>15.8f} | '
    msg += f'{pos.gain_loss_pct:>8.2f} % | '
    msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
    msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
    msg += f'{pos.gain_loss_amt:>15.8f} | '
    msg += f'{pos.gain_loss_amt_est_high:>15.8f}'

    msg = cs_pct_color(pos.prc_chg_pct, msg)
    chart_row(msg)

#<=====>#

@narc(1)
def disp_pos_close(title, pos, show_pos_close_header_yn='Y'):
    if debug_tf: G(f'==> reports_base.disp_pos_close()')
    hmsg = ""
    hmsg += f"{'mkt':^14} | "
    hmsg += f"{'T':^1} | "
    hmsg += f"{'pos_id':^7} | "
    hmsg += f"{'strat':^10} | "
    hmsg += f"{'freq':^5} | "
    hmsg += f"{'sell':^14} | "
    hmsg += f"{'age':^10} | "
    hmsg += f"{'sold @ est':^16} | "
    hmsg += f"{'buy_val':^17} | "
    hmsg += f"{'buy_prc':^15} | "
    hmsg += f"{'curr_prc':^15} | "
    hmsg += f"{'gain_pct':^8} % | "
    hmsg += f"{'gain_est':^8} % | "
    hmsg += f"{'gain_top':^8} % | "
    hmsg += f"{'drop_pct':^8} % | "
    hmsg += f"{'gain_loss':^15} | "
    hmsg += f"{'gain_loss_est':^15} | "
    hmsg += f"{'gain_loss_high':^15}"

    if show_pos_close_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg, align='center')
        chart_mid()
        show_pos_close_header_yn = 'N'

    pos.pos_end_dttm = datetime.strptime(pos.pos_end_dttm, "%m-%d-%Y %H:%M")
    utc_timezone = pytz.utc
    pos.pos_end_dttm = utc_timezone.localize(pos.pos_end_dttm)
    local_timezone = pytz.timezone('America/New_York')
    pos.pos_end_dttm = pos.pos_end_dttm.astimezone(local_timezone)
    pos.pos_end_dttm = datetime.strftime(pos.pos_end_dttm, "%m-%d-%Y %H:%M")
    if pos.test_txn_yn == 'N': pos.test_txn_yn = ''

    msg = ''
    msg += f'{pos.prod_id:<14} | '
    msg += f'{pos.test_txn_yn:^1} | '
    msg += f'{pos.pos_id:<7} | '
    msg += f'{pos.buy_strat_name:>10} | '
    msg += f'{pos.buy_strat_freq:>5} | '
    msg += f'{pos.sell_strat_name:>14} | '
    msg += f'{pos.report_age:>10} | '
    msg += f"{pos.pos_end_dttm:>16} | "
    msg += f'$ {pos.tot_out_cnt:>15.8f} | '
    msg += f'{pos.prc_buy:>15.8f} | '
    msg += f'{pos.prc_curr:>15.8f} | '
    msg += f'{pos.gain_loss_pct:>8.2f} % | ' # Open Shows Estimates, Closed Shows Actual
    msg += f'{pos.gain_loss_pct_est:>8.2f} % | '  # Open Shows Estimates, Closed Shows Actual
    msg += f'{pos.gain_loss_pct_est_high:>8.2f} % | '
    msg += f'{pos.prc_chg_pct_drop:>8.2f} % | '
    msg += f'{pos.gain_loss_amt:>15.8f} | '
    msg += f'{pos.gain_loss_amt_est:>15.8f} | '   # Open Shows Estimates, Closed Shows Actual
    msg += f'{pos.gain_loss_amt_est_high:>15.8f}'

    msg = cs_pct_color(pos.prc_chg_pct, msg)
    chart_row(msg)

#<=====>#

@narc(1)
def disp_strat(title, mkt_strat_perf, show_strat_header_yn):
    if debug_tf: G(f'==> reports_base.disp_strat()')
    hmsg = ""
    hmsg += f"{'mkt':<15} | "
#    hmsg += f"{'desc':<45} | "
    hmsg += f"{'strat':<15} | "
    hmsg += f"{'freq':<15} | "
    hmsg += f"{'total':^5} | "
    hmsg += f"{'open':^5} | "
    hmsg += f"{'close':^5} | "
    hmsg += f"{'wins':^5} | "
    hmsg += f"{'lose':^5} | "
    hmsg += f"{'win':^6} % | "
    hmsg += f"{'lose':^6} % | "
    hmsg += f"{'gain_amt':^10} | "
    hmsg += f"{'gain_pct':^10} % | "
    hmsg += f"{'gain_hr':^10} % | "
    hmsg += f"{'gain_day':^10} %"
    hmsg = cs(hmsg, font_color='white', bg_color='blue')

    if show_strat_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg, align='left')
        chart_mid()
        show_strat_header_yn = 'N'

    msg = ''
    msg += f'{mkt_strat_perf.prod_id:<15} | '
#    msg += f'{mkt_strat_perf.buy_strat_desc:<45} | '
    msg += f'{mkt_strat_perf.buy_strat_name:<15} | '
    msg += f'{mkt_strat_perf.buy_strat_freq:<15} | '
    msg += f'{int(mkt_strat_perf.tot_cnt):>5} | '
    msg += f'{int(mkt_strat_perf.tot_open_cnt):>5} | '
    msg += f'{int(mkt_strat_perf.tot_close_cnt):>5} | '
    msg += f'{int(mkt_strat_perf.win_cnt):>5} | '
    msg += f'{int(mkt_strat_perf.lose_cnt):>5} | '
    msg += f'{mkt_strat_perf.win_pct:>6.2f} % | '
    msg += f'{mkt_strat_perf.lose_pct:>6.2f} % | '
    msg += f'{mkt_strat_perf.gain_loss_amt:>10.2f} | '
    msg += f'{mkt_strat_perf.gain_loss_pct:>10.2f} % | '
    msg += f'{mkt_strat_perf.gain_loss_pct_hr:>10.2f} % | '
    msg += f'{mkt_strat_perf.gain_loss_pct_day:>10.2f} %'
#    msg += f'{mkt_strat_perf.strat_last_elapsed:>7} | '
    msg = cs_pct_color_50(pct=mkt_strat_perf.win_pct, msg=msg)

    chart_row(in_str=msg)


#<=====>#

@narc(1)
def disp_strat_green_gradient(title, mkt_strat_perf, show_strat_header_yn, max_pct):
    if debug_tf: G(f'==> reports_base.disp_strat_green_gradient()')
    hmsg = ""
    hmsg += f"{'mkt':<15} | "
#    hmsg += f"{'desc':<45} | "
    hmsg += f"{'strat':<15} | "
    hmsg += f"{'freq':<15} | "
    hmsg += f"{'total':^5} | "
    hmsg += f"{'open':^5} | "
    hmsg += f"{'close':^5} | "
    hmsg += f"{'wins':^5} | "
    hmsg += f"{'lose':^5} | "
    hmsg += f"{'win':^6} % | "
    hmsg += f"{'lose':^6} % | "
    hmsg += f"{'gain_amt':^10} | "
    hmsg += f"{'gain_pct':^10} % | "
    hmsg += f"{'gain_hr':^10} % | "
    hmsg += f"{'gain_day':^10} %"
    hmsg = cs(hmsg, font_color='white', bg_color='blue')

    if show_strat_header_yn == 'Y':
        chart_top(in_str=title, align='center')
        chart_headers(in_str=hmsg, align='left')
        chart_mid()
        show_strat_header_yn = 'N'

    msg = ''
    msg += f'{mkt_strat_perf.prod_id:<15} | '
#    msg += f'{mkt_strat_perf.buy_strat_desc:<45} | '
    msg += f'{mkt_strat_perf.buy_strat_name:<15} | '
    msg += f'{mkt_strat_perf.buy_strat_freq:<15} | '
    msg += f'{int(mkt_strat_perf.tot_cnt):>5} | '
    msg += f'{int(mkt_strat_perf.tot_open_cnt):>5} | '
    msg += f'{int(mkt_strat_perf.tot_close_cnt):>5} | '
    msg += f'{int(mkt_strat_perf.win_cnt):>5} | '
    msg += f'{int(mkt_strat_perf.lose_cnt):>5} | '
    msg += f'{mkt_strat_perf.win_pct:>6.2f} % | '
    msg += f'{mkt_strat_perf.lose_pct:>6.2f} % | '
    msg += f'{mkt_strat_perf.gain_loss_amt:>10.2f} | '
    msg += f'{mkt_strat_perf.gain_loss_pct:>10.2f} % | '
    msg += f'{mkt_strat_perf.gain_loss_pct_hr:>10.2f} % | '
    msg += f'{mkt_strat_perf.gain_loss_pct_day:>10.2f} %'
#    msg += f'{mkt_strat_perf.strat_last_elapsed:>7} | '
    msg = cs_pct_color_green_gradient(pct=mkt_strat_perf.gain_loss_pct_day, max_pct=max_pct, msg=msg)

    chart_row(in_str=msg)

#<=====>#

@narc(1)
def disp_strats():
    if debug_tf: G(f'==> reports_base.disp_strats()')
    hf = ''
    mf = ''
    hs = []

    hs.append('mkt')
    hf += '{:^14} | '
    mf += '{:<14} | '

    hs.append('stat')
    hf += '{:^8} | '
    mf += '{:^8} | '

    hs.append('win_cnt')
    hf += '{:^8} | '
    mf += '{:^8} | '

    hs.append('loss_cnt')
    hf += '{:^8} | '
    mf += '{:^8} | '

    hs.append('sell_cnt')
    mf += '{:^8} | '
    hf += '{:^8} | '

    hs.append('spent_amt')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('recv_amt')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('win_amt')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('loss_amt')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('pocket_amt')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('clip_amt')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('hold_amt')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('val_curr')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('fees_tot')
    hf += '{:^10} | '
    mf += '{:>10.2f} | '

    hs.append('gain_loss_amt')
    hf += '{:^21} | '
    mf += '{:>21.8f} | '

    hs.append('gain_loss_amt_est_high')
    hf += '{:^21}'
    mf += '{:>21.8f}'

    header = hf.format(*hs)

    strats = cbtrade_db.db_strats_w_stats_get_all()

    for strat in strats:
        print_adv(2)

        buy_strat_type = strat['buy_strat_type']
        buy_strat_name = strat['buy_strat_name']
        buy_strat_freq = strat['buy_strat_freq']

        WoM('{:^200}'.format('Strategy ==> {} - {} - {}'.format(buy_strat_type.upper(), buy_strat_name.upper(), buy_strat_freq.upper())))

        x = cbtrade_db.db_strats_perf_get_all(buy_strat_type=buy_strat_type, buy_strat_name=buy_strat_name, buy_strat_freq=buy_strat_freq)
        if x:
            win_cnt_tot            = 0
            loss_cnt_tot           = 0
            sell_cnt_tot           = 0
            spent_amt_tot          = 0
            recv_amt_tot           = 0
            win_amt_tot            = 0
            loss_ant_tot           = 0
            hold_amt_tot           = 0
            pocket_amt_tot         = 0
            clip_amt_tot           = 0
            fees_buy_tot           = 0
            fees_sell_tot          = 0
            fees_tot_tot           = 0
            val_tot_tot            = 0
            gain_loss_amt_tot      = 0
            gain_loss_amt_est_high_tot = 0
    
            first_loop_yn = 'Y'
            for r in x:
                if first_loop_yn == 'Y':
                    chart_headers(header, len(header))
                    first_loop_yn = 'N'

                mkt                     = r['mkt']
                pos_stat                = r['pos_stat']
                win_cnt             = int(r['win_cnt'])
                loss_cnt            = int(r['loss_cnt'])
                sell_cnt            = int(r['sell_cnt'])
                spent_amt           = float(r['spent_amt'])
                recv_amt            = float(r['recv_amt'])
                win_amt             = float(r['win_amt'])
                loss_amt            = float(r['loss_amt'])
                hold_amt            = float(r['hold_amt'])
                pocket_amt          = float(r['pocket_amt'])
                clip_amt            = float(r['clip_amt'])
                val_tot             = float(r['val_tot'])
                fees_buy            = float(r['fees_buy'])
                fees_sell           = float(r['fees_sell'])
                fees_tot            = float(r['fees_tot'])
                gain_loss_amt       = float(r['gain_loss_amt'])
                gain_loss_amt_est_high  = float(r['gain_loss_amt_est_high'])

                win_cnt_tot            += win_cnt
                loss_cnt_tot           += loss_cnt
                sell_cnt_tot           += sell_cnt
                spent_amt_tot          += spent_amt
                recv_amt_tot           += recv_amt
                win_amt_tot            += win_amt
                loss_ant_tot           += loss_amt
                hold_amt_tot           += hold_amt
                pocket_amt_tot         += pocket_amt
                clip_amt_tot           += clip_amt
                fees_buy_tot           += fees_buy
                fees_sell_tot          += fees_sell
                fees_tot_tot           += fees_tot
                val_tot_tot            += val_tot
                gain_loss_amt_tot      += gain_loss_amt
                gain_loss_amt_est_high_tot += gain_loss_amt_est_high

                md = []
                md.append(mkt)
                md.append(pos_stat)
                md.append(win_cnt)
                md.append(loss_cnt)
                md.append(sell_cnt)
                md.append(spent_amt)
                md.append(recv_amt)
                md.append(win_amt)
                md.append(loss_amt)
                md.append(pocket_amt)
                md.append(clip_amt)
                md.append(hold_amt)
                md.append(val_tot)
                md.append(fees_tot)
                md.append(gain_loss_amt)
                md.append(gain_loss_amt_est_high)
                msg = mf.format(*md)
                if gain_loss_amt > 0:
                    WoG(msg)
                elif gain_loss_amt < 0:
                    WoR(msg)
                else:
                    print(msg)

            header2 = header
            WoB(header2)

            ms2 = []
            ms2.append('')
            ms2.append('')
            ms2.append(win_cnt_tot)
            ms2.append(loss_cnt_tot)
            ms2.append(sell_cnt_tot)
            ms2.append(spent_amt_tot)
            ms2.append(recv_amt_tot )
            ms2.append(win_amt_tot)
            ms2.append(loss_ant_tot)
            ms2.append(pocket_amt_tot)
            ms2.append(clip_amt_tot)
            ms2.append(hold_amt_tot)
            ms2.append(val_tot_tot)
            ms2.append(fees_tot_tot)
            ms2.append(gain_loss_amt_tot)
            ms2.append(gain_loss_amt_est_high_tot)

            msg2 = mf.format(*ms2)
            if gain_loss_amt_tot > 0:
                WoG(msg2)
            elif gain_loss_amt_tot < 0:
                WoR(msg2)
            else:
                print(msg2)

#<=====>#

@narc(1)
def report_buys_recent(base_symb=None, quote_symb=None, prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None, lta=None, cnt=15):
    if debug_tf: G(f'==> reports_base.report_buys_recent()')
    print_adv(2)

    title = f'Last {cnt} Opened Positions'
    if lta == 'L':
        title = f'Last {cnt} Opened Positions - Live'
        lta = 'L'
    elif lta == 'T':
        title = f'Last {cnt} Opened Positions - Test'
        lta = 'T'
    else:
        lta = None


    poss = cbtrade_db.db_poss_open_recent_get(base_symb=base_symb, quote_symb=quote_symb, prod_id=prod_id, buy_strat_type=buy_strat_type, buy_strat_name=buy_strat_name, buy_strat_freq=buy_strat_freq, lta=lta, lmt=cnt)
    # print(len(poss))

    show_pos_open_header_yn = 'Y'
    if poss:
        for pos in poss:
            pos = AttrDict(pos)
            # 🔴 GILFOYLE: Database now automatically converts _dttm fields
            if pos.test_txn_yn == 'N': pos.test_txn_yn = ''
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_open(title, pos, show_pos_open_header_yn)
            show_pos_open_header_yn = 'N'

        chart_bottom()


#<=====>#

@narc(1)
def report_sells_recent(base_symb=None, quote_symb=None, prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None, lta=None, cnt=15):
    if debug_tf: G(f'==> reports_base.report_sells_recent()')
    print_adv(2)

    title = f'Last {cnt} Closed Positions'
    if lta == 'L':
        title = f'Last {cnt} Closed Positions - Live'
    elif lta == 'T':
        title = f'Last {cnt} Closed Positions - Test'

    poss = cbtrade_db.db_poss_closed_recent_get(base_symb=base_symb, quote_symb=quote_symb, prod_id=prod_id, buy_strat_type=buy_strat_type, buy_strat_name=buy_strat_name, buy_strat_freq=buy_strat_freq, lta=lta, lmt=cnt)
    # print(len(poss))

    show_pos_close_header_yn = 'Y'
    if poss:
        for pos in poss:
            pos = AttrDict(pos)
            # 🔴 GILFOYLE: Database now automatically converts _dttm fields
            if pos.test_txn_yn == 'N': pos.test_txn_yn = ''
            if pos.pos_end_dttm:
                pos.pos_end_dttm = pos.pos_end_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_close(title, pos, show_pos_close_header_yn)
            show_pos_close_header_yn = 'N'

        chart_bottom()


#<=====>#

@narc(1)
def report_open_overview(quote_symb=None, lta=None, cnt=15):
    if debug_tf: G(f'==> reports_base.report_open_overview()')
    print_adv(2)
    title = 'Outstanding Overview'
    out_ovrs = cbtrade_db.db_open_overview(quote_symb=None, lta=None, cnt=15)
    # print(len(out_ovrs))

    show_header_yn = 'Y'
    if out_ovrs:
        for out_ovr in out_ovrs:
            out_ovr = AttrDict(out_ovr)
            disp_open_overview2(title, out_ovr, show_header_yn)
            show_header_yn = 'N'
        chart_bottom()

#<=====>#

@narc(1)
def report_closed_overview(quote_symb=None, lta=None, cnt=15):
    if debug_tf: G(f'==> reports_base.report_closed_overview()')
    print_adv(2)
    title = 'Closed Overview'
    out_ovrs = cbtrade_db.db_closed_overview(quote_symb=quote_symb, lta=lta, cnt=cnt)
    # print(len(out_ovrs))
    # print(out_ovrs)
    show_header_yn = 'Y'
    if out_ovrs:
        for out_ovr in out_ovrs:
            # print(out_ovr)
            out_ovr = AttrDict(out_ovr)
            disp_close_overview2(title, out_ovr, show_header_yn)
            show_header_yn = 'N'
        chart_bottom()

#<=====>#

@narc(1)
def report_closed_overview_recent_test(base_symb=None, quote_symb=None, prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None, lta=None, cnt=15):
    if debug_tf: G(f'==> reports_base.report_closed_overview_recent_test()')
    print_adv(2)
    title = 'Closed Recent Overview - Test (Daily)'
    out_ovrs = cbtrade_db.db_closed_overview_recent_test(base_symb=base_symb, quote_symb=quote_symb, prod_id=prod_id, buy_strat_type=buy_strat_type, buy_strat_name=buy_strat_name, buy_strat_freq=buy_strat_freq, lta=lta, cnt=cnt)
    # print(len(out_ovrs))
    
    show_header_yn = 'Y'
    if out_ovrs:
        for out_ovr in out_ovrs:
            out_ovr = AttrDict(out_ovr)
            disp_close_overview_daily(title, out_ovr, show_header_yn)
            show_header_yn = 'N'
        chart_bottom()

#<=====>#

@narc(1)
def report_closed_overview_recent_live(base_symb=None, quote_symb=None, prod_id=None, buy_strat_type=None, buy_strat_name=None, buy_strat_freq=None, lta=None, cnt=15):
    if debug_tf: G(f'==> reports_base.report_closed_overview_recent_live()')
    print_adv(2)
    title = 'Closed Recent Overview - Live (Daily)'
    out_ovrs = cbtrade_db.db_closed_overview_recent_live(base_symb=base_symb, quote_symb=quote_symb, prod_id=prod_id, buy_strat_type=buy_strat_type, buy_strat_name=buy_strat_name, buy_strat_freq=buy_strat_freq, lta=lta, cnt=cnt)
    # print(len(out_ovrs))
    
    show_header_yn = 'Y'
    if out_ovrs:
        for out_ovr in out_ovrs:
            out_ovr = AttrDict(out_ovr)
            disp_close_overview_daily(title, out_ovr, show_header_yn)
            show_header_yn = 'N'
        chart_bottom()
#<=====>#

@narc(1)
def report_open():
    if debug_tf: G(f'==> reports_base.report_open()')
    poss = cbtrade_db.db_poss_open_get()

    if poss:
        print_adv(2)
        title = 'Open Positions - By Age'
        show_pos_open_header_yn = 'Y'
        poss_sorted = sorted(poss, key=lambda x: x["age_mins"], reverse=True)
        poss = poss_sorted
        for pos in poss:
            pos = AttrDict(pos)
            # 🔴 GILFOYLE: Database now automatically converts _dttm fields
            if pos.test_txn_yn == 'N': pos.test_txn_yn = ''
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_open(title, pos, show_pos_open_header_yn)
            show_pos_open_header_yn = 'N'

        chart_bottom()

    if poss:
        print_adv(2)
        title = f'Open Positions - By Prod, Strat, Freq, Pos_Id'
        show_pos_open_header_yn = 'Y'
        poss_sorted = sorted(poss, key=lambda x: x["prod_id"])
        poss = poss_sorted
        for pos in poss:
            pos = AttrDict(pos)
            # 🔴 GILFOYLE: Database now automatically converts _dttm fields
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_open(title, pos, show_pos_open_header_yn)
            show_pos_open_header_yn = 'N'

        chart_bottom()

#<=====>#

@narc(1)
def report_open_by_age():
    if debug_tf: G(f'==> reports_base.report_open_by_age()')
    poss = cbtrade_db.db_poss_open_get()

    if poss:
        print_adv(2)
        title = 'Open Positions - By Age'
        show_pos_open_header_yn = 'Y'
        poss_sorted = sorted(poss, key=lambda x: x["age_mins"], reverse=True)
        poss = poss_sorted
        for pos in poss:
            pos = AttrDict(pos)
            # 🔴 GILFOYLE: Database now automatically converts _dttm fields
            if pos.test_txn_yn == 'N': pos.test_txn_yn = ''
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_open(title, pos, show_pos_open_header_yn)
            show_pos_open_header_yn = 'N'

        chart_bottom()

#<=====>#

@narc(1)
def report_open_by_gain():
    if debug_tf: G(f'==> reports_base.report_open_by_gain()')
    poss = cbtrade_db.db_poss_open_get()

    if poss:
        print_adv(2)
        title = 'Open Positions - By Gain Amt'
        show_pos_open_header_yn = 'Y'
        poss_sorted = sorted(poss, key=lambda x: x["gain_loss_pct"], reverse=True)
        poss = poss_sorted
        for pos in poss:
            pos = AttrDict(pos)
            # 🔴 GILFOYLE: Database now automatically converts _dttm fields
            if pos.test_txn_yn == 'N': pos.test_txn_yn = ''
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_open(title, pos, show_pos_open_header_yn)
            show_pos_open_header_yn = 'N'

        chart_bottom()

#<=====>#

@narc(1)
def report_open_by_prod_id(quote_symb=None, test_only_yn='N', live_only_yn='Y'):
    if debug_tf: G(f'==> reports_base.report_open_by_prod_id()')
    poss = cbtrade_db.db_poss_open_get(test_only_yn=test_only_yn, live_only_yn=live_only_yn)
    # print(len(poss))

    if poss:
        print_adv(2)
        title = 'Open Positions - By Prod, Strat, Freq, Pos_Id'
        show_pos_open_header_yn = 'Y'
        poss_sorted = sorted(poss, key=lambda x: x["prod_id"])
        poss = poss_sorted
        for pos in poss:
            pos = AttrDict(pos)
            # 🔴 GILFOYLE: Database now automatically converts _dttm fields
            if pos.test_txn_yn == 'N': pos.test_txn_yn = ''
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_open(title, pos, show_pos_open_header_yn)
            show_pos_open_header_yn = 'N'

        chart_bottom()

#<=====>#

@narc(1)
def report_open_test_by_gain(quote_symb=None, ):
    if debug_tf: G(f'==> reports_base.report_open_test_by_gain()')
    # poss = cbtrade_db.db_poss_open_get(quote_symb=quote_symb)
    # print(len(poss))
    cnt = 0

    sql = ""
    sql += " select * "
    sql += " from poss "
    sql += f" where symb = '{quote_symb}' "
    sql += f" and pos_stat in ('OPEN', 'SELL')"
    sql += " and test_txn_yn = 'Y' "
    sql += " order by prod_id, buy_strat_name, buy_strat_freq, pos_id "
    poss = cbtrade_db.seld(sql, always_list_yn='Y')

    if poss:
        print_adv(2)
        title = 'Test Open Positions - Prod, Strat, Freq, Pos_Id'
        show_pos_open_header_yn = 'Y'
        for pos in poss:
            pos = AttrDict(pos)
            cnt += 1
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_open(title, pos, show_pos_open_header_yn)
            show_pos_open_header_yn = 'N'

        chart_bottom(in_str=cnt)

#<=====>#

@narc(1)
def report_open_live_by_gain(quote_symb=None, ):
    if debug_tf: G(f'==> reports_base.report_open_live_by_gain()')
    # poss = cbtrade_db.db_poss_open_get(quote_symb=quote_symb)
    # print(len(poss))
    cnt = 0

    sql = ""
    sql += " select * "
    sql += " from poss "
    sql += f" where symb = '{quote_symb}' "
    sql += f" and pos_stat in ('OPEN', 'SELL')"
    sql += " and test_txn_yn = 'N' "
    sql += " order by prod_id, buy_strat_name, buy_strat_freq, pos_id "
    poss = cbtrade_db.seld(sql, always_list_yn='Y')

    if poss:
        print_adv(2)
        title = 'Live Open Positions - Prod, Strat, Freq, Pos_Id'
        show_pos_open_header_yn = 'Y'
        for pos in poss:
            pos = AttrDict(pos)
            cnt += 1
            pos.pos_begin_dttm = pos.pos_begin_dttm.strftime('%m-%d-%Y %H:%M')
            pos.report_age = format_disp_age(pos.age_mins)
            disp_pos_open(title, pos, show_pos_open_header_yn)
            show_pos_open_header_yn = 'N'

        chart_bottom(in_str=cnt)

#<=====>#

@narc(1)
def report_strats_best(cnt=10, quote_symb=None, min_trades=1):
    if debug_tf: G(f'==> reports_base.report_strats_best()')

    title = f'Best Performing Strategies - Min {min_trades} Trade(s)'
    # Get all strategy performance data with minimum trades filter

    sql = ""
    sql += " select * "
    sql += " from trade_strat_perfs "
    sql += f" where quote_symb = '{quote_symb}' "
    sql += f" and lta = 'A' "
    sql += f" and tot_close_cnt >= {min_trades} "
    sql += " order by gain_loss_pct_hr desc "
    sql += f" limit {cnt} "

    mkt_strat_perfs = []
    results = cbtrade_db.seld(sql, always_list_yn='Y')
    for x in results:
        x = AttrDict(x)
        mkt_strat_perfs.append(x)

    show_strat_header_yn = 'Y'

    if mkt_strat_perfs:
        print_adv(2)
        max_pct = max(strat.get('gain_loss_pct_hr', 0) for strat in mkt_strat_perfs)
        for mkt_strat_perf in mkt_strat_perfs:
            disp_strat_green_gradient(title, mkt_strat_perf, show_strat_header_yn, max_pct)
            show_strat_header_yn = 'N'
        chart_bottom()

#<=====>#
# Post Variables
#<=====>#

@narc(1)
def test_reports():
    # disp_recent(show_pos_close_header_yn='Y')
    report_buys_recent(cnt=15, test_yn='N')
    report_closed_overview()
    report_closed_overview_recent_test()
    report_closed_overview_recent_live()
    report_open()
    report_open_by_age()
    report_open_by_gain()
    report_open_by_prod_id(quote_symb=None, test_only_yn='N', live_only_yn='Y')
    report_open_test_by_gain()
    report_open_live_by_gain()
    report_open_overview()
    report_sells_recent(cnt=15, test_yn='N')
    report_strats_best(cnt=10, quote_symb=None, min_trades=1)
    # disp_strats()

    # disp_close_overview(title, out_ovr, show_header_yn='Y')
    # disp_close_overview_daily(title, out_ovr, show_header_yn='Y')
    # report_open_overview(title, out_ovr, show_header_yn='Y')
    # disp_pos_open(title, pos, show_pos_open_header_yn='Y')
    # disp_pos_close(title, pos, show_pos_close_header_yn='Y')
    # report_strat(title, mkt_strat_perf, show_strat_header_yn)
    # disp_strat_green_gradient(title, mkt_strat_perf, show_strat_header_yn, max_pct)


#<=====>#
# Default Run
#<=====>#

if __name__ == '__main__':
    test_reports()


#<=====>#
