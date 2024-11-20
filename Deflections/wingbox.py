import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

FRONTSPARFRAC = 0.2
BACKSPARFRAC = 0.6

def readCSVFile(name) -> pd.DataFrame:
    path = os.path.join(os.getcwd(), name)
    df = pd.read_csv(path)
    return df

def sparHeight(upperCoords, lowerCoords, sparLoc) -> list:
    interpUpper = interp1d(upperCoords[0], upperCoords[1], bounds_error=False, fill_value="extrapolate")
    interpLower = interp1d(lowerCoords[0], lowerCoords[1], bounds_error=False, fill_value="extrapolate")
    coords = [[sparLoc, sparLoc], [float(interpUpper(sparLoc)), float(interpLower(sparLoc))]]
    return coords

def wingbox(chord: float, sparLocs: list = None, plot: bool = False) -> tuple[list, list]: #Returns in flipped coordinate axis
    #data is for chord of 0.1m MAC 8.17m
    spars = [FRONTSPARFRAC, BACKSPARFRAC]
    if sparLocs != None: spars.extend(sparLocs)

    scaleFactor = chord/0.1/1000

    frontSpar = FRONTSPARFRAC*chord #c frac
    backSpar = BACKSPARFRAC*chord #c frac

    df = readCSVFile('naca64a210-il.csv')
    xCoor = np.array(df['X(mm)'].to_list())*scaleFactor
    yCoor = np.array(df['Y(mm)'].to_list())*scaleFactor
    xcCoor = np.array(df['XC(mm)'].to_list())*scaleFactor
    ycCoor = np.array(df['YC(mm)'].to_list())*scaleFactor

    yUpperCoor = []
    yLowerCoor = [0]
    xUpperCoor = []
    xLowerCoor = [0]

    for i, coor in enumerate(yCoor):
        if coor >= 0: 
            yUpperCoor.append(coor)
            xUpperCoor.append(xCoor[i])
        else:
            yLowerCoor.append(coor)
            xLowerCoor.append(xCoor[i])

    yUpperCoor.append(0)
    xUpperCoor.append(0)

    upperCoords = [xUpperCoor, yUpperCoor]
    lowerCoords = [xLowerCoor, yLowerCoor]

    interpUpper = interp1d(upperCoords[0], upperCoords[1], bounds_error=False, fill_value="extrapolate")
    interpLower = interp1d(lowerCoords[0], lowerCoords[1], bounds_error=False, fill_value="extrapolate")

    baseUpperWingboxCoords = [[frontSpar, backSpar], [float(interpUpper(frontSpar)), float(interpUpper(backSpar))]]
    baseLowerWingboxCoords = [[frontSpar, backSpar], [float(interpLower(frontSpar)), float(interpLower(backSpar))]]

    upperWingBoxCoords = [[],[]]
    lowerWingBoxCoords = [[],[]]

    for spar in spars:
        loc = spar*chord
        point = sparHeight(baseUpperWingboxCoords, baseLowerWingboxCoords, loc)
        upperWingBoxCoords[0].append(loc)
        lowerWingBoxCoords[0].append(loc)
        upperWingBoxCoords[1].append(point[1][0])
        lowerWingBoxCoords[1].append(point[1][1])
        if plot: plt.plot(point[0], point[1], color='blue')


    if plot:
        plt.plot(xUpperCoor, yUpperCoor, color='red')
        plt.plot(xLowerCoor, yLowerCoor, color='red')
        plt.plot(xcCoor, ycCoor, color='black')

        plt.plot(upperWingBoxCoords[0], upperWingBoxCoords[1], color='blue')
        plt.plot(lowerWingBoxCoords[0], lowerWingBoxCoords[1], color='blue')

        plt.axis('equal')
        plt.grid(True)
        #plt.show()
    return upperWingBoxCoords, lowerWingBoxCoords

if __name__ == '__main__':
    print(wingbox(8.14))