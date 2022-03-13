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
KEY = "50b3e4b1972f05f68760a2caaece786ed0bda969"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"

engine = create_engine("mysql+pymysql://root:no104349@localhost:3306",echo=True)
sql = """
    CREATE DATABASE IF NOT EXISTS dbikes;
"""
engine.execute(sql)


def write_to_file(text):
    f = open("data/weather/bikes__{}".format(now).replace(" ", "_"), "w")
    f.write(r.text)
    f.close()


def weather_to_db(text):
    d_weather = json.loads(text)
    vals = (
        d_weather['dt'],d_weather['weather'][0]['description'],d_weather['weather'][0]['icon'],
        d_weather['main']['temp'], d_weather['main']['pressure'],d_weather['main']['humidity'],
        d_weather['visibility']
    )
    print(vals)
    engine.execute("insert into station values(%s, %s, %s, %s, %s, %s, %s)",vals)
    
    return


KEY = "2150ca8b3c3f0f799010b1403ca77a5d"
WEATHER = "https://api.openweathermap.org/data/2.5/weather"
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