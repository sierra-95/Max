import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node


def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
    )
    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="True",
    )
    use_master_arg = DeclareLaunchArgument(
        "use_master",
        default_value="False",
    )

    max_description = get_package_share_directory('max_description')
    max_controller = get_package_share_directory('max_controller')
    max_firmware = get_package_share_directory('max_firmware')
    max_universal = get_package_share_directory('max_universal')
    max_bringup = get_package_share_directory('max_bringup')

    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=os.path.join(
            max_description,
            'urdf',
            'max.urdf.xacro'
        ),
        description='Absolute path to robot urdf file'
    )

    use_model = LaunchConfiguration("model")
    use_slam = LaunchConfiguration("use_slam")
    use_master = LaunchConfiguration("use_master")
    use_sim_time = LaunchConfiguration("use_sim_time")

    robot_description = ParameterValue(
        Command([
            "xacro", 
            " ",
            use_model,
            " ",
            "is_sim:=false",
        ]), 
        value_type=str
    )

    master = GroupAction(
        condition = IfCondition(use_master),
        actions = [
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                parameters=[{"robot_description": robot_description}],
                output='screen'
            ),
            Node(
                package='joy',
                executable='joy_node',
                name='joystick',
                parameters=[
                    os.path.join(max_controller, 'config', 'joy_config.yaml')
                ]
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
    slave = GroupAction(
        condition = UnlessCondition(use_master),
        actions = [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory("rplidar_ros"),
                        "launch",
                        "rplidar_a1_launch.py"
                    )
                ),
                launch_arguments={
                    "channel_type": "serial",
                    "serial_port": "/dev/ttyUSB0",
                    "serial_baudrate": "115200",
                    "frame_id": "lidar_link",
                    "inverted": "false",
                    "angle_compensate": "true",
                    "scan_mode": "Sensitivity",
                }.items()
            ),
            TimerAction(
                period=3.0,
                actions=[
                    IncludeLaunchDescription(
                        os.path.join(
                            max_firmware,
                            'launch',
                            'hardware_interface.launch.py'
                        ),
                        launch_arguments={
                            "model": use_model,
                        }.items()
                    ),
                    IncludeLaunchDescription(
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
                ]
            )
        ]
    )

    return LaunchDescription([
        model_arg,
        use_sim_time_arg,
        use_slam_arg,
        use_master_arg,
        master,
        slave,
    ])