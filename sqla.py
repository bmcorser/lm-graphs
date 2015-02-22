import sqlalchemy as sa
import models


def engine():
    return sa.create_engine('sqlite:///lm-sqla.db')


def session():
    return sa.orm.sessionmaker(bind=engine())()


def get(S, model, cols, struct):
    col_values = {}
    for col in cols:
        value = getattr(struct, col)
        if isinstance(value, bytes):
            col_values[col] = str(value, 'utf-8')
        else:
            col_values[col] = str(value)
    print(col_values)
    Q = S.query(model).filter_by(**col_values)
    try:
        return Q.one()
    except sa.orm.exc.NoResultFound:
        instance = model()
        for col, value in col_values.items():
            print(value)
            setattr(instance, col, value)
        S.add(instance)
        S.flush()
        return instance


def init():
    models.Base.metadata.create_all(engine())
