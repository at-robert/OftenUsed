
import os
import sys
import shutil
import re
from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#----------------------------------------------------------------------
def is_time_normal(last_t, next_t):
    dt = datetime.strptime(last_t, '%H:%M:%S')
    dt1 = datetime.strptime(next_t, '%H:%M:%S')
    res = dt1 - dt
    if res.days < 0:
        return False
    else:
        return True

#----------------------------------------------------------------------
def check_time_order(file_):
    rule = re.compile(r'^[0-9]{2}:[0-9]{2}:[0-9]{2}', re.IGNORECASE)
    last_time = '00:00:00'
    dt = datetime.strptime(last_time, '%H:%M:%S')

    linenum = 0
    with open(file_ , 'rb') as f:
        for line in f:
            linenum = linenum + 1
            linestr = line.decode("utf-8") 
            if(rule.search(linestr)):
                m = re.match(r'^[0-9]{2}:[0-9]{2}:[0-9]{2}', linestr, re.IGNORECASE)
                match_str = m.group(0)

                if is_time_normal(last_time,match_str) == False:
                    print (" Line[{}] = {}".format(linenum,match_str))
                    return False

                last_time = match_str

    return True

#----------------------------------------------------------------------
def search_file(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".srt"):
                #print "Found File = %s" %(file)
                #print (os.path.join(root, file))
                fullpath = os.path.join(root, file)
                print (" Found File = \n{}".format(fullpath))

                if check_time_order(fullpath) == True:
                    print(bcolors.BOLD + " {} is ok".format(fullpath) + bcolors.ENDC)
                else:
                    print("Please check {}".format(fullpath))
                    return


#----------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ('no argument; Usage: python srt_check.py IN_PATH')
        sys.exit()
    
    target_path = str(sys.argv[1])
    print ("Target Path = {}".format(target_path))
    search_file(target_path)