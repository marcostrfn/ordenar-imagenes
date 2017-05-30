
import sys
import os
import numpy as np
import cv2


from imgsort.funciones.files.findFiles import get_files_yield



def carita(file):

	dir_nombre = os.path.dirname(file)
	nuevo_nombre = os.path.basename(file);
	nombre,extension = os.path.splitext(nuevo_nombre)
	
	nombre_final = os.path.join(dir_nombre,"out","{}.{}".format(nombre,extension))
	
	lista = [(file,nombre_final)]

	for img_source,img_result in lista:
		img = cv2.imread(img_source)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)	
		print img_source, len(faces)
		for (x,y,w,h) in faces:
			print 'face', x,y,w,h,
			img2 = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)			
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			
			eyes = eye_cascade.detectMultiScale(roi_gray)
			print 'eye', len(eyes)
			for (ex,ey,ew,eh) in eyes:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

		
		if len(faces) > 0:
			cv2.imwrite(img_result, img)
			# cv2.imshow('img',img)
			# cv2.waitKey(0)
			
		cv2.destroyAllWindows()
		


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

lista = get_files_yield('/media/ubuntu/DATA/imagenes/face')
for file in lista:
	carita(file)
