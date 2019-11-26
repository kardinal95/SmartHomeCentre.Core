from pydoc import locate

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from py.drivers import DriverTypeEnum
from py.models import DatabaseModel
from py.models.endpoint import EndpointMdl  # Do not delete!


class DriverInstanceMdl(DatabaseModel):
    __tablename__ = 'driver_instances'
    driver_type = Column(Enum(DriverTypeEnum))
    comment = Column(String(128), nullable=True)
    parameters = relationship("DriverParameterMdl")
    endpoints = relationship("EndpointMdl")


class DriverParameterMdl(DatabaseModel):
    __tablename__ = 'driver_parameters'
    driver_uuid = Column(UUID(as_uuid=True), ForeignKey('driver_instances.uuid'))
    param_name = Column(String(64))
    param_type = Column(String(64))
    param_value = Column(String(64))

    def get_as_pair(self):
        p_type = locate(self.param_type)
        return self.param_name, p_type(self.param_value)
