import requests
import time, sys
import os
def report_message(addr, msg):
    requests.post(addr, {"message":msg, "timestamp": time.time()})

def request_reports(addr):
    resp = requests.post(addr)
    return resp.json() 

def print_at(x,y,s):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % ( y, x, s))
    sys.stdout.flush()

def clear():
    os.system("clear")