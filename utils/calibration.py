import glob
import cv2 as cv
import find_squares from game_area_detection

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

bd_box=find_squares(img)[2] #get the second bounding box

side = len(bd_box)

top_left, top_right, bottom_left, bottom_right = [bd_box[0,:], bd_box[side*1/3 - 1,:], bd_box[side*2/3 - 1,:], bd_box[side*1/3 - 1,:]]

