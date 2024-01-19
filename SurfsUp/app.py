# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine 
from sqlalchemy import func

from flask import Flask
from flask import jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
#precipitation route
#################################################

@app.route("/api.v1.0/precipitation")
def precipitation():
    print("server received request for 'precipitation' page...")
    
    # Calculate the date one year from the last date in data set.
    date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    precipitation_data =  session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= date).all()


    # create dictionary
    prcp_data_list = []
    for date, precipitation in precipitation_data:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = precipitation
        prcp_data_list.append(prcp_dict)

# close the session
    session.close()
#show list
    return jsonify(prcp_data_list)


#################################################
#stations route
#################################################

@app.route("/api.v1.0/stations")
def stations():
    print("server received request for 'stations' page...")

    #query station data
    station_data = [Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    
    stations = session.query(*station_data).all()


    #create dictionary for stations data
    station_data_list = []
    for id, station, name, latitude, longitude, elevation in stations:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_data_list.append(station_dict)

# close the session
    session.close()
#show list
    return jsonify(station_data_list)    

#################################################
#tobs route
#################################################

@app.route("/api.v1.0/tobs")
def tobs():
    print("server received request for 'tobs' page...")
    
    # Calculate the date one year from the last date in data set.
    date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    #Query for most active station
    most_active_station = [Measurement.date, Measurement.tobs]

    most_active_data = session.query(*most_active_station).\
        filter(func.strftime(Measurement.date) >= date).\
        filter(Measurement.station == 'USC00519281').all()
        
    #create dictionary
    tobs_data_list=[]
    for date, tobs in most_active_data:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs']= tobs
        tobs_data_list.append(tobs_dict)
     
# close the session
    session.close()
#show list
    return jsonify(tobs_data_list)  

    
#################################################
#start route as /YYYY-MM-DD
#################################################
@app.route("/api.v1.0/<start>")
def start(start):
    print("server received request for 'start' page...")
 
 #query for min, max, and avg tobs
    start_date_data = [func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs)]

    start_date_tobs = session.query(*start_date_data).\
        filter(Measurement.date >= start).all()
    

    #create dictionary
    tobs_date_data_list = []

    for min, max, avg in start_date_tobs:
        tobs_date_dict ={}
        tobs_date_dict["min"] = min
        tobs_date_dict["max"] = max
        tobs_date_dict["avg"] = avg
        tobs_date_data_list.append(tobs_date_dict)

   # close the session
    session.close()
    #show list
    return jsonify(tobs_date_data_list)  

#################################################
#start/end route as /YYYY-MM-DD/YYYY-MM-DD
#################################################
@app.route("/api.v1.0/<start>/<end>")
def start_end(start, end):
    print("server received request for 'start/end' page...")
    
    #query for min, max, and avg tobs
    date_range_data = [func.min(Measurement.tobs),
                 func.max(Measurement.tobs),
                  func.avg(Measurement.tobs)]
    
    
    date_range_tobs = session.query(*date_range_data).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
    #create dictionary
    tobs_date_range_list = []

    for min, max, avg in date_range_tobs:
        tobs_range_dict ={}
        tobs_range_dict["min"] = min
        tobs_range_dict["max"] = max
        tobs_range_dict["avg"] = avg
        tobs_date_range_list.append(tobs_range_dict)
        
    # close the session 
    session.close()
    
    #show list
    return jsonify(tobs_date_range_list) 
    
#################################################
#home route
#################################################

@app.route("/")
def home():
    print("Server received request for 'default' page...")
    return (f"Available Routes:<br/>"
            f"/api.v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>")
    

#End
if __name__ == "__main__":
    app.run(debug = True)