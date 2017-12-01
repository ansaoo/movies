#! /usr/bin/env python3


def group(data):
    return {'cfilm': cfilm,
            'cmedia': [media for media in data if cfilm in data]}


def merge(json_file):
    data = json.load(open(json_file))
    cfilms = []
    return [0]


def update(json_file):
    conn = sqlite3.connect("new_movies.db")
    c = conn.cursor()
    df = pd.read_json(json_file, orient='records')
    df.groupby('cfilm')['cmedia'].apply(lambda x: ';'.join(x))
    news = merge(json_file)
    for val in news:
        c.execute("UPDATE movies SET cmedia=:cmedia WHERE cfilm=:cfilm", val)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import sys
    import json
    import sqlite3
    import pandas as pd
    update(sys.argv[1])
