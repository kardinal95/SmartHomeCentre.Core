import uuid

from flask_jwt_extended import jwt_required
from flask_restful import Resource

from py.api import EndpointDTO
from py.api.client.models.device import DeviceDTO, DeviceExtendedDTO
from py.api.client.models.room import RoomDTO
from py.api.client.operations.devices import *
from py.api.client.operations.rooms import *
from py.api.exceptions import abort_on_exc


class Rooms(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, session):
        rooms = get_all_rooms(session=session)

        return [RoomDTO(x).as_json() for x in rooms]


class RoomDevices(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, room_uuid, session):
        devices = get_room_devices(uuid=uuid.UUID(room_uuid), session=session)

        return [DeviceDTO(x).as_json() for x in devices]


class RoomDevicesExtended(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, room_uuid, session):
        data = get_room_devices_extended(uuid=uuid.UUID(room_uuid), session=session)

        devices = list()
        for item in data.keys():
            device_dto = DeviceExtendedDTO(item)
            device_dto.add_endpoints([EndpointDTO(uuid=x,
                                                  name=data[item][x]['name'],
                                                  if_type=data[item][x]['type'],
                                                  writable=data[item][x]['writable'],
                                                  values=data[item][x]['values']) for x in data[item].keys()])
            devices.append(device_dto)
        return [x.as_json() for x in devices]
