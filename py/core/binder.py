from loguru import logger

from py.core import MainHub
from py.core.db import DatabaseSrv
from py.models.device import DeviceParameterBinding
from py.models.scenario import Scenario
from py.models.trigger import TriggerParamMdl, TriggerMdl


class BinderSrv:
    def __init__(self, redis):
        redis.add_watcher(self)
        logger.info('Binder service started')

    def invoke(self, **kwargs):
        device_parameters = self.get_device_parameter(kwargs['name'], kwargs['key'])
        scenarios = self.get_scenarios(device_parameters)
        # TODO Do something with scenarios
        # TODO Pass to interface
        logger.debug('Scenarios found. {}'.format(scenarios))

    def get_device_parameter(self, uuid, key):
        session = MainHub.retrieve(DatabaseSrv).session()
        bindings = session.query(DeviceParameterBinding)\
            .filter(DeviceParameterBinding.endpoint_uuid == uuid)\
            .filter(DeviceParameterBinding.endpoint_parameter == key)\
            .all()
        session.close()

        return [(x.device_uuid, x.device_parameter) for x in bindings]

    def get_scenarios(self, items):
        scenario_uuids = []
        session = MainHub.retrieve(DatabaseSrv).session()

        for item in items:
            param_list = session.query(TriggerParamMdl)\
                .filter(TriggerParamMdl.parameter_name == 'device')\
                .filter(TriggerParamMdl.parameter_value == str(item[0]))\
                .all()
            uuids = [x.trigger_uuid for x in param_list]
            filtered = session.query(TriggerParamMdl)\
                .filter(TriggerParamMdl.parameter_name == 'parameter')\
                .filter(TriggerParamMdl.parameter_value == item[1])\
                .filter(TriggerParamMdl.trigger_uuid.in_(uuids))\
                .all()
            trigger_uuids = [x.trigger_uuid for x in filtered]
            triggers = session.query(TriggerMdl).filter(TriggerMdl.uuid.in_(trigger_uuids)).all()
            scenario_uuids += [x.scenario_uuid for x in triggers]

        scenarios = session.query(Scenario).filter(Scenario.uuid.in_(scenario_uuids)).all()
        session.close()

        return scenarios