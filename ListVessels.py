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

Init()
clear()
f = Figlet("ansi_regular")
w, h = os.get_terminal_size()
SafeZone = (1, 1)
displays = cluster()
display = Screen((w-SafeZone[0]*2, (h-SafeZone[1]*2)), SafeZone)
displays.screens.append(display)
while True:
    display.fill(" ")
    time = datetime.datetime.now()
    H = 12 if int(time.strftime("%H")) % 12 == 0 else int(
        time.strftime("%H")) % 12
    Hours = f.renderText(time.strftime(
        f"{H}/%M/%S"))
    ampm = f.renderText(time.strftime("%p"))
    Date = f.renderText(time.strftime("%d/%m/%Y"))
    display.blit(Hours, (display.size[0]//2-len(Hours.split("\n")[0])//2, display.size[1]//2-len(Hours.split("\n"))//2), front_modifier=Fore.RED +
                 Back.BLACK, back_modifier=RESET)
    display.blit(ampm, (display.size[0]//2+len(Hours.split("\n")[0])//2+1, display.size[1]//2-len(ampm.split("\n"))//2),
                 front_modifier=Fore.RED+Back.BLACK, back_modifier=RESET)
    display.blit(Date, (display.size[0]//2-len(Date.split("\n")[0])//2, display.size[1]//2+3),
                 front_modifier=Fore.RED+Back.BLACK, back_modifier=RESET)
    displays.draw_all()


exit()

conn = krpc.connect(name='Telemetry', address=KRPC_SERVER)
# input("Press Enter to continue...")
spc = conn.space_center
clear()
t = time.time()
ns = time.time_ns()
_ns = time.time_ns()
lastcontent = ""
x = 100
y = 10
ActiveVessel = None
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
