from loguru import logger


class MainHub:
    services = dict()

    @staticmethod
    def register(srv: object, srv_class: type) -> None:
        if srv_class in MainHub.services.keys():
            raise Exception('Already registered such a service!')
        MainHub.services[srv_class] = srv
        logger.info('Service {} registered'.format(srv_class.__name__))

    @staticmethod
    def deregister(srv_class: type) -> None:
        if srv_class not in MainHub.services.keys():
            raise Exception('No registered service of such class found!')
        del(MainHub.services[srv_class])
        logger.info('Service {} deregistered'.format(srv_class.__name__))

    @staticmethod
    def retrieve(srv_class: type):
        if srv_class in MainHub.services.keys():
            return MainHub.services[srv_class]
        return None
