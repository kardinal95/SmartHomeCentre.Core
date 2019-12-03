import uuid

from flask_restful import Resource, abort

from py.api.client.models.device import DeviceDTO, DeviceExtendedDTO
from py.api.client.models.room import RoomDTO
from py.api.client.operations.devices import *
from py.api.client.operations.rooms import *


class Rooms(Resource):
    def get(self):
        rooms = get_all_rooms()

        if rooms is None:
            return []
        return [RoomDTO(x).as_json() for x in rooms]


class RoomDevices(Resource):
    def get(self, room_uuid):
        devices = None
        try:
            devices = get_room_devices(uuid.UUID(room_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if devices is None:
            abort(404, message='Room with uuid {} does not exist'.format(room_uuid))
        return [DeviceDTO(x).as_json() for x in devices]


class RoomDevicesExtended(Resource):
    def get(self, room_uuid):
        data = None
        try:
            data = get_room_devices_extended(uuid.UUID(room_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if data is None:
            abort(404, message='Room with uuid {} does not exist'.format(room_uuid))

        devices = list()
        for device, endpoints in data:
            device_dto = DeviceExtendedDTO(device)
            device_dto.add_endpoints([EndpointDTO(x[0], x[1], x[2], False, x[3]) for x in endpoints])
            devices.append(device_dto)
        return [x.as_json() for x in devices]


class RoomDevicesExtended(Resource):
    def get(self, room_uuid):
        data = None
        try:
            data = get_room_devices_extended(uuid.UUID(room_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if data is None:
            abort(404, message='Room with uuid {} does not exist'.format(room_uuid))

        devices = list()
        for device, endpoints in data:
            device_dto = DeviceExtendedDTO(device)
            device_dto.add_endpoints([EndpointDTO(x[0], x[1], x[2], False, x[3]) for x in endpoints])
            devices.append(device_dto)
        return [x.as_json() for x in devices]
