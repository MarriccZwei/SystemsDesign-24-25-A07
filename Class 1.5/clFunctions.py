from math import sqrt
import General.Constants as c


def clDesign(wingLoading, weightFuel, wingArea):
    rho = c.CRUISEDENSITY
    vCruise = c.CRUISEVELOCITY
    q = 0.5*rho*vCruise**2
    w = (wingLoading*wingArea)-weightFuel
    averageLoading = 0.5*(2*(w/wingArea)+1.05*(weightFuel/wingArea))
    cl = 1.1*averageLoading*(1/q)
    return cl

def dCLdAlpha(AR, mach, sweepQuarter):
    return

print(c.CRUISEVELOCITY)
