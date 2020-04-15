cmake_minimum_required(VERSION 2.8.3)
project(read_encoders)

find_package(catkin REQUIRED COMPONENTS
  rospy
  duckietown_msgs # Every duckietown packages should use this.

# Only the encoder_ticks_node needs these
  std_msgs
)

catkin_package()
