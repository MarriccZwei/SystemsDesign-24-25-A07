#here the matching diagram will be created based the given constraints

import matplotlib.pyplot as plt
import numpy as np

import constraints
import refAcData

WSmax = 10000
TWmax = 1
WSres = 1000

WSaxis = np.linspace(0, WSmax, WSres+1)
plt.axis((0, WSmax, 0, TWmax))

#0 - stallspeed
#1 - 5 - climb gradient
#6,7 - TO/Landing distance
#8 - cruise speed
#9 - climb speed
print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")


f = constraints.StallSpeedconstraint(WSaxis)
g = constraints.ClimbRate.ClimbRate(WSaxis)
h =[]
for i in range(1000):
    h.append(abs(f[0][i] - g[0][i]))
print(min(h))
print(h.index(min(h)))
intx = h.index(min(h))*WSmax/WSres
inty = constraints.CruiseSpeedConstraint(intx)[1]
plt.plot(intx, inty, '+r')
plt.text(intx + 30, inty + 0.005, "POINT")

#generating constraints
for constraint in constraints.constraints: 
    plt.plot(*constraint(WSaxis))

#input refrence aircraft data loading points
loadingPointsList = refAcData.generateLoadingPoints()
for i, point in enumerate(loadingPointsList):
    plt.plot(point[0], point[1], 'r+')
    plt.text(point[0] + 30, point[1] + 0.005, i+1) #Hard coded numbers are offset of labels.

plt.show()