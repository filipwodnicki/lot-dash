from flask import render_template, jsonify, request
from app import app
from app.models import Airline, Airport, Origin, Destination, BTS_Record as R
from app.forms import RouteForm
from sqlalchemy import or_, and_
from sqlalchemy import func

content = ""
with open("README.md", "r") as f:
	content = f.read()
	
@app.route('/about')
def about():
	return render_template('about.html', text=content)

@app.route('/chart')
def chart():
	# Get the relevant months
	west_labels = R.query.join(Origin, R.origin).join(Destination, R.dest).filter( and_((Origin.code == "ORD"),(Destination.code == "KRK")) ).with_entities(R.month).order_by(R.month).all()
	# Get the ORD-KRK passenger values
	west_values = R.query.join(Origin, R.origin).join(Destination, R.dest).filter( and_((Origin.code == "ORD"),(Destination.code == "KRK")) ).with_entities(R.passengers).order_by(R.month).all()
	# Get the KRK-ORD Passenger values
	east_values = R.query.join(Origin, R.origin).join(Destination, R.dest).filter( and_((Origin.code == "KRK"),(Destination.code == "ORD")) ).with_entities(R.passengers).order_by(R.month).all()
	return render_template('chart.html', west_labels=west_labels, west_values=west_values, east_values=east_values)

@app.route('/map')
def map():
	return render_template('map2.html')

@app.route('/routes', methods = ['GET', 'POST'])
def routes():
	form = RouteForm()
	if request.method == 'POST':
		airline_id = form.airline.data
		origin_id = form.origin.data
		destination_id = form.destination.data
		year = form.year.data

		airline = Airline.query.filter(Airline.id == airline_id).first()
		origin = Airport.query.filter(Airport.id == origin_id).first()
		destination = Airport.query.filter(Airport.id == destination_id).first()

		airline_name = airline.carrier_name
		airline_code = airline.carrier
		origin_city_name = origin.city_name
		origin_city_code = origin.code
		destination_city_name = destination.city_name
		destination_city_code = destination.code

		table_data = R.query\
						.filter(R.year == year)\
						.filter(R.airline_id == airline_id)\
						.filter( or_( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) , and_((R.origin_id == destination_id),(R.dest_id == origin_id)) ) )\
						.join(Origin, R.origin)\
						.join(Destination, R.dest)\
						.join(Airline, R.airline)\
						.with_entities(Airline.carrier, R.month, Origin.code, Destination.code, func.sum(R.seats), func.sum(R.passengers) )\
						.group_by(R.origin_id, R.month)\
						.order_by(R.origin_id, R.month)\
						.all()

		# Get the relevant months
		west_labels = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) )\
						.with_entities(R.month)\
						.group_by(R.month)\
						.order_by(R.month).all()
		
		# Get the ORD-KRK passenger values
		west_values = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) )\
						.with_entities(func.sum(R.passengers))\
						.group_by(R.month)\
						.order_by(R.month).all()
		
		# Get the KRK-ORD Passenger values
		east_values = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == destination_id),(R.dest_id == origin_id)) )\
						.with_entities(func.sum(R.passengers))\
						.group_by(R.month)\
						.order_by(R.month).all()
		return render_template('index.html', form=form,\
					 data=table_data, west_labels=west_labels, west_values=west_values, east_values=east_values,\
					 airline_name=airline_name, airline_code=airline_code, origin_city_name=origin_city_name, \
					 origin_city_code=origin_city_code, destination_city_name=destination_city_name, destination_city_code=destination_city_code)
	return render_template('index.html', form=form)

@app.route('/airline')
def route_airlines():
	airlines = Airline.query.order_by(Airline.carrier_name).all()
	airlineArray = []

	for airline in airlines:
		airlineObj = {}
		airlineObj['id'] = airline.id
		airlineObj['carrier'] = airline.carrier
		airlineObj['carrier_name'] = airline.carrier_name
		airlineArray.append(airlineObj)

	return jsonify({'airlines' : airlineArray})

@app.route('/airline/<airline>/')
def route_airline_origins(airline):

	records = R.query\
				.filter_by(airline_id = airline)\
				.join(Origin, R.origin)\
				.group_by(Origin.id)\
				.order_by(Origin.city_name)\
				.all()

	originArray = []

	for record in records:
		originObj = {}
		originObj['id'] = record.origin.id
		originObj['code'] = record.origin.code
		originObj['city_name'] = record.origin.city_name
		originArray.append(originObj)

	return jsonify({'origins' : originArray})

@app.route('/airline/<airline>/<origin>')
def route_airline_origin_destination(airline, origin):
	records = R.query.filter_by(airline_id = airline).filter_by(origin_id = origin).join(Destination, R.dest).group_by(Destination.id).order_by(Destination.city_name).all()
	
	destinationArray = []

	for record in records:
		destinationObj = {}
		destinationObj['id'] = record.dest.id
		destinationObj['code'] = record.dest.code
		destinationObj['city_name'] = record.dest.city_name
		destinationArray.append(destinationObj)

	return jsonify({'destinations' : destinationArray})

@app.route('/airline/<airline>/<origin>/<destination>')
def route_airline_origins_destination_years(airline, origin, destination):
	records = R.query.filter_by(airline_id = airline).filter_by(origin_id = origin).filter_by(dest_id = destination).group_by(R.year).order_by(R.year).all()
	
	yearArray = []

	for record in records:
		yearObj = {}
		yearObj['year'] = record.year
		yearArray.append(yearObj)

	return jsonify({'years' : yearArray})


	