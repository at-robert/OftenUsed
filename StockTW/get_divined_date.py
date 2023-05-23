import datetime 
import requests
import pandas as pd
import re
import platform
import os



stock_ids = ['2105', '3045', '2412', '2892', '0056', '00878']
stock_names = ['正新','台灣大','中華電','第一金','元大高股息','國泰高股息']
FILE_PATH_FINMIND_CERT=r"D:\work_platform\CERT\finmind"
FILE_PATH_MACOS_FINMIND_CERT= 'Documents/CERT/finmind'

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

    start_date = datetime.date(2023, 5, 1)
    end_date = start_date + datetime.timedelta(days=180)

    pwd = os.path.expanduser('~') + '/'
    cert_data = []

    if platform.system() == 'Darwin':
        print("It's Mac OS system!!")
        path_ = pwd + FILE_PATH_MACOS_FINMIND_CERT
    else:
        path_ = FILE_PATH_FINMIND_CERT

    url = "https://api.finmindtrade.com/api/v4/data"
    date_format = '%Y-%m-%d'
    merge_data = []
    idx = 0

    search_auth_file(path_,cert_data)

    # print("Cert = {}".format(cert_data[0]))

    for stock_id in stock_ids:
        print(f"Get stock_id:{stock_id}")
        parameter = {
            "dataset": "TaiwanStockDividend",
            "data_id":stock_id,
            "start_date": datetime.datetime.strftime(start_date, date_format),
            "end_date": datetime.datetime.strftime(end_date, date_format),
            "token": cert_data[0], # 參考登入，獲取金鑰
        }
        data = requests.get(url, params=parameter)
        data = data.json()
        TaiwanStockDividend = pd.DataFrame(data['data'])
        if not TaiwanStockDividend.empty:     
            TaiwanStockDividend = TaiwanStockDividend[
                [
                    'date',
                    'stock_id',
                    'StockExDividendTradingDate',
                    'CashExDividendTradingDate',
                    'CashDividendPaymentDate',
                    'StockEarningsDistribution',
                    'StockStatutorySurplus',
                    'CashEarningsDistribution',
                    'CashStatutorySurplus'
                ]
            ]
            TaiwanStockDividend['TotalStock'] = TaiwanStockDividend['StockEarningsDistribution'] + TaiwanStockDividend['StockStatutorySurplus']
            TaiwanStockDividend['TotalCash'] = TaiwanStockDividend['CashEarningsDistribution'] + TaiwanStockDividend['CashStatutorySurplus']
            TaiwanStockDividend['Name'] = stock_names[idx]
            merge_data.append(TaiwanStockDividend)
            
        idx = idx + 1

    # print(merge_data)
        
    merge_datas = pd.concat(merge_data, axis=0)
    merge_datas = merge_datas.sort_values(by=["CashExDividendTradingDate"])
    merge_datas = merge_datas[
        [
            'date',
            'stock_id',
            'StockExDividendTradingDate',
            'CashExDividendTradingDate',
            'CashDividendPaymentDate',
            'TotalStock',
            'TotalCash',
            'Name'
        ]
    ]

    merge_datas.to_csv('Out.csv')
    print(merge_datas)