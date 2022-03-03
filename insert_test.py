import datetime
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
from IPython.display import display
URL="database-2.ceamwd5mbowc.eu-west-1.rds.amazonaws.com"
PASSWORD="11223344"
PORT="3306"
DB="dbikes"
USER ="TianyuHuang"
engine =create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER,PASSWORD,URL,PORT,DB),echo=True)

def main():
    while True:
        try:
            now=datetime.datetime.now()
            r=requests.get(STATIONS,params={"apiKey":APIKEY,"contract":NAME})
            print(r,now)
            write_to_file(r.text)
            write_to_db(r.text)
            time.sleep(8*60)
        except:
            print(traceback.format_exc())
            if engine is None:return

def stations_to_db(text): 
    stations=json.loads(text)
    print(type(stations),len(stations))
    for station in stations: 
        print(station)
        vals=(station.get('address'),int(station.get('banking')),
station.get('bike stands'),int(station.get('bonus')),
                        station.get('contract name'), station.get('name'),
station.get('number'),
                        station.get('position').get('lat'),
station.get('position').get('lng'),station.get('status')
)
        engine.execute("insert into station values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",vals)
        break
    return
stations_to_db(r.text)