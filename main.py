# -*- coding: utf-8 -*-

import telebot
from requests import post
from time import time

import config
from command_list import command_list
from parsing_currencies import parsing_currencies
from command_chart import create_chart

from create_bd import create_and_update_currencies, create_and_update_users
from get_data_of_bd import *
from updata_data_in_bd import *


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.send_message(message.chat.id, 'Hello, i will help convert one currency to another currency.'
                                      '\nBase currency USD '
                                      '\nCommand list:'
                                      '\n/list - display a list of all currencies and their exchange rates;'
                                      '\n/basecurrency  - change base currency; '
                                      '\n/quotedcurrency - change the quoted currency;'
                                      '\n/chart - will show the price chart for the last 7 days;'
                                      '\n/help - detailed information about commands and how to use them;')
    create_and_update_currencies(parsing_currencies())
    user_id = message.from_user.id
    create_and_update_users(user_id, 'USD', 'USD', 1, 1, False, False)


@bot.message_handler(commands=['list'])
def send_list_currencies(message):

    update_bd()  # if more than 10 minutes have passed, then update the exchange rate in the local database

    # function check for cases if the command is entered after the command to change currencies
    check_command(message.from_user.id)

    bot.send_message(message.chat.id, '\n'.join(command_list()))


@bot.message_handler(commands=['basecurrency'])
def command_base_currency(message):

    user_id = message.from_user.id
    # check for cases of command entry after command /quotedcurrency
    if get_change_base_currency(user_id) or get_change_quoted_currency(user_id):
        update_change_quoted_currency(user_id, False)
        update_change_base_currency(user_id, True)
    else:
        update_change_base_currency(user_id, True)

    bot.send_message(message.chat.id, 'Enter the name of the base currency')


@bot.message_handler(commands=['quotedcurrency'])
def command_quoted_currency(message):

    user_id = message.from_user.id
    # check for cases of command entry after command /basecurrency
    if get_change_base_currency(user_id) or get_change_quoted_currency(user_id):
        update_change_base_currency(user_id, False)
        update_change_quoted_currency(user_id, True)
    else:
        update_change_quoted_currency(user_id, True)

    bot.send_message(message.chat.id, 'Enter the name of the quoted currency')


@bot.message_handler(commands=['chart'])
def send_chart(message):

    update_bd()  # if more than 10 minutes have passed, then update the exchange rate in the local database

    # function check for cases if the command is entered after the command to change currencies
    check_command(message.from_user.id)

    name_chart = get_name_base_currency(message.from_user.id) + get_name_quoted_currency(message.from_user.id)

    if create_chart(name_chart) != -1:
        url = "https://api.telegram.org/bot" + config.token + "/sendPhoto"
        files = {'photo': open('chart.png', 'rb')}
        data = {'chat_id': message.chat.id}
        r = post(url, files=files, data=data)
    else:
        bot.send_message(message.chat.id, 'No exchange rate data is available for the selected currency')


@bot.message_handler(commands=['help'])
def command_help(message):

    # function check for cases if the command is entered after the command to change currencies
    check_command(message.from_user.id)

    bot.send_message(message.chat.id, '\nCommand list:'
                                      '\n/list - display a list of all currencies and their exchange rates;'
                                      '\n/basecurrency   - to change the base currency; '
                                      '\n/quotedcurrency - to change the quoted currency; '
                                      '\n/chart - will show the price chart for the '
                                      'current currency pair for the last 7 days;')


@bot.message_handler(content_types=['text'])
def convert(message):
    # if more than 10 minutes have passed, then update the exchange rate in the local database
    update_bd()

    user_id = message.from_user.id

    price_base_currency = get_price_base_currency(user_id)
    price_quoted_currency = get_price_quoted_currency(user_id)

    update_bd()  # if more than 10 minutes have passed then update the local database

    if get_change_base_currency(user_id):
        name_base_currency = message.text.replace(' ', '').upper()

        if name_base_currency.upper() == 'USD':
            price_base_currency = 1
        else:
            price_base_currency = get_price(name_base_currency,)

        # checking if there is such a currency
        if price_base_currency != -1:
            update_name_base_currency(user_id, name_base_currency)

            bot.send_message(message.chat.id, 'Currency pair '
                                              ''+get_name_base_currency(user_id)+get_name_quoted_currency(user_id)
                                              + '\nEnter the amount:')
            update_change_base_currency(user_id, False)
            update_price_base_currency(user_id, price_base_currency)
        else:
            bot.send_message(message.chat.id, 'There is no such currency')

    elif get_change_quoted_currency(user_id):
        name_quoted_currency = message.text.replace(' ', '').upper()

        if name_quoted_currency == 'USD':
            price_quoted_currency = 1
        else:
            price_quoted_currency = get_price(name_quoted_currency)

        # checking if there is such a currency
        if price_quoted_currency != -1:
            update_name_quoted_currency(user_id, name_quoted_currency)

            bot.send_message(message.chat.id, 'Currency pair '
                                              ''+get_name_base_currency(user_id)+get_name_quoted_currency(user_id)
                                              + '\nEnter the amount:')
            update_change_quoted_currency(user_id, False)
            update_price_quoted_currency(user_id, price_quoted_currency)
        else:
            bot.send_message(message.chat.id, 'There is no such currency')

    else:
        if is_number(message.text):

            number = float(message.text)

            # obtaining the ratio of the first currency to the quoted
            coefficient = price_quoted_currency / price_base_currency
            # convert currencies
            amount = number * coefficient

            if amount > 1:
                text_message = get_name_base_currency(user_id)+' : '+str('%.2f' % number) + \
                               '\n'+get_name_quoted_currency(user_id) + ' : ' + str('%.2f' % float(amount))
            else:
                text_message = get_name_base_currency(user_id)+' : '+str('%.2f' % number) + \
                               '\n'+get_name_quoted_currency(user_id) + ' : ' + str('%.6f' % float(amount))
            bot.send_message(message.chat.id, text_message)

        else:
            text = 'incorrect number entered'
            bot.send_message(message.chat.id, text)


# check for cases if the command is entered after the command to change currencies
def check_command(user_id):
    if get_change_base_currency(user_id) or get_change_quoted_currency(user_id):
        update_change_quoted_currency(user_id, False)
        update_change_base_currency(user_id, False)


def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


# function to check the last update of the exchange rate,
# if more than 10 minutes have passed, then update the exchange rate in the local database
def update_bd():
    timestamp = get_time()
    if (time() - timestamp) >= 600:
        create_and_update_currencies(parsing_currencies())


if __name__ == '__main__':
     bot.infinity_polling()
