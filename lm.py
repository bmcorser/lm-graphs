import datetime
import time
import sqla
import models
import sensors

def getcallattr(obj, name):
    attr = getattr(obj, name)
    if not callable(attr):
        return attr
    return attr()

def create_models():
    sensors.init()
    S = sqla.session()
    try:
        for chip_struct in sensors.iter_detected_chips():
            chip = sqla.create(S, models.Chip, ['addr', 'bus', 'path', 'prefix'], chip_struct)
            S.add(chip)
            S.flush()
            for sensor_struct in chip_struct:
                sensor = sqla.create(S, models.Sensor, ['chip', 'label'], sensor_struct)
                sensor.chip_id = chip.id
                S.add(sensor)
                S.flush()
        S.commit()
    finally:
        sensors.cleanup()

def record():
    sensors.init()
    S = sqla.session()
    sensors_dict = {}
    for chip_struct in sensors.iter_detected_chips():
        for sensor_struct in chip_struct:
            key = "{0}{1}".format(sensor_struct.chip, sensor_struct.label)
            sensors_dict[key] = sqla.get(S, models.Sensor, ['chip', 'label'], sensor_struct).id
    try:
        while True:
            for chip_struct in sensors.iter_detected_chips():
                for sensor_struct in chip_struct:
                    key = "{0}{1}".format(sensor_struct.chip, sensor_struct.label)
                    sensor_id = sensors_dict[key]
                    reading = models.Reading()
                    reading.datetime = datetime.datetime.now()
                    reading_value = sensor_struct.get_value()
                    print(key, reading_value)
                    reading.value = reading_value
                    reading.sensor_id = sensor_id
                    S.add(reading)
                    S.commit()
            time.sleep(1)
    finally:
        sensors.cleanup()
