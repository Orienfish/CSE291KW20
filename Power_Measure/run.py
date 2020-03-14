#!/usr/bin/python3
from ina219_pi import ina219_pi

SOLAR = dict(address = 0x40, logFile = "./data/solar.csv")
BAT = dict(address = 0x41, logFile = "./data/bat.csv")
DEV = dict(address = 0X44, logFile = "./data/dev.csv")

SAMPLE_INTERVAL = 10 # 10 s
sensors = []
for pwr_sensor in [SOLAR, BAT, DEV]:
    cur_sensor = ina219_pi(address=pwr_sensor['address'], \
        filename=pwr_sensor['logFile'])
    cur_sensor.run(SAMPLE_INTERVAL)
    sensors.append(cur_sensor)

print('start sampling with interval {} seconds...'.format(SAMPLE_INTERVAL))
print('press \'q\' to quit.')
while True:
    key = input()
    if key == 'q':
        break
print('wait for threads to join...')
for cur_sensor in sensors:
    cur_sensor.stop()
