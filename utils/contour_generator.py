
# 导入必要的包
import argparse
import imutils
import cv2

# import cvui

import numpy as np

from operator import itemgetter

from utils import settings as config


# def init_windows():
#     WINDOW_NAME = "control panel"
#     cvui.init(WINDOW_NAME)
#     background = np.zeros((200, 400, 3), np.uint8)

#     cvui.text(background,10,15,'hello')

#     cvui.button(background,10,15,'Load Config')
#     cvui.button(background,25,55,'Save Config')

#     cvui.imshow(WINDOW_NAME, background)


def empty(a):
    pass


gray = 1
blurred = 2
imgCanny = 3
thresh = 4
imgDialation = 5

ths = 0
kernel_config = 0


def contour_generator(frame):

    ratio = 3

    # imgHLS = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    # Lchannel = imgHLS[:,:,1]
    # mask = cv2.inRange(Lchannel, 0,200)
    # res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 300)

    # Tracker Bars are for adjusting the params to get a better
    # and smoother contour of the target, which will help calculating
    # hit areas and doing the scoring.
    cv2.createTrackbar("HUE min", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("HUE max", "TrackBars", 19, 179, empty)
    cv2.createTrackbar("SAT min", "TrackBars", 0, 170, empty)
    cv2.createTrackbar("SAT max", "TrackBars", 0, 170, empty)
    cv2.createTrackbar("VAL min", "TrackBars", 153, 259, empty)
    cv2.createTrackbar("VAL max", "TrackBars", 255, 255, empty)
    cv2.createTrackbar("THS", "TrackBars", 0, 85, empty)
    cv2.createTrackbar("KNL size", "TrackBars", 0, 10, empty)

    ths = None
    kernel_config = None
    # print(config.read_img_settings())
    if(config.read_img_settings() is not None):
        ths, kernel_config = itemgetter(
            "threshold", "kernel_config")(config.read_img_settings())
        if((ths is not None) and (kernel_config is not None)):
            cv2.setTrackbarPos("THS", "TrackBars", ths)
            cv2.setTrackbarPos("KNL size", "TrackBars", kernel_config)

    while True:

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("HUE min", "TrackBars")
        h_max = cv2.getTrackbarPos("HUE max", "TrackBars")
        s_min = cv2.getTrackbarPos("SAT min", "TrackBars")
        s_max = cv2.getTrackbarPos("SAT max", "TrackBars")
        v_min = cv2.getTrackbarPos("VAL max", "TrackBars")
        v_max = cv2.getTrackbarPos("VAL max", "TrackBars")

        # if(ths == 0 and kernel_config == 0):
        ths = cv2.getTrackbarPos("THS", "TrackBars")

        kernel_config_val = cv2.getTrackbarPos("KNL size", "TrackBars")

        kernel_config = 2 * kernel_config_val + 1

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        kernel_size = (kernel_config, kernel_config)
        kernel = np.ones(kernel_size, np.uint8)

        mask = cv2.inRange(hsv, lower, upper)
        imgResult = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("imgResult", imgResult)

        # 加载图像，转换为灰度，使用5 x 5内核进行高斯平滑处理，阈值化
        gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
        #blurred = cv2.GaussianBlur(gray, kernel_size, 0)
        blurred = cv2.bilateralFilter(
            gray, d=kernel_config, sigmaColor=112, sigmaSpace=kernel_config, borderType=cv2.BORDER_REPLICATE)
        imgCanny = cv2.Canny(blurred, ths, ths*ratio, 5, L2gradient=True)
        thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]
        imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)

        # 注意，在应用阈值化之后，形状表是如何在黑色背景上示为白色前景。
        # 下一步是使用轮廓检测??找到这些白色区域的位置：
        # HACK: CV_RETR_LIST : https://blog.csdn.net/c20081052/article/details/22422919
        # cnts = cv2.findContours(imgDialation.copy(), cv2.RETR_LIST,
        #                         cv2.CHAIN_APPROX_SIMPLE)

        # cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
        #                         cv2.CHAIN_APPROX_NONE)

        cv2.imshow("generated thresh", thresh)
        cv2.imshow("generated dialation", imgDialation)

        cv2.moveWindow("generated thresh", 400, 100)
        cv2.moveWindow("generated dialation", 800, 100)

        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows
            break

    cnts = cv2.findContours(imgDialation, cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)

    # Saving settings to the local folder
    config.save_img_settings(ths, kernel_config_val)

    return cnts, imgDialation
