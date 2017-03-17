
import os
import sys
import re

import exifread
import pickle
import json
from shutil import copyfile
from optparse import OptionParser

from funciones import module


# para ver mas informacion de error no-handlers-could-be-found-for-logger-exifread
import logging
logging.basicConfig()


def getFileData():
	# pickle donde dejara la informacion de las imagenes
	dir_data = os.path.join(os.path.abspath(os.path.dirname(__file__)),'_data')	
	if not os.path.exists(dir_data):
		os.makedirs(dir_data)	
	
	file_data = os.path.join(dir_data,'data.p')
	return file_data


def verFichero():
	file_data = getFileData()
	info = pickle.load(open( file_data, "rb" ))
	for line in sorted(info):
		print json.dumps(line, indent=4, sort_keys=True)		
		# if "Image XResolution" in line: print line[r'Image XResolution']	

		
		
def copiarImagenes(opts):
	module.print_n("[copiarImagenes]")
	file_data = getFileData()
	if file_data is None:
		return None
		
	dir_source = opts.DIR
	dir_dest, types = module.get_data_config()
	info = pickle.load(open( file_data, "rb" ))
	for line in info:
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
		
		
		file_src = os.path.join(line["File"]["Dirname"], line["File"]["Filename"])
		file_des = os.path.join(dir_dest, file_name)
		
		if os.path.isfile(file_des):
			num_file = 1
			while True:
				file_name = "{}({}).{}".format(dateTime, num_file, extension)
				file_des = os.path.join(dir_dest,  file_name)
				if not os.path.isfile(file_des):
					break
				num_file += 1

		module.print_n("[copiarImagenes] {} => {}".format(line["File"]["Filename"],file_name))
		copyfile(file_src,file_des)
		
		
def main(opts):
	file_data = getFileData()
	if file_data is None:
		return None
		
	info = []	
	
	dir_source = opts.DIR
	dir_dest, types = module.get_data_config()	
	if opts.RECURSIVO:
		files = module.get_files_recursive(dir_source, types)
	else:
		files = module.get_files(dir_source, types)
		
	total_files = len(files)
	
	num_file = 0
	for file in files:	
		num_file += 1
		module.print_n("[main] parsing file {} de {}".format(num_file, total_files))
		# Open image file for reading (binary mode)
		# and return Exif tags
		f = open(file, 'rb')
		tags = exifread.process_file(f)
		f.close()

		file_tag = {}
		exif_tag = {}
		
		file_tag['Filename'] = os.path.basename(file)
		file_tag['Dirname'] = os.path.dirname(file)
		
		for tag in sorted(tags.keys()):
			match = re.search("thumb", tag, re.IGNORECASE)
			if not match:
				try:
					exif_tag[tag] = tags.get(tag).printable.strip() 
				except:
					pass
				
		info.append({'File':file_tag, 'Exif':exif_tag})

	module.print_n("[main] dumping pickle")
	pickle.dump( info, open( file_data, "wb" ) )
	return
	
def ayuda():
	print '''Use -h para ayuda'''
	
if __name__ == '__main__':	
		parser = OptionParser()
		parser.add_option('-d', '--directorio', dest='DIR', help='[OBLIGATORIO] Directorio a leer')
		parser.add_option('-r', '--recursivo', dest='RECURSIVO', action="store_true", default=False, help='recorrer directorio en modo recursivo')
		parser.add_option('-v', '--verbose', action="store_true", dest="verbose", default=False, help='Activar salida de mensajes por consola')	
		parser.add_option('-c', '--copiar', dest='COPIAR', action="store_true", default=False, help='copiar imagenes')


		
		(opts, args) = parser.parse_args()
		
		
		if opts.DIR is None:
			ayuda()
			sys.exit(1)
		
		if not os.path.exists(opts.DIR):			
			ayuda()
			sys.exit(1)
		
		file_data = getFileData()
		if os.path.exists(file_data):
			os.remove(file_data)	

		main(opts)
		# verFichero()
		if opts.COPIAR:
			copiarImagenes(opts)

	


