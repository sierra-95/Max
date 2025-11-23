import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="True",
    )
    use_slam = LaunchConfiguration("use_slam")

    max_firmware = get_package_share_directory('max_firmware')
    max_universal = get_package_share_directory('max_universal')
    max_bringup = get_package_share_directory('max_bringup')

    hardware_interface = IncludeLaunchDescription(
        os.path.join(
            max_firmware,
            'launch',
            'hardware_interface.launch.py'
        )
    )

    rplidar = Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='rplidar_node',
        output='screen',
        parameters=[
            os.path.join(
                max_bringup,
                'config',
                'rplidar_a1.yaml'
            )
        ]
    )

    universal = IncludeLaunchDescription(
        os.path.join(
            max_universal,
            'launch',
            'universal.launch.py'
        ),
        launch_arguments={
            "use_sim_time": "False",
            "use_slam": use_slam,
            "use_rviz": "False"
        }.items()
    )

    return LaunchDescription([
        use_slam_arg,
        hardware_interface,
        rplidar,
        universal
    ])