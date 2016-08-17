import COM
import Struts
import math
from matplotlib import pyplot as plt

# Load data and compute center of mass
points = COM.load_points("data.csv")
com = COM.compute_com(points)
print "Center of mass: ", com

# Calculate torque vs tilt angle
torq_dis = []
angles = range(20,80)
for angle in angles:
    torq_dis.append(COM.compute_torque(com, angle) / 1000.0)

# Add two gas struts
struts = Struts.Struts([260,-430], [30,-300])
struts.set_force(300)
struts_dists = []
for idx in range(len(angles)):
    struts.tilt(angles[idx])
    torq = struts.f2t(2 * struts.compute_force())
    torq_dis[idx] -= torq
    struts_dists.append(struts.distance_extend())

# Add CounterWeight
counter_weight = COM.Point(-500,0,15)
for idx in range(len(angles)):
    torq = COM.compute_torque(counter_weight, angles[idx]) / 1000.0
    torq_dis[idx] += torq

# Calculate shaft force required vs tilt angle to withstand the torque
shaft = Struts.Struts([-500,0], [0,-800])
shaft_forces = []
for idx in range(len(angles)):
    shaft.tilt(angles[idx])
    shaft_forces.append(struts.t2f(torq_dis[idx]))

# Log data
print "Force range from: ", min(shaft_forces), "to", max(shaft_forces)
print "Distance range from: ", min(struts_dists), "to", max(struts_dists)

# Plot
if True:
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)

    ax0.plot(angles, torq_dis)
    ax0.set_xlabel("Tilt (degree)")
    ax0.set_ylabel("Net Torque (Nm)")

    ax1.plot(angles, struts_dists)
    ax1.set_xlabel("Tilt (degree)")
    ax1.set_ylabel("Struts length (mm)")

    ax2.plot(angles, shaft_forces)
    ax2.set_xlabel("Tilt (degree)")
    ax2.set_ylabel("Shaft Force(N)")

    plt.show()
