# TODO: https://dmaiorino.com/?p=12
# TODO: install cv2

import cv2, time

# 1. Create an object
video=cv2.VideoCapture(1)


a = 0

# 2. must add!!! TODO: https://www.raspberrypi.org/forums/viewtopic.php?t=35689#p305473
video.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
# cv2.VideoWriter_fourcc(*'MJPG')

cv2.namedWindow("capturing", 0)
cv2.resizeWindow("capturing", 800, 600)
video.set(3,1920)
 
video.set(4,1440)




while True:
    a = a + 1

    # 3. Create a frame object
    check, frame = video.read()

    print(check)
    print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("capturing", gray)


# 4 show the frame!
# cv2.imshow("capturing", frame)



    # 5 For press any key to out (ms)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

print(a)

video.release()

cv2.destroyAllWindows