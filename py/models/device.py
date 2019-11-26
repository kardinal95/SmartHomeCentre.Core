from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from py.core import MainHub
from py.core.db import DatabaseSrv
from py.core.redis import RedisSrv
from py.drivers.service import DriverSrv
from py.models import DatabaseModel
from py.models.endpoint import EndpointMdl


class DeviceParameterBinding(DatabaseModel):
    __tablename__ = 'device_parameter_bindings'
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    device_parameter = Column(String(64), nullable=False)
    endpoint_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    endpoint_parameter = Column(String(64), nullable=False)
    # TODO Writable state, ACL


class DeviceMdl(DatabaseModel):
    __tablename__ = 'devices'
    name = Column(String(128), nullable=False)

    def get_value_for_parameter(self, name):
        session = MainHub.retrieve(DatabaseSrv).session()
        binding = session.query(DeviceParameterBinding)\
            .filter(DeviceParameterBinding.device_uuid == self.uuid)\
            .filter(DeviceParameterBinding.device_parameter == name)\
            .first()
        value = MainHub.retrieve(RedisSrv).hget(str(binding.endpoint_uuid), binding.endpoint_parameter)
        session.close()
        # TODO Exception on non-existent parameters

        return value

    def set_value_for_parameter(self, parameter, value):
        session = MainHub.retrieve(DatabaseSrv).session()
        binding = session.query(DeviceParameterBinding)\
            .filter(DeviceParameterBinding.device_uuid == self.uuid)\
            .filter(DeviceParameterBinding.device_parameter == parameter)\
            .first()
        ep = session.query(EndpointMdl).filter(EndpointMdl.uuid == binding.endpoint_uuid).first()
        session.close()

        MainHub.retrieve(DriverSrv).instances[ep.driver_uuid].process_data_to_ep(ep.uuid, {binding.endpoint_parameter: value})