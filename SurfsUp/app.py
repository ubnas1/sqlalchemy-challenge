import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect,desc, func
import datetime as dt
import pandas as pd
import json


from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
# Base.prepare(autoload_with=engine)
Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

# starting session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<'start'><br/>"
        f"/api/v1.0/<'start'>/<'end'><br/> <br/>Date format example -- /api/v1.0/2015-8-12/2017-5-10"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # creating date time objects of first and last date required
    date1 = dt.datetime(2017,8,23)
    date2 = dt.datetime(2016,8,23)
    
    # extracting the required columns from the database.
    prec_1_year = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date>date2).filter(Measurement.date<date1).all()
    session.close()

    # returning JSON
    return jsonify(prec_1_year)



@app.route("/api/v1.0/stations")
def stations():

    # extracting the required columns from the database.
    stations_list = session.query(Station.name).all()
    session.close()

    # returning JSON
    return jsonify(stations_list)




@app.route("/api/v1.0/tobs")
def tobs():

    # extracting the required columns from the database.
    measurements_list = session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all()

    # closing session 
    session.close()

    # converting to Pandas Dataframe
    measurements_df = pd.DataFrame(measurements_list, columns=["id", "station", "date", "prcp", "tobs"])
    
    # finding the bussiest station
    measurements_stations_df = measurements_df.groupby('station').count()
    bussiest_station = measurements_stations_df['id'].idxmax()
    bussiest_station_df = measurements_df.loc[measurements_df['station'] == bussiest_station]
    bussiest_station_1_year_df = bussiest_station_df[(bussiest_station_df['date'] >= '2016-1-1') & (bussiest_station_df['date'] <= '2017-8-18')]
    bussiest_station_1_year_df.set_index('date', inplace=True)

    # bussiest station last 1 year tobs
    bussiest_station_1_year_df = bussiest_station_1_year_df[["tobs"]]
    
    # converting to a dictionary
    bussiest_station_1_year_df = bussiest_station_1_year_df.to_dict()
    
    # returning JSON
    return jsonify(bussiest_station_1_year_df)

@app.route("/api/v1.0/<start>")
def start(start):
    
    # extracting the required columns from the database.
    measurements_list = session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.tobs).all()
    
    # closing session 
    session.close()

    # converting to Pandas Dataframe
    measurements_df = pd.DataFrame(measurements_list, columns=["id", "station", "date", "tobs"])
   
    # finding the bussiest station
    measurements_stations_df = measurements_df.groupby('station').count()
    bussiest_station = measurements_stations_df['id'].idxmax()
    bussiest_station_df = measurements_df.loc[measurements_df['station'] == bussiest_station]
    bussiest_station_df['date'] = pd.to_datetime(bussiest_station_df['date'])
   
    # extracting bussiest station's tobs starting from the provided start date   
    bussiest_station_df_2 = bussiest_station_df.loc[(bussiest_station_df['date']) >= start]
    
    # bussiest station's min, max and average tobs
    min = bussiest_station_df_2["tobs"].min()
    max = bussiest_station_df_2["tobs"].max()
    avg = bussiest_station_df_2["tobs"].mean()

    # creating a dictionary of reesults
    values = {"Minimum Temperature": min,
              "Maximum Temperature": max,
              "Average Temperature": avg}

    # returning JSON
    return jsonify(values)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
   
    # extracting the required columns from the database.
    measurements_list = session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.tobs).all()

    # closing session
    session.close()

    # converting to pandas dataframe
    measurements_df = pd.DataFrame(measurements_list, columns=["id", "station", "date", "tobs"])
    
    # finding bussiest station
    measurements_stations_df = measurements_df.groupby('station').count()
    bussiest_station = measurements_stations_df['id'].idxmax()
    bussiest_station_df = measurements_df.loc[measurements_df['station'] == bussiest_station]
    bussiest_station_df['date'] = pd.to_datetime(bussiest_station_df['date'])
    
    
    # extracting bussiest station's tobs starting from the provided start date and finishing on provided end date 
    bussiest_station_df_2 = bussiest_station_df.loc[(bussiest_station_df['date'] >= start) & (bussiest_station_df['date'] <= end)]
    min = bussiest_station_df_2["tobs"].min()
    max = bussiest_station_df_2["tobs"].max()
    avg = bussiest_station_df_2["tobs"].mean()


    # creating a dictionary of reesults
    values = {"Minimum Temperature": min,
              "Maximum Temperature": max,
              "Average Temperature": avg}

    # returning JSON
    return jsonify(values)


if __name__ == '__main__':
    app.run(debug=True)