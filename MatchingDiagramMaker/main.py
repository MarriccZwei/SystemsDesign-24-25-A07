#here the matching diagram will be created based the given constraints
import matplotlib.pyplot as plt
import numpy as np
import pointFinder
import constraints
import refAcData
import ClimbRate
import maxFunctionFinder

WSmax = 10000
TWmax = 1
WSres = 1000

#Finding & marking points where constraints cross
crossOverEvents = maxFunctionFinder.maxFunctionFinder()
for point in crossOverEvents:
    print(point)
    print(point[1], point[2], point[0]-100, point[0]+100)
    #pointFinder.pointFinder(point[1], point[2], point[0]-100, point[0]+100)

#intersection with stall speed and landing distance constraints, may break
#pointFinder.pointFinder(crossOverEvents[-1][2], 0, crossOverEvents[-1][0]-100)
pointFinder.pointFinder(crossOverEvents[-1][2], 7, crossOverEvents[-1][0]-100)

WSaxis = np.linspace(0, WSmax, WSres+1)
plt.axis((0, WSmax, 0, TWmax))

# 0 Stall - Vert
# 1 Climb gradient I
# 2 Climb gradient II: Electric Boogaloo
# 3 Climb gradient III: Revenge of the CLmax
# 4 Climb gradient IV: The Climb Rate Strikes Back
# 5 Climb gradient V: Climbier Gradients
# 6 TO dist
# 7  Land dist - Vert
# 8 Cruise speed
# 9 Climb rate

#generating constraints
i=0
for constraint in constraints.constraints: 
    plt.plot(*constraint(WSaxis),label=constraints.constraintNames[i])
    i=i+1
plt.legend()
#input refrence aircraft data loading points
loadingPointsList = refAcData.generateLoadingPoints()
for i, point in enumerate(loadingPointsList):
    plt.plot(point[0], point[1], 'r+')
    plt.text(point[0] + 30, point[1] + 0.005, i+1) #Hard coded numbers are offset of labels.
    plt.xlabel("Wing Loading, [N/m^2]")
    plt.ylabel("Thrust-Weight Ratio, [-]")

plt.show()