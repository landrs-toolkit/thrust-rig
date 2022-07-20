
from time import sleep
import pigpio
import datetime
import RPi.GPIO as GPIO
import sys
import csv
import os    
import time 

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import hx711




pi = pigpio.pi()


EMULATE_HX711=False

#referenceUnit = 1
referenceUnit = 2253
GPIO.setwarnings(False)

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
    print("Another hx711")
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        print("Just hx711")
    print("Bye!")
    sys.exit()


hx = HX711(5, 6)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize communication with TMP102
#hx711.init()



# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    
    #global val
    #c=0

    #for j in range(10):

        #val = hx.get_weight(5)
        #val = round(val,0)
        #Tvals.append(val)
        #ys.append(val)
        #print (val)
        #return val
        #buses.append(c)
        #c=c+c
    
    val = hx.get_weight(5)
    val = round(val,0)

    hx.power_down()
    hx.power_up()
    sleep(0.1)

    #val = round(weight())
    for x in range(100):
        xs.append(x)
        ys.append(val)
        #return i
        
    #x_val = (for i in range(100):  )

    # Add x and y to lists
    #xs.append(i)
    #ys.append(val)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]
    print(ys)
    #print(xs)

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)
    plt.savefig('plotdata.png')

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Thrust values over Time')
    plt.ylabel('Thrust (g)')

#plt.savefig('plotdata.png')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)

# Save the image

plt.show()
