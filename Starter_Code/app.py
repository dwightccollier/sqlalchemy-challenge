# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session
from sqlalchemy import create_engine, func
import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqllite://Resources/hawaii.sqlite")


# reflect an existing database into a new model
BMap = automap_base

# reflect the tables
BMap.prepare(autoload_with=engine)

# Save references to each table
Measure = BMap.classes.measurement
Stat = BMap.classes.station


# Create our session (link) from Python to the DB
application = Flask(__name__)

#################################################
# Flask Setup
#################################################

def year():
    session = session(engine)
    #Defines the most recent date then uses that date to get the last date
    RDate = session.query(func.max(Measure.date)).first()[0]
    FDate = dt.datetime.strptime(RDate, "%Y-%m-%d") - dt.timedelta(days=365)

    session.close()

    return(FDate)
#This determines what happens when user goes to homepage
@application.route("/")

def home():
    return """ <h1> This is the Honolulu Climate API </h1.
    <h3> The available routes are: </h3>
    <ul>
    <li><a href = "/api/v1.0/precipitation"> Precipitation</a>: <strong>/api/v1.0/precipation</strong> </li>
    <li><a href = "/api/v1.0/stations"> Stations </a>: <strong>/api/v1.0/stations</strong></li>
    <li><a href = "/api/v1.0/tobs"> TOBS </a>: <strong>/api/v1.0/tobs</strong></li>
    <li>To retrieve the minimum, average, and maximum temperatures for the start date, use <strong>/api/v1.0/&ltstart&gt</strong> (use yyyy-mm-dd format)</li>
    <li> To retrieve the minimum, average, and maximum temperatures for the end range, use <strong>/api/v1.0/&ltstart&gt/&ltend&gt</strong> (use yyyy-mm-dd format)</li>
    </ul>
    """""
#Defines what to do when we hit the precipitation url
@application.route("/api/v1.0/precipitation")

def precipitation():
    session = session(engine)
    #Performs a query from last 12 months from most recent date in Measurement table
    Statdata = session.query(Measure.date,Measure.prcp).filter(Measure.date >= year()).all()

    session.close()
    #Creating our dictionary
    preList = []
    for date, prcp in Statdata:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        preList.append(dict)
    return jsonify(preList)
@application.route("/api/v1.0/stations")
def stations():
    session = session(engine)

    StatData = session.query(Stat.station).all()

    session.close()

    statList = list(np.ravel(StatData))

    return jsonify(statList)

@application.route("/api/v1.0/tobs")
def tobs():
    session = session(engine)

    tobsData = session.query(Measure.date,Measure.tobs).filter(Measure.station == 'USC00519281').filter(Measure.date >= year()).all()
    session.close()

    tobslist = []
    for date, tobs in tobsData:
        tobsDict = {}
        tobsDict["date"] = date
        tobsDict["tobs"] = tobs
        tobslist.append(tobsDict)
    return jsonify(tobslist)
@application.route("/api/v1.0/<start>")
@application.route("/api/v1.0/<start>/<end>")
def CalculateTemp(start=None,end=None):
    session = session(engine)

    GetTemp = [func.min(Measure.tobs),func.avg(Measure.tobs),func.max(Measure.tobs)]

    if end == None:
        BeginData = session.query(*GetTemp).filter(Measure.date >= start).all()
        BeginList = list(np.ravel(BeginData))

        return jsonify(BeginList)
    else:
        EndData = session.query(*GetTemp).filter(Measure.date >= start).filter(Measure.date <= end).all()
        EndList = list(np.ravel(EndData))

        return jsonify(BeginList)
    session.close()

    if __name__ == "_main_":
        app.run(debug = True)





#################################################
# Flask Routes
#################################################
