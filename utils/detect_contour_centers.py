
# 导入必要的包
import argparse
import imutils
import cv2
import numpy as np

def detect_contour_centers(frame):
    # 构建命令行参数
    # --frame 要处理的图像路径
    kernel_size = (5, 5)
    kernel = np.ones(kernel_size, np.uint8)
    ratio = 2
    
    # 加载图像，转换为灰度，使用5 x 5内核进行高斯平滑处理，阈值化
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, kernel_size, 0)
    imgCanny = cv2.Canny(blurred, 100, 100*ratio, 6)
    thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
    
    # 注意，在应用阈值化之后，形状表是如何在黑色背景上示为白色前景。
    # 下一步是使用轮廓检测??找到这些白色区域的位置：
    # HACK: CV_RETR_LIST : https://blog.csdn.net/c20081052/article/details/22422919
    cnts = cv2.findContours(imgDialation.copy(), cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # 遍历轮廓集
    for c in cnts:
        #print(c)
        # 计算轮廓区域的图像矩。 在计算机视觉和图像处理中，图像矩通常用于表征图像中对象的形状。这些力矩捕获了形状的基本统计特性，包括对象的面积，质心（即，对象的中心（x，y）坐标），方向以及其他所需的特性。
        M = cv2.moments(c) #moments of each small contour
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # 在图像上绘制轮廓及中心
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        # cv2.circle(frame, (cX, cY), 7, (0, 255, 255), -1)
        cv2.putText(frame, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # # 展示图像
        # cv2.imshow("frame", frame)
        # cv2.imshow("imgCanny", imgCanny)
        # cv2.waitKey(0)
    
        # for sub_c in c:
        #     print(sub_c) 
            # # 计算轮廓区域的图像矩。 在计算机视觉和图像处理中，图像矩通常用于表征图像中对象的形状。这些力矩捕获了形状的基本统计特性，包括对象的面积，质心（即，对象的中心（x，y）坐标），方向以及其他所需的特性。
            # M = cv2.moments(sub_c)
            # cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])
            # # 在图像上绘制轮廓及中心
            # cv2.drawContours(frame, [sub_c], -1, (0, 255, 0), 2)
            # cv2.circle(frame, (cX, cY), 7, (0, 255, 255), -1)
            # cv2.putText(frame, "center", (cX - 20, cY - 20),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
    
        # 展示图像
        # cv2.imshow("frame", frame)
        # cv2.imshow("imgDialation2", imgDialation)
        #cv2.imshow("imgCanny", imgCanny)
        #cv2.waitKey(0)
        #print(frame)
        
    
    #print(len(cnts))
    return cnts