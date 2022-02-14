from imutils.video import VideoStream
import cv2
import time
import numpy as np
from process_frame import process_frame
from camera_calibration import setup_trackbars,get_trackbar_values,show_calibration_window
import os

vs = VideoStream(src=0).start()

# allow the camera or video file to warm up
time.sleep(2.0)

if os.path.isfile('trackbar_values.txt'):
  trackbar_values = np.loadtxt('trackbar_values.txt')
else:
  trackbar_values = [0, 0, 0, 255, 255, 255]

setup_trackbars("HSV", trackbar_values)
text = ''

# keep looping
while True:
  # grab the current frame
  frame = vs.read()
  
  # if we are viewing a video and we did not grab a frame,
  # then we have reached the end of the video
  if frame is None:
    break
  # resize the frame, blur it, and convert it to the HSV
  # color space
  
  show_calibration_window(frame, "HSV")
  v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values("HSV")
  output,text = process_frame(frame, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max), text)

  # show the frame to our screen
  cv2.imshow("Frame", output)
  key = cv2.waitKey(1) & 0xFF
  
  # if the 'q' key is pressed, stop the loop
  if key == ord("q"):
    break

trackbar_values = get_trackbar_values("HSV")
np.savetxt('trackbar_values.txt', trackbar_values, fmt='%d')

# close all windows
cv2.destroyAllWindows()