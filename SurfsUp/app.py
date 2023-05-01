# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


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
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome! Please see below. "
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# For precipitation
@app.route('/api/v1.0/precipitation')
def Precipitation():
    session = Session(engine)
    precip = [Measurement.date,Measurement.prcp]
    all_precip = session.query(*precip).all()
    session.close()

    # For dictionary
    total_precipitation = []
    for date, prcp in all_precip:
        prcp_dictionary = {}
        prcp_dictionary["Date"] = date
        prcp_dictionary["Precipitation"] = prcp
        total_precipitation.append(prcp_dictionary)

    return jsonify(total_precipitation)

# For stations
@app.route('/api/v1.0/stations')
def Stations():
    session = Session(engine)
    for_station = session.query(Station.station, Station.id).all()
    session.close()

    #For dictionary
    stations_values = []
    for station, id in for_station:

        stations_dict = {}

        stations_dict['station'] = station
        stations_dict['id'] = id
        stations_values.append(stations_dict)
        
    return jsonify (stations_values) 

#For tobs
@app.route('/api/v1.0/tobs')
def Tobs():
    session = Session(engine)
    tobs = session.query(Measurement.date,Measurement.tobs,Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').filter(Measurement.station=='USC00519281').order_by(Measurement.date).all()
    session.close()

    #For dictionary
    all_tobs = []
    for date, tobs, prcp in tobs:

        tobs_dict = {}

        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs        
        tobs_dict["Precipitation"] = prcp    
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

#For Start Date only
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    session = Session(engine)

    """Return the TMIN, TAVG, and TMAX for dates greater than or equal to the start date"""

    start_res = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    start_date_info = []
    for min, avg, max in start_res:

        start_dict = {}

        start_dict["Min Temp"] = min
        start_dict["Avg Temp"] = avg
        start_dict["Max Temp"] = max

        start_date_info.append(start_dict) 

    return jsonify(start_date_info)

#For start date AND send date
@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    session = Session(engine)

    """Return the TMIN, TAVG, and TMAX for dates greater than or equal to the start date to the end date"""

    start_end_res = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    start_end_date = []
    for min, avg, max in start_end_res:

        start_end_dict = {}

        start_end_dict["Min Temp"] = min
        start_end_dict["Avg Temp"] = avg
        start_end_dict["Max Temp"] = max

        start_end_date.append(start_end_dict) 

    return jsonify(start_end_date)


if __name__ == '__main__':
    app.run(debug=True)