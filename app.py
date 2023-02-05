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

if __name__ == '__main__':
    app.run(debug=True)

