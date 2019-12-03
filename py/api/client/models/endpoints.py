from py.drivers.interface.models import InterfaceEpTypeEnum


class EndpointDTO:
    def __init__(self, uuid, name, if_type: InterfaceEpTypeEnum, writable, params: dict):
        self.uuid = uuid
        self.name = name
        self.if_type = if_type
        self.params = params
        self.writable = writable

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name,
            'type': self.if_type.value,
            'writable': self.writable,
            'state': self.params
        }
