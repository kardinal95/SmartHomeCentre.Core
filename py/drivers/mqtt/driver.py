from string import Template

import paho.mqtt.client as mqtt
from loguru import logger

from py.core import MainHub
from py.core.db import DatabaseSrv
from py.core.redis import RedisSrv
from py.drivers.base import BaseDriver

from py.drivers.mqtt.models import MqttParamsMdl, MqttEpTypeMdl


class MqttDriver(BaseDriver):
    enum_type = 'mqtt'

    def destroy(self):
        # TODO Complete driver destruction
        pass

    def delete_ep(self, endpoint, parameters):
        # TODO Deletion of endpoints
        pass

    def add_ep(self, endpoint, parameters):
        # TODO Make this load_ep and switch add to actually new eps
        required = None
        for param in parameters:
            if param.ep_uuid == endpoint.uuid:
                required = param
                break

        logger.debug('Subscribing on MQTT device with name {}'.format(endpoint.name))
        self.client.subscribe(required.topic_read)

    def __init__(self, uuid, host, port, timeout=60):
        from py.models.endpoint import EndpointMdl
        self.uuid = uuid
        # TODO Check if parameters exists
        self.client = mqtt.Client()
        self.client.on_message = self.on_message

        # TODO Connection errors
        logger.info('Connecting to mqtt server on {}:{}', host, port)
        self.client.connect(host, port, timeout)
        logger.info('Connected!')

        session = MainHub.retrieve(DatabaseSrv).session()
        mqtt_eps = session.query(EndpointMdl).filter(EndpointMdl.driver_type == MqttDriver.enum_type).all()
        parameters = session.query(MqttParamsMdl).all()
        for item in mqtt_eps:
            self.add_ep(item, parameters)
        session.close()

        self.client.loop_start()

    @staticmethod
    def on_message(client, userdata, msg):
        logger.debug('Received message on {} with data: {}'.format(msg.topic, msg.payload))

        session = MainHub.retrieve(DatabaseSrv).session()
        param = session.query(MqttParamsMdl).filter(MqttParamsMdl.topic_read == msg.topic).first()
        mqtt_type = session.query(MqttEpTypeMdl).filter(MqttEpTypeMdl.uuid == param.type_uuid).first()
        session.close()

        MqttDriver.process_data_from_ep(msg.payload, param.ep_uuid, mqtt_type)

    @staticmethod
    def process_data_from_ep(payload, ep_uuid, mqtt_type):
        parameters = mqtt_type.as_dict(payload)

        changed = list()

        current = MainHub.retrieve(RedisSrv).hgetall(str(ep_uuid))
        current = mqtt_type.fix_types(current)

        for pair in parameters.items():
            if len(current) == 0 or current[pair[0]] != pair[1]:
                MainHub.retrieve(RedisSrv).hset(str(ep_uuid), pair[0], pair[1])
                logger.info('New value for {}: {} = {}'.format(ep_uuid, pair[0], pair[1]))
                changed.append(pair[0])

    def process_data_to_ep(self, ep_uuid, parameters):
        session = MainHub.retrieve(DatabaseSrv).session()
        param = session.query(MqttParamsMdl).filter(MqttParamsMdl.ep_uuid == ep_uuid).first()
        mqtt_type = session.query(MqttEpTypeMdl).filter(MqttEpTypeMdl.uuid == param.type_uuid).first()
        session.close()

        current = MainHub.retrieve(RedisSrv).hgetall(str(ep_uuid))

        for key in current.keys():
            if key in parameters.keys():
                current[key] = str(parameters[key])

        t = Template(mqtt_type.write_template)
        msg = t.substitute(current)
        logger.debug(msg)

        self.publish(param.topic_write, msg)

    def publish(self, topic, msg):
        logger.debug('Publishing on {} with data {}'.format(topic, msg))
        self.client.publish(topic, msg)
