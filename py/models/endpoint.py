from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from py import db_session
from py.models import DatabaseModel
from py.drivers import DriverTypeEnum


class EndpointMdl(DatabaseModel):
    __tablename__ = 'endpoints'
    name = Column(String(64))
    driver_uuid = Column(UUID(as_uuid=True), ForeignKey('driver_instances.uuid'))
    driver_type = Column(Enum(DriverTypeEnum))

    @classmethod
    @db_session
    def get_endpoint_by_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.uuid == uuid).first()