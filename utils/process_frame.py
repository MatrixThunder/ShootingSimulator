# TODO: https://dmaiorino.com/?p=12
# TODO: install cv2

import cv2
import time
from . import detect_contour_centers

'''
A high level function that processes each frame, used in a while loop for processing 
'''

'''
Args:
    frame                  :  The matrix 
    detect_contour_centers :  The function that detects centers of all the contours of a frame
    generated_dialation    :  
'''


def process_frame(frame, detect_contour_centers,  detect_hit, generated_cnts, generated_dialation):
    try:
        detect_contour_centers(frame)
        # game_area = grab_game_area()
        detect_hit(frame, generated_cnts, generated_dialation)
        # detect_hit(frame,cnts)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except Exception:
        print("can't process frame!!")
