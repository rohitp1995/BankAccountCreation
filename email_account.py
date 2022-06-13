import smtplib
import zipfile
import time
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate 
from email import encoders
import os
import json


class mail:
    def __init__(self, config):

        param = config['EMAIL']
        self.user = param['USER']
        self.pwd =  param['PWD']
        self.From = param['FROM']
        self.Subject = param['SUBJECT']

    def sendmail(self, To, mail_msg):

        msg = MIMEMultipart()
        msg['From'] = self.From
        msg['To'] = To
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = self.Subject
        msg.attach(MIMEText(mail_msg))        
        
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login(self.user, self.pwd)
            server.sendmail(self.From, To, str(msg))
            server.close()
            print ('successfully sent the mail')
        except Exception as e:
            print(e)

