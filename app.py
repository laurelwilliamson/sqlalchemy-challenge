#Imports
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import warnings
warnings.filterwarnings('ignore')

from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///hawaii1.sqlite", echo=False)

# create engine to hawaii.sqlite
hawaii_path = "hawaii_db"
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#create session
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Create routes for homepage, prcp, stations, tobs, start/start-end
#Homepage:
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    ) 


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query
    results = session.query(measurement.prcp, measurement.date).\
    filter(measurement.date >= '2016-08-23').\
    order_by(measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    date_prcp_dict = []
    for date, prcp in results:
        dpdict = {}
        dpdict["precipitation"] = prcp
        dpdict["date"] = date
        date_prcp_dict.append(dpdict)

    return jsonify(date_prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query 
    results = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query all passengers
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= '2016-08-23').\
    filter(measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    lastyr = list(np.ravel(results))

    return jsonify(lastyr)

@app.route('/api/v1.0/<start>', methods=['GET'])
def start(start):
    #query
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start).all()
    
    session.close()
    
    stats = list(np.ravel(results))

    return (
        f"The min, max, and avg are : !<br/>"
        jsonify(stats)
    )

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
# Create our session (link) from Python to the DB
    session = Session(engine)
 
   
    # Query 
    
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start, measurement.date <= end).all()

    session.close()

   #JSONify
    stats = list(np.ravel(results))

    return (
        f"The min, max, and avg are : !<br/>"
        jsonify(stats)
    )


if __name__ == '__main__':
    app.debug = True
    app.run()
  