if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

from math import sqrt, pi, tan
from General import Constants as c
from OOP.Planform import Planform
#from OOP.HLDs import HLDs


def clDesign(wingLoading, weightFuel, planform: Planform):
    rho = c.CRUISEDENSITY
    vCruise = c.CRUISEVELOCITY
    q = 0.5*rho*vCruise**2
    w = (wingLoading*planform.S)-weightFuel
    averageLoading = 0.5*(2*(w/planform.S)+1.05*(weightFuel/planform.S))
    cl = 1.1*averageLoading*(1/q)
    return cl

def dCLdAlpha(mach, planform: Planform, radians=False):
    beta = sqrt(1-mach**2)
    AR = planform.AR
    sweepC4 = planform.sweepC4
    sqrtPart = sqrt(4+(1+(tan(sweepC4)/beta)**2)*(AR*beta/0.95)**2)
    clAlpha = 2*pi*AR/(2+sqrtPart)
    if radians: return clAlpha
    else: return pi/180*clAlpha


def maxCL(clmax2d, planform: Planform, mach = 0.0):
    x = planform.sweepLE
    tc = c.THICKNESSTOCHORD
    sharpness = 21.3*tc

    if sharpness <= 1.5: #line 1.4-
        cl_cl = (-3 * 10**(-8) * x**3) + (8 * 10**(-5) * x*x) + 0.0019 * x + 0.9
    
    elif sharpness <= 1.7: #line 1.6
        cl_cl = (-7 * 10**(-7) * x**3) + (0.0001 * x*x) + 0.0009 * x + 0.9

    elif sharpness <= 1.9: #line 1.8
        cl_cl = (-4 * 10**(-10) * x**3) + (0.00002 * x*x) + 0.0012 * x + 0.9
    
    elif sharpness <= 2.1: #line 2.0
        cl_cl = (-3 * 10**(-6) * x*x) - (0.0004 * x) + 0.9
    
    elif sharpness <= 2.3: #line 2.2
        cl_cl = (-2 * 10**(-7) * x**3) - (6 * 10**(-5) * x*x) + 0.00006 * x + 0.9

    elif sharpness < 2.5: #line 2.4
        cl_cl = (-5 * 10**(-7) * x**3) - (2 * 10**(-5) * x*x) - 0.0017 * x + 0.9002

    elif sharpness >= 2.5: #line 2.5+
        cl_cl = (-2 * 10**(-6) * x**3) + (0.0001 * x*x) - 0.0048 * x + 0.9

    if mach <= 0.2:
        deltaCL = 0
    else:
        deltaCL = sharpness / 24 * 0.82

    maxCLtrue = cl_cl * clmax2d + deltaCL

    return maxCLtrue

