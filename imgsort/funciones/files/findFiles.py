#!/usr/bin/python

import os

def get_files_yield(dir=None, filtro=None): 
	if dir is not None and os.path.exists(dir):
		if filtro is None:
			for filename in os.listdir(dir):
				if os.path.isfile(os.path.join(dir, filename)):
					yield os.path.join(dir, filename)
		else:
			for filename in os.listdir(dir):
				if os.path.isfile(os.path.join(dir, filename)):
					base, ext = os.path.splitext(filename)					
					if ext.lower() in filtro:
						yield os.path.join(dir, filename)

						
						
def get_files_recursive_yield(dir=None, filtro=None):	
	if dir is not None and os.path.exists(dir):
		if filtro is None:
			for root, dirnames, filenames in os.walk(dir):
				for filename in filenames:
					yield os.path.join(root, filename)
		else:
			for root, dirnames, filenames in os.walk(dir):
				for filename in filenames:
					base, ext = os.path.splitext(filename)					
					if ext.lower() in filtro:	
						yield os.path.join(root, filename)


def get_files(dir=None, filtro=None):
	if dir is None:
		return None
	
	matches = []		
	for filename in os.listdir(dir):
		if os.path.isfile(os.path.join(dir, filename)):
			if filtro is None:
				matches.append(os.path.join(dir, filename))
			else:
				base, ext = os.path.splitext(filename)
				if ext.lower() in filtro:
					matches.append(os.path.join(dir, filename))

	return matches

					
	
def get_files_recursive(dir=None, filtro=None):
	if dir is None:
		return None
		
	matches = []
	for root, dirnames, filenames in os.walk(dir):		
		for filename in filenames:
			if filtro is None:
				matches.append(os.path.join(root, filename))
			else:
				base, ext = os.path.splitext(filename)
				if ext.lower() in filtro:					
					print_n("[get_files] {:60}".format(filename))
					matches.append(os.path.join(root, filename))
			
	return matches