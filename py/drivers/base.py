from abc import abstractmethod


class BaseDriver:
    @abstractmethod
    def add_ep(self, endpoint, parameters):
        pass

    @abstractmethod
    def delete_ep(self, endpoint, parameters):
        pass

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def process_data_to_ep(self, ep_uuid, parameters):
        pass