#include <chrono>
#include <memory>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "std_msgs/msg/string.hpp"
#include "rover_safety/safety_logic.hpp"

using namespace std::chrono_literals;

class SafetyMonitor : public rclcpp::Node {
 public:
  SafetyMonitor() : Node("safety_monitor"), logic_(std::chrono::milliseconds(declare_parameter("scan_timeout_ms", 750))) {
    scan_sub_ = create_subscription<sensor_msgs::msg::LaserScan>("scan", rclcpp::SensorDataQoS(),
      [this](sensor_msgs::msg::LaserScan::ConstSharedPtr) { logic_.record_scan(std::chrono::steady_clock::now()); });
    velocity_sub_ = create_subscription<geometry_msgs::msg::Twist>("cmd_vel_nav", 10,
      [this](geometry_msgs::msg::Twist::ConstSharedPtr command) {
        if (logic_.motion_allowed(std::chrono::steady_clock::now())) velocity_pub_->publish(*command);
      });
    velocity_pub_ = create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
    state_pub_ = create_publisher<std_msgs::msg::String>("safety/state", 10);
    timer_ = create_wall_timer(100ms, [this] { tick(); });
  }

 private:
  void tick() {
    const auto state = logic_.evaluate(std::chrono::steady_clock::now());
    std_msgs::msg::String message;
    if (state == rover_safety::SafetyState::kHealthy) message.data = "HEALTHY";
    else if (state == rover_safety::SafetyState::kWaitingForScan) message.data = "WAITING_FOR_SCAN";
    else message.data = "SCAN_STALE";
    state_pub_->publish(message);
    if (state != rover_safety::SafetyState::kHealthy) velocity_pub_->publish(geometry_msgs::msg::Twist{});
  }

  rover_safety::SafetyLogic logic_;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr velocity_sub_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr state_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SafetyMonitor>());
  rclcpp::shutdown();
  return 0;
}
