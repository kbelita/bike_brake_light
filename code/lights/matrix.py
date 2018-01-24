import lights.ht16k33_matrix_framebuffer as ht

from machine import I2C 	#necessary to use the machine version of I2C instead of pyb, as this is what the matrix class expects
from pyb import Pin
from time import sleep_ms

############################################
# Wiring
#
# This code uses I2C. Refer to the feather_schem image for full specs
# on the pinout of the matrix backpack. With the shorter line of pins
# on the left and full line of pins on the right, the four pins needed are:
# - SDA pin is top left
# - SCL is second from top left
# - 3V pin is second from bottom right
# - GND pin is 4th from bottom right

# On the Pyboard, when using bus 2 (as below) 
# - connect SCL to 'Y9'
# - connect SDA to 'Y10'

class MainGrid:
	def __init__(self):
		self.iic = I2C(2)  #SCL on bus 2, SDA on bus 2
		self.matrix = ht.Matrix16x8(self.iic, address=0x70)

		#edit individual pixels
		#matrix.pixel(row,column,0) #off
		#matrix.pixel(row,column,1) #on
		#matrix.show()

	def on(self):
		self.matrix.fill(1)
		self.matrix.show()

		
	def off(self):
		self.matrix.fill(0)
		self.matrix.show()
