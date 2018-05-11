import time, math, bno055
from machine import I2C, Pin

print("Starting main.py")
time.sleep(1)

#led = Pin(2, Pin.OUT)

i2c = I2C(-1, Pin(5), Pin(4), freq=400000, timeout=10000)
# i2c.scan()

print("Starting I2C scan")

while True:
    devices = i2c.scan()
    print("Found devices: %s" % (repr(devices)))
    if 41 in devices:
        break

sensor = bno055.BNO055(i2c, address=41)

#sensor.operation_mode(bno055.COMPASS_MODE)
sensor.operation_mode(bno055.NDOF_MODE)
#sensor.operation_mode(bno055.M4G_MODE)
#with open('bno055_readings.txt', 'a+') as file:
while True:
    try:
        ex, ey, ez = sensor.euler()
        w, x, y, z = sensor.quaternion()

        ysqr = y * y
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (ysqr + z * z)
        yaw = math.degrees(math.atan2(t3, t4))

        #yaw  = math.asin(2*x*y + 2*z*w)
        #yawdegrees = yaw * 180/math.pi
        #print("% 4.2f % 4.2f % 4.2f" % (ex, yaw, yawdegrees))
        calib_stat = sensor.calib_stat()
        st_result = sensor.st_result()
        sys_error = sensor.sys_error()
        sys_status = sensor.sys_status()

        print("% 4.2f % 4.2f %s result=%d err=%d status=%d" % (ex, yaw, bin(calib_stat), st_result, sys_error, sys_status))


        mag_status = calib_stat & 3
        acc_status = (calib_stat >> 2) & 3
        gyr_status = (calib_stat >> 4) & 3
        sys_status = (calib_stat >> 6) & 3

        print("mag_status=%d acc_status=%d gyr_status=%d sys_status=%d" % (mag_status, acc_status, gyr_status, sys_status))


        acc = "x=%d y=%d z=%d" % sensor.acc_offset()
        mag = "x=%d y=%d z=%d" % sensor.mag_offset()
        gyr = "x=%d y=%d z=%d" % sensor.gyr_offset()

        sensor.operation_mode(bno055.CONFIG_MODE)

        print("cal acc=(%s) mag=(%s) gyr=(%s) acc_r=%d mag_r=%d" % (acc, mag, gyr, sensor.acc_radius(), sensor.mag_radius()))


        #file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(ex), str(yaw), str(st_result), str(sys_error), str(sys_status), str(mag_status), str(acc_status), str(gyr_status), str(sys_status)))
        # file.write(str(ex))

        sensor._system_trigger(1) # Run a self test.
        sensor.operation_mode(bno055.NDOF_MODE)
        #print("% 4.2f % 4.2f % 4.2f  % -50s %d %s %s" % (x, y, z, sensor.quaternion(), sensor.temperature(), bin(sensor.calib_stat()[0]), bin(sensor.calib_stat()[1])))

    except OSError as e:
        print(dir(e))

    time.sleep(.1)




