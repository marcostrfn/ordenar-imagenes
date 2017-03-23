
import os
import sys
import re

import exifread
import pickle
import json
from shutil import copyfile
from optparse import OptionParser
import numpy as np
import cv2

from funciones import module
from funciones.files import findFiles
from funciones.exif.exifData import ExifExtractor

# para ver mas informacion de error no-handlers-could-be-found-for-logger-exifread
import logging
logging.basicConfig()

		


def getFileData():
	# pickle donde dejara la informacion de las imagenes
	dir_data = os.path.join(os.path.abspath(os.path.dirname(__file__)),'_data')
	if not os.path.exists(dir_data):
		os.makedir(dir_data)

	file_data = os.path.join(dir_data,'data.p')
	return file_data


def verFichero():
	file_data = getFileData()
	info = pickle.load(open( file_data, "rb" ))
	for line in sorted(info):
		print json.dumps(line, indent=4, sort_keys=True)
		# if "Image XResolution" in line: print line[r'Image XResolution']

		
		
def tratar_img(img_number, file, dir_dest, opts, face_cascade=None):	
	
	num_faces = 0
	if opts.FACE and face_cascade is not None:
		img = cv2.imread(file)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		num_faces = len(faces)	
		cv2.destroyAllWindows()

	
	
	exif = ExifExtractor(file)		
	name = os.path.splitext(os.path.basename(file))[0][0:]
	extension = os.path.splitext(os.path.basename(file))[1][1:]
	
	
	# nuevo nombre del fichero
	sub_dir = None	
	hayDate = None
	if exif.hasTag('EXIF', 'DateTimeOriginal') and exif.getDateTimeOriginal() is not None:
		date_time = exif.getDateTimeOriginal()		
		sub_dir = os.path.join('Si_DateTimeOriginal',date_time[0:7])
		if not os.path.exists(os.path.join(dir_dest,'Si_DateTimeOriginal',date_time[0:7])):
			os.makedirs(os.path.join(dir_dest,'Si_DateTimeOriginal',date_time[0:7]))

		if opts.FACE:
			if not os.path.exists(os.path.join(dir_dest,'Si_DateTimeOriginal',date_time[0:7],'Si_Face')):
				os.makedirs(os.path.join(dir_dest,'Si_DateTimeOriginal',date_time[0:7],'Si_Face'))

			if not os.path.exists(os.path.join(dir_dest,'Si_DateTimeOriginal',date_time[0:7],'No_Face')):
				os.makedirs(os.path.join(dir_dest,'Si_DateTimeOriginal',date_time[0:7],'No_Face'))

		file_name = "{}.{}".format(date_time, extension)
		hayDate = True

	else:
		date_time = name
		sub_dir = 'No_DateTimeOriginal'
		if opts.FACE:
			if not os.path.exists(os.path.join(dir_dest,'No_DateTimeOriginal','Si_Face')):
				os.makedirs(os.path.join(dir_dest,'No_DateTimeOriginal','Si_Face'))
			if not os.path.exists(os.path.join(dir_dest,'No_DateTimeOriginal','No_Face')):
				os.makedirs(os.path.join(dir_dest,'No_DateTimeOriginal','No_Face'))



		file_name = "{}.{}".format(date_time, extension)

	
	if opts.FACE:
		if num_faces > 0:		
			sub_dir = os.path.join(sub_dir, 'Si_Face')
		else:
			sub_dir = os.path.join(sub_dir, 'No_Face')


	file_des = os.path.join(dir_dest, sub_dir, file_name)
	
	if os.path.isfile(file_des) and opts.DELETE:
		os.remove(file_des)
			
	if os.path.isfile(file_des) and not opts.DELETE:
		sub_dir = 'copias'
		num_file = 1
		while True:										
			file_name = "{}({}).{}".format(date_time.lower(), num_file, extension.lower())
											
			file_des = os.path.join(dir_dest, sub_dir, file_name)
			if not os.path.isfile(file_des):
				break
			num_file += 1

	print("[copy] {} {} => {}".format(img_number, os.path.basename(file),os.path.basename(file_des)))	
	copyfile(file,file_des)		
	
	

def img_sort(opts):
	dir_source = opts.dir_source
	dir_dest = opts.dir_dest
	types = opts.types.split(",")	
		
	if opts.FACE:
		file_cascade = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
		face_cascade = cv2.CascadeClassifier(file_cascade)
	else:
		face_cascade = None
	
	img_number = 0
	if opts.RECURSIVO:		
		for file in findFiles.get_files_recursive_yield(dir_source, types):	
			img_number += 1	
			tratar_img(img_number, file, dir_dest, opts, face_cascade)		
	else:
		for file in findFiles.get_files_yield(dir_source, types):
			img_number += 1
			tratar_img(img_number, file, dir_dest, opts, face_cascade)

	print("[main] finalizado")

	return

def ayuda():
	print '''Usage: imgsort.py [options]

Options:
  -h, --help			show this help message and exit
  -s DIR_SOURCE, --source=DIR_SOURCE
						[OBLIGATORIO] directorio a leer
  -d DIR_DEST, --dest=DIR_DEST
						[OBLIGATORIO con opcion COPIAR] directorio destino
  -t TYPES, --types=TYPES
						tipo de fichero a leer
  -r, --recursivo		recorrer directorio en modo recursivo
  -v, --verbose			Activar salida de mensajes por consola
  --delete				eliminar imagenes en DIR_DEST si existen'''
  

def img_init():

	parser = OptionParser()

	parser.add_option('-s', '--source', dest='dir_source', help='[OBLIGATORIO] directorio a leer')
	parser.add_option('-d', '--dest', dest='dir_dest', help='[OBLIGATORIO con opcion COPIAR] directorio destino')
	
	parser.add_option('-t', '--types', dest='types', help='tipo de fichero a leer')
	
	parser.add_option('-r', '--recursive', dest='RECURSIVO', action="store_true", default=False, help='recorrer directorio en modo recursivo')
	parser.add_option('-v', '--verbose', dest="VERBOSE", action="store_true", default=False, help='Activar salida de mensajes por consola')
	parser.add_option('--delete', dest='DELETE', action="store_true", default=False, help='eliminar imagenes en DIR_DEST si existen')
	parser.add_option('--face', dest='FACE', action="store_true", default=False, help='marcar imagenes con rostros')
		
	(opts, args) = parser.parse_args()

	if opts.dir_source is None:
		ayuda()
		sys.exit(1)

	if not opts.types:
		opts.types = '.jpg,.jpeg,.png'
	
	if opts.dir_dest is None:
		ayuda()
		sys.exit(1)

	if not os.path.exists(opts.dir_source):
		ayuda()
		sys.exit(1)
			
	if not os.path.exists(opts.dir_dest):
		os.makedirs(opts.dir_dest)

	if not os.path.exists(os.path.join(opts.dir_dest,'copias')):
		os.makedirs(os.path.join(opts.dir_dest,'copias'))

	Si_DateTimeOriginal = os.path.join(opts.dir_dest,'Si_DateTimeOriginal')
	No_DateTimeOriginal = os.path.join(opts.dir_dest,'No_DateTimeOriginal')
	
	if not os.path.exists(Si_DateTimeOriginal):
		os.makedirs(Si_DateTimeOriginal)
			

	if not os.path.exists(No_DateTimeOriginal):
		os.makedirs(No_DateTimeOriginal)
		
	img_sort(opts)
