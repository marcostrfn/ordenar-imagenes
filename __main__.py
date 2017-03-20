
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
        os.makedir(dir_data)

    file_data = os.path.join(dir_data,'data.p')
    return file_data


def verFichero():
    file_data = getFileData()
    info = pickle.load(open( file_data, "rb" ))
    for line in sorted(info):
        print json.dumps(line, indent=4, sort_keys=True)
        # if "Image XResolution" in line: print line[r'Image XResolution']


def main(opts):
    file_data = getFileData()
    if file_data is None:
        return None

    dir_source = opts.dir_source
    types = opts.types.split(",")

    if opts.RECURSIVO:
        files = module.get_files_recursive(dir_source, types)
    else:
        files = module.get_files(dir_source, types)

    
    total_files = len(files)
    info = []
    num_file = 0

    for file in files:
        num_file += 1
        module.print_n("[main] parsing file {} de {}".format(num_file, total_files))
		
        exif = ExifExtractor(file)
        info.append(exif.getExifData())
        if exif.hasTag('EXIF', 'DateTimeOriginal'):
            if opts.COPIAR: 
                dir_dest = opts.dir_dest
                line = exif.getExifData()
                dateTime = exif.getDateTimeOriginal()
                
                if dateTime is not None:
                    extension = os.path.splitext(line["file"]["filename"])[1][1:]
                    file_name = "{}.{}".format(dateTime, extension)
                else:
                    file_name = line["file"]["filename"]

                file_src = os.path.join(line["file"]["dirname"], line["file"]["filename"])
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
                module.print_n("[copiarImagenes] {} {} => {}".format(num_file, line["file"]["filename"],file_name))
                
    pickle.dump( info, open( file_data, "wb" ) )
    module.print_n("[main] finalizado")

    return

def ayuda():
    print '''Usage: ordenar-imagenes-optionparse [options]

Options:
  -h, --help            show this help message and exit
  -s DIR_SOURCE, --source=DIR_SOURCE
                        [OBLIGATORIO] directorio a leer
  -d DIR_DEST, --dest=DIR_DEST
                        [OBLIGATORIO] directorio destino
  -t TYPES, --types=TYPES
                        [OBLIGATORIO] tipo de fichero a leer
  -r, --recursivo       recorrer directorio en modo recursivo
  -v, --verbose         Activar salida de mensajes por consola
  -c, --copiar          copiar imagenes a DIR_DEST renombradas'''
  

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-s', '--source', dest='dir_source', help='[OBLIGATORIO] directorio a leer')
    parser.add_option('-t', '--types', dest='types', help='[OBLIGATORIO] tipo de fichero a leer')
    parser.add_option('-r', '--recursivo', dest='RECURSIVO', action="store_true", default=False, help='recorrer directorio en modo recursivo')
    parser.add_option('-v', '--verbose', dest="VERBOSE", action="store_true", default=False, help='Activar salida de mensajes por consola')
    parser.add_option('-c', '--copiar', dest='COPIAR', action="store_true", default=False, help='copiar imagenes a DIR_DEST renombradas')
    parser.add_option('-d', '--dest', dest='dir_dest', help='[OBLIGATORIO con opcion COPIAR] directorio destino')
    
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

    if opts.COPIAR:
        if opts.dir_dest is None:
            ayuda()
            sys.exit(1)
            
        if not os.path.exists(opts.dir_dest):
            os.makedirs(opts.dir_dest)

    file_data = getFileData()
    if os.path.exists(file_data):
        os.remove(file_data)

    main(opts)