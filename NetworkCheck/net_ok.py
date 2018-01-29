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

print (is_connected())
print("local host ip = {}".format(get_lohost_ip()))