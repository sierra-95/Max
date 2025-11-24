import os
from launch import LaunchDescription
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    max_controller = get_package_share_directory('max_controller')

    robot_description = ParameterValue(
        Command([
            "xacro", 
            " ",
            LaunchConfiguration('model'),
            " ",
            "is_sim:=false",
        ]), 
        value_type=str
    )

    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {"robot_description": robot_description,
             "use_sim_time": False
            },
            os.path.join(
                max_controller,
                'config',
                'max_controller.yaml'
            )
        ],
        output='screen'
    )
    return LaunchDescription([
        controller_manager
    ])