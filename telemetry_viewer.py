import krpc
import time
import math
from utils import *
print(request_reports())

exit()

conn = krpc.connect(name='Telemetry', address=KRPC_SERVER)
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
ns = time.time_ns()
_ns = time.time_ns()
flight_profile = {
    f"Target Alt": 0,
    f"Orbit Burn": False,
    f"Return Descent": False,
    f"Carrying Payload": False,
}

while True:
    _t = time.time()
    dt = _t-t
    t = _t
    velocity = [1, 1, 1]
    alt = altitude()
    apo = apoapsis()
    if dt > 1:
        clear()
        pass  # reports = request_reports()
        if "Flight Profile" in reports[0].keys():
            flight_profile = reports[0]['Flight Profile']
    print_i = 1
    print_at(1, print_i, f"frametime {(_ns-ns)/1000000000}")
    print_i += 1
    print_at(
        1, print_i, f"Vessel: {vessel.name} SAS: {control.sas} RCS: {control.rcs} Throttle: {round(control.throttle*100)/100}")
    print_i += 1
    print_at(
        1, print_i, f"Brakes: {control.brakes} Gear: {control.gear} Antennas: {control.antennas} Cargo Bays: {control.cargo_bays} Lights: {control.lights}")
    print_i += 1
    print_at(
        1, print_i, f"Radiators: {control.radiators} Panels: {control.solar_panels} Antennas: {control.antennas} Stage: {control.current_stage} Abort: {control.abort}")
    print_i += 1
    print_at(1, print_i, f"Stage: {control.current_stage} ")
    print_i += 1
    print_at(1, print_i, f"Altitude: {alt} Apoapsis: {apo}")
    print_i += 1
    print_at(1, print_i, f"Velocity, RPH:")
    print_i += 1
    print_at(1, print_i, f"X: {velocity[0]}     R: {control.roll}")
    print_i += 1
    print_at(1, print_i, f"Y: {velocity[1]}     P: {control.pitch}")
    print_i += 1
    print_at(1, print_i, f"Z: {velocity[2]}     H: {control.yaw}")
    print_i += 1
    print_at(1, print_i, f"Time to Surface: {alt/(abs(velocity[0])+1)}")
    print_i += 1
    print_at(1, print_i, f"Flight Profile:")
    print_i += 1
    for i, k in enumerate(list(flight_profile.keys())):
        print_at(1, i+print_i, f"{k}: {flight_profile[k]}")
    print_i += len(list(flight_profile.keys()))
    print_i = 30
    print_at(1, print_i, f"Flight Log:")
    print_i += 1
    for i, log in enumerate(reports):
        print_at(0, print_i+i, log['message'])
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
    ns = _ns
    _ns = time.time_ns()
