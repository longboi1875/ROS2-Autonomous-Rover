#include <chrono>
#include <stdexcept>

#include "gtest/gtest.h"
#include "rover_safety/safety_logic.hpp"

using namespace std::chrono_literals;

TEST(SafetyLogic, BlocksMotionUntilFirstScan) {
  rover_safety::SafetyLogic logic(500ms);
  EXPECT_EQ(logic.evaluate(std::chrono::steady_clock::time_point{}), rover_safety::SafetyState::kWaitingForScan);
}

TEST(SafetyLogic, ScanExpiresAfterTimeout) {
  rover_safety::SafetyLogic logic(500ms);
  const auto start = std::chrono::steady_clock::time_point{};
  logic.record_scan(start);
  EXPECT_TRUE(logic.motion_allowed(start + 500ms));
  EXPECT_EQ(logic.evaluate(start + 501ms), rover_safety::SafetyState::kScanStale);
}

TEST(SafetyLogic, RejectsNonsenseTimeout) {
  EXPECT_THROW(rover_safety::SafetyLogic(0ms), std::invalid_argument);
}
