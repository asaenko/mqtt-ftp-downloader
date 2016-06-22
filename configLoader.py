"""
 Script:  configLoader.py
 Author: Sascha Sambale
 Date:   June 7th, 2016
 Purpose: Loads all configurations (sensors, mqtt & rest connection, logger,...)
        from the given config file (which is being passed as argument)
"""

import configparser
import logging
import logging.handlers

try:
    from mqttConn import MQTTConnection

    mqtt_support = True
except:
    mqtt_support = False
    print('MQTT required files not found. MQTT not supported.')

try:
    from ftpConn import FTPConnection

    ftp_support = True
except:
    ftp_support = False
    print('FTP required files not found. FTP not supported.')


class ConfigLoader:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(config_file)
        print("Loaded " + config_file)
        self.mqtt_conn = MQTTConnection()
        self.ftp_conn = FTPConnection()
        self.logger = logging.getLogger('ftpDownloader')

    def config_logger(self):
        logger = logging.getLogger('sensorReporter')

        file = self.config.get("Logging", "File")
        size = self.config.getint("Logging", "MaxSize")
        num = self.config.getint("Logging", "NumFiles")

        print("Configuring logger: file = " + file + " size = " + str(size) + " num = " + str(num))
        logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler(file, mode='a', maxBytes=size, backupCount=num)
        log_level = self.config.get("Logging", "LogLevel")
        print("LogLevel retrieved from options: " + log_level)

        if log_level.lower().strip() == "debug":
            fh.setLevel(logging.DEBUG)
        else:
            log_level = "info"
            fh.setLevel(logging.INFO)

        print("LogLevel set to " + log_level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info("---------------Started")

        self.logger = logger
        return logger

    def config_ftp(self):
        self.logger.info("Configuring the FTP Connection: %s",self.config.get("FTP", "Host"))
        self.ftp_conn.config(self.logger, self.config.get("FTP", "User"),
                             self.config.get("FTP", "Password"), self.config.get("FTP", "Host"),
                             self.config.getint("FTP", "Port"),
                             self.config.get("FTP", "Path"),
                             self.config.get("FTP", "LocalPath"))

    def config_mqtt(self):
        self.logger.info("Configuring the MQTT Broker: %s ", self.config.get("MQTT", "Host"))
        self.mqtt_conn.config(self.logger, self.config.get("MQTT", "User"),
                              self.config.get("MQTT", "Password"), self.config.get("MQTT", "Host"),
                              self.config.getint("MQTT", "Port"),
                              self.config.getfloat("MQTT", "Keepalive"),
                              self.config.get("MQTT", "Topic"),
                              self.config.get("MQTT", "LWT-Topic"),
                              self.config.get("MQTT", "LWT-Msg"),
                              self.config.get("MQTT", "TLS"))

    def get_mqtt(self, ftp):
        self.mqtt_conn.set_ftp_client(ftp)
        return self.mqtt_conn

    def get_ftp(self):
        return self.ftp_conn

    def load_config(self):
        self.config_logger()
        self.config_ftp()
        if mqtt_support:
            self.config_mqtt()
