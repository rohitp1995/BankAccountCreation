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
from database_operation.data_ingestion import insertdata
import json
    

class App:

    def __init__(self, config_path):
        
        self.config = config_path

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
        
        st.title('Application Form')
        with st.form(key = 'form1'):

            record = self.get_record()
            Name = st.text_input("Name", value = record["name"])
            BirthDate = st.text_input("BirthDate", value = record["dob"])
            Gender = st.text_input("Gender", value = record["sex"])
            Email_Address = st.text_input("Email_address")
            submit_button = st.form_submit_button(label = 'Submit')

        if submit_button: 
            st.success(f'Hello {Name}, Your Account has been succesfully created and a mail is sent to you email id with all the details')
            
        btn = st.button('go back')
        if btn :
            st.session_state.runpage = main        
            st.experimental_rerun()

    def main(self):
        st.title("Bank Account Creation")
        st.warning('This is a warning')
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

            if message == 3:
                ## checking if data inserted
                record = self.get_record()
                ins = insertdata(record, self.config)

               ## checking for duplication and inserting 
                insert_message = ins.check_duplicate_and_insert()

                if insert_message == 3:
                    page_switcher(page1)
                    st.experimental_rerun()

                

if __name__ == '__main__':
    ### setting arguments
    args = argparse.ArgumentParser()
    args.add_argument("--setup_info", "-s", default="setup_info.yaml")
    parsed_args = args.parse_args()
    clapp = App(config_path = parsed_args.setup_info)
    
    if 'runpage' not in st.session_state:
        st.session_state.runpage = clapp.main
    st.session_state.runpage()





   




