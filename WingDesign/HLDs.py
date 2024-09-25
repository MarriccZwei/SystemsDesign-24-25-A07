import numpy as np
from math import tan, cos, radians, sqrt
import json
import os
import pandas as pd

# Import maindata json file
maindata = json.load(open("Protocols/main.json"))

# Target DeltaCL when landing, with CL-max in clean configuration (1.6)
targetDeltaCL = 0.9

# Flap deflection suggested in ADSEE II Lecture 3
deltaFlap = 50  # [deg]

# This value can be between 0.35 and 0.40 of the airfoil chord lenght
flapFactor = 0.35


surface = maindata["S"]  # Total wing surface
sweepLE = radians(maindata["sweepLE"])
sweepTE = radians(maindata["sweepTE"])

cRoot = maindata["Cr"]  # [m]

# Calculates the AIRFOIL DeltaCl
def deltaCl(delta, factor):
    dcCf = 0.01*delta + 0.4

    return 1.6 * (1+factor*dcCf)

# Calculates the required flap surface. ATTENTION: Flap surface is not the area of the flaps itself! See ADSEE II Lecture 3 slides
def flapSurface():
    return ((targetDeltaCL*surface)/(0.9*deltaCl(deltaFlap, flapFactor)*cos(sweepTE)))

def radiusFuselageRef():
    aircraftDataExcelPath = os.path.join(os.getcwd(), 'aircraftReferenceData.xlsx')
    aircraftDataFrame = pd.read_excel(aircraftDataExcelPath)
    dList = aircraftDataFrame['Diameter'].tolist()
    dAverage = sum(dList)/len(dList)
    return dAverage/2


# calculates covered area by fuselage and thus not useable
r = radiusFuselageRef()
coveredSurface = 2*(((cRoot-r*tan(sweepLE))*r)-0.5*r**2 * (tan(sweepTE)+tan(sweepLE)))
totalSurface = flapSurface() + coveredSurface
# ABC formula for calculation of spanwise position of flaps (they start at the root)
a = tan(sweepTE)-0.5*tan(sweepTE)-0.5*tan(sweepLE)
b = cRoot
c = -0.5*totalSurface
y = (-b+sqrt(b**2 -4*a*c))/(2*a) #This is spanwise location at one side
dAlphaLand = -15 * (flapSurface()/surface)*cos(sweepTE)
dAlphaTakeoff = -10 * (flapSurface()/surface)*cos(sweepTE)


print('Flap Surface: ', round(flapSurface(), 1), '[m^2]')
print('Flap Lenght Spanwise: ', round(y, 1), '[m]')
print('Delta Alpha Landing ', round(dAlphaLand, 1), '[deg]')
print('Delta Alpha Takeoff ', round(dAlphaTakeoff, 1), '[deg]')





