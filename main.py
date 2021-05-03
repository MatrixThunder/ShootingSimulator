from utils import capture_camera as cc
from utils import detect_contour_centers as dcc
from utils import detect_hit as dh
from utils import contour_generator as cg
import cv2
if __name__ == '__main__':
    target_img = cv2.imread("man_target_none.png")
    generated_cnts = cg.contour_generator(target_img)
    # cc.capture_camera("utils/recording3.mp4",dcc.detect_contour_centers,dh.detect_hit, generated_cnts)
    cc.capture_camera("man_target.mp4",dcc.detect_contour_centers,dh.detect_hit, generated_cnts)