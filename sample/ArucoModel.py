import numpy as np
import time
import cv2
from multiprocessing import Process, Queue


# Store all possible Aruco Dicts
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


aruco_type = "DICT_4X4_50"

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters_create()

# Create a video capture object and  setup the height and width
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Create img objects of each minecraft block
# img_ID where ID is the corresponding marker ID
img_0_path = "sample\images\mc_coal_ore.jpeg"
img_1_path = "sample\images\mc_copper_ore.png"
img_2_path = "sample\images\mc_diamond_ore.png"
img_3_path = "sample\images\mc_emerald_ore.png"
img_4_path = "sample\images\mc_gold_ore.png"
img_5_path = "sample\images\mc_grass_block.jpg"
img_6_path = "sample\images\mc_iron_ore.jpeg"
img_7_path = "sample\images\mc_lapis_lazuli_ore.png"
img_8_path = "sample\images\mc_redstone_ore.png"
img_9_path = "sample\images\white_square.png"


img_0  = cv2.imread(img_0_path)
img_1  = cv2.imread(img_1_path)
img_2  = cv2.imread(img_2_path)
img_3  = cv2.imread(img_3_path)
img_4  = cv2.imread(img_4_path)
img_5  = cv2.imread(img_5_path)
img_6  = cv2.imread(img_6_path)
img_7  = cv2.imread(img_7_path)
img_8  = cv2.imread(img_8_path)
img_9  = cv2.imread(img_9_path)

# Create a connection between the IDs and IMG data
ID_TO_IMG_DICT = {
	0: img_0,
	1: img_1,
	2: img_2,
	3: img_3,
	4: img_4,
	5: img_5,
	6: img_6,
	7: img_7,
	8: img_8,
	9: img_9
}

# text for each image
img_0_alt_text = r"Jovany is 23 years old!"
img_1_alt_text = r"My favorite color is blue!"
img_2_alt_text = r"My favorite anime is Mushoko Tensei"
img_3_alt_text = r"I am 50% european and 50% indigenous american!"
img_4_alt_text = r"I am studying electrical engineering"
img_5_alt_text = r"I have a cat named Hope"
img_6_alt_text = r"My favorite PC game is Elden Ring"
img_7_alt_text = r"I am 5 foot and 4 inches tall"
img_8_alt_text = "My hobbies include robotics,\n gaming, engineering, and audible"
img_9_alt_text = "TEST-TEST-TEST-TEST-TEST-\n TEST-TEST-TEST-TEST-TEST-TEST-TEST-TEST"

# Create a connection between IDs and Text data
ID_TO_TEXT_DICT = {
	0: img_0_alt_text,
	1: img_1_alt_text,
	2: img_2_alt_text,
	3: img_3_alt_text,
	4: img_4_alt_text,
	5: img_5_alt_text,
	6: img_6_alt_text,
	7: img_7_alt_text,
	8: img_8_alt_text,
	9: img_9_alt_text
}

# Create global flags that Enable or Disable each image
# if the flag is false -> Show text on white background
G_IMG_0_ENABLE_FLAG = True
G_IMG_1_ENABLE_FLAG = True
G_IMG_2_ENABLE_FLAG = True
G_IMG_3_ENABLE_FLAG = True
G_IMG_4_ENABLE_FLAG = True
G_IMG_5_ENABLE_FLAG = True
G_IMG_6_ENABLE_FLAG = True
G_IMG_7_ENABLE_FLAG = True
G_IMG_8_ENABLE_FLAG = True



