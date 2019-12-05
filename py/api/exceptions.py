from flask_restful import abort
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import ExpiredSignatureError


def abort_on_exc(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IncorrectTargetException as e:
            abort(404, message=str(e))
        except JWTExtendedException as e:
            abort(400, message=str(e))
        except ExpiredSignatureError as e:
            abort(400, message=str(e))
    return wrapper


class IncorrectTargetException(Exception):
    def __init__(self, uuid, target_type):
        self.uuid = uuid
        self.target_type = target_type

    def __str__(self):
        try:
            name = self.target_type.__short__
        except AttributeError:
            name = self.target_type.__name__
        return '{} with uuid {} does not exist'.format(name, self.uuid)
