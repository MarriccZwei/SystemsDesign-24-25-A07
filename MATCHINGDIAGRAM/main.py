if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import numpy as np
import matchingFunctions
import ISAGEO as ISA
import matplotlib.pyplot as plt
from General import Constants as c
from ClassI import refAcData

G = 9.81

def ApproachSpeedconstraint(betaLand, clMaxLand, vApp, dT=0):
    rho = ISA.density(0, dT)
    val = 1/betaLand*rho/2*(vApp/1.23)**2*clMaxLand
    return val

def LandingFieldLengthConstraint(betaLand, landingfieldlength, landingfieldAltitude, clMaxLand, dT=0):
    rho = ISA.density(landingfieldAltitude, dT)
    val = 1/betaLand*landingfieldlength/0.45*rho/2*clMaxLand
    return val

def CruiseSpeedConstraint(WSaxis, cd0, ar, e, cruisalt, cruisemach, betacruise, bypass, dT=0):
    alphaT = matchingFunctions.thrustLapse(cruisalt, cruisemach, bypass, dT)
    rho = ISA.density(cruisalt, dT)
    v = cruisemach*ISA.speedOfSound(cruisalt, dT)
    val = betacruise/alphaT*((cd0*0.5*rho*v**2)/(betacruise*WSaxis)+(betacruise*WSaxis)/(np.pi*ar*e*0.5*rho*v**2))
    return val

def Climbrate(WSaxis, ar, e, cd0, c, rateAlt, betaCruise, bypass, dT=0):
    rho = ISA.density(rateAlt, dT)
    Cl = np.sqrt(cd0*np.pi*ar*e)
    v = np.sqrt(betaCruise*WSaxis*2/rho*1/Cl)
    m = v/ISA.speedOfSound(rateAlt)
    alphaT = matchingFunctions.thrustLapse(rateAlt, m, bypass, dT)
    val = betaCruise/alphaT*(np.sqrt(c**2/(betaCruise*WSaxis)*rho/2*Cl)+2*np.sqrt(cd0/(np.pi*ar*e)))
    return val

def Climbgradient(WSaxis, ar, e, cd0, beta, trustFrac, grad, bypass, dT=0):
    rho = ISA.density(0, dT)
    Cl = (cd0*np.pi*ar*e)**0.5
    v = (beta*WSaxis*2/rho*1/Cl)**0.5
    m = v/ISA.speedOfSound(0, dT)
    alphaT=matchingFunctions.thrustLapse(0,m,bypass,dT)
    val = 1/trustFrac*beta/alphaT*(grad+2*(cd0/(np.pi*ar*e))**0.5)
    return val

def TakeOffFieldLengthConstraint(WSaxis, ar, e, trustfrac, takeoffdis, takeoffCL, takeoffAltitude, bypass, dT=0):
    cl2 = (1/1.13)**2*takeoffCL
    rho = ISA.density(takeoffAltitude, dT)
    v2 = np.sqrt(WSaxis*2/rho*1/cl2)
    m = v2/ISA.speedOfSound(0, dT)
    alphaT=matchingFunctions.thrustLapse(0,m, bypass, dT)
    val = 1.15*alphaT*np.sqrt(1/trustfrac*WSaxis/(takeoffdis*0.85*rho*G*np.pi*ar*e))+1/trustfrac*4*11/takeoffdis
    return val


def matchingDiagramconstraints(ar, dragpolar: list, betaLand, clMaxLand, approachSpeed, landLength, cruiseAltitude, cruiseMach, betaCruise, climbrate, climbAltitude, 
                               takeoffLength, takeoffCL, bypass, landingAltitude ,takeoffAltitude,dT = 0):
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

    stallspeed = ApproachSpeedconstraint(betaLand, clMaxLand, approachSpeed)


    landingfield = LandingFieldLengthConstraint(betaLand, landLength, landingAltitude, clMaxLand, dT)


    cruiseSpeed = []
    for i in range(wingloading[0], wingloading[1]):
        val = CruiseSpeedConstraint(i, dragpolar[0][1], ar, dragpolar[0][0], cruiseAltitude, cruiseMach, betaCruise, bypass)
        cruiseSpeed.append(val)
    
    cRate = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbrate(i, ar, dragpolar[0][0], dragpolar[0][1], climbrate, climbAltitude, betaCruise, bypass)
        cRate.append(val)
    
    # ClimbgradientTest = []
    # for i in range(wingloading[0], wingloading[1]):
    #     val = Climbgradient(i, ar, dragpolar[2][0], dragpolar[2][1], 1, 0.5, 0.024, bypass, dT)
    #     ClimbgradientTest.append(val)

    Climbgradient1 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[5][0], dragpolar[5][1], 1, 1, 0.032,bypass, dT)
        Climbgradient1.append(val)
    
    Climbgradient2 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[3][0], dragpolar[3][1], 1, 0.5, 0,bypass, dT)
        Climbgradient2.append(val)
    
    Climbgradient3 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[2][0], dragpolar[2][1], 1, 0.5, 0.024,bypass, dT)
        Climbgradient3.append(val)

    Climbgradient4 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[0][0], dragpolar[0][1], 1, 0.5, 0.012,bypass, dT)
        Climbgradient4.append(val)
    
    Climbgradient5 = []
    for i in range(wingloading[0], wingloading[1]):
        val = Climbgradient(i, ar, dragpolar[4][0], dragpolar[4][1], betaLand, 0.5, 0.021,bypass, dT)
        Climbgradient5.append(val)

    takeoff = []
    for i in range(wingloading[0], wingloading[1]):
        val = TakeOffFieldLengthConstraint(i, ar, dragpolar[3][0],0.5,takeoffLength, takeoffCL, takeoffAltitude, bypass, dT)
        takeoff.append(val)


    constraints = [stallspeed, landingfield, cruiseSpeed, cRate,Climbgradient1, Climbgradient2, Climbgradient3, Climbgradient4, Climbgradient5, takeoff]
    constraintNames.append("Minimum speed requirement")
    constraintNames.append("Landing distance requirement")
    constraintNames.append("Cruise speed requirement")
    constraintNames.append("Climb rate requirement")
    #constraintNames.append("Climb gradient test requirement")
    constraintNames.append("Climb gradient requirement CS 25.119")
    constraintNames.append("Climb gradient requirement CS 25.121a")
    constraintNames.append("Climb gradient requirement CS 25.121b")
    constraintNames.append("Climb gradient requirement CS 25.121c")
    constraintNames.append("Climb gradient requirement CS 25.121d")
    constraintNames.append("Take-off distance requirement")
    point = matchingFunctions.pointFinder(constraints)
    return constraints, constraintNames, point


