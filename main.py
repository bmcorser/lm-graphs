import sqla
import lm

if __name__ == '__main__':
    sqla.init()
    lm.create_models()
    lm.record()
