import krpc
import time
import math
from utils import *
from MultiTerm import *

import datetime
from pyfiglet import Figlet
import pyfiglet

conn = krpc.connect(name='Telemetry', address=KRPC_SERVER)
# input("Press Enter to continue...")
spc = conn.space_center
t_1 = time.time()
t_2 = time.time()
t_3 = time.time()
ns = time.time_ns()
_ns = time.time_ns()
lastcontent = ""
x = 100
y = 10
ActiveVessel = None
control = None
ref_frame = None
ut = None
altitude = None
apoapsis = None
reports = []
flight_plan = {}

"MultiTerm Setup"
Init()
clear()
f = Figlet("ansi_regular")
w, h = os.get_terminal_size()
SafeZone = (1, 1)
displays = cluster()
display = Screen((w-SafeZone[0]*2, (h-SafeZone[1]*2)), SafeZone)
displays.screens.append(display)
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


def ActiveVessel_DISPLAY():
    global t_1, t_2, t_3, w, h, x, y, ns, _ns, spc, conn, ActiveVessel, lastcontent, rocketimg, reports, flight_plan
    rocketimgx = 60
    rocketimgy = 20
    _t = time.time()
    dt_2 = _t-t_2
    display.fill(" ")
    dt_1 = _t-t_1
    if dt_1 > 10:
        t_1 = _t
        pull()
    if dt_2 > 1:
        t_2 = _t
        reports = safe_request()['data']
        for report in reports:  # use latest flight plan in the list
            if 'fp' in report.keys():
                flight_plan = report['fp']
        reports = reports[-20:]  # keep the latest few messages to display
    velocity = ActiveVessel.flight(ref_frame).velocity
    alt = altitude()
    apo = apoapsis()
    time_to_next_pull = round(10-dt_1)
    time_to_next_report_pull = round(1-dt_2)
    extra_info = (
        f" TTP:{time_to_next_pull} TTR:{time_to_next_report_pull}"+(" "*40))[:40]
    print_i = 1
    display.blit(
        f"frametime {round((t_3-_t))} {extra_info}", (1, print_i))
    print_i += 1
    display.blit(
        f"Vessel: {ActiveVessel.name} SAS: {control.sas} RCS: {control.rcs} Throttle: {round(control.throttle*100)/100}", (1, print_i))
    print_i += 1
    display.blit(
        f"Brakes: {control.brakes} Gear: {control.gear}", (1, print_i))
    print_i += 1
    display.blit(
        f"Radiators: {control.radiators} Abort: {control.abort}", (1, print_i))
    print_i += 1
    display.blit(f"Stage: {control.current_stage}", (1, print_i))
    print_i += 1
    display.blit(
        f"Altitude: {round(alt)} Apoapsis: {round(apoapsis(), 5)}", (1, print_i))
    print_i += 1
    display.blit(f"Velocity, RPH:", (1, print_i))
    print_i += 1
    display.blit(
        f"X: {round(velocity[0])}     R: {round(control.roll)}", (1, print_i))
    print_i += 1
    display.blit(
        f"Y: {round(velocity[1])}     P: {round(control.pitch)}", (1, print_i))
    print_i += 1
    display.blit(
        f"Z: {round(velocity[2])}     H: {round(control.yaw)}", (1, print_i))
    print_i += 1
    display.blit(
        f"Time to Surface: {round(alt/(abs(velocity[0])+1))}", (1, print_i))
    print_i += 1
    display.blit(f"Flight Profile:", (1, print_i))
    print_i += 1
#    for i, k in enumerate(list(flight_profile.keys())):
#        display.blit(1, i+print_i, f"{k}: {flight_profile[k]}")
#    print_i += len(list(flight_profile.keys()))

    rocketimg = rocketimg.split("\n")
    r"""
    |SAS       |       RCS|
    |         /|\         |
    |        / | \        |
    |       /  |  \       |
    |      /___|___\      |
    |     |    |    |     |
    |     |    |    |     |
    |     |    |    |     |
    |     |    |    |     |
    |     |    |    |     |
    |     |    |    |     |
    |    /|   |||   |\    |
    |   / |   |||   | \   |
    |  /  |   |||   |  \  |
    | /___|   |||   |___\ |
    |     |    |    |     |
    |      \   |   /      |
    |       || | ||       |
    |GEAR     |||    BRAKE|
    """
    line_i = 0
    if control.sas:
        rocketimg[line_i] = r"SAS"
    else:
        rocketimg[line_i] = r"   "
    rocketimg[line_i] += "              "
    if control.rcs:
        rocketimg[line_i] += "RCS"
    else:
        rocketimg[line_i] += "   "
    line_i = 18
    if control.gear:
        rocketimg[line_i] = r"GEAR"
    else:
        rocketimg[line_i] = r"    "
    rocketimg[line_i] += "     "
    t = control.throttle
    c = "x"
    if t < .1:
        c = "x"
    if t > .25:
        c = "-"
    if t > .5:
        c = "="
    if t > .9:
        c = "|"
    rocketimg[line_i] += c+c
    rocketimg[line_i] += "    "

    if control.brakes:
        rocketimg[line_i] += "BRAKE"
    else:
        rocketimg[line_i] += "     "
    rocketimg = "\n".join(rocketimg)
    display.blit(rocketimg, (rocketimgx, rocketimgy))
    displays.draw_all()
    t_3 = time.time()


