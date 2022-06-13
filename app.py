import os
import streamlit as st
import argparse 
import warnings
from PIL import Image, ImageOps
warnings.filterwarnings('ignore')
import time
import json
from predictor import Predict
from validation.validator import validator
from src.ocr import OCR
from src.utils.common import read_config
from database_operation.mongo_operation import MongodbOperations
from database_operation.data_ingestion import insertdata
from src.account_number import AccountNumber
from src.utils.get_mail_message import replace_placeholders
from email_account import mail
import json

class App:

    def __init__(self, config_path):
        
        self.config = config_path
        self.config_obj = read_config(self.config)
        self.db_ops = MongodbOperations(self.config_obj['database']['username'], self.config_obj['database']['pwd'])
        self.next_acc = AccountNumber(self.config_obj)
        self.mail = mail(self.config_obj)

    def get_record(self):
        with open('output.json', 'r') as openfile:
            json_object = json.load(openfile)
            return json_object

    def progress_bar(self, timesleep):
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(timesleep)
            my_bar.progress(percent_complete + 1)

    def page_switcher(self, page):
        st.session_state.runpage = page
        
    def page1(self):
        record = self.get_record()
        ins = insertdata(record, self.config)
        insert_message = ins.check_duplicate()
        aadhar_number = record["number"]

        if insert_message == 3:

            st.title('Application Form')
            with st.form(key = 'form1'):

                Name = st.text_input("Name", value = record["name"])
                BirthDate = st.text_input("BirthDate", value = record["dob"])
                Gender = st.text_input("Gender", value = record["sex"])
                aadhar_number = st.text_input("AadharNumber", value = record["number"])
                Email_Address = st.text_input("Email_address")
                submit_button = st.form_submit_button(label = 'Submit')
            
            if submit_button:
                ## adding email and account number in our database and then emailing to the email specified
                ins.insert()
                st.success(f'Hello {Name}, Your Account has been succesfully created and a mail is sent to you email id with all the details')
                condition = {'number': aadhar_number}
                mail   = {"$set": {'email': Email_Address}}
                self.db_ops.AddnewField(self.config_obj['database']['db_name'], self.config_obj['database']['collection'],
                                        condition, mail)
                acc_number = self.next_acc.get_account_number()
                set_acc_number = {"$set": {'account_number': acc_number}}
                self.db_ops.AddnewField(self.config_obj['database']['db_name'], self.config_obj['database']['collection'],
                                        condition, set_acc_number)
                ## sending email
                mail_msg = replace_placeholders(Name, acc_number)
                self.mail.sendmail(Email_Address, mail_msg)

            btn = st.button('go back')
            if btn :
                    st.session_state.runpage = self.main        
                    st.experimental_rerun()

        else:
            st.error('The Aadhar entry already exists in the database')
            btn = st.button('go back')
            if btn :
                    st.session_state.runpage = self.main        
                    st.experimental_rerun()
      

    def main(self):
        st.title("Bank Account Creation")
        st.text("Upload a clear aadhar card image for the account creation")

        uploaded_file = st.file_uploader("Choose a aadhar card image ...", type="jpg")
        if uploaded_file is not None:

        ## adding image for processing     
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Aadhar.', use_column_width=True)
        
            st.write("")
            st.caption('Validating the image, Please wait')
            self.progress_bar(0.01)

            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            ##making prediction
            predictor = Predict(uploaded_file.name, 'coco/output.json')
            result = predictor.get_prediction()
            
            ## validating and inserting into db if valid
            val_obj = validator(result, uploaded_file.name)
            message = val_obj.isaadharvalid()

            print(uploaded_file.name)
            os.remove(uploaded_file.name)

            with open('message.json', 'r') as openfile:
                text_m = json.load(openfile)

            if message == 3:
                self.page_switcher(self.page1)
                st.experimental_rerun()

            elif message == 0:
                st.error(text_m["0"])

            elif message == 1:
                st.error(text_m["1"])

            elif message == 1.1:
                st.error(text_m["1.1"])
            
            elif message == 2:
                st.error(text_m["2"])

            else:
                st.error(text_m["4"])


if __name__ == '__main__':
    ### setting arguments
    args = argparse.ArgumentParser()
    args.add_argument("--setup_info", "-s", default="setup_info.yaml")
    parsed_args = args.parse_args()
    clapp = App(config_path = parsed_args.setup_info)
    
    if 'runpage' not in st.session_state:
        st.session_state.runpage = clapp.main
    st.session_state.runpage()





   




