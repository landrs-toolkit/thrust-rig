import csv
import random
import time
import RPi.GPIO as GPIO
import sys
import csv

EMULATE_HX711=False

#referenceUnit = 1
referenceUnit = 2253
GPIO.setwarnings(False)


if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
   # print("Another hx711")
else:
    from emulated_hx711 import HX711

def cleanAndExit():
   # print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
       # print("Just hx711")
    #print("Bye!")
    sys.exit()

hx = HX711(5, 6)

push_button = 18
LED_Light = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(push_button, GPIO.IN)
GPIO.setup(push_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_Light, GPIO.OUT)

def Turn_LED_ON():
    if GPIO.input(push_button):
        time.sleep(0.25)
        if GPIO.input(push_button):
            hx.tare()
            GPIO.output(LED_Light,GPIO.LOW)
    else:
        GPIO.output(LED_Light, GPIO.HIGH)
    pass

# I've found out that, for some reason, the order of the bytes is not always the $
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB u$
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long$
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't $
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and$
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers ne$
# and I got numbers around 184000 when I added 2kg. So, according to the rule of $
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

#print("Tare done! Add weight now...")
Tvals = []
buses = []
i=0
x_value = 0
# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the $
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and unco$

        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string

        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)
        #Turn_LED_ON()
        #val = round(val,2)
        val = round(val,0)
        Tvals.append(val)
        #print(val)
        buses.append(i)
        #hx.tare()
        if GPIO.input(push_button):
            time.sleep(0.25)
            if GPIO.input(push_button):
                GPIO.output(LED_Light, GPIO.HIGH)
               # hx.tare()
        else:
            GPIO.output(LED_Light, GPIO.LOW)
            hx.tare()
        #pass

        # To get weight from both channels (if you have load cells hooked up
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )
        i=i+1
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        #print(Tvals)
        #print("buses")
        #print(buses)
        fieldnames = ["x_value","thrust"]

        with open('data.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

        while True:
            with open('data.csv', 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                info = {
                        "x_value": x_value,
                        "thrust": val,
                        #"total_2": total_2
                        }

        csv_writer.writerow(info)
        print(val)

        x_value += 1
        time.sleep(1)    
        cleanAndExit()
