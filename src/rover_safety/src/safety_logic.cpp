#include "rover_safety/safety_logic.hpp"

#include <stdexcept>

namespace rover_safety {

SafetyLogic::SafetyLogic(std::chrono::milliseconds scan_timeout) : scan_timeout_(scan_timeout) {
  if (scan_timeout.count() <= 0) throw std::invalid_argument("scan timeout must be positive");
}

void SafetyLogic::record_scan(std::chrono::steady_clock::time_point stamp) {
  last_scan_ = stamp;
  has_scan_ = true;
}

SafetyState SafetyLogic::evaluate(std::chrono::steady_clock::time_point now) const {
  if (!has_scan_) return SafetyState::kWaitingForScan;
  if (now - last_scan_ > scan_timeout_) return SafetyState::kScanStale;
  return SafetyState::kHealthy;
}

bool SafetyLogic::motion_allowed(std::chrono::steady_clock::time_point now) const {
  return evaluate(now) == SafetyState::kHealthy;
}

}  // namespace rover_safety

