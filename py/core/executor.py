from pydoc import locate
from typing import List

from loguru import logger

from py.core import MainHub
from py.core.db import DatabaseSrv
from py.models.condition import ConditionMdl
from py.models.device import Device
from py.models.instruction import InstructionMdl
from py.models.scenario import Scenario
from py.models.setpoint import SetPointMdl


class ExecutorSrv:
    def __init__(self):
        logger.info('Executor service started')

    def execute_multi(self, scenarios: List[Scenario]):
        for item in scenarios:
            self.execute(item)

    def execute(self, scenario: Scenario):
        session = MainHub.retrieve(DatabaseSrv).session()
        conditions = session.query(ConditionMdl).filter(ConditionMdl.scenario_uuid == scenario.uuid).all()
        session.close()

        for condition in conditions:
            if not condition.is_met():
                return

        logger.info('Executing scenario {}'.format(scenario.title))
        session = MainHub.retrieve(DatabaseSrv).session()
        instructions = session.query(InstructionMdl)\
            .filter(InstructionMdl.scenario_uuid == scenario.uuid)\
            .order_by(InstructionMdl.order)\
            .all()
        session.close()

        for instruction in instructions:
            self.execute_instructions(instruction)

    def execute_instructions(self, instruction: InstructionMdl):
        session = MainHub.retrieve(DatabaseSrv).session()
        target = session.query(Device).filter(Device.uuid == instruction.target_uuid).first()

        if instruction.setpoint_uuid is None:
            source = session.query(Device).filter(Device.uuid == instruction.source_uuid).first()
            value = source.get_value_for_parameter(instruction.source_parameter)
        else:
            setpoint = session.query(SetPointMdl).filter(SetPointMdl.uuid == instruction.setpoint_uuid).first()
            value = setpoint.value
        session.close()

        target.set_value_for_parameter(instruction.target_parameter, value)
