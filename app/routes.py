from flask import render_template, jsonify
from app import app
from app.models import Airline, Airport, Origin, Destination, BTS_Record as R

@app.route('/')
@app.route('/index')
def index():
	# For all fligths to/from this city, Get the carrier/month/origin/destination/seats/passengers
	table_data = R.query\
					.join(Airline, R.airline)\
					.join(Origin, R.origin)\
					.join(Destination, R.dest)\
					.filter((Destination.code == "KRK")|(Origin.code == "KRK"))\
					.filter(Airline.carrier == "LO")\
					.with_entities(Airline.carrier, R.month, Origin.code, Destination.code, R.seats, R.passengers).all()
	# R.query.join(Airline, R.airline).join(Origin, R.origin).join(Destination, R.dest).filter((Destination.code == "KRK")|(Origin.code == "KRK")).filter(Airline.carrier == "LO").with_entities(Airline.carrier, R.month, Origin.code, Destination.code, R.seats, R.passengers).all()

	# Get the relevant months
	west_labels = R.query.join(Origin, R.origin).join(Destination, R.dest).filter((Origin.code == "ORD"),(Destination.code == "KRK")).with_entities(R.month).order_by(R.month).all()
	
	# Get the ORD-KRK passenger values
	west_values = R.query.join(Origin, R.origin).join(Destination, R.dest).filter((Origin.code == "ORD"),(Destination.code == "KRK")).with_entities(R.passengers).order_by(R.month).all()
	
	# Get the KRK-ORD Passenger values
	east_values = R.query.join(Origin, R.origin).join(Destination, R.dest).filter((Origin.code == "KRK"),(Destination.code == "ORD")).with_entities(R.passengers).order_by(R.month).all()
	return render_template('index.html', data=table_data, west_labels=west_labels, west_values=west_values, east_values=east_values)

content = ""
with open("README.md", "r") as f:
	content = f.read()
	
@app.route('/about')
def about():
	return render_template('about.html', text=content)

@app.route('/chart')
def chart():
	# Get the relevant months
	west_labels = R.query.join(Origin, R.origin).join(Destination, R.dest).filter((Origin.code == "ORD"),(Destination.code == "KRK")).with_entities(R.month).order_by(R.month).all()
	
	# Get the ORD-KRK passenger values
	west_values = R.query.join(Origin, R.origin).join(Destination, R.dest).filter((Origin.code == "ORD"),(Destination.code == "KRK")).with_entities(R.passengers).order_by(R.month).all()
	
	# Get the KRK-ORD Passenger values
	east_values = R.query.join(Origin, R.origin).join(Destination, R.dest).filter((Origin.code == "KRK"),(Destination.code == "ORD")).with_entities(R.passengers).order_by(R.month).all()
	return render_template('chart.html', west_labels=west_labels, west_values=west_values, east_values=east_values)

@app.route('/map')
def map():
	return render_template('map2.html')

# @app.route('/data')
# def data():
# 	result = R.query.with_entities(R.unique_carrier, R.month, R.origin, R.dest, R.seats, R.passengers).filter((R.origin == "KRK")|(R.dest == "KRK")).order_by(R.origin).all()
# 	return( jsonify(result ) )
	