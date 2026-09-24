# CameraCalibration
Camera mount angle changes daily, but the lens itself doesn't — focal length and distortion coefficients are fixed properties of the camera/lens pair. So we will do two different calibrations:
- **Intrinsic calibration (once, ever):** standard OpenCV checkerboard calibration → `camera_matrix`, `dist_coeffs`. Save to disk, reuse forever. Undistort every frame with this before anything else.
- **Extrinsic calibration (daily, ~10 sec):** just the ground homography, using a known rectangle shape. This is the part that changes when the mount gets bumped.
