# TODO: https://dmaiorino.com/?p=12
# TODO: install cv2

import cv2
import time

import sys
import logging as log


# 1. Create an object
video = cv2.VideoCapture(0)


a = 0

# 2. must add!!! TODO: https://www.raspberrypi.org/forums/viewtopic.php?t=35689#p305473
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
# cv2.VideoWriter_fourcc(*'MJPG')

cv2.namedWindow("capturing", 0)
cv2.resizeWindow("capturing", 800, 600)
video.set(3, 1920)

video.set(4, 1440)


while True:
    a = a + 1

    # 3. Create a frame object
    check, frame = video.read()
    # cv2.putText(frame,'eyes detected!',(25,25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    print(check)
    print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 二值化
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 寻找轮廓
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 画出轮廓，-1,表示所有轮廓，画笔颜色为(0, 255, 0)，即Green，粗细为3
    cv2.drawContours(gray, contours, -1, (255, 255, 0), 3)

    cv2.imshow("capturing", gray)

    # 4 show the frame!
    # cv2.imshow("capturing", frame)

    # 5 For press any key to out (ms)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

print(a)

video.release()

cv2.destroyAllWindows
