#!/usr/bin/env python


## to run
# roslaunch prrexamples linemission.launch model:=waffle
# rosrun prrexamples follower.py

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy

bridge = CvBridge()
# Callback does nothing yet
def image_callback(msg):
    image = bridge.imgmsg_to_cv2(msg) 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 

    lower_yellow = numpy.array([ 40, 0, 0])
    upper_yellow = numpy.array([ 120, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow) 
    masked = cv2.bitwise_and(image, image, mask=mask) 
    # cv2.imshow("window", mask)
    # cv2.waitKey(3)

    h, w, d = image.shape
    search_top = int(3*h/4)
    search_bot = search_top + 20
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    M = cv2.moments(mask)

    twist = Twist()   
    if M['m00'] > 0:
        cx = int(M['m10']/M['m00']) + 100
        cy = int(M['m01']/M['m00'])
        cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
        err = cx - w/2
        print(cx, w/2, err)
        twist.linear.x = 0.2
        twist.angular.z = -float(err) / 1000
        cmd_vel_pub.publish(twist)
    else:
        cmd_vel_pub.publish(twist)
    cv2.imshow("window", image)
    cv2.waitKey(3)



rospy.init_node('follower')

cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

# Subscribe to raw image topic
image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, image_callback)
rospy.spin()