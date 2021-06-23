from utils import capture_camera as cc
from utils import detect_contour_centers as dcc
from utils import detect_hit as dh
from utils import contour_generator as cg
from utils import detect_contour_centers as d

import cv2


if __name__ == '__main__':

    # 读取标靶图片。 Reading the picture you want to use as the target
    target_img = cv2.imread("./images/man_target_none.png")
    # 生成轮廓，用于计分。 Generating contours and dialations for next steps (scoring / show hit area)
    generated_cnts, generated_dialation = cg.contour_generator(target_img)

    # cc.capture_camera("utils/recording3.mp4",dcc.detect_contour_centers,dh.detect_hit, generated_cnts) # pre-recorded video for testing
    cc.capture_camera("./videos/man_target_2.mp4", dcc.detect_contour_centers,
                      dh.detect_hit, generated_cnts, generated_dialation)
    # cc.capture_camera(0, dcc.detect_contour_centers,
    #                   dh.detect_hit, generated_cnts, generated_dialation) # on-cam shooting
