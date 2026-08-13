from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import SetRemap
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution([FindPackageShare('rover_navigation'), 'config', 'nav2.yaml'])
    slam_params = PathJoinSubstitution([FindPackageShare('rover_navigation'), 'config', 'slam.yaml'])
    bringup = PathJoinSubstitution([FindPackageShare('nav2_bringup'), 'launch', 'bringup_launch.py'])

    return LaunchDescription([
        DeclareLaunchArgument('slam', default_value='True', description='Map live instead of loading a map'),
        DeclareLaunchArgument('map', default_value='', description='Map YAML used when slam is false'),
        DeclareLaunchArgument('use_sim_time', default_value='True'),
        GroupAction([
            SetRemap(src='/cmd_vel', dst='/cmd_vel_nav'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(bringup),
                launch_arguments={
                    'slam': LaunchConfiguration('slam'),
                    'map': LaunchConfiguration('map'),
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'params_file': params,
                    'slam_params_file': slam_params,
                    'autostart': 'True',
                }.items(),
            ),
        ]),
    ])

