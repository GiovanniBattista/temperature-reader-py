import pytesseract
from pytesseract import Output
import logging

def recognize_text(frame):
  d = pytesseract.image_to_data(frame, output_type=Output.DICT, config="--tessdata-dir ./tessdata -l LCDDot_FT_500 --psm 9 -c tessedit_char_whitelist='0123456789'")
  n_boxes = len(d['text'])
  
  text = ''
  for i in range(n_boxes):
    if int(float(d['conf'][i])) >= 0:
      vtext = d['text'][i]
      if vtext and vtext.strip() != "":
        text += vtext
        #break
  return text