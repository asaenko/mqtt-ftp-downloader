#!/bin/sh
# Delete files and folders more than 3 days
# You can run this script as cron job
# Make sure you enter the correct directory here (same as FTP local path)
# Since I'm (one-way-)syncing this directory to Google Drive I can delete these files locally

dir="/home/pi/camera/"
days=+3
dt=`date +%y%m%d`

du -sh ${dir} > ${dir}Delete_$dt.log
find ${dir} -mtime $days -exec rm -Rf {} \;
du -sh ${dir} >> ${dir}Delete_$dt.log