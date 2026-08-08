# ROS 2 Autonomous Rover

A fully simulated differential-drive rover that maps an unknown environment,
navigates waypoint missions, and fails safely when its LiDAR data goes stale.

## Planned stack

- Ubuntu 24.04 and ROS 2 Jazzy
- Gazebo Harmonic with `ros_gz`
- Nav2 and SLAM Toolbox
- Python mission manager
- C++ sensor safety monitor

The repository is being developed in small, runnable milestones. Setup and
demo instructions will grow alongside the implementation.

## Repository layout

```text
src/                  ROS 2 packages
docs/                 design notes and demo guide
scripts/              developer utilities
```

## License

Apache-2.0
