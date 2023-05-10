
import cv2
import numpy as mp

# Create img objects of each minecraft block
# img_ID where ID is the corresponding marker ID
img_0_path = "\images\mc_grass_block.jpg"
img_1_path = "\images\mc_diamond_ore.png"
img_white_path = "\images\white_square.png"


img_0 = cv2.imread(img_0_path)
img_1 = cv2.imread(img_1_path)
img_white = cv2.imread(img_white_path)

cv2.imshow("test image",img_0)

# Grab the height and width 
h,w = img_0.size
print("Height = " + str(h) + " width = " + str(w))
h2,w2 = img_0.shape()
print("Height = " + str(h2) + " width = " + str(w2))


