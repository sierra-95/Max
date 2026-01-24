import RPi.GPIO as GPIO
import time

# GPIO pins connected to the RGB LED
RED_PIN = 17
GREEN_PIN = 26
BLUE_PIN = 24

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Function to turn off all colors
def led_off():
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)

try:
    while True:
        # Red
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        print("Red ON")
        time.sleep(1)

        # Green
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        print("Green ON")
        time.sleep(1)

        # Blue
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        print("Blue ON")
        time.sleep(1)

        # Purple (Red + Blue)
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        print("Purple ON")
        time.sleep(1)

        # Yellow (Red + Green)
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        print("Yellow ON")
        time.sleep(1)

        # Cyan (Green + Blue)
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        print("Cyan ON")
        time.sleep(1)

        # White (Red + Green + Blue)
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        print("White ON")
        time.sleep(1)

        # Turn off
        led_off()
        time.sleep(0.5)

except KeyboardInterrupt:
    # Cleanup GPIO on Ctrl+C
    led_off()
    GPIO.cleanup()
    print("GPIO cleanup done, program exited")
