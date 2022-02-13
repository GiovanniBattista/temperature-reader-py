import cv2
from recognize_text import recognize_text
import logging

frame = cv2.imread('webcam_found2.png')

text = recognize_text(frame)

logging.warning('Recognized text: ' + text)