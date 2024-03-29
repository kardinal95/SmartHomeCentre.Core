from string import Template

import paho.mqtt.client as mqtt
from loguru import logger

from py import db_session
from py.core import MainHub
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
        pass

    @db_session
    def on_connect(self, client, userdata, flags, rc, session):
        from py.models.endpoint import EndpointMdl
        logger.info('Connected with result code {}'.format(str(rc)))

        mqtt_eps = session.query(EndpointMdl).filter(EndpointMdl.driver_type == MqttDriver.enum_type).all()
        parameters = session.query(MqttParamsMdl).all()
        for item in zip(mqtt_eps, parameters):
            logger.debug('Subscribing on MQTT device with name {}'.format(item[0].name))
            self.client.subscribe(item[1].topic_read)

    def __init__(self, uuid, host, port, timeout=60):
        self.uuid = uuid
        # TODO Check if parameters exists
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        # TODO Connection errors
        logger.info('Connecting to mqtt server on {}:{}', host, port)
        self.client.connect(host, port, timeout)

        self.client.loop_start()

    @staticmethod
    @db_session
    def on_message(client, userdata, msg, session):
        logger.debug('Received message on {} with data: {}'.format(msg.topic, msg.payload))

        param = session.query(MqttParamsMdl).filter(MqttParamsMdl.topic_read == msg.topic).first()
        mqtt_type = session.query(MqttEpTypeMdl).filter(MqttEpTypeMdl.uuid == param.type_uuid).first()

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

    @db_session
    def process_data_to_ep(self, ep_uuid, parameters, session):
        param = session.query(MqttParamsMdl).filter(MqttParamsMdl.ep_uuid == ep_uuid).first()
        mqtt_type = session.query(MqttEpTypeMdl).filter(MqttEpTypeMdl.uuid == param.type_uuid).first()

        current = MainHub.retrieve(RedisSrv).hgetall(str(ep_uuid))

        for key in current.keys():
            if key in parameters.keys():
                current[key] = str(parameters[key])

        t = Template(mqtt_type.write_template)
        msg = t.substitute(current)

        self.publish(param.topic_write, msg)

    def publish(self, topic, msg):
        logger.debug('Publishing on {} with data {}'.format(topic, msg))
        self.client.publish(topic, msg)
