from py import db_session
from py.core import MainHub
from py.core.notifications import NotificationSrv, NotificationSeverityEnum
from py.core.redis import RedisSrv
from py.drivers.alarm.models import AlarmParamsMdl, AlarmSeverityEnum
from py.drivers.base import BaseDriver


severity_map = {
    AlarmSeverityEnum.CRITICAL: NotificationSeverityEnum.CRITICAL,
    AlarmSeverityEnum.WARNING: NotificationSeverityEnum.WARNING,
    AlarmSeverityEnum.ERROR: NotificationSeverityEnum.ERROR,
    AlarmSeverityEnum.INFO: NotificationSeverityEnum.INFO
}


class AlarmDriver(BaseDriver):
    @db_session
    def process_data_to_ep(self, ep_uuid, parameters, session):
        # TODO Error processing
        # TODO Check if the same value?
        MainHub.retrieve(RedisSrv).hset(str(ep_uuid), 'alarm', parameters['alarm'])

        if bool(parameters['alarm']) is True:
            params = session.query(AlarmParamsMdl).filter(AlarmParamsMdl.ep_uuid == ep_uuid).first()

            MainHub.retrieve(NotificationSrv).send(title=params.name,
                                                   comment=params.comment,
                                                   severity=severity_map[params.severity],
                                                   ep_uuid=ep_uuid)
        # TODO Make calls to notification service?

    def add_ep(self, endpoint, parameters):
        pass

    def delete_ep(self, endpoint, parameters):
        pass

    def destroy(self):
        pass

    def __init__(self, uuid):
        self.uuid = uuid
