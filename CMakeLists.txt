cmake_minimum_required(VERSION 3.0.2)
project(owayeol)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rosbag
  rospy
  move_base_msgs
  geometry_msgs
  std_msgs
  message_generation
)

add_message_files(
  FILES
  YoloResult.msg
  ChangeRobot.msg
  RobotState.msg
)

#catkin_package(
#  CATKIN_DEPENDS std_msgs message_runtime
#)

generate_messages(
  DEPENDENCIES
  std_msgs
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
