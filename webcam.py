# program to capture single image from webcam in python 

# importing OpenCV library 
import cv2 as cv

def get_change(current, previous):
	if current == previous:
		return 0
	try:
		return (abs(current - previous) / previous) * 100.0
	except ZeroDivisionError:
		return float('inf')

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
_, white_tresh = cv.threshold(final_crop_image, 180, 255, cv.THRESH_BINARY)
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
s2 = 50
dots = [] 
for cnt in suoer_good_contours: 
    if s1<cv.contourArea(cnt) <s2: 
        dots.append(cnt) 

# Get the Number of dots
num_of_dots = len(dots)
print("\nDots number: {}".format(num_of_dots)) 
# print(dots)

# Recognize Braille
diff_level = 5

# Figure out colums
colums = []
for i in range(num_of_dots):
	x, y, w, h = cv.boundingRect(dots[i])
	num_comlums = len(colums)
	if num_comlums == 0:
		colums.append(x)
	else:
		match_tue = False
		for j in range(num_comlums):
			col_x = colums[j]
			perc_diff = get_change(x, col_x)
			# print("percent diff: " + str(perc_diff))
			if perc_diff < diff_level:
				match_tue = True
		if match_tue == False:
			colums.append(x)

# Number of colums
num_comlums = len(colums)
print("Number of colums " + str(num_comlums))
print(colums)

# Figure out rows
rows = []
for i in range(num_of_dots):
	x, y, w, h = cv.boundingRect(dots[i])
	num_rows = len(rows)
	if num_rows == 0:
		rows.append(y)
	else:
		match_tue = False
		for j in range(num_rows):
			row_y = rows[j]
			perc_diff = get_change(y, row_y)
			# print("percent diff: " + str(perc_diff))
			if perc_diff < diff_level:
				match_tue = True
		if match_tue == False:
			rows.append(y)

# Number of rows
num_rows = len(rows)
print("Number of rows " + str(num_rows))
print(rows)

# max_y = 0
# max_index = 0
# for i in range(num_of_dots):
# 	x, y, w, h = cv.boundingRect(dots[i])
# 	print("Dot {}".format(i))
# 	print(x)
# 	print(y)
# 	if y > max_y:
# 		max_y = y
# 		max_index = i
 
# print("Highest Dot: " + str(max_y) + " at index " + str(max_index))

# Print the Braile Character
if num_of_dots == 1:
	print("Braille Letter " + "A")
elif (num_of_dots == 2) and (num_comlums == 1) and (num_rows == 2):
	print("Braille Letter " + "B")
elif (num_of_dots == 2) and (num_comlums == 2) and (num_rows == 1):
	print("Braille Letter " + "C")
elif (num_of_dots == 3) and (num_comlums == 2) and (num_rows == 2):
	print("Braille Letter " + "D")
elif (num_of_dots == 2) and (num_comlums == 2) and (num_rows == 2):
	print("Braille Letter " + "E")




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
