#!/usr/bin/env python
import rospy
import time
import sys
from std_msgs.msg import String,Int8
from owayeol.msg import ChangeRobot, YoloResult,RobotState

##clear
stamp=-1
alert_robot=-1
robot_num=[0]*3
wait_num=[0]*3
wait_num[1]=1
##

def ALERT(data):
    global stamp
    global alert_robot
    global catch
    global wait_num
    try: 
        first_wait=wait_num.index(1)
        stamp=data.stamp                            #yolo add
        catch=data.catch

        changrobot_topic="/robot%s/changepath" % first_wait
        #topic /robot%s/maincommand patrol??????
        change_pub = rospy.Publisher(changrobot_topic, Int8, queue_size=1)
        # change.way_robot=data.alert_robot
        # change.wait_robot=first_wait
        # change.path_num=data.path_num
        change_pub.publish(data.path_num)
        # rospy.loginfo(rospy.get_time())
        
    except ValueError:
        rospy.loginfo("no more wait robot")
    
def robotstate(data):
    pass

if __name__ == '__main__':
    rospy.init_node('PatrolServer')
    rospy.Subscriber("/alert", YoloResult, ALERT)
    rospy.Subscriber("/robotstate", RobotState, robotstate)
    ##clear
    ex=YoloResult()
    ex.stamp=999
    ex.alert_robot=999
    ex.path_num=999
    ex.catch=999
    ALERT(ex)
    ##
    while not rospy.is_shutdown():
        try:
            pass
        except rospy.ROSInterruptException:
            pass