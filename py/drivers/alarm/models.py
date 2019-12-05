import enum

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from py.models import DatabaseModel


class AlarmSeverityEnum(enum.Enum):
    CRITICAL = enum.auto(),
    ERROR = enum.auto(),
    WARNING = enum.auto(),
    INFO = enum.auto()


class AlarmParamsMdl(DatabaseModel):
    __tablename__ = 'alarm_params'
    severity = Column(Enum(AlarmSeverityEnum))
    ep_uuid = Column(UUID(as_uuid=True), ForeignKey('endpoints.uuid'))
    name = Column(String(64))
    comment = Column(String(256), nullable=True)
