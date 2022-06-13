import cv2
import numpy as np
import pytesseract
import re
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from log.logger import Logger
from src.utils.utils import zoom

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCR:

    def __init__(self, image):
        
        self.image = image
        self.log_obj = Logger('Generatedlogs')
        self.logger = self.log_obj.logging()

    def store_name_and_sex(self):

        try:
            self.logger.info('Started fetching name from the image')
            img = cv2.imread(self.image)   

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, 1.3, 7)
            sex = 'NA'
            if len(faces) != 0:
                self.logger.info('Started fetching name and gender')

                for (x, y, w, h) in faces:

                    roi_color = gray[y-60: y + h+40, x: x + w+900]
                    text = pytesseract.image_to_string(roi_color)
                    name = str(re.findall(r"[A-Z][a-z]+,?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+", text, flags=re.DOTALL)).replace("]", "").replace("[","").replace("'", "")
                    sex = str(re.findall(r"Male|MALE|Female|FEMALE", text)).replace("[","").replace("'", "").replace("]", "")
            else:         
                name = None

            return name, sex
            self.logger.info('Completed fetching name from image') 

        except Exception as e:
            self.logger.error('Error while storing the name: ' + str(e))
            sys.exit(1)
        
    def store_aadhar_number(self):

        try:
            self.logger.info('Started fetching aadhar number from the image')
            img = cv2.imread(self.image)   

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, 1.3, 7)
            
            if len(faces) != 0:
                for (x, y, w, h) in faces:
                    for z in range(1,4):    
                        roi_gray = gray[x+w+90: x+w + 50000, x+w: x+w + 50000]
                        roi_gray_zoom = zoom(roi_gray, z)
                        text = pytesseract.image_to_string(roi_gray_zoom).upper().replace(" ", "")
                        number = str(re.findall(r"[0-9]{11,12}", text)).replace("]", "").replace("[","").replace("'", "")
                        
                        if number not in ('', None):
                            break
                        else:
                            continue
                return number 

            else:      
                number = ''
                return number

        except Exception as e:
            self.logger.error('Error while storing the name: ' + str(e))
            sys.exit(1)


    def store_date(self):

        try:
            self.logger.info('Started fetching other details from the image')
            img = cv2.imread(self.image)
            rgb_planes = cv2.split(img)

            result_planes = []
            result_norm_planes = []
            
            for plane in rgb_planes:
                dilated_img = cv2.dilate(plane, np.ones((10, 10), np.uint8))       
                bg_img = cv2.medianBlur(dilated_img, 21)
                diff_img = 255 - cv2.absdiff(plane, bg_img)
                norm_img = cv2.normalize(diff_img, None, alpha=0, beta=250, norm_type=cv2.NORM_MINMAX,
                                                            dtype=cv2.CV_8UC1)
                result_planes.append(diff_img)
                result_norm_planes.append(norm_img)

            result = cv2.merge(result_planes)
            result_norm = cv2.merge(result_norm_planes)
            dst = cv2.fastNlMeansDenoisingColored(result_norm, None, 10, 10, 7, 11)   
    
            text = pytesseract.image_to_string(dst).upper().replace(" ", "")

            date = str(re.findall(r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}", text)).replace("]", "").replace("[","").replace("'", "")
            
            if date in ('',None):
                date = '01/01/1960'

            return date
            self.logger.info('Completed fetching other details from image') 
        
        except Exception as e:
            self.logger.error('Error while fetching other details from image: '+ str(e))
            sys.exit(1)
