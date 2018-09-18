from flask import render_template, jsonify, request
from app import app
from app.models import Airline, Airport, AirportGEO, Origin, Destination, BTS_Record as R
from app.forms import RouteForm
from sqlalchemy import or_, and_, func, cast, Float

content = ""
with open("README.md", "r") as f:
	content = f.read()
	
@app.route('/about')
def about():
	return render_template('about.html', text=content)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index')
def index():
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

		origin_geo = AirportGEO.query.filter(AirportGEO.airport_id == origin_id).first()
		destination_geo = AirportGEO.query.filter(AirportGEO.airport_id == destination_id).first()

		origin_lat = origin_geo.lat
		origin_lng = origin_geo.lng
		destination_lat = destination_geo.lat
		destination_lng = destination_geo.lng

		# table_data = R.query\
		# 				.filter(R.year == year)\
		# 				.filter(R.airline_id == airline_id)\
		# 				.filter( or_( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) , and_((R.origin_id == destination_id),(R.dest_id == origin_id)) ) )\
		# 				.join(Origin, R.origin)\
		# 				.join(Destination, R.dest)\
		# 				.join(Airline, R.airline)\
		# 				.with_entities(Airline.carrier, R.month, Origin.code, Destination.code, func.sum(R.departures), func.sum(R.seats), func.sum(R.passengers), func.sum(cast(R.passengers, Float())) / func.sum(cast(R.seats, Float())))\
		# 				.group_by(R.origin_id, R.month)\
		# 				.order_by(R.origin_id, R.month)\
		# 				.all()

		table_data = R.query\
						.with_entities(Origin.code, Destination.code, Airline.carrier, R.month, func.sum(R.departures), func.sum(R.seats), func.sum(R.passengers), func.sum(cast(R.passengers, Float())) / func.sum(cast(R.seats, Float())))\
						.filter(R.year == year)\
						.filter(R.airline_id == airline_id)\
						.filter( or_( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) , and_((R.origin_id == destination_id),(R.dest_id == origin_id)) ) )\
						.join(Origin, R.origin)\
						.join(Destination, R.dest)\
						.join(Airline, R.airline)\
						.group_by(Origin.code, Destination.code, Airline.carrier, R.month)\
						.order_by(R.month, Origin.code)\
						.all()

		# Get the relevant months
		months = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) )\
						.filter(R.year == year)\
						.with_entities(R.month)\
						.group_by(R.month)\
						.order_by(R.month).all()
		
		# Get the ORD-KRK passenger values
		pax = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) )\
						.filter(R.year == year)\
						.with_entities(func.sum(R.passengers))\
						.group_by(R.month)\
						.order_by(R.month).all()
		
		# Get the KRK-ORD Passenger values
		paxreverse = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == destination_id),(R.dest_id == origin_id)) )\
						.filter(R.year == year)\
						.with_entities(func.sum(R.passengers))\
						.group_by(R.month)\
						.order_by(R.month).all()

		seats = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) )\
						.filter(R.year == year)\
						.with_entities(func.sum(R.seats))\
						.group_by(R.month)\
						.order_by(R.month).all()

		seatsreverse = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == destination_id),(R.dest_id == origin_id)) )\
						.filter(R.year == year)\
						.with_entities(func.sum(R.seats))\
						.group_by(R.month)\
						.order_by(R.month).all()

		flights = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == origin_id),(R.dest_id == destination_id)) )\
						.filter(R.year == year)\
						.with_entities(func.sum(R.departures))\
						.group_by(R.month)\
						.order_by(R.month).all()

		flightsreverse = R.query\
						.filter(R.airline_id == airline_id)\
						.filter( and_((R.origin_id == destination_id),(R.dest_id == origin_id)) )\
						.filter(R.year == year)\
						.with_entities(func.sum(R.departures))\
						.group_by(R.month)\
						.order_by(R.month).all()


		stats = {}

		yearly_pax = sum(i for i, in pax + paxreverse)
		stats['yearly_pax'] = "{:,.0f}".format(yearly_pax)
		yearly_seats = sum(i for i, in seats + seatsreverse)
		stats['yearly_seats'] = "{:,.0f}".format(yearly_seats)
		stats['yearly_lf'] = "{0:.1%}".format(float(yearly_pax) / float(yearly_seats))
		yearly_flights = sum(i for i, in flights + flightsreverse)
		stats['yearly_flights'] = "{:,.0f}".format(yearly_flights)
		stats['seats_per_flight'] = "{0:.1f}".format(float(yearly_seats) / float(yearly_flights))
		stats['passengers_per_flight'] = "{0:.1f}".format(float(yearly_pax) / float(yearly_flights))

		# yearly_us_arrivals = 
		# yearly_us_departures =


		return render_template('index.html', scroll="content", form=form,\
					 data=table_data, months=months, pax=pax, paxreverse=paxreverse, seats=seats,\
					 airline_name=airline_name, airline_code=airline_code, origin_city_name=origin_city_name, \
					 origin_city_code=origin_city_code, destination_city_name=destination_city_name, destination_city_code=destination_city_code,\
					 origin_lat = origin_lat, origin_lng=origin_lng, destination_lat=destination_lat, destination_lng=destination_lng,\
					 stats=stats)
	return render_template('index.html', form=form)

@app.route('/airline')
def route_airlines():
	
	# SQLite syntax
	# airlines = R.query\
	# 			.filter(R.passengers >= 1)\
	# 			.filter(R.departures >=4)\
	# 			.group_by(R.airline_id)\
	# 			.join(Airline, R.airline)\
	# 			.add_columns(Airline.id, Airline.carrier, Airline.carrier_name)\
	# 			.order_by(Airline.carrier_name)\
	# 			.all()

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

	# SQLite syntax
	# records = R.query\
	# 			.filter_by(airline_id = airline)\
	# 			.filter(R.departures > 1)\
	# 			.filter(R.passengers > 1)\
	# 			.join(Origin, R.origin)\
	# 			.group_by(Origin.id)\
	# 			.order_by(Origin.city_name)\
	# 			.all()

	records = R.query\
				.filter_by(airline_id = airline)\
				.filter(R.departures >= 1)\
				.filter(R.passengers >= 1)\
				.distinct(R.origin_id)\
				.join(R.origin)\
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
	# SQLite syntax
	# records = R.query.filter_by(airline_id = airline).filter_by(origin_id = origin).join(Destination, R.dest).group_by(Destination.id).order_by(Destination.city_name).all()
	
	records = R.query\
				.filter_by(airline_id = airline)\
				.filter_by(origin_id = origin)\
				.filter(R.departures >= 1)\
				.filter(R.passengers >= 1)\
				.distinct(R.dest_id)\
				.join(R.dest)\
				.all()

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
	# SQLite syntax
	# records = R.query.filter_by(airline_id = airline).filter_by(origin_id = origin).filter_by(dest_id = destination).group_by(R.year).order_by(R.year).all()
	
	records = R.query\
            .filter_by(airline_id = airline)\
            .filter_by(origin_id = origin)\
            .filter_by(dest_id = destination)\
            .distinct(R.year)\
            .order_by(R.year.desc())\
            .all()

	yearArray = []

	for record in records:
		yearObj = {}
		yearObj['year'] = record.year
		yearArray.append(yearObj)

	return jsonify({'years' : yearArray})


	