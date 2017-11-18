#!/bin/sh

source venv/bin/activate

cd scrapy/download
cp recentMovies.db recentMovies-backup.db
python3 recents.py
# python3 read.py
sqlite3 recentMovies.db < dump.script
cd ../../

sbt run
mv results/*.json results/predicts.json
cd scrapy/download
python3 update.py
python3 read.py
cd ../../
rm -rf results
