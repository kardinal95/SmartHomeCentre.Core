from loguru import logger

from py.core import MainHub
from py.core.db import DatabaseSrv
from py.core.executor import ExecutorSrv
from py.models.device import DeviceParameterBinding
from py.models.scenario import ScenarioMdl
from py.models.trigger import TriggerParamMdl, TriggerMdl


class TriggerService:
    def __init__(self, redis):
        redis.add_watcher(self)

    def invoke(self, **kwargs):
        device_parameters = self.get_device_parameter_pairs(kwargs['name'], kwargs['key'])
        scenarios = self.get_scenarios(device_parameters)
        # TODO Pass to interface
        logger.debug('Found {} scenarios.'.format(len(scenarios)))
        MainHub.retrieve(ExecutorSrv).execute_multi(scenarios)

    @staticmethod
    def get_device_parameter_pairs(uuid, key):
        session = MainHub.retrieve(DatabaseSrv).session()
        bindings = session.query(DeviceParameterBinding)\
            .filter(DeviceParameterBinding.endpoint_uuid == uuid)\
            .filter(DeviceParameterBinding.endpoint_parameter == key)\
            .all()
        session.close()

        return [(x.device_uuid, x.device_parameter) for x in bindings]

    @staticmethod
    def get_scenarios(items):
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

        scenarios = session.query(ScenarioMdl).filter(ScenarioMdl.uuid.in_(scenario_uuids)).all()
        session.close()

        return scenarios
