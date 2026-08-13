from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def package_launch(package, filename):
    return PythonLaunchDescriptionSource(
        PathJoinSubstitution([FindPackageShare(package), 'launch', filename])
    )


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='False'),
        DeclareLaunchArgument('slam', default_value='True'),
        DeclareLaunchArgument('map', default_value=''),
        DeclareLaunchArgument('mission', default_value='True'),
        IncludeLaunchDescription(
            package_launch('rover_gazebo', 'sim.launch.py'),
            launch_arguments={'headless': LaunchConfiguration('headless')}.items(),
        ),
        IncludeLaunchDescription(
            package_launch('rover_navigation', 'navigation.launch.py'),
            launch_arguments={
                'slam': LaunchConfiguration('slam'),
                'map': LaunchConfiguration('map'),
                'use_sim_time': 'True',
            }.items(),
        ),
        Node(
            package='rover_safety', executable='safety_monitor', name='safety_monitor',
            output='screen', parameters=[{'use_sim_time': True, 'scan_timeout_ms': 750}],
        ),
        Node(
            package='rover_mission', executable='mission_manager', name='mission_manager',
            output='screen', parameters=[{'use_sim_time': True}], condition=IfCondition(LaunchConfiguration('mission')),
        ),
    ])
