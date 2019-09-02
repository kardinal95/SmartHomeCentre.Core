from sqlalchemy.ext.declarative import declarative_base


class ModelBase:
    base = None

    @staticmethod
    def get_base():
        if ModelBase.base is None:
            ModelBase.base = declarative_base()
        return ModelBase.base
