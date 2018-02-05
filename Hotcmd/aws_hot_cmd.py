import re
import os
import sys
import shutil
import chardet
import time

AWS_PEM='~/Documents/AWS_CERT/jupyterone.pem'
MACHINE_DNS='ec2-54-92-236-169.compute-1.amazonaws.com'

#----------------------------------------------------------------------
def aws_ec2_check_status():
    cmd_str = 'ssh -i ' + AWS_PEM + ' ubuntu@' + MACHINE_DNS
    os.system(cmd_str)
    os.system('cd opencv_ws')
    os.system('cat nohup.out')
    os.system('exit')

#----------------------------------------------------------------------
if __name__ == "__main__":

    aws_ec2_check_status()
    

