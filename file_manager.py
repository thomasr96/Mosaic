import glob
import cv2
import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance


def fileCheck(path, source):

	for picName in glob.glob(path + '*.jpg'):
		try:
			Image.open(picName)
		except IOError:
			if source == "library":
				print(picName + " could not be opened. Consider removing it from the image library.")
				sys.exit(0)
			else:
				os.remove(picName)

def createFile(fileName):
	cur_dur = os.getcwd()
	if fileName in os.listdir(cur_dur):
		os.remove(fileName)
	
	return open(fileName, "w+")