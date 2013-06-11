#!/bin/sh
### BEGIN INIT INFO
# Provides:          rpi-conf
# Required-Start: udev mountkernfs $remote_fs
# Required-Stop:
# Default-Start: S
# Default-Stop:
# Short-Description: Copies files from EXT4 partition to /boot FAT32 partition for editing on computers that cannot access EXT4 partitions
# Description:
### END INIT INFO

case "$1" in
  start)
    echo "Checking for rpi-conf copy operations"
    python /etc/rpi_conf/config.py &
    ;;
  stop)
    echo "Nothing to stop"
    ;;
  *)
    echo "Usage: /etc/init.d/rpi_conf {start|stop}"
    exit 1
    ;;
esac

exit 0
