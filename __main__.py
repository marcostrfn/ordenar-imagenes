﻿
import os
import sys
import exifread
import re

from funciones import module


def mainWin():
    # https://pypi.python.org/pypi/ExifRead

	# dir = r"C:\tmp"
	dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'img')
	files = module.get_files(dir, [".png", ".jpg"])
	for file in files:
		print file
		print "=" * len(file)

		# Open image file for reading (binary mode)
		# and return Exif tags
		f = open(file, 'rb')
		tags = exifread.process_file(f)
		f.close()

		for tag in sorted(tags.keys()):
			match = re.search("thumb", tag, re.IGNORECASE)
			if not match:
				match = re.search("^(EXIF|image){1}\s(model|datetimeoriginal){1}", tag, re.IGNORECASE)
				if match:
					print ("{0:20}\t\t{1}".format(tag, tags[tag]))

		print


if __name__ == '__main__': mainWin()
