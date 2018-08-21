from flask import render_template, jsonify
from app import app
from app.models import Record
from app.models import Record as R

@app.route('/')
@app.route('/index')
def index():
	# result = R.query.with_entities(R.unique_carrier, R.month, R.origin, R.dest, R.seats, R.passengers).filter((R.origin == "KRK")|(R.dest == "KRK")).order_by(R.origin).all()
	result = R.query.with_entities(R.unique_carrier, R.month, R.origin, R.dest, R.seats, R.passengers).filter((Record.origin == "KRK")|(Record.dest == "KRK")).order_by(R.origin).all()
	west_labels = Record.query.with_entities(Record.month).filter(Record.origin == "KRK").all()#returns tuple like: [(1,), (2,)]
	west_values = Record.query.with_entities(Record.passengers).filter(Record.origin == "KRK").all()
	east_values = Record.query.with_entities(Record.passengers).filter((Record.origin == "ORD"),(Record.dest == "KRK")).all() 
	return render_template('index.html', data=result, west_labels=west_labels, west_values=west_values, east_values=east_values)

@app.route('/chart')
def chart():
	west_labels = Record.query.with_entities(Record.month).filter(Record.origin == "KRK").all()#returns tuple like: [(1,), (2,)]
	west_values = Record.query.with_entities(Record.passengers).filter(Record.origin == "KRK").all()
	east_values = Record.query.with_entities(Record.passengers).filter((Record.origin == "ORD"),(Record.dest == "KRK")).all() 
	return render_template('chart.html', west_labels=west_labels, west_values=west_values, east_values=east_values)

# @app.route('/data')
# def data():
# 	result = R.query.with_entities(R.unique_carrier, R.month, R.origin, R.dest, R.seats, R.passengers).filter((R.origin == "KRK")|(R.dest == "KRK")).order_by(R.origin).all()
# 	return( jsonify(result ) )
	