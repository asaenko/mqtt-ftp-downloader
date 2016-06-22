"""
 Script: mqttConn.py
 Author: Sascha Sambale
 Date:   June 21st, 2016
 Purpose: Provides and maintains a connection to the MQTT broker
"""

import logging

import paho.mqtt.client as mqtt

from ftpConn import FTPConnection


class MQTTConnection(object):
    def __init__(self):
        self.logger = logging.getLogger('ftpDownloader')
        self.client = mqtt.Client()
        self.topic = "myTopic/myFTPTopic"
        self.host = "please_set_host"
        self.port = 1883
        self.keep_alive = "60"
        self.ftp_client = FTPConnection()

    def config(self, logger, user, password, host, port, keep_alive, topic, lwt_topic, lwt_message,
               tls):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.logger = logger
        self.client.username_pw_set(user, password)
        if tls.upper() == "YES":
            self.client.tls_set("./certs/ca.crt")
        self.topic = topic
        self.host = host
        self.port = port
        self.keep_alive = keep_alive
        self.client.will_set(str(lwt_topic), str(lwt_message), 0, False)

    def start(self):
        self.logger.debug("Trying to connect %s/%s/%s ", self.host, self.port, self.keep_alive)
        self.client.connect(self.host, self.port, self.keep_alive)
        print("Started MQTT listener. Listening to topic: " + self.topic + ". See log file for "
                                                                           "more details.")
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info(
                "Connected with result code " + str(rc) + ", subscribing to command topic " +
                self.topic)
        client.subscribe(str(self.topic))

    def on_disconnect(self, client, userdata, rc):
        self.logger.info("Disconnected from the MQTT broker with code " + str(rc))
        if rc != 0:
            self.logger.info("Unexpected disconnect: code = " + str(rc) + " reconnecting")

    def on_message(self, client, userdata, msg):
        self.logger.info("Downloading file: %s", str(msg.payload))
        self.ftp_client.download(str(msg.payload))

    def set_ftp_client(self, ftp_conn):
        self.ftp_client = ftp_conn
