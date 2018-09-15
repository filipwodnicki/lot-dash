from app import db
from sqlalchemy.orm import relationship, aliased



class Airport(db.Model):
	__tablename__ = 'airport'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	code = db.Column(db.String(6), unique=True) #primary key
	city_name = db.Column(db.String(64))
	country_code = db.Column(db.String(6))
	country_name = db.Column(db.String(64))
	geo = relationship("AirportGEO", uselist=False, back_populates="airport")

class AirportGEO(db.Model):
	__tablename__ = 'airportgeo'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'))
	airport = relationship("Airport", back_populates="geo")
	lat = db.Column(db.Numeric)
	lng = db.Column(db.Numeric)

class Airline(db.Model):
	__tablename__ = 'airline'
	__table_args__ = (db.UniqueConstraint('carrier', 'carrier_name', name='uix_1'),)
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	carrier = db.Column(db.String(6)) # get from unique
	carrier_name = db.Column(db.String(128)) # get from unique

	# records = relationship("BTS_Record", foreign_keys="BTS_Record.airline_id", back_populates="airline")
	

class BTS_Record(db.Model):
	__tablename__ = 'bts_record'
	# __table_args__ = (db.UniqueConstraint('airline_id', 'origin_id', 'dest_id', 'year', 'month', name='uix_2'),)
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	origin_id = db.Column(db.Integer, db.ForeignKey('airport.id'))
	dest_id = db.Column(db.Integer, db.ForeignKey('airport.id'))
	airline_id = db.Column(db.Integer, db.ForeignKey('airline.id'))
	year = db.Column(db.Integer)
	quarter = db.Column(db.Integer)
	month = db.Column(db.Integer)
	departures = db.Column(db.Integer) #departures_performed
	payload = db.Column(db.Integer)
	seats = db.Column(db.Integer)
	passengers = db.Column(db.Integer)
	freight = db.Column(db.Integer)

	def loadfactor(self):
		return (float(self.passengers) / float(self.seats))

	airline = relationship("Airline", foreign_keys=[airline_id])
	origin = relationship("Airport", foreign_keys=[origin_id])
	dest = relationship("Airport", foreign_keys=[dest_id])

Origin = aliased(Airport)
Destination = aliased(Airport)


	# class Parent(Base):
	#     __tablename__ = 'parent'
	#     id = Column(Integer, primary_key=True)
	#     children = relationship("Child", back_populates="parent")

	# class Child(Base):
	#     __tablename__ = 'child'
	#     id = Column(Integer, primary_key=True)
	#     parent_id = Column(Integer, ForeignKey('parent.id'))
	#     parent = relationship("Parent", back_populates="children")
