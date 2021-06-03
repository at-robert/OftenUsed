# -*- coding:utf-8 -*-
# file: pysmtp.py
#

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

# To import text color object
pwd = os.path.expanduser('~') + '/'
tools_path = pwd + 'Documents/Github/OftenUsed/Tools'
sys.path.append(tools_path)
import text_color as tc

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
def sendEmail_attach(subject, fullpath):                                 
    try:                                        # 例外處理
        sender = 'robert.lo@amtran.com.tw'
        # recipients = ['robert.lo@amtran.com.tw'] 
        # recipients = ['atttrobert@gmail.com'] 
        recipients = ['robert.lo@amtran.com.tw','louis.lin@amtran.com.tw','dennis.lin@amtran.com.tw','joe.hsiao@amtran.com.tw','darcy.chiu@amtran.com.tw','jason.huang@amtran.com.tw','eric.pan@amtran.com.tw','nice.hsieh@amtran.com.tw']

        emaillist = [elem.strip().split(',') for elem in recipients]
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['Reply-to'] = sender

        pwd = os.path.expanduser('~') + '/'
        auth_data = []
        pass_data = []
        
        search_auth_file(pwd + 'Documents/CERT/auth_ee3_gmail', auth_data, pass_data)
        # search_auth_file(pwd + 'Documents/CERT/auth_amt_gmail', auth_data, pass_data)

        if not os.path.isfile(fullpath):
            print ("{} doesn't exist".format(fullpath))
            sys.exit()

        user = str(auth_data[0]).strip()                     # 取得使用者名稱
        pw = str(pass_data[0]).strip()                       # 取得密碼

        # print(" User = {} , Pass = {} ".format(user,pw))
         
        msg.preamble = 'Multipart massage.\n'
         
        part = MIMEText("Hi All \n\n Please refer to the attached file for AmTRAN JIRA daily report \n\n Thanks!")
        msg.attach(part)
         
        part = MIMEApplication(open(fullpath,"rb").read())
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(fullpath))
        msg.attach(part)
         
        
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(user, pw)
         
        server.sendmail(msg['From'], emaillist , msg.as_string())
        server.quit()                             # 中斷伺服器
        print (tc.bcolors.OKGREEN + "Email sending ok !!" + tc.bcolors.ENDC)

    except :
        print (tc.bcolors.FAIL + "Email sending error !!" + tc.bcolors.ENDC)

#----------------------------------------------------------------------
if __name__ == "__main__":

    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    if len(sys.argv) < 3:
        # print 'no argument; Usage: SendMail_attach.py TITLE FILE'
        # sys.exit()
        print ("Default Title and Path:")
        subject = "AmTRAN JIRA Daily Report !!!"
        # fullpath = "/Volumes/robert.lo/"
        pwd = os.path.expanduser('~') + '/'
        fullpath = pwd + "Downloads/AmTJIRA.txt"
    else:
        subject = str(sys.argv[1])
        fullpath = str(sys.argv[2])

    print (tc.bcolors.CYELLOW + "Title = {}".format(subject) + tc.bcolors.ENDC)
    print ("Full path = {}".format(fullpath))

    sendEmail_attach(subject, fullpath)

