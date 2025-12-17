import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
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

    use_slam = LaunchConfiguration("use_slam")
    use_sim_time = LaunchConfiguration("use_sim_time")

    max_universal = get_package_share_directory('max_universal')
    max_controller = get_package_share_directory('max_controller')
    max_description = get_package_share_directory('max_description')
    bumperbot_description = get_package_share_directory('bumperbot_description')

    use_max = GroupAction(
        condition = IfCondition(LaunchConfiguration("use_max")),
        actions=[
            IncludeLaunchDescription(
                os.path.join(
                    max_description,
                    'launch',
                    'gazebo.launch.py'
                )
            ),
            IncludeLaunchDescription(
                os.path.join(
                    max_description,
                    'launch',
                    'display.launch.py'
                )
            )
        ]
    )

    use_bumperbot = GroupAction(
        condition = UnlessCondition(LaunchConfiguration("use_max")),
        actions=[
            IncludeLaunchDescription(
                os.path.join(
                    bumperbot_description,
                    'launch',
                    'gazebo.launch.py'
                )
            ),
            IncludeLaunchDescription(
                os.path.join(
                    bumperbot_description,
                    'launch',
                    'display.launch.py'
                )
            )
        ]
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
        }.items()
    )

    return LaunchDescription([
        use_slam_arg,
        use_sim_time_arg,
        use_max_arg,
        use_max,
        use_bumperbot,
        joy_node,
        universal
    ])