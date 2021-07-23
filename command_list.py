# -*- coding: utf-8 -*-

import sqlite3 as sql


def command_list():

    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM currency;")
    three_results = cur.fetchall()
    cur.close()
    list_result = []

    for i in three_results:
        list_result.append(i[0]+' : '+str(i[1]))

    return list_result
