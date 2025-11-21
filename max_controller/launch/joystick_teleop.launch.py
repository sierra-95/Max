import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription

def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")
    max_controller = get_package_share_directory('max_controller')

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joystick',
        parameters=[
            os.path.join(max_controller, 'config', 'joy_config.yaml')
        ]
    )

    joy_teleop = Node(
        package='joy_teleop',
        executable='joy_teleop',
        parameters=[
            os.path.join(max_controller, 'config', 'joy_teleop.yaml'),
            {'use_sim_time': use_sim_time}
        ]
    )

    teleop_twist_joy = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        parameters=[
            os.path.join(max_controller,'config','teleop_twist_joy.yaml'),
            {'use_sim_time': use_sim_time}
        ],
        remappings=[('/cmd_vel', '/input_joy/cmd_vel')]
    )

    twist_mux_launch = IncludeLaunchDescription(
        os.path.join(get_package_share_directory("twist_mux"), "launch", "twist_mux_launch.py"),
        launch_arguments={
            "cmd_vel_out": "max_controller/cmd_vel_unstamped",
            "config_locks": os.path.join(max_controller, "config", "twist_mux_locks.yaml"),
            "config_topics": os.path.join(max_controller, "config", "twist_mux_topics.yaml"),
            "config_joy": os.path.join(max_controller, "config", "twist_mux_joy.yaml"),
            "use_sim_time": use_sim_time,
        }.items(),
    )

    return LaunchDescription([
        joy_node,
        teleop_twist_joy,
        twist_mux_launch
    ])