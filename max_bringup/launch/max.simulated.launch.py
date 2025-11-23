import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="False",
    )

    use_slam = LaunchConfiguration("use_slam")

    max_universal = get_package_share_directory('max_universal')
    max_description = get_package_share_directory('max_description')
    
    gazebo = IncludeLaunchDescription(
        os.path.join(
            max_description,
            'launch',
            'gazebo.launch.py'
        )
    )

    universal = IncludeLaunchDescription(
        os.path.join(
            max_universal,
            'launch',
            'universal.launch.py'
        ),
        launch_arguments={
            "use_sim_time": "True",
            "use_slam": use_slam,
            "use_rviz": "True"
        }.items()
    )

    return LaunchDescription([
        use_slam_arg,
        gazebo,
        universal
    ])