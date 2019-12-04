import uuid

from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort

from py.api.client.models.device import *
from py.api.client.operations.devices import *


class Devices(Resource):
    @jwt_required
    def get(self):
        devices = get_devices()

        if devices is None:
            return []
        return [DeviceDTO(x).as_json() for x in devices]


class Device(Resource):
    @jwt_required
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
    @jwt_required
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
        device_dto.add_endpoints([EndpointDTO(x[0], x[1], x[2], x[3], x[4]) for x in endpoints])
        return device_dto.as_json()


class DeviceEndpoints(Resource):
    @jwt_required
    def get(self, device_uuid):
        endpoints = None
        try:
            _, endpoints = get_device_extended(uuid.UUID(device_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if endpoints is None:
            abort(404, message='Device with uuid {} does not exist'.format(device_uuid))

        return [EndpointDTO(x[0], x[1], x[2], x[3], x[4]).as_json() for x in endpoints]


class DeviceEndpoint(Resource):
    @jwt_required
    def get(self, device_uuid, endpoint_uuid):
        endpoint = None
        try:
            endpoint = get_device_endpoint(uuid.UUID(device_uuid), uuid.UUID(endpoint_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if endpoint is None:
            abort(404, message='Device with uuid {} does not exist'.format(device_uuid))

        return EndpointDTO(endpoint[0], endpoint[1], endpoint[2], endpoint[3], endpoint[4]).as_json()


class DeviceEndpointState(Resource):
    @jwt_required
    def patch(self, device_uuid, endpoint_uuid):
        endpoint = None
        try:
            endpoint = get_device_endpoint(uuid.UUID(device_uuid), uuid.UUID(endpoint_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if endpoint[3] is False:
            abort(400, message='Not allowed')

        #change_devive_state(args)

    @jwt_required
    def get(self, device_uuid, endpoint_uuid):
        endpoint = None
        try:
            endpoint = get_device_endpoint(uuid.UUID(device_uuid), uuid.UUID(endpoint_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if endpoint is None:
            abort(404, message='Device with uuid {} does not exist'.format(device_uuid))

        return endpoint[4]
