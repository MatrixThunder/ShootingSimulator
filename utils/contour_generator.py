
# 导入必要的包
import argparse
import imutils
import cv2
import numpy as np

def contour_generator(frame):
    # 构建命令行参数
    # --frame 要处理的图像路径
    kernel_size = (5, 5)
    kernel = np.ones(kernel_size, np.uint8)
    ratio = 2

    # imgHLS = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    # Lchannel = imgHLS[:,:,1]
    # mask = cv2.inRange(Lchannel, 0,200)
    # res = cv2.bitwise_and(frame,frame, mask= mask)

    # 加载图像，转换为灰度，使用5 x 5内核进行高斯平滑处理，阈值化
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, kernel_size, 0)
    imgCanny = cv2.Canny(blurred, 100, 100*ratio, 5)
    thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
    
    # 注意，在应用阈值化之后，形状表是如何在黑色背景上示为白色前景。
    # 下一步是使用轮廓检测??找到这些白色区域的位置：
    # HACK: CV_RETR_LIST : https://blog.csdn.net/c20081052/article/details/22422919
    cnts = cv2.findContours(imgDialation.copy(), cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.imshow("generated dialation",imgDialation)

    
    return cnts

# if __name__ == "__main__":
#     img = cv2.imread("./target.png")
#     contour_generator(img)
#     cv2.waitKey(0)