import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():

    use_slam = LaunchConfiguration("use_slam")
    use_rtab = LaunchConfiguration("use_rtab")

    max_controller = get_package_share_directory('max_controller')
    max_localization = get_package_share_directory('max_localization')
    max_mapping = get_package_share_directory('max_mapping')
    max_navigation = get_package_share_directory('max_navigation')

    controller = IncludeLaunchDescription(
        os.path.join(
            max_controller,
            'launch',
            'controller.launch.py'
        ),
        launch_arguments={
            "use_simple_controller": "False",
            "use_python" : "False"
        }.items()
    )

    joystick = IncludeLaunchDescription(
        os.path.join(
            max_controller,
            'launch',
            'joystick_teleop.launch.py'
        )
    )

    plotjuggler_node = Node(
        package="plotjuggler",
        executable="plotjuggler",
        name="plotjuggler",
        output="screen",
    )

    safety_stop = Node(
        package="max_utils",
        executable="safety_stop.py",
        output="screen"
    )

    GroupAction(
        condition=UnlessCondition(use_rtab),
        actions=[
            IncludeLaunchDescription(
                os.path.join(
                    max_localization,
                    'launch',
                    'global_localization.launch.py'
                ),
                condition=UnlessCondition(use_slam)
            ),
            IncludeLaunchDescription(
                os.path.join(
                    max_mapping,
                    'launch',
                    'slam.launch.py'
                ),
                condition=IfCondition(use_slam)
            ),
            IncludeLaunchDescription(
                os.path.join(
                    max_navigation,
                    'launch',
                    'navigation.launch.py'
                )
            )
        ]
    )

    return LaunchDescription([
        controller,
        joystick,
        plotjuggler_node,
        safety_stop
    ])