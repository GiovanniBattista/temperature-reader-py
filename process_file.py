import cv2
from process_frame import process_frame

scalarLower = (10, 43, 255)
scalarUpper = (142, 255, 255)

frame = cv2.imread('webcam3.png')

output = process_frame(frame)

cv2.imshow("Frame", output)
key = cv2.waitKey(0)