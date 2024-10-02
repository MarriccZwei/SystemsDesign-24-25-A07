import numpy as np
from math import tan, cos, radians, sqrt
import json
import os
import pandas as pd

# Import maindata json file
maindata = json.load(open("Protocols/main.json"))

# Target DeltaCL when landing, with CL-max in clean configuration (1.6)
# TODO This has to be recalculated when CL-max values are here and thus when airfoil has been chosen

maxClCL = maindata["CLmaxClean"]
targetDeltaCL = maindata["UltimateCL"] - maxClCL
span = maindata["b"]
taper = maindata['tr']

# Flap deflection suggested in ADSEE II Lecture 3
deltaFlap = 40  # [deg]

# This value can be between 0.35 and 0.40 of the airfoil chord lenght
flapFactor = 0.38

deltaCl_slat = 0.3

aileron_span = 33.0 - 26.9



surface = maindata["S"]  # Total wing surface
sweepLE = maindata["sweepLE"]
sweepTE = maindata["sweepTE"]

cRoot = maindata["Cr"]  # [m]
cTip = maindata["Ct"]

# Calculates the AIRFOIL DeltaCl
def deltaCl(delta, factor):
    dcCf = 0.004*delta + 0.43
    deltaCl_flap = 1.3 * (1+factor*dcCf)
    return (deltaCl_flap)   # DCl for flaps


def radiusFuselageRef():
    aircraftDataExcelPath = os.path.join(os.getcwd(), 'aircraftReferenceData.xlsx')
    aircraftDataFrame = pd.read_excel(aircraftDataExcelPath)
    dList = aircraftDataFrame['Diameter'].tolist()
    dAverage = sum(dList)/len(dList)
    return dAverage/2


def flapSurface():
    # Used trigonometry and whatnot to find the chord where the aileron starts in order to calculate the TE Flap surface area
    m = (span/2) - r - aileron_span  
    a = tan(sweepTE) * span / 2
    b = tan(sweepLE) * m
    c = tan(sweepTE) * aileron_span

    c_aileron_begin = cRoot + a - b - c

    # Calculate the TE surface area
    SW_flap = (cRoot + c_aileron_begin) * m / 2
    return (SW_flap)


def Slat_surface(sweepTE, totalSurface, deltaCl_flap, surface, SW_flap):

    slat_surface = (((deltaCl(deltaFlap, flapFactor)+deltaCl_slat) * surface) / (0.9 * cos(sweepTE)) - SW_flap * deltaCl(deltaFlap, flapFactor)) / (deltaCl_slat)

    return slat_surface


def slat_span(slat_surface):
    a = (cRoot*(1-taper)) / (span/2)
    b = - (cRoot + a * (span/2) + cTip)
    c = cRoot*(span/2) + cTip*(span/2) - 2*slat_surface
    start_slat = (-b + sqrt(b**2 - 4*a*c)) / (2*a)
    return start_slat




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

deltaCl_flap = deltaCl(deltaFlap, flapFactor)
SW_flap = flapSurface()

print('Flap Surface: ', round(flapSurface(), 1), '[m^2]')
print('Slat Surface: ', round(Slat_surface(sweepTE, totalSurface, deltaCl_flap, surface, SW_flap), 1))
print('Flap Lenght Spanwise: ', round(y, 1), '[m]')
print('Delta Alpha Landing ', round(dAlphaLand, 1), '[deg]')
print('Delta Alpha Takeoff ', round(dAlphaTakeoff, 1), '[deg]')
print(slat_span(Slat_surface(sweepTE, totalSurface, deltaCl_flap, surface, SW_flap)))