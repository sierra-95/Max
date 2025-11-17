import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription


def generate_launch_description():

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('max_description'),
            'launch',
            'gazebo.launch.py'
        )
    )

    universal = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('max_universal'),
            'launch',
            'universal.launch.py'
        )
    )

    return LaunchDescription([
        gazebo,
        universal
    ])