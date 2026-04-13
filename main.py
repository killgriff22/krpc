import krpc
import time
from utils import *

conn = krpc.connect(name='Ascent Guidance', address=KRPC_SERVER)
vessel = conn.space_center.active_vessel
control = vessel.control
control.brakes = False
control.rcs = True
control.sas = True
report_message(vessel.name)
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
ap = vessel.auto_pilot
ap.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.engage()
vessel.control.throttle = 1
time.sleep(1)
report_message('Launch!')
vessel.control.activate_next_stage()

mean_altitude = conn.get_call(getattr, vessel.flight(), 'mean_altitude')
expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(mean_altitude),
    conn.krpc.Expression.constant_double(4000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()


report_message('Throttle Back')
vessel.control.throttle = 0
time.sleep(2)

report_message('Secondary parachute deployment')
vessel.control.toggle_action_group(2)

time.sleep(5)
report_message('Faring separation')
vessel.control.activate_next_stage()
report_message('Retrograde')
# Point the vessel in the retrograde direction
ap.target_direction = (0, -1, 0)
# ap.wait()
report_message('Brakes')
control.brakes = True

ref_frame = conn.space_center.ReferenceFrame.create_hybrid(
    position=vessel.orbit.body.reference_frame,
    rotation=vessel.surface_reference_frame)
parachute_flag_b = False
parachute_flag_a = False
while True:
    velocity = vessel.flight(ref_frame).velocity
    alt = altitude()
    if alt < 2000:
        parachute_flag_b = False
        if not parachute_flag_b:
            vessel.control.toggle_action_group(1)
            parachute_flag_b = True
    if alt < 1000 and False:  # BAD.
        if not parachute_flag_a:
            vessel.control.toggle_action_group(3)
            parachute_flag_a = True
    if velocity[0] < 0:
        VerticalVel = abs(velocity[0])

ap.disengage()
