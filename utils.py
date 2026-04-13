import requests
import time
import sys
import os
KRPC_SERVER = "192.168.1.191"
REPORTER_SERVER = KRPC_SERVER
REPORTER_PORT = 8601
REPORTER_ADDR = f"http://{KRPC_SERVER}:{REPORTER_PORT}/"


def report_message(msg):
    requests.post(REPORTER_ADDR, json={
                  "message": msg, "timestamp": time.time()})


def report_Profile(msg, fp):
    requests.post(REPORTER_ADDR, json={
                  "message": msg, "timestamp": time.time(), "Flight Profile": fp})


def request_reports():
    resp = requests.post(REPORTER_ADDR)
    return resp.json()


def print_at(x, y, s):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, s))
    sys.stdout.flush()


def print_at_mult(x, y, s):
    ss = s.split("\n")
    for i, _s in enumerate(ss):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y+i, x, _s))
        sys.stdout.flush()


def clear():
    os.system("clear")
