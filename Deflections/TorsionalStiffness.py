if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
from Deflections.wingbox import wingbox
import matplotlib.pyplot as plt
import numpy as np

chord = 8.14
spars = [0.3, 0.4]
upperCoords, lowerCoords = wingbox(chord, plot=False, sparLocs=spars)
xBar, yBar = (1.632, 0.35)
origin = (upperCoords[0][0]+xBar, upperCoords[1][0]-yBar)
upperPoints = list(zip(upperCoords[0],upperCoords[1]))
lowerPoints = list(zip(lowerCoords[0],lowerCoords[1]))
points = upperPoints+lowerPoints
transformedPoints = []
for point in points:
    shiftedx = (point[0]- origin[0])*-1
    shiftedy = (point[1] - origin[1])*-1
    transformedPoints.append((shiftedx, shiftedy))
#transformedPoints = np.array(transformedPoints)
angles = [np.arctan2(p[1], p[0]) for p in transformedPoints]
angles, transformedPoints = zip(*sorted(zip(angles, transformedPoints)))
for i, point in enumerate(transformedPoints):
    plt.text(point[0], point[1], i+1)
xCoor, yCoor = zip(*transformedPoints)

areas = []
for i in range(len(spars)+1):
    points = [transformedPoints[0+i], transformedPoints[1+i], transformedPoints[-2-i], transformedPoints[-1-i]]
    sum = 0
    for n in range(len(points)):
        sum += points[n][0]*points[(n+1)%4][1]-points[n][1]*points[(n+1)%4][0]
    areas.append(0.5*sum)
    
print(areas)
plt.plot(xCoor, yCoor, color='blue')
for i in range(len(spars)+1):
    plt.plot([xCoor[i], xCoor[-1-i]], [yCoor[i], yCoor[-1-i]], color = 'blue')
plt.show()


