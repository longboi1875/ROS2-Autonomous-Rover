from dataclasses import dataclass
from enum import Enum, auto
from math import isfinite
from typing import Iterable, Optional, Tuple


class MissionState(Enum):
    IDLE = auto()
    NAVIGATING = auto()
    COMPLETE = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass(frozen=True)
class Waypoint:
    x: float
    y: float
    yaw: float = 0.0

    def __post_init__(self) -> None:
        if not all(isfinite(value) for value in (self.x, self.y, self.yaw)):
            raise ValueError('waypoint values must be finite')


class Mission:
    def __init__(self, waypoints: Iterable[Waypoint]):
        self._waypoints: Tuple[Waypoint, ...] = tuple(waypoints)
        if not self._waypoints:
            raise ValueError('mission needs at least one waypoint')
        self._index = 0
        self.state = MissionState.IDLE

    @property
    def current(self) -> Optional[Waypoint]:
        return self._waypoints[self._index] if self._index < len(self._waypoints) else None

    @property
    def progress(self) -> float:
        return self._index / len(self._waypoints)

    def start(self) -> Waypoint:
        if self.state is not MissionState.IDLE:
            raise RuntimeError('mission was already started')
        self.state = MissionState.NAVIGATING
        return self._waypoints[0]

    def waypoint_reached(self) -> Optional[Waypoint]:
        if self.state is not MissionState.NAVIGATING:
            raise RuntimeError('mission is not navigating')
        self._index += 1
        if self._index == len(self._waypoints):
            self.state = MissionState.COMPLETE
            return None
        return self.current

    def fail(self) -> None:
        if self.state is MissionState.NAVIGATING:
            self.state = MissionState.FAILED

    def cancel(self) -> None:
        if self.state in (MissionState.IDLE, MissionState.NAVIGATING):
            self.state = MissionState.CANCELLED

