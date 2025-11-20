import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition


def generate_launch_description():

    use_plotjuggler_arg = DeclareLaunchArgument(
        "use_plotjuggler",
        default_value="False",
        description="Launch PlotJuggler GUI"
    )
    
    use_plotjuggler = LaunchConfiguration("use_plotjuggler")

    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('max_controller'),
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
            get_package_share_directory('max_controller'),
            'launch',
            'joystick_teleop.launch.py'
        )
    )

    plotjuggler_node = Node(
        package="plotjuggler",
        executable="plotjuggler",
        name="plotjuggler",
        output="screen",
        condition=IfCondition(use_plotjuggler)
    )

    rviz2 = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('max_description'),
            'launch',
            'display.launch.py'
        )
    )

    return LaunchDescription([
        use_plotjuggler_arg,
        controller,
        joystick,
        plotjuggler_node,
        rviz2
    ])