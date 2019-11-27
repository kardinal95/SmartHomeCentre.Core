from py.drivers.base import BaseDriver


class InterfaceDriver(BaseDriver):
    def process_data_to_ep(self, ep_uuid, parameters):
        pass

    def add_ep(self, endpoint, parameters):
        pass

    def delete_ep(self, endpoint, parameters):
        pass

    def destroy(self):
        pass

    def __init__(self, uuid):
        self.uuid = uuid
