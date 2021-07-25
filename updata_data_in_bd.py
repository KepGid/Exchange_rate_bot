# -*- coding: utf-8 -*-

import sqlite3 as sql


def update_name_base_currency(user_id,  name_base_currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET base == ? WHERE id_user == ?', (name_base_currency, user_id))
    con.commit()
    cur.close()


def update_name_quoted_currency(user_id,  name_quoted_currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET quoted == ? WHERE id_user == ?', (name_quoted_currency, user_id))
    con.commit()
    cur.close()


def update_price_base_currency(user_id,  price_base):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET price_base == ? WHERE id_user == ?', (price_base, user_id))
    con.commit()
    cur.close()


def update_price_quoted_currency(user_id,  price_quoted):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET price_quoted == ? WHERE id_user == ?', (price_quoted, user_id))
    con.commit()
    cur.close()


def update_change_base_currency(user_id,  change_base_currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    print('123')
    cur.execute('UPDATE users SET change_base == ? WHERE id_user == ?', (change_base_currency, user_id))
    con.commit()
    cur.close()


def update_change_quoted_currency(user_id,  change_quoted_currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET change_quoted == ? WHERE id_user == ?', (change_quoted_currency, user_id))
    con.commit()
    cur.close()
