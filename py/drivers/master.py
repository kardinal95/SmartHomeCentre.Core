from loguru import logger

from py.models.driver_instance import DriverInstance, mapping
from py.main.db import DatabaseObjects as do


class DriverMaster:
    instances = list()

    def __init__(self):
        session = do.session()
        # TODO Error handling
        for item in session.query(DriverInstance).all():
            logger.info('Loading {type} driver with uuid {uuid}', type=item.driver, uuid=item.uuid)
            self.instances.append(mapping[item.driver](item.uuid, item.parameters))