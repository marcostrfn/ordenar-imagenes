
import os
import sys
import re

import exifread
import pickle
import json
from shutil import copyfile
from optparse import OptionParser
import threading

from funciones import module

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



def ExifExtractor:
	''' Extrae datos exif de una imagen '''
	file = None
	exif_data = None
	exif_tags = {}
	exif_file = {}
	tags = None
	
	def __init__(self, file):
		self.file = file
	
	
	def __extract(self):
		''' cargar datos exif de un imagen '''
		f = open(self.file, 'rb')
		self.tags = exifread.process_file(f)
		f.close()

		
	def setFileInfo(self):
		''' cargar informacion del fichero '''
		file_tag['filename'] = os.path.basename(self.file)
		file_tag['dirname'] = os.path.dirname(self.file)
		self.exif_file['file'] = file_tag
	
	
	def setExifInfo(self):
		''' parsear datos exif excepto thumb '''
		self.__extract()
		for tag in sorted(self.tags.keys()):
			match = re.search("thumb", tag, re.IGNORECASE)
			if not match:
				try:
					self.exif_tag[tag] = tags.get(tag).printable.strip()
				except:
					pass
		
	
	
		
		
def copiarImagenes(n_file, exif_data, dir_source, dir_dest, types, opts):
	line = exif_data
	dateTime = None
	for exif in line["Exif"]:
		match = re.search("^(EXIF){1}\s(datetimeoriginal){1}",exif, re.IGNORECASE)
		if match: # existe EXIF dateTimeOriginal
			dateTime = line["Exif"][exif].replace(' ','_').replace(':','')
			break

	if dateTime is not None and not dateTime=="00000000_000000":
		extension = os.path.splitext(line["File"]["Filename"])[1][1:]
		file_name = "{}.{}".format(dateTime, extension)
	else:
		file_name = line["File"]["Filename"]


	file_src = os.path.join(line["File"]["dirname"], line["File"]["Filename"])
	file_des = os.path.join(dir_dest, file_name)

	if os.path.isfile(file_des):
		num_file = 1
		while True:
			file_name = "{}({}).{}".format(dateTime, num_file, extension)
			file_des = os.path.join(dir_dest, file_name)
			if not os.path.isfile(file_des):
				break
			num_file += 1

	copyfile(file_src,file_des)
	module.print_n("[copiarImagenes] {} {} => {}".format(n_file, line["File"]["Filename"],file_name))
	


def parseData(num_file, file, dir_source, dir_dest, types, info, opts):
	# Open image file for reading (binary mode)
	# and return Exif tags
	f = open(file, 'rb')
	tags = exifread.process_file(f)
	f.close()

	file_tag = {}
	exif_tag = {}

	for tag in sorted(tags.keys()):
		match = re.search("thumb", tag, re.IGNORECASE)
		if not match:
			try:
				exif_tag[tag] = tags.get(tag).printable.strip()
			except:
				pass

	file_tag['Filename'] = os.path.basename(file)
	file_tag['dirname'] = os.path.dirname(file)
	exif_data = {'File':file_tag, 'Exif':exif_tag}

	if opts.COPIAR:
		copiarImagenes(num_file, exif_data, dir_source, dir_dest, types, opts)
		info.append(exif_data)



def main(opts):
	file_data = getFileData()
	if file_data is None:
		return None

	dir_source = opts.dir_source
	dir_dest = opts.dir_dest
	types = opts.types.split(",")

	if opts.RECURSIVO:
		files = module.get_files_recursive(dir_source, types)
	else:
		files = module.get_files(dir_source, types)

	threads = list()
	total_files = len(files)
	info = []
	num_file = 0

	for file in files:
		num_file += 1
		module.print_n("[main] parsing file {} de {}".format(num_file, total_files))
		t = threading.Thread(target=parseData, args=(num_file, file, dir_source, dir_dest, types, info, opts,))
		threads.append(t)


	# Start all threads
	for x in threads:
		x.start()

	# Wait for all of them to finish
	for x in threads:
		x.join()

	pickle.dump( info, open( file_data, "wb" ) )
	module.print_n("[main] finalizado")

	return

def ayuda():
	print '''Use -h para ayuda'''



if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-s', '--source', dest='dir_source', help='[OBLIGATORIO] directorio a leer')
	parser.add_option('-d', '--dest', dest='dir_dest', help='[OBLIGATORIO] directorio destino')
	parser.add_option('-t', '--types', dest='types', help='[OBLIGATORIO] tipo de fichero a leer')
	parser.add_option('-r', '--recursivo', dest='RECURSIVO', action="store_true", default=False, help='recorrer dir_sourceectorio en modo recursivo')
	parser.add_option('-v', '--verbose', dest="VERBOSE", action="store_true", default=False, help='Activar salida de mensajes por consola')
	parser.add_option('-c', '--copiar', dest='COPIAR', action="store_true", default=False, help='copiar imagenes')

	(opts, args) = parser.parse_args()

	if opts.dir_source is None:
		ayuda()
		sys.exit(1)

	if not opts.types:
		ayuda()
		sys.exit(1)
	
	if not os.path.exists(opts.dir_source):
		ayuda()
		sys.exit(1)

	if not os.path.exists(opts.dir_dest):
		os.makedirs(opts.dir_dest)

	file_data = getFileData()
	if os.path.exists(file_data):
		os.remove(file_data)

	main(opts)