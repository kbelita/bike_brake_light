# Copied from here: https://github.com/turbinenreiter/micropython/blob/master/examples/SDdatalogger/datalogger.py

# datalogger.py
# Logs the data from the acceleromter to a file on the SD-card
# To use: 
# - Turn on pyboard. Don't press usr button until after orange light goes off
# - Press once to start logging
# - Press again to stop logging

import pyb
import machine
from time import sleep_ms

# creating objects
accel = pyb.Accel()
blue = pyb.LED(4)
switch = pyb.Switch()

# Set up the switch to read 0 when not triggered, 1 when triggered
# Wiring: 
# - Connect one side of switch to the 'X1' pin
# - Connect the other side of the switch to ground
brake_switch = machine.Pin('X1', machine.Pin.IN, machine.Pin.PULL_UP)

# Output effect of switch to the red LED matrix
from lights import matrix
brake_lights = matrix.MainGrid()
brake_lights.off()

# Options
sleeptime = 50 #milliseconds; 50 = 20 times/second

# loop
while True:

    # wait for interrupt
    # this reduces power consumption while waiting for switch press
    pyb.wfi()

    # start if switch is pressed
    if switch():
        pyb.delay(200)                      # delay avoids detection of multiple presses
        blue.on()                           # blue LED indicates file open
        log = open('/sd/log.csv', 'w')       # open file on SD (SD: '/sd/', flash: '/flash/)
        log.write("Time,X,Y,Z,Brake\n")

        # until switch is pressed again
        while not switch():




            t = pyb.millis()                            # get time
            x, y, z = accel.filtered_xyz()              # get acceleration data
            braking = brake_switch.value()              # is brake switch triggered?
            log.write('{},{},{},{},{}\n'.format(t,x,y,z,braking))  # write data to file
            
            #TODO this triggers every loop, would be more efficient to toggle
            try:
                if braking == 1:
                    brake_lights.on()
                else:
                    brake_lights.off()
            except Exception as e:
                pass

            sleep_ms(sleeptime)
            

            

        # end after switch is pressed again
        log.close()                         # close file
        blue.off()                          # blue LED indicates file closed
        pyb.delay(200)                      # delay avoids detection of multiple presses
