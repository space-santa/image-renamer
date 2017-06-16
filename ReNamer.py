#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script renames all .jpg-files in its directory using the original
creation-date-time. The new filename is YYYY-MM-DD_hh.mm.ss.jpg
The original files are copied into ./backup

Usage (assuming ReNamer.py is in your $PATH):

    cd /path/to/many/picture
    ReNamer.py *.jpg

 This program is (c) 2014-2017 Claus Zirkel.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License version 3
 as published by the Free Software Foundation.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the
 Free Software Foundation, Inc.
 51 Franklin Street, Fifth Floor
 Boston, MA  02110-1301, USA.
"""

import sys
import exifread
import os
import shutil

basedir = os.getcwd()
backupdir = basedir + "/backup"

dry_run = "dry-run" in sys.argv
do_backup = "backup" in sys.argv


def rename(filename):
    """ Rename a jpeg file to YYYY-MM-DD_hh.mm.ss.

    Args:
        filename: the path to the file that should be renamed
    """
    if not os.path.exists(filename):
        print("File not found")
        return 0

    old = filename
    new = getDateTimeOriginal(old) + '.jpg'

    if dry_run:
        print("dry-run: " + old + " -> " + new)
        return 0

    if old == new:
        print("File " + old + " is already renamed.")
        return 0
    else:
        if do_backup:
            if not os.path.isdir(backupdir):
                os.makedirs(backupdir)

            shutil.copyfile(old, backupdir + '/' + old)

        shutil.move(old, new)
        print(old + " -> " + new)


def getDateTimeOriginal(filename):
    """ Get the EXIF DateTimeOriginal.

        Args:
            filename: the name of the file

        Returns:
            the formatted original date and time as YYYY-MM-DD_hh.mm.ss
    """
    f = open(filename, 'rb')
    tags = exifread.process_file(f, details=False)
    tmp = str(tags['EXIF DateTimeOriginal'])
    tmp = tmp.replace(" ", "_")
    s = tmp.split(':')
    return s[0] + "-" + s[1] + "-" + s[2] + "." + s[3] + "." + s[4]


for file in sys.argv:
    if file.endswith(".jpg") or file.endswith(".JPG"):
        rename(file)
    else:
        print(file + " is not a jpg")
