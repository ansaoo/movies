#! /usr/bin/env python3
import sqlite3
import json
from tabulate import tabulate


def loadJSON():
    return open("../../results/predicts.json").readlines()


def update():
    conn = sqlite3.connect("recentMovies.db")
    c=conn.cursor()
    predicts = loadJSON()
    for val in predicts:
        temp = json.loads(val.strip())
        temp['prediction'] = temp['prediction']/5
        c.execute("UPDATE movies SET rate=:prediction WHERE id=:index", temp)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    update()
