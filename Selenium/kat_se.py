from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import sys, os


LIST_FILE = "katlist.txt"

#----------------------------------------------------------------------
def search_auth_file(folder, auth_data, pass_data):
    # print ("Target Path = {}".format(folder))
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

    # print "pass = %s, account = %s" %(pass_data[0],auth_data[0])


#----------------------------------------------------------------------
if __name__ == "__main__":

    pwd = os.path.expanduser('~') + '/'

    # if len(sys.argv) < 2:
    #     print("用法：python kat_se.py <<target url>>")
    #     exit(1)  

    auth_data = []
    pass_data = []

    search_auth_file(pwd + 'Documents/CERT/auth_kat', auth_data, pass_data)

    KATLIST = pwd + 'Downloads/katlist.txt'
    DOWNLOAD_DIR = "/Volumes/Transcend/"  # ★ 指定你自己的路徑
    

    # 建立 Chrome 設定
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ★★ 指定下載位置 ★★
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
    )

    # 建立 Chrome Driver Service
    service = Service(ChromeDriverManager().install())

    # 啟動 Chrome
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 開啟登入頁面
    driver.get("https://katfile.cloud/login.html")
    time.sleep(2)

    # 填寫 login/password
    driver.find_element(By.NAME, "login").send_keys(auth_data[0])
    driver.find_element(By.NAME, "password").send_keys(pass_data[0])

    # 按登入按鈕
    driver.find_element(By.NAME, "submit").click()
    time.sleep(3)

    print("Current URL:", driver.current_url)

    # =========================
    # 讀取 katlist.txt
    # =========================
    with open(KATLIST, "r", encoding="utf-8") as f:
        links = [x.strip() for x in f.readlines() if x.strip()]

    print("讀取到", len(links), "個連結")

    # =========================
    # 處理每一個下載頁面
    # =========================
    for url in links:
        print("開啟:", url)

        # 在新分頁開啟網址
        driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(1)

        # 切換到最新分頁
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(3)

        # =========================
        # 方法 A：若直接有 dlink → 直接下載
        # =========================
        try:
            dlink = driver.find_element(By.ID, "dlink").get_attribute("href")
            print("找到直接下載連結:", dlink)

            # 直接開啟下載連結
            driver.get(dlink)
            time.sleep(3)
            continue

        except Exception:
            pass  # 沒有 dlink → 進入下一步


        # =========================
        # 方法 B：自動按下載按鈕 (id=downloadbtn)
        # =========================
        try:
            download_btn = driver.find_element(By.ID, "downloadbtn")
            download_btn.click()
            print("已自動點擊下載按鈕")

            time.sleep(5)
        except Exception as e:
            print("找不到下載按鈕:", e)

    # 不呼叫 driver.quit() → 留下所有分頁
    print("全部處理完成！")