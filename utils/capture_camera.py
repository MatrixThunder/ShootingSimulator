# TODO: https://dmaiorino.com/?p=12
# TODO: install cv2

import cv2, time

def capture_camera(id, process_func,detect_hit,generated_cnts):
    # 1. Create an object
    video = cv2.VideoCapture(id)


    # 2. must add!!! TODO: https://www.raspberrypi.org/forums/viewtopic.php?t=35689#p305473

    # video.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    # cv2.VideoWriter_fourcc(*'MJPG')

    cv2.namedWindow("capturing", 0)
    cv2.resizeWindow("capturing", 800, 600)
    video.set(3, 1280)

    video.set(4, 768)

    a = 0
    while True:
        a = a + 1

        # 3. Create a frame object
        check, frame = video.read()
        # Returns  Center Coordinate X and Y
        # Returns the contour array
        cnts = process_func(frame.copy())

        detect_hit(frame,generated_cnts)
        # detect_hit(frame,cnts)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("capturing", gray)

        # 4 show the frame!
        # cv2.imshow("capturing", frame)

        # 5 For press any key to out (ms)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    print(a)

    video.release()

    cv2.destroyAllWindows




