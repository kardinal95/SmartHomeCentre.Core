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