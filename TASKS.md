# ShootingSimulator

## Purpose:
    We want to make a Shooting Simulator that has the following features:
    
    1. Obtain the position where user is aiming by caputure the laser dot pointed by user.
    2. Being able to determine if the user hit the target by calculating the error between the laser dot and the target.
    3. Target's colour will change upon hit.
    4. Being able to obtain the coordinate of the laser dot in real world from pixel coordinate.

### Folder Structure:

- main.py: the entry point of the program
- utils  : The folder the holds all the utility functions

    - 1.process_frame.py : a helper function that does the processing by receiving a frame matrix
    
    - 2.contour_generator.py      : help generate a perfect contour for the shooting target, which is good for later steps of hit detection.        

    - 3.detect_contour_centers.py : find contours and mark the centers of them.
    
    - 4.detect_hit.py             : detects hit area
