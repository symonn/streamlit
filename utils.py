# list of imports
import numpy as np
import pandas as pd
import ccxt
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datetime import datetime
from datetime import date
from datetime import timedelta
import time as time_true



def initialize_exchange(market,api_key,secret_key):
    """
    Initialize the exchange class.
    market (string): name of the broker
    return exchange object
    """
    exchange_class = getattr(ccxt,market)
    exchange = exchange_class({
        'apiKey':api_key,
        'secret':secret_key,
        'timeout':10000,
        'enableRateLimit':True
    })
    return exchange


def get_balance(exchange,currency):
    """
    Get the balance for a specific symbol
    symbol (string): name of the symbol
    Return a dictionary 
    """
    res = exchange.fetchBalance()
    return(res[currency])


def open_data(since,name):
    """
    Open data
    """
    data = pd.read_csv(name+".csv",header=0,sep=',')
    data['datetime'] = pd.to_datetime(data['day']).dt.tz_localize(None)
    data = data[data['datetime']>=since]
    data.sort_values(by=['trade_number'], inplace=True)
    return data


def get_trades(exchange,since):

	# format the date in milliseconds
	since = datetime.combine(since, datetime.min.time())
	since = int(datetime.timestamp(since)*1000)

	# get the recent trades
	trades = exchange.fetchMyTrades(symbol='BTC/USDT',since=since)
	trades = pd.DataFrame(trades)
	trades['datetime'] = pd.to_datetime(trades['datetime']).dt.tz_localize(None)
	trades['day'] = trades['datetime'].apply(lambda x: x.strftime("%m/%d/%Y"))
	trades = trades[trades['side']=='sell']
	trades = trades[['datetime','day','symbol','side','cost']]
	trades.sort_values(by=['datetime', 'symbol'], inplace=True)
	trades = trades.reset_index(drop=True)
	
	return trades


def get_statistics_on_trades(data):

    #data = data.reset_index()

    data['# of trades'] = 1

    data_grouped = data.groupby(['day'])['# of trades'].sum()


    grouped_day = data.groupby(by=['day'],as_index=False,sort=False)
    data['Amount'] = grouped_day['cost'].head(1)
    data['last'] = grouped_day['cost'].tail(1)
    first = data[['day','Amount']].dropna()
    first = first.reset_index(drop=True)
    last = data[['day','last']].dropna()

    data_grouped = data_grouped.reset_index()
    data_grouped = pd.merge(data_grouped,first,on='day')
    data_grouped = pd.merge(data_grouped,last,on='day')
    data_grouped['Earnings'] = data_grouped['last']-data_grouped['Amount']
    data_grouped['Earnings (%)'] = (data_grouped['last']-data_grouped['Amount'])/data_grouped['Amount']*100
    data_grouped = data_grouped[['day','Amount','# of trades','Earnings','Earnings (%)']]
    data_grouped.sort_values(by=['day'], inplace=True)
    data_grouped = data_grouped.reset_index(drop=True)
    data_grouped.sort_index(inplace=True)

    return data_grouped
    

def plot_balance(data):

    fig = go.Figure(data=go.Scatter(y=data['Amount'], x=data['day'],
                                    line = dict(color = "#A89EA3",width=1,dash="dot"),
                                    showlegend=False))

    fig.update_layout(template = "xgridoff") 
    fig.update_layout(height=500,width=1200)
    fig.update_yaxes(title_text = "Amount (USD)") 
    fig.update_xaxes(title_text = "Days") 

    st.plotly_chart(fig)

