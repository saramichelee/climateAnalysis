from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

prcpselect = [Measurement.date,Measurement.prcp]
yeardata = session.query(*prcpselect).order_by(Measurement.date).all()
prcp_dict = dict(yeardata)

statselect = [Station.id,Station.name]
stations = session.query(*statselect).order_by(Station.id).all()
stat_dict = dict(stations)

tobsselect = [Measurement.date,Measurement.tobs]
tobs = session.query(*tobsselect).filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
tobs_dict = dict(tobs)

@app.route("/")
def home():
    return (
        f"Welcome to the climateAnalysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate (YYYY-MM-DD)<br/>"
        f"/api/v1.0/startdate/enddate (YYYY-MM-DD)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(stat_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)

    def calc_temps(start_date):
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    empty_dict = {'min_temp' : [],"average_temp" : [],"max_temp" : []}

    strtdate = [start]

    for rng in strtdate:
        temp_loop = calc_temps(rng)
    
        empty_dict['min_temp'].append(temp_loop[0][0])
        empty_dict['average_temp'].append(temp_loop[0][1])
        empty_dict['max_temp'].append(temp_loop[0][2])  

    return jsonify(empty_dict)

@app.route("/api/v1.0/<start>/<end>")
def startend(start=None, end=None):
    engine = create_engine("sqlite:///hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)

    ranges = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
 
    rng_dict = {'min_temp' : [],"average_temp" : [],"max_temp" : []}

    rng_dict['min_temp'].append(ranges[0][0])
    rng_dict['average_temp'].append(ranges[0][1])
    rng_dict['max_temp'].append(ranges[0][2]) 

    return jsonify(rng_dict)

if __name__ == "__main__":
    app.run(debug=True, port=5008)
