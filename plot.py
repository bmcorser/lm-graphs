import operator
import uuid
import sqla, models, pandas, plotly

S = sqla.session()
P = plotly.plotly

readings = S.query(models.Reading.datetime, models.Reading.value).filter(models.Reading.sensor_id == 13).order_by(models.Reading.datetime).all()


def attrlist(name, lst):
    return list(map(operator.attrgetter(name), lst))

def methlist(name, lst):
    return list(map(operator.methodcaller(name), lst))

ts = (pandas.Series.from_array(attrlist('value', readings),
                               index=attrlist('datetime', readings))
                   .resample('5min', how='mean'))
plotly_dict = dict(x=methlist('to_datetime', ts.index), y=list(map(float, ts.values)))

print(P.plot([plotly_dict], uuid.uuid4(), auto_open=False))
