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
import os

from math import atan, atan2, sin, cos, radians, degrees, sqrt, pow, pi

# creating objects
accel = pyb.Accel()
blue = pyb.LED(4)
orange = pyb.LED(3)
switch = pyb.Switch()

# Throw away first 4 readings of filtered_xyz, since it is returned as a sum of last 4 calls
# This ensures first reading is on the same basis as other readings
for i in range(0,4):
    x,y,z = accel.filtered_xyz()


def main():

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
    sleeptime = 20 #milliseconds; 20 = 50 times/second

    # infinite loop allows data logging while the system is on
    while True:

        # wait for interrupt
        # this reduces power consumption while waiting for switch press
        pyb.wfi()

        # start if switch is pressed
        if switch():

            blue.on() #Acknowledge button press
            pyb.delay(200)                      # delay avoids detection of multiple presses

           
            #Calibrate - assume no motion for 2 seconds after button is pressed
            blue.off() #indicate that calibration is occuring - data not yet logging
            orange.on()
            pitch,roll = calc_tilt_angles()
            
            #Create the log file
            filename = make_filename('/sd/log','.csv')
            log = open(filename, 'w')           # open file on SD (SD: '/sd/', flash: '/flash/)
            orange.off()
            blue.on() #indicate data logging is starting
            log.write("pitch_degrees:{},roll_degrees:{},Time,X,Y,Z,Brake\n".format(pitch,roll))

            #Initialize some loop utility variables
            brake_lights.off() #make sure this matches previous_braking
            previous_braking = 0
            last_save_t = pyb.millis() #initialize to now

            # until switch is pressed again
            while not switch():

                #Get the data and log it
                t = pyb.millis()                            # get time
                #x, y, z = accel.filtered_xyz()              # get acceleration data
                x = accel.x()
                y = accel.y()
                z = accel.z()
                braking = brake_switch.value()              # is brake switch triggered?
                log.write('{},{},{},{},{},{},{}\n'.format('','',t,x,y,z,braking))  # write data to file
                
                #Toggle the lights if needed
                if previous_braking != braking:
                    try:
                       brake_lights.toggle()
                    except Exception as e:
                        #Needed because the I2C connection sometimes has timeout errors. 
                        # It's more important to continue logging, and let the lights
                        # toggle on the next switch press instead.
                        pass

                #autosave the data in case of crash during long write function
                if t > (last_save_t + 1000):
                    last_save_t = t
                    log.close()
                    log = open(filename,'a')

                #Wrap up stuff in the loop
                previous_braking = braking
                sleep_ms(sleeptime)

            # end after switch is pressed again
            log.close()                         # close file
            blue.off()                          # blue LED indicates file closed
            pyb.delay(200)                      # delay avoids detection of multiple presses

def scale_accel(xyz_tuple):
    x,y,z = xyz_tuple

    # Calibration factors from previous testing
    x_zero = 6
    y_zero = 0
    z_zero = 1
    scale = 88

    xAcc = (x - x_zero)/scale
    yAcc = (y - y_zero)/scale
    zAcc = (z - z_zero)/scale

    return xAcc,yAcc,zAcc

def calc_tilt_angles():
            
    sleep_ms(1000) #wait a second after button press to stabilize

    # Throw away first 4 readings of filtered_xyz, since it is returned as a sum of last 4 calls
    # This ensures first reading is on the same basis as other readings
    for i in range(0,4):
        x,y,z = accel.filtered_xyz()
    
    #Get the average of a few readings, assumes the board is in a stable position
    #TODO could check that variance is not large, and repeat until stable...
    xs = []
    ys = []
    zs = []

    for i in range(0,100):

        #Read and scale the acceleration
        x, y, z = scale_accel(accel.filtered_xyz()) # filtered is sum of 4 readings

        xs.append(x)
        ys.append(y)
        zs.append(z)
        sleep_ms(10)

    x = sum(xs)/len(xs)
    y = sum(ys)/len(ys)
    z = sum(zs)/len(zs)

    #Calculate tilt
    #apply trigonometry to get the pitch and roll:http://physics.rutgers.edu/~aatish/teach/srr/workshop3.pdf
    #Unclear which is better pitch/roll formula, listing above is disputed..
    #pitch = rotation y, roll = rotation x
    #unknown z (because no gyroscope) requires consistent train/test of board in consistent orientation
    #orient with usb 'tail' trailing away from travel direction.
    try:
        #roll = atan2(y,z) 
        #pitch = atan2(x, sqrt(y*y + z*z + 0.00001))
        pitch = atan(x/sqrt(pow(y,2) + pow(z,2)))
        roll = atan(y/sqrt(pow(x,2) + pow(z,2)))

        pitch_d = pitch * (180.0/pi)
        roll_d = roll * (180.0/pi)

        print("Pitch: {}, roll: {}".format(pitch_d, roll_d))
    except ZeroDivisionError:
        print('divide by zero error: x {}, y {}, z {}'.format(x,y,z))
    

    #todo need to figure out multipliers....
    #mx = 1
    #my = y*cos(pitch) + z * sin(pitch)
    #mz = y * sin(pitch) + z * cos(pitch)

    return pitch_d,roll_d


def check_file_exists(filename):
    try:
        os.stat(filename)
        return True;
    except OSError:
        return False

def make_filename(base="/sd/log",ending=".csv"):

    file_exists = True #assume file already exists
    version = 0 #the first file name to try
    while file_exists == True:
        version += 1
        current_filename = base + str(version) + ending
        file_exists = check_file_exists(current_filename)

    return current_filename


if __name__ == '__main__':
    main()