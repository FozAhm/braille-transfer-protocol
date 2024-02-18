# program to capture single image from webcam in python 

# importing OpenCV library 
import cv2 as cv

print('Starting Test Webcam program')

# initialize the camera 
# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that 
cam_port = 0
cam = cv.VideoCapture(cam_port) 

# reading the input using the camera 
result, orig_image = cam.read() 

# Basic Crop the image
crop_image = orig_image[200:1080, 700:1300]
cv.imwrite("1BasicCrop.png", crop_image)

# Convert Image to Grayscale
gray_image = cv.cvtColor(crop_image, cv.COLOR_BGR2GRAY)
cv.imwrite("2BasicCropGray.png", gray_image)

# Apply threshold
_, thresh = cv.threshold(gray_image, 200, 255, cv.THRESH_BINARY)

# Find contours
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Assuming the largest contour is the card
card_contour = max(contours, key=cv.contourArea)

# Get bounding rectangle
x, y, w, h = cv.boundingRect(card_contour)

# Crop the image
y_offset = 20
x_offset = 20
final_crop_image = gray_image[y+y_offset:y+h-y_offset, x+x_offset:x+w-x_offset]
cv.imwrite("3FinalCropGray.png", final_crop_image)

# Make the image whiter
_, white_tresh = cv.threshold(final_crop_image, 175, 255, cv.THRESH_BINARY)
cv.imwrite("4WhiteImage.png", white_tresh)

# threshold 
th, threshed = cv.threshold(white_tresh, 100, 255, cv.THRESH_BINARY|cv.THRESH_OTSU)
cv.imwrite("5SuperWhiteImage.png", white_tresh)
  
# findcontours 
suoer_good_contours = cv.findContours(threshed, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[-2] 

# Find good contours
good_contours, _ = cv.findContours(final_crop_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# filter by area 
s1 = 0
s2 = 40
xcnts = [] 
for cnt in suoer_good_contours: 
    if s1<cv.contourArea(cnt) <s2: 
        xcnts.append(cnt) 


print("\nDots number: {}".format(len(xcnts))) 




# If image will detected without any error, 
# show result 
#if result: 

	# showing result, it take frame name and image 
	# output 
	# cv.imshow("GeeksForGeeks", image) 

	# saving image in local storage 


	# If keyboard interrupt occurs, destroy image 
	# window 
	# cv.waitKey(0) 
	# cv.destroyWindow("GeeksForGeeks") 

# If captured image is corrupted, moving to else part 
#else: 
	#print("No image detected. Please! try again") 
