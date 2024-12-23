if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
from Deflections.wingbox import wingbox
import matplotlib.pyplot as plt
import numpy as np

def length(point1, point2) -> int:
    dx = point1[0]-point2[0]
    dy = point1[1]-point2[1]
    return np.sqrt(dx**2+dy**2)

chord = 8.14
spars = [0.3, 0.5]
G = 28*10**9
T = 1

 #from Left to right
thicknesses = [(2,1,2,1), (2,1,2,1), (2,1,2,1)] #From Left to right areas start bottom and then clockwise 

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

matrix = np.empty((0, len(spars)+2))
formula = []
for area in areas:
    formula.append(2*area)
formula.append(0)
formula = np.array(formula)
matrix = np.vstack([matrix, formula])

for i in range(len(spars)+1):
    areaFactor = 1/(2*areas[i])
    points = [transformedPoints[0+i], transformedPoints[1+i], transformedPoints[-2-i], transformedPoints[-1-i]]
    qi = 0
    for n, t in enumerate(thicknesses[i]):
        leng = length(points[n], points[(n+1)%4])
        qi += leng/(G*t*10**-3)
    qPrev = length(points[-1], points[0])/(G*thicknesses[i][-1]*10**-3)
    qNext = length(points[1], points[2])/(G*thicknesses[i][1]*10**-3)
    formula = np.zeros(len(spars)+2)
    formula[i] = qi
    if i == 0: 
        formula[i+1] = -qNext
        formula = formula*areaFactor
        formula[-1] = -1
        matrix = np.vstack([matrix, formula])
        continue
    elif i == len(spars): 
        formula[i-1] = -qPrev
        formula = formula*areaFactor
        formula[-1] = -1
        matrix = np.vstack([matrix, formula])
        continue
    formula[i+1] = -qNext
    formula[i-1] = -qPrev
    formula = formula*areaFactor
    formula[-1] = -1
    matrix = np.vstack([matrix, formula])


rhs = np.zeros((len(spars)+2,1))
rhs[0,0] = T

solution = np.linalg.solve(matrix,rhs)
J = T/(G*solution[-1])
print(J)
plt.plot(xCoor, yCoor, color='blue')
for i in range(len(spars)+1):
    plt.plot([xCoor[i], xCoor[-1-i]], [yCoor[i], yCoor[-1-i]], color = 'blue')
plt.show()


