# how to run this program ####
in one terminal: `roslaunch prrexamples linemission.launch model:=waffle` to build the gazebo environment
in another terminal: `rosrun prrexamples follower.py` to start line following




# link of demo video ####
https://brandeis.zoom.us/rec/share/1vnOkLwJys9isN-F2jI2vOHzRikOwZFOTC_-gO0cVeAAfCq1K5dNk5LjbWE8GqT6.o5PvR2z3d6prT3lT




# the essences of this program (some codes are omitted) ####
#### We use opencv to these three lines to detect the yellow line
lower_yellow = numpy.array([ 40, 0, 0])
upper_yellow = numpy.array([ 120, 255, 255])
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

#### only look at a 20-row portion of the image (defined as the region of interest), starting three-quarters of the way down the image. 
search_top = int(3*h/4)
search_bot = search_top + 20

#### The robot will continue moving when there's yellow line in the view
if M['m00'] > 0:
-# don't really undersand how M works, but based on chatgpt
-cx = int(M['m10']/M['m00']) + 100
-cy = int(M['m01']/M['m00'])
	# plot a centroid of the line
        cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
	# calculate the deviation of the robot from the centrod
        err = cx - w/2
        # move at 0.2 m/s and turn based on the deviation's degree
        twist.linear.x = 0.2
        twist.angular.z = -float(err) / 1000
        cmd_vel_pub.publish(twist)

#### Stops when no yellow line in sight
else:
        cmd_vel_pub.publish(twist)