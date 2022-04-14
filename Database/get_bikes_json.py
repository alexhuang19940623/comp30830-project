#!/usr/bin/env python3
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
import simplejson as json
from IPython.display import display
import pandas as pd
import requests
import traceback
import datetime
import time
from keys import *
KEY = bike_key
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
# url
URL="database-1.cyhnb62nmtav.eu-west-1.rds.amazonaws.com"
PASSWORD=db_pw
PORT="3306"
USER ="kuroko"

engine = create_engine("mysql+pymysql://{}:{}@{}:{}".format(USER,PASSWORD,URL,PORT),echo=True)

# engine = create_engine("mysql+pymysql://root:no104349@localhost:3306",echo=True)

sql = """
    CREATE DATABASE IF NOT EXISTS dbbikes;
"""
engine.execute(sql)

sql1 = """
use dbbikes;

"""
engine.execute(sql1)


def stations_to_db(text):
    stations = json.loads(text)
    print(type(stations), len(stations))
    for station in stations:
        # print(station)
        vals = (
            station.get('address'), int(station.get('banking')), station.get('bike_stands'), int(station.get('bonus')), 
            station.get('contract_name'), station.get('name'), station.get('number'), 
            station.get('position').get('lat'), station.get('position').get('lng'), station.get('status')
        )
        engine.execute("insert into station values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",vals)
    return


def avail_bikes_to_db(text):
    avail_bikes = json.loads(text)
    print(type(avail_bikes), len(avail_bikes))
    for station in avail_bikes:
        print(station)
        vals = (
            station.get('number'), station.get('available_bikes'), 
            station.get('available_bike_stands'),station.get('last_update'),
        )
        engine.execute("insert into availability values(%s, %s, %s, %s)",vals)
    return

def write_to_file(text):
    f = open("data/bikes/bikes__{}".format(now).replace(" ", "_"), "w")
    f.write(r.text)
    f.close()

while True:
    try:
        now = datetime.datetime.now()
        r = requests.get(STATIONS, params={"apiKey": KEY, "contract": NAME})
        # print(r, now)
        write_to_file(r.text)
        avail_bikes_to_db(r.text)
        stations_to_db(r.text)
        time.sleep(8*60)
    except:
        print(traceback.format_exc())