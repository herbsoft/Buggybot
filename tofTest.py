from I2C_SW import *
import VL53L1X

SW.chn(1) # This will enable the channel that the ToF sensor is on

tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof1.open()
tof1.start_ranging(1)

distance_in_mm=tof1.get_distance()
print('Distance {}'.format(distance_in_mm))

tof1.stop_ranging()
tof1.close()

SW._rst() # Reset switch and turn off all channels
