
# coding=UTF-8
import sys
import os
import re



FILE_PATH_OPENAI_CERT=r"D:\work_platform\CERT\openai_cert"


#----------------------------------------------------------------------
def search_auth_file(folder, cert_data_):
    # print ("Target Path = {}".format(folder))
    c = re.compile(r'\[cert\]', re.IGNORECASE)


    fp = open(folder,"r")
    zops = fp.readlines()
    for lineStr in zops:
        if(c.match(lineStr)):
            lineStr = lineStr.strip()
            cert_data_.append(re.sub(c,r'',lineStr))


#----------------------------------------------------------------------
if __name__ == "__main__":


    pwd = os.path.expanduser('~') + '/'
    cert_data = []

    search_auth_file(FILE_PATH_OPENAI_CERT,cert_data)

    print(cert_data[0])