# TODO: https://dmaiorino.com/?p=12
# TODO: install cv2

import cv2, time

import sys
import logging as log

# https://www.pianshen.com/article/25231761732/
cascPath = "C:/Users/Rickson Judao Zhong/AppData/Local/Programs/Python/Python39/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"
pathEyes = 'C:/Users/Rickson Judao Zhong/AppData/Local/Programs/Python/Python39/Lib/site-packages/cv2/data/haarcascade_eye.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
eyesCascade = cv2.CascadeClassifier(pathEyes)

# 1. Create an object
video=cv2.VideoCapture(0)


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
    # cv2.putText(frame,'eyes detected!',(25,25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    print(check)
    print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,1.1,3)

    for (x, y, w, h) in faces:
        print("face detected!")
        cv2.rectangle(gray, (int(x), int(y)), (int(x+w), int(y+h)), (255, 255, 0), 2)
        face_re = gray[y:y+h, x:x+h]
        face_re_g = gray[y:y+h, x:x+h]
        eyes = eyesCascade.detectMultiScale(face_re_g)
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(face_re,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
            print("eyes detected!")
            cv2.putText(gray,'eyes detected!',(25,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

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