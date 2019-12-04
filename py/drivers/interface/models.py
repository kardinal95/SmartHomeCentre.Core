import enum

from sqlalchemy import Column, ForeignKey, Enum, String, Integer
from sqlalchemy.dialects.postgresql import UUID

from py.models import DatabaseModel


class InterfaceEpTypeEnum(enum.Enum):
    switch = enum.auto()
    rgb = enum.auto()
    display = enum.auto()


class InterfaceParamsMdl(DatabaseModel):
    __tablename__ = 'interface_params'
    ep_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    type = Column(Enum(InterfaceEpTypeEnum))
    write_acl = Column(Integer, server_default='999')
    read_acl = Column(Integer, server_default='1')
    # TODO Read/Write ACL?


class InterfaceBindingMdl(DatabaseModel):
    __tablename__ = 'interface_bindings'
    ep_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    ep_parameter = Column(String(64), nullable=False)
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    device_parameter = Column(String(64), nullable=False)