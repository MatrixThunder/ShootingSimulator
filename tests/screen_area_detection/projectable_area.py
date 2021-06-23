import cv2
import time
import json
import imutils
import cv2
import numpy as np


from cv2 import aruco
from imutils.video import VideoStream


def show_full_frame(frame):
    """
    Given a frame, display the image in full screen
    :param frame: image to display full screen
    """
    cv2.namedWindow('Full Screen', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(
        'Full Screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow('Full Screen', frame)


def hide_full_frame(window='Full Screen'):
    """
    Kill a named window, the default is the window named 'Full Screen'
    :param window: Window name if different than default
    """
    cv2.destroyWindow(window)


def get_reference_image(img_resolution=(1680, 1050)):
    """
    Build the image we will be searching for.  In this case, we just want a
    large white box (full screen)
    :param img_resolution: this is our screen/projector resolution
    """
    width, height = img_resolution
    img = np.ones((height, width, 1), np.uint8) * 255
    return img


def undistort_image(image, camera_matrix=None, dist_coeffs=None, prop_file=None):
    """
    Given an image from the camera module, load the camera properties and correct
    for camera distortion
    """
    resolution = image.shape
    if len(resolution) == 3:
        resolution = resolution[:2]
    # if camera_matrix is None and dist_coeffs is None:
    #     camera_matrix, dist_coeffs = load_camera_props(prop_file)
    # Shape gives us (height, width) so reverse it
    resolution = resolution[::-1]
    new_camera_matrix, valid_pix_roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix,
        dist_coeffs,
        resolution,
        0
    )
    mapx, mapy = cv2.initUndistortRectifyMap(
        camera_matrix,
        dist_coeffs,
        None,
        new_camera_matrix,
        resolution,
        5
    )
    image = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)
    return image


def find_edges(frame):
    """
    Given a frame, find the edges
    :param frame: Camera Image
    :return: Found edges in image
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Add some blur
    edged = cv2.Canny(gray, 30, 200)  # Find our edges
    return edged


def get_region_corners(frame):
    """
    Find the four corners of our projected region and return them in
    the proper order
    :param frame: Camera Image
    :return: Projection region rectangle
    """
    edged = find_edges(frame)
    # findContours is destructive, so send in a copy
    contours, hierachy = cv2.findContours(
        edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort our contours by area, and keep the 10 largest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screen_contours = None

    for idx, c in enumerate(contours):
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # If our contour has four points, we probably found the screen
        if len(approx) == 4:

            print(idx)
            screen_contours = approx
            # break
            # cv2.drawContours(frame, [screen_contours], -1, (0, 255, 0), 3)
            # cv2.imshow('Screen', frame)

        else:
            print('Did not find contour')

    try:
        # Uncomment these lines to see the contours on the image
        cv2.drawContours(frame, [screen_contours], -1, (0, 255, 0), 3)

        x, y = [], []

        for contour_line in [screen_contours]:
            for contour in contour_line:
                x.append(contour[0][0])
                y.append(contour[0][1])

        x1, x2, y1, y2 = min(x), max(x), min(y), max(y)

        cropped = frame[y1:y2, x1:x2]

        cv2.imshow('Screen', frame)
        cv2.imshow('Cropped', cropped)

        # cv2.waitKey(0)
        pts = screen_contours.reshape(4, 2)
        rect = order_corners(pts)
        print("rect %s" % rect)
        return rect

    except Exception:
        print("except!")


def order_corners(pts):
    """
    Given the four points found for our contour, order them into
    Top Left, Top Right, Bottom Right, Bottom Left
    This order is important for perspective transforms
    :param pts: Contour points to be ordered correctly
    """
    rect = np.zeros((4, 2), dtype='float32')

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def get_destination_array(rect):
    """
    Given a rectangle return the destination array
    :param rect: array of points  in 
    [
    - tl top left, 
    - tr top right,
    - br bottom right,
    - bl bottom left
    ] 
    format
    """
    (tl, tr, br, bl) = rect  # Unpack the values

    # Compute the new image width
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    # Compute the new image height
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    # Our new image width and height will be the largest of each
    max_width = max(int(width_a), int(width_b))
    max_height = max(int(height_a), int(height_b))

    # Create our destination array to map to top-down view
    dst = np.array([
        [0, 0],  # Origin of the image, Top left
        [max_width - 1, 0],  # Top right point
        [max_width - 1, max_height - 1],  # Bottom right point
        [0, max_height - 1],  # Bottom left point
    ], dtype='float32')
    return dst, max_width, max_height


def get_perspective_transform(stream, screen_resolution):
    """
    Determine the perspective transform for the current physical layout
    return the perspective transform, max_width, and max_height for the
    projected region
    :param stream: Video stream from our camera
    :param screen_resolution: Resolution of projector or screen
    :param prop_file: camera property file
    """
    try:
        reference_image = get_reference_image(screen_resolution)

        # Display the reference image
        # show_full_frame(reference_image)
        # Delay execution a quarter of a second to make sure the image is displayed
        # Don't use time.sleep() here, we want the IO loop to run.  Sleep doesn't do that
        cv2.waitKey(1)

        # Grab a photo of the frame
        frame = stream.read()
        # We're going to work with a smaller image, so we need to save the scale
        ratio = frame.shape[0] / 300.0

        # # Undistort the camera image
        # frame = undistort_image(frame)

        orig = frame.copy()
        # Resize our image smaller, this will make things a lot faster
        frame = imutils.resize(frame, height=300)

        rect = get_region_corners(frame)
        rect *= ratio  # We shrank the image, so now we have to scale our points up

        dst, max_width, max_height = get_destination_array(rect)

        # Remove the reference image from the display
        # hide_full_frame()

        m = cv2.getPerspectiveTransform(rect, dst)

        # Uncomment the lines below to see the transformed image
        # wrap = cv2.warpPerspective(orig, m, (max_width, max_height))

        # cv2.imshow('all better', wrap)
        # cv2.waitKey(0)
        return m, max_width, max_height
    except Exception:
        print("except!")


if __name__ == '__main__':

    # args = parse_args()
    # Camera frame resolution
    # resolution = (args.get('camera_width'), args.get('camera_height'))

    stream = VideoStream(usePiCamera=False, resolution=(320, 240)).start()

    time.sleep(2)  # Let the camera warm up

    screen_res = (320, 240)

    while(True):
        get_perspective_transform(stream, screen_res)
        # frame = stream.read()
        # cv2.imshow('Screen', frame)
        # stream.stop()
        # cv2.waitKey(1)

    stream.stop()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
