# ROS 2 Autonomous Rover

A fully simulated differential-drive rover that maps an unknown environment,
navigates waypoint missions, and fails safely when its LiDAR data goes stale.

## Stack

- Ubuntu 24.04 and ROS 2 Jazzy
- Gazebo Harmonic with `ros_gz`
- Nav2 and SLAM Toolbox
- Python mission manager
- C++ sensor safety monitor

## Quick start

ROS 2 Jazzy is supported on Ubuntu 24.04. In a Jazzy desktop installation:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 launch rover_bringup rover.launch.py
```

Wait until Nav2 reports that it is active, then start the four-waypoint mission:

```bash
ros2 service call /mission/start std_srvs/srv/Trigger '{}'
```

Watch mission and safety state:

```bash
ros2 topic echo /mission/status
ros2 topic echo /safety/state
```

Run without the Gazebo client with `headless:=True`. To localize in a saved map,
pass `slam:=False map:=/absolute/path/to/map.yaml`.

## What is implemented

- Differential-drive URDF/Xacro with LiDAR and IMU simulation
- Bounded agricultural test world with crop-row obstacles
- Gazebo-to-ROS topic bridges and TF/odometry
- SLAM Toolbox mapping configuration
- Nav2 planning, costmaps, recovery behaviours, and velocity smoothing
- Multi-waypoint action client with progress/status reporting
- C++ LiDAR watchdog that gates velocity commands fail-safe
- Unit tests for mission state/config parsing and watchdog timing

## Repository layout

```text
src/                  ROS 2 packages
docs/                 design notes and demo guide
scripts/              developer utilities
```

See [the architecture notes](docs/architecture.md) for node/topic ownership and
[the demo guide](docs/demo.md) for a short application-ready walkthrough.

## Development

```bash
colcon build --symlink-install --event-handlers console_direct+
colcon test
colcon test-result --verbose
python3 -m pytest
```

The pure Python tests can run without ROS if `pytest` and `PyYAML` are installed.
Full simulation requires Linux because ROS 2 Jazzy and Gazebo Harmonic are not
natively supported as a complete stack on macOS.

## License

Apache-2.0
