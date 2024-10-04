import numpy as np
from math import tan, cos, radians, sqrt, atan
import json
import os
import pandas as pd
from CruiseConditions import datcom_cLalpha
from stallConditions import maxCL

# Import maindata json file
maindata = json.load(open("Protocols/main.json"))

# Target DeltaCL when landing, with CL-max in clean configuration (1.6)
# TODO This has to be recalculated when CL-max values are here and thus when airfoil has been chosen

machLand = 0.2
machCruise = 0.82

maxClCL = maxCL(2.0, '64a210', machLand)
targetDeltaCL = maindata["UltimateCL"] - maxClCL
span = maindata["b"]
taper = maindata['tr']
S_wing = maindata["S"]
ar = maindata["AR"]

CLDesign = maindata["CLDesign"]
#alpha_trim = 5.2

# Flap deflection suggested in ADSEE II Lecture 3
# This value can be between 0.35 and 0.40 of the airfoil chord lenght
#deltaCl_slat = 0.3
#aileron_span = 33.0 - 26.9

deltaFlapLand = 40
deltaFlapTakeoff = 15   # [deg]
cfC = 0.25 #flapcord to main cord


sparLoc = 1-0.05-cfC

surface = maindata["S"]  # Total wing surface
sweepLE = maindata["sweepLE"]
sweepTE = maindata["sweepTE"]
sweepHalf = maindata["sweepC/2"]

cRoot = maindata["Cr"]  # [m]
cTip = maindata["Ct"]

# Calculates the AIRFOIL DeltaCl
def deltaCl(delta):
    if delta == 40: dcCf = 0.6
    else: dcCf = 0.48
    #dcCf = 0.6 #0.004*delta + 0.43
    #cprimeCf = 1/cfC + dcCf
    cprimeC = 1+dcCf*cfC
    deltaCl_flap = 1.3 * cprimeC
    return deltaCl_flap, cprimeC   # DCl for flaps


def radiusFuselageRef():
    aircraftDataExcelPath = os.path.join(os.getcwd(), 'aircraftReferenceData.xlsx')
    aircraftDataFrame = pd.read_excel(aircraftDataExcelPath)
    dList = aircraftDataFrame['Diameter'].tolist()
    dAverage = sum(dList)/len(dList)
    return dAverage/2

def chordSpanwise(y):
    c = cRoot-cRoot*(1-taper)*(y/(span*0.5))
    return c

def areaCalc(cb, ce, b):
    s = b*(cb+ce)*0.5
    return s

def deltaCL(s, dcl, angle):
    return 0.9*dcl*(s/surface)*cos(angle)

def sweepRelations(frac):
    s = atan(tan(sweepLE)-frac*(2*cRoot)/span *(1-taper))
    return s

sweepHinge = sweepRelations(sparLoc)

def partialSurface(a):
    area = (a*tan(sweepTE)+cRoot)*a-0.5*a**2*tan(sweepTE)-0.5*a**2*tan(sweepLE)
    return area

r = radiusFuselageRef()
#areaFus = areaCalc(cRoot, chordSpanwise(r), r*2)
areaFus = 2*partialSurface(r)

def calcflapdCL(y):
    #area = areaCalc(cRoot, chordSpanwise(y), y*2)
    area = 2*partialSurface(y)
    flappedArea = area-areaFus
    d = deltaCL(flappedArea, deltaCl(deltaFlapLand)[0], sweepHinge)
    return d

def calcY(ystart, yend, steps):
    ycur = ystart
    mindif = 100000
    while ycur < yend:
        d = calcflapdCL(ycur)
        dif = abs(targetDeltaCL-d)
        if dif < mindif:
            mindif = dif
            y = ycur
        ycur = ycur + steps
    return y

ymin = calcY(10, 30, 0.01)
yAileron = ymin #aileron_span = 33.0 - 26.9

#areaBeginAileron = areaCalc(cRoot, chordSpanwise(yAileron), yAileron*2)
#yAileron = 18.15
areaBeginAileron = 2*partialSurface(yAileron)
areaTEFlaps = areaBeginAileron-areaFus


DCLTEflaps = deltaCL(areaTEFlaps, deltaCl(deltaFlapLand)[0], sweepHinge)
DCLTEtakeoff = deltaCL(areaTEFlaps, deltaCl(deltaFlapTakeoff)[0], sweepHinge)

#print(DCLTEflaps/DCLTEtakeoff)



alphaZeroLift = 1.66

# cBEGIN = chordSpanwise(r)
# cEND = chordSpanwise(yAileron)
# trFlapped = cEND/cBEGIN
# meanCFlaps = 2/3 * cBEGIN*((1+trFlapped+trFlapped**2)/(1+trFlapped))


def deltaAlpha(deltaAirfoil, angle):
    dA = deltaAirfoil*(areaTEFlaps/S_wing)*cos(angle)
    return dA


def CLofCLEAN(alpha, mach):
    dCLdALPHA = np.pi*datcom_cLalpha(ar, mach, sweepHalf)/180
    cL = dCLdALPHA*(alpha+alphaZeroLift)
    maxCLCLEAN = maxCL(2.0, '64a210', mach)
    return cL, maxCLCLEAN

def CLofLAND(alpha):
    dCLdALPHACLEAN = np.pi*datcom_cLalpha(ar, machLand, sweepHalf)/180
    sPrimeS = 1+(areaTEFlaps/S_wing)*(deltaCl(deltaFlapLand)[1]-1)
    dCLdALPHAFLAPPED = dCLdALPHACLEAN*sPrimeS
    deltaAlphaLand = deltaAlpha(15, sweepHinge)
    cL = dCLdALPHAFLAPPED*(alpha+(alphaZeroLift+deltaAlphaLand))
    maxCLFLAPPED = maxCL(2.0, '64a210', machLand)+DCLTEflaps
    return cL, maxCLFLAPPED

