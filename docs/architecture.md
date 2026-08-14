# Architecture

## Data flow

```text
Gazebo sensors ──scan/imu/odom──> SLAM or AMCL ──map→odom TF──┐
                                                              │
mission_manager ──NavigateToPose action──> Nav2 planner/controller
                                                │
                                           /cmd_vel_nav
                                                │
LiDAR /scan ──> safety_monitor watchdog ─────────┤
                                                │ healthy only
                                           /cmd_vel
                                                │
                                      Gazebo diff drive
```

## Packages

| Package | Language | Responsibility |
| --- | --- | --- |
| `rover_description` | Xacro | Geometry, inertia, joints, sensors, plugins |
| `rover_gazebo` | Python/SDF | World, spawning, and ROS/Gazebo bridges |
| `rover_navigation` | Python/YAML | SLAM, AMCL, planner, controller, costmaps |
| `rover_mission` | Python | Mission state machine and Nav2 action client |
| `rover_safety` | C++ | Scan watchdog and velocity command interlock |
| `rover_bringup` | Python | Whole-system orchestration |

## Frame tree

```text
map → odom → base_footprint → base_link → lidar_link
                                      └→ imu_link
                                      ├→ left_wheel_link
                                      └→ right_wheel_link
```

SLAM Toolbox or AMCL owns `map → odom`. Gazebo's differential drive owns
`odom → base_footprint`, and `robot_state_publisher` owns the fixed/joint frames.

## Safety behaviour

Nav2 is deliberately remapped to `/cmd_vel_nav`. The safety monitor is the only
normal publisher to `/cmd_vel`, which Gazebo consumes. Motion remains blocked
until the first scan and is stopped when scans are more than 750 ms old. The
timing logic uses a monotonic clock, so simulation-clock jumps cannot bypass it.

This is a software interlock for simulation, not a certified emergency stop.