def aruco_display(corners, ids, rejected, image):
	if len(corners) > 0:
		ids = ids.flatten()

		# store all transformed images, 3 channels for RGB
		all_warped_mc_img = np.zeros_like(a=image)

		# Go through all found markers and ids in frame
		# A SET of corners for each ID
		for (markerCorner, markerID) in zip(corners, ids):
			# print(f"Corners = {corners}")
			# using NUMPY attributes and turn the vector into a matrix
			corners = markerCorner.reshape((4, 2))

			# extract the corners pixel locations
			# We are unpacking each row of croners into smaller arrays
			(topLeft, topRight, bottomRight, bottomLeft) = corners
			
			# We will create tuples that are essentially PIXEL x and Y corridinates
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			# Draw a square around the arucos with RED lines and border thinkness of 2
			# cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
			# cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
			# cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
			# cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
			
			# Calculate the Center X and center Y position
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)

			# Draw a circle to indicate the center of the aruco
			# cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
			
			
			cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (255, 0, 0), 2)
			# print("[Inference] ArUco marker ID: {}".format(markerID))

			image = ArucoToImg(markerID=markerID, 
		      				   topLeft=topLeft, 
							   topRight=topRight, 
							   bottomRight=bottomRight,
							   image=image, 
							   all_warped_mc_img=all_warped_mc_img,
							   image_center_y=cY,
							   image_center_x=cX)

	return image

def TextToImg(img,text, y_start_position, y_text_spacing, x_position):
	y0, dy = y_start_position, y_text_spacing
	for i, line in enumerate(text.split('\n')):
		y = y0 + i*dy
		cv2.putText(img, line, (x_position, y ), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=2, color=(0,0,255))


def CheckIfImageEnabled(markerID, mc_img):
	# check if the image enable flag is true -> do nothing
		# otherwise make mc_img equal to white and add text
		
	if ( (G_IMG_0_ENABLE_FLAG is not True) and (markerID==0)):
		mc_img = ID_TO_IMG_DICT.get(9)

	if ( (G_IMG_1_ENABLE_FLAG is not True) and (markerID==1)):
		mc_img = ID_TO_IMG_DICT.get(9)

	if ( (G_IMG_2_ENABLE_FLAG is not True) and (markerID==2)):
		mc_img = ID_TO_IMG_DICT.get(9)

	if ( (G_IMG_3_ENABLE_FLAG is not True) and (markerID==3)):
		mc_img = ID_TO_IMG_DICT.get(9)

	if ( (G_IMG_4_ENABLE_FLAG is not True) and (markerID==4)):
		mc_img = ID_TO_IMG_DICT.get(9)

	if ( (G_IMG_5_ENABLE_FLAG is not True) and (markerID==5)):
		mc_img = ID_TO_IMG_DICT.get(9)

	if ( (G_IMG_6_ENABLE_FLAG is not True) and (markerID==6)):
		mc_img = ID_TO_IMG_DICT.get(9)

	if ( (G_IMG_7_ENABLE_FLAG is not True) and (markerID==7)):
		mc_img = ID_TO_IMG_DICT.get(9)

	if ( (G_IMG_8_ENABLE_FLAG is not True) and (markerID==8)):
		mc_img = ID_TO_IMG_DICT.get(9)	

	return mc_img


def CheckIfTextEnabled(image, markerID, image_center_y, topLeft, y_spacing):
	# will add alt text if the image enabled flag is False
	if ( (G_IMG_0_ENABLE_FLAG is not True) and (markerID==0)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)

	if ( (G_IMG_1_ENABLE_FLAG is not True) and (markerID==1)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)

	if ( (G_IMG_2_ENABLE_FLAG is not True) and (markerID==2)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)

	if ( (G_IMG_3_ENABLE_FLAG is not True) and (markerID==3)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)

	if ( (G_IMG_4_ENABLE_FLAG is not True) and (markerID==4)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)

	if ( (G_IMG_5_ENABLE_FLAG is not True) and (markerID==5)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)

	if ( (G_IMG_6_ENABLE_FLAG is not True) and (markerID==6)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)

	if ( (G_IMG_7_ENABLE_FLAG is not True) and (markerID==7)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)

	if ( (G_IMG_8_ENABLE_FLAG is not True) and (markerID==8)):
		mc_text = ID_TO_TEXT_DICT.get(markerID)
			
		TextToImg(img=image,
				text=mc_text,
				y_start_position=image_center_y,
				x_position=topLeft[0],
				y_text_spacing=y_spacing)	





