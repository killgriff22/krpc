rocketimgx = 60
rocketimgy = 20
time_to_next_pull = round(10-dt_1)
time_to_next_report_pull = round(1-dt_2)
extra_info = (
    f" TTP:{time_to_next_pull} TTR:{time_to_next_report_pull}"+(" "*40))[:40]
print_i = 1
print_at(
    1, print_i, f"frametime {round((_ns-ns)/1000000000)} {extra_info}")
print_i += 1
print_at(
    1, print_i, f"Vessel: {vessel.name} SAS: {control.sas} RCS: {control.rcs} Throttle: {round(control.throttle*100)/100}")
print_i += 1
print_at(
    1, print_i, f"Brakes: {control.brakes} Gear: {control.gear}")
print_i += 1
print_at(
    1, print_i, f"Radiators: {control.radiators} Abort: {control.abort}")
print_i += 1
print_at(1, print_i, f"Stage: {control.current_stage}")
print_i += 1
print_at(1, print_i, f"Altitude: {round(alt)} Apoapsis: {round(apo)}")
print_i += 1
print_at(1, print_i, f"Velocity, RPH:")
print_i += 1
print_at(
    1, print_i, f"X: {round(velocity[0])}     R: {round(control.roll)}")
print_i += 1
print_at(
    1, print_i, f"Y: {round(velocity[1])}     P: {round(control.pitch)}")
print_i += 1
print_at(
    1, print_i, f"Z: {round(velocity[2])}     H: {round(control.yaw)}")
print_i += 1
print_at(
    1, print_i, f"Time to Surface: {round(alt/(abs(velocity[0])+1))}")
print_i += 1
print_at(1, print_i, f"Flight Profile:")
print_i += 1
for i, k in enumerate(list(flight_profile.keys())):
    print_at(1, i+print_i, f"{k}: {flight_profile[k]}")
print_i += len(list(flight_profile.keys()))

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
