import sensors

sensors.init()
try:
    for chip in sensors.iter_detected_chips():
        def is_public(attr_name):
            if attr_name.startswith('_') or attr_name.upper() == attr_name:
                return False
            return not isinstance(getattr(type(chip), attr_name, None), property)
        for attr in filter(is_public, dir(chip)):
            print(getattr(chip, attr))
        # print ('%s at %s' % (chip, chip.adapter_name))
        # for feature in chip:
            # print ('  %s: %.2f' % (feature.label, feature.get_value()))
finally:
    sensors.cleanup()
