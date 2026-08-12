import pytest

from rover_mission.mission import Mission, MissionState, Waypoint


def test_runs_each_waypoint_in_order():
    mission = Mission([Waypoint(1, 2), Waypoint(3, 4, 1.2)])
    assert mission.start() == Waypoint(1, 2)
    assert mission.waypoint_reached() == Waypoint(3, 4, 1.2)
    assert mission.progress == 0.5
    assert mission.waypoint_reached() is None
    assert mission.state is MissionState.COMPLETE
    assert mission.progress == 1.0


def test_empty_mission_is_rejected():
    with pytest.raises(ValueError, match='at least one'):
        Mission([])


@pytest.mark.parametrize('bad_value', [float('nan'), float('inf'), -float('inf')])
def test_non_finite_waypoint_is_rejected(bad_value):
    with pytest.raises(ValueError, match='finite'):
        Waypoint(bad_value, 0)


def test_cancel_is_terminal():
    mission = Mission([Waypoint(1, 2)])
    mission.start()
    mission.cancel()
    assert mission.state is MissionState.CANCELLED
    with pytest.raises(RuntimeError, match='not navigating'):
        mission.waypoint_reached()

