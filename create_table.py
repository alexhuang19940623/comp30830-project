import sqlalchemy as sqla
from sqlalchemy import create_engine
URL="database-2.ceamwd5mbowc.eu-west-1.rds.amazonaws.com"
PASSWORD="11223344"
PORT="3306"
DB="dbikes"
USER="TianyuHuang"
engine =create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URL,PORT,DB),echo=True)
sql="""
CREATE DATABASE IF NOT EXISTS dbikes;
"""
engine.execute(sql)
sq1="""
CREATE TABLE IF NOT EXISTS Station(
address VARCHAR(256)
banking INTEGER,
bike_stands INTEGER,
bonus INTEGER,
contract_name VARCHAR(256),
name VARCHAR(256),
number INTEGER,
position_lat REAL,
position_lng REAL,
status VARCHAR(256)
"""
try:
    res=engine.execute("DROP TABLE IF EXISTS station")
    res=engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)