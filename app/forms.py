from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class RouteForm(FlaskForm):
	airline = SelectField('Airline', choices=[])
	origin = SelectField('Origin', choices=[])
	destination = SelectField('Destination', choices=[])
	year = SelectField('Year', choices=[])
	submit = SubmitField('Explore')
