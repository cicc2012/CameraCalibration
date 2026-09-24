from picamera2 import Picamera2, Preview
import time
import os

picam2 = Picamera2()

camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)

picam2.start_preview(Preview.QTGL)
picam2.start()

# Allow the camera to warm up
time.sleep(2)

output_path = "/home/rob/Documents/cam/cv/calibration/"
# Create the folder if it doesn't already exist
os.makedirs(output_path, exist_ok=True)

# Capture 20 images, one every 5 seconds
for i in range(20):
    filename = f"image_{i+1:02d}.jpg"
    filepath = os.path.join(output_path, filename)
    picam2.capture_file(filepath)
    print(f"Captured {filepath}")

    # Wait 5 seconds before the next image
    if i < 19:
        time.sleep(5)

picam2.close()