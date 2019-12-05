from typing import List

from loguru import logger

from py import db_session
from py.core import MainHub
from py.core.db import DatabaseSrv
from py.models.condition import ConditionMdl
from py.models.device import DeviceMdl
from py.models.instruction import InstructionMdl
from py.models.scenario import ScenarioMdl
from py.models.setpoint import SetPointMdl


class ExecutorSrv:
    def execute_multi(self, scenarios: List[ScenarioMdl]):
        for item in scenarios:
            self.execute(item)

    @db_session
    def execute(self, scenario: ScenarioMdl, session):
        # TODO Spawn subprocess?
        conditions = session.query(ConditionMdl).filter(ConditionMdl.scenario_uuid == scenario.uuid).all()

        for condition in conditions:
            if not condition.is_met():
                return

        logger.info('Executing scenario "{}"'.format(scenario.title))
        instructions = session.query(InstructionMdl)\
            .filter(InstructionMdl.scenario_uuid == scenario.uuid)\
            .order_by(InstructionMdl.order)\
            .all()

        for instruction in instructions:
            self.execute_instruction(instruction)

    @staticmethod
    @db_session
    def execute_instruction(instruction: InstructionMdl, session):
        target = session.query(DeviceMdl).filter(DeviceMdl.uuid == instruction.target_uuid).first()

        if instruction.setpoint_uuid is None:
            source = session.query(DeviceMdl).filter(DeviceMdl.uuid == instruction.source_uuid).first()
            value = source.get_value_for_parameter(instruction.source_parameter)
        else:
            setpoint = session.query(SetPointMdl).filter(SetPointMdl.uuid == instruction.setpoint_uuid).first()
            value = setpoint.value

        target.set_value_for_parameter(instruction.target_parameter, value)
