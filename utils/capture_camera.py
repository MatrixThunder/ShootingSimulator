# TODO: https://dmaiorino.com/?p=12
# TODO: install cv2

import cv2, time

# 1. Create an object
video=cv2.VideoCapture(0)

# 2. must add!!! TODO: https://www.raspberrypi.org/forums/viewtopic.php?t=35689#p305473
video.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

# 3. Create a frame object
check, frame = video.read()

print(check)
print(frame)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imshow("capturing", gray)


# 4 show the frame!
# cv2.imshow("capturing", frame)



# 5 For press any key to out (ms)

cv2.waitKey(0)

video.release()