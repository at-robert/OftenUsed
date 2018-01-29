import socket

REMOTE_SERVER = "www.google.com"
def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        
        return True
    except:
        pass
    return False

def get_lohost_ip():
    return socket.gethostbyname(socket.gethostname())

'''
The test field : below source code should be kept closed in the regular time
'''
# print (is_connected())
# print("local host ip = {}".format(get_lohost_ip()))