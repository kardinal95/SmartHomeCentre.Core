import re
from pydoc import locate

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.orm import relationship

from py.models import DatabaseModel


class MqttParamsMdl(DatabaseModel):
    __tablename__ = 'mqtt_params'
    ep_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    type_uuid = Column(UUID(as_uuid=True), ForeignKey('mqtt_types.uuid'))
    topic_read = Column(String(128), nullable=False)
    topic_write = Column(String(128), nullable=True)


class MqttEpTypeMdl(DatabaseModel):
    __tablename__ = 'mqtt_types'
    read_template = Column(String(256), nullable=False)
    write_template = Column(String(256), nullable=True)
    comment = Column(String(64), nullable=True)
    parameters = Column(JSON(256))
    mqtt_params = relationship('MqttParamsMdl')

    def fix_types(self, inp: dict):
        type_dict = {x: locate(self.parameters[x]) for x in self.parameters}
        return {str(x): type_dict[str(x)](y) for x, y in inp.items()}

    def as_dict(self, payload):
        regex = self.read_template
        matches = re.search(regex, str(payload))

        return self.fix_types(matches.groupdict())