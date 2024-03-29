from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


class ModelBase:
    base = None

    @staticmethod
    def get_base():
        if ModelBase.base is None:
            ModelBase.base = declarative_base()
        return ModelBase.base


class DatabaseModel(ModelBase.get_base()):
    __abstract__ = True

    uuid = Column(UUID(as_uuid=True),
                  unique=True,
                  nullable=False,
                  primary_key=True,
                  server_default=text('uuid_generate_v4()'))