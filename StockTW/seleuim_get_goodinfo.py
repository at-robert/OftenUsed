from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

import time
import re
import sys, os

def selenium_get_good_info_div():
    url = 'https://goodinfo.tw/StockInfo/StockDividendScheduleList.asp?MARKET_CAT=%E4%B8%8A%E5%B8%82&INDUSTRY_CAT=%E5%85%A8%E9%83%A8&YEAR=2020'
    pwd = os.path.expanduser('~') + '/'

    # 不打開瀏覽器執行
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')

    web = webdriver.Chrome(pwd + 'chromedriver')
    web.get(url)
    web.set_window_position(0,0)
    web.set_window_size(800,600)

    ids = web.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr/td/div/nobr/input[2]").click()
    time.sleep(4)

    web.quit()

