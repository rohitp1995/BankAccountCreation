import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from src.ocr import OCR
from validation.verhoff_verification import validateVerhoeff
import json
from log.logger import Logger

class validator:

    def __init__(self, result, image):
        
        self.result = result
        self.image = image
        self.log_obj = Logger('Generatedlogs')
        self.logger = self.log_obj.logging()
        self.ocr_obj = OCR(self.image)

    def isaadharvalid(self):
        
        try:
            self.logger.info('started validating aadhar card')
            if [0,1,2] == self.result:
                
                message = 3

                (name, sex) = self.ocr_obj.store_name_and_sex()
                number = self.ocr_obj.store_aadhar_number()
                dob = self.ocr_obj.store_date()

                if name in ('', None):
                    ## message for name check
                    message = 0
                    return message
                
                elif number in ('', None):
                    ## message for number check
                    message = 1 
                    return message

                elif not validateVerhoeff(number):
                    ## verify number 
                    message = 1.1
                    return message

                elif sex in ('', None) and sex.upper() not in ('MALE', 'FEMALE'):
                    ## message for gender check
                    message = 2
                    return message

                else:
                    ## aadhar verified message
                    details = {"name": name, "dob": dob, "sex": sex, "number": number}
                    json_object = json.dumps(details, indent = 4)

                    with open('output.json', 'w') as f:
                        f.write(json_object) 
                    return message

            else:
                ## image not captured clearly or wrong image
                message = 4
                return message

        except Exception as e:
                self.logger.error('Error while validating aadhar: ' + str(e))
                sys.exit(1) 
