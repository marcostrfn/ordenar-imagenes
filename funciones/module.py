
import os
import ConfigParser

def uno():
    print 'uno'

def print_n(string):
    import sys
    sys.stdout.write("{}\r".format(string))
    sys.stdout.flush()
	
def get_data_config(file_config = None):

	if file_config is None:
		file_config = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','config.ini')	

	# configuracion
	config = ConfigParser.ConfigParser()	
	config.read(file_config)
		
	# print config.sections()
	dir_mode = config.get('directories', 'mode')		
	

	if dir_mode == 'relative':
		dir_source = os.path.join(os.path.abspath(os.path.dirname(__file__)),config.get('directories', 'source'))
		dir_dest = os.path.join(os.path.abspath(os.path.dirname(__file__)),config.get('directories', 'dest'))
		

	elif dir_mode == 'absolute':
		dir_source = config.get('directories', 'source')
		dir_dest = config.get('directories', 'dest')		
				
	if not os.path.exists(dir_source):
		os.makedirs(dir_source)

	if not os.path.exists(dir_dest):
		os.makedirs(dir_dest)	
	
	types = config.get('files', 'type').split(",")   	
	
	return dir_source, dir_dest, types
	
	
	
	
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

			
