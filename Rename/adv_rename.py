import os
import sys
import shutil
import re
from datetime import datetime



#----------------------------------------------------------------------
def search_file(folder):
    num_file = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".mp4"):
                fullpath = os.path.join(root, file)

                s = file.split(' ')

                split_tup = s[0].split('.')
                # print(len(split_tup))

                if (len(split_tup) == 1):
                    print (" Found File with Full path = \n{}".format(fullpath))
                    # print (" Filename = {} \n".format(s))
                    # print (" Full Path = {} \n".format(root))
                    new_file = root + '/' + split_tup[0] + '_' + str(num_file) + '.mp4'
                    print (" New Name = {} \n".format(new_file))
                    os.rename(fullpath,new_file)
                    num_file = num_file + 1




#----------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ('no argument; Usage: python adv_rename.py IN_PATH')

        pwd = os.path.expanduser('~') + '/'
        fullpath = pwd + "Downloads/v"

        target_path = fullpath
        print ("Target Path = {}".format(target_path))
        search_file(target_path)

    else:
        target_path = str(sys.argv[1])
        print ("Target Path = {}".format(target_path))
        search_file(target_path)