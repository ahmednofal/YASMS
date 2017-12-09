from datetime import datetime
import time
import socket
def jobj(afb):
    return afb.__dict__
def myip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
peerport = 8880
CAport = 9999
