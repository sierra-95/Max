import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joystick',
        parameters=[os.path.join(get_package_share_directory('max_controller'), 'config', 'joy_config.yaml')]
    )

    joy_teleop = Node(
        package='joy_teleop',
        executable='joy_teleop',
        parameters=[os.path.join(get_package_share_directory('max_controller'), 'config', 'joy_teleop.yaml')]
    )

    teleop_twist_joy = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        parameters=[
            os.path.join(
                get_package_share_directory('max_controller'),
                'config',
                'teleop_twist_joy.yaml'
            )
        ],
        remappings=[('/cmd_vel', '/max_controller/cmd_vel')]
    )


    return LaunchDescription([
        joy_node,
        teleop_twist_joy,
    ])