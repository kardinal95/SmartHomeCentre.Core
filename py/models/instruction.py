from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from py.models import DatabaseModel


class InstructionMdl(DatabaseModel):
    __tablename__ = 'instructions'
    order = Column(Integer, nullable=False)
    scenario_uuid = Column(UUID(as_uuid=True), ForeignKey('scenarios.uuid'))
    source_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'), nullable=True)
    source_parameter = Column(String(64), nullable=True)
    target_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'), nullable=False)
    target_parameter = Column(String(64), nullable=False)
    setpoint_uuid = Column(UUID(as_uuid=True), ForeignKey('setpoints.uuid'), nullable=True)
