from utils import process_frame as process_frame
from utils import detect_contour_centers as dcc
from utils import detect_hit as dh
from utils import contour_generator as cg
from utils import grab_game_area as gga
import time

from imutils.video import VideoStream

import cv2


if __name__ == '__main__':

    # 1. 读取标靶图片。 Reading the picture you want to use as the target
    target_img = cv2.imread("./images/target_blue_ridge.jpg")
    # target_img = cv2.imread("./images/man_target_none.png")
    cv2.imshow("target_img", target_img)

    # 2. 生成轮廓，用于计分/高亮击中区域
    # 2. Generating contours and dialations for next steps (scoring / show hit area)
    generated_cnts, generated_dialation = cg.contour_generator(target_img)

    # cc.capture_camera("utils/recording3.mp4",dcc.detect_contour_centers,dh.detect_hit, generated_cnts) # pre-recorded video for testing
    # - 用 grab_game_area.py 生成一个frame

    # 3. 获取视频流.
    # 3. Get VideoStream from default camera.
    stream = VideoStream(usePiCamera=False, resolution=(320, 240)).start()

    # TODO: python里面，import的代码里面的相对路径
    # 是相对于调用处的路径！！！！！！

    time.sleep(2)  # Let the camera warm up

    # 4. 将 stream 传入 grab_game_area, 会进行剪裁操作，并返回一个只有游戏区域的Matrix
    # 4. The videostream is passed into grab_game_area
    # in which it's going to crop the game area out from the
    while True:
        resized = gga.grab_game_area(stream, target_img)
        # cv2.imshow("resized", resized)

        # 5.然后放进process frame 里面处理：
        # 5.It is then processed in the process frame function.
        process_frame.process_frame(resized, dcc.detect_contour_centers,
                                    dh.detect_hit, generated_cnts, generated_dialation)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

            # start_processing.start_processing("./videos/man_target_2.mp4", dcc.detect_contour_centers,
            #                                   dh.detect_hit, generated_cnts, generated_dialation)

            # cc.capture_camera(0, dcc.detect_contour_centers,
            #                   dh.detect_hit, generated_cnts, generated_dialation) # on-cam shooting
