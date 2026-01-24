#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import RPi.GPIO as GPIO

# GPIO setup
RED_PIN = 7
GREEN_PIN = 8
BLUE_PIN = 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def led_off():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

class ProximityLED(Node):
    def __init__(self):
        super().__init__('proximity_led_node')
        # Subscribe to lidar scan topic
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',  # change to your LiDAR topic if different
            self.scan_callback,
            10
        )
        self.scan_offset = 0.0  # any offset you want in meters

    def scan_callback(self, msg: LaserScan):
        # Get the closest distance in the scan
        distances = [d for d in msg.ranges if d > 0.0]  # ignore 0 readings
        if not distances:
            return  # no valid readings
        closest = min(distances) - self.scan_offset

        led_off()  # reset LEDs before setting new color

        if closest < 0.2:
            # RED
            GPIO.output(RED_PIN, GPIO.HIGH)
            GPIO.output(GREEN_PIN, GPIO.LOW)
            GPIO.output(BLUE_PIN, GPIO.LOW)
            #print(f"Obstacle very close: {closest:.2f}m - RED ON")
        elif closest < 0.4:
            # YELLOW
            GPIO.output(RED_PIN, GPIO.HIGH)
            GPIO.output(GREEN_PIN, GPIO.HIGH)
            GPIO.output(BLUE_PIN, GPIO.LOW)
            #print(f"Obstacle nearby: {closest:.2f}m - YELLOW ON")
        else:
            # GREEN
            GPIO.output(GREEN_PIN, GPIO.HIGH)
            GPIO.output(RED_PIN, GPIO.LOW)
            GPIO.output(BLUE_PIN, GPIO.LOW)
            #print(f"No obstacle nearby: {closest:.2f}m - GREEN ON")

def main(args=None):
    rclpy.init(args=args)
    node = ProximityLED()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        led_off()
        GPIO.cleanup()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
