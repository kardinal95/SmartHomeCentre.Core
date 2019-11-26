import enum

from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy.dialects.postgresql import UUID

from py.models import DatabaseModel


class TriggerTypeEnum(enum.Enum):
    ValueChange = enum.auto(),
    Manual = enum.auto()


class TriggerMdl(DatabaseModel):
    __tablename__ = 'triggers'
    comment = Column(String(128), nullable=True)
    scenario_uuid = Column(UUID(as_uuid=True), ForeignKey('scenarios.uuid'))
    trigger_type = Column(Enum(TriggerTypeEnum))


class TriggerParamMdl(DatabaseModel):
    __tablename__ = 'trigger_params'
    trigger_uuid = Column(UUID(as_uuid=True), ForeignKey('triggers.uuid'))
    parameter_name = Column(String(64), nullable=False)
    parameter_value = Column(String(128), nullable=False)
    parameter_type = Column(String(32), nullable=False)
