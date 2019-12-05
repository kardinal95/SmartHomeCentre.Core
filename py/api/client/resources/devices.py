import uuid

from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort

from py.api.exceptions import abort_on_exc
from py.api.client.models.device import *
from py.api.client.operations.devices import *


class Devices(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, session):
        devices = get_devices(session=session)

        if devices is None:
            return []
        return [DeviceDTO(x).as_json() for x in devices]


class Device(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, device_uuid, session):
        return DeviceDTO(get_device(uuid=uuid.UUID(device_uuid), session=session)).as_json()


class DeviceExtended(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, device_uuid, session):
        device = DeviceExtendedDTO(get_device(uuid=uuid.UUID(device_uuid), session=session))
        endpoints = get_device_endpoints_full(uuid=device_uuid, session=session)
        device.add_endpoints([EndpointDTO(uuid=x,
                                          name=endpoints[x]['name'],
                                          if_type=endpoints[x]['type'],
                                          writable=endpoints[x]['writable'],
                                          values=endpoints[x]['values']) for x in endpoints.keys()])
        return device.as_json()


class DeviceEndpoints(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, device_uuid, session):
        endpoints = get_device_endpoints_full(uuid=device_uuid, session=session)
        return [EndpointDTO(uuid=x,
                            name=endpoints[x]['name'],
                            if_type=endpoints[x]['type'],
                            writable=endpoints[x]['writable'],
                            values=endpoints[x]['values']).as_json() for x in endpoints.keys()]


class DeviceEndpoint(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, device_uuid, endpoint_uuid, session):
        ep = get_device_endpoint(device_uuid=device_uuid,
                                 endpoint_uuid=endpoint_uuid,
                                 session=session)
        return EndpointDTO(uuid=ep['uuid'],
                           name=ep['name'],
                           if_type=ep['type'],
                           writable=ep['writable'],
                           values=ep['values']).as_json()


class DeviceEndpointState(Resource):
    @abort_on_exc
    @jwt_required
    @db_session
    def patch(self, device_uuid, endpoint_uuid):
        endpoint = None
        try:
            endpoint = get_device_endpoint(uuid.UUID(device_uuid), uuid.UUID(endpoint_uuid))
        except ValueError:
            abort(400, message='Badly formatted UUID')

        if endpoint[3] is False:
            abort(400, message='Not allowed')

        #change_devive_state(args)

    @abort_on_exc
    @jwt_required
    @db_session
    def get(self, device_uuid, endpoint_uuid, session):
        endpoint = get_device_endpoint(device_uuid=uuid.UUID(device_uuid),
                                       endpoint_uuid=uuid.UUID(endpoint_uuid),
                                       session=session)
        return endpoint['values']