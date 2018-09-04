#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script renames all .jpg-files in its directory using the original
creation-date-time. The new filename is YYYY-MM-DD_hh.mm.ss.jpg
The original files are copied into ./backup

Usage (assuming ReNamer.py is in your $PATH):

    cd /path/to/many/picture
    ReNamer.py *.jpg

 This program is ©️ 2014-2017 Claus Zirkel.

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


def extract_video_datetime_string(filename):
    """
    Extract the datetime of a filename.

    :param filename: Filename as string the contains datetime as e.g.
        something_20170204_123456.mp4
    :return: Datetime as string e.g. 2017-02-04_12.34.56
    :raises: AttributeError if there is no datetime in the filename.
    """
    manual_date = re.search(r"\d\d\d\d\d\d\d\d_\d\d\d\d\d\d", filename)
    timestamp = datetime.datetime.strptime(manual_date.group(0), '%Y%m%d_%H%M%S')
    return timestamp.strftime("%Y-%m-%d_%H.%M.%S")


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


def create_backup(filename):
    """ Copy filename to backup/filename. """
    basedir = os.getcwd()
    backupdir = basedir + "/backup"

    if not os.path.isdir(backupdir):
        os.makedirs(backupdir)

    shutil.copyfile(filename, backupdir + '/' + filename)


def rename(filename, dry_run=False, do_backup=False):
    """
    Rename a jpeg file to YYYY-MM-DD_hh.mm.ss.

    :param filename: The path to the file that should be renamed.
    """
    if not os.path.exists(filename):
        print("File not found")
        return

    try:
        new = get_new_filename(filename)
    except RuntimeError as err:
        print(err)
        return

    if dry_run:
        print("dry-run: " + filename + " -> " + new)
        # We return after doing the dry run because we don't want to allow
        # an accidental backup when doing a dry run.
        return

    if filename == new:
        print("File " + filename + " is already renamed.")
        return

    if do_backup:
        create_backup(filename)

    shutil.move(filename, new)
    print(filename + " -> " + new)


def get_datetime_original(filename):
    """
    Get the EXIF DateTimeOriginal.

    :param filename: The name of the file.
    :return: The formatted original date and time as YYYY-MM-DD_hh.mm.ss
    :raises: KeyError
    """
    file = open(filename, 'rb')
    tags = exifread.process_file(file, details=False)
    tmp = str(tags['EXIF DateTimeOriginal'])
    tmp = tmp.replace(" ", "_")
    parts = tmp.split(':')
    return parts[0] + "-" + parts[1] + "-" + parts[2] + "." + parts[3] + "." + parts[4]


if __name__ == '__main__':
    DRY_RUN = "dry-run" in sys.argv
    DO_BACKUP = "backup" in sys.argv

    for name in sys.argv:
        rename(name, dry_run=DRY_RUN, do_backup=DO_BACKUP)
