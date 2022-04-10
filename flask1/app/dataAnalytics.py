import numpy as np
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
pd.options.mode.chained_assignment=None
import os
import pymysql
import pandas as pd
import sys
import datetime

import pickle

# Declare and initialize database connection credentials
URL="database-1.cyhnb62nmtav.eu-west-1.rds.amazonaws.com"
PASSWORD=11223344
PORT="3306"
USER ="kuroko"
DB = 'dbbikes'

# Attempt connection to database
# Print a statement on the screen to check whether the connection is working
try:
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}".format(USER,PASSWORD,URL,PORT),echo=True)
    print('+=========================+')
    print('|  CONNECTED TO DATABASE  |')
    print('+=========================+')
    engine.execute("use dbbikes;")
    
# Exit if connection not working   
except Exception as e:
        sys.exit(e)

# Create dataframe and store data running SQL query
rows = engine.execute("SELECT * from dbbikes.availability;")
df = []
for row in rows:
        df.append(dict(row))
df=pd.DataFrame(df)
# Examine dataframe object, show first 10 rows

df['number'] = df['number'].astype(int)
df['available_bikes'] = df['available_bikes'].astype(int)
df['available_bike_stands'] = df['available_bike_stands'].astype(int)

df['last_update'] = df['last_update'].astype(int)
df['last_update'] = df['last_update']//1000
df['last_update'] = df['last_update'].astype(str)
df['last_update'] = pd.to_datetime(df['last_update'], unit='s')
df['day_of_week'] = df['last_update'].dt.dayofweek + 1
df['hour'] = df['last_update'].dt.hour
df['date'] = df['last_update'].dt.date

# Create dataframe and store data running SQL query
rows = engine.execute("SELECT * from dbbikes.weather;")
df2 = []
for row in rows:
        df2.append(dict(row))
df2=pd.DataFrame(df2)

df2['dt'] = pd.to_datetime(df2['dt'], unit='s')

df2['date'] = df2['dt'].dt.date
df2['hour'] = df2['dt'].dt.hour
mergedStuff = pd.merge(df, df2, on = ['date', 'hour'], how = 'inner')
# Create a separate dataframe with days of the week (categorical)
data_input1 = pd.DataFrame(mergedStuff['day_of_week'])

# Create a separate dataframe with cloud coverage information (categorical)
data_input2 = pd.DataFrame(mergedStuff['description'])

# Concatenate the two dataframes in the main one
dummy = pd.get_dummies(data_input1)
dummy_2 = pd.get_dummies(data_input2)
mergedStuff = pd.concat([mergedStuff,dummy],axis=1)
mergedStuff = pd.concat([mergedStuff,dummy_2],axis=1)
# Select model features and store them in a new dataframe
input_model = pd.DataFrame(mergedStuff[['number', 'hour', 'temperture', 
'visibility', 'day_of_week','description_broken clouds', 'description_clear sky',
       'description_few clouds', 'description_fog', 'description_haze',
       'description_light intensity drizzle rain',
       'description_light intensity shower rain', 'description_light rain',
       'description_mist', 'description_moderate rain',
       'description_overcast clouds', 'description_scattered clouds']])

# Define target variable
output = mergedStuff['available_bikes']

# Split dataset to train and test
X_train,X_test,Y_train,Y_test=train_test_split(input_model,output,test_size=0.33,random_state=42)
print("Training the model on %s rows and %s columns." % X_train.shape)

# Instantiate RandomForestRegressor object calling 100 decision tree models
rf = RandomForestRegressor(n_estimators=100)

# Train the model
rf.fit(X_train, Y_train)

print("Testing the model on %s rows." % Y_test.shape[0])
LinearReg=LinearRegression()
LinearReg.fit(X_train,Y_train)
pred=LinearReg.predict(X_test)
pred1=pd.DataFrame(pred)
print (pred1)
print(X_test)
print(np.array(X_test))

# Get prediction for test cases
prediction = rf.predict(X_test)

# Show the predicted test cases
print(prediction)
print(Y_test)

print("RMSE: %f" % np.sqrt(metrics.mean_squared_error(Y_test,prediction)))

pickle.dump(rf, open('final_prediction.pickle', 'wb'))

# This is not strictly functional to the application
random_forest = pickle.load(open("final_prediction.pickle", "rb"))