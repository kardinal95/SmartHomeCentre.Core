import json

from loguru import logger

from py.main.db import DatabaseObjects as do
from py.models.instruction import InstructionType


def set_ep_value(parameters):
    parsed = json.loads(parameters)

    session = do.session()
    endpoint = None
    if parsed['type'] == 'mqtt':
        from py.drivers.mqtt.endpoint import MqttEndpoint
        endpoint = session.query(MqttEndpoint).filter(MqttEndpoint.uuid == parsed['target']).first()
        endpoint.modify(parsed['parameters'])


class InstructionExecutor:
    mapping = {
        "EP_SET_VALUE": set_ep_value
    }
    types = None

    @staticmethod
    def process(instructions):
        if InstructionExecutor.types is None:
            session = do.session()
            InstructionExecutor.types = {x.uuid: x.name for x in session.query(InstructionType).all()}
            session.close()

        for item in instructions:
            InstructionExecutor.mapping[InstructionExecutor.types[item.instruction_type_uuid]](item.parameters)
