Introduction
============
I'm using this script to download the latest footage from my [Xiaomi Xiaoyi Ants (720p)](http://www.yitechnology.com/homecamera.php?id=1) security cam, which contains the latest [Yi Hack custom firmware](https://github.com/fritz-smh/yi-hack/) that allows to access the camera via FTP.

Flow
====
My server checks every 30seconds whether there was a motion by calling the REST API of the camera. As soon as some footage has been captures, it will send the filename to a certain (configured) topic on my [Mosquitto MQTT queue](http://mosquitto.org/). This script listens to the topic and will download that file from the camera.

Configuration
=============
The configuration is pretty self-explaining. Just have a look at the ftpdownloader_demo.ini file. Just edit that file and rename it to ftpDownloader.ini.

Usage
=====
To run the script manually you must pass the ini file to the script.

`sudo python ftpDownloader ftpDownloader.ini`

If it has been installed as a systemd service (see config/install.sh for more information), run:

`sudo systemctl start ftpDownloader`

# Support
I won't be able to give you premium support here. So you should be able to understand the code when something unexpected happens. I also won't take any responsibility if something messes up your system.
