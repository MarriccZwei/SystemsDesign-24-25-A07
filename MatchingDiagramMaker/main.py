#here the matching diagram will be created based the given constraints

import matplotlib.pyplot as plt
import numpy as np

import constraints

WSmax = 10000
TWmax = 1
WSres = 1000

WSaxis = np.linspace(0, WSmax, WSres+1)
plt.axis((0, WSmax, 0, TWmax))

#generating constraints
for constraint in constraints.constraints: 
    plt.plot(*constraint(WSaxis))

plt.show()