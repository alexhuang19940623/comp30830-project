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
sql2 = """
    CREATE TABLE IF NOT EXISTS station(
        address VARCHAR(256),
        banking INTEGER,
        bike_stands INTEGER,
        bonus INTEGER,
        contract_name VARCHAR(256),
        name VARCHAR(256),
        number INTEGER,
        position_lat REAL,
        position_lng REAL,
        status VARCHAR(256)
	);
"""
sql3 = """
    CREATE TABLE IF NOT EXISTS availability(
        number VARCHAR(256),
        available_bikes VARCHAR(256),
        available_bike_stands VARCHAR(256),
        last_update VARCHAR(256)
	);
"""
try:
    res = engine.execute(sql1)
    res = engine.execute("DROP TABLE IF EXISTS stations")
    res = engine.execute("DROP TABLE IF EXISTS availability")
    res = engine.execute(sql2)
    res = engine.execute(sql3)
    print(res.fetchall())
except Exception as e:
    print(e)



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

p = "data/bikes/"
if(os.path.exists(p)):
    path_list = os.listdir(p)
    for i in range(len(path_list)):
        text = open(p + path_list[i] ,'r').read()
        stations_to_db(text)
        avail_bikes_to_db(text)