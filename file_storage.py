import numpy as np
import sys
import csv
import glob
import csv
import cv2
from sklearn.cluster import KMeans
from file_manager import createFile

def getDomColor(tempfile, cNum):
# 	reshape the picture as a linear array such that each row corresponds to a new pixel
# 	and each column in said row refers to a B,G, or R value, respectively 
	
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