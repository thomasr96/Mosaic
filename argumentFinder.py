import argparse
import glob
import cv2
import sys

# construct the argument parser and parse the arguments
def getArgs():
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--picture", required = True,
		help = "Path and filename to the target image")
	ap.add_argument("-t", "--tile", required = False,
		help = "Subject with which the program is to search images for")
	ap.add_argument("-l", "--library", required = False,
		help = "Path to directory of tile images")
	args = vars(ap.parse_args())

	if (args['tile'] == None) and (args['library'] == None):
		print("User must include either a tile image subject in the form: \n-t \"subject\""+
		"\nOr a path to directory with an image library of possible tiles in the form: \n-l \"path to directory\"" )
		sys.exit(0)
		
	return args
# 	if args['tile'] == None:
# 		tile = "false"
# 		library = args["library"]
# 	else:
# 		tile = args["tile"]
# 		library = "false"