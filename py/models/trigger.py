from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from py.models import ModelBase


class Trigger(ModelBase.get_base()):
    __tablename__ = 'triggers'
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    source_uuid = Column(UUID(as_uuid=True))
    scenario_uuid = Column(UUID(as_uuid=True), ForeignKey('scenarios.uuid'))