# type: ignore
#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
# Standard library imports
import calendar
from datetime import date, datetime, timedelta
import decimal
import re
import sys
import time
import traceback
import uuid
from datetime import timezone

# Third-party imports
from flask import Flask
from markupsafe import Markup
import sqlparse

# Local imports
from fstrent_colors import BoW
from libs.common import dttm_get, now_utc_get
from libs.db_mysql.cbtrade.db_main import cbtrade_db as db


#<=====>#
# Variables
#<=====>#
lib_name      = 'bot_web'
log_name      = 'bot_web'


#<=====>#
# Assignments Pre
#<=====>#


#<=====>#
# Classes
#<=====>#


#<=====>#
# Functions
#<=====>#

def print_sql(sql) -> None:
    print(sqlparse.format(sql, reindent=True, keyword_case='upper'))

#<=====>#

def build_topnav():

    s = ""
    s += "select distinct prod_id as mkt "
    s += "  from cbtrade.poss "
    s += "  order by prod_id "
    try:
        mkt_data = db.sel(s)
    except:
        print(s)
        raise
    else:
        pass

    s = ""
    s += "select distinct date_format(pos_end_dttm,'%Y-%m-%d') as cdt "
    s += "  from cbtrade.poss  "
    s += "  order by 1 desc"
    try:
        date_data = db.sel(s)
    except:
        print(s)
        raise
    else:
        pass

    s = ""
    s = s + "select distinct date_format(pos_end_dttm,'%Y') as cy "
    s = s + "  , date_format(pos_end_dttm,'%m') as cm "
    s = s + "  , date_format(pos_end_dttm,'%M') as mn "
    s = s + "  from cbtrade.poss "
    s = s + "  order by 1 desc, 2 desc "
    try:
        month_data = db.seld(s)
    except:
        print(s)
        raise
    else:
        pass

    s = ""
    s += "select distinct date_format(pos_end_dttm,'%Y') as cy  "
    s += "  from cbtrade.poss "
    s += "  order by 1"
    try:
        year_data = db.sel(s)
    except:
        print(s)
        raise
    else:
        pass

    mkt_dd = ""
    mkt_dd = mkt_dd + "<select id='mkts' onchange=" + chr(34) + "window.open(this.value,'_self');" + chr(34) + ">"
    mkt_dd = mkt_dd + "<option value='#'>Choose Market</option>"
    if mkt_data:
        for mkt in mkt_data:
            if mkt is not None:
                mkt = mkt.replace('-','_')
                mkt_dd = mkt_dd + "<option value='/market_" + mkt + "'>" + mkt + "</option>"
    mkt_dd = mkt_dd + "</select>"

    s_dt_dd = ""
    s_dt_dd += "<select id='sales_dt_dd' onchange=" + chr(34) + "window.open(this.value,'_self');" + chr(34) + ">"
    s_dt_dd += "<option value='#'>Choose Date</option>"
    if date_data:
        for cdt in date_data:
            if cdt is not None:
                s_dt_dd += f"<option value='/sales_dt_{cdt}'>{cdt}</option>"
    s_dt_dd += "</select>"

    s_m_dd = ""
    s_m_dd += "<select id='sales_m_dd' onchange=" + chr(34) + "window.open(this.value,'_self');" + chr(34) + ">"
    s_m_dd += "<option value='#'>Choose Month</option>"
    if month_data:
        for row in month_data:
            if row['cy'] is not None:
                cy = row['cy']
                cm = row['cm']
                s_m_dd += f"<option value='/sales_month_{cy}_{cm}'>{cy} {cm}</option>"
    s_m_dd += "</select>"

    s_y_dd = ""
    s_y_dd += "<select id='sales_y_dd' onchange=" + chr(34) + "window.open(this.value,'_self');" + chr(34) + ">"
    s_y_dd += "<option value='#'>Choose Year</option>"
    if year_data:
        for cy in year_data:
            if cy is not None:
                s_y_dd += f"<option value='/sales_year_{cy}'>{cy}</option>"
    s_y_dd += "</select>"


    html = ""
    html += "<table class='nav'>"
    html += "<thead>"
    html += "  <tr><th class='nav2' width='*'>Navs</th></tr>"
    html += "</thead>"
    html += "<tbody>"

    # Home
    html = build_topnav_link( in_str='Home', in_url='home.htm',  in_html=html)
    html = build_topnav_link( in_str='All Reports Test', in_url='all_reports_test.htm',  in_html=html)

    # Quick Looks
    html = build_topnav_title(in_str='Quick Looks', in_html=html)
    html = build_topnav_link( in_str='Balances',    in_url='balances.htm',  in_html=html)
    html = build_topnav_link( in_str='Open Positions',   in_url='open_positions.htm', in_html=html)
    html = build_topnav_link( in_str='Closed Positions',   in_url='closed_positions.htm', in_html=html)
    html = build_topnav_link( in_str='Buys - Recent',   in_url='buys_recent.htm', in_html=html)
    html = build_topnav_link( in_str='Sells - Recent',   in_url='sells_recent.htm', in_html=html)
    html = build_topnav_link( in_str='Buy Strats',   in_url='buy_strats.htm', in_html=html)
    html = build_topnav_link( in_str='Market Buy Strats',   in_url='mkt_buy_strats.htm', in_html=html)
    html = build_topnav_link( in_str='Markets',     in_url='markets.htm',   in_html=html)
    html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;'>" + mkt_dd + "</td></tr>"

    # NEW: Fast Performance Dashboard  
    html = build_topnav_title(in_str='⚡ Fast Performance', in_html=html)
    html = build_topnav_link( in_str='Fast Home Dashboard', in_url='fast_home.htm',  in_html=html)
    html = build_topnav_link( in_str='Fast Markets Dashboard', in_url='fast_markets.htm',  in_html=html)
    html = build_topnav_link( in_str='Fast Strategies Dashboard', in_url='fast_strategies.htm',  in_html=html)

    # Sales Summary
    html = build_topnav_title(in_str='Sales Summary', in_html=html)
    html = build_topnav_link( in_str='All',    in_url='sales_all.htm',  in_html=html)
    html = build_topnav_link( in_str='Today',   in_url='sales_today.htm', in_html=html)
    html = build_topnav_link( in_str='Yesterday',     in_url='sales_yesterday.htm',   in_html=html)
    html += "  <tr>"
    html += "    <td>"
    html += "      <table width='100%' border=0 style='background-color:#0000ff;'>"
    html += "        <tr>"
    html += "          <td class='dud' style='text-align:left;'>Past</td>"
    html += "          <td>"
    html += "            <table width='100%' border=0 border=0 style='background-color:#0000ff;'>"
    html += "              <tr>"
    for x in (3,7,14,30):
        html += "            <td class='nav' style='vertical-align:top;text-align:left;' onclick=" + chr(34) + "window.open('/sales_{}d.htm','_self');".format(x) + chr(34) + "><a href='/sales_{}d.htm'>{}</a></td>".format(x,x)
    html += "                <td class='nav' style='vertical-align:top;text-align:left;' onclick=" + chr(34) + "window.open('/sales_all.htm','_self');" + chr(34) + "><a href='/sales_all.htm'>*</a></td>"
    html += "              </tr>"
    html += "            </table>"
    html += "          </td>"
    html += "          <td class='dud' style='text-align:left'>Days</td>"
    html += "        </tr>"
    html += "      </table>"
    html += "    </td>"
    html += "  </tr>"

    html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;'>" + s_dt_dd + "</td></tr>"
    html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;'>" + s_m_dd + "</td></tr>"
    html += "  <tr><td class='nav' style='vertical-align:top;text-align:left;'>" + s_y_dd + "</td></tr>"

    # Sales Summary - Test
    html = build_topnav_title(in_str='Sales Summary - Tests', in_html=html)
    html = build_topnav_link( in_str='All - Tests',    in_url='sales_all_test.htm',  in_html=html)
    html = build_topnav_link( in_str='Today - Tests',   in_url='sales_today_test.htm', in_html=html)
    html = build_topnav_link( in_str='Yesterday - Tests',     in_url='sales_yesterday_test.htm',   in_html=html)

    # Misc
    html = build_topnav_title(in_str='Misc', in_html=html)
    html = build_topnav_link(in_str='DB Size', in_url='db_size.htm', in_html=html)

    html += "</tbody>"
    html += "</table>"

    html = Markup(html)

    return html

#<=====>#

def build_topnav_title(in_str, in_html):
    html = in_html
    html += "<tr>"
    html += "<th class='nav' style='vertical-align:top;text-align:left;'>"
    html += "{}".format(in_str)
    html += "</th>"
    html += "</tr>"
    return html

#<=====>#

def build_topnav_link(in_str, in_url, in_html):
    html = in_html
    html += "<tr>"
    html += "<td "
    html += "  class='nav' "
    html += "  style='vertical-align:top;text-align:left;' "
    html += "  onclick={}window.open('/{}','_self');{}>".format('"', in_url,'"')
    html += "<a href='/{}'>{}</a>".format(in_url, in_str)
    html += "</td>"
    html += "</tr>"
    return html

#<=====>#

def html_up_add(u=None) -> str:
    if not u:
        u = ""
        u = "<table width=100%><tr><td width=100%>"
    return u

#<=====>#

def html_down_add(d=None) -> str:
    if not d:
        d = ""
        d = "</td></td></table>"
    return d

#<=====>#

def html_h1_add(t, m=None, u=None, d=None) -> tuple[str, str, str]:
    more = f'<hr><h1>{t}</h3>'
    m, u, d = html_add(more=more, m=m, u=u, d=d)
    return m, u, d

#<=====>#

def html_h2_add(t, m=None, u=None, d=None) -> tuple[str, str, str]:
    more = f'<hr><h2>{t}</h3>'
    m, u, d = html_add(more=more, m=m, u=u, d=d)
    return m, u, d

#<=====>#

