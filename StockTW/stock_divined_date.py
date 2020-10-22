import pandas as pd
import numpy as np
import os
import seleuim_get_goodinfo as goodinfo_se
import send_line as sl

file_name_ = 'tw_stock_div_data.txt'

def count_file_lines(file_):
    file = open(file_,"r") 
    Counter = 0
    
    # Reading from file 
    Content = file.read() 
    CoList = Content.split("\n") 
    
    for i in CoList: 
        if i: 
            Counter += 1
    
    return Counter

def write_to_file(str_a):
    s1 = 0
    s2 = 0

    # with open(file_name_,'r') as f:
    #     print("The size 1 of {} ".format(f.__sizeof__()))
    #     s1 = f.__sizeof__()

    s1 = count_file_lines(file_name_)
    print("The size 1 of {} ".format(s1))

    with open(file_name_,'w') as f:
        for str_ in str_a:
            f.write(str_ + "\n")
            print(str_ + "\n")
        # print("The size 2 of {} ".format(f.__sizeof__()))
        # s2 = f.__sizeof__()

    s2 = count_file_lines(file_name_)
    print("The size 2 of {} ".format(s2))

    if (s1 == s2):
        return 0
    else:
        return 1


def print_stock_divined_date(df_):
    stock_id_list = ['2412','3045','2105','1229']

    key0 = '代碼'
    key1 = '股票名稱'
    key2 = '股東會日期'
    key3 = '除息日程'

    str_list = []

    str_list.append(" {}  -- {} --- {} ".format(key1,key2,key3))
    # print(" {}  -- {} --- {} ".format(key1,key2,key3))

    for i in range(0, len(stock_id_list)):
        stock_df = df_[df_[key0] == stock_id_list[i]]
        
        try:
            if stock_df[[key0]].values[0] == stock_id_list[i]:
                str_list.append(" {} - {} - {}".format(stock_df[[key1]].values[0],stock_df[[key2]].values[0],stock_df[[key3]].values[0]))
                # print(" {} - {} - {}".format(stock_df[[key1]].values[0],stock_df[[key2]].values[0],stock_df[[key3]].values[0]))
        except:
            print("Date Not available ",stock_id_list[i])

    if(write_to_file(str_list) != 0):
        print(" Send Line Message !!")
        sl.lineNotify(str_list)

#----------------------------------------------------------------------
if __name__ == "__main__":

    pwd = os.path.expanduser('~') + '/'
    filepath = pwd + 'Downloads/SaleMonDetail.html'

    if os.path.isfile(filepath):
        print("To delete {} \n".format(filepath))
        os.remove(filepath)
    else:
        print("The file {} doesn't exist\n".format(filepath))

    goodinfo_se.selenium_get_good_info_div()

    if os.path.isfile(filepath):
        df = pd.read_html(filepath, encoding='utf-8')
        arr = df[0]

        # print("The length of arr = {} ".format(len(arr)))
        # print(arr)

        # To get columns value name
        data = np.array(arr[len(arr)-3:len(arr)-2])
        d = data.tolist()
        arr.columns = d[0]
        df = arr[['代碼', '股票名稱', '股東會日期','除息日程']]
        df = df.iloc[:,:4]

        print_stock_divined_date(df)
    else:
        print("The file {} doesn't exist\n".format(filepath))
