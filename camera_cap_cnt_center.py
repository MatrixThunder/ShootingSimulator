# TODO: https://dmaiorino.com/?p=12
# TODO: install cv2

import cv2
import time
import numpy as np
import imutils

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

kernel = np.ones((5, 5), np.uint8)


while True:
    a = a + 1

    # 3. Create a frame object
    check, frame = video.read()

    print(check)
    print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 100, 100)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    imgDialation = cv2.dilate(canny, kernel, iterations=2)

    # 注意，在应用阈值化之后，形状是如何在黑色背景上表示为白色前景。
    # 下一步是使用轮廓检测??找到这些白色区域的位置：
    cnts = cv2.findContours(imgDialation.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # 遍历轮廓集
    for c in cnts:
        # 计算轮廓区域的图像矩。 在计算机视觉和图像处理中，图像矩通常用于表征图像中对象的形状。这些力矩捕获了形状的基本统计特性，包括对象的面积，质心（即，对象的中心（x，y）坐标），方向以及其他所需的特性。
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # cv2.imshow("capturing", frame)

        cv2.drawContours(gray, [c], -1, (0, 255, 0), 2)
        cv2.circle(gray, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(gray, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # 展示图像
        cv2.imshow("Bullet Point Dialation", gray)


# 4 show the frame!
# cv2.imshow("capturing", frame)

    # 5 For press any key to out (ms)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

print(a)

video.release()

cv2.destroyAllWindows
