import datetime
from tkinter.tix import MAX
import pandas as pd
from cal_setup import get_calendar_service

# How to get Google Calendar ID, please refer to the following Evernote "Google Calendar Read" article
CAL_ID_FINISH_TASK = '5h3ema8s5bbua11vdh1vcopfpk@group.calendar.google.com'

def out_to_csv(date_in, sum_):

    cal_dict = {
        "date": date_in,
        "events": sum_,
        }
    cal_dict_df = pd.DataFrame(cal_dict)

    cal_dict_df.sort_values(by=['date'],ascending=True,inplace=True)
    # To output to csv file
    cal_dict_df.to_csv('cal_.csv', encoding='utf-8', index=False)
    

def main():
    cal_id = ['primary',CAL_ID_FINISH_TASK]
    date_ = []
    summary_ = []
    MAX_OUT = 500
    act_out = 0

    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time{}

    d = datetime.datetime.utcnow().date()
    print("Month = {} ".format(d.month))

    tomorrow = datetime.datetime(d.year, 1, 1, 10)
    now = tomorrow.isoformat() + 'Z'

    print('Getting List to 10 events')

    for i in range(0,2):
        events_result = service.events().list(calendarId=cal_id[i], timeMin=now,
                                            maxResults=MAX_OUT, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = start[0:10]
            dt_start = datetime.datetime.strptime(start, "%Y-%m-%d")

            if( dt_start <  datetime.datetime.utcnow()):
                print(start, event['summary'])
                # To store to pandas dataframe
                date_.append(start)
                summary_.append(event['summary'])
                act_out = act_out + 1
    
    out_to_csv(date_, summary_)

    if act_out >= MAX_OUT:
        print (" The actual output {} is larger than {}".format(act_out,MAX_OUT))

if __name__ == '__main__':
    main()