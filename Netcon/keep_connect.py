import os
import time

while True:
    os.system("ping www.google.com.tw -c 5")
    print("Wait for 1 minute")
    time.sleep(60)
    