from py.core import MainHub
from py.core.db import DatabaseSrv


def db_session(func):
    def wrapper(*args, **kwargs):
        if 'session' not in kwargs.keys():
            s = MainHub.retrieve(DatabaseSrv).session()
            kwargs['session'] = s
            res = func(*args, **kwargs)
            s.close()
            return res
        else:
            return func(*args, **kwargs)
    return wrapper
