from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from os import pathsep


def generate_launch_description():
    
    max_description = get_package_share_directory('max_description')
    max_description_prefix = get_package_prefix('max_description')

    model_path = os.path.join(
        max_description,
        "models",
    )
    model_path += pathsep + os.path.join(
        max_description_prefix,
        "share",
    )
    env_variable = SetEnvironmentVariable("GAZEBO_MODEL_PATH", model_path)
    
    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=os.path.join(
            max_description,
            'urdf',
            'max.urdf.xacro'
        ),
        description='Absolute path to robot urdf file'
    )

    robot_description = ParameterValue(Command(["xacro ", LaunchConfiguration('model')]), value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{"robot_description": robot_description}],
        output='screen'
    )

    start_gazebo_server = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('gazebo_ros'),
            'launch',
            'gzserver.launch.py',
        )
    ))
    start_gazebo_client = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('gazebo_ros'),
            'launch',
            'gzclient.launch.py',
        )
    ))

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=["-entity", "max", "-topic", "robot_description"],
        output='screen'
    )
    return LaunchDescription([
        spawn_robot,
        model_arg,
        robot_state_publisher_node,
        env_variable,
        start_gazebo_server,
        start_gazebo_client
    ])