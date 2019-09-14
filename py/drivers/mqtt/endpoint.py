import json
import re
from pydoc import locate

from loguru import logger
from sqlalchemy import Column, Boolean, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from py.drivers import instances
from py.drivers.mqtt import storage
from py.main.db import DatabaseObjects as do
from py.models import ModelBase
from py.models.endpoint import BaseEndpoint


class MqttParameterPattern(ModelBase.get_base()):
    __tablename__ = 'mqtt_patterns'
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    regex = Column(String(256), nullable=False)
    typing = Column(String(256), nullable=False)
    children = relationship('MqttEndpoint')
    type_dict = None

    def make_types(self):
        self.type_dict = json.loads(self.typing)
        # Replace with types
        self.type_dict = {x: locate(self.type_dict[x]) for x in self.type_dict.keys()}


class MqttEndpoint(BaseEndpoint):
    __tablename__ = 'mqtt_endpoints'
    parent_uuid = Column(UUID(as_uuid=True), ForeignKey('driver_instances.uuid'))
    retain = Column(Boolean, nullable=False)
    connection_string = Column(String(128), nullable=False)
    connection_on_string = Column(String(128), nullable=True)
    name = Column(String(256), nullable=True)
    type_uuid = Column(UUID(as_uuid=True), ForeignKey('mqtt_patterns.uuid'))

    def update_values(self, inp):
        session = do.session()
        pattern = session.query(MqttParameterPattern).filter(MqttParameterPattern.uuid == self.type_uuid).first()
        session.close()

        regex = pattern.regex
        matches = re.search(regex, str(inp))

        pattern.make_types()
        #TODO Consider errors on incorrect db values
        for pair in matches.groupdict().items():
            if not storage.update_parameter(self.uuid, pair):
                return
            logger.debug('New value for {}: {} = {}'.format(self.name, pair[0], pair[1]))

        self.trigger_update()

    def modify(self, parameters):
        logger.debug(parameters.items())
        for pair in parameters.items():
            storage.update_parameter(self.uuid, pair)
        temp = '{p[value]}' #TODO Replace from DB
        instances[self.parent_uuid].publish(self.connection_on_string, temp.format(p=parameters))
        logger.debug(parameters)
