import os
from launch import LaunchDescription
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    max_description = get_package_share_directory('max_description')

    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=os.path.join(
            max_description,
            'urdf',
            'max.urdf.xacro'
        ),
        description='Absolute path to robot urdf file'
    )

    is_sim_arg = DeclareLaunchArgument(
        'is_sim',
        default_value='False',
        description='Set to True when running in simulation'
    )


    robot_description = ParameterValue(
        Command([
            "xacro", 
            " ",
            LaunchConfiguration('model'),
            " ",
            "is_sim:=", LaunchConfiguration('is_sim')
        ]), 
        value_type=str
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{"robot_description": robot_description}],
        output='screen'
    )

    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {"robot_description": robot_description,
             "use_sim_time": False
            },
            os.path.join(
                get_package_share_directory('max_controller'),
                'config',
                'max_controller.yaml'
            )
        ],
        output='screen'
    )
    return LaunchDescription([
        model_arg,
        is_sim_arg,
        robot_state_publisher_node,
        controller_manager
    ])