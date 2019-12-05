from typing import List

from loguru import logger

from py import db_session
from py.drivers import mapping
from py.models.driver_instance import *


class DriverSrv:
    instances = {}

    @db_session
    def __init__(self, session):
        items = session.query(DriverInstanceMdl).all()
        parameters = session.query(DriverParameterMdl).all()

        for item in items:
            self.add_instance(item, parameters)

    def get(self, uuid):
        return self.instances[uuid]

    def add_instance(self, instance: DriverInstanceMdl, params: List[DriverParameterMdl]):
        logger.info('Loading {type} driver with uuid {uuid}',
                    type=instance.driver_type,
                    uuid=instance.uuid)
        required = dict([x.get_as_pair() for x in params if x.driver_uuid == instance.uuid])
        driver = mapping[instance.driver_type](instance.uuid, **required)
        self.instances[instance.uuid] = driver

    def delete_instance(self):
        # TODO Add deletion
        pass
