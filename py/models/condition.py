import enum
from pydoc import locate

from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID

from py.core import MainHub
from py.core.db import DatabaseSrv
from py.models import DatabaseModel
from py.models.device import DeviceParameterBinding, DeviceMdl
from py.models.setpoint import SetPointMdl


class ConditionTypeEnum(enum.Enum):
    IsEqual = enum.auto(),
    IsMore = enum.auto(),
    IsLess = enum.auto(),
    NotEqual = enum.auto(),
    InMode = enum.auto(),
    NotInMode = enum.auto()


class ConditionMdl(DatabaseModel):
    __tablename__ = 'conditions'
    comment = Column(String(128), nullable=False)
    scenario_uuid = Column(UUID(as_uuid=True), ForeignKey('scenarios.uuid'))
    condition_type = Column(Enum(ConditionTypeEnum))
    target_uuid = Column(UUID(as_uuid=True))
    target_parameter_name = Column(String(64), nullable=False)
    setpoint_uuid = Column(UUID(as_uuid=True), ForeignKey('setpoints.uuid'))

    value_types = [ConditionTypeEnum.IsEqual,
                   ConditionTypeEnum.IsLess,
                   ConditionTypeEnum.IsMore,
                   ConditionTypeEnum.NotEqual]

    def is_met(self):
        if self.condition_type in self.value_types:
            session = MainHub.retrieve(DatabaseSrv).session()
            target = session.query(DeviceMdl).filter(DeviceMdl.uuid == self.target_uuid).first()
            setpoint = session.query(SetPointMdl).filter(SetPointMdl.uuid == self.setpoint_uuid).first()
            session.close()

            value = target.get_value_for_parameter(self.target_parameter_name)
            # TODO Make type fixing better
            value = locate(setpoint.type)(value)
            setpoint_value = locate(setpoint.type)(setpoint.value)
            if self.condition_type == ConditionTypeEnum.IsEqual:
                return value == setpoint_value
            if self.condition_type == ConditionTypeEnum.IsMore:
                return value > setpoint_value
            if self.condition_type == ConditionTypeEnum.IsLess:
                return value < setpoint_value
            if self.condition_type == ConditionTypeEnum.NotEqual:
                return value != setpoint_value
