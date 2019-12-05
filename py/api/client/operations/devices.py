from flask_jwt_extended import get_jwt_identity

from py import db_session
from py.api.client.operations.rooms import get_room
from py.drivers.interface.converters import convert
from py.models.device import DeviceMdl
from py.models.endpoint import EndpointMdl
from py.models.room import DeviceRoomBinding
from py.api.exceptions import IncorrectTargetException
from py.models.user import UserMdl


@db_session
def get_room_devices(uuid, session):
    get_room(uuid=uuid, session=session)
    return DeviceRoomBinding.get_devices_by_room_uuid(uuid=uuid, session=session)


@db_session
def get_room_devices_extended(uuid, session):
    devices = get_room_devices(uuid=uuid, session=session)
    return {x: get_device_endpoints_full(x.uuid) for x in devices}


@db_session
def get_devices(session):
    return DeviceMdl.get_all_devices(session=session)


@db_session
def get_device(uuid, session):
    device = DeviceMdl.get_device_with_uuid(uuid=uuid, session=session)
    if device is None:
        raise IncorrectTargetException(uuid, DeviceMdl)
    return device


@db_session
def get_device_endpoints_full(uuid, session):
    device = get_device(uuid=uuid, session=session)
    acl = UserMdl.get_user_with_username(username=get_jwt_identity(), session=session).acl

    values = device.get_all_values()
    result = dict()
    for item in device.iface_binds:
        ep = item.ep
        param = ep.iface_param
        if param.read_acl > acl:
            continue
        if ep.uuid not in result.keys():
            result[ep.uuid] = dict()
            result[ep.uuid]['values'] = dict()
            result[ep.uuid]['name'] = ep.name
            result[ep.uuid]['type'] = param.type
            result[ep.uuid]['writable'] = acl >= param.write_acl
        result[ep.uuid]['values'][item.ep_parameter] = values[item.device_parameter]

    for item in result.keys():
        result[item]['values'] = convert(result[item]['type'], 'encode', result[item]['values'])

    return result


@db_session
def get_device_endpoint(device_uuid, endpoint_uuid, session):
    device = get_device(uuid=device_uuid, session=session)
    acl = UserMdl.get_user_with_username(username=get_jwt_identity(), session=session).acl

    endpoint = EndpointMdl.get_endpoint_by_uuid(uuid=endpoint_uuid, session=session)
    binds = [x for x in device.iface_binds if x.ep_uuid == endpoint.uuid]
    params = endpoint.iface_param
    values = {x.ep_parameter: device.get_value_for_parameter(x.device_parameter) for x in binds}

    if endpoint.iface_param.read_acl > acl:
        return None

    return {
        'uuid': endpoint.uuid,
        'name': endpoint.name,
        'type': params.type,
        'writable': acl >= params.write_acl,
        'values': convert(params.type, 'encode', values)
    }
