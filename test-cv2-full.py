

# Python 2/3 compatibility
from __future__ import print_function


import sys
import os
import re

from funciones.files.findFiles import get_files_yield




import numpy as np
import cv2


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':
    import sys
    from glob import glob
    import itertools as it

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    
    lista = get_files_yield('img')
    
    for fn in lista:   
        print (fn)		
        if re.search('out', fn):
			continue
            
        try:
            img = cv2.imread(fn)
            if img is None:
                print('Failed to load image file:', fn)
                continue
        except:
            print('loading error')
            continue

        found, w = hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
        found_filtered = []
        for ri, r in enumerate(found):
            for qi, q in enumerate(found):
                if ri != qi and inside(r, q):
                    break
            else:
                found_filtered.append(r)
                
        draw_detections(img, found)
        draw_detections(img, found_filtered, 3)
        
            
        dir_nombre = os.path.dirname(fn)
        nuevo_nombre = os.path.basename(fn);
        nombre,extension = os.path.splitext(nuevo_nombre)
        nombre_final = os.path.join(dir_nombre,"out-{}.{}".format(nombre,extension))
        
        print('{} {} {} found'.format(nombre, len(found_filtered), len(found)))
        
        cv2.imwrite(nombre_final, img)
            
        # cv2.imshow('img', img)
        #ch = cv2.waitKey()
        # if ch == 27:
            #   break
            
                
                
    cv2.destroyAllWindows()
