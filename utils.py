import requests
import time
import sys
import os
import krpc
KRPC_SERVER = "192.168.1.191"
REPORTER_SERVER = KRPC_SERVER
REPORTER_PORT = 8601
REPORTER_ADDR = f"http://{KRPC_SERVER}:{REPORTER_PORT}/"
DEBUG = False


def round(num, places=2):
    s = str(num).split(".")
    if len(s) == 1:
        return num
    return float(s[0]+"." + s[1][:2])


def report_message(msg, clear=False):
    requests.post(REPORTER_ADDR, json={
                  "message": msg, "timestamp": time.time(), 'clear': clear})


def report_Profile(msg, fp):
    requests.post(REPORTER_ADDR, json={
                  "message": msg, "timestamp": time.time(), "Flight Profile": fp, 'clear': True})


def safe_report(msg, fp=None, clear=False):
    try:
        if fp:
            report_Profile(msg, fp)
        else:
            report_message(msg, clear)
        return True
    except:
        return False


def request_reports():
    resp = requests.post(REPORTER_ADDR)
    return resp.json()


def safe_request():
    try:
        return request_reports()
    except:
        return {'data': []}


def move_cursor(row, col):
    # ANSI sequence to move cursor to (row, col)
    sys.stdout.write(f"\x1B[{row};{col}H")
    sys.stdout.flush()


def print_at(x, y, s):
    screensize = os.get_terminal_size().columns
    s = (s+(" "*screensize))[:screensize]
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, s))
    sys.stdout.flush()


def print_at_mult(x, y, s):
    ss = s.split("\n")
    for i, _s in enumerate(ss):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y+i, x, _s))
        sys.stdout.flush()


def clear():
    os.system("clear")


def pull():
    move_cursor(0, 0)
    os.system("git pull")
    move_cursor(0, 0)


class FlightController:
    def __init__(self):
        self.conn = krpc.connect(name='Ascent Guidance', address=KRPC_SERVER)
        self.spc = self.conn.space_center
        self.active_vessel = None
        self.mj = None

    def init_mechjeb(self):
        self.mj = self.conn.mech_jeb

    def get_active_vessel(self):
        try:
            self.active_vessel = self.spc.active_vessel
        except:
            self.active_vessel = None

    def set_brakes(self, state: bool = None):
        """Will set the state of the brakes actuation if given one, will toggle otherwise.

        Args:
            state (Bool, optional): the state of the Brakes. Defaults to None.
        """
        self.get_active_vessel()
        if self.active_vessel:
            self.active_vessel.control.brakes = state if state is not None else not self.active_vessel.control.brakes

    def set_rcs(self, state: bool = None):
        """Will set the state of the RCS value if given one, will toggle otherwise.

        Args:
            state (Bool, optional): the state of the craft RCS. Defaults to None.
        """
        self.get_active_vessel()
        if self.active_vessel:
            self.active_vessel.control.rcs = state if state is not None else not self.active_vessel.control.rcs

    def set_rcs_ap(self, state: bool = None):
        """Will set the state of the RCS value if given one, will toggle otherwise.

        Args:
            state (Bool, optional): the state of the auto pilot RCS. Defaults to None.
        """
        self.get_active_vessel()
        if self.active_vessel:
            self.active_vessel.auto_pilot.rcs = state if state is not None else not self.active_vessel.auto_pilot.rcs

    def set_sas(self, state: bool = None):
        """Will set the state of the SAS value if given one, will toggle otherwise.

        Args:
            state (Bool, optional): the state of the craft SAS. Defaults to None.
        """
        self.get_active_vessel()
        if self.active_vessel:
            self.active_vessel.control.sas = state if state is not None else not self.active_vessel.control.sas

    def set_sas_ap(self, state: bool = None):
        """Will set the state of the SAS value if given one, will toggle otherwise.

        Args:
            state (Bool, optional): the state of the auto pilot SAS. Defaults to None.
        """
        self.get_active_vessel()
        if self.active_vessel:
            self.active_vessel.auto_pilot.sas = state if state is not None else not self.active_vessel.auto_pilot.sas

    def set_gear(self, state: bool = None):
        """Will set the state of the Gear value if given one, will toggle otherwise.

        Args:
            state (Bool, optional): the state of the Landing Gear. Defaults to None.
        """
        self.get_active_vessel()
        if self.active_vessel:
            self.active_vessel.control.gear = state if state is not None else not self.active_vessel.control.gear

    def set_throttle(self, state: int = None):
        """Will set the state of the throttle actuation if given one, will toggle otherwise.

        Args:
            state (int, optional): the state of the Throttle. Defaults to None.
        """
        self.get_active_vessel()
        if self.active_vessel:
            self.active_vessel.control.throttle = state if state is not None else 0 if self.active_vessel.control.throttle > 0 else 1

    def surface_altitude(self) -> float:
        """Will return the surface altitude variable from the active vessel's flight()

        Returns:
            float: Surface Altidude.
        """
        self.get_active_vessel()
        if self.active_vessel:
            return self.active_vessel.flight().surface_altitude
