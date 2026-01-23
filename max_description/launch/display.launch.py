from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
import os

def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rtab = LaunchConfiguration("use_rtab")
    max_description_dir = get_package_share_directory("max_description")

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )
    
    slam = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-d', os.path.join(
            max_description_dir,
            'rviz',
            'display.rviz'
        )],
        condition = UnlessCondition(use_rtab)
    )

    vslam = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-d', os.path.join(
            max_description_dir,
            'rviz',
            'rtab.rviz'
        )],
        condition = IfCondition(use_rtab)
    )
    
    return LaunchDescription([
        slam,
        vslam
    ])