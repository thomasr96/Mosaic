# Photographic Mosaic
This program is designed to create a photographic mosaic, which is a photograph that is pixelated into a mosaic and each pixel region 
contains a picture. More can be read on the [Wikipedia page](https://en.wikipedia.org/wiki/Photographic_mosaic), which gives an example.

The user specifies an image to be used as the "main image" of the mosaic and can either specify the path to an image library for the possible mosaic tiles or input a subject so that the program will search for and download images from Google Images to create a usable image library. 

## How to Run

The user must first have at least Python 2.7.13 installed on their machine - the program runs on Python 3.x as well. The program additionally requires the following Python modules: numpy, sklearn, cv2, imutils, and PIL. Additionally, one must clone and download the [Github repository from Hardikvasa](https://github.com/hardikvasa/google-images-download). The directory from this repository titled, "google_images_download", must be included in the directory with the mosaic program. The program is run in a command line interface. 

If running the program with an existing image library, then specify the path to the main image with ` -p ` and the path to the image library directory with ` -l `, the following is an example.
```
python mosaic.py -p "/path/beach.jpg" -l "/path/img_library_directory"
```
If you wish the program to create an image library using Google Image search, then specify the path to the main image with ` -p ` and the subject to  ` -t `, the following is an example.
```
python mosaic.py -p "/path/musician.jpg" -t "violin"
```
## Examples

* My test image throughout this project has been the following image of Jesus Christ with "doves" as the subject

   ![alt text](https://imgur.com/J1Qyfbk.jpg "Main Image Target")
   <img src="ihttps://imgur.com/J1Qyfbk.jpg" width="40%">
  * I used the following weighting schemes (discussed in next section), given in brackets in decreasing order of dominance for each color group 
    * Cost metric weights [10/17,4/17,3/17]  
      ![alt text](https://i.imgur.com/yWUr7NB.jpg)
    * Cost metric weights [10/20,5/20,5/20]  
      ![alt text](https://i.imgur.com/yWUr7NB.jpg)
    * Cost metric weights [6/10,4/10, 0/10]  
      ![alt text](https://i.imgur.com/yWUr7NB.jpg)
      
* The second test image was the following photo of a wheel on a motorcycle with "falcon" as the subject

   ![alt text](https://i.imgur.com/v6g5npL.jpg "Main Image Target")
  * I used the following weighting schemes, given in brackets in decreasing order of dominance for each color group 
  
    * Cost metric weights [10/17,5/17,2/17] with photo multiplier = 30  
      ![alt text](https://i.imgur.com/7AQFA68.jpg)
    * Cost metric weights [10/20,7/20,3/20] with photo multiplier = 30  
      ![alt text](https://i.imgur.com/ZgYA825.jpg)
    * Cost metric weights [10/22,8/22,4/22] with photo multiplier = 30  
      ![alt text](https://i.imgur.com/Dn57H2s.jpg)

* I also attempted the full sized photo with which the wheel photo was cropped from

  ![alt text](https://i.imgur.com/INQc4An.jpg "Main Image Target")
  * Cost metric weights [10/17,5/17,2/17] with photo multiplier = 30  
      ![alt text](https://i.imgur.com/B7kQJbi.jpg)
      
* The last test image was the following photo of a daisy flower with "flower" as the subject

   ![alt text](https://i.imgur.com/58AGP2W.jpg "Main Image Target")
  * I used the following weighting schemes, given in brackets in decreasing order of dominance for each color group 
    * Cost metric weights [10/16,4/16,2/16] with photo multiplier = 15  
      ![alt text](https://i.imgur.com/R0FwbwG.jpg)
    * Cost metric weights [10/20,7/20,3/20] with photo multiplier = 15  
      ![alt text](https://i.imgur.com/4Ca1IaT.jpg)
    * Cost metric weights [10/27,9/27,8/27] with photo multiplier = 15  
      ![alt text](https://i.imgur.com/ytPcYYx.jpg)

## Procedure

The Python file, mosaic.py, takes in the path to what the user wants to be the "main photograph" as well as well as either a path to a directory containing images that the user wants to be possible tiles or it takes a subject phrase, searches Google Images, downloads the images corresponding to said subject, and filters by the color palette on Google. The Google search and download process is run by the getimgs.py file, which uses the ["google-images-download" code](https://github.com/hardikvasa/google-images-download). 

When the final image library has been created (or inputed by the user), mosaic.py then checks every file in the image library to see if they have any errors in being opened (Errors will most likely occur only with images downloaded from Google). If the user is using their own image library, then the program ends and prompts the user with which file has an error. If the user opted for the program to find images via Google, then the program deletes the files with errors. 

With the image library now complete, mosaic.py refits the main image such that there will be a positive integer number of tiles in each row and column. It also resizes the photo, twenty times over, so the tile photos are not too heavily pixelated. The program then uses file_storage.py, which loops through the main picture in order to find the dominant color of each square region. This process is performed by Python's sci-kit learn Kmeans clustering algorithm, which breaks the possible amount of RGB colors used into four groups (specified by RGB color values) and then selects the three most dominant. These color values are then stored in a .csv file. This same process of searching for color groups and saving the top three is also performed for the image library (Note that the images in the image library are then scaled down to their respective size on the to-be mosaic).

The Python file mosaic.py matches the main picture tiles with images in the image library and stores the paths of these files using image_comparison.py. This file uses a low-cost approximation [distance formulae](https://www.compuphase.com/cmetric.htm) to compare the three most dominant colors of each tile region on the main photo with the respective three most dominant colors of each photo in the image library. The three distances are averaged using a weighted average of the three. I found that a good choice of weights is 10, 7, and 3 corresponding to the three most dominant colors in decreasing order. When the weighted averges between the main image tile region and all of the pictures in the image library have been computed - the program then saves the minimum average in a .csv file. This process repeats for every single tile region of the main image.

The program mosaic.py concludes with pasting the images by order with which they are in the .csv file containing the paths of each image in the library that corresponds to a tile region. The image is finally saved in the directory where the program is found.


   
## Comments 

This program has been able to create photo mosaics, where the main image is reasonably preserverd - that is, the user should be able to still identify what the main image is intended to be. I found that the use of the kmeans clustering algorithm effective, as it heavily simplifies color comparison between images. I also find using a cluster k value of k=4 to be most effective, as compared to higher k values. I additionaly experimented with the actual color comparison process. One possibly drawback to this process is the fact that clusters might be very close to each other.

All test cases that I used have used image libraries generated by Google Images. The "google-images-download" function would originally split up each search specified by a color on Google Images' allowed color palette into a new directory. I then had the program go through each tile region on the main image and saved the minimum Euclidean distance between the main color of the region and that of each allowable color specification (the options from the palette that Google uses). I found that sometimes images that had dominant colors in between certain colors would be broken up into a less accurate directory, so I opted for saving the image library into one directory. The color comparison process of each picture has also changed.

I originally compared the RGB values of the dominant color of each image. I found that this did not follow human perception, so I tried comparing the values from the HSV color space. This process did not find the dominant color nor did it find the distances between them. Rather, it recorded the histograms of each H, S, and V value and interpreted them as probability distributions. Thus one could compare the first moment (mean), second moment (variance), and third moment of each histogram. I additionally condensed the histograms to only contain around ten or twenty boxes. This process was concluded by comparing the moments using the "psuedo-norm" found in [this paper](https://www.vision.ee.ethz.ch/publications/papers/proceedings/eth_biwi_00061.ps.gz), written by Markus Stricker and Markus Orengo. While this process works well in theory, it failed for this specific project. The first three moments came out to be very similar for most of the main image tile regions. I suspect this to be the case as since each region is relatively small compared to the main image, there is not much difference in color values in each region. Thus little variance and skewness are recorded. I additionally tried using the chi-square distance between the histograms and came to the same conlusion as I did with the previous comparison process. With this said, I opted to use the color [difference formulae](https://www.compuphase.com/cmetric.htm). It is said that this measure uses a weighted Euclidean distance formula, who's weights depend on the red value. This comparison has seen the best results and all examples posted use it. The weighted average of the most dominant colors will now be discussed. 

As said previously, I found weights that work well in a general setting. This process could be improved though, by finding the ratio of each of the dominant colors within the inputed picture and then creating the weights based on this ratio. This "dynamic weight" process could then be automatically optimized for different images. One can clearly see that in all the images, this would be effective. For example, in the image of Jesus Christ, much detail is lost by tile images that seemed to be incorrectly placed (especially the face, heart, and hands/fingers). With a weighting scheme that is dynamic, these details would probably be better represented. Although the color comparison process as well as the dominant color clustering are effective, they seem to be very expensive in the computational and time sense. An image that is 1000x1000 pixels large could take hours to complete, and if the user's computer is insufficiently powerful, then it could longer. Additionally the multiplier that is used to resize the main image such that the future mosaic tile images are not heavily pixelated, is not dynamic. Some images might contain not much detail, while others contain a large amount. The time to run this program could be better optimized if this multiplier were to consider the size of the image as well possibly the detail (I hypothesize that this could be measured by searching through the main image and seeing if groups of pixels have a large difference in color, how much the color changes over these group regions, or the "acceleration" in the color). Paying more attention to storage, if the main image has dimension (in terms of pixel) 1000x1000, then the mosaic could be 100 MB in size. A possible remedy to this would be to decrease the reshape the final mosaic such that it has a more realistic/manageable size. 

With this said, I will give some hopeful future updates below. 


### Future Updates
* Dynamic weights: When comparing tile regions with images from the image library, a weighted average of the low cost comparison between the three most dominant colors is used. The weights are currently static, but if they change based on the ratio of the dominant color groups, then a more recognizable image should be achieved.
* Dynamic multiplier: The program enlarges the image twenty fold in order to make the tile pictures more recognizable. Currently, the multiplier is static, but it could change based off of 
* Decrease the size of the output mosaic: The saved mosaic is normally large in terms of memory storage. It would probably be helpful to the user so that the produced mosaic is size less than one megabyte. 

