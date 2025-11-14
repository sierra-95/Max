from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    joint_state_broadcaster_node = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            "--controller-manager",
            "/controller_manager"
        ],
        output='screen'
    )

    simple_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'simple_velocity_controller',
            "--controller-manager",
            "/controller_manager"
        ],
        output='screen'
    )

    return LaunchDescription([
        joint_state_broadcaster_node,
        simple_controller
    ])