# _*_ coding: utf-8 *_*
# 程式 10-6 (Python 3 version)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.service import Service

import time
import re
import sys, os

#----------------------------------------------------------------------
def search_auth_file(folder, auth_data, pass_data, key_data):
    # print ("Target Path = {}".format(folder))
    p = re.compile(r'\[pass\]', re.IGNORECASE)
    a = re.compile(r'\[account\]', re.IGNORECASE)
    k = re.compile(r'\[key\]', re.IGNORECASE)

    fp = open(folder,"r")
    zops = fp.readlines()
    for lineStr in zops:
        if(p.match(lineStr)):
            lineStr = lineStr.strip()
            pass_data.append(re.sub(p,r'',lineStr))

        if(a.match(lineStr)):
            lineStr = lineStr.strip()
            auth_data.append(re.sub(a,r'',lineStr))

        if(k.match(lineStr)):
            lineStr = lineStr.strip()
            key_data.append(re.sub(k,r'',lineStr))

    # print "pass = %s, account = %s" %(pass_data[0],auth_data[0])

#----------------------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("用法：python Envy_SE.py <<target url>>")
        exit(1)  

    url = sys.argv[1]
    pwd = os.path.expanduser('~') + '/'

    auth_data = []
    pass_data = []
    key_data = []

    search_auth_file(pwd + 'Documents/CERT/auth_envy', auth_data, pass_data, key_data)

    '''
    To control Chrome
    '''
    service = Service(executable_path= pwd + 'chromedriver')
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    web = webdriver.Chrome(service=service, options=options)

    web.get(url)
    web.set_window_position(0,0)
    # web.set_window_size(1442 + 610 ,1071)
    web.maximize_window()
    web.find_element("link text", "登錄").click()
    time.sleep(2)

    ids = web.find_elements("xpath",'//*[@id]')

    for ii in ids: 
        if(re.search(r'^password.*',ii.get_attribute('id'))):
            password_id = ii.get_attribute('id')
            print (password_id)
        elif(re.search(r'^username.*',ii.get_attribute('id'))):
            username_id = ii.get_attribute('id')
            print (username_id)

    web.find_element("id",username_id).clear()
    web.find_element("id",username_id).send_keys(auth_data[0])
    web.find_element("id",password_id).clear()
    web.find_element("id",password_id).send_keys(pass_data[0])

    str_ = username_id.split('_')
    id_ = str_[1]
    print(id_)

    # find id of option
    x = web.find_element("id",'loginquestionid_' + id_)
    drop=Select(x)
     
    # select by visible text
    drop.select_by_visible_text("父親出生的城市")

    time.sleep(3)

    print('loginanswer_row_' + id_ )

    web.find_element("name",'answer').send_keys(key_data[0])
    web.find_element("name","loginsubmit").click()





