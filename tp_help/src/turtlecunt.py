#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose as TurtlePose
import math

class TurtleController:
    def __init__(self):
        rospy.init_node('turtle_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', TurtlePose, self.pose_callback)
        self.pose = TurtlePose()
        while self.pose.x == 0:
            pass
        print("initialized")

    def pose_callback(self, data):
        self.pose = data

    def move(self, linear_speed, angular_speed):
        twist = Twist()
        twist.linear.x = linear_speed
        twist.angular.z = angular_speed
        self.velocity_publisher.publish(twist)

    def rotate(self, angular_speed):
        self.move(0, angular_speed)

    def stop(self):
        self.move(0, 0)

    def go_forward_and_stop(self, linear_speed, distance):
        initial_x = self.pose.x
        distance_moved = 0.0
        print(3)
        while distance_moved < distance:
            self.move(linear_speed, 0)
            print(4)
            #rospy.sleep(0.1)  # Sleep for a short duration to update the pose
            distance_moved = abs(self.pose.x - initial_x)



        self.stop()

    def go_to_goal(self, goal_pose):
        distance = math.sqrt((goal_pose.x - self.pose.x)*2 + (goal_pose.y - self.pose.y)*2)
        angle = math.atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

        while distance > 0.1:
            self.move(1.0, 2.0 * (angle - self.pose.theta))
            distance = math.sqrt((goal_pose.x - self.pose.x)*2 + (goal_pose.y - self.pose.y)*2)

        self.stop()

if __name__ == '__main__':   #double underscore for name and main
    while not rospy.is_shutdown():
        print(1)
        try:
            controller = TurtleController()
            print(2)


            controller.go_forward_and_stop(1.0, 2.0) 

            controller.rotate(1.0)
            controller.stop()  

        except ROSinterruptException:
            print("input")