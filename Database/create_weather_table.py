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
        visibility VARCHAR(256),
	);
"""
try:
    res = engine.execute(sql1)
    res = engine.execute("DROP TABLE IF EXISTS weather")
    res = engine.execute(sql2)
    print(res.fetchall())
except Exception as e:
    print(e)


