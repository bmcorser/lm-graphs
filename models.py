import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Chip(Base):
    __tablename__ = 'chip'
    id = sa.Column(sa.Integer, primary_key=True)
    addr = sa.Column(sa.String)
    bus = sa.Column(sa.String)
    path = sa.Column(sa.String)
    prefix = sa.Column(sa.String)


class Sensor(Base):
    __tablename__ = 'sensor'
    id = sa.Column(sa.Integer, primary_key=True)
    chip_id = sa.Column(sa.Integer, sa.ForeignKey('chip.id'))
    label = sa.Column(sa.String)

    chip = sa.orm.relationship(Chip, backref=sa.orm.backref('sensors'))


class Reading(Base):
    __tablename__ = 'reading'
    id = sa.Column(sa.Integer, primary_key=True)
    sensor_id = sa.Column(sa.Integer, sa.ForeignKey('sensor.id'))
    sensor = sa.orm.relationship(Sensor, backref=sa.orm.backref('readings'))
    value = sa.Column(sa.Float)
