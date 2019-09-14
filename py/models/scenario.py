from loguru import logger
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from py.main.db import DatabaseObjects as do
from py.main.executor import InstructionExecutor
from py.models import ModelBase


class ScenarioInstruction(ModelBase.get_base()):
    __tablename__ = 'scenario_instructions'
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    seq_number = Column(Integer, nullable=False)
    scenario_uuid = Column(UUID(as_uuid=True), ForeignKey('scenarios.uuid'))
    instruction_type_uuid = Column(UUID(as_uuid=True), ForeignKey('instruction_types.uuid'))
    parameters = Column(String(256))


class Scenario(ModelBase.get_base()):
    __tablename__ = 'scenarios'
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    title = Column(String(128), nullable=True)
    description = Column(String(256), nullable=True)
    instructions = relationship("ScenarioInstruction")
    triggers = relationship("Trigger")

    def execute(self):
        logger.debug('Executing scenario {}'.format(self.title))

        session = do.session()
        inst = session.query(ScenarioInstruction).filter(ScenarioInstruction.scenario_uuid == self.uuid).all()
        session.close()

        InstructionExecutor.process(inst)