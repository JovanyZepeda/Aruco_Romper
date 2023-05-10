import numpy as np
import time
import cv2


ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}


def aruco_display(corners, ids, rejected, image):
	if len(corners) > 0:
		
		ids = ids.flatten()
		
		# Go through all found markers and ids in frame
		for (markerCorner, markerID) in zip(corners, ids):
			
			# using NUMPY attributes and turn the vector into a matrix
			corners = markerCorner.reshape((4, 2))
			# extract the cornes pixel locations
			(topLeft, topRight, bottomRight, bottomLeft) = corners
			
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			# Draw a square around the arucos with RED lines and border thinkness of 2
			cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
			
			# Calculate the Center X and center Y position
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)

			# Draw a circle to indicate the center of the aruco
			cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
			
			
			cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 255, 0), 2)
			print("[Inference] ArUco marker ID: {}".format(markerID))



			# overlay all minecraft blocks over corresponding markers

			
	return image




aruco_type = "DICT_4X4_50"

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters_create()

# Create a video capture object and  setup the height and width
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Create img objects of each minecraft block
# img_ID where ID is the corresponding marker ID
img_0_path = "\images\mc_grass_block.jpg"
img_1_path = "\images\mc_diamond_ore.png"

img_0 = cv2.imread(img_0_path)
img_1 = cv2.imread(img_1_path)



while cap.isOpened():
    
	ret, img = cap.read()
	
	# .shape is a numpy function that return array dimension
	# for a colored image -> (height, width, color_channels)
	# RGB image -> color_channels = 3
	h, w, _ = img.shape


	width = 1000
	height = int(width*(h/w))
	img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
 
	corners, ids, rejected = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)

	detected_markers = aruco_display(corners, ids, rejected, img)

	cv2.imshow("Image", detected_markers)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
	    break

cv2.destroyAllWindows()
cap.release()