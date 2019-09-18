#Implemented Otsu?s method to find a good threshold to generate a binary image.
#Input: a greyscale image.
#Output: a binary image png image.
#Optional argument which prints the threshold found
#Example: python otsu_threshold.py –-input input.png –-output binary.png –- threshold
#Created by Arvind Bahl

#Library import
import cv2
import numpy as np
import sys
import getopt

printme = "no"

#Get the arguments
try:
	opts, args = getopt.getopt(sys.argv,"--input:--output", ["--threshold"])
except getopt.GetoptError:
	print ("error in arguments")
	sys.exit(2)
	
for i in range(0,len(args)):

	if args[i] == "--input":
		filename = args[i+1]
	elif args[i] =="--output":
		outputfile = args[i+1]
		
img = cv2.imread(filename, 0)
hist = cv2.calcHist([img], [0], None, [256], [0,256])

tweigth = hist.sum()
pixelb =0
weigthb =0
weigthf =0
twb=0
twf=0
listb =[]
listf =[]
newmax =0

def avoidzero(first, second):
    try:
        if second ==0:
            return 0
        else:
            return (first/second)
    except:
        return 0

for j in range(0, 256):

    twf = twf + (hist[j][0] * j)

for i in range(0,256):

    pixelb = pixelb + hist[i][0]
    weigthb =  avoidzero(pixelb,tweigth)
    twb = twb + (hist[i][0] * i)
    meanb = avoidzero(twb,pixelb)
    listb.append(((i-meanb)**2)*hist[i][0])
    svarb = avoidzero((sum(listb)),pixelb)

    pixelf = tweigth - pixelb
    weigthf =  avoidzero(pixelf,tweigth)
    meanf = avoidzero((twf - twb),pixelf)
    for k in range(i+1, 256):
        listf.append(((k-meanf)**2)*hist[k][0])
    svarf = avoidzero((sum(listf)),pixelf)

    bcvar = weigthb*weigthf*(meanb- meanf)*(meanb- meanf)

    if newmax <bcvar:
        newmax = bcvar
        thres = i
#Creates binary image.         
for i in range(0, img.shape[0]):
	for j in range(0, img.shape[1]):
		if img[i][j] <= thres:
			img[i][j] = 0
		else:
			img[i][j] = 255
			
#prints the threshold value
if len(args) == 6:
	print(thres)

cv2.imwrite(outputfile, img)
    

    
