import operator
import uuid
import sqla, models, plotly
from scipy import signal

S = sqla.session()
P = plotly.plotly

readings = (S.query(models.Reading.datetime, models.Reading.value)
             .filter(models.Reading.sensor_id == 13)
             .order_by(models.Reading.datetime)
             .all())


def attrs(name, lst):
    return list(map(operator.attrgetter(name), lst))

values = attrs('value', readings)
b, a = signal.butter(2, 0.0006)
filtered_values = signal.lfilter(b, a, values)
plotly_dict = dict(x=attrs('datetime', readings), y=filtered_values)

print(P.plot([plotly_dict], uuid.uuid4(), auto_open=False))
