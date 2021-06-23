import cv2
import numpy as np

img = cv2.imread('./laser_dot2.jpg')


def onmouse(event, x, y, flags, param):  # 标准鼠标交互函数
    #    if event==cv2.EVENT_LBUTTONDBLCLK :      #当鼠标点击时
    #        print("y=",y), print("x=",x), print(img[y,x],"\n")           #显示鼠标所在像素的数值，注意像素表示方法和坐标位置的不同
    if event == cv2.EVENT_MOUSEMOVE:  # 当鼠标移动时
        print("y=", y, "x=", x, img[y, x], "\n")


def main():

    kernel = np.ones((5, 5), np.uint8)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
    imgCanny = cv2.Canny(img, 100, 100)
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
    imgEroded = cv2.erode(imgDialation, kernel, iterations=1)

    ret, thresh = cv2.threshold(imgGray, 128, 15, cv2.THRESH_BINARY)

    # 寻找轮廓
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]  # 取第一条轮廓
    M = cv2.moments(cnt)  # 计算第一条轮廓的各阶矩,字典形式

    print(M)
    # 这两行是计算中心点坐标
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print(cx)
    print(cy)
    cv2.line(img, (0, 0), (cx, cy), (255, 255, 0), 1, 4)
    print(len(hierarchy))
    cv2.drawContours(img, contours, -1, (0, 0, 255), 2)

    cv2.imshow("Gray Image", imgGray)
    # cv2.imshow("Blur Image", imgBlur)
    cv2.imshow("Canny Image", imgCanny)
    cv2.imshow("imgDialation Image", imgDialation)

    cv2.imshow("img", img)
    cv2.waitKey(0)


if __name__ == '__main__':  # 运行
    main()
