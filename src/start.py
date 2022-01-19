#! /usr/bin/python2

from time import sleep
import pigpio
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
push_button = 18
LED_Light = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(push_button, GPIO.IN)
GPIO.setup(push_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_Light, GPIO.OUT)
pi = pigpio.pi()


def Turn_LED_ON():
    if GPIO.input(push_button):
        sleep(0.25)
        if GPIO.input(push_button):
            hx.tare()
            GPIO.output(LED_Light,GPIO.LOW)
    else:
        GPIO.output(LED_Light, GPIO.HIGH)
    pass

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done! Add weight now...")
Tvals = []
buses = []
i=0
print("Calibrating the ESC\n")
Max_Value = input("Enter the Max Throttle value\n")
Min_Value = input("Enter the Min Throttle value\n")

Max_Value = int(Max_Value)
Min_Value = int(Min_Value)

ESC_GPIO = 4
#pi.set_servo_pulsewidth(ESC_GPIO,Max_Value) #Max Throttle
pi.set_servo_pulsewidth(ESC_GPIO,Max_Value)
sleep(5)
#pi.set_servo_pulsewidth(ESC_GPIO,Min_Value) #Min Throttle
pi.set_servo_pulsewidth(ESC_GPIO,Min_Value)
sleep(5)
speed = Min_Value
print("Speed of motor will now increase from Min to Max Throttle")
sleep(1)


#pi.set_servo_pulsewidth(ESC_GPIO,speed)

while True:
    try:
        if(GPIO.input(push_button)):
            sleep(0.25)
            if(GPIO.input(push_button)):
                GPIO.output(LED_Light,GPIO.HIGH)
        else:
            GPIO.output(LED_Light,GPIO.LOW)
            hx.tare()
        while(speed<1900):
            pi.set_servo_pulsewidth(ESC_GPIO,speed)
            #speed+=100
            sleep(5)
            print(speed)
            for j in range(10):
                val = hx.get_weight(5)
                val = round(val,0)
                Tvals.append(val)
                print(val)
                buses.append(i)
                i=i+1
            speed+=100
        val = hx.get_weight(5)
        val = round(val,0)
        Tvals.append(val)
        print(val)
        buses.append(i)
        i=i+1
        hx.power_down()
        hx.power_up()
        sleep(0.1)
    except(KeyboardInterrupt, SystemExit):
        speed = 0
        now = datetime.datetime.now()
        pi.set_servo_pulsewidth(ESC_GPIO,0)
        pi.stop()
        print("Motor has stopped\n")
        print("Done_Completely")
        file = open("Thrust_Values.csv", "a", encoding='UTF8', newline='')
        writer = csv.writer(file)
        writer.writerow(now.strftime("%Y-%m-%d %H:%M:%S"))
        for w in range(len(buses)):
            writer.writerow([buses[w], Tvals[w]])
        file.close()
        cleanAndExit()

