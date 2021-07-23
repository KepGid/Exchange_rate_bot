# -*- coding: utf-8 -*-

import requests


def parsing_currencies():
    url = "https://fxmarketapi.com/apicurrencies"
    querystring = {"api_key": "gMEf0GH5_3_dEHnsCW2I"}
    response = requests.get(url, params=querystring)

    dict_currencies = response.json()

    currencies = ''

    name_currencies = dict_currencies.pop('currencies')

    for i in name_currencies.keys():
        currencies = currencies + i + ','

    url = "https://fxmarketapi.com/apilive"
    querystring = {"api_key": "gMEf0GH5_3_dEHnsCW2I", "currency": currencies[:-1]}
    response = requests.get(url, params=querystring)

    dict_rate = response.json()
    timestamp = (dict_rate.get('timestamp'))

    rate = dict_rate.pop('price')
    result = []

    for i in rate.keys():
        if i == 'BTCUSD':
            price = '%.6f' % (1 / rate.get(i))
        else:
            if rate.get(i) > 0.01:
                price = '%.2f' % (rate.get(i))
            else:
                price = rate.get(i)
        currency = i.replace('USD', '')
        list_currency = [currency, price, timestamp]
        result.append(list_currency)

    return result

