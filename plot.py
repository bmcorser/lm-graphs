import operator
import uuid
import pandas
import plotly
from scipy import signal

import sqla
import models


def attrs(name, lst):
    return list(map(operator.attrgetter(name), lst))


def calls(name, lst):
    return list(map(operator.methodcaller(name), lst))

S = sqla.session()
P = plotly.plotly

sensors = (S.query(models.Sensor)
            .filter(models.Sensor.id.in_([13, 14, 18]))
            .all())

plotly_dicts = []
for sensor in sensors:
    b, a = signal.butter(2, 0.0006)
    ts = (pandas.Series.from_array(signal.lfilter(b, a, attrs('value', sensor.readings)),
                                   index=attrs('datetime', sensor.readings))
                       .resample('5min', how='mean'))
    plotly_dicts.append({
        'name': "{0}: {1}".format(sensor.chip, sensor.label),
        'x': calls('to_datetime', ts.index)[8:],
        'y': ts.values[8:],
    })

print(P.plot(plotly_dicts, uuid.uuid4(), auto_open=False))
