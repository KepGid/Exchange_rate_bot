# -*- coding: utf-8 -*-

from time import time
from datetime import datetime
import requests
import matplotlib.pyplot as plt


def create_chart(name_currency):

    url = "https://fxmarketapi.com/apitimeseries"

    start_date = str(datetime.fromtimestamp(time()-604800).strftime("%Y-%m-%d"))
    end_date = str(datetime.fromtimestamp(time()).strftime("%Y-%m-%d"))

    querystring = {"api_key": "gMEf0GH5_3_dEHnsCW2I", "currency": name_currency, "start_date": start_date,
                   "end_date": end_date, "format": "ohlc"}

    response = requests.get(url, params=querystring)
    try:
        dict_time_series = response.json().pop('price')

    except KeyError:
        return -1

    date = []
    price = []

    for i in dict_time_series:
        date.append(i)
        price.append(dict_time_series.get(i).get(name_currency).get('close'))

    plt.plot(date, price)
    plt.xlabel('Data', fontsize=15)
    plt.ylabel('Price', fontsize=15)
    plt.title(name_currency+' chart price ', fontsize=17)
    plt.savefig('chart.png')
    plt.close()

    return 0
