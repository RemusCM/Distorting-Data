#Import needed libraries
import numpy as np
import cv2
import math
import os
from pathlib import Path
import random

#Definition of the two possible shrink transformations.
def horizontalShrink(point, angle):
        point[0][0] = point[0][0]* (np.sin(np.pi/2 - math.radians(angle)) - (point[0][1]* np.sin(math.radians(angle))/100))

def verticalShrink(point, angle):
        point[0][1] = point[0][1]* (np.sin(np.pi/2 - math.radians(angle)) - (point[0][0]* np.sin(math.radians(angle))/100))

#Global Distortions
#angle should be between -10 and 10 degrees.
def rotation(point, angle):
    point[0][0] = point[0][0] * np.cos(math.radians(angle)) + point[0][1] * np.sin(math.radians(angle))
    point[0][1] = point[0][0] * np.sin(math.radians(angle)) + point[0][1] * np.cos(math.radians(angle))

#scaling factor should be between 0.7 and 1.3
def scaling(point, scalingFactor):
    point[0][0] = scalingFactor * point[0][0]
    point[0][1] = scalingFactor * point[0][1]



#Function that takes in a file, and applies shearing (horizontal or vertical)
#and potentially applies global distortions.
def shrink(file):
        #open file
        img = cv2.imread(os.path.join(Path("OriginalData/"),file))

        #Make a blank canvas with same size as file. (256x256)
        canvas = np.zeros_like(img)

        #Create the binarized version of the image.
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                        127, 255, cv2.THRESH_BINARY)


        threshed_img = cv2.bitwise_not(threshed_img)

        #Find the contours of the image that will need to be modified.
        contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        scalingFactor = 1
        shrinkGlobal = random.random()
        if(shrinkGlobal < 0.5):
            scalingFactor = random.uniform(0.7,1.3)
            rotationFactor = random.randint(0,20) - 10

        # #SHRINK
        #if < 0.5, use horizontal, otherwise vertical
        shrinkType = random.random()
        angle = random.randint(0,20) - 10
        for c in range(0, len(contours)):
            #Decide angle between -5 and 5:


            #Get bounding rectangle for that symbol
            x, y, w, h = cv2.boundingRect(contours[c])
            # draw a green rectangle to visualize the bounding rect
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            if(shrinkType < 0.5):
                for point in contours[c]:
                    horizontalShrink(point,angle)
                    #If we decided to apply global distortions to this image.
                    if(shrinkGlobal < 0.5):
                        rotation(point, rotationFactor)
                        scaling(point, scalingFactor)

            else:
                for point in contours[c]:
                    verticalShrink(point,angle)
                    if(shrinkGlobal < 0.5):
                        rotation(point, rotationFactor)
                        scaling(point, scalingFactor)


        if(scalingFactor>1):
            canvas = cv2.resize(canvas,(int(400*scalingFactor),int(400*scalingFactor)) ,interpolation = cv2.INTER_AREA)
        else:
            canvas = cv2.resize(canvas,(400,400) ,interpolation = cv2.INTER_AREA)

        cv2.drawContours(canvas , contours, -1, (255, 255, 255), -1, offset = (85,85))
        #invert colors
        canvas = cv2.bitwise_not(canvas)
        #all files need to be 256x256.
        canvas = cv2.resize(canvas, (256,256), interpolation = cv2.INTER_AREA)
        #Need to save in DistortedData/ as filename_shear
        filename = file[:len(file)-4] + "_shrink" + file[len(file)-4:]
        print(filename)
        cv2.imwrite(os.path.join(Path("DistortedData/"),filename), canvas)
