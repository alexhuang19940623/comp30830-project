import re
from flask import Flask, render_template, request, g, jsonify
from sqlalchemy import create_engine
from app import app
import pandas as pd
import requests
import datetime
from datetime import date
URL="database-1.cyhnb62nmtav.eu-west-1.rds.amazonaws.com"
PASSWORD=wwwww
PORT="3306"
USER ="kuroko"

def connect_to_database():
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}".format(USER,PASSWORD,URL,PORT),echo=True)
    # engine = create_engine("mysql+pymysql://root:no104349@localhost:3306",echo=True)
    engine.execute("use dbbikes;")
    return engine


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/map', methods=["GET","POST"])
def map():
    if request.method == "POST":
        result = request.form
        print(result)
        return render_template("map.html", result=result)

@app.route("/weather")
def query_weather():
    engine = get_db()
    res = []
    rows = engine.execute("SELECT * from weather order by dt desc limit 1;")
    for row in rows:
        res.append(dict(row))
    
    return jsonify(weather = res)

@app.route('/now_available')
def get_now():
    engine = get_db()
    stations = []
    rows = engine.execute("SELECT * from dbbikes.availability limit 110;")
    for row in rows:
        stations.append(dict(row))
    return jsonify(available = stations)

@app.route('/station')
def get_stations():
    engine = get_db()
    stations = []
    rows = engine.execute("SELECT * from station limit 110;")
    for row in rows:
        stations.append(dict(row))
    
    return jsonify(stations = stations)


@app.route("/available/<int:station_id>")
def get_station(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT * FROM dbbikes.availability  where number = {} order by last_update desc limit 24;".format(station_id))
    for row in rows:
        data.append(dict(row))
    
    return jsonify(available = data)



@app.route('/register/')
def register():
    return render_template("register.html")

# @app.route('/chartDataframe/<int:station_id>/<string:date>')
# def chartDataframe(station_id):
