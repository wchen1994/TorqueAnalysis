import App
import math
from matplotlib import pyplot as plt

w1 = 0.00000001
w2 = 1 - w1

foo = App.Simulate()
foo._plot = False

def CostFun(f1, f2):
    return w1*math.fabs(f1+f2)/2 + w2*math.fabs(f2-f1)

init_cw = 15
init_cost = 0

cost = []
for sf in range(100, 400):
    force = foo.sim(sf,40)
    cost.append(CostFun(force[0], force[1]))

plt.plot(range(100,400), cost)
plt.show()

#for cw in range(1,40):
#    force = foo.sim(375,cw)
#    cost.append(CostFun(force[0], force[1]))
#
#plt.plot(range(1,40), cost)
#plt.show()
