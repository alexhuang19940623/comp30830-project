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
KEY = "50b3e4b1972f05f68760a2caaece786ed0bda969"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"

def write_to_file(text):
    f = open("data/weather/weather__{}".format(now).replace(" ", "_"), "w")
    f.write(r.text)
    f.close()


while True:
    try:
        now = datetime.datetime.now()
        r = requests.get(STATIONS, params={"apiKey": KEY, "contract": NAME})
        # print(r, now)
        write_to_file(r.text)
        # avail_bikes_to_db(r.text)
        # stations_to_db(r.text)
        time.sleep(60*60)
    except:
        print(traceback.format_exc())