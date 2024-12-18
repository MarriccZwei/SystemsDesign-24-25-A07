if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
from OOP.Planform import Planform
import pandas as pd
from General import Constants as c
from General.generalFunctions import sparHeight, length
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import os 

class FlexBox():
    def __init__(self, planform:Planform, wingboxThicknesses: dict, position: float, midSpar: float):
        self.midSpar = midSpar
        self.chord = planform.chord_spanwise(position/(planform.b/2))
        self.position = position
        self.thicknesses = wingboxThicknesses

    @property
    def wingBoxCoords(self):
        path = os.path.join(os.getcwd(), 'naca64a210-il.csv')
        df = pd.read_csv(path)
        spars = [c.FRONTSPARFRAC, c.BACKSPARFRAC]
        if self.midSpar != None: spars.append(self.midSpar)
        chord = self.chord
        scaleFactor = chord/0.1/1000

        frontSpar = spars[0]*chord
        backSpar = spars[1]*chord

        xCoor = np.array(df['X(mm)'].to_list())*scaleFactor
        yCoor = np.array(df['Y(mm)'].to_list())*scaleFactor

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
        

        x0 = chord/4

        transFormedX = []
        transFormedY = []
        xWingBoxCoords = upperWingBoxCoords[0]+lowerWingBoxCoords[0]
        yWingBoxCoords = upperWingBoxCoords[1]+lowerWingBoxCoords[1]
        for x in xWingBoxCoords:
            xTrans = x-x0
            transFormedX.append(xTrans)
        for y in yWingBoxCoords:
            yTrans = -y
            transFormedY.append(yTrans)
        
        if self.midSpar != None:
            xElement = transFormedX.pop(2)
            transFormedX.insert(-1, xElement)
            yElement = transFormedY.pop(2)
            transFormedY.insert(-1, yElement)

        coordsList = list(zip(transFormedX, transFormedY))

        coordsDict = {
            'ft': coordsList[0],
            'rt': coordsList[1],
            'fb': coordsList[2],
            'rb': coordsList[3],
        }

        if self.midSpar != None:
            coordsDict['mt'] = coordsList[4]
            coordsDict['mb'] = coordsList[5]

        return coordsDict
    
    @property
    def lengths(self):
        coordsDict = self.wingBoxCoords
        lengthsDict = {
            'f': length(coordsDict['ft'], coordsDict['fb']),
            'r': length(coordsDict['rt'], coordsDict['rb']),
            't': length(coordsDict['ft'], coordsDict['rt']),
            'b': length(coordsDict['fb'], coordsDict['rb'])
        }
        if self.midSpar != None:
            lengthsDict['m'] = length(coordsDict['mt'], coordsDict['mb'])
            lengthsDict['ft'] = length(coordsDict['ft'], coordsDict['mt'])
            lengthsDict['rt'] = length(coordsDict['rt'], coordsDict['mt'])
            lengthsDict['fb'] = length(coordsDict['fb'], coordsDict['mb'])
            lengthsDict['rb'] = length(coordsDict['rb'], coordsDict['mb'])
        return lengthsDict
    
    @property
    def areas(self):
        lengths = self.lengths
        fArea = lengths['f']*thicknesses['f']
        rArea = lengths['r']*thicknesses['r']
        tArea = lengths['t']*thicknesses['t']
        bArea = lengths['b']*thicknesses['b']
        areaDict = {
            'f': fArea,
            'r': rArea,
            't': tArea,
            'b': bArea
        }
        if self.midSpar != None:
            areaDict['m'] = lengths['m']*thicknesses['m']
        return areaDict

    @property
    def centroidComponent(self):
        coordsDict = self.wingBoxCoords
        areasDict = self.areas
        xf = (coordsDict['ft'][0]+coordsDict['fb'][0])/2
        xr = (coordsDict['rt'][0]+coordsDict['rb'][0])/2
        xt = (coordsDict['ft'][0]+coordsDict['rt'][0])/2
        xb = (coordsDict['fb'][0]+coordsDict['rb'][0])/2
        productX = areasDict['f']*xf+areasDict['r']*xr+areasDict['t']*xt+areasDict['b']*xb

        yf = (coordsDict['ft'][1]+coordsDict['fb'][1])/2
        yr = (coordsDict['rt'][1]+coordsDict['rb'][1])/2
        yt = (coordsDict['ft'][1]+coordsDict['rt'][1])/2
        yb = (coordsDict['fb'][1]+coordsDict['rb'][1])/2
        productY = areasDict['f']*yf+areasDict['r']*yr+areasDict['t']*yt+areasDict['b']*yb

        area = areasDict['f']+areasDict['r']+areasDict['t']+areasDict['b']
        if self.midSpar != None:
            area += areasDict['m']
            xm = (coordsDict['mt'][0]+coordsDict['mb'][0])/2
            ym = (coordsDict['mt'][1]+coordsDict['mb'][1])/2
            productX += areasDict['m']*xm
            productY += areasDict['m']*ym
        
        x = productX/area
        y = productY/area
        return (x, y)
    
    def airfoilCoords(self):
        path = os.path.join(os.getcwd(), 'naca64a210-il.csv')
        df = pd.read_csv(path)
        chord = self.chord
        scaleFactor = chord/0.1/1000
        xCoor = np.array(df['X(mm)'].to_list())*scaleFactor
        yCoor = np.array(df['Y(mm)'].to_list())*scaleFactor
        x0 = chord/4
        transFormedX = []
        transFormedY = []
        for x in xCoor:
            xTrans = x-x0
            transFormedX.append(xTrans)
        for y in yCoor:
            yTrans = -y
            transFormedY.append(yTrans)
        coordsList = list(zip(transFormedX,transFormedY))
        return coordsList
    
    def plot(self):
        airfoilList = list(zip(*self.airfoilCoords()))
        wingBoxList = list(zip(*list(self.wingBoxCoords.values())))
        centroid = self.centroidComponent
        plt.plot(airfoilList[0], airfoilList[1], color = 'red')
        plt.scatter(wingBoxList[0], wingBoxList[1], color = 'black')
        plt.scatter(centroid[0], centroid[1])
        plt.axis('equal')
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.show()


    
    




if __name__ == '__main__':
    thicknesses = {
        'f': 0.001,
        'r': 0.001,
        't': 0.001,
        'b': 0.001,
        'm': 0.001
    }
    planform = Planform(251, 9.87,0.1,28.5,2.15,False)
    position = 15
    midSpar = 0.4
    wingBox = FlexBox(planform, thicknesses, position, midSpar)
    # print(wingBox.wingBoxCoords)
    # print(wingBox.lengths)
    # print(wingBox.centroidComponent)
    #wingBox.airfoilCoords()
    wingBox.plot()