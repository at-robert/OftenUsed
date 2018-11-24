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
def sendEmail_attach(subject, fullpath, fullpath_next):                                      
    try:                                        # 例外處理
        sender = 'robert.lo@amtran.com.tw'
        # recipients = ['robert.lo@amtran.com.tw','wayne.mai@amtran.com.tw'] 
        recipients = ['robert.lo@amtran.com.tw','wayne.mai@amtran.com.tw','tony.tsou@amtran.com.tw','louis.lin@amtran.com.tw','miles.liu@amtran.com.tw','paul.fan@amtran.com.tw','johnson.yang@amtran.com.tw'] 

        # recipients = ['atttrobert@gmail.com'] 
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

        user = str(auth_data[0]).strip()                     # 取得使用者名稱
        pw = str(pass_data[0]).strip()                       # 取得密碼
         
        msg.preamble = 'Multipart massage.\n'
         
        part = MIMEText("Hi Wayne \n\n Please refer to the attached file for FW5 Weekly report \n\n Thanks!")
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
        print ("Email sending ok !!")

        print("To copy {} ".format(fullpath))
        print ("To create %s for the next week" %(fullpath_next))
        shutil.copy(fullpath, fullpath_next)
    except :
        print ("Email sending error !!")

#----------------------------------------------------------------------
if __name__ == "__main__":

    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    Date_offset = 0 # To plus one day for special case
    wknum = datetime.datetime.now().isocalendar()[1] + Date_offset

    if len(sys.argv) < 3:
        print ("Default Title and Path:")
        subject = "FW5 Weekly Report"
        fullpath = r'/Volumes/robert.lo/Data/DOC/Weekly_Report/FW5-report-wk%d.docx' %(wknum)

        if wknum > 52:
            fullpath_next = r'/Volumes/robert.lo/Data/DOC/Weekly_Report/FW5-report-wk1.docx'
        else:
            fullpath_next = r'/Volumes/robert.lo/Data/DOC/Weekly_Report/FW5-report-wk%d.docx' %(wknum + 1)

    else:
        subject = str(sys.argv[1])
        fullpath = str(sys.argv[2])

    print ("Title = %s" %(subject))
    print ("Full path = %s" %(fullpath))
    print ("The current Week Number is : W%d" %(datetime.datetime.now().isocalendar()[1]))

    if os.path.isfile(fullpath_next):
        print ("%s exist so the report was sent before!!" %(fullpath_next))
        sys.exit()

    if not os.path.isfile(fullpath):
        print ("%s doesn't exist" %(fullpath))
        sys.exit()

    sendEmail_attach(subject, fullpath, fullpath_next)

