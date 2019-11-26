from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from py.models import ModelBase


#class InstructionType(ModelBase.get_base()):
#    __tablename__ = 'instruction_types'
#    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
#    name = Column(String(64), nullable=False)
