from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription, GroupAction
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
import os
from os import pathsep


def generate_launch_description():

    max_description = get_package_share_directory('max_description')
    max_description_prefix = get_package_prefix('max_description')

    is_ignition_arg = DeclareLaunchArgument(
        "is_ignition",
        default_value="False",
    )

    # Worlds
    world_name_arg = DeclareLaunchArgument(
        name='world_name',
        default_value='empty',
    )
    world_path = PathJoinSubstitution([
        max_description,
        'worlds',
        PythonExpression(expression=["'", LaunchConfiguration("world_name"), "'", " + '.world'"])
    ])

    #Models
    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=os.path.join(
            max_description,
            'urdf',
            'max.urdf.xacro'
        ),
        description='Absolute path to robot urdf file'
    )
    model_path = os.path.join(
        max_description,
        "models",
    )
    model_path += pathsep + os.path.join(
        max_description_prefix,
        "share",
    )
    #Robot *
    robot_description = ParameterValue(
        Command(["xacro ", 
                LaunchConfiguration('model'),
                " ",
                "is_ignition:=",
                LaunchConfiguration("is_ignition")
            ]), 
            value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            "robot_description": robot_description,
            "use_sim_time": False
        }],
        output='screen'
    )

    is_ignition = GroupAction(
        condition = IfCondition(LaunchConfiguration("is_ignition")),
        actions = [
                SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", model_path),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource([
                        os.path.join(
                            get_package_share_directory("ros_gz_sim"), 
                            "launch", 
                            "gz_sim.launch.py"
                        )
                    ]),
                    launch_arguments={
                        "gz_args": PythonExpression(["'", world_path, " -v 4 -r'"])
                    }.items()
                ),
                Node(
                    package="ros_gz_sim",
                    executable="create",
                    arguments=["-topic", "robot_description", "-name", "max"],
                    output="screen"
                )
        ]
    )
    is_classic = GroupAction(
        condition = UnlessCondition(LaunchConfiguration("is_ignition")),
        actions = [
                    SetEnvironmentVariable("GAZEBO_MODEL_PATH", model_path),
                    IncludeLaunchDescription(
                        PythonLaunchDescriptionSource(
                            os.path.join(
                                get_package_share_directory('gazebo_ros'),
                                'launch',
                                'gzserver.launch.py',
                            )                    
                        ),
                        launch_arguments  = {
                            'world': world_path
                        }.items()
                    ),
                    IncludeLaunchDescription(
                        PythonLaunchDescriptionSource(
                            os.path.join(
                                get_package_share_directory('gazebo_ros'),
                                'launch',
                                'gzclient.launch.py',
                            )
                        )
                    ),
                    Node(
                        package='gazebo_ros',
                        executable='spawn_entity.py',
                        arguments=["-entity", "max", "-topic", "robot_description"],
                        output='screen'
                    )
        ]
    )
    return LaunchDescription([
        model_arg,
        is_ignition_arg,
        world_name_arg,
        robot_state_publisher_node,
        is_ignition,
        is_classic
    ])