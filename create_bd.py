# -*- coding: utf-8 -*-

import sqlite3 as sql


def create_and_update_currencies(list_currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS currency (currency TEXT PRIMARY KEY, price REAL, time INTEGER);""")

    for i in list_currency:
        try:
            cur.execute(f"INSERT INTO currency VALUES (?,?,?)", i)
        except sql.IntegrityError:
            cur.execute('UPDATE currency SET price == ?, time == ? WHERE currency == ?', (i[1], i[2], i[0]))

    con.commit()
    cur.close()


def create_and_update_users(user_id, base_currency, quoted_currency, base_price, price_quoted,
                            change_base_currency, change_quoted_currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (id_user INTEGER PRIMARY KEY, base TEXT, 
    quoted TEXT, price_base REAL, price_quoted REAL, change_base INTEGER, change_quoted INTEGER);""")
    try:
        cur.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?,?)",
                    (user_id, base_currency, quoted_currency, base_price,
                     price_quoted, change_base_currency, change_quoted_currency))
    except sql.IntegrityError:
        cur.execute('UPDATE users SET  base == ? , quoted == ? , price_base == ?, price_quoted  == ?, '
                    'change_base  == ?, change_quoted  == ?  WHERE id_user == ?', (base_currency, quoted_currency,
                                                                                   base_price, price_quoted,
                                                                                   change_base_currency,
                                                                                   change_quoted_currency, user_id))

    con.commit()
    cur.close()
