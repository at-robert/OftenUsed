import sys
# sys.path.append("../OftenUsed/NetworkCheck/")
import net_ok
import time


while True:
    if (net_ok.is_connected() == False):
        print(" Network goes off !! ")
        break
    else:
        print(" Network is on !! ")
    time.sleep(60)

