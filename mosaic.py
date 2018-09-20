import sys
import os 
import time
import numpy as np
import cv2
import csv
import imutils
from PIL import Image, ImageFont, ImageDraw, ImageEnhance  

from argument_finder import getArgs
from getimgs import googlesearch
from image_comparison import colorCompare, colorCompare_lowcost, storeFilePaths
from file_storage import getDomColor, storePicFile, storeTileFile
from file_manager import fileCheck 



##########################################################################################

def printMosaic(filename, mult, unit, weights):
	print("Assembling photographic mosaic - starting count")
	
	counter = 0
	counterx = 0
	countery = 0
	
	lastFile = Image.open(filename)
	
	s = lastFile.size
	sss = [0]*2
	for i in range(0,2):
		sss[i] = (s[i]*mult - (s[i]*mult % unit))
# 	lastFile = lastFile.resize(sss)
	lastFile = Image.new("RGB", sss, "white")
	start_time = time.time()
	
	with open(mapFile, "r") as f1:
		reader1 = csv.reader(f1)
#	 	Loop through the stored file paths		
		for row in reader1:

			if counterx == sss[0]/unit:
				counterx = 0
				countery += 1
			
			file1 = Image.open(row[0])
# 			Resize each tile picture to the desired dimension
			file2 = file1.resize((unit,unit))
# 			Paste the resized tile picture onto the mosaic
			lastFile.paste(file2, (unit*counterx, unit*countery, unit*counterx+unit, unit*countery+unit))

			if counter % 100 == 0:
				print(counter)
				print(time.time() - start_time)
				print("\n")
			counter+=1
			counterx+=1

	sumW8 = np.sum(np.array([float(num) for num in weights]))
	w8String = "_".join([str(c) + "-" + str(int(sumW8)) for c in weights])
	
	lastFile.save(filename[0:filename.find(".")] + "cost_metric" + w8String + "_mult=" + str(mult) + ".JPEG", 'JPEG', quality=95)

##########################################################################################

if __name__ == '__main__':
	

	
	arguments = getArgs()
	
	filename = arguments["picture"]
	
	if arguments["tile"] == None:
		library = arguments["library"]
	else:
		tilename = arguments["tile"]
	


	weights = [["10","7", "3"]]
# 	Multiplier to resize the mosaic 
	mult = [20]
	for jjj in range(0,len(mult)):
		for jj in range(0,len(weights)):
			time0 = str(time.localtime()[3]) + ":" + str(time.localtime()[4])
			
			print("Start time: " + time0)
				
			
			picFile = "picFiles.csv"
			mapFile = "mapFile.csv"
			tileFile = "tileFiles.csv"

# 			tile size 
			unit = 30
 	
# 		 	Number of clusters for color clustering
			cNum = 4
			
			
			if arguments["tile"] == None:
				path = arguments["library"]
				if not(path[len(path)-1] == "/"):
					path += "/"
				fileCheck(path, "library")
			else:
				path = os.getcwd() + "/downloads/"
				print("Getting Images")
				googlesearch(tilename, path)
				fileCheck(path, "subject")
			
			file = cv2.imread(filename)

			ss = [0]*2
# 			dimensions 	
			print(str(weights[jj]))
		# 	resize picture to fit an integer number of tiles
			for i in range(0,2):
				ss[i] = (file.shape[i]*mult[jjj] - (file.shape[i]*mult[jjj] % unit))
			file = cv2.resize(file, (ss[1], ss[0])) 
			
			print(ss)
			
		# 	Retrieve and store dominant pixel region values in main picture 
			if jj == 0:	
				storePicFile(picFile, unit, file, mult[jjj],ss, cNum)

		# 	Retrieve and store dominant pixel region values of the possible tile pictures 
			storeTileFile(tileFile, unit, mult[jjj],ss, cNum, path)

		#   Find the tile photos with colors closest to the pixel regions and store their file paths
			storeFilePaths(picFile, tileFile, mapFile,ss, weights[jj], unit)

		# 	Retrieve file paths of stored to-be tile photos, paste them onto the mosaic, and print said mosaic 
			printMosaic(filename, mult[jjj], unit, weights[jj])

			time1 = str(time.localtime()[3]) + ":" + str(time.localtime()[4])
			
			print("Time start: " + time0 + "\n\nTime end: " + time1)
			

# 	 Code to display image in cv2
		# 	cv2.imshow('image', file)
		# 	cv2.waitKey(0)
		# 	cv2.destroyAllWindows()
		# 	sys.exit(0)
		
	
	
	
	
	
	
	
	
	
