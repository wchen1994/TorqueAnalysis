import App
import math
from matplotlib import pyplot as plt

w1 = 0.8
w2 = 1 - w1

foo = App.Simulate()
foo._plot = False

def CostFun(f1, f2):
    return w1*math.fabs(f1+f2)/2 + w2*math.fabs(f2-f1)

const_cw = 48
const_force=150
init_cost = 0

cost = []
if False:
    force_range = range(100,300)
    for sf in force_range:
        force = foo.sim(sf,const_cw)
        cost.append(CostFun(force[0], force[1]))

    plt.plot(force_range, cost)
    plt.ylabel("Cost")
    plt.show()
else:
    cw_range = range(30,60)
    for cw in cw_range:
        force = foo.sim(const_force,cw)
        cost.append(CostFun(force[0], force[1]))

    plt.plot(cw_range, cost)
    plt.ylabel("Cost")
    plt.show()
