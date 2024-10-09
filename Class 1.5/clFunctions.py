from General import Constants as var
from math import sqrt
def clDesign(wingLoading, weightFuel, wingArea):
    rho = ISA.density(cruiseAltitude)
    temp = ISA.temperature(cruiseAltitude)
    vSound = sqrt(gamma*constantAir*temp)
    vCruise = cruiseMach*vSound
    q = 0.5*rho*vCruise**2
    w = (wingLoading*wingArea)-weightFuel
    averageLoading = 0.5*(2*(w/wingArea)+1.05*(weightFuel/wingArea))
    cl = 1.1*averageLoading*(1/q)
    return cl

