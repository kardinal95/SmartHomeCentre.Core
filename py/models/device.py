from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from py.models import DatabaseModel


class DeviceParameterBinding(DatabaseModel):
    __tablename__ = 'device_parameter_bindings'
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    device_parameter = Column(String(64), nullable=False)
    endpoint_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    endpoint_parameter = Column(String(64), nullable=False)
    # TODO Writable state, ACL


class Device(DatabaseModel):
    __tablename__ = 'devices'
    name = Column(String(128), nullable=False)