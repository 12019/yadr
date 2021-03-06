#!/usr/bin/python

# http://forums.trossenrobotics.com/tutorials/introduction-129/delta-robot-kinematics-3276/

import sys
import io
from pprint import pprint
from math import *



# robot geometry
# (look at pics above for explanation)
e = 115.0     # end effector
f = 457.3     # base
re = 232.0
rf = 112.0

# trigonometric constants
sqrt3 = sqrt(3.0)
sin120 = sqrt3/2.0
cos120 = -0.5
tan60 = sqrt3
sin30 = 0.5
tan30 = 1/sqrt3

dtr = pi/180.0
t = (f-e)*tan30/2

# forward kinematics: (theta1, theta2, theta3) -> (x0, y0, z0)
# returned status: 0=OK, -1=non-existing position
def delta_calcForward(theta1, theta2, theta3) :

	theta1 *= dtr
	theta2 *= dtr
	theta3 *= dtr

	y1 = -(t + rf*cos(theta1))
	z1 = -rf*sin(theta1)

	y2 = (t + rf*cos(theta2))*sin30
	x2 = y2*tan60
	z2 = -rf*sin(theta2)

	y3 = (t + rf*cos(theta3))*sin30
	x3 = -y3*tan60
	z3 = -rf*sin(theta3)

	dnm = (y2-y1)*x3-(y3-y1)*x2

	w1 = y1*y1 + z1*z1
	w2 = x2*x2 + y2*y2 + z2*z2
	w3 = x3*x3 + y3*y3 + z3*z3

	# x = (a1*z + b1)/dnm
	a1 = (z2-z1)*(y3-y1)-(z3-z1)*(y2-y1)
	b1 = -((w2-w1)*(y3-y1)-(w3-w1)*(y2-y1))/2.0

	# y = (a2*z + b2)/dnm
	a2 = -(z2-z1)*x3+(z3-z1)*x2
	b2 = ((w2-w1)*x3 - (w3-w1)*x2)/2.0

	# a*z^2 + b*z + c = 0
	a = a1*a1 + a2*a2 + dnm*dnm
	b = 2*(a1*b1 + a2*(b2-y1*dnm) - z1*dnm*dnm)
	c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - re*re)

	# discriminant
	d = b*b - 4.0*a*c
	if d < 0:
		return (False, 0,0,0) # non-existing point

	z0 = -0.5*(b+sqrt(d))/a
	x0 = (a1*z0 + b1)/dnm
	y0 = (a2*z0 + b2)/dnm

	return (True, x0, y0, z0)


# inverse kinematics
# helper functions, calculates angle theta1 (for YZ-pane)
def delta_calcAngleYZ(x0, y0, z0) :

	y1 = -0.5 * 0.57735 * f # f/2 * tg 30
	y0 -= 0.5 * 0.57735 * e    # shift center to edge

	# z = a + b*y
	a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2*z0)
	b = (y1-y0)/z0

	# discriminant
	d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf)

	if d < 0:
		return (False, 0) # non-existing point

	yj = (y1 - a*b - sqrt(d))/(b*b + 1) # choosing outer point
	zj = a + b*yj

	theta = 180.0*atan(-zj/(y1 - yj))/pi + (180.0 if yj>y1 else 0.0)

	return (True, theta)



# inverse kinematics: (x0, y0, z0) -> (theta1, theta2, theta3)
# returned status: 0=OK, -1=non-existing position
def delta_calcInverse(x0, y0, z0) :

	theta1 = 0
	theta2 = 0
	theta3 = 0

	status, theta1 = delta_calcAngleYZ(x0, y0, z0)

	if status:
		status, theta2 = delta_calcAngleYZ(x0*cos120 + y0*sin120, y0*cos120-x0*sin120, z0)  # rotate coords to +120 deg
	if status:
		status, theta3 = delta_calcAngleYZ(x0*cos120 - y0*sin120, y0*cos120+x0*sin120, z0)  # rotate coords to -120 deg

	return (status, theta1, theta2, theta3)

theta_min = -60
theta_max = 60
theta_step = 10


data = []

for theta1 in range(theta_min, theta_max + theta_step, theta_step):
	for theta2 in range(theta_min, theta_max + theta_step, theta_step):
		for theta3 in range(theta_min, theta_max + theta_step, theta_step):
			xyz = delta_calcForward(theta1, theta2, theta3)[1:]
			data.append(xyz)

sorted_data = sorted(data, key=lambda d: d[2])


X = []
Y = []
Z = []

for d in sorted_data:
	X.append(d[0])
	Y.append(d[1])
	Z.append(d[2])


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z, s=4)

plt.show()



