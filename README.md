# Photographic Mosaic
This program is designed to create a photographic mosaic, which is a photograph that is pixelated into a mosaic and each pixel region 
contains a new picture. More can be read on the Wikipedia page, which gives an example (https://en.wikipedia.org/wiki/Photographic_mosaic).

# Procedure

The Python file, mosaic.py, takes in the path to what the user wants to be the "main photograph" as well as well as either a path to a directory 
containingimages that the user wants to be possible tiles or it takes a subject phrase, searches google images, downloads the images 
corresponding to said subject, and filters by the color palette on google. The google search and download process is run by the getimgs.py
file, which uses the "google-images-download" code from (https://github.com/hardikvasa/google-images-download). 

When the final image library has been created (or inputed by the user), mosaic.py then refits the main image such that there will be a
positive integer number of tiles in each row and column. It then loops through the main picture in order to find the dominant color of 
each square region. This process is performed by Python's sci-kit learn Kmeans clustering algorithm, which breaks the possible amount of 
RGB colors used into four groups (specified by RGB color values) and then selects the three most dominant. These color values are then stored
in a .csv file. This same process of searching for color groups and saving the top three is also performed for the image library.

The Python file mosaic.py matches the main picture tiles with images in the image library by
finding the Euclidean distance between the most dominant RGB color of each, between the second most dominant RGB 
color of each, and the between the third as well. The program then find the weighted average of the three. I found that a good weight
choice of weights is 10, 7, and 3 corresponding to the three most dominant colors in decreasing order. I feel that this is dependent on 
the color distribution of the image and how many unique color groups there are. When the weighted averges between all of the pictures 
in the image library and the main image have been computed - the program then saves the minimum average in a .csv file. 

The program concludes with pasting the images by order with which they are in the .csv file containing the paths of each image in the library
that corresponds to a tile. 

Comments and examples:

This program runs has been run with a few examples given below. 
  

My first
