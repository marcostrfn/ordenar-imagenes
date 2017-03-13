
import os
import sys
import exiftool
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



def main():

	dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'img')
	matches = module.get_files(dir, [".jpg"])

	if len(matches)==0:
		sys.exit()

	with exiftool.ExifTool() as et:
		metadata = et.get_metadata_batch(matches)

	print
	for d in metadata:


		# dname = os.path.dirname(d["SourceFile"])
		# bname = os.path.basename(d["SourceFile"])
		# para imagenes con pocos metadatos
		# try:
		#	dateOriginal = d["EXIF:DateTimeOriginal"]
		# except:
		# 	dateOriginal = None

		# print dname, bname, dateOriginal

		# para ver todas las claves de la imagen
		for key in sorted(d):
			print ( "{0} {1}".format(key,d[key]) )



if __name__ == '__main__': mainWin()
