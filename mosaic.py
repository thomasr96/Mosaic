import sys
import os 
import time
import glob
import numpy as np
from sklearn.cluster import KMeans
import cv2
import csv
import imutils
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from getimgs import googlesearch
from argumentFinder import getArgs


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

def fileCheck(path, source):
	
	for picName in glob.glob(path + '*'):
		try:
			Image.open(picName)
		except IOError:
			if source == "library":
				print(picName + " could not be opened. Consider removing it from the image library."
				sys.exit(0)
			else:
				os.remove(picName)

def createFile(fileName):
	cur_dur = os.getcwd()
	if fileName in os.listdir(cur_dur):
		os.remove(fileName)
	
	return open(fileName, "w+")

##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
def getDomColor(tempfile, cNum):
# 	reshape the picture as a linear array such that each row corresponds to a new picture
# 	and each column refers to a B,G, or R value, respectively 
	
	tempfile = tempfile.reshape((tempfile.shape[0] * tempfile.shape[1], 3))
# 	Cluster the color values
	clt = KMeans(n_clusters = cNum)
	clt.fit(tempfile)
	
	hist = np.histogram(clt.labels_, bins = np.arange(cNum))[0]

	color = [[0, 0, 0] for n in range(0,3)]
	maxEl = [0]*3
	
# 	Find the three colors that are used most in the picture and store in color[] 
# 	with decreasing frequency	
	for ii in range(0,3):

		maxEl[ii] = np.where(hist == max(hist))[0][0]
		hist = np.delete(hist, maxEl[ii])
		color[ii] = list(clt.cluster_centers_[maxEl[ii]])

	return [str(c) for f in color for c in f]
	
##########################################################################################

def storePicFile(picFile, unit, file, mult,ss,cNum):

	
	datafile = createFile(picFile)

	print("Getting picture colors")
	
	for j in range(0,ss[0], unit):
		for i in range(0,ss[1], unit):
# 			Retrieve picture region	
			tempfile = file[j:(j+unit), i:(i+unit)]
# 			Retrieve three most dominant colors of region
			features = getDomColor(tempfile, cNum)
# 			write most dominant colors to .csv file
			datafile.write("%s\n" % (','.join(features)))
		
	datafile.close()


##########################################################################################

def storeTileFile(tileFile, unit, mult,ss,cNum, path):
	unit1 = 50
	
	print("Getting tile colors")
	
	datafile = createFile(tileFile)
	

# 	loop through picture tile library
	for picName in glob.glob(path + '*'):
# 		Retrieve picture that is to be used as a possible tile in mosaic
# 		and resize it such that the dimensions are not too small
# 		print(picName)	
		try:
			tempfile = cv2.resize(cv2.imread(picName), (unit1,unit1))
		except cv2.error:
			continue
# 		Retrieve three most dominant colors of region
		try:
			features = getDomColor(tempfile, cNum)
		except ValueError:
			continue
		datafile.write("%s,%s\n" % (picName, ',' .join(features)))
		
	datafile.close()
	
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

def colorCompare(fileColor, tileColor, weights):
# 	weights = [5.0/10,4.0/10,1.0/10]
	
	sumW8 = np.sum(np.array([float(num) for num in weights]))
	w8s = [float(c)/sumW8 for c in weights]
	colorMult = [3,4,2]
	dist = 0
	for iii in range(0,3):
		dist1 = 0
		for jjj in range(0,3):
			dist1 += (colorMult[jjj]*(fileColor[iii][jjj] - tileColor[iii][jjj]))**2
		dist += w8s[iii]*dist1
	return dist

##########################################################################################

def colorCompare_lowcost(fileColor, tileColor, weights):
	# weights = [10/22,8/22,4/22]
	sumW8 = np.sum(np.array([float(num) for num in weights]))
	w8s = [float(c)/sumW8 for c in weights]
	dist = 0
	for picNum in range(0,3):
		rBar = (fileColor[picNum][2] + tileColor[picNum][2])/2.0
		delR = (fileColor[picNum][2] - tileColor[picNum][2])**2
		delG = (fileColor[picNum][1] - tileColor[picNum][1])**2
		delB = (fileColor[picNum][0] - tileColor[picNum][0])**2
		dist += w8s[picNum]*((2.0+rBar/256.0)*delR+4.0*delG+(2.0+(255.0-rBar)/256.0)*delB)
		
	return dist

##########################################################################################


def storeFilePaths(mapFile, ss, weights):

	print("Comparing distances")
	
	datafile = createFile(mapFile)

	county = 0
	
	fileColor = [[0,0,0] for i in range(0,3)]

	with open(picFile, "r") as f1:
		reader1 = csv.reader(f1)
	
		countx = -1
# 		Loop through each row in file of picture region BGR values	
		for row1 in reader1:
	
			countx += 1
# 			Reset count when the region at the end of each row in the main picture is reached
			if countx == ss[1]/unit:
				countx = 0
				county+=1
# 			Retrieve the three BGR values in each row 
			for i in range(0,3):
				fileColor[i] = [float(row1[i*3]), float(row1[i*3+1] ), float(row1[i*3+2])] 
		
			minD = -1

			with open(tileFile, "rU") as f2:
				reader2 = csv.reader(f2, dialect='excel')
# 				Loop through each row in file of possible picture tiles
				for row2 in reader2:
					tileColor = [[0,0,0] for i in range(0,3)]
# 					Retrieve the three BGR values of each possible picture tile 
					for ii in range(0,3):	
						tileColor[ii] = [float(row2[i*3+n]) for n in range(1,4)]
					

					if minD == -1:
# 						retrieve distance between the colors of the regions and possible tile pictures
						dist = colorCompare_lowcost(fileColor, tileColor, weights)						
						minD = dist
# 						Store the path to the tile picture file with the minimum distance
						minF = row2[0]
						
					else:
						dist = colorCompare_lowcost(fileColor, tileColor, weights)
						if dist < minD:
							minD = dist
							minF = row2[0]

				datafile.write("%s\n" % minF)
	f2.close()
	f1.close()


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

def printMosaic(filename, mult, unit, weights):
	print("here we go")
	
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
##########################################################################################
##########################################################################################
##########################################################################################
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
	for jjj in range(0,len(mult):
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
			print(str(weights[jj]))
		# 	resize picture to fit an integer number of tiles
			for i in range(0,2):
				ss[i] = (file.shape[i]*mult[jjj] - (file.shape[i]*mult[jjj] % unit))
			file = cv2.resize(file, (ss[1], ss[0])) 
			
			print(ss)
			
		# 	Retrieve and store dominant pixel region values in main picture 
			if jj == 0:	
				storePicFile(picFile, unit, file, mult[jjj],ss, cNum)
		#	fileCheck(path)
		# 	Retrieve and store dominant pixel region values of the possible tile pictures 
			storeTileFile(tileFile, unit, mult[jjj],ss, cNum, path)
		#   Find the tile photos with colors closest to the pixel regions and store their file paths
			storeFilePaths(mapFile,ss, weights[jj])
		# 	Retrieve file paths of stored to-be tile photos, paste them onto the mosaic, and print said mosaic 
			printMosaic(filename, mult[jjj], unit, weights[jj])
			time1 = str(time.localtime()[3]) + ":" + str(time.localtime()[4])
			
			print("Time start: " + time0 + "\n\nTime end: " + time1)
			
# 			Remove the downloads folder if image library was retrieved by google
			if arguments["tile"] == None:
				os.remove(path)
# 		    Code to display image in cv2
		# 	cv2.imshow('image', file)
		# 	cv2.waitKey(0)
		# 	cv2.destroyAllWindows()
		# 	sys.exit(0)
		
	
	
	
	
	
	
	
	
	
