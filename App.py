import COM
import Struts
import math
from matplotlib import pyplot as plt

class Simulate():
    def __init__(self):
        self._plot = True

    def sim(self, struts_force, counter_weight):
        # Load data and compute center of mass
        points = COM.load_points("data.csv")
        com = COM.compute_com(points)
        print "Center of mass: ", com

        # Calculate torque vs tilt angle
        torq_dis = []
        angles = range(0,80)
        for angle in angles:
            torq_dis.append(COM.compute_torque(com, angle) / 1000.0)

        # Add CounterWeight
        tmp = []
        counter_weight = COM.Point(-480,0,counter_weight)
        for idx in range(len(angles)):
            torq = COM.compute_torque(counter_weight, angles[idx]) / 1000.0
            tmp.append(torq)
            torq_dis[idx] += torq

        # Add two gas struts
        struts = Struts.Struts([260,-430], [30,-300])
        struts.set_force(struts_force)
        struts_dists = []
        struts_forces = [] # Forces required when there is only frame torque
        for idx in range(len(angles)):
            struts.tilt(angles[idx])
            struts_forces.append(struts.t2f(torq_dis[idx]))
            torq = struts.f2t(2 * struts.compute_force())
            torq_dis[idx] -= torq
            struts_dists.append(struts.distance_extend())

        # Calculate shaft force required vs tilt angle to withstand the torque
        shaft = Struts.Struts([-480,0], [0,-680])
        shaft_forces = []
        for idx in range(len(angles)):
            shaft.tilt(angles[idx])
            shaft_forces.append(shaft.t2f(torq_dis[idx]))

        # Log data
        print "Torque range from: ", min(torq_dis), "to", max(torq_dis)
        print "Force range from: ", min(shaft_forces), "to", max(shaft_forces)
        print "Distance range from: ", min(struts_dists), "to", max(struts_dists)

        # Plot
        if self._plot:
            fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)

            ax0.plot(angles, torq_dis)
            ax0.plot(angles, tmp)
            ax0.set_xlabel("Tilt (degree)")
            ax0.set_ylabel("Net Torque (Nm)")

            ax1.plot(angles, struts_dists)
            ax1.set_xlabel("Tilt (degree)")
            ax1.set_ylabel("Struts length (mm)")

            # plot the shaft force
            ax2.plot(angles, shaft_forces)
            ax2.set_xlabel("Tilt (degree)")
            ax2.set_ylabel("Shaft Force(N)")

            # plot the struts force when there is only frame torque
            #ax2.plot(angles, struts_forces)
            #ax2.set_xlabel("Tilt (degree)")
            #ax2.set_ylabel("Struts Force(N)")


            plt.show()
        return (min(shaft_forces), max(shaft_forces))

    def snap(self, angle, counter_weight):
        """
        calculate the properity in a angle and counter weight
        """
        # Load data and compute center of mass
        points = COM.load_points("data.csv")
        com = COM.compute_com(points)

        # compute torque
        torque = COM.compute_torque(com, angle) / 1000.0
        com_tilt = COM.compute_new_com(com, angle)
        
        # Add CounterMass
        counter_mass = COM.Point(-480, 0, counter_weight)
        torque_cw = COM.compute_torque(counter_mass, angle) / 1000.0
        torque += torque_cw

        # compute strut force
        struts = Struts.Struts([260,-430], [30,-300])
        struts.tilt(angle)
        attatch_point = struts.get_att()
        extend_length = struts.distance_extend()
        struts_force = struts.t2f(torque)

        return com_tilt, torque, attatch_point, extend_length, struts_force

if __name__ == '__main__':
    foo = Simulate()
    foo.sim(520, 26)
    #foo.sim(0, 0)

    #print foo.snap(80, 26)
