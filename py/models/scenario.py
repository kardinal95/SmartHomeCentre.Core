from sqlalchemy import Column, String

from py.models import DatabaseModel


class ScenarioMdl(DatabaseModel):
    __tablename__ = 'scenarios'
    title = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)