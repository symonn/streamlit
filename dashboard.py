# list of imports
import numpy as np
import pandas as pd
import ccxt
import streamlit as st

from datetime import datetime,timezone
from datetime import date
from datetime import timedelta
import time as time_true

import utils as utils
import config as conf


def main():

	st.set_page_config(layout="wide")

	# ROW 1 ------------------------------------------------------------------------
	col1, col2 = st.beta_columns([1,2])
	col1.image('https://cdn.futura-sciences.com/buildsv6/images/wide1920/4/1/d/41d6867f78_50171855_bitcoin.jpg',width=300)
	col2.title("Welcome to the Crypto Trader Dashboard")


	# ROW 2 ------------------------------------------------------------------------
	exchange = utils.initialize_exchange(conf.market,conf.api_key,conf.secret_key)
	balance = utils.get_balance(exchange,conf.currency)
	wallet = round(balance['total'],0)
	st.markdown(f"<h3> Your account balance is equal to <span style='font-weight:bolder;font-size:30px;'>{wallet:.0f}$</span> </h3>",unsafe_allow_html=True)

	## ROW 3 ------------------------------------------------------------------------
	start_date = st.date_input("View trades since:")

	# ROW 4 ------------------------------------------------------------------------
	row4_1, row4_spacer1, row4_2 = st.beta_columns((2, .2, 1))
	start_date = datetime.combine(start_date, datetime.min.time())
	trades = utils.get_trades(exchange,since=start_date)
	stats = utils.get_statistics_on_trades(trades)

	with row4_1:
		row4_1.subheader('Statistics per day:')
		row4_1.write(stats)

	with row4_2:
		start = float(stats.head(1)['Amount'])
		end = float(stats.tail(1)['Amount']) + float(stats.tail(1)['Earnings'])
		evolution = end-start
		pourcentage = (end-start)/start*100
		row4_2.markdown("<h3> \n </h3>",unsafe_allow_html=True)
		row4_2.markdown("<h3> \n </h3>",unsafe_allow_html=True)
		row4_2.markdown(f"<h3 style='text-align:center;'> Evolution during the selected period \n <span style='font-weight:bolder;font-size:30px;'>{evolution:.0f}$ ({pourcentage:.1f}%)</span> </h3>",unsafe_allow_html=True)

	# ROW 5 ------------------------------------------------------------------------
	st.subheader('Evolution of the amount (usd):')
	utils.plot_balance(stats)


	update = st.button('Update')
	if update:
		pass


if __name__ == "__main__":
	# execute only if run as a script
    main()

