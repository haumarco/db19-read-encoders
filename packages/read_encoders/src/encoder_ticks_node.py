#!/usr/bin/env python

import os
import rospy
from duckietown import DTROS
from duckietown_msgs.msg import WheelsCmdStamped, EncoderTicksStamped
from std_msgs.msg import Header
import pigpio
import numpy as np


class MyNode(DTROS):

	def __init__(self, node_name):
		# initialize the DTROS parent class
		super(MyNode, self).__init__(node_name=node_name)
		# construct publisher
		self.pub = rospy.Publisher("~encoder_ticks", EncoderTicksStamped, queue_size=1)

		self.msg = EncoderTicksStamped() # Following the Duckietown convention

		# setup for getting wheel direction
		self.lastcb_left = 0
		self.lastcb_right = 0
		self.wheel_dir_left = WheelsCmdStamped()
		self.wheel_dir_right = WheelsCmdStamped()
		self.sub_wheel_dir =rospy.Subscriber("wheels_driver_node/wheels_cmd_executed", WheelsCmdStamped, self.update_wheel_direction, queue_size=1)

		####################
		self.left_ticks=0
		self.right_ticks=0
		self.last_left_ticks = 0
		self.last_right_ticks = 0

		# Relate pi to the pigpio interface
		self.pi = pigpio.pi()

		self.left_motor_pin = 18
		self.right_motor_pin = 19

		rospy.loginfo("%s has finished initializing!" % node_name)

		self.cb_left = self.pi.callback(18, pigpio.RISING_EDGE)
		self.cb_right = self.pi.callback(19, pigpio.RISING_EDGE)

	#updates wheel direction of each wheel
	def update_wheel_direction(self, msg_wheel_dir):
		if (msg_wheel_dir.vel_left != 0):
			self.wheel_dir_left = msg_wheel_dir.vel_left
		if (msg_wheel_dir.vel_right != 0):
			self.wheel_dir_right = msg_wheel_dir.vel_right


	def run(self):

		rospy.loginfo("Encoder ticks node has reached the main run function and is running")

		rate = rospy.Rate(20) # Hz - User can adjust this.

		self.lastcb_left = self.cb_left.tally()
		self.lastcb_right = self.cb_right.tally()

		while not rospy.is_shutdown():
			# .tally() is a counter of total ticks, get the diff and multiply with wheel direction
			tally_left = self.cb_left.tally()
			tally_right = self.cb_right.tally()
			self.left_ticks += (tally_left - self.lastcb_left) * np.sign(self.wheel_dir_left)
			self.right_ticks += (tally_right - self.lastcb_right) * np.sign(self.wheel_dir_right)
			#self.left_ticks = (tally_left - self.lastcb_left) * np.sign(self.wheel_dir_left)
			#self.right_ticks = (tally_right - self.lastcb_right) * np.sign(self.wheel_dir_right)
			self.lastcb_left = tally_left
			self.lastcb_right = tally_right

			if (self.left_ticks != self.last_left_ticks or self.right_ticks != self.last_right_ticks) and (self.left_ticks != 0 or self.right_ticks != 0):
				self.msg.header.stamp = rospy.get_rostime()
				self.msg.left_ticks = self.left_ticks
				self.msg.right_ticks = self.right_ticks
				self.pub.publish(self.msg)
				# for analysing purposes:
				rospy.loginfo("Published %d %d @ secs: %d nsecs: %d" % (self.msg.left_ticks, self.msg.right_ticks, self.msg.header.stamp.secs, self.msg.header.stamp.nsecs))
			
			self.last_left_ticks = self.left_ticks
			self.last_right_ticks = self.right_ticks
			rate.sleep()




if __name__ == '__main__':
	# create the node
	node = MyNode(node_name='my_node')
	# run node
	node.run()
	# keep spinning
	rospy.spin()