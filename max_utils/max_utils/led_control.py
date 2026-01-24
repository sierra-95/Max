import RPi.GPIO as GPIO
import time

RED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(RED_PIN, GPIO.HIGH)
        print("RED ON")
        time.sleep(1)
        GPIO.output(RED_PIN, GPIO.LOW)
        print("RED OFF")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
