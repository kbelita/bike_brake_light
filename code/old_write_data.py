import machine
from pyb import Accel, ADC, Pin
from time import sleep_ms
import urandom

from math import atan, atan2, sin, cos, radians, degrees, sqrt, pow, pi

# Set up the switch to read 0 when not triggered, 1 when triggered
# Wiring: 
# - Connect one side of switch to the 'X1' pin
# - Connect the other side of the switch to ground
switch = machine.Pin('X1', machine.Pin.IN, machine.Pin.PULL_UP)
accel = Accel()

print("Setup accel and switch objects")
print(accel)
print(switch)


sleeptime = 50 #milliseconds, i.e. 20 times/second
savetime = 5000 #milliseconds, how often to close and reopen the file in case of sudden shutdown

g_scaling = 22.42 #based on calibration readings, estimated reading in the z axis of 1g
yaw = 0			#assume consistent orientation towards front

def random_filename(N=6):
	#TODO this isn't returning a random name....
	filename = ''.join(urandom.choice('ABCDEFG1234567890') for _ in range(N))
	return filename + '.data'


def calc_tilt_adjustments():
			
	sleep_ms(1000) #wait a second after button press to stabilize

	#Get the average of a few readings, assumes the board is in a stable position
	#TODO could check that variance is not large, and repeat until stable...
	xs = []
	ys = []
	zs = []

	for i in range(0,10):

		#Read the acceleration
		x = accel.x()
		y = accel.y()
		z = accel.z()

		#Scale it to between 1 and -1
		x,y,z = x/g_scaling, y/g_scaling, z/g_scaling

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
		roll = atan2(y,z) 
		pitch = atan2(x, sqrt(y*y + z*z + 0.00001))
		#pitch = atan(x/sqrt(pow(y,2) + pow(z,2) + 0.01));
		#roll = atan(y/sqrt(pow(x,2) + pow(z,2) + 0.01))
	except ZeroDivisionError:
		print('divide by zero error: x {}, y {}, z {}'.format(x,y,z))
	
	#for debugging
	#convert radians into degrees
	#pitch = pitch * (180.0/pi);
	#roll = roll * (180.0/pi) ;
	#print("Pitch: {}, roll: {}".format(pitch, roll))

	#todo need to figure out multipliers....
	mx = 1
	my = y*cos(pitch) + z * sin(pitch)
	mz = y * sin(pitch) + z * cos(pitch)

	return mx, my, mz

def log_data():
	#get the scaling factor. 
	mx,my,mz = calc_tilt_adjustments()

	current_filename = "/sd/data/angles1.data" #random_filename()
	print("Saving data to:",current_filename)

	#start a new file
	#TODO refactor to create a new file every X minutes if needed (currently 1 per session)
	with open(current_filename, 'w') as f:
		f.write("braking,x,y,z,adjX,adjY,adjZ\n")

	#Log the data. While loop logs continuously
	#while True:

	#For loop used to close/open the file every 'savetime' (in ms) to make sure file is saved before shutdown
	for j in range(0,2):
		with open(current_filename,'a') as f:
			for i in range(0,savetime / sleeptime):
				
				#Read the acceleration
				x = accel.x()
				y = accel.y()
				z = accel.z()

				roll = atan2(y,z) 
				pitch = atan2(x, sqrt(y*y + z*z + 0.00001))

				#for debugging
				#convert radians into degrees
				pitch = pitch * (180.0/pi);
				roll = roll * (180.0/pi) ;

				#Read the switch status
				braking = switch.value()
				

				#Save the data
				#f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(braking,x,y,z,adjX,adjY,adjZ,mx,my,mz))
				
				f.write('{},{},{}\n'.format(braking, pitch, roll))
				sleep_ms(sleeptime)

		f.close()
	print("Saving file. Current values:",braking,pitch,roll)
