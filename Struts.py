import math
from matplotlib import pyplot as plt

class Struts():
    def __init__(self, point_att, point_sat):
        self._pt_att = point_att
        self._pt_sat = point_sat
        self._tilt = 0

    def tilt(self, angle):
        self._tilt = angle

    def get_att(self):
        point = self._pt_att
        hypotenuse = math.sqrt(point[0] ** 2 + point[1] ** 2)
        adjancent = point[0]
        opposite = point[1]
        cos = adjancent / hypotenuse
        sin = opposite / hypotenuse
        tilt = math.pi * self._tilt / 180.0
        new_point = [None, None]
        new_point[0] = hypotenuse * (cos * math.cos(tilt) + sin * math.sin(tilt))
        new_point[1] = hypotenuse * (sin * math.cos(tilt) - cos * math.sin(tilt))
        return new_point

    def distance_to_point(self):
        pt_att = self.get_att()
        x1, y1 = pt_att
        x2, y2 = self._pt_sat
        A = (y1 - y2)
        B = (x2 - x1)
        C = (y2*x1 - y1*x2)
        return math.fabs(C / math.sqrt(A ** 2 + B ** 2)) / 1000.0

    def distance_extend(self):
        pt_att = self.get_att()
        x1, y1 = pt_att
        x2, y2 = self._pt_sat
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def t2f(self, torque):
        """
        Torque to Force
        """
        return torque / float(self.distance_to_point())

    def f2t(self, force):
        return force * float(self.distance_to_point())
        

if __name__ == "__main__":
    struts = Struts([40,-500], [0,-1000])

    angles = range(360)
    forces = []
    torques = []
    for angle in angles:
        struts.tilt(angle)
        forces.append(struts.t2f(307))

    plt.plot(angles, forces)
    plt.show()
