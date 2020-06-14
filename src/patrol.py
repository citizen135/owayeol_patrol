#!/usr/bin/env python

import rosbag
import rospy
import os, sys
import time
import move_base
from move_base_msgs.msg import MoveBaseActionResult
from geometry_msgs.msg import PoseStamped
from os.path import expanduser

#way_list=os.listdir("%s/bagfiles" % homedir)
#rate = rospy.Rate(1) #10hz


def callback(data):
	global stat
	stat=data.status.status
	print(stat)
    #rospy.loginfo(rospy.get_caller_id() + " \n%s\n%s"

def patrol():
	global stat
	global homedir
	global i
	time.sleep(1)
	#for i in range(1,len(os.walk("%s/bagfiles" % homedir).next()[2])):
	if stat==3:
		bag = rosbag.Bag("%s/bagfiles/waypoint%s.bag" % (homedir,i))
		goal_publisher = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=2)
		goal = PoseStamped()
		for topic, msg, t in bag.read_messages(topics=[]):
			goal.header.stamp =rospy.Time.now()
			goal.header.frame_id = "map"
			goal.pose=msg.pose.pose
			print(msg.pose.pose)
			print(goal.pose)
			goal_publisher.publish(goal)
			goal_publisher.publish(goal)
		stat=1
		i=i+1
		if i==5:
			i=1
			
	#rate.sleep()
	#way_list.sort()
	#for i in way_list:
	#	os.system("rosbag play ~/bagfiles/%s" % i )
	#os.system("rostopic pub /path_ready std_msgs/Empty -1")

def waypoint():
	
      	#pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
      	rospy.init_node('talker', anonymous = True)
      	rate = rospy.Rate(10) #10hz
      	while not rospy.is_shutdown():
            	hello_str = "hello world %s" % rospy.get_time()
            	rospy.loginfo(hello_str)
            	pub.publish(hello_str)
            	rate.sleep()

if __name__=="__main__":
	homedir=expanduser("~")
	way_num=0
	stat=3
	i=1

	rospy.init_node("patrol", anonymous=True)
	rospy.Subscriber('/move_base/result', MoveBaseActionResult, callback)
	while True:
		try:
			patrol()
		except rospy.ROSInterruptException:
			exit()
		except KeyboardInterrupt:
			print("goodbye")
			exit()
