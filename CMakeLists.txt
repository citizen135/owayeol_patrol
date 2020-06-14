cmake_minimum_required(VERSION 3.0.2)
project(owayeol)

find_package(catkin REQUIRED COMPONENTS
  rosbag
  rospy
  move_base_msgs
  geometry_msgs
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
