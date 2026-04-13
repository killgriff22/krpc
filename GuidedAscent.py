import krpc
import time
import random
from utils import *
FLIGHT_PROFILE = {
    "Target Apo": 4000,
    "Descent Alt": 2000,
    "Orbit Burn": False,
    "Return Descent": True,
    "Carrying Payload": False,
    "Payload Drop Height": 50000,
    "Landed Margin Alt": 10,
    "Landed Margin": 5,
}
conn = krpc.connect(name='Ascent Guidance', address=KRPC_SERVER)
spc = conn.space_center
vessel = conn.space_center.active_vessel
control = vessel.control
control.brakes = False
control.rcs = True
control.sas = True
report_Profile(vessel.name, FLIGHT_PROFILE)
input("Flight Plan sent! await ready to launch!")
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
ref_frame = conn.space_center.ReferenceFrame.create_hybrid(
    position=vessel.orbit.body.reference_frame,
    rotation=vessel.surface_reference_frame)
ap = vessel.auto_pilot
ap.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.engage()
vessel.control.throttle = 1
time.sleep(1)
report_message('Launch!')
vessel.control.activate_next_stage()
while altitude() < 1000:
    pass
control.gear = False
while apoapsis() < FLIGHT_PROFILE['Target Apo']:
    pass


report_message('Throttle Back')
vessel.control.throttle = 0
time.sleep(2)

if FLIGHT_PROFILE['Carrying Payload']:
    report_message('Await Drop Height')
    while altitude() < FLIGHT_PROFILE['Payload Drop Height']:
        pass
else:
    report_message('Await Apoapsis')
    delta_altapo = apoapsis() - altitude()
    t = time.time()
    while delta_altapo > 100:
        velocity = vessel.flight(ref_frame).velocity
        _t = time.time()
        delta_altapo = apoapsis() - altitude()
        if _t-t >= .5:
            report_message(f"Time to Apoapsis: {delta_altapo/velocity[0]}")
            report_message(f"Delta to Apoapsis: {delta_altapo}")
            t = _t
        pass
report_message('Faring separation')
vessel.control.activate_next_stage()


report_message('Prepare for Reentry')

if altitude() > 10000:
    if not control.get_action_group(4):
        control.toggle_action_group(4)


report_message('Secondary parachute deployment')
vessel.control.toggle_action_group(2)

if FLIGHT_PROFILE['Carrying Payload']:
    input("await user to circularize payload!\nPress enter when ready!")

    while altitude() > 10000:
        pass


report_message('Retrograde')
# Point the vessel in the retrograde direction
ap.target_direction = (0, -1, 0)
# ap.wait()
report_message('Brakes')
control.brakes = True


parachute_flag_b = False
parachute_flag_a = False
report_message("begin control loop")
msg1 = False
msg2 = False
msg3 = False
msg4 = False
msg5 = False
msg6 = False
while FLIGHT_PROFILE["Return Descent"]:
    velocity = vessel.flight(ref_frame).velocity
    alt = altitude()
    if alt < FLIGHT_PROFILE['Descent Alt']:
        if not control.gear:
            control.gear = True
        if not parachute_flag_b:
            report_message('Pop Primary Parachute')
            vessel.control.toggle_action_group(1)
            control.gear = True
            parachute_flag_b = True
    if alt < FLIGHT_PROFILE['Descent Alt'] and velocity[0] < -60:
        msg1 = True
        msg2 = False
        msg3 = False
        msg4 = False
        msg5 = False
        msg6 = False
        if not msg1:
            report_message('half descent burn half      ')
        control.throttle = .4
    if alt < 500 and velocity[0] < -15:
        msg1 = False
        msg2 = True
        msg3 = False
        msg4 = False
        msg5 = False
        msg6 = False
        if not msg2:
            report_message('half descent burn half      ')
        control.throttle = .4
    if alt < FLIGHT_PROFILE['Descent Alt'] and velocity[0] < -160:
        msg1 = False
        msg2 = False
        msg3 = True
        msg4 = False
        msg5 = False
        msg6 = False
        if not msg3:
            report_message('max descent burn max        ')
        control.throttle = 1
    if alt < FLIGHT_PROFILE['Descent Alt'] and alt > 500 and velocity[0] > -30:
        msg1 = False
        msg2 = False
        msg3 = False
        msg4 = True
        msg5 = False
        msg6 = False
        if not msg4:
            report_message('cut descent burn cut        ')
        control.throttle = 0
    if alt < FLIGHT_PROFILE['Descent Alt'] and alt < 500 and velocity[0] < -10:
        msg1 = False
        msg2 = False
        msg3 = False
        msg4 = False
        msg5 = True
        msg6 = False
        if not msg5:
            report_message('quarter descent burn quarter')
        control.throttle = .4
    if alt < FLIGHT_PROFILE['Descent Alt'] and alt < 500 and velocity[0] > -2:
        msg1 = False
        msg2 = False
        msg3 = False
        msg4 = False
        msg5 = False
        msg6 = True
        if not msg6:
            report_message('cut descent burn cut        ')
        control.throttle = 0
    if abs(altitude()-FLIGHT_PROFILE['Landed Margin Alt']) < FLIGHT_PROFILE['Landed Margin']:
        break
time.sleep(10)
spc.screenshot(f"{random.randint(1000, 9999)}.png")
spc.quickload()

exit()
