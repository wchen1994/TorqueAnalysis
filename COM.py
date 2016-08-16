#!/usr/bin/python2
import sys
import math
from matplotlib import pyplot as plt

class Point():
    def __init__(self, x, y, m):
        self.x = float(x)
        self.y = float(y)
        self.m = float(m)
        self.angle = 0

    def __repr__(self):
        return "Point<%.3fkg, (%.3f, %.3f)>" %(self.m, self.x, self.y)

    def __str__(self):
        return "%.3f kg at (%.3f, %.3f)" %(self.m, self.x, self.y)

    def __add__(obj1, obj2):
        mass = obj1.m + obj2.m
        pos_x = (obj1.m * obj1.x + obj2.m * obj2.x) / mass
        pos_y = (obj1.m * obj1.y + obj2.m * obj2.y) / mass
        obj = Point(pos_x, pos_y, mass)
        return obj

    def __eq__(obj1, obj2):
        if obj1.x != obj2.x:
            return False
        if obj1.y != obj2.y:
            return False
        if obj1.m != obj2.m:
            return False
        return True

def load_points(filename):
    fp = open(filename, "r")
    if fp == None:
        exit(1)

    points = []
    for line in fp.readlines():
        line = line.strip()
        data = line.split(",")
        points.append(Point(float(data[0]), float(data[1]), float(data[2])))

    fp.close()
    return points

def compute_com(points):
    result = Point(0,0,0)
    for point in points:
        result += point
    return result

def compute_torque(point, tilt):
    hypotenuse = math.sqrt(point.x ** 2 + point.y ** 2)
    opposite = point.y
    adjancent = point.x
    cos = adjancent / hypotenuse
    sin = opposite / hypotenuse
    tilt = math.pi * tilt / 180.0
    new_cos = cos * math.cos(tilt) + sin * math.sin(tilt)
    return hypotenuse * new_cos * point.m * 9.807

if __name__ == "__main__":
    """
    take first argument as input file compute the center of mass
    """
    if len(sys.argv) == 2:
        points = load_points(sys.argv[1])
        com = compute_com(points)
        print "Center of mass: ", com

        torq_dis = []
        angles = range(90)
        for angle in angles:
            torq_dis.append(compute_torque(com, angle) / 1000.0)
        plt.plot(angles, torq_dis)
        plt.ylabel("Torque (Nm)")
        plt.xlabel("Tile (degree)")
        plt.show()

        print "Max torque: ", math.sqrt(com.x ** 2 + com.y ** 2) * 9.807 * com.m / 1000

    else:
        sys.stderr.write("[USAGE]\n./COM.py <inputfile>\n")