def MatchingDiagram(ar, betaLand, betaCruise,takeoffCL,oswaldClean, cd0clean, plot):
    dragpolar = matchingFunctions.crudeDragpolar(oswaldClean, cd0clean, c.TODEFLECTION, c.LADEFELCTION, False)
    constraints, constraintNames, point = matchingDiagramconstraints(ar, dragpolar, betaLand, c.ULTIMATECL, c.VAPPROACH, c.LANDINGDISTANCE, c.CRUISEALTITUDE, c.CRUISEMACH, betaCruise, 
                                                                        c.CRUISEROC, c.CRUISEALTITUDE, c.TAKEOFFDISTANCE, takeoffCL, c.BYPASS, c.LANDINGALTITUDE,c.TAKEOFFALTITUDE)
    if plot:
        plt.axis((0, 10000, 0, 1))
        for i,constraint in enumerate(constraints): 
            if i < 2:
                plt.axvline(constraint, label=constraintNames[i])
            else:
                plt.plot(constraint,label=constraintNames[i])
        plt.plot(point[0], point[1], marker='o', markersize=10, color='red')

        loadingPointsList = refAcData.generateLoadingPoints()
        for i, point in enumerate(loadingPointsList):
            plt.plot(point[0], point[1], 'r+')
            plt.text(point[0] + 30, point[1] + 0.005, i+1) #Hard coded numbers are offset of labels.
        plt.xlabel("Wing Loading, [N/m^2]")
        plt.ylabel("Thrust-Weight Ratio, [-]")
        plt.legend()
        plt.show()
        return constraints, constraintNames, point
    else:
        return constraints, constraintNames, point



"""TESTCASE"""
#Vapp 68 - betaland 0.85 |||||| -> 5500 stallspeed
# 2.5 CLmaxland, dT 15, LF 1800 |||||| -> 5840 landingfield
# CD0 0.018, e 0.80, MCR 0.8, hcr 11000, beta 0.95, dT =0 Bypass 10 AR 8 ||||| 7000-> 0.29 Cruise Speed
# climbAlt = 11500 c=0.5 dT = 0 |||| 7000 -> 0.31 climb rate
# fuselage mounted flapTO 15 flapLA 35 CLTO 2.1 dT = 15 |||||| 7000 -> 0.29 climb gradient
# TOLENGTH 2500 altitude 1600 dT = 15 ||||| 7000 ->0.38 takeoff length

#LANDINGDISTANCE
#Takeoff


if __name__ == "__main__":
    #dragpolar = matchingFunctions.crudeDragpolar(0.8, 0.018,15,35, False)
    #print(dragpolar)
    #plotMatchingDiagram(8, dragpolar,0.85, 2.5, 68, 1800, 11000, 0.8, 0.95, 0.5, 11000, 2500, 2.1, 10, 1600, 1600, 15)
    #constraints, names = matchingDiagramconstraints(8, dragpolar,0.85, 2.5, 68, 1800, 11000, 0.8, 0.95, 0.5, 11000, 2500, 2.1, 10, 1600, 1600, 15)
    # for i,constraint in enumerate(constraints): 
    #     if i < 2:
    #         print(names[i]+f"has values of {constraint}")
    #     else:
    #         print(names[i]+f"at ws 7000 has value of {constraint[6999]}")
    
    #dragpolar = matchingFunctions.crudeDragpolar(0.8, 0.016, c.TODEFLECTION, c.LADEFELCTION, False)
    #constraints, names, point = matchingDiagramconstraints(9.87, dragpolar, c.BETA_LAND, c.ULTIMATECL, c.VAPPROACH, c.LANDINGDISTANCE, c.CRUISEALTITUDE, c.CRUISEMACH, c.BETA_CRUISE, 
                        #c.CRUISEROC, c.CRUISEALTITUDE, c.TAKEOFFDISTANCE, c.TAKEOFFCL, c.BYPASS, c.LANDINGALTITUDE,c.TAKEOFFALTITUDE)
    MatchingDiagram(9.87, c.BETA_LAND, c.BETA_CRUISE, c.TAKEOFFCL, 0.8, 0.016, True)
    # point = matchingFunctions.pointFinder(constraints)
    # print(point)

    #pointFinder.pointFinder(point[1], point[2], point[0]-100, point[0]+100)
    #WSselected, TWselected = pointFinder.pointFinder(constraints, crossOverEvents[-1][2], 0, crossOverEvents[-1][0]-100)