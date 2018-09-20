from google_images_download import google_images_download   #importing the library
import os 
import sys

# Searches google images for tile pictures and downloads them
def googlesearch(tilename, imgDirectory):
	
	colors = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'teal', 'white', 'yellow']

#   Number of pictures downloaded corresponding to each color option 
	colorcount = 30
	counter = 0

	for i in range(0, len(colors)):
# 		class instantiation
		response = google_images_download.googleimagesdownload()   
	
# 		creates list of arguments for google search
		arguments = {"keywords": tilename,"limit":colorcount,"print_urls":False, "color": colors[i]}   
		paths = response.download(arguments)   
# 		list of file paths for colors[i]
		fileList = paths[tilename]

# 		renames the files by increasing order with which they were downloaded
		for imgName in fileList:
			try:
				os.rename(imgName, imgDirectory + "pic__" + str(counter) + ".jpg")
			except FileNotFoundError:
				continue 
			counter+=1
	
