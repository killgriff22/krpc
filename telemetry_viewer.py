import krpc
import time
import math
from utils import *

# exit()

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
reports = []
t_1 = time.time()
t_2 = time.time()
ns = time.time_ns()
_ns = time.time_ns()
flight_profile = {}
plan_recived = False
lastcontent = ""
extra_info = ""
rocketimgx = 40
rocketimgy = 20
rocketimg = r"""
         /\         
        /  \        
       /    \       
      /______\      
     |        |     
     |        |     
     |        |     
     |        |     
     |        |     
     |        |     
    /|   ||   |\    
   / |   ||   | \   
  /  |   ||   |  \  
 /___|   ||   |___\ 
     |        |     
      \      /      
       ||  ||       
"""
while True:
    _t = time.time()
    dt_1 = _t-t_1
    dt_2 = _t-t_2
    velocity = vessel.flight(ref_frame).velocity
    alt = altitude()
    apo = apoapsis()
    if dt_1 >= 10:
        t_1 = _t
        os.system("git pull")
        continue
    if dt_2 > 1:
        t_2 = _t
        reports = request_reports()['data']
        while len(reports) > 16:
            reports.pop(0)
        brk = False
        if len(reports) == 0:
            clear()
            continue
            brk = True
        if not brk and not plan_recived:
            if "Flight Profile" in reports[0].keys():
                flight_profile = reports[0]['Flight Profile']
                clear()
                plan_recived = True
    print_i = 30
    print_at(1, print_i, f"Flight Log:")
    print_i += 1
    for i, log in enumerate(reports):
        print_at(0, print_i+i, (log['message']+(" "*40))[:40])
    print_at_mult(rocketimgx, rocketimgy, rocketimg)
    content = open("telemetry_mut.py", "r").read()
    if not content == lastcontent:
        lastcontent = content
        clear()
    exec(compile(f"{content}", "bleh.py", "exec"))
    ns = _ns
    _ns = time.time_ns()
