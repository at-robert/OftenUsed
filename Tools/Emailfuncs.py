from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
import os
import datetime
import shutil
import re

#----------------------------------------------------------------------
def search_auth_file(folder, auth_data, pass_data):
    print ("Target Path = %s" %(folder))
    p = re.compile(r'\[pass\]', re.IGNORECASE)
    a = re.compile(r'\[account\]', re.IGNORECASE)

    fp = open(folder,"r")
    zops = fp.readlines()
    for lineStr in zops:
        if(p.match(lineStr)):
            lineStr = lineStr.strip()
            pass_data.append(re.sub(p,r'',lineStr))

        if(a.match(lineStr)):
            lineStr = lineStr.strip()
            auth_data.append(re.sub(a,r'',lineStr))

#----------------------------------------------------------------------
def sendEmail_text(subject, context):
    try:                                        # 例外處理
        sender = 'robert.lo@amtran.com.tw'
        recipients = ['atttrobert@gmail.com','robert.lo@amtran.com.tw','darcy.chiu@amtran.com.tw']
        emaillist = [elem.strip().split(',') for elem in recipients]
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['Reply-to'] = sender

        pwd = os.path.expanduser('~') + '/'
        auth_data = []
        pass_data = []

        search_auth_file(pwd + 'Documents/CERT/auth_ee3_gmail', auth_data, pass_data)

        user = str(auth_data[0]).strip()                     # 取得使用者名稱
        pw = str(pass_data[0]).strip()                       # 取得密碼

        msg.preamble = 'Multipart massage.\n'

        part = MIMEText(context)
        msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(user, pw)

        server.sendmail(msg['From'], emaillist , msg.as_string())
        server.quit()                             # 中斷伺服器
        print ("Email sending ok !!")
    except :
        print ("Email sending error !!")

#----------------------------------------------------------------------
