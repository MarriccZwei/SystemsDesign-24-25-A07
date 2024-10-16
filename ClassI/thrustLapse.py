import ISA
import math
import numpy as np

def thrustLapse(altitude, mach, BYPASS):
    GAMMA = 1.4
    SLpressure = 101325
    SLtemp = 288.15
    thetaBreak = 1.07 #between 1.06 and 1.08, can be changed

    pressure = ISA.pressure(altitude)
    temperature = ISA.temperature(altitude)

    totalTemp = temperature*(1+ (GAMMA-1)/GAMMA*mach*mach)#total temperature accounting for transsonic effects
    totalPressure = pressure*(1+ (GAMMA-1)/GAMMA*mach*mach)**(GAMMA/(GAMMA-1))#total pressure accounting for transsonic effects
    delta = totalPressure/SLpressure#useful constant
    theta = totalTemp/SLtemp#useful constant

    #these calculations assume a BYPASS value between 5 and 15
    if theta <= thetaBreak:
        thrustlapse = delta*(1 - (0.43+0.014*BYPASS)*math.sqrt(mach) )

    if theta > thetaBreak:
        thrustlapse = delta*(1 - (0.43+0.014*BYPASS)*math.sqrt(mach) - 3*(theta - thetaBreak)/(1.5+mach))

    return(thrustlapse)

def thrustLapseNP(altitude, mach):
    lapseList = []
    for m in mach:
        lapseList.append(thrustLapse(altitude,m))
    return(np.array(lapseList))