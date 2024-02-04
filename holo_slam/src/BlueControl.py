#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import socket

addres="94:E6:86:3C:EC:6E"
channel = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 
socket.BTPROTO_RFCOMM)



def cmd_vel_callback(msg):
    # Convert linear and angular velocities to holonomic drive commands
    vx = msg.linear.x*2
    vy = msg.linear.y*2
    wz = msg.angular.z*1.1

    # Calculate the individual wheel speeds for a holonomic drive
    wheel1_speed = (vx - wz)*100
    wheel2_speed = -(vy + wz)*100
    wheel3_speed = (vx + wz)*100
    wheel4_speed = -(vy - wz)*100
    print(wheel1_speed,wheel2_speed,wheel3_speed,wheel4_speed)

    # Send the wheel speeds to the ESP32 via Bluetooth
    cmd = f"Z{wheel1_speed},{wheel2_speed},{wheel3_speed},{wheel4_speed}\n"
    s.send(cmd.encode())

def main():

    s.connect((addres,channel))
    print("ready")
    rospy.init_node('blue_control')
    rospy.Subscriber('/cmd_vel', Twist, cmd_vel_callback)
    rospy.spin()

if __name__ == '__main__':
    main()
