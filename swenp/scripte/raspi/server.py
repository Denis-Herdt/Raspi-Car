#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import socket
import RPi.GPIO as GPIO
import os

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("",50013))

#motorForward = 20		#Pin vor enabled
#motorBackward = 21		#pin zurück enabled
pwmForward = 18			#pwm für Motor vorwärts
pwmBackward = 17		#pwm Leitung für rückwärts
pwmServo = 4			#pwm Signal für den Servo
     
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(motorForward,GPIO.OUT)
#GPIO.setup(motorBackward,GPIO.OUT)
GPIO.setup(pwmForward,GPIO.OUT)
GPIO.setup(pwmBackward,GPIO.OUT)
GPIO.setup(pwmServo,GPIO.OUT)

f = GPIO.PWM(pwmForward,100)
f.start(0)
b = GPIO.PWM(pwmBackward,100)
b.start(0)
#s = GPIO.PWM(pwmServo,50)
#s.start(7.5)

#while True:
#	pwmServo = 4

while True:
	frame = sock.recvfrom(1024)
	data = str(frame[0]).split(",")
	speed = int(data[0])
	steering = int(data[1])
#	print "Speed: " + str(speed)
#	print "Angle: " +str(steering)
	if speed == 0:
		#print "Stehen"
		f.ChangeDutyCycle(0)
		b.ChangeDutyCycle(0)
	elif speed > 0:
		#GPIO.output(motorForward,GPIO.HIGH)
		f.ChangeDutyCycle(speed*10)
		#print "vor"
	else:
		#GPIO.output(motorBackward,GPIO.HIGH)
		b.ChangeDutyCycle((speed * -1)*10)
		#print "hinten"
	if steering < 0:#links
		if steering == -1:
                        os.system('echo "4=0.17" > /dev/pi-blaster')
                elif steering == -2:
                        os.system('echo "4=0.18" > /dev/pi-blaster')
                else:
                        os.system('echo "4=0.19" > /dev/pi-blaster')
		#os.system('echo "4=0.20" > /dev/pi-blaster')
		#s.ChangeDutyCycle(9.5)
	elif steering > 0:#rechts
		if steering == 1:
                        os.system('echo "4=0.13" > /dev/pi-blaster')
                elif steering == 2:
                        os.system('echo "4=0.12" > /dev/pi-blaster')
                else:
                        os.system('echo "4=0.11" > /dev/pi-blaster')
		#os.system('echo "4=0.10" > /dev/pi-blaster')
		#s.ChangeDutyCycle(4.5)
	else:#gerade
		os.system('echo "4=0.146" > /dev/pi-blaster')
		#os.system('echo "4=0." > /dev/pi-blaster')
		#s.ChangeDutyCycle(7)	
s.close()
