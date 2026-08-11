from pathlib import Path
from typing import List, Tuple

import yaml

from .mission import Waypoint


def load_mission(path: str) -> Tuple[str, List[Waypoint]]:
    mission_path = Path(path)
    with mission_path.open(encoding='utf-8') as stream:
        raw = yaml.safe_load(stream)
    if not isinstance(raw, dict) or not isinstance(raw.get('waypoints'), list):
        raise ValueError('mission file must contain a waypoints list')
    frame_id = raw.get('frame_id', 'map')
    if not isinstance(frame_id, str) or not frame_id:
        raise ValueError('frame_id must be a non-empty string')
    waypoints = [Waypoint(float(item['x']), float(item['y']), float(item.get('yaw', 0.0))) for item in raw['waypoints']]
    return frame_id, waypoints

