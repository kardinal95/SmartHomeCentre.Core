from sqlalchemy import *

from py.models import DatabaseModel


class SetPointMdl(DatabaseModel):
    __tablename__ = 'setpoints'
    name = Column(String(64), nullable=True)
    value = Column(String(128), nullable=False)
    type = Column(String(64), nullable=False)