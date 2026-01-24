import RPi.GPIO as GPIO
import time

# Assign GPIO numbers (BCM mode) to RGB pins
RED_PIN = 4    # Physical pin 7
GREEN_PIN = 17 # Physical pin 11
BLUE_PIN = 27  # Physical pin 13

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Function to turn off all LEDs
def led_off():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

try:
    while True:
        # Red
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        print("RED ON")
        time.sleep(1)

        # Green
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        print("GREEN ON")
        time.sleep(1)

        # Yellow (Red + Green)
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        print("YELLOW ON")
        time.sleep(1)

        # Turn off
        led_off()
        print("ALL OFF")
        time.sleep(0.5)

except KeyboardInterrupt:
    led_off()
    GPIO.cleanup()
    print("Cleanup done, program stopped")
