from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from py import db_session
from py.core import MainHub
from py.core.redis import RedisSrv
from py.drivers.service import DriverSrv
from py.models import DatabaseModel


class DeviceParameterBinding(DatabaseModel):
    __tablename__ = 'device_parameter_bindings'
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    device_parameter = Column(String(64), nullable=False)
    endpoint_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    endpoint_parameter = Column(String(64), nullable=False)
    ep = relationship('EndpointMdl', uselist=False)


class DeviceMdl(DatabaseModel):
    __tablename__ = 'devices'
    name = Column(String(128), nullable=False)
    binds = relationship('DeviceParameterBinding')

    @classmethod
    @db_session
    def get_all_devices(cls, session):
        return session.query(cls).all()

    @classmethod
    @db_session
    def get_device_with_uuid(cls, uuid, session):
        return session.query(cls).filter(cls.uuid == uuid).first()

    def get_all_values(self):
        redis = MainHub.retrieve(RedisSrv)
        return {x.device_parameter: redis.hget(str(x.endpoint_uuid), x.endpoint_parameter) for x in self.binds}

    def get_value_for_parameter(self, name):
        bind = [x for x in self.binds if x.device_parameter == name][0]
        return MainHub.retrieve(RedisSrv).hget(str(bind.endpoint_uuid), bind.endpoint_parameter)

    def get_values_for_parameters(self, names):
        binds = [x for x in self.binds if x.device_parameter in names]
        rsrv = MainHub.retrieve(RedisSrv)
        return {x.device_parameter: rsrv.hget(str(x.endpoint_uuid), x.endpoint_parameter) for x in binds}

    def set_value_for_parameter(self, name, value):
        bind = [x for x in self.binds if x.device_parameter == name][0]
        driver = MainHub.retrieve(DriverSrv).get(bind.ep.driver_uuid)
        driver.process_data_to_ep(bind.ep.uuid, {bind.endpoint_parameter: value})