from typing import List

from py.api.client.models.endpoints import EndpointDTO
from py.models.device import DeviceMdl


class DeviceDTO:
    def __init__(self, device: DeviceMdl):
        self.uuid = device.uuid
        self.name = device.name

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': str(self.name)
        }


class DeviceExtendedDTO(DeviceDTO):
    def __init__(self, device: DeviceMdl):
        super().__init__(device)
        self.endpoints = list()

    def add_endpoints(self, endpoints: List[EndpointDTO]):
        self.endpoints += endpoints

    def as_json(self):
        return {
            'uuid': str(self.uuid),
            'name': str(self.name),
            'endpoints': [x.as_json() for x in self.endpoints]
        }