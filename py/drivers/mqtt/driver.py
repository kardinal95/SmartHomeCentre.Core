import json

import paho.mqtt.client as mqtt
from loguru import logger


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
        self.client.loop_start()

    def on_connect(self):
        pass

    def on_message(self):
        pass