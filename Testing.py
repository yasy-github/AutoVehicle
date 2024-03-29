from auto_drive_functions import retrieve_angle
from ImageFrame import Frame
from debug_mode import debugging
from gpiozero import Servo, Motor
from time import sleep
import cv2
import numpy as np
import math
import timeit

frame1 = Frame(640,480,10)
cam = cv2.VideoCapture(0)

#init servo
gpioPin = 4
correction = 0.45
maxPW = (2.0 + correction) / 1000
minPW = (1.0 - correction) / 1000
myServo = Servo(gpioPin, min_pulse_width=minPW, max_pulse_width=maxPW)

#init motor
print('init motor')
motor = Motor(forward = 23, backward = 24, enable = 25, pwm=True)

def servo_begin(servo, angle):
	try:
		print("Angle: ", angle)
		angleValue = (2/180 * angle - 1)
		servo.value = angleValue
		#sleep(1)
	except KeyboardInterrupt:
		print("Program stopped")


def main():
	#print('move forward')
	#motor.forward(1)
	x = 1
	while True:
		start = timeit.default_timer()
		img = cam.read()[1]
		
		#cv2.imwrite('~/Desktop/testimage/img'+str(x)+'.jpg', img)
		x=x+1
		
		points, mid_points, myAngle = retrieve_angle(s1=60, hd=5, img_path=img, frame=frame1)
        debugging(img, myAngle, points, mid_points)
		
		if myAngle.shape > (1,):
			if math.isnan(myAngle[1]) : continue
			myAngle = myAngle[1]
		else:
			myAngle = 90
		
		if myAngle <= 80 or myAngle >= 100 :
			print('slow')
			motor.forward(0.25)
		else:
			print('fast')
			motor.forward(0.25)
		
		servo_begin(servo=myServo, angle=myAngle)
# 		print('runtime : '+str(timeit.default_timer() - start))

# def debug():
#     while True:
#         start = timeit.default_timer()
#         img = cam.read()[1]
#         #cv2.imwrite('~/Desktop/testimage/img'+str(x)+'.jpg', img)
#         #print(img.shape)
#         myAngle = retrieve_angle(s1=60, hd=5, img_path=img, frame=frame1)
#         print('runtime : '+str(timeit.default_timer() - start))
# debug()
