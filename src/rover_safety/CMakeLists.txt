cmake_minimum_required(VERSION 3.8)
project(rover_safety)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

add_library(safety_logic src/safety_logic.cpp)
target_include_directories(safety_logic PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>)
target_compile_features(safety_logic PUBLIC cxx_std_17)

add_executable(safety_monitor src/safety_monitor_node.cpp)
target_link_libraries(safety_monitor safety_logic)
ament_target_dependencies(safety_monitor geometry_msgs rclcpp sensor_msgs std_msgs)

install(TARGETS safety_logic safety_monitor EXPORT export_rover_safety
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)
install(DIRECTORY include/ DESTINATION include)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_safety_logic test/test_safety_logic.cpp)
  target_link_libraries(test_safety_logic safety_logic)
endif()

ament_export_include_directories(include)
ament_export_libraries(safety_logic)
ament_export_targets(export_rover_safety HAS_LIBRARY_TARGET)
ament_package()
