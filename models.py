import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Chip(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    addr = sa.Column(sa.String)
    bus = sa.Column(sa.String)
    prefix = sa.Column(sa.String)

    features = 

class Sensor(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    addr = sa.Column(sa.String)
    bus = sa.Column(sa.String)
    prefix = sa.Column(sa.String)

class SensorReading(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    sensor_id = sa.Column(sa.Integer, primary_key=True)
