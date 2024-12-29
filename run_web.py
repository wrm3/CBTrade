#<=====>#
# Description
#<=====>#



#<=====>#
# Known To Do List
#<=====>#



#<=====>#
# Imports
#<=====>#
#<=====>#
# Imports
#<=====>#
from datetime import datetime
from flask import Flask, render_template
import sys
import time
import traceback
import warnings

from libs.bot_web import (
    ext_all_reports_test, ext_balances, ext_buy_strats, ext_buys_recent,
    ext_closed_positions, ext_db_size, ext_home, ext_market, ext_markets,
    ext_mkt_buy_strats, ext_open_positions, ext_sales_all, ext_sales_all_test,
    ext_sales_day_cntd, ext_sales_day_cntd_test, ext_sales_dt, ext_sales_dt_test,
    ext_sales_month, ext_sales_month_test, ext_sales_today, ext_sales_today_test,
    ext_sales_yesterday_test, ext_sales_yr, ext_sales_yr_test, ext_sells_recent
)
from libs.lib_common import dttm_get


#<=====>#
# Variables
#<=====>#
lib_name      = 'web'
log_name      = 'web'
lib_verbosity = 1
lib_debug_lvl = 1
lib_secs_max  = 2

#<=====>#
# Assignments Pre
#<=====>#

#<=====>#
# Classes
#<=====>#

#<=====>#
# Functions
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

now = datetime.now()

#<=====>#

@app.route("/")
@app.route("/home.htm")
def home() -> str:
	tn, pt, sh = ext_home()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/all_reports_test.htm")
def all_reports_test() -> str:
	tn, pt, sh = ext_all_reports_test()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/balances.htm")
def balances() -> str:
	tn, pt, sh = ext_balances()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/open.htm")
@app.route("/open_positions.htm")
def open_positions() -> str:
	tn, pt, sh = ext_open_positions()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/closed.htm")
@app.route("/closed_positions.htm")
def closed_positions() -> str:
	tn, pt, sh = ext_closed_positions()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/buys.htm")
@app.route("/buys_recent.htm")
def buys_recent() -> str:
	tn, pt, sh = ext_buys_recent()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sells.htm")
@app.route("/sells_recent.htm")
def sells_recent() -> str:
	tn, pt, sh = ext_sells_recent()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/buy_strats.htm")
def buy_strats() -> str:
	tn, pt, sh = ext_buy_strats()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/mkt_buy_strats.htm")
def mkt_buy_strats() -> str:
	tn, pt, sh = ext_mkt_buy_strats()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/markets.htm")
def markets() -> str:
	tn, pt, sh = ext_markets()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/market_<mkt>")
def market(mkt) -> str:
	tn, pt, sh = ext_market(mkt)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_all.htm")
def sales_all() -> str:
	tn, pt, sh = ext_sales_all()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales.htm")
@app.route("/sales_today.htm")
def sales_today() -> str:
	tn, pt, sh = ext_sales_today()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_yesterday.htm")
def sales_yesterday() -> str:
	tn, pt, sh = ext_sales_today()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_<day_cnt>d.htm")
def sales_day_cntd(day_cnt) -> str:
	tn, pt, sh = ext_sales_day_cntd(day_cnt)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_dt_<dt>")
def sales_dt(dt) -> str:
	tn, pt, sh = ext_sales_dt(dt)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_month_<yr>_<m>")
def sales_month(yr,m) -> str:
	tn, pt, sh = ext_sales_month(yr,m)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_year_<yr>")
def sales_yr(yr) -> str:
	tn, pt, sh = ext_sales_yr(yr)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_all_test.htm")
def sales_all_test() -> str:
	tn, pt, sh = ext_sales_all_test()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_test.htm")
@app.route("/sales_today_test.htm")
def sales_today_test() -> str:
	tn, pt, sh = ext_sales_today_test()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_yesterday_test.htm")
def sales_yesterday_test() -> str:
	tn, pt, sh = ext_sales_yesterday_test()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_<day_cnt>d_test.htm")
def sales_day_cntd_test(day_cnt) -> str:
	tn, pt, sh = ext_sales_day_cntd_test(day_cnt)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_dt_test_<dt>")
def sales_dt_test(dt) -> str:
	tn, pt, sh = ext_sales_dt_test(dt)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_month_test_<yr>_<m>")
def sales_month_test(yr,m) -> str:
	tn, pt, sh = ext_sales_month_test(yr,m)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/sales_year_test_<yr>")
def sales_yr_test(yr) -> str:
	tn, pt, sh = ext_sales_yr_test(yr)
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

@app.route("/db_size.htm")
def db_size() -> str:
	tn, pt, sh = ext_db_size()
	return render_template('web_home.html'
							, top_nav= tn
							, page_title = pt
							, html_disp  = sh
							)

#<=====>#

def main():
	while True:
		try:
			app.run(host='0.0.0.0', debug=True, port=8080)
		except KeyboardInterrupt as e:
			print('{} ==> keyed exit...')
			sys.exit()
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

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=8080)

#<=====>#