def CLofTAKEOFF(alpha):
    dCLdALPHACLEAN = np.pi*datcom_cLalpha(ar, machLand, sweepHalf)/180
    sPrimeS = 1+(areaTEFlaps/S_wing)*(deltaCl(deltaFlapTakeoff)[1]-1)
    dCLdALPHAFLAPPED = dCLdALPHACLEAN*sPrimeS
    deltaAlphaTakeoff = deltaAlpha(10, sweepHinge)
    cL = dCLdALPHAFLAPPED*(alpha+(alphaZeroLift+deltaAlphaTakeoff))
    maxCLTAKEOFF = maxCL(2.0, '64a210', machLand)+DCLTEtakeoff
    return cL, maxCLTAKEOFF

#print(f"The area for TE flaps is: {areaTEFlaps}")
print(f"Max CL in landing config is: {CLofLAND(0)[1]}")
print(f"Max CL in takeoff config is: {CLofTAKEOFF(0)[1]}")
print(f"Max CL in clean config is: {CLofCLEAN(0, machCruise)[1]}")

cl = CLofCLEAN(0, machCruise)[0]
a = 0
while cl < CLDesign:
    a = a + 0.1
    cl = CLofCLEAN(a, machCruise)[0]
alpha_trim = a
print(f"CL design at alpha {a} = {cl}")
print(f"alpha design of plane = {a-alpha_trim}")




cl = CLofLAND(0)[0]
a = 0
while cl < 2.5:
    a = a + 0.1
    cl = CLofLAND(a)[0]
print(f"CL land at alpha {a} = {cl}")
print(f"alpha land/stall/CLMAX of plane = {a-alpha_trim}")

cl = CLofTAKEOFF(0)[0]
a = 0
while cl < 1.8:
    a = a + 0.1
    cl = CLofTAKEOFF(a)[0]
print(f"CL takeoff at alpha {a} = {cl}")
print(f"alpha takeoff/stall/CLMAX of plane = {a-alpha_trim}")

# for i in range(-3, 25):
#     print(f"CL at alpha: {i} = {CLofLAND(i)[0]}")

#print(CLofCLEAN(alpha_trim, machCruise))




# def flapSurface(coveredSurface):
#     # Used trigonometry and whatnot to find the chord where the aileron starts in order to calculate the TE Flap surface area
#     m = (span/2) - r - aileron_span  
#     a = tan(sweepTE) * span / 2
#     b = tan(sweepLE) * m
#     c = tan(sweepTE) * aileron_span

#     c_aileron_begin = cRoot + a - b - c

#     SW_flap = S_wing - coveredSurface - (cTip + cRoot - (cRoot*(1-taper)* (span/2 - aileron_span))/(span/2))*(aileron_span/2)

#     return (SW_flap)




# def Slat_surface(sweepTE, totalSurface, deltaCl_flap, surface, SW_flap):

#     slat_surface = (((deltaCl(deltaFlap, flapFactor)+deltaCl_slat) * surface) / (0.9 * cos(sweepTE)) - SW_flap * deltaCl(deltaFlap, flapFactor)) / (deltaCl_slat)

#     return slat_surface

# def slat_span(slat_surface):
#     a = (cRoot*(1-taper)) / (span/2)
#     b = - (cRoot + a * (span/2) + cTip)
#     c = cRoot*(span/2) + cTip*(span/2) - 2*slat_surface
#     start_slat = (-b + sqrt(b**2 - 4*a*c)) / (2*a)
#     return start_slat


# calculates covered area by fuselage and thus not useable

# coveredSurface = 2*(((cRoot-r*tan(sweepLE))*r)-0.5*r**2 * (tan(sweepTE)+tan(sweepLE)))
# totalSurface = flapSurface(coveredSurface) + coveredSurface
# ABC formula for calculation of spanwise position of flaps (they start at the root)
# a = tan(sweepTE)-0.5*tan(sweepTE)-0.5*tan(sweepLE)
# b = cRoot
# c = -0.5*totalSurface

# y = (-b+sqrt(b**2 -4*a*c))/(2*a)   # This is spanwise location at one side
# dAlphaLand = -15 * (flapSurface(coveredSurface)/surface)*cos(sweepTE)
# dAlphaTakeoff = -10 * (flapSurface(coveredSurface)/surface)*cos(sweepTE)

# deltaCl_flap = deltaCl(deltaFlap, flapFactor)
# SW_flap = flapSurface(coveredSurface)

# print('Flap Surface: ', round(flapSurface(coveredSurface), 1), '[m^2]')
# print('Slat Surface: ', round(Slat_surface(sweepTE, totalSurface, deltaCl_flap, surface, SW_flap), 1))
# print('Flap Lenght Spanwise: ', round(y, 1), '[m]')
# print('Delta Alpha Landing ', round(dAlphaLand, 1), '[deg]')
# print('Delta Alpha Takeoff ', round(dAlphaTakeoff, 1), '[deg]')
# print(slat_span(Slat_surface(sweepTE, totalSurface, deltaCl_flap, surface, SW_flap)))

# flapSurface2 = 2*(partialSurface(xAileron)-partialSurface(r))
# CLdecrease = deltaCL(flapSurface2, deltaCl(deltaFlap, flapFactor), sweepTE)



# print(r)
# print(flapSurface2)
# print(CLdecrease)
# print(targetDeltaCL)