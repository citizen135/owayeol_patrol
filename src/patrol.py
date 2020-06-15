#!/usr/bin/env python
import rosbag
import rospy
import os, sys, select										#input key
import time
import move_base
from move_base_msgs.msg import MoveBaseActionResult
from geometry_msgs.msg import PoseStamped
from os.path import expanduser								#find homedir
if os.name == 'nt':											#input key
  import msvcrt
else:
  import tty, termios
#way_list=os.listdir("%s/bagfiles" % homedir)
#rate = rospy.Rate(1) #10hz
def getKey():												#key
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def callback(data):										
	global stat
	stat=data.status.status
	print(stat)
    #rospy.loginfo(rospy.get_caller_id() + " \n%s\n%s",)

def patrol_init():
	global homedir
	bag = rosbag.Bag("%s/owayeol/map1/path1/init.bag" % homedir)
	goal_publisher = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
	goal = PoseStamped()
	print("init")
	for topic, msg, t in bag.read_messages(topics=[]):
		goal.header.stamp =rospy.Time.now()
		goal.header.frame_id = "map"
		goal.pose=msg.pose.pose
		goal_publisher.publish(goal)
		goal_publisher.publish(goal)

def patrol():
	global stat
	global homedir
	global way_num
	#for i in range(1,len(os.walk("%s/bagfiles" % homedir).next()[2])):
	if stat==3:
		bag = rosbag.Bag("%s/owayeol/map1/path1/waypoint%s.bag" % (homedir,way_num))
		goal_publisher = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=2)
		goal = PoseStamped()
		for topic, msg, t in bag.read_messages(topics=[]):
			goal.header.stamp =rospy.Time.now()
			goal.header.frame_id = "map"
			goal.pose=msg.pose.pose
			goal_publisher.publish(goal)
			goal_publisher.publish(goal)
		stat=1
		way_num+=1
		if way_num==5:
			way_num=1
			
	#rate.sleep()
	#way_list.sort()
	#for i in way_list:
	#	os.system("rosbag play ~/bagfiles/%s" % i )
	#os.system("rostopic pub /path_ready std_msgs/Empty -1")

# def waypoint():
	
#       	#pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
#       	rospy.init_node('talker', anonymous = True)
#       	rate = rospy.Rate(10) #10hz
#       	while not rospy.is_shutdown():
#             	hello_str = "hello world %s" % rospy.get_time()
#             	rospy.loginfo(hello_str)
#             	pub.publish(hello_str)
#             	rate.sleep()

if __name__=="__main__":
	if os.name != 'nt':
		settings = termios.tcgetattr(sys.stdin)
	homedir=expanduser("~")
	way_last=len(os.walk("%s/bagfiles" % homedir).next()[2])			#waypoint number
	stat=3
	way_num=1															#current waypoint
	pause=False
	rospy.init_node("patrol", anonymous=True)
	rospy.Subscriber('/move_base/result', MoveBaseActionResult, callback)
	rospy.loginfo("if you initialpose robot, press 'S'\n help 'h'")
	while True:
		try:
			key=getKey()
			if (key=='s'):												#stop & start
				patrol_init()
				pause= not pause
				print("run: "+str(pause))
			elif key=='k':
				patrol_init()
				exit()
			elif key=='h':
				print("""
				's' start/stop
				'k' kill program
				'h' help
				""")
			if pause==True:
				patrol()
		except KeyboardInterrupt:
			exit()