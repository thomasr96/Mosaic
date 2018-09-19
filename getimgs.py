from google_images_download import google_images_download   #importing the library
import os 
import sys
def googlesearch(tilename, imgDirectory):
	colors = ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'teal', 'white', 'yellow']

# 	pathlist = [["" for i in range(0, max(colorcount))] for j in range(0, max(colorcount))]

# 	colorcounttemp = colorcount
	colorcount = 50
	counter = 0
	cur_dur = os.getcwd()
	i = 0
	for i in range(0, len(colors)):

		response = google_images_download.googleimagesdownload()   #class instantiation
	

		arguments = {"keywords": tilename,"limit":colorcount,"print_urls":False, "color": colors[i], "chromedriver": cur_dur}   #creating list of arguments
		paths = response.download(arguments)   #passing the arguments to the function
	
		fileList = paths[tilename]
		
		for imgName in fileList:
			try:
				os.rename(imgName, imgDirectory + "pic__" + str(counter) + ".jpg")
			except FileNotFoundError:
				continue 
			counter+=1
	
# 	print(paths)