def SPC_DISPLAY():
    global t_1, t_2, t_3, w, h, x, y, ns, _ns, spc, conn, ActiveVessel, lastcontent
    display.fill(" ")
    _t_1 = time.time()
    dt_1 = _t_1-t_1
    if dt_1 > 10:
        t_1 = _t_1
        pull()
    print_i = 1
    display.blit(
        f"frametime {round((_ns-ns)/1000000000)}, time to pull: {10-dt_1}", (1, print_i))
    print_i += 1
    display.blit(f"Active Vessel: {""}", (1, print_i))
    print_i += 1
    display.blit(f"Launchpads:", (1, print_i))
    print_i += 1
    _t_2 = time.time()
    for ls in spc.launch_sites:
        display.blit(f"{ls.name}: {ls.body.name}", (1, print_i))
        print_i += 1
    display.blit(f"Vessels:", (1, print_i))
    print_i += 1
    for v in spc.vessels:
        display.blit(f"{v.name}: {v.recoverable} {v.crew}", (1, print_i,))
        print_i += 1
    _t_3 = time.time()
    display.blit(f"dt_2:{_t_2-_t_3} dt_3:{_t_3-_t_1}", (1, print_i))
    displays.draw_all()


"Main Loop"
while True:
    try:
        ActiveVessel = spc.active_vessel
        control = ActiveVessel.control
        ref_frame = conn.space_center.ReferenceFrame.create_hybrid(
            position=ActiveVessel.orbit.body.reference_frame,
            rotation=ActiveVessel.surface_reference_frame)
        ut = conn.add_stream(getattr, conn.space_center, 'ut')
        altitude = conn.add_stream(
            getattr, ActiveVessel.flight(), 'surface_altitude')
        apoapsis = conn.add_stream(
            getattr, ActiveVessel.orbit, 'apoapsis_altitude')
    except:
        ActiveVessel = None
        control = None
        ref_frame = None
        ut = None
        altitude = None
        apoapsis = None
    if ActiveVessel:
        ActiveVessel_DISPLAY()
        continue
    SPC_DISPLAY()

exit()


pagecontent = """
  00000000000000001111111111111111222222222222222333333333333333444444444444444
  01234567879ABCEF0123456789ABCDEF0123456789ABCEF0123456789ABCEF0123456789ABCEF
00┌───────────────────────────────────────────────────────────────┐            
01│                                                 /\\           │            
02│                                                /  \\          │            
03│                    \\|   \\                     /    \\         │            
04│                   \\\\\\ \\ \\                    /______\\        │            
05│                     \\\\  \\  \\                |        |        │            
06│                     \\ \\   \\-                |        |        │            
07│                     \\\\-\\   \\\\\\              |        |        │            
08│                      ┌─┐   ┌─┐              |        |        │            
09│                      │ │   │ │              |        |        │            
0A│                      │ │   │ │              |        |        │            
0B│                      │ │   │ │             /|   ||   |\\      │            
0C│                      │ │   │ │            / |   ||   | \\     │            
0D│                      │ │   │ │           /  |   ||   |  \\    │            
0E│  ┌───────────────────│ │───│ │          /___|   ||   |___\\   │            
0F│  │                   │ │   │ │              |        |        │            
10│  │        ┌────┐     │ │   │ │               \\      /         │            
11│  │        │    │     │ │   │ │                ||  ||          │            
12│  │        └────┘     │ │   │ │           ┌──────────────┐     │            
13│  │  ┌───┐            │ │   │ │          /    /          │     │            
14│  │  │   │            │ │   │ │     ┌───/    /           │     │            
15│  │  │   │            └─┘   └─┘     │  /    /            |     │            
16│  │  │   │                    │  ┌────/────/─────────────|───┐ │            
17│  └──└───┘────────────────────┘  └───────────────────────────┘ │            
18└───────────────────────────────────────────────────────────────┘            
19                                     └────────┘                              
1A                                                                             
1B                                                                             
1C                                                                             
1D                                                                             
1E                                                                             
1F                                                                             
"""
while True:
    _t = time.time()
    dt = _t-t
    if dt > 10:
        t = _t
        pull()
        clear()
    print_i = 1
    print_at(1, print_i, f"frametime {round((_ns-ns)/1000000000)}")
    print_i += 1
    print_at(
        1, print_i, f"Active Vessel: {""}")
    print_i += 1
    print_at(
        1, print_i, f"Vessels:")
    print_i += 1
    for ls in spc.launch_sites:
        print_at(
            1, print_i, f"{ls.name}: {ls.body.name}")
        print_i += 1
    for v in spc.vessels:
        print_at(
            1, print_i, f"{v.name}: {v.recoverable} {v.crew}")
        print_i += 1
    content = open("muts.py", "r").read()
    if not content == lastcontent:
        lastcontent = content
        clear()
    exec(compile(f"{content}", "bleh.py", "exec"))
    print_at_mult(x, y, pagecontent)
    ns = _ns
    _ns = time.time_ns()
