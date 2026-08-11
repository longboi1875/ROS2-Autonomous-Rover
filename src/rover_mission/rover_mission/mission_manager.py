import math
from pathlib import Path

import rclpy
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger

from .config import load_mission
from .mission import Mission


class MissionManager(Node):
    def __init__(self) -> None:
        super().__init__('mission_manager')
        default_file = str(Path(get_package_share_directory('rover_mission')) / 'config' / 'demo_mission.yaml')
        mission_file = self.declare_parameter('mission_file', default_file).value
        self._frame_id, waypoints = load_mission(mission_file)
        self._mission = Mission(waypoints)
        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self._status = self.create_publisher(String, 'mission/status', 10)
        self.create_service(Trigger, 'mission/start', self._start)
        self.create_service(Trigger, 'mission/cancel', self._cancel)
        self._goal_handle = None
        self._publish('IDLE')

    def _start(self, _request, response):
        if not self._client.wait_for_server(timeout_sec=2.0):
            response.success, response.message = False, 'Nav2 action server is unavailable'
            return response
        try:
            waypoint = self._mission.start()
        except RuntimeError as error:
            response.success, response.message = False, str(error)
            return response
        self._send(waypoint)
        response.success, response.message = True, 'mission started'
        return response

    def _send(self, waypoint) -> None:
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = self._frame_id
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x, goal.pose.pose.position.y = waypoint.x, waypoint.y
        goal.pose.pose.orientation.z = math.sin(waypoint.yaw / 2.0)
        goal.pose.pose.orientation.w = math.cos(waypoint.yaw / 2.0)
        self._publish(f'NAVIGATING {waypoint.x:.2f} {waypoint.y:.2f}')
        future = self._client.send_goal_async(goal)
        future.add_done_callback(self._goal_response)

    def _goal_response(self, future) -> None:
        self._goal_handle = future.result()
        if not self._goal_handle.accepted:
            self._mission.fail()
            self._publish('FAILED goal rejected')
            return
        result = self._goal_handle.get_result_async()
        result.add_done_callback(self._result)

    def _result(self, future) -> None:
        if future.result().status != 4:  # action_msgs/GoalStatus.STATUS_SUCCEEDED
            self._mission.fail()
            self._publish(f'FAILED status={future.result().status}')
            return
        next_waypoint = self._mission.waypoint_reached()
        if next_waypoint is None:
            self._publish('COMPLETE')
        else:
            self._send(next_waypoint)

    def _cancel(self, _request, response):
        self._mission.cancel()
        if self._goal_handle is not None:
            self._goal_handle.cancel_goal_async()
        self._publish('CANCELLED')
        response.success, response.message = True, 'mission cancelled'
        return response

    def _publish(self, text: str) -> None:
        self._status.publish(String(data=text))
        self.get_logger().info(text)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MissionManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
