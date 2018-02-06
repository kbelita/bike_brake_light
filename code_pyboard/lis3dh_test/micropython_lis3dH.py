
Pinouts:
#purple =  X9 (scl)
#gray  = X10 (SDA)
#black = 3x3 (tied high)

from LIS3DH import LIS3DH

sensor = LIS3DH(debug=True)

while True:

    x = sensor.getX()
    y = sensor.getY()
    z = sensor.getZ()

    print("Values: {}, {}, {}".format(x,y,z))
    sleep(1)
    