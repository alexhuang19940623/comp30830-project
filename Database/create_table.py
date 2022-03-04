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
KEY = "50b3e4b1972f05f68760a2caaece786ed0bda969"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
URL="database-2.ceamwd5mbowc.eu-west-1.rds.amazonaws.com"
PASSWORD="11223344"
PORT="3306"
DB="dbikes"
USER ="TianyuHuang"
engine =create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER,PASSWORD,URL,PORT,DB),echo=True)
sql = """
    CREATE DATABASE IF NOT EXISTS dbikes;
"""
engine.execute(sql)

for res in engine.execute("SHOW VARIABLES"):
    print(res)

sql1 = """
use dbikes;

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
try:
    
    res = engine.execute(sql1)
    res = engine.execute("DROP TABLE IF EXISTS station")
    res = engine.execute(sql2)
    print(res.fetchall())
except Exception as e:
    print(e)