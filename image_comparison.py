import numpy as np
import csv
from file_manager import createFile




def colorCompare(fileColor, tileColor, weights):	
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

def storeFilePaths(picFile, tileFile, mapFile, ss, weights, unit):

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