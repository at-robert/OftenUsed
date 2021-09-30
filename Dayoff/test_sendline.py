
import os
import sys


pwd_path = os.path.expanduser('~') + '/'
sys.path.append(pwd_path + "Documents/Github/OftenUsed/Tools/")
import send_line as sl



#----------------------------------------------------------------------
if __name__ == "__main__":

    out = 'test fw3 string'
    sl.lineNotify_fw3_leader(out)