import cv2
import numpy as np

while True:
    src = cv2.imread('../images/testing/qrcode.jpg')
    srcCopy = src.clone()

    canvas = np.zeros(src.length())

    srcGray = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

    srcGray = cv2.blur(srcGray, size(3,3))

    src_map = cv2.convertScaleAbs(src)
    srcGray_map = cv2.equalizeHist(srcGray)

    #int s = srcGray.at<Vec3b>(0, 0)[0];

    thres = cv2.threshold(srcGray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    cv2.imshow('threshold', srcGray)

    contours = cv2.findContours(srcGray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    numOfRec = 0

    ic = 0
    parentIdx = -1

    for i in range(contours.length()):
        if