def html_h3_add(t, m=None, u=None, d=None) -> tuple[str, str, str]:
    more = f'<hr><h3>{t}</h3>'
    m, u, d = html_add(more=more, m=m, u=u, d=d)
    return m, u, d


#<=====>#

def html_hr_add(m=None, u=None, d=None) -> tuple[str, str, str]:
    more = '<br><hr><br>'
    m, u, d = html_add(more=more, m=m, u=u, d=d)
    return m, u, d

#<=====>#

def html_add(more, m=None, u=None, d=None) -> tuple[str, str, str]:
    if not u: html_up_add()
    if not d: html_down_add()
    if m:
        m = '{}{}'.format(m, more)
    else:
        m = more
    return m, u, d

#<=====>#

def html_comb(m=None, u=None, d=None) -> str:
    html = ''
    if u:
        html = '{}{}'.format(html, u)
    if m:
        html = '{}{}'.format(html, m)
    if d:
        html = '{}{}'.format(html, d)

    html = Markup(html)

    return html

#<=====>#

def frmt_sci_not_tf(s):
    # Regular expression to identify scientific notation
    scientific_notation_pattern = re.compile(r'^[+-]?\d+(\.\d+)?[eE][+-]?\d+$')
    return bool(scientific_notation_pattern.match(str(s)))

#<=====>#

def frmt_sci_not_2_dec(s):
    s = str(s)
    if frmt_sci_not_tf(s):
        # Convert to float
        num = float(s)
        # Get the number of decimal places
        decimal_places = get_decimal_places(s)
        # Use format to display the correct number of decimals
        formatted_number = f"{num:.{decimal_places + abs(int(s.split('e')[-1]))}f}"
        f = formatted_number.rstrip('0').rstrip('.') if '.' in formatted_number else formatted_number
        return f
    else:
        return s  # Return the original string if not in scientific notation

#<=====>#

def get_decimal_places(s):
    s = str(s)
    # Regular expression to capture the number of decimal places in the scientific notation
    match = re.match(r'^[+-]?\d+(\.\d+)?[eE][+-]?\d+$', s)
    if match:
        decimal_part = match.group(1)
        if decimal_part:
            return len(decimal_part) - 1  # Subtract 1 to account for the dot
    return 0

#<=====>#

def gen_guid():
    guid = str(uuid.uuid4())
    return guid

    #<=====>#

def build_data_display(data, t=None):

    table_id = gen_guid()

    html = ''

    if not data:
        return html

    if not isinstance(data, list):
        return html

    # get first dict from list to grab keys as headers
    first_d = data[0]
    headers = []  # Initialize headers to prevent unbound variable error
    if isinstance(first_d, dict):
        headers = list(first_d.keys())

    rows = data

    re_prod_id       = re.compile(r'^[a-zA-Z0-9]+-[a-zA-Z0-9]+$')

    html = ""
#    html += "<html>"
#    html += "<body>"
    html += f"<table class='dt' border=1 id='{table_id}' width=100%>"
    html += "<thead>"


    head_cnt = 0
    for header in headers:
        if header != 'exclude':
            head_cnt += 1


    if t:
        html += "<tr>"
        html += f"<th class='dt_title' colspan={head_cnt} style='text-align:center'>{t}</th>"
        html += "</tr>"

    #headers
    html += "<tr>"
    head_cnt = 0
    for header in headers:
        if header != 'exclude':
            html += f"<th class='dt' style='text-align:center'>{header}</th>"
            head_cnt += 1
    html += "</tr>"
    html += "</thead>"
    html += "<tbody>"

    #contents
    for row in rows:
        html += "<tr class='dt'>"
        for k in row:
            v = row[k]

            if isinstance(v, decimal.Decimal):
                if v == int(v):
                    v = int(v)
                else:
                    v = float(v)

            try:

                if 0 == 1:
                    print('never going to give you up!')

                elif k in ('exclude'):
                    pass

                elif k in ('prod_id','buy_strat_name','sell_strat_name'):
                    html += build_td_important(v, align='left')

                elif k in ('buy_strat_freq','sell_strat_freq'):
                    html += build_td_important(v, align='center')

                # USD
                elif k[-4:].lower() == '_usd':
                    html += build_td_usd(v)

                # USD
                elif isinstance(v, str) and k[-4:].lower() == '_usd' or str(v).find('$') >= 0:
                    html += build_td_usd(v)

                # Logo Img
                elif isinstance(v, str) and v[-4:].lower() in ('.png','.jpg','.jpeg','.gif'):
                    html += build_td_img(v)

                # URL
                elif isinstance(v, str) and v[:6].lower() in ('http:/','https:'):
                    html += build_td_url(v)

                # URL
                elif isinstance(v, str) and v[:4].lower() in ('www.'):
                    html += build_td_url(v)

                # PERCENT
                elif isinstance(v, str) and k[-4:].lower() == '_pct' or str(v).find('%') >= 0:
                    html += build_td_pct(v)


                # BOLD
                elif k in ('symb','prod_id', 'mkt'):
                    html += build_td_important(v)

                # integer
                elif isinstance(v, int):
                    html += build_td_int(v)

                # decimal
                elif isinstance(v, (float,decimal.Decimal)):
                    html += build_td_dec(v)


                # datetime
                elif isinstance(v, datetime):
                    html += build_td_str(str(v))


                # BOLD
                elif isinstance(v, str) and re_prod_id.match(str(v)):
                    html += build_td_bold(v)

                # STR
                elif isinstance(v, str):
                    html += build_td_str(v)

                # NULL
                elif v == 0:
                    html += build_td_int(v)

                # NULL
                elif not v:
                    html += build_td_str('')

                else:
                    html += "<td class='dt' style='text-align:center'>" + str(v) + "</td>"

            except:
                traceback.print_exc()
                print(f'v ({type(v)}): {v}')
                pass

        html += "</tr>"

    html += "</tbody>"
    html += "</table>"
#    html += "</body>"
#    html += "</html>"

    html = html.replace('>None<','-')
    html = html.replace('0E-8','0')

    html = Markup(html)
    return html

#<=====>#

def build_sql_display(s, t=None):

    data = db.seld(s)

    html = build_data_display(data, t)

    return html

#<=====>#

def build_td_int(v=None) -> str:
    if not v:
        return "<td></td>"
    else:
        html = "<td class='dt' style='text-align:left'>" + str(v) + "</td>"
    return html

#<=====>#

def build_td_dec(v=None) -> str:
    if not v:
        return "<td></td>"
    else:
        html = "<td class='dt' style='text-align:right'>" + str(v) + "</td>"
    return html

#<=====>#

def build_td_usd(v=None) -> str:
    if not v:
        return "<td></td>"
    else:
        html = ""
        if str(v).find('-') >= 0:
            html += "<td class='dt' style='text-align:right;background:red;color:yellow'>"
            html += "<div style='float:left;width=10%;'>$</div>"
            html += "<div style='float:right;width=90%;'>"
            st    = str(v)
            st = st.replace('$','')
            st = st.replace(' ','')
            html += st
            html += "</div>"
            html += "</td>"
        else:
            html += "<td class='dt' style='text-align:right;background:green;color:yellow'>"
            html += "<div style='float:left;width=10%;'>$</div>"
            html += "<div style='float:right;width=90%;'>"
            st    = str(v)
            st = st.replace('$','')
            st = st.replace(' ','')
            html += st
            html += "</div>"
            html += "</td>"
    return html

#<=====>#

def build_td_pct(v=None) -> str:
    if not v:
        return "<td></td>"
    else:
        html = ""
        if str(v).find('-') >= 0:
            html += "<td class='dt' style='text-align:right;background:red;color:yellow;'>"
            html += str(v)
            html += "</td>"
        else:
            html += "<td class='dt' style='text-align:right;background:green;color:yellow;'>"
            html += str(v)
            html += "</td>"
    return html

#<=====>#

def build_td_str(v=None) -> str:
    if not v:
        return "<td></td>"
    else:
        html = "<td class='dt' style='text-align:left'>" + str(v) + "</td>"
    return html

#<=====>#

def build_td_important(v=None, align='center') -> str:
    if not v:
        return "<td></td>"
    else:
        html = ""
        html += f"<td class='dt' style='text-align:{align};color:#ffffff;background-color:#000000'>"
        html += "{}".format(v)
        html += "</td>"
    return html

#<=====>#

def build_td_bold(v=None) -> str:
    if not v:
        return "<td></td>"
    else:
        html = ""
        html += "<td class='dt' style='text-align:center;background:silver'>"
        html += "{}".format(v)
        html += "</td>"
    return html

#<=====>#

def build_td_img(v=None) -> str:
    if not v:
        return "<td></td>"
    else:
        html = ""
        html += "<td class='dt' style='text-align:center;background:black'>"
        html += "<a href='/{}'>{}</a>".format(v, v)
        html += "</td>"
    return html

#<=====>#

def build_td_url(v=None) -> str:
    if not v:
        return "<td></td>"
    else:
        html = ""
        html += "<td class='dt' style='text-align:center;background:black'>"
        html += "<img src='" + str(v) + "' width='25' height='25'></img>"
        html += "</td>"
    return html

#<=====>#

