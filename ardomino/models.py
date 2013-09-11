from flask.ext.sqlalchemy import SQLAlchemy

from .app import app


db = SQLAlchemy(app)


class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    device_name = db.Column(db.Text)
    sensor_name = db.Column(db.Text)
    sensor_value = db.Column(db.Text)
    sensor_units = db.Column(db.Text)
