import twstock
import time
import requests
import os

stock_list = [['中華電','2412',107,106],['台灣大','3045',97,94],['正新','2105',37,35],['聯華','1229',40,35]]

# 中華電 = 0 , 台灣大 = 1 , 正新 = 2 , 聯華 = 3
idx = 0

stock_name = stock_list[idx][0]
stock_id = stock_list[idx][1]
Max_ = stock_list[idx][2]
Min_ = stock_list[idx][3]

def update_stock_data(idx_):
    stock_name = stock_list[idx_][0]
    stock_id = stock_list[idx_][1]
    Max_ = stock_list[idx_][2]
    Min_ = stock_list[idx_][3]
    print(" {} is setup , id = {} , Max = {} , Min = {}".format(stock_name, stock_id, Max_, Min_))

def lineNotify(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    notify = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return notify.status_code

def sendline(mode, realprice, counterLine, token):
    print(stock_name + '目前股價：' + str(realprice))
    if mode == 1:
        message = stock_name + '現在股價為 ' + str(realprice) + '元，可以賣出股票了！'
    else:
        message = stock_name + '現在股價為 ' + str(realprice) + '元，可以買入股票了！'
    code = lineNotify(token, message)
    if code == 200:
        counterLine = counterLine + 1
        print('第 ' + str(counterLine) + ' 次發送 LINE 訊息。')
    else:
        print('發送 LINE 訊息失敗！')
    return counterLine

pwd = os.path.expanduser('~') + '/'
cert_path = pwd + 'Documents/CERT/Line_Notify_stock.txt'
fp = open(cert_path,"r")
zops = fp.readlines()

token = zops[0]  #權杖
counterLine = 0  #儲存發送次數
counterError = 0  #儲存錯誤次數

print('程式開始執行！')
while True:
    for c in range(0,len(stock_list)):
        stock_name = stock_list[c][0]
        stock_id = stock_list[c][1]
        Max_ = stock_list[c][2]
        Min_ = stock_list[c][3]
        print(" {} is setup , id = {} , Max = {} , Min = {}".format(stock_name, stock_id, Max_, Min_))

        realdata = twstock.realtime.get(stock_id)  #即時資料
        if realdata['success']:
            realprice = realdata['realtime']['latest_trade_price']  #目前股價

            print( "Realtime Price = {}".format(realprice))

            if float(realprice) >= Max_:
                counterLine = sendline(1, realprice, counterLine, token)
            elif float(realprice) <= Min_:
                counterLine = sendline(2, realprice, counterLine, token)
            if counterLine >= 12:  #最多發送3次就結束程式
                print('程式結束！')
                break
        else:
            print('twstock 讀取錯誤，錯誤原因：' + realdata['rtmessage'])
            counterError = counterError + 1
            if counterError >= 3:  #最多錯誤3次
                print('程式結束！')
                break

        for i in range(300):  #每1分鐘讀一次
            time.sleep(1)       
    