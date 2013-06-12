Rpi-conf
========

Copies user defined config files from EXT4 partions to FAT32 partions to be edited on PCs which cannot view EXT4 partitions.

To Install:
------------
Installation is very minimal, copy all files from gist and perform

> Sudo make install

This will copy all files to relevant locations and check for file copy operations on boot

How to Run Manually:
-------------------
If you just want to test the program out, you can manually initiate the program by typing

> sudo python /etc/rpi_conf/config.py

How to Use:
-----------
Rpi-conf uses a file named list located in

> /etc/rpi_conf/

to search for specific file names in the FAT32 /boot partition and their associated config file.  It can be used for any type of file you wish.  To add a new association in list simply type in

> Name_to_check_for_in_boot, path_to_the_source_file

on a new line.  I.E.

> network.cfg, /etc/network/interfaces

In this example, on each boot the program will check to see if the file network.cfg exists in /boot.  If it finds network.cfg it will check for one of 5 modes controlled by putting mode=r/w/b/d/u somewhere in network.cfg file.

Explination of the Modes:
--------------------------

**mode=r**

"r"ead mode - Reads the contents from the provided path to the source file and copies it to associated file in /boot (i.e. Network.cfg).  If any file is read, the pi will automatically halt when the program finishes running.  If there are multiple file operations, the pi will default to halting.

**mode=w**

"w"rite mode - Makes a backup of the original source file and then reads the contents of the file in /boot and overwrite the original source file.  If any file is written, the pi will automatically reboot when the program finishes running.

**mode=b**

"b"ackup mode - Provided a backup of the oringinal source file exists, it overwrites the original source file with the backup.  After backup restorations, the pi will automatically reboot when the program finishes running.

**mode=d**

Deletes the file in the FAT32 /boot partitions, does not affect the original source file.  The pi continues normal operation if any files from the /boot partition are deleted.

**mode=u**

"u"ndefined mode - After a mode=r/w/b operation, the mode is automatically set to u.  Nothing is performed on files whose mode is set to u.

Known Limitations:
------------------
This program does not supporpt files with spaces in the file path or file name
