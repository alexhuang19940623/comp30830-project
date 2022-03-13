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
import cryptography
from keys import *

engine = create_engine("mysql+pymysql://root:no104349@localhost:3306",echo=True)
sql = """
    CREATE DATABASE IF NOT EXISTS dbikes;
"""
engine.execute(sql)

sql1 = """
use dbikes;

"""
sql2 = """
    CREATE TABLE IF NOT EXISTS weather(
        dt VARCHAR(256),
        description VARCHAR(256),
        icon VARCHAR(256),
        temperture VARCHAR(256),
        pressure VARCHAR(256),
        humidity VARCHAR(256),
        visibility VARCHAR(256)
	);
"""
try:
    res = engine.execute(sql1)
    res = engine.execute("DROP TABLE IF EXISTS weather")
    res = engine.execute(sql2)
    print(res.fetchall())
except Exception as e:
    print(e)


def weather_to_db(text):
    d_weather = json.loads(text)
    vals = (
        d_weather['dt'],d_weather['weather'][0]['description'],d_weather['weather'][0]['icon'],
        d_weather['main']['temp'], d_weather['main']['pressure'],d_weather['main']['humidity'],
        d_weather['visibility']
    )
    print(vals)
    engine.execute("insert into weather values(%s, %s, %s, %s, %s, %s, %s)",vals)
    return


KEY = "2150ca8b3c3f0f799010b1403ca77a5d"
WEATHER = "https://api.openweathermap.org/data/2.5/weather"
# while True:
try:
    p = "weather/"
    path_list = os.listdir(p)
    for i in range(len(path_list)):
        text = open(p + path_list[i] ,'r').read()
        weather_to_db(text)
    # time.sleep(60*60)
except:
    print(traceback.format_exc())