#!/usr/bin/env python
import rospy
import time
import sys
from std_msgs.msg import String,Int8
from owayeol.msg import ChangeRobot, YoloResult
import rosnode
#rosnode.get_node_names()
stamp=-1
alert_robot=-1
robot_num=[0]*3
wait_num=[0]*3

def callback(data):
    global stamp
    global alert_robot
    global catch
    global wait_num
    try: 
        first_wait=wait_num.index(1)
        stamp=data.stamp
        catch=data.catch

        changrobot_topic="/robot%s/changerobot" % first_wait
        change_pub = rospy.Publisher(changrobot_topic, ChangeRobot, queue_size=10)
        change=ChangeRobot()
        change.way_robot=data.alert_robot
        change.wait_robot=first_wait
        change.path_num=data.path_num
        change_pub.publish(change)
    except ValueError:
        rospy.loginfo("no more wait robot")
    


if __name__ == '__main__':
    rospy.init_node('PatrolServer', anonymous=True)
    rospy.Subscriber("/alert", YoloResult, callback)
    ex=YoloResult()
    ex.stamp=1
    ex.alert_robot=1
    ex.path_num=1
    ex.catch=1
    callback(ex)
    while not rospy.is_shutdown():
        try:
            pass
        except rospy.ROSInterruptException:
            pass