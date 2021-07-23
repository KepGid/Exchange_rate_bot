# -*- coding: utf-8 -*-

import telebot
from requests import post
from time import time


import config
from command_list import command_list
from create_bd import create_and_update
from parsing_currencies import parsing_currencies
from get_price_and_time import get_price, get_time
from command_chart import create_chart


bot = telebot.TeleBot(config.token)

price_first_currency = 1
price_second_currency = 1


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello, i will help convert one currency to another currency.'
                                      '\nBase currency USD '
                                      '\nCommand list:'
                                      '\n/list - display a list of all currencies and their exchange rates;'
                                      '\n/basecurrency currency name - change base currency; '
                                      '\n/quotedcurrency currency name - change the currency into which the amount is converted;'
                                      '\n/chart currency pair name - will show the price chart for the last 7 days;'
                                      '\n/help - detailed information about commands and how to use them;')
    create_and_update(parsing_currencies())


@bot.message_handler(commands=['list'])
def send_list_currencies(message):
    update_bd()
    bot.send_message(message.chat.id, '\n'.join(command_list()))


@bot.message_handler(commands=['basecurrency'])
def send_welcome(message):
    global price_first_currency
    update_bd()

    name_currency = message.text.replace('/basecurrency', '').replace(' ', '')

    if name_currency == 'USD':
        price_first_currency = 1
    else:
        price_first_currency = get_price(name_currency)

    if price_first_currency != -1:
        bot.send_message(message.chat.id, 'if the second currency is indicated, then enter the amount, '
                                          'otherwise specify the second currency via the /quotedcurrency command')
    else:
        bot.send_message(message.chat.id, 'no currency')


@bot.message_handler(commands=['quotedcurrency'])
def send_welcome(message):
    global price_second_currency
    update_bd()

    name_currency = message.text.replace('/quotedcurrency', '').replace(' ', '')

    if name_currency == 'USD':
        price_second_currency = 1
    else:
        price_second_currency = get_price(name_currency)

    if price_second_currency != -1:
        bot.send_message(message.chat.id, 'enter the amount: ')
    else:
        bot.send_message(message.chat.id, 'no currency')


@bot.message_handler(commands=['chart'])
def send_chart(message):

    name_chart = message.text.replace('/chart', '').replace(' ', '')

    if create_chart(name_chart.upper()) != -1:
        url = "https://api.telegram.org/bot" + config.token + "/sendPhoto";
        files = {'photo': open('chart.png', 'rb')}
        data = {'chat_id': message.chat.id}
        r = post(url, files=files, data=data)
    else:
        bot.send_message(message.chat.id, 'No exchange rate data is available for the selected currency')


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, '\nCommand list:'
                                      '\n/basecurrency currency name - change base currency; '
                                      '\n  Example: /basecurrency EUR  or /basecurrency eur'
                                      '\n/quotedcurrency currency name - change the currency into which '
                                      'the amount is converted;'
                                      '\n  Example: /quotedcurrency USD or /quotedcurrency usd'
                                      '\n/chart currency pair name - will show the price chart for the last 7 days;'
                                      '\n  Example: /chart USDPLN or /chart usdpln')


@bot.message_handler(content_types=['text'])
def find_file_ids(message):
    global price_first_currency
    global price_second_currency

    update_bd()

    if is_number(message.text):
        number = float(message.text)
        coefficient = price_second_currency / price_first_currency

        if number*coefficient > 1:
            amount = '%.2f' % float(number * coefficient)
        else:
            amount = '%.6f' % float(number * coefficient)
        bot.send_message(message.chat.id, amount)
    else:
        text = 'incorrect number entered'
        bot.send_message(message.chat.id, text)


def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


def update_bd():
    timestamp = get_time()
    if (time() - timestamp) >= 600:
        create_and_update(parsing_currencies())


if __name__ == '__main__':
     bot.infinity_polling()
