import sys
import os
import pandas as pd

from datetime import datetime


# ------------------  To calculate time difference ------------------------------------
def extract_time_data(str_):
    str_date = str_.split('-', 1)[0]
    str_t1 = str_.split('-', 1)[1].split('~', 1)[0]
    str_t2 = str_.split('-', 1)[1].split('~', 1)[1]
    str_date = str_date.strip()
    str_t1 = str_t1.strip()
    str_t2 = str_t2.strip()
    return str_date,str_t1,str_t2

# -------------------  To print Day off time for each person   ---------------------------------------------------------------------
def print_day_off_time(name_ , date_):
    dts = datetime.strptime("00:00", "%H:%M")

    for idx,day_ in enumerate(date_):
        str_date,str_t1,str_t2 = extract_time_data(day_)
        dt1 = datetime.strptime(str_date + " - " + str_t1, "%Y/%m/%d - %H:%M")
        dt2 = datetime.strptime(str_date + " - " + str_t2, "%Y/%m/%d - %H:%M")

        if ( df['Name'][idx] == name_ ):
            print("{}: Name = {} , Date = {} , time spend = {} ".format(idx, df['Name'][idx], str_date, dt2 - dt1))

            if(idx == 0):
                dts = (dt2 - dt1)
            else:
                dts = dts + (dt2 - dt1)
    print(dts)

# str_date,str_t1,str_t2 = extract_time_data("2020/11/10 - 09:00 ~ 12:00")
# dt1 = datetime.strptime(str_date + " - " + str_t1, "%Y/%m/%d - %H:%M")
# dt2 = datetime.strptime(str_date + " - " + str_t2, "%Y/%m/%d - %H:%M")

# # print(" Date = {} , T1 = {} , T2 = {} ".format(str_date,str_t1, str_t2))
# print(dt2 - dt1)

df = pd.read_excel("test_date.xlsx")

print_day_off_time('Robert.Lo', df['Date'])
print_day_off_time('Joe.Hsiao', df['Date'])

print_day_off_time('Darcy.Chiu', df['Date'])
print_day_off_time('Dennis.Lin', df['Date'])

# for idx,day_ in enumerate(df["Date"]):
#     str_date,str_t1,str_t2 = extract_time_data(day_)
#     dt1 = datetime.strptime(str_date + " - " + str_t1, "%Y/%m/%d - %H:%M")
#     dt2 = datetime.strptime(str_date + " - " + str_t2, "%Y/%m/%d - %H:%M")

#     if ( df['Name'][idx] == 'Robert.Lo' ):
#         print("{}: Name = {} , Date = {} , time spend = {} ".format(idx, df['Name'][idx], str_date, dt2 - dt1))

#         if(idx == 0):
#             dts = (dt2 - dt1)
#         else:
#             dts = dts + (dt2 - dt1)

# print(dts)