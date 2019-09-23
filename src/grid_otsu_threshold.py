#Implementation of Otsu's method to find a good threshold to generate a binary image using grids.
# The image is split into a grid of cells of given size and then Otsu's method is applied on each cell treating it as a separate image (and presuming a bi-modal histogram). 
# If a sub-image cannot be thresholded well, then the threshold from one of the neighbouring cells is used. 
# The encoding of 0/255 for nodules/background is used.
# Created by Arvind Bahl
# **************************************************************************************************************

# Import of the libraries 
import cv2
import numpy as np
import math
import sys
import getopt


# Get the input arguments
try:
	opts, args = getopt.getopt(sys.argv,"--input:--output", [])
except getopt.GetoptError:
	print ("error in arguments")
	sys.exit(2)
	
for i in range(0,len(args)):

	if args[i] == "--input":
		filename = args[i+1]
	elif args[i] =="--output":
		outputfile = args[i+1]
	elif i ==3:
		n = int(args[i])

# Calculation of histogram on the image.
img = cv2.imread(filename , 0)
hist = cv2.calcHist([img], [0], None, [256], [0,256])

# Function to avoid zero error. 
def avoidzero(first, second):
    try:
        if second ==0:
            return 0
        else:
            return (first/second)
    except:
        return 0

# Initialization of the variables.
gsize = math.sqrt(n)
vlimit = int(img.shape[0]/gsize)
hlimit = int(img.shape[1]/gsize)
svpixel =0
shpixel = 0
evpixel = vlimit
ehpixel = hlimit
lthresh = []

# The image is divided into grids and variable values are calculated. 
for i in range(0, int(gsize)):

    for j in range(0, int(gsize)):      
        pixelb =0
        weigthb =0
        weigthf =0
        twb=0
        twf=0
        listb =[]
        listf =[]
        newmax =0
        if i==(gsize-1) and (img.shape[0]//2)!=0:
            evpixel=evpixel+ int((img.shape[0]-(vlimit*gsize)))
        if j==(gsize-1)and(img.shape[1]//2)!=0:
            ehpixel = ehpixel+int((img.shape[1]-(hlimit*gsize)))
        timg = img[svpixel:evpixel, shpixel:ehpixel]
        thist = cv2.calcHist([timg], [0], None, [256], [0,256])
        tweigth = thist.sum()
        for jj in range(0, 256):
            twf = twf + (thist[jj][0] * jj)

        for ii in range(0,256):
            pixelb = pixelb + thist[ii][0]
            weigthb =  avoidzero(pixelb,tweigth)
            twb = twb + (thist[ii][0] * ii)
            meanb = avoidzero(twb,pixelb)
            listb.append(((ii-meanb)**2)*thist[ii][0])
            svarb = avoidzero((sum(listb)),pixelb)

            pixelf = tweigth - pixelb
            weigthf =  avoidzero(pixelf,tweigth)
            meanf = avoidzero((twf - twb),pixelf)
            '''for kk in range(ii+1, 256):
                listf.append(((kk-meanf)**2)*thist[kk][0])
                svarf = avoidzero((sum(listf)),pixelf)'''

            bcvar = weigthb*weigthf*(meanb- meanf)*(meanb- meanf)

            if newmax <bcvar:
                newmax = bcvar
                thres = ii

        lthresh.append(thres)
        ehpixel= ehpixel + hlimit
        shpixel = shpixel + hlimit

    svpixel = svpixel + vlimit
    evpixel = evpixel + vlimit
    shpixel = 0
    ehpixel=  hlimit


svpixel =0
shpixel = 0
evpixel = vlimit
ehpixel = hlimit    

ind =0
# The sub images are thresholded.
for i in range(0, len(lthresh)):
    if lthresh[i] >180 or lthresh[i]<90:
        if i==0:
            lthresh[i] = lthresh[i+1]
        elif i == (len(lthresh) -1):
            lthresh[i] = lthresh[i-1]
        else:
            lthresh[i] = lthresh[i+1]
        
for ii in range(0, int(gsize)):
    for jj in range(0, int(gsize)):
        if ii==(gsize-1) and (img.shape[0]//2)!=0:
            evpixel=evpixel+ int((img.shape[0]-(vlimit*gsize)))
        if jj==(gsize-1)and(img.shape[1]//2)!=0:
            ehpixel = ehpixel+int((img.shape[1]-(hlimit*gsize)))
        timg = img[svpixel:evpixel, shpixel:ehpixel]
        for i in range(0, timg.shape[0]):
            for j in range(0, timg.shape[1]):
                if timg[i][j] <= lthresh[ind]:
                    timg[i][j] = 0
                else:
                    timg[i][j] = 255

        img[svpixel:evpixel, shpixel:ehpixel] = timg
        ehpixel= ehpixel + hlimit
        shpixel = shpixel + hlimit
        ind = ind+1
    svpixel = svpixel + vlimit
    evpixel = evpixel + vlimit
    shpixel = 0
    ehpixel=  hlimit
    
		
# Output written to the file.			
#print(newmax)
#print(thres)
#cv2.imshow("abc", img)
cv2.imwrite(outputfile, img)
    

    
