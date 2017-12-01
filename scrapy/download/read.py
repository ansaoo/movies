#! /usr/bin/env python3
import sqlite3
from tabulate import tabulate


def read():
    conn = sqlite3.connect("recentMovies.db")
    c=conn.cursor()
    # c.execute("select id,title,date,genre,rate,trailer from movies order by id desc limit 15")
    c.execute("select id,date,trailer from movies order by id asc")
    results = []
    for val in c.fetchall():
        results.append(list(val)) 
    print(tabulate(results, tablefmt="grid"))


if __name__ == "__main__":
    read()
