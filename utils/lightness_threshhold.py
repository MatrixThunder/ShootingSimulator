import cv2
import numpy as np

img = cv2.imread("./laser_dot.png")
imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
# Get the L channel

Lchannel = imgHLS[:,:,1]
# Create the mask

#change 250 to lower numbers to include more values as "white"
mask = cv2.inRange(Lchannel, 253, 255)
# Apply Mask to original image

res = cv2.bitwise_and(img,img, mask= mask)
# This also depends on what is white for you, and you may change the values :) I used inRange in the L channel but you can save one step and do

# mask = cv2.inRange(imgHLS, np.array([0,250,0]), np.array([255,255,255]))
# instead of the lines:

Lchannel = imgHLS[:,:,1]
# mask = cv2.inRange(Lchannel, 250, 255)
cv2.imshow("capturing", mask)

# 5 For press any key to out (ms)
cv2.waitKey(0)
cv2.destroyAllWindows
