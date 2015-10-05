#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import pygame
import time
import socket
from pygame import locals

host = '192.168.2.157'
port = 50013

x1 = 0			#X-Achse des linken Analogsticks
y1 = 0			#Y-Achse des linken Analogsticks
x2 = 0			#X-Achse des rechten Analogsticks
y2 = 0			#Y-Achse des rechten Analogsticks
psspeed = 0		#Joystick Geschwindigkeit in einem Bereich von 0 bis 100%
psangle = 0		#gibt den Joystick Lenkeinschlag an
rStick = True		#setzt Lenken auf rechten oder linken Analogstick

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Racer')
pygame.mouse.set_visible(0)
pygame.key.set_repeat(True)
finished = False

deadZone = 0.001 # make a wide deadzone

try:
   j = pygame.joystick.Joystick(0) # create a joystick instance
   j.init() # init instance
   print 'Enabled joystick: ' + j.get_name()
except pygame.error:
   print 'no joystick found.'

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
	command = str(speed) + "," + str(angle)
#	print command
	s.sendto(command,(host,port))
 	time.sleep(0.1)

#----------------------------------------------------------------------------------------------------
#Funktion		:	setSpeed()
#Beschreibung		:	Die Funktion ermittelt anhand, der ihr als Parameter übergebenen Zeit,
#				die Geschwindigkeit des Autos. Diese wird anschließend zurückgegeben.
#Parameter		:	Zeit für die Pfeiltaste oben bzw. unten gedrückt wurde
#Rückgabewert		:	dutycycle für den Motor des Autos
#-----------------------------------------------------------------------------------------------------
def setSpeed(speed):  

	if speed < 0 and speed > -0.2:
        	return -1;	#10% Geschwindigkeit
        elif speed <= -0.2 and speed > -0.3:
                return -2;	#20% Geschwindigkeit
        elif speed <= -0.3 and speed > -0.4:
                return -3;
        elif speed <= -0.4 and speed > -0.5:
                return -4;
        elif speed <= -0.5 and speed > -0.6:
                return -5;
        elif speed <= -0.6 and speed > -0.7:
               return -6;
        elif speed <= -0.7 and speed > -0.8:
               return -7;
        elif speed <= -0.8 and speed > -0.9:
                return -8
        elif speed <= -0.9 and speed > -1:
               	return -9;
        elif speed <= -1:
                return -10;

	if speed < 0.01 and speed > -0.01:
		return 0;       

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
	if angle < -0.01 and angle > -0.33:
		return -1;
	elif angle <= -0.33 and angle > -0.66:
		return -2;
	elif angle <= -0.66:
		return -3;

	if angle < 0.01 and angle > -0.01:
		return 0;

	if angle > 0.01 and angle < 0.33:
		return 1;
	elif angle >=0.33 and angle < 0.66:
		return 2;
	elif angle >= 0.66:
		return 3;

while not finished:
#	if j.get_button(1):
#		if rStick:
#			y1 = j.get_axis(1)*0 # Linker Analogstick
#			x2 = j.get_axis(3) # Rechter Analogstick
#		else:
#			y1 = j.get_axis(1)*0 # Linker Analogstick
#			x2 = j.get_axis(0) # Rechter Analogstick
#	elif j.get_button(2):
#		if rStick:
#			y1 = j.get_axis(1) # Linker Analogstick
#			x2 = j.get_axis(3) # Rechter Analogstick
#		else:
#			y1 = j.get_axis(1) # Linker Analogstick
#			x2 = j.get_axis(0) # Rechter Analogstick
#	else:
#		if rStick:
#			y1 = j.get_axis(1)*0.5 	# Linker Analogstick
#			x2 = j.get_axis(3) 	# Rechter Analogstick
#		else:
#			y1 = j.get_axis(1)*0.5 	# Linker Analogstick
#			x2 = j.get_axis(0) 	# Rechter Analogstick
	if j.get_button(1):
		y1 = j.get_axis(1)*0 # Linker Analogstick
	elif j.get_button(2):
		y1 = j.get_axis(1) # Linker Analogstick
	else:
		y1 = j.get_axis(1)*0.5 	# Linker Analogstick
	if rStick:
		x2 = j.get_axis(3) # Rechter Analogstick
	else:
		x2 = j.get_axis(0) # Rechter Analogstick	
		
	sendCommand(setSpeed(y1*-1),setAngle(x2)) #sollte nicht in if-Abfragen gebettet werden
	
	pygame.event.pump()
			
	
	if j.get_button(10):
		rStick = False
	if j.get_button(11):
		rStick = True
	if j.get_button(0):
		print 'Programm wird beendet'
		j.quit()
		finished = True