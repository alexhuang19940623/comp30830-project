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
KEY = weather_key
WEATHER = "https://api.openweathermap.org/data/2.5/weather"

engine = create_engine("mysql+pymysql://root:no104349@localhost:3306",echo=True)
sql = """
    CREATE DATABASE IF NOT EXISTS dbikes;
"""
engine.execute(sql)

sql1 = """
use dbikes;

"""
try:
    res = engine.execute(sql1)
    print(res.fetchall())
except Exception as e:
    print(e)

def write_to_file(text):
    f = open("data/weather/weather__{}".format(now).replace(" ", "_"), "w")
    f.write(text)
    f.close()


def weather_to_db(text):
    d_weather = json.loads(text)
    # print('**************')
    # print(d_weather)
    vals = (
        d_weather['dt'],d_weather['weather'][0]['description'],d_weather['weather'][0]['icon'],
        d_weather['main']['temp'], d_weather['main']['pressure'],d_weather['main']['humidity'],
        d_weather['visibility']
    )
    print(vals)
    engine.execute("insert into weather values(%s, %s, %s, %s, %s, %s, %s)",vals)
    return


# while True:
try:
    now = datetime.datetime.now()
    lat = 53.343897
    lon = -6.29706
    r = requests.get(WEATHER, params={"lat": lat, "lon": lon,"appid": KEY})
    write_to_file(r.text)
    weather_to_db(r.text)
    # time.sleep(60*60)
except:
    print(traceback.format_exc())