from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world = LaunchConfiguration('world')
    description_file = PathJoinSubstitution([FindPackageShare('rover_description'), 'urdf', 'rover.urdf.xacro'])
    robot_description = {'robot_description': Command([FindExecutable(name='xacro'), ' ', description_file])}
    bridge_config = PathJoinSubstitution([FindPackageShare('rover_gazebo'), 'config', 'bridge.yaml'])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare('ros_gz_sim'), '/launch/gz_sim.launch.py']),
        launch_arguments={'gz_args': [PythonExpression([
            "'-s -r -v 3 ' if '", LaunchConfiguration('headless'),
            "'.lower() == 'true' else '-r -v 3 '",
        ]), world]}.items(),
    )
    return LaunchDescription([
        DeclareLaunchArgument('world', default_value=PathJoinSubstitution([FindPackageShare('rover_gazebo'), 'worlds', 'training_field.sdf'])),
        DeclareLaunchArgument('headless', default_value='False'),
        gazebo,
        Node(package='robot_state_publisher', executable='robot_state_publisher', parameters=[robot_description, {'use_sim_time': True}]),
        Node(package='ros_gz_bridge', executable='parameter_bridge', parameters=[{'config_file': bridge_config}], output='screen'),
        TimerAction(period=2.0, actions=[Node(package='ros_gz_sim', executable='create', arguments=['-name', 'rover', '-topic', 'robot_description', '-x', '-4', '-y', '-4', '-z', '0.3'], output='screen')]),
    ])
