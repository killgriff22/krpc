import krpc
import time
from utils import *
KRPC_SERVER = "192.168.1.191"
REPORTER_SERVER = KRPC_SERVER
REPORTER_PORT = 86001
conn = krpc.connect(name='Telemetry',address=KRPC_SERVER)
vessel = conn.space_center.active_vessel
control = vessel.control
print(vessel.name)
ref_frame = conn.space_center.ReferenceFrame.create_hybrid(
    position=vessel.orbit.body.reference_frame,
    rotation=vessel.surface_reference_frame)
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
clear()
reports = {}
t = time.time()
while True:
    _t = time.time()
    dt = _t-t
    velocity = vessel.flight(ref_frame).velocity
    alt = altitude()
    apo = apoapsis()
    if dt > 1:
        reports = request_reports()
    print_at(1, 1, f"Altitude: {alt} Apoapsis: {apo} Vel: {velocity}")
    #print_at(1, 2, f"")