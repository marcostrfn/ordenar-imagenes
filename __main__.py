
import os
import sys
import re

import exifread
import pickle
import json
from shutil import copyfile

from funciones import module


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

		
		
def copiarImagenes():
	file_data = getFileData()
	if file_data is None:
		return None
		
	dir_source, dir_dest, types = module.get_data_config()
	info = pickle.load(open( file_data, "rb" ))
	for line in info:
		dateTime = None
		for exif in line["Exif"]:			
			match = re.search("^(EXIF){1}\s(datetimeoriginal){1}",exif, re.IGNORECASE)						
			if match: # existe EXIF dateTimeOriginal				
				dateTime = line["Exif"][exif].replace(' ','_')
				# file_src = os.path.join(line["File"]["Dirname"], line["File"]["Filename"])
				# file_des = os.path.join(dir_dest,  line["Exif"][exif].replace(' ','_'))
				# copyfile(file_src,file_des)
				break
		
		if dateTime is not None:
			file_name = dateTime
		else:
			file_name = line["File"]["Filename"]
			
		
		
def main(file_data=None):
	file_data = getFileData()
	if file_data is None:
		return None
		
	info = []	
	
	dir_source, dir_dest, types = module.get_data_config()			
	files = module.get_files(dir_source, types)
	
	for file in files:		
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
				exif_tag[tag] = tags.get(tag).printable.strip() 
				# match = re.search("^(EXIF|image){1}\s(model|datetimeoriginal){1}", tag, re.IGNORECASE)
				# if match:					
					# new_tag.append((tag,tags.get(tag).printable))
					# print ("{0:20}\t\t{1}".format(tag, tags[tag]))
				
		info.append({'File':file_tag, 'Exif':exif_tag})

	
	pickle.dump( info, open( file_data, "wb" ) )
	return
	
		
if __name__ == '__main__':
	file_data = getFileData()
	if os.path.exists(file_data):
		os.remove(file_data)	

	main()
	# verFichero()
	copiarImagenes()
