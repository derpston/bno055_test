import time
import pyb

led = pyb.Pin("C6", pyb.Pin.OUT_PP)

import machine
i = machine.I2C(-1, scl=pyb.Pin.cpu.C9, sda=pyb.Pin.cpu.A8, freq=400000, timeout=10000)
i.scan()

import bno055
#s = bno055.BNO055(i)

while True:
    devices = i.scan()
    print("Found devices: %s" % (repr(devices)))
    if 41 in devices:
        break

s = bno055.BNO055(i, address=41)

time.sleep(1)

#s.operation_mode(bno055.COMPASS_MODE)
s.operation_mode(bno055.NDOF_MODE)
#s.operation_mode(bno055.M4G_MODE)

import math

while True:
    try:
        ex, ey, ez = s.euler()
        w, x, y, z = s.quaternion()
        
        ysqr = y * y
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (ysqr + z * z)
        yaw = math.degrees(math.atan2(t3, t4))

        #yaw  = math.asin(2*x*y + 2*z*w)
        #yawdegrees = yaw * 180/math.pi
        #print("% 4.2f % 4.2f % 4.2f" % (ex, yaw, yawdegrees))
        print("% 4.2f % 4.2f %s result=%d err=%d status=%d" % (ex, yaw, bin(s.calib_stat()), s.st_result(), s.sys_error(), s.sys_status()))
        acc = "x=%d y=%d z=%d" % s.acc_offset()
        mag = "x=%d y=%d z=%d" % s.mag_offset()
        gyr = "x=%d y=%d z=%d" % s.gyr_offset()
        s.operation_mode(bno055.CONFIG_MODE)
        print("cal acc=(%s) mag=(%s) gyr=(%s) acc_r=%d mag_r=%d" % (acc, mag, gyr, s.acc_radius(), s.mag_radius()))
        s._system_trigger(1) # Run a self test.
        s.operation_mode(bno055.NDOF_MODE)
        #print("% 4.2f % 4.2f % 4.2f  % -50s %d %s %s" % (x, y, z, s.quaternion(), s.temperature(), bin(s.calib_stat()[0]), bin(s.calib_stat()[1])))
    except OSError as e:
        print(dir(e))
    time.sleep(1)


#while True:
#   for _ in range(3):
#       led.on()
#       time.sleep(0.1)
#       led.off()
#       time.sleep(0.1)
#   time.sleep(0.5)

