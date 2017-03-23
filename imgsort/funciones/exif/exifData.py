#!/usr/bin/python

import exifread
import os
import re
import json


class ExifExtractor:
	''' Extrae datos exif de una imagen '''
	
	def __init__(self, file):
		self.file = file
		self.exif_tags = {}
		self.exif_file = {}
		self.tags = None
	
		self.__extract()
		self.__setFileInfo()
		self.__setExifInfo()
	
	
	def __extract(self):
		''' cargar datos exif de un imagen '''
		f = open(self.file, 'rb')
		self.tags = exifread.process_file(f)
		f.close()

		
	def __setFileInfo(self):
		''' cargar informacion del fichero '''
		self.exif_file['filename'] = os.path.basename(self.file)
		self.exif_file['dirname'] = os.path.dirname(self.file)
	
	
	def __setExifInfo(self):
		''' parsear datos exif excepto thumb '''
		for tag in sorted(self.tags.keys()):
			match = re.search("thumb", tag, re.IGNORECASE)
			if not match:
				try:
					self.exif_tags[tag] = self.tags.get(tag).printable.strip()
				except:
					pass

	def getFilename(self):
		return os.path.basename(self.file)

	def getDirname(self):
		return os.path.dirname(self.file)
		
	def getExifData(self):
		return { 'file': self.exif_file, 'exif': self.exif_tags }
	
	def getExifJson(self):
		return json.dumps({ 'file': self.exif_file, 'exif': self.exif_tags })
		
	def getExifPrettyJson(self):
		return json.dumps({ 'file': self.exif_file, 'exif': self.exif_tags },
			sort_keys=True, indent=4, separators=(',', ': '))
		
		
	def hasTag(self, code, tag):
		s = "^(%s){1}\s(%s){1}" % (code, tag,)
		for exif in self.exif_tags:
			match = re.search(s , exif, re.IGNORECASE)
			if match: return True
		
		return None
	
	def getTag(self, code, tag):
		s = "%s %s" % (code,tag,)
		return self.exif_tags[s]

	def getDateTimeOriginal(self):
		if self.hasTag('EXIF', 'DateTimeOriginal') is None:
			return None
		
		dateTimeOriginal = self.getTag('EXIF', 'DateTimeOriginal').replace(' ','_').replace(':','-')
		if dateTimeOriginal == "0000-00-00_00-00-00":
			return None
		
		s = "^([0-9]{4})-([0-9]{2})-([0-9]{2})_([0-9]{2})-([0-9]{2})-([0-9]{2})"
		match = re.search(s , dateTimeOriginal, re.IGNORECASE)
		if match is None:
			return None
		
		return dateTimeOriginal
