import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription


def generate_launch_description():

    hardware_interface = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('max_firmware'),
            'launch',
            'hardware_interface.launch.py'
        )
    )

    universal = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('max_universal'),
            'launch',
            'universal.launch.py'
        ),
        launch_arguments={
            "use_sim_time": "False"
        }.items()
    )

    return LaunchDescription([
        hardware_interface,
        universal
    ])