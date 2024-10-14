if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
from General import Constants
import json
import numpy as np
import thrustLapse
import ISA
import math
import Cd0_Oswald_Flaps
import ClimbRate
import pitchUpConstraint

inputData = json.load(open("input.json"))
CLmaxLand = inputData["CLMAXLAND"]

#TODO change these!!!!
betaCruise = 0.75
betaLand = 0.73

star = pitchUpConstraint.sweepTaperAspect(Constants.CRUISEMACH)
aspect = star[0]
taper = star[1]
sweep = star[2]

gee = 9.81

#here be the list of all constraint functions
constraints = []
constraintNames = []
vertConstraints = []

def StallSpeedconstraint(WSaxis): #here we need to start using the adsee book xd, just to demo a v line now
    return np.zeros(len(WSaxis))+7407.37, WSaxis
    #return np.zeros(len(WSaxis))+1/betaCruise*acparams.VSTALL**2*1.225/2*acparams.CLMAX, WSaxis

constraints.append(StallSpeedconstraint)
constraintNames.append("Minimum speed requirement")

'''Climb gradient calculations'''
def climb_gradient_general(WSaxis, nEngines, nEnginesInoper, massFraction, gradient, flapDefl, lgDefl): #do not append this one directly to constraints!!!
    Cd0, oswald = Cd0_Oswald_Flaps.Cd0_Oswald_flaps(flapDefl, acparams.OSWALD, acparams.CD_0, lgDefl)
    #the expression for T/W is divided into subterms, as it is quite a big one
    #the subterm names are arbitrary
    optCl = (Cd0*np.pi*aspect*oswald)**0.5
    speed = (WSaxis*2/Constants.LANDDENSITY/optCl)**0.5
    mach = speed/340
    situationFraction = nEngines*massFraction/(nEngines-nEnginesInoper)/thrustLapse.thrustLapseNP(0, mach)
    freeTerm = 2*(Cd0/np.pi/aspect/oswald)**0.5
    '''print(f"sf: {situationFraction}")
    print(f"ft: {freeTerm}")
    print(f"cd0: {Cd0}")
    print(f"pi: {np.pi}")
    print(f"asp: {aspect}")
    print(f"os: {oswald}")'''
    return WSaxis, np.zeros(len(WSaxis))+situationFraction*(gradient+freeTerm)

constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 0, 1, 0.032, 30, True))
constraintNames.append("Climb gradient requirement CS 25.119")
constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 1, 1, 0, 15, True))
constraintNames.append("Climb gradient requirement CS 25.121a")
constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 1, 1, 0.024, 15, False))
constraintNames.append("Climb gradient requirement CS 25.121b")
constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 1, 1, 0.012, 0, False))
constraintNames.append("Climb gradient requirement CS 25.121c")
constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 0, 0.92, 0.021, 30, True))
constraintNames.append("Climb gradient requirement CS 25.121d")

def TakeOffFieldLength(WSaxis):
    return WSaxis, np.zeros(len(WSaxis))+(1.15*thrustLapse.thrustLapse(0, 0)*np.sqrt(WSaxis/(Constants.TAKEOFFLENGTH*Constants.KT*Constants.LANDDENSITY*gee*np.pi*aspect*acparams.OSWALD)) + 44/Constants.TAKEOFFLENGTH)

constraints.append(TakeOffFieldLength)
constraintNames.append("Take-off distance requirement")

def LandingFieldLengthConstraint(WSaxis):
    return np.zeros(len(WSaxis))+((Constants.LANDLENGTH*Constants.LANDDENSITY*CLmaxLand)/(betaLand*Constants.CLFL*2)), WSaxis

constraints.append(LandingFieldLengthConstraint)
constraintNames.append("Landing distance requirement")

def CruiseSpeedConstraint(WSaxis):
    crmf = betaCruise
    cr_density = Constants.CRUISEDENSITY
    Vcr = math.sqrt(287*1.4*Constants.CRUISETEMPERATURE)*Constants.CRUISEMACH
    return WSaxis, (crmf/thrustLapse.thrustLapse(Constants.CRUISEALTITUDE,Constants.CRUISEMACH))*( (acparams.CD_0*0.5*cr_density*Vcr*Vcr)/(betaCruise*WSaxis) + (betaCruise*WSaxis)/(math.pi*aspect*0.5*acparams.OSWALD*cr_density*Vcr*Vcr) )

constraints.append(CruiseSpeedConstraint)
constraintNames.append("Cruise speed requirement")

constraints.append(ClimbRate.ClimbRate)
constraintNames.append("Rate of climb requirement")

if __name__ == "__main__":
    print(climb_gradient_general(np.linspace(0, 10000, 100), 2, 0, 1, 0.032, 3, True)) 