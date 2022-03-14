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
# from keys import *

URL="database-1.cyhnb62nmtav.eu-west-1.rds.amazonaws.com"
PASSWORD="11223344"
PORT="3306"
USER ="kuroko"

engine = create_engine("mysql+mysqldb://{}:{}@{}:{}".format(USER,PASSWORD,URL,PORT,DB),echo=True)

# engine = create_engine("mysql+pymysql://root:no104349@localhost:3306",echo=True)

sql = """
    CREATE DATABASE IF NOT EXISTS dbbikes;
"""
engine.execute(sql)

sql1 = """
use dbbikes;

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


# while True:
# try:
#     p = "data/weather/"
#     path_list = os.listdir(p)
#     for i in range(len(path_list)):
#         text = open(p + path_list[i] ,'r').read()
#         weather_to_db(text)
#     # time.sleep(60*60)
# except:
#     print(traceback.format_exc())