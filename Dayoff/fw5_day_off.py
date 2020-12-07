import gspread
import os
import sys
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

pwd_path = os.path.expanduser('~') + '/'
sys.path.append(pwd_path + "Documents/Github/OftenUsed/Tools/")
import send_line as sl

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
def get_day_off_times(date_):
    # dts = datetime.strptime("00:00", "%H:%M")
    start_dt = []
    end_dt = []

    for idx,day_ in enumerate(date_):
        str_date,str_t1,str_t2 = extract_time_data(day_)
        dt1 = datetime.strptime(str_date + " - " + str_t1, "%Y/%m/%d - %H:%M")
        dt2 = datetime.strptime(str_date + " - " + str_t2, "%Y/%m/%d - %H:%M")
        start_dt.append(dt1)
        end_dt.append(dt2)

    return start_dt,end_dt

# ------------------  To setup Certification and then get work sheet ------------------------------------
def get_cert_and_work_sheet():
    pwd = os.path.expanduser('~') + '/'
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(pwd + 'Documents/Gdrive_credential/client_secret.json', scope)
    client = gspread.authorize(creds)
    google_sheet = "FW5 Day Off"

    sheet = client.open(google_sheet)
    worksheet_year = sheet.worksheet(str(datetime.today().year))
    return worksheet_year

# ------------------  To search for matched day off ------------------------------------
def find_match_day_off(start_,df_):
    times_ls = df_['time'].tolist()
    names_ls = df_['name'].tolist()
    reasons_ls = df_['reason'].tolist()

    today = datetime.today().date()
    tomorrow = today + timedelta(1)  
    out_str = []

    for idx,time in enumerate(start_):
        if time.date() == today or time.date() == tomorrow :
            out_str.append("day Off = {} , Name = {} , Reason = {}".format(time.date(),names_ls[idx],reasons_ls[idx]))

    return out_str

#----------------------------------------------------------------------
if __name__ == "__main__":

    sheet = get_cert_and_work_sheet()
    names = sheet.col_values(1) 
    times = sheet.col_values(2) 
    reasons = sheet.col_values(3) 

    # for i,name in enumerate(names):
    #     if i != 0:
    #         print("Name = {} , Time = {} , Reason = {}".format(names[i],times[i],reasons[i]))

    dayoff_dict = {
    "name": names,
    "time": times,
    "reason": reasons,
    }
    dayoff_dict_df = pd.DataFrame(dayoff_dict)
    dayoff_dict_df
    dayoff_dict_df.replace('', np.nan, inplace=True)
    dayoff_dict_df = dayoff_dict_df.dropna()
    dayoff_df = dayoff_dict_df[1:]

    # print(dayoff_df)
    times_ls = dayoff_df['time'].tolist()

    # to extract start and end time 
    start,end = get_day_off_times(times_ls)

    # print(start)

    out = find_match_day_off(start,dayoff_df)

    if (len(out) > 0):
        sl.lineNotify(out)
        print(out)
