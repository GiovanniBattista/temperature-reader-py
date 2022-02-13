import cv2

def callback(value):
    pass

def setup_trackbars(range_filter, trackbar_values):
  cv2.namedWindow("Trackbars", 0)

  k = 0
  for i in ["MIN", "MAX"]:

    for j in range_filter:
      v = int(trackbar_values[k])
      k += 1
      cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)

def get_trackbar_values(range_filter):
  values = []

  for i in ["MIN", "MAX"]:
    for j in range_filter:
      v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
      values.append(v)

  return values

def show_calibration_window(frame, range_filter):
  v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  mask = cv2.inRange(hsv, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
  mask = cv2.erode(mask, None, iterations=2)
  mask = cv2.dilate(mask, None, iterations=4)

  #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  #preview = cv2.bitwise_and(gray, gray, mask=mask)

  cv2.imshow("Calibration", mask)