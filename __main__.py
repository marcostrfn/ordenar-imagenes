
import os
import sys
import re

import exifread
import pickle
import json


from funciones import module

def verFichero():
	
	file_data = module.get_data_data()
	info = pickle.load(open( file_data, "rb" ))
	for line in info:
		print json.dumps(line, indent=4, sort_keys=True)		
		if "Image XResolution" in line:
			print line[r'Image XResolution']
	



def main():
	
	info = []	
	
	dir_source, dir_dest, dir_data, file_data, types = module.get_data_config()			
	files = module.get_files(dir_source, types)
	
	for file in files:
		print file
		# print "=" * len(file)

		# Open image file for reading (binary mode)
		# and return Exif tags
		f = open(file, 'rb')
		tags = exifread.process_file(f)
		f.close()

		new_tag = {}
		new_tag['filename'] = os.path.basename(file)
		new_tag['dirname'] = os.path.dirname(file)
		
		for tag in sorted(tags.keys()):
			match = re.search("thumb", tag, re.IGNORECASE)
			if not match:
				new_tag[tag] = tags.get(tag).printable
				# match = re.search("^(EXIF|image){1}\s(model|datetimeoriginal){1}", tag, re.IGNORECASE)
				# if match:					
					# new_tag.append((tag,tags.get(tag).printable))
					# print ("{0:20}\t\t{1}".format(tag, tags[tag]))
		
		# print
		info.append(new_tag)

	
	pickle.dump( info, open( file_data, "wb" ) )
	return
	
		
if __name__ == '__main__':
	main()
	verFichero()
