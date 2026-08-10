#pragma once

#include <chrono>

namespace rover_safety {

enum class SafetyState { kWaitingForScan, kHealthy, kScanStale };

class SafetyLogic {
 public:
  explicit SafetyLogic(std::chrono::milliseconds scan_timeout);
  void record_scan(std::chrono::steady_clock::time_point stamp);
  SafetyState evaluate(std::chrono::steady_clock::time_point now) const;
  bool motion_allowed(std::chrono::steady_clock::time_point now) const;

 private:
  std::chrono::milliseconds scan_timeout_;
  std::chrono::steady_clock::time_point last_scan_{};
  bool has_scan_{false};
};

}  // namespace rover_safety

