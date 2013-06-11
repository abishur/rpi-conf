#! /usr/bin/python

# This program is provide free for use.  Parts or all of this program may be reproduced
# for non-profit or non-commerical application, but the author does ask that you notate
# which parts you used from them.  The author of this program is not responsible for
# any damage you cause to your computer by this program

# Made by Matthew Bennett (Abishur on the Raspberry Pi Forums, raspberrypi.org/) 06/08/2013
# Allows users to modify files in the ext4 partition from a Windows PC by
# copying them into the /boot FAT32 partition and then copying it back into the ext4

# Runs command in shell, prints any error message
def run_command(command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        if (p.returncode != 0):
                print err

# Modules needed for this program to work
import os
import csv
import shutil
import subprocess

#sets path to /boot partition
path = "/boot/"

#sets list of vital files on /boot to ignore
ignores = ['bootcode.bin','cmdline.txt','config.txt','.firmware_revision','fixup_cd.dat','fixup.dat','fixup_x.dat','issue.txt','kernel_emergency.img','kernel.img','start_cd.elf','start.elf','start_x.elf']

#get list of files in /boot partition
dirs = os.listdir(path)

# make a multidimensional list separated by commas and newlines
array = list( csv.reader( open( r'/etc/rpi_conf/list') ) )

# remove any elements that are empty lines
array = filter(lambda x: len(x)>0, array)

# remove white spaces from first element to ensure comments are properly removed
for line in array:
        if line [0][0] == ' ':
                line [0] = line[0].replace (' ','')

# remove any commented out lines
for line in array[:]:
        if line[0][0] == "#":
                array.remove(line)

# Remove white spaces from source file locations
for line in array:
        if line[1][0]==' ':
                line[1] = line[1].replace(' ','')


# checks each file name in /boot
for file in dirs:
        igCheck = 0

        #checks to make sure file is not on the ignore list
        for ign in ignores:
                if ign == file:
                        igCheck = 1
        # If the file isn't in the list of ignores
        if igCheck == 0:

                for line in array:
                        # for each file in /boot it checks to see if list matches that filename
                        #if they match it sets the file path for the file in /boot
                        # and checks file to see if it needs to read from or write to it
                        if line[0] == file:
                                textReplace = ""
                                filePath = path+file
                                searchfile = open (filePath, "r")
                                for results in searchfile:

                                        # If mode is "r"ead copy the actual config file to the /boot partition
                                        if "mode=r" in results:

                                                # Try to copy file
                                                try:
                                                        shutil.copy2(line[1], filePath)

                                                # If file does not exit give warning message
                                                except IOError as e:
                                                        print e

                                                # If file copied successfully change mode from "r"ead to "u"ndefined
                                                else:
                                                        textReplace = ("sed -i 's/mode=r/mode=u/g' " + filePath)
                                                        run_command(textReplace)

                                        # If mode is "w"rite make a backup of the actual config file and then overwrite
                                        # actual config file with contents in /boot partition
                                        elif "mode=w" in results:
                                                try:
                                                        shutil.copy2(line[1], line[1]+".bak")
                                                except IOError as e:
                                                        print e
                                                else:
                                                        try:
                                                                shutil.copy2(filePath, line[1])
                                                        except IOError as e:
                                                                print e
                                                        else:
                                                                textReplace = "sed -i 's/mode=w/mode=u/g' " + filePath
                                                                run_command(textReplace)
                                                                # remove mode=w from actual config file
                                                                textReplace = "sed -i 's/mode=w//g' " + line[1]
                                                                run_command(textReplace)

                                        # If mode is "b"ackup copy .bak file and overwrite current config file
                                        elif "mode=b" in results:
                                                try:
                                                        shutil.copy2(line[1]+".bak", line[1])
                                                except IOError as e:
                                                        print e
                                                else:
                                                        textReplace = "sed -i 's/mode=b/mode=u/g' " + filePath
                                                        run_command(textReplace)
                                        #if mode is "d"elete remove the file from /boot
                                        elif "mode=d" in results:
                                                # no try is performed because if the file did not exist you'd
                                                # never be able to search it for mode=d
                                                os.remove(filePath)

                                # Close file
                                searchfile.close()
                                # If Read/write operation was performed, halt system
if textReplace != "":
        run_command("halt")
