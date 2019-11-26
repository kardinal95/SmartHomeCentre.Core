from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID

from py.models import DatabaseModel
from py.drivers import DriverTypeEnum


class EndpointMdl(DatabaseModel):
    __tablename__ = 'endpoints'
    name = Column(String(64))
    driver_uuid = Column(UUID(as_uuid=True), ForeignKey('driver_instances.uuid'))
    driver_type = Column(Enum(DriverTypeEnum))