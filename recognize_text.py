import pytesseract
from pytesseract import Output
import logging

def recognize_text(frame):
  d = pytesseract.image_to_data(frame, output_type=Output.DICT, config="-l eng --psm 9 -c tessedit_char_whitelist='0123456789'")
  n_boxes = len(d['text'])
  
  text = ''
  for i in range(n_boxes):
    logging.warning(d['conf'][i])
    if int(float(d['conf'][i])) > 60:
      logging.warning('Konfidenz ueber 60')
      text = d['text'][i]
      if text and text.strip() != "":
        logging.warn('Erkannter Text! ' + text)
        break
    return text