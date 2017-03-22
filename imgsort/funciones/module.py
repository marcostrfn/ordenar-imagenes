
import os
import sys
import ConfigParser

def uno():
	print 'uno'

	
	
def getTerminalSizeW():
	from ctypes import windll, create_string_buffer

	# stdin handle is -10
	# stdout handle is -11
	# stderr handle is -12

	h = windll.kernel32.GetStdHandle(-12)
	csbi = create_string_buffer(22)
	res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

	if res:
		import struct
		(bufx, bufy, curx, cury, wattr,
		 left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
		sizex = right - left + 1
		sizey = bottom - top + 1
	else:
		sizex, sizey = 80, 25 # can't determine actual size - return default values

	return sizex, sizey

def getTerminalSize():
	import os
	env = os.environ
	def ioctl_GWINSZ(fd):
		try:
			import fcntl, termios, struct, os
			cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
		'1234'))
		except:
			return
		return cr
	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
	if not cr:
		try:
			fd = os.open(os.ctermid(), os.O_RDONLY)
			cr = ioctl_GWINSZ(fd)
			os.close(fd)
		except:
			pass
	if not cr:
		cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

		### Use get(key[, default]) instead of a try/catch
		#try:
		#	 cr = (env['LINES'], env['COLUMNS'])
		#except:
		#	 cr = (25, 80)
	return int(cr[1]), int(cr[0])

	
def mprint(string):
	w,h = getTerminalSizeW()
	f = w - 4
	s = "{:%s}{:%s}\r" % (f,3)
	# s = "{:%s}{:%s}\n" % (f,3)
	sys.stdout.write(s.format(string,"[+]"))
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
		dir_dest = os.path.join(os.path.abspath(os.path.dirname(__file__)),config.get('directories', 'dest'))
		

	elif dir_mode == 'absolute':
		dir_dest = config.get('directories', 'dest')		
				
	if not os.path.exists(dir_dest):
		os.makedirs(dir_dest)	
	
	types = config.get('files', 'type').split(",")		
	
	return dir_dest, types
	
	
	
	


			
