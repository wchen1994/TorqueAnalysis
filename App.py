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
angles = range(90)
for angle in angles:
    torq_dis.append(COM.compute_torque(com, angle) / 1000.0)
print "Max torque: ", math.sqrt(com.x ** 2 + com.y ** 2) * 9.807 * com.m / 1000

# Calculate distance and force required vs tilt angle to withstand the torque
struts = Struts.Struts([40,-500], [0,-1000])
forces = []
distances = []
for idx in range(len(angles)):
    struts.tilt(angles[idx])
    forces.append(struts.t2f(torq_dis[idx]))
    distances.append(struts.distance_extend())

# Plot
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)

ax0.plot(angles, torq_dis)
ax0.set_xlabel("Tilt (degree)")
ax0.set_ylabel("Torque (Nm)")

ax1.plot(angles, forces)
ax1.set_xlabel("Tilt (degree)")
ax1.set_ylabel("Force required (N)")

ax2.plot(angles, distances)
ax2.set_xlabel("Tilt (degree)")
ax2.set_ylabel("distance (mm)")


plt.show()
