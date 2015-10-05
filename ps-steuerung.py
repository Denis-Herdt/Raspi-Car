#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import pygame
import time
import socket
from pygame import locals
import webbrowser

#host = '192.168.2.157'
host = '10.42.0.64'
port = 50013

# ----- Keys ------- #
forwardTime = 0		#Variable zum stoppen wie lange Pfeiltaste nach oben gedrückt wurde	
backwardTime = 0	#Variable zum stoppen wie lange Pfeiltaste nach unten gedrückt wurde
rightTime = 0		#Variable wie lange rechte Pfeiltaste gedrückt wurde
leftTime = 0		#Variable wie lange linke Pfeiltaste gedrückt wurde
forward = False		#Verhindert gleichzeitiges Drücken von Pfeiltaste nach oben und nach unten
backward = False	#Verhindert gleichzeitiges Drücken von Pfeiltaste nach oben und nach unten
right = False		#Verhindert gleichzeitiges Drücken von Pfeil rechts und links
left = False		#Verhindert gleichzeitiges Drücken von Pfeil rechts und links
speed = 0		#Geschwindigkeit in einem Bereich von 0 bis 100%
angle = 0		#gibt den Lenkeinschlag an
timeSent = 0		#Zeitsetempel bei versendeten Nachrichten
# ----- Keys ------- #

# ----- Joystick ------- #
x1 = 0			#X-Achse des linken Analogsticks
y1 = 0			#Y-Achse des linken Analogsticks
x2 = 0			#X-Achse des rechten Analogsticks
y2 = 0			#Y-Achse des rechten Analogsticks
psspeed = 0		#Joystick Geschwindigkeit in einem Bereich von 0 bis 100%
psangle = 0		#gibt den Joystick Lenkeinschlag an
rStick = True		#setzt Lenken auf rechten oder linken Analogstick
ultrasonic = 0
ki = 0
lights = 0
ulights = 0
# ----- Joystick ------- #

f = False
b = False

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('RaspiCar')
pygame.mouse.set_visible(0)
pygame.key.set_repeat(True)
finished = False
webbrowser.open_new('http://' + host + ':8080/stream_simple.html')

try:
   j = pygame.joystick.Joystick(0) # create a joystick instance
   j.init() # init instance
   print 'Enabled joystick: ' + j.get_name()
   js = True
except pygame.error:
   print 'no joystick found.'
   js = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#IPv4 TCP socket erstellen

#----------------------------------------------------------------------------------------------------
#Funktion		:	sendCommand()
#Beschreibung		:	Die Funktion versendet die aktuellen Bewegungsparameter des Autos an
#				den RaspberryPi. Dieser setzt diese anschließend in Steuerbefehle um.
#Parameter		:	Richtung, Geschwindigkeit, Lenkrichtung sowie Lenkeinschlag des Autos.
#Rückgabewert		:	keiner
#----------------------------------------------------------------------------------------------------
def sendCommand(speed, angle):
	global timeSent
	global f
	global b
	command = str(speed) + "," + str(angle) + "," + str(ultrasonic) + "," + str(ki) + "," + str(lights) + "," + str(ulights)
	if speed > 0:
		f= True
		b= False
	elif speed < 0:
		b= True
		f= False
	else:
		f= False
		b= False
	print command
	s.sendto(command,(host,port))
 	time.sleep(0.1)

#----------------------------------------------------------------------------------------------------
#Funktion		:	setSpeed()
#Beschreibung		:	Die Funktion ermittelt anhand, der ihr als Parameter übergebenen Zeit,
#				die Geschwindigkeit des Autos. Diese wird anschließend zurückgegeben.
#Parameter		:	Zeit für die Pfeiltaste oben bzw. unten gedrückt wurde
#Rückgabewert		:	dutycycle für den Motor des Autos
#-----------------------------------------------------------------------------------------------------
def breaks(angle):
	
	if f:
		sendCommand(-10, angle)
		time.sleep(0.3)
	elif b:
		sendCommand(10, angle)
		time.sleep(0.3)
	
def setSpeed(speed):  

	#if speed < 0 and speed > -0.2:
        	#return -1;	#10% Geschwindigkeit
        #elif speed <= -0.2 and speed > -0.3:
                #return -2;	#20% Geschwindigkeit
        #elif speed <= -0.3 and speed > -0.4:
                #return -3;
        #elif speed <= -0.4 and speed > -0.5:
                #return -4;
        #elif speed <= -0.5 and speed > -0.6:
                #return -5;
        #elif speed <= -0.6 and speed > -0.7:
               #return -6;
        #elif speed <= -0.7 and speed > -0.8:
               #return -7;
        #elif speed <= -0.8 and speed > -0.9:
                #return -8
        #elif speed <= -0.9 and speed > -1:
               	#return -9;
        #elif speed <= -1:
                #return -10;

	#if speed < 0.01 and speed > -0.01:
		#return 0;       

        if speed > 0 and speed < 0.2:
        	return 1;	#10% Geschwindigkeit
        elif speed >= 0.2 and speed < 0.3:
                return 2;	#20% Geschwindigkeit
        elif speed >=0.3 and speed < 0.4:
                return 3;
        elif speed >= 0.4 and speed < 0.5:
                return 4;
        elif speed >= 0.5 and speed < 0.6:
                return 5;
        elif speed >= 0.6 and speed < 0.7:
               return 6;
        elif speed >= 0.7 and speed < 0.8:
               return 7;
        elif speed >= 0.8 and speed < 0.9:
                return 8
        elif speed >= 0.9 and speed < 1:
               	return 9;
        elif speed >= 1:
                return 10;

