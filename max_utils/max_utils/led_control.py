import RPi.GPIO as GPIO
import time

TEST_PIN = 19  # The pin you want to toggle

GPIO.setmode(GPIO.BCM)
GPIO.setup(TEST_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(TEST_PIN, GPIO.HIGH)
        print("Pin 19 HIGH")
        time.sleep(1)
        GPIO.output(TEST_PIN, GPIO.LOW)
        print("Pin 19 LOW")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO cleaned up")
