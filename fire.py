import RPi.GPIO as GPIO
import time

fire_pin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(fire_pin, GPIO.IN)
# 불 인식하면 0, 없으면 1
while 1:
	fire = GPIO.input(fire_pin)
	print(fire)
	time.sleep(1)
