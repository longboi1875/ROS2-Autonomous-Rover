# Demo walkthrough

1. Launch the stack and show the robot spawning between the crop rows.
2. In RViz, point out the LiDAR scan, occupancy grid, TF tree, and costmaps.
3. Call `/mission/start`; show the global path and local obstacle avoidance.
4. Insert a box in front of the rover to demonstrate replanning.
5. Pause Gazebo sensor publication and show `/safety/state` become `SCAN_STALE`
   while `/cmd_vel` is forced to zero.
6. Resume the simulation and restart the launch for a clean mission run.

Useful diagnostics:

```bash
ros2 topic hz /scan
ros2 topic echo /safety/state
ros2 action info /navigate_to_pose
ros2 run tf2_tools view_frames
ros2 node list
```

If Nav2 does not activate, first check that `/scan`, `/odom`, `/tf`, and `/clock`
are publishing and that `base_footprint` can transform to `odom`.
