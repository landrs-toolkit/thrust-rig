from time import sleep
import pigpio
#import datetime
import RPi.GPIO as GPIO
import sys
#import csv
import os    
import time   
os.system ("sudo pigpiod") 
time.sleep(1) 
import pigpio 


class pwm:

    def __init__ (self):
        self.pi = pigpio.pi()
        self.ESC = 4

        pi.set_servo_pulsewidth(self.ESC, 0)

        self.Max_Value = input("Enter the Max Throttle value\n")
        self.Min_Value = input("Enter the Min Throttle value\n")

        self.Max_Value = int(self.Max_Value)
        self.Min_Value = int(self.Min_Value)


    def calibrate(self):

    pi.set_servo_pulsewidth(self.ESC, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(self.ESC, self.Max_Value)

    print("Connect battery.. then press Enter")
    inp = input()
    if inp == '':

        pi.set_servo_pulsewidth(self.ESC, self.Min_Value)
        time.sleep(7)
        time.sleep (5)

        pi.set_servo_pulsewidth(self.ESC, 0)
        time.sleep(2)
        print ("Arming...")

        pi.set_servo_pulsewidth(self.ESC, self.Min_Value)
        time.sleep(1)
        control()


    def control():

    time.sleep(1)
    self.speed = self.Min_Value

    print ("a : decrease speed & d : increase speed | q : decrease A lot & e : increase A lot")
    while True:

        pi.set_servo_pulsewidth(self.ESC, self.speed)
        #inp = input()

        if self.get_inpt() == "q":
            speed -= 100
            print ("Throttle speed = %d" % self.speed)
            #weight()

        elif self.get_inp() == "e":
            speed += 100
            print ("Throtle speed = %d" % self.speed)
            #weight()
            

        elif self.get_inp() == "d":
            speed += 10
            print ("Throttle speed = %d" % speed)
            #weight()

        elif self.get_inp() == "a":
            speed -= 10
            print ("Throttle speed = %d" % speed)
            #weight()
        elif self.get_inp() == "stop":
            stop()
            break
        else:
            print ("Press a,q,d or e")

    def get_input(self):

        self.inp = input()
        return self.inp

    def start(self):
        if self.inp == "cal":
            calibrate()
        elif self.inp == "stop":
            stop()




