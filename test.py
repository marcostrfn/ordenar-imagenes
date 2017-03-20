#!/usr/bin/python


import os
import sys
from shutil import copyfile

from funciones.module import mprint
from funciones.exif.exifData import ExifExtractor
from funciones.files.findFiles import get_files_recursive_yield


def parseData(f, n):
	
	base, ext = os.path.splitext(f)
	
	exif = ExifExtractor(f)
	filename = exif.getDateTimeOriginal()
	if filename is None:
		filename = exif.getExifData()['file']['filename']
		destino = r'c:\tmp\copia_no_data'
	else:
		filename = "{}{}".format(filename, ext)
		destino = r'c:\tmp\copia_si_data'
		
	file_des = os.path.join(destino, filename)
	
	if os.path.isfile(file_des):
		num_file = 1
		extension = os.path.splitext(filename)[1][1:]
		while True:
			filename = "{}({}).{}".format(filename, num_file, extension)
			file_des = os.path.join(destino, filename)
			if not os.path.isfile(file_des):
				break
			num_file += 1

	copyfile(f,file_des)			
	mprint( "{} {} ---> {}".format(n, os.path.basename(f), filename) )



def main():
	dir_source = r'C:\Users\xx\Pictures\'
	types = ['.jpg','.png']

	n = 0
	files = get_files_recursive_yield(dir_source, types)
	for f in files:
		n += 1
		parseData(f,n)
		
		
		
if __name__ == '__main__': main()