def ArucoToImg(markerID,topLeft, topRight, bottomRight, image, all_warped_mc_img, image_center_x, image_center_y ):
	# ====== NEW Code ====== #
	# check that the found markerID is less then 10
	if markerID<10:

		# Use the Id to Dict to extract the corresponding image
		mc_img = ID_TO_IMG_DICT.get(markerID)
		
		mc_img = CheckIfImageEnabled(mc_img=mc_img, markerID=markerID)
		
		# Generate corners for imported images
		mc_img_rows, mc_img_cols = mc_img.shape[:2]
		# print(f"SRC Img Rows =  {mc_img_rows}  Columns = {mc_img_cols}")

		mc_img_topRight = ( int(0), int(mc_img_cols) )
		mc_img_bottomRight = ( int(mc_img_rows), int(mc_img_cols) )
		mc_img_bottomLeft = ( int(mc_img_rows), int(0) )
		mc_img_topLeft = ( int(0), int(0) )

		# get three points for the src image and dst image
		dst_tri_pts = np.array( [[topLeft], [topRight], [bottomRight]] ).astype(np.float32) 
		src_tri_pts = np.array( [[mc_img_topLeft], [mc_img_topRight], [mc_img_bottomRight]] ).astype(np.float32)
		# print(f"DST TRI PTS = {dst_tri_pts}")
		# print(f"SRC Tri Pts = {src_tri_pts}")

		# Generate a Affine Transformation Matrix and apply it
		affine_warp_matrix = cv2.getAffineTransform(src=src_tri_pts, dst=dst_tri_pts)

		mc_img_warped = cv2.warpAffine(src=mc_img, M=affine_warp_matrix, dsize=(image.shape[1], image.shape[0]), flags= cv2.INTER_NEAREST)

		# cv2.imshow("warp", mc_img_warped)
		# Add up all the warped images
		all_warped_mc_img = cv2.bitwise_or(src1=all_warped_mc_img, src2=mc_img_warped)
		# cv2.imshow("ALL Warp", all_warped_mc_img)


		# Create a grayscale and mask from the all warped img and apply it to the src image
		all_warped_mc_img_grayscale = cv2.cvtColor(src=all_warped_mc_img, code=cv2.COLOR_RGB2GRAY)

		#using "_" to ignore it
		_,all_warped_mc_img_monotone = cv2.threshold(src=all_warped_mc_img_grayscale, thresh=1, maxval=255, type=cv2.THRESH_BINARY)
	
		# cv2.imshow("monotone warp image", all_warped_mc_img_monotone)

		# create the inverse of the monotome warped image
		warp_image_mask = cv2.bitwise_not(all_warped_mc_img_monotone)

		# black out the warp image from the original image
		image_masked = cv2.bitwise_and(src1=image,src2=image, mask=warp_image_mask)

		# or this masked image with the all_warped_images
		image = cv2.bitwise_or(src1=image_masked, src2=all_warped_mc_img)

		# add Text if needed
		CheckIfTextEnabled(
			image=image,
			markerID=markerID,
			image_center_y=image_center_y,
			topLeft=topLeft,
			y_spacing=15
		)


	return image

def video_loop():
	try: 
		# print("Take IMAGE")
		ret, img = cap.read()
		
		# .shape is a numpy function that return array dimension
		# for a colored image -> (height, width, color_channels)
		# RGB image -> color_channels = 3
		h, w, _ = img.shape

		# The frame from camera "cap" will be resized
		# we can go from a high resolution to a lower one
		width = 1000
		height = int(width*(h/w))
		img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
	
		corners, ids, rejected = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)

		detected_markers = aruco_display(corners, ids, rejected, img)

		detected_markers = cv2.cvtColor(
			code=cv2.COLOR_BGR2RGB,
			src=detected_markers
		)
		
		# exit openCV via lowercase "q"
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			cv2.destroyAllWindows()
			cap.release()

		# cv2.imshow("Image", detected_markers)
		return detected_markers
		# put proccessed image in queue
		# q.put(detected_markers)

		# exit openCV via lowercase "q"
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			cv2.destroyAllWindows()
			cap.release()

		
	except:
		cv2.destroyAllWindows()
		cap.release()
		print("VideoCamera Released")
		pass

if(__name__ == "__main__" ):
	# Create a queue to hold frames from the video capture
    # q = Queue()

    # # Create a process to capture video frames and put them in the queue
    # p = Process(target=video_loop, args=(q,))
    # p.start()

    # # Wait for the process to finish
    # p.join()
	pass