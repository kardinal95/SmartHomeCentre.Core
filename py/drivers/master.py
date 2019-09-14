from loguru import logger

from py.drivers import instances
from py.main.db import DatabaseObjects as do
from py.models.driver_instance import DriverInstance, mapping


class DriverMaster:
    def __init__(self):
        session = do.session()
        # TODO Error handling
        for item in session.query(DriverInstance).all():
            logger.info('Loading {type} driver with uuid {uuid}', type=item.driver, uuid=item.uuid)
            instances[item.uuid] = mapping[item.driver](item.uuid, item.parameters)