#-----------------------------------------------------------------------------------------------
#Funktion	:	setAngle()
#Beschreibung	:	Die Funktion ermittelt, anhand der ihr als Parameter übergebenen Zeit,
#			den Lenkeinschlag des Autos. Dieser wird anschließend zurückgegeben.
#Parameter	:	Zeit für die Pfeiltaste rechts bzw. links gedrückt wurde#Rückgabewert	:	dutycycle für den Servo der Lenkung 
#-----------------------------------------------------------------------------------------------
def setAngle(angle):
	#if angle < -0.01 and angle > -0.33:
		#return -1;
	#elif angle <= -0.33 and angle > -0.66:
		#return -2;
	#elif angle <= -0.66:
		#return -3;

	#if angle < 0.01 and angle > -0.01:
		#return 0;

	if angle > 0.01 and angle < 0.33:
		return 1;
	elif angle >=0.33 and angle < 0.66:
		return 2;
	elif angle >= 0.66:
		return 3;

# ----- Joystick ------- #
while not finished:
  
	while js:
		if j.get_button(1):
			breaks(x2)
			y1 = j.get_axis(1)*0 # y-Achse
		elif j.get_button(2):
			y1 = j.get_axis(1) # y-Achse
		else:
			y1 = j.get_axis(1)*0.5 	# y-Achse
		if rStick:
			x2 = j.get_axis(3) # x-Achse
		else:
			x2 = j.get_axis(0) # x-Achse	
		
		sendCommand(round((y1*-10),2),round((x2*10/3),2))
		pygame.event.pump()
		if j.get_button(10):
			rStick = False
		if j.get_button(11):
			rStick = True
		if j.get_button(0):
			print 'change to keys'
			js = False
		if j.get_button(4):
			if ki == 0:
				ki = 1
				time.sleep(0.1)
			else:
				ki = 0
				time.sleep(0.1)
		if j.get_button(5):
			if ultrasonic == 0:
				ultrasonic = 1
				time.sleep(0.1)
			else:
				ultrasonic = 0
				time.sleep(0.1)
		if j.get_button(6):
			if lights == 0:
				lights = 1
				time.sleep(0.1)
			else:
				lights = 0
				time.sleep(0.1)
		if j.get_button(7):
			if ulights == 0:
				ulights = 1
				time.sleep(0.1)
			else:
				ulights = 0
				time.sleep(0.1)

	# ----- Keys ------- #

	while not js:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					print 'change to joystick'
					js=True
				if event.key == pygame.K_UP and not backward:
					forward = True 
					if forwardTime == 0:
						forwardTime = time.time()	#aktuelle Zeit ermitteln			#Flag für vorwärts Bewegung setzen
				if event.key == pygame.K_DOWN and not forward:
					backward = True
					if backwardTime == 0:
						backwardTime = time.time()
				if event.key == pygame.K_LEFT and not right:
					left = True
					if leftTime == 0:
						leftTime = time.time()
				if event.key == pygame.K_RIGHT and not left:
					right = True
					if rightTime == 0:
						rightTime = time.time()

		if not forward and not backward and time.time() - timeSent >= 0.1 or not left and not right and time.time() - timeSent >= 0.1:
			if not forward and not backward:
				speed = 0
				forwardTime = 0
				backwardTime = 0
		  
			if not left and not right:
				angle = 0
				timeLeft = 0
				timeRight = 0
			sendCommand(speed,angle)
		else:
			if  pygame.key.get_pressed()[pygame.K_UP] == 1 and forward:	#vorwärts noch immer gedrückt?
				speed = setSpeed(time.time()-forwardTime)		#anhand der Zeit für die vörwärts gedrückt wurde Geschwindigkeit ermitteln
				backwardTime = 0
				if time.time() - timeSent >= 0.1:
					sendCommand(speed,angle)

			elif pygame.key.get_pressed()[pygame.K_UP] == 0 and forward:
				forward = False
				if time.time() - timeSent >= 0.1:
					sendCommand(speed,angle)

			if pygame.key.get_pressed()[pygame.K_DOWN] == 1 and backward:
				speed = setSpeed(time.time()-backwardTime)*-1
				forwardTime = 0
				if time.time() - timeSent >= 0.1:
					sendCommand(speed,angle)

			elif pygame.key.get_pressed()[pygame.K_DOWN] == 0 and backward:
				backward = False
				if time.time() - timeSent >= 0.1:
					sendCommand(speed,angle)

			if pygame.key.get_pressed()[pygame.K_LEFT] == 1 and left:
				angle = setAngle(time.time() - leftTime) * -1
				rightTime = 0
				if time.time() - timeSent >= 0.1:
					sendCommand(speed,angle)
	
			elif pygame.key.get_pressed()[pygame.K_LEFT] == 0 and left:
				left = False
				if time.time() - timeSent >= 0.1:
					sendCommand(speed,angle)

			if pygame.key.get_pressed()[pygame.K_RIGHT] == 1 and right:
				angle = setAngle(time.time() - rightTime)
				leftTime = 0
				if time.time() - timeSent >= 0.1:
					sendCommand(speed,angle)

			elif pygame.key.get_pressed()[pygame.K_RIGHT] == 0 and right:
				right = False
				if time.time() - timeSent >= 0.1:
					sendCommand(speed,angle)
