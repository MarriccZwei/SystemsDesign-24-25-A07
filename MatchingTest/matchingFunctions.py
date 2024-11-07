from General import ISA
from General import Constants as c
import math

def thrustLapse(altitude, mach):
    GAMMA = c.GAMMA
    SLpressure = c.SLPRESSURE
    SLtemp = c.SLTEMPERATURE
    thetaBreak = 1.07 #between 1.06 and 1.08, can be changed

    pressure = ISA.pressure(altitude)
    temperature = ISA.temperature(altitude)

    totalTemp = temperature*(1+ (GAMMA-1)/2*mach**2)#total temperature accounting for transsonic effects
    totalPressure = pressure*(1+ (GAMMA-1)/2*mach**2)**(GAMMA/(GAMMA-1))#total pressure accounting for transsonic effects
    delta = totalPressure/SLpressure#useful constant
    theta = totalTemp/SLtemp#useful constant

    if theta <= thetaBreak:
        thrustlapse = delta*(1 - (0.43+0.014*12)*math.sqrt(mach) )

    if theta > thetaBreak:
        thrustlapse = delta*(1 - (0.43+0.014*12)*math.sqrt(mach) - 3*(theta - thetaBreak)/(1.5+mach))
    return thrustlapse

def crudeDragpolar(cleanE, cleanCd0, TODeflection, LADeflection):
    """DRAGPOLAR: ls[[cr],[cd],[tr],[td],[lr],[ld]]"""
    """Form: e(0), cd0(1)"""
    """cruise retracted(0)"""
    """cruise deployed(1)"""
    """takeoff retracted(2)"""
    """takeoff deployed(3)"""
    """landing retracted(4)"""
    """landing deployed(5)"""
    deltaCDLG = (0.0100+0.0250)/2

    cruiseRetracted = [cleanE, cleanCd0]
    cruiseDeployed = [cleanE, cleanCd0+deltaCDLG]
    takeoffRetracted = [cleanE+0.0026*TODeflection, cleanCd0+0.0013*TODeflection]
    takeoffDeployed = [cleanE+0.0026*TODeflection, cleanCd0+0.0013*TODeflection+deltaCDLG]
    landingRetracted = [cleanE+0.0026*LADeflection, cleanCd0+0.0013*LADeflection]
    landingDeployed = [cleanE+0.0026*LADeflection, cleanCd0+0.0013*LADeflection+deltaCDLG]

    return [cruiseRetracted, cruiseDeployed, takeoffRetracted, takeoffDeployed, landingRetracted, landingDeployed]


