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
        pass#reports = request_reports()
    print_i = 1
    print_at(1, print_i, f"Vessel: {vessel.name} SAS: {control.sas} RCS: {control.rcs}")
    print_i += 1
    print_at(1, print_i, f"Altitude: {alt} Apoapsis: {apo}")
    print_i += 1
    print_at(1, print_i, f"Velocity:")
    print_i += 1
    print_at(1, print_i, f"X: {velocity[0]}")
    print_i += 1
    print_at(1, print_i, f"Y: {velocity[1]}")
    print_i += 1
    print_at(1, print_i, f"Z: {velocity[2]}")
    print_i += 1
    print_at_mult(200, 20, """
         /\\
        /  \\
       /    \\
      /______\\
     |        |
     |        |
     |        |
     |        |
     |        |
     |        |
    /|   ||   |\\
   / |   ||   | \\
  /  |   ||   |  \\
 /___|   ||   |___\\
     |        |
      \      /
       ||  ||
""")