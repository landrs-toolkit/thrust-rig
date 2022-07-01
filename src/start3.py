#  ESC Calibration for Drones

from time import sleep
import pigpio
import datetime
import RPi.GPIO as GPIO
import sys
import csv
import os    
import time   
os.system ("sudo pigpiod") 
time.sleep(1) 
import pigpio 


pi = pigpio.pi();


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
ESC = 4 
LED_Light = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(push_button, GPIO.IN)
GPIO.setup(push_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_Light, GPIO.OUT)
#pi = pigpio.pi()
##

def Turn_LED_ON():
    if GPIO.input(push_button):
        sleep(0.25)
        if GPIO.input(push_button):
            hx.tare()
            GPIO.output(LED_Light,GPIO.LOW)
    else:
        GPIO.output(LED_Light, GPIO.HIGH)
        sleep(2)
    pass

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done! Add weight now...")
Tvals = []
buses = []
i=0

pi.set_servo_pulsewidth(ESC, 0) 

Max_Value = input("Enter the Max Throttle value\n")
Min_Value = input("Enter the Min Throttle value\n")

Max_Value = int(Max_Value)
Min_Value = int(Min_Value)


print("please disconnect battery.. then press cal")
                
def calibrate():   
     
    pi.set_servo_pulsewidth(ESC, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, Max_Value)

    print("Connect battery.. then press Enter")
    inp = input()
    if inp == '': 
        
        pi.set_servo_pulsewidth(ESC, Min_Value)   
        time.sleep(7)
        time.sleep (5)        
        
        pi.set_servo_pulsewidth(ESC, 0)           
        time.sleep(2) 
        print ("Arming...")
        
        pi.set_servo_pulsewidth(ESC, Min_Value)
        time.sleep(1)
        control()

def cleanAndExit():
    print("cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
        print("Just hx711")
    print("Bye!")
    sys.exit()

   
def weight():

    Tvals = []
    buses = []
    i=0

    for j in range(10):

        val = hx.get_weight(5)
        val = round(val,0)
        Tvals.append(val)
        print (val)
        buses.append(i)
        i=i+1

    hx.power_down()
    hx.power_up()
    sleep(0.1)



def control(): 



    time.sleep(1)
    speed = Min_Value
    print ("a : decrease speed & d : increase speed | q : decrease A lot & e : increase A lot")
    while True:
        if(GPIO.input(push_button)):
            sleep(0.25)
            if(GPIO.input(push_button)):
                GPIO.output(LED_Light,GPIO.HIGH)
        else:
            GPIO.output(LED_Light,GPIO.LOW)
            hx.tare()


        #for E in Count_ESC:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()
        
        if inp == "q":
            speed -= 100    
            print ("Throttle speed = %d" % speed)
            weight()

        elif inp == "e":    
            speed += 100    
            print ("Throtle speed = %d" % speed)
            weight()

        elif inp == "d":
            speed += 10     
            print ("Throttle speed = %d" % speed)
            weight()

        elif inp == "a":
            speed -= 10     
            print ("Throttle speed = %d" % speed)
            weight()
        elif inp == "stop":
            stop()          
            break
        else:
            print ("Press a,q,d or e")
      
def stop(): 
    #for E in Count_ESC:
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()
    print("drone propeller motor has stopped\n")
    print("Done Completely")

    file = open("Thrust_Values.csv", "a", encoding='UTF8', newline='')
    writer = csv.writer(file)
    writer.writerow(now.strftime("%Y-%m-%d %H:%M:%S"))
    for w in range(len(buses)):
        writer.writerow([buses[w], Tvals[w]])
    file.close()
    cleanAndExit()

  
inp = input()

if inp == "cal":
    calibrate()

elif inp == "stop":
    stop()

