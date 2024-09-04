#here the matching diagram will be created based the given constraints

import matplotlib.pyplot as plt
import numpy as np

import constraints
import refAcData

WSmax = 100
TWmax = 1
WSres = 1000

WSaxis = np.linspace(0, WSmax, WSres+1)
plt.axis((0, WSmax, 0, TWmax))

#generating constraints
for constraint in constraints.constraints: 
    plt.plot(*constraint(WSaxis))

#input refrence aircraft data loading points
loadingPointsList = refAcData.generateLoadingPoints()
for point in loadingPointsList:
    plt.plot(point[0], point[1], label=point[2])

plt.show()