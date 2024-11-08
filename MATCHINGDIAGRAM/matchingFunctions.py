import ISAGEO as ISA
import math
from General import Constants

def thrustLapse(altitude, mach, bypass, dT=0):
    GAMMA = 1.4
    SLpressure = ISA.pressure(0)
    SLtemp = ISA.temperature(0, dT)
    thetaBreak = Constants.THETABREAK #between 1.06 and 1.08, can be changed
    pressure = ISA.pressure(altitude)
    temperature = ISA.temperature(altitude, dT)
    totalTemp = temperature*(1+ (GAMMA-1)/2*mach**2)#total temperature accounting for transsonic effects
    totalPressure = pressure*(1+ (GAMMA-1)/2*mach**2)**(GAMMA/(GAMMA-1))#total pressure accounting for transsonic effects
    delta = totalPressure/SLpressure#useful constant
    theta = totalTemp/SLtemp#useful constant
    # print(theta)
    # print(delta)


    if theta <= thetaBreak:
        thrustlapse = delta*(1 - (0.43+0.014*bypass)*math.sqrt(mach) )

    if theta > thetaBreak:
        thrustlapse = delta*(1 - (0.43+0.014*bypass)*math.sqrt(mach) - 3*(theta - thetaBreak)/(1.5+mach))
    return thrustlapse

def crudeDragpolar(cleanE, cleanCd0, TODeflection, LADeflection, wingMounted):
    """DRAGPOLAR: ls[[cr],[cd],[tr],[td],[lr],[ld]]"""
    """Form: e(0), cd0(1)"""
    """cruise retracted(0)"""
    """cruise deployed(1)"""
    """takeoff retracted(2)"""
    """takeoff deployed(3)"""
    """landing retracted(4)"""
    """landing deployed(5)"""
    deltaCDLG = (0.0100+0.0250)/2 #between 0.01 and 0.025
    if wingMounted: a = 0.0026
    else: a = 0.0046

    cruiseRetracted = [cleanE, cleanCd0]
    cruiseDeployed = [cleanE, cleanCd0+deltaCDLG]
    takeoffRetracted = [cleanE+a*TODeflection, cleanCd0+0.0013*TODeflection]
    takeoffDeployed = [cleanE+a*TODeflection, cleanCd0+0.0013*TODeflection+deltaCDLG]
    landingRetracted = [cleanE+a*LADeflection, cleanCd0+0.0013*LADeflection]
    landingDeployed = [cleanE+a*LADeflection, cleanCd0+0.0013*LADeflection+deltaCDLG]

    return [cruiseRetracted, cruiseDeployed, takeoffRetracted, takeoffDeployed, landingRetracted, landingDeployed]

def pointFinder(constraints):
    values = []
    if constraints[0] < constraints[1]: WSmax = math.floor(constraints[0])
    else: WSmax = math.floor(constraints[1])
    for i, constraint in enumerate(constraints):
        if i < 2: continue
        else:
            values.append(constraint[WSmax-1])
    values.sort()
    return [WSmax, values[-1]]





