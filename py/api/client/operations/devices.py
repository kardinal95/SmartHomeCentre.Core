from itertools import groupby

from flask_jwt_extended import get_jwt_identity

from py.api.client.operations.rooms import get_room
from py.api.client.operations.users import get_user_acl
from py.core import MainHub
from py.core.db import DatabaseSrv
from py.drivers.interface.converters import convert
from py.drivers.interface.models import InterfaceBindingMdl, InterfaceParamsMdl
from py.models.device import DeviceMdl
from py.models.endpoint import EndpointMdl


def get_room_devices(room_uuid):
    room = get_room(room_uuid)
    if room is None:
        return None
    devices = room.get_devices()

    return devices


def get_room_devices_extended(room_uuid):
    # TODO Filter ACL?

    room = get_room(room_uuid)
    if room is None:
        return None
    devices = room.get_devices()
    result = list()
    for item in devices:
        result.append(get_device_extended(item.uuid))

    return result


def get_devices():
    session = MainHub.retrieve(DatabaseSrv).session()
    devices = session.query(DeviceMdl).all()
    session.close()

    return devices


def get_device(device_uuid):
    session = MainHub.retrieve(DatabaseSrv).session()
    device = session.query(DeviceMdl).filter(DeviceMdl.uuid == device_uuid).first()
    session.close()

    return device


def get_device_extended(device_uuid):
    device = get_device(device_uuid)
    acl = get_user_acl(get_jwt_identity())

    session = MainHub.retrieve(DatabaseSrv).session()
    objs = session.query(InterfaceBindingMdl, EndpointMdl, InterfaceParamsMdl)\
        .filter(InterfaceBindingMdl.device_uuid == device_uuid)\
        .filter(InterfaceParamsMdl.read_acl <= acl)\
        .join(EndpointMdl, InterfaceBindingMdl.ep_uuid == EndpointMdl.uuid)\
        .join(InterfaceParamsMdl, InterfaceParamsMdl.ep_uuid == EndpointMdl.uuid)\
        .all()
    session.close()

    # TODO Rework this part. Maybe shift something to functions in models?
    endpoints = list()
    data = list()
    for item in objs:
        data.append((item[1].uuid, item[1].name, item[2].type, item[2].write_acl <= acl, item[0].ep_parameter, item[0].device_parameter))
    data = groupby(data, lambda x: [x[0], x[1], x[2], x[3]])
    for key, group in data:
        params_dev = list()
        mapping = dict()
        for item in group:
            params_dev.append(item[5])
            mapping[item[5]] = item[4]
        values = device.get_values_for_parameters(params_dev)
        params_ep = {mapping[x]: y for x, y in values.items()}
        converted = convert(key[2], 'encode', params_ep)

        endpoints.append((key[0], key[1], key[2], key[3], converted))

    return device, endpoints


def get_device_endpoint(device_uuid, endpoint_uuid):
    device = get_device(device_uuid)
    acl = get_user_acl(get_jwt_identity())

    session = MainHub.retrieve(DatabaseSrv).session()
    objs = session.query(InterfaceBindingMdl, EndpointMdl, InterfaceParamsMdl)\
        .filter(InterfaceBindingMdl.device_uuid == device_uuid)\
        .filter(EndpointMdl.uuid == endpoint_uuid)\
        .filter(InterfaceParamsMdl.read_acl <= acl)\
        .join(EndpointMdl, InterfaceBindingMdl.ep_uuid == EndpointMdl.uuid).\
        join(InterfaceParamsMdl, InterfaceParamsMdl.ep_uuid == EndpointMdl.uuid)\
        .all()
    session.close()

    # TODO Rework this part. Maybe shift something to functions in models?
    endpoints = list()
    data = list()
    for item in objs:
        data.append((item[1].uuid, item[1].name, item[2].type, item[2].write_acl <= acl, item[0].ep_parameter, item[0].device_parameter))
    data = groupby(data, lambda x: [x[0], x[1], x[2], x[3]])
    for key, group in data:
        params_dev = list()
        mapping = dict()
        for item in group:
            params_dev.append(item[5])
            mapping[item[5]] = item[4]
        values = device.get_values_for_parameters(params_dev)
        params_ep = {mapping[x]: y for x, y in values.items()}
        converted = convert(key[2], 'encode', params_ep)

        endpoints.append((key[0], key[1], key[2], key[3], converted))

    return endpoints[0]
