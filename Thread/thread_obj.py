import threading
import time

class mythread(threading.Thread):
    def __init__(self,num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        for i in range(self.num):
            print("I'm {}".format(i))
            time.sleep(1)
