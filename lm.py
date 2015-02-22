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
            chip = sqla.get(S, models.Chip, ['addr', 'bus', 'path', 'prefix'], chip_struct)
            for sensor_struct in chip_struct:
                sensor = sqla.get(S, models.Sensor, ['label'], sensor_struct)
                sensor.chip = chip
                S.add(sensor)
        S.flush()
        S.commit()
    finally:
        sensors.cleanup()

def record():
    sensors.init()
    S = sqla.session()
    try:
        while True:
            for chip_struct in sensors.iter_detected_chips():
                chip = sqla.get(S, models.Chip, ['addr', 'bus', 'path', 'prefix'], chip_struct)
                for sensor_struct in chip_struct:
                    sensor = sqla.get(S, models.Sensor, ['label'], sensor_struct)
                    sensor.chip = chip
                    reading = models.Reading()
                    reading_value = sensor_struct.get_value()
                    print(sensor.label, reading_value)
                    reading.value = reading_value
                    reading.sensor = sensor
                    S.add(reading)
                    S.flush()
                    S.commit()
            time.sleep(1)
    finally:
        sensors.cleanup()