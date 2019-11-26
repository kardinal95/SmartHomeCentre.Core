from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from py.models import DatabaseModel


class DeviceRoomBinding(DatabaseModel):
    __tablename__ = 'device_room_binds'
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    room_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))


class RoomMdl(DatabaseModel):
    __tablename__ = 'rooms'
    name = Column(String(64), nullable=False)
    # TODO Modes/States?