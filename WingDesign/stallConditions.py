from math import cos, sin, tan, radians, degrees
import HLDs
import json
def maxCL(clmax2d, airfoil='63215', mach = 0.0):
    mainData = json.load(open("Protocols/main.json"))
    x = mainData["sweepLE"]
    tc = int(airfoil[-2:-1])/100
    sharpness = 1.4
    
    if str(airfoil)[1] == '1':
        sharpness = 27.3 * tc
    elif str(airfoil)[1] == '2':
        sharpness = 25.3 * tc
    elif str(airfoil)[1] == '3':
        sharpness = 23.3 * tc
    elif str(airfoil)[1] == '4':
        sharpness = 21.3 * tc
    elif str(airfoil)[1] == '5':
        sharpness = 19.3 * tc

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

    sweepTE = mainData["sweepTE"]
    S = mainData["S"]
    flapFactor = HLDs.flapFactor
    flapSurface = HLDs.flapSurface()
    cPrimeC = 1 + 0.875*flapFactor
    delta = 1.6 * cPrimeC 
    deltaCLmax = 0.9 * delta * flapSurface* cos(sweepTE) / S
    CLmaxLand = (maxCLtrue + deltaCLmax)
    
    cPrimeC = 1 + 0.58*flapFactor
    delta = 1.6 * cPrimeC 
    deltaCLmax = 0.9 * delta * flapSurface * cos(sweepTE) / S
    CLmaxTO = (maxCLtrue + deltaCLmax)

    return maxCLtrue, CLmaxTO, CLmaxLand

def stallAlpha(airfoil, alphaZero, clmax2d, mach = 0.0):
    mainData = json.load(open("Protocols/main.json"))
    LEsweep = mainData["sweepLE"]
    tc = int(airfoil[-2:-1])/100
    if str(airfoil)[1] == '4':
        sharpness = 19.3 * tc
    elif str(airfoil)[1] == '5':
        sharpness = 21.3 * tc
    
    if sharpness <= 1.6:
        deltaAlphaCL = (-1*10**-5)*LEsweep**3 + 0.004*LEsweep**2 - 0.0006*LEsweep + 1.781
    elif sharpness <2.5:
        deltaAlphaCL = (3*10**-6)*LEsweep**3 + 0.0009*LEsweep**2 + 0.1023*LEsweep - 0.0857
    elif sharpness < 3.5:
        deltaAlphaCL = (-6*10**-6)*LEsweep**3 + 0.0014*LEsweep**2 + 0.0303*LEsweep + 1.1905
    elif sharpness >= 3.5:
        deltaAlphaCL = (-1*10**-5)*LEsweep**3 + 0.0018*LEsweep**2 -0.0399*LEsweep + 2.2095
    
    clmax = maxCL(airfoil, LEsweep, clmax2d, mach)

    clAlpha = 0.08 #TODO change

    alphaStall = clmax/clAlpha + alphaZero + deltaAlphaCL

    return alphaStall