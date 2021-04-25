from __future__ import print_function
import cv2 as cv
import numpy as np


def laser_coor(image):
    detector = cv.SimpleBlobDetector()  # initiate laser detector
    laser_dot = detector.detect(image)
    x = laser_dot.pt[0]  # x coordinate of the detected laser dot
    y = laser_dot.pt[1]  # y coordinate of the detected laser dot
    s = laser_dot.size  # the diameter of the meaningful laser dot neighborhood
    return x, y, s


def error(lasercor, target):
    ex = np.abs(lasercor[0] - target[0])  # error between target and laser in x-axis
    ey = np.abs(lasercor[1] - target[1])  # error between target and laser in y-axis
    err = np.linalg.norm([ex,ey])  # calculate the Euclidean Distance error
    return err


