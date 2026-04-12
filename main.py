import krpc
import time

message_reporter_address = "192.168.1.199"

conn = krpc.connect(name='Ascent Guidance', address="192.168.1.191")
vessel = conn.space_center.active_vessel
control = vessel.control
control.brakes = False
control.rcs = True
control.sas = True
print(vessel.name)
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
ap = vessel.auto_pilot
ap.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.engage()
vessel.control.throttle = 1
time.sleep(1)
print('Launch!')
vessel.control.activate_next_stage()

mean_altitude = conn.get_call(getattr, vessel.flight(), 'mean_altitude')
expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(mean_altitude),
    conn.krpc.Expression.constant_double(4000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()


print('Throttle Back')
vessel.control.throttle = 0
time.sleep(2)

print('Secondary parachute deployment')
vessel.control.toggle_action_group(2)

time.sleep(5)
print('Faring separation')
vessel.control.activate_next_stage()
print('Retrograde')
# Point the vessel in the retrograde direction
ap.target_direction = (0, -1, 0)
#ap.wait()
print('Brakes')
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
    if alt < 1000:
        if not parachute_flag_a:
            vessel.control.toggle_action_group(3)
            parachute_flag_a = True
    if velocity[0] < 0:
        VerticalVel = abs(velocity[0])
    
ap.disengage()
