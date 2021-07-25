# -*- coding: utf-8 -*-

import sqlite3 as sql


# getting a price for the specified currency
def get_price(currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT price FROM currency WHERE currency=?", (currency.upper(),))
    three_results = cur.fetchall()
    cur.close()

    if not three_results:  # check for a non-empty list
        return -1

    price = three_results[0][0]  # getting a price

    return price


#  getting the time of the last update
def get_time():

    con = sql.connect('currencies.db')
    cur = con.cursor()
    try:
        cur.execute("SELECT time FROM currency WHERE currency=?", ('CAD',))
        three_results = cur.fetchall()
        cur.close()

        if not three_results:  # check for a non-empty list
            return -1

        time = three_results[0][0]   # getting the time

        return time

    except sql.OperationalError:
        return 0


def get_name_base_currency(id_user):
    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT base FROM users WHERE id_user=?", (id_user,))
    three_results = cur.fetchall()
    cur.close()

    if not three_results:  # check for a non-empty list
        return -1

    base_currency = three_results[0][0]  # getting a name base currency

    return base_currency


def get_name_quoted_currency(id_user):
    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT quoted FROM users WHERE id_user=?", (id_user,))
    three_results = cur.fetchall()
    cur.close()

    if not three_results:  # check for a non-empty list
        return -1

    quoted_currency = three_results[0][0]  # getting a name quoted currency

    return quoted_currency


def get_price_base_currency(id_user):
    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT price_base FROM users WHERE id_user=?", (id_user,))
    three_results = cur.fetchall()
    cur.close()

    if not three_results:  # check for a non-empty list
        return -1

    price_base_currency = three_results[0][0]  # getting a price base currency

    return price_base_currency


def get_price_quoted_currency(id_user):
    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT price_quoted FROM users WHERE id_user=?", (id_user,))
    three_results = cur.fetchall()
    cur.close()

    if not three_results:  # check for a non-empty list
        return -1

    price_quoted_currency = three_results[0][0]  # getting a price quoted currency

    return price_quoted_currency


def get_change_base_currency(id_user):
    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT change_base FROM users WHERE id_user=?", (id_user,))
    three_results = cur.fetchall()
    cur.close()

    if not three_results:  # check for a non-empty list
        return -1

    change_base_currency = three_results[0][0]  # getting status command change base currency

    return change_base_currency


def get_change_quoted_currency(id_user):
    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT change_quoted FROM users WHERE id_user=?", (id_user,))
    three_results = cur.fetchall()
    cur.close()

    if not three_results:  # check for a non-empty list
        return -1

    change_quoted_currency = three_results[0][0]  # getting status command change quoted currency

    return change_quoted_currency
