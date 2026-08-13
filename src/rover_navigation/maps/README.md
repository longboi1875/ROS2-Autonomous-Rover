# Saved maps

Save SLAM Toolbox maps here with:

```bash
ros2 run nav2_map_server map_saver_cli -f src/rover_navigation/maps/training_field
```

Then launch localization with `slam:=False` and
`map:=/absolute/path/to/training_field.yaml`.
