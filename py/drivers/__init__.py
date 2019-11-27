import enum

from py.drivers.alarm.driver import AlarmDriver
from py.drivers.interface.driver import InterfaceDriver
from py.drivers.mqtt.driver import MqttDriver


class DriverTypeEnum(enum.Enum):
    mqtt = enum.auto(),
    iface = enum.auto(),
    alarm = enum.auto()


mapping = {
    DriverTypeEnum.mqtt: MqttDriver,
    DriverTypeEnum.iface: InterfaceDriver,
    DriverTypeEnum.alarm: AlarmDriver
}
