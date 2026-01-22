import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="True",
    )
    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="False",
    )

    use_max_arg = DeclareLaunchArgument(
        "use_max",
        default_value="True",
    )

    use_rtab_arg = DeclareLaunchArgument(
        "use_rtab",
        default_value="False",
    )

    use_slam = LaunchConfiguration("use_slam")
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rtab = LaunchConfiguration("use_rtab")

    max_universal = get_package_share_directory('max_universal')
    max_controller = get_package_share_directory('max_controller')
    max_description = get_package_share_directory('max_description')

    gazebo = IncludeLaunchDescription(
        os.path.join(
            max_description,
            'launch',
            'gazebo.launch.py'
        )
    )
    rviz2 = IncludeLaunchDescription(
        os.path.join(
            max_description,
            'launch',
            'display.launch.py'
        )
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joystick',
        parameters=[
            os.path.join(max_controller, 'config', 'joy_config.yaml')
        ]
    )

    universal = IncludeLaunchDescription(
        os.path.join(
            max_universal,
            'launch',
            'universal.launch.py'
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "use_slam": use_slam,
            "use_rtab": use_rtab,
        }.items()
    )

    return LaunchDescription([
        use_slam_arg,
        use_sim_time_arg,
        use_max_arg,
        use_rtab_arg,
        gazebo,
        rviz2,
        joy_node,
        universal
    ])