import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setup the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Flask routes
@app.route("/")
def home():
    """List all available API routes"""

    return (
        f"Welcome to the homepage API for Climate Analysis<br/>"
        f"The available routes are:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary by using date as the key and prcp as the value"""
    """"Return the JSON representation of the dictionary"""

    # Session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation date and quantity from Measurement table
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list of precipitation_res
    precipitation_res = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_res.append(precipitation_dict)

    # Retun the JSON representation of the precitation_res dictionary
    return jsonify(precipitation_res)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""

    # Session (link) from Python to the DB
    session = Session(engine)

    # Query all stations from Station table
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    # Return the JSON representation of the stations list
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temps():
    """Return a JSON list of temperature observations for the previous year"""

    # Session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()
    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    # Return the JSON representation of the temps list
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return a JSON list of the minimum temperature, the average temperature,"""
    """and the maximum temperature for a specified start or start-end range"""

    # Session (link) from Python to the DB
    session = Session(engine)

    # Logic when start date only given
    if not end:
        results = session.query(\
            func.min(Measurement.tobs),\
            func.avg(Measurement.tobs),\
            func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    # Logic when start and end dates give
    results = session.query(\
        func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)

