#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is (c) 2014 Armin Zirkel.
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import exifread
import os
import shutil

basedir = "."
backupdir = "./backup"

def rename(filename):
	# gets the filename, calls the function to get the EXIF DateTimeOriginal
	# checks if the filename needs to be changed
	# if so, copies the original file to ./backup and then renames the file
	if not os.path.exists(filename):
		print "File not found"
		return 0
	old = filename
	new = getDateTimeOriginal(old) + '.jpg'
	#print new
	#return 0
	if old == new:
		print "File " + old + " is already renamed."
		return 0
	else:
		if not os.path.isdir(backupdir):
			os.makedirs(backupdir)
		
		shutil.copyfile(old, backupdir + '/' + old)
		
		shutil.move(old, new)
		print old + " -> " + new
	
def getDateTimeOriginal(filename):
	# gets the file and returns the formatted original date and time as YYYY-MM-DD hh.mm.ss
	f = open(filename, 'rb')
	tags = exifread.process_file(f, details = False)
	s = str(tags['EXIF DateTimeOriginal']).split(':')
	return s[0] + "-" + s[1] + "-" + s[2] + "." + s[3] + "." + s[4]

for file in os.listdir(basedir):
	if file.endswith(".jpg") or file.endswith(".JPG"):
		rename(file)
	else:
		print file + " is not a jpg"

		
