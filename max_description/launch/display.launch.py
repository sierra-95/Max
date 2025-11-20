from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
import os

def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")
    max_description_dir = get_package_share_directory("max_description")

    rviz_node = Node(
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
    )
    
    return LaunchDescription([
        rviz_node,
    ])