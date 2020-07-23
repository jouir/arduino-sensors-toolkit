#!/usr/bin/env python3
import argparse
import configparser
import logging
import os
import sys
import time

import paho.mqtt.client as paho
import serial

logger = logging.getLogger(__name__)


def read_serial(interface):
    try:
        logger.debug('reading serial interface {}'.format(interface))
        s = serial.Serial(interface)
        s.flushInput()
        for i in range(2):
            data = s.readline()
            if i > 0:
                return data
    except Exception as err:
        logger.warning(str(err))
        time.sleep(2)


def parse_sensor_values(data):
    """
    Input line: <humidity>,<temperature>,<sound>
    Output structure:
        data = {
            'humidity': <humidity>,
            'temperature': <temperature>,
            'sound': <sound>
        }
    """
    humidity, temperature, sound = data.decode('utf-8').strip().split(',')
    return {'humidity': humidity, 'temperature': temperature, 'sound': sound}


def connect_mqtt(config):
    """Connect to MQTT broken from MQTT config and return client"""
    mqtt_host = config.get('host', 'localhost')
    mqtt_port = int(config.get('port', 1883))
    mqtt_username = config.get('username')
    mqtt_password = config.get('password')
    mqtt_client_id = config.get('client_id', 'serial2mqtt')

    client = paho.Client(client_id=mqtt_client_id)
    client.on_connect = on_connect
    if mqtt_username:
        client.username_pw_set(username=mqtt_username, password=mqtt_password)
    logging.debug('connecting to MQTT broker at {}:{}'.format(mqtt_host, mqtt_port))
    client.connect(mqtt_host, mqtt_port)
    return client


def publish(client, topic, value):
    logger.debug('publishing to topic "{}" with value "{}"'.format(topic, value))
    client.publish(topic, value)


def on_connect(client, userdata, flags, rc):
    if rc > 0:
        logger.error(paho.connack_string(rc))
    else:
        logger.info('connected to MQTT broker')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='path to configuration file', default='serial2mqtt.ini')
    parser.add_argument('-v', '--verbose', dest='loglevel', action='store_const', const=logging.INFO,
                        help='print more output')
    parser.add_argument('-d', '--debug', dest='loglevel', action='store_const', const=logging.DEBUG,
                        default=logging.WARNING, help='print even more output')
    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=args.loglevel)

    config = configparser.ConfigParser()
    if os.path.isfile(args.config):
        config.read(args.config)

    mqtt_config = config['mqtt'] if 'mqtt' in config else {}
    mqtt_topic_prefix = mqtt_config.get('topic_prefix', 'sensors')
    serial_config = config['serial'] if 'serial' in config else {}

    try:
        client = connect_mqtt(mqtt_config)
    except Exception as err:
        logger.error('connection to MQTT broker failed: {}'.format(str(err)))
        sys.exit(1)

    try:
        client.loop_start()

        while True:
            data = read_serial(serial_config.get('interface', '/dev/cuaU0'))
            if data:
                data = parse_sensor_values(data)
                for sensor_name, value in data.items():
                    topic = '/'.join([mqtt_topic_prefix, sensor_name])
                    publish(client, topic, value)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
