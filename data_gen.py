#This file will complete the desired transformations on every image file in
#the OriginalData folder
#Needed imports.
import numpy as np
import cv2
import math
import os
from pathlib import Path
import random
from shear import *
from shrink import *
from shrink_rotation import *
from perspective import *
from perspective_rotation import *
from os import walk


#We're going to first open every file.
for file in os.listdir(Path("OriginalData/")):
    #Apply Shear + Potential Global Distortions.
    shear(file)
    #Apply Shrink + Potential Global Distortions.
    shrink(file)
    #Apply Shrink & rotation + Potential Global Distortions.
    shrink_rotation(file)
    #Apply Perspective + Potential Global Distortions.
    perspective(file)
    #Apply Perspective & rotation + Potential Global Distortions.
    perspective_rotation(file)

while True:
    key = cv2.waitKey(1)
    if key == 27: #ESC key to break
        break


    #Apply Shrink + Potential Global Distortions.
