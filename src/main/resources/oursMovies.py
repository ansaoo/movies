#! /usr/bin/env python3
# coding:utf-8

import os
import sys
import sqlite3
from tabulate import tabulate

columnsMovie = {'idMovie': 'movieId', 
                'idFile': 'fileId', 
                'c00': 'title',
                'c01': 'synopsis',
                'c02': '',
                'c03': 'tag',
                'c04': '',
                'c05': '',
                'c06': 'screenplay',
                'c07': '',
                'c08': 'thumb',
                'c09': '',
                'c10': '',
                'c11': '',
                'c12': 'rated',
                'c13': '',
                'c14': 'genre',
                'c15': 'director',
                'c16': 'originalTitle',
                'c17': '',
                'c18': 'stutio',
                'c19': '',
                'c20': 'fanart',
                'c21': 'country',
                'c22': 'filePath',
                'c23': '',
                'idSet': 'setId',
                'userrating': 'ourRate',
                'premiered': 'date',
                }


def connexion():
    return sqlite3.connect('MyVideos107.db')


if __name__ == "__main__":
    conn = connexion()
    c = conn.cursor()
    #    c.execute(".nullvalue NONE;")
    c.execute(sys.argv[1])
    results = []
    for val in c.fetchall():
        results.append(list(val))
    conn.close()
    print(results)
