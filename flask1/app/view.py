from pydoc import describe
import re
from flask import Flask, render_template, request, g, jsonify,json
from sqlalchemy import create_engine
from app import app
import pandas as pd
import requests
import datetime
from datetime import date
import pickle
import os
# fn = os.path.join(app.config['DOCUMENTATION_PATH'],
#                           slug, 'index.html')
# with open('../t) as f:
#     f.read()
# with open('final_prediction_bike_stands.pickle','rb') as f:
#     random_forest_stands = pickle.load(f)
cur_dir = os.path.dirname(__file__)
random_forest = pickle.load(open(os.path.join(cur_dir,'final_prediction.pickle'),'rb'))


URL="database-1.cyhnb62nmtav.eu-west-1.rds.amazonaws.com"
PASSWORD=11223344
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
def map():
    return render_template("map.html")

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



@app.route("/prediction_model", methods=['GET','POST'])
def prediction_model():
    """Based on user's request for source/destination we invoke the required pickle file to predict available bikes/available bike stands"""

    import numpy as np
    
    # # Store the request from JS
    post = request.args.get('post',0,type=str)
    post=post.split(',')
    print(post)

    print("Data to be sent to prediction model ",post)
    print(type(post))

    number=int(post[0])
    day_of_week = int(post[1])
    hour=int(post[2])
    temperture= float(post[3])
    visibility = int(post[4])
    description = post[5]
    broken_clouds = clear_sky = few_clouds = fog = haze = 0
    light_intensity_drizzle_rain = light_intensity_shower_rain = 0
    light_rain = mist = moderate_rain = overcast_clouds = 0
    scattered_clouds = 0

    if(description=='scattered clouds'):
        scattered_clouds = 1
    if(description=='broken clouds'):
        broken_clouds = 1
    if(description=='few clouds'):
        few_clouds = 1
    if(description=='clear sky'):
        clear_sky = 1
    if(description=='overcast clouds'):
        overcast_clouds = 1
    if(description=='light rain'):
        light_rain = 1
    if(description=='moderate rain'):
        moderate_rain = 1
    if(description=='mist'):
        mist = 1
    if(description=='fog'):
        fog = 1
    if(description=='haze'):
        haze = 1
    if(description=='light intensity shower rain'):
        light_intensity_shower_rain = 1
    if(description=='light intensity drizzle rain'):
        light_intensity_drizzle_rain = 1
    
    # predict_request = [[number,day_of_week,hour,temperture,visibility,broken_clouds,clear_sky,few_clouds,
    # fog,haze,light_intensity_drizzle_rain,light_intensity_shower_rain,light_rain,mist,moderate_rain,
    # overcast_clouds,scattered_clouds]]

    predict_request = [[number, hour, temperture, 
visibility, day_of_week,day_of_week,broken_clouds, clear_sky,
       few_clouds, fog, haze,
       light_intensity_drizzle_rain,
       light_intensity_shower_rain, light_rain,
       mist, moderate_rain,
       overcast_clouds, scattered_clouds]]

    print(predict_request)

    predicted_available_bikes = random_forest.predict(predict_request)
    print("Predicted available bikes for the station is",int(predicted_available_bikes[0]))

    data_from_model= [int(predicted_available_bikes[0])]
    return json.dumps(data_from_model)