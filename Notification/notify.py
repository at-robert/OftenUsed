
import os
import sys


pwd_path = os.path.expanduser('~') + '/'
sys.path.append(pwd_path + "Documents/Github/OftenUsed/Tools/")
import send_line as sl



#----------------------------------------------------------------------
if __name__ == "__main__":

    out = 'DONE !!'
    print(sl.lineNotify_r(out))