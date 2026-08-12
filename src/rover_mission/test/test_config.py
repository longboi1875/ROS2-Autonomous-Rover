from pathlib import Path

import pytest

from rover_mission.config import load_mission
from rover_mission.mission import Waypoint


def test_loads_demo_mission():
    config = Path(__file__).parents[1] / 'config' / 'demo_mission.yaml'
    frame, waypoints = load_mission(str(config))
    assert frame == 'map'
    assert waypoints[0] == Waypoint(-4.0, 4.0, 1.57)
    assert len(waypoints) == 4


def test_rejects_missing_waypoint_list(tmp_path):
    config = tmp_path / 'bad.yaml'
    config.write_text('frame_id: map\n', encoding='utf-8')
    with pytest.raises(ValueError, match='waypoints list'):
        load_mission(str(config))
