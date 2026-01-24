import RPi.GPIO as GPIO         # Import Raspberry Pi GPIO library
from time import sleep          # Import the sleep function 

pinLED = 4                      # LED GPIO Pin

GPIO.setmode(GPIO.BCM)          # Use GPIO pin number
GPIO.setwarnings(False)         # Ignore warnings in our case
GPIO.setup(pinLED, GPIO.OUT)    # GPIO pin as output pin

while True:                          # Endless Loop
    GPIO.output(pinLED, GPIO.HIGH)   # Turn on
    print("LED on")                    # Prints state to console
    sleep(1)                         # Pause 1 second
    GPIO.output(pinLED, GPIO.LOW)    # Turn off
    print("LED off")                   # Prints state to console
    sleep(1)                         # Pause 1 second