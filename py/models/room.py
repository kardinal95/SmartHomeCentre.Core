from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from py.core import MainHub
from py.core.db import DatabaseSrv
from py.models import DatabaseModel
from py.models.device import DeviceMdl


class DeviceRoomBinding(DatabaseModel):
    __tablename__ = 'device_room_binds'
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'))
    room_uuid = Column(UUID(as_uuid=True), ForeignKey('rooms.uuid'))


class RoomMdl(DatabaseModel):
    __tablename__ = 'rooms'
    name = Column(String(64), nullable=False)
    # TODO Modes/States?

    def get_devices(self):
        session = MainHub.retrieve(DatabaseSrv).session()
        binds = session.query(DeviceRoomBinding).filter(DeviceRoomBinding.room_uuid == self.uuid).all()
        binds_ids = [x.device_uuid for x in binds]
        devices = session.query(DeviceMdl).filter(DeviceMdl.uuid.in_(binds_ids)).all()
        session.close()

        return devices
