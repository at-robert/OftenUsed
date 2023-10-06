# _*_ coding: utf-8 *_*
# 程式 10-6 (Python 3 version)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


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

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    if len(sys.argv) < 2:
        print("用法：python Envy_SE.py <<target url>>")
        exit(1)  

    url = sys.argv[1]
    pwd = os.path.expanduser('~') + '/'

    auth_data = []
    pass_data = []
    key_data = []

    search_auth_file(pwd + 'Documents/CERT/auth_envy', auth_data, pass_data, key_data)

    # binary = FirefoxBinary(pwd + 'firefox/firefox')
    # print "path = %s" %(pwd + 'firefox')

    # web = webdriver.Firefox(firefox_binary=binary)
    # web = webdriver.Firefox()
    '''
    To control Chrome
    '''
    web = webdriver.Chrome(pwd + 'chromedriver', chrome_options=chrome_options)

    web.get(url)
    web.set_window_position(0,0)
    web.set_window_size(1442,1051)
    # web.find_element_by_name("submit").click()
    # web.find_element_by_link_text('登錄').click()
    web.find_element("link text", "登錄").click()
    time.sleep(2)

    # ids = web.find_elements_by_xpath('//*[@id]')
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

    # web.find_element("id",'loginanswer_row_'+id_).clear()
    # web.find_element("id",'loginanswer_row_'+id_).send_keys("Taipai")

    web.find_element("name",'answer').send_keys(key_data[0])
    # web.find_element("name","loginsubmit").click()


    # try:
    #     web.find_element_by_link_text(u"[ 點擊這裡返回上一頁 ]").click()

    #     time.sleep(2)
    #     print ("Need to login again!!")
    #     ids = web.find_elements_by_xpath('//*[@id]')

    #     for ii in ids: 
    #         if(re.search(r'^password.*',ii.get_attribute('id'))):
    #             password_id = ii.get_attribute('id')
    #             print (password_id)
    #         elif(re.search(r'^username.*',ii.get_attribute('id'))):
    #             username_id = ii.get_attribute('id')
    #             print (username_id)

    #     web.find_element_by_id(username_id).clear()
    #     web.find_element_by_id(username_id).send_keys("robert_bt")
    #     web.find_element_by_id(password_id).clear()
    #     web.find_element_by_id(password_id).send_keys("070713")
    #     web.find_element_by_name("loginsubmit").click()

    #     time.sleep(3)
    #     # web.find_element_by_link_text(u"成人電影(上傳空間)").click()
    #     web.find_element("link text", u"成人電影(上傳空間)").click()
    #     time.sleep(3)
    #     # web.find_element_by_link_text(u"成人電影(上傳空間)").click()
    #     web.find_element("link text", u"成人電影(上傳空間)").click()
    #     time.sleep(6)
    #     web.find_elements_by_xpath('//*[@id="wp"]/div[4]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/form/input[2]').click()

    # except: 
    #     exit(1)





