if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

from General import Constants as c
import numpy as np
import matchingFunctions
from General import ISA
import matplotlib.pyplot as plt


def StallSpeedconstraint(betaLand, clMaxLand, vApp):
    val = 1/betaLand*c.SLDENSITY/2*(vApp/1.23)**2*clMaxLand
    return val

def LandingFieldLengthConstraint(betaLand, landingfield, clMaxLand):
    val = 1/betaLand*landingfield/c.CLFL*c.SLDENSITY/2*clMaxLand
    return val

def CruiseSpeedConstraint(WSaxis, cd0, ar, e, cruisalt, cruisemach, betacruise):
    alphaT = matchingFunctions.thrustLapse(cruisalt, cruisemach)
    rho = ISA.density(cruisalt)
    v = cruisemach*ISA.speedOfSound(cruisalt)
    val = betacruise/alphaT*((cd0*0.5*rho*v**2)/(betacruise*WSaxis)+(betacruise*WSaxis)/(np.pi*ar*e*0.5*rho*v**2))
    return val

def Climbrate(WSaxis, ar, e, cd0, c, rateAlt, betaCruise):
    rho = ISA.density(rateAlt)
    Cl = np.sqrt(cd0*np.pi*ar*e)
    v = np.sqrt(betaCruise*WSaxis*2/rho*1/Cl)
    m = v/ISA.speedOfSound(rateAlt)
    alphaT = matchingFunctions.thrustLapse(rateAlt, m)
    val = betaCruise/alphaT*(np.sqrt(c**2/(betaCruise*WSaxis)*rho/2*Cl)+2*np.sqrt(cd0/(np.pi*ar*e)))
    return val

def Climbgradient(WSaxis, ar, e, cd0, beta, trustFrac, grad):
    Cl = (cd0*np.pi*ar*e)**0.5
    v = (beta*WSaxis*2/c.SLDENSITY*1/Cl)**0.5
    m = v/ISA.speedOfSound(0)   
    alphaT=matchingFunctions.thrustLapse(0,m)
    val = 1/trustFrac*beta/alphaT*(grad+2*(cd0/(np.pi*ar*e))**0.5)
    return val

def TakeOffFieldLengthConstraint(WSaxis, ar, e, trustfrac, takeoffdis, takeoffCL):
    cl2 = (1/1.13)**2*takeoffCL
    v2 = np.sqrt(WSaxis*2/c.SLDENSITY*1/cl2)
    m = v2/ISA.speedOfSound(0)
    alphaT=matchingFunctions.thrustLapse(0,m)
    val = 1.15*alphaT*np.sqrt(1/trustfrac*WSaxis/(takeoffdis*0.85*c.SLDENSITY*c.G*np.pi*ar*e))+1/trustfrac*4*11/takeoffdis
    return val


def matchingDiagramconstraints(ar, dragpolar: list, betaLand, clMaxLand, approachSpeed, landLength, cruiseAltitude, cruiseMach, betaCruise, climbrate, climbAltitude, takeoffLength, takeoffCL):
    """DRAGPOLAR: ls[[cr],[cd],[tr],[td],[lr],[ld]]"""
    """Form: e(0), cd0(1)"""
    """cruise retracted(0)"""
    """cruise deployed(1)"""
    """takeoff retracted(2)"""
    """takeoff deployed(3)"""
    """landing retracted(4)"""
    """landing deployed(5)"""
    wingloading = [1, 10000]
    constraintNames = []

    stallspeed = StallSpeedconstraint(betaLand, clMaxLand, approachSpeed)


    landingfield = LandingFieldLengthConstraint(betaLand, landLength, clMaxLand)


    cruiseSpeed = []
    for i in range(wingloading[0], wingloading[1]):
        val = CruiseSpeedConstraint(i, dragpolar[0][1], ar, dragpolar[0][0], cruiseAltitude, cruiseMach, betaCruise)
        cruiseSpeed.append(val)
    
    cRate = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbrate(i, ar, dragpolar[0][0], dragpolar[0][1], climbrate, climbAltitude, betaCruise)
        cRate.append(val)
    
    Climbgradient1 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[5][0], dragpolar[5][1], 1, 1, 0.032)
        Climbgradient1.append(val)
    
    Climbgradient2 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[3][0], dragpolar[3][1], 1, 0.5, 0)
        Climbgradient2.append(val)
    
    Climbgradient3 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[2][0], dragpolar[2][1], 1, 0.5, 0.024)
        Climbgradient3.append(val)

    Climbgradient4 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[0][0], dragpolar[0][1], 1, 0.5, 0.012)
        Climbgradient4.append(val)
    
    Climbgradient5 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[4][0], dragpolar[4][1], betaLand, 0.5, 0.021)
        Climbgradient5.append(val)

    takeoff = []
    for i in range(wingloading[0], wingloading[1]):
        val = TakeOffFieldLengthConstraint(i, ar, dragpolar[3][0],0.5,takeoffLength, takeoffCL)
        takeoff.append(val)


    constraints = [stallspeed, landingfield, cruiseSpeed, cRate, Climbgradient1, Climbgradient2, Climbgradient3, Climbgradient4, Climbgradient5, takeoff]
    constraintNames.append("Minimum speed requirement")
    constraintNames.append("Landing distance requirement")
    constraintNames.append("Cruise speed requirement")
    constraintNames.append("Climb rate requirement")
    constraintNames.append("Climb gradient requirement CS 25.119")
    constraintNames.append("Climb gradient requirement CS 25.121a")
    constraintNames.append("Climb gradient requirement CS 25.121b")
    constraintNames.append("Climb gradient requirement CS 25.121c")
    constraintNames.append("Climb gradient requirement CS 25.121d")
    constraintNames.append("Take-off distance requirement")
    return constraints, constraintNames


def plotMatchingDiagram(ar, dragpolar, betaLand, clMaxLand, approachSpeed, landLength, cruiseAltitude, cruiseMach, betaCruise, climbrate, climbAltitude, takeoffLength, takeoffCL):
    constraints, constraintNames = matchingDiagramconstraints(ar, dragpolar, betaLand, clMaxLand, approachSpeed, landLength, cruiseAltitude, cruiseMach, betaCruise, climbrate, climbAltitude, takeoffLength, takeoffCL)

    
    plt.axis((0, 10000, 0, 1))
    for i,constraint in enumerate(constraints): 
        if i < 2:
            plt.axvline(constraint, label=constraintNames[i])
        else:
            plt.plot(constraint,label=constraintNames[i])
    plt.legend()
    plt.show()

if __name__ == "__main__":
    dragpolar = matchingFunctions.crudeDragpolar(0.8, 0.016,15,40)
    #print(dragpolar)
    plotMatchingDiagram(9.3, dragpolar, c.BETA_LAND, c.ULTIMATECL, c.VAPPROACH, c.LANDINGDISTANCE, c.CRUISEALTITUDE, c.CRUISEMACH, c.BETA_CRUISE, c.CLIMBRATE, c.CLIMBRATEALTITUDE, c.TAKEOFFDISTANCE, c.TAKEOFFCL)
    #print(Climbgradient(7000, 9.4, dragpolar[2][0], dragpolar[2][1], 1, 0.5, 0.024))