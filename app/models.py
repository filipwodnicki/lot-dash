from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(128))

	def __repr__(self):
		return '<User {}>'.format(self.name)

class Record(db.Model):
	__tablename__ = 'record'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	departures_scheduled = db.Column(db.Integer)
	departures_performed = db.Column(db.Integer)
	payload = db.Column(db.Integer)
	seats = db.Column(db.Integer)
	passengers = db.Column(db.Integer)
	freight = db.Column(db.Integer)
	mail = db.Column(db.Integer)
	distance = db.Column(db.Integer)
	ramp_to_ramp = db.Column(db.Integer)
	air_time = db.Column(db.Integer)
	unique_carrier = db.Column(db.String(6))
	airline_id = db.Column(db.Integer)
	unique_carrier_name = db.Column(db.String(128))
	unique_carrier_entity = db.Column(db.String(16))
	region = db.Column(db.String(3))
	carrier = db.Column(db.String(6))
	carrier_name = db.Column(db.String(128))
	carrier_group = db.Column(db.String(3))
	carrier_group_new = db.Column(db.String(3))
	origin_airport_id = db.Column(db.Integer)
	origin_airport_seq_id = db.Column(db.Integer)
	origin_city_market_id = db.Column(db.Integer)
	origin = db.Column(db.String(6))
	origin_city_name = db.Column(db.String(64))
	origin_country = db.Column(db.String(6))
	origin_country_name = db.Column(db.String(64))
	origin_wac = db.Column(db.Integer)
	dest_airport_id = db.Column(db.Integer)
	dest_airport_seq_id = db.Column(db.Integer)
	dest_city_market_id = db.Column(db.Integer)
	dest = db.Column(db.String(6))
	dest_city_name = db.Column(db.String(64))
	dest_country = db.Column(db.String(6))
	dest_country_name = db.Column(db.String(64))
	dest_wac = db.Column(db.Integer)
	aircraft_group = db.Column(db.Integer)
	aircraft_type = db.Column(db.Integer)
	aircraft_config = db.Column(db.Integer)
	year = db.Column(db.Integer)
	quarter = db.Column(db.Integer)
	month = db.Column(db.Integer)
	distance_group = db.Column(db.Integer)
	CLASS = db.Column(db.String(6))

	def __repr__(self):
		return '<Record {}: {}-{} {}/{} Seats:{} PAX:{}>'.format(self.unique_carrier, self.origin, self.dest, self.month, self.year, self.seats, self.passengers)

