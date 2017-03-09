
import os
import exiftool

from funciones import module


def main():
	
	dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'img')	
	matches = module.get_files(dir, [".png"])
		
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
		


if __name__ == '__main__': main()
