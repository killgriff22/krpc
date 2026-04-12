import krpc
import time
conn = krpc.connect(name='Hello World')
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
time.sleep(10)
print('Launch!')
vessel.control.activate_next_stage()

ref_frame = conn.space_center.ReferenceFrame.create_hybrid(
    position=vessel.orbit.body.reference_frame,
    rotation=vessel.surface_reference_frame)

while True:
    velocity = vessel.flight(ref_frame).velocity
    alt = altitude()
    #x,y,z = [float(a) for a in vel]
    print('Surface velocity = (%.1f, %.1f, %.1f)' % velocity)
    print(f'Altitude: {altitude()}')
    VerticalVel = velocity[0]
    if velocity[0] < 0:
        VerticalVel = abs(velocity[0])
    if VerticalVel > 300:
        control.throttle = 0
    if VerticalVel < 250:
        control.throttle = .5
    if alt > 70_000:
        exit()
    
ap.disengage()
