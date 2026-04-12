import krpc
import time
conn = krpc.connect(name='Telemetry',address="192.168.1.191")
vessel = conn.space_center.active_vessel
control = vessel.control
print(vessel.name)
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')