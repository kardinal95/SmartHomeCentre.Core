import json

import paho.mqtt.client as mqtt
from loguru import logger

from py.drivers.mqtt.endpoint import MqttEndpoint
from py.main.db import DatabaseObjects as do


class MqttDriver:
    def __init__(self, uuid, parameters):
        self.uuid = uuid
        # TODO Check if parameters exists
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        filtered = json.loads(parameters)
        # TODO Connection errors
        logger.info('Connecting mqtt server on {}:{}', filtered['host'], filtered['port'])
        self.client.connect(filtered['host'], filtered['port'], filtered['timeout'])

        session = do.session()
        mqtt_eps = session.query(MqttEndpoint).filter(MqttEndpoint.parent_uuid == self.uuid).all()
        for item in mqtt_eps:
            self.client.subscribe(item.connection_string)
            logger.debug('Subscribing on MQTT device with name {}'.format(item.name))
        session.close()

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        pass

    def on_message(self, client, userdata, msg):
        logger.debug('Received message on {} with data: {}'.format(msg.topic, msg.payload))

        session = do.session()
        endpoint = session.query(MqttEndpoint).filter(MqttEndpoint.connection_string == msg.topic).first()
        session.close()

        endpoint.update_values(msg.payload)

    def publish(self, topic, msg):
        logger.debug('Publishing on {} with data {}'.format(topic, msg))
        self.client.publish(topic, msg)