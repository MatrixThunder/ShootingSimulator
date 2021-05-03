import numpy as np
import cv2

def floodFill(start_pt):
    matrix_np = np.asarray(matrix)
    numeric_matrix = np.where(matrix_np=="a", 255, 0).astype(np.uint8)
    mask = np.zeros(np.asarray(numeric_matrix.shape)+2, dtype=np.uint8)
    # start_pt = (y,x)
    if matrix_np[start_pt]:
    cv2.floodFill(numeric_matrix, mask, start_pt, 255, flags=4)
    mask = mask[1:-1, 1:-1]
    matrix_np[mask==1] = "c"
    matrix = matrix_np.tolist()
