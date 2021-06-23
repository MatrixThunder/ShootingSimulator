import cv2
import numpy as np

# img = cv2.imread("../images/gray_background.png")
# img = cv2.imread("../images/test.png")
# img = cv2.imread("../images/laser_dot2.png")
# img = cv2.imread("../images/target.png")
img = cv2.imread("../images/captured_man_target_hit_center.png")

# 转到HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print(hsv)

# 设置阈值
l_blue = np.array([[0, 0, 250]])
h_blue = np.array([180, 30, 255])

# 构建掩模
mask = cv2.inRange(hsv, l_blue, h_blue)

# 进行位运算
res = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("img", img)
cv2.imshow("mask", mask)
cv2.imshow("res", res)

cv2.waitKey(0)
cv2.destroyAllWindows()
