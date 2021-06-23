import cv2

# 载入并显示图片
img = cv2.imread('H:/Shooting_Simulator/1.jpg')
# cv2.imshow('img',img)
# 灰度化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 输出图像大小，方便根据图像大小调节minRadius和maxRadius
print(img.shape)
# cv2.imshow('gray',gray)

th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY, 11, 2)
#cv2.imshow('binary', th2)

ret, thresh1 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
cv2.imshow('thresh1', thresh1)

canny = cv2.Canny(thresh1, 40, 80)
cv2.imshow('Canny', canny)


canny = cv2.blur(canny, (3, 3))
cv2.imshow('blur', canny)

# 霍夫变换圆检测
circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, 1,
                           100, param1=50, param2=30, minRadius=30, maxRadius=150)
# 输出返回值，方便查看类型
print(circles)
# 输出检测到圆的个数
print(len(circles[0]))

print('-------------我是条分割线-----------------')
# 根据检测到圆的信息，画出每一个圆
for circle in circles[0]:
    if (circle[2] >= 100):
        continue
    # 圆的基本信息
    print(circle[2])
    # 坐标行列
    x = int(circle[0])
    y = int(circle[1])
    # 半径
    r = int(circle[2])

    # 在原图用指定颜色标记出圆的位置
    img = cv2.circle(img, (x, y), r, (0, 0, 255), -1)
# 显示新图像
cv2.imshow('res', img)

# 按任意键退出
cv2.waitKey(0)
cv2.destroyAllWindows()
