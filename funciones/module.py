
import os

def uno():
    print 'uno'
	
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
					matches.append(os.path.join(root, filename))
			
	return matches

			
