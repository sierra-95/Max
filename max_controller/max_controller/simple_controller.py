#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import JointState
import numpy as np
from rclpy.time import Time
from rclpy.constants import S_TO_NS


class SimpleController(Node):
    def __init__(self):
        super().__init__('simple_controller')
        
        self.declare_parameter("wheel_radius", 0.0425)
        self.declare_parameter("wheel_separation", 0.232)

        self.wheel_radius = self.get_parameter("wheel_radius").get_parameter_value().double_value
        self.wheel_separation = self.get_parameter("wheel_separation").get_parameter_value().double_value

        self.get_logger().info(f"Wheel Radius: {self.wheel_radius}, Wheel Separation: {self.wheel_separation}")

        self.left_wheel_prev_pos = 0.0
        self.right_wheel_prev_pos = 0.0
        self.prev_time = self.get_clock().now()
        
        self.wheel_cmd_pub_ = self.create_publisher(Float32MultiArray, 'simple_velocity_controller/commands', 10)
        self.vel_sub_ = self.create_subscription(TwistStamped, 'max_controller/cmd_vel', self.velCallback, 10)
        self.joint_sub_ = self.create_subscription(JointState, 'joint_states', self.jointCallback, 10)
        
        self.speed_conversion = np.array([[self.wheel_radius/2, self.wheel_radius/2],
                                          [self.wheel_radius/self.wheel_separation, -self.wheel_radius/self.wheel_separation]])
    
        self.get_logger().info(f"The conversion matrix is:\n{self.speed_conversion}")
    
    def velCallback(self, msg):
        robot_speed = np.array([[msg.twist.linear.x],
                                [msg.twist.angular.z]])
        
        wheel_speed = np.matmul(np.linalg.inv(self.speed_conversion), robot_speed)
        wheel_speed_msg = Float32MultiArray()
        wheel_speed_msg.data = [wheel_speed[0,0],  # FL  ## 0,0 Left wheel velocity, 0,1 Right wheel velocity
                                wheel_speed[1,0],  # FR
                                wheel_speed[0,0],  # RL
                                wheel_speed[1,0]]  # RR
        
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

    def jointCallback(self, msg):
        dp_left = msg.position[0] - self.left_wheel_prev_pos
        dp_right = msg.position[1] - self.right_wheel_prev_pos
        dt = Time.from_msg(msg.header.stamp) - self.prev_time

        self.left_wheel_prev_pos = msg.position[0]
        self.right_wheel_prev_pos = msg.position[1]
        self.prev_time = Time.from_msg(msg.header.stamp)

        fi_left = dp_left / (dt.nanoseconds / S_TO_NS)
        fi_right = dp_right / (dt.nanoseconds / S_TO_NS)

        linear = (self.wheel_radius * fi_left + self.wheel_radius * fi_right) / 2
        angular = (self.wheel_radius * fi_left - self.wheel_radius * fi_right) / self.wheel_separation
        self.get_logger().info(f"Linear Velocity: {linear:.3f} m/s, Angular Velocity: {angular:.3f} rad/s")

def main():
    rclpy.init()
    simple_controller = SimpleController()
    rclpy.spin(simple_controller)
    simple_controller.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()

