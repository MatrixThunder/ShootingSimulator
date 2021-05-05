import cv2
import numpy as np
import imutils


a = 0
def detect_hit(frame,cnts,passed_in_dialation):

    passed_in_dialation_copy = passed_in_dialation.copy()

    kernel_size = (5, 5)
    kernel = np.ones(kernel_size, np.uint8)
    ratio = 2


    imgHLS = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    # Get the L channel

    Lchannel = imgHLS[:,:,1]
    # Create the mask

    #change 250 to lower numbers to include more values as "white"
    mask = cv2.inRange(Lchannel, 220, 255)
    # Apply Mask to original image

    res = cv2.bitwise_and(frame,frame, mask= mask)
    # This also depends on what is white for you, and you may change the values :) I used inRange in the L channel but you can save one step and do

    # mask = cv2.inRange(imgHLS, np.array([0,250,0]), np.array([255,255,255]))
    # instead of the lines:

    # Lchannel = imgHLS[:,:,1]
    # mask = cv2.inRange(Lchannel, 250, 255)

    # laser beam cnt
    blurred = cv2.GaussianBlur(mask, kernel_size, 0)
    imgCanny = cv2.Canny(blurred, 100, 100*ratio, 6)
    thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=2)
    
    laser_cnts = cv2.findContours(imgDialation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    laser_cnts = imutils.grab_contours(laser_cnts)

    laser_cnt = None
    M = None
    cX = None
    cY = None

    if(len(laser_cnts) != 0):
        laser_cnt = laser_cnts[0]
        M_test = cv2.moments(laser_cnt) #moments of each small contour
        if(M_test["m00"] != 0):
            # The center of the beam
            M = cv2.moments(laser_cnt) #moments of each small contour
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            print(cX)
            print(cY)



    hit_area = []
    # passed in cnts.
    idx = 0
    # print(len(cnts))
    for c in cnts:
        
        if(cX!=None and cY!=None):
            
            flag = cv2.pointPolygonTest(c, (cX,cY), True)
            # print(flag)
            if(flag > 0 ):
                idx += 1
                # print('hit')
                hit_area = c
                print("you hit: ", idx, "ring")
                if(len(hit_area) != 0 ):
                    # print(hit_area)
                    # Thick contour
                    cv2.drawContours(frame, [hit_area], -1, (0, 0, 255), 2)
                   

                    # cv2.fillPoly(frame, pts =[hit_area], color=(0,0,255))
                    
                    h, w = frame.shape[:2]
                    mask = np.zeros([h+2, w+2], np.uint8)
                    # mask = np.zeros(frame, dtype=np.uint8)
                    cv2.floodFill(frame, mask, (cX,cY), (0, 0, 255), (90, 90, 90), (10, 10, 10), flags=8)

                    
                    cv2.drawContours(passed_in_dialation_copy, [hit_area], -1, (255, 255, 255), 2)
                    cv2.floodFill(passed_in_dialation_copy, mask, (cX,cY), (0, 0, 255), (90, 90, 90), (10, 10, 10), flags=8)
                    # cv2.fillPoly(passed_in_dialation_copy, pts =[hit_area], color=(255,255,255))




    cv2.imshow("hit_in_dialation", passed_in_dialation_copy)

    cv2.imshow("hit_colored", frame)

    cv2.moveWindow("hit_in_dialation",400,500)
    cv2.moveWindow("hit_colored",800,500)


   
