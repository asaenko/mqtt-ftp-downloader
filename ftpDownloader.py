#!/usr/bin/python3
"""
 Script:  ftpdownloader.py
 Author: Sascha Sambale
 Date:   June 21st, 2016
 Purpose: This application received messages from an MQTT queue and will then download a given file
        to a local directory.
"""
import sys

from configLoader import *


def main():
    # load the config from file
    config_loader = ConfigLoader(sys.argv[1])

    # init the configuration
    config_loader.load_config()

    # get the FTP connection
    ftp = config_loader.get_ftp()

    # get the MQTT connection and set the FTP connection as client
    mqtt = config_loader.get_mqtt(ftp)

    # start listening
    mqtt.start()

if __name__ == "__main__":
    main()
