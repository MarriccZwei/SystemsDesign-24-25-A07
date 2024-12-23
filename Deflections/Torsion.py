if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
from Deflections.wingbox import wingbox
import matplotlib.pyplot as plt
from General import Constants as c
import numpy as np
import scipy.integrate as integrate
from scipy.interpolate import interp1d
from OOP.Planform import Planform
from Deflections import MoISpanwise as center

def length(point1: tuple, point2: tuple) -> int:
    dx = point1[0]-point2[0]
    dy = point1[1]-point2[1]
    return np.sqrt(dx**2+dy**2)

def calcJ(chord: float, thicknesses: list, centroid: tuple, spars: list = None, plot = False) -> int:
    #Thicknesses list from Leftmost area to right areas start bottom t and then counterclockwise
    if spars == None: spars = []
    G = c.G_MODULUS
    T = 1
    upperCoords, lowerCoords = wingbox(chord, plot=False, sparLocs=spars)
    xBar, yBar = centroid #(1.632, 0.35)
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
    if plot:
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
    if plot:
        plt.plot(xCoor, yCoor, color='blue')
        for i in range(len(spars)+1):
            plt.plot([xCoor[i], xCoor[-1-i]], [yCoor[i], yCoor[-1-i]], color = 'blue')
        plt.show()
    return J

def deltatwist(planform: Planform, thicknesses: list, range: tuple, torque: list, zCoordsForce: list, 
          xBars: list, yBars: list, zCoordsCent: list, spars: list = None) -> float:
    G = c.G_MODULUS
    tFunc = interp1d(zCoordsForce, torque, bounds_error=False, fill_value=0)
    xfunc = interp1d(zCoordsCent, xBars, bounds_error=False, fill_value="extrapolate")
    yfunc = interp1d(zCoordsCent, yBars, bounds_error=False, fill_value="extrapolate")
    twist, error = integrate.quad(lambda z: tFunc(z)/(G*calcJ(planform.chord_spanwise(z/(planform.b/2)), thicknesses, (xfunc(z), yfunc(z)), spars)), range[0], range[1])
    return twist
 
def twist(planform: Planform, thicknesses: list, loc: float, torque: list, zCoordsForce: list, 
          xBars: list, yBars: list, zCoordsCent: list, cutoff: float = None, spars: list = None) -> float:
    if cutoff != None and loc > cutoff:
        left = (0, cutoff)
        right = (cutoff, loc)
        deltaBase = deltatwist(planform, thicknesses, left, torque, zCoordsForce, xBars, yBars, zCoordsCent, spars)
        thicknesses = [(thicknesses[0][0], thicknesses[-1][1], thicknesses[0][2], thicknesses[0][3])]
        deltaRight = deltatwist(planform, thicknesses, right, torque, zCoordsForce, xBars, yBars, zCoordsCent)
        return deltaBase+deltaRight
    delta = deltatwist(planform, thicknesses, (0, loc), torque, zCoordsForce, xBars, yBars, zCoordsCent, spars)
    return delta

def jGraph(planform: Planform, thicknesses: list, xBars: list, yBars: list, zCoordsCent: list, zAxis: list, spars: list = None) -> list:
    xfunc = interp1d(zCoordsCent, xBars, bounds_error=False, fill_value="extrapolate")
    yfunc = interp1d(zCoordsCent, yBars, bounds_error=False, fill_value="extrapolate")
    jlist = []
    for z in zAxis:
        chord = planform.chord_spanwise(z/(planform.b/2))
        j = calcJ(chord, thicknesses, (xfunc(z), yfunc(z)), spars)
        jlist.append(j)
    return jlist

def graphs(planform: Planform, thicknesses: list, torque: list, zCoordsForce: list, 
           xBars: list, yBars: list, zCoordsCent: list, zAxis: list, cutoff: float = None, spars: list = None) -> list:
    twistList = []
    jList =[]
    xfunc = interp1d(zCoordsCent, xBars, bounds_error=False, fill_value="extrapolate")
    yfunc = interp1d(zCoordsCent, yBars, bounds_error=False, fill_value="extrapolate")
    for z in zAxis:
        chord = planform.chord_spanwise(z/(planform.b/2))
        j = calcJ(chord, thicknesses, (xfunc(z), yfunc(z)), spars)
        theta = twist(planform, thicknesses, z, torque, zCoordsForce, xBars, yBars, zCoordsCent, cutoff, spars)
        jList.append(j)
        twistList.append(np.rad2deg(theta))
    return jList, twistList


if __name__ == '__main__':
    #wing = Planform(251, 9.87,0.1,28.5,2.15,False)
    #spars = [0.3]
    #thicknessesExtra = [(20,10,20,10), (20,10,20,10), (20,10,20,10)]
    #thicknesses = [(20,10,20,10)]
    #cent = (1.632, 0.35)
    # loc = 10
    # chord = wing.chord_spanwise(loc/(wing.b/2))
    # xfunc = interp1d(center.z_values, center.x_bar_values, bounds_error=False, fill_value="extrapolate")
    # yfunc = interp1d(center.z_values, center.y_bar_values, bounds_error=False, fill_value="extrapolate")
    # J = calcJ(chord, thicknesses, (xfunc(loc), yfunc(loc)), spars, True)
    #deltatheta = deltatwist(wing, thicknessesExtra, (0, 10), [1000, 0], [0, 30], center.x_bar_values, center.y_bar_values, center.z_values, spars)
    #print(deltatheta)
    #zAxis = np.linspace(0, wing.b/2)
    #jsE, thetasE = graphs(wing, thicknessesExtra,[200000, 20000], [10, 15], center.x_bar_values, center.y_bar_values, center.z_values, zAxis,12.5, spars=spars)
    #js, thetas = graphs(wing, thicknesses,[200000, 20000], [10, 15], center.x_bar_values, center.y_bar_values, center.z_values, zAxis) 
    # fig, (ax1, ax2, ax3) = plt.subplots(3)
    # fig.suptitle('Torsion Graphs')
    # ax1.plot(zAxis, thetasE)
    # ax2.plot(zAxis, thetas)
    # ax3.plot(zAxis, abs(np.array(thetasE))-abs(np.array(thetas)))
    # plt.show()
    #print(f"Total twist: {twist(wing, thicknessesExtra, wing.b/2, [200000, 20000], [10, 15], center.x_bar_values, center.y_bar_values, center.z_values, 12.5, spars)}")
    #print(f"Total twist: {twist(wing, thicknesses, wing.b/2, [200000, 20000], [10, 15], center.x_bar_values, center.y_bar_values, center.z_values)}")
    #print(f"delta twist: {deltatwist(wing, thicknessesExtra, (0, 10), [200000, 20000], [10, 15], center.x_bar_values, center.y_bar_values, center.z_values,spars)}")
    #print(f"delta twist: {deltatwist(wing, thicknesses, (0,10), [200000, 20000], [10, 15], center.x_bar_values, center.y_bar_values, center.z_values)}")
    #print(calcJ(8, thicknessesExtra, cent, spars))
    #print(calcJ(8, thicknesses, cent))
    wing = Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    zAxis = np.linspace(0, wing.b/2)
    """Design one"""
    thicknesses = [(7,7,7,7)]
    spars = None
    cutoff = None
    Js, thetas = graphs(wing, thicknesses,[200000, 20000], [10, 15], center.x_bar_values, center.y_bar_values, center.z_values, zAxis, cutoff, spars)

