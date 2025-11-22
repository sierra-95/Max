import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():

    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="True",
        description="Launch SLAM package"
    )

    use_plotjuggler_arg = DeclareLaunchArgument(
        "use_plotjuggler",
        default_value="False",
        description="Launch PlotJuggler GUI"
    )
    
    use_plotjuggler = LaunchConfiguration("use_plotjuggler")
    use_slam = LaunchConfiguration("use_slam")

    max_controller = get_package_share_directory('max_controller')
    max_description = get_package_share_directory('max_description')
    max_localization = get_package_share_directory('max_localization')
    max_mapping = get_package_share_directory('max_mapping')

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
        condition=IfCondition(use_plotjuggler)
    )

    rviz2 = IncludeLaunchDescription(
        os.path.join(
            max_description,
            'launch',
            'display.launch.py'
        )
    )

    localization =  IncludeLaunchDescription(
        os.path.join(
            max_localization,
            'launch',
            'global_localization.launch.py'
        ),
        condition=UnlessCondition(use_slam)
    )

    slam = IncludeLaunchDescription(
        os.path.join(
            max_mapping,
            'launch',
            'slam.launch.py'
        ),
        condition=IfCondition(use_slam)
    )

    safety_stop = Node(
        package="max_utils",
        executable="safety_stop.py",
        output="screen"
    )

    return LaunchDescription([
        use_plotjuggler_arg,
        use_slam_arg,
        controller,
        joystick,
        plotjuggler_node,
        rviz2,
        localization,
        slam,
        safety_stop,
    ])