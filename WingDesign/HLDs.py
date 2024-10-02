import numpy as np
from math import tan, cos, radians, sqrt
import json
import os
import pandas as pd

# Import maindata json file
maindata = json.load(open("Protocols/main.json"))

# Target DeltaCL when landing, with CL-max in clean configuration (1.6)
# TODO This has to be recalculated when CL-max values are here and thus when airfoil has been chosen
maxClTO = maindata["CLmaxTO"]
maxClLA = maindata["CLmaxLand"]
maxClCL = maindata["CLmaxClean"]
targetDeltaCL = maxClLA - maxClCL
span = maindata["b"]

# Flap deflection suggested in ADSEE II Lecture 3
deltaFlap = 40  # [deg]

# This value can be between 0.35 and 0.40 of the airfoil chord lenght
flapFactor = 0.38

deltaCl_slat = 0.3

aileron_span = 33.0 - 28.067



surface = maindata["S"]  # Total wing surface
sweepLE = maindata["sweepLE"]
sweepTE = maindata["sweepTE"]

cRoot = maindata["Cr"]  # [m]

# Calculates the AIRFOIL DeltaCl
def deltaCl(delta, factor):
    dcCf = 0.004*delta + 0.43

    return (1.3 * (1+factor*dcCf))   # DCl for flaps


# Calculates the required flap and slat surface. ATTENTION: Flap surface is not the area of the flaps itself! See ADSEE II Lecture 3 slides
def flapSurface():
    return (((targetDeltaCL - DCL_Slats())*surface)/(0.9*deltaCl(deltaFlap, flapFactor)*cos(sweepTE)))


def radiusFuselageRef():
    aircraftDataExcelPath = os.path.join(os.getcwd(), 'aircraftReferenceData.xlsx')
    aircraftDataFrame = pd.read_excel(aircraftDataExcelPath)
    dList = aircraftDataFrame['Diameter'].tolist()
    dAverage = sum(dList)/len(dList)
    return dAverage/2

def Slat_surface(sweepTE, totalSurface, deltaCl(deltaFlap, flapFactor), surface):

    # Used trigonometry and whatnot to find the chord where the aileron starts in order to calculate the TE Flap surface area
    m = (b/2) - r - aileron_span  
    a = tan(sweepTE) * span / 2
    b = tan(sweepLE) * m
    c = tan(sweepTE) * aileron_span

    c_aileron_begin = cRoot + a - b - c

    # Calculate the TE surface area
    SW_flap = (cRoot + c_aileron_begin) * m / 2

    slat_surface = (((deltaCl+deltaCl_slat) * surface) / (0.9 * cos(sweepTE)) - SW_flap * deltaCl) / (deltaCl_slat)

    return slat_surface

def slat_span(slat_surface):
    




# calculates covered area by fuselage and thus not useable
r = radiusFuselageRef()
coveredSurface = 2*(((cRoot-r*tan(sweepLE))*r)-0.5*r**2 * (tan(sweepTE)+tan(sweepLE)))
totalSurface = flapSurface() + coveredSurface
# ABC formula for calculation of spanwise position of flaps (they start at the root)
a = tan(sweepTE)-0.5*tan(sweepTE)-0.5*tan(sweepLE)
b = cRoot
c = -0.5*totalSurface

y = (-b+sqrt(b**2 -4*a*c))/(2*a)   # This is spanwise location at one side
dAlphaLand = -15 * (flapSurface()/surface)*cos(sweepTE)
dAlphaTakeoff = -10 * (flapSurface()/surface)*cos(sweepTE)


print('Flap Surface: ', round(flapSurface(), 1), '[m^2]')
print('Slat Surface: ', round(SwSlats_to_S*surface, 1))
print('Flap Lenght Spanwise: ', round(y, 1), '[m]')
print('Delta Alpha Landing ', round(dAlphaLand, 1), '[deg]')
print('Delta Alpha Takeoff ', round(dAlphaTakeoff, 1), '[deg]')