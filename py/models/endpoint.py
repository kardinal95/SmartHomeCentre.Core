from abc import abstractmethod

from loguru import logger
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from py.main.db import DatabaseObjects as do
from py.models import ModelBase
from py.models.scenario import Scenario
from py.models.trigger import Trigger


class BaseEndpoint(ModelBase.get_base()):
    __abstract__ = True
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)

    def trigger_update(self):
        logger.debug('Endpoint {} causing trigger update...'.format(self.uuid))

        session = do.session()
        triggers = session.query(Trigger).filter(Trigger.source_uuid == self.uuid).all()
        scenarios_ids = [x.scenario_uuid for x in triggers]
        scenarios = session.query(Scenario).filter(Scenario.uuid.in_(scenarios_ids))
        session.close()

        for item in scenarios:
            item.execute()
        pass

    @abstractmethod
    def modify(self, parameters):
        pass