def add_table_dump(table_name, m=None, u=None, d=None) -> str:
    print(f"{str(datetime.now(timezone.utc))} ext_table_dump({table_name})")
    tn = build_topnav()


    pt = 'My Balances'

    m, u, d = add_bals_total(t='Total Balance', m=m, u=u, d=d)

    m, u, d = html_hr_add(m=m, u=u, d=d)


    sql = f"select * from {table_name}"

    t = f'Table => {table_name}'

    h = build_sql_display(sql, t)
    m, u, d = html_add(more=h, m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_bals_total(t='Total Balance', m=None, u=None, d=None) -> str:
    print(str(datetime.now(timezone.utc)) + " add_bals_total(t, m, u, d, h)")

    sql = " "
    sql += "select x.cnt "
    sql += "  , concat('$',' ', round(x.total_val_usd,4)) as bal_val_usd "
    sql += "  , concat('$',' ', round(x.total_val_usd,4)) as bot_val_usd "
    sql += "  , concat('$',' ', round(x.avail_val_usd,4)) as free_val_usd"

    sql += "  , concat('$',' ', round((select sum(tot_out_cnt) from cbtrade.poss px where px.quote_curr_symb='USD' and px.ignore_tf=0 and px.pos_stat='CLOSE'), 2)) as tot_out_usd"
    sql += "  , concat('$',' ', round((select sum(tot_in_cnt) from cbtrade.poss px where px.quote_curr_symb='USD' and px.ignore_tf=0 and px.pos_stat='CLOSE'), 2)) as tot_in_usd"

    sql += "  , concat('$',' ', round((select sum(tot_out_cnt) from cbtrade.poss px where px.quote_curr_symb='USDC' and px.ignore_tf=0 and px.pos_stat='CLOSE'), 2)) as tot_out_usdc"
    sql += "  , concat('$',' ', round((select sum(tot_in_cnt) from cbtrade.poss px where px.quote_curr_symb='USDC' and px.ignore_tf=0 and px.pos_stat='CLOSE'), 2)) as tot_in_usdc"

    sql += "  , concat('$',' ', round((select sum(tot_out_cnt) from cbtrade.poss px where px.quote_curr_symb='USDT' and px.ignore_tf=0 and px.pos_stat='CLOSE'), 2)) as tot_out_usdt"
    sql += "  , concat('$',' ', round((select sum(tot_in_cnt) from cbtrade.poss px where px.quote_curr_symb='USDT' and px.ignore_tf=0 and px.pos_stat='CLOSE'), 2)) as tot_in_usdt"

    sql += "  , (select sum(tot_out_cnt) from cbtrade.poss px where px.quote_curr_symb='BTC' and px.ignore_tf=0 and px.pos_stat='CLOSE') as tot_out_btc"
    sql += "  , (select sum(tot_in_cnt) from cbtrade.poss px where px.quote_curr_symb='BTC' and px.ignore_tf=0 and px.pos_stat='CLOSE') as tot_in_btc"

    sql += "  , (select sum(tot_out_cnt) from cbtrade.poss px where px.quote_curr_symb='ETH' and px.ignore_tf=0 and px.pos_stat='CLOSE') as tot_out_eth"
    sql += "  , (select sum(tot_in_cnt) from cbtrade.poss px where px.quote_curr_symb='ETH' and px.ignore_tf=0 and px.pos_stat='CLOSE') as tot_in_eth"

    sql += "  , (select sum(tot_out_cnt) from cbtrade.poss px where px.quote_curr_symb='SOL' and px.ignore_tf=0 and px.pos_stat='CLOSE') as tot_out_sol"
    sql += "  , (select sum(tot_in_cnt) from cbtrade.poss px where px.quote_curr_symb='SOL' and px.ignore_tf=0 and px.pos_stat='CLOSE') as tot_in_sol"

    sql += "  , concat('$',' ', round((select sum(tot_out_cnt) from cbtrade.poss px where px.ignore_tf=0 and px.pos_stat='OPEN'), 2)) as spent_open"
    sql += "  , concat('$',' ', round((select sum(tot_in_cnt) from cbtrade.poss px join cbtrade.mkts m on m.prod_id = px.prod_id where px.ignore_tf=0 and px.pos_stat='OPEN'), 2)) as value_open "
    sql += "  , concat('$',' ', round((select sum(hold_cnt * (select m.prc from cbtrade.mkts m where m.prod_id = px.prod_id)) from cbtrade.poss px where px.ignore_tf=0 and px.pos_stat='OPEN'), 2)) as value_open_2 "

    sql += "  from (select count(b.symb) as cnt "
    sql += "          , sum(b.curr_val_usd) as total_val_usd "
    sql += "          , sum(b.bal_avail * b.curr_prc_usd) as avail_val_usd "
    sql += "          from cbtrade.bals b "
    sql += "          where b.ignore_tf = 0 "
    sql += "       ) x "

    h = build_sql_display(sql, t)
    m, u, d = html_add(more=h, m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report(
        t='Sales Summary', 
        inc_prod_id=False, 
        inc_pos_id=False, 
        inc_sd_dt=False, 
        inc_td_dt=False, 
        inc_stat=False, 
        inc_wl=False, 
        inc_buy_strat_name=False, 
        inc_buy_strat_freq=False, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_gain=False, 
        inc_loss=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat=None, 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='ALL',
        lmt=None, 
        order_by_sql=None, 
        m=None, u=None, d=None
        ) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(t={t}, m, u, d, h)")

    if sd_dt1: sd_dt1_str = sd_dt1.strftime('%Y-%m-%d')
    if sd_dt2: sd_dt2_str = sd_dt2.strftime('%Y-%m-%d')
    if td_dt1: td_dt1_str = td_dt1.strftime('%Y-%m-%d')
    if td_dt2: td_dt2_str = td_dt2.strftime('%Y-%m-%d')

    top_sql = ""
    mid_sql = ""
    group_by_sql = ""

    if not order_by_sql:
        order_by_sql = 'order by x.gain_loss_pct_hr desc'

    if inc_prod_id:
        top_sql      += " , x.prod_id "
    if inc_prod_id or prod_id:
        mid_sql      += " , p.prod_id "
        group_by_sql += " p.prod_id,"
    # print(f"group_by_sql 1: {group_by_sql}")

    if inc_pos_id:
        top_sql      += " , x.pos_id "
    if inc_pos_id or pos_id:
        mid_sql      += " , p.pos_id "
        group_by_sql += " p.pos_id,"
    # print(f"group_by_sql 2: {group_by_sql}")

    if inc_sd_dt:
        top_sql      += " , x.sd_dt "
    if inc_sd_dt or sd_dt1 or sd_dt2:
        if inc_pos_id:
            mid_sql      += " , p.pos_begin_dttm as sd_dt "
        else:
            mid_sql      += " , date(p.pos_begin_dttm) as sd_dt "
    if inc_sd_dt:
        if inc_pos_id:
            group_by_sql      += " p.pos_begin_dttm, "
        else:
            group_by_sql      += " date(p.pos_begin_dttm),"
    # print(f"group_by_sql 3: {group_by_sql}")

    if inc_td_dt:
        top_sql      += " , x.td_dt "
    if inc_td_dt or td_dt1 or td_dt2:
        if inc_pos_id:
            mid_sql      += " , p.pos_end_dttm as td_dt "
        else:
            mid_sql      += " , date(p.pos_end_dttm) as td_dt "
    if inc_td_dt:
        if inc_pos_id:
            group_by_sql      += " p.pos_end_dttm, "
        else:
            group_by_sql      += " date(p.pos_end_dttm),"
    # print(f"group_by_sql 4: {group_by_sql}")

    if inc_stat:
        top_sql      += " , x.pos_stat "
    if inc_stat or stat:
        mid_sql      += " , p.pos_stat "
        group_by_sql += " p.pos_stat,"
    # print(f"group_by_sql 5: {group_by_sql}")

    if inc_wl:
        top_sql      += " , x.wl "
    if inc_wl or wl:
        mid_sql      += " , case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 'WIN' else 'LOSE' end as wl "
        group_by_sql += " case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 'WIN' else 'LOSE' end, "
    # print(f"group_by_sql 6: {group_by_sql}")

    if inc_test:
        top_sql      += " , test_txn_yn as test_yn "
    if inc_test or test_txn_yn in ('Y', 'N'):
        mid_sql      += " , p.test_txn_yn "
        group_by_sql += " p.test_txn_yn,"
    # print(f"group_by_sql 7: {group_by_sql}")

    if inc_buy_strat_name:
        top_sql      += " , x.buy_strat_name "
    if inc_buy_strat_name or buy_strat_name:
        mid_sql      += " , p.buy_strat_name "
        group_by_sql += " p.buy_strat_name,"
    # print(f"group_by_sql 8: {group_by_sql}")

    if inc_buy_strat_freq:
        top_sql      += " , x.buy_strat_freq "
    if inc_buy_strat_freq or buy_strat_freq:
        mid_sql      += " , p.buy_strat_freq "
        group_by_sql += " p.buy_strat_freq,"
    # print(f"group_by_sql 9: {group_by_sql}")

    if inc_sell_strat_name:
        top_sql      += " , x.sell_strat_name "
    if inc_sell_strat_name or sell_strat_name:
        mid_sql      += " , p.sell_strat_name "
        group_by_sql += " p.sell_strat_name,"
    # print(f"group_by_sql 10: {group_by_sql}")

    if inc_sell_strat_freq:
        top_sql      += " , x.sell_strat_freq "
    if inc_sell_strat_freq or sell_strat_freq:
        mid_sql      += " , p.sell_strat_freq "
        group_by_sql += " p.sell_strat_freq,"
    # print(f"group_by_sql 11: {group_by_sql}")

    if group_by_sql != "":
        group_by_sql = "group by " + group_by_sql
    # print(f"group_by_sql 12: {group_by_sql}")

    # if sql ends with a comma, remove it
    top_sql = re.sub(r',\s*$', '', top_sql)
    mid_sql = re.sub(r',\s*$', '', mid_sql)
    group_by_sql = re.sub(r',\s*$', '', group_by_sql)
    # print(f"group_by_sql 13: {group_by_sql}")

    sql = ""
    sql += "select x.exclude "
    sql += f"  {top_sql} "
    if not inc_pos_id:
        sql += "  , x.tot_cnt "
        sql += "  , x.win_cnt "
        sql += "  , x.lose_cnt "
        sql += "  , concat(x.win_pct, ' %') as win_pct "
        sql += "  , concat(x.lose_pct, ' %') as lose_pct "
        sql += "  , concat('$ ', x.gain_amt) as gain_amt "
        sql += "  , concat('$ ', x.loss_amt) as loss_amt "
    sql += "  , concat('$ ', x.gain_loss_amt) as gain_loss_amt "
    sql += "  , concat('$ ', x.gain_loss_amt_net) as gain_loss_amt_net "
    sql += "  , concat(x.gain_loss_pct, ' %') as gain_loss_pct "
    sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
    sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
    
    # Add Unix timestamp-based calculations to the output
    sql += "  , concat(x.gain_loss_pct_hr, ' %') as gain_loss_pct_hr "
    sql += "  , concat(x.gain_loss_pct_hr * 24, ' %') as gain_loss_pct_day "
    sql += "  , x.age_hours "
    
    sql += "  , concat('$ ', x.tot_out_cnt) as tot_out_cnt "
    sql += "  , concat('$ ', x.tot_in_cnt) as tot_in_cnt "
    sql += "  , concat('$ ', x.fees_cnt_tot) as fees_cnt_tot "
    sql += "  , concat('$ ', x.val_curr) as val_curr "
    sql += "  , concat('$ ', x.val_tot) as val_tot "
    sql += "  , x.age_hours "
    sql += "  from (select 'x' as exclude  "
    sql += f"          {mid_sql} "
    if not inc_pos_id:
        sql += "          , count(p.pos_id) as tot_cnt  "
        sql += "          , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt  "
        sql += "          , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt  "
        sql += "          , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct  "
        sql += "          , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct  "
        sql += "          , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 4),0) as gain_amt  "
        sql += "          , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 4),0) as loss_amt  "
    # sql += "          , sum(p.age_mins) as age_mins "
    # sql += "          , sum(p.age_mins) / 60 as age_hours "
    
    # Add Unix timestamp-based age calculations for more accurate results
    sql += "          , sum((p.pos_end_unix - p.pos_begin_unix) / 60) as age_mins "
    sql += "          , sum((p.pos_end_unix - p.pos_begin_unix) / 3600) as age_hours "
    
    sql += "          , round(sum(p.tot_out_cnt), 2) as tot_out_cnt "
    sql += "          , round(sum(p.tot_in_cnt), 2) as tot_in_cnt "
    sql += "          , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt "
    sql += "          , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot "
    sql += "          , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot "
    sql += "          , sum(p.buy_cnt) as buy_cnt "
    sql += "          , sum(p.sell_cnt_tot) as sell_cnt_tot "
    sql += "          , sum(p.hold_cnt) as hold_cnt "
    sql += "          , sum(p.pocket_cnt) as pocket_cnt "
    sql += "          , sum(p.clip_cnt) as clip_cnt "
    sql += "          , sum(p.sell_order_cnt) as sell_order_cnt "
    sql += "          , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt "
    sql += "          , round(sum(p.val_curr), 2) as val_curr "
    sql += "          , round(sum(p.val_tot), 2) as val_tot "
    sql += "          , round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt  "
    sql += "          , round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt "
    sql += "          , round(sum(p.gain_loss_amt), 2) as gain_loss_amt "
    sql += "          , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net "
    sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct "
#    sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr "
    
    # Add Unix timestamp-based gain/loss per hour calculation for more accurate results
    sql += "          , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum((p.pos_end_unix - p.pos_begin_unix) / 3600)), 8) as gain_loss_pct_hr "    
    sql += "          , concat(round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum((p.pos_end_unix - p.pos_begin_unix) / 3600)), 8) * 24, ' %') as gain_loss_pct_day "

    sql += "          from cbtrade.poss p "
    sql += "          where ignore_tf = 0 "

    if prod_id:
        sql += f"     and p.prod_id = '{prod_id}' "

    if pos_id:
        sql += f"     and p.pos_id = '{pos_id}' "

    if sd_dt1 and not sd_dt2:
        sql += f"     and date(p.pos_begin_dttm) = str_to_date('{sd_dt1}','%Y-%m-%d') "
        # Also add Unix timestamp condition for more accurate filtering
        sql += f"     and FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d') = '{sd_dt1}' "
    elif sd_dt2 and not sd_dt1:
        sql += f"     and date(p.pos_begin_dttm) = str_to_date('{sd_dt2}','%Y-%m-%d') "
        # Also add Unix timestamp condition for more accurate filtering
        sql += f"     and FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d') = '{sd_dt2}' "
    elif sd_dt1 and sd_dt2:
        sql += f"     and date(p.pos_begin_dttm) >= str_to_date('{sd_dt1}','%Y-%m-%d') "
        sql += f"     and date(p.pos_begin_dttm) <= str_to_date('{sd_dt2}','%Y-%m-%d') "
        # Also add Unix timestamp conditions for more accurate filtering
        sql += f"     and FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d') >= '{sd_dt1}' "
        sql += f"     and FROM_UNIXTIME(p.pos_begin_unix, '%Y-%m-%d') <= '{sd_dt2}' "

    if td_dt1 and not td_dt2:
        sql += f"     and date(p.pos_end_dttm) = str_to_date('{td_dt1}','%Y-%m-%d') "
        # Also add Unix timestamp condition for more accurate filtering
        sql += f"     and FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') = '{td_dt1}' "
    elif td_dt2 and not td_dt1:
        sql += f"     and date(p.pos_end_dttm) = str_to_date('{td_dt2}','%Y-%m-%d') "
        # Also add Unix timestamp condition for more accurate filtering
        sql += f"     and FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') = '{td_dt2}' "
    elif td_dt1 and td_dt2:
        sql += f"     and date(p.pos_end_dttm) >= str_to_date('{td_dt1}','%Y-%m-%d') "
        sql += f"     and date(p.pos_end_dttm) <= str_to_date('{td_dt2}','%Y-%m-%d') "
        # Also add Unix timestamp conditions for more accurate filtering
        sql += f"     and FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') >= '{td_dt1}' "
        sql += f"     and FROM_UNIXTIME(p.pos_end_unix, '%Y-%m-%d') <= '{td_dt2}' "

    if stat:
        sql += f"     and p.pos_stat = '{stat}' "

    if wl:
        if wl == 'WIN':
            sql += f" and p.val_tot > p.tot_out_cnt "
        elif wl == 'LOSE':
            sql += f" and p.val_tot <= p.tot_out_cnt "

    if buy_strat_name:
        sql += f"     and p.buy_strat_name = '{buy_strat_name}' "

    if buy_strat_freq:
        sql += f"     and p.buy_strat_freq = '{buy_strat_freq}' "

    if sell_strat_name:
        sql += f"     and p.sell_strat_name = '{sell_strat_name}' "

    if sell_strat_freq:
        sql += f"     and p.sell_strat_freq = '{sell_strat_freq}' "

    if test_txn_yn in ('Y', 'N'):
            sql += f"      and test_txn_yn = '{test_txn_yn}' "

    sql += f"         {group_by_sql} "

    sql += "          ) x "
    sql += f"  {order_by_sql} "

    if lmt:
        sql += f"limit {lmt}"


    h = build_sql_display(sql, t)
    m, u, d = html_add(more=h, m=m, u=u, d=d)
    return m, u, d

#<=====>#

def add_report_summary(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report_summary(m, u, d, h)")

    m, u, d = add_report(
        t='Summary - All Time - Combined', 
        test_txn_yn='N', 
        m=m, u=u, d=d)
    m, u, d = add_report(
        t='Summary - All Time - Test', 
        test_txn_yn='Y', 
        m=m, u=u, d=d)
    m, u, d = add_report(
        t='Summary - All Time - Live', 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_status(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report_summary_status(m, u, d, h)")

    m, u, d = add_report(
        t='Summary - By Status - All Time - *', 
        inc_stat=True, 
        test_txn_yn='N', 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_closed(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report_summary_closed(m, u, d, h)")

    m, u, d = add_report(
        t='Summary - Closed Status - *', 
        inc_stat=True, 
        stat='CLOSE', 
        test_txn_yn='N', 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_mkt(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report_summary_mkt(m, u, d, h)")

    m, u, d = add_report(
        t='Markets Summary - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        stat='OPEN', 
        test_txn_yn='ALL', 
        order_by_sql="Order by x.prod_id, x.pos_stat desc, x.test_txn_yn desc ", 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_mkt_closed(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report_summary_mkt_closed(m, u, d, h)")

    m, u, d = add_report(
        t='Markets Summary - Closed Positions - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        stat='CLOSE', 
        test_txn_yn='ALL', 
        order_by_sql="Order by x.prod_id, x.pos_stat desc, x.test_txn_yn desc ", 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_mkt_opened_today(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    today = now_utc_get()

    m, u, d = add_report(
        t='Markets Summary - Opened Today - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        sd_dt1=today, 
        test_txn_yn='ALL', 
        order_by_sql="Order by x.prod_id desc, x.test_txn_yn desc, x.pos_stat desc", 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_mkt_closed_today(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    today = now_utc_get()

    m, u, d = add_report(
        t='Markets Summary - Opened Today - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        td_dt1=today, 
        test_txn_yn='ALL', 
        order_by_sql="Order by x.prod_id desc, x.test_txn_yn desc, x.pos_stat desc", 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_winlose(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report_summary_winlose(m, u, d, h)")

    m, u, d = add_report(
        t='Win-Lose Summary - *', 
        inc_stat=True, 
        inc_wl=True, 
        wl=None, 
        test_txn_yn='ALL', 
        order_by_sql=None, 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_winlose_open(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    m, u, d = add_report(
        t='Win-Lose Summary - Open Positions - *', 
        inc_stat=True, 
        inc_wl=True, 
        stat='OPEN', 
        wl=None, 
        test_txn_yn='ALL', 
        order_by_sql=None, 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_winlose_closed(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    m, u, d = add_report(
        t='Win-Lose Summary - Closed Positions - *', 
        inc_stat=True, 
        inc_wl=True, 
        stat='CLOSE', 
        wl=None, 
        test_txn_yn='ALL', 
        order_by_sql=None, 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_opened_today(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    today = now_utc_get()

    m, u, d = add_report(
        t='Summary - Opened Today', 
        inc_prod_id=False, 
        inc_pos_id=False, 
        inc_sd_dt=False, 
        inc_td_dt=False, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=False, 
        inc_buy_strat_freq=False, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=today, 
        td_dt2=None, 
        stat='CLOSE', 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='N', 
        order_by_sql=None, 
        lmt=None,
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_closed_today(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    today = now_utc_get()

    m, u, d = add_report(
        t='Summary - Closed Today', 
        inc_prod_id=False, 
        inc_pos_id=False, 
        inc_sd_dt=False, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=False, 
        inc_buy_strat_freq=False, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=today, 
        td_dt2=None, 
        stat='CLOSE', 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='N', 
        order_by_sql=None, 
        lmt=None,
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_daily_opened(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    m, u, d = add_report(
        t='Daily Sales Summary - All Time', 
        inc_prod_id=False, 
        inc_pos_id=False, 
        inc_sd_dt=False, 
        inc_td_dt=True, 
        inc_stat=False, 
        inc_wl=True, 
        inc_buy_strat_name=False, 
        inc_buy_strat_freq=False, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat='CLOSE', 
        wl=True, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='N', 
        order_by_sql="Order by x.td_dt desc", 
        lmt=None,
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_daily_closed(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    m, u, d = add_report(
        t='Daily Sales Summary - All Time', 
        inc_prod_id=False, 
        inc_pos_id=False, 
        inc_sd_dt=False, 
        inc_td_dt=True, 
        inc_stat=False, 
        inc_wl=False, 
        inc_buy_strat_name=False, 
        inc_buy_strat_freq=False, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat='CLOSE', 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='N', 
        order_by_sql="Order by x.td_dt desc", 
        lmt=None,
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_pos_closed(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    m, u, d = add_report(
        t='Markets - Open Positions', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=False, 
        inc_td_dt=False, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat='CLOSE', 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id, x.pos_id", 
        lmt=None,
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_mkt_pos_open(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    m, u, d = add_report(
        t='Markets - Open Positions', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=False, 
        inc_td_dt=False, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat='OPEN', 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id, x.pos_id", 
        lmt=None,
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_mkt_pos_closed_today(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    today = now_utc_get()

    m, u, d = add_report(
        t=f'Markets - Closed Positions - Today - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=today, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

#When you are using Flask, it is generally a good practice to run the app in the debug mode.
#You can also control the port number. Make the following changes in your python file:
#app.run(debug=True, port=3134)
#Now run the code and go to http://localhost:3134 to see the output.
#If you want to make this application accessible externally using the IP address,
#then you need to tell Flask by specifying the host parameter. Make the following change in your python file:
#app.run(host='0.0.0.0', debug=True, port=3134)
#Run the code and go to http://x.x.x.x:3134 (replace x.x.x.x with the right IP address) to see your external web server live!

#template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#template_dir = os.path.join(template_dir, 'flask')
#template_dir = os.path.join(template_dir, 'templates')
## hard coded absolute path for testing purposes
#working = 'C:\Python34\pro\\frontend\    emplates'
#print(working == template_dir)
#app = Flask(__name__, template_folder=template_dir)

app = Flask(__name__)

now = datetime.now(timezone.utc)

#<=====>#

def ext_home() -> str:
    print(str(datetime.now(timezone.utc)) + " home()")
    tn = build_topnav()
    today = now_utc_get()

    m     = None
    u     = None
    d     = None

    pt    = 'Home'

    m, u, d = add_bals_total(t='Total Balance', m=m, u=u, d=d)

    m, u, d = add_report_summary(m=m, u=u, d=d)

    m, u, d = add_report_summary_status(m=m, u=u, d=d)

    m, u, d = add_report_summary_winlose_closed(m=m, u=u, d=d)

    m, u, d = add_report_summary_open(m=m, u=u, d=d)

    m, u, d = add_report_summary_closed_today(m=m, u=u, d=d)

    m, u, d = add_report_summary_daily_closed(m=m, u=u, d=d)

    m, u, d = add_report_summary_mkt_closed(m=m, u=u, d=d)

    m, u, d = add_report_summary_mkt_open(m=m, u=u, d=d)

    m, u, d = add_report_mkt_pos_open(m=m, u=u, d=d)

    m, u, d = add_report_mkt_pos_closed_today(m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_all_reports_test() -> str:
    print(str(datetime.now(timezone.utc)) + " all_reports_test()")
    tn = build_topnav()

    today = now_utc_get()

    m     = None
    u     = None
    d     = None

    pt    = 'All Reports For Testing'

    m, u, d = add_report_summary(m=m, u=u, d=d)
    m, u, d = add_report_summary_status(m=m, u=u, d=d)
    m, u, d = add_report_summary_open(m=m, u=u, d=d)
    m, u, d = add_report_summary_closed(m=m, u=u, d=d)

    m, u, d = add_report_summary_mkt(m=m, u=u, d=d)
    m, u, d = add_report_summary_mkt_open(m=m, u=u, d=d)
    m, u, d = add_report_summary_mkt_closed(m=m, u=u, d=d)

    m, u, d = add_report_summary_winlose(m=m, u=u, d=d)
    m, u, d = add_report_summary_winlose_open(m=m, u=u, d=d)
    m, u, d = add_report_summary_winlose_closed(m=m, u=u, d=d)

    m, u, d = add_report_summary_opened_today(m=m, u=u, d=d)
    m, u, d = add_report_summary_closed_today(m=m, u=u, d=d)

    m, u, d = add_report_summary_daily_opened(m=m, u=u, d=d)
    m, u, d = add_report_summary_daily_closed(m=m, u=u, d=d)

    m, u, d = add_report_summary_mkt_opened_today(m=m, u=u, d=d)
    m, u, d = add_report_summary_mkt_closed_today(m=m, u=u, d=d)

    m, u, d = add_report_summary_mkt_open(m=m, u=u, d=d)

    m, u, d = add_report_mkt_pos_open(m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_balances() -> str:
    print(str(datetime.now(timezone.utc)) + " balances()")
    tn = build_topnav()

    m = None
    u = None
    d = None

    pt = 'My Balances'

    m, u, d = add_bals_total(t='Total Balance', m=m, u=u, d=d)

    m, u, d = html_hr_add(m=m, u=u, d=d)
    # sql = ""
    # sql += "select z.* from ( "
    # sql += "select x.symb "
    # sql += "  , x.open_cnt "
    # sql += "  , x.sell_cnt "
    # sql += "  , x.close_cnt "
    # sql += "  , x.open_hold_cnt "
    # sql += "  , round(x.open_hold_cnt * x.curr_prc_usd, 3) as open_hold_usd "
    # sql += "  , x.sell_hold_cnt "
    # sql += "  , round(x.sell_hold_cnt * x.curr_prc_usd, 3) as sell_hold_usd "
    # sql += "  , x.close_hold_cnt "
    # sql += "  , round(x.close_hold_cnt * x.curr_prc_usd, 3) as close_hold_usd "
    # sql += "  , round(x.curr_prc_usd,5) as curr_prc_usd "
    # sql += "  , x.bal_tot "
    # sql += "  , round(x.curr_val_usd,3) as bal_usd "
    # sql += "  , x.open_hold_cnt + x.sell_hold_cnt + x.close_hold_cnt as need_cnt_tot "
    # sql += "  , round((x.open_hold_cnt + x.sell_hold_cnt + x.close_hold_cnt) * x.curr_prc_usd, 3) as need_val_usd "
    # sql += "  , x.bal_tot - (x.open_hold_cnt + x.close_hold_cnt) as over_under_cnt "
    # sql += "  , round((x.bal_tot - (x.open_hold_cnt + x.close_hold_cnt)) * x.curr_prc_usd, 3) as over_under_usd "
    # sql += "from ( "
    # sql += "select distinct p.buy_curr_symb as symb "
    # sql += "  , sum(case when p.pos_stat in ( 'OPEN' ) then 1 else 0 end) as open_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'OPEN' ) then p.hold_cnt else 0 end) as open_hold_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'OPEN' ) then p.pocket_cnt else 0 end) as open_pocket_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'OPEN' ) then p.clip_cnt else 0 end) as open_clip_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'OPEN' ) then p.buy_cnt else 0 end) as open_buy_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'OPEN' ) then p.sell_cnt_tot else 0 end) as open_sell_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'OPEN' ) then p.buy_cnt else 0 end) - sum(case when p.pos_stat = 'OPEN' then p.sell_cnt_tot else 0 end) - sum(case when p.pos_stat in ( 'OPEN' ) then p.hold_cnt else 0 end) as open_buy_sell_diff "
    # sql += "  , sum(case when p.pos_stat in ( 'SELL' ) then 1 else 0 end) as sell_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'SELL' ) then p.buy_cnt else 0 end) as sell_hold_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'SELL' ) then p.pocket_cnt else 0 end) as sell_pocket_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'SELL' ) then p.clip_cnt else 0 end) as sell_clip_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'SELL' ) then p.buy_cnt else 0 end) as sell_buy_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'SELL' ) then p.sell_cnt_tot else 0 end) as selln_sell_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'SELL' ) then p.buy_cnt else 0 end) - sum(case when p.pos_stat = 'OPEN' then p.sell_cnt_tot else 0 end)  as sell_buy_sell_diff "
    # sql += "  , sum(case when p.pos_stat in ( 'CLOSE' ) then 1 else 0 end) as close_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'CLOSE' ) then p.hold_cnt else 0 end) as close_hold_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'CLOSE' ) then p.pocket_cnt else 0 end) as close_pocket_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'CLOSE' ) then p.clip_cnt else 0 end) as close_clip_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'CLOSE' ) then p.buy_cnt else 0 end) as close_buy_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'CLOSE' ) then p.sell_cnt_tot else 0 end) as close_sell_cnt "
    # sql += "  , sum(case when p.pos_stat in ( 'CLOSE' ) then p.buy_cnt else 0 end) - sum(case when p.pos_stat = 'OPEN' then p.sell_cnt_tot else 0 end)  as close_buy_sell_diff "
    # sql += "  , sum(p.hold_cnt) as hold_cnt "
    # sql += "  , b.bal_tot "
    # sql += "  , b.curr_prc_usd "
    # sql += "  , b.curr_val_usd "
    # sql += "  , ((b.bal_tot - sum(case when p.pos_stat in ( 'CLOSE' ) then p.hold_cnt else 0 end)) * b.curr_prc_usd) as var_usd "
    # sql += "  from cbtrade.poss p "
    # sql += "  join cbtrade.bals b on b.symb = p.buy_curr_symb "
    # sql += "  where 1=1 "
    # sql += "  and p.ignore_tf = 0 "
    # sql += "  group by p.prod_id "
    # sql += "  order by 1 "
    # sql += ") x "
    # sql += ") z "
    # sql += "where 1=1 "


    sql = """
        SELECT z.*
        FROM (
            SELECT x.symb,
                x.open_cnt,
                x.sell_cnt,
                x.close_cnt,
                x.open_hold_cnt,
                ROUND(x.open_hold_cnt * x.curr_prc_usd, 3) AS open_hold_usd,
                x.sell_hold_cnt,
                ROUND(x.sell_hold_cnt * x.curr_prc_usd, 3) AS sell_hold_usd,
                x.close_hold_cnt,
                ROUND(x.close_hold_cnt * x.curr_prc_usd, 3) AS close_hold_usd,
                ROUND(x.curr_prc_usd, 5) AS curr_prc_usd,
                x.bal_tot,
                ROUND(x.curr_val_usd, 3) AS bal_usd,
                x.open_hold_cnt + x.sell_hold_cnt + x.close_hold_cnt AS need_cnt_tot,
                ROUND((x.open_hold_cnt + x.sell_hold_cnt + x.close_hold_cnt) * x.curr_prc_usd, 3) AS need_val_usd,
                x.bal_tot - (x.open_hold_cnt + x.close_hold_cnt) AS over_under_cnt,
                ROUND((x.bal_tot - (x.open_hold_cnt + x.close_hold_cnt)) * x.curr_prc_usd, 3) AS over_under_usd
            FROM (
                SELECT b.symb,
                    SUM(CASE WHEN p.pos_stat IN ('OPEN') THEN 1 ELSE 0 END) AS open_cnt,
                    SUM(CASE WHEN p.pos_stat IN ('OPEN') THEN p.hold_cnt ELSE 0 END) AS open_hold_cnt,
                    SUM(CASE WHEN p.pos_stat IN ('SELL') THEN 1 ELSE 0 END) AS sell_cnt,
                    SUM(CASE WHEN p.pos_stat IN ('SELL') THEN p.buy_cnt ELSE 0 END) AS sell_hold_cnt,
                    SUM(CASE WHEN p.pos_stat IN ('CLOSE') THEN 1 ELSE 0 END) AS close_cnt,
                    SUM(CASE WHEN p.pos_stat IN ('CLOSE') THEN p.hold_cnt ELSE 0 END) AS close_hold_cnt,
                    b.bal_tot,
                    b.curr_prc_usd,
                    b.curr_val_usd
                FROM cbtrade.bals b
                LEFT OUTER JOIN cbtrade.poss p 
                ON p.buy_curr_symb = b.symb
                AND p.ignore_tf = 0
                AND p.test_txn_yn = 'N'
                GROUP BY b.symb, b.bal_tot, b.curr_prc_usd, b.curr_val_usd
            ) x
        ) z
        WHERE 1=1
        ORDER BY bal_usd DESC
        """

    t = 'Current Balances'
    # ORDER BY already included in main SQL - don't append duplicate
#    print_sql(sql)
    h = build_sql_display(sql, t)
    m, u, d = html_add(more=h, m=m, u=u, d=d)

#    m, u, d = add_table_dump('bals', m, u, d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def add_report_summary_open(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report_summary_open(m, u, d, h)")

    m, u, d = add_report(
        t='Summary - Open Status - *', 
        inc_stat=True, 
        inc_wl=True, 
        stat='OPEN', 
        test_txn_yn='N', 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_summary_mkt_open(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report_summary_mkt_open(m, u, d, h)")

    m, u, d = add_report(
        t='Markets Summary - Open Positions - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        stat='OPEN', 
        test_txn_yn='ALL', 
        order_by_sql="Order by x.prod_id, x.pos_stat desc, x.test_txn_yn desc ", 
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def add_report_pos_open(m, u, d) -> str:
    print('')
    BoW(str(datetime.now(timezone.utc)) + f" add_report(m, u, d, h)")

    m, u, d = add_report(
        t='Markets - Open Positions', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_test=True, 
        stat='OPEN', 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id, x.pos_id", 
        lmt=None,
        m=m, u=u, d=d)

    return m, u, d

#<=====>#

def ext_open_positions() -> str:
    print(str(datetime.now(timezone.utc)) + " open_positions()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = 'Open Positions'

    m, u, d = add_report_summary_open(m=m, u=u, d=d)
    m, u, d = add_report_summary_mkt_open(m=m, u=u, d=d)
    m, u, d = add_report_pos_open(m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_closed_positions() -> str:
    print(str(datetime.now(timezone.utc)) + " closed_positions()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = 'Closed Positions'

    m, u, d = add_report_summary_closed(m=m, u=u, d=d)
    m, u, d = add_report_summary_mkt_closed(m=m, u=u, d=d)
    m, u, d = add_report_pos_closed(m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_buys_recent() -> str:
    print(str(datetime.now(timezone.utc)) + " buys_recent()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = 'Buys - Recent'

    disp_cnt = 100
    m, u, d = add_report(
        t=f'Last {disp_cnt} Opened Positions', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat=None, 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='N', 
        order_by_sql="Order by x.pos_id desc", 
        lmt=disp_cnt,
        m=m, u=u, d=d)

    disp_cnt = 100
    m, u, d = add_report(
        t=f'Last {disp_cnt} Opened Positions - Test', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=False, 
        inc_sell_strat_freq=False, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat=None, 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.pos_id desc", 
        lmt=disp_cnt,
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sells_recent() -> str:
    print(str(datetime.now(timezone.utc)) + " sells_recent()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = 'Sells - Recent'

    disp_cnt = 100
    m, u, d = add_report(
        t=f'Last {disp_cnt} Closed Positions', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat='CLOSE', 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='N', 
        order_by_sql="Order by x.td_dt desc", 
        lmt=disp_cnt,
        m=m, u=u, d=d)

    disp_cnt = 100
    m, u, d = add_report(
        t=f'Last {disp_cnt} Closed Positions - Test', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_wl=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        pos_id=None, 
        sd_dt1=None, 
        sd_dt2=None, 
        td_dt1=None, 
        td_dt2=None, 
        stat='CLOSE', 
        wl=None, 
        buy_strat_name=None, 
        buy_strat_freq=None, 
        sell_strat_name=None, 
        sell_strat_freq=None, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.td_dt desc", 
        lmt=disp_cnt,
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_buy_strats() -> str:
    print(str(datetime.now(timezone.utc)) + " buy_strats()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = 'Buys Strats'

    m, u, d = add_report(
        t=f'Buy Strats Summary - Closed', 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        stat='CLOSE', 
        test_txn_yn='N', 
        order_by_sql="order by x.gain_loss_pct_hr desc ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Buy Strats Summary - Closed', 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        stat='CLOSE', 
        test_txn_yn='N', 
        order_by_sql="order by x.buy_strat_name, x.buy_strat_freq ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_mkt_buy_strats() -> str:
    print(str(datetime.now(timezone.utc)) + " mkt_buy_strats()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = 'Market Buys Strats'

    m, u, d = add_report(
        t=f'Market Buy Strats Summary - Closed', 
        inc_prod_id=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        stat='CLOSE', 
        test_txn_yn='N', 
        order_by_sql="order by x.gain_loss_pct_hr desc ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Market Buy Strats Summary - Closed', 
        inc_prod_id=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        stat='CLOSE', 
        test_txn_yn='N', 
        order_by_sql="order by x.prod_id, x.buy_strat_name, x.buy_strat_freq ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_markets() -> str:
    print(str(datetime.now(timezone.utc)) + " markets()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = 'Markets'

    m, u, d = add_report(
        t=f'Markets - By Gain Rate', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        test_txn_yn='N', 
        order_by_sql="Order by x.gain_loss_pct_hr desc ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Markets - By Product', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Markets - Test - By Gain Rate', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.gain_loss_pct_hr desc ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Markets - Test - By Product', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_market(mkt) -> str:
    print(str(datetime.now(timezone.utc)) + f" market({mkt})")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    mkt = mkt.replace('_','-')

    pt    = f'Market - {mkt}'

    m, u, d = add_report(
        t=f'Markets Summary', 
        inc_prod_id=True, 
        prod_id=mkt, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Markets Summary - Status', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=mkt, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Market Buy Strats Summary - Open', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_test=True, 
        prod_id=mkt, 
        stat='OPEN', 
        test_txn_yn='ALL', 
        order_by_sql="order by x.prod_id, x.buy_strat_name, x.buy_strat_freq, x.pos_stat ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Market Buy Strats Summary - Closed', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_test=True, 
        prod_id=mkt, 
        stat='CLOSE', 
        test_txn_yn='ALL', 
        order_by_sql="order by x.prod_id, x.buy_strat_name, x.buy_strat_freq, x.pos_stat ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Market Buy Strats Summary - Test', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_test=True, 
        prod_id=mkt, 
        stat=None, 
        test_txn_yn='Y', 
        order_by_sql="order by x.prod_id, x.buy_strat_name, x.buy_strat_freq, x.pos_stat ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Markets Positions - Open', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=mkt, 
        stat='OPEN', 
        test_txn_yn='N', 
        order_by_sql="Order by x.pos_id desc ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Markets Positions - Closed', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=mkt, 
        stat='CLOSE', 
        test_txn_yn='N', 
        order_by_sql="Order by x.pos_id desc ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Markets - Test - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=mkt, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Markets Positions - Test - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=mkt, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_all() -> str:
    print("sales_all()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary'

    m, u, d = add_report(
        t=f'Sales Summary', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary Positions', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - Test - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - Test - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_today() -> str:
    print(str(datetime.now(timezone.utc)) + " sales_today()")
    tn = build_topnav()

    today = now_utc_get()

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - Today'

    m, u, d = add_report(
        t=f'Sales Summary - Today - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=today, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - Today - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=today, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary Positions - Today - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=today, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - Today - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=today, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_yesterday() -> str:
    print(str(datetime.now(timezone.utc)) + " sales_yesterday()")
    tn = build_topnav()

    today = now_utc_get()
    one_day = timedelta(days=1)
    yesterday = today - one_day

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - Yesterday'

    m, u, d = add_report(
        t=f'Sales Summary - Yesterday - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=yesterday, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - Yesterday - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=yesterday, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary Positions - Yesterday - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=yesterday, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - Yesterday - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=yesterday, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_day_cntd(day_cnt) -> str:
    print("{} sales_{}d()".format(str(datetime.now(timezone.utc)), day_cnt))
    tn = build_topnav()

    td = now_utc_get()
    days = timedelta(days=int(day_cnt)-1)
    sd = td - days

    m     = None
    u     = None
    d     = None

    sd_str = sd.strftime('%Y-%m-%d')
    td_str = td.strftime('%Y-%m-%d')

    dt_str = 'Last {} Days - {} - {}'.format(day_cnt, sd_str, td_str)

    pt    = f'Sales Summary - {dt_str}'

    m, u, d = add_report(
        t=f'Sales Summary - {dt_str} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=sd, 
        td_dt2=td, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - {dt_str} - Test - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=sd, 
        td_dt2=td, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary Positions - {dt_str} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=sd, 
        td_dt2=td, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - {dt_str} - Test - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=sd, 
        td_dt2=td, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)
    return tn, pt, sh

#<=====>#

def ext_sales_dt(dt) -> str:
    print(str(datetime.now(timezone.utc)) + " sales_dt()")
    tn = build_topnav()

    td = datetime.strptime(dt, '%Y-%m-%d')
    td_str = td.strftime('%Y-%m-%d')
    dt_str = '{}'.format(td_str)

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - {dt_str}'

    m, u, d = add_report(
        t=f'Sales Summary - {dt_str} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - {dt_str} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary Positions - {dt_str} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - {dt_str} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_month(yr,m) -> str:
    print(str(datetime.now(timezone.utc)) + " sales_month()")
    tn = build_topnav()

    yr = int(yr)
    m = int(m)
    if yr < 2019 or yr > 2049:
        yr = date.today.year
    if m < 1 or m > 12:
        m = date.today.month

    td_dt1 = date(yr, m, 1)
    td_dt2 = date(yr, m, calendar.monthrange(yr, m)[-1])

    print(f'td_dt1 : {td_dt1}, {type(td_dt1)}')
    print(f'td_dt2 : {td_dt2}, {type(td_dt2)}')

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - {td_dt1} - {td_dt2}'

    m, u, d = add_report(
        t=f'Sales Summary - {td_dt1} - {td_dt2} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - {td_dt1} - {td_dt2} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary Positions - {td_dt1} - {td_dt2} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - {td_dt1} - {td_dt2} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)



    return tn, pt, sh

#<=====>#

def ext_sales_yr(yr) -> str:
    print(str(datetime.now(timezone.utc)) + " sales_year()")
    tn = build_topnav()

    yr = int(yr)
    if yr < 2019 or yr > 2049:
        yr = date.today.year

    td_dt1 = date(yr, 1, 1)
    td_dt2 = date(yr, 12, 31)

    print(f'td_dt1 : {td_dt1}, {type(td_dt1)}')
    print(f'td_dt2 : {td_dt2}, {type(td_dt2)}')

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - {yr}'

    m, u, d = add_report(
        t=f'Sales Summary - {yr} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Sales Summary - {yr} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='N', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_all_test() -> str:
    print("sales_all_test()")
    tn = build_topnav()

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - Test'

    m, u, d = add_report(
        t=f'Sales Summary - Test - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Positions - Test - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_today_test() -> str:
    print(str(datetime.now(timezone.utc)) + " sales_today_test()")
    tn = build_topnav()

    today = now_utc_get()

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - Today - Test'

    m, u, d = add_report(
        t=f'Sales Summary - Today - Test - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=today, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Positions - Today - Test - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=today, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_yesterday_test() -> str:
    print(str(datetime.now(timezone.utc)) + " sales_yesterday_test()")
    tn = build_topnav()

    today = now_utc_get()
    one_day = timedelta(days=1)
    yesterday = today - one_day

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - Yesterday - Test'

    m, u, d = add_report(
        t=f'Sales Summary - Yesterday - Test - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=yesterday, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Positions - Yesterday - Test - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=yesterday, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_day_cntd_test(day_cnt) -> str:
    print("{} sales_{}d_test()".format(str(datetime.now(timezone.utc)), day_cnt))
    tn = build_topnav()

    td = now_utc_get()
    days = timedelta(days=int(day_cnt)-1)
    sd = td - days

    m     = None
    u     = None
    d     = None

    sd_str = sd.strftime('%Y-%m-%d')
    td_str = td.strftime('%Y-%m-%d')

    dt_str = 'Last {} Days - {} - {}'.format(day_cnt, sd_str, td_str)

    pt    = f'Sales Summary - Test - {dt_str}'

    m, u, d = add_report(
        t=f'Sales Summary - Test - {dt_str} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=sd, 
        td_dt2=td, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Positions - Test - {dt_str} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=sd, 
        td_dt2=td, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)
    return tn, pt, sh

#<=====>#

def ext_sales_dt_test(dt) -> str:
    print(str(datetime.now(timezone.utc)) + " sales_dt_test()")
    tn = build_topnav()

    td = datetime.strptime(dt, '%Y-%m-%d')
    td_str = td.strftime('%Y-%m-%d')
    dt_str = '{}'.format(td_str)

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - Test - {dt_str}'

    m, u, d = add_report(
        t=f'Sales Summary - Test - {dt_str} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Positions - Test - {dt_str} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_month_test(yr,m) -> str:
    print(str(datetime.now(timezone.utc)) + " sales_month_test()")
    tn = build_topnav()

    yr = int(yr)
    m = int(m)
    if yr < 2019 or yr > 2049:
        yr = date.today.year
    if m < 1 or m > 12:
        m = date.today.month

    td_dt1 = date(yr, m, 1)
    td_dt2 = date(yr, m, calendar.monthrange(yr, m)[-1])

    print(f'td_dt1 : {td_dt1}, {type(td_dt1)}')
    print(f'td_dt2 : {td_dt2}, {type(td_dt2)}')

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - Test - {td_dt1} - {td_dt2}'

    m, u, d = add_report(
        t=f'Sales Summary - Test - {td_dt1} - {td_dt2} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Positions - Test - {td_dt1} - {td_dt2} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_sales_yr_test(yr) -> str:
    print(str(datetime.now(timezone.utc)) + " sales_year_test()")
    tn = build_topnav()

    yr = int(yr)
    if yr < 2019 or yr > 2049:
        yr = date.today.year

    td_dt1 = date(yr, 1, 1)
    td_dt2 = date(yr, 12, 31)

    print(f'td_dt1 : {td_dt1}, {type(td_dt1)}')
    print(f'td_dt2 : {td_dt2}, {type(td_dt2)}')

    m     = None
    u     = None
    d     = None

    pt    = f'Sales Summary - Test - {yr}'

    m, u, d = add_report(
        t=f'Sales Summary - Test - {yr} - *', 
        inc_prod_id=True, 
        inc_stat=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    m, u, d = add_report(
        t=f'Positions - Test - {yr} - *', 
        inc_prod_id=True, 
        inc_pos_id=True, 
        inc_sd_dt=True, 
        inc_td_dt=True, 
        inc_stat=True, 
        inc_buy_strat_name=True, 
        inc_buy_strat_freq=True, 
        inc_sell_strat_name=True, 
        inc_sell_strat_freq=True, 
        inc_test=True, 
        prod_id=None, 
        td_dt1=td_dt1, 
        td_dt2=td_dt2, 
        test_txn_yn='Y', 
        order_by_sql="Order by x.prod_id ", 
        m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#

def ext_db_size() -> str:
    print(str(datetime.now(timezone.utc)) + " db_size()")
    tn = build_topnav()

    m   = None
    u    = None
    d  = None

    pt = 'MySQL Database'

    st = 'MySQL Health Check'

    t = 'MySQL DB Size'
    sql = " "
    sql +=  "SELECT x.table_schema as db_name,"
    sql +=  "    sum( data_length + index_length ) / 1024 / 1024 as db_size_mb,"
    sql +=  "    sum( data_free )/ 1024 / 1024 as free_size_mb "
    sql +=  "FROM information_schema.TABLES x "
    sql +=  "GROUP BY x.table_schema "
    h = build_sql_display(sql, t)

    m, u, d = html_add(more=h, m=m, u=u, d=d)

    t = 'DB Size with Tables'
    sql = " "
    sql +=  "SELECT x.table_schema as db_name, x.table_name as table_name,"
    sql +=  "    sum( data_length + index_length ) / 1024 / 1024 as db_size_mb,"
    sql +=  "    sum( data_free )/ 1024 / 1024 as free_size_mb "
    sql +=  "FROM information_schema.TABLES x "
    sql +=  "GROUP BY x.table_schema, x.table_name"
    h = build_sql_display(sql, t)

    m, u, d = html_add(more=h, m=m, u=u, d=d)

    sh = html_comb(m=m, u=u, d=d)

    return tn, pt, sh

#<=====>#
# Fast Performance Functions Using Pre-Calculated Tables  
#<=====>#

def add_fast_market_summary(title="Market Performance Summary", status_filter="CLOSE", m=None, u=None, d=None) -> tuple[str, str, str]:
    """Fast market performance using pre-calculated trade_perfs table"""
    
    sql = f"""
    SELECT 
        tp.prod_id,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tp.tot_close_cnt
            WHEN '{status_filter}' = 'OPEN' THEN tp.tot_open_cnt  
            ELSE tp.tot_cnt
        END as positions,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tp.win_close_cnt
            WHEN '{status_filter}' = 'OPEN' THEN tp.win_open_cnt
            ELSE tp.win_cnt
        END as wins,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tp.lose_close_cnt
            WHEN '{status_filter}' = 'OPEN' THEN tp.lose_open_cnt
            ELSE tp.lose_cnt
        END as losses,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN CONCAT(ROUND(tp.win_close_pct, 1), ' %')
            WHEN '{status_filter}' = 'OPEN' THEN CONCAT(ROUND(tp.win_open_pct, 1), ' %')
            ELSE CONCAT(ROUND(tp.win_pct, 1), ' %')
        END as win_rate,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN CONCAT('$ ', ROUND(tp.gain_loss_close_amt, 2))
            WHEN '{status_filter}' = 'OPEN' THEN CONCAT('$ ', ROUND(tp.gain_loss_open_amt, 2))
            ELSE CONCAT('$ ', ROUND(tp.gain_loss_amt, 2))
        END as total_pnl,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN CONCAT(ROUND(tp.gain_loss_close_pct_hr, 6), ' %')
            WHEN '{status_filter}' = 'OPEN' THEN CONCAT(ROUND(tp.gain_loss_open_pct_hr, 6), ' %')
            ELSE CONCAT(ROUND(tp.gain_loss_pct_hr, 6), ' %')
        END as pct_per_hour
    FROM cbtrade.trade_perfs tp
    WHERE tp.lta = 'L'  -- Live trades only
    AND (
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tp.tot_close_cnt
            WHEN '{status_filter}' = 'OPEN' THEN tp.tot_open_cnt
            ELSE tp.tot_cnt
        END
    ) > 0
    ORDER BY 
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tp.gain_loss_close_pct_hr
            WHEN '{status_filter}' = 'OPEN' THEN tp.gain_loss_open_pct_hr
            ELSE tp.gain_loss_pct_hr
        END DESC
    """
    
    h = build_sql_display(sql, title)
    m, u, d = html_add(more=h, m=m, u=u, d=d)
    return m, u, d

def add_fast_strategy_summary(title="Strategy Performance Summary", status_filter="CLOSE", limit_count=20, m=None, u=None, d=None) -> tuple[str, str, str]:
    """Fast strategy performance using pre-calculated trade_strat_perfs table"""
    
    sql = f"""
    SELECT 
        tsp.prod_id,
        tsp.buy_strat_name,
        tsp.buy_strat_freq,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tsp.tot_close_cnt
            WHEN '{status_filter}' = 'OPEN' THEN tsp.tot_open_cnt
            ELSE tsp.tot_cnt
        END as positions,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tsp.win_close_cnt
            WHEN '{status_filter}' = 'OPEN' THEN tsp.win_open_cnt
            ELSE tsp.win_cnt
        END as wins,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN CONCAT(ROUND(tsp.win_close_pct, 1), ' %')
            WHEN '{status_filter}' = 'OPEN' THEN CONCAT(ROUND(tsp.win_open_pct, 1), ' %')
            ELSE CONCAT(ROUND(tsp.win_pct, 1), ' %')
        END as win_rate,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN CONCAT('$ ', ROUND(tsp.gain_loss_close_amt, 2))
            WHEN '{status_filter}' = 'OPEN' THEN CONCAT('$ ', ROUND(tsp.gain_loss_open_amt, 2))
            ELSE CONCAT('$ ', ROUND(tsp.gain_loss_amt, 2))
        END as total_pnl,
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN CONCAT(ROUND(tsp.gain_loss_close_pct_hr, 6), ' %')
            WHEN '{status_filter}' = 'OPEN' THEN CONCAT(ROUND(tsp.gain_loss_open_pct_hr, 6), ' %')
            ELSE CONCAT(ROUND(tsp.gain_loss_pct_hr, 6), ' %')
        END as pct_per_hour
    FROM cbtrade.trade_strat_perfs tsp
    WHERE tsp.lta = 'L'  -- Live trades only
    AND (
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tsp.tot_close_cnt
            WHEN '{status_filter}' = 'OPEN' THEN tsp.tot_open_cnt
            ELSE tsp.tot_cnt
        END
    ) > 5  -- Only strategies with meaningful sample size
    ORDER BY 
        CASE 
            WHEN '{status_filter}' = 'CLOSE' THEN tsp.gain_loss_close_pct_hr
            WHEN '{status_filter}' = 'OPEN' THEN tsp.gain_loss_open_pct_hr
            ELSE tsp.gain_loss_pct_hr
        END DESC
    LIMIT {limit_count}
    """
    
    h = build_sql_display(sql, title)
    m, u, d = html_add(more=h, m=m, u=u, d=d)
    return m, u, d

def add_fast_overall_summary(title="Overall Performance Summary", m=None, u=None, d=None) -> tuple[str, str, str]:
    """Fast overall performance aggregating trade_perfs table"""
    
    sql = """
    SELECT 
        'Live Trading' as category,
        SUM(tp.tot_close_cnt) as total_positions,
        SUM(tp.win_close_cnt) as total_wins, 
        SUM(tp.lose_close_cnt) as total_losses,
        CONCAT(ROUND(SUM(tp.win_close_cnt) / SUM(tp.tot_close_cnt) * 100, 2), ' %') as overall_win_rate,
        CONCAT('$ ', ROUND(SUM(tp.gain_loss_close_amt), 2)) as total_pnl,
        CONCAT('$ ', ROUND(SUM(tp.win_close_amt), 2)) as total_gains,
        CONCAT('$ ', ROUND(ABS(SUM(tp.lose_close_amt)), 2)) as total_losses_amt,
        CONCAT('$ ', ROUND(SUM(tp.fees_close_cnt_tot), 2)) as total_fees
    FROM cbtrade.trade_perfs tp
    WHERE tp.lta = 'L'  -- Live trades only
    AND tp.tot_close_cnt > 0
    
    UNION ALL
    
    SELECT 
        'Currently Open' as category,
        SUM(tp.tot_open_cnt) as total_positions,
        SUM(tp.win_open_cnt) as total_wins,
        SUM(tp.lose_open_cnt) as total_losses, 
        CONCAT(ROUND(CASE WHEN SUM(tp.tot_open_cnt) > 0 THEN SUM(tp.win_open_cnt) / SUM(tp.tot_open_cnt) * 100 ELSE 0 END, 2), ' %') as overall_win_rate,
        CONCAT('$ ', ROUND(SUM(tp.gain_loss_open_amt), 2)) as total_pnl,
        CONCAT('$ ', ROUND(SUM(tp.win_open_amt), 2)) as total_gains,
        CONCAT('$ ', ROUND(ABS(SUM(tp.lose_open_amt)), 2)) as total_losses_amt,
        CONCAT('$ ', ROUND(SUM(tp.fees_open_cnt_tot), 2)) as total_fees
    FROM cbtrade.trade_perfs tp
    WHERE tp.lta = 'L'  -- Live trades only
    AND tp.tot_open_cnt > 0
    """
    
    h = build_sql_display(sql, title)
    m, u, d = html_add(more=h, m=m, u=u, d=d)
    return m, u, d

def ext_fast_home() -> tuple[str, str, str]:
    """Optimized home page using performance tables - FAST!"""
    tn = build_topnav()
    
    m = None
    u = None  
    d = None
    
    pt = 'Home - Fast Performance Dashboard'
    
    # Overall summary from performance tables (sub-second response)
    m, u, d = add_fast_overall_summary("Overall Trading Performance", m, u, d)
    
    # Top performing markets (sub-second response)
    m, u, d = add_fast_market_summary("Top Markets by Performance", "CLOSE", m, u, d)
    
    # Top performing strategies - limited to top 15 for speed
    m, u, d = add_fast_strategy_summary("Top Strategies by Performance", "CLOSE", 15, m, u, d)
    
    sh = html_comb(m=m, u=u, d=d)
    return tn, pt, sh

def ext_fast_markets() -> tuple[str, str, str]:
    """Optimized markets page using performance tables - FAST!"""
    tn = build_topnav()
    
    m = None
    u = None
    d = None
    
    pt = 'Markets - Fast Performance Dashboard'
    
    # Closed positions by market (sub-second response)
    m, u, d = add_fast_market_summary("Markets - Closed Positions Performance", "CLOSE", m, u, d)
    
    # Open positions by market (sub-second response)
    m, u, d = add_fast_market_summary("Markets - Open Positions Performance", "OPEN", m, u, d)
    
    sh = html_comb(m=m, u=u, d=d)
    return tn, pt, sh

def ext_fast_strategies() -> tuple[str, str, str]:
    """Optimized strategies page using performance tables - FAST!"""
    tn = build_topnav()
    
    m = None
    u = None
    d = None
    
    pt = 'Strategies - Fast Performance Dashboard'
    
    # Top 25 strategies by closed performance (sub-second response)
    m, u, d = add_fast_strategy_summary("Top 25 Strategies - Closed Performance", "CLOSE", 25, m, u, d)
    
    # Current open strategies performance (sub-second response)
    m, u, d = add_fast_strategy_summary("Current Open Strategies Performance", "OPEN", 20, m, u, d)
    
    sh = html_comb(m=m, u=u, d=d)
    return tn, pt, sh

#<=====>#

def ext_main():
    while True:
        try:
            app.run(host='0.0.0.0', debug=True, port=8080)
        except KeyboardInterrupt as e:
            print('{} ==> keyed exit...')
            sys.exit(f"sys.exit from {__name__}")
        except Exception as e:
            print(dttm_get())
            traceback.print_exc()
            print(type(e))
            print(e)
            print('sleeping 60 then restarting...')
            time.sleep(60)

#<=====>#
# Post Variables
#<=====>#



#<=====>#
# Default Run
#<=====>#



#<=====>#
