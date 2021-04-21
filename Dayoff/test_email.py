import gspread
import os
import sys

pwd_path = os.path.expanduser('~') + '/'
sys.path.append(pwd_path + "Documents/Github/OftenUsed/Tools/")
import Emailfuncs as efs


#----------------------------------------------------------------------
if __name__ == "__main__":
    str_ = 'Several people are having vacation tomorrow!!!'
    efs.sendEmail_text('FW3 Day Off Info',str_)