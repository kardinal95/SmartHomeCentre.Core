from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from py.drivers.mqtt.driver import MqttDriver
from py.models import ModelBase

mapping = {
    'mqtt': MqttDriver,
    'virtual': None
}


class DriverInstance(ModelBase.get_base()):
    __tablename__ = 'driver_instances'
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    driver = Column(Enum(*mapping.keys(), name='driver_enum'))
    parameters = Column(String(256), nullable=True)