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

import datetime
import os
import re
import shutil
import sys

import exifread


def get_extension(filename):
    """ Convenience function to get the extension of a filename. """
    filename, extension = os.path.splitext(filename)
    return extension


def extract_video_datetime_string(name):
    """
    Extract the datetime of a filename.

    :param name: Filename as string the contains datetime as e.g.
        something_20170204_123456.mp4
    :return: Datetime as string e.g. 2017-02-04_12.34.56
    :raises: AttributeError if there is no datetime in the filename.
    """
    m = re.search(r"\d\d\d\d\d\d\d\d_\d\d\d\d\d\d", name)
    d = datetime.datetime.strptime(m.group(0), '%Y%m%d_%H%M%S')
    return d.strftime("%Y-%m-%d_%H.%M.%S")


def get_new_filename(filename):
    """
    Get the new filename if possible.

    :param filename: The filename for which a new filename should be found.
    :return: The new filename.
    :raises: RuntimeError if no new filename can be found.
    """
    extension = get_extension(filename).lower()

    try:
        new = get_datetime_original(filename)
    except KeyError:
        try:
            new = extract_video_datetime_string(filename)
        except AttributeError:
            raise RuntimeError("Can't rename {}.".format(filename))

    return new + extension


def rename(filename):
    """
    Rename a jpeg file to YYYY-MM-DD_hh.mm.ss.

    :param filename: The path to the file that should be renamed.
    """
    if not os.path.exists(filename):
        print("File not found")
        return 0

    old = filename
    try:
        new = get_new_filename(filename)
    except RuntimeError as err:
        print(err)
        return

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


def get_datetime_original(filename):
    """
    Get the EXIF DateTimeOriginal.

    :param filename: The name of the file.
    :return: The formatted original date and time as YYYY-MM-DD_hh.mm.ss
    :raises: KeyError
    """
    f = open(filename, 'rb')
    tags = exifread.process_file(f, details=False)
    tmp = str(tags['EXIF DateTimeOriginal'])
    tmp = tmp.replace(" ", "_")
    s = tmp.split(':')
    return s[0] + "-" + s[1] + "-" + s[2] + "." + s[3] + "." + s[4]


if __name__ == '__main__':
    basedir = os.getcwd()
    backupdir = basedir + "/backup"

    dry_run = "dry-run" in sys.argv
    do_backup = "backup" in sys.argv

    for file in sys.argv:
        rename(file)
