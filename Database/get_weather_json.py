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
KEY = weather_key
WEATHER = "https://api.openweathermap.org/data/2.5/weather"


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


def write_to_file(text):
    f = open("data/weather/weather__{}".format(now).replace(" ", "_"), "w")
    f.write(text)
    f.close()


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


while True:
    try:
        now = datetime.datetime.now()
        lat = 53.343897
        lon = -6.29706
        r = requests.get(WEATHER, params={"lat": lat, "lon": lon,"appid": KEY})
        write_to_file(r.text)
        weather_to_db(r.text)
        time.sleep(60*60)
    except:
        print(traceback.format_exc())