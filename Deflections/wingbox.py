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

def mainSparHeight():
    

def plotWingbox():
#data is for chord of 0.1m MAC 8.17m
chord = 8.17
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

interpUpper = interp1d(xUpperCoor, yUpperCoor, bounds_error=False, fill_value="extrapolate")
interpLower = interp1d(xLowerCoor, yLowerCoor, bounds_error=False, fill_value="extrapolate")

yUpperFront = interpUpper(frontSpar)
yLowerFront = interpLower(frontSpar)

yUpperBack = interpUpper(backSpar)
yLowerBack = interpLower(backSpar)

frontSparHeight = yUpperFront-yLowerFront
backSparHeight = yUpperBack-yLowerBack

plt.plot(xUpperCoor, yUpperCoor, color='red')
plt.plot(xLowerCoor, yLowerCoor, color='red')
plt.plot(xcCoor, ycCoor, color='black')
plt.plot([frontSpar, frontSpar], [yUpperFront, yLowerFront], color='blue')
plt.plot([backSpar, backSpar], [yUpperBack, yLowerBack], color='blue')
plt.plot([backSpar, frontSpar], [yUpperBack, yUpperFront], color='blue')
plt.plot([backSpar, frontSpar], [yLowerBack, yLowerFront], color='blue')
plt.axis('equal')
plt.grid(True)
plt.show()