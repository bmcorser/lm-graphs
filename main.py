import sensors

def getcallattr(obj, name):
    attr = getattr(obj, name)
    if not callable(attr):
        return attr
    return attr()

sensors.init()
try:
    for chip in sensors.iter_detected_chips():
        print('--')
        def is_public(attr_name):
            if attr_name.startswith('_') or attr_name.upper() == attr_name:
                return False
            return not isinstance(getattr(type(chip), attr_name, None), property)
        for attr in filter(is_public, dir(chip)):
            print("{0}: {1}".format(attr, getattr(chip, attr)))
        for feature in chip:
            for attr in filter(is_public, dir(feature)):
                print("  {0}: {1}".format(attr, getcallattr(feature, attr)))
finally:
    sensors.cleanup()
