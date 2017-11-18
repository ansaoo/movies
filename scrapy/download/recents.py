#! /usr/bin/env python
# coding: utf-8

import sys
import os
import json
import sqlite3


def analyser(data):
    title = data['titre']
    date = data['genre'][0]
    genres = []
    for i in range(3, 6):
        try:
            genres.append(data['genre'][i])
        except IndexError:
            genres.append('none')
    genre = parseGenre(genres)
    synopsis = data['synopsis'].strip()
    trailer = "http://www.allocine.fr" + str(data['trailer'])
    rate = "0"
    return (title, date, genre, synopsis, trailer, rate)


def parseGenre(liste):
    temp = ''
    for val in liste:
        if val != 'none':
            temp += val
            temp += ','
    return temp[:-1]


def run():
    os.system("scrapy crawl recents -o results.json")
    data_json = open("results.json")
    data = json.load(data_json)
    conn = sqlite3.connect("recentMovies.db")
    c = conn.cursor()
    purchases = []
    for val in data:
        purchases.append(analyser(val))
    c.executemany("INSERT INTO movies (title,date,genre,synopsis,trailer,rate) VALUES (?,?,?,?,?,?)", purchases)
    conn.commit()
    conn.close()
    os.system("rm results.json")


if __name__ == "__main__":
    run()
