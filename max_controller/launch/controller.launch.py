from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    use_python_arg = DeclareLaunchArgument(
        "use_python",
        default_value="False",
    )

    wheel_radius_arg = DeclareLaunchArgument(
        "wheel_radius",
        default_value="0.0425",
    )

    wheel_separation_arg = DeclareLaunchArgument(
        "wheel_separation",
        default_value="0.232",
    )

    use_simple_controller_arg = DeclareLaunchArgument(
        "use_simple_controller",
        default_value="True",
    )

    use_python = LaunchConfiguration("use_python")
    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")
    use_simple_controller = LaunchConfiguration("use_simple_controller")

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    wheel_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "max_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        condition = UnlessCondition(use_simple_controller),
    )

    simple_controller = GroupAction(
        condition = IfCondition(use_simple_controller),
        actions = [
                Node(
                    package="controller_manager",
                    executable="spawner",
                    arguments=["simple_velocity_controller",
                            "--controller-manager",
                            "/controller_manager"
                    ]
                ),

                Node(
                    package="max_controller",
                    executable="simple_controller.py",
                    parameters=[
                        {"wheel_radius": wheel_radius},
                        {"wheel_separation": wheel_separation},
                    ],
                    condition=IfCondition(use_python),
                ),

                Node(
                    package="max_controller",
                    executable="simple_controller",
                    parameters=[
                        {"wheel_radius": wheel_radius},
                        {"wheel_separation": wheel_separation},
                    ],
                    condition=UnlessCondition(use_python),
                )

        ]
    )

    return LaunchDescription(
        [
            use_python_arg,
            wheel_radius_arg,
            wheel_separation_arg,
            use_simple_controller_arg,
            simple_controller,
            wheel_controller_spawner,
            joint_state_broadcaster_spawner,
        ]
    )