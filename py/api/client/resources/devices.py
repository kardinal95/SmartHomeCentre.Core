import uuid

from flask_restful import Resource, abort

from py.api.client.models.device import *
from py.api.client.operations.devices import *


class Devices(Resource):
    def get(self):
        devices = get_devices()

        if devices is None:
            return []
        return [DeviceDTO(x).as_json() for x in devices]


class Device(Resource):
    def get(self, device_uuid):
        device = None
        try:
            device = get_device(uuid.UUID(device_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if device is None:
            abort(404, message='Device with uuid {} does not exist'.format(device_uuid))
        return DeviceDTO(device).as_json()


class DeviceExtended(Resource):
    def get(self, device_uuid):
        device = None
        endpoints = None
        try:
            device, endpoints = get_device_extended(uuid.UUID(device_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if device is None:
            abort(404, message='Device with uuid {} does not exist'.format(device_uuid))

        device_dto = DeviceExtendedDTO(device)
        device_dto.add_endpoints([EndpointDTO(x[0], x[1], x[2], False, x[3]) for x in endpoints])
        return device_dto.as_json()


class DeviceEndpoints(Resource):
    def get(self, device_uuid):
        endpoints = None
        try:
            _, endpoints = get_device_extended(uuid.UUID(device_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if endpoints is None:
            abort(404, message='Device with uuid {} does not exist'.format(device_uuid))

        return [EndpointDTO(x[0], x[1], x[2], False, x[3]).as_json() for x in endpoints]


class DeviceEndpoint(Resource):
    def get(self, device_uuid, endpoint_uuid):
        endpoint = None
        try:
            endpoint = get_device_endpoint(uuid.UUID(device_uuid), uuid.UUID(endpoint_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if endpoint is None:
            abort(404, message='Device with uuid {} does not exist'.format(device_uuid))

        return EndpointDTO(endpoint[0], endpoint[1], endpoint[2], False, endpoint[3]).as_json()


class DeviceEndpointState(Resource):
    def patch(self):
        pass

    def get(self, device_uuid, endpoint_uuid):
        endpoint = None
        try:
            endpoint = get_device_endpoint(uuid.UUID(device_uuid), uuid.UUID(endpoint_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if endpoint is None:
            abort(404, message='Device with uuid {} does not exist'.format(device_uuid))

        return endpoint[3]