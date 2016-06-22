"""
 Script: ftpConn.py
 Author: Sascha Sambale
 Date:   June 21st, 2016
 Purpose: Accesses an FTP Server to download a given file from a given path.
"""

import ftplib
import logging
import tempfile


class FTPConnection(object):
    def __init__(self):
        self.logger = logging.getLogger('ftpDownloader')
        self.ftp_conn = ftplib.FTP()
        self.user = "user"
        self.password = "password"
        self.port = 21
        self.path = "/"
        self.local_path = tempfile.gettempdir() + "/"
        self.host = "myHost"

    def config(self, logger, user, password, host, port, path, local_path):
        self.logger = logger
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.path = path
        self.local_path = local_path

    def download(self, filename):
        self.ftp_conn = ftplib.FTP(str(self.host))
        file_name = filename.split("/")
        local_filename = filename
        if len(file_name) > 1:
            local_filename = file_name[len(file_name) - 1]
            self.logger.info(
                    "Local filename must not contain a full path - will reduce to filename only!")
            self.logger.info("Old file name: %s", filename)
            self.logger.info("New file name: %s", local_filename)
        file = open(self.local_path + local_filename, 'wb')
        self.ftp_conn.cwd(self.path)
        self.ftp_conn.retrbinary('RETR ' + filename, file.write)
        self.logger.info("File downloaded: " + self.local_path + local_filename)
        file.close()
        self.ftp_conn.quit()
