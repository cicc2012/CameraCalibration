import cv2
import numpy as np
import glob

# Define grid size (number of INSIDE corners, not total squares)
CHECKERBOARD = (8, 6) 
SQUARE_SIZE_MM = 25.0  # Measured width of one square

# Prepare 3D object points (0,0,0), (25,0,0), (50,0,0)...
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) * SQUARE_SIZE_MM

objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane

images = glob.glob('calibration_images/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        # Refine corner locations for high precision
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imgpoints.append(corners2)

# Run OpenCV Camera Calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("--- CALIBRATION COMPLETE ---")
print("Camera Matrix (Intrinsics):\n", mtx)
print("Distortion Coefficients:\n", dist)

# Save calibration results to a file for use in your parking project
np.savez("camera_calib.npz", matrix=mtx, dist=dist)
