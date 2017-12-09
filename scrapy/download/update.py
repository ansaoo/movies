#! /usr/bin/env python3


def update(liste):
    conn = sqlite3.connect("new_movies.db")
    c = conn.cursor()
    for val in liste:
        c.execute("UPDATE movies SET cmedia=:cmedia WHERE cfilm=:cfilm", val)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import sys
    import sqlite3
    import pandas as pd
    df = pd.read_json(sys.argv[1], orient='records')
    temp = df.groupby('cfilm')['cmedia'].apply(lambda x: ';'.join([str(el) for el in x]))
    new = pd.DataFrame()
    new['cfilm'] = temp.index
    new['cmedia'] = temp.values
    new = new.to_dict(orient='records')
    update(new)
