import cv2
import numpy as np

# 用于矫正
transformCorner: list
transformQRcode: list

# 用于判断角点
IsQrPoint: bool
isCorner: bool
Rate: float
leftTopPoint: int
otherTwoPoint: list
rotateAngle: float

'''
版权声明：本文为CSDN博主「Bubbliiiing」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_44791964/article/details/101477630
'''

while True:
    src = cv2.imread('../images/testing/qrcode.jpg')
    srcCopy = src.copy()

    canvas = np.zeros(src.shape)

    srcGray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    srcGray = cv2.blur(srcGray, (3,3))

    src_map = cv2.convertScaleAbs(src)
    srcGray_dst = cv2.equalizeHist(srcGray)

    #print(srcGray_dst)

    s: int = srcGray_dst[0];

    thres = cv2.threshold(srcGray_dst, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    cv2.imshow('threshold', srcGray_dst)

    contours, hierarchy = cv2.findContours(srcGray_dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(hierarchy)

    numOfRec = 0

    ic = 0
    parentIdx = -1


    for i in range(contours.length()):
        if hierarchy[i][2] != -1 and ic == 0:
            parentIdx = i
            ic += 1
        elif hierarchy[i][2] != -1:
            ic += 1
        elif hierarchy[i][2] == -1:
            parentIdx =-1
            ic =0

        if ic >= 2 and ic <= 2:
            if contours[parentIdx] == src:
                rect = cv2.minAreaRect(contours[parentIdx])

                points = [0] * 4

                rect.points(points);
                for j in range(4):
                    cv2.line(src, points[j], points[(j + 1) % 4], (0, 255, 0), 2);

                cv2.drawContours(canvas, contours, parentIdx, (0, 0, 255), -1);