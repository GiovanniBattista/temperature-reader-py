import numpy as np
import argparse
import cv2
import imutils
import logging
from four_point_transform import four_point_transform
from recognize_text import recognize_text

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# works not bad

#scalarLower = (23, 75, 182)
#scalarUpper = (99, 255, 255)

# This should work in the evening
#scalarLower = (10, 43, 255)
#scalarUpper = (142, 255, 255)

# This should work at 10:00 (bedectk)
#scalarLower = (17, 173, 109)
#scalarUpper = (213, 255, 255)

#scalarLower = (21, 78, 94)
#scalarUpper = (49, 255, 255)

def process_frame(frame, scalarLower, scalarUpper, text):
  #frame = imutils.resize(frame, width=600)
  orig = frame.copy()

  blurred = cv2.GaussianBlur(frame, (3, 3), 0)
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  # construct a mask for the color "green", then perform
  # a series of dilations and erosions to remove any small
  # blobs left in the mask
  mask = cv2.inRange(hsv, scalarLower, scalarUpper)
  mask = cv2.erode(mask, None, iterations=2)
  mask = cv2.dilate(mask, None, iterations=4)

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  preview = cv2.bitwise_and(gray, gray, mask=mask)

  # find contours in the edge map, then sort them by their
  # size in descending order
  cnts = cv2.findContours(preview, cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
  
  displayCnt = None

  list_pts = []
  if len(cnts) > 0:
    frame = cv2.drawContours(frame, cnts, -1, (22,22,22), 2)

    i = 0
    for c in cnts:
      list_pts += [pt[0] for pt in c]
      i += 1
      if i == 3:
        break
    displayCnt = np.array(list_pts).reshape((-1,1,2)).astype(np.int32)

  # extract the thermostat display, apply a perspective transform to it
  #warped = four_point_transform(gray, displayCnt.reshape(4, 2))
  if displayCnt is None: 
    output = frame
  else:
    frame = cv2.drawContours(frame, [displayCnt], 0, (255,0,0), 2)
    
    # draw bouding rectangle on frame
    #x,y,w,h = cv2.boundingRect(displayCnt)
    #cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)

    #gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    #pts = np.array( [(x,y), (x+w,y), (x+w,y+h), (x,y+h)])
    #rectangle = four_point_transform(orig, pts)

    rect = cv2.minAreaRect(displayCnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(frame, [box],0,(0,255,0),2)

    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    rectangle = four_point_transform(gray, box)

    # variante 1
    blur = cv2.GaussianBlur(rectangle, (5,5), 0)
    #thresh = cv2.threshold(rectangle, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    recognizedText = recognize_text(thresh)

    if recognizedText and recognizedText != "":
      if len(recognizedText) == 3:
        text = recognizedText[0] + recognizedText[1] + "." + recognizedText[2] + "C"

    # only for debugging
    cv2.imshow("Found", thresh)
        
    frame = cv2.putText(frame, text, box[0], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
  return